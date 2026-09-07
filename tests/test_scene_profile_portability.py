from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
spec = importlib.util.spec_from_file_location("scene_replay_portability", REPO / "scripts/render_scene_replay.py")
scene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scene)

TRACE = REPO / "evidence/castaway/scene-profile-portability-v0.json"
PROFILE = REPO / "reference_worlds/castaway/scene-profile-v0.json"


class SecondRealWorldUsesTheSameRenderer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile, cls.world_entities = scene.load_scene_profile(PROFILE)
        cls.trace = scene.load_trace(TRACE, expected_world=cls.profile["world"])
        cls.frames = scene.build_frames(cls.trace, cls.profile, cls.world_entities)
        cls.html = scene.render_html(cls.trace, cls.profile, cls.world_entities, PROFILE.parent)

    def test_castaway_uses_eight_real_scripted_turns(self):
        self.assertEqual([f["turn"] for f in self.frames], list(range(1, 9)))
        self.assertEqual(self.trace["world"], "castaway")
        self.assertEqual(self.trace.get("cost_usd", 0), 0)

    def test_world_model_initial_ownership_becomes_visual_attachment(self):
        self.assertEqual(self.frames[0]["holders"].get("cup-robinson"), "robinson")

    def test_different_actions_are_profiled_without_renderer_branches(self):
        labels = {row["actors"][actor]["action"] for row in self.frames for actor in self.trace["actors"]}
        self.assertTrue(any(label.startswith("fill clay-pot from unsafe-pool") for label in labels))
        self.assertTrue(any(label.startswith("drink 250 ml from clay-pot") for label in labels))
        self.assertIn("Castaway replay: water at camp", self.html)
        self.assertIn("Unsafe pool", self.html)

    def test_generic_renderer_contains_no_castaway_ids(self):
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for word in ("castaway", "robinson", "friday", "clay-pot", "unsafe-pool", "fire-camp"):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
