"""Phase 5 source-level contracts for the bilingual Laboratory editorial page."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = (
    "steplab-axial-torsional", "schenck-axial-torsional", "rumul-resonant",
    "mts-uniaxial", "steplab-electromechanical", "three-actuator-bench",
    "vibration-testing", "environmental-conditioning",
    "specimen-preparation-metrology", "flir-x6901sc",
)


def read(path):
    return (ROOT / path).read_text(encoding="utf8")


class LaboratorySourceTests(unittest.TestCase):
    def setUp(self):
        self.lab = json.loads(read("_data/laboratory.json"))
        self.records = {r["id"]: r for r in self.lab["equipment"]}
        self.italian = json.loads(read("_data/i18n/it/laboratory.json"))

    def test_equipment_canonical_values(self):
        self.assertEqual(tuple(self.records), IDS)
        self.assertEqual(len(self.records), len(self.lab["equipment"]))
        self.assertEqual(len(self.lab["capabilities"]), 5)
        self.assertEqual(len(self.lab["measurement_context"]), 3)
        combined = json.dumps(self.lab, ensure_ascii=False)
        self.assertIn("700 bar", combined)
        self.assertNotIn("700 MPa", combined)
        self.assertIn("250 kN", str(self.records["schenck-axial-torsional"]))
        self.assertIn("2000 N·m", str(self.records["schenck-axial-torsional"]))
        self.assertIn("33 kN", str(self.records["steplab-axial-torsional"]))
        self.assertIn("43.5 kN", str(self.records["steplab-axial-torsional"]))
        self.assertIn("250 Hz", str(self.records["steplab-axial-torsional"]))
        self.assertIn("10 kN", str(self.records["steplab-electromechanical"]))
        self.assertIn("20 Hz", str(self.records["steplab-electromechanical"]))
        self.assertIn("25 kN", str(self.records["mts-uniaxial"]))
        self.assertIn("100 kN", str(self.records["mts-uniaxial"]))
        self.assertIn("20 kN", str(self.records["rumul-resonant"]))
        self.assertIn("150 kN", str(self.records["rumul-resonant"]))
        self.assertEqual(self.records["rumul-resonant"]["evidence_scope"], "historical")
        self.assertIn("three", self.records["three-actuator-bench"]["description"].lower())
        self.assertIn("seven", self.records["three-actuator-bench"]["status_note"].lower())
        chamber_specs = [spec for record in self.lab["equipment"] for spec in record["specifications"] if spec["label"] == "StepLab climatic chamber"]
        self.assertEqual(len(chamber_specs), 1)
        self.assertNotIn("20 kN machine", self.records["rumul-resonant"]["image_caption"])
        self.assertNotIn("150 kN machine", self.records["rumul-resonant"]["image_caption"])

    def test_equipment_locale_parity_and_metadata(self):
        all_ids = {r["id"] for r in self.lab["capabilities"] + self.lab["measurement_context"] + self.lab["equipment"]}
        self.assertTrue(all_ids.issubset(self.italian))
        for record in self.lab["equipment"]:
            translation = self.italian[record["id"]]
            self.assertTrue(translation.get("title"))
            self.assertTrue(translation.get("description"))
            self.assertNotIn("specifications", translation)
            if record.get("image"):
                self.assertTrue(translation.get("image_alt"))
                self.assertTrue(translation.get("image_caption"))
        en = json.loads(read("_data/i18n/en/ui.json"))
        it = json.loads(read("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))
        flir = json.dumps(self.records["flir-x6901sc"], ensure_ascii=False)
        for value in ("X6901sc", "640 × 512", "3–5 µm", "1004", "20 mK"):
            self.assertIn(value, flir)


    def test_photo_assets_and_privacy(self):
        listed = self.lab["equipment"] + [self.lab["hero"]]
        for record in listed:
            photo = record.get("image")
            if photo is None:
                continue
            self.assertTrue(record.get("image_alt"), record["id"])
            self.assertTrue(record.get("image_caption"), record["id"])
            stem = photo["base"].split("/")[-1]
            self.assertNotIn("IMG_0420", stem)
            self.assertTrue(stem.isascii())
            for width in (640, 1280):
                file = ROOT / "assets" / "img" / "laboratory" / f"{stem}-{width}.webp"
                self.assertTrue(file.is_file(), str(file))
                data = file.read_bytes()
                self.assertTrue(data.startswith(b"RIFF") and data[8:12] == b"WEBP", str(file))
                self.assertLess(len(data), 200000, str(file))
        self.assertFalse((ROOT / "assets/img/laboratory/IMG_0420.JPG").exists())
        include = read("_includes/laboratory_equipment.html")
        for token in ("srcset", "image_alt", "image_caption", "specifications", "loading=", "width=", "height="):
            self.assertIn(token, include)
        self.assertIn("spec.label | t", include)


    def test_page_semantics_and_anchors(self):
        page = read("_pages/laboratory.md")
        self.assertIn("translation_key: laboratory", page)
        self.assertIn("layout: page", page)
        self.assertIn('class="laboratory-editorial"', page)
        for anchor in ("research-expertise", "instrumentation", "equipment", "laboratory-collaboration"):
            self.assertIn('id="' + anchor + '"', page)
        self.assertIn("include laboratory_equipment.html", page)
        self.assertIn("site.data.laboratory.equipment", page)
        self.assertIn("mailto:andrea.chiocca@unipi.it?subject=Experimental", page)
        for route in ("/research/", "/publications/", "/repositories/", "/thesis/"):
            self.assertIn(route, page)
        styles = read("_sass/_laboratory_editorial.scss")
        self.assertIn(".laboratory-editorial", styles)
        self.assertIn("prefers-reduced-motion", styles)
        self.assertIn(":focus-visible", styles)
        self.assertNotIn("@import url(", styles)
        self.assertEqual(read("assets/css/main.scss").count('@import "laboratory_editorial";'), 1)
        self.assertNotIn("IMG_0420", page)
        self.assertNotIn("700 MPa", page)



class LaboratoryRenderedTests(unittest.TestCase):
    @staticmethod
    def verifier():
        import importlib.util
        path = ROOT / "scripts/verify_laboratory_editorial.py"
        spec = importlib.util.spec_from_file_location("laboratory_verify", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def fixture(pressure="700 bar (70 MPa)", alt="Genuine mechanical specimen"):
        return f"""<!doctype html><html lang="en"><main><h1>Laboratory</h1>
        <section id="equipment"><h2>Equipment</h2>
        <article data-laboratory-id="schenck-axial-torsional"
        data-evidence-scope="current-description">
        <h3>Schenck</h3><p>Servo-hydraulic equipment</p><dl>
        <dt>Pressure</dt><dd>{pressure}</dd></dl>
        </article></section>
        <div id="research-expertise"></div><div id="instrumentation"></div>
        <div id="laboratory-collaboration"></div>
        <figure><picture><source srcset="/assets/img/laboratory/specimen-640.webp 640w, /assets/img/laboratory/specimen-1280.webp 1280w">
        <img src="/assets/img/laboratory/specimen-640.webp" alt="{alt}"
          width="640" height="853" loading="eager"></picture>
        <figcaption>Machined specimen</figcaption></figure>
        <a href="mailto:andrea.chiocca@unipi.it?subject=Experimental">Contact</a>
        </main></html>"""

    def test_verifier_accepts_correct_pressure_and_real_image(self):
        module = self.verifier()
        expected = [{"id": "schenck-axial-torsional",
                     "evidence_scope": "current-description",
                     "specifications": [{"label": "Internal pressure", "value": "700 bar (70 MPa)"}]}]
        module.verify_document(self.fixture(), expected, ROOT, "en")

    def test_verifier_rejects_700_mpa_typo(self):
        module = self.verifier()
        expected = [{"id": "schenck-axial-torsional",
                     "evidence_scope": "current-description",
                     "specifications": [{"label": "Internal pressure", "value": "700 bar (70 MPa)"}]}]
        with self.assertRaisesRegex(ValueError, "700 bar|700 MPa"):
            module.verify_document(self.fixture(pressure="700 MPa"), expected, ROOT, "en")

    def test_verifier_rejects_missing_image_alt(self):
        module = self.verifier()
        expected = [{"id": "schenck-axial-torsional",
                     "evidence_scope": "current-description",
                     "specifications": [{"label": "Internal pressure", "value": "700 bar (70 MPa)"}]}]
        with self.assertRaisesRegex(ValueError, "alt"):
            module.verify_document(self.fixture(alt=""), expected, ROOT, "en")

if __name__ == "__main__":
    unittest.main()
