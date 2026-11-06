"""Precompute FIG. R04.1 (Rosenthal map of metal additive manufacturing) from the literature dataset.

The website only draws the result. Equations are those of Moda, Chiocca, Macoretta, Monelli and
Bertini, Materials & Design 223 (2022) 110991 (doi:10.1016/j.matdes.2022.110991), cited by number:

    Ry = P U / (4 pi lambda alpha dTm)                                   (4)
    U~ = U R_ / (2 alpha),   P~ = P / (2 pi lambda R_ dTm),  Ry = P~ U~   (20, 21)
    melt isotherm:  (l / r) exp(-(r + x) / l) = 1 / Ry,  l = 2 alpha / U  (2, 3)
    X+ = (l / 2) W0(2 Ry),  X- = -l Ry                                   (9, 10)
    A_r ~ [1 + (e Ry / 8)^(eta/2)]^(1/eta),  eta = 1.904                 (12)
    R = R_ boundary:  U~ = 2 / (e P~) (P~^-beta - 1)^(-2/beta), beta = -1.7312   (22, 24)

Input: the review workbook (sheet "Parametri"), whose rows hold the nominal operating conditions
of each cited paper with the thermophysical properties used. U~ and P~ are recomputed here from the
raw columns and checked against the workbook's own values. The melt-pool outline of each point is
the exact isotherm of Eq. (2) in its polar Lambert-W form; A_r is reported exact and from Eq. (12).

    python scripts/generate_rosenthal_map.py --workbook Parametri_letteratura_rev_5.xlsx

Repository choices:
  - processes: SLM and LMD (LMwD, wire-fed, is kept and labelled as such). EBM rows are left out,
    as in the article, because few of them have complete parameters;
  - rows without a process, a material or complete inputs are dropped and counted, and so are rows
    the workbook itself leaves without U*, P* (not part of its analysed selection);
  - power is the nominal power (the workbook's absorptivity column is 1 throughout), so P~ is an
    upper bound of the absorbed power, as for the markers of the article's Fig. 5.
"""
import argparse
from datetime import date
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar
from scipy.special import lambertw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/data/figures/rosenthal-process-map.json'
BETA, ETA = -1.7312, 1.904
PROCESSES = {'SLM': 'SLM', 'LMD': 'LMD', 'LMwD': 'LMD'}
# Material families of the article's Fig. 5, assigned from the alloy names used in the workbook.
FAMILIES = [
    ('ni', ('inconel', 'hastelloy', 'waspalloy')),
    ('ti', ('ti6al4v', 'ti ', 'ti-')),
    ('co', ('co-cr', 'cocr', 'stellite')),
    ('cu', ('cu', 'bronze', 'cusn')),
    ('al', ('al', 'aa', 'scalmalloy')),
    ('steel', ('aisi', 'h13', 'maraging', '17-4', 'steel', '316', '304')),
]


def family(material):
    name = material.lower().strip() + ' '
    if name.startswith('ti'):
        return 'ti'
    for key, tokens in FAMILIES:
        if any(name.startswith(t) or t in name for t in tokens):
            return key
    raise SystemExit(f'No family for material {material!r}')


def radius(Ry, theta):
    """Polar form of Eq. (2) about the source: r e^{r (1 + cos theta)} = Ry (units of l)."""
    c = 1 + math.cos(theta)
    return Ry if c < 1e-14 else lambertw(Ry * c).real / c


def isotherm(Ry, n=29):
    """Exact melt isotherm of Eq. (2) in units of l: samples, half-width R and tips X+, X-.

    With (x, rho) = r (cos theta, sin theta), Eq. (2) gives r = W0(Ry (1 + cos theta)) / (1 + cos theta),
    which is closed-form; theta = 0 is the front tip X+ = W0(2 Ry) / 2 and theta = pi the tail X- = -Ry.
    """
    x_plus, x_minus = 0.5 * lambertw(2 * Ry).real, -Ry
    # Denser sampling towards the tail, where the outline turns most sharply for large Ry.
    thetas = np.pi * np.sin(np.linspace(0, np.pi / 2, n)) ** 0.5
    pts = [(radius(Ry, th) * math.cos(th), radius(Ry, th) * math.sin(th)) for th in thetas]
    pts[0], pts[-1] = (x_plus, 0.0), (x_minus, 0.0)
    # rho(theta) is unimodal on (0, pi): its maximum is the half-width R.
    best = minimize_scalar(lambda th: -radius(Ry, th) * math.sin(th), bounds=(1e-9, math.pi - 1e-9),
                           method='bounded', options={'xatol': 1e-13})
    R = -best.fun
    xs, rho = np.array([p[0] for p in pts]), np.array([p[1] for p in pts])
    return xs, rho, R, x_plus, x_minus


def boundary(p_min=1.001, p_max=40.0, n=80):
    """R = R_ boundary (Eq. 24 with equality): U~ as a function of P~ > 1."""
    out = []
    for p in np.geomspace(p_min, p_max, n):
        u = 2 / (math.e * p) * (p ** -BETA - 1) ** (-2 / BETA)
        out.append([round(u, 6), round(p, 6)])
    return out


