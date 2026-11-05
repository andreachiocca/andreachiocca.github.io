"""CLAUDE.md must not point at files, scripts or test modules that no longer exist."""
from itertools import product
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]
TEXT = (ROOT / 'CLAUDE.md').read_text(encoding='utf8')
# Top-level entries a cited path may start from (directories and root files).
ROOTS = {p.name for p in ROOT.iterdir() if p.name not in {'.git', 'vendor', 'node_modules', '_site'}}


def expand_braces(token):
    """`a/{en,it}/b` -> [`a/en/b`, `a/it/b`]."""
    parts = re.split(r'\{([^{}]*,[^{}]*)\}', token)
    options = [parts[i].split(',') if i % 2 else [parts[i]] for i in range(len(parts))]
    return [''.join(choice) for choice in product(*options)]


def cited_paths():
    tokens = set(re.findall(r'`([^`\s]+)`', TEXT))
    for block in re.findall(r'```[a-z]*\n(.*?)```', TEXT, re.S):
        tokens.update(re.findall(r'(?:scripts|tests|tools|_[a-z]+|assets|docs)/[\w./*{},-]+', block))
    for token in tokens:
        token = token.rstrip('.,;:)')
        if '<' in token or '://' in token or token.startswith(('#', '/', '-', '{', ':')):
            continue
        if token.split('/')[0] in ROOTS and (('/' in token) or '.' in token):
            yield token


def cited_test_modules():
    return set(re.findall(r'\btests\.(test_\w+)', TEXT))


class ClaudeMdReferenceTests(unittest.TestCase):
    def test_cited_paths_exist(self):
        paths = sorted(set(cited_paths()))
        self.assertGreater(len(paths), 20, 'path extraction found suspiciously few references')
        missing = []
        for token in paths:
            for candidate in expand_braces(token):
                if '*' in candidate:
                    if not list(ROOT.glob(candidate)):
                        missing.append(candidate)
                elif not (ROOT / candidate).exists():
                    missing.append(candidate)
        self.assertEqual(missing, [], 'CLAUDE.md cites paths that do not exist; update it with the change')

    def test_cited_test_modules_exist(self):
        modules = cited_test_modules()
        self.assertTrue(modules)
        for module in modules:
            self.assertTrue((ROOT / 'tests' / f'{module}.py').is_file(), module)

    def test_ci_checks_listed_here_are_the_ones_ci_runs(self):
        # Every check script the build workflow runs must appear in the command list.
        workflow = (ROOT / '.github/workflows/build.yml').read_text(encoding='utf8')
        for script in sorted(set(re.findall(r'scripts/(?:check|verify)_\w+\.(?:rb|py)', workflow))):
            self.assertIn(script, TEXT, f'{script} runs in CI but is missing from CLAUDE.md')


if __name__ == '__main__':
    unittest.main()
