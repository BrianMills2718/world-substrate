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
    "Define a simulation world from the scenario using the schema. Every named actor has its own profile and memory. "
    "Profiles contain that actor's beliefs, not omniscient truth or required reactions. Claims may be false or disputed; "
    "information_items preserve the holder, intended recipients, apparent source, common source_lineage and hidden provenance. "
    "Separate actual technical state from claims, delivery, personal interpretation, public stance, recorded assent and institutional holds. "
    "Write public_summary using only facts explicitly shared by all actors before any delivery; never copy the omniscient description. "
    "World records declare visible_to_actor_ids for public_state; hidden_state stays private. Use stable neutral labels without private facts. "
    "Each actor's memories and profile contain only their declared knowledge, own interpretations and plausible personal tendencies. "
    "Do not copy narrator statements of withheld information into an actor's profile: 'Bo has not received the failure report' "
    "would itself tell Bo a failure report exists, and 'Mara was not given channel C or batch V17 detail' would reveal C and V17. "
    "Omit such narrator-only negatives entirely; do not replace them with invented beliefs. Personality, goals, ordinary preferences "
    "and explicitly held beliefs remain actor-facing, whether or not those beliefs are true. "
    "For information already received at the start use initially_delivered=true, holder_id as the receiving holder, "
    "recipient_ids including the holder, and source_id as the actual source person only when the source names one; "
    "otherwise leave source_id null rather than inventing a sender. Apparent source is a reported attribution, not proof "
    "of actual origin. A pending item defaults to "
    "initially_delivered=false and must not appear in an intended recipient's brief or memories. "
    "Use independent_decision for fresh collective activation/approval scenarios involving technical validation: declare required_actor_ids, "
    "validator_ids, repairer_ids, condition_initially_passing and initial_validation. This compiles actor-owned public stance and assent, "
    "requests for review, authorized repair and actual validation, a public technical hold and activation checks. "
    "A failed validation creates the hold; authorized passing revalidation clears only that hold. Repair is a declared effective technical intervention, "
    "never the passing of time. Reports never alter the technical condition or force agreement or assent. "
    "Use legacy decision only for explicitly stipulated scripted conditional-support fixtures, not as a model of persuasion. "
    "Do not duplicate compiled decision, condition, stance or assent records as world_records. "
    "Regular meetings/deadlines may be scheduled_moments. Behaviors state possibilities, never prescribed actor responses. "
    "Use lowercase underscore ids. List omitted unsupported details and invented fidelity assumptions explicitly. "
    "No ending, social reaction, timer cure or recurrent conflict is required. Actors may disagree, ignore evidence or retain support."
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


def scenario_spec(text: str, *, model: str, trace_id: str, max_budget: float = 0.20, reasoning_effort: str = "medium",
                  route_policy: Any = None):
    """``route_policy`` is an llm_client OpenRouterRoutePolicyV1 (the World Builder asks for the fastest provider)."""
    from llm_client import call_llm_structured
    spec, result = call_llm_structured(
        model, [{"role": "system", "content": SPEC_SYSTEM}, {"role": "user", "content": text}], ScenarioSpecV1,
        task="world-substrate-scenario-spec", trace_id=trace_id, max_budget=max_budget, reasoning_effort=reasoning_effort,
        num_retries=1, model_justification=SPEC_MODEL_WHY,
        **({"openrouter_route_policy": route_policy} if route_policy else {}))
    from scripts.generate_world_bundle import is_recorded_authoring_replay
    if not spec.public_summary.strip() and not is_recorded_authoring_replay():
        raise ValueError("Fresh scenario authoring requires an explicit actor-safe public_summary")
    return spec, result


