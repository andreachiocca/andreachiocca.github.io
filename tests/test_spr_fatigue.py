"""FIG. R05.1 data checks: test records, S-N fits of the article's structural stress and band ratio."""
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/spr-fatigue.json').read_text(encoding='utf8'))
VARIANTS = ('one_parameter', 'two_parameter')
# Row 5 of Data/FATICA/LAP/2_15_NO_GLUE/2_15_NO.txt reads Fmax 2860, Fmin 286, Fa 1400, Fm 1573: Fa and
# the stress column fit Fmax ~ 3111 N, Fmax/Fmin/Fm fit Fa = 1287 N. The article's stress uses Fa = 1400;
# the figure reproduces it until the author resolves the row.
KNOWN_FORCE_MISMATCH = {'LAP_2_15_NO_FILTERED_5'}


def fit(points):
    xs, ys = [math.log10(n) for n, _ in points], [math.log10(s) for _, s in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    return a, b, math.sqrt(sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)) / (n - 2))


class SprFatigueTests(unittest.TestCase):
    def test_records(self):
        tests = DATA['tests']
        self.assertEqual(len({t['id'] for t in tests}), len(tests))
        self.assertGreaterEqual(len(tests), 40)
        for t in tests:
            self.assertIn(t['geometry'], ('LAP', 'PEEL'))
            self.assertIn((t['t_al'], t['t_steel']), {(1.5, 1.5), (1.5, 1.8), (2.0, 1.5), (2.0, 1.8)})
            self.assertAlmostEqual(t['R'], 0.1)
            # Force amplitude at R = 0.1: Fa = (1 - R) Fmax / 2.
            consistent = math.isclose(t['Fa'], (1 - t['R']) * t['Fmax'] / 2, rel_tol=1e-9)
            self.assertEqual(consistent, t['id'] not in KNOWN_FORCE_MISMATCH, t['id'])
            self.assertGreater(t['N'], 0)
            self.assertEqual(set(t['sigma']), set(VARIANTS))

    def test_stored_curves_are_least_squares_fits(self):
        for v in VARIANTS:
            m = DATA['models'][v]
            a, b, sd = fit([(t['N'], t['sigma'][v]) for t in DATA['tests']])
            self.assertAlmostEqual(m['intercept'], a, places=4)
            self.assertAlmostEqual(m['slope'], b, places=4)
            self.assertLess(abs(m['sd_log10'] / sd - 1), 0.03)
            self.assertLess(m['slope'], 0)
            self.assertAlmostEqual(m['band_ratio'], 10 ** (2 * m['n_std'] * m['sd_log10']), places=9)

    def test_no_curve_on_the_raw_force(self):
        # Lap-shear and coach-peel joints form two populations in force: no single S-N curve is drawn.
        self.assertEqual(set(DATA['models']), set(VARIANTS))
        lap = [t['Fa'] for t in DATA['tests'] if t['geometry'] == 'LAP']
        peel = [t['Fa'] for t in DATA['tests'] if t['geometry'] == 'PEEL']
        self.assertGreater(min(lap), max(peel))

    def test_figure_is_bound_to_the_testing_chapter(self):
        areas = json.loads((ROOT / '_data/research_areas.json').read_text(encoding='utf8'))
        chapter = next(a for a in areas if a['id'] == 'component-testing-and-industrial-applications')
        self.assertIn('spr_fatigue.html', chapter.get('figures', []))
        en = json.loads((ROOT / '_data/i18n/en/spr_fatigue.json').read_text(encoding='utf8'))
        it = json.loads((ROOT / '_data/i18n/it/spr_fatigue.json').read_text(encoding='utf8'))
        self.assertEqual(set(en), set(it))
        self.assertEqual(set(en['views']), set(it['views']))


if __name__ == '__main__':
    unittest.main()
