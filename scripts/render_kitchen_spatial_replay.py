#!/usr/bin/env python3
"""Compatibility wrapper for the kitchen's declarative scene profile."""
from __future__ import annotations

import argparse
from pathlib import Path

from render_scene_replay import (
    build_frames as _build_frames,
    load_scene_profile,
    render_file,
    render_html as _render_html,
)

REPO = Path(__file__).resolve().parents[1]
PROFILE_PATH = REPO / "reference_worlds/kitchen/scene-profile-v0.json"
PROFILE, WORLD_ENTITIES = load_scene_profile(PROFILE_PATH)


def build_frames(trace):
    """Kitchen compatibility view over generic scene frames."""
    frames = _build_frames(trace, PROFILE, WORLD_ENTITIES)
    for frame in frames:
        frame["knife_owner"] = frame["holders"].get("knife")
        for state in frame["items"].values():
            state["prep"] = state.get("state")
            state["plated_to"] = state.get("placed_at") if state.get("state") == "plated" else None
    return frames


def render_html(trace):
    return _render_html(trace, PROFILE, WORLD_ENTITIES, PROFILE_PATH.parent)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render_file(args.input, PROFILE_PATH, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
