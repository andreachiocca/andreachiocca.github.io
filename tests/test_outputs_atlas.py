"""Source-level contracts for the bilingual Research Outputs Atlas."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf8")


class OutputsAtlasTests(unittest.TestCase):
    def setUp(self):
        self.outputs = json.loads(read("_data/research_outputs.json"))
        self.selected = json.loads(read("_data/research_output_spotlight.json"))
        self.page = read("_pages/repositories.md")

    def test_canonical_resources_and_highlight_links(self):
        ids = [record["id"] for record in self.outputs]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(self.selected), 4)
        self.assertEqual(len(self.selected), len(set(self.selected)))
        self.assertTrue(set(self.selected).issubset(ids))
        self.assertIn("zenodo-21534682", self.selected)
        self.assertEqual(self.page.count("include research_output.html"), 1)
        self.assertIn("site.data.research_output_spotlight", self.page)
        self.assertIn("localized_record: 'outputs'", self.page)
        self.assertIn("site.data.research_outputs", self.page)
        self.assertIn('href="#{{ canonical_feature.id | escape }}"', self.page)

    def test_bilingual_controls_and_anchors(self):
        english = json.loads(read("_data/i18n/en/ui.json"))
        italian = json.loads(read("_data/i18n/it/ui.json"))
        self.assertEqual(set(english), set(italian))
        for name in ("Selected outputs", "Complete catalogue",
                     "Search by title, method, material or DOI",
                     "No research outputs match the selected filters.",
                     "Clear catalogue filters", "View in catalogue"):
            self.assertTrue(english[name])
            self.assertTrue(italian[name])
        for token in ('id="selected-outputs"', 'id="complete-catalogue"',
                      'id="output-search"', 'id="output-empty"',
                      'id="output-reset"', 'id="output-grid"',
                      'data-filter="software"', 'data-filter="data"'):
            self.assertIn(token, self.page)
        self.assertIn("translation_key: repositories", self.page)

    def test_progressive_search_and_responsive_styles(self):
        script = read("assets/js/research_outputs.js")
        for token in ("search.addEventListener('input'", "normalise", "card.hidden",
                      "revealLinkedResource", "reset.hidden",
                      "controls.hidden = false", "searchPanel.hidden = false"):
            self.assertIn(token, script)
        self.assertIn('class="output-catalogue output-atlas"', self.page)
        self.assertEqual(read("assets/css/main.scss").count('@import "outputs_atlas";'), 1)
        css = read("_sass/_outputs_atlas.scss")
        self.assertIn(".output-atlas", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("min-height: 44px", css)
        self.assertNotIn("@import url(", css)
        self.assertNotIn("<img", self.page)

    def test_generated_verification_is_in_both_workflows(self):
        self.assertTrue((ROOT / "scripts/verify_outputs_atlas.py").is_file())
        for path in (".github/workflows/build.yml", ".github/workflows/preview.yml"):
            self.assertIn("python scripts/verify_outputs_atlas.py _site", read(path))


if __name__ == "__main__":
    unittest.main()
