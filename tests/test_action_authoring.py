from __future__ import annotations

import json
import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO))

from world_substrate.action_authoring import (
    ActionDeclarationError,
    CausalModel,
    CompiledActionMechanic,
)
from world_substrate.engine import Engine
from world_substrate.model import Entity, LocationState, OwnershipState, PortableState, World
from world_substrate.profile import MechanicProfile
from world_substrate.rules import RuleRegistry

BUNDLE = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())


@dataclass
class FruitState:
    stage: str
    tree_id: str


def causal_model() -> dict:
    return {
        "schema_version": "world-substrate-causal-model/v0",
        "mechanics": [
            {
                "schema_version": "world-substrate-action-mechanic/v0",
                "mechanic_id": "orchard.action.pick",
                "version": "1",
                "action_kind": "pick",
                "rationale": "A worker can take a ripe fruit in the same place; the fruit becomes picked and owned by that worker.",
                "actor_selector": {"categories": ["worker"], "components": []},
                "participants": {
                    "fruit": {"categories": ["fruit"], "components": ["fruit"]}
                },
                "parameters": {},
                "checks": [
                    {
                        "label": "Fruit is ripe",
                        "left": {"participant": {"name": "fruit", "path": "components.fruit.stage"}},
                        "op": "eq",
                        "right": {"literal": "ripe"},
                    },
                    {
                        "label": "Fruit is in the worker's location",
                        "left": {"participant": {"name": "fruit", "path": "location.location_id"}},
                        "op": "eq",
                        "right": {"participant": {"name": "actor", "path": "location.location_id"}},
                    },
                    {
                        "label": "Fruit is in the shared store",
                        "left": {"participant": {"name": "fruit", "path": "ownership.owner_ref"}},
                        "op": "eq",
                        "right": {"literal": "place:orchard"},
                    },
                ],
                "effects": [
                    {
                        "participant": "fruit",
                        "path": "ownership.owner_ref",
                        "op": "set",
                        "value": {"owner_ref": "actor"},
                    },
                    {
                        "participant": "fruit",
                        "path": "components.fruit.stage",
                        "op": "set",
                        "value": {"literal": "picked"},
                    },
                ],
                "limits": ["Picking does not model reach, damage, or carrying capacity."],
                "tests": ["ripe fruit can be picked; already-picked fruit is refused"],
                "semantic_bindings": [],
            }
        ],
        "terminal": {
            "mode": "all",
            "selector": {"categories": ["fruit"], "components": ["fruit"]},
            "checks": [
                {"path": "components.fruit.stage", "op": "eq", "value": "picked"}
            ],
        },
    }


def build_engine(model: CausalModel) -> Engine:
    registry = RuleRegistry()
    profile = MechanicProfile()
    for declared in model.mechanics:
        compiled = CompiledActionMechanic(declared)
        findings = profile.install(declared.package(), compiled)
        assert not [f for f in findings if f.severity == "reject"]
        registry.register_action(compiled)
    profile.freeze()
    entities = {
        "ava": Entity(
            "ava", "Ava", ("worker",), location=LocationState("orchard")
        ),
        "tree-1": Entity(
            "tree-1", "Apple tree", ("tree",), location=LocationState("orchard")
        ),
        "apple-1": Entity(
            "apple-1",
            "Apple",
            ("fruit",),
            location=LocationState("orchard"),
            ownership=OwnershipState("place:orchard"),
            portable=PortableState(True),
            components={"fruit": FruitState("ripe", "tree-1")},
        ),
    }
    world = World(
        world_id="orchard-v0",
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id="world-substrate-orchard@1",
        rule_versions=registry.versions(),
    )
    return Engine(world, registry)


