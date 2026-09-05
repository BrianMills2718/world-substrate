"""A declared mechanic may reach one related entity.

Before this, selection and effects were confined to a single entity, so the
only expressible mechanics were per-entity field updates -- clamp or decay a
number. M7 read the resulting triviality as a property of the model. It was at
least partly a property of the language, and these tests fix the wider one.
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
from world_substrate.engine import ScopeViolation


def declaration(**overrides):
    value = {
        "mechanic_id": "workshop.process.held-tool-tires-holder",
        "rationale": "Holding a tool is work.",
        "order": 40,
        "selector": {
            "has_component": "tool",
            "where": [],
            "related": {
                "via": "ownership.owner_ref",
                "as": "holder",
                "has_component": "worker",
                "where": [],
            },
        },
        "effects": [
            {"path": "holder.components.worker.fatigue", "op": "add", "value": 4}
        ],
        "reads": ["entities.<x>.ownership.owner_ref"],
        "writes": ["entities.<x>.components.worker.fatigue"],
    }
    value.update(overrides)
    return value


def install(engine, value):
    compiled = CompiledMechanic(DeclaredMechanic.from_dict(value))
    engine.registry.register_process(compiled)
    engine.world.rule_versions = engine.registry.versions()
    return compiled


def pick_up(engine, item):
    return engine.submit(
        {
            "actor": "mira",
            "kind": "pick_up",
            "item": item,
            "base_revision": engine.world.revision,
            "controller": "test",
        }
    )


class ARelationReachesASecondEntity(unittest.TestCase):
    def test_no_relation_means_no_match(self):
        # The wrench starts owned by the bench, which is not a worker.
        engine = build_engine()
        install(engine, declaration())
        before = engine.world.entities["mira"].components["worker"].fatigue
        engine.advance(1)
        # Only the world's own fatigue process ran.
        self.assertEqual(
            engine.world.entities["mira"].components["worker"].fatigue - before, 3
        )

    def test_the_relation_resolves_once_it_holds(self):
        engine = build_engine()
        install(engine, declaration())
        self.assertEqual(pick_up(engine, "wrench-1")["status"], "accepted")
        self.assertEqual(
            engine.world.entities["wrench-1"].ownership.owner_ref, "actor:mira"
        )
        before = engine.world.entities["mira"].components["worker"].fatigue
        engine.advance(1)
        # 3 from the world's fatigue process, 4 from the tool she now holds.
        self.assertEqual(
            engine.world.entities["mira"].components["worker"].fatigue - before, 7
        )

    def test_a_relation_can_travel_a_plain_entity_id(self):
        # `attached_to` holds a bare id rather than an ownership reference.
        engine = build_engine()
        install(
            engine,
            declaration(
                mechanic_id="workshop.process.attached-part-marks-assembly",
                selector={
                    "has_component": "part",
                    "where": [],
                    "related": {
                        "via": "components.part.attached_to",
                        "as": "target",
                        "has_component": "assembly",
                        "where": [],
                    },
                },
                effects=[
                    {
                        "path": "target.components.assembly.requires_tool",
                        "op": "set",
                        "value": "none",
                    }
                ],
                writes=["entities.<x>.components.assembly.requires_tool"],
            ),
        )
        engine.advance(1)
        # Nothing is attached yet, so the relation resolves for no entity.
        self.assertEqual(
            engine.world.entities["frame-a"].components["assembly"].requires_tool,
            "wrench",
        )
        engine.world.entities["leg-1"].components["part"].attached_to = "frame-a"
        engine.advance(1)
        self.assertEqual(
            engine.world.entities["frame-a"].components["assembly"].requires_tool,
            "none",
        )

    def test_conditions_may_read_the_related_entity(self):
        engine = build_engine()
        install(
            engine,
            declaration(
                selector={
                    "has_component": "tool",
                    "where": [],
                    "related": {
                        "via": "ownership.owner_ref",
                        "as": "holder",
                        "has_component": "worker",
                        "where": [
                            {
                                "path": "components.worker.skill",
                                "op": "gte",
                                "value": 99,
                            }
                        ],
                    },
                },
            ),
        )
        pick_up(engine, "wrench-1")
        before = engine.world.entities["mira"].components["worker"].fatigue
        engine.advance(1)
        # Mira's skill is 2, so the related condition excludes her.
        self.assertEqual(
            engine.world.entities["mira"].components["worker"].fatigue - before, 3
        )


class RelationalWritesAreStillScoped(unittest.TestCase):
    def test_an_undeclared_relational_write_is_refused(self):
        """The first thing an authored mechanic could do that scope must catch.

        Confined to one entity, a declaration would have had to contradict
        itself to violate scope, which is why M7's zero violations said little.
        """
        engine = build_engine()
        install(
            engine,
            declaration(
                mechanic_id="workshop.process.sneaky",
                effects=[
                    {"path": "components.tool.wear", "op": "add", "value": 1},
                    {
                        "path": "holder.components.worker.skill",
                        "op": "subtract",
                        "value": 1,
                    },
                ],
                writes=["entities.<x>.components.tool.wear"],
            ),
        )
        pick_up(engine, "wrench-1")
        skill = engine.world.entities["mira"].components["worker"].skill
        state = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as caught:
            engine.advance(1)
        self.assertIn("components.worker.skill", str(caught.exception))
        self.assertEqual(engine.world.material_hash(), state)
        self.assertEqual(
            engine.world.entities["mira"].components["worker"].skill, skill
        )


class MalformedRelationsAreRefused(unittest.TestCase):
    def bad(self, related, expected):
        with self.assertRaises(DeclarationError) as caught:
            DeclaredMechanic.from_dict(
                declaration(
                    selector={
                        "has_component": "tool",
                        "where": [],
                        "related": related,
                    }
                )
            )
        self.assertIn(expected, str(caught.exception))

    def test_via_must_name_a_real_string_field(self):
        base = {"as": "holder", "has_component": "worker", "where": []}
        self.bad({**base, "via": "ownership.ownre_ref"}, "no field")
        self.bad({**base, "via": "components.tool.wear"}, "string field")
        self.bad({**base, "via": "nonsense.field"}, "unknown component")

    def test_the_bound_name_may_not_shadow_a_component(self):
        self.bad(
            {
                "via": "ownership.owner_ref",
                "as": "ownership",
                "has_component": "worker",
                "where": [],
            },
            "collides",
        )

    def test_the_related_component_must_be_registered(self):
        self.bad(
            {
                "via": "ownership.owner_ref",
                "as": "holder",
                "has_component": "survivor",
                "where": [],
            },
            "unknown component",
        )

    def test_a_relational_effect_path_is_still_type_checked(self):
        with self.assertRaises(DeclarationError) as caught:
            DeclaredMechanic.from_dict(
                declaration(
                    effects=[
                        {
                            "path": "holder.components.worker.fatigue",
                            "op": "set",
                            "value": "tired",
                        }
                    ]
                )
            )
        self.assertIn("fatigue", str(caught.exception))

    def test_an_unbound_prefix_is_not_silently_ignored(self):
        # No `related`, so `holder.` names nothing and must be refused rather
        # than resolving to nothing at runtime.
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                declaration(selector={"has_component": "tool", "where": []})
            )


class TheOldLanguageStillWorks(unittest.TestCase):
    def test_a_single_entity_mechanic_needs_no_relation(self):
        engine = build_engine()
        install(
            engine,
            declaration(
                mechanic_id="workshop.process.tool-rust",
                selector={"has_component": "tool", "where": []},
                effects=[{"path": "components.tool.wear", "op": "add", "value": 2}],
                writes=["entities.<x>.components.tool.wear"],
            ),
        )
        before = engine.world.entities["wrench-1"].components["tool"].wear
        engine.advance(1)
        self.assertEqual(
            engine.world.entities["wrench-1"].components["tool"].wear - before, 2
        )


if __name__ == "__main__":
    unittest.main()
