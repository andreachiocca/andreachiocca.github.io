"""FIG. R04.1 data checks against the closed-form results of Moda et al., Materials & Design 223 (2022) 110991."""
import json
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/rosenthal-process-map.json').read_text(encoding='utf8'))
BETA, ETA = DATA['constants']['beta'], DATA['constants']['eta']


def lambert_w0(z):
    """Principal branch of the Lambert W function for z > 0 (Newton iteration)."""
    w = math.log1p(z)
    for _ in range(60):
        e = math.exp(w)
        w -= (w * e - z) / (e * (w + 1))
    return w


def ar_eq12(Ry):
    return (1 + (math.e * Ry / 8) ** (ETA / 2)) ** (1 / ETA)


def r_eq6(Ry):
    """Half-width R / l from Eq. (6)."""
    return Ry * (1 + (2 / (math.e * Ry)) ** (BETA / 2)) ** (1 / BETA)


class RosenthalMapTests(unittest.TestCase):
    def test_provenance(self):
        src = DATA['source']
        self.assertEqual(src['doi'], '10.1016/j.matdes.2022.110991')
        self.assertEqual(len(src['workbooks']), 2)
        for digest in src['workbooks'].values():
            self.assertRegex(digest, r'^[0-9a-f]{64}$')
        self.assertGreater(len(DATA['points']), 100)
        # Melting processes only: friction stir welding (solid state) and EBM are left out.
        self.assertEqual({p['process'] for p in DATA['points']}, {'AW', 'BW', 'LMD', 'SLM'})
        self.assertNotIn('FSW', {p['process_label'] for p in DATA['points']})
        self.assertLessEqual({p['family'] for p in DATA['points']}, {'steel', 'al', 'ti', 'ni', 'cu', 'co'})

    def test_rykalin_number_is_the_product_of_the_dimensionless_controls(self):
        # Eqs. (20, 21): Ry = P~ U~.
        for p in DATA['points']:
            self.assertAlmostEqual(p['Ry'], p['P_t'] * p['U_t'], delta=1e-5 * max(1, p['Ry']), msg=p['author'])

    def test_aspect_ratio_matches_eq12_within_its_stated_accuracy(self):
        # Eq. (12) is quoted within 1.994 %; the exact isotherm gives at most 2.01 % on this data
        # (cross-checked with a 30-digit solution), so 2.1 % bounds the comparison.
        for p in DATA['points']:
            self.assertAlmostEqual(p['Ar_eq12'], ar_eq12(p['Ry']), places=4)
            self.assertLess(abs(p['Ar'] - p['Ar_eq12']) / p['Ar'], 0.021, p['author'])

    def test_half_width_matches_eq6(self):
        for p in DATA['points']:
            exact = p['R_over_Rbar'] * p['U_t']  # R / l
            self.assertLess(abs(r_eq6(p['Ry']) - exact) / exact, 0.0075, p['author'])

    def test_every_point_satisfies_the_width_constraint(self):
        # Constraint (13)/(22): R >= R_ for the analysed operating conditions.
        for p in DATA['points']:
            self.assertGreaterEqual(p['R_over_Rbar'], 1 - 1e-6, p['author'])

    def test_outline_is_the_rosenthal_isotherm(self):
        for p in DATA['points']:
            Ry, R = p['Ry'], p['R_over_Rbar'] * p['U_t']
            pts = p['outline']
            # Tips of Eqs. (9, 10): X+ = W0(2 Ry) / 2 and X- = -Ry, in units of l.
            self.assertAlmostEqual(pts[0][0] * R, lambert_w0(2 * Ry) / 2, delta=1e-3 * R + 1e-6)
            self.assertAlmostEqual(pts[-1][0] * R, -Ry, delta=1e-3 * R + 1e-6)
            self.assertLessEqual(max(q[1] for q in pts), 1.001)
            for x, rho in pts[1:-1]:
                x, rho = x * R, rho * R
                r = math.hypot(x, rho)
                if rho < 1e-2 * R:
                    continue
                # Eq. (2): ln Ry - (r + x) - ln r = 0, up to the 3-decimal rounding of the outline.
                self.assertLess(abs(math.log(Ry) - (r + x) - math.log(r)), 4e-3 * R / min(r, 1) + 1e-3, p['author'])

    def test_boundary_and_isolines(self):
        for u, pt in DATA['boundary']:
            # Eq. (22) with equality on the R = R_ boundary.
            self.assertAlmostEqual(pt * (1 + (2 / (math.e * pt * u)) ** (BETA / 2)) ** (1 / BETA), 1, places=4)
        for iso in DATA['ar_isolines']:
            self.assertAlmostEqual(ar_eq12(iso['Ry']), iso['Ar'], places=4)

    def test_figure_is_bound_to_the_additive_chapter(self):
        areas = json.loads((ROOT / '_data/research_areas.json').read_text(encoding='utf8'))
        chapter = next(a for a in areas if a['id'] == 'additive-manufacturing-and-material-behaviour')
        self.assertIn('rosenthal_map.html', chapter.get('figures', []))
        en = json.loads((ROOT / '_data/i18n/en/rosenthal_map.json').read_text(encoding='utf8'))
        it = json.loads((ROOT / '_data/i18n/it/rosenthal_map.json').read_text(encoding='utf8'))
        self.assertEqual(set(en), set(it))
        self.assertEqual(set(en['families']), set(it['families']))
        self.assertEqual(set(en['processes']), {'AW', 'BW', 'LMD', 'SLM'})
        self.assertEqual(set(en['processes']), set(it['processes']))


if __name__ == '__main__':
    unittest.main()
