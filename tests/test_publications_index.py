"""Phase 4 Publications page contracts (pre-build, no external dependencies)."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PublicationsIndexSourceTests(unittest.TestCase):
    def test_page_scope_and_canonical_bibliographies(self):
        page = read("_pages/publications.md")
        self.assertIn("translation_key: publications", page)
        self.assertIn("layout: page", page)
        self.assertIn('class="publications-index"', page)
        self.assertIn('id="publication-list"', page)
        self.assertIn("{% include bib_search.liquid %}", page)
        self.assertIn('id="Moda2022a"', page)
        self.assertEqual(re.findall(r'data-publication-category="([^"]+)"', page),
                         ["article", "inproceedings", "phdthesis"])
        self.assertEqual(re.findall(r'{% bibliography --query @(\w+) %}', page),
                         ["article", "inproceedings", "phdthesis"])
        for heading in ("journal-articles", "conference-contributions", "doctoral-thesis"):
            self.assertIn('id="' + heading + '"', page)
        self.assertEqual(read("assets/css/main.scss").count('@import "publications_index";'), 1)
        self.assertTrue((ROOT / "_sass/_publications_index.scss").is_file())

    def test_filter_controls_and_i18n(self):
        markup = read("_includes/bib_search.liquid")
        types = re.findall(r'data-publication-filter="([^"]+)"', markup)
        self.assertEqual(types, ["all", "article", "inproceedings", "phdthesis"])
        for marker in ('id="publication-type-filters"', 'id="bibsearch-empty"',
                       'id="bibsearch-clear"', 'id="bibsearch-status"', 'id="bibsearch"'):
            self.assertIn(marker, markup)
        self.assertIn('aria-pressed="true"', markup)
        self.assertEqual(markup.count('aria-pressed="false"'), 3)
        self.assertIn('aria-live="polite"', markup)
        self.assertIn('role="status"', markup)
        self.assertIn('data-count-template=', markup)
        self.assertIn('hidden', markup)
        en = json.loads(read("_data/i18n/en/ui.json"))
        it = json.loads(read("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))
        for label in ("Publication type", "No publications match your search.", "Clear filters"):
            self.assertIn(label, en)
            self.assertTrue(it[label].strip())
        script = read("assets/js/bibsearch.js")
        for token in ('data-publication-filter', 'aria-pressed', 'bibsearch-empty',
                      'bibsearch-clear', 'filterPublications', 'DOMContentLoaded'):
            self.assertIn(token, script)
        config = read("_config.yml")
        self.assertIn("altmetric: false", config)
        self.assertIn("dimensions: false", config)
        self.assertIn("enable_publication_thumbnails: false", config)


    def test_scoped_entry_styles_and_no_external_badges(self):
        styles = read("_sass/_publications_index.scss")
        for selector in (
            ".publications-index .publications .title",
            ".publications-index .publications .author",
            ".publications-index .publications .periodical",
            ".publications-index .publications .links .btn",
            ".publications-index .publication-details summary",
            ".publications-index .publications h2.bibliography",
            ".publications-index :focus-visible",
            ".publications-index [hidden]"
        ):
            self.assertIn(selector, styles)
        for rule in ("min-height: 44px", "overflow-wrap: anywhere", "@media (max-width: 575px)"):
            self.assertIn(rule, styles)
        self.assertNotIn("@import url(", styles)
        self.assertNotIn("https://", styles)
        config = read("_config.yml")
        self.assertIn("altmetric: false", config)
        self.assertIn("dimensions: false", config)
        self.assertIn("enable_publication_thumbnails: false", config)

if __name__ == "__main__":
    unittest.main()
