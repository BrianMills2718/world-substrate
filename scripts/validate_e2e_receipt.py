#!/usr/bin/env python3
"""Validate the complete local EndToEndObservationV1 contract and claim gate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

IDENTIFIER = re.compile(r"^[a-z][a-z0-9_-]*$")
OBSERVATION_ID = re.compile(r"^E2E-[A-Za-z0-9._-]+$")
CLAIM_ID = re.compile(r"^CLAIM-[A-Za-z0-9._-]+$")


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _timestamp(value: object, path: str, errors: list[str]) -> datetime | None:
    if not _nonempty(value):
        errors.append(f"{path} must be a date-time string")
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path} must be a valid date-time")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{path} must include a timezone")
        return None
    return parsed


def _object(
    value: object,
    path: str,
    *,
    required: set[str],
    optional: set[str] | frozenset[str] = frozenset(),
    errors: list[str],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return None
    missing = sorted(required - set(value))
    unknown = sorted(set(value) - required - optional)
    if missing:
        errors.append(f"{path} missing required fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"{path} contains unknown fields: {', '.join(unknown)}")
    return value


def _string_fields(
    value: dict[str, Any], fields: set[str], path: str, errors: list[str]
) -> None:
    for field in fields:
        if field in value and not _nonempty(value[field]):
            errors.append(f"{path}.{field} must be a nonempty string")


def _string_array(
    value: object,
    path: str,
    errors: list[str],
    *,
    minimum: int = 0,
    unique: bool = False,
) -> list[str] | None:
    if not isinstance(value, list) or len(value) < minimum or any(
        not _nonempty(item) for item in value
    ):
        errors.append(f"{path} must be an array of nonempty strings")
        return None
    if unique and len(value) != len(set(value)):
        errors.append(f"{path} values must be unique")
    return value


def _validate_grounded_answer(
    grounding_value: object,
    *,
    status: object,
    required_surfaces: set[str],
    observations: list[dict[str, Any]],
    errors: list[str],
) -> None:
    grounding = _object(
        grounding_value,
        "grounded_answer",
        required={"answer_ref", "material_claims"},
        optional={
            "complete_trace_ref",
            "trace_inspected_at",
            "trace_inspection_summary",
            "inspected_tool_event_refs",
        },
        errors=errors,
    )
    if grounding is None:
        return
    _string_fields(grounding, {"answer_ref"}, "grounded_answer", errors)
    trace_fields = {
        "complete_trace_ref",
        "trace_inspected_at",
        "trace_inspection_summary",
        "inspected_tool_event_refs",
    }
    present_trace_fields = trace_fields & set(grounding)
    if present_trace_fields and present_trace_fields != trace_fields:
        errors.append("grounded_answer complete-trace fields must appear together")
    if "complete_trace_ref" in grounding:
        _string_fields(
            grounding,
            {"complete_trace_ref", "trace_inspection_summary"},
            "grounded_answer",
            errors,
        )
        _timestamp(grounding.get("trace_inspected_at"), "grounded_answer.trace_inspected_at", errors)
        _string_array(
            grounding.get("inspected_tool_event_refs"),
            "grounded_answer.inspected_tool_event_refs",
            errors,
            minimum=1,
            unique=True,
        )

    claims_value = grounding.get("material_claims")
    if not isinstance(claims_value, list) or not claims_value:
        errors.append("grounded_answer.material_claims must be a nonempty array")
        claims: list[dict[str, Any]] = []
    else:
        claims = []
        for index, item in enumerate(claims_value):
            claim = _object(
                item,
                f"grounded_answer.material_claims[{index}]",
                required={
                    "claim_id",
                    "claim",
                    "tool_event_refs",
                    "source_ref",
                    "source_reopened",
                    "support_status",
                    "inspection",
                },
                errors=errors,
            )
            if claim is None:
                continue
            claims.append(claim)
            _string_fields(
                claim,
                {"claim_id", "claim", "source_ref", "inspection"},
                f"grounded_answer.material_claims[{index}]",
                errors,
            )
            if _nonempty(claim.get("claim_id")) and not CLAIM_ID.fullmatch(
                claim["claim_id"]
            ):
                errors.append(f"material claim {index} has an invalid claim_id")
            _string_array(
                claim.get("tool_event_refs"),
                f"grounded_answer.material_claims[{index}].tool_event_refs",
                errors,
                unique=True,
            )
            if type(claim.get("source_reopened")) is not bool:
                errors.append(f"material claim {index} source_reopened must be boolean")
            if claim.get("support_status") not in {"supported", "contradicted", "unclear"}:
                errors.append(f"material claim {index} has invalid support_status")
        claim_ids = [item.get("claim_id") for item in claims]
        if len(claim_ids) != len(set(claim_ids)):
            errors.append("grounded_answer material claim IDs must be unique")

    for surface in {"llm_trace", "source_reopen"} - required_surfaces:
        errors.append(f"grounded_llm_answer requires the {surface!r} surface")
    if status == "pass":
        if present_trace_fields != trace_fields:
            errors.append("passing grounded answer requires complete-trace fields")
        trace_refs = {
            item.get("evidence_ref")
            for item in observations
            if item.get("surface") == "llm_trace" and item.get("status") == "observed"
        }
        if grounding.get("complete_trace_ref") not in trace_refs:
            errors.append("complete_trace_ref must match the observed llm_trace surface")
        inspected = set(grounding.get("inspected_tool_event_refs", []))
        mapped = {
            event_ref
            for item in claims
            for event_ref in item.get("tool_event_refs", [])
        }
        if mapped - inspected:
            errors.append("material claim events must be present in the inspected trace")
        if any(
            not item.get("tool_event_refs")
            or item.get("source_reopened") is not True
            or item.get("support_status") != "supported"
            for item in claims
        ):
            errors.append("passing grounded answer requires every material claim to be supported")


def validate_receipt(value: object) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "record_type",
        "observation_id",
        "criterion_id",
        "status",
        "scope",
        "observed_at",
        "producer",
        "source_revision",
        "execution_context",
        "test_selection",
        "journey",
        "required_surfaces",
        "surface_observations",
        "unexpected_events",
        "outcome_kind",
        "outcome",
        "limitations",
    }
    record = _object(
        value,
        "receipt",
        required=required,
        optional={"grounded_answer"},
        errors=errors,
    )
    if record is None:
        return errors
    if record.get("schema_version") != "1.0":
        errors.append("schema_version must be '1.0'")
    if record.get("record_type") != "end_to_end_observation":
        errors.append("record_type must be 'end_to_end_observation'")
    _string_fields(
        record,
        {"observation_id", "criterion_id", "scope", "producer", "source_revision"},
        "receipt",
        errors,
    )
    if _nonempty(record.get("observation_id")) and not OBSERVATION_ID.fullmatch(
        record["observation_id"]
    ):
        errors.append("observation_id has an invalid format")
    if _nonempty(record.get("source_revision")) and len(record["source_revision"]) < 7:
        errors.append("source_revision must contain at least seven characters")
    if record.get("status") not in {"pass", "fail", "inconclusive"}:
        errors.append("status must be pass, fail, or inconclusive")
    observed_at = _timestamp(record.get("observed_at"), "observed_at", errors)

    context = _object(
        record.get("execution_context"),
        "execution_context",
        required={"target", "configuration_ref", "dependency_set_ref", "route"},
        errors=errors,
    )
    if context is not None:
        _string_fields(context, set(context), "execution_context", errors)

    selection = _object(
        record.get("test_selection"),
        "test_selection",
        required={
            "criterion_id",
            "changed_boundary",
            "failure_hypothesis",
            "discriminating_probe",
            "decision_if_pass",
            "decision_if_fail",
        },
        errors=errors,
    )
    if selection is not None:
        _string_fields(selection, set(selection), "test_selection", errors)
        if selection.get("criterion_id") != record.get("criterion_id"):
            errors.append("test_selection.criterion_id must match criterion_id")
        pass_action = " ".join(str(selection.get("decision_if_pass", "")).split()).casefold()
        fail_action = " ".join(str(selection.get("decision_if_fail", "")).split()).casefold()
        if pass_action == fail_action:
            errors.append("decision_if_pass and decision_if_fail must differ")

    journey = _object(
        record.get("journey"),
        "journey",
        required={"starting_state", "input", "steps", "correlation_id", "observation_window"},
        errors=errors,
    )
    if journey is not None:
        _string_fields(journey, {"starting_state", "input", "correlation_id"}, "journey", errors)
        _string_array(journey.get("steps"), "journey.steps", errors, minimum=1)
        window = _object(
            journey.get("observation_window"),
            "journey.observation_window",
            required={"started_at", "ended_at"},
            errors=errors,
        )
        if window is not None:
            started = _timestamp(window.get("started_at"), "journey.observation_window.started_at", errors)
            ended = _timestamp(window.get("ended_at"), "journey.observation_window.ended_at", errors)
            if started is not None and ended is not None and ended < started:
                errors.append("journey observation window ends before it starts")
            if observed_at is not None and ended is not None and observed_at < ended:
                errors.append("observed_at cannot precede the observation window end")

    surfaces = _string_array(
        record.get("required_surfaces"),
        "required_surfaces",
        errors,
        minimum=1,
        unique=True,
    ) or []
    if any(not IDENTIFIER.fullmatch(item) for item in surfaces):
        errors.append("required_surfaces contain an invalid identifier")
    required_surfaces = set(surfaces)

    observations_value = record.get("surface_observations")
    observations: list[dict[str, Any]] = []
    if not isinstance(observations_value, list) or not observations_value:
        errors.append("surface_observations must be a nonempty array")
    else:
        for index, item in enumerate(observations_value):
            observation = _object(
                item,
                f"surface_observations[{index}]",
                required={"surface", "status"},
                optional={"evidence_ref", "inspected_at", "observation", "limitation"},
                errors=errors,
            )
            if observation is None:
                continue
            observations.append(observation)
            surface = observation.get("surface")
            if not isinstance(surface, str) or not IDENTIFIER.fullmatch(surface):
                errors.append(f"surface_observations[{index}].surface is invalid")
            status = observation.get("status")
            if status not in {"observed", "missing", "unavailable"}:
                errors.append(f"surface_observations[{index}].status is invalid")
            if status == "observed":
                _string_fields(
                    observation,
                    {"evidence_ref", "observation"},
                    f"surface_observations[{index}]",
                    errors,
                )
                if "evidence_ref" not in observation or "observation" not in observation:
                    errors.append(f"observed surface {surface!r} lacks evidence")
                _timestamp(observation.get("inspected_at"), f"surface_observations[{index}].inspected_at", errors)
                if "limitation" in observation:
                    errors.append(f"observed surface {surface!r} cannot retain a limitation")
            else:
                if not _nonempty(observation.get("limitation")):
                    errors.append(f"unobserved surface {surface!r} requires a limitation")
                if {"evidence_ref", "inspected_at", "observation"} & set(observation):
                    errors.append(f"unobserved surface {surface!r} cannot claim evidence")
    observed_names = [item.get("surface") for item in observations]
    if len(observed_names) != len(set(observed_names)):
        errors.append("surface_observations must name each surface exactly once")
    observed_set = set(observed_names)
    if required_surfaces - observed_set:
        errors.append("surface_observations omit required surfaces")
    if observed_set - required_surfaces:
        errors.append("surface_observations contain undeclared surfaces")
    unavailable = [
        item.get("surface") for item in observations if item.get("status") != "observed"
    ]
    if unavailable and record.get("status") != "inconclusive":
        errors.append("missing or unavailable surfaces require status=inconclusive")

    events_value = record.get("unexpected_events")
    events: list[dict[str, Any]] = []
    if not isinstance(events_value, list):
        errors.append("unexpected_events must be an array")
    else:
        for index, item in enumerate(events_value):
            event = _object(
                item,
                f"unexpected_events[{index}]",
                required={"event_ref", "disposition", "explanation"},
                errors=errors,
            )
            if event is None:
                continue
            events.append(event)
            _string_fields(event, {"event_ref", "explanation"}, f"unexpected_events[{index}]", errors)
            if event.get("disposition") not in {"expected", "explained", "defect", "unresolved"}:
                errors.append(f"unexpected_events[{index}].disposition is invalid")
    if any(item.get("disposition") == "unresolved" for item in events) and record.get("status") != "inconclusive":
        errors.append("unresolved events require status=inconclusive")
    if record.get("status") == "pass" and any(
        item.get("disposition") == "defect" for item in events
    ):
        errors.append("status=pass cannot retain defect events")

    outcome_kind = record.get("outcome_kind")
    if outcome_kind not in {"system_behavior", "grounded_llm_answer"}:
        errors.append("outcome_kind is invalid")
    outcome = _object(
        record.get("outcome"),
        "outcome",
        required={"observed_result", "state_change", "evidence_ref"},
        errors=errors,
    )
    if outcome is not None:
        _string_fields(outcome, set(outcome), "outcome", errors)

    limitations = _string_array(record.get("limitations"), "limitations", errors) or []
    if record.get("status") == "inconclusive" and not limitations:
        errors.append("status=inconclusive requires at least one limitation")

    if outcome_kind == "grounded_llm_answer":
        if "grounded_answer" not in record:
            errors.append("grounded_llm_answer requires grounded_answer")
        else:
            _validate_grounded_answer(
                record["grounded_answer"],
                status=record.get("status"),
                required_surfaces=required_surfaces,
                observations=observations,
                errors=errors,
            )
    elif "grounded_answer" in record:
        errors.append("system_behavior cannot include grounded_answer")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument(
        "--claim-kind",
        choices=("ordinary_completion", "human_handoff", "maturity_promotion", "release_decision", "central_llm_result"),
        default="ordinary_completion",
    )
    args = parser.parse_args()
    try:
        payload = json.loads(args.receipt.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid end-to-end observation input: {exc}", file=sys.stderr)
        return 2
    errors = validate_receipt(payload)
    if args.claim_kind != "ordinary_completion" and isinstance(payload, dict) and payload.get("status") != "pass":
        errors.append(f"{args.claim_kind} requires status=pass")
    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        return 1
    assert isinstance(payload, dict)
    print(f"valid {args.claim_kind} evidence claim: {payload['observation_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
