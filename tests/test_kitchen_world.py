"""A third world, built to be contested.

Castaway asked whether a world runs; the workshop asked whether the contracts
transfer. This one was built against a measured requirement: the two-agent
Castaway run spent six of ten turns with both agents correctly waiting, because
that world has one pot, one cup and one fire and nothing to compete over.

So this world has two cooks with *different* orders, one knife, two burners, and
exactly enough ingredients that wasting one loses a dish.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.kitchen.probe import build_engine


def act(engine, actor, **fields):
    return engine.submit(
        {
            "actor": actor,
            "base_revision": engine.world.revision,
            "controller": "test",
            **fields,
        }
    )


def accept(engine, actor, **fields):
    result = act(engine, actor, **fields)
    assert result["status"] == "accepted", (
        fields.get("kind"),
        result["status"],
        [c for c in result["event"]["checks"] if not c["ok"]],
    )
    return result


class TheWorldIsScarceByConstruction(unittest.TestCase):
    def test_there_is_exactly_enough_of_everything(self):
        engine = build_engine()
        have: dict[str, int] = {}
        need: dict[str, int] = {}
        for entity in engine.world.entities.values():
            ingredient = entity.component("ingredient")
            if ingredient is not None:
                have[ingredient.kind] = have.get(ingredient.kind, 0) + 1
            order = entity.component("order")
            if order is not None:
                for kind in order.wants:
                    need[kind] = need.get(kind, 0) + 1
        self.assertEqual(have, need, "the world must have zero slack")

    def test_the_two_cooks_want_different_dishes(self):
        engine = build_engine()
        orders = {
            entity.component("cook").order_id
            for entity in engine.world.entities.values()
            if entity.component("cook") is not None
        }
        self.assertEqual(len(orders), 2)

    def test_there_is_one_knife_and_two_burners(self):
        engine = build_engine()
        knives = [
            e for e in engine.world.entities.values()
            if (t := e.component("kitchen_tool")) is not None and t.tool_kind == "knife"
        ]
        burners = [
            e for e in engine.world.entities.values() if e.component("burner") is not None
        ]
        self.assertEqual(len(knives), 1)
        self.assertEqual(len(burners), 2)


class OneOrderEndToEnd(unittest.TestCase):
    def test_a_cook_can_fill_their_dish(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="knife")
        for item, burner in (("onion-1", "burner-1"), ("carrot-1", "burner-2")):
            accept(engine, "ama", kind="take", item=item)
            accept(engine, "ama", kind="chop", item=item)
            accept(engine, "ama", kind="cook", item=item, burner=burner)
            accept(engine, "ama", kind="plate", item=item, order="order-stew")
        self.assertEqual(
            engine.world.entities["ama"].components["cook"].plated, ["onion", "carrot"]
        )
        self.assertTrue(
            engine.world.entities["order-stew"].components["order"].filled
        )


class EachStageNeedsItsContestedResource(unittest.TestCase):
    def test_chopping_needs_the_knife(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="onion-1")
        result = act(engine, "ama", kind="chop", item="onion-1")
        self.assertEqual(result["status"], "precondition_failed")
        self.assertIn(
            "You are holding the knife",
            [c["label"] for c in result["event"]["checks"] if not c["ok"]],
        )

    def test_cooking_needs_a_free_burner(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="knife")
        for item in ("onion-1", "carrot-1"):
            accept(engine, "ama", kind="take", item=item)
            accept(engine, "ama", kind="chop", item=item)
        accept(engine, "ama", kind="cook", item="onion-1", burner="burner-1")
        result = act(engine, "ama", kind="cook", item="carrot-1", burner="burner-1")
        self.assertEqual(result["status"], "precondition_failed")
        self.assertIn(
            "The burner is free",
            [c["label"] for c in result["event"]["checks"] if not c["ok"]],
        )
        # ...and the other burner is still available, so two can cook at once.
        accept(engine, "ama", kind="cook", item="carrot-1", burner="burner-2")

    def test_a_burner_frees_itself_next_tick(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="knife")
        accept(engine, "ama", kind="take", item="onion-1")
        accept(engine, "ama", kind="chop", item="onion-1")
        accept(engine, "ama", kind="cook", item="onion-1", burner="burner-1")
        self.assertEqual(
            engine.world.entities["burner-1"].components["burner"].occupied_by, "ama"
        )
        engine.advance(1)
        self.assertEqual(
            engine.world.entities["burner-1"].components["burner"].occupied_by, ""
        )

    def test_only_one_cook_can_hold_the_knife(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="knife")
        result = act(engine, "bo", kind="take", item="knife")
        self.assertEqual(result["status"], "precondition_failed")
        self.assertIn(
            "Nobody else is holding it",
            [c["label"] for c in result["event"]["checks"] if not c["ok"]],
        )


class ACookHasAuthorityOverTheirOwnOrderOnly(unittest.TestCase):
    def test_you_cannot_plate_toward_someone_elses_dish(self):
        engine = build_engine()
        accept(engine, "ama", kind="take", item="knife")
        accept(engine, "ama", kind="take", item="onion-1")
        accept(engine, "ama", kind="chop", item="onion-1")
        accept(engine, "ama", kind="cook", item="onion-1", burner="burner-1")
        result = act(engine, "ama", kind="plate", item="onion-1", order="order-hash")
        self.assertEqual(result["status"], "precondition_failed")
        self.assertIn(
            "It is your own order",
            [c["label"] for c in result["event"]["checks"] if not c["ok"]],
        )


class TheWorldCannotDeadlock(unittest.TestCase):
    """Found by running it, not by designing it.

    With take and no release, the first distribution of the knife and the
    ingredients was permanent: Ama held ingredients, Bo held the knife, and
    after five turns both had zero available actions, each blocked on "nobody
    else is holding it" for what the other had.
    """

    def test_hoarding_starves_the_other_cook_but_does_not_stop_the_world(self):
        """The distinction that matters, and my first version of this test got
        it wrong by asserting the stronger thing.

        If one cook holds everything the other genuinely has nothing to do --
        that is a real and reasonable state, not a bug. What must never happen
        is that *nobody* can move, because no agent could then resolve it.
        """
        engine = build_engine()
        for item in ("knife", "onion-1", "onion-2", "carrot-1", "potato-1"):
            accept(engine, "ama", kind="take", item=item)

        self.assertEqual(engine.discover("bo")["available"], [], "bo should be starved")
        self.assertTrue(
            engine.discover("ama")["available"],
            "the world is deadlocked: neither cook can move",
        )

        # And the starvation is recoverable by the cook who caused it.
        releases = [
            row for row in engine.discover("ama")["available"]
            if row["action"]["kind"] == "put_down"
        ]
        self.assertTrue(releases)
        accept(engine, "ama", kind="put_down", item="knife")
        self.assertEqual(
            engine.world.entities["knife"].ownership.owner_ref, "place:kitchen"
        )
        takeable = [
            row["action"]["item"] for row in engine.discover("bo")["available"]
            if row["action"]["kind"] == "take"
        ]
        self.assertIn("knife", takeable)

    def test_nobody_is_ever_left_with_no_move(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "rcw", REPO / "scripts/run_contested_world.py"
        )
        runner = importlib.util.module_from_spec(spec)
        sys.modules["rcw"] = runner
        spec.loader.exec_module(runner)

        payload = runner.contested_run(turns=10, world="kitchen")
        stuck = [
            (t["turn"], actor)
            for t in payload["transcript"]
            for actor in payload["actors"]
            if t["actors"][actor]["status"] == "nothing_left"
        ]
        self.assertEqual(stuck, [], f"an actor ran out of moves: {stuck}")


if __name__ == "__main__":
    unittest.main()


class EveryOfferedActionIsDistinguishable(unittest.TestCase):
    """A policy cannot choose between options it cannot tell apart.

    `describe_action` listed Castaway's participant vocabulary and rendered
    nothing else, so all five of a cook's opening moves read as the bare word
    "take": five distinct action ids, one description. Whatever a model did
    with that was going to look like indecision.
    """

    def test_distinct_actions_get_distinct_descriptions(self):
        from world_substrate.policy import describe_action

        for world_build, actor in (
            (build_engine, "ama"),
            (_castaway(), "robinson"),
        ):
            engine = world_build()
            page = engine.discover(actor)
            with self.subTest(actor=actor):
                self.assertTrue(page["available"])
                described = {describe_action(r["action"]) for r in page["available"]}
                ids = {r["action_id"] for r in page["available"]}
                self.assertEqual(
                    len(described),
                    len(ids),
                    f"{len(ids)} actions collapsed into {len(described)} descriptions",
                )

    def test_a_description_names_what_the_action_acts_on(self):
        from world_substrate.policy import describe_action

        engine = build_engine()
        takes = [
            r for r in engine.discover("ama")["available"]
            if r["action"]["kind"] == "take"
        ]
        self.assertTrue(takes)
        for row in takes:
            self.assertIn(row["action"]["item"], describe_action(row["action"]))


def _castaway():
    from reference_worlds.castaway.probe import build_transfer_engine

    return build_transfer_engine
