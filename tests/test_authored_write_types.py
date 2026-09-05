"""Authored declarations may not write a value the field's type forbids.

M7 found a model-authored mechanic setting `ownership.owner_ref` to "" and
nothing in the repository could catch it. That was closed by validating
`owner_ref`. These tests fix the *class* rather than that instance: the
declaration language could put any JSON scalar into any field, and
`World.validate()` covers only some of them.

Each corruption below was observed committing against the live workshop world
before this check existed. The comments record what it did.
"""

from __future__ import annotations

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


def declaration(**overrides):
    value = {
        "mechanic_id": "workshop.process.probe",
        "rationale": "Fixture for type checking.",
        "order": 90,
        "selector": {"has_component": "worker", "where": []},
        "effects": [{"path": "components.worker.fatigue", "op": "add", "value": 1}],
        "reads": [],
        "writes": ["entities.<x>.components.worker.fatigue"],
    }
    value.update(overrides)
    return value


class TypeUnsoundWritesAreRefused(unittest.TestCase):
    """Each of these committed into canonical state before the check existed."""

    def test_string_into_an_integer_field(self):
        # Committed at tick 1, then crashed FatigueProcess -- a correct,
        # hand-written mechanic -- at tick 2, pointing diagnosis at the wrong rule.
        with self.assertRaises(DeclarationError) as caught:
            DeclaredMechanic.from_dict(
                declaration(
                    effects=[
                        {
                            "path": "components.worker.fatigue",
                            "op": "set",
                            "value": "tired",
                        }
                    ]
                )
            )
        self.assertIn("fatigue", str(caught.exception))

    def test_boolean_into_an_integer_field(self):
        # `True` is an `int` to isinstance, so only an exact type check refuses it.
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                declaration(
                    selector={"has_component": "tool", "where": []},
                    effects=[
                        {"path": "components.tool.wear", "op": "set", "value": True}
                    ],
                )
            )

    def test_arithmetic_on_a_string_field(self):
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                declaration(
                    selector={"has_component": "part", "where": []},
                    effects=[
                        {"path": "components.part.part_kind", "op": "add", "value": 1}
                    ],
                )
            )

    def test_wrong_type_into_an_identifier_field(self):
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                declaration(
                    selector={"has_component": "part", "where": []},
                    effects=[
                        {"path": "location.location_id", "op": "set", "value": 0}
                    ],
                )
            )

    def test_an_emptied_location_is_refused_and_rolled_back(self):
        # The worst of the observed corruptions, and the one a type check does
        # *not* catch -- "" is a perfectly good `str`. Before this, it committed:
        # `World.validate()` passed, the snapshot round-tripped, and four of
        # seven entities silently vanished from `observe()` because nothing
        # shared their location any more.
        engine = build_engine()
        visible_before = sorted(engine.observe("mira")["entities"])
        self.assertEqual(len(visible_before), len(engine.world.entities))

        compiled = CompiledMechanic(
            DeclaredMechanic.from_dict(
                declaration(
                    selector={"has_component": "part", "where": []},
                    effects=[
                        {"path": "location.location_id", "op": "set", "value": ""}
                    ],
                    writes=["entities.<x>.location.location_id"],
                )
            )
        )
        engine.registry.register_process(compiled)
        engine.world.rule_versions = engine.registry.versions()
        state_before = engine.world.material_hash()

        with self.assertRaises(ValueError) as caught:
            engine.advance(1)
        self.assertIn("location_id", str(caught.exception))
        # Nothing committed, and every entity is still observable.
        self.assertEqual(engine.world.material_hash(), state_before)
        self.assertEqual(sorted(engine.observe("mira")["entities"]), visible_before)

    def test_validate_rejects_every_emptied_identifier(self):
        """The other identifier fields, on the world that actually has them."""
        from reference_worlds.castaway.probe import build_freshwater_engine
        from world_substrate.model import World

        cases = (
            ("location", "location_id"),
            ("container", "definition_id"),
            ("material", "material_id"),
        )
        for component, field_name in cases:
            with self.subTest(field=field_name):
                engine = build_freshwater_engine()
                holder = next(
                    getattr(entity, component)
                    for entity in engine.world.entities.values()
                    if getattr(entity, component) is not None
                )
                setattr(holder, field_name, "")
                with self.assertRaises(ValueError) as caught:
                    engine.world.validate()
                self.assertIn(field_name, str(caught.exception))
                # And it cannot be smuggled back in through a snapshot.
                with self.assertRaises(ValueError):
                    World.from_snapshot(engine.world.snapshot())


class PathsThatNameNothingAreRefused(unittest.TestCase):
    """Each of these installed cleanly, fired, and changed nothing at all."""

    def test_typo_in_an_effect_path(self):
        with self.assertRaises(DeclarationError) as caught:
            DeclaredMechanic.from_dict(
                declaration(
                    effects=[{"path": "wroker.fatigue", "op": "add", "value": 5}]
                )
            )
        self.assertIn("unknown component", str(caught.exception))

    def test_typo_in_an_effect_field(self):
        with self.assertRaises(DeclarationError) as caught:
            DeclaredMechanic.from_dict(
                declaration(
                    effects=[
                        {
                            "path": "components.worker.fatigeu",
                            "op": "add",
                            "value": 5,
                        }
                    ]
                )
            )
        self.assertIn("no field", str(caught.exception))

    def test_typo_in_a_selector_path(self):
        # The quietest of the three: the condition resolves to None, never
        # matches, and the mechanic is inert for the whole run.
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                declaration(
                    selector={
                        "has_component": "worker",
                        "where": [
                            {
                                "path": "components.worker.fatigeu",
                                "op": "gte",
                                "value": 0,
                            }
                        ],
                    }
                )
            )

    def test_effect_on_a_component_the_selected_entity_lacks_fails_visibly(self):
        # The path is real, so this is refused when it runs rather than when it
        # is declared -- and the tick rolls back rather than committing nothing.
        engine = build_engine()
        compiled = CompiledMechanic(
            DeclaredMechanic.from_dict(
                declaration(
                    effects=[
                        {"path": "components.tool.wear", "op": "add", "value": 5}
                    ],
                    writes=["entities.<x>.components.tool.wear"],
                )
            )
        )
        engine.registry.register_process(compiled)
        engine.world.rule_versions = engine.registry.versions()
        before = engine.world.material_hash()
        with self.assertRaises(DeclarationError):
            engine.advance(1)
        self.assertEqual(engine.world.material_hash(), before)


class HonestDeclarationsStillCompile(unittest.TestCase):
    def test_every_valid_m7_declaration_still_parses(self):
        import json

        evidence = json.loads(
            (REPO / "evidence/m7/authoring-attempts-v0.json").read_text()
        )

        def declarations(node):
            if isinstance(node, dict):
                if "selector" in node and "effects" in node:
                    yield node
                for item in node.values():
                    yield from declarations(item)
            elif isinstance(node, list):
                for item in node:
                    yield from declarations(item)

        parsed = 0
        for value in declarations(evidence):
            try:
                DeclaredMechanic.from_dict(value)
            except DeclarationError:
                continue
            parsed += 1
        # Nine of ten were valid before this change; the tenth named a
        # component rather than a field. None of the nine is type-unsound.
        self.assertEqual(parsed, 9)


if __name__ == "__main__":
    unittest.main()
