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

from scripts.bootstrap_scene_profile import bootstrap_profile
from scripts.render_scene_replay import render_html
from scripts.run_authored_world import _runtime_catalog, build_engine
from scripts.scaffold_world import _render_model, load_bundle
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


def _automatic_profile(
    bundle: dict[str, Any],
    trace: dict[str, Any],
    causal_model: Any,
) -> tuple[dict[str, Any], str]:
    model = _render_model(bundle)
    catalog = _runtime_catalog(bundle, causal_model)
    profile = bootstrap_profile(
        model,
        trace,
        catalog,
        world_model_ref=f"{bundle['world']['id']}-v0.json",
        auto_layout=True,
    )
    for actor in profile.get("actors", {}).values():
        actor.setdefault("carry_offset", [5, 3])
        actor.setdefault("carry_spacing", [0, 5])
    by_id = {row["entity_id"]: row for row in model["entities"]}
    html = render_html(trace, profile, by_id, REPO)
    return profile, html


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
    profile, html = _automatic_profile(bundle, trace, causal_model)
    return {
        "trace": trace,
        "projection": projection,
        "profile": profile,
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
