"""Open attempts: a person's own words for what they try, read into one typed move (docs/plans/open_attempt.md, piece 1).

A resident no longer picks from a menu. It says what it physically does ("walk through the wall into the hangar"),
and one typed light-model call reads that sentence against the world's action kinds and their fields. The reading
says only what is being tried: its schema has no success or outcome field, so it can never decide whether the
attempt works. The matched move goes to `Engine.submit` like any other envelope and the installed rules alone decide
its effect; a refusal comes only from a rule's checks.

An attempt that fits no kind goes through the engine's existing unsupported path (`UnsupportedAction`): it is
recorded with its words, nothing in the world changes, and the run lists it so the next build can add a rule. Letting
an AI game master invent an effect instead is decision D2 in the plan: not yet (Brian, 2026-10-26).

The reading is kept with the move, and the envelope it produced is what the engine records as the command, so a
replay never calls the model again.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROMPT = Path(__file__).resolve().parents[2] / "prompts/attempt_interpreter.yaml"
TASK = "world-builder-attempt-interpreter"
UNMATCHED_KIND = "unmatched-attempt"  # never a generated kind: generated kinds are the bundle's action slugs
NONE = "none"
WAIT_KIND = "wait"
RESERVED_FIELDS = ("actor", "kind", "base_revision", "controller")


def interpreter_schema(signatures: list[dict[str, Any]]) -> dict[str, Any]:
    """The typed reading: which kind, which value for each of its fields and the words that named it. No outcome."""
    kinds = sorted(str(s["kind"]) for s in signatures)
    fields = sorted({str(f["name"]) for s in signatures for f in s.get("fields") or []}) or [NONE]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["kind", "fields", "nearest_kind", "why"],
        "properties": {
            "kind": {"type": "string", "enum": kinds + [WAIT_KIND, NONE],
                     "description": "The action kind this attempt is, 'wait' for doing nothing, or 'none' if no kind fits."},
            "fields": {
                "type": "array",
                "description": "One row per field of the chosen kind; empty for 'wait' or 'none'.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["field", "value", "quoted_span"],
                    "properties": {
                        "field": {"type": "string", "enum": fields},
                        "value": {"type": "string", "description": "An entity id for an entity field, else the value."},
                        "quoted_span": {"type": "string", "description": "The exact words of the attempt that name it."},
                    },
                },
            },
            "nearest_kind": {"type": "string", "enum": kinds + [NONE],
                             "description": "When kind is 'none', the closest kind; otherwise the chosen kind."},
            "why": {"type": "string", "description": "One sentence on which words decided the kind."},
        },
    }


def _coerce(field_type: str, raw: str) -> tuple[bool, Any]:
    if field_type in {"entity_ref", "string"}:
        return True, raw
    if field_type == "integer":
        try:
            return True, int(raw)
        except ValueError:
            return False, None
    if field_type == "number":
        try:
            return True, float(raw)
        except ValueError:
            return False, None
    if field_type == "boolean" and raw in {"true", "false"}:
        return True, raw == "true"
    return False, None


def read_interpretation(value: object, attempt: str, signatures: list[dict[str, Any]],
                        entity_ids: set[str], actor: str | None = None) -> dict[str, Any]:
    """Check the model's reading against the world's kinds and entities.

    Returns {"kind", "fields", "quoted_spans", "nearest_kind", "why"} for a matched move, {"kind": "wait", ...} for a
    wait, or {"unmatched": True, "nearest_kind", "why"} when no kind fits or the reading does not fit the world (an
    unknown entity, a missing field, words not in the attempt). Never says whether the move will work.
    """
    if not isinstance(value, dict):
        return {"unmatched": True, "nearest_kind": NONE, "why": "the reading was not an object"}
    kind = str(value.get("kind") or NONE)
    why = str(value.get("why") or "")
    nearest = str(value.get("nearest_kind") or NONE)
    if kind == WAIT_KIND:
        return {"kind": WAIT_KIND, "fields": {}, "quoted_spans": {}, "nearest_kind": NONE, "why": why}
    signature = next((s for s in signatures if s["kind"] == kind), None)
    if signature is None:
        return {"unmatched": True, "nearest_kind": nearest, "why": why}
    declared = {str(f["name"]): str(f["type"]) for f in signature.get("fields") or []}
    rows = value.get("fields") if isinstance(value.get("fields"), list) else []
    fields: dict[str, Any] = {}
    spans: dict[str, str] = {}
    problems: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or row.get("field") not in declared or row["field"] in fields:
            problems.append(f"field row {row!r} is not one of {kind}'s fields once")
            continue
        name, raw, span = str(row["field"]), str(row.get("value", "")), str(row.get("quoted_span", ""))
        ok, typed = _coerce(declared[name], raw)
        if declared[name] == "integer" and (not span or span not in attempt):
            # An amount the person never said is one: 2026-10-27 pencil c_SrKPfa3rpE, the lead-maker's "I try to make
            # leads from my clay and graphite" was refused in 3 rounds as quantity='' or 'unspecified'; pencil
            # czt5uoGw5t3L refused the reader's own "1" with an empty quote 5 times when only failed numbers defaulted.
            fields[name], spans[name] = 1, ""
            continue
        if not ok:
            problems.append(f"{name}={raw!r} is not a {declared[name]}")
        elif declared[name] == "entity_ref" and typed not in entity_ids:
            problems.append(f"{name}={raw!r} names no entity in this world")
        elif (not span or span not in attempt) and not (declared[name] == "entity_ref" and typed == actor):
            # The speaker names themself as "I": 2026-10-27 pencil iMrL2U84cLCS, the shop's own "I try to sell one
            # pencil" was refused in 9 of 15 rounds because the reader quoted the shop's id instead of "I".
            problems.append(f"{name}'s quoted words {span!r} are not in the attempt")
        else:
            fields[name], spans[name] = typed, span
    for name in [n for n, t in declared.items() if t == "integer" and n not in fields and not problems]:
        fields[name], spans[name] = 1, ""
    missing = sorted(set(declared) - set(fields))
    if missing and not problems:
        problems.append(f"no value for {', '.join(missing)}")
    if problems:
        return {"unmatched": True, "nearest_kind": kind, "why": "the reading did not fit the world: " + "; ".join(problems)}
    return {"kind": kind, "fields": fields, "quoted_spans": spans, "nearest_kind": kind, "why": why}


def envelope(reading: dict[str, Any], *, actor: str, attempt: str, base_revision: int,
             controller: str) -> dict[str, Any] | None:
    """The envelope to submit: the typed move, an unsupported envelope carrying the words, or None for a wait."""
    if reading.get("kind") == WAIT_KIND:
        return None
    head = {"actor": actor, "base_revision": base_revision, "controller": controller}
    if reading.get("unmatched"):
        return {**head, "kind": UNMATCHED_KIND, "attempt": attempt,
                "nearest_kind": reading.get("nearest_kind"), "why": reading.get("why")}
    return {**head, "kind": reading["kind"], **reading["fields"]}


def signatures_for(bundle: dict[str, Any], mechanics: Any) -> list[dict[str, Any]]:
    """Each installed action rule's kind and fields (from the rule, so a matched envelope has exactly its keys), with
    the bundle's description of the action."""
    described = {a.get("kind"): a.get("description", "") for a in bundle.get("actions") or []}
    return [
        {"kind": m.action_kind, "description": described.get(m.action_kind, ""),
         "fields": [dict(f) for f in m.action_signature.get("fields") or [] if f.get("name") not in RESERVED_FIELDS]}
        for m in mechanics
    ]


def interpret(attempt: str, *, actor: str, signatures: list[dict[str, Any]], entities: dict[str, str],
              model: str, trace_id: str, max_budget: float) -> tuple[dict[str, Any], float]:
    """One typed llm_client call reading `attempt`; returns (checked reading, cost). `entities` maps id to label."""
    from llm_client import call_llm_json_schema, render_prompt

    messages = render_prompt(PROMPT, actor_id=actor, attempt=attempt,
                             kinds=json.dumps(signatures, indent=1), entities=json.dumps(entities, indent=1))
    value, result = call_llm_json_schema(
        model, messages, interpreter_schema(signatures), schema_name="world_substrate_attempt_reading",
        task=TASK, trace_id=trace_id, max_budget=max_budget, max_tokens=400, reasoning_effort="low",
    )
    return read_interpretation(value, attempt, signatures, set(entities), actor), float(getattr(result, "cost", 0.0) or 0.0)


__all__ = ["NONE", "TASK", "UNMATCHED_KIND", "WAIT_KIND", "envelope", "interpret", "interpreter_schema",
           "read_interpretation", "signatures_for"]
