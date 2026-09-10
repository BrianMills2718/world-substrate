from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import load_live_projection_bundle, load_scene_contract

spec = importlib.util.spec_from_file_location("composed_living_renderer", REPO / "scripts/render_composed_living_scene.py")
renderer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(renderer)

PROFILE = REPO / "tests/fixtures/living_scene/neutral-render-profile-v1.json"
PROJECTION = REPO / "tests/fixtures/living_scene/neutral-render-projection-v0.json"


class ComposedLivingSceneRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load_scene_contract(PROFILE)
        cls.bundle = load_live_projection_bundle(PROJECTION)
        cls.html = renderer.render_html(cls.bundle, cls.profile, PROFILE.parent)

    def test_generic_renderer_has_world_first_interaction_shell(self) -> None:
        for marker in ("class='stage'", "class='controls'", "id='scrub'", "id='inspector'", "id='inspectorClose'", "data-kind='actors'", "data-kind='entities'", "data-kind='activities'", "data-kind='institutions'"):
            self.assertIn(marker, self.html)

    def test_inspector_is_selection_driven_not_persistent_dashboard(self) -> None:
        self.assertIn(".inspector.open", self.html)
        self.assertIn("function showInspector(group,id)", self.html)
        self.assertIn("function closeInspector()", self.html)
        self.assertNotIn("causal graph", self.html.lower())
        self.assertNotIn("trace table", self.html.lower())

    def test_composed_renderer_supports_presentation_only_motion_and_state_positions(self) -> None:
        self.assertIn("function actorPositions(f)", self.html)
        self.assertIn("status==='active'", self.html)
        self.assertIn("position_by_state", self.html)
        self.assertIn("event-focus", self.html)

    def test_generic_source_contains_no_waltzman_specific_ids(self) -> None:
        source = (REPO / "scripts/render_composed_living_scene.py").read_text().lower()
        for word in ("waltzman", "mara", "selene", "validation-capacity", "clinical-staff", "shared-reserve", "safeguard-record"):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
