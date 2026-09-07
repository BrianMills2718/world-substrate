"""Rule code cannot mutate outside the enclosing engine transition.

Write-scope tests cover material paths a rule changes during apply(). These
negative controls cover the stronger coordinator boundary: discovery and
applicability hooks are read-only, command/event history belongs to the engine,
and revision is advanced only by the engine after a proposal is accepted.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.engine import ScopeViolation
from world_substrate.mechanisms.liquid import FillRule
from world_substrate.mechanisms.thermal import ThermalProcess
from world_substrate.mechanisms.time import HydrationDecayProcess


def _swap_action(engine, rule) -> None:
    engine.registry._actions[rule.action_kind] = rule


def _swap_process(engine, process) -> None:
    for index, existing in enumerate(engine.registry._processes):
        if existing.rule_id == process.rule_id:
            engine.registry._processes[index] = process
            return
    raise AssertionError(f"no registered process {process.rule_id} to replace")


def _fill_envelope(engine, *, minimum: int = 1) -> dict:
    row = next(
        item
        for item in engine.discover("robinson", kind="fill")["available"]
        if item["action"]["vessel"] == "clay-pot"
        and item["action"]["source"] == "unsafe-pool"
        and item["action"]["volume_ml"] >= minimum
    )
    return {**row["action"], "controller": "authority-test"}


def _fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


class MutatingDiscoverFillRule(FillRule):
    def discover(self, world, actor_id):
        world.entities[actor_id].actor.health = 99
        return super().discover(world, actor_id)


class MutatingChecksFillRule(FillRule):
    def checks(self, world, action):
        world.revision += 7
        return super().checks(world, action)


class MutatingConsequencesFillRule(FillRule):
    def consequences(self, world, action):
        world.entities[action.actor_id].actor.health = 99
        return super().consequences(world, action)


class MutatingProgressThermalProcess(ThermalProcess):
    def progress(self, world):
        world.tick += 10
        return super().progress(world)


class MutatingDueHydrationProcess(HydrationDecayProcess):
    def due(self, world):
        world.entities["robinson"].actor.health = 99
        return True


class MutatingHistoryFillRule(FillRule):
    def apply(self, world, action, event_id):
        super().apply(world, action, event_id)
        if world.events:
            world.events[0]["status"] = "tampered"
        else:
            world.events.append({"event_id": "forged", "status": "accepted"})
        world.commands.append({"command_id": "forged", "op": "action"})


class MutatingRevisionFillRule(FillRule):
    def apply(self, world, action, event_id):
        super().apply(world, action, event_id)
        world.revision += 100


class MutatingHistoryHydrationProcess(HydrationDecayProcess):
    def apply(self, world):
        super().apply(world)
        world.events.append({"event_id": "forged", "status": "accepted"})


class ReadOnlyHooksAreActuallyReadOnly(unittest.TestCase):
    def test_discover_cannot_mutate_canonical_state(self) -> None:
        engine = build_transfer_engine(REPO)
        _swap_action(engine, MutatingDiscoverFillRule())
        before = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.discover("robinson", kind="fill")

        self.assertIn(".discover mutated a read-only rule view", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(engine.world.entities["robinson"].actor.health, 100)
        self.assertEqual(engine.world.commands, [])
        self.assertEqual(engine.world.events, [])

    def test_checks_are_refused_if_they_write(self) -> None:
        engine = build_transfer_engine(REPO)
        envelope = _fill_envelope(engine)
        _swap_action(engine, MutatingChecksFillRule())
        before = engine.world.material_hash()

        result = engine.submit(envelope)

        self.assertEqual(result["status"], "scope_violation")
        self.assertEqual(engine.world.material_hash(), before)
        failing = [check for check in result["event"]["checks"] if not check["ok"]]
        self.assertEqual(failing[-1]["label"], "Rule checks are read-only")
        self.assertEqual(failing[-1]["actual"], ["revision"])
        self.assertTrue(engine.replay()["ok"])

    def test_consequences_cannot_write(self) -> None:
        engine = build_transfer_engine(REPO)
        _swap_action(engine, MutatingConsequencesFillRule())
        before = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.discover("robinson", kind="fill")

        self.assertIn(".consequences mutated a read-only rule view", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(engine.world.entities["robinson"].actor.health, 100)

    def test_progress_cannot_write(self) -> None:
        engine = build_transfer_engine(REPO)
        _swap_process(engine, MutatingProgressThermalProcess())
        before = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.discover("robinson")

        self.assertIn(".progress mutated a read-only rule view", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(engine.world.tick, 0)

    def test_due_cannot_write_and_the_tick_is_rolled_back(self) -> None:
        engine = build_transfer_engine(REPO)
        _swap_process(engine, MutatingDueHydrationProcess())
        before = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.advance(1)

        self.assertIn(".due mutated a read-only rule view", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(engine.world.tick, 0)
        self.assertEqual(engine.world.commands, [])
        self.assertEqual(engine.world.events, [])


class EngineOwnedStateStaysEngineOwned(unittest.TestCase):
    def test_action_rule_cannot_touch_history_or_prior_events(self) -> None:
        engine = build_transfer_engine(REPO)
        first = engine.submit(_fill_envelope(engine))
        self.assertEqual(first["status"], "accepted")
        prior_fingerprint = _fingerprint(engine.world.events[0])
        before = engine.world.material_hash()
        envelope = _fill_envelope(engine)
        _swap_action(engine, MutatingHistoryFillRule())

        result = engine.submit(envelope)

        self.assertEqual(result["status"], "scope_violation")
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(_fingerprint(engine.world.events[0]), prior_fingerprint)
        failing = [check for check in result["event"]["checks"] if not check["ok"]]
        self.assertEqual(
            failing[-1]["label"], "Rules cannot write engine-owned state or history"
        )
        self.assertEqual(failing[-1]["actual"], ["commands", "events"])

    def test_action_rule_cannot_advance_revision(self) -> None:
        engine = build_transfer_engine(REPO)
        envelope = _fill_envelope(engine)
        _swap_action(engine, MutatingRevisionFillRule())
        before = engine.world.material_hash()

        result = engine.submit(envelope)

        self.assertEqual(result["status"], "scope_violation")
        self.assertEqual(engine.world.material_hash(), before)
        failing = [check for check in result["event"]["checks"] if not check["ok"]]
        self.assertEqual(failing[-1]["actual"], ["revision"])
        self.assertEqual(engine.world.revision, 0)
        self.assertTrue(engine.replay()["ok"])

    def test_process_rule_cannot_touch_history(self) -> None:
        engine = build_transfer_engine(REPO)
        _swap_process(engine, MutatingHistoryHydrationProcess())
        before = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.advance(1)

        self.assertIn("wrote engine-owned state or history", str(raised.exception))
        self.assertIn("events", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        self.assertEqual(engine.world.commands, [])
        self.assertEqual(engine.world.events, [])


if __name__ == "__main__":
    unittest.main()
