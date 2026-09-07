from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

import bootstrap_scene_profile as bootstrap
import render_scene_replay as renderer
from reference_worlds.workshop.mechanics import AttachAction, PickUpAction
from reference_worlds.workshop.probe import build_engine

MODEL = REPO / "reference_worlds/workshop/bench-v0.json"
TRACE = REPO / "evidence/workshop/scene-profile-greenfield-v0.json"
CATALOG = REPO / "reference_worlds/scene-asset-catalog-v0.json"
REVIEW = REPO / "reference_worlds/workshop/scene-review-v0.json"
PROFILE = REPO / "reference_worlds/workshop/scene-profile-v0.json"
REPLAY = REPO / "evidence/renders/workshop-spatial-replay-v0.html"


def load(path: Path):
    return json.loads(path.read_text())


class WorkshopGreenfieldSceneProof(unittest.TestCase):
    def test_retained_trace_is_real_workshop_engine_behavior(self):
        trace = load(TRACE)
        engine = build_engine(REPO)
        for turn in trace["transcript"]:
            row = turn["actors"]["mira"]["did"]
            action = PickUpAction.from_dict(row) if row["kind"] == "pick_up" else AttachAction.from_dict(row)
            self.assertEqual(engine.apply(action)["status"], "accepted")
        attached = sorted(
            e.entity_id for e in engine.world.entities.values()
            if e.component("part") and e.component("part").attached_to == "frame-a"
        )
        self.assertEqual(attached, ["leg-1", "leg-2", "seat-1"])
        self.assertTrue(engine.replay()["ok"])

    def test_greenfield_bootstrap_infers_structure_but_not_layout(self):
        draft = bootstrap.bootstrap_profile(
            load(MODEL), load(TRACE), load(CATALOG), world_model_ref="bench-v0.json"
        )
        self.assertEqual(draft["actors"]["mira"]["asset"], "worker")
        self.assertEqual(set(draft["stations"]), {"frame-a"})
        self.assertEqual(draft["entities"]["wrench-1"]["asset"], "wrench")
        self.assertEqual(draft["entities"]["leg-1"]["asset"], "leg")
        self.assertEqual(
            draft["bootstrap"]["inferred_action_fields"]["attach"],
            {"item_field": "part", "station_field": "assembly"},
        )
        self.assertFalse(bootstrap.is_complete(draft))
        self.assertNotIn("home", draft["actors"]["mira"])
        self.assertNotIn("rect", draft["stations"]["frame-a"])

    def test_reviewed_bootstrap_is_complete_and_renders_without_domain_branch(self):
        assembled = bootstrap.bootstrap_profile(
            load(MODEL), load(TRACE), load(CATALOG), world_model_ref="bench-v0.json", review=load(REVIEW)
        )
        self.assertTrue(bootstrap.is_complete(assembled))
        self.assertEqual(assembled, load(PROFILE))
        loaded, world_entities = renderer.load_scene_profile(PROFILE)
        frames = renderer.build_frames(load(TRACE), loaded, world_entities)
        self.assertEqual(frames[-1]["items"]["leg-1"]["placed_at"], "frame-a")
        self.assertEqual(frames[-1]["items"]["leg-2"]["placed_at"], "frame-a")
        self.assertEqual(frames[-1]["items"]["seat-1"]["placed_at"], "frame-a")
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for token in ("workshop", "mira", "frame-a", "wrench-1"):
            self.assertNotIn(token, source)
        self.assertIn("Workshop replay: assembling a chair", REPLAY.read_text())

    def test_greenfield_review_fraction_is_below_prior_full_profile_threshold(self):
        core = {k: v for k, v in load(PROFILE).items() if k != "bootstrap"}
        full_size = len(json.dumps(core, separators=(",", ":")))
        review_size = len(json.dumps(load(REVIEW), separators=(",", ":")))
        self.assertLess(review_size / full_size, 0.70)


if __name__ == "__main__":
    unittest.main()