def action_signatures(spec: ScenarioSpecV1, bundle: dict[str, Any], coverage: dict[str, Any], *, model: str,
                      trace_id: str, max_budget: float = 0.05, guidance: str = "", reasoning_effort: str = "low",
                      route_policy: Any = None):
    """Action kinds people can attempt for the behaviors the compiler leaves to the generator (validated here).
    ``guidance`` is appended to the instructions (the World Builder adds its keep-running rules)."""
    from llm_client import call_llm_structured
    wanted = [r for r in coverage["rows"] if r["classification"] == "to_generate"]
    if not wanted:
        return [], None
    context = {
        "people": [{"id": p.entity_id, "position": p.position} for p in spec.people],
        "behaviors_to_cover": wanted,
        # Kinds alone hid what the compiled actions do, so the writer re-proposed them (inc15g: its own postpone,
        # reject and concern-raising actions beside the compiled decision).
        "existing_actions": [{"kind": a["kind"], "description": a.get("description", "")} for a in bundle["actions"]],
        "entities": [{"id": e["id"], "categories": e["categories"], "components": e["components"]}
                     for e in bundle["entities"] if "information" not in e["categories"]
                     and "delivery" not in e["categories"]],
    }
    sigs, result = call_llm_structured(
        model, [{"role": "system", "content": (
            "Propose the actions people can attempt so the listed behaviors can happen. An action is something a "
            "person chooses to try (hold a meeting, reopen an issue, attach a condition to support, vote, "
            "deploy); things that happen on their own each tick are processes and are not actions. Do not "
            "repeat an existing action or propose another that does what one already does. Fields name the entities or values the attempt needs (entity_ref for an "
            "entity); the person attempting it is implied, so never add an actor field. Name in for_behaviors the request_ids each action serves." + (" " + guidance if guidance else ""))},
            {"role": "user", "content": json.dumps(context, indent=2)}],
        ActionSignatures, task="world-substrate-action-signatures", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort=reasoning_effort, num_retries=1,
        **({"openrouter_route_policy": route_policy} if route_policy else {}))
    existing = {a["kind"] for a in bundle["actions"]}
    known = {r["request_id"] for r in wanted}
    out, seen = [], set()
    for a in sigs.actions:  # client-side validation: unique, new, serving a real behavior
        kind = a.kind.replace("_", "-")
        if kind in existing or kind in seen or not set(a.for_behaviors) & known:
            continue
        seen.add(kind)
        fields, names = [], set()
        for f in a.fields:  # the engine supplies who acts and the bookkeeping fields; a repeated name is one field
            if f.name in RESERVED_ACTION_FIELDS or f.name in names:
                continue
            names.add(f.name)
            fields.append(f.model_dump())
        out.append({"kind": a.kind.replace("_", "-"), "description": a.description,  # bundle kinds use hyphens
                    "fields": fields, "for_behaviors": a.for_behaviors})
    return out, result


# Action fields the engine fills itself (scripts/scaffold_world.py RESERVED_ACTION_FIELDS, which rejects a bundle that
# declares them). 2026-10-16: a generated action declared "actor" and the whole Waltzman build failed.
RESERVED_ACTION_FIELDS = {"actor", "kind", "base_revision", "controller"}

COMPILED_COMPONENTS = ("information", "delivery", "moment", "support", "concern", "group_decision",
                       "claim_provenance", "technical_condition", "validation_decision", "actor_position", "technical_role",
                       "report_log")  # written only by the compiled rules


# The one compiled field a generated move may write: matters put before a group decision (compile_spec GROUP_DECISION).
GENERATED_MAY_WRITE = ("components.group_decision.agenda_items",)


def _writes_compiled(effect: dict[str, Any], *, by_move: bool = False) -> bool:
    if by_move and effect["path"] in GENERATED_MAY_WRITE and effect.get("op") in {"add", "subtract"}:
        return False
    return any(effect["path"].startswith(f"components.{c}.") for c in COMPILED_COMPONENTS)


# The one compiled write a generated process may make (#128, attempt from belief): stop a remedy part-way. The
# compiled resolve rules start a remedy and the compiled remedy processes finish it after its rounds; nothing could
# make one fail, so a person never learned that their fix did not hold. A world process may now put the concern
# back to open when something the remedy needs is gone, and only while the remedy is under way.
REMEDY_STOP = {("components.concern.status", "open"), ("components.concern.remedy_ticks_left", 0)}


def _stops_remedy(process: dict[str, Any]) -> bool:
    """Every compiled write of this process stops a remedy under way on the concern it checks."""
    watched = {(c["left"]["participant"]["name"]) for c in process.get("checks", [])
               if c.get("op") == "eq" and isinstance(c.get("left"), dict) and "participant" in c["left"]
               and c["left"]["participant"].get("path") == "components.concern.status"
               and (c.get("right") or {}).get("literal") == "remedy_under_way"}
    writes = [e for e in process.get("effects", []) if _writes_compiled(e)]
    return bool(watched and writes) and all(
        e.get("op") == "set" and e.get("participant") in watched
        and (e["path"], (e.get("value") or {}).get("literal", object())) in REMEDY_STOP for e in writes)


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
        kept = [e for e in m.get("effects", []) if not _writes_compiled(e, by_move=True)]
        if len(kept) < len(m.get("effects", [])):
            dropped.append(f"generated mechanic {m.get('mechanic_id')}: effects on compiled components removed")
        if not kept:
            dropped.append(f"generated mechanic {m.get('mechanic_id')} dropped: no effects left")
            continue
        mechanics.append({**m, "effects": kept})
    processes = []
    for p in generated.get("processes", []):
        if p["process_id"] in pids or (any(_writes_compiled(e) for e in p.get("effects", [])) and not _stops_remedy(p)):
            dropped.append(f"generated process {p['process_id']} dropped: it writes what a compiled rule owns")
            continue
        processes.append(p)
    merged = {**{k: v for k, v in generated.items() if k not in ("mechanics", "processes")},
              "schema_version": compiled["schema_version"],
              "mechanics": compiled["mechanics"] + mechanics, "processes": compiled["processes"] + processes}
    return merged, dropped


DECISION_STATUS = "components.group_decision.status"


