"""Detachable Waltzman-style analysis over material projection data.

These values are observer-side heuristics. They never enter canonical world
state, never change affordances, and never become primitive causal parents.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from world_substrate.projection import apply_changes

ANALYSIS_SCHEMA_VERSION = "world-substrate-waltzman-analysis/v0"

_CONSTRAINT_IDS = (
    "validation-capacity",
    "clinical-staff",
    "shared-reserve",
    "safeguard-record",
)


def _components(material: dict[str, Any], entity_id: str) -> dict[str, Any]:
    record = material["entities"][entity_id]
    value = record.get("components", {})
    return value if isinstance(value, dict) else {}


def _satisfied(material: dict[str, Any], entity_id: str) -> bool:
    components = _components(material, entity_id)
    resource = components.get("resource")
    if isinstance(resource, dict):
        return int(resource["current"]) >= int(resource["required"])
    constraint = components.get("constraint")
    if isinstance(constraint, dict):
        return constraint.get("status") == constraint.get("required_status")
    return False


def analyze_material(material: dict[str, Any]) -> dict[str, Any]:
    """Return an observer-only Waltzman analysis for one material state."""

    unsatisfied = [entity_id for entity_id in _CONSTRAINT_IDS if not _satisfied(material, entity_id)]
    institution = _components(material, "coalition-hub")["institution"]
    commitments = [
        components["commitment"]["stance"]
        for record in material["entities"].values()
        if isinstance((components := record.get("components")), dict)
        and isinstance(components.get("commitment"), dict)
    ]
    utterances = [
        record
        for record in material["entities"].values()
        if "utterance" in record.get("category_ids", [])
        and isinstance(record.get("components", {}).get("information"), dict)
        and record["components"]["information"].get("active") is True
    ]
    total_commitments = max(1, len(commitments))
    support = sum(stance == "support" for stance in commitments)
    trust_proxy = round(min(1.0, len(utterances) / 4), 3)
    risk = round(len(unsatisfied) / len(_CONSTRAINT_IDS), 3)
    readiness = round(support / total_commitments, 3)
    return {
        "schema_version": ANALYSIS_SCHEMA_VERSION,
        "layer": "detachable-analysis",
        "causal": False,
        "tick": material["tick"],
        "trust_proxy": trust_proxy,
        "perceived_risk_proxy": risk,
        "coordination_readiness_proxy": readiness,
        "institution_status": institution["status"],
        "unsatisfied_constraints": unsatisfied,
        "assumptions": [
            "trust_proxy is represented utterance coverage, not a latent psychological state",
            "risk proxy is the fraction of the four demo prerequisites currently unsatisfied",
            "readiness proxy is the fraction of explicit resident commitments currently supporting",
            "these values are interpretations and do not affect the run",
        ],
    }


def analysis_series(initial_snapshot: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Compute detachable analysis for initial state and every retained event."""

    material = deepcopy(initial_snapshot["world"])
    rows: dict[str, dict[str, Any]] = {"initial": analyze_material(material)}
    for event in events:
        apply_changes(material, event["changes"])
        rows[event["event_id"]] = analyze_material(material)
    return rows
