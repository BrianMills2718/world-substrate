#!/usr/bin/env python3
"""Server-authoritative supported comparison mutations for native coordination."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from scripts.scaffold_world import validate_bundle


def _gate(bundle: dict[str, Any]) -> dict[str, Any]:
    rows = [
        row
        for row in bundle["entities"]
        if "gate" in row.get("categories", [])
        and "gate" in (row.get("components") or {})
    ]
    if len(rows) != 1:
        raise ValueError(f"native coordination comparison requires exactly one gate, got {len(rows)}")
    return rows[0]


def _informed_recipient_count(bundle: dict[str, Any]) -> int:
    recipients = {
        row["components"]["delivery"]["recipient_id"]
        for row in bundle["entities"]
        if "delivery" in (row.get("components") or {})
    }
    return len(recipients)


def with_approval_threshold(
    baseline_bundle: dict[str, Any],
    required_approvals: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Clone a validated baseline and change only gate.required_approvals."""

    baseline = validate_bundle(baseline_bundle)
    if type(required_approvals) is not int:
        raise ValueError("required_approvals must be an integer")

    baseline_gate = _gate(baseline)
    before = baseline_gate["components"]["gate"]["required_approvals"]
    max_approvals = _informed_recipient_count(baseline)
    if max_approvals < 2:
        raise ValueError("comparison requires at least two represented informed recipients")
    if not 1 <= required_approvals <= max_approvals:
        raise ValueError(
            f"required_approvals must be between 1 and {max_approvals}"
        )
    if required_approvals == before:
        raise ValueError("comparison approval threshold must differ from baseline")

    comparison = deepcopy(baseline)
    comparison_gate = _gate(comparison)
    comparison_gate["components"]["gate"]["required_approvals"] = required_approvals
    comparison = validate_bundle(comparison)

    return comparison, {
        "schema_version": "world-substrate-native-coordination-comparison-change/v0",
        "path": f"entities.{comparison_gate['id']}.components.gate.required_approvals",
        "before": before,
        "after": required_approvals,
        "max_supported": max_approvals,
    }
