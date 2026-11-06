"""Regression checks for bilingual search metadata and academic profile schema."""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
KEYS = (
    "research", "publications", "repositories", "laboratory",
    "teaching", "thesis", "cv",
)


def frontmatter(key):
    source = (ROOT / "_pages" / f"{key}.md").read_text(encoding="utf-8")
    parts = source.split("---", 2)
    if len(parts) != 3:
        raise AssertionError(f"Missing front matter for {key}")
    return parts[1]


class SEOMetadataTests(unittest.TestCase):
    def test_bilingual_seo_titles_are_descriptive_and_distinct(self):
        it = json.loads((ROOT / "_data/i18n/it/pages.json").read_text(encoding="utf-8"))
        titles = {"en": [], "it": []}
        for key in KEYS:
            match = re.search(r"^seo_title: (.+)$", frontmatter(key), re.M)
            self.assertIsNotNone(match, key)
            en_title = match.group(1).strip()
            it_title = it[key]["seo_title"].strip()
            self.assertNotEqual(en_title, it_title, key)
            for lang, title in (("en", en_title), ("it", it_title)):
                self.assertGreaterEqual(len(title), 20, (key, lang))
                self.assertLessEqual(len(title), 65, (key, lang))
                titles[lang].append(title)
        for lang in titles:
            self.assertEqual(len(titles[lang]), len(set(titles[lang])))

    def test_home_schema_is_a_profile_page_with_person_entity(self):
        metadata = (ROOT / "_includes/metadata.html").read_text(encoding="utf-8")
        self.assertIn("ProfilePage", metadata)
        self.assertIn("page.translation_key == 'home'", metadata)
        self.assertIn('"mainEntity": { "@id": {{ person_id | jsonify }} }', metadata)
        self.assertIn('"@id": {{ webpage_id | jsonify }}', metadata)
        self.assertIn("'/assets/img/prof_pic.jpg' | absolute_url", metadata)
        self.assertTrue((ROOT / "assets/img/prof_pic.jpg").is_file())

    def test_search_console_and_previews_stay_configured(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        preview = (ROOT / "_config_preview.yml").read_text(encoding="utf-8")
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("enable_google_verification: true", config)
        self.assertIn("enable_google_analytics:    true", config)
        self.assertIn("Sitemap:", robots)
        self.assertIn("enable_google_analytics: false", preview)
        self.assertIn("noindex", (ROOT / "_includes/metadata.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
