"""Check that the static Cloudflare Pages preview is separate and non-indexable."""
import sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
origin = sys.argv[2].rstrip("/") if len(sys.argv) > 2 else None
if not origin or not origin.startswith("https://pr-") or not origin.endswith(".academic-website-preview.pages.dev"):
    raise SystemExit("FAIL: require the PR-specific preview origin")

class Tags(HTMLParser):
    def __init__(self, content):
        self.canonical = None
        self.robots = ""
        self.stylesheets = []
        self.lang = None
        super().__init__()
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "meta" and values.get("name") == "robots":
            self.robots = values.get("content", "")
        if tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href")
        if tag == "link" and values.get("rel") == "stylesheet":
            self.stylesheets.append(values.get("href", ""))

routes = ["/", "/it/", "/publications/", "/it/publications/",
          "/research/", "/it/research/", "/repositories/", "/it/repositories/"]
for route in routes:
    path = root / route.lstrip("/") / "index.html"
    if not path.is_file():
        raise SystemExit("FAIL: missing page " + str(path))
    doc = Tags(path.read_text(encoding="utf8"))
    if doc.canonical != origin + route:
        raise SystemExit(f"FAIL: incorrect canonical for {route}: {doc.canonical}")
    if "noindex" not in doc.robots or "nofollow" not in doc.robots:
        raise SystemExit("FAIL: missing noindex meta tag on " + route)
    if not any("/assets/css/main.css" in value for value in doc.stylesheets):
        raise SystemExit("FAIL: main stylesheet absent on " + route)
    if doc.lang != ("it" if route.startswith("/it/") else "en"):
        raise SystemExit("FAIL: incorrect language on " + route)

headers = (root / "_headers").read_text(encoding="utf8")
if "/*" not in headers or "X-Robots-Tag: noindex" not in headers:
    raise SystemExit("FAIL: Cloudflare _headers noindex policy absent")
robots = (root / "robots.txt").read_text(encoding="utf8")
if "Disallow: /" in robots or "andreachiocca.github.io" in robots:
    raise SystemExit("FAIL: incorrect preview robots.txt")
if not (root / "assets/css/main.css").is_file():
    raise SystemExit("FAIL: generated stylesheet absent")

print(f"PASS: 8 English/Italian preview routes, PR-specific canonicals, noindex metadata and Cloudflare headers ({origin})")
