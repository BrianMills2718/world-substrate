#!/usr/bin/env python3
"""Extract the stable Castaway freshwater behavior fixture from the pinned donor."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references/sources.json"
OUTPUT = REPO / "tests/fixtures/castaway/freshwater-v0.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_payload() -> dict[str, object]:
    manifest = json.loads(MANIFEST.read_text())
    donor_record = manifest["sources"]["castaway_world_systems"]
    donor = (REPO / donor_record["local_path"]).resolve()
    observed_revision = subprocess.run(
        ["git", "-C", str(donor), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if observed_revision != donor_record["revision"]:
        raise RuntimeError(
            f"donor revision drift: expected {donor_record['revision']}, observed {observed_revision}"
        )

    receipt_path = (REPO / donor_record["freshwater_receipt_path"]).resolve()
    run_path = (REPO / donor_record["freshwater_run_path"]).resolve()
    if sha256(receipt_path) != donor_record["freshwater_receipt_sha256"]:
        raise RuntimeError("freshwater receipt hash drift")

    receipt = json.loads(receipt_path.read_text())
    with gzip.open(run_path, "rt") as stream:
        run = json.load(stream)

    commands: list[dict[str, object]] = []
    keep = ("actor", "kind", "vessel", "source", "destination", "target", "volume_ml")
    for command in run["engine"]["commands"]:
        if command["op"] == "tick":
            commands.append({"op": "tick"})
            continue
        action = {
            key: command["action"][key]
            for key in keep
            if command["action"].get(key) not in (None, "")
        }
        commands.append({"op": "action", "action": action})

    checkpoints: list[dict[str, object]] = []
    for checkpoint in receipt["checkpoints"]:
        checkpoints.append(
            {
                "label": checkpoint["label"],
                "tick": checkpoint["tick"],
                "state_hash": checkpoint["state_hash"],
                "vessels": {
                    key: checkpoint["vessels"][key]
                    for key in ("clay-pot", "cup-robinson")
                },
                "actors": checkpoint["actors"],
                "totals": checkpoint["totals"],
            }
        )

    return {
        "schema_version": "world-substrate-reference-fixture/v0",
        "fixture_id": "castaway-freshwater-v0",
        "claim": "Expected deterministic behavior for the first neutral extraction; no LLM-policy claim.",
        "source": {
            "repository": donor_record["repository"],
            "branch": donor_record["branch"],
            "revision": donor_record["revision"],
            "receipt_path": donor_record["freshwater_receipt_path"],
            "receipt_sha256": donor_record["freshwater_receipt_sha256"],
            "content_hash": receipt["content_hash"],
            "implementation_hash": receipt["implementation_hash"],
        },
        "controller": receipt["controller"],
        "llm_calls": receipt["llm_calls"],
        "commands": commands,
        "expected": {
            "tick": receipt["tick"],
            "command_count": receipt["commands"],
            "event_count": receipt["events"],
            "replay": receipt["replay"],
            "restart_equal": receipt["restart_equal"],
            "checkpoints": checkpoints,
            "final_totals": receipt["final_totals"],
        },
    }


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = encoded(stable_payload())

    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != expected:
            print(f"fixture drift: {OUTPUT}", file=sys.stderr)
            return 1
        print(f"fixture matches pinned donor: {OUTPUT.relative_to(REPO)}")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(expected)
    print(f"wrote {OUTPUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
