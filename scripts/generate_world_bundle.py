#!/usr/bin/env python3
"""Propose a world-authoring bundle from a plain-English description.

This is the first half of natural-language building in the World Builder. The
model proposes *represented structure only* (components, entities, action
signatures, presentation hints). It does not author consequences: executable
law still comes from `generate_causal_model`, is compiled locally, and must be
explicitly approved before any run. `validate_bundle` is the authority gate
here; up to two validator-guided repairs are allowed.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.scaffold_world import FIELD_TYPES, SCHEMA_VERSION, BundleError, validate_bundle

DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
DEFAULT_BUDGET = 0.08
MAX_BUNDLE_OUTPUT_TOKENS = 6144
MAX_DESCRIPTION_CHARS = 2000
EXAMPLE = REPO / "examples/world_authoring/orchard-v0.json"

# Small worlds keep generated law reviewable and runs short enough to watch.
SIZE_RULES = [
    "2 to 10 entities; 1 to 4 components; 1 to 4 actions.",
    "At least one entity is an actor that can act (give it a component such as worker/person and a clear category).",
    "Every action must be something an actor in this world could plausibly do repeatedly until the situation resolves.",
    "Represent the state the actions change (e.g. stage, count, location) as component fields with typed defaults.",
    "Make the situation able to finish: there must be represented state from which 'done' can be read (e.g. all orders served).",
]


def _contract() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "world": "{id (lowercase-slug), label, summary (one sentence), location (slug), content_version: 1}",
        "components": "[{name (python identifier), fields: [{name, type, default}]}]",
        "field_types": sorted(FIELD_TYPES),
        "entities": (
            "[{id (lowercase-slug), label, categories: [nonempty strings], components: {component: {every declared field}},"
            " optional portable: bool, optional owner_ref: 'actor:<id>'|'place:<id>'|'entity:<id>'|'unowned'}]"
        ),
        "actions": "[{kind (lowercase-slug), description, fields: [{name, type in string|integer|number|boolean|entity_ref}]}]",
        "reserved_action_field_names": ["actor", "kind", "base_revision", "controller"],
        "presentation": (
            "{assets: {asset_id: {kind: 'emoji', value}}, category_assets: {category: asset_id},"
            " station_roles: {category: one of source|workstation|surface|goal}} (station_roles may be {})"
        ),
        "not_modeled": (
            "Top-level list of short plain-English strings naming every part of the description you could NOT "
            "represent with this format (for example deadlines, clocks, probabilities, money, distances). "
            "Use [] only if everything was represented."
        ),
        "rules": [
            "Every entity component object must list exactly the component's declared fields, with values of the declared type.",
            "entity_ref values must name an entity id that exists in this bundle.",
            "Labels and descriptions are plain English a visitor would use (\"Ava\", \"watering can\"), never internal jargon.",
            *SIZE_RULES,
        ],
    }


def _messages(description: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You turn a plain-English description of a small situation into the represented structure "
                "of a governed simulation. Return exactly one JSON object and no prose or markdown. "
                "You are describing what exists and what actors may attempt, not what happens: do not "
                "describe consequences or rules. Follow the contract exactly; the example shows the format."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": description,
                    "contract": _contract(),
                    "example_bundle": json.loads(EXAMPLE.read_text()),
                },
                indent=2,
            ),
        },
    ]


MAX_REPAIRS = 2


def generate_world_bundle(
    description: str,
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    reasoning_effort: str = "low",
) -> tuple[dict[str, Any], list[str], Any]:
    """Return (validated bundle, parts of the description not represented, last LLM result)."""
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a nonempty string")
    if len(description) > MAX_DESCRIPTION_CHARS:
        raise ValueError(f"description must be at most {MAX_DESCRIPTION_CHARS} characters")
    from llm_client import call_llm, safe_json_loads

    trace_id = trace_id or f"world-builder-bundle-{uuid.uuid4().hex}"
    messages = _messages(description.strip())
    last_error: Exception | None = None
    for attempt in range(MAX_REPAIRS + 1):
        result = call_llm(
            model,
            messages,
            task="world-substrate-world-authoring",
            trace_id=trace_id,
            max_budget=max_budget,
            max_tokens=MAX_BUNDLE_OUTPUT_TOKENS,
            reasoning_effort=reasoning_effort,
            num_retries=1,
        )
        try:
            parsed = safe_json_loads(result.content)
            if not isinstance(parsed, dict):
                raise BundleError("model returned a non-object bundle")
            not_modeled = parsed.pop("not_modeled", [])
            if not isinstance(not_modeled, list) or not all(isinstance(x, str) for x in not_modeled):
                raise BundleError("not_modeled must be a list of strings")
            bundle = validate_bundle(parsed)
            if not bundle["actions"]:
                raise BundleError("bundle must declare at least one action")
            return bundle, [x.strip() for x in not_modeled if x.strip()][:8], result
        except (BundleError, ValueError, TypeError, KeyError) as error:
            last_error = error
            if attempt == MAX_REPAIRS:
                break
            messages = [
                *messages,
                {"role": "assistant", "content": result.content},
                {
                    "role": "user",
                    "content": (
                        "The local bundle validator rejected that proposal. "
                        f"Validator error: {type(error).__name__}: {error}. "
                        "Return a corrected JSON object only."
                    ),
                },
            ]
    assert last_error is not None
    raise ValueError(f"world proposal remained invalid after {MAX_REPAIRS} repairs: {last_error}") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-budget", type=float, default=DEFAULT_BUDGET)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bundle, not_modeled, result = generate_world_bundle(args.description, model=args.model, max_budget=args.max_budget)
    rendered = json.dumps(bundle, indent=2) + "\n"
    if not_modeled:
        print("not modeled: " + "; ".join(not_modeled), file=sys.stderr)
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    print(f"model={getattr(result, 'model', args.model)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
