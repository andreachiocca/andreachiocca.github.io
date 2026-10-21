"""Verify the rendered Publications Atlas against the canonical BibTeX source."""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


SECTIONS = {
    "article": "journal-articles",
    "inproceedings": "conference-contributions",
    "phdthesis": "doctoral-thesis",
}


def bibliography_records(path):
    text = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^@(article|inproceedings|phdthesis)\s*\{\s*([^,]+),", text))
    records = {}
    for index, match in enumerate(matches):
        block = text[match.end():matches[index + 1].start() if index + 1 < len(matches) else len(text)]
        doi = re.search(r"(?m)^\s*doi\s*=\s*\{([^}]+)\}", block)
        key = match.group(2).strip()
        if key in records:
            raise AssertionError("Duplicate BibTeX key: " + key)
        records[key] = (match.group(1), doi.group(1).strip() if doi else None)
    if not records:
        raise AssertionError("No supported BibTeX records found")
    return records


class PublicationsPage(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.main = 0
        self.h1 = 0
        self.atlas = 0
        self.ids = set()
        self.index_links = set()
        self.buttons = set()
        self.controls_hidden = False
        self.records = {}
        self.keyword_ids = set()
        self.doi_links = set()
        self.links = set()
        self.section = None
        self.in_bibliography = False
        self.in_entry = False
        self.in_index = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set(a.get("class", "").split())
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        if "publication-atlas" in classes:
            self.atlas += 1
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "nav" and "publication-index" in classes:
            self.in_index = True
        if tag == "section" and "publication-section" in classes:
            self.section = a.get("data-publication-type")
        if tag == "ol" and "bibliography" in classes:
            self.in_bibliography = True
        if tag == "li" and self.in_bibliography:
            self.in_entry = True
        if self.in_entry and tag == "div" and a.get("id"):
            self.records[a["id"]] = self.section
            if "data-publication-keywords" in a:
                self.keyword_ids.add(a["id"])
        if tag == "div" and "publication-controls" in classes:
            self.controls_hidden = "hidden" in a
        if tag == "button" and a.get("data-publication-type"):
            self.buttons.add(a["data-publication-type"])
        if tag == "a" and a.get("href"):
            self.links.add(a["href"])
            if self.in_index:
                self.index_links.add(a["href"])
            if a["href"].startswith("https://doi.org/"):
                self.doi_links.add(a["href"])

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_index = False
        if tag == "li":
            self.in_entry = False
        if tag == "ol":
            self.in_bibliography = False
        if tag == "section":
            self.section = None


def verify_publications_atlas(root, bibliography=None):
    root = Path(root)
    bibliography = Path(bibliography or "_bibliography/PersonalPub.bib")
    expected = bibliography_records(bibliography)
    errors = []
    for lang, path in (("en", root / "publications/index.html"),
                       ("it", root / "it/publications/index.html")):
        if not path.is_file():
            errors.append(lang + ": missing Publications page")
            continue
        page = PublicationsPage(path.read_text(encoding="utf-8"))
        if (page.lang, page.main, page.h1, page.atlas) != (lang, 1, 1, 1):
            errors.append(lang + ": invalid language, landmark or title structure")
        if not set(SECTIONS.values()).issubset(page.ids):
            errors.append(lang + ": missing publication section anchor")
        if page.index_links != {"#" + anchor for anchor in SECTIONS.values()}:
            errors.append(lang + ": publication index destinations differ")
        catalogue_url = "/it/repositories/" if lang == "it" else "/repositories/"
        if catalogue_url not in page.links:
            errors.append(lang + ": research-output catalogue link is missing")
        if page.buttons != {"all", *SECTIONS} or not page.controls_hidden:
            errors.append(lang + ": progressive filter controls are incomplete")
        if set(page.records) != set(expected):
            errors.append(lang + ": publication keys differ from the canonical BibTeX source")
        if page.keyword_ids != set(expected):
            errors.append(lang + ": searchable keyword metadata is missing")
        for key, (kind, doi) in expected.items():
            if page.records.get(key) != kind:
                errors.append(lang + ": wrong publication type for " + key)
            if doi and "https://doi.org/" + doi not in page.doi_links:
                errors.append(lang + ": DOI link missing for " + key)
    if errors:
        raise AssertionError("; ".join(errors))
    print(f"PASS: {len(expected)} canonical publications, EN/IT sections, DOI links and progressive controls")


if __name__ == "__main__":
    try:
        verify_publications_atlas(sys.argv[1] if len(sys.argv) > 1 else "_site")
    except (AssertionError, OSError) as exc:
        print("ERROR:", exc)
        raise SystemExit(1)
