"""Generic embodied Living Scene renderer acceptance."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import build_living_scene_frames, load_live_projection_bundle, load_scene_contract

spec = importlib.util.spec_from_file_location("living_renderer", REPO / "scripts/render_living_scene.py")
living_renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(living_renderer)

PROFILE = REPO / "tests/fixtures/living_scene/neutral-render-profile-v1.json"
PROJECTION = REPO / "tests/fixtures/living_scene/neutral-render-projection-v0.json"


class LivingSceneRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_scene_contract(PROFILE)
        cls.bundle = load_live_projection_bundle(PROJECTION)
        cls.frames = build_living_scene_frames(cls.bundle, cls.profile)
        cls.html = living_renderer.render_html(cls.bundle, cls.profile, PROFILE.parent)

    def test_domain_neutral_fixture_renders_embodied_scene_elements(self):
        for expected in (
            "Living Scene neutral renderer",
            "Shared lab",
            "Rhea",
            "Sol",
            "Reserve",
            "Coordination task",
            "Shared gate",
        ):
            self.assertIn(expected, self.html)
        self.assertIn("data-actor='actor-a'", self.html)
        self.assertIn("data-entity='resource-a'", self.html)
        self.assertIn("data-activity='activity-a'", self.html)
        self.assertIn("data-institution='institution-a'", self.html)

    def test_resource_activity_and_institution_views_come_from_canonical_bindings(self):
        initial, dropped, active = self.frames
        self.assertEqual(initial["views"]["entities"]["resource-a"]["bindings"]["current"], 10)
        self.assertEqual(dropped["views"]["entities"]["resource-a"]["bindings"]["current"], 5)
        self.assertEqual(active["views"]["activities"]["activity-a"]["bindings"]["status"], "active")
        self.assertEqual(active["views"]["activities"]["activity-a"]["bindings"]["started_tick"], 2)
        self.assertEqual(active["views"]["activities"]["activity-a"]["bindings"]["end_tick"], 4)
        self.assertEqual(active["views"]["institutions"]["institution-a"]["bindings"]["status"], "blocked")

    def test_actor_movement_and_gathering_are_declared_presentation_behaviors(self):
        self.assertIn("op.op==='actor.move_to'", self.html)
        self.assertIn("Array.isArray(av.participants)", self.html)
        self.assertEqual(
            self.profile["activities"]["activity-a"]["participants"],
            ["actor-a", "actor-b"],
        )
        self.assertEqual(self.profile["event_visuals"]["neutral.resource.drop"]["operations"][0]["entity"], "resource-a")

    def test_unknown_render_kind_does_not_gain_domain_semantics(self):
        self.assertNotIn("render.kind===", self.html)
        self.assertNotIn("switch(r.kind", self.html)

    def test_generic_renderer_contains_no_waltzman_special_cases(self):
        source = (REPO / "scripts/render_living_scene.py").read_text().lower()
        for word in (
            "waltzman", "mara", "selene", "validation-capacity",
            "clinical-staff", "shared-reserve", "safeguard-record",
        ):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
