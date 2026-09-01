"""Focused contract evidence through the pinned ownership-transfer checkpoint."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import (
    build_transfer_engine,
    build_transfer_registry,
    run_transfer_probe,
)
from world_substrate.engine import Engine
from world_substrate.model import World
from world_substrate.rules import (
    DrinkAction,
    FillAction,
    GiveAction,
    HeatAction,
    PourAction,
    TakeAction,
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
    if kind == "give":
        return GiveAction.from_dict(value)
    if kind == "heat":
        return HeatAction.from_dict(value)
    if kind == "pour":
        return PourAction.from_dict(value)
    if kind == "take":
        return TakeAction.from_dict(value)
    if kind == "unheat":
        return UnheatAction.from_dict(value)
    raise ValueError(f"unsupported test action: {kind}")


def reach_drink_checkpoint(engine) -> None:
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
    engine.apply(
        select_action(
            engine,
            "drink",
            vessel="cup-robinson",
            volume_ml=250,
        )
    )
    engine.advance()


class TransferCheckpointTests(unittest.TestCase):
    def test_versioned_initial_snapshot_round_trips_through_json(self) -> None:
        engine = build_transfer_engine(REPO)

        snapshot = json.loads(json.dumps(engine.initial_snapshot()))
        restored = World.from_snapshot(snapshot)

        self.assertEqual(snapshot["schema_version"], "world-substrate-snapshot/v1")
        self.assertEqual(restored.material_dict(), engine.world.material_dict())
        self.assertEqual(restored.commands, [])
        self.assertEqual(restored.events, [])

    def test_loaded_snapshot_and_commands_replay_without_source_engine_state(
        self,
    ) -> None:
        engine = build_transfer_engine(REPO)
        initial_snapshot = json.loads(json.dumps(engine.initial_snapshot()))
        reach_drink_checkpoint(engine)
        commands = json.loads(json.dumps(engine.world.commands))

        replayed = Engine.replay_commands(
            initial_snapshot=initial_snapshot,
            commands=commands,
            registry=build_transfer_registry(),
        )

        self.assertEqual(replayed.world.material_hash(), engine.world.material_hash())
        self.assertEqual(replayed.world.events, engine.world.events)

    def test_committed_trace_replays_in_a_fresh_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "receipt.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(REPO / "scripts/replay_transfer_evidence.py"),
                    "--output",
                    str(output),
                ],
                cwd=REPO,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            receipt = json.loads(output.read_text())
            self.assertTrue(receipt["accepted"])
            self.assertTrue(receipt["observation"]["event_match"])
            self.assertEqual(
                receipt["observation"]["expected_material_hash"],
                receipt["observation"]["actual_material_hash"],
            )

    def test_take_and_give_preserve_vessel_identity_and_match_final_checkpoint(
        self,
    ) -> None:
        engine = build_transfer_engine(REPO)
        reach_drink_checkpoint(engine)
        source_identity = engine.world.entities["clay-pot"].source_entity_id

        take_result = engine.apply(select_action(engine, "take", vessel="clay-pot"))
        engine.advance()
        give_result = engine.apply(
            select_action(
                engine,
                "give",
                vessel="clay-pot",
                target="friday",
            )
        )
        engine.advance()

        pot = engine.world.entities["clay-pot"]
        cup = engine.world.entities["cup-robinson"]
        robinson = engine.world.entities["robinson"]
        friday = engine.world.entities["friday"]
        assert pot.liquid and pot.thermal and pot.ownership
        assert cup.liquid and cup.thermal and cup.ownership
        assert robinson.actor and friday.actor and engine.world.physical_ledger

        self.assertEqual(take_result["status"], "accepted")
        self.assertEqual(give_result["status"], "accepted")
        self.assertEqual(engine.world.tick, 15)
        self.assertEqual(pot.entity_id, "clay-pot")
        self.assertEqual(pot.source_entity_id, source_identity)
        self.assertEqual(pot.ownership.owner_ref, "actor:friday")
        self.assertEqual(cup.ownership.owner_ref, "actor:robinson")
        self.assertEqual(
            pot.liquid.as_dict(),
            {
                "volume_ml": 728,
                "salt_mg": 0,
                "pathogens": 0,
                "heat_units": 20_278,
            },
        )
        self.assertEqual(pot.thermal.temperature_c, 27.85)
        self.assertEqual(cup.thermal.temperature_c, 27.86)
        self.assertEqual(robinson.actor.hydration, 60)
        self.assertEqual(friday.actor.hydration, 35)
        self.assertEqual(engine.world.physical_ledger.heat_lost, 68_552)
        self.assertTrue(engine.replay()["ok"])

    def test_recipient_capacity_rejection_is_atomic(self) -> None:
        engine = build_transfer_engine(REPO)
        reach_drink_checkpoint(engine)
        engine.apply(select_action(engine, "take", vessel="clay-pot"))
        friday = engine.world.entities["friday"]
        assert friday.carrying
        friday.carrying.capacity_weight = 4
        before = engine.world.material_dict()
        result = engine.apply(
            GiveAction(
                actor_id="robinson",
                vessel_id="clay-pot",
                target_actor_id="friday",
                base_revision=engine.world.revision,
                controller_id="verification_script",
            )
        )
        self.assertEqual(result["status"], "precondition_failed")
        self.assertEqual(before, engine.world.material_dict())

    def test_transfer_probe_matches_semantic_donor_projection(self) -> None:
        evidence = run_transfer_probe(REPO)
        self.assertTrue(evidence["accepted"])
        self.assertTrue(evidence["checkpoint_comparison"]["matched"])
        self.assertTrue(evidence["ledger_comparison"]["matched"])
        self.assertTrue(evidence["identity"]["preserved"])
        self.assertTrue(evidence["replay"]["ok"])


if __name__ == "__main__":
    unittest.main()
