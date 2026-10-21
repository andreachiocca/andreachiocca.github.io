"""Run the tensor, projection and static-fallback tests in the existing CI suite."""
import subprocess
import unittest
from pathlib import Path


class StressVisualTests(unittest.TestCase):
    def test_scientific_model_and_static_svg(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            ["node", "--test", "tests/stress_visual.test.cjs"], cwd=root,
            capture_output=True, text=True, timeout=30, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
