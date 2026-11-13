"""An independent review of a generated world's rules (docs/plans/declared_laws.md, piece 3, slice S3).

One typed llm_client call on a model of another family than the rules writer, with a fresh context holding only the
description, the world's laws and the compiled rules. It returns mechanical findings
`{rule_id, description_words, problem}`; the build loop sends them to revision and redesign.
Declared actor-information worlds also require a source-grounded privacy verdict on each
actual starting actor context in that same call. Missing or rejected privacy review raises
ActorInputPrivacyError so the builder cannot treat it as an optional mechanical finding.
Independent decisions also require a canonical-state authority verdict in the same call.
Only well-formed negative source judgments permit the existing bounded source repair.
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


class SourceDraftReviewError(ValueError):
    """A required source judgment failed; only a valid typed negative permits repair."""

    def __init__(self, message: str, review: Any = None, *, repairable: bool = False):
        super().__init__(message)
        self.review = review
        self.repairable = repairable
        self.feedback = message + "\n" + json.dumps(review, ensure_ascii=False)


class ActorInputPrivacyError(SourceDraftReviewError):
    """The generated candidate has not passed the required actor-input review.

    The builder must reject this candidate, rather than treating this as an
    optional mechanical-review failure. The native model trace retains the
    complete review, and ``review`` permits the builder to retain it as well.
    """


class CanonicalStateAuthorityError(SourceDraftReviewError):
    """Current material state has not passed the independent authority review."""


def rule_ids(causal_model: dict[str, Any]) -> list[str]:
    """Every installed rule's id: the mechanics', then the processes'."""
    return ([str(m["mechanic_id"]) for m in causal_model.get("mechanics") or []]
            + [str(p["process_id"]) for p in causal_model.get("processes") or []])


def review_schema(ids: list[str], actor_ids: list[str] | None = None, *, independent: bool = False) -> dict[str, Any]:
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
    if independent:
        schema["required"].append("canonical_state_review")
        schema["properties"]["canonical_state_review"] = {
            "type": "object", "additionalProperties": False,
            "required": ["consistent", "explanation"], "properties": {
                "consistent": {"type": "boolean"},
                "explanation": {"type": "string", "minLength": 1}}}
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
    if any(not row["authorized"] for row in [public, *actors]):
        raise ActorInputPrivacyError("generated candidate discloses unauthorized actor information", review,
                                     repairable=True)


def require_canonical_state_review(value: Any) -> None:
    review = value.get("canonical_state_review") if isinstance(value, dict) else None
    if (not isinstance(review, dict) or set(review) != {"consistent", "explanation"}
            or type(review.get("consistent")) is not bool
            or not isinstance(review.get("explanation"), str) or not review["explanation"].strip()):
        raise CanonicalStateAuthorityError("canonical-state authority review is missing or malformed", review)
    if not review["consistent"]:
        raise CanonicalStateAuthorityError("generated candidate duplicates or contradicts canonical current state",
                                           review, repairable=True)



def initial_actor_inputs(bundle: dict[str, Any], causal_model: dict[str, Any]) -> dict[str, Any]:
    """The same assembled declared contexts residents receive at the start."""
    from scripts.actor_information import actor_context
    from scripts.run_authored_world import build_engine

    engine, _, _ = build_engine(bundle, causal_model)
    return {actor: actor_context(engine, bundle, actor) for actor in bundle["actor_information"]["actors"]}


