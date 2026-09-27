"""advance() reports only events it actually committed.

A due process whose apply() leaves material state unchanged commits no event,
so it must not appear in advance()'s returned events list either.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.mechanisms.time import HydrationDecayProcess


class DueNoOpHydrationProcess(HydrationDecayProcess):
    def due(self, world):
        return True

    def apply(self, world):
        return None


class AdvanceEventsTests(unittest.TestCase):
    def test_due_process_without_change_returns_no_phantom_event(self) -> None:
        engine = build_transfer_engine(REPO)
        registry = engine.registry._processes
        index = next(
            i for i, p in enumerate(registry) if p.rule_id == HydrationDecayProcess.rule_id
        )
        registry[index] = DueNoOpHydrationProcess()
        committed_before = len(engine.world.events)

        result = engine.advance(3)

        committed = engine.world.events[committed_before:]
        self.assertNotIn({}, result["events"])
        self.assertEqual(result["events"], committed)
        self.assertTrue(engine.replay()["ok"])


if __name__ == "__main__":
    unittest.main()
