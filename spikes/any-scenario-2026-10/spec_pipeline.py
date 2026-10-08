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


COMPILED_COMPONENTS = ("information", "delivery", "moment")  # written only by the compiled rules


def _writes_compiled(effect: dict[str, Any]) -> bool:
    return any(effect["path"].startswith(f"components.{c}.") for c in COMPILED_COMPONENTS)


def merge_causal(compiled: dict[str, Any], generated: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Compiled rules win. The reviewed communicate rule and the moment processes are never replaced, and only they
    write the information, delivery and moment components: a generated process that writes one is dropped (it would,
    for example, count a meeting down twice per tick), and a generated action loses those effects (dropped if none
    remain). Every drop is recorded."""
    kinds = {m["action_kind"] for m in compiled["mechanics"]}
    pids = {p["process_id"] for p in compiled["processes"]}
    dropped: list[str] = []
    mechanics = []
    for m in generated.get("mechanics", []):
        if m["action_kind"] in kinds:
            dropped.append(f"generated mechanic {m.get('mechanic_id')} dropped: action {m['action_kind']} is compiled")
            continue
        kept = [e for e in m.get("effects", []) if not _writes_compiled(e)]
        if len(kept) < len(m.get("effects", [])):
            dropped.append(f"generated mechanic {m.get('mechanic_id')}: effects on compiled components removed")
        if not kept:
            dropped.append(f"generated mechanic {m.get('mechanic_id')} dropped: no effects left")
            continue
        mechanics.append({**m, "effects": kept})
    processes = []
    for p in generated.get("processes", []):
        if p["process_id"] in pids or any(_writes_compiled(e) for e in p.get("effects", [])):
            dropped.append(f"generated process {p['process_id']} dropped: it writes what a compiled rule owns")
            continue
        processes.append(p)
    merged = {**{k: v for k, v in generated.items() if k not in ("mechanics", "processes")},
              "schema_version": compiled["schema_version"],
              "mechanics": compiled["mechanics"] + mechanics, "processes": compiled["processes"] + processes}
    return merged, dropped


def record_fields(spec: ScenarioSpecV1, sigs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Give each action an entity field for every world record or moment its behaviors involve, so its rule can
    change them (the signature call proposes people fields; without these no rule can reach a record)."""
    targets = {r.record_id for r in spec.world_records} | {m.moment_id for m in spec.scheduled_moments}
    subjects = {b.request_id: [s for s in b.subject_refs if s in targets] for b in spec.behaviors}
    out = []
    for a in sigs:
        fields = list(a["fields"])
        names = {f["name"] for f in fields}
        for req in a["for_behaviors"]:
            for subject in subjects.get(req, []):
                if subject not in names:
                    fields.append({"name": subject, "type": "entity_ref"})
                    names.add(subject)
        out.append({**a, "fields": fields})
    return out


def behavior_coverage(spec: ScenarioSpecV1, sigs: list[dict[str, Any]], causal: dict[str, Any],
                      coverage: dict[str, Any]) -> dict[str, Any]:
    """A generated behavior is `coarse` only if a rule of one of its actions changes one of the behavior's own records
    or moments (or, for a behavior about people only, changes anything); otherwise `unsupported`."""
    targets = {r.record_id for r in spec.world_records} | {m.moment_id for m in spec.scheduled_moments}
    subjects = {b.request_id: {s for s in b.subject_refs if s in targets} for b in spec.behaviors}
    for row in coverage["rows"]:
        if row["classification"] != "to_generate":
            continue
        kinds = {a["kind"] for a in sigs if row["request_id"] in a["for_behaviors"]}
        rules = [m for m in causal["mechanics"] if m["action_kind"] in kinds]
        wanted = subjects.get(row["request_id"], set())
        hits = [m["mechanic_id"] for m in rules
                if any((e.get("participant") in wanted) if wanted else True for e in m.get("effects", []))]
        row["by"] = hits or None
        row["classification"] = "coarse" if hits else "unsupported"
        if not hits:
            row["why"] = ("no rule changes " + ", ".join(sorted(wanted))) if wanted else "no rule for this behavior"
    return coverage


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
