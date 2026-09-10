#!/usr/bin/env python3
"""Verify and build the retained Waltzman Living Scene branch player."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_living_scene_branches import render_branching_html
from world_substrate.living_scene import (
    build_living_scene_frames,
    load_live_projection_bundle,
    load_scene_contract,
    normalized_frame_json,
    rebuild_living_scene_frame,
)

PROFILE = REPO / "reference_worlds/waltzman/living-scene-v1.json"
BASELINE = REPO / "evidence/waltzman/demo-baseline-v0.json"
INTERVENTION = REPO / "evidence/waltzman/demo-intervention-v0.json"
OUTPUT = REPO / "evidence/renders/waltzman-living-v1.html"
MANIFEST = REPO / "evidence/waltzman/living-replay-manifest-v1.json"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame_record(branch: str, player_index: int, frame: dict[str, Any]) -> dict[str, Any]:
    event = frame.get("event") or {}
    return {
        "branch": branch,
        "player_frame_index": player_index,
        "boundary_index": frame["boundary_index"],
        "event_id": event.get("event_id"),
        "tick": frame.get("tick"),
        "revision": frame.get("revision"),
        "frame_sha256": hashlib.sha256(normalized_frame_json(frame).encode()).hexdigest(),
    }


def verify() -> tuple[dict[str, dict[str, Any]], dict[str, Any], dict[str, Any]]:
    profile = load_scene_contract(PROFILE)
    bundles = {
        "baseline": load_live_projection_bundle(BASELINE),
        "intervention": load_live_projection_bundle(INTERVENTION),
    }
    frames = {name: build_living_scene_frames(bundle, profile) for name, bundle in bundles.items()}
    shared_count = bundles["intervention"].get("fork", {}).get("shared_event_count")
    if shared_count != len(bundles["baseline"]["events"]):
        raise AssertionError("intervention shared_event_count must equal retained baseline event count")
    if bundles["intervention"]["events"][:shared_count] != bundles["baseline"]["events"]:
        raise AssertionError("intervention branch does not preserve exact retained baseline prefix")
    for name, bundle in bundles.items():
        for event_index in range(-1, len(bundle["events"])):
            direct = rebuild_living_scene_frame(bundle, profile, event_index)
            if direct != frames[name][event_index + 1]:
                raise AssertionError(f"direct rebuild diverges for {name} boundary {event_index}")
    baseline_gate = frames["baseline"][-1]["views"]["institutions"]["coalition-hub"]["bindings"]
    intervention_gate = frames["intervention"][-1]["views"]["institutions"]["coalition-hub"]["bindings"]
    if baseline_gate.get("status") != "blocked" or intervention_gate.get("status") != "ready":
        raise AssertionError("retained branch outcomes are not blocked -> ready")
    meeting_frames = [
        frame for frame in frames["baseline"]
        if frame["views"]["activities"]["coordination-meeting"]["bindings"].get("status") == "active"
    ]
    if {frame.get("tick") for frame in meeting_frames} != {4, 5, 6}:
        raise AssertionError("meeting active presentation must follow canonical ticks 4, 5, 6")
    checkpoints = {
        "initial": frame_record("baseline", 0, frames["baseline"][0]),
        "meeting_active": frame_record("baseline", 17, frames["baseline"][17]),
        "blocked": frame_record("baseline", len(frames["baseline"]) - 1, frames["baseline"][-1]),
        "intervention_applied": frame_record("intervention", 22, frames["intervention"][22]),
        "ready": frame_record("intervention", len(frames["intervention"]) - 1, frames["intervention"][-1]),
    }
    manifest = {
        "schema_version": "world-substrate-living-replay-manifest/v1",
        "world_id": profile["world"],
        "profile": str(PROFILE.relative_to(REPO)),
        "inputs": {
            "baseline": {"path": str(BASELINE.relative_to(REPO)), "sha256": file_hash(BASELINE)},
            "intervention": {"path": str(INTERVENTION.relative_to(REPO)), "sha256": file_hash(INTERVENTION)},
            "profile": {"path": str(PROFILE.relative_to(REPO)), "sha256": file_hash(PROFILE)},
        },
        "branches": {
            name: {
                "event_count": len(bundle["events"]),
                "frame_count": len(frames[name]),
                "final_event_id": bundle["events"][-1]["event_id"],
            }
            for name, bundle in bundles.items()
        },
        "shared_history_event_count": shared_count,
        "checkpoints": checkpoints,
        "provider_spend_usd": 0,
    }
    return bundles, profile, manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    bundles, profile, manifest = verify()
    if not args.check:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(render_branching_html(bundles, profile, PROFILE.parent))
        MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
