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
             "teaching/index.html", "cv/index.html"):
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
        if not re.fullmatch(r"10\.\d{4,9}/\S+", str(paper.get("identifier", "")), re.I):
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

if errors:
    for error in sorted(set(errors)):
        print("ERROR:", error)
    sys.exit(1)
print(f"PASS: {len(pages)} HTML pages, {checked} local references, core metadata, publication JSON-LD and sitemap")
