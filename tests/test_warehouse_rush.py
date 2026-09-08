from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.run_authored_world import build_engine
from scripts.scaffold_world import load_bundle

REPO = Path(__file__).resolve().parents[1]
BUNDLE = REPO / "examples/world_authoring/warehouse-rush-v0.json"
CAUSAL = REPO / "examples/world_authoring/warehouse-rush-causal-v0.json"


class WarehouseRushTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(BUNDLE)
        self.causal = json.loads(CAUSAL.read_text())
        self.engine, self.model, _ = build_engine(self.bundle, self.causal)
        self.actors = ["worker-a", "worker-b", "worker-c", "worker-d"]
        self.peak_candidates = 0
        self.accepted = 0

    def measure(self):
        for actor in self.actors:
            page = self.engine.discover(actor)
            self.peak_candidates = max(
                self.peak_candidates,
                len(page["available"]) + len(page["blocked"]),
            )

    def do(self, actor: str, kind: str, **fields):
        page = self.engine.discover(actor)
        matches = [
            row["action"]
            for row in page["available"]
            if row["action"]["kind"] == kind
            and all(row["action"].get(key) == value for key, value in fields.items())
        ]
        self.assertEqual(len(matches), 1, (actor, kind, fields, page["available"]))
        outcome = self.engine.submit({**matches[0], "controller": "warehouse-oracle"})
        self.assertEqual(outcome["status"], "accepted", outcome)
        self.accepted += 1
        self.measure()

    def test_intended_world_is_solvable_without_dsl_changes(self):
        self.measure()
        self.do("worker-a", "claim-forklift", forklift="forklift-red")
        self.do("worker-b", "claim-forklift", forklift="forklift-blue")
        for index in range(1, 4):
            self.do("worker-a", "transport-cargo", cargo=f"cargo-east-{index}", forklift="forklift-red", dock="dock-a")
            self.do("worker-b", "transport-cargo", cargo=f"cargo-west-{index}", forklift="forklift-blue", dock="dock-b")
            self.do("worker-a", "load-cargo", cargo=f"cargo-east-{index}", truck="truck-east", forklift="forklift-red")
            self.do("worker-b", "load-cargo", cargo=f"cargo-west-{index}", truck="truck-west", forklift="forklift-blue")
            if index < 3:
                self.do("worker-a", "drive-forklift", forklift="forklift-red", location="staging")
                self.do("worker-b", "drive-forklift", forklift="forklift-blue", location="staging")
        self.do("worker-a", "dispatch-truck", truck="truck-east")
        self.do("worker-b", "dispatch-truck", truck="truck-west")

        self.assertEqual(self.accepted, 20)
        self.assertTrue(self.model.terminal and self.model.terminal.reached(self.engine.world))
        self.assertLess(self.peak_candidates, 256)
        self.assertEqual(self.engine.world.entities["truck-east"].component("truck").loaded, 3)
        self.assertEqual(self.engine.world.entities["truck-west"].component("truck").loaded, 3)
        self.assertEqual(self.engine.world.entities["worker-a"].component("worker").energy, 1)
        self.assertEqual(self.engine.world.entities["worker-b"].component("worker").energy, 1)


if __name__ == "__main__":
    unittest.main()
