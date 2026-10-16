"""Refresh a reviewable, offline Jekyll catalogue using only Python's standard library.

Run without arguments to report discovery; --write updates the checked-in snapshot.
Remote errors or incomplete searches abort before any existing file is replaced.
Curated descriptions, classifications and stable anchors survive metadata refreshes.
"""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ACCOUNTS = ("achiocca1", "andreachiocca")
ORCID = "0000-0002-1472-4398"
ZENODO_OWNER = "275783"  # Owner of the explicitly supplied deposits, verified by ORCID.
REQUIRED_RECORDS = {21875885, 21534682, 18416255, 14198237, 12721131}
EXCLUDED_REPOSITORIES = frozenset(name.casefold() for name in json.loads((ROOT / '_data/catalogue_exclusions.json').read_text(encoding='utf8')))


def excluded_repository(name):
    return (name or '').casefold() in EXCLUDED_REPOSITORIES


def included_entry(entry):
    name = entry.get('github_full_name') or entry.get('url', '').removeprefix('https://github.com/')
    return not excluded_repository(name)


def fetch(url):
    headers = {"User-Agent": "AndreaChioccaPortfolioCatalogue/1.0", "Accept": "application/json"}
    # Optional token is sent only to the GitHub API, never to Zenodo or the browser.
    if urlsplit(url).netloc == "api.github.com" and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=40) as response:
                return json.load(response)
        except HTTPError as exc:
            delay = exc.headers.get("Retry-After", "2")
            delay = int(delay) if delay.isdigit() else 2
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2 or delay > 10:
                raise
            time.sleep(max(1, delay))


def github_repositories(account):
    records, page = [], 1
    while True:
        batch = fetch(f"https://api.github.com/users/{account}/repos?per_page=100&page={page}&type=owner&sort=full_name")
        if not isinstance(batch, list):
            raise ValueError("Unexpected GitHub repository response")
        records.extend(batch)
        if len(batch) < 100:
            return records
        page += 1


def zenodo_search(query):
    url = "https://zenodo.org/api/records?" + urlencode({"q": query, "size": 25, "all_versions": "true", "sort": "mostrecent"})
    records, seen = [], set()
    while url:
        if url in seen or urlsplit(url).netloc != "zenodo.org":
            raise ValueError("Unexpected Zenodo pagination link")
        seen.add(url)
        data = fetch(url)
        records.extend(data["hits"]["hits"])
        total = data["hits"]["total"]
        if isinstance(total, dict):
            if total.get("relation") != "eq":
                raise ValueError("Zenodo did not supply an exact search count")
            total = total["value"]
        url = data.get("links", {}).get("next")
    if len(records) != total:
        raise ValueError("Incomplete Zenodo search; retaining the existing catalogue")
    return records


def verified_deposit(record):
    owned = any(str(owner["id"]) == ZENODO_OWNER for owner in record.get("owners", []))
    for creator in record["metadata"].get("creators", []):
        orcid = (creator.get("orcid") or "").removeprefix("https://orcid.org/")
        if orcid == ORCID:
            return True
        name = " ".join(creator.get("name", "").casefold().split())
        if not orcid and owned and name in ("chiocca, andrea", "andrea chiocca"):
            return True
    return False


def group_versions(records):
    groups = {}
    for record in records:
        groups.setdefault(str(record.get("conceptrecid") or record["id"]), []).append(record)
    for versions in groups.values():
        # Zenodo's version index is authoritative when available; date/id break ties.
        versions.sort(key=lambda r: ((r.get("relations", {}).get("version") or [{}])[0].get("index", -1), r["metadata"]["publication_date"], int(r["id"])), reverse=True)
    return groups


def plain_description(value):
    text = unescape(re.sub(r"<[^>]+>", " ", value or ""))
    text = " ".join(text.split())
    if len(text) > 450:
        text = text[:447].rsplit(" ", 1)[0] + "â€¦"
    return text or "Public research record. Consult the landing page for scope and contents."


