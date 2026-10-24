"""Verify the generated bilingual Outputs Atlas and canonical resource links."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


class AtlasDocument(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.lang = ""
        self.cards = []
        self.spotlights = []
        self.links = []
        self.ids = set()
        self.controls = {}
        self.script = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "")
        if a.get("id"):
            self.ids.add(a["id"])
            if a["id"] in ("output-search", "output-empty", "output-reset"):
                self.controls[a["id"]] = a
        if tag == "article":
            cls = a.get("class", "").split()
            if "research-output" in cls:
                self.cards.append(a.get("id"))
            if "output-atlas-feature" in cls:
                self.spotlights.append(a.get("data-spotlight-id"))
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "script" and a.get("src", "").split("?")[0].endswith("/assets/js/research_outputs.js"):
            self.script = True


def verify_outputs_atlas(root):
    root = Path(root)
    records = json.loads((PROJECT / "_data/research_outputs.json").read_text(encoding="utf8"))
    spotlight = json.loads((PROJECT / "_data/research_output_spotlight.json").read_text(encoding="utf8"))
    ids = [record["id"] for record in records]
    if len(ids) != len(set(ids)) or len(spotlight) != 4 or len(spotlight) != len(set(spotlight)):
        raise ValueError("Invalid canonical Outputs Atlas identifiers")
    for language, route in (("en", "repositories/index.html"), ("it", "it/repositories/index.html")):
        page = root / route
        if not page.is_file():
            raise ValueError(f"{language}: missing Outputs Atlas page")
        doc = AtlasDocument(page.read_text(encoding="utf8"))
        if doc.lang != language:
            raise ValueError(f"{language}: wrong HTML language {doc.lang}")
        if doc.cards != ids:
            raise ValueError(f"{language}: canonical catalogue records missing or out of order")
        if doc.spotlights != spotlight or any("#" + id not in doc.links for id in spotlight):
            raise ValueError(f"{language}: selected record links invalid")
        for anchor in ("selected-outputs", "complete-catalogue", "output-grid", "output-count"):
            if anchor not in doc.ids:
                raise ValueError(f"{language}: missing {anchor}")
        for control in ("output-search", "output-empty", "output-reset"):
            if control not in doc.controls or "hidden" not in doc.controls[control]:
                raise ValueError(f"{language}: {control} must be hidden without JavaScript")
        if not doc.script:
            raise ValueError(f"{language}: catalogue filter script missing")
    print(f"PASS: bilingual Outputs Atlas, {len(ids)} resources, {len(spotlight)} selected links and progressive controls")


if __name__ == "__main__":
    verify_outputs_atlas(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
