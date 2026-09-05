"""Decision 002's eight required observability fields are all present.

Observability is the one property Decision 002 makes *required* — it explicitly
demotes exact replay to optional and does not do the same for this. Three of the
eight fields were computed by the engine and never attached, so an inspector
reading `world.events` could not tell who acted, what the attempt meant, or what
the actor had been shown. These tests are the guard against that regressing.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.rules import FillAction, HeatAction


class ObservabilityFieldTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_transfer_engine(REPO)

    def _fill(self):
        return self.engine.apply(
            FillAction(
                "robinson", "clay-pot", "unsafe-pool", 500,
                self.engine.world.revision, "test",
            )
        )

    def test_an_accepted_action_names_its_causal_bearer(self) -> None:
        event = self._fill()["event"]

        self.assertEqual(
            event["causal_bearer"],
            {"kind": "actor", "id": "robinson", "controller": "test"},
        )

    def test_an_action_carries_what_its_actor_could_see_when_it_chose(self) -> None:
        before = self.engine.world.entities["clay-pot"].liquid.volume_ml
        event = self._fill()["event"]

        observation = event["observation"]
        self.assertIsNotNone(observation)
        self.assertEqual(observation["actor_id"], "robinson")
        # Captured before the action applied, not after.
        self.assertEqual(
            observation["entities"]["clay-pot"]["liquid"]["volume_ml"], before
        )
        self.assertNotEqual(
            self.engine.world.entities["clay-pot"].liquid.volume_ml, before
        )

    def test_a_bound_action_carries_its_sense_and_roles(self) -> None:
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "tge", REPO / "tests/test_give_exchange.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        engine = module._exchange_world()

        event = engine.apply(
            module._select_give(engine, "robinson", "cup-robinson", "friday")
        )["event"]

        binding = event["semantic_binding"]
        self.assertEqual(binding["sense_id"], "lc:give_transfer")
        self.assertEqual(binding["roles"]["giver"], "lc.role.donor")

    def test_an_unbound_action_says_null_rather_than_omitting_the_field(self) -> None:
        # `unheat` is the one M1 action kind with no binding, and it has none
        # because the pinned Linguistic Core subset has no sense for removing a
        # vessel from a heat source -- not because nothing was recorded. An
        # explicit null is the difference between those two, so the field must
        # still be present.
        from world_substrate.rules import UnheatAction
        from world_substrate.semantic import SEMANTIC_BINDINGS, UNBOUND_ACTION_KINDS

        self.assertIn("unheat", UNBOUND_ACTION_KINDS)
        self.assertNotIn("unheat", SEMANTIC_BINDINGS)

        self._fill()
        self.engine.apply(
            HeatAction(
                "robinson", "clay-pot", "fire-camp",
                self.engine.world.revision, "test",
            )
        )
        event = self.engine.apply(
            UnheatAction(
                "robinson", "clay-pot", self.engine.world.revision, "test"
            )
        )["event"]

        self.assertEqual(event["status"], "accepted")
        self.assertIn("semantic_binding", event)
        self.assertIsNone(event["semantic_binding"])

    def test_every_other_action_kind_is_bound(self) -> None:
        """C4, honestly scoped: six of seven, and the seventh is named."""
        from world_substrate.semantic import SEMANTIC_BINDINGS, UNBOUND_ACTION_KINDS

        kinds = set(self.engine.registry.action_kinds())
        self.assertEqual(kinds - set(SEMANTIC_BINDINGS), UNBOUND_ACTION_KINDS)
        for kind in sorted(kinds & set(SEMANTIC_BINDINGS)):
            with self.subTest(kind=kind):
                binding = SEMANTIC_BINDINGS[kind]
                # Every binding names a rule that is actually registered.
                self.assertEqual(
                    binding.mechanic_id, self.engine.registry.action(kind).rule_id
                )
                self.assertTrue(binding.sense_id.startswith("lc:"))
                self.assertTrue(
                    all(role.startswith("lc.role.") for role in binding.roles.values())
                )

    def test_a_process_names_itself_as_bearer_and_has_no_observation(self) -> None:
        self.engine.advance(1)

        process_events = [
            event
            for event in self.engine.world.events
            if event["causal_bearer"]["kind"] == "process"
        ]
        self.assertTrue(process_events)
        for event in process_events:
            self.assertIsNone(event["observation"], event["rule_id"])
            self.assertEqual(event["causal_bearer"]["id"], event["rule_id"])

    def test_a_malformed_envelope_still_names_who_claimed_to_act(self) -> None:
        # Every untrusted policy submission arrives through submit(), so these
        # are exactly the events an inspector needs attributed. The bearer is
        # marked claimed_actor because nothing in a malformed envelope has been
        # validated.
        result = self.engine.submit(
            {
                "actor": "robinson",
                "kind": "fill",
                "controller": "policy:llm",
                "base_revision": self.engine.world.revision,
                "vessel": "clay-pot",
                "source": "unsafe-pool",
                "volume_ml": "500",  # string, not int
            }
        )

        self.assertEqual(result["status"], "invalid_action")
        self.assertEqual(
            result["event"]["causal_bearer"],
            {"kind": "claimed_actor", "id": "robinson", "controller": "policy:llm"},
        )
        self.assertIsNotNone(result["event"]["observation"])

    def test_an_envelope_naming_nobody_records_no_bearer_rather_than_guessing(
        self,
    ) -> None:
        result = self.engine.submit({"kind": "fill"})

        self.assertEqual(result["status"], "invalid_action")
        self.assertIsNone(result["event"]["causal_bearer"])
        self.assertIsNone(result["event"]["observation"])

    def test_every_decision_002_field_is_present_on_every_event(self) -> None:
        self._fill()
        self.engine.submit({"actor": "robinson", "kind": "fill"})
        self.engine.advance(2)

        required = {
            "observation",          # what the bearer observed
            "cause",                # what it attempted / what fired
            "semantic_binding",     # sense and roles
            "causal_bearer",        # authority
            "rule_id",              # installed mechanic
            "checks",               # applicability / authorisation
            "declared_write_paths", # proposed and committed changes
            "changes",
            "status",               # refusal reasons
            "hash_after",           # resulting state identity
        }
        self.assertTrue(self.engine.world.events)
        for event in self.engine.world.events:
            self.assertEqual(required - set(event), set(), event["rule_id"])


if __name__ == "__main__":
    unittest.main()
