"""FIG. R03.1 data checks: provenance, band consistency and validation counts from sharCP outputs."""
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/sharcp-ecp-validation.json').read_text(encoding='utf8'))


class SharcpFigureDataTests(unittest.TestCase):
    def test_provenance_is_pinned_and_shown(self):
        commit = DATA['source']['commit']
        self.assertRegex(commit, r'^[0-9a-f]{40}$')
        include = (ROOT / '_includes/sharcp_figure.html').read_text(encoding='utf8')
        self.assertIn(commit, include)
        self.assertIn(commit[:7], include)

    def test_three_criteria_share_the_same_tests(self):
        self.assertEqual(set(DATA['criteria']), {'FI', 'FS', 'SWT'})
        counts = {(len(c['calibration']), len(c['validation'])) for c in DATA['criteria'].values()}
        self.assertEqual(counts, {(165, 55)})

    def test_band_is_the_scripts_two_sigma_band(self):
        for key, c in DATA['criteria'].items():
            self.assertLess(c['b'], 0, key)
            self.assertAlmostEqual(c['A_plus'] / c['A'], math.exp(DATA['nsigma'] * c['std_ln']), delta=1e-6 * c['A_plus'] / c['A'])
            self.assertAlmostEqual(c['A_minus'] / c['A'], math.exp(-DATA['nsigma'] * c['std_ln']), delta=1e-6)

    def test_inside_band_count_matches_points(self):
        for key, c in DATA['criteria'].items():
            inside = sum(c['A_minus'] * p['N'] ** c['b'] <= p['P'] <= c['A_plus'] * p['N'] ** c['b'] for p in c['validation'])
            self.assertEqual(inside, c['validation_inside_band'], key)

    def test_values_are_physical(self):
        for key, c in DATA['criteria'].items():
            self.assertTrue(0 < c['rc_mm'] < 1, key)
            for p in c['calibration'] + c['validation']:
                self.assertGreater(p['N'], 0)
                self.assertGreater(p['P'], 0)
                self.assertIn(p['mode'], ('MI', 'MIII'))


if __name__ == '__main__':
    unittest.main()
