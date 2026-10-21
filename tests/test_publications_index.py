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


class PublicationsIndexGeneratedTests(unittest.TestCase):
    @staticmethod
    def verifier():
        import importlib.util
        script = ROOT / "scripts/verify_publications_index.py"
        spec = importlib.util.spec_from_file_location("publications_index_verifier", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def fixture():
        return """<!doctype html><html lang="en"><main><h1>Publications</h1>
        <div class="publications-index">
        <input id="bibsearch" type="search" hidden>
        <div id="publication-type-filters" hidden>
        <button data-publication-filter="all" aria-pressed="true"></button>
        <button data-publication-filter="article" aria-pressed="false"></button>
        <button data-publication-filter="inproceedings" aria-pressed="false"></button>
        <button data-publication-filter="phdthesis" aria-pressed="false"></button></div>
        <p id="bibsearch-status" role="status" aria-live="polite"></p>
        <p id="bibsearch-empty" hidden></p><button id="bibsearch-clear" hidden></button>
        <div id="publication-list">
        <section data-publication-category="article"><h2 id="journal-articles">Journal articles</h2>
        <h2 class="bibliography">2020</h2>
        <ol class="bibliography"><li><div id="Alpha">
        <script type="application/ld+json">{"@type":"ScholarlyArticle","name":"Example",
        "datePublished":"2020","author":[{"@type":"Person","name":"Author Example"}]}</script>
        <div class="title">Example</div></div></li></ol></section>
        <section data-publication-category="inproceedings"><h2 id="conference-contributions">Conferences</h2></section>
        <section data-publication-category="phdthesis"><h2 id="doctoral-thesis">Doctoral thesis</h2></section>
        </div><p id="Moda2022a">Rosenthal dataset</p></div></main></html>"""

    def test_generated_document_accepts_valid_single_entry(self):
        verifier = self.verifier()
        verifier.verify_document(self.fixture(),
                                 [{"key": "Alpha", "category": "article", "year": "2020", "doi": None}],
                                 "en")

    def test_generated_document_rejects_missing_entry(self):
        verifier = self.verifier()
        expected = [{"key": "Alpha", "category": "article", "year": "2020", "doi": None},
                    {"key": "Missing", "category": "article", "year": "2021", "doi": None}]
        with self.assertRaisesRegex(ValueError, "Missing"):
            verifier.verify_document(self.fixture(), expected, "en")

    def test_generated_document_accepts_percent_encoded_pdf_path(self):
        verifier = self.verifier()
        html = self.fixture().replace('<div class="title">Example</div>',
                                      '<div class="title">Example</div><a href="/assets/pdf/report%20name.pdf">PDF</a>')
        verifier.verify_document(html,
                                 [{"key": "Alpha", "category": "article", "year": "2020",
                                   "doi": None, "pdf": "report name.pdf"}], "en")

    def test_generated_document_rejects_wrong_category(self):
        verifier = self.verifier()
        with self.assertRaisesRegex(ValueError, "category|inproceedings"):
            verifier.verify_document(self.fixture(),
                                     [{"key": "Alpha", "category": "inproceedings", "year": "2020", "doi": None}],
                                     "en")

    def test_generated_verifier_rejects_missing_italian_route(self):
        import tempfile
        verifier = self.verifier()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            english = root / "publications/index.html"
            english.parent.mkdir(parents=True)
            english.write_text(self.fixture(), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Italian|it/publications"):
                verifier.verify_publications_index(root)

if __name__ == "__main__":
    unittest.main()