def ar_isoline_ry(a):
    """Ry of the aspect-ratio isoline A_r = a from Eq. (12); the isoline is P~ U~ = Ry."""
    return 8 / math.e * (a ** ETA - 1) ** (2 / ETA)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--workbook', type=Path, required=True)
    args = ap.parse_args()
    raw = args.workbook.read_bytes()
    df = pd.read_excel(args.workbook, sheet_name='Parametri').iloc[:, :28]
    df.columns = [str(c).strip() for c in df.columns]
    col = {k: next(c for c in df.columns if c.startswith(k)) for k in
           ('Autore', 'Anno', 'DOI', 'Processo', 'Materiale', 'U [m/s]', 'P [W]', 'T_prerisc', 'R_', 'k', 'α', 'Τ_m', 'P*', 'U*')}
    dropped = {'no process': 0, 'EBM': 0, 'incomplete': 0, 'not selected in the workbook': 0}
    points = []
    for _, r in df.iterrows():
        proc = r[col['Processo']]
        if not isinstance(proc, str) or not isinstance(r[col['Materiale']], str):
            dropped['no process'] += 1 if isinstance(r[col['Materiale']], str) else 0
            continue
        proc = proc.strip()
        if proc.upper().startswith('EBM'):
            dropped['EBM'] += 1
            continue
        if proc not in PROCESSES:
            continue
        vals = [r[col[k]] for k in ('U [m/s]', 'P [W]', 'T_prerisc', 'R_', 'k', 'α', 'Τ_m')]
        if any(not isinstance(v, (int, float)) or not np.isfinite(v) or v <= 0 for v in vals):
            dropped['incomplete'] += 1
            continue
        U, P, T0, Rb, lam, alpha, Tm = map(float, vals)
        dT = Tm - T0
        u_t, p_t = U * Rb / (2 * alpha), P / (2 * math.pi * lam * Rb * dT)
        sheet_u, sheet_p = r[col['U*']], r[col['P*']]
        # Rows the workbook leaves without U*, P* are not part of its analysed selection.
        if not all(isinstance(v, (int, float)) and np.isfinite(v) for v in (sheet_u, sheet_p)):
            dropped['not selected in the workbook'] += 1
            continue
        # The workbook's own U*, P* must agree with Eqs. (20, 21) applied to its raw columns.
        if not (math.isclose(u_t, sheet_u, rel_tol=1e-6) and math.isclose(p_t, sheet_p, rel_tol=1e-6)):
            raise SystemExit(f'U*/P* mismatch for {r[col["Autore"]]}: {u_t, p_t} vs {sheet_u, sheet_p}')
        Ry = p_t * u_t
        xs, rho, R, x_plus, x_minus = isotherm(Ry)
        ar_exact = (x_plus - x_minus) / (2 * R)
        ar_eq12 = (1 + (math.e * Ry / 8) ** (ETA / 2)) ** (1 / ETA)
        year = r[col['Anno']]
        doi = r[col['DOI']]
        points.append({
            'process': PROCESSES[proc], 'process_label': proc, 'material': r[col['Materiale']].strip(),
            'family': family(r[col['Materiale']]), 'author': str(r[col['Autore']]).strip(),
            'year': int(year) if isinstance(year, (int, float)) and np.isfinite(year) else None,
            'doi': doi.strip() if isinstance(doi, str) and doi.strip() else None,
            'U': round(U, 6), 'P': round(P, 3), 'R_bar_um': round(Rb * 1e6, 3),
            'U_t': round(u_t, 6), 'P_t': round(p_t, 6), 'Ry': round(Ry, 6),
            'R_over_Rbar': round(R * 2 * alpha / U / Rb, 6),
            'Ar': round(ar_exact, 5), 'Ar_eq12': round(ar_eq12, 5),
            # Outline normalised by the half-width R: x from tail (x-) to front (x+).
            'outline': [[round(float(x / R), 3), round(float(y / R), 3)] for x, y in zip(xs, rho)],
        })
    if not points:
        raise SystemExit('No usable rows')
    data = {
        'figure': 'FIG. R04.1',
        'source': {
            'article': 'Moda, Chiocca, Macoretta, Monelli, Bertini, Materials & Design 223 (2022) 110991',
            'doi': '10.1016/j.matdes.2022.110991', 'dataset_doi': '10.17632/b2437352ky.2',
            'workbook': args.workbook.name, 'workbook_sha256': hashlib.sha256(raw).hexdigest(),
            'generated': date.today().isoformat(), 'dropped_rows': dropped,
        },
        'constants': {'beta': BETA, 'eta': ETA},
        'boundary': boundary(),
        'ar_isolines': [{'Ar': a, 'Ry': round(ar_isoline_ry(a), 6)} for a in (1.5, 2, 3, 5, 8)],
        'points': sorted(points, key=lambda p: (p['process'], p['family'], p['U_t'])),
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf8')
    print(f'Wrote {OUT.relative_to(ROOT)}: {len(points)} points, dropped {dropped}, {OUT.stat().st_size // 1024} kB')


if __name__ == '__main__':
    main()
