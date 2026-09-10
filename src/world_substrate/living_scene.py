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

from world_substrate.information import DELIVERED_STATUSES, information_visible_in_material_world
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
        if "mobile_rect" in zone:
            zone["mobile_rect"] = _rect(zone["mobile_rect"], f"zone {zone_id}.mobile_rect")
        if "anchor" in zone:
            zone["anchor"] = _point(zone["anchor"], f"zone {zone_id}.anchor")
        if "mobile_anchor" in zone:
            zone["mobile_anchor"] = _point(zone["mobile_anchor"], f"zone {zone_id}.mobile_anchor")

    allowed_style_tokens = {"positive", "warning", "danger", "neutral", "muted"}
    for state, token in profile["state_styles"].items():
        if not isinstance(state, str) or not state:
            raise ValueError("state_styles keys must be nonempty strings")
        if token not in allowed_style_tokens:
            raise ValueError(
                "state_styles values must be one of: "
                + ", ".join(sorted(allowed_style_tokens))
            )

    for group in _BINDABLE_GROUPS:
        for visual_id, visual in profile[group].items():
            if not isinstance(visual_id, str) or not visual_id or not isinstance(visual, dict):
                raise ValueError(f"living scene {group} must map nonempty ids to objects")
            if "home" in visual:
                visual["home"] = _point(visual["home"], f"{group}.{visual_id}.home")
            if "mobile_home" in visual:
                visual["mobile_home"] = _point(visual["mobile_home"], f"{group}.{visual_id}.mobile_home")
            if "anchor" in visual:
                visual["anchor"] = _point(visual["anchor"], f"{group}.{visual_id}.anchor")
            if "mobile_anchor" in visual:
                visual["mobile_anchor"] = _point(visual["mobile_anchor"], f"{group}.{visual_id}.mobile_anchor")
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


