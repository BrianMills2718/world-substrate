#!/usr/bin/env python3
"""Generate a constrained causal model proposal for a world-authoring bundle.

The model returns JSON only.  Its output is then compiled by
``world_substrate.action_authoring``; arbitrary source code is never executed.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.scaffold_world import load_bundle, validate_bundle
from world_substrate.action_authoring import (
    ACTION_MECHANIC_SCHEMA_VERSION,
    CAUSAL_MODEL_SCHEMA_VERSION,
    CausalModel,
)

DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
DEFAULT_BUDGET = 0.12
MAX_MECHANICS_OUTPUT_TOKENS = 8192


def _primitive_schema(kind: str) -> dict[str, Any]:
    return {
        "string": {"type": "string", "minLength": 1},
        "entity_ref": {"type": "string", "minLength": 1},
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "boolean": {"type": "boolean"},
    }[kind]


def _selector_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "categories": {"type": "array", "items": {"type": "string"}},
            "components": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["categories", "components"],
        "additionalProperties": False,
    }


def _expr_schema(participants: list[str], fields: list[str]) -> dict[str, Any]:
    names = ["actor", *participants]
    return {
        "anyOf": [
            {
                "type": "object",
                "properties": {
                    "literal": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "boolean"},
                            {"type": "null"},
                        ]
                    }
                },
                "required": ["literal"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"action_field": {"enum": fields}},
                "required": ["action_field"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {
                    "participant": {
                        "type": "object",
                        "properties": {
                            "name": {"enum": names},
                            "path": {"type": "string", "minLength": 1},
                        },
                        "required": ["name", "path"],
                        "additionalProperties": False,
                    }
                },
                "required": ["participant"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"entity_id": {"enum": names}},
                "required": ["entity_id"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"owner_ref": {"enum": names}},
                "required": ["owner_ref"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"event_id": {"const": True}},
                "required": ["event_id"],
                "additionalProperties": False,
            },
        ]
    }


def _mechanic_schema(action: dict[str, Any]) -> dict[str, Any]:
    fields = action.get("fields") or []
    field_names = [row["name"] for row in fields]
    entity_fields = [row["name"] for row in fields if row["type"] == "entity_ref"]
    scalar_fields = [row for row in fields if row["type"] != "entity_ref"]
    expr = _expr_schema(entity_fields, field_names)
    participant_properties = {name: _selector_schema() for name in entity_fields}
    parameter_properties = {
        row["name"]: {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": _primitive_schema(row["type"]),
        }
        for row in scalar_fields
    }
    participant_object: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
    }
    if participant_properties:
        participant_object["properties"] = participant_properties
        participant_object["required"] = entity_fields
    parameter_object: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
    }
    if parameter_properties:
        parameter_object["properties"] = parameter_properties
        parameter_object["required"] = [row["name"] for row in scalar_fields]
    return {
        "type": "object",
        "properties": {
            "schema_version": {"const": ACTION_MECHANIC_SCHEMA_VERSION},
            "mechanic_id": {"type": "string", "minLength": 1},
            "version": {"type": "string", "minLength": 1},
            "action_kind": {"const": action["kind"]},
            "rationale": {"type": "string", "minLength": 1},
            "actor_selector": _selector_schema(),
            "participants": participant_object,
            "parameters": parameter_object,
            "checks": {
                "type": "array",
                "minItems": 1,
                "maxItems": 12,
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "minLength": 1},
                        "left": expr,
                        "op": {"enum": ["eq", "ne", "lt", "lte", "gt", "gte", "contains"]},
                        "right": expr,
                    },
                    "required": ["label", "left", "op", "right"],
                    "additionalProperties": False,
                },
            },
            "effects": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "properties": {
                        "participant": {"enum": ["actor", *entity_fields]},
                        "path": {"type": "string", "minLength": 1},
                        "op": {"enum": ["set", "add", "subtract"]},
                        "value": expr,
                    },
                    "required": ["participant", "path", "op", "value"],
                    "additionalProperties": False,
                },
            },
            "limits": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
            "tests": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
            "semantic_bindings": {
                "type": "array",
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
        },
        "required": [
            "schema_version",
            "mechanic_id",
            "version",
            "action_kind",
            "rationale",
            "actor_selector",
            "participants",
            "parameters",
            "checks",
            "effects",
            "limits",
            "tests",
            "semantic_bindings",
        ],
        "additionalProperties": False,
    }


def causal_model_schema(bundle: dict[str, Any]) -> dict[str, Any]:
    actions = bundle.get("actions") or []
    return {
        "type": "object",
        "properties": {
            "schema_version": {"const": CAUSAL_MODEL_SCHEMA_VERSION},
            "mechanics": {
                "type": "array",
                "minItems": len(actions),
                "maxItems": len(actions),
                "items": {"anyOf": [_mechanic_schema(action) for action in actions]},
            },
            "terminal": {
                "anyOf": [
                    {"type": "null"},
                    {
                        "type": "object",
                        "properties": {
                            "mode": {"enum": ["all", "any"]},
                            "selector": _selector_schema(),
                            "checks": {
                                "type": "array",
                                "minItems": 1,
                                "maxItems": 8,
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string", "minLength": 1},
                                        "op": {"enum": ["eq", "ne", "lt", "lte", "gt", "gte", "contains"]},
                                        "value": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "integer"},
                                                {"type": "number"},
                                                {"type": "boolean"},
                                            ]
                                        },
                                    },
                                    "required": ["path", "op", "value"],
                                    "additionalProperties": False,
                                },
                            },
                        },
                        "required": ["mode", "selector", "checks"],
                        "additionalProperties": False,
                    },
                ]
            },
        },
        "required": ["schema_version", "mechanics", "terminal"],
        "additionalProperties": False,
    }


def _context(bundle: dict[str, Any]) -> dict[str, Any]:
    paths: list[str] = [
        "location.location_id",
        "ownership.owner_ref",
        "portable.portable",
    ]
    for comp in bundle.get("components") or []:
        for field in comp.get("fields") or []:
            paths.append(f"components.{comp['name']}.{field['name']}")
    # Built-in state is not written in the bundle's component values, so state
    # it exactly as build_engine will initialise it. Without this a proposer
    # guesses (e.g. "the can is in the garden" when every entity starts at the
    # world location) and every action is refused from the first round.
    initial_builtin_state = {
        row["id"]: {
            "location.location_id": row.get("location") or bundle["world"]["location"],
            "ownership.owner_ref": row.get("owner_ref"),
            "portable.portable": row.get("portable"),
        }
        for row in bundle.get("entities", [])
    }
    return {
        "world": bundle["world"],
        "components": bundle.get("components", []),
        "entities": bundle.get("entities", []),
        "initial_builtin_state": initial_builtin_state,
        "actions": bundle.get("actions", []),
        "allowed_state_paths": paths,
        "authority_rules": [
            "Use only action participants as effect targets.",
            "Checks on location/ownership/portable paths must agree with initial_builtin_state "
            "(null means unset), so that at least one action is possible from the starting state.",
            "Never check ownership.owner_ref or portable.portable on an entity whose initial_builtin_state "
            "value is null, unless one of your own effects sets that value first; use component fields instead.",
            "A participant's selector must list in `components` every component whose fields that participant's checks or effects read or write.",
            "Checks and effects must use only allowed_state_paths.",
            "Do not invent source code, hidden state, or new entities.",
            "An action should change only state causally implied by its description and represented world.",
            "Use owner_ref expressions for actor ownership rather than hard-coded actor ids.",
            "Terminal, if present, must be derivable from represented state and must not duplicate a completion flag.",
            "Limits and tests must name omissions and refusal/boundary cases honestly.",
            "Every check label is a short plain-English condition a visitor understands, using entity labels "
            "(e.g. \"the watering can is free\", \"Ava is holding the knife\"); never jargon such as actor, "
            "owner_ref, context, entity, component or participant.",
        ],
    }


def generate_causal_model(
    bundle: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    reasoning_effort: str = "low",
    guidance: str = "",
) -> tuple[dict[str, Any], Any]:
    bundle = validate_bundle(bundle)
    if not bundle.get("actions"):
        raise ValueError("bundle has no action signatures to generate mechanics for")
    # Do not depend on provider-native JSON Schema here. Some routes accept the
    # policy-choice schema but reject richer nested unions. The model remains a
    # proposer only: ordinary text is parsed as JSON and the local causal
    # compiler below is the authority gate. No returned source code is executed.
    from llm_client import call_llm, safe_json_loads

    trace_id = trace_id or f"world-builder-mechanics-{uuid.uuid4().hex}"
    context = _context(bundle)
    context["response_contract"] = causal_model_schema(bundle)
    if guidance.strip():
        context["author_guidance"] = guidance.strip()[:4000]
    messages = [
        {
            "role": "system",
            "content": (
                "You are proposing causal mechanics for a governed world model. "
                "Return exactly one JSON object and no prose or markdown. You are not writing code. "
                "The response must satisfy response_contract. Every effect must be justified by "
                "represented state and the action description. Prefer conservative refusal checks "
                "over assumptions. Do not add reads/writes fields; the local compiler derives authority. "
                "Whenever you name a state path, copy it EXACTLY from allowed_state_paths."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(context, indent=2, sort_keys=True),
        },
    ]
    result = None
    value: dict[str, Any] | None = None
    last_error: Exception | None = None
    # One compiler-guided repair is enough to recover common notation mistakes
    # without turning generation into an open-ended autonomous loop. Both calls
    # share the same trace id and hard budget ceiling.
    for attempt in range(2):
        result = call_llm(
            model,
            messages,
            task="world-substrate-mechanic-authoring",
            trace_id=trace_id,
            max_budget=max_budget,
            max_tokens=MAX_MECHANICS_OUTPUT_TOKENS,
            reasoning_effort=reasoning_effort,
            num_retries=1,
        )
        try:
            parsed = safe_json_loads(result.content)
            if not isinstance(parsed, dict):
                raise ValueError("model returned a non-object causal model")
            value = parsed
            compiled = CausalModel.from_dict(value, bundle=bundle)
            review = compiled.as_review()
            out = deepcopy(value)
            out["review"] = review
            return out, result
        except (ValueError, TypeError, KeyError) as error:
            last_error = error
            if attempt == 1:
                break
            messages = [
                *messages,
                {"role": "assistant", "content": result.content},
                {
                    "role": "user",
                    "content": (
                        "The local causal compiler rejected that proposal. "
                        f"Compiler error: {type(error).__name__}: {error}. "
                        "Return a corrected JSON object only. State paths in participant/path and "
                        "effect/path fields must be copied EXACTLY from allowed_state_paths; do not "
                        "abbreviate component containers (for example use portable.portable, not portable)."
                    ),
                },
            ]
    assert last_error is not None
    raise ValueError(f"causal proposal remained invalid after one repair: {last_error}") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--trace-id")
    parser.add_argument("--max-budget", type=float, default=DEFAULT_BUDGET)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bundle = load_bundle(args.bundle)
    value, result = generate_causal_model(
        bundle,
        model=args.model,
        trace_id=args.trace_id,
        max_budget=args.max_budget,
    )
    rendered = json.dumps(value, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
        print(args.output)
    else:
        print(rendered, end="")
    cost = getattr(result, "cost", None)
    if cost is not None:
        print(f"cost_usd={cost}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
