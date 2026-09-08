#!/usr/bin/env python3
"""Retain a deterministic, zero-spend Greenhouse run through the real engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from reference_worlds.greenhouse.mechanics import PutDownAction, WaterAction
from reference_worlds.greenhouse.probe import build_engine
from reference_worlds.greenhouse.terminal import garden_complete
from world_substrate.rules import FillAction, TakeAction, TypedAction

REPO = Path(__file__).resolve().parents[1]
ACTORS = ("nora", "leo")


def _progress(engine) -> dict[str, dict[str, object]]:
    result = {}
    for actor, plant_id in (("nora", "fern-1"), ("leo", "tomato-1")):
        plant = engine.world.entities[plant_id].component("plant")
        filled = plant.stage == "watered"
        result[actor] = {
            "plant": plant_id,
            "filled": filled,
            "plated": [],
            "still_wants": [] if filled else [plant_id],
        }
    return result


def retained_run() -> dict[str, object]:
    engine = build_engine(REPO)
    steps: list[tuple[str, Callable[[], TypedAction], str]] = [
        (
            "nora",
            lambda: TakeAction("nora", "can-1", engine.world.revision, "greenhouse-fixture"),
            "Take the shared watering can so the fern can be watered first.",
        ),
        (
            "nora",
            lambda: FillAction("nora", "can-1", "tap-1", 1, engine.world.revision, "greenhouse-fixture"),
            "Fill the watering can at the tap before using it on a plant.",
        ),
        (
            "nora",
            lambda: WaterAction("nora", "can-1", "fern-1", "bed-1", engine.world.revision, "greenhouse-fixture"),
            "Water the dry fern in the garden bed, consuming the can's water.",
        ),
        (
            "nora",
            lambda: PutDownAction("nora", "can-1", engine.world.revision, "greenhouse-fixture"),
            "Return the empty watering can to the shared store so Leo can use it.",
        ),
        (
            "leo",
            lambda: TakeAction("leo", "can-1", engine.world.revision, "greenhouse-fixture"),
            "Take the returned watering can to finish the remaining dry plant.",
        ),
        (
            "leo",
            lambda: FillAction("leo", "can-1", "tap-1", 1, engine.world.revision, "greenhouse-fixture"),
            "Refill the empty can at the tap before watering the tomato plant.",
        ),
        (
            "leo",
            lambda: WaterAction("leo", "can-1", "tomato-1", "bed-1", engine.world.revision, "greenhouse-fixture"),
            "Water the tomato plant so every represented plant is watered.",
        ),
    ]

    transcript = []
    for turn, (actor, make_action, reasoning) in enumerate(steps, 1):
        revision = engine.world.revision
        action = make_action()
        result = engine.apply(action)
        if result["status"] != "accepted":
            raise RuntimeError(f"fixture action failed at turn {turn}: {result}")
        action_record = action.as_dict()
        rows = {}
        for seat in ACTORS:
            if seat == actor:
                rows[seat] = {
                    "wanted": action_record,
                    "did": action_record,
                    "status": "accepted",
                    "retried": False,
                    "lost_what_it_wanted": False,
                    "refused_because": [],
                    "said": reasoning,
                }
            else:
                rows[seat] = {
                    "wanted": None,
                    "did": None,
                    "status": "no_action",
                    "retried": False,
                    "lost_what_it_wanted": False,
                    "refused_because": [],
                    "said": "Wait while the other gardener uses the shared watering can.",
                }
        transcript.append(
            {
                "turn": turn,
                "revision_when_decided": revision,
                "committed_first": actor,
                "actors": rows,
                "progress": _progress(engine),
            }
        )

    if not garden_complete(engine.world):
        raise RuntimeError("greenhouse fixture did not reach its terminal state")
    if not engine.replay()["ok"]:
        raise RuntimeError("greenhouse fixture did not replay exactly")
    return {
        "schema_version": "world-substrate-contested-run/v3",
        "world": "greenhouse",
        "actors": list(ACTORS),
        "model": "scripted-greenhouse-fixture",
        "cost_usd": 0.0,
        "claim": "Deterministic two-gardener Greenhouse trace. Every action is an accepted commit through the shared engine; the run demonstrates represented shared-tool handoff, not concurrent-policy behavior.",
        "summary": {
            "turns": len(transcript),
            "terminal_reached": True,
            "plants_watered": 2,
            "model_spend_usd": 0.0,
        },
        "transcript": transcript,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO / "evidence/greenhouse/first-service-v0.json")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(retained_run(), indent=2) + "\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
