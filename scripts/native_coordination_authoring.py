#!/usr/bin/env python3
"""One-shot natural-language authoring for the bounded native coordination family.

The model proposes *configuration*, requirements, and assumptions only. It does
not author executable law. A deterministic compiler turns the reviewed draft
into the existing World Substrate authoring bundle, and the shared reviewed
coordination causal model remains the only executable mechanics family.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.scaffold_world import validate_bundle
from world_substrate.action_authoring import CausalModel

DRAFT_SCHEMA_VERSION = "world-substrate-native-coordination-draft/v0"
PROPOSAL_SCHEMA_VERSION = "world-substrate-native-coordination-proposal/v0"
SUPPORTED_FAMILY = "bounded-coordination-v0"
DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
DEFAULT_BUDGET = 0.08
MAX_OUTPUT_TOKENS = 4096
DEFAULT_CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"

SURFACES = (
    "participants",
    "authorization",
    "resource_threshold",
    "approval_threshold",
    "information_delivery",
    "finalization",
    "unsupported",
)
SURFACE_RULES = {
    "participants": [],
    "authorization": ["coordination.action.intervene"],
    "resource_threshold": [
        "coordination.action.approve",
        "coordination.action.intervene",
        "coordination.action.finalize",
    ],
    "approval_threshold": [
        "coordination.action.approve",
        "coordination.action.finalize",
    ],
    "information_delivery": [
        "coordination.action.communicate",
        "coordination.action.approve",
    ],
    "finalization": ["coordination.action.finalize"],
    "unsupported": [],
}

_COMPONENTS = [
    {
        "name": "member",
        "fields": [
            {"name": "role", "type": "string", "default": "participant"},
            {"name": "authorized", "type": "boolean", "default": False},
            {"name": "approved", "type": "boolean", "default": False},
            {"name": "aware", "type": "boolean", "default": False},
        ],
    },
    {
        "name": "resource",
        "fields": [
            {"name": "current", "type": "integer", "default": 0},
            {"name": "required", "type": "integer", "default": 1},
            {"name": "unit", "type": "string", "default": "unit"},
        ],
    },
    {
        "name": "gate",
        "fields": [
            {"name": "status", "type": "string", "default": "blocked"},
            {"name": "approval_count", "type": "integer", "default": 0},
            {"name": "required_approvals", "type": "integer", "default": 1},
        ],
    },
    {
        "name": "information",
        "fields": [
            {"name": "content", "type": "string", "default": "report"},
            {"name": "source_id", "type": "entity_ref", "default": "placeholder"},
            {"name": "channel_id", "type": "string", "default": "brief"},
            {"name": "visibility", "type": "string", "default": "direct"},
            {"name": "topic", "type": "string", "default": "coordination"},
            {"name": "active", "type": "boolean", "default": False},
        ],
    },
    {
        "name": "delivery",
        "fields": [
            {"name": "info_id", "type": "entity_ref", "default": "placeholder"},
            {"name": "recipient_id", "type": "entity_ref", "default": "placeholder"},
            {"name": "channel_id", "type": "string", "default": "brief"},
            {"name": "status", "type": "string", "default": "pending"},
        ],
    },
]

_ACTIONS = [
    {
        "kind": "communicate",
        "description": "Deliver one represented information item to its declared recipient.",
        "fields": [
            {"name": "information", "type": "entity_ref"},
            {"name": "delivery", "type": "entity_ref"},
            {"name": "recipient", "type": "entity_ref"},
        ],
    },
    {
        "kind": "approve",
        "description": "Add one informed member approval when all represented prerequisites are healthy.",
        "fields": [
            {"name": "gate", "type": "entity_ref"},
            {"name": "prereq_a", "type": "entity_ref"},
            {"name": "prereq_b", "type": "entity_ref"},
            {"name": "prereq_c", "type": "entity_ref"},
            {"name": "prereq_d", "type": "entity_ref"},
        ],
    },
    {
        "kind": "intervene",
        "description": "Restore the one represented restorable prerequisite when authorized.",
        "fields": [{"name": "resource", "type": "entity_ref"}],
    },
    {
        "kind": "finalize",
        "description": "Mark the represented gate ready after threshold and prerequisite checks pass.",
        "fields": [
            {"name": "gate", "type": "entity_ref"},
            {"name": "prereq_a", "type": "entity_ref"},
            {"name": "prereq_b", "type": "entity_ref"},
            {"name": "prereq_c", "type": "entity_ref"},
            {"name": "prereq_d", "type": "entity_ref"},
        ],
    },
]

_PRESENTATION = {
    "assets": {
        "participant": {"kind": "emoji", "value": "👤"},
        "resource": {"kind": "emoji", "value": "📦"},
        "information": {"kind": "emoji", "value": "✉️"},
        "delivery": {"kind": "text", "value": "→"},
    },
    "category_assets": {
        "member": "participant",
        "resource": "resource",
        "information": "information",
        "delivery": "delivery",
    },
    "station_roles": {"gate": "goal"},
}


def proposal_schema() -> dict[str, Any]:
    member = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "label": {"type": "string", "minLength": 1},
            "role": {"type": "string", "minLength": 1},
            "authorized": {"type": "boolean"},
        },
        "required": ["id", "label", "role", "authorized"],
        "additionalProperties": False,
    }
    resource = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "label": {"type": "string", "minLength": 1},
            "current": {"type": "integer", "minimum": 0},
            "required": {"type": "integer", "minimum": 1},
            "unit": {"type": "string", "minLength": 1},
            "restorable": {"type": "boolean"},
        },
        "required": ["id", "label", "current", "required", "unit", "restorable"],
        "additionalProperties": False,
    }
    report = {
        "type": "object",
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
            "label": {"type": "string", "minLength": 1},
            "source_id": {"type": "string", "minLength": 1},
            "recipient_id": {"type": "string", "minLength": 1},
            "channel_id": {"type": "string", "minLength": 1},
            "topic": {"type": "string", "minLength": 1},
            "content": {"type": "string", "minLength": 1},
        },
        "required": [
            "id", "label", "source_id", "recipient_id",
            "channel_id", "topic", "content",
        ],
        "additionalProperties": False,
    }
    coverage = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "minLength": 1},
            "surface": {"enum": list(SURFACES)},
        },
        "required": ["text", "surface"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "schema_version": {"const": PROPOSAL_SCHEMA_VERSION},
            "world": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                    "label": {"type": "string", "minLength": 1},
                    "summary": {"type": "string", "minLength": 1},
                    "location": {"type": "string", "minLength": 1},
                },
                "required": ["id", "label", "summary", "location"],
                "additionalProperties": False,
            },
            "members": {
                "type": "array", "minItems": 3, "maxItems": 6, "items": member
            },
            "resources": {
                "type": "array", "minItems": 4, "maxItems": 4, "items": resource
            },
            "gate": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                    "label": {"type": "string", "minLength": 1},
                    "required_approvals": {"type": "integer", "minimum": 1, "maximum": 6},
                },
                "required": ["id", "label", "required_approvals"],
                "additionalProperties": False,
            },
            "reports": {
                "type": "array", "minItems": 1, "maxItems": 6, "items": report
            },
            "requirement_coverage": {
                "type": "array", "minItems": 1, "maxItems": 20, "items": coverage
            },
            "assumptions": {
                "type": "array", "maxItems": 12,
                "items": {"type": "string", "minLength": 1},
            },
            "unsupported_requests": {
                "type": "array", "maxItems": 12,
                "items": {"type": "string", "minLength": 1},
            },
        },
        "required": [
            "schema_version", "world", "members", "resources", "gate", "reports",
            "requirement_coverage", "assumptions", "unsupported_requests",
        ],
        "additionalProperties": False,
    }


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value.strip()


def _slug(value: object, label: str) -> str:
    value = _nonempty(value, label)
    if not re.fullmatch(r"[a-z][a-z0-9-]*", value):
        raise ValueError(f"{label} must be a lowercase slug")
    return value


def validate_native_coordination_draft(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError("native coordination draft must be an object")
    if value.get("schema_version") != DRAFT_SCHEMA_VERSION:
        raise ValueError(f"draft schema_version must be {DRAFT_SCHEMA_VERSION}")
    if value.get("family") != SUPPORTED_FAMILY:
        raise ValueError(f"draft family must be {SUPPORTED_FAMILY}")
    if value.get("draft_version") != 1:
        raise ValueError("draft_version must be 1")
    _nonempty(value.get("source_description"), "source_description")
    proposal = value.get("proposal")
    if not isinstance(proposal, dict) or proposal.get("schema_version") != PROPOSAL_SCHEMA_VERSION:
        raise ValueError("draft proposal has unsupported schema")

    world = proposal.get("world")
    if not isinstance(world, dict):
        raise ValueError("proposal.world must be an object")
    _slug(world.get("id"), "world.id")
    for key in ("label", "summary", "location"):
        _nonempty(world.get(key), f"world.{key}")

    members = proposal.get("members")
    if not isinstance(members, list) or not 3 <= len(members) <= 6:
        raise ValueError("proposal requires 3-6 members")
    member_ids: set[str] = set()
    authorized: list[str] = []
    for index, row in enumerate(members):
        if not isinstance(row, dict):
            raise ValueError(f"members[{index}] must be an object")
        member_id = _slug(row.get("id"), f"members[{index}].id")
        if member_id in member_ids:
            raise ValueError(f"duplicate member id: {member_id}")
        member_ids.add(member_id)
        _nonempty(row.get("label"), f"members[{index}].label")
        _nonempty(row.get("role"), f"members[{index}].role")
        if type(row.get("authorized")) is not bool:
            raise ValueError(f"members[{index}].authorized must be boolean")
        if row["authorized"]:
            authorized.append(member_id)
    if len(authorized) != 1:
        raise ValueError(f"exactly one member must be authorized; got {authorized}")

    resources = proposal.get("resources")
    if not isinstance(resources, list) or len(resources) != 4:
        raise ValueError("proposal requires exactly four resources/prerequisites")
    resource_ids: set[str] = set()
    restorable: list[str] = []
    for index, row in enumerate(resources):
        if not isinstance(row, dict):
            raise ValueError(f"resources[{index}] must be an object")
        resource_id = _slug(row.get("id"), f"resources[{index}].id")
        if resource_id in resource_ids or resource_id in member_ids:
            raise ValueError(f"duplicate entity id: {resource_id}")
        resource_ids.add(resource_id)
        _nonempty(row.get("label"), f"resources[{index}].label")
        _nonempty(row.get("unit"), f"resources[{index}].unit")
        current, required = row.get("current"), row.get("required")
        if type(current) is not int or current < 0:
            raise ValueError(f"resources[{index}].current must be a nonnegative integer")
        if type(required) is not int or required < 1:
            raise ValueError(f"resources[{index}].required must be a positive integer")
        if type(row.get("restorable")) is not bool:
            raise ValueError(f"resources[{index}].restorable must be boolean")
        if row["restorable"]:
            restorable.append(resource_id)
            if current >= required:
                raise ValueError("the restorable resource must begin below its requirement")
        elif current < required:
            raise ValueError("only the one restorable resource may begin below requirement")
    if len(restorable) != 1:
        raise ValueError(f"exactly one resource must be restorable; got {restorable}")

    gate = proposal.get("gate")
    if not isinstance(gate, dict):
        raise ValueError("proposal.gate must be an object")
    gate_id = _slug(gate.get("id"), "gate.id")
    if gate_id in member_ids or gate_id in resource_ids:
        raise ValueError(f"duplicate entity id: {gate_id}")
    _nonempty(gate.get("label"), "gate.label")
    threshold = gate.get("required_approvals")
    if type(threshold) is not int or threshold < 1 or threshold > len(members):
        raise ValueError("gate.required_approvals must fit the member count")

    reports = proposal.get("reports")
    if not isinstance(reports, list) or not reports:
        raise ValueError("proposal requires at least one represented report")
    report_ids: set[str] = set()
    recipients: list[str] = []
    for index, row in enumerate(reports):
        if not isinstance(row, dict):
            raise ValueError(f"reports[{index}] must be an object")
        report_id = _slug(row.get("id"), f"reports[{index}].id")
        if report_id in report_ids or report_id in member_ids or report_id in resource_ids or report_id == gate_id:
            raise ValueError(f"duplicate entity id: {report_id}")
        report_ids.add(report_id)
        for key in ("label", "channel_id", "topic", "content"):
            _nonempty(row.get(key), f"reports[{index}].{key}")
        source, recipient = row.get("source_id"), row.get("recipient_id")
        if source not in member_ids or recipient not in member_ids:
            raise ValueError(f"reports[{index}] source/recipient must name represented members")
        if source == recipient:
            raise ValueError(f"reports[{index}] source and recipient must differ")
        recipients.append(recipient)
    if len(set(recipients)) != len(recipients):
        raise ValueError("report recipients must be unique in this bounded family")
    if len(recipients) < threshold:
        raise ValueError("report recipients must cover the approval threshold")

    coverage = proposal.get("requirement_coverage")
    if not isinstance(coverage, list) or not coverage:
        raise ValueError("requirement_coverage must be a nonempty list")
    for index, row in enumerate(coverage):
        if not isinstance(row, dict):
            raise ValueError(f"requirement_coverage[{index}] must be an object")
        _nonempty(row.get("text"), f"requirement_coverage[{index}].text")
        if row.get("surface") not in SURFACES:
            raise ValueError(f"requirement_coverage[{index}].surface is unsupported")

    for key in ("assumptions", "unsupported_requests"):
        rows = proposal.get(key)
        if not isinstance(rows, list) or any(not isinstance(row, str) or not row.strip() for row in rows):
            raise ValueError(f"{key} must contain nonempty strings")

    return deepcopy(value)


def _resource_order(resources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    restorable = [row for row in resources if row["restorable"]]
    healthy = [row for row in resources if not row["restorable"]]
    return [*restorable, *healthy]


def draft_to_bundle(draft: dict[str, Any]) -> dict[str, Any]:
    draft = validate_native_coordination_draft(draft)
    proposal = draft["proposal"]
    entities: list[dict[str, Any]] = []

    for member in proposal["members"]:
        entities.append({
            "id": member["id"],
            "label": member["label"],
            "categories": ["member"],
            "components": {
                "member": {
                    "role": member["role"],
                    "authorized": member["authorized"],
                    "approved": False,
                    "aware": False,
                }
            },
        })

    letters = ("a", "b", "c", "d")
    for letter, resource in zip(letters, _resource_order(proposal["resources"]), strict=True):
        categories = ["resource", f"prereq-{letter}"]
        if resource["restorable"]:
            categories.append("restorable")
        entities.append({
            "id": resource["id"],
            "label": resource["label"],
            "categories": categories,
            "components": {
                "resource": {
                    "current": resource["current"],
                    "required": resource["required"],
                    "unit": resource["unit"],
                }
            },
        })

    gate = proposal["gate"]
    entities.append({
        "id": gate["id"],
        "label": gate["label"],
        "categories": ["gate"],
        "components": {
            "gate": {
                "status": "blocked",
                "approval_count": 0,
                "required_approvals": gate["required_approvals"],
            }
        },
    })

    for report in proposal["reports"]:
        entities.append({
            "id": report["id"],
            "label": report["label"],
            "categories": ["information"],
            "components": {
                "information": {
                    "content": report["content"],
                    "source_id": report["source_id"],
                    "channel_id": report["channel_id"],
                    "visibility": "direct",
                    "topic": report["topic"],
                    "active": False,
                }
            },
        })
        entities.append({
            "id": f"delivery-{report['id']}",
            "label": f"Delivery: {report['label']}",
            "categories": ["delivery"],
            "components": {
                "delivery": {
                    "info_id": report["id"],
                    "recipient_id": report["recipient_id"],
                    "channel_id": report["channel_id"],
                    "status": "pending",
                }
            },
        })

    bundle = {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {
            **deepcopy(proposal["world"]),
            "content_version": draft["draft_version"],
        },
        "components": deepcopy(_COMPONENTS),
        "entities": entities,
        "actions": deepcopy(_ACTIONS),
        "presentation": deepcopy(_PRESENTATION),
    }
    return validate_bundle(bundle)


def draft_review(
    draft: dict[str, Any],
    *,
    causal_path: Path = DEFAULT_CAUSAL,
) -> dict[str, Any]:
    draft = validate_native_coordination_draft(draft)
    bundle = draft_to_bundle(draft)
    causal_value = json.loads(causal_path.read_text())
    compiled = CausalModel.from_dict(causal_value, bundle=bundle)
    coverage = []
    for row in draft["proposal"]["requirement_coverage"]:
        surface = row["surface"]
        coverage.append({
            "requirement": row["text"],
            "status": "unsupported" if surface == "unsupported" else "represented",
            "surface": surface,
            "implemented_by": list(SURFACE_RULES[surface]),
        })
    explicitly_unsupported = list(draft["proposal"]["unsupported_requests"])
    for row in coverage:
        if row["status"] == "unsupported" and row["requirement"] not in explicitly_unsupported:
            explicitly_unsupported.append(row["requirement"])
    return {
        "schema_version": "world-substrate-native-coordination-draft-review/v0",
        "family": SUPPORTED_FAMILY,
        "draft_version": draft["draft_version"],
        "source_description": draft["source_description"],
        "structure": {
            "world_id": bundle["world"]["id"],
            "members": [
                {"id": row["id"], "label": row["label"], "role": row["components"]["member"]["role"]}
                for row in bundle["entities"] if "member" in row["categories"]
            ],
            "resources": [
                {
                    "id": row["id"],
                    "label": row["label"],
                    **row["components"]["resource"],
                    "restorable": "restorable" in row["categories"],
                }
                for row in bundle["entities"] if "resource" in row["categories"]
            ],
            "gate": deepcopy(draft["proposal"]["gate"]),
            "reports": deepcopy(draft["proposal"]["reports"]),
        },
        "requirements": coverage,
        "assumptions": list(draft["proposal"]["assumptions"]),
        "unsupported_requests": explicitly_unsupported,
        "mechanics": compiled.as_review(),
        "narrowing_is_explicit": bool(explicitly_unsupported),
    }


def _proposal_messages(description: str) -> list[dict[str, str]]:
    contract = proposal_schema()
    context = {
        "description": description,
        "supported_family": {
            "name": SUPPORTED_FAMILY,
            "limits": [
                "3-6 members in one coordination space",
                "exactly four represented prerequisites/resources",
                "exactly one uniquely authorized member",
                "exactly one restorable prerequisite starts below requirement",
                "direct represented reports with distinct recipients",
                "an approval threshold no larger than the number of informed recipients",
                "shared executable rules: communicate, approve, intervene, finalize",
                "no arbitrary scheduling, deception, probabilistic behavior, hidden cognition, or custom institutions",
            ],
        },
        "response_contract": contract,
    }
    return [
        {
            "role": "system",
            "content": (
                "Extract one bounded coordination-world proposal from the user's description. "
                "Return exactly one JSON object and no prose or markdown. Do not invent executable "
                "law: executable rules are fixed by the supported family. Preserve supplied "
                "requirements in requirement_coverage, list every material inference in assumptions, "
                "and list unsupported requests explicitly instead of silently dropping them. "
                "Choose exactly one authorized member and one restorable resource. The restorable "
                "resource must begin below its required value; the other three must begin at or above "
                "their requirements. Report recipients must be distinct and numerous enough to meet "
                "the approval threshold. Use compact lowercase ids."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(context, ensure_ascii=False, sort_keys=True),
        },
    ]


def generate_native_coordination_draft(
    description: str,
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    reasoning_effort: str = "low",
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Any]:
    description = _nonempty(description, "description")
    if len(description) > 8000:
        raise ValueError("description must be at most 8000 characters")
    from llm_client import call_llm, safe_json_loads

    trace_id = trace_id or f"native-coordination-draft-{uuid.uuid4().hex}"
    result = call_llm(
        model,
        _proposal_messages(description),
        task="native-coordination-one-shot-authoring",
        trace_id=trace_id,
        max_budget=max_budget,
        max_tokens=MAX_OUTPUT_TOKENS,
        reasoning_effort=reasoning_effort,
    )
    proposal = safe_json_loads(result.content)
    if not isinstance(proposal, dict):
        raise ValueError("model proposal must be a JSON object")
    draft = {
        "schema_version": DRAFT_SCHEMA_VERSION,
        "family": SUPPORTED_FAMILY,
        "draft_version": 1,
        "source_description": description,
        "proposal": proposal,
    }
    draft = validate_native_coordination_draft(draft)
    bundle = draft_to_bundle(draft)
    review = draft_review(draft)
    return draft, bundle, review, result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-budget", type=float, default=DEFAULT_BUDGET)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    draft, bundle, review, result = generate_native_coordination_draft(
        args.description,
        model=args.model,
        max_budget=args.max_budget,
    )
    payload = {
        "draft": draft,
        "bundle": bundle,
        "review": review,
        "model": getattr(result, "model", args.model),
        "cost_usd": float(getattr(result, "cost", 0.0) or 0.0),
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