def zenodo_entry(versions, existing=None):
    record = versions[0]
    metadata = record["metadata"]
    entry = deepcopy(existing or {})
    entry.setdefault("id", "zenodo-" + str(record["id"]))
    kind = "software" if metadata["resource_type"]["type"] == "software" else "data" if metadata["resource_type"]["type"] == "dataset" else "other"
    entry.setdefault("kind", kind)
    entry.setdefault("type_label", metadata["resource_type"].get("title", "Research output"))
    entry.setdefault("schema_type", "SoftwareSourceCode" if kind == "software" else "Dataset" if kind == "data" else "CreativeWork")
    entry.setdefault("description", plain_description(metadata.get("description")))
    if existing is None:
        entry["needs_review"] = True
    entry.update({"title": metadata["title"], "source": "Zenodo", "zenodo_concept_id": str(record.get("conceptrecid") or record["id"]),
                  "zenodo_record_id": str(record["id"]), "concept_doi": record.get("conceptdoi"),
                  "url": "https://zenodo.org/records/" + str(record["id"]), "doi": metadata["doi"],
                  "creators": [creator["name"] for creator in metadata.get("creators", [])],
                  "date": metadata["publication_date"], "year": metadata["publication_date"][:4],
                  "registry_type": metadata["resource_type"].get("title", "Research output"),
                  "access_right": metadata["access_right"],
                  "access_label": {"open": "Open files", "restricted": "Restricted files", "closed": "Closed files", "embargoed": "Embargoed files"}.get(metadata["access_right"], "Consult record for access")})
    entry.pop("version", None)
    if metadata.get("version"):
        entry["version"] = metadata["version"]
    entry["earlier_versions"] = [{"record_id": str(r["id"]), "version": r["metadata"].get("version") or r["metadata"]["publication_date"],
                                  "doi": r["metadata"]["doi"], "url": "https://zenodo.org/records/" + str(r["id"])} for r in versions[1:]]
    return entry


def github_entry(repo, existing=None):
    entry = deepcopy(existing or {})
    name = repo["full_name"]
    detail = fetch("https://api.github.com/repos/" + name) if repo["fork"] else repo
    commits = fetch("https://api.github.com/repos/" + name + "/commits?per_page=1") if repo["size"] else []
    entry.setdefault("id", "github-" + name.replace("/", "-"))
    entry.setdefault("kind", "other" if repo["fork"] or name.endswith(".github.io") else "software")
    entry.setdefault("schema_type", "SoftwareSourceCode")
    entry.setdefault("type_label", "Fork" if repo["fork"] else "Website" if name.endswith(".github.io") else "Software")
    entry.setdefault("description", repo.get("description") or "Public repository. Consult the README for scope and usage.")
    entry.setdefault("creators", [])
    if existing is None:
        entry["needs_review"] = True
    entry.update({"title": entry.get("title") or repo["name"], "github_name": repo["name"], "github_full_name": name,
                  "source": "GitHub", "github_url": repo["html_url"], "url": repo["html_url"],
                  "language": repo.get("language"), "fork": repo["fork"], "archived": repo["archived"], "mirror_url": repo.get("mirror_url"),
                  "last_code_update": commits[0]["commit"]["committer"]["date"][:10] if commits else None})
    if detail.get("parent"):
        entry["upstream_url"] = detail["parent"]["html_url"]
    return entry


def validate_catalogue(entries, github_names, zenodo_ids):
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate catalogue anchors")
    listed_github = [entry["github_full_name"] for entry in entries if entry.get("github_full_name")]
    expected = {name for name in github_names if not excluded_repository(name)}
    if any(excluded_repository(name) for name in listed_github):
        raise ValueError("An explicitly excluded GitHub repository is advertised")
    if len(listed_github) != len(set(listed_github)) or not expected.issubset(listed_github):
        raise ValueError("Missing or duplicate public GitHub repositories")
    listed_zenodo = [str(entry["zenodo_record_id"]) for entry in entries if entry.get("zenodo_record_id")]
    listed_zenodo += [str(version["record_id"]) for entry in entries for version in entry.get("earlier_versions", [])]
    if len(listed_zenodo) != len(set(listed_zenodo)) or not set(map(str, zenodo_ids)).issubset(listed_zenodo):
        raise ValueError("Missing or duplicate Zenodo versions")
    for entry in entries:
        if not all(entry.get(key) for key in ("id", "title", "description", "url", "kind")):
            raise ValueError("Incomplete catalogue entry")
        if entry["kind"] not in ("software", "data", "benchmark", "other"):
            raise ValueError("Unknown resource category")


