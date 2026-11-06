"""Regenerate the figures computed from the owner's research code when a source repository changes.

For every entry of _data/figure_sources.yml this script reads the latest commit of the source
repository's default branch. When it differs from the pinned commit (or with --force), it clones
the repository at that commit, installs it, reruns the figure's own generator and updates the pin.
The generators call the original libraries; nothing is recomputed here.

    python scripts/refresh_figures.py --summary summary.md            # only figures with new commits
    python scripts/refresh_figures.py --force --only multifat_comparison

Run from a virtual environment: the source packages are installed into the current interpreter.
"""
import argparse
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / '_data/figure_sources.yml'

# How each figure is rebuilt: what to install from the clone and how to call its generator.
RECIPES = {
    'damage_sphere': {'install': 'package', 'generator': ['scripts/generate_damage_sphere.py']},
    'seancp_sphere': {'install': 'package', 'generator': ['scripts/generate_seancp_sphere.py']},
    'sharcp_figure': {'install': 'requirements', 'generator': ['scripts/generate_sharcp_figure.py', '--sharcp', '{clone}']},
    'multifat_comparison': {'install': 'package', 'generator': ['scripts/generate_multifat_comparison.py', '--multifat', '{clone}']},
}


def run(cmd, **kw):
    print('+', ' '.join(map(str, cmd)), flush=True)
    return subprocess.run(cmd, check=True, text=True, **kw)


def read_sources():
    """Minimal reader for the flat two-level YAML written by this script (no PyYAML needed)."""
    entries, key = {}, None
    for line in SOURCES.read_text(encoding='utf8').splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if not line.startswith(' '):
            key = line.rstrip(':'); entries[key] = {}
        else:
            k, v = line.strip().split(': ', 1); entries[key][k] = v
    return entries


def write_pin(key, commit):
    text = SOURCES.read_text(encoding='utf8')
    pattern = re.compile(rf'(^{re.escape(key)}:\n  repository: [^\n]+\n  commit: )[0-9a-f]{{40}}', re.M)
    new, count = pattern.subn(lambda m: m.group(1) + commit, text)
    if count != 1:
        raise SystemExit(f'Could not update the pin of {key}')
    SOURCES.write_text(new, encoding='utf8')


def latest_commit(repository):
    out = run(['git', 'ls-remote', f'https://github.com/{repository}', 'HEAD'], capture_output=True).stdout.split()
    if not out or not re.fullmatch(r'[0-9a-f]{40}', out[0]):
        raise SystemExit(f'Cannot read the default-branch commit of {repository}')
    return out[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--force', action='store_true', help='regenerate even if the pinned commit is current')
    ap.add_argument('--only', nargs='*', help='restrict to these figure keys')
    ap.add_argument('--summary', type=Path, help='write a Markdown summary of the refresh')
    args = ap.parse_args()
    sources = read_sources()
    unknown = set(sources) - set(RECIPES)
    if unknown:
        raise SystemExit(f'No recipe for {sorted(unknown)}')
    rows, changed = [], []
    with tempfile.TemporaryDirectory() as tmp:
        clones = {}
        for key, entry in sources.items():
            if args.only and key not in args.only:
                continue
            repository, pinned = entry['repository'], entry['commit']
            latest = latest_commit(repository)
            if latest == pinned and not args.force:
                rows.append(f'| {key} | `{repository}` | `{pinned[:7]}` | unchanged |')
                continue
            if repository not in clones:
                clone = Path(tmp) / repository.replace('/', '_')
                run(['git', 'clone', '--quiet', f'https://github.com/{repository}', str(clone)])
                run(['git', '-C', str(clone), 'checkout', '--quiet', latest])
                recipe = RECIPES[key]
                if recipe['install'] == 'package':
                    run([sys.executable, '-m', 'pip', 'install', '--quiet', str(clone)])
                else:
                    run([sys.executable, '-m', 'pip', 'install', '--quiet', '-r', str(clone / 'requirements.txt')])
                clones[repository] = clone
            command = [sys.executable] + [part.format(clone=clones[repository]) for part in RECIPES[key]['generator']] + ['--commit', latest]
            run(command, cwd=ROOT)
            write_pin(key, latest)
            changed.append(key)
            rows.append(f'| {key} | `{repository}` | `{pinned[:7]}` → `{latest[:7]}` | regenerated |')
    report = ['| Figure | Source | Commit | Status |', '|---|---|---|---|', *rows]
    print('\n'.join(report))
    if args.summary:
        args.summary.write_text('\n'.join(report) + '\n', encoding='utf8')
    if changed:
        print('Regenerated:', ', '.join(changed))


if __name__ == '__main__':
    main()
