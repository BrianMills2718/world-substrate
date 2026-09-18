#!/usr/bin/env python3
"""Run one structured native coordination world through Engine and Automatic UI."""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_composed_living_scene import render_html
from scripts.run_authored_world import build_engine
from scripts.scaffold_world import load_bundle
from world_substrate.living_scene import build_living_scene_frames
from world_substrate.projection import build_live_projection

DEFAULT_CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"


def _members(bundle: dict[str, Any]) -> list[str]:
    return [
        row["id"]
        for row in bundle["entities"]
        if "member" in row.get("categories", [])
    ]


def _entity_with_category(bundle: dict[str, Any], category: str) -> str:
    rows = [
        row["id"]
        for row in bundle["entities"]
        if category in row.get("categories", [])
    ]
    if len(rows) != 1:
        raise ValueError(f"expected exactly one {category!r} entity, got {rows}")
    return rows[0]


def _report_plan(bundle: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    entities = {row["id"]: row for row in bundle["entities"]}
    deliveries = {}
    for row in bundle["entities"]:
        delivery = (row.get("components") or {}).get("delivery")
        if isinstance(delivery, dict):
            deliveries[delivery["info_id"]] = (row["id"], delivery["recipient_id"])
    plan = []
    for row in bundle["entities"]:
        info = (row.get("components") or {}).get("information")
        if not isinstance(info, dict):
            continue
        delivery_id, recipient_id = deliveries[row["id"]]
        if recipient_id not in entities:
            raise ValueError(f"report recipient is absent: {recipient_id}")
        plan.append((info["source_id"], row["id"], delivery_id, recipient_id))
    return sorted(plan)


def _authorized_member(bundle: dict[str, Any]) -> str:
    rows = [
        row["id"]
        for row in bundle["entities"]
        if ((row.get("components") or {}).get("member") or {}).get("authorized") is True
    ]
    if len(rows) != 1:
        raise ValueError(f"expected exactly one authorized member, got {rows}")
    return rows[0]


def _required_approvals(bundle: dict[str, Any]) -> int:
    gate_id = _entity_with_category(bundle, "gate")
    row = next(entity for entity in bundle["entities"] if entity["id"] == gate_id)
    return int(row["components"]["gate"]["required_approvals"])


def _attempt(
    engine: Any,
    actor: str,
    kind: str,
    *,
    expected_status: str,
    **fields: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    page = engine.discover(actor, kind=kind)
    matches = [
        row
        for row in [*page["available"], *page["blocked"]]
        if all(row["action"].get(key) == value for key, value in fields.items())
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"expected one {kind} attempt for {actor} {fields}, got {len(matches)}"
        )
    action = dict(matches[0]["action"])
    action["controller"] = "native-coordination-fixture"
    outcome = engine.submit(action)
    if outcome["status"] != expected_status:
        raise AssertionError(
            f"{kind} for {actor} returned {outcome['status']!r}, expected {expected_status!r}"
        )
    return action, outcome


def _transcript_turn(
    turn: int,
    actors: list[str],
    actor: str,
    action: dict[str, Any],
    outcome: dict[str, Any],
) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for actor_id in actors:
        if actor_id != actor:
            rows[actor_id] = {
                "wanted": None,
                "did": None,
                "status": "no_action",
                "retried": False,
                "said": "not scheduled for this deterministic fixture step",
                "refused_because": [],
                "lost_what_it_wanted": False,
            }
            continue
        failed = [
            check["label"]
            for check in outcome["event"].get("checks", [])
            if not check.get("ok") and check.get("label") != "Base revision is current"
        ]
        rows[actor_id] = {
            "wanted": deepcopy(action),
            "did": deepcopy(action),
            "status": outcome["status"],
            "retried": False,
            "said": f"deterministic fixture attempt: {action['kind']}",
            "refused_because": failed,
            "lost_what_it_wanted": False,
        }
    return {
        "turn": turn,
        "revision_when_decided": action["base_revision"],
        "committed_first": actor,
        "actors": rows,
        "progress": {},
    }


def _spread_points(count: int, *, y: float) -> list[list[float]]:
    if count < 1:
        return []
    if count == 1:
        return [[50.0, y]]
    left, right = 14.0, 86.0
    step = (right - left) / (count - 1)
    return [[round(left + index * step, 2), y] for index in range(count)]


def _living_profile(
    bundle: dict[str, Any],
    projection: dict[str, Any],
) -> dict[str, Any]:
    presentation = bundle.get("presentation") or {}
    assets = deepcopy(presentation.get("assets") or {})
    assets.setdefault("gate_marker", {"kind": "text", "value": "◎"})
    category_assets = presentation.get("category_assets") or {}

    members = [
        row for row in bundle["entities"]
        if "member" in row.get("categories", [])
    ]
    resources = [
        row for row in bundle["entities"]
        if "resource" in row.get("categories", [])
    ]
    gates = [
        row for row in bundle["entities"]
        if "gate" in row.get("categories", [])
    ]
    if len(gates) != 1:
        raise ValueError(f"expected exactly one gate for Living Scene, got {len(gates)}")

    actors: dict[str, Any] = {}
    for row, home in zip(members, _spread_points(len(members), y=76.0), strict=True):
        actors[row["id"]] = {
            "entity": row["id"],
            "asset": category_assets.get("member", "participant"),
            "label": row["label"],
            "home": home,
            "bindings": {
                "role": "components.member.role",
                "authorized": "components.member.authorized",
                "approved": "components.member.approved",
                "aware": "components.member.aware",
            },
            "render": {
                "state_binding": "approved",
                "inspector_fields": ["role", "authorized", "approved", "aware"],
            },
        }

    entity_views: dict[str, Any] = {}
    for row, home in zip(resources, _spread_points(len(resources), y=28.0), strict=True):
        entity_views[row["id"]] = {
            "entity": row["id"],
            "asset": category_assets.get("resource", "resource"),
            "label": row["label"],
            "home": home,
            "bindings": {
                "current": "components.resource.current",
                "required": "components.resource.required",
                "unit": "components.resource.unit",
            },
            "render": {
                "kind": "resource",
                "current_binding": "current",
                "required_binding": "required",
                "unit_binding": "unit",
                "inspector_fields": ["current", "required", "unit"],
            },
        }

    gate = gates[0]
    institutions = {
        gate["id"]: {
            "entity": gate["id"],
            "asset": "gate_marker",
            "label": gate["label"],
            "anchor": [50.0, 53.0],
            "bindings": {
                "status": "components.gate.status",
                "support": "components.gate.approval_count",
                "required": "components.gate.required_approvals",
            },
            "render": {
                "status_binding": "status",
                "support_binding": "support",
                "required_binding": "required",
                "inspector_fields": ["status", "support", "required"],
            },
        }
    }

    event_visuals = {
        "coordination.action.communicate": {
            "label": "represented information delivered",
            "operations": [
                {"op": "information.transmit", "delivery_from_changed_entities": True},
                {"op": "action.feedback", "label": "communication attempt"},
            ],
        },
        "coordination.action.approve": {
            "label": "approval attempt",
            "operations": [{"op": "action.feedback", "label": "approval attempt"}],
        },
        "coordination.action.intervene": {
            "label": "represented prerequisite restored",
            "operations": [{"op": "action.feedback", "label": "intervention attempt"}],
        },
        "coordination.action.finalize": {
            "label": "coordination gate evaluated",
            "operations": [{"op": "action.feedback", "label": "finalization attempt"}],
        },
    }

    return {
        "schema_version": "world-substrate-living-scene/v1",
        "scene_id": f"{bundle['world']['id']}-automatic-v1",
        "world": projection["world_id"],
        "title": bundle["world"]["label"],
        "subtitle": bundle["world"]["summary"],
        "note": "Automatic read-only Living Scene generated from structured world state and retained Engine history.",
        "assets": assets,
        "scene": {
            "aspect_ratio": "16 / 9",
            "autoplay_ms": 900,
            "mobile_min_height": 680,
        },
        "zones": {
            "coordination-space": {
                "label": "Coordination space",
                "rect": [4.0, 7.0, 92.0, 86.0],
                "anchor": [50.0, 50.0],
            }
        },
        "actors": actors,
        "entities": entity_views,
        "activities": {},
        "institutions": institutions,
        "event_visuals": event_visuals,
        "state_styles": {
            "true": "positive",
            "false": "neutral",
            "ready": "positive",
            "blocked": "danger",
        },
        "presentation": {},
    }


def _living_ui(
    bundle: dict[str, Any],
    projection: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    profile = _living_profile(bundle, projection)
    frames = build_living_scene_frames(projection, profile)
    html = render_html(projection, profile, REPO)
    return profile, frames, html

def run_native_coordination(
    bundle: dict[str, Any],
    causal_value: dict[str, Any],
) -> dict[str, Any]:
    engine, causal_model, profile_id = build_engine(bundle, causal_value)
    actors = _members(bundle)
    gate_id = _entity_with_category(bundle, "gate")
    prerequisites = {
        f"prereq_{letter}": _entity_with_category(bundle, f"prereq-{letter}")
        for letter in ("a", "b", "c", "d")
    }
    restorable = _entity_with_category(bundle, "restorable")
    authorized = _authorized_member(bundle)
    reports = _report_plan(bundle)
    transcript: list[dict[str, Any]] = []
    turn = 1

    for source, information, delivery, recipient in reports:
        action, outcome = _attempt(
            engine,
            source,
            "communicate",
            expected_status="accepted",
            information=information,
            delivery=delivery,
            recipient=recipient,
        )
        transcript.append(_transcript_turn(turn, actors, source, action, outcome))
        turn += 1

    voters = [recipient for _, _, _, recipient in reports]
    if len(voters) < _required_approvals(bundle):
        raise AssertionError("fixture does not deliver enough reports to satisfy its approval threshold")

    blocked_action, blocked = _attempt(
        engine,
        voters[0],
        "approve",
        expected_status="precondition_failed",
        gate=gate_id,
        **prerequisites,
    )
    transcript.append(_transcript_turn(turn, actors, voters[0], blocked_action, blocked))
    blocked_event_id = blocked["event"]["event_id"]
    turn += 1

    intervention_action, intervention = _attempt(
        engine,
        authorized,
        "intervene",
        expected_status="accepted",
        resource=restorable,
    )
    transcript.append(
        _transcript_turn(turn, actors, authorized, intervention_action, intervention)
    )
    turn += 1

    for actor in voters[: _required_approvals(bundle)]:
        action, outcome = _attempt(
            engine,
            actor,
            "approve",
            expected_status="accepted",
            gate=gate_id,
            **prerequisites,
        )
        transcript.append(_transcript_turn(turn, actors, actor, action, outcome))
        turn += 1

    finalize_action, finalized = _attempt(
        engine,
        authorized,
        "finalize",
        expected_status="accepted",
        gate=gate_id,
        **prerequisites,
    )
    transcript.append(_transcript_turn(turn, actors, authorized, finalize_action, finalized))

    if causal_model.terminal is None or not causal_model.terminal.reached(engine.world):
        raise AssertionError("native coordination fixture did not reach its state-derived terminal")

    trace = {
        "schema_version": "world-substrate-contested-run/v3",
        "world": bundle["world"]["id"],
        "actors": actors,
        "model": "scripted-native-coordination",
        "cost_usd": 0.0,
        "mechanic_profile_id": profile_id,
        "summary": {
            "turns": len(transcript),
            "terminal_reached": True,
            "accepted_actions": sum(
                1
                for row in transcript
                for record in row["actors"].values()
                if record.get("status") == "accepted"
            ),
            "blocked_event_id": blocked_event_id,
        },
        "transcript": transcript,
    }
    projection = build_live_projection(
        initial_snapshot=engine.initial_snapshot(),
        events=engine.world.events,
        scene={
            "kind": "automatic-scene-profile-v0",
            "source": "structured-native-coordination",
        },
        branch_id=f"{bundle['world']['id']}-deterministic",
    )
    profile, frames, html = _living_ui(bundle, projection)
    return {
        "trace": trace,
        "projection": projection,
        "profile": profile,
        "frames": frames,
        "html": html,
        "engine": engine,
        "causal_model": causal_model,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--causal-model", type=Path, default=DEFAULT_CAUSAL)
    parser.add_argument("--trace-output", type=Path)
    parser.add_argument("--projection-output", type=Path)
    parser.add_argument("--profile-output", type=Path)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args()

    bundle = load_bundle(args.bundle)
    causal_value = json.loads(args.causal_model.read_text())
    result = run_native_coordination(bundle, causal_value)
    outputs = [
        (args.trace_output, result["trace"]),
        (args.projection_output, result["projection"]),
        (args.profile_output, result["profile"]),
    ]
    for path, value in outputs:
        if path is not None:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(value, indent=2) + "\n")
    if args.html_output is not None:
        args.html_output.parent.mkdir(parents=True, exist_ok=True)
        args.html_output.write_text(result["html"])
    print(json.dumps(result["trace"]["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
