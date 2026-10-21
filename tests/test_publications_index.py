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

if __name__ == "__main__":
    unittest.main()