def build_catalogue(existing):
    existing = [item for item in existing if included_entry(item)]
    repos = [repo for account in ACCOUNTS for repo in github_repositories(account)]
    candidates = {}
    for query in (f'creators.orcid:"{ORCID}"', "creators.name:Chiocca", "owners:" + ZENODO_OWNER):
        candidates.update({str(r["id"]): r for r in zenodo_search(query)})
    verified = [record for record in candidates.values() if verified_deposit(record)]
    if not REQUIRED_RECORDS.issubset({int(record["id"]) for record in verified}):
        raise ValueError("A required Zenodo record was not discovered and identity-verified")
    # Match existing records by URL on the first refresh, then by stable concept ID.
    repo_map = {item.get("github_full_name") or item["url"].removeprefix("https://github.com/"): item for item in existing if item.get("github_full_name") or item["url"].startswith("https://github.com/")}
    groups = group_versions(verified)
    used = set()
    entries = []
    for repo in repos:
        if excluded_repository(repo['full_name']):
            continue
        original = repo_map.get(repo["full_name"])
        if original:
            used.add(original["id"])
        entries.append(github_entry(repo, original))
    for concept, versions in groups.items():
        urls = {"https://zenodo.org/records/" + str(r["id"]) for r in versions}
        original = next((item for item in existing if item.get("zenodo_concept_id") == concept or item["url"] in urls), None)
        if original:
            used.add(original["id"])
        refreshed = zenodo_entry(versions, original)
        # A manually verified software/archive equivalence stays one card.
        combined = next((item for item in entries if item["id"] == refreshed["id"]), None)
        if combined is not None:
            combined.update(refreshed)
        else:
            entries.append(refreshed)
    # Never silently delete older records, privately moved repos, or other archives.
    entries.extend(deepcopy(item) for item in existing if item["id"] not in used and item["url"] not in {entry["url"] for entry in entries})
    entries.sort(key=lambda item: (item.get("featured", False), item.get("last_code_update") or item.get("date") or item.get("year", ""), item["title"].casefold()), reverse=True)
    names = sorted(repo["full_name"] for repo in repos)
    record_ids = sorted(str(record["id"]) for record in verified)
    validate_catalogue(entries, names, record_ids)
    status = {"verified_on": datetime.now(timezone.utc).date().isoformat(), "github_accounts": list(ACCOUNTS), "github_full_names": names,
              "github_repositories": len(repos), "github_repositories_included": len([name for name in names if not excluded_repository(name)]),
              "excluded_github_full_names": [name for name in names if excluded_repository(name)],
              "zenodo_record_ids": record_ids, "zenodo_records": len(verified), "zenodo_resources": len(groups),
              "excluded_zenodo_ids": sorted(set(candidates) - set(record_ids)), "total_cards": len(entries)}
    return entries, status


def refresh(target, status_target=None, write=True):
    existing = json.loads(target.read_text(encoding="utf8"))
    entries, status = build_catalogue(existing)  # All remote work and validation precedes writes.
    if write:
        staged = target.with_suffix(".json.tmp")
        staged.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n")
        staged.replace(target)
        if status_target:
            status_target.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf8", newline="\n")
    return entries, status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Update the checked-in catalogue after complete discovery; review the diff before committing")
    args = parser.parse_args()
    try:
        entries, status = refresh(ROOT / "_data/research_outputs.json", ROOT / "_data/catalogue_status.json", write=args.write)
        print(json.dumps(status, indent=2))
        print("Review descriptions of new resources:", [item["id"] for item in entries if item.get("needs_review")])
        print("Snapshot updated; review the diff." if args.write else "Discovery only; snapshot unchanged. Use --write to refresh.")
    except (OSError, ValueError, KeyError) as exc:
        print("Refresh failed; the existing catalogue was retained:", exc, file=sys.stderr)
        sys.exit(1)
