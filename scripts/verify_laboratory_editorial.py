"""Verify the bilingual Laboratory page, machine specifications and genuine images."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
ANCHORS = ("research-expertise", "instrumentation", "equipment", "laboratory-collaboration")
CONTACT = "mailto:andrea.chiocca@unipi.it?subject=Experimental"


class LaboratoryDocument(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.main = 0
        self.h1 = 0
        self.anchors = set()
        self.links = []
        self.records = []
        self.current = None
        self.photos = []
        self.sources = []
        self.figcaptions = 0
        self.in_caption = False
        self.page_text = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if tag == "html":
            self.lang = attr.get("lang")
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.h1 += 1
        if attr.get("id"):
            self.anchors.add(attr["id"])
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag == "article" and attr.get("data-laboratory-id"):
            if self.current is not None:
                raise ValueError("Nested Laboratory equipment records")
            self.current = {
                "id": attr["data-laboratory-id"],
                "scope": attr.get("data-evidence-scope"),
                "text": [],
            }
        if tag == "img" and "/assets/img/laboratory/" in attr.get("src", ""):
            self.photos.append(attr)
        if tag == "source" and "/assets/img/laboratory/" in attr.get("srcset", ""):
            self.sources.append(attr["srcset"])
        if tag == "figcaption":
            self.in_caption = True
            self.figcaptions += 1

    def handle_data(self, data):
        self.page_text.append(data)
        if self.current is not None:
            self.current["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "article" and self.current is not None:
            self.records.append(self.current)
            self.current = None
        if tag == "figcaption":
            self.in_caption = False


def validate_asset(url: str, root: Path, language: str) -> None:
    path = unquote(urlsplit(url).path)
    if path.startswith("/it/assets/") or not path.startswith("/assets/img/laboratory/"):
        raise ValueError(f"{language}: invalid localized Laboratory image path {path}")
    if "IMG_0420" in path:
        raise ValueError(f"{language}: private camera serial-number photo referenced")
    asset = root / path.lstrip("/")
    if not asset.is_file():
        raise ValueError(f"{language}: missing Laboratory photo file {path}")
    data = asset.read_bytes()
    if not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise ValueError(f"{language}: malformed Laboratory WebP {path}")
    if len(data) > 200000:
        raise ValueError(f"{language}: Laboratory photo exceeds 200 KB {path}")


def verify_document(html: str, expected: list[dict], root: Path, language: str) -> LaboratoryDocument:
    root = Path(root)
    doc = LaboratoryDocument()
    doc.feed(html)
    if doc.lang != language or doc.main != 1 or doc.h1 != 1:
        raise ValueError(f"{language}: incorrect page language or landmarks")
    if not set(ANCHORS).issubset(doc.anchors):
        raise ValueError(f"{language}: missing Laboratory section anchors: {sorted(set(ANCHORS) - doc.anchors)}")
    if not any(link.startswith(CONTACT) for link in doc.links):
        raise ValueError(f"{language}: Laboratory contact link missing")
    if "IMG_0420" in html or "700 MPa" in html or "X6901sc SLS" in html:
        raise ValueError(f"{language}: unsupported or private Laboratory content")
    keys = [record["id"] for record in doc.records]
    wanted = [record["id"] for record in expected]
    if keys != wanted:
        raise ValueError(f"{language}: Laboratory records/order differ: {keys} != {wanted}")
    for rendered, canonical in zip(doc.records, expected):
        if rendered["scope"] != canonical["evidence_scope"]:
            raise ValueError(f"{language}: wrong evidence scope for {rendered['id']}")
        content = " ".join(rendered["text"])
        for spec in canonical.get("specifications", []):
            if spec["value"] not in content:
                raise ValueError(f"{language}: {rendered['id']} missing specification {spec['label']}: {spec['value']}")
        if rendered["id"] == "schenck-axial-torsional" and "700 bar" not in content:
            raise ValueError(f"{language}: Schenck 700 bar internal-pressure limit missing")

    if not doc.photos or doc.figcaptions < len(doc.photos):
        raise ValueError(f"{language}: Laboratory photo or caption missing")
    for photo in doc.photos:
        if not photo.get("alt", "").strip():
            raise ValueError(f"{language}: Laboratory image missing alt text")
        if not photo.get("width", "").isdigit() or not photo.get("height", "").isdigit():
            raise ValueError(f"{language}: Laboratory image missing dimensions")
        if int(photo["width"]) <= 0 or int(photo["height"]) <= 0:
            raise ValueError(f"{language}: invalid Laboratory image dimensions")
        if photo.get("loading") not in ("lazy", "eager"):
            raise ValueError(f"{language}: no explicit Laboratory image loading priority")
        validate_asset(photo["src"], root, language)
    if len(doc.sources) != len(doc.photos):
        raise ValueError(f"{language}: each Laboratory image needs a responsive srcset")
    for srcset in doc.sources:
        values = [item.strip().split()[0] for item in srcset.split(",")]
        if not any("640.webp" in value for value in values) or not any("1280.webp" in value for value in values):
            raise ValueError(f"{language}: incomplete 640/1280 WebP srcset")
        for value in values:
            validate_asset(value, root, language)
    return doc


def verify_laboratory_editorial(root: Path) -> None:
    root = Path(root)
    canonical = json.loads((ROOT / "_data/laboratory.json").read_text(encoding="utf8"))
    expected = canonical["equipment"]
    actual = []
    for language, relative in (("en", "laboratory/index.html"), ("it", "it/laboratory/index.html")):
        page = root / relative
        if not page.is_file():
            raise ValueError(f"Missing {language} Laboratory page at {relative}")
        actual.append(verify_document(page.read_text(encoding="utf8"), expected, root, language))
    english, italian = actual
    if [r["id"] for r in english.records] != [r["id"] for r in italian.records]:
        raise ValueError("EN/IT Laboratory equipment identities diverged")
    for name, page in (("en", english), ("it", italian)):
        expected_count = 1 + sum(bool(r.get("image")) for r in expected)
        if len(page.photos) != expected_count:
            raise ValueError(f"{name}: expected {expected_count} Laboratory photos, got {len(page.photos)}")
    if english.photos[0]["alt"] == italian.photos[0]["alt"]:
        raise ValueError("Missing bilingual Laboratory hero alternative text")


if __name__ == "__main__":
    verify_laboratory_editorial(Path(sys.argv[1] if len(sys.argv) > 1 else "_site"))
    print("PASS: bilingual Laboratory equipment, 700 bar pressure, images and scientific metadata")
