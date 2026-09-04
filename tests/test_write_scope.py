"""Declared write scopes are enforced, not merely recorded.

Root CLAUDE.md, docs/architecture.md, and docs/contracts/transition-envelope-v0.md
all state that a mechanic may write only within its declared state-path scope.
Before this slice the engine copied `write_paths` onto the event as
`declared_write_paths` and never compared it to what changed, so the invariant
held only by the good behaviour of hand-reviewed rules.

These are the negative controls: rules that deliberately violate their own
declaration, which must be refused rather than committed. The positive control
is the rest of the suite -- every registered M1 rule and process passes with the
guard active.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.engine import Engine, ScopeViolation
from world_substrate.mechanisms.liquid import DrinkRule
from world_substrate.mechanisms.ownership import GiveRule
from world_substrate.mechanisms.time import HydrationDecayProcess
from world_substrate.model import World
from world_substrate.rules import DrinkAction, FillAction, GiveAction


def _two_owner_engine() -> Engine:
    """The M1 transfer world with friday holding clay-pot, as in M2."""
    engine = build_transfer_engine()
    world = World.from_snapshot(engine.initial_snapshot())
    world.entities["clay-pot"].ownership.owner_ref = "actor:friday"
    world.rule_versions = engine.registry.versions()
    return Engine(world, engine.registry)


def _swap_action(engine: Engine, rule) -> None:
    """Replace a registered action rule, keeping rule_id and version stable."""
    engine.registry._actions[rule.action_kind] = rule


def _swap_process(engine: Engine, process) -> None:
    for index, existing in enumerate(engine.registry._processes):
        if existing.rule_id == process.rule_id:
            engine.registry._processes[index] = process
            return
    raise AssertionError(f"no registered process {process.rule_id} to replace")


class ReachesOtherComponentsGiveRule(GiveRule):
    """Declares only ownership writes; also drains health and fuel."""

    def apply(self, world, action, event_id) -> None:
        super().apply(world, action, event_id)
        world.entities[action.target_actor_id].actor.health = 1
        world.entities["fire-camp"].heat_source.fuel = 0


class ReachesThirdPartyDrinkRule(DrinkRule):
    """Declares `entities.<actor>.actor.health` -- and harms a different actor."""

    def apply(self, world, action, event_id) -> None:
        super().apply(world, action, event_id)
        bystander = next(
            entity
            for entity in world.entities.values()
            if entity.actor is not None and entity.entity_id != action.actor_id
        )
        bystander.actor.health = 1


class ReachesHealthHydrationProcess(HydrationDecayProcess):
    """Declares only hydration; also writes health."""

    def apply(self, world) -> None:
        super().apply(world)
        for entity in world.entities.values():
            if entity.actor is not None:
                entity.actor.health = 1


class WriteScopeTests(unittest.TestCase):
    def test_action_reaching_undeclared_components_is_refused(self) -> None:
        engine = _two_owner_engine()
        _swap_action(engine, ReachesOtherComponentsGiveRule())
        before_hash = engine.world.material_hash()

        result = engine.apply(
            GiveAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                target_actor_id="friday",
                base_revision=engine.world.revision,
                controller_id="test",
            )
        )

        self.assertEqual(result["status"], "scope_violation")
        failing = [check for check in result["event"]["checks"] if not check["ok"]]
        self.assertEqual(len(failing), 1)
        self.assertEqual(
            failing[0]["label"], "Committed writes stay in declared scope"
        )
        self.assertEqual(
            failing[0]["actual"],
            ["entities.fire-camp.heat_source.fuel", "entities.friday.actor.health"],
        )
        # Nothing committed: not even the transfer the rule was entitled to make.
        self.assertEqual(engine.world.material_hash(), before_hash)
        self.assertEqual(
            engine.world.entities["cup-robinson"].ownership.owner_ref,
            "actor:robinson",
        )
        self.assertEqual(engine.world.entities["friday"].actor.health, 100)

    def test_action_reaching_a_third_party_through_a_declared_shape_is_refused(
        self,
    ) -> None:
        # `entities.<actor>.actor.health` is genuinely declared by DrinkRule.
        # The placeholder may only bind to an entity the attempt itself names,
        # so harming a bystander is still out of scope.
        engine = _two_owner_engine()
        _swap_action(engine, ReachesThirdPartyDrinkRule())
        # Vessels start empty; fill through the ordinary registered path so the
        # drink itself has a real precondition-satisfying subject.
        engine.apply(
            FillAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                source_id="unsafe-pool",
                volume_ml=250,
                base_revision=engine.world.revision,
                controller_id="test",
            )
        )
        before_hash = engine.world.material_hash()

        result = engine.apply(
            DrinkAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                volume_ml=250,
                base_revision=engine.world.revision,
                controller_id="test",
            )
        )

        self.assertEqual(result["status"], "scope_violation")
        failing = [check for check in result["event"]["checks"] if not check["ok"]]
        self.assertEqual(failing[0]["actual"], ["entities.friday.actor.health"])
        self.assertEqual(engine.world.material_hash(), before_hash)
        self.assertEqual(engine.world.entities["friday"].actor.health, 100)

    def test_process_reaching_undeclared_state_stops_the_tick(self) -> None:
        engine = _two_owner_engine()
        _swap_process(engine, ReachesHealthHydrationProcess())
        before_hash = engine.world.material_hash()

        with self.assertRaises(ScopeViolation) as raised:
            engine.advance(1)

        self.assertIn("process.actor.hydration-decay", str(raised.exception))
        self.assertIn("entities.robinson.actor.health", str(raised.exception))
        # advance() restores the whole tick, including the earlier clock process.
        self.assertEqual(engine.world.material_hash(), before_hash)
        self.assertEqual(engine.world.tick, 0)

    def test_a_refused_scope_violation_replays_identically(self) -> None:
        # The new status enters the retained command log, so replay from the
        # initial snapshot must reproduce it rather than diverge.
        engine = _two_owner_engine()
        _swap_action(engine, ReachesOtherComponentsGiveRule())
        engine.apply(
            GiveAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                target_actor_id="friday",
                base_revision=engine.world.revision,
                controller_id="test",
            )
        )
        self.assertEqual(
            [command["status"] for command in engine.world.commands],
            ["scope_violation"],
        )

        replay = engine.replay()

        self.assertTrue(replay["ok"])
        self.assertTrue(replay["event_match"])

    def test_registered_m1_rules_stay_within_their_declared_scope(self) -> None:
        # Positive control: the guard is not vacuous only because nothing
        # exercises it. The full committed give path runs unchanged.
        engine = _two_owner_engine()

        result = engine.apply(
            GiveAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                target_actor_id="friday",
                base_revision=engine.world.revision,
                controller_id="test",
            )
        )

        self.assertEqual(result["status"], "accepted")
        self.assertEqual(
            engine.world.entities["cup-robinson"].ownership.owner_ref, "actor:friday"
        )
        engine.advance(3)
        self.assertEqual(engine.world.tick, 3)


if __name__ == "__main__":
    unittest.main()
