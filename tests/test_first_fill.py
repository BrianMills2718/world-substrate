"""Focused evidence for the first neutral consumer path."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import (
    build_first_fill_engine,
    run_first_fill_probe,
)
from world_substrate.rules import FillAction


def select_fill(engine, volume_ml: int = 1000) -> FillAction:
    page = engine.discover("robinson", kind="fill")
    row = next(
        item
        for item in page["available"]
        if item["action"]["vessel"] == "clay-pot"
        and item["action"]["source"] == "unsafe-pool"
        and item["action"]["volume_ml"] == volume_ml
    )
    return FillAction.from_dict({**row["action"], "controller": "verification_script"})


class FirstFillTests(unittest.TestCase):
    def test_observation_is_a_lossy_actor_projection(self) -> None:
        engine = build_first_fill_engine(REPO)
        observation = engine.observe("robinson")
        self.assertEqual(observation["entities"]["robinson"]["actor"]["hydration"], 50)
        self.assertNotIn("hydration", observation["entities"]["friday"]["actor"])
        self.assertIn("hydration", engine.world.entities["friday"].as_dict()["actor"])

    def test_discovery_separates_available_and_blocked_candidates(self) -> None:
        engine = build_first_fill_engine(REPO)
        condition = engine.world.entities["clay-pot"].condition
        assert condition is not None
        condition.value = 0
        page = engine.discover("robinson", kind="fill")
        self.assertFalse(
            any(row["action"]["vessel"] == "clay-pot" for row in page["available"])
        )
        self.assertTrue(
            any(row["action"]["vessel"] == "clay-pot" for row in page["blocked"])
        )

    def test_discovery_executes_registered_fill_and_conserves_liquid(self) -> None:
        engine = build_first_fill_engine(REPO)
        before = {
            key: sum(
                getattr(entity.liquid, key)
                for entity in engine.world.entities.values()
                if entity.liquid is not None
            )
            for key in ("volume_ml", "salt_mg", "pathogens", "heat_units")
        }
        result = engine.apply(select_fill(engine))
        self.assertEqual(result["status"], "accepted")
        source = engine.world.entities["unsafe-pool"].liquid
        vessel = engine.world.entities["clay-pot"].liquid
        self.assertIsNotNone(source)
        self.assertIsNotNone(vessel)
        assert source is not None and vessel is not None
        self.assertEqual(
            source.as_dict(),
            {
                "volume_ml": 5000,
                "salt_mg": 0,
                "pathogens": 2000,
                "heat_units": 110000,
            },
        )
        self.assertEqual(
            vessel.as_dict(),
            {
                "volume_ml": 1000,
                "salt_mg": 0,
                "pathogens": 400,
                "heat_units": 22000,
            },
        )
        after = {
            key: sum(
                getattr(entity.liquid, key)
                for entity in engine.world.entities.values()
                if entity.liquid is not None
            )
            for key in before
        }
        self.assertEqual(before, after)
        self.assertEqual(result["event"]["rule_id"], "mechanism.liquid.fill")
        self.assertTrue(result["event"]["changes"])

    def test_overfill_rejection_preserves_material_state(self) -> None:
        engine = build_first_fill_engine(REPO)
        before = engine.world.material_dict()
        action = FillAction(
            actor_id="robinson",
            vessel_id="clay-pot",
            source_id="unsafe-pool",
            volume_ml=10_000,
            base_revision=engine.world.revision,
            controller_id="verification_script",
        )
        result = engine.apply(action)
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(before, engine.world.material_dict())
        self.assertEqual(result["event"]["changes"], [])
        self.assertEqual(result["event"]["hash_before"], result["event"]["hash_after"])

    def test_stale_revision_is_rejected_without_material_change(self) -> None:
        engine = build_first_fill_engine(REPO)
        current = select_fill(engine, volume_ml=250)
        engine.apply(current)
        before = engine.world.material_dict()
        stale = FillAction(
            actor_id=current.actor_id,
            vessel_id=current.vessel_id,
            source_id=current.source_id,
            volume_ml=current.volume_ml,
            base_revision=0,
            controller_id=current.controller_id,
        )
        result = engine.apply(stale)
        self.assertEqual(result["status"], "stale_revision")
        self.assertEqual(before, engine.world.material_dict())

    def test_fill_tick_and_replay_match_exactly(self) -> None:
        engine = build_first_fill_engine(REPO)
        engine.apply(select_fill(engine))
        engine.advance()
        receipt = engine.replay()
        self.assertTrue(receipt["ok"])
        self.assertTrue(receipt["event_match"])
        self.assertEqual(receipt["steps"], 2)

    def test_probe_matches_selected_pinned_donor_checkpoint(self) -> None:
        evidence = run_first_fill_probe(REPO)
        self.assertTrue(evidence["accepted"])
        self.assertTrue(evidence["conservation"]["matched"])
        self.assertTrue(evidence["checkpoint_comparison"]["matched"])
        self.assertTrue(evidence["replay"]["ok"])


if __name__ == "__main__":
    unittest.main()
