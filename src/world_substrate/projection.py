"""Read-only living-world projection over canonical snapshots and events."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any, Iterable

LIVE_PROJECTION_SCHEMA_VERSION = "world-substrate-live-projection/v0"


def apply_changes(material_world: dict[str, Any], changes: Iterable[dict[str, Any]]) -> None:
    """Apply an Engine event's deterministic leaf deltas to a material projection."""

    for change in changes:
        path = change.get("path")
        if not isinstance(path, str) or not path:
            raise ValueError("projection change path must be a nonempty string")
        cursor: Any = material_world
        segments = path.split(".")
        for segment in segments[:-1]:
            if not isinstance(cursor, dict) or segment not in cursor:
                raise ValueError(f"projection change parent is missing: {path}")
            cursor = cursor[segment]
        if not isinstance(cursor, dict):
            raise ValueError(f"projection change parent is not an object: {path}")
        cursor[segments[-1]] = deepcopy(change.get("after"))


def replay_projection(initial_snapshot: dict[str, Any], events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Reconstruct material state from the one-way initial-snapshot + delta seam."""

    if initial_snapshot.get("schema_version") != "world-substrate-snapshot/v1":
        raise ValueError("unsupported initial snapshot")
    world = deepcopy(initial_snapshot["world"])
    for event in events:
        changes = event.get("changes")
        if not isinstance(changes, list):
            raise ValueError("projection event changes must be an array")
        apply_changes(world, changes)
    return world


def build_live_projection(
    *,
    initial_snapshot: dict[str, Any],
    events: list[dict[str, Any]],
    scene: dict[str, Any],
    branch_id: str,
    annotations: dict[str, dict[str, Any]] | None = None,
    analysis: dict[str, Any] | None = None,
    adequacy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Package canonical run data plus explicitly downstream presentation metadata."""

    if not branch_id:
        raise ValueError("branch_id must be nonempty")
    annotations = annotations or {}
    event_ids = [event.get("event_id") for event in events]
    if any(not isinstance(event_id, str) or not event_id for event_id in event_ids):
        raise ValueError("every projected event must have a stable event_id")
    if len(set(event_ids)) != len(event_ids):
        raise ValueError("projected event ids must be unique")
    reconstructed = replay_projection(initial_snapshot, events)
    return {
        "schema_version": LIVE_PROJECTION_SCHEMA_VERSION,
        "branch_id": branch_id,
        "world_id": initial_snapshot["world"]["world_id"],
        "initial_snapshot": deepcopy(initial_snapshot),
        "events": deepcopy(events),
        "scene": deepcopy(scene),
        "annotations": deepcopy(annotations),
        "analysis": deepcopy(analysis) if analysis is not None else None,
        "adequacy": deepcopy(adequacy) if adequacy is not None else None,
        "projection_final": reconstructed,
        "projection_final_hash": events[-1]["hash_after"] if events else None,
    }


def encode_sse(event: str, data: dict[str, Any], *, event_id: str | None = None) -> str:
    """Encode one server-sent event for the read-only living stream."""

    if not event or "\n" in event:
        raise ValueError("SSE event name must be one line")
    rows = []
    if event_id is not None:
        if "\n" in event_id:
            raise ValueError("SSE id must be one line")
        rows.append(f"id: {event_id}")
    rows.append(f"event: {event}")
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"))
    for line in payload.splitlines() or [""]:
        rows.append(f"data: {line}")
    return "\n".join(rows) + "\n\n"


def projection_sse_messages(bundle: dict[str, Any]) -> list[str]:
    """Return the initial snapshot followed by canonical event/delta messages."""

    if bundle.get("schema_version") != LIVE_PROJECTION_SCHEMA_VERSION:
        raise ValueError("unsupported live projection bundle")
    messages = [
        encode_sse(
            "snapshot",
            {
                "branch_id": bundle["branch_id"],
                "snapshot": bundle["initial_snapshot"],
                "scene": bundle["scene"],
            },
            event_id=f"{bundle['branch_id']}:snapshot",
        )
    ]
    for event in bundle["events"]:
        event_id = event["event_id"]
        messages.append(
            encode_sse(
                "world-event",
                {
                    "branch_id": bundle["branch_id"],
                    "event": event,
                    "annotation": bundle.get("annotations", {}).get(event_id),
                },
                event_id=f"{bundle['branch_id']}:{event_id}",
            )
        )
    messages.append(
        encode_sse(
            "complete",
            {
                "branch_id": bundle["branch_id"],
                "event_count": len(bundle["events"]),
                "projection_final_hash": bundle.get("projection_final_hash"),
            },
            event_id=f"{bundle['branch_id']}:complete",
        )
    )
    return messages
