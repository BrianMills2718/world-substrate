"""Focused contract evidence through the pinned boiling checkpoint."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import (
    build_freshwater_engine,
    run_boiling_probe,
)
from world_substrate.rules import FillAction, HeatAction, UnheatAction


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
    raise ValueError(f"unsupported test action: {kind}")


def reach_boiling_checkpoint(engine) -> None:
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


class BoilingCheckpointTests(unittest.TestCase):
    def test_registered_heat_processes_match_pinned_boiling_checkpoint(self) -> None:
        engine = build_freshwater_engine(REPO)
        reach_boiling_checkpoint(engine)

        pot = engine.world.entities["clay-pot"]
        fire = engine.world.entities["fire-camp"]
        assert pot.container and pot.liquid and pot.thermal
        assert fire.heat_source and engine.world.physical_ledger
        self.assertEqual(engine.world.tick, 6)
        self.assertEqual(
            pot.liquid.as_dict(),
            {
                "volume_ml": 978,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 97_800,
            },
        )
        self.assertEqual(pot.thermal.temperature_c, 100.0)
        self.assertEqual(pot.container.boiling_ticks, 2)
        self.assertEqual(pot.container.heat_source_id, "fire-camp")
        self.assertEqual(fire.heat_source.fuel, 18)
        self.assertEqual(
            engine.world.physical_ledger.semantic_deltas(),
            {
                "evaporated": {
                    "volume_ml": 22,
                    "salt_mg": 0,
                    "pathogens": 0,
                    "heat_units": 2200,
                },
                "pathogens_killed": 400,
                "heat_added": 78_000,
                "heat_lost": 0,
                "latent_heat_used": 22_000,
                "drunk": {
                    "volume_ml": 0,
                    "salt_mg": 0,
                    "pathogens": 0,
                    "heat_units": 0,
                },
            },
        )
        robinson = engine.world.entities["robinson"].actor
        friday = engine.world.entities["friday"].actor
        assert robinson is not None and friday is not None
        self.assertEqual(robinson.hydration, 44)
        self.assertEqual(friday.hydration, 44)
        self.assertTrue(engine.replay()["ok"])

    def test_heat_requires_a_local_intact_fueled_source_and_is_atomic(self) -> None:
        engine = build_freshwater_engine(REPO)
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
        fire = engine.world.entities["fire-camp"].heat_source
        assert fire is not None
        fire.fuel = 0
        page = engine.discover("robinson", kind="heat")
        self.assertFalse(page["available"])
        row = next(item for item in page["blocked"] if item["action"]["vessel"] == "clay-pot")
        before = engine.world.material_dict()
        result = engine.apply(
            HeatAction.from_dict(
                {**row["action"], "controller": "verification_script"}
            )
        )
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(before, engine.world.material_dict())

    def test_unheat_is_registered_and_detaches_the_same_vessel(self) -> None:
        engine = build_freshwater_engine(REPO)
        reach_boiling_checkpoint(engine)
        action = select_action(engine, "unheat", vessel="clay-pot")
        result = engine.apply(action)
        self.assertEqual(result["status"], "accepted")
        container = engine.world.entities["clay-pot"].container
        assert container is not None
        self.assertIsNone(container.heat_source_id)
        self.assertTrue(engine.replay()["ok"])

    def test_boiling_probe_matches_semantic_donor_projection(self) -> None:
        evidence = run_boiling_probe(REPO)
        self.assertTrue(evidence["accepted"])
        self.assertTrue(evidence["checkpoint_comparison"]["matched"])
        self.assertTrue(evidence["replay"]["ok"])


if __name__ == "__main__":
    unittest.main()
