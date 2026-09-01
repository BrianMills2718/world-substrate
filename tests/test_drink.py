"""Focused contract evidence through the pinned post-drink checkpoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import (
    build_drink_engine,
    run_drink_probe,
)
from world_substrate.rules import (
    DrinkAction,
    FillAction,
    HeatAction,
    PourAction,
    UnheatAction,
)


def select_action(engine, kind: str, **matches: object):
    page = engine.discover("robinson", kind=kind)
    row = next(
        item
        for item in page["available"]
        if all(item["action"].get(key) == value for key, value in matches.items())
    )
    value = {**row["action"], "controller": "verification_script"}
    if kind == "drink":
        return DrinkAction.from_dict(value)
    if kind == "fill":
        return FillAction.from_dict(value)
    if kind == "heat":
        return HeatAction.from_dict(value)
    if kind == "pour":
        return PourAction.from_dict(value)
    if kind == "unheat":
        return UnheatAction.from_dict(value)
    raise ValueError(f"unsupported test action: {kind}")


def reach_pour_checkpoint(engine) -> None:
    engine.apply(
        select_action(
            engine,
            "fill",
            vessel="clay-pot",
            source="unsafe-pool",
            volume_ml=1000,
        )
    )
    engine.advance()
    engine.apply(
        select_action(
            engine,
            "heat",
            vessel="clay-pot",
            target="fire-camp",
        )
    )
    engine.advance(5)
    engine.apply(select_action(engine, "unheat", vessel="clay-pot"))
    engine.advance(5)
    engine.apply(
        select_action(
            engine,
            "pour",
            vessel="clay-pot",
            destination="cup-robinson",
            volume_ml=250,
        )
    )
    engine.advance()


class DrinkCheckpointTests(unittest.TestCase):
    def test_drink_and_empty_vessel_cooling_match_pinned_checkpoint(self) -> None:
        engine = build_drink_engine(REPO)
        reach_pour_checkpoint(engine)
        result = engine.apply(
            select_action(
                engine,
                "drink",
                vessel="cup-robinson",
                volume_ml=250,
            )
        )
        engine.advance()

        pot = engine.world.entities["clay-pot"]
        cup = engine.world.entities["cup-robinson"]
        robinson = engine.world.entities["robinson"]
        friday = engine.world.entities["friday"]
        assert pot.liquid and pot.thermal and cup.liquid and cup.thermal
        assert robinson.actor and friday.actor and engine.world.physical_ledger

        self.assertEqual(result["status"], "accepted")
        self.assertEqual(engine.world.tick, 13)
        self.assertEqual(robinson.actor.health, 100)
        self.assertEqual(robinson.actor.hydration, 62)
        self.assertEqual(friday.actor.hydration, 37)
        self.assertEqual(
            pot.liquid.as_dict(),
            {
                "volume_ml": 728,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 23_594,
            },
        )
        self.assertEqual(
            cup.liquid.as_dict(),
            {"volume_ml": 0, "salt_mg": 0, "pathogens": 0, "heat_units": 0},
        )
        self.assertEqual(pot.thermal.temperature_c, 32.41)
        self.assertEqual(cup.thermal.temperature_c, 32.41)
        self.assertEqual(engine.world.physical_ledger.heat_lost, 65_236)
        self.assertEqual(
            engine.world.physical_ledger.drunk.as_dict(),
            {
                "volume_ml": 250,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 8_970,
            },
        )
        self.assertTrue(engine.replay()["ok"])

    def test_drinking_hazards_are_possible_and_have_deterministic_harm(self) -> None:
        engine = build_drink_engine(REPO)
        cup = engine.world.entities["cup-robinson"]
        robinson = engine.world.entities["robinson"]
        assert cup.liquid and cup.thermal and robinson.actor
        cup.liquid.volume_ml = 250
        cup.liquid.salt_mg = 8_750
        cup.liquid.pathogens = 100
        cup.liquid.heat_units = 20_000
        cup.thermal.temperature_c = 80
        before_health = robinson.actor.health
        before_hydration = robinson.actor.hydration

        result = engine.apply(
            DrinkAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                volume_ml=250,
                base_revision=engine.world.revision,
                controller_id="verification_script",
            )
        )

        robinson = engine.world.entities["robinson"]
        assert robinson.actor
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(robinson.actor.health, before_health - 26)
        self.assertEqual(robinson.actor.hydration, before_hydration - 10)
        self.assertTrue(
            any(
                check["label"].startswith("Warning:")
                for check in result["event"]["checks"]
            )
        )

    def test_overdraw_is_atomic(self) -> None:
        engine = build_drink_engine(REPO)
        reach_pour_checkpoint(engine)
        before = engine.world.material_dict()
        result = engine.apply(
            DrinkAction(
                actor_id="robinson",
                vessel_id="cup-robinson",
                volume_ml=251,
                base_revision=engine.world.revision,
                controller_id="verification_script",
            )
        )
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(before, engine.world.material_dict())

    def test_drink_probe_matches_semantic_donor_projection(self) -> None:
        evidence = run_drink_probe(REPO)
        self.assertTrue(evidence["accepted"])
        self.assertTrue(evidence["checkpoint_comparison"]["matched"])
        self.assertTrue(evidence["ledger_comparison"]["matched"])
        self.assertTrue(evidence["replay"]["ok"])


if __name__ == "__main__":
    unittest.main()