def drop_decision_copies(causal: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """A generated move that reads the decision's status and sets a record to a value no rule ever sets back copies
    the decision into that record, which then contradicts it once the decision moves on. The copy is removed: the
    decision's own status says whether it is in effect (#128 slice 2, E4). 2026-10-23 c1r20: the partnership's
    deploy move set `activation_state` to 'activated' while the decision was authorized (r9-e00009); authorization
    was withdrawn in round 15, and people said "the system is already activated" for 35 rounds.
    A move that writes one of the decision's own later statuses into another record is a copy too, even when other
    rules set that record to other values. 2026-10-23 c1r22: the same deploy move set the readiness record (ready,
    logistics_staged, ...) to 'deployed' at r10-e00009 while the decision was authorized and rolling out until
    r14-e00004, and six people said "the system is already deployed" during the rollout (r11, r12)."""
    rules = [*causal.get("mechanics", []), *causal.get("processes", [])]
    def values(path: str) -> set[str]:
        return {repr((e.get("value") or {}).get("literal")) for r in rules for e in r.get("effects", [])
                if e.get("path") == path and e.get("op") == "set"}
    decision_states = values(DECISION_STATUS) - {repr("open")}  # every status the decision moves to after it opens
    dropped = []
    for m in causal.get("mechanics", []):
        if m.get("mechanic_id", "").startswith("decision.") or not any(
                isinstance(c.get(side), dict) and (c[side].get("participant") or {}).get("path") == DECISION_STATUS
                for c in m.get("checks", []) for side in ("left", "right")):
            continue
        kept = []
        for e in m.get("effects", []):
            value = e.get("value") or {}
            one_way = (e.get("op") == "set" and "literal" in value and not isinstance(value["literal"], bool)
                       and e.get("path") != DECISION_STATUS
                       and (values(e["path"]) == {repr(value["literal"])} or repr(value["literal"]) in decision_states))
            if one_way:
                dropped.append(f"generated mechanic {m['mechanic_id']}: setting {e['path'].removeprefix('components.')} "
                               f"to {value['literal']!r} removed: it copied the decision's status into a record no "
                               "rule sets back, so it would contradict the decision once it moves on")
            else:
                kept.append(e)
        m["effects"] = kept
    return causal, dropped


def pin_named_slots(spec: ScenarioSpecV1, causal: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """A rule slot named after a specific record or moment accepts only that entity. Without this, a slot named
    `activation_decision_deadline` (category `moment`) accepted the weekly meeting, and an agent blocked deployment
    at tick 5 because the meeting had occurred 5 times (run-20261008T184545, event e00047)."""
    named = {r.record_id: r.record_id for r in spec.world_records} | {m.moment_id: m.moment_id for m in spec.scheduled_moments}
    pinned = []
    for m in causal.get("mechanics", []):
        for slot, selector in (m.get("participants") or {}).items():
            if slot in named:
                eid = named[slot].replace("_", "-")
                if selector.get("categories") != [eid]:
                    selector["categories"] = [eid]
                    pinned.append(f"{m.get('mechanic_id')}.{slot} -> {eid}")
    return causal, pinned


def fix_moment_due_checks(causal: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """A generated action check "ticks_until == 0" can never pass: the tick that brings a moment to 0 also restarts
    it, before anyone acts (2026-10-16 Waltzman inc15a: "the weekly meeting is due" kept four countries waiting 40
    rounds). What the rule means is "the moment is on now", which the compiled `happening_now` field says."""
    fixed = []
    for m in causal.get("mechanics", []):
        for check in m.get("checks") or []:
            for side, other in (("left", "right"), ("right", "left")):
                ref = (check.get(side) or {}).get("participant") if isinstance(check.get(side), dict) else None
                if (isinstance(ref, dict) and ref.get("path") == "components.moment.ticks_until"
                        and check.get("op") == "eq" and check.get(other) == {"literal": 0}):
                    check[side] = {"participant": {**ref, "path": "components.moment.happening_now"}}
                    check[other] = {"literal": True}
                    fixed.append(f"{m.get('mechanic_id')}: check '{check.get('label')}' reads happening_now "
                                 "(ticks_until is never 0 when people act)")
    return causal, fixed


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
            if spec.independent_decision:
                # This index only maps generated signatures. Absence here cannot
                # prove absence from compiled procedure or resident cognition.
                row["classification"] = "unverified"
                row["why"] = "No generated-action mapping; coverage by compiled procedure or resident choice needs source review."
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
        # Modern contexts expose held/received reports through the canonical
        # information and delivery projection. Repeating the narrator's item
        # description here can contradict initial delivery or reveal metadata
        # the declared projection withholds. Preserve historical brief text only
        # for legacy worlds that have no actor-information declaration.
        held = ([i for i in spec.information_items if i.holder_id == p.entity_id]
                if not spec.public_summary and not spec.independent_decision else [])
        if held:
            parts.append("You hold this information and may pass it on: " + " ".join(
                f"'{i.content}' (for {', '.join(i.recipient_ids)}, via {i.channel_id})." for i in held))
        out[re.sub(r"[^a-z0-9]+", "-", p.entity_id.lower()).strip("-")] = " ".join(parts)
    return out