def _changed_entity_ids(event: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for change in event.get("changes") or []:
        path = change.get("path") if isinstance(change, dict) else None
        if not isinstance(path, str):
            continue
        parts = path.split(".")
        if len(parts) >= 2 and parts[0] == "entities" and parts[1] not in ids:
            ids.append(parts[1])
    return ids


def _information_transmissions(
    world: dict[str, Any],
    event: dict[str, Any],
    operation: dict[str, Any],
    observer_actor_id: str | None,
) -> list[dict[str, Any]]:
    entities = world.get("entities")
    if not isinstance(entities, dict):
        return []
    explicit = operation.get("delivery_entity")
    if explicit is not None and (not isinstance(explicit, str) or not explicit):
        raise ValueError("information.transmit delivery_entity must be a nonempty string")
    if isinstance(explicit, str):
        candidates = [explicit]
    elif operation.get("delivery_from_changed_entities") is True:
        candidates = _changed_entity_ids(event)
    else:
        raise ValueError(
            "information.transmit requires delivery_entity or delivery_from_changed_entities=true"
        )

    rows: list[dict[str, Any]] = []
    for delivery_id in candidates:
        delivery_entity = entities.get(delivery_id)
        if not isinstance(delivery_entity, dict):
            if isinstance(explicit, str):
                raise ValueError(f"information.transmit references absent delivery entity {delivery_id!r}")
            continue
        components = delivery_entity.get("components")
        delivery = components.get("delivery") if isinstance(components, dict) else None
        if not isinstance(delivery, dict) or delivery.get("status") not in DELIVERED_STATUSES:
            continue
        info_id = delivery.get("info_id")
        if not isinstance(info_id, str):
            continue
        info_entity = entities.get(info_id)
        info_components = info_entity.get("components") if isinstance(info_entity, dict) else None
        info = info_components.get("information") if isinstance(info_components, dict) else None
        if not isinstance(info, dict):
            continue
        source_id = info.get("source_id")
        recipient_id = delivery.get("recipient_id")
        if not isinstance(source_id, str) or not isinstance(recipient_id, str):
            continue
        public_content = info.get("visibility") == "public" and info.get("active") is True
        observer_authorized = (
            isinstance(observer_actor_id, str)
            and information_visible_in_material_world(world, observer_actor_id, info_id)
        )
        content_visible = public_content or observer_authorized
        rows.append(
            {
                "kind": "information_transmission",
                "delivery_id": delivery_id,
                "info_id": info_id,
                "source_id": source_id,
                "recipient_id": recipient_id,
                "channel_id": delivery.get("channel_id"),
                "topic": info.get("topic"),
                "content_visible": content_visible,
                "content": deepcopy(info.get("content")) if content_visible else None,
            }
        )
    return rows


def _action_feedback(event: dict[str, Any], operation: dict[str, Any]) -> dict[str, Any]:
    status = event.get("status")
    if status not in {"accepted", "rejected", "refused", "blocked"}:
        status = "unknown"
    reasons: list[str] = []
    for check in event.get("checks") or []:
        if isinstance(check, dict) and check.get("ok") is False:
            label = check.get("label")
            if isinstance(label, str) and label:
                reasons.append(label)
    return {
        "kind": "action_feedback",
        "status": status,
        "label": operation.get("label"),
        "reasons": reasons,
    }


def _presentation_effects(
    world: dict[str, Any],
    event: dict[str, Any] | None,
    event_visual: dict[str, Any] | None,
    observer_actor_id: str | None,
) -> list[dict[str, Any]]:
    if event is None or not isinstance(event_visual, dict) or event_visual.get("kind") != "declared":
        return []
    effects: list[dict[str, Any]] = []
    for operation in event_visual.get("operations") or []:
        op = operation.get("op") if isinstance(operation, dict) else None
        if op == "information.transmit":
            effects.extend(_information_transmissions(world, event, operation, observer_actor_id))
        elif op == "action.feedback":
            effects.append(_action_feedback(event, operation))
    return effects


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


def _presentation_event(event: dict[str, Any] | None) -> dict[str, Any] | None:
    """Return only event metadata safe for the generic living-scene payload.

    Retained events can carry actor-scoped observations and information-context
    content. Those remain evidence-layer data and are deliberately not copied
    wholesale into a public presentation frame.
    """

    if event is None:
        return None
    safe: dict[str, Any] = {}
    for key in (
        "event_id",
        "rule_id",
        "rule_version",
        "status",
        "tick",
        "world_revision",
        "causal_bearer",
        "causal_parent_event_ids",
    ):
        if key in event:
            safe[key] = deepcopy(event[key])
    return safe


def _frame_from_world(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    world: dict[str, Any],
    boundary_index: int,
    event: dict[str, Any] | None,
    observer_actor_id: str | None = None,
) -> dict[str, Any]:
    event_visual = _event_visual(event, profile) if event is not None else None
    return {
        "schema_version": LIVING_SCENE_SCHEMA_VERSION,
        "scene_id": profile["scene_id"],
        "world_id": profile["world"],
        "branch_id": bundle.get("branch_id"),
        "boundary_index": boundary_index,
        "tick": world.get("tick"),
        "revision": world.get("revision"),
        "event": _presentation_event(event),
        "event_visual": event_visual,
        "presentation_effects": _presentation_effects(
            world, event, event_visual, observer_actor_id
        ),
        "views": {
            "zones": deepcopy(profile["zones"]),
            "actors": _project_group(world, profile, "actors"),
            "entities": _project_group(world, profile, "entities"),
            "activities": _project_group(world, profile, "activities"),
            "institutions": _project_group(world, profile, "institutions"),
        },
    }


def rebuild_living_scene_frame(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    boundary_index: int,
    *,
    observer_actor_id: str | None = None,
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
    return _frame_from_world(
        bundle, profile, world, boundary_index, event, observer_actor_id
    )


def build_living_scene_frames(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    *,
    observer_actor_id: str | None = None,
) -> list[dict[str, Any]]:
    """Build initial plus every canonical event-boundary logical frame."""

    _validate_live_projection(bundle, profile)
    world = deepcopy(bundle["initial_snapshot"]["world"])
    frames = [_frame_from_world(bundle, profile, world, -1, None, observer_actor_id)]
    for index, event in enumerate(bundle["events"]):
        changes = event.get("changes")
        if not isinstance(changes, list):
            raise ValueError("living scene event changes must be an array")
        apply_changes(world, changes)
        frames.append(
            _frame_from_world(bundle, profile, world, index, event, observer_actor_id)
        )
    return frames


def normalized_frame_json(frame: dict[str, Any]) -> str:
    """Stable serialization for evidence and deterministic comparison."""

    return json.dumps(frame, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
