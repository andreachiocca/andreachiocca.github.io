"""Precompute the Findley damage sphere (FIG. R02) with the original multifat code.

Every plane value comes from multifat's own ``evaluate_findley`` called on a single
candidate plane, so the website reimplements no fatigue criterion. The browser only
draws the stored grid. Run inside an environment where multifat is installed at the
pinned commit:

    pip install "git+https://github.com/andreachiocca/multiaxial-fatigue@<commit>"
    python scripts/generate_damage_sphere.py --commit <commit>

Loading (zero mean, R = -1, normalised by sigma_a):
    sigma_xx(t) = sigma_a sin(wt),  tau_xy(t) = lambda sigma_a sin(wt - dphi)
"""
import argparse
import base64
from datetime import date
import hashlib
import json
from pathlib import Path

import numpy as np
from multifat.models.cp_methods.fin_harmonic import evaluate_findley
from multifat.planes.sampling import gentang

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/damage-sphere-findley.json'
K_FI = 0.3                      # Illustrative Findley coefficient, not a material calibration.
LAMBDAS = [0.0, 0.25, 0.5, 0.75, 1.0]
PHASES_DEG = [0, 15, 30, 45, 60, 75, 90]
STEP_DEG = 3.0
ZERO = np.zeros((3, 3))


def harmonics(lam, dphi_deg):
    """Sine/cosine stress coefficients of the axial-torsional history."""
    d = np.radians(dphi_deg)
    s_sin, s_cos = np.zeros((3, 3)), np.zeros((3, 3))
    s_sin[0, 0] = 1.0
    s_sin[0, 1] = s_sin[1, 0] = lam * np.cos(d)
    s_cos[0, 1] = s_cos[1, 0] = -lam * np.sin(d)
    return s_sin, s_cos


def findley(s_sin, s_cos, frames):
    kwargs = dict(S0=s_sin, E0=ZERO, S1=-s_sin, E1=ZERO, params={'k_FI': K_FI},
                  harmonics={'S_mean': ZERO, 'S_sin': s_sin, 'S_cos': s_cos},
                  shear_amplitude_algorithm='mcc_harmonic')
    return evaluate_findley(R_list=frames, **kwargs).values['']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit', required=True, help='multiaxial-fatigue commit used for the run')
    args = parser.parse_args()

    # Hemisphere of plane normals: n and -n describe the same material plane.
    theta = np.radians(np.arange(0.0, 90.0 + 1e-9, STEP_DEG))
    phi = np.radians(np.arange(0.0, 360.0, STEP_DEG))
    tt, pp = np.meshgrid(theta, phi, indexing='ij')
    normals = np.stack([np.sin(tt) * np.cos(pp), np.sin(tt) * np.sin(pp), np.cos(tt)], -1).reshape(-1, 3)
    frames = np.asarray(gentang(normals, return_matrices=True))
    assert np.allclose(frames[:, :, 2], normals), 'gentang must use the normal as local z'

    cases, fields = [], []
    for lam in LAMBDAS:
        for dphi in PHASES_DEG:
            s_sin, s_cos = harmonics(lam, dphi)
            values = np.array([findley(s_sin, s_cos, [frame]) for frame in frames])
            # Cross-check: the library's own search over the same grid finds the same maximum.
            best = findley(s_sin, s_cos, list(frames))
            assert abs(best - values.max()) < 1e-12, (lam, dphi, best, values.max())
            i = int(values.argmax())
            cases.append({'lambda': lam, 'dphi_deg': dphi, 'dp_max': round(float(values.max()), 6),
                          'dp_min': round(float(values.min()), 6),
                          'critical_normal': [round(float(c), 6) for c in normals[i]]})
            fields.append(values)
            print(f'lambda={lam:.2f} dphi={dphi:2d}  DP*/sigma_a={values.max():.4f}  n*={normals[i].round(3)}')

    # One global scale keeps colours comparable across load cases.
    vmax = float(max(field.max() for field in fields))
    packed = np.concatenate([np.round(field / vmax * 255.0) for field in fields]).astype(np.uint8)
    payload = {
        'figure': 'FIG. R02',
        'quantity': 'Findley damage parameter DP / sigma_a',
        'source': {'repository': 'https://github.com/andreachiocca/multiaxial-fatigue', 'commit': args.commit,
                   'function': 'multifat.models.cp_methods.fin_harmonic.evaluate_findley',
                   'shear_amplitude_algorithm': 'mcc_harmonic', 'plane_frames': 'multifat.planes.sampling.gentang'},
        'loading': 'sigma_xx = sigma_a sin(wt); tau_xy = lambda sigma_a sin(wt - dphi); zero mean',
        'parameters': {'k_FI': K_FI, 'note': 'illustrative coefficient, not a material calibration'},
        'grid': {'step_deg': STEP_DEG, 'n_theta': len(theta), 'n_phi': len(phi),
                 'theta': 'polar angle of the normal from +z, 0..90 deg', 'phi': 'azimuth from +x, 0..357 deg',
                 'order': 'case-major, then theta-major, then phi'},
        'lambdas': LAMBDAS, 'phases_deg': PHASES_DEG, 'value_scale_max': round(vmax, 6),
        'cases': cases,
        'values_uint8_base64': base64.b64encode(packed.tobytes()).decode('ascii'),
        'generated_on': date.today().isoformat(),
    }
    payload['values_sha256'] = hashlib.sha256(packed.tobytes()).hexdigest()
    OUT.write_text(json.dumps(payload, separators=(',', ':')) + '\n', encoding='utf8')
    print('Wrote', OUT.relative_to(ROOT), f'{OUT.stat().st_size / 1024:.0f} kB')


if __name__ == '__main__':
    main()
