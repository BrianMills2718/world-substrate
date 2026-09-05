"""Two policies in one world: what the retry fixes, and what it cannot.

The substrate has carried `base_revision` on every action, `stale_revision`
refusal and atomic commit since M1, and no two live policies had ever exercised
any of it.

These tests fix the distinction the first version of the runner got wrong. A
naive loop -- both decide at one revision, both submit, no retry -- refuses
whoever goes second on every single turn. That is starvation manufactured by
the protocol, and it looks exactly like contention until you let the loser try
again.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

_spec = importlib.util.spec_from_file_location(
    "run_contested_world", REPO / "scripts/run_contested_world.py"
)
contested = importlib.util.module_from_spec(_spec)
sys.modules["run_contested_world"] = contested
_spec.loader.exec_module(contested)

from reference_worlds.castaway.probe import build_transfer_engine


class TheWorldSupportsTwoLivePolicies(unittest.TestCase):
    def test_both_actors_get_a_usable_affordance_page(self):
        engine = build_transfer_engine(REPO)
        for actor in contested.WORLDS["castaway"][1]:
            with self.subTest(actor=actor):
                page = engine.discover(actor)
                self.assertTrue(page["available"], f"{actor} was offered nothing")


class OptimisticConcurrencyIsRealAndSoIsTheRetry(unittest.TestCase):
    def test_a_decision_made_before_someone_else_moved_is_refused(self):
        engine = build_transfer_engine(REPO)
        page = engine.discover("robinson")
        stale = dict(page["available"][0]["action"])  # decided at this revision

        engine.submit({**page["available"][1]["action"], "controller": "other"})
        result = engine.submit({**stale, "controller": "me"})

        self.assertEqual(result["status"], "stale_revision")
        failed = [c["label"] for c in result["event"]["checks"] if not c["ok"]]
        self.assertIn("Base revision is current", failed)

    def test_the_retry_removes_the_starvation(self):
        # This is the number that separates a protocol artifact from a finding.
        payload = contested.contested_run(turns=8, world="castaway")
        self.assertEqual(payload["summary"]["refused_after_retry"], 0)
        self.assertEqual(payload["summary"]["refusal_kinds"], [])

    def test_a_stale_retry_is_not_the_same_as_losing_the_thing(self):
        """Two numbers, and only the second one is about the world.

        Whoever commits second is stale every single turn by construction, so
        the retry count saturates and says nothing. What matters is whether the
        plan was still on offer after the other actor moved. In the kitchen's
        first LLM run those read 14 of 14 and 1 of 14; reporting the first as
        contention would have been reporting the loop again.
        """
        payload = contested.contested_run(turns=8, world="castaway")
        summary = payload["summary"]
        self.assertGreater(summary["retried_because_stale"], 0)
        self.assertLessEqual(
            summary["plan_actually_taken_by_the_other"],
            summary["retried_because_stale"],
        )

    def test_the_contested_world_contends_more_than_the_first_one(self):
        """The kitchen was built against a measured shortfall; this is the
        measurement it was built to move, same scripted policy in both."""
        kitchen = contested.contested_run(turns=12, world="kitchen")["summary"]
        castaway = contested.contested_run(turns=12, world="castaway")["summary"]
        self.assertGreater(
            kitchen["plan_actually_taken_by_the_other"],
            castaway["plan_actually_taken_by_the_other"],
        )

    def test_the_run_is_deterministic(self):
        first = contested.contested_run(turns=6, world="kitchen")["summary"]
        second = contested.contested_run(turns=6, world="kitchen")["summary"]
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
