"""FIG. R02.1 data checks: provenance, Phase 3 reference values and SeAn-CP path geometry."""
import base64
import hashlib
import json
import re
import math
from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
DATA = json.loads((ROOT / 'assets/data/figures/seancp-paths-fs-ext.json').read_text(encoding='utf8'))
CASES = {c['id']: c for c in DATA['cases']}


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# fs_ext_reference / fs_ext_seancp from SeAn-CP results/phase3_reference/worst_four.csv (fine quality).
PHASE3_REFERENCE = {
    'torque_90_0014': (0.002441848476154973, 0.002349831395870753),
    'general_0012': (0.001465656559314127, 0.001416643684674431),
    'mean_shifted_0008': (0.0026022283934308043, 0.002559679037453598),
    'mixed_90_0004': (0.0013581410967782896, 0.001347723385505632),
}


class SeancpSphereDataTests(unittest.TestCase):
    def test_provenance_is_pinned_and_shown(self):
        commit = DATA['source']['commit']
        self.assertRegex(commit, r'^[0-9a-f]{40}$')
        # Includes read the commit from _data/figure_sources.yml; it must match the data file.
        sources = (ROOT / '_data/figure_sources.yml').read_text(encoding='utf8')
        pinned = re.search(r'^seancp_sphere:\n  repository: [^\n]+\n  commit: ([0-9a-f]{40})$', sources, re.M)
        self.assertIsNotNone(pinned)
        self.assertEqual(pinned.group(1), commit)
        self.assertIn('site.data.figure_sources.seancp_sphere', (ROOT / '_includes/seancp_sphere.html').read_text(encoding='utf8'))

    def test_payload_integrity(self):
        raw = base64.b64decode(DATA['values_uint8_base64'])
        grid = DATA['grid']
        self.assertEqual(len(raw), len(DATA['cases']) * grid['n_theta'] * grid['n_phi'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), DATA['values_sha256'])

    def test_reproduces_the_phase3_reference_table(self):
        for case_id, (reference, seancp) in PHASE3_REFERENCE.items():
            self.assertAlmostEqual(CASES[case_id]['fs_reference'] / reference, 1, delta=1e-5, msg=case_id)
            self.assertAlmostEqual(CASES[case_id]['fs_seancp'] / seancp, 1, delta=1e-5, msg=case_id)

    def test_restricted_search_never_exceeds_the_reference(self):
        for case in DATA['cases']:
            self.assertLessEqual(case['fs_seancp'], case['fs_reference'] * (1 + 2e-6), case['id'])
            self.assertAlmostEqual(case['error_percent'], 100 * (case['fs_seancp'] / case['fs_reference'] - 1), places=9)
        for control in ('control_axial_torsion_proportional', 'control_pressure_torsion_90'):
            self.assertAlmostEqual(CASES[control]['error_percent'], 0, delta=1e-4)

    def test_paths_are_great_circles_of_unit_normals(self):
        for case in DATA['cases']:
            self.assertEqual(len(case['paths']), 3)
            for path in case['paths']:
                n = path['normals']
                self.assertTrue(all(abs(math.sqrt(dot(v, v)) - 1) < 1e-3 for v in n))
                pole = cross(n[0], n[len(n) // 2]); norm = math.sqrt(dot(pole, pole))
                self.assertLess(max(abs(dot(v, pole)) / norm for v in n), 2e-3, case['id'])
            best = max(p['best_ratio'] for p in case['paths'])
            self.assertAlmostEqual(best, case['fs_seancp'] / case['fs_reference'], delta=2e-6)


if __name__ == '__main__':
    unittest.main()
