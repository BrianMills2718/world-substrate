"""A policy chooses; it never causes.

The consequence boundary is `world_substrate.policy.resolve_choice`: whatever a
policy returns is matched against the action_ids the engine itself produced for
the current revision. These tests drive that seam with scripted policies, so
they establish the boundary without spending anything. Whether a *model* can
play the world well is a different question and is answered by
`scripts/run_llm_policy.py` and its retained evidence.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.policy import (
    ScriptedPolicy,
    apply_choice,
    present,
    resolve_choice,
)

ACTOR = "robinson"


class PolicySeamTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_transfer_engine(REPO)
        self.page = self.engine.discover(ACTOR)
        self.before = self.engine.world.material_hash()

    def _drive(self, answer: str):
        policy = ScriptedPolicy([answer])
        action_id, reasoning = policy.select(self.page, {})
        choice = resolve_choice(self.page, action_id, reasoning)
        result = apply_choice(self.engine, choice, controller="test")
        return choice, result

    def test_an_invented_action_id_causes_nothing(self) -> None:
        choice, result = self._drive("deadbeefcafe")

        self.assertEqual(choice.kind, "refused")
        self.assertIn("no action the world offered", choice.refusal_reason)
        self.assertIsNone(result)
        self.assertEqual(self.engine.world.material_hash(), self.before)

    def test_prose_that_looks_like_an_action_causes_nothing(self) -> None:
        # The failure this boundary exists to prevent: a policy describing an
        # effect and the effect happening. Nothing parses policy text into an
        # action, so even a well-formed description is inert.
        choice, result = self._drive(
            '{"kind": "drink", "actor": "robinson", "vessel": "clay-pot", '
            '"volume_ml": 250}'
        )

        self.assertEqual(choice.kind, "refused")
        self.assertIsNone(result)
        self.assertEqual(self.engine.world.material_hash(), self.before)

    def test_choosing_a_blocked_action_is_refused_with_that_reason(self) -> None:
        blocked = self.page["blocked"]
        self.assertTrue(blocked, "fixture should offer at least one blocked action")

        choice, result = self._drive(blocked[0]["action_id"])

        self.assertEqual(choice.kind, "refused")
        self.assertIn("currently blocks", choice.refusal_reason)
        self.assertIsNone(result)
        self.assertEqual(self.engine.world.material_hash(), self.before)

    def test_a_genuinely_offered_action_commits(self) -> None:
        offered = self.page["available"][0]

        choice, result = self._drive(offered["action_id"])

        self.assertEqual(choice.kind, "action")
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "accepted")
        self.assertNotEqual(self.engine.world.material_hash(), self.before)

    def test_wait_commits_nothing_but_time_still_passes(self) -> None:
        choice, result = self._drive("wait")

        self.assertEqual(choice.kind, "wait")
        self.assertIsNone(result)
        self.assertEqual(self.engine.world.material_hash(), self.before)
        self.engine.advance(1)
        self.assertEqual(self.engine.world.tick, 1)

    def test_live_policy_prompt_treats_installed_effect_preview_as_authoritative(self) -> None:
        prompt = (REPO / "prompts/generic_world_policy.yaml").read_text()
        self.assertIn("preview derived from the installed world mechanic", prompt)
        self.assertIn("Treat it as authoritative", prompt)
        self.assertIn("Do not", prompt)
        self.assertIn("absent from that preview", prompt)

    def test_the_view_a_policy_receives_is_lossy_and_carries_no_authority(
        self,
    ) -> None:
        context = present(self.engine, ACTOR, self.page)

        # It sees a rendered summary, not canonical state, and the action list
        # is the engine's own -- ids included.
        self.assertIsInstance(context["visible"], str)
        self.assertEqual(
            [row["action_id"] for row in context["actions"]],
            [row["action_id"] for row in self.page["available"]],
        )
        self.assertNotIn("material_hash", context)
        self.assertNotIn("revision", context)


if __name__ == "__main__":
    unittest.main()
