"""Precompute FIG. R02.2 (multiaxial criteria compared across materials) from the multifat pipeline.

The website only draws the result. This script runs the owner's `multifat-pipeline --all`
(validate, calibrate, run every model, compare) on the repository's experimental workbooks and
collects the load-equivalent error statistics it writes. Nothing is recomputed here.

    git clone https://github.com/andreachiocca/multiaxial-fatigue mf && git -C mf checkout <commit>
    python -m pip install ./mf
    python scripts/generate_multifat_comparison.py --multifat mf --commit <commit>

Metric: e_L = ln(1/s*), where s* scales the load history so that the calibrated method predicts
the observed life (multifat.eval.load_error). Only assessment observations (Flag = 1, failures
that were not used to calibrate) enter the statistics; design points and run-outs are excluded.
Workbooks with fatigue-limit rows only have no life-based e_L and are not part of this matrix.
"""
import argparse
import csv
from datetime import date
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/multifat-comparison.json'
METRIC, ROLE = 'Error_load', 'assessment'
# Display order of the method families (module folders of multifat.models).
FAMILIES = ['cp_methods', 'invariant_methods', 'integral_methods', 'energy_based_methods']


def run_pipeline(clone, results, jobs):
    env = dict(os.environ, MPLBACKEND='Agg')
    cmd = [sys.executable, '-m', 'multifat.cli.pipeline', '--all', '--jobs', str(jobs), '--results-dir', str(results)]
    # The pipeline exits non-zero when one model fails on one material; the summary is still written.
    code = subprocess.run(cmd, cwd=clone, env=env, stdout=subprocess.DEVNULL).returncode
    if not (results / 'Comparison/summary_error_stats_by_role.csv').is_file():
        raise SystemExit(f'multifat-pipeline wrote no comparison (exit {code})')
    return code


def method_info():
    """Family and citation of every registered method, read from the installed multifat."""
    from multifat.models import registry
    from multifat.models.references import method_reference
    models = {**registry._available_cp_methods(), **registry._available_direct_models()}
    info = {}
    for key, model in models.items():
        ref = method_reference(key)
        info[key] = {'family': type(model).__module__.split('.')[2], 'citation': ref['citation'], 'url': ref['url']}
    return info


def number(text):
    value = float(text) if text not in ('', None) else math.nan
    return value if math.isfinite(value) else None


def collect(results):
    rows = []
    with (results / 'Comparison/summary_error_stats_by_role.csv').open(encoding='utf8') as handle:
        for row in csv.DictReader(handle):
            if row['Metric'] == METRIC and row['Observation_role'] == ROLE and int(row['n']) > 0:
                rows.append(row)
    if not rows:
        raise SystemExit('No assessment load errors in the comparison table')
    return rows


def build(rows, info, commit, exit_code):
    base = lambda m: m.removesuffix('_ext')
    unknown = sorted({base(r['Method']) for r in rows} - set(info))
    if unknown:
        raise SystemExit(f'Methods missing from the multifat registry: {unknown}')
    cells = [{
        'material': r['Material'], 'method': r['Method'], 'n': int(r['n']),
        'mean': number(r['Error_mean']), 'sd': number(r['Error_std']),
        'within10': number(r['Within_10pct']), 'within20': number(r['Within_20pct']),
    } for r in rows]
    # Materials: most assessment tests first; methods: by family, then best median within-10 % share.
    tests = {}
    for c in cells:
        tests[c['material']] = max(tests.get(c['material'], 0), c['n'])
    materials = sorted(tests, key=lambda m: (-tests[m], m))

    def median(values):
        values = sorted(values)
        k = len(values)
        return (values[(k - 1) // 2] + values[k // 2]) / 2 if k else 0.0

    score = {}
    for c in cells:
        score.setdefault(c['method'], []).append(c['within10'] or 0.0)
    methods = sorted(score, key=lambda m: (FAMILIES.index(info[base(m)]['family']), -median(score[m]), m))
    return {
        'figure': 'multifat_comparison',
        'source': {
            'repository': 'andreachiocca/multiaxial-fatigue', 'commit': commit,
            'command': 'multifat-pipeline --all', 'table': 'Results/current/Comparison/summary_error_stats_by_role.csv',
            'pipeline_exit_code': exit_code, 'generated': date.today().isoformat(),
        },
        'metric': {'name': METRIC, 'role': ROLE, 'definition': 'e_L = ln(1/s*)',
                   'within': '|1/s* - 1| <= 0.10 or 0.20'},
        'families': FAMILIES,
        'materials': [{'id': m, 'assessment_tests': tests[m]} for m in materials],
        'methods': [{'id': m, **info[base(m)]} for m in methods],
        'cells': sorted(cells, key=lambda c: (materials.index(c['material']), methods.index(c['method']))),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--multifat', type=Path, required=True, help='clone of multiaxial-fatigue at --commit')
    ap.add_argument('--commit', required=True, help='full commit hash of the clone')
    ap.add_argument('--results', type=Path, help='reuse an existing pipeline results folder instead of running it')
    ap.add_argument('--jobs', type=int, default=os.cpu_count() or 1)
    args = ap.parse_args()
    head = subprocess.run(['git', '-C', str(args.multifat), 'rev-parse', 'HEAD'], capture_output=True, text=True, check=True).stdout.strip()
    if head != args.commit:
        raise SystemExit(f'Clone is at {head}, not {args.commit}')
    with tempfile.TemporaryDirectory() as tmp:
        results = args.results or Path(tmp) / 'results'
        code = None if args.results else run_pipeline(args.multifat.resolve(), results.resolve(), args.jobs)
        data = build(collect(results), method_info(), args.commit, code)
    OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + '\n', encoding='utf8')
    print(f'Wrote {OUT.relative_to(ROOT)}: {len(data["methods"])} methods x {len(data["materials"])} materials')


if __name__ == '__main__':
    main()
