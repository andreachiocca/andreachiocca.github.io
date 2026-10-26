"""Source checks for bilingual Teaching and Thesis editorial pages."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class TeachingThesisEditorialTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(read("_data/thesis_opportunities.json"))
        self.italian = json.loads(read("_data/i18n/it/thesis.json"))
        self.teaching = read("_pages/teaching.md")
        self.thesis = read("_pages/thesis.md")

    def test_project_records_scientific_papers_and_images(self):
        projects = self.data["projects"]
        self.assertEqual(len(projects), 3)
        self.assertEqual({p["id"] for p in projects},
                         {"open-multiaxial-fatigue", "pcb-capacitor-vibration-fatigue", "coated-lattice-fatigue"})
        self.assertEqual(len(self.data["directions"]), 5)
        self.assertEqual(len(self.data["approaches"]), 3)
        self.assertEqual(len(self.data["international_contacts"]), 4)
        for project in projects:
            record_id = project["id"]
            self.assertIn(record_id, self.italian)
            for key in ("title", "mode", "description", "activities", "image_alt", "image_caption", "tags"):
                self.assertTrue(self.italian[record_id][key], (record_id, key))
                self.assertTrue(project[key], (record_id, key))
            self.assertEqual(
                [paper["doi"].lower() for paper in project["related_papers"]],
                {
                    "open-multiaxial-fatigue": ["10.1016/j.ijmecsci.2022.107974",
                                                "10.1016/j.euromechsol.2024.105274"],
                    "pcb-capacitor-vibration-fatigue": ["10.1016/j.prostr.2023.07.043"],
                    "coated-lattice-fatigue": ["10.1016/j.prostr.2022.12.101"],
                }[record_id])
            for paper in project["related_papers"]:
                self.assertTrue(paper["title"] and paper["doi"] and paper["url"])
                self.assertTrue(paper["url"].startswith("/") or paper["url"].startswith("https://doi.org/"))
            self.assertTrue(project["image"].startswith("/assets/img/thesis/"))
            photo = ROOT / project["image"].lstrip("/")
            self.assertTrue(photo.is_file(), str(photo))
            payload = photo.read_bytes()
            self.assertTrue(payload.startswith(b"RIFF") and payload[8:12] == b"WEBP", str(photo))
            self.assertNotIn("—", project["description"])
            self.assertNotIn("—", self.italian[record_id]["description"])
        fatigue, pcb, lattice = projects
        self.assertIn("multiaxial-fatigue", fatigue["links"][0]["url"])
        self.assertIn("PCBAs", pcb["description"])
        self.assertIn("shakers", pcb["description"])
        self.assertIn("10.1016/j.prostr.2022.12.101", {p["doi"] for p in lattice["related_papers"]})
        self.assertEqual(lattice["image_original"], "/assets/img/thesis/lattice-thermal-imaging-original.gif")
        self.assertTrue((ROOT / lattice["image_original"].lstrip("/")).read_bytes().startswith(b"GIF"))

    def test_render_safe_page_sources(self):
        self.assertIn("translation_key: teaching", self.teaching)
        self.assertIn("translation_key: thesis", self.thesis)
        self.assertIn('class="teaching-editorial teaching-editorial-hero"', self.teaching)
        self.assertIn("capture teaching_intro", self.teaching)
        self.assertIn("markdownify", self.teaching)
        self.assertNotIn('markdown="1"', self.teaching)
        self.assertNotIn('markdown="1"', self.thesis)
        self.assertIn('class="thesis-editorial thesis-editorial-banner"', self.thesis)
        self.assertIn('id="specific-projects"', self.thesis)
        self.assertIn("include thesis_project_panel.html", self.thesis)
        self.assertIn('id="research-directions"', self.thesis)
        self.assertIn('id="discuss-a-thesis"', self.thesis)
        self.assertIn("mailto:andrea.chiocca@unipi.it", self.thesis)
        include = read("_includes/thesis_project_panel.html")
        for marker in ("localized_record: 'thesis'", "related_papers", "thesis-project-tags",
                       "image_original", "loading=\"lazy\"", "image_caption", "mailto:andrea.chiocca@unipi.it"):
            self.assertIn(marker, include)

    def test_teaching_materials_and_scope(self):
        for filename, period in (("_projects/2_project.md", "2018–2026/27"),
                                 ("_projects/3_project.md", "2024–2026/27"),
                                 ("_projects/4_project.md", "2024–2026/27")):
            record = read(filename)
            self.assertIn("teaching_period: " + period, record)
            self.assertIn("teaching_group: recent", record)
        self.assertIn("teaching_group: previous", read("_projects/1_project.md"))
        self.assertIn("teaching_materials[course.materials_key]", self.teaching)
        self.assertIn("2026/27", self.teaching)
        self.assertIn("Three computational and experimental thesis projects", self.thesis)

    def test_styles_translations_and_ci(self):
        css = read("_sass/_teaching_thesis_editorial.scss")
        for selector in (".teaching-editorial", ".thesis-editorial", ".thesis-project-references",
                         ".thesis-editorial-banner", "max-width: 699px"):
            self.assertIn(selector, css)
        self.assertEqual(read("assets/css/main.scss").count('@import "teaching_thesis_editorial";'), 1)
        for path in (".github/workflows/build.yml", ".github/workflows/preview.yml"):
            self.assertIn("python scripts/verify_teaching_thesis_editorial.py _site", read(path))
        en = json.loads(read("_data/i18n/en/ui.json"))
        it = json.loads(read("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))
        for key in ("Related publications", "Available thesis projects", "View original thermal image",
                    "Research-led thesis opportunities"):
            self.assertTrue(it[key])
        self.assertTrue((ROOT / "assets/img/thesis/robot-lattice-concept.svg").is_file())
        illustration = read("assets/img/thesis/robot-lattice-concept.svg")
        self.assertIn("M100 350L175 265L300 296L394 169", illustration)
        for marker in ('cx="100" cy="350"', 'cx="175" cy="265"', 'cx="300" cy="296"'):
            self.assertIn(marker, illustration)
        for removed in ("M385 170L429 140", "M449 168L482 165", "M482 175L515 175"):
            self.assertNotIn(removed, illustration)
        import re
        entries = re.split(r"(?=@[A-Za-z]+\{)", read("_bibliography/PersonalPub.bib"))
        for project in self.data["projects"]:
            for paper in project["related_papers"]:
                matches = [entry for entry in entries if paper["doi"].lower() in entry.lower()]
                self.assertEqual(len(matches), 1, paper["doi"])
                self.assertIn("Chiocca", matches[0])

if __name__ == "__main__":
    unittest.main()
