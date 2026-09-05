"""A thing can be held by nobody.

Two of ten M7b proposals meant "this is no longer held" and could only say it
by blanking `ownership.owner_ref`. Making that a checked reference correctly
refused them and left the intent inexpressible: the refusal made a missing
capability visible without supplying one.

The declaration under test is read from M7b's own evidence file rather than
retyped, so this is the mechanic a model actually wrote.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.workshop.probe import build_engine
from world_substrate.authoring import (
    CompiledMechanic,
    DeclarationError,
    DeclaredMechanic,
)
from world_substrate.model import UNOWNED, owner_ref, parse_owner_ref

EVIDENCE = REPO / "evidence/m7/authoring-attempts-relational-v1.json"


def authored(mechanic_id: str) -> dict:
    """The declaration a model actually produced, from retained evidence."""
    payload = json.loads(EVIDENCE.read_text())
    for attempt in payload["attempts"]:
        value = attempt["declaration"]
        if isinstance(value, dict) and value.get("mechanic_id") == mechanic_id:
            return value
    raise AssertionError(f"{mechanic_id} not in {EVIDENCE}")


class UnownedIsAValidReference(unittest.TestCase):
    def test_it_parses_as_naming_no_owner(self):
        self.assertEqual(parse_owner_ref(UNOWNED), (UNOWNED, ""))
        self.assertEqual(parse_owner_ref(owner_ref("actor", "mira")), ("actor", "mira"))

    def test_the_empty_string_is_still_refused(self):
        engine = build_engine()
        engine.world.entities["wrench-1"].ownership.owner_ref = ""
        with self.assertRaises(ValueError):
            engine.world.validate()

    def test_an_unowned_entity_validates_and_round_trips(self):
        from world_substrate.model import World

        engine = build_engine()
        engine.world.entities["wrench-1"].ownership.owner_ref = UNOWNED
        engine.world.validate()
        World.from_snapshot(engine.world.snapshot())

    def test_nobody_holds_an_unowned_thing(self):
        from reference_worlds.workshop.mechanics import _held_by

        engine = build_engine()
        engine.submit(
            {
                "actor": "mira",
                "kind": "pick_up",
                "item": "wrench-1",
                "base_revision": engine.world.revision,
                "controller": "test",
            }
        )
        self.assertIn("wrench-1", _held_by(engine.world, "mira"))
        engine.world.entities["wrench-1"].ownership.owner_ref = UNOWNED
        self.assertNotIn("wrench-1", _held_by(engine.world, "mira"))


class TheAuthoredDropMechanicNowWorks(unittest.TestCase):
    """C3: the intent behind M7b's `worn-tool-drop`, end to end."""

    def declaration(self):
        return authored("workshop.process.worn-tool-drop")

    def test_as_the_model_wrote_it_it_is_still_refused(self):
        # The model set owner_ref to "". That stays a malformed reference.
        value = self.declaration()
        self.assertEqual(value["effects"][0]["value"], "")
        engine = build_engine()
        engine.registry.register_process(
            CompiledMechanic(DeclaredMechanic.from_dict(value))
        )
        engine.world.rule_versions = engine.registry.versions()
        engine.world.entities["wrench-1"].components["tool"].wear = 100
        engine.submit(
            {
                "actor": "mira",
                "kind": "pick_up",
                "item": "wrench-1",
                "base_revision": engine.world.revision,
                "controller": "test",
            }
        )
        with self.assertRaises(ValueError):
            engine.advance(1)

    def test_with_the_vocabulary_it_now_had_it_installs_fires_and_drops(self):
        # The only edit is the value the model had no way to express.
        value = self.declaration()
        value["effects"][0]["value"] = UNOWNED

        engine = build_engine()
        engine.registry.register_process(
            CompiledMechanic(DeclaredMechanic.from_dict(value))
        )
        engine.world.rule_versions = engine.registry.versions()
        engine.submit(
            {
                "actor": "mira",
                "kind": "pick_up",
                "item": "wrench-1",
                "base_revision": engine.world.revision,
                "controller": "test",
            }
        )
        # `advance` commits by swapping in a clone, so an entity handle taken
        # before it is stale afterwards. Always re-read through the engine.
        wrench = lambda: engine.world.entities["wrench-1"]
        self.assertEqual(wrench().ownership.owner_ref, owner_ref("actor", "mira"))

        # Not worn out yet, so the mechanic must not fire.
        engine.advance(1)
        self.assertNotEqual(wrench().ownership.owner_ref, UNOWNED)

        wrench().components["tool"].wear = 100
        engine.advance(1)
        self.assertEqual(
            parse_owner_ref(wrench().ownership.owner_ref)[0], UNOWNED
        )
        self.assertEqual(wrench().ownership.owner_ref, UNOWNED)
        # It fired as an ordinary causal event, not a silent mutation.
        self.assertTrue(
            any(
                event["rule_id"] == "workshop.process.worn-tool-drop"
                for event in engine.world.events
            )
        )

    def test_a_still_malformed_reference_is_refused_at_declaration(self):
        value = self.declaration()
        value["effects"][0]["value"] = 0
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(value)


if __name__ == "__main__":
    unittest.main()
