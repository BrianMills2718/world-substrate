#!/usr/bin/env python3
"""Probe Jev as a non-cognitive typed estimator for World Substrate research.

This is deliberately outside the consequence engine. Jev receives bounded
maintenance evidence and returns typed probabilities; no answer mutates world
state or bypasses installed mechanics.

OpenRouter exposes Jev through its Decisions API, not chat completions:
    POST https://openrouter.ai/api/alpha/decisions

The script reuses llm_client's OpenRouter account/key resolution so experimental
spend follows the same billing-account policy as the rest of this repository.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

DEFAULT_MODEL = "typesafe/jev-1.13"
ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_OUTPUT = REPO / "evidence/jev/maintenance-estimator-probe-v0.json"

QUESTIONS: dict[str, Any] = {
    "failure_mode": {
        "type": "choice",
        "instructions": (
            "Which failure mode best explains the maintenance evidence? Choose "
            "the most likely primary diagnosis, not every plausible contributor."
        ),
        "criteria": {
            "bearing_wear": "Mechanical bearing wear or seizure.",
            "shaft_misalignment": "Rotating shaft or coupling misalignment.",
            "coolant_loss": "Cooling-fluid loss or inadequate cooling flow.",
            "sensor_fault": "The apparent problem is primarily a faulty sensor or instrumentation.",
            "electrical_fault": "Electrical supply, motor, wiring, or control-electronics fault.",
        },
    },
    "shutdown_required": {
        "type": "noul",
        "instructions": (
            "Should this machine be taken out of service immediately based only "
            "on the supplied evidence?"
        ),
        "criteria": {
            "true": "Continuing operation presents a meaningful immediate damage or safety risk.",
            "false": "The evidence supports continued monitored operation or routine maintenance.",
        },
    },
    "severity": {
        "type": "score",
        "instructions": "How severe is the likely equipment condition?",
        "criteria": [
            "Minor: routine monitoring or maintenance is sufficient.",
            "Moderate: maintenance should be scheduled soon.",
            "Serious: prompt intervention is warranted.",
            "Critical: immediate shutdown or emergency intervention is warranted.",
        ],
    },
}

CASES: list[dict[str, Any]] = [
    {
        "id": "misalignment-01",
        "state": {
            "machine": "centrifugal pump",
            "telemetry": {
                "vibration": "high axial vibration, strongest at 1x shaft speed",
                "temperature": "normal",
                "motor_current": "normal",
            },
            "maintenance_note": (
                "Vibration increased immediately after coupling replacement. "
                "Operator reports a new lateral wobble. No leakage or overheating."
            ),
        },
        "expected_failure_mode": "shaft_misalignment",
        "expected_shutdown_required": True,
    },
    {
        "id": "bearing-01",
        "state": {
            "machine": "conveyor drive",
            "telemetry": {
                "vibration": "broadband vibration rising over three weeks",
                "temperature": "bearing housing 18 C above baseline",
                "motor_current": "slightly elevated",
            },
            "maintenance_note": (
                "Grinding noise under load. Grease contains fine metallic debris. "
                "Alignment check last week was within tolerance."
            ),
        },
        "expected_failure_mode": "bearing_wear",
        "expected_shutdown_required": True,
    },
    {
        "id": "coolant-01",
        "state": {
            "machine": "CNC spindle",
            "telemetry": {
                "temperature": "rapidly rising under normal load",
                "coolant_flow": "near zero",
                "vibration": "normal",
            },
            "maintenance_note": (
                "Coolant reservoir is unexpectedly low and a wet patch is visible "
                "under the return hose. Spindle sounds normal."
            ),
        },
        "expected_failure_mode": "coolant_loss",
        "expected_shutdown_required": True,
    },
    {
        "id": "sensor-01",
        "state": {
            "machine": "air compressor",
            "telemetry": {
                "pressure_sensor": "jumps between 2 and 14 bar within one second",
                "backup_gauge": "steady at 7.1 bar",
                "temperature": "normal",
                "vibration": "normal",
            },
            "maintenance_note": (
                "No audible cycling or process change corresponds to the pressure "
                "spikes. Connector was recently exposed to washdown."
            ),
        },
        "expected_failure_mode": "sensor_fault",
        "expected_shutdown_required": False,
    },
    {
        "id": "electrical-01",
        "state": {
            "machine": "exhaust fan",
            "telemetry": {
                "motor_current": "intermittently drops to zero",
                "vibration": "normal while energized",
                "temperature": "normal",
            },
            "maintenance_note": (
                "Fan stops randomly and restarts when the control cabinet is tapped. "
                "Terminal block shows discoloration around one loose connection."
            ),
        },
        "expected_failure_mode": "electrical_fault",
        "expected_shutdown_required": True,
    },
]


def build_request(case: dict[str, Any], model: str = DEFAULT_MODEL) -> dict[str, Any]:
    """Build the exact Decisions API payload for one benchmark case."""
    return {
        "model": model,
        "state": case["state"],
        "questions": QUESTIONS,
    }


def _resolve_openrouter_key() -> str:
    """Use llm_client's account-aware OpenRouter key resolution.

    The helper is private because llm_client has not yet exposed the Decisions
    API as a first-class transport. This research-only probe keeps the exception
    local and obvious instead of adding a provider client to runtime code.
    """
    from llm_client.utils.openrouter import _openrouter_key_candidates_from_env

    candidates = _openrouter_key_candidates_from_env()
    if not candidates:
        raise RuntimeError(
            "No OpenRouter credential is configured through llm_client's supported "
            "environment/account routing."
        )
    return candidates[0]


def call_jev(
    case: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    timeout_seconds: float = 30.0,
) -> dict[str, Any]:
    """Run one live Jev Decisions request and return response plus timing."""
    payload = build_request(case, model=model)
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {_resolve_openrouter_key()}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": "World Substrate Jev research probe",
        },
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8")
            status = response.status
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter Decisions API HTTP {exc.code}: {detail}") from exc
    elapsed_ms = round((time.perf_counter() - started) * 1000.0, 3)
    parsed = json.loads(body)
    if not isinstance(parsed, dict) or not isinstance(parsed.get("answers"), dict):
        raise RuntimeError("OpenRouter Decisions API response is missing an answers object")
    return {
        "http_status": status,
        "latency_ms": elapsed_ms,
        "response": parsed,
    }


def grade_case(case: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    """Grade only the bounded labels fixed before the request."""
    answers = response["answers"]
    failure = answers.get("failure_mode") or {}
    shutdown = answers.get("shutdown_required") or {}
    predicted_mode = failure.get("choice")
    shutdown_p = shutdown.get("noul")
    predicted_shutdown = (
        bool(float(shutdown_p) >= 0.5)
        if isinstance(shutdown_p, (int, float))
        else None
    )
    return {
        "failure_mode_correct": predicted_mode == case["expected_failure_mode"],
        "shutdown_correct": predicted_shutdown == case["expected_shutdown_required"],
        "predicted_failure_mode": predicted_mode,
        "predicted_shutdown_required": predicted_shutdown,
        "shutdown_probability": shutdown_p,
        "failure_mode_probabilities": failure.get("probabilities"),
        "severity": (answers.get("severity") or {}).get("score"),
    }


def run_live(model: str, selected_case: str | None) -> dict[str, Any]:
    chosen = [case for case in CASES if selected_case in {None, case["id"]}]
    if selected_case and not chosen:
        raise ValueError(f"unknown case id: {selected_case}")

    trace_id = f"world-substrate-jev-{uuid.uuid4().hex[:10]}"
    rows: list[dict[str, Any]] = []
    for case in chosen:
        result = call_jev(case, model=model)
        response = result["response"]
        rows.append(
            {
                "case_id": case["id"],
                "expected": {
                    "failure_mode": case["expected_failure_mode"],
                    "shutdown_required": case["expected_shutdown_required"],
                },
                "grade": grade_case(case, response),
                "latency_ms": result["latency_ms"],
                "model_returned": response.get("model"),
                "usage": response.get("usage"),
                "answers": response.get("answers"),
            }
        )

    mode_correct = sum(bool(row["grade"]["failure_mode_correct"]) for row in rows)
    shutdown_correct = sum(bool(row["grade"]["shutdown_correct"]) for row in rows)
    latencies = [float(row["latency_ms"]) for row in rows]
    return {
        "schema_version": "world-substrate-jev-estimator-probe/v0",
        "status": "live",
        "trace_id": trace_id,
        "endpoint": ENDPOINT,
        "requested_model": model,
        "claim_boundary": (
            "Jev performs typed non-cognitive estimation only. These answers do not "
            "mutate canonical state and are not World Substrate consequence authority."
        ),
        "cases": rows,
        "summary": {
            "cases": len(rows),
            "failure_mode_accuracy": mode_correct / len(rows) if rows else None,
            "shutdown_accuracy": shutdown_correct / len(rows) if rows else None,
            "mean_latency_ms": sum(latencies) / len(latencies) if latencies else None,
        },
    }


def dry_run(model: str, selected_case: str | None) -> dict[str, Any]:
    chosen = [case for case in CASES if selected_case in {None, case["id"]}]
    if selected_case and not chosen:
        raise ValueError(f"unknown case id: {selected_case}")
    return {
        "schema_version": "world-substrate-jev-estimator-probe/v0",
        "status": "dry-run",
        "endpoint": ENDPOINT,
        "requested_model": model,
        "requests": [
            {
                "case_id": case["id"],
                "expected": {
                    "failure_mode": case["expected_failure_mode"],
                    "shutdown_required": case["expected_shutdown_required"],
                },
                "payload": build_request(case, model=model),
            }
            for case in chosen
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--case", help="run one case id instead of the full fixture")
    parser.add_argument(
        "--live",
        action="store_true",
        help="spend against OpenRouter; without this flag only print request payloads",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    payload = (
        run_live(args.model, args.case)
        if args.live
        else dry_run(args.model, args.case)
    )
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(f"wrote {args.output.relative_to(REPO)}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
