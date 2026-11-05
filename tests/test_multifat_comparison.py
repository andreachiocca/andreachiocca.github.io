"""FIG. R02.2 data checks: provenance, structure and internal consistency of the multifat statistics."""
import json
import math
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/multifat-comparison.json').read_text(encoding='utf8'))
INCLUDE = (ROOT / '_includes/multifat_comparison.html').read_text(encoding='utf8')


class MultifatComparisonDataTests(unittest.TestCase):
    def test_provenance_is_pinned_and_shown(self):
        commit = DATA['source']['commit']
        self.assertRegex(commit, r'^[0-9a-f]{40}$')
        sources = (ROOT / '_data/figure_sources.yml').read_text(encoding='utf8')
        pinned = re.search(r'^multifat_comparison:\n  repository: [^\n]+\n  commit: ([0-9a-f]{40})$', sources, re.M)
        self.assertIsNotNone(pinned)
        self.assertEqual(pinned.group(1), commit)
        self.assertIn('site.data.figure_sources.multifat_comparison', INCLUDE)
        self.assertEqual(DATA['source']['repository'], 'andreachiocca/multiaxial-fatigue')

    def test_only_assessment_load_errors(self):
        # Design points would measure calibration fit, not prediction; e_L is the slope-independent metric.
        self.assertEqual(DATA['metric']['name'], 'Error_load')
        self.assertEqual(DATA['metric']['role'], 'assessment')

    def test_cells_reference_listed_methods_and_materials(self):
        methods = {m['id'] for m in DATA['methods']}
        materials = {m['id'] for m in DATA['materials']}
        self.assertGreaterEqual(len(methods), 10)
        self.assertGreaterEqual(len(materials), 2)
        keys = [(c['method'], c['material']) for c in DATA['cells']]
        self.assertEqual(len(keys), len(set(keys)), 'duplicate cells')
        for method, material in keys:
            self.assertIn(method, methods)
            self.assertIn(material, materials)
        self.assertEqual(methods, {c['method'] for c in DATA['cells']})

    def test_methods_are_grouped_by_family(self):
        order = [DATA['families'].index(m['family']) for m in DATA['methods']]
        self.assertEqual(order, sorted(order))

    def test_shares_are_test_fractions(self):
        # Within-band shares are k/n for an integer k, and the 20 % band contains the 10 % band.
        for c in DATA['cells']:
            n = c['n']
            self.assertGreater(n, 0)
            self.assertLessEqual(n, next(m['assessment_tests'] for m in DATA['materials'] if m['id'] == c['material']))
            for key in ('within10', 'within20'):
                share = c[key]
                self.assertTrue(0 <= share <= 1, c)
                self.assertAlmostEqual(share * n, round(share * n), places=6, msg=c)
            self.assertLessEqual(c['within10'], c['within20'])
            self.assertTrue(math.isfinite(c['mean']))
            if n > 1:
                self.assertGreaterEqual(c['sd'], 0)

    def test_mean_bias_is_compatible_with_the_bands(self):
        # If every test is within +/-10 % of the load, |e_L| <= ln(1.1) for each, so the mean is too.
        for c in DATA['cells']:
            if c['within10'] == 1:
                self.assertLessEqual(abs(c['mean']), math.log(1 / 0.9) + 1e-12, c)

    def test_complexity_facets_are_declared(self):
        # Complexity is reported beside the score, as declared by multifat, never as a fitted score.
        for m in DATA['methods']:
            self.assertIn(m['inputs'], ('stress', 'stress_strain'), m['id'])
            self.assertIn(m['life_law'], ('master_curve', 'native'), m['id'])
            self.assertIsInstance(m['constants'], list)
            self.assertIsInstance(m['optional_constants'], list)
            if m['inputs'] == 'stress':
                self.assertNotIn('E', m['constants'], m['id'])
        self.assertNotIn('score', json.dumps(DATA['methods']))

    def test_figure_is_bound_to_the_multiaxial_chapter(self):
        areas = json.loads((ROOT / '_data/research_areas.json').read_text(encoding='utf8'))
        chapter = next(a for a in areas if a['id'] == 'multiaxial-fatigue-and-critical-plane-methods')
        self.assertIn('multifat_comparison.html', chapter.get('figures', []))

    def test_strings_are_localised(self):
        en = json.loads((ROOT / '_data/i18n/en/multifat_comparison.json').read_text(encoding='utf8'))
        it = json.loads((ROOT / '_data/i18n/it/multifat_comparison.json').read_text(encoding='utf8'))
        self.assertEqual(set(en), set(it))
        self.assertEqual(set(en['families']), set(DATA['families']))
        self.assertEqual(set(it['families']), set(DATA['families']))


if __name__ == '__main__':
    unittest.main()
