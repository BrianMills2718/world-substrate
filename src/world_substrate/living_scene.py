"""Deterministic, read-only logical frames for living-world presentation.

Living Scene profiles describe how retained canonical facts may be presented.
They never own canonical state, event history, information delivery, or causal
ancestry.  This module intentionally has no DOM/browser dependency.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from world_substrate.projection import LIVE_PROJECTION_SCHEMA_VERSION, apply_changes

LIVING_SCENE_SCHEMA_VERSION = "world-substrate-living-scene/v1"
LEGACY_SCENE_PROFILE_SCHEMA_VERSION = "world-substrate-scene-profile/v0"

_ALLOWED_TOP_LEVEL = {
    "schema_version", "scene_id", "world", "title", "subtitle", "note",
    "assets", "scene", "zones", "actors", "entities", "activities",
    "institutions", "event_visuals", "state_styles", "presentation",
}
_REQUIRED_OBJECTS = (
    "assets", "zones", "actors", "entities", "activities", "institutions",
    "event_visuals", "state_styles",
)
_LEGACY_REQUIRED_OBJECTS = ("assets", "actors", "stations", "entities", "action_visuals")
_BINDABLE_GROUPS = ("actors", "entities", "activities", "institutions")
_PATH_RE = re.compile(r"^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$")
_FORBIDDEN_OPERATION_KEYS = {
    "changes", "after", "before", "causal_parent_event_ids",
    "information_context", "canonical_state", "world_state",
}


def _point(value: object, label: str) -> list[float]:
    if (
        not isinstance(value, list)
        or len(value) != 2
        or any(type(item) not in (int, float) for item in value)
    ):
        raise ValueError(f"{label} must be [x, y]")
    return [float(value[0]), float(value[1])]


def _rect(value: object, label: str) -> list[float]:
    if (
        not isinstance(value, list)
        or len(value) != 4
        or any(type(item) not in (int, float) for item in value)
    ):
        raise ValueError(f"{label} must be [x, y, width, height]")
    return [float(item) for item in value]


def _path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or not _PATH_RE.fullmatch(value):
        raise ValueError(f"{label} must be a dotted read path")
    return value


def _lookup(value: object, path: str) -> object:
    current = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _validate_bindings(value: object, label: str) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    checked: dict[str, str] = {}
    for name, path in value.items():
        if not isinstance(name, str) or not name:
            raise ValueError(f"{label} keys must be nonempty strings")
        checked[name] = _path(path, f"{label}.{name}")
    return checked


def _validate_v1_profile(raw: dict[str, Any]) -> dict[str, Any]:
    unknown = sorted(set(raw) - _ALLOWED_TOP_LEVEL)
    if unknown:
        raise ValueError(f"living scene profile has unknown fields: {', '.join(unknown)}")
    if not isinstance(raw.get("scene_id"), str) or not raw["scene_id"]:
        raise ValueError("living scene profile must name scene_id")
    if not isinstance(raw.get("world"), str) or not raw["world"]:
        raise ValueError("living scene profile must name world")
    for key in _REQUIRED_OBJECTS:
        if not isinstance(raw.get(key), dict):
            raise ValueError(f"living scene profile {key!r} must be an object")

    profile = deepcopy(raw)
    scene = profile.get("scene")
    if scene is not None and not isinstance(scene, dict):
        raise ValueError("living scene profile 'scene' must be an object")
    presentation = profile.get("presentation")
    if presentation is not None and not isinstance(presentation, dict):
        raise ValueError("living scene profile 'presentation' must be an object")

    for zone_id, zone in profile["zones"].items():
        if not isinstance(zone_id, str) or not zone_id or not isinstance(zone, dict):
            raise ValueError("living scene zones must map nonempty ids to objects")
        zone["rect"] = _rect(zone.get("rect"), f"zone {zone_id}.rect")
        if "anchor" in zone:
            zone["anchor"] = _point(zone["anchor"], f"zone {zone_id}.anchor")

    for group in _BINDABLE_GROUPS:
        for visual_id, visual in profile[group].items():
            if not isinstance(visual_id, str) or not visual_id or not isinstance(visual, dict):
                raise ValueError(f"living scene {group} must map nonempty ids to objects")
            if "home" in visual:
                visual["home"] = _point(visual["home"], f"{group}.{visual_id}.home")
            if "anchor" in visual:
                visual["anchor"] = _point(visual["anchor"], f"{group}.{visual_id}.anchor")
            entity_id = visual.get("entity", visual_id)
            if not isinstance(entity_id, str) or not entity_id:
                raise ValueError(f"{group}.{visual_id}.entity must be a nonempty string")
            visual["entity"] = entity_id
            visual["bindings"] = _validate_bindings(
                visual.get("bindings"), f"{group}.{visual_id}.bindings"
            )

    for exact_rule_id, visual in profile["event_visuals"].items():
        if not isinstance(exact_rule_id, str) or not exact_rule_id:
            raise ValueError("event_visuals keys must be exact nonempty rule ids")
        if not isinstance(visual, dict):
            raise ValueError(f"event_visuals.{exact_rule_id} must be an object")
        operations = visual.get("operations", [])
        if not isinstance(operations, list):
            raise ValueError(f"event_visuals.{exact_rule_id}.operations must be a list")
        for index, operation in enumerate(operations):
            if not isinstance(operation, dict):
                raise ValueError(
                    f"event_visuals.{exact_rule_id}.operations[{index}] must be an object"
                )
            forbidden = sorted(set(operation) & _FORBIDDEN_OPERATION_KEYS)
            if forbidden:
                raise ValueError(
                    "living scene operations cannot carry canonical authority fields: "
                    + ", ".join(forbidden)
                )
            op = operation.get("op")
            if not isinstance(op, str) or not op:
                raise ValueError(
                    f"event_visuals.{exact_rule_id}.operations[{index}].op must be nonempty"
                )
            reads = operation.get("read_paths", {})
            operation["read_paths"] = _validate_bindings(
                reads, f"event_visuals.{exact_rule_id}.operations[{index}].read_paths"
            )
            animation_ms = operation.get("animation_ms")
            if animation_ms is not None and (type(animation_ms) not in (int, float) or animation_ms < 0):
                raise ValueError("animation_ms must be a nonnegative presentation duration")

    return profile


def _validate_legacy_profile(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw.get("world"), str) or not raw["world"]:
        raise ValueError("legacy scene profile must name world")
    for key in _LEGACY_REQUIRED_OBJECTS:
        if not isinstance(raw.get(key), dict):
            raise ValueError(f"legacy scene profile {key!r} must be an object")
    return deepcopy(raw)


def load_scene_contract(path: Path) -> dict[str, Any]:
    """Load either the living-scene v1 contract or an unchanged legacy v0 profile."""

    raw = json.loads(path.read_text())
    if not isinstance(raw, dict):
        raise ValueError("scene contract must be a JSON object")
    schema = raw.get("schema_version")
    if schema == LIVING_SCENE_SCHEMA_VERSION:
        return _validate_v1_profile(raw)
    if schema == LEGACY_SCENE_PROFILE_SCHEMA_VERSION:
        return _validate_legacy_profile(raw)
    raise ValueError(f"unsupported scene contract schema: {schema!r}")


def validate_live_projection_bundle(bundle: dict[str, Any]) -> None:
    """Validate the retained canonical projection seam without interpreting a scene."""

    if bundle.get("schema_version") != LIVE_PROJECTION_SCHEMA_VERSION:
        raise ValueError("living scene requires world-substrate-live-projection/v0")
    branch_id = bundle.get("branch_id")
    if not isinstance(branch_id, str) or not branch_id:
        raise ValueError("living scene projection branch_id must be nonempty")
    initial = bundle.get("initial_snapshot")
    if not isinstance(initial, dict) or initial.get("schema_version") != "world-substrate-snapshot/v1":
        raise ValueError("living scene requires world-substrate-snapshot/v1 initial_snapshot")
    world = initial.get("world")
    if not isinstance(world, dict) or not isinstance(world.get("world_id"), str) or not world["world_id"]:
        raise ValueError("living scene initial snapshot must name world_id")
    if bundle.get("world_id") != world["world_id"]:
        raise ValueError("living scene bundle world_id does not match initial snapshot")
    events = bundle.get("events")
    if not isinstance(events, list):
        raise ValueError("living scene projection events must be an array")
    ids = [event.get("event_id") for event in events if isinstance(event, dict)]
    if len(ids) != len(events) or any(not isinstance(event_id, str) or not event_id for event_id in ids):
        raise ValueError("every living scene event must have a stable event_id")
    if len(set(ids)) != len(ids):
        raise ValueError("living scene event ids must be unique")
    for event in events:
        if not isinstance(event.get("changes"), list):
            raise ValueError("living scene event changes must be an array")


def load_live_projection_bundle(path: Path) -> dict[str, Any]:
    """Load one retained live-projection bundle without invoking simulation authority."""

    raw = json.loads(path.read_text())
    if not isinstance(raw, dict):
        raise ValueError("living scene projection must be a JSON object")
    validate_live_projection_bundle(raw)
    return deepcopy(raw)


def canonical_world_at_boundary(bundle: dict[str, Any], boundary_index: int) -> dict[str, Any]:
    """Reconstruct canonical material state at one retained event boundary."""

    validate_live_projection_bundle(bundle)
    events = bundle["events"]
    if boundary_index < -1 or boundary_index >= len(events):
        raise IndexError("living scene boundary index is outside retained history")
    world = deepcopy(bundle["initial_snapshot"]["world"])
    for index in range(boundary_index + 1):
        apply_changes(world, events[index]["changes"])
    return world


def _validate_live_projection(bundle: dict[str, Any], profile: dict[str, Any]) -> None:
    validate_live_projection_bundle(bundle)
    if profile.get("schema_version") != LIVING_SCENE_SCHEMA_VERSION:
        raise ValueError("logical living frames require world-substrate-living-scene/v1")
    world = bundle["initial_snapshot"]["world"]
    if world.get("world_id") != profile.get("world"):
        raise ValueError("living scene profile world does not match canonical snapshot")


def _project_group(world: dict[str, Any], profile: dict[str, Any], group: str) -> dict[str, Any]:
    entities = world.get("entities")
    if not isinstance(entities, dict):
        raise ValueError("canonical world must contain entity mapping")
    rows: dict[str, Any] = {}
    for visual_id, visual in profile[group].items():
        entity_id = visual["entity"]
        entity = entities.get(entity_id)
        if not isinstance(entity, dict):
            raise ValueError(f"{group}.{visual_id} references absent canonical entity {entity_id!r}")
        bindings = {
            name: deepcopy(_lookup(entity, path))
            for name, path in visual.get("bindings", {}).items()
        }
        row: dict[str, Any] = {"entity": entity_id, "bindings": bindings}
        if "home" in visual:
            row["home"] = list(visual["home"])
        if "anchor" in visual:
            row["anchor"] = list(visual["anchor"])
        rows[visual_id] = row
    return rows


def _event_visual(event: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    rule_id = event.get("rule_id")
    visual = profile["event_visuals"].get(rule_id) if isinstance(rule_id, str) else None
    if not isinstance(visual, dict):
        return {
            "kind": "generic_event",
            "rule_id": rule_id,
            "operations": [],
        }
    return {
        "kind": "declared",
        "rule_id": rule_id,
        "label": visual.get("label"),
        "operations": deepcopy(visual.get("operations", [])),
    }


def _frame_from_world(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    world: dict[str, Any],
    boundary_index: int,
    event: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "schema_version": LIVING_SCENE_SCHEMA_VERSION,
        "scene_id": profile["scene_id"],
        "world_id": profile["world"],
        "branch_id": bundle.get("branch_id"),
        "boundary_index": boundary_index,
        "tick": world.get("tick"),
        "revision": world.get("revision"),
        "event": deepcopy(event),
        "event_visual": _event_visual(event, profile) if event is not None else None,
        "views": {
            "zones": deepcopy(profile["zones"]),
            "actors": _project_group(world, profile, "actors"),
            "entities": _project_group(world, profile, "entities"),
            "activities": _project_group(world, profile, "activities"),
            "institutions": _project_group(world, profile, "institutions"),
        },
    }


def rebuild_living_scene_frame(
    bundle: dict[str, Any], profile: dict[str, Any], boundary_index: int
) -> dict[str, Any]:
    """Rebuild one logical frame directly from canonical retained inputs.

    ``boundary_index`` is ``-1`` for the initial snapshot and otherwise names
    an event index in the retained projection bundle.
    """

    _validate_live_projection(bundle, profile)
    events = bundle["events"]
    if boundary_index < -1 or boundary_index >= len(events):
        raise IndexError("living scene boundary index is outside retained history")
    world = deepcopy(bundle["initial_snapshot"]["world"])
    event: dict[str, Any] | None = None
    for index in range(boundary_index + 1):
        event = events[index]
        changes = event.get("changes")
        if not isinstance(changes, list):
            raise ValueError("living scene event changes must be an array")
        apply_changes(world, changes)
    return _frame_from_world(bundle, profile, world, boundary_index, event)


def build_living_scene_frames(
    bundle: dict[str, Any], profile: dict[str, Any]
) -> list[dict[str, Any]]:
    """Build initial plus every canonical event-boundary logical frame."""

    _validate_live_projection(bundle, profile)
    world = deepcopy(bundle["initial_snapshot"]["world"])
    frames = [_frame_from_world(bundle, profile, world, -1, None)]
    for index, event in enumerate(bundle["events"]):
        changes = event.get("changes")
        if not isinstance(changes, list):
            raise ValueError("living scene event changes must be an array")
        apply_changes(world, changes)
        frames.append(_frame_from_world(bundle, profile, world, index, event))
    return frames


def normalized_frame_json(frame: dict[str, Any]) -> str:
    """Stable serialization for evidence and deterministic comparison."""

    return json.dumps(frame, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
