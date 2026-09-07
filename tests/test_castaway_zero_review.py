from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import bootstrap_scene_profile as bootstrap
import render_scene_replay as renderer

MODEL = REPO / "reference_worlds/castaway/freshwater-v0.json"
TRACE = REPO / "evidence/castaway/scene-profile-portability-v0.json"
CATALOG = REPO / "reference_worlds/scene-asset-catalog-v0.json"
PROFILE = REPO / "evidence/castaway/scene-profile-zero-review-v0.json"
REPLAY = REPO / "evidence/renders/castaway-zero-review-v0.html"


def load(path: Path):
    return json.loads(path.read_text())


class CastawayZeroReviewReplay(unittest.TestCase):
    def test_zero_review_profile_regenerates_with_no_todos(self):
        generated = bootstrap.bootstrap_profile(
            load(MODEL), load(TRACE), load(CATALOG),
            world_model_ref="../../reference_worlds/castaway/freshwater-v0.json",
            auto_layout=True,
        )
        self.assertTrue(bootstrap.is_complete(generated))
        self.assertEqual(generated, load(PROFILE))
        self.assertEqual(generated["bootstrap"]["declared_action_bindings"], ["drink", "fill"])
        self.assertEqual(generated["bootstrap"]["todos"], [])

    def test_initial_actor_ownership_and_action_states_survive_projection(self):
        profile, world_entities = renderer.load_scene_profile(PROFILE)
        frames = renderer.build_frames(load(TRACE), profile, world_entities)
        self.assertIn("cup-robinson", frames[0]["holdings"]["robinson"])
        self.assertIn("unsafe-pool", frames[0]["active_stations"])
        self.assertEqual(frames[0]["items"]["clay-pot"]["state"], "used")
        self.assertEqual(frames[-1]["items"]["clay-pot"]["state"], "used")
        self.assertEqual(frames[-1]["actors"]["robinson"]["action"], "drink 250 ml from clay-pot")
        self.assertEqual(frames[-1]["actors"]["friday"]["action"], "fill clay-pot from unsafe-pool")

    def test_zero_review_replay_regenerates_exactly(self):
        profile, world_entities = renderer.load_scene_profile(PROFILE)
        html = renderer.render_html(load(TRACE), profile, world_entities, PROFILE.parent)
        self.assertEqual(html, REPLAY.read_text())
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for token in ("castaway", "robinson", "friday", "unsafe-pool", "clay-pot"):
            self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
