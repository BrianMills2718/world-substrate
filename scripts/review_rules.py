"""An independent review of a generated world's rules (docs/plans/declared_laws.md, piece 3, slice S3).

One typed llm_client call on a model of another family than the rules writer, with a fresh context holding only the
description, the world's laws and the compiled rules. It returns mechanical findings
`{rule_id, description_words, problem}`; the build loop sends them to revision and redesign.
Declared actor-information worlds also require a source-grounded privacy verdict on each
actual starting actor context in that same call. Missing or rejected privacy review raises
ActorInputPrivacyError so the builder cannot treat it as an optional mechanical finding.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPT = Path(__file__).resolve().parents[1] / "prompts/rules_reviewer.yaml"
TASK = "world-substrate-rules-review"
# Another family than the rules writer's gpt-6-luna (Q44): chosen by the review of saved incident worlds,
# evidence/declared-laws/s3-review-choice/README.md.
REVIEW_MODEL = "openrouter/google/gemini-4-argon"
MISSING = "missing"


class ActorInputPrivacyError(ValueError):
    """The generated candidate has not passed the required actor-input review.

    The builder must reject this candidate, rather than treating this as an
    optional mechanical-review failure. The native model trace retains the
    complete review, and ``review`` permits the builder to retain it as well.
    """

    def __init__(self, message: str, review: Any = None):
        super().__init__(message)
        self.review = review


def rule_ids(causal_model: dict[str, Any]) -> list[str]:
    """Every installed rule's id: the mechanics', then the processes'."""
    return ([str(m["mechanic_id"]) for m in causal_model.get("mechanics") or []]
            + [str(p["process_id"]) for p in causal_model.get("processes") or []])


