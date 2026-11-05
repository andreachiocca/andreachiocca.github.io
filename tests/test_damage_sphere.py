"""FIG. T01 data checks: integrity, provenance and agreement with closed-form Findley solutions."""
import base64
import hashlib
import json
import re
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/damage-sphere-findley.json').read_text(encoding='utf8'))
K = DATA['parameters']['k_FI']
# Tolerance covers the 3 degree plane grid; the closed forms are exact maxima.
GRID_TOL = 2e-3


def case(lam, dphi):
    return next(c for c in DATA['cases'] if c['lambda'] == lam and c['dphi_deg'] == dphi)


class DamageSphereDataTests(unittest.TestCase):
    def test_payload_integrity(self):
        raw = base64.b64decode(DATA['values_uint8_base64'])
        grid = DATA['grid']
        self.assertEqual(len(raw), len(DATA['cases']) * grid['n_theta'] * grid['n_phi'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), DATA['values_sha256'])
        self.assertEqual(len(DATA['cases']), len(DATA['lambdas']) * len(DATA['phases_deg']))
        self.assertEqual(max(raw), 255)

    def test_provenance_is_pinned_and_shown(self):
        commit = DATA['source']['commit']
        self.assertRegex(commit, r'^[0-9a-f]{40}$')
        # Includes read the commit from _data/figure_sources.yml; it must match the data file.
        sources = (ROOT / '_data/figure_sources.yml').read_text(encoding='utf8')
        pinned = re.search(r'^damage_sphere:\n  repository: [^\n]+\n  commit: ([0-9a-f]{40})$', sources, re.M)
        self.assertIsNotNone(pinned)
        self.assertEqual(pinned.group(1), commit)
        self.assertIn('site.data.figure_sources.damage_sphere', (ROOT / '_includes/damage_sphere.html').read_text(encoding='utf8'))
        self.assertEqual(DATA['source']['function'], 'multifat.models.cp_methods.fin_harmonic.evaluate_findley')

    def test_uniaxial_matches_closed_form(self):
        # sigma_a only: DP*/sigma_a = (k + sqrt(1 + k^2)) / 2, on a cone of planes.
        expected = 0.5 * (K + math.sqrt(1 + K * K))
        for dphi in DATA['phases_deg']:
            self.assertAlmostEqual(case(0.0, dphi)['dp_max'], expected, delta=GRID_TOL)
        n = case(0.0, 0)['critical_normal']
        alpha = 0.5 * math.atan(1 / K)  # angle between the critical normal and the load axis
        self.assertAlmostEqual(math.degrees(math.acos(abs(n[0]))), math.degrees(alpha), delta=3.0)

    def test_proportional_matches_closed_form(self):
        # In-phase axial-torsional: DP*/sigma_a = k/2 + sqrt(1/4 + lambda^2) sqrt(1 + k^2).
        for lam in DATA['lambdas']:
            expected = K / 2 + math.sqrt(0.25 + lam * lam) * math.sqrt(1 + K * K)
            self.assertAlmostEqual(case(lam, 0)['dp_max'], expected, delta=GRID_TOL, msg=lam)

    def test_ninety_degrees_bounded_by_axial_plane(self):
        # On the plane normal to x: sigma_n,max = sigma_a and tau_a = lambda sigma_a.
        for lam in DATA['lambdas']:
            self.assertGreaterEqual(case(lam, 90)['dp_max'], lam + K - 1e-9)
        for lam in (0.5, 0.75, 1.0):
            self.assertAlmostEqual(case(lam, 90)['dp_max'], lam + K, delta=1e-6)

    def test_phase_shift_does_not_increase_findley_damage_here(self):
        # For this loading, out-of-phase shear lowers the Findley maximum (monotone in dphi).
        for lam in DATA['lambdas'][1:]:
            series = [case(lam, d)['dp_max'] for d in DATA['phases_deg']]
            self.assertTrue(all(a >= b - 1e-9 for a, b in zip(series, series[1:])), (lam, series))


if __name__ == '__main__':
    unittest.main()
