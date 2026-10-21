"""Source contracts for the bilingual Publications page."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PublicationsAtlasTests(unittest.TestCase):
    def test_single_source_and_existing_destinations(self):
        page = source("_pages/publications.md")
        self.assertIn("layout: publications_atlas", page)
        self.assertIn("{% bibliography --query @article %}", page)
        self.assertIn("{% bibliography --query @inproceedings %}", page)
        self.assertIn("{% bibliography --query @phdthesis %}", page)
        self.assertIn('id="Moda2022a"', page)
        self.assertIn("'/repositories/' | local_url | relative_url", page)
        self.assertNotIn("@article{", page)

    def test_layout_and_editorial_index(self):
        layout = source("_layouts/publications_atlas.html")
        self.assertIn("layout: default", layout)
        self.assertEqual(layout.count("<h1"), 1)
        self.assertEqual(layout.count("{{ content }}"), 1)
        self.assertIn("{% locale publications.intro %}", layout)
        for anchor in ("journal-articles", "conference-contributions", "doctoral-thesis"):
            self.assertIn('href="#' + anchor + '"', layout)

    def test_filter_progressively_enhances_bibliography(self):
        controls = source("_includes/bib_search.liquid")
        script = source("assets/js/bibsearch.js")
        bib = source("_layouts/bib.html")
        self.assertIn('class="publication-controls" hidden', controls)
        for kind in ("all", "article", "inproceedings", "phdthesis"):
            self.assertIn('data-publication-type="' + kind + '"', controls)
        self.assertIn("controls.hidden = false", script)
        self.assertIn("data-publication-keywords", bib)
        self.assertIn("entry.keywords | escape", bib)
        self.assertIn('id="{{entry.key}}"', bib)
        self.assertIn("https://doi.org/{{ entry.doi | escape }}", bib)
        self.assertIn('type="application/ld+json"', bib)

    def test_styles_and_locales_are_scoped(self):
        css = source("_sass/_publications_atlas.scss")
        self.assertIn(".publication-atlas", css)
        self.assertIn("prefers-reduced-motion", css)
        self.assertEqual(source("assets/css/main.scss").count('@import "publications_atlas";'), 1)
        en = json.loads(source("_data/i18n/en/ui.json"))
        it = json.loads(source("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))
        for key in ("Publication type", "No matching publications", "Clear search"):
            self.assertTrue(en[key] and it[key])


if __name__ == "__main__":
    unittest.main()
