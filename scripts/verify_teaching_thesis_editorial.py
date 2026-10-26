"""Validate generated bilingual Teaching/Thesis pages and reject printed HTML source."""
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
        self.code_level = 0
        self.code_text = []
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
        if tag in ("code", "pre"):
            self.code_level += 1

    def handle_endtag(self, tag):
        if tag in ("code", "pre"):
            self.code_level = max(0, self.code_level - 1)

    def handle_data(self, content):
        self.text.append(content)
        if self.code_level:
            self.code_text.append(content)

def verify(root):
    root = Path(root)
    projects = json.loads((BASE / "_data/thesis_opportunities.json").read_text(encoding="utf-8"))["projects"]
    ids = [project["id"] for project in projects]
    if len(ids) != 3 or len(ids) != len(set(ids)):
        raise ValueError("Expected three distinct thesis projects")
    for folder in ("", "it/"):
        locale = "Italian" if folder else "English"
        teaching = root / folder / "teaching/index.html"
        thesis = root / folder / "thesis/index.html"
        if not teaching.is_file() or not thesis.is_file():
            raise ValueError(locale + ": Teaching/Thesis page missing")
        teach = Parsed(teaching.read_text(encoding="utf-8"))
        doc = Parsed(thesis.read_text(encoding="utf-8"))
        for cls in ("teaching-editorial-hero",):
            if cls not in teach.classes:
                raise ValueError(locale + ": missing Teaching editorial hero")
        if "thesis-editorial-banner" not in doc.classes:
            raise ValueError(locale + ": missing thesis conceptual illustration")
        if any(term in "".join(teach.code_text) for term in ("editorial-index", "teaching-editorial-links", "teaching-editorial-title", "<p class=")):
            raise ValueError(locale + ": HTML rendered as code in Teaching page")
        if any(term in "".join(doc.code_text) for term in ("thesis-editorial-banner", "thesis-project-panel", "<section class=")):
            raise ValueError(locale + ": HTML rendered as code in Thesis page")
        if "recent-teaching" not in teach.ids or "2018–2026/27" not in "".join(teach.text):
            raise ValueError(locale + ": current teaching section or dates missing")
        for anchor in ("specific-projects", "research-directions", "discuss-a-thesis"):
            if doc.ids.count(anchor) != 1:
                raise ValueError(locale + ": duplicated or missing thesis anchor " + anchor)
        if len([cls for cls in doc.classes if cls == "thesis-project-panel"]) != 3:
            raise ValueError(locale + ": incorrect thesis project panel count")
        for project in projects:
            if doc.ids.count(project["id"]) != 1:
                raise ValueError(locale + ": missing thesis project " + project["id"])
            photo = project["image"]
            if not (root / photo.lstrip("/")).is_file():
                raise ValueError(locale + ": generated thesis photo absent " + photo)
            if not any(photo in source and alt for source, alt in doc.image_sources):
                raise ValueError(locale + ": thesis photo not rendered with alt text " + photo)
            for paper in project["related_papers"]:
                if not any(paper["doi"] in href for href in doc.links):
                    raise ValueError(locale + ": missing publication DOI " + paper["doi"])
        if not any("lattice-thermal-imaging-original.png" in href for href in doc.links):
            raise ValueError(locale + ": original thermal PNG link absent")
        if not any("github.com/andreachiocca/multiaxial-fatigue" in href for href in doc.links):
            raise ValueError(locale + ": multiaxial repository link absent")
        if not any(href.startswith("mailto:andrea.chiocca@unipi.it") for href in doc.links):
            raise ValueError(locale + ": student email contact absent")
    print("PASS: safe Teaching HTML and 3 bilingual thesis projects with images, references and direct contact")

if __name__ == "__main__":
    verify(sys.argv[1] if len(sys.argv) > 1 else "_site")
