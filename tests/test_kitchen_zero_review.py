from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import bootstrap_scene_profile as bootstrap
import render_scene_replay as renderer

MODEL = REPO / "reference_worlds/kitchen/service-v0.json"
TRACE = REPO / "evidence/kitchen/full-service-replication-v1-run1.json"
CATALOG = REPO / "reference_worlds/scene-asset-catalog-v0.json"
PROFILE = REPO / "evidence/kitchen/scene-profile-zero-review-v0.json"
REPLAY = REPO / "evidence/renders/kitchen-zero-review-v0.html"
POLISHED = REPO / "evidence/renders/kitchen-spatial-replay-v1.html"


def load(path: Path):
    return json.loads(path.read_text())


class KitchenZeroReviewReplay(unittest.TestCase):
    def test_zero_review_profile_regenerates_with_all_five_bindings(self):
        generated = bootstrap.bootstrap_profile(
            load(MODEL), load(TRACE), load(CATALOG),
            world_model_ref="../../reference_worlds/kitchen/service-v0.json",
            auto_layout=True,
        )
        self.assertTrue(bootstrap.is_complete(generated))
        self.assertEqual(generated, load(PROFILE))
        self.assertEqual(
            generated["bootstrap"]["declared_action_bindings"],
            ["chop", "cook", "plate", "put_down", "take"],
        )
        self.assertEqual(generated["bootstrap"]["todos"], [])
        self.assertEqual(generated["bootstrap"]["binding_resolution_errors"], {})

    def test_handoff_and_terminal_truth_remain_visible_without_review(self):
        profile, world_entities = renderer.load_scene_profile(PROFILE)
        frames = renderer.build_frames(load(TRACE), profile, world_entities)
        t10, t11, t17 = frames[9], frames[10], frames[16]
        self.assertNotIn("knife", t10["holdings"]["bo"])
        self.assertNotIn("knife", t10["holdings"]["ama"])
        self.assertEqual(t10["actors"]["bo"]["action"], "put down knife")
        self.assertIn("lets Ama use it", t10["actors"]["bo"]["reasoning"])
        self.assertIn("knife", t11["holdings"]["ama"])
        self.assertEqual(t11["actors"]["ama"]["action"], "take knife")
        self.assertTrue(t17["progress"]["ama"]["filled"])
        self.assertTrue(t17["progress"]["bo"]["filled"])
        self.assertEqual(t17["items"]["carrot-1"]["state"], "plated")
        self.assertEqual(t17["items"]["onion-1"]["state"], "plated")

    def test_zero_review_replay_regenerates_exactly(self):
        profile, world_entities = renderer.load_scene_profile(PROFILE)
        html = renderer.render_html(load(TRACE), profile, world_entities, PROFILE.parent)
        self.assertEqual(html, REPLAY.read_text())
        self.assertIn("put down knife", html)
        self.assertIn("lets Ama use it", html)
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for token in ("kitchen", "ama", "knife", "burner-1", "order-stew"):
            self.assertNotIn(token, source)

    def test_polished_flagship_remains_a_separate_artifact(self):
        self.assertNotEqual(REPLAY.read_text(), POLISHED.read_text())
        self.assertIn("Kitchen replay: two cooks, one knife", POLISHED.read_text())
        self.assertIn("Scene replay", REPLAY.read_text())


if __name__ == "__main__":
    unittest.main()