class ActionAuthoringTests(unittest.TestCase):
    def test_declared_action_installs_discovers_commits_and_reaches_terminal(self):
        model = CausalModel.from_dict(causal_model(), bundle=BUNDLE)
        declared = model.mechanics[0]
        self.assertIn("entities.<fruit>.components.fruit.stage", declared.read_paths)
        self.assertIn("entities.<fruit>.ownership.owner_ref", declared.write_paths)
        self.assertIn("entities.<fruit>.last_cause_event_id", declared.write_paths)
        engine = build_engine(model)
        page = engine.discover("ava")
        self.assertEqual(len(page["available"]), 1)
        action = dict(page["available"][0]["action"])
        result = engine.submit({**action, "controller": "test"})
        self.assertEqual(result["status"], "accepted")
        apple = engine.world.entities["apple-1"]
        self.assertEqual(apple.ownership.owner_ref, "actor:ava")
        self.assertEqual(apple.component("fruit").stage, "picked")
        self.assertTrue(apple.last_cause_event_id)
        self.assertTrue(model.terminal and model.terminal.reached(engine.world))
        self.assertEqual(engine.discover("ava")["available"], [])

    def test_review_exposes_derived_authority_not_model_claimed_authority(self):
        model = CausalModel.from_dict(causal_model(), bundle=BUNDLE)
        review = model.as_review()
        row = review["mechanics"][0]
        self.assertIn("entities.<fruit>.ownership.owner_ref", row["writes"])
        self.assertNotIn("writes", causal_model()["mechanics"][0])

    def test_unknown_effect_path_is_rejected_before_installation(self):
        value = causal_model()
        value["mechanics"][0]["effects"][0]["path"] = "components.fruit.magic"
        with self.assertRaisesRegex(ActionDeclarationError, "unknown state path"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_mechanic_cannot_name_a_participant_absent_from_action_signature(self):
        value = causal_model()
        value["mechanics"][0]["participants"]["tree"] = {
            "categories": ["tree"],
            "components": [],
        }
        with self.assertRaisesRegex(ActionDeclarationError, "exactly name entity_ref fields"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_empty_participant_selector_is_rejected(self):
        value = causal_model()
        value["mechanics"][0]["participants"]["fruit"] = {"categories": [], "components": []}
        with self.assertRaisesRegex(ActionDeclarationError, "constrain at least one"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_component_path_requires_participant_selector_to_require_component(self):
        value = causal_model()
        value["mechanics"][0]["participants"]["fruit"]["components"] = []
        with self.assertRaisesRegex(ActionDeclarationError, "does not require component 'fruit'"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_type_incoherent_check_is_rejected(self):
        value = causal_model()
        value["mechanics"][0]["checks"][0]["op"] = "gt"
        value["mechanics"][0]["checks"][0]["right"] = {"literal": 2}
        with self.assertRaisesRegex(ActionDeclarationError, "requires numeric"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_engine_owned_cause_id_cannot_be_authored_as_effect(self):
        value = causal_model()
        value["mechanics"][0]["effects"][0] = {
            "participant": "fruit", "path": "last_cause_event_id", "op": "set",
            "value": {"event_id": True},
        }
        with self.assertRaisesRegex(ActionDeclarationError, "engine-owned"):
            CausalModel.from_dict(value, bundle=BUNDLE)

    def test_entity_id_expression_supports_relational_identity_checks(self):
        value = causal_model()
        value["mechanics"][0]["checks"].append({
            "label": "Fruit is not actor",
            "left": {"entity_id": "fruit"},
            "op": "ne",
            "right": {"entity_id": "actor"},
        })
        model = CausalModel.from_dict(value, bundle=BUNDLE)
        engine = build_engine(model)
        self.assertEqual(len(engine.discover("ava")["available"]), 1)

    def test_scalar_action_fields_require_finite_declared_choices(self):
        bundle = json.loads(json.dumps(BUNDLE))
        bundle["actions"][0]["fields"].append({"name": "count", "type": "integer"})
        value = causal_model()
        with self.assertRaisesRegex(ActionDeclarationError, "parameters must exactly"):
            CausalModel.from_dict(value, bundle=bundle)
        value["mechanics"][0]["parameters"] = {"count": [1, 2]}
        model = CausalModel.from_dict(value, bundle=bundle)
        self.assertEqual(model.mechanics[0].parameters["count"], (1, 2))


if __name__ == "__main__":
    unittest.main()
