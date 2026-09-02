#!/usr/bin/env python3
"""Generate or verify the M2 give/exchange evidence receipt.

Smallest versioned binding-and-trace slice for the M2 active roadmap milestone:
runs two independent give actions between two actors, classifies them through
the derived exchange view, and records that the classification changed no
committed state. See roadmap/README.md "Active slice: M2" and
docs/decisions/003-semantic-mechanical-boundary.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.engine import Engine
from world_substrate.exchange import find_exchanges
from world_substrate.model import World
from world_substrate.rules import GiveAction
from world_substrate.semantic import GIVE_BINDING

OUTPUT = REPO / "evidence/m2/give-exchange-v0.json"


def _select_give(engine: Engine, actor_id: str, vessel: str, target: str) -> GiveAction:
    page = engine.discover(actor_id, kind="give")
    row = next(
        item
        for item in page["available"]
        if item["action"]["vessel"] == vessel and item["action"]["target"] == target
    )
    value = {**row["action"], "controller": "give_exchange_probe"}
    return GiveAction.from_dict(value)


def run_give_exchange_probe() -> dict[str, object]:
    engine = build_transfer_engine(REPO)
    world = World.from_snapshot(engine.initial_snapshot())
    world.entities["clay-pot"].ownership.owner_ref = "actor:friday"
    world.rule_versions = engine.registry.versions()
    engine = Engine(world, engine.registry)

    ownership_before_classification = {
        "cup-robinson": None,
        "clay-pot": None,
    }

    result_a = engine.apply(_select_give(engine, "robinson", "cup-robinson", "friday"))
    result_b = engine.apply(_select_give(engine, "friday", "clay-pot", "robinson"))
    accepted = (
        result_a["event"]["status"] == "accepted"
        and result_b["event"]["status"] == "accepted"
    )

    ownership_before_classification["cup-robinson"] = engine.world.entities[
        "cup-robinson"
    ].ownership.owner_ref
    ownership_before_classification["clay-pot"] = engine.world.entities[
        "clay-pot"
    ].ownership.owner_ref
    event_count_before = len(engine.world.events)
    command_count_before = len(engine.world.commands)

    exchanges = find_exchanges(engine.world.events, engine.world.commands)

    no_transfer_from_classification = (
        len(engine.world.events) == event_count_before
        and len(engine.world.commands) == command_count_before
        and engine.world.entities["cup-robinson"].ownership.owner_ref
        == ownership_before_classification["cup-robinson"]
        and engine.world.entities["clay-pot"].ownership.owner_ref
        == ownership_before_classification["clay-pot"]
    )

    return {
        "accepted": accepted and no_transfer_from_classification,
        "binding": GIVE_BINDING.as_dict(),
        "give_events": [
            {
                "event_id": result_a["event"]["event_id"],
                "status": result_a["event"]["status"],
            },
            {
                "event_id": result_b["event"]["event_id"],
                "status": result_b["event"]["status"],
            },
        ],
        "derived_exchanges": [exchange.as_dict() for exchange in exchanges],
        "final_ownership": {
            "cup-robinson": engine.world.entities["cup-robinson"].ownership.owner_ref,
            "clay-pot": engine.world.entities["clay-pot"].ownership.owner_ref,
        },
        "classification_performed_no_transfer": no_transfer_from_classification,
        "event_count_after_two_gives": event_count_before,
        "event_count_after_classification": len(engine.world.events),
    }


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = run_give_exchange_probe()
    if payload.get("accepted") is not True:
        print("give/exchange probe rejected the evidence", file=sys.stderr)
        return 1
    expected = encoded(payload)
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print(f"give/exchange evidence drift: {output}", file=sys.stderr)
            return 1
        print(f"give/exchange evidence matches executable probe: {output.relative_to(REPO)}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    print(f"wrote {output.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
