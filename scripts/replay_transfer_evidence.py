#!/usr/bin/env python3
"""Replay the committed transfer trace in a fresh process and retain a receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import (
    TRANSFER_REGISTRY_ID,
    build_transfer_registry,
)
from world_substrate.engine import Engine

TRACE = REPO / "evidence/m1/transfer-v0.json"
OUTPUT = REPO / "evidence/m1/transfer-replay-v1.json"


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return value


def _current_revision() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _trace_at_revision(trace_path: Path, source_revision: str) -> bytes:
    relative = trace_path.resolve().relative_to(REPO)
    completed = subprocess.run(
        ["git", "show", f"{source_revision}:{relative}"],
        cwd=REPO,
        check=True,
        capture_output=True,
    )
    return completed.stdout


def replay_trace(
    trace_path: Path, *, source_revision: str | None = None
) -> dict[str, object]:
    trace_bytes = trace_path.read_bytes()
    trace = _object(json.loads(trace_bytes), "transfer trace")
    execution = _object(trace.get("execution"), "transfer execution")
    identity = _object(execution.get("registry_identity"), "registry identity")
    registry = build_transfer_registry()
    expected_identity = {
        "registry_id": TRANSFER_REGISTRY_ID,
        "engine_id": "world-substrate-core@1",
        "content_id": "castaway-water-workshop-m1@da5ccb46fa536505bbc0235a4157c648c8bb4bcb",
        "rule_versions": registry.versions(),
    }
    if identity != expected_identity:
        raise ValueError("committed registry/content identity is not supported")

    snapshot = _object(execution.get("initial_snapshot"), "initial snapshot")
    snapshot_world = _object(snapshot.get("world"), "initial snapshot world")
    for field in ("engine_id", "content_id", "rule_versions"):
        if snapshot_world.get(field) != identity[field]:
            raise ValueError(f"initial snapshot {field} does not match registry identity")

    replayed = Engine.replay_commands(
        initial_snapshot=snapshot,
        commands=execution.get("commands"),
        registry=registry,
    )
    expected_hash = execution.get("final_material_hash")
    expected_events = execution.get("events")
    actual_hash = replayed.world.material_hash()
    event_match = replayed.world.events == expected_events
    accepted = bool(actual_hash == expected_hash and event_match)
    return {
        "schema_version": "world-substrate-replay-receipt/v1",
        "record_type": "fresh_process_replay_receipt",
        "source_revision": source_revision or _current_revision(),
        "source_trace": str(trace_path.resolve().relative_to(REPO)),
        "source_trace_sha256": hashlib.sha256(trace_bytes).hexdigest(),
        "inputs": {
            "snapshot_schema_version": snapshot.get("schema_version"),
            "registry_identity": identity,
            "command_count": len(execution.get("commands", [])),
        },
        "observation": {
            "expected_material_hash": expected_hash,
            "actual_material_hash": actual_hash,
            "expected_event_count": len(expected_events)
            if isinstance(expected_events, list)
            else None,
            "actual_event_count": len(replayed.world.events),
            "event_match": event_match,
        },
        "accepted": accepted,
    }


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--trace", type=Path, default=TRACE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--source-revision")
    args = parser.parse_args()
    output = args.output.resolve()
    source_revision = args.source_revision
    if args.check and source_revision is None and output.exists():
        try:
            retained = _object(json.loads(output.read_bytes()), "replay receipt")
            retained_revision = retained.get("source_revision")
            if not isinstance(retained_revision, str) or not retained_revision:
                raise ValueError("replay receipt lacks source_revision")
            source_revision = retained_revision
        except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
            print(f"invalid retained replay receipt: {error}", file=sys.stderr)
            return 1
    try:
        trace_path = args.trace.resolve()
        payload = replay_trace(trace_path, source_revision=source_revision)
        if (
            args.check
            and source_revision is not None
            and _trace_at_revision(trace_path, source_revision)
            != trace_path.read_bytes()
        ):
            raise ValueError("source_revision does not contain the retained trace")
    except (
        OSError,
        subprocess.CalledProcessError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as error:
        print(f"fresh-process replay failed: {error}", file=sys.stderr)
        return 1
    if not payload["accepted"]:
        print("fresh-process replay did not match retained outputs", file=sys.stderr)
        return 1

    expected = encoded(payload)
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print(f"fresh-process replay receipt drift: {output}", file=sys.stderr)
            return 1
        print(f"fresh-process replay receipt passes: {display_path(output)}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    print(f"wrote {display_path(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
