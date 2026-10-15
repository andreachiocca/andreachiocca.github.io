"""Check generated academic pages without additional Python packages."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
ORIGIN = "https://andreachiocca.github.io"
errors = []


class Page(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.schemas = []
        self.json_buffer = None
        self.lang = None
        self.main = 0
        self.h1 = 0
        self.title = False
        self.description = False
        self.canonical = False
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.description = bool(attrs.get("content", "").strip())
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href", "").startswith(ORIGIN)
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.json_buffer = ""
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])
        if attrs.get("srcset"):
            self.links.extend(value.strip().split()[0] for value in attrs["srcset"].split(","))

    def handle_data(self, value):
        if self.json_buffer is not None:
            self.json_buffer += value

    def handle_endtag(self, tag):
        if tag == "script" and self.json_buffer is not None:
            try:
                self.schemas.append(json.loads(self.json_buffer))
            except json.JSONDecodeError as exc:
                errors.append("Invalid JSON-LD: " + str(exc))
            self.json_buffer = None


pages = {}
for path in ROOT.rglob("*.html"):
    if path.relative_to(ROOT).parts[0] == "assets":
        continue
    pages[path] = Page(path.read_text(encoding="utf-8"))

for name in ("index.html", "publications/index.html", "research/index.html",
             "teaching/index.html", "cv/index.html", "repositories/index.html"):
    path = ROOT / name
    if path not in pages:
        errors.append("Missing core page: " + name)
        continue
    page = pages[path]
    if page.lang != "en" or page.main != 1 or page.h1 != 1:
        errors.append("Expected English language, one main landmark and one H1: " + name)
    if not (page.title and page.description and page.canonical and page.schemas):
        errors.append("Missing page metadata: " + name)

checked = 0
for path, page in pages.items():
    page_url = ORIGIN + "/" + path.relative_to(ROOT).as_posix()
    for link in page.links:
        url = urlsplit(urljoin(page_url, link))
        if url.scheme not in ("https", "http") or url.netloc != urlsplit(ORIGIN).netloc:
            continue
        target = ROOT / unquote(url.path).lstrip("/")
        if target.is_dir():
            target /= "index.html"
        checked += 1
        if not target.is_file():
            errors.append(str(path.relative_to(ROOT)) + ": missing local target " + link)
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(str(path.relative_to(ROOT)) + ": missing local anchor " + link)

publication_page = pages.get(ROOT / "publications/index.html")
if publication_page:
    papers = [item for item in publication_page.schemas
              if item.get("@type") in ("ScholarlyArticle", "Thesis", "CreativeWork")]
    source = Path("_bibliography/PersonalPub.bib").read_text(encoding="utf-8")
    expected = len(re.findall(r"^@\w+\s*\{", source, re.M))
    if len(papers) != expected:
        errors.append("Expected one structured record per bibliography entry")
    for paper in papers:
        if not paper.get("name") or not paper.get("author"):
            errors.append("Publication missing title or author")
        if paper.get("identifier") and not re.fullmatch(r"10\.\d{4,9}/\S+", str(paper["identifier"]), re.I):
            errors.append("Missing or malformed publication DOI")

try:
    sitemap = ET.parse(ROOT / "sitemap.xml")
    locations = [node.text for node in sitemap.findall(".//{*}loc")]
    for required in ("/research/", "/publications/", "/teaching/", "/cv/"):
        if ORIGIN + required not in locations:
            errors.append("Sitemap missing " + required)
    if any("/people/" in loc or "/readme_preview/" in loc for loc in locations):
        errors.append("Sitemap contains theme demo content")
except (OSError, ET.ParseError) as exc:
    errors.append("Invalid sitemap: " + str(exc))

for path in ROOT.rglob("*.html"):
    if "polyfill.io/" in path.read_text(encoding="utf-8"):
        errors.append("Unsafe polyfill script reference remains: " + str(path.relative_to(ROOT)))


outputs = json.loads(Path("_data/research_outputs.json").read_text(encoding="utf-8"))
required = {"multiaxial-fatigue", "zenodo-21875885", "zenodo-21534682", "zenodo-18416255", "zenodo-14198237", "zenodo-12721131"}
output_page = pages.get(ROOT / "repositories/index.html")
if not output_page or not required.issubset(output_page.ids):
    errors.append("Requested scientific resources are missing from the generated output catalogue")
from sync_research_outputs import validate_catalogue
catalogue_status = json.loads(Path("_data/catalogue_status.json").read_text(encoding="utf8"))
try:
    validate_catalogue(outputs, catalogue_status["github_full_names"], catalogue_status["zenodo_record_ids"])
except ValueError as exc:
    errors.append(str(exc))
if output_page:
    expected_ids = {item["id"] for item in outputs}
    if not expected_ids.issubset(output_page.ids):
        errors.append("A catalogue card is absent from the generated page")
    expected_urls = {"https://github.com/" + name for name in catalogue_status["github_full_names"]}
    expected_urls.update("https://zenodo.org/records/" + record_id for record_id in catalogue_status["zenodo_record_ids"])
    if not expected_urls.issubset(set(output_page.links)):
        errors.append("A discovered repository or Zenodo version link is missing")
    catalogue_html = (ROOT / "repositories/index.html").read_text(encoding="utf8")
    if any(service in catalogue_html for service in ("github-readme-stats", "github-profile-trophy", "<iframe", "<img")):
        errors.append("The catalogue still depends on image previews or embeds")

restricted = next(item for item in outputs if item["id"] == "zenodo-21875885")
if restricted["access_right"] != "restricted":
    errors.append("Restricted Zenodo record is incorrectly classified")
if not errors:
    from check_browser import check_browser
    errors.extend(check_browser(ROOT))

if errors:
    for error in sorted(set(errors)):
        print("ERROR:", error)
    sys.exit(1)
print(f"PASS: {len(pages)} HTML pages, {checked} local references, core metadata, publication JSON-LD and sitemap")
