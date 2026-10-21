"""Check generated English and Italian Research Atlas HTML against canonical records.

This is deliberately scoped to Research; verify_site.py and
verify_languages.py continue to own global metadata and link validation.
"""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    "multiaxial-fatigue-and-critical-plane-methods": "Candidate-plane traction schematic",
    "residual-stresses-and-welded-structures": "Welded-joint geometry schematic",
    "additive-manufacturing-and-material-behaviour": "Layered structure schematic",
    "component-testing-and-industrial-applications": "Axial specimen loading schematic",
}


class ResearchPage(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.main_count = 0
        self.h1_count = 0
        self.ids = []
        self.links = []
        self.chapters = []
        self.chapter = None
        self.figure = None
        self.caption = False
        self.details_depth = 0
        self.previous_projects = False
        self.project = False
        self.faber_fragments = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = set(a.get("class", "").split())
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "section" and "research-chapter" in classes:
            self.chapter = {"heading": None, "visible": [], "further": [],
                            "details": 0, "figures": []}
            self.chapters.append(self.chapter)
        elif tag == "h2" and self.chapter is not None and a.get("id"):
            self.chapter["heading"] = a["id"]
        elif tag == "figure" and "research-technical-figure" in classes and self.chapter is not None:
            self.figure = {"label": a.get("aria-label", ""), "caption": "", "svgs": 0}
            self.chapter["figures"].append(self.figure)
        elif tag == "svg" and self.figure is not None:
            self.figure["svgs"] += 1
        elif tag == "figcaption" and self.figure is not None:
            self.caption = True
        elif tag == "details":
            self.details_depth += 1
            if self.chapter is not None:
                self.chapter["details"] += 1
            if "previous-projects" in classes:
                self.previous_projects = True
        elif tag == "article" and a.get("data-project") == "faber":
            self.project = True
        elif tag == "a":
            href = a.get("href", "")
            self.links.append(href)
            if self.chapter is not None:
                self.chapter["further" if self.details_depth else "visible"].append(href)

    def handle_data(self, data):
        if self.caption and self.figure is not None:
            self.figure["caption"] += data
        if self.project:
            self.faber_fragments.append(data)

    def handle_endtag(self, tag):
        if tag == "figcaption":
            self.caption = False
        elif tag == "figure":
            self.figure = None
        elif tag == "details":
            self.details_depth = max(0, self.details_depth - 1)
        elif tag == "article":
            self.project = False
        elif tag == "section" and self.chapter is not None:
            self.chapter = None


def verify_research_atlas(root: Path) -> None:
    areas = json.loads((ROOT / "_data/research_areas.json").read_text(encoding="utf8"))
    expected_ids = [item["id"] for item in areas]
    translations = {
        lang: json.loads((ROOT / f"_data/i18n/{lang}/ui.json").read_text(encoding="utf8"))
        for lang in ("en", "it")
    }
    errors = []
    anchors = ("research-areas", "projects", "selected-collaborative-projects",
               "international-collaborations", "research-environment")
    for lang, prefix in (("en", ""), ("it", "it/")):
        path = root / prefix / "research/index.html"
        if not path.is_file():
            errors.append(f"{lang}: missing Research HTML at {path}")
            continue
        page = ResearchPage(path.read_text(encoding="utf8"))
        if page.lang != lang or page.main_count != 1 or page.h1_count != 1:
            errors.append(f"{lang}: Research language, main or h1 structure invalid")
        for anchor in anchors:
            if page.ids.count(anchor) != 1:
                errors.append(f"{lang}: Research anchor '{anchor}' missing or duplicated")
        actual = [chapter["heading"] for chapter in page.chapters]
        if actual != expected_ids:
            errors.append(f"{lang}: Research area IDs or order changed: {actual}")
        if not page.previous_projects:
            errors.append(f"{lang}: previous research projects disclosure missing")
        faber = " ".join(page.faber_fragments)
        expected_roles = ("WG3", "Co-Leader", "WG4.3", "WG5.3",
                          "Participant" if lang == "en" else "Partecipante")
        if any(role not in faber for role in expected_roles):
            errors.append(f"{lang}: FABER group memberships or verified roles missing")
        for index, area in enumerate(areas):
            if index >= len(page.chapters):
                break
            chapter = page.chapters[index]
            if chapter["heading"] != area["id"]:
                continue
            if chapter["details"] != 1:
                errors.append(f"{lang}: research chapter '{area['id']}' disclosure missing")
            if len(chapter["figures"]) != 1:
                errors.append(f"{lang}: research chapter '{area['id']}' requires one labelled figure")
            else:
                figure = chapter["figures"][0]
                label = translations[lang][LABELS[area["id"]]]
                if figure["svgs"] != 1 or label not in figure["caption"] or label != figure["label"]:
                    errors.append(f"{lang}: research figure label/SVG invalid for {area['id']}")
            for group, destination in (("visible", area["links"]), ("further", area["further"])):
                found = chapter[group]
                for link in destination:
                    expected = ("/it" if lang == "it" and link["url"].startswith("/") else "") + link["url"]
                    if expected not in found:
                        errors.append(f"{lang}: missing {group} research link '{expected}' in {area['id']}")
        for target in ("#research-areas", "#projects", "#international-collaborations"):
            if target not in page.links:
                errors.append(f"{lang}: research navigation link {target} missing")
    if errors:
        raise ValueError("Research Atlas verification failed:\n" + "\n".join(errors))
    print("PASS: four canonical Research chapters, diagrams, links, FABER roles and EN/IT anchors")


if __name__ == "__main__":
    try:
        verify_research_atlas(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
    except (ValueError, FileNotFoundError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
