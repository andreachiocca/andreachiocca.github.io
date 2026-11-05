"""Precompute FIG. R04 (SeAn-CP search paths on the FS_ext damage sphere) with the original seancp code.

For each load case on the thick-walled tube of the SeAn-CP Phase 3 study, this script
stores, all computed by seancp itself:
  * FS_ext on a hemisphere grid of plane normals (seancp.evaluate_fs_ext),
  * the three SeAn-CP candidate-plane paths and the restricted maximum (seancp.seancp_fs_ext),
  * the independent full-plane reference maximum (seancp.full_plane_scan).
The website only draws the result.

    pip install "git+https://github.com/andreachiocca/SeAn-CP@<commit>"
    python scripts/generate_seancp_sphere.py --commit <commit>
"""
import argparse
import base64
from datetime import date
import hashlib
import json
from pathlib import Path

import numpy as np
from seancp import evaluate_fs_ext, full_plane_scan, harmonic_history, seancp_fs_ext
from seancp.study import StudyConfig, fixed_cases, random_cases

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/seancp-paths-fs-ext.json'
STEP_DEG = 3.0
ALGORITHM = 'mce'          # shear amplitude used by the Phase 3 reference ranking
RADIUS_MM = 7.5            # outer surface; governing radius of every case below
PATH_SAMPLES = 181         # seancp default resolution of each Mohr great circle
# Phase 3 cases with the largest SeAn-CP underprediction, plus two control histories.
CASES = ['control_axial_torsion_proportional', 'control_pressure_torsion_90',
         'mixed_90_0004', 'mean_shifted_0008', 'general_0012', 'torque_90_0014']


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--commit', required=True, help='SeAn-CP commit used for the run')
    args = ap.parse_args()
    config = StudyConfig()  # Phase 3 defaults: seed 23109, Sy = 900 MPa, k_FS = 0.4
    available = {c.case_id: c for c in fixed_cases() + random_cases(config, 18)}

    theta = np.radians(np.arange(0.0, 90.0 + 1e-9, STEP_DEG))
    phi = np.radians(np.arange(0.0, 360.0, STEP_DEG))
    tt, pp = np.meshgrid(theta, phi, indexing='ij')
    normals = np.stack([np.sin(tt) * np.cos(pp), np.sin(tt) * np.sin(pp), np.cos(tt)], -1).reshape(-1, 3)

    out_cases, fields = [], []
    for case_id in CASES:
        case = available[case_id]
        h = harmonic_history(config.geometry, config.material, case.loads, RADIUS_MM, end_condition=config.end_condition)
        kw = dict(k_fs=config.k_fs, sigma_y=config.sigma_y_mpa, algorithm=ALGORITHM)
        field = evaluate_fs_ext(h, normals, **kw)
        restricted = seancp_fs_ext(h, samples_per_path=PATH_SAMPLES, **kw)
        # Same resolution as the Phase 3 "fine" reference.
        ref_value, ref_normal = full_plane_scan(h, n_theta=121, n_phi=241, **kw)
        assert restricted.value <= ref_value * (1 + 2e-6), case_id
        fields.append(field / ref_value)
        # Families coincide when their great circles share a pole (same extreme eigenvectors).
        poles = []
        for path in restricted.paths:
            pole = np.cross(path.normals[0], path.normals[len(path.normals) // 2])
            poles.append(pole / np.linalg.norm(pole))
        coincident = all(abs(abs(float(np.dot(poles[0], q))) - 1) < 1e-6 for q in poles[1:])
        out_cases.append({
            'id': case_id, 'family': case.family,
            'fs_reference': ref_value, 'fs_seancp': restricted.value,
            'error_percent': 100 * (restricted.value / ref_value - 1),
            'reference_normal': [round(float(c), 5) for c in ref_normal],
            'seancp_normal': [round(float(c), 5) for c in restricted.normal],
            'field_max_ratio': round(float(field.max() / ref_value), 6),
            'paths_coincide': coincident,
            'paths': [{'family': p.family, 'best_ratio': round(p.best_value / ref_value, 6),
                       'normals': np.round(p.normals, 4).tolist()} for p in restricted.paths],
        })
        print(f'{case_id:38s} FS_ref={ref_value:.6g} FS_SeAn={restricted.value:.6g} err={out_cases[-1]["error_percent"]:+.3f}%')

    packed = np.concatenate([np.round(np.clip(f, 0, 1) * 255) for f in fields]).astype(np.uint8)
    payload = {
        'figure': 'FIG. R04',
        'quantity': 'FS_ext / FS_ext,ref (full-plane reference maximum)',
        'source': {'repository': 'https://github.com/andreachiocca/SeAn-CP', 'commit': args.commit,
                   'functions': ['seancp.evaluate_fs_ext', 'seancp.seancp_fs_ext', 'seancp.full_plane_scan'],
                   'study': 'Phase 3 thick-walled tube, seed 23109, StudyConfig defaults'},
        'parameters': {'k_fs': config.k_fs, 'sigma_y_mpa': config.sigma_y_mpa, 'algorithm': ALGORITHM,
                       'radius_mm': RADIUS_MM, 'note': 'illustrative material constants, not measured properties'},
        'grid': {'step_deg': STEP_DEG, 'n_theta': len(theta), 'n_phi': len(phi),
                 'order': 'case-major, then theta-major, then phi'},
        'cases': out_cases,
        'values_uint8_base64': base64.b64encode(packed.tobytes()).decode('ascii'),
        'values_sha256': hashlib.sha256(packed.tobytes()).hexdigest(),
        'generated_on': date.today().isoformat(),
    }
    OUT.write_text(json.dumps(payload, separators=(',', ':')) + '\n', encoding='utf8')
    print('Wrote', OUT.relative_to(ROOT), f'{OUT.stat().st_size / 1024:.0f} kB')


if __name__ == '__main__':
    main()
