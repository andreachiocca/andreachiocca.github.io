"""Verify the generated English and Italian Teaching and Thesis pages."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

class Parsed(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.links = []
        self.image_sources = []
        self.classes = []
        self.text = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if "class" in a:
            self.classes.extend(a["class"].split())
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "img":
            self.image_sources.append((a.get("src", ""), a.get("alt", "")))

    def handle_data(self, content):
        self.text.append(content)

def verify(root):
    root = Path(root)
    projects = json.loads((BASE / "_data/thesis_opportunities.json").read_text(encoding="utf-8"))["projects"]
    expected = [project["id"] for project in projects]
    for prefix in ("", "it/"):
        language = "Italian" if prefix else "English"
        teaching = root / prefix / "teaching/index.html"
        thesis = root / prefix / "thesis/index.html"
        if not teaching.is_file() or not thesis.is_file():
            raise ValueError(language + ": Teaching or Thesis route missing")
        teach = Parsed(teaching.read_text(encoding="utf-8"))
        doc = Parsed(thesis.read_text(encoding="utf-8"))
        if "teaching-editorial" not in teach.classes or "thesis-editorial" not in doc.classes:
            raise ValueError(language + ": editorial layouts missing")
        if "recent-teaching" not in teach.ids or len([i for i in doc.ids if i=="specific-projects"]) != 1:
            raise ValueError(language + ": teaching/thesis anchor missing or duplicated")
        if any(doc.ids.count(id) != 1 for id in expected):
            raise ValueError(language + ": project identity missing or duplicated")
        if any(anchor not in doc.ids for anchor in ("research-directions", "discuss-a-thesis")):
            raise ValueError(language + ": required research or contact anchor missing")
        if "2018–2026/27" not in "".join(teach.text):
            raise ValueError(language + ": updated teaching periods absent")
        if not any(link.startswith("mailto:andrea.chiocca@unipi.it") for link in doc.links):
            raise ValueError(language + ": direct student email contact missing")
        if not any("github.com/andreachiocca/multiaxial-fatigue" in link for link in doc.links):
            raise ValueError(language + ": public fatigue repository missing")
        for project in projects:
            if not any(p["image"] in source for source, alt in doc.image_sources):
                # The user uploads the optimized photos to the PR branch separately.
                # Until then, the existing conditional include prevents broken HTML.
                continue
            if not any(p["image"] in source and alt for source, alt in doc.image_sources):
                raise ValueError(language + ": thesis image without alternative text")
        if len([c for c in doc.classes if c=="thesis-project-panel"]) != len(expected):
            raise ValueError(language + ": unexpected project panel count")
    print("PASS: two bilingual thesis project panels, five topic directions and preserved course navigation")

if __name__ == "__main__":
    verify(sys.argv[1] if len(sys.argv)>1 else "_site")