def builtin_semantics(bundle: dict[str, Any]) -> dict[str, Any]:
    """Give semantic review the executable operator and opted-in procedure contracts."""
    from world_substrate.action_authoring import REPORT_RECORD_KEYS
    semantics = {"append_report": {
        "implementation": "src/world_substrate/action_authoring.py:report_record",
        "record_fields": sorted(REPORT_RECORD_KEYS),
        "effect": "Append one immutable JSON record to the recipient participant's string_list. source_id is the actual acting person, recipient_id the target; content is their verbatim action string. Event, revision and direct delivered status are recorded. Unknown claim lineage remains explicitly undeclared. The operation changes neither belief, stance, assent nor technical condition.",
    }}
    if any("validation_decision" in e.get("components", {}) for e in bundle.get("entities", [])):
        semantics["independent_decision"] = {
            "implementation": "spikes/any-scenario-2026-10/compile_spec.py:_independent_family",
            "authority": "docs/model/modeling-choices.md:single-concern institutional procedure (Brian-approved I0/I1 contract)",
            "initial_state": "initial_validation is an already recorded result. A failed initial result creates a public hold at initialization. Public dashboard exposure is distinct from receiving a private report; a public hold legitimately reveals failed validation under this explicit procedure. No new filing action is required to expose already recorded initial public state.",
            "canonical_state_authority": "technical_condition.passing is the current technical truth, changed only by authorized repair. validation_decision.validation records the latest validation, its hold is institutional state, and actor_position owns every actor's stance and assent, including nonrequired actors whose assent has zero decision weight; activation checks the required actors' individual assents. A separate world_record asserting the current actual condition must not duplicate this truth unless every relevant transition keeps it consistent. Immutable dated reports, past test measurements and historical results may remain unchanged after repair: they describe the past or a claim, not the current actual condition. Private historical evidence does not become public merely because the public validation state changes.",
            "review_boundary": "Check the opted-in public procedure against the source and adopted contract. Lack of a private report does not imply lack of authorized public evidence. Private test details and hidden actual technical condition still require separate grants. Reject any source-inconsistent disclosure; the compiled declaration alone does not authorize arbitrary private facts.",
        }
    return semantics


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
    """(findings, cost); required source reviews fail closed on missing, invalid or rejected judgments."""
    from llm_client import call_llm_json_schema, render_prompt

    ids = rule_ids(causal_model)
    laws = {"resources": bundle.get("resources") or [], "laws": bundle.get("laws") or []}
    rules = {"mechanics": causal_model.get("mechanics") or [], "processes": causal_model.get("processes") or []}
    # The starting numbers let the reviewer see a move that can never work from the start (#293: pencil
    # XlX1z5lyl8QT's carrier charged 0, so its own purchase law refused every purchase).
    start = starting_values(bundle)
    messages = render_prompt(PROMPT, description=description, laws=json.dumps(laws, indent=1),
                             rules=json.dumps(rules, indent=1), start=json.dumps(start, indent=1))
    independent = any("validation_decision" in e.get("components", {}) for e in bundle.get("entities", []))
    actor_ids = None
    if independent:
        messages.append({"role": "user", "content": (
            "Also return canonical_state_review: an explicit consistent boolean and a source-grounded explanation. "
            "Check the ORIGINAL description, all starting entity fields and the ACTUAL compiled rules against the "
            "builtin contracts below. Identify every representation of the same CURRENT material fact, including "
            "semantic aliases in world_records. Reject duplicate current technical condition, validation, hold, stance "
            "or assent truth that relevant transitions do not keep consistent. In particular a repair must not leave "
            "a second field still asserting the current actual condition is failed. Do not reject immutable historical "
            "reports or past measurements just because they remain unchanged after a repair. Explain which fields "
            "own current truth and how their writers preserve it, citing the source. Never infer authority from a "
            "field's name alone. Mechanical findings and actor privacy judgments remain separate.\n" +
            json.dumps({"builtin_semantics": builtin_semantics(bundle)}, indent=1))})
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
            "not proof of its origin. For an initial report, actual transmitter attribution requires an explicitly "
            "named sender in the source; an unspecified sender must stay unspecified even if one seems plausible. "
            "Apparent source and common claim lineage are distinct from actual transmitter identity. Exposure is "
            "not endorsement or knowledge that the claim is true. Check labels, identities, action forms, "
            "briefs and initial knowledge as well as field values. An authorized judgment needs a short "
            "explanation grounded in the source; reject invented disclosures even when put in a limitation. "
            "Never repair or suppress the inputs silently. Mechanical findings remain separate.\n" +
            json.dumps({"public_summary": bundle["actor_information"]["public_summary"],
                        "builtin_semantics": builtin_semantics(bundle),
                        "initial_actor_inputs": initial_actor_inputs(bundle, causal_model)}, indent=1))})
    value, result = call_llm_json_schema(
        model, messages, review_schema(ids, actor_ids, independent=independent), schema_name="world_substrate_rules_review", task=TASK,
        trace_id=trace_id, max_budget=max_budget, max_tokens=16000, reasoning_effort=reasoning_effort,
        model_justification="independent rules review on another model family (declared-laws plan, Q44)",
    )
    findings = read_findings(value, ids)
    failures = []
    for check in ([lambda: require_actor_input_review(value, actor_ids)] if actor_ids is not None else []) + (
            [lambda: require_canonical_state_review(value)] if independent else []):
        try:
            check()
        except SourceDraftReviewError as error:
            failures.append(error)
    if failures:
        # A malformed gate cannot be disguised as a repairable negative on another gate.
        error = next((e for e in failures if not e.repairable), failures[0])
        error.feedback = "\n".join(e.feedback for e in failures)
        error.full_review = value
        raise error
    return findings, float(getattr(result, "cost", 0.0) or 0.0)


__all__ = ["MISSING", "REVIEW_MODEL", "TASK", "read_findings", "review_rules", "review_schema", "rule_ids",
           "starting_values", "SourceDraftReviewError", "ActorInputPrivacyError", "CanonicalStateAuthorityError",
           "require_actor_input_review", "require_canonical_state_review", "initial_actor_inputs"]
