"""Teaching and thesis editorial source contracts."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class TeachingThesisEditorialTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(read("_data/thesis_opportunities.json"))
        self.it = json.loads(read("_data/i18n/it/thesis.json"))
        self.teaching = read("_pages/teaching.md")
        self.thesis = read("_pages/thesis.md")

    def test_project_scope_and_research_links(self):
        self.assertEqual(len(self.data["projects"]), 2)
        projects = {item["id"]: item for item in self.data["projects"]}
        self.assertEqual(set(projects), {"open-multiaxial-fatigue", "pcb-capacitor-vibration-fatigue"})
        self.assertEqual(len(self.data["directions"]), 5)
        self.assertEqual(len(self.data["approaches"]), 3)
        self.assertEqual(len(self.data["international_contacts"]), 4)
        self.assertEqual(set(projects).intersection(x["id"] for x in self.data["directions"]), set())
        self.assertEqual(set(projects).intersection(x["id"] for x in self.data["approaches"]), set())
        self.assertIn("https://github.com/andreachiocca/multiaxial-fatigue",
                      [link["url"] for link in projects["open-multiaxial-fatigue"]["links"]])
        for key, project in projects.items():
            self.assertIn(key, self.it)
            for field in ("title", "description", "activities", "mode", "image_alt", "image_caption"):
                self.assertTrue(self.it[key][field])
                self.assertTrue(project[field])
            self.assertTrue(project["image"].startswith("/assets/img/thesis/"))
            self.assertEqual(Path(project["image"]).suffix, ".webp")
            self.assertGreater(project["image_width"], 0)
            self.assertGreater(project["image_height"], 0)
            self.assertNotIn("—", project["description"])
            self.assertNotIn("—", self.it[key]["description"])
        self.assertIn("PCBAs", projects["pcb-capacitor-vibration-fatigue"]["description"])
        self.assertIn("shakers", projects["pcb-capacitor-vibration-fatigue"]["description"])
        self.assertIn("Not experimental", projects["open-multiaxial-fatigue"]["image_caption"].replace("These are not experimental", "Not experimental"))

    def test_bilingual_layouts_and_direct_contact(self):
        self.assertEqual(self.teaching.count('translation_key: teaching'), 1)
        self.assertEqual(self.thesis.count('translation_key: thesis'), 1)
        self.assertIn('class="teaching-editorial" markdown="1"', self.teaching)
        self.assertIn('class="thesis-editorial" markdown="1"', self.thesis)
        self.assertIn('id="specific-projects"', self.thesis)
        self.assertIn("include thesis_project_panel.html", self.thesis)
        self.assertEqual(self.thesis.count("include thesis_project_panel.html"), 1)
        self.assertIn('id="research-directions"', self.thesis)
        self.assertIn('id="discuss-a-thesis"', self.thesis)
        self.assertIn("mailto:andrea.chiocca@unipi.it", self.thesis)
        inc = read("_includes/thesis_project_panel.html")
        self.assertIn("canonical.image", inc)
        self.assertIn("site.static_files", inc)
        self.assertIn("loading=\"lazy\"", inc)
        self.assertIn("project.image_alt", inc)
        self.assertIn("project.image_caption", inc)
        self.assertIn("mailto:andrea.chiocca@unipi.it", inc)
        self.assertIn("markdown=\"1\"", self.teaching)

    def test_same_courses_and_sources(self):
        for path, expected in (("_projects/2_project.md", "2018–2026/27"),
                               ("_projects/3_project.md", "2024–2026/27"),
                               ("_projects/4_project.md", "2024–2026/27")):
            course = read(path)
            self.assertIn("teaching_period: " + expected, course)
            self.assertIn("teaching_group: recent", course)
        self.assertIn("teaching_group: previous", read("_projects/1_project.md"))
        self.assertIn("2026/27", self.teaching)
        self.assertIn("teaching_materials[course.materials_key]", self.teaching)

    def test_only_page_scoped_styles_and_translation_parity(self):
        css = read("_sass/_teaching_thesis_editorial.scss")
        self.assertIn(".teaching-editorial", css)
        self.assertIn(".thesis-editorial", css)
        self.assertIn("max-width: 699px", css)
        self.assertEqual(read("assets/css/main.scss").count('@import "teaching_thesis_editorial";'), 1)
        en = json.loads(read("_data/i18n/en/ui.json"))
        it = json.loads(read("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))
        for key in ("Available thesis projects", "Project activities", "Discuss a project",
                    "Courses and teaching materials", "See available thesis projects"):
            self.assertIn(key, it)
            self.assertTrue(it[key])

    def test_verification_wired_to_ci(self):
        for path in (".github/workflows/build.yml", ".github/workflows/preview.yml"):
            self.assertIn("python scripts/verify_teaching_thesis_editorial.py _site", read(path))

if __name__ == "__main__":
    unittest.main()
