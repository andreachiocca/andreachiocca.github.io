"""Precompute FIG. R05.1 (fatigue of hybrid self-piercing-riveted joints) from the article's outputs.

The website only draws the result. Inputs are the outputs of the fatigue-assessment scripts of the
manuscript "Fatigue resistance of hybrid self-piercing-riveted aluminium-steel joints" (in
preparation; tests run by A. Chiocca within a PRIN project): one row per fatigue test with the
applied force and the Rupp-type structural stress of each assessment variant, plus the fitted
S-N curve and its scatter. Nothing is recomputed except the checks below.

    python scripts/generate_spr_fatigue.py --outputs "<article folder>/fatigue_assessment_output"

One raw row with inconsistent forces is corrected from its confirmed force amplitude (FA_CONFIRMED).

Checks: every test appears once in both variants with the same force and life; the stored S-N
intercept, slope and standard deviation reproduce a least-squares fit of log10(sigma) on log10(N)
of the same points.

Repository choices:
  - the plotted stress is `sigma_global_MPa`, the quantity of the article's S-N plots;
  - the scatter band is the article's mean +/- 2 standard deviations of log10(sigma); `band_ratio`
    is the ratio of its upper to its lower bound at the same life.
"""
import argparse
import csv
from datetime import date
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/spr-fatigue.json'
VARIANTS = ('one_parameter', 'two_parameter')
# Row 5 of Data/FATICA/LAP/2_15_NO_GLUE/2_15_NO.txt reads Fmax 2860, Fmin 286, Fa 1400, Fm 1573 N. The
# author confirmed (2026-11-06) that Fa = 1400 N, used by the article, is correct: Fmax is 3111 N.
FA_CONFIRMED = {'LAP_2_15_NO_FILTERED_5'}


def rows(path):
    with path.open(encoding='utf8', newline='') as handle:
        return [{k.strip(): v for k, v in r.items() if k} for r in csv.DictReader(handle)]


def fit(points):
    """Least squares log10(sigma) = a + b log10(N); returns a, b and the sample standard deviation."""
    xs, ys = [math.log10(n) for n, _ in points], [math.log10(s) for _, s in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = my - b * mx
    sd = math.sqrt(sum((y - a - b * x) ** 2 for x, y in zip(xs, ys)) / (n - 2))
    return a, b, sd


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--outputs', type=Path, required=True, help='fatigue_assessment_output folder')
    args = ap.parse_args()
    summary = {r['assessment_variant']: r for r in rows(args.outputs / 'optimized_weights_and_sn_summary.csv')}
    tests, models = {}, {}
    for variant in VARIANTS:
        pts = []
        for r in rows(args.outputs / f'structural_stress_results_{variant}.csv'):
            key = r['test_id']
            rec = tests.setdefault(key, {
                'id': key, 'geometry': r['geometry'], 'adhesive': r['glue'] == 'YES',
                't_al': float(r['t_al_mm']), 't_steel': float(r['t_steel_mm']),
                'Fa': float(r['Fa_N']), 'Fmax': float(r['Fmax_N']), 'R': float(r['Load_Ratio']),
                'N': float(r['N_failure']), 'sigma': {},
            })
            if rec['Fa'] != float(r['Fa_N']) or rec['N'] != float(r['N_failure']):
                raise SystemExit(f'{key}: force or life differ between variants')
            rec['sigma'][variant] = round(float(r['sigma_global_MPa']), 4)
            pts.append((rec['N'], float(r['sigma_global_MPa'])))
        s = summary[variant]
        a, b, sd = float(s['sn_intercept_log10_sigma']), float(s['sn_slope_log10sigma_vs_log10N']), float(s['std_log10_sigma'])
        fa, fb, fsd = fit(pts)
        # The stored curve must be the least-squares fit of these points (sd within the n-1 / n-2 choice).
        if not (math.isclose(a, fa, rel_tol=1e-6) and math.isclose(b, fb, rel_tol=1e-6) and abs(sd / fsd - 1) < 0.03):
            raise SystemExit(f'{variant}: stored S-N fit {a, b, sd} differs from {fa, fb, fsd}')
        k = float(s['scatter_n_std'])
        models[variant] = {
            'intercept': a, 'slope': b, 'sd_log10': sd, 'n_std': k, 'n': len(pts),
            'band_ratio': 10 ** (2 * k * sd), 'R2': float(s['R2_loglog']),
            'weights': {w: float(s[w]) for w in ('SFs', 'SFz', 'SFb', 'WGn', 'WGs')},
        }
    # Author-confirmed corrections of the raw data: the force amplitude is right, the other forces of
    # the row are typos, so they are rebuilt from Fa and R.
    for key in FA_CONFIRMED:
        t = tests[key]
        t['Fmax'] = round(2 * t['Fa'] / (1 - t['R']), 3)
    for t in tests.values():
        if not math.isclose(t['Fa'], (1 - t['R']) * t['Fmax'] / 2, rel_tol=1e-6):
            raise SystemExit(f'{t["id"]}: Fa = {t["Fa"]} N but (1 - R) Fmax / 2 = {(1 - t["R"]) * t["Fmax"] / 2:g} N')
    missing = [t for t in tests.values() if set(t['sigma']) != set(VARIANTS)]
    if missing:
        raise SystemExit(f'Tests missing a variant: {[t["id"] for t in missing]}')
    data = {
        'figure': 'FIG. R05.1',
        'source': {
            'manuscript': 'Fatigue resistance of hybrid self-piercing-riveted aluminium-steel joints (in preparation)',
            'outputs': 'fatigue_assessment_output', 'generated': date.today().isoformat(),
            'materials': {'aluminium': 'Al 5005', 'steel': 'Fe P05', 'adhesive': 'Terokal 4497'},
        },
        'models': models,
        'tests': sorted(tests.values(), key=lambda t: (t['geometry'], t['adhesive'], t['t_al'], t['t_steel'], t['N'])),
    }
    OUT.write_text(json.dumps(data, indent=1) + '\n', encoding='utf8')
    print(f'Wrote {OUT.relative_to(ROOT)}: {len(tests)} tests; ' +
          ', '.join(f'{v}: band ratio={m["band_ratio"]:.3f}' for v, m in models.items()))


if __name__ == '__main__':
    main()
