"""Linked participants for processes (docs/plans/linked_process_participants.md, checks L1 and L2).

A process may name participants resolved from its own entity `it` (ownership, an entity_ref field, or shared
location). Its effects on them commit in the same single Engine event, under the same write-scope enforcement.
The world here is the generated any-scenario truck world (bundle only); the causal models are written in the
tests because they exercise the compiler/Engine contract, not generation (generation is checked by L4/L5).
"""
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.run_authored_world import build_engine  # noqa: E402
from world_substrate.action_authoring import ActionDeclarationError, CausalModel  # noqa: E402
from world_substrate.engine import ScopeViolation  # noqa: E402
from world_substrate.mechanisms.time import ClockAdvanceProcess  # noqa: E402

TRUCK = REPO / "spikes/any-scenario-2026-10/evidence/truck"
BUNDLE = json.loads((TRUCK / "bundle.json").read_text())
BASE = json.loads((TRUCK / "causal.json").read_text())
BASE.pop("review", None)

DRIVE_LINKED = {
    "process_id": "drive-with-driver",
    "rationale": "A driving vehicle carries its driver: both advance ten miles per tick.",
    "selector": {"categories": ["vehicle"], "components": ["vehicle"]},
    "participants": {"driver": {"link": "owner_of_it", "selector": {"categories": ["driver"], "components": ["driver"]}}},
    "checks": [{"label": "the vehicle is driving", "op": "eq",
                "left": {"participant": {"name": "it", "path": "components.vehicle.operational_status"}},
                "right": {"literal": "linked-driving"}}],
    "effects": [
        {"participant": "it", "path": "components.vehicle.road_position", "op": "add", "value": {"literal": 10}},
        {"participant": "driver", "path": "components.driver.road_position", "op": "add", "value": {"literal": 10}},
    ],
}


def _causal(*processes):
    c = deepcopy(BASE)
    c["processes"] = list(processes)
    return c


def _bundle(status="linked-driving"):
    b = deepcopy(BUNDLE)
    next(e for e in b["entities"] if e["id"] == "delivery-vehicle")["components"]["vehicle"]["operational_status"] = status
    return b


def _pos(engine, eid, comp):
    return engine.world.entities[eid].as_dict()["components"][comp]["road_position"]


class CompilerTests(unittest.TestCase):  # L1
    def test_accepts_linked_participants_and_derives_scope(self):
        model = CausalModel.from_dict(_causal(DRIVE_LINKED), bundle=_bundle())
        process = model.processes[0]
        self.assertEqual(list(process.participants), ["driver"])
        self.assertIn("entities.<driver>.components.driver.road_position", process.write_paths)
        self.assertIn("entities.<it>.ownership.owner_ref", process.read_paths)

    def test_rejects_unknown_link(self):
        bad = deepcopy(DRIVE_LINKED)
        bad["participants"]["driver"]["link"] = "nearest"
        with self.assertRaisesRegex(ActionDeclarationError, "unknown link"):
            CausalModel.from_dict(_causal(bad), bundle=_bundle())

    def test_rejects_ref_to_a_field_that_is_not_an_entity_ref(self):
        bad = deepcopy(DRIVE_LINKED)
        bad["participants"]["driver"]["link"] = "ref:vehicle.fuel"
        with self.assertRaisesRegex(ActionDeclarationError, "entity_ref"):
            CausalModel.from_dict(_causal(bad), bundle=_bundle())

    def test_rejects_effect_on_undeclared_participant(self):
        bad = deepcopy(DRIVE_LINKED)
        bad["participants"] = {}
        with self.assertRaisesRegex(ActionDeclarationError, "unknown participant"):
            CausalModel.from_dict(_causal(bad), bundle=_bundle())

    def test_process_without_participants_is_unchanged(self):
        plain = {k: v for k, v in DRIVE_LINKED.items() if k != "participants"}
        plain["effects"] = plain["effects"][:1]
        process = CausalModel.from_dict(_causal(plain), bundle=_bundle()).processes[0]
        self.assertEqual(process.participants, {})
        self.assertNotIn("entities.<it>.ownership.owner_ref", process.read_paths)


class EngineTests(unittest.TestCase):  # L2
    def test_one_event_changes_the_vehicle_and_its_driver(self):
        engine, _, _ = build_engine(_bundle(), _causal(DRIVE_LINKED))
        engine.registry.register_process(ClockAdvanceProcess())
        events = [e for e in engine.advance(1)["events"] if e["rule_id"] == "drive-with-driver"]
        self.assertEqual(len(events), 1)
        changed = {c["path"] for c in events[0]["changes"]}
        self.assertIn("entities.delivery-vehicle.components.vehicle.road_position", changed)
        self.assertIn("entities.delivery-driver.components.driver.road_position", changed)
        self.assertEqual(_pos(engine, "delivery-vehicle", "vehicle"), 10)
        self.assertEqual(_pos(engine, "delivery-driver", "driver"), 10)
        self.assertEqual(engine.world.entities["delivery-driver"].last_cause_event_id, events[0]["event_id"])

    def test_link_that_resolves_to_nothing_means_not_due(self):
        b = _bundle()
        next(e for e in b["entities"] if e["id"] == "delivery-vehicle")["owner_ref"] = "unowned"
        engine, _, _ = build_engine(b, _causal(DRIVE_LINKED))
        self.assertEqual([e for e in engine.advance(1)["events"] if e["rule_id"] == "drive-with-driver"], [])
        self.assertEqual(_pos(engine, "delivery-vehicle", "vehicle"), 0)

    def test_out_of_scope_linked_write_is_refused_with_nothing_changed(self):
        engine, _, _ = build_engine(_bundle(), _causal(DRIVE_LINKED))
        process = next(p for p in engine.registry.processes() if p.rule_id == "drive-with-driver")
        process.write_paths = tuple(p for p in process.write_paths if "<driver>" not in p)  # narrow the declared scope
        before = json.dumps(engine.world.material_dict(), sort_keys=True)
        with self.assertRaises(ScopeViolation):
            engine.advance(1)
        self.assertEqual(json.dumps(engine.world.material_dict(), sort_keys=True), before)


LINKED_TRUCK = REPO / "spikes/any-scenario-2026-10/evidence/linked/truck"


class GeneratedTruckTests(unittest.TestCase):  # L4, from the recorded generated-world run
    def test_generated_world_declares_a_linked_driving_process(self):
        causal = json.loads((LINKED_TRUCK / "causal.json").read_text())
        linked = [p for p in causal["processes"] if p.get("participants")]
        movers = [p for p in linked if {e["participant"] for e in p["effects"] if e["path"].endswith("route_position")} >= {"it", "vehicle"}]
        self.assertTrue(movers, "a generated process moves both its entity and the linked vehicle")

    def test_every_drive_event_moves_driver_and_vehicle_together(self):
        import gzip
        with gzip.open(LINKED_TRUCK / "run/events.jsonl.gz", "rt") as fh:
            events = [json.loads(line) for line in fh if line.strip()]
        drives = [e for e in events if e["rule_id"] == "advance-started-driving-interval"]
        self.assertGreaterEqual(len(drives), 10)
        for e in drives:
            after = {c["path"]: c["after"] for c in e["changes"]}
            self.assertEqual(after["entities.delivery-driver.components.driver.route_position"],
                             after["entities.delivery-vehicle.components.vehicle.route_position"], e["event_id"])
        summary = json.loads((LINKED_TRUCK / "run/summary.json").read_text())
        self.assertEqual(summary["ended"], "terminal")


if __name__ == "__main__":
    unittest.main(verbosity=2)
