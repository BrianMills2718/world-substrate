#!/usr/bin/env python3
"""Run one structured native coordination world through Engine and Automatic UI."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_composed_living_scene import render_html
from scripts.run_authored_world import build_engine
from scripts.scaffold_world import load_bundle
from world_substrate.action_authoring import CausalModel
from world_substrate.information import information_visible_in_material_world
from world_substrate.living_scene import build_living_scene_frames
from world_substrate.projection import build_live_projection

DEFAULT_CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"
DEFAULT_ACCEPTANCE = REPO / "examples/native_coordination/acceptance-v0.json"
DIAGNOSTIC_SCHEMA = "world-substrate-native-coordination-diagnostic/v0"
ACCEPTANCE_SCHEMA = "world-substrate-native-coordination-acceptance/v0"
ACCEPTANCE_RESULT_SCHEMA = "world-substrate-native-coordination-acceptance-result/v0"
MANIFEST_SCHEMA = "world-substrate-native-coordination-diagnostic-manifest/v0"
STAGE_FAILURE_CATEGORY = {
    "input": "input",
    "compiler": "compiler",
    "engine": "engine",
    "projection": "projection",
    "renderer": "renderer",
    "acceptance": "acceptance",
}
FAILURE_CATEGORIES = frozenset({
    "input",
    "compiler",
    "mechanic_check",
    "authority",
    "engine",
    "information_visibility",
    "projection",
    "renderer",
    "acceptance",
    "environment",
})


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_manifest(output_dir: Path, run_id: str) -> dict[str, Any]:
    rows = {}
    for path in sorted(output_dir.iterdir(), key=lambda row: row.name):
        if not path.is_file() or path.name == "manifest.json":
            continue
        rows[path.name] = {
            "sha256": _file_hash(path),
            "bytes": path.stat().st_size,
        }
    value = {
        "schema_version": MANIFEST_SCHEMA,
        "run_id": run_id,
        "artifacts": rows,
    }
    _write_json(output_dir / "manifest.json", value)
    return value


def load_acceptance(path: Path = DEFAULT_ACCEPTANCE) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if value.get("schema_version") != ACCEPTANCE_SCHEMA:
        raise ValueError(f"acceptance matrix must use {ACCEPTANCE_SCHEMA}")
    if not isinstance(value.get("common"), dict):
        raise ValueError("acceptance matrix common must be an object")
    if not isinstance(value.get("worlds"), dict):
        raise ValueError("acceptance matrix worlds must be an object")
    return value


def _acceptance_expectation(
    acceptance: dict[str, Any], bundle: dict[str, Any]
) -> dict[str, Any]:
    world_id = bundle["world"]["id"]
    row = acceptance["worlds"].get(world_id)
    if not isinstance(row, dict) or not isinstance(row.get("expected"), dict):
        raise ValueError(f"acceptance matrix has no expectations for {world_id!r}")
    return row["expected"]


def _check(
    check_id: str,
    category: str,
    passed: bool,
    *,
    expected: object = None,
    observed: object = None,
) -> dict[str, Any]:
    return {
        "id": check_id,
        "category": category,
        "passed": bool(passed),
        "expected": deepcopy(expected),
        "observed": deepcopy(observed),
    }


def evaluate_acceptance(
    bundle: dict[str, Any],
    result: dict[str, Any],
    acceptance: dict[str, Any],
) -> dict[str, Any]:
    expected = _acceptance_expectation(acceptance, bundle)
    common = acceptance["common"]
    checks: list[dict[str, Any]] = []
    entities = bundle["entities"]
    members = [row for row in entities if "member" in row.get("categories", [])]
    resources = [row for row in entities if "resource" in row.get("categories", [])]
    infos = [row for row in entities if "information" in row.get("categories", [])]
    deliveries = {
        row["components"]["delivery"]["info_id"]: row["components"]["delivery"]
        for row in entities
        if "delivery" in (row.get("components") or {})
    }
    gate_id = expected["gate_id"]
    gate_row = next(row for row in entities if row["id"] == gate_id)
    channels = sorted(
        {row["components"]["information"]["channel_id"] for row in infos}
    )
    mechanics = sorted(m.action_kind for m in result["causal_model"].mechanics)

    checks.extend([
        _check(
            "config.member_count", "input",
            len(members) == expected["member_count"],
            expected=expected["member_count"], observed=len(members),
        ),
        _check(
            "config.resource_count", "input",
            len(resources) == expected["resource_count"],
            expected=expected["resource_count"], observed=len(resources),
        ),
        _check(
            "config.report_count", "input",
            len(infos) == expected["report_count"],
            expected=expected["report_count"], observed=len(infos),
        ),
        _check(
            "config.channels", "input",
            channels == sorted(expected["channels"]),
            expected=sorted(expected["channels"]), observed=channels,
        ),
        _check(
            "config.required_approvals", "input",
            gate_row["components"]["gate"]["required_approvals"] == expected["required_approvals"],
            expected=expected["required_approvals"],
            observed=gate_row["components"]["gate"]["required_approvals"],
        ),
        _check(
            "compiler.action_kinds", "compiler",
            mechanics == sorted(common["mechanic_action_kinds"]),
            expected=sorted(common["mechanic_action_kinds"]), observed=mechanics,
        ),
    ])

    trace = result["trace"]
    projection = result["projection"]
    events = projection["events"]
    blocked_id = trace["summary"]["blocked_event_id"]
    blocked = next(event for event in events if event["event_id"] == blocked_id)
    failed_labels = sorted(
        row["label"] for row in blocked.get("checks", []) if row.get("ok") is False
    )
    checks.extend([
        _check(
            "engine.zero_provider_spend", "engine",
            trace["cost_usd"] == common["provider_spend_usd"],
            expected=common["provider_spend_usd"], observed=trace["cost_usd"],
        ),
        _check(
            "engine.terminal_reached", "engine",
            trace["summary"]["terminal_reached"] is True,
            expected=True, observed=trace["summary"]["terminal_reached"],
        ),
        _check(
            "engine.intentional_block", "mechanic_check",
            blocked.get("status") == "precondition_failed"
            and expected["blocked_check"] in failed_labels,
            expected={
                "status": "precondition_failed",
                "failed_check": expected["blocked_check"],
            },
            observed={"status": blocked.get("status"), "failed_checks": failed_labels},
        ),
    ])

    scope_violations = [
        event["event_id"]
        for event in events
        if event.get("status") == "scope_violation"
    ]
    checks.append(
        _check(
            "authority.no_scope_violations",
            "authority",
            not scope_violations,
            expected=[],
            observed=scope_violations,
        )
    )

    intervention = [
        event for event in events
        if event.get("rule_id") == "coordination.action.intervene"
        and event.get("status") == "accepted"
    ]
    intervention_actor = (
        (intervention[-1].get("causal_bearer") or {}).get("id")
        if intervention else None
    )
    intervention_changed = (
        any(
            change.get("path", "").startswith(
                f"entities.{expected['restorable_resource']}."
            )
            for change in intervention[-1].get("changes", [])
        )
        if intervention else False
    )
    checks.append(
        _check(
            "engine.represented_intervention", "engine",
            bool(intervention)
            and intervention_actor == expected["intervention_actor"]
            and intervention_changed,
            expected={
                "actor": expected["intervention_actor"],
                "resource": expected["restorable_resource"],
            },
            observed={
                "actor": intervention_actor,
                "resource_changed": intervention_changed,
            },
        )
    )

    final_gate = result["engine"].world.entities[gate_id].component("gate")
    checks.append(
        _check(
            "engine.final_gate", "engine",
            final_gate.status == common["terminal_gate_status"]
            and final_gate.approval_count >= final_gate.required_approvals,
            expected={
                "status": common["terminal_gate_status"],
                "required_approvals": expected["required_approvals"],
            },
            observed={
                "status": final_gate.status,
                "approval_count": final_gate.approval_count,
                "required_approvals": final_gate.required_approvals,
            },
        )
    )

    final_world = projection["projection_final"]
    member_ids = [row["id"] for row in members]
    visibility_failures: list[dict[str, Any]] = []
    for info_row in infos:
        info_id = info_row["id"]
        info = info_row["components"]["information"]
        delivery = deliveries[info_id]
        source = info["source_id"]
        recipient = delivery["recipient_id"]
        recipient_visible = information_visible_in_material_world(
            final_world, recipient, info_id
        )
        outsiders = [
            actor for actor in member_ids if actor not in {source, recipient}
        ]
        leaked = [
            actor for actor in outsiders
            if information_visible_in_material_world(final_world, actor, info_id)
        ]
        if not recipient_visible or leaked:
            visibility_failures.append({
                "info_id": info_id,
                "recipient": recipient,
                "recipient_visible": recipient_visible,
                "leaked_to": leaked,
            })
    checks.append(
        _check(
            "information.actor_scoped_visibility", "information_visibility",
            not visibility_failures,
            expected="recipient sees direct delivery; unrelated members do not",
            observed=visibility_failures,
        )
    )

    final_hash = events[-1]["hash_after"] if events else None
    checks.extend([
        _check(
            "projection.final_hash", "projection",
            projection.get("projection_final_hash") == final_hash,
            expected=final_hash, observed=projection.get("projection_final_hash"),
        ),
        _check(
            "projection.frame_count", "projection",
            len(result["frames"]) == len(events) + 1,
            expected=len(events) + 1, observed=len(result["frames"]),
        ),
        _check(
            "projection.matches_canonical_world", "projection",
            projection.get("projection_final") == result["engine"].world.material_dict(),
            expected="exact canonical material state",
            observed="match"
            if projection.get("projection_final") == result["engine"].world.material_dict()
            else "mismatch",
        ),
    ])

    html = result["html"]
    final_frame = result["frames"][-1]
    gate_view = final_frame["views"]["institutions"][gate_id]["bindings"]
    transmissions = [
        effect
        for frame in result["frames"]
        for effect in frame.get("presentation_effects", [])
        if effect.get("kind") == "information_transmission"
    ]
    blocked_frame = next(
        frame for frame in result["frames"]
        if (frame.get("event") or {}).get("event_id") == blocked_id
    )
    feedback_rows = [
        effect for effect in blocked_frame.get("presentation_effects", [])
        if effect.get("kind") == "action_feedback"
    ]
    feedback_reasons = sorted(
        {
            reason
            for effect in feedback_rows
            for reason in effect.get("reasons", [])
        }
    )
    checks.extend([
        _check(
            "renderer.generic_controls", "renderer",
            "id='inspector'" in html and "id='scrub'" in html,
            expected=["inspector", "canonical event scrubber"],
            observed={
                "inspector": "id='inspector'" in html,
                "scrubber": "id='scrub'" in html,
            },
        ),
        _check(
            "renderer.final_gate", "renderer",
            gate_view.get("status") == common["terminal_gate_status"]
            and gate_view.get("support", 0) >= gate_view.get("required", 0),
            expected=common["terminal_gate_status"], observed=gate_view,
        ),
        _check(
            "renderer.information_movement", "renderer",
            bool(transmissions),
            expected="at least one represented transmission",
            observed=len(transmissions),
        ),
        _check(
            "renderer.private_content_hidden", "information_visibility",
            bool(transmissions)
            and all(effect.get("content_visible") is False for effect in transmissions),
            expected=False,
            observed=sorted({effect.get("content_visible") for effect in transmissions}),
        ),
        _check(
            "renderer.failed_check_feedback", "renderer",
            expected["blocked_check"] in feedback_reasons,
            expected=expected["blocked_check"], observed=feedback_reasons,
        ),
    ])

    failed = [row for row in checks if not row["passed"]]
    return {
        "schema_version": ACCEPTANCE_RESULT_SCHEMA,
        "world_id": bundle["world"]["id"],
        "passed": not failed,
        "checks": checks,
        "failed_check_ids": [row["id"] for row in failed],
    }


def _summary(
    *,
    run_id: str,
    bundle: dict[str, Any],
    stage: str,
    status: str,
    failure_category: str | None = None,
    error: BaseException | None = None,
    result: dict[str, Any] | None = None,
    acceptance_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    trace = result.get("trace") if result else None
    projection = result.get("projection") if result else None
    value: dict[str, Any] = {
        "schema_version": DIAGNOSTIC_SCHEMA,
        "run_id": run_id,
        "world_id": bundle["world"]["id"],
        "stage": stage,
        "status": status,
        "failure_category": failure_category,
        "provider_spend_usd": trace.get("cost_usd") if trace else None,
        "mechanic_profile_id": trace.get("mechanic_profile_id") if trace else None,
        "terminal_reached": (trace.get("summary") or {}).get("terminal_reached") if trace else None,
        "event_count": len(projection.get("events", [])) if projection else None,
        "projection_final_hash": projection.get("projection_final_hash") if projection else None,
        "acceptance_passed": acceptance_result.get("passed") if acceptance_result else None,
    }
    if error is not None:
        value["error"] = {
            "type": type(error).__name__,
            "message": str(error),
        }
    return value


def run_diagnostic(
    bundle: dict[str, Any],
    causal_value: dict[str, Any],
    *,
    acceptance: dict[str, Any],
    output_dir: Path,
    run_id: str | None = None,
) -> dict[str, Any]:
    run_id = run_id or f"native-coordination/{bundle['world']['id']}/{uuid.uuid4().hex}"
    output_dir.mkdir(parents=True, exist_ok=True)
    stage = "input"
    result: dict[str, Any] | None = None
    acceptance_result: dict[str, Any] | None = None
    _write_json(output_dir / "input-bundle.json", bundle)
    _write_json(output_dir / "causal-model.json", causal_value)
    _write_json(output_dir / "acceptance-matrix.json", acceptance)
    _write_json(
        output_dir / "summary.json",
        _summary(run_id=run_id, bundle=bundle, stage=stage, status="running"),
    )

    def checkpoint(name: str, payload: dict[str, Any]) -> None:
        nonlocal stage
        stage = name
        engine = payload.get("engine")
        causal_model = payload.get("causal_model")
        if causal_model is not None:
            _write_json(output_dir / "mechanics-review.json", causal_model.as_review())
        if engine is not None:
            _write_json(output_dir / "initial-snapshot.json", engine.initial_snapshot())
            _write_json(output_dir / "commands.json", engine.world.commands)
            _write_json(output_dir / "events.json", engine.world.events)
        projection = payload.get("projection")
        if projection is not None:
            _write_json(output_dir / "projection.json", projection)
        profile = payload.get("profile")
        if profile is not None:
            _write_json(output_dir / "living-profile.json", profile)
        frames = payload.get("frames")
        if frames is not None:
            _write_json(output_dir / "living-frames.json", frames)
        html = payload.get("html")
        if isinstance(html, str):
            _write_text(output_dir / "render.html", html)
        _write_json(
            output_dir / "summary.json",
            _summary(run_id=run_id, bundle=bundle, stage=stage, status="running"),
        )

    try:
        stage = "compiler"
        declared = CausalModel.from_dict(causal_value, bundle=bundle)
        _write_json(output_dir / "mechanics-review.json", declared.as_review())
        _write_json(
            output_dir / "summary.json",
            _summary(run_id=run_id, bundle=bundle, stage=stage, status="running"),
        )
        result = run_native_coordination(
            bundle, causal_value, stage_callback=checkpoint
        )
        _write_json(output_dir / "trace.json", result["trace"])
        checkpoint("projection", {"projection": result["projection"]})
        checkpoint(
            "renderer",
            {
                "profile": result["profile"],
                "frames": result["frames"],
                "html": result["html"],
            },
        )
        stage = "acceptance"
        acceptance_result = evaluate_acceptance(bundle, result, acceptance)
        _write_json(output_dir / "acceptance.json", acceptance_result)
        if not acceptance_result["passed"]:
            first = next(
                row for row in acceptance_result["checks"] if not row["passed"]
            )
            category = first["category"]
            failure_category = (
                category if category in FAILURE_CATEGORIES else "acceptance"
            )
            summary = _summary(
                run_id=run_id,
                bundle=bundle,
                stage=stage,
                status="failed",
                failure_category=failure_category,
                result=result,
                acceptance_result=acceptance_result,
            )
            _write_json(output_dir / "summary.json", summary)
            _write_manifest(output_dir, run_id)
            return summary

        stage = "complete"
        summary = _summary(
            run_id=run_id,
            bundle=bundle,
            stage=stage,
            status="passed",
            result=result,
            acceptance_result=acceptance_result,
        )
        _write_json(output_dir / "summary.json", summary)
        _write_manifest(output_dir, run_id)
        return summary
    except Exception as error:
        failure_category = STAGE_FAILURE_CATEGORY.get(stage, "environment")
        summary = _summary(
            run_id=run_id,
            bundle=bundle,
            stage=stage,
            status="failed",
            failure_category=failure_category,
            error=error,
            result=result,
            acceptance_result=acceptance_result,
        )
        _write_json(output_dir / "summary.json", summary)
        _write_manifest(output_dir, run_id)
        return summary



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
    *,
    stage_callback: Any | None = None,
) -> dict[str, Any]:
    def checkpoint(stage: str, **payload: Any) -> None:
        if stage_callback is not None:
            stage_callback(stage, payload)

    checkpoint("compiler")
    engine, causal_model, profile_id = build_engine(bundle, causal_value)
    checkpoint(
        "engine",
        engine=engine,
        causal_model=causal_model,
        mechanic_profile_id=profile_id,
    )
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
        checkpoint("engine", engine=engine, causal_model=causal_model)
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
    checkpoint("engine", engine=engine, causal_model=causal_model)
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
    checkpoint("engine", engine=engine, causal_model=causal_model)
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
        checkpoint("engine", engine=engine, causal_model=causal_model)
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
    checkpoint("engine", engine=engine, causal_model=causal_model)

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
    checkpoint("projection", engine=engine, causal_model=causal_model)
    projection = build_live_projection(
        initial_snapshot=engine.initial_snapshot(),
        events=engine.world.events,
        scene={
            "kind": "automatic-living-scene-v1",
            "source": "structured-native-coordination",
        },
        branch_id=f"{bundle['world']['id']}-deterministic",
    )
    checkpoint("projection", engine=engine, causal_model=causal_model, projection=projection)
    checkpoint("renderer", projection=projection)
    profile, frames, html = _living_ui(bundle, projection)
    checkpoint(
        "renderer",
        projection=projection,
        profile=profile,
        frames=frames,
        html=html,
    )
    checkpoint("complete", engine=engine, causal_model=causal_model, projection=projection)
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
    parser.add_argument("--acceptance", type=Path, default=DEFAULT_ACCEPTANCE)
    parser.add_argument("--diagnostic-dir", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--trace-output", type=Path)
    parser.add_argument("--projection-output", type=Path)
    parser.add_argument("--profile-output", type=Path)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args()

    if args.diagnostic_dir is not None:
        args.diagnostic_dir.mkdir(parents=True, exist_ok=True)
        fallback_run_id = args.run_id or f"native-coordination/input/{uuid.uuid4().hex}"
        raw_inputs = {
            "input-bundle.raw": args.bundle,
            "causal-model.raw": args.causal_model,
            "acceptance-matrix.raw": args.acceptance,
        }
        for name, source in raw_inputs.items():
            try:
                _write_text(args.diagnostic_dir / name, source.read_text())
            except OSError:
                pass
        try:
            bundle = load_bundle(args.bundle)
            causal_value = json.loads(args.causal_model.read_text())
            acceptance = load_acceptance(args.acceptance)
        except Exception as error:
            summary = {
                "schema_version": DIAGNOSTIC_SCHEMA,
                "run_id": fallback_run_id,
                "world_id": None,
                "stage": "input",
                "status": "failed",
                "failure_category": "input",
                "provider_spend_usd": None,
                "mechanic_profile_id": None,
                "terminal_reached": None,
                "event_count": None,
                "projection_final_hash": None,
                "acceptance_passed": None,
                "error": {
                    "type": type(error).__name__,
                    "message": str(error),
                },
            }
            _write_json(args.diagnostic_dir / "summary.json", summary)
            _write_manifest(args.diagnostic_dir, fallback_run_id)
            print(json.dumps(summary, sort_keys=True))
            return 2
        summary = run_diagnostic(
            bundle,
            causal_value,
            acceptance=acceptance,
            output_dir=args.diagnostic_dir,
            run_id=args.run_id,
        )
        print(json.dumps(summary, sort_keys=True))
        return 0 if summary["status"] == "passed" else 2

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
            _write_json(path, value)
    if args.html_output is not None:
        _write_text(args.html_output, result["html"])
    print(json.dumps(result["trace"]["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