def review_schema(ids: list[str], actor_ids: list[str] | None = None) -> dict[str, Any]:
    schema = {
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
    if actor_ids is not None:
        judgment = {"type": "object", "additionalProperties": False,
                    "required": ["authorized", "explanation"], "properties": {
                        "authorized": {"type": "boolean"},
                        "explanation": {"type": "string", "minLength": 1}}}
        actor = {**judgment, "required": ["actor_id", "authorized", "explanation"],
                 "properties": {**judgment["properties"],
                                "actor_id": {"type": "string", "enum": actor_ids}}}
        schema["required"].append("actor_input_review")
        schema["properties"]["actor_input_review"] = {
            "type": "object", "additionalProperties": False,
            "required": ["public_summary", "actors"], "properties": {
                "public_summary": judgment,
                "actors": {"type": "array", "minItems": len(actor_ids), "maxItems": len(actor_ids), "items": actor}}}
    return schema


def require_actor_input_review(value: Any, actor_ids: list[str]) -> None:
    """Require source-grounded approval of each exact initial actor context.

    This validates the semantic review's typed result; it does not pretend to
    infer the meaning of a profile or source text with string matching.
    """
    review = value.get("actor_input_review") if isinstance(value, dict) else None
    if not isinstance(review, dict) or set(review) != {"public_summary", "actors"}:
        raise ActorInputPrivacyError("actor-input review is missing or malformed", review)
    public = review["public_summary"]
    actors = review["actors"]
    if (not isinstance(actors, list) or len(actors) != len(actor_ids)
            or any(not isinstance(row, dict) or set(row) != {"actor_id", "authorized", "explanation"} for row in actors)
            or {row["actor_id"] for row in actors if isinstance(row.get("actor_id"), str)} != set(actor_ids)):
        raise ActorInputPrivacyError("actor-input review must cover every declared actor exactly once", review)
    if not isinstance(public, dict) or set(public) != {"authorized", "explanation"}:
        raise ActorInputPrivacyError("public-summary review is missing or malformed", review)
    for row in [public, *actors]:
        if (type(row.get("authorized")) is not bool or not isinstance(row.get("explanation"), str)
                or not row["explanation"].strip()):
            raise ActorInputPrivacyError("actor-input review needs an explicit judgment and source basis", review)
        if not row["authorized"]:
            raise ActorInputPrivacyError("generated candidate discloses unauthorized actor information", review)


def initial_actor_inputs(bundle: dict[str, Any], causal_model: dict[str, Any]) -> dict[str, Any]:
    """The same assembled declared contexts residents receive at the start."""
    from scripts.actor_information import actor_context
    from scripts.run_authored_world import build_engine

    engine, _, _ = build_engine(bundle, causal_model)
    return {actor: actor_context(engine, bundle, actor) for actor in bundle["actor_information"]["actors"]}


def read_findings(value: Any, ids: list[str]) -> list[dict[str, str]]:
    """The findings whose rule id is a real rule (or 'missing'); anything else in the reply is dropped."""
    rows = value.get("findings") if isinstance(value, dict) else None
    if not isinstance(rows, list):
        raise ValueError(f"the review did not return a findings list: {str(value)[:200]}")
    known = {*ids, MISSING}
    return [{"rule_id": str(r["rule_id"]), "description_words": str(r.get("description_words", "")),
             "problem": str(r.get("problem", ""))}
            for r in rows if isinstance(r, dict) and r.get("rule_id") in known and str(r.get("problem", "")).strip()]


def starting_values(bundle: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Each thing's starting state under the paths rules read, built-in fields included.

    Where a thing is, who owns it and whether it can be carried are entity fields, not components; the reviewer
    shown only components reported them missing four times in one café build (s4c, 2026-10-29).
    """
    here = (bundle.get("world") or {}).get("location")
    start: dict[str, dict[str, Any]] = {}
    for e in bundle.get("entities") or []:
        if not isinstance(e, dict):
            continue
        row: dict[str, Any] = {"categories": list(e.get("categories") or []),
                               "location": {"location_id": e.get("location") or here}}
        if e.get("owner_ref") is not None:
            row["ownership"] = {"owner_ref": e["owner_ref"]}
        if e.get("portable") is not None:
            row["portable"] = {"portable": bool(e["portable"])}
        start[str(e.get("id"))] = {**row, "components": e.get("components") or {}}
    return start


def review_rules(description: str, bundle: dict[str, Any], causal_model: dict[str, Any], *, trace_id: str,
                 max_budget: float, model: str = REVIEW_MODEL,
                 reasoning_effort: str = "medium") -> tuple[list[dict[str, str]], float]:
    """(findings, cost) for one compiled world. Raises on a failed call; the caller records that and goes on."""
    from llm_client import call_llm_json_schema, render_prompt

    ids = rule_ids(causal_model)
    laws = {"resources": bundle.get("resources") or [], "laws": bundle.get("laws") or []}
    rules = {"mechanics": causal_model.get("mechanics") or [], "processes": causal_model.get("processes") or []}
    # The starting numbers let the reviewer see a move that can never work from the start (#293: pencil
    # XlX1z5lyl8QT's carrier charged 0, so its own purchase law refused every purchase).
    start = starting_values(bundle)
    messages = render_prompt(PROMPT, description=description, laws=json.dumps(laws, indent=1),
                             rules=json.dumps(rules, indent=1), start=json.dumps(start, indent=1))
    actor_ids = None
    if "actor_information" in bundle:
        actor_ids = list(bundle["actor_information"]["actors"])
        messages.append({"role": "user", "content": (
            "Also review the EXACT initial actor inputs below against the ORIGINAL description above. "
            "Return actor_input_review with a source-grounded judgment for public_summary and EVERY actor. "
            "Public facts must be explicitly shared. Profiles may include the person's own personality, goals, "
            "beliefs and interpretations, including mistaken beliefs; this is not a truth check. They must not "
            "disclose another person's private state or a narrator's knowledge of what was withheld. "
            "Negative knowledge can disclose secrets: 'you have not received the failure report' reveals that "
            "a report exists; 'you were not given channel C or batch V17' reveals its private identifiers. "
            "An intended recipient does not know a pending message. A delivered report is exposure to a claim, "
            "not endorsement or knowledge that the claim is true. Check labels, identities, action forms, "
            "briefs and initial knowledge as well as field values. An authorized judgment needs a short "
            "explanation grounded in the source; reject invented disclosures even when put in a limitation. "
            "Never repair or suppress the inputs silently. Mechanical findings remain separate.\n" +
            json.dumps({"public_summary": bundle["actor_information"]["public_summary"],
                        "initial_actor_inputs": initial_actor_inputs(bundle, causal_model)}, indent=1))})
    value, result = call_llm_json_schema(
        model, messages, review_schema(ids, actor_ids), schema_name="world_substrate_rules_review", task=TASK,
        trace_id=trace_id, max_budget=max_budget, max_tokens=16000, reasoning_effort=reasoning_effort,
        model_justification="independent rules review on another model family (declared-laws plan, Q44)",
    )
    if actor_ids is not None:
        require_actor_input_review(value, actor_ids)
    return read_findings(value, ids), float(getattr(result, "cost", 0.0) or 0.0)


__all__ = ["MISSING", "REVIEW_MODEL", "TASK", "read_findings", "review_rules", "review_schema", "rule_ids",
           "starting_values", "ActorInputPrivacyError", "require_actor_input_review", "initial_actor_inputs"]
