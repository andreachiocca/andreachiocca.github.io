"""Source and mechanics contracts for the Technical Research Atlas."""
from pathlib import Path
import json
import math
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def source(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


class ResearchAtlasSourceTests(unittest.TestCase):
    def test_layout_and_localized_intro(self):
        page = source("_pages/research.md")
        shell = source("_layouts/research_atlas.html")
        self.assertIn("layout: research_atlas", page)
        self.assertIn("layout: default", shell)
        self.assertEqual(shell.count("<h1"), 1)
        self.assertEqual(shell.count("{% locale research.intro %}"), 1)
        self.assertIn("I study how materials and components respond to repeated loads", shell)
        self.assertNotIn("{% locale research.intro %}", page)
        self.assertIn("{{ content }}", shell)
        self.assertEqual(source("assets/css/main.scss").count('@import "research_atlas";'), 1)
        en = json.loads(source("_data/i18n/en/ui.json"))
        it = json.loads(source("_data/i18n/it/ui.json"))
        self.assertEqual(set(en), set(it))

    def test_jump_link_targets(self):
        shell = source("_layouts/research_atlas.html")
        page = source("_pages/research.md")
        for anchor in ("research-areas", "projects", "international-collaborations"):
            self.assertIn('href="#' + anchor + '"', shell)
            self.assertIn('id="' + anchor + '"', page)

    def test_four_canonical_chapters(self):
        page = source("_pages/research.md")
        panel = source("_includes/research_area_panel.html")
        self.assertIn("site.data.research_areas", page)
        self.assertIn("localized_record: 'research_areas'", page)
        self.assertIn("include research_area_panel.html", page)
        self.assertIn("canonical_id=canonical_area.id", page)
        self.assertIn("ordinal=forloop.index", page)
        self.assertIn('class="research-area', panel)
        self.assertIn('id="{{ include.canonical_id }}"', panel)
        self.assertIn("{{ area.summary }}", panel)
        self.assertIn("{{ area.methods }}", panel)
        self.assertIn("link.url | local_url | relative_url", panel)
        self.assertIn('class="context-details"', panel)
        self.assertIn("area.further", panel)
        self.assertIn("area.links", panel)


    def test_projects_and_visits_preserved(self):
        page = source("_pages/research.md")
        self.assertIn('id="projects"', page)
        self.assertIn('id="selected-collaborative-projects"', page)
        self.assertIn('id="international-collaborations"', page)
        self.assertIn('id="research-environment"', page)
        self.assertIn('class="research-projects"', page)
        self.assertIn('class="research-collaborations"', page)
        self.assertIn('class="research-contact"', page)
        self.assertIn("include research_project.html project=project", page)
        self.assertIn("include international_experiences.html", page)
        self.assertIn("previous-projects", page)
        self.assertIn("/laboratory/", page)
        self.assertIn("/thesis/", page)
        self.assertIn("{% locale research.contact %}", page)
        project = source("_includes/research_project.html")
        self.assertIn('data-project="{{ project.id }}"', project)
        self.assertIn("project.working_groups", project)



class ResearchAtlasFigureTests(unittest.TestCase):
    def test_fatigue_traction_decomposition(self):
        import importlib.util
        script = ROOT / "scripts/generate_research_atlas_figures.py"
        spec = importlib.util.spec_from_file_location("research_atlas_figures", script)
        figures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(figures)
        q = 1 / math.sqrt(2)
        tensor = [[0, 0, .6], [0, 0, 0], [.6, 0, 1]]
        normal, shear = figures.traction_components(tensor, (q, 0, q))
        self.assertAlmostEqual(sum(normal[i] * (q, 0, q)[i] for i in range(3)), 1.1)
        expected = ((1.1*q, 0, 1.1*q), (-.5*q, 0, .5*q))
        for actual, ref in zip((normal, shear), expected):
            for a, b in zip(actual, ref):
                self.assertAlmostEqual(a, b, delta=1e-9)
        self.assertAlmostEqual(sum(shear[i]*(q,0,q)[i] for i in range(3)), 0, delta=1e-9)
        with self.assertRaises(ValueError):
            figures.traction_components(tensor, (0, 0, 0))

    def test_projected_vectors_share_one_mapping(self):
        import importlib.util
        script = ROOT / "scripts/generate_research_atlas_figures.py"
        spec = importlib.util.spec_from_file_location("research_atlas_figures_projection", script)
        figures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(figures)
        for vector, expected in [
            ((1, 0, 0), (math.sqrt(3)/2, .5)),
            ((0, 1, 0), (-math.sqrt(3)/2, .5)),
            ((0, 0, 1), (0, -1)),
        ]:
            actual = figures.project_iso(vector)
            for a, b in zip(actual, expected):
                self.assertAlmostEqual(a, b, delta=1e-9)

    def test_four_svg_figures_and_total_size(self):
        import xml.etree.ElementTree as ET
        paths = [ROOT / "_includes/research_figures" / (name + ".svg") for name in
                 ("fatigue", "weld", "additive", "testing")]
        self.assertLess(sum(path.stat().st_size for path in paths), 35000)
        for path in paths:
            root = ET.parse(path).getroot()
            self.assertTrue(root.tag.endswith("svg"), path)
            self.assertEqual(root.attrib.get("viewBox"), "0 0 480 320")

    def test_weld_haz_is_mirrored_outside_fusion_and_without_labels(self):
        import xml.etree.ElementTree as ET
        svg = ET.fromstring(source("_includes/research_figures/weld.svg"))
        zones = {node.attrib.get("data-heat-affected-zone"): node
                 for node in svg.iter() if "data-heat-affected-zone" in node.attrib}
        self.assertEqual(set(zones), {"left", "right"})
        coordinates = []
        for side in ("left", "right"):
            points = [(int(x), int(y)) for x, y in
                      re.findall(r"(\\d+),(\\d+)", zones[side].attrib["d"])]
            self.assertEqual(len(points), 6)
            coordinates.append(points)
        for left, right in zip(*coordinates):
            self.assertEqual(left[0] + right[0], 480)
            self.assertEqual(left[1], right[1])
        self.assertFalse(any(node.tag.endswith("}text") or node.tag == "text"
                             for node in svg.iter()))
        self.assertEqual(len([node for node in svg.iter()
                              if node.attrib.get("data-joint-type") == "double-v"]), 1)

    def test_unknown_figure_id_falls_back_to_text(self):
        dispatch = source("_includes/research_area_visual.html")
        panel = source("_includes/research_area_panel.html")
        self.assertIn("case include.canonical_id", dispatch)
        self.assertEqual(dispatch.count("{% when "), 4)
        self.assertIn("research_area_visual.html", panel)
        self.assertIn("{{ area.summary }}", panel)
        self.assertIn("{{ area.methods }}", panel)
        self.assertIn("area.links", panel)


class ResearchAtlasRenderedContractTests(unittest.TestCase):
    def test_verifier_is_wired_after_build(self):
        path = ROOT / "scripts/verify_research_atlas.py"
        self.assertTrue(path.is_file())
        for workflow in (".github/workflows/build.yml", ".github/workflows/preview.yml"):
            text = source(workflow)
            self.assertIn("python scripts/verify_research_atlas.py _site", text)
            self.assertGreater(text.index("python scripts/verify_research_atlas.py _site"), text.index("bundle exec jekyll build"))

    def test_verifier_rejects_missing_areas_and_roles(self):
        import importlib.util
        import tempfile
        spec = importlib.util.spec_from_file_location("atlas_verifier", ROOT / "scripts/verify_research_atlas.py")
        verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(verifier)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for prefix, lang in (("", "en"), ("it/", "it")):
                target = root / prefix / "research/index.html"
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(f'<html lang="{lang}"><main><h1>Research</h1><section id="projects"></section></main></html>', encoding="utf8")
            with self.assertRaisesRegex((ValueError, AssertionError), "research|area|figure|FABER"):
                verifier.verify_research_atlas(root)


if __name__ == "__main__":
    unittest.main()
