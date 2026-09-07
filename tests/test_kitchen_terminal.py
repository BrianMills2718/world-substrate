"""The kitchen service ends when its represented work is actually done."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.kitchen.probe import build_engine
from reference_worlds.kitchen.terminal import service_complete

_spec = importlib.util.spec_from_file_location(
    "terminal_contested_run", REPO / "scripts/run_contested_world.py"
)
runner = importlib.util.module_from_spec(_spec)
sys.modules["terminal_contested_run"] = runner
_spec.loader.exec_module(runner)


class CompletionComesFromOrderState(unittest.TestCase):
    def test_a_fresh_service_is_not_complete(self) -> None:
        engine = build_engine(REPO)
        self.assertFalse(service_complete(engine.world))

    def test_one_filled_order_is_not_the_end(self) -> None:
        engine = build_engine(REPO)
        engine.world.entities["order-stew"].components["order"].filled = True
        self.assertFalse(service_complete(engine.world))

    def test_every_filled_order_is_terminal(self) -> None:
        engine = build_engine(REPO)
        for entity in engine.world.entities.values():
            order = entity.component("order")
            if order is not None:
                order.filled = True
        self.assertTrue(service_complete(engine.world))

    def test_the_runner_uses_the_kitchen_terminal_condition(self) -> None:
        self.assertIs(runner.WORLD_TERMINALS["kitchen"], service_complete)


class AWorldCanEndBeforeTheTurnCeiling(unittest.TestCase):
    def test_terminal_predicate_stops_before_another_decision(self) -> None:
        # Exercise the generic runner seam without needing a policy that happens
        # to complete the whole kitchen. Castaway has deterministic scripted
        # actions and a canonical tick, so two completed ticks are an exact
        # synthetic terminal condition for this test only.
        saved = runner.WORLD_TERMINALS.get("castaway")
        runner.WORLD_TERMINALS["castaway"] = lambda world: world.tick >= 2
        try:
            payload = runner.contested_run(turns=10, world="castaway")
        finally:
            if saved is None:
                runner.WORLD_TERMINALS.pop("castaway", None)
            else:
                runner.WORLD_TERMINALS["castaway"] = saved

        self.assertEqual(payload["schema_version"], "world-substrate-contested-run/v3")
        self.assertEqual(payload["turns_run"], 2)
        self.assertEqual(payload["summary"]["turns"], 2)
        self.assertTrue(payload["summary"]["terminal_reached"])
        self.assertEqual(len(payload["transcript"]), 2)

    def test_open_ended_world_still_runs_to_its_ceiling(self) -> None:
        payload = runner.contested_run(turns=3, world="castaway")
        self.assertEqual(payload["turns_run"], 3)
        self.assertFalse(payload["summary"]["terminal_reached"])


if __name__ == "__main__":
    unittest.main()
