"""Bounded declared-dependency mapping for the Waltzman showcase scenario."""

from __future__ import annotations

from typing import Any

from world_substrate.rules import RuleRegistry

ADEQUACY_SCHEMA_VERSION = "world-substrate-causal-adequacy-report/v0"


def build_adequacy_report(registry: RuleRegistry) -> dict[str, Any]:
    """Map declared consequential assumptions to installed enforcement surfaces.

    Mapping says the named enforcing rule IDs are installed. It is not a
    counterfactual proof of necessity/sufficiency or a real-world validity claim.
    """

    installed = set(registry.versions())
    dependencies = [
        {
            "id": "validation-capacity-binds-mara",
            "claim": "Loss of validation capacity can make Mara's explicit commitment conditional.",
            "represented_by": ["validation-capacity.resource", "mara.commitment"],
            "enforced_by": ["waltzman.process.validation-failure", "waltzman.commitment.reassess"],
        },
        {
            "id": "staffing-binds-tomas",
            "claim": "A staffing shortfall can make Tomas's explicit commitment conditional.",
            "represented_by": ["clinical-staff.resource", "tomas.commitment"],
            "enforced_by": ["waltzman.process.staffing-shortfall", "waltzman.commitment.reassess"],
        },
        {
            "id": "reserve-binds-nira",
            "claim": "The shared reserve constraint can make Nira's explicit commitment conditional.",
            "represented_by": ["shared-reserve.resource", "nira.commitment"],
            "enforced_by": ["waltzman.process.reserve-conflict", "waltzman.commitment.reassess"],
        },
        {
            "id": "safeguard-binds-idris",
            "claim": "A missing safeguard can make Idris's explicit commitment conditional.",
            "represented_by": ["safeguard-record.constraint", "idris.commitment"],
            "enforced_by": ["waltzman.process.safeguard-gap", "waltzman.commitment.reassess"],
        },
        {
            "id": "asymmetric-information-delivery",
            "claim": "A represented message is visible to its source/recipient after delivery without becoming universal knowledge.",
            "represented_by": ["information", "delivery"],
            "enforced_by": ["waltzman.information.communicate"],
            "substrate_enforcement": ["world_substrate.information.entity_visible_to_actor"],
        },
        {
            "id": "meeting-duration-before-decision",
            "claim": "The coalition gate evaluates only after the represented meeting completes.",
            "represented_by": ["coordination-meeting.activity", "coalition-hub.institution"],
            "enforced_by": ["waltzman.activity.start-meeting", "waltzman.process.meeting-completion", "waltzman.institution.coalition-gate"],
        },
        {
            "id": "coalition-gate-consumes-commitments",
            "claim": "Coalition readiness is computed from represented explicit commitments rather than narration.",
            "represented_by": ["*.commitment", "coalition-hub.institution"],
            "enforced_by": ["waltzman.institution.coalition-gate"],
        },
        {
            "id": "stabilization-intervention",
            "claim": "The intervention changes represented prerequisites, after which residents must separately reassess before the gate can recover.",
            "represented_by": ["stabilization-package.package", "four prerequisite entities", "resident commitments"],
            "enforced_by": ["waltzman.intervention.deliver-package", "waltzman.commitment.reassess", "waltzman.institution.coalition-gate"],
        },
    ]
    for dependency in dependencies:
        required = set(dependency["enforced_by"])
        mapped = required <= installed
        dependency["mapping_status"] = "mapped" if mapped else "unmapped"
        # Retained for compatibility with the v0 evidence schema. New UI/docs use
        # mapping_status because installation mapping is the claim actually tested.
        dependency["status"] = "enforced" if mapped else "gap"
        dependency["missing_enforcement"] = sorted(required - installed)
    return {
        "schema_version": ADEQUACY_SCHEMA_VERSION,
        "scope": "waltzman-coordination-lab-v0",
        "bounded": True,
        "global_completeness_claimed": False,
        "claim_level": "declared-dependency-mapping",
        "interpretation": (
            "Mapped means the declared enforcement rule IDs are installed for this scenario; "
            "it does not prove counterfactual necessity/sufficiency or real-world causal validity."
        ),
        "dependencies": dependencies,
        "summary": {
            "mapped": sum(row["mapping_status"] == "mapped" for row in dependencies),
            "unmapped": sum(row["mapping_status"] == "unmapped" for row in dependencies),
            # Legacy v0 names retained for compatibility.
            "enforced": sum(row["status"] == "enforced" for row in dependencies),
            "gaps": sum(row["status"] == "gap" for row in dependencies),
        },
        "residual_risk": [
            "Resident belief formation and psychological trust updates are not modeled as canonical mechanics.",
            "The communication channels do not yet model latency, corruption, deception detection, or probabilistic delivery.",
            "The coalition institution is intentionally simplified to explicit support/conditional commitments and one decision gate.",
            "The stabilization package is an explicit scenario intervention, not evidence that comparable real-world interventions would have the same effect.",
            "Predictive behavioral validity is outside the acceptance claim for this demo.",
        ],
    }
