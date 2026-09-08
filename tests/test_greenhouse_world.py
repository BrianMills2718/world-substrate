from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.greenhouse.mechanics import PutDownAction, WaterAction
from reference_worlds.greenhouse.probe import build_engine
from reference_worlds.greenhouse.terminal import garden_complete
from world_substrate.model import owner_ref
from world_substrate.rules import FillAction, TakeAction


class GreenhouseWorldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_engine(REPO)

    def test_initial_discovery_exposes_the_shared_can_without_special_policy_code(self):
        page = self.engine.discover("nora")
        self.assertEqual([row["action"]["kind"] for row in page["available"]], ["take"])
        self.assertEqual(page["available"][0]["action"]["vessel"], "can-1")
        self.assertFalse(garden_complete(self.engine.world))

    def test_fill_without_holding_the_can_is_refused(self):
        result = self.engine.apply(
            FillAction("nora", "can-1", "tap-1", 1, self.engine.world.revision, "test")
        )
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(self.engine.world.revision, 0)
        self.assertEqual(self.engine.world.entities["can-1"].component("watering_can").state, "empty")

    def test_shared_can_handoff_waters_both_plants_and_replays(self):
        e = self.engine
        sequence = [
            lambda: TakeAction("nora", "can-1", e.world.revision, "test"),
            lambda: FillAction("nora", "can-1", "tap-1", 1, e.world.revision, "test"),
            lambda: WaterAction("nora", "can-1", "fern-1", "bed-1", e.world.revision, "test"),
            lambda: PutDownAction("nora", "can-1", e.world.revision, "test"),
            lambda: TakeAction("leo", "can-1", e.world.revision, "test"),
            lambda: FillAction("leo", "can-1", "tap-1", 1, e.world.revision, "test"),
            lambda: WaterAction("leo", "can-1", "tomato-1", "bed-1", e.world.revision, "test"),
        ]
        for make_action in sequence:
            self.assertEqual(e.apply(make_action())["status"], "accepted")
        self.assertEqual(e.world.entities["fern-1"].component("plant").stage, "watered")
        self.assertEqual(e.world.entities["tomato-1"].component("plant").stage, "watered")
        self.assertEqual(e.world.entities["can-1"].ownership.owner_ref, owner_ref("actor", "leo"))
        self.assertTrue(garden_complete(e.world))
        self.assertTrue(e.replay()["ok"])

    def test_watering_consumes_the_fill_and_cannot_repeat_without_refilling(self):
        e = self.engine
        self.assertEqual(e.apply(TakeAction("nora", "can-1", e.world.revision, "test"))["status"], "accepted")
        self.assertEqual(e.apply(FillAction("nora", "can-1", "tap-1", 1, e.world.revision, "test"))["status"], "accepted")
        self.assertEqual(e.apply(WaterAction("nora", "can-1", "fern-1", "bed-1", e.world.revision, "test"))["status"], "accepted")
        retry = e.apply(WaterAction("nora", "can-1", "fern-1", "bed-1", e.world.revision, "test"))
        self.assertEqual(retry["status"], "precondition_failed")
        self.assertEqual(e.world.entities["can-1"].component("watering_can").state, "empty")
        self.assertEqual(e.world.entities["fern-1"].component("plant").stage, "watered")


if __name__ == "__main__":
    unittest.main()
