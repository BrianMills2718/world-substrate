from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

import bootstrap_scene_profile as bootstrap
import render_scene_replay as renderer
from reference_worlds.greenhouse.mechanics import PutDownAction, WaterAction
from reference_worlds.greenhouse.probe import build_engine
from reference_worlds.greenhouse.terminal import garden_complete
from run_greenhouse_fixture import retained_run
from world_substrate.rules import FillAction, TakeAction

MODEL = REPO / "reference_worlds/greenhouse/bed-v0.json"
TRACE = REPO / "evidence/greenhouse/first-service-v0.json"
CATALOG = REPO / "reference_worlds/scene-asset-catalog-v0.json"
PROFILE = REPO / "evidence/greenhouse/scene-profile-zero-review-v0.json"
REPLAY = REPO / "evidence/renders/greenhouse-zero-review-v0.html"


def load(path: Path):
    return json.loads(path.read_text())


class GreenhouseZeroReviewTests(unittest.TestCase):
    def test_retained_fixture_regenerates_and_is_real_engine_behavior(self):
        self.assertEqual(retained_run(), load(TRACE))
        engine = build_engine(REPO)
        action_types = {
            "take": TakeAction,
            "fill": FillAction,
            "put_down": PutDownAction,
            "water": WaterAction,
        }
        for turn in load(TRACE)["transcript"]:
            row = turn["actors"][turn["committed_first"]]["did"]
            action = action_types[row["kind"]].from_dict(row)
            self.assertEqual(engine.apply(action)["status"], "accepted")
        self.assertTrue(garden_complete(engine.world))
        self.assertTrue(engine.replay()["ok"])

    def test_bootstrap_generates_complete_profile_without_review_overlay(self):
        generated = bootstrap.bootstrap_profile(
            load(MODEL),
            load(TRACE),
            load(CATALOG),
            world_model_ref="../../reference_worlds/greenhouse/bed-v0.json",
            auto_layout=True,
        )
        self.assertTrue(bootstrap.is_complete(generated))
        self.assertEqual(generated, load(PROFILE))
        self.assertEqual(
            set(generated["bootstrap"]["declared_action_bindings"]),
            {"take", "fill", "water", "put_down"},
        )
        self.assertEqual(generated["bootstrap"]["binding_resolution_errors"], {})
        self.assertEqual(generated["action_visuals"]["water"]["item_field"], "plant")
        self.assertEqual(generated["action_visuals"]["water"]["actor_target"], {"action_field": "bed"})

    def test_semantics_place_can_by_source_and_plants_inside_bed(self):
        profile = load(PROFILE)
        self.assertEqual(profile["entities"]["can-1"]["home"], profile["stations"]["tap-1"]["item_anchor"])
        x, y, width, height = profile["stations"]["bed-1"]["rect"]
        for plant_id in ("fern-1", "tomato-1"):
            px, py = profile["entities"][plant_id]["home"]
            self.assertTrue(x <= px <= x + width)
            self.assertTrue(y <= py <= y + height)

    def test_water_projection_updates_both_plant_and_can_state(self):
        profile, world_entities = renderer.load_scene_profile(PROFILE)
        frames = renderer.build_frames(load(TRACE), profile, world_entities)
        self.assertEqual(frames[1]["items"]["can-1"]["state"], "filled")
        self.assertEqual(frames[2]["items"]["fern-1"]["state"], "watered")
        self.assertEqual(frames[2]["items"]["can-1"]["state"], "empty")
        self.assertEqual(frames[5]["items"]["can-1"]["state"], "filled")
        self.assertEqual(frames[6]["items"]["tomato-1"]["state"], "watered")
        self.assertEqual(frames[6]["items"]["can-1"]["state"], "empty")

    def test_replay_regenerates_exactly_through_generic_renderer(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "greenhouse.html"
            renderer.render_file(TRACE, PROFILE, output)
            self.assertEqual(output.read_text(), REPLAY.read_text())
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        bootstrap_source = (REPO / "scripts/bootstrap_scene_profile.py").read_text().lower()
        for token in ("greenhouse", "can-1", "bed-1", "fern-1", "tomato-1"):
            with self.subTest(token=token):
                self.assertNotIn(token, source)
                self.assertNotIn(token, bootstrap_source)


if __name__ == "__main__":
    unittest.main()
