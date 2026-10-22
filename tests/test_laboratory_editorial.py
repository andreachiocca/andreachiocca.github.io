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
        self.assertEqual(combined.lower().count("climatic chamber"), 1)
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

if __name__ == "__main__":
    unittest.main()
