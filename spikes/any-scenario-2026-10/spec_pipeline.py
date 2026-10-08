"""The scenario-spec path of the describe-any-scenario pipeline (plan scenario-spec-adoption, check S4).

text --(1 structured call)--> ScenarioSpecV1 --(compile_spec, no call)--> bundle + reviewed communicate rule +
moment processes + coverage --(1 structured call)--> action signatures for the behaviors left `to_generate` -->
existing mechanics generator --> merged causal model (the reviewed communicate rule and the moment processes are
kept as compiled; a generated rule with the same id or kind is dropped and recorded).
"""
from __future__ import annotations

import json
import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from compile_spec import compile_spec
from scenario_spec import ScenarioSpecV1

SPEC_SYSTEM = (
    "You define a simulation world from a plain-language scenario, filling the given schema exactly. "
    "Rules: (1) Every person, group, organisation or country the scenario names or implies as acting is a person, "
    "with a behavioral profile taken from what the scenario says about them; never fold a named group into "
    "another. (2) Information that the scenario says someone holds or passes on is an information item: its holder "
    "is who has it at the start, its recipients are who it should reach, its channel is the route named or implied "
    "(for example a group's own channel). Make concrete items: a short true statement each, not a category. "
    "(3) Regular events (meetings, reviews, deadlines) are scheduled moments with a tick and, if they repeat, "
    "every_ticks; one tick is one week unless the scenario implies otherwise; a deadline is a moment too. "
    "(4) Quantities and states that change (support, readiness, time available, decision status, votes) are world "
    "records with public_state values; visible_to_actor_ids names who can see them. (5) Each behavior the scenario "
    "says must be possible (raising concerns, meetings slowing, settled issues reopening, support becoming "
    "conditional, delay, deployment) is a behavior whose subject_refs name the people, records, items or moments it "
    "involves. (6) Ids are lowercase with underscores. (7) Anything the schema cannot represent goes in "
    "`unsupported` in plain words; never drop it silently."
)
SPEC_MODEL_WHY = ("The scenario spec is the whole world definition; the stronger tier is used for the same reason as "
                  "rule writing (see RULE_MODEL_WHY).")


class ActionField(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    type: Literal["entity_ref", "integer", "string", "boolean"]


class ActionSignature(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: str = Field(pattern=r"^[a-z][a-z0-9_-]*$")
    description: str = Field(min_length=1)
    fields: list[ActionField]
    for_behaviors: list[str] = Field(min_length=1)


class ActionSignatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    actions: list[ActionSignature]


def scenario_spec(text: str, *, model: str, trace_id: str, max_budget: float = 0.20):
    from llm_client import call_llm_structured
    spec, result = call_llm_structured(
        model, [{"role": "system", "content": SPEC_SYSTEM}, {"role": "user", "content": text}], ScenarioSpecV1,
        task="world-substrate-scenario-spec", trace_id=trace_id, max_budget=max_budget, reasoning_effort="medium",
        num_retries=1, model_justification=SPEC_MODEL_WHY)
    return spec, result


def action_signatures(spec: ScenarioSpecV1, bundle: dict[str, Any], coverage: dict[str, Any], *, model: str,
                      trace_id: str, max_budget: float = 0.05):
    """Action kinds people can attempt for the behaviors the compiler leaves to the generator (validated here)."""
    from llm_client import call_llm_structured
    wanted = [r for r in coverage["rows"] if r["classification"] == "to_generate"]
    if not wanted:
        return [], None
    context = {
        "people": [{"id": p.entity_id, "position": p.position} for p in spec.people],
        "behaviors_to_cover": wanted,
        "existing_actions": [a["kind"] for a in bundle["actions"]],
        "entities": [{"id": e["id"], "categories": e["categories"], "components": e["components"]}
                     for e in bundle["entities"] if "information" not in e["categories"]
                     and "delivery" not in e["categories"]],
    }
    sigs, result = call_llm_structured(
        model, [{"role": "system", "content": (
            "Propose the actions people can attempt so the listed behaviors can happen. An action is something a "
            "person chooses to try (hold a meeting, reopen an issue, attach a condition to support, vote, "
            "deploy); things that happen on their own each tick are processes and are not actions. Do not "
            "repeat an existing action. Fields name the entities or values the attempt needs (entity_ref for an "
            "entity). Name in for_behaviors the request_ids each action serves.")},
            {"role": "user", "content": json.dumps(context, indent=2)}],
        ActionSignatures, task="world-substrate-action-signatures", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort="low", num_retries=1)
    existing = {a["kind"] for a in bundle["actions"]}
    known = {r["request_id"] for r in wanted}
    out, seen = [], set()
    for a in sigs.actions:  # client-side validation: unique, new, serving a real behavior
        kind = a.kind.replace("_", "-")
        if kind in existing or kind in seen or not set(a.for_behaviors) & known:
            continue
        seen.add(kind)
        out.append({"kind": a.kind.replace("_", "-"), "description": a.description,  # bundle kinds use hyphens
                    "fields": [f.model_dump() for f in a.fields], "for_behaviors": a.for_behaviors})
    return out, result


def merge_causal(compiled: dict[str, Any], generated: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Compiled rules win: the reviewed communicate rule and the moment processes are never replaced."""
    kinds = {m["action_kind"] for m in compiled["mechanics"]}
    pids = {p["process_id"] for p in compiled["processes"]}
    dropped = [f"generated mechanic {m.get('mechanic_id')} dropped: action {m['action_kind']} is compiled"
               for m in generated.get("mechanics", []) if m["action_kind"] in kinds]
    dropped += [f"generated process {p['process_id']} dropped: id is compiled"
                for p in generated.get("processes", []) if p["process_id"] in pids]
    merged = {**{k: v for k, v in generated.items() if k not in ("mechanics", "processes")},
              "schema_version": compiled["schema_version"],
              "mechanics": compiled["mechanics"] + [m for m in generated.get("mechanics", [])
                                                    if m["action_kind"] not in kinds],
              "processes": compiled["processes"] + [p for p in generated.get("processes", [])
                                                    if p["process_id"] not in pids]}
    return merged, dropped


def person_briefs(spec: ScenarioSpecV1) -> dict[str, str]:
    """One brief per person, from its own profile (shown to that person's agent only)."""
    out = {}
    for p in spec.people:
        prof = p.behavioral_profile
        parts = [f"You are {p.label} ({p.position}). {p.disposition}"]
        for label, items in (("Your goals", prof.goals), ("You value", prof.values), ("You believe", prof.beliefs),
                             ("You tend to", prof.decision_tendencies), ("How you see others", prof.social_perceptions),
                             ("Right now", prof.current_state), ("You can", prof.capabilities),
                             ("You cannot", prof.limitations), ("You remember", p.memories)):
            if items:
                parts.append(f"{label}: " + "; ".join(items) + ".")
        held = [i for i in spec.information_items if i.holder_id == p.entity_id]
        if held:
            parts.append("You hold this information and may pass it on: " + " ".join(
                f"'{i.content}' (for {', '.join(i.recipient_ids)}, via {i.channel_id})." for i in held))
        out[re.sub(r"[^a-z0-9]+", "-", p.entity_id.lower()).strip("-")] = " ".join(parts)
    return out
