"""Precompute FIG. R03 (ECP for sharp notches) by running the original sharCP scripts.

The website only draws the result. This script runs sharCP's own calibration and
prediction programs for Findley (FI), Fatemi-Socie (FS) and Smith-Watson-Topper (SWT),
then collects their output files into one JSON. No criterion is reimplemented here.

    git clone https://github.com/andreachiocca/sharCP && git -C sharCP checkout <commit>
    python -m pip install -r sharCP/requirements.txt
    python scripts/generate_sharcp_figure.py --sharcp sharCP --commit <commit>

Settings are the illustrative README commands with a common +/-2 sigma band; they are
not claimed to reproduce the calibration published in the associated article.
"""
import argparse
import csv
from datetime import date
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/sharcp-ecp-validation.json'
NSIGMA = 2.0
CRITERIA = {
    'FI': {'name': 'Findley', 'k': ('--kF', '0.30'), 'cal': 'calibrate_findley.py', 'pred': 'predict_findley.py',
           'cal_args': ['--planeI', 'strain', '--rcmin', '0.02', '--rcmax', '0.50', '--rcsteps', '40'], 'column': 'FI', 'tag': 'FINDLEY'},
    'FS': {'name': 'Fatemi–Socie', 'k': ('--kFS', '0.50'), 'cal': 'calibrate_fatemi_socie.py', 'pred': 'predict_fatemi_socie.py',
           'cal_args': ['--planeI', 'strain', '--rcmin', '0.02', '--rcmax', '0.50', '--rcsteps', '40'], 'column': 'FS', 'tag': 'FS'},
    'SWT': {'name': 'Smith–Watson–Topper', 'k': None, 'cal': 'calibrate_swt.py', 'pred': 'predict_swt.py',
            'cal_args': ['--plane', 'strain', '--rc_min', '0.02', '--rc_max', '0.50', '--rc_steps', '40'], 'column': 'SWT', 'tag': 'SWT'},
}


def run(script, args, cwd):
    env = dict(os.environ, MPLBACKEND='Agg')
    subprocess.run([sys.executable, str(cwd / 'scripts' / script), *args], cwd=cwd, env=env, check=True,
                   stdout=subprocess.DEVNULL)


def tex_macros(path):
    """Read \\def\\Name{value} macros written by the calibration scripts."""
    return {k: float(v) for k, v in re.findall(r'\\def\\([A-Za-z]+)\{([-+0-9.eE]+)\}', path.read_text())}


def calibration_points(caldir, tag):
    points = []
    for txt in sorted((caldir / 'Data').rglob(f'*_{tag}_*.txt')):
        mode, author = txt.relative_to(caldir / 'Data').parts[:2]
        with txt.open() as handle:
            next(handle)
            for line in handle:
                nf, value = line.split()[:2]
                points.append({'mode': mode, 'source': author, 'N': float(nf), 'P': float(value)})
    return points


def validation_points(preddir, column):
    rows = list(csv.DictReader(next(preddir.glob('prevision_points_*.csv')).open()))
    return [{'mode': r['Mode'], 'source': r['Author'], 'N': float(r['Nf']), 'P': float(r[column]),
             'location': r['Location'], 'alpha_deg': float(r['alpha_deg'])} for r in rows]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--sharcp', required=True, type=Path)
    ap.add_argument('--commit', required=True)
    args = ap.parse_args()
    repo = args.sharcp.resolve()
    figure = {'figure': 'FIG. R03', 'nsigma': NSIGMA,
              'source': {'repository': 'https://github.com/andreachiocca/sharCP', 'commit': args.commit,
                         'settings': 'README illustrative commands, global plane strain for Mode I, nsigma = 2'},
              'generated_on': date.today().isoformat(), 'criteria': {}}
    with tempfile.TemporaryDirectory() as tmp:
        for key, c in CRITERIA.items():
            caldir, preddir = Path(tmp) / 'cal' / key, Path(tmp) / 'pred' / key
            k = list(c['k']) if c['k'] else []
            run(c['cal'], ['--root', 'data/calibration', '--outdir', str(caldir), '--nsigma', str(NSIGMA), *c['cal_args'], *k], repo)
            run(c['pred'], ['--root', 'data/validation', '--calibdir', str(caldir), '--outdir', str(preddir), *k], repo)
            fit = tex_macros(next(caldir.glob('powerlaw_fit_*_all.tex')))
            prefix = 'FI' if key == 'FI' else 'FS'  # the SWT script reuses the FS macro prefix
            rc = fit.get(prefix + 'FitRcmm')
            if rc is None:  # SWT writes the radius only as a comment line
                rc = float(re.search(r'Best rc = ([0-9.eE+-]+)', next(caldir.glob('powerlaw_fit_*_all.tex')).read_text()).group(1))
            A, b, s = fit[prefix + 'FitA'], fit[prefix + 'Fitb'], fit[prefix + 'FitStdLn']
            assert math.isclose(fit[prefix + 'FitAplus'], A * math.exp(NSIGMA * s), rel_tol=1e-6), key
            val = validation_points(preddir, c['column'])
            # Band membership uses the script's own band constants (P = A_band * N^b).
            inside = sum(fit[prefix + 'FitAminus'] * p['N'] ** b <= p['P'] <= fit[prefix + 'FitAplus'] * p['N'] ** b for p in val)
            figure['criteria'][key] = {
                'name': c['name'], 'parameter_k': float(c['k'][1]) if c['k'] else None, 'rc_mm': rc,
                'A': A, 'b': b, 'std_ln': s, 'A_plus': fit[prefix + 'FitAplus'], 'A_minus': fit[prefix + 'FitAminus'],
                'T_ECP': fit[prefix + 'FitTECP'], 'calibration': calibration_points(caldir, c['tag']),
                'validation': val, 'validation_inside_band': inside,
            }
            print(f"{key}: rc={rc:.4f} mm  T={fit[prefix + 'FitTECP']:.2f}  validation inside band {inside}/{len(val)}")
    OUT.write_text(json.dumps(figure, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8')
    print('Wrote', OUT.relative_to(ROOT), f'{OUT.stat().st_size / 1024:.0f} kB')


if __name__ == '__main__':
    main()
