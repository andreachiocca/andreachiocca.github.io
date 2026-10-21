"""Source and mechanics contracts for the Technical Research Atlas."""
from pathlib import Path
import json
import math
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class ResearchAtlasSourceTests(unittest.TestCase):
    def test_layout_and_localized_intro(self):
        page = source("_pages/research.md")
        shell = source("_layouts/research_atlas.html")
        self.assertIn("layout: research_atlas", page)
        self.assertIn("layout: default", shell)
        self.assertEqual(shell.count("<h1"), 1)
        self.assertEqual(shell.count("{% locale research.intro %}"), 1)
        self.assertIn("I study how materials and components respond to repeated loads", shell)
        self.assertNotIn("{% locale research.intro %}", page)
        self.assertIn("{{ content }}", shell)
        self.assertEqual(source("assets/css/main.scss").count('@import "research_atlas";'), 1)
        en = json.loads(source("_data/i18n/en/ui.json"))
        it = json.loads(source("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))

    def test_jump_link_targets(self):
        shell = source("_layouts/research_atlas.html")
        page = source("_pages/research.md")
        for anchor in ("research-areas", "projects", "international-collaborations"):
            self.assertIn('href="#' + anchor + '"', shell)
            self.assertIn('id="' + anchor + '"', page)


if __name__ == "__main__":
    unittest.main()
