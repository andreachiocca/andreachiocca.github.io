"""Static checks for the Step 3 design system: self-hosted fonts, licences and safe motion."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]
SCSS = (ROOT / '_sass/_design_system.scss').read_text(encoding='utf8')


class DesignSystemTests(unittest.TestCase):
    def test_no_third_party_font_requests(self):
        head = (ROOT / '_includes/head.html').read_text(encoding='utf8')
        self.assertNotIn('fonts.googleapis.com', head)
        self.assertNotIn('fonts.gstatic.com', head)

    def test_every_declared_font_file_exists_with_its_licence(self):
        files = set(re.findall(r'"([a-z0-9-]+\.woff2)"', SCSS))
        self.assertGreaterEqual(len(files), 6)
        for name in files:
            self.assertTrue((ROOT / 'assets/fonts' / name).is_file(), name)
        for family in ('inter', 'source-serif-4', 'jetbrains-mono'):
            self.assertIn('SIL OPEN FONT LICENSE', (ROOT / f'assets/fonts/licenses/{family}-OFL.txt').read_text(encoding='utf8').upper())

    def test_greek_subsets_cover_stress_symbols(self):
        # σ (U+03C3), τ (U+03C4) and φ (U+03C6) fall in the declared Greek range.
        self.assertIn('U+03A3-03FF', SCSS)
        self.assertGreaterEqual(SCSS.count('greek-wght-normal.woff2'), 3)

    def test_motion_is_opacity_only_and_respects_reduced_motion(self):
        motion = (ROOT / 'assets/js/motion.js').read_text(encoding='utf8')
        self.assertIn('prefers-reduced-motion: reduce', motion)
        self.assertIn('prefers-reduced-motion: reduce', SCSS)
        reveal = SCSS[SCSS.index('html.motion-ready [data-reveal] {'):]
        self.assertNotIn('transform', reveal.split('}')[0], 'reveal must not move layout or hit areas')

    def test_design_system_is_imported_last(self):
        imports = re.findall(r'@import "([a-z_]+)";', (ROOT / 'assets/css/main.scss').read_text(encoding='utf8'))
        self.assertEqual(imports[-1], 'design_system')


if __name__ == '__main__':
    unittest.main()
