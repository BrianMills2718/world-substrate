"""Focused contract evidence through the pinned cooled-and-poured checkpoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_pour_engine, run_pour_probe
from world_substrate.rules import FillAction, HeatAction, PourAction, UnheatAction


def select_action(engine, kind: str, **matches: object):
    page = engine.discover("robinson", kind=kind)
    row = next(
        item
        for item in page["available"]
        if all(item["action"].get(key) == value for key, value in matches.items())
    )
    value = {**row["action"], "controller": "verification_script"}
    if kind == "fill":
        return FillAction.from_dict(value)
    if kind == "heat":
        return HeatAction.from_dict(value)
    if kind == "unheat":
        return UnheatAction.from_dict(value)
    if kind == "pour":
        return PourAction.from_dict(value)
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


class PourCheckpointTests(unittest.TestCase):
    def test_cooling_and_pour_match_pinned_checkpoint(self) -> None:
        engine = build_pour_engine(REPO)
        reach_pour_checkpoint(engine)
        pot = engine.world.entities["clay-pot"]
        cup = engine.world.entities["cup-robinson"]
        assert pot.liquid and pot.thermal and cup.liquid and cup.thermal
        assert engine.world.physical_ledger
        self.assertEqual(engine.world.tick, 12)
        self.assertEqual(
            pot.liquid.as_dict(),
            {
                "volume_ml": 728,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 26_121,
            },
        )
        self.assertEqual(
            cup.liquid.as_dict(),
            {
                "volume_ml": 250,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 8_970,
            },
        )
        self.assertEqual(pot.thermal.temperature_c, 35.88)
        self.assertEqual(cup.thermal.temperature_c, 35.88)
        self.assertEqual(engine.world.physical_ledger.heat_lost, 62_709)
        robinson = engine.world.entities["robinson"].actor
        friday = engine.world.entities["friday"].actor
        assert robinson and friday
        self.assertEqual(robinson.hydration, 38)
        self.assertEqual(friday.hydration, 38)
        self.assertTrue(engine.replay()["ok"])

    def test_over_capacity_pour_is_atomic(self) -> None:
        engine = build_pour_engine(REPO)
        engine.apply(
            select_action(
                engine,
                "fill",
                vessel="clay-pot",
                source="unsafe-pool",
                volume_ml=1000,
            )
        )
        before = engine.world.material_dict()
        result = engine.apply(
            PourAction(
                actor_id="robinson",
                vessel_id="clay-pot",
                destination_id="cup-robinson",
                volume_ml=600,
                base_revision=engine.world.revision,
                controller_id="verification_script",
            )
        )
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(before, engine.world.material_dict())

    def test_pour_probe_matches_semantic_donor_projection(self) -> None:
        evidence = run_pour_probe(REPO)
        self.assertTrue(evidence["accepted"])
        self.assertTrue(evidence["checkpoint_comparison"]["matched"])
        self.assertTrue(evidence["ledger_comparison"]["matched"])
        self.assertTrue(evidence["replay"]["ok"])


if __name__ == "__main__":
    unittest.main()
