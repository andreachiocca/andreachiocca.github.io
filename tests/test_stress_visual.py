"""Run the tensor, projection and static-fallback tests in the existing CI suite."""
import subprocess
import unittest
from pathlib import Path


class StressVisualTests(unittest.TestCase):
    def test_home_figure_model_description_uses_user_approved_bilingual_notation(self):
        import json
        root = Path(__file__).resolve().parents[1]
        en = json.loads((root / "_data/i18n/en/stress_visual.json").read_text(encoding="utf-8"))
        it = json.loads((root / "_data/i18n/it/stress_visual.json").read_text(encoding="utf-8"))
        self.assertIn("σ_zz / σ_a = sin(ωt)", en["description"])
        self.assertIn("τ_zx / σ_a = τ_xz / σ_a = 0.6 sin(ωt + 90 degrees)", en["description"])
        self.assertIn("τ_zx / σ_a = τ_xz / σ_a = 0,6 sin(ωt + 90 gradi)", it["description"])
        for record in (en, it):
            self.assertIn("ωt = 45", record["description"])
            self.assertIn("τ_zx", record["description"])
            self.assertIn("σ_zz", record["description"])
        self.assertIn("face-normal axis first", en["convention"])
        self.assertIn("asse normale alla faccia", it["convention"])
        self.assertIn("not experimental data or a fatigue-life prediction", en["convention"])
        self.assertIn("non rappresenta dati sperimentali né una previsione della vita a fatica", it["convention"])

    def test_scientific_model_and_static_svg(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["node", "--test", "tests/stress_visual.test.cjs"], cwd=root,
            capture_output=True, text=True, timeout=30, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
