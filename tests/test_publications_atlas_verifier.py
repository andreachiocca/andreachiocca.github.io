"""Mutation tests for generated Publications-page checks."""

import tempfile
import unittest
from pathlib import Path

from scripts.verify_publications_atlas import verify_publications_atlas


def fixture(lang):
    sections = (("article", "journal-articles", "PaperA", "10.1234/paper"),
                ("inproceedings", "conference-contributions", "PaperB", None),
                ("phdthesis", "doctoral-thesis", "ThesisC", None))
    links = "".join(f'<a href="#{anchor}">{anchor}</a>' for _, anchor, _, _ in sections)
    controls = "".join(f'<button data-publication-type="{kind}">{kind}</button>'
                       for kind in ("all", "article", "inproceedings", "phdthesis"))
    records = "".join(
        f'<section class="publication-section" data-publication-type="{kind}"><h2 id="{anchor}"></h2>'
        f'<ol class="bibliography"><li><div id="{key}" data-publication-keywords="test">'
        + (f'<a href="https://doi.org/{doi}">DOI</a>' if doi else "")
        + "</div></li></ol></section>"
        for kind, anchor, key, doi in sections)
    catalogue = '/it/repositories/' if lang == 'it' else '/repositories/'
    return (f'<html lang="{lang}"><main><div class="publication-atlas"><h1>Publications</h1>'
            f'<a href="{catalogue}">Research outputs</a>'
            f'<nav class="publication-index">{links}</nav><div class="publication-controls" hidden>'
            f'{controls}</div><div id="publication-list">{records}</div></div></main></html>')


class PublicationsVerifierTests(unittest.TestCase):
    def test_accepts_canonical_pair_and_rejects_missing_record_or_doi(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bib = root / "papers.bib"
            bib.write_text("@article{PaperA,\n  doi = {10.1234/paper}\n}\n"
                           "@inproceedings{PaperB,\n}\n@phdthesis{ThesisC,\n}\n", encoding="utf-8")
            en = root / "publications/index.html"
            it = root / "it/publications/index.html"
            en.parent.mkdir(parents=True)
            it.parent.mkdir(parents=True)
            en.write_text(fixture("en"), encoding="utf-8")
            it.write_text(fixture("it"), encoding="utf-8")
            verify_publications_atlas(root, bib)
            it.write_text(fixture("it").replace('id="PaperB"', 'id="LostB"'), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "publication keys differ"):
                verify_publications_atlas(root, bib)
            it.write_text(fixture("it").replace("https://doi.org/10.1234/paper", "https://example.org/paper"), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "DOI link missing"):
                verify_publications_atlas(root, bib)


if __name__ == "__main__":
    unittest.main()
