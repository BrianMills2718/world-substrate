"""An independent review of a generated world's rules (docs/plans/declared_laws.md, piece 3, slice S3).

One typed llm_client call on a model of another family than the rules writer, with a fresh context holding only the
description, the world's laws and the compiled rules. It returns findings `{rule_id, description_words, problem}`,
never a pass mark; the build loop sends them to the rules writer's revision and the world designer's redesign, and the
build record lists them. A failed or malformed review is recorded with its error and the build goes on without it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPT = Path(__file__).resolve().parents[1] / "prompts/rules_reviewer.yaml"
TASK = "world-substrate-rules-review"
# Another family than the rules writer's gpt-6-luna (Q44): chosen by the review of saved incident worlds,
# evidence/declared-laws/s3-review-choice/README.md.
REVIEW_MODEL = "openrouter/google/gemini-3.1-pro-preview"
MISSING = "missing"


def rule_ids(causal_model: dict[str, Any]) -> list[str]:
    """Every installed rule's id: the mechanics', then the processes'."""
    return ([str(m["mechanic_id"]) for m in causal_model.get("mechanics") or []]
            + [str(p["process_id"]) for p in causal_model.get("processes") or []])


def review_schema(ids: list[str]) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False, "required": ["findings"],
        "properties": {"findings": {"type": "array", "items": {
            "type": "object", "additionalProperties": False,
            "required": ["rule_id", "description_words", "problem"],
            "properties": {
                "rule_id": {"type": "string", "enum": [*ids, MISSING],
                            "description": f"The rule the problem is in, or '{MISSING}' when no rule does it."},
                "description_words": {"type": "string", "description": "The description's own words it fails."},
                "problem": {"type": "string", "description": "What is wrong, in one or two plain sentences."},
            }}}},
    }


def read_findings(value: Any, ids: list[str]) -> list[dict[str, str]]:
    """The findings whose rule id is a real rule (or 'missing'); anything else in the reply is dropped."""
    rows = value.get("findings") if isinstance(value, dict) else None
    if not isinstance(rows, list):
        raise ValueError(f"the review did not return a findings list: {str(value)[:200]}")
    known = {*ids, MISSING}
    return [{"rule_id": str(r["rule_id"]), "description_words": str(r.get("description_words", "")),
             "problem": str(r.get("problem", ""))}
            for r in rows if isinstance(r, dict) and r.get("rule_id") in known and str(r.get("problem", "")).strip()]


def review_rules(description: str, bundle: dict[str, Any], causal_model: dict[str, Any], *, trace_id: str,
                 max_budget: float, model: str = REVIEW_MODEL,
                 reasoning_effort: str = "medium") -> tuple[list[dict[str, str]], float]:
    """(findings, cost) for one compiled world. Raises on a failed call; the caller records that and goes on."""
    from llm_client import call_llm_json_schema, render_prompt

    ids = rule_ids(causal_model)
    laws = {"resources": bundle.get("resources") or [], "laws": bundle.get("laws") or []}
    rules = {"mechanics": causal_model.get("mechanics") or [], "processes": causal_model.get("processes") or []}
    messages = render_prompt(PROMPT, description=description, laws=json.dumps(laws, indent=1),
                             rules=json.dumps(rules, indent=1))
    value, result = call_llm_json_schema(
        model, messages, review_schema(ids), schema_name="world_substrate_rules_review", task=TASK,
        trace_id=trace_id, max_budget=max_budget, max_tokens=16000, reasoning_effort=reasoning_effort,
        model_justification="independent rules review on another model family (declared-laws plan, Q44)",
    )
    return read_findings(value, ids), float(getattr(result, "cost", 0.0) or 0.0)


__all__ = ["MISSING", "REVIEW_MODEL", "TASK", "read_findings", "review_rules", "review_schema", "rule_ids"]
