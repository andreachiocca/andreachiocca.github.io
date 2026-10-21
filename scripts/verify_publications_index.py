"""Post-build check for the bilingual static Publications index."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys

TYPES = ("article", "inproceedings", "phdthesis")
KEYS = ("all",) + TYPES


def canonical_entries():
    text = (Path(__file__).resolve().parents[1] / "_bibliography/PersonalPub.bib").read_text(encoding="utf8")
    matches = list(re.finditer(r"(?im)^@(article|inproceedings|phdthesis)\s*\{\s*([^,]+),", text))
    out = []
    for i, match in enumerate(matches):
        block = text[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
        def field(name):
            found = re.search(r"(?im)^\s*" + name + r"\s*=\s*[{ ]([^}\n]+)", block)
            return found.group(1).strip() if found else None
        out.append(dict(key=match.group(2).strip(), category=match.group(1).lower(),
                        year=field("year"), doi=field("doi"), pdf=field("pdf")))
    if not out or len({e["key"] for e in out}) != len(out):
        raise ValueError("Canonical BibTeX entries missing or duplicated")
    return out


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.landmarks = [0, 0]
        self.ids = set()
        self.sections = []
        self.section_stack = []
        self.ols = []
        self.year = None
        self.year_buf = None
        self.current = None
        self.li_depth = 0
        self.rows = []
        self.filters = []
        self.hidden = {}
        self.live = False
        self.schema_buf = None
        self.schemas = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if tag == "main": self.landmarks[0] += 1
        if tag == "h1": self.landmarks[1] += 1
        if a.get("id"):
            self.ids.add(a["id"])
            if a["id"] in ("bibsearch", "publication-type-filters", "bibsearch-empty", "bibsearch-clear"):
                self.hidden[a["id"]] = "hidden" in a
            if a["id"] == "bibsearch-status":
                self.live = a.get("role") == "status" and a.get("aria-live") == "polite"
        if tag == "section":
            cat = a.get("data-publication-category")
            self.section_stack.append(cat)
            if cat in TYPES:
                self.sections.append(cat)
                self.year = None
        if tag == "h2" and "bibliography" in a.get("class", "").split(): self.year_buf = []
        if tag == "ol": self.ols.append("bibliography" in a.get("class", "").split())
        if tag == "li":
            if self.current is not None: self.li_depth += 1
            elif self.ols and self.ols[-1]:
                self.current = dict(key=None, category=self.section_stack[-1] if self.section_stack else None,
                                    year=self.year, links=[], hidden="hidden" in a)
                self.li_depth = 1
        if self.current is not None:
            if a.get("id") and self.current["key"] is None: self.current["key"] = a["id"]
            if tag == "a" and a.get("href"): self.current["links"].append(a["href"])
        if tag == "button" and "data-publication-filter" in a:
            self.filters.append((a["data-publication-filter"], a.get("aria-pressed")))
        if tag == "script" and a.get("type") == "application/ld+json": self.schema_buf = []

    def handle_data(self, data):
        if self.year_buf is not None: self.year_buf.append(data)
        if self.schema_buf is not None: self.schema_buf.append(data)

    def handle_endtag(self, tag):
        if tag == "h2" and self.year_buf is not None:
            year = re.search(r"\b\d{4}\b", "".join(self.year_buf))
            self.year = year.group() if year else None
            self.year_buf = None
        if tag == "script" and self.schema_buf is not None:
            obj = json.loads("".join(self.schema_buf))
            if isinstance(obj, dict) and obj.get("@type") in ("ScholarlyArticle", "Thesis", "CreativeWork"):
                self.schemas.append(obj)
            self.schema_buf = None
        if tag == "li" and self.current is not None:
            self.li_depth -= 1
            if self.li_depth == 0:
                self.rows.append(self.current)
                self.current = None
        if tag == "ol" and self.ols: self.ols.pop()
        if tag == "section" and self.section_stack: self.section_stack.pop()


def verify_document(html: str, expected: list, language: str):
    doc = Document()
    doc.feed(html)
    if doc.lang != language or doc.landmarks != [1, 1]:
        raise ValueError(language + ": invalid document language or landmarks")
    if doc.sections != list(TYPES):
        raise ValueError(language + ": publication category sections differ")
    if not set(("journal-articles", "conference-contributions", "doctoral-thesis",
                "publication-list", "Moda2022a")).issubset(doc.ids):
        raise ValueError(language + ": publication or Rosenthal anchors missing")
    if doc.filters != [(x, "true" if x == "all" else "false") for x in KEYS]:
        raise ValueError(language + ": publication filter values or initial pressed state differ")
    if not doc.live or not all(doc.hidden.get(x) is True for x in
                               ("bibsearch", "publication-type-filters", "bibsearch-empty", "bibsearch-clear")):
        raise ValueError(language + ": search controls lack progressive accessibility")
    expected_map = {x["key"]: x for x in expected}
    keys = [r["key"] for r in doc.rows]
    missing = set(expected_map) - set(keys)
    if missing or set(keys) != set(expected_map) or len(keys) != len(expected):
        raise ValueError(language + ": missing or duplicate bibliography IDs " + repr(sorted(missing)))
    for row in doc.rows:
        e = expected_map[row["key"]]
        if row["category"] != e["category"]:
            raise ValueError(language + ": wrong category for " + row["key"])
        if row["hidden"]:
            raise ValueError(language + ": static record hidden " + row["key"])
        if e.get("doi") and "https://doi.org/" + e["doi"] not in row["links"]:
            raise ValueError(language + ": DOI link absent for " + row["key"])
        if e.get("pdf") and not any(href.endswith(e["pdf"]) for href in row["links"]):
            raise ValueError(language + ": PDF link absent for " + row["key"])
    if len(doc.schemas) != len(expected):
        raise ValueError(language + ": bibliography JSON-LD count mismatch")
    return doc


def verify_publications_index(root: Path) -> None:
    root = Path(root)
    routes = (("en", "publications/index.html"), ("it", "it/publications/index.html"))
    for lang, filename in routes:
        if not (root / filename).is_file():
            raise ValueError("Missing " + ("Italian" if lang == "it" else "English") + " publications page " + filename)
    expected = canonical_entries()
    docs = [verify_document((root / filename).read_text(encoding="utf8"), expected, lang)
            for lang, filename in routes]
    english, italian = docs
    if [(r["key"], r["category"]) for r in english.rows] != [(r["key"], r["category"]) for r in italian.rows]:
        raise ValueError("EN/IT bibliography key/type order differs")
    if english.schemas != italian.schemas:
        raise ValueError("EN/IT scholarly JSON-LD differs")


if __name__ == "__main__":
    verify_publications_index(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
    print("PASS: canonical bilingual Publications index and scholarly metadata")
