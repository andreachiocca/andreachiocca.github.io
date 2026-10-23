"""Lab page source contracts: equipment, bilingual copy, and privacy."""
from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf8"))
class LabTests(unittest.TestCase):
    def test_machines_and_units(self):
        d=load("_data/laboratory.json")
        ids=[r["id"] for r in d["equipment"]]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),10)
        by={r["id"]:r for r in d["equipment"]}
        for id in ("schenck-axial-torsional","rumul-resonant","flir-x6901sc","three-actuator-bench"):
            self.assertIn(id,by)
        def joined(id):
            r=by[id]
            return " ".join([r["description"]]+[s["value"] for s in r.get("specifications",[])])
        self.assertIn("700 bar",joined("schenck-axial-torsional"))
        self.assertNotIn("700 MPa",joined("schenck-axial-torsional"))
        self.assertIn("1004",joined("flir-x6901sc"))
        self.assertIn("640 × 512",joined("flir-x6901sc"))
        self.assertIn("three",joined("three-actuator-bench").lower())
        self.assertIn("20 kN",joined("rumul-resonant"))
        self.assertIn("150 kN",joined("rumul-resonant"))
        self.assertIn("25 kN",joined("mts-uniaxial"))
        self.assertIn("100 kN",joined("mts-uniaxial"))
        self.assertTrue(d["capabilities"] and d["measurement_context"])
    def test_it_translations_complete(self):
        d=load("_data/laboratory.json")
        it=load("_data/i18n/it/laboratory.json")
        for r in d["equipment"]:
            self.assertIn(r["id"],it)
            self.assertTrue(it[r["id"]].get("title"))
            self.assertTrue(it[r["id"]].get("description"))
            self.assertNotIn("specifications",it[r["id"]])
    def test_page_and_images(self):
        page=(ROOT/"_pages/laboratory.md").read_text(encoding="utf8")
        css=(ROOT/"assets/css/main.scss").read_text(encoding="utf8")
        self.assertIn('class="laboratory-editorial"',page)
        for anchor in ("research-expertise","instrumentation","equipment","laboratory-collaboration"):
            self.assertIn('id="'+anchor+'"',page)
        self.assertIn('@import "laboratory_editorial";',css)
        self.assertTrue((ROOT/"_sass/_laboratory_editorial.scss").is_file())
        self.assertTrue((ROOT/"_includes/laboratory_equipment.html").is_file())
        for text in (page,css,(ROOT/"_data/laboratory.json").read_text()):
            self.assertNotIn("IMG_0420",text)
