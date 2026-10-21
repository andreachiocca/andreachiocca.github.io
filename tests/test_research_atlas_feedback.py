"""Contracts for the owner-reviewed Research Atlas figure refinements."""
import importlib.util
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SVG = "{http://www.w3.org/2000/svg}"


def source(path):
    return (ROOT / path).read_text(encoding="utf-8")


class ResearchAtlasFeedbackTests(unittest.TestCase):
    def test_candidate_plane_caption_is_brief_and_localized(self):
        dispatch = source("_includes/research_area_visual.html")
        verifier = source("scripts/verify_research_atlas.py")
        self.assertIn("'Candidate-plane' | t", dispatch)
        self.assertNotIn("Candidate-plane traction schematic", dispatch)
        self.assertIn('"multiaxial-fatigue-and-critical-plane-methods": "Candidate-plane"', verifier)
        self.assertEqual(json.loads(source("_data/i18n/en/ui.json"))["Candidate-plane"], "Candidate-plane")
        self.assertEqual(json.loads(source("_data/i18n/it/ui.json"))["Candidate-plane"], "Piano candidato")

    def test_weld_cross_section_is_symmetric_double_v(self):
        root = ET.fromstring(source("_includes/research_figures/weld.svg"))
        fusion = root.find(f".//{SVG}polygon[@data-joint-type='double-v']")
        self.assertIsNotNone(fusion)
        points = [tuple(map(float, pair.split(","))) for pair in fusion.attrib["points"].split()]
        self.assertEqual(points, [(180, 110), (300, 110), (262, 170),
                                  (300, 230), (180, 230), (218, 170)])
        self.assertNotIn("geometry only", source("_includes/research_figures/weld.svg"))

    def test_hilbert_path_is_continuous_and_generator_owned(self):
        spec = importlib.util.spec_from_file_location(
            "research_atlas_figures", ROOT / "scripts/generate_research_atlas_figures.py"
        )
        figures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(figures)
        points = figures.hilbert_points(3)
        self.assertEqual(len(points), 64)
        self.assertEqual(len(set(points)), 64)
        self.assertEqual({coord for point in points for coord in point}, set(range(8)))
        self.assertTrue(all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
                            for a, b in zip(points, points[1:])))
        root = ET.fromstring(source("_includes/research_figures/additive.svg"))
        path = root.find(f".//{SVG}path[@data-hilbert-path='order-3']")
        self.assertIsNotNone(path)
        self.assertEqual(path.attrib["d"], figures.hilbert_svg_path(3))

    def test_motion_has_static_fallback_and_reduced_motion(self):
        css = source("_sass/_research_atlas.scss")
        self.assertIn("@keyframes research-hilbert-draw", css)
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn(".research-hilbert-trace", css)
        self.assertIn("Research reduced-motion path", source("scripts/check_browser.py"))
        root = ET.fromstring(source("_includes/research_figures/additive.svg"))
        self.assertIsNotNone(root.find(f".//{SVG}path[@data-hilbert-path='order-3']"))

    def test_gauge_and_overview_have_explicit_meaning(self):
        root = ET.fromstring(source("_includes/research_figures/testing.svg"))
        self.assertIsNotNone(root.find(f".//{SVG}g[@data-sensor='axial-strain-gauge']"))
        self.assertIsNotNone(root.find(f".//{SVG}path[@data-grid-axis='x']"))
        overview = source("_includes/research_overview_visual.html")
        for method in ("analytical", "numerical", "experimental"):
            self.assertIn(f'data-method="{method}"', overview)

    def test_project_panel_text_is_light(self):
        css = source("_sass/_research_atlas.scss")
        self.assertIn(".research-featured-project-head span", css)
        self.assertIn(".research-featured-project .research-project li", css)
        self.assertIn(".research-featured-project .research-project strong", css)
        self.assertIn("Research featured project text contrast", source("scripts/check_browser.py"))


if __name__ == "__main__":
    unittest.main()
