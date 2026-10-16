"""Compile a ScenarioSpecV1 into a World Substrate bundle and causal model (plan scenario-spec-adoption, check S2).

Deterministic, no model call. What compiles to what:
  person            -> an actor entity with the `member` component of the reviewed coordination family
  information item  -> one `information` entity per recipient (topic = the spec item id) plus a pending `delivery`;
                       the reviewed `communicate` rule (examples/native_coordination/coordination-causal-v0.json)
                       delivers it, unchanged. That rule sets `information.active`, so one entity carries one
                       delivery; an item for three recipients becomes three entities with the same topic.
  world record      -> an entity with one component named after the record, public and hidden fields alike
                       (hidden fields are prefixed `hidden_`; actor-scoped visibility is not enforced yet)
  scheduled moment  -> an entity with a `moment` countdown, driven by two processes (declarative rules cannot read
                       the world clock): `moment-countdown` lowers ticks_until each tick, `moment-occurs` fires at 0,
                       counts the occurrence and restarts the countdown from every_ticks (-1 means never again)
  behavior          -> a coverage row: `exact` when the compiled communicate rule produces it, otherwise
                       `to_generate` for the mechanics generator; unported parts stay `unsupported`
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from scenario_spec import ScenarioSpecV1

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
COORDINATION_CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"
BUNDLE_SCHEMA = "world-substrate-authoring-bundle/v0"

MEMBER = {"name": "member", "fields": [
    {"name": "role", "type": "string", "default": "participant"},
    {"name": "authorized", "type": "boolean", "default": False},
    {"name": "approved", "type": "boolean", "default": False},
    {"name": "aware", "type": "boolean", "default": False}]}
INFORMATION = {"name": "information", "fields": [
    {"name": "content", "type": "string", "default": "report"},
    {"name": "source_id", "type": "entity_ref", "default": "placeholder"},
    {"name": "channel_id", "type": "string", "default": "brief"},
    {"name": "visibility", "type": "string", "default": "direct"},
    {"name": "topic", "type": "string", "default": "coordination"},
    {"name": "active", "type": "boolean", "default": False}]}
DELIVERY = {"name": "delivery", "fields": [
    {"name": "info_id", "type": "entity_ref", "default": "placeholder"},
    {"name": "recipient_id", "type": "entity_ref", "default": "placeholder"},
    {"name": "channel_id", "type": "string", "default": "brief"},
    {"name": "status", "type": "string", "default": "pending"}]}
MOMENT = {"name": "moment", "fields": [
    {"name": "ticks_until", "type": "integer", "default": 0},
    {"name": "every_ticks", "type": "integer", "default": -1},
    {"name": "occurrences", "type": "integer", "default": 0},
    # True for the one round right after the moment occurs (the round people act in), false otherwise. ticks_until
    # is never 0 when people act: the same tick that reaches 0 restarts it (2026-10-16 Waltzman inc15a: four countries
    # waited 40 rounds for "the weekly meeting is due").
    {"name": "happening_now", "type": "boolean", "default": False}]}
COMMUNICATE_ACTION = {"kind": "communicate",
                      "description": "Deliver one represented information item to its declared recipient.",
                      "fields": [{"name": "information", "type": "entity_ref"},
                                 {"name": "delivery", "type": "entity_ref"},
                                 {"name": "recipient", "type": "entity_ref"}]}


# The group decision family (spec `decision`): exact rules for support, the concerns it may wait on, and the deadline.
# A concern is a `concern` component on the information entity it arrived in, so each recipient's concern is its own
# record and a rule binds it in one participant (discovery tries every combination, capped at 256).
SUPPORT = {"name": "support", "fields": [
    {"name": "holder_id", "type": "entity_ref", "default": "placeholder"},
    {"name": "stance", "type": "string", "default": "none"},  # none | full | conditional
    {"name": "condition_id", "type": "entity_ref", "default": "placeholder"}]}
CONCERN = {"name": "concern", "fields": [
    {"name": "recipient_id", "type": "entity_ref", "default": "placeholder"},
    {"name": "status", "type": "string", "default": "open"},  # open | remedy_under_way | resolved
    {"name": "remedy_ticks_left", "type": "integer", "default": 0},
    {"name": "times_resolved", "type": "integer", "default": 0},
    {"name": "times_reopened", "type": "integer", "default": 0}]}
GROUP_DECISION = {"name": "group_decision", "fields": [
    {"name": "question", "type": "string", "default": "decision"},
    {"name": "status", "type": "string", "default": "open"},  # open | authorized | rejected
    {"name": "support", "type": "integer", "default": 0},
    {"name": "conditional", "type": "integer", "default": 0},
    {"name": "needed", "type": "integer", "default": 1},
    {"name": "postponements", "type": "integer", "default": 0},
    {"name": "max_postponements", "type": "integer", "default": 0},
    {"name": "postpone_ticks", "type": "integer", "default": 1},
    {"name": "deadline_id", "type": "entity_ref", "default": "placeholder"}]}


def _ref(name: str, path: str) -> dict[str, Any]:
    return {"participant": {"name": name, "path": path}}


def _check(label: str, left: dict[str, Any], op: str, right: Any) -> dict[str, Any]:
    if not isinstance(right, dict):
        right = {"literal": right}
    return {"label": label, "left": left, "op": op, "right": right}


def _effect(participant: str, path: str, op: str, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        value = {"literal": value}
    return {"participant": participant, "path": path, "op": op, "value": value}


# A remedy takes this many rounds once started. 2026-10-16 inc15i (luna): with resolving instant, each country declared
# its own concern fixed in round 2 and nobody had anything left to do; a remedy under way gives the holder and the
# recipient a stretch in which support can wait on it.
REMEDY_TICKS = 2

_SUPPORT_SEL = {"categories": ["support"], "components": ["support"]}
_MATTER_SEL = {"categories": ["information"], "components": ["information", "concern"]}
_DECISION_SEL = {"categories": ["group-decision"], "components": ["group_decision"]}


def _mechanic(kind: str, rationale: str, participants: dict[str, Any], checks: list, effects: list) -> dict[str, Any]:
    return {"schema_version": "world-substrate-action-mechanic/v0", "mechanic_id": f"decision.action.{kind}",
            "version": "1", "action_kind": kind, "rationale": rationale,
            "actor_selector": {"categories": ["member"], "components": ["member"]}, "participants": participants,
            "parameters": {}, "checks": checks, "effects": effects,
            "limits": ["Compiled from the scenario's decision; the stance is represented, not inferred from talk."],
            "tests": ["tests/test_scenario_spec.py: the group decision moves support both ways and settles at its deadline"],
            "semantic_bindings": []}


def _decision_rules(has_deadline: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """(actions, mechanics, processes) of the group decision family."""
    own = _check("this is the actor's own support", _ref("support", "components.support.holder_id"), "eq",
                 {"entity_id": "actor"})
    is_open = _check("the decision is still open", _ref("decision", "components.group_decision.status"), "eq", "open")
    counts = lambda a, b: [_effect("decision", "components.group_decision.support", a, 1),  # noqa: E731
                           _effect("decision", "components.group_decision.conditional", b, 1)]
    mine = _check("the concern reached the actor", _ref("matter", "components.concern.recipient_id"), "eq",
                  {"entity_id": "actor"})
    arrived = _check("the concern has been delivered", _ref("matter", "components.information.active"), "eq", True)
    sd = {"support": _SUPPORT_SEL, "decision": _DECISION_SEL}
    smd = {**sd, "matter": _MATTER_SEL}
    mechanics = [
        _mechanic("give-support", "A decider who does not yet support the decision gives it full support.", sd,
                  [own, is_open, _check("the actor does not support it yet", _ref("support", "components.support.stance"),
                                        "eq", "none")],
                  [_effect("support", "components.support.stance", "set", "full"),
                   _effect("decision", "components.group_decision.support", "add", 1)]),
        _mechanic("make-support-conditional",
                  "A supporting decider who received an open concern makes its support wait on that concern.", smd,
                  [own, is_open, mine, arrived,
                   _check("the actor fully supports it", _ref("support", "components.support.stance"), "eq", "full"),
                   _check("the concern is open", _ref("matter", "components.concern.status"), "eq", "open")],
                  [_effect("support", "components.support.stance", "set", "conditional"),
                   _effect("support", "components.support.condition_id", "set", {"entity_id": "matter"}),
                   *counts("subtract", "add")]),
        _mechanic("restore-full-support",
                  "A decider whose condition's concern is resolved gives full support again.", smd,
                  [own, is_open,
                   _check("the actor's support is conditional", _ref("support", "components.support.stance"), "eq",
                          "conditional"),
                   _check("this is the concern the support waits on", _ref("support", "components.support.condition_id"),
                          "eq", {"entity_id": "matter"}),
                   _check("the concern is resolved", _ref("matter", "components.concern.status"), "eq", "resolved")],
                  [_effect("support", "components.support.stance", "set", "full"), *counts("add", "subtract")]),
        _mechanic("resolve-concern", f"Whoever holds a concern's information starts the remedy; {REMEDY_TICKS} rounds later the concern is resolved.",
                  {"matter": _MATTER_SEL},
                  [_check("the actor holds this information", _ref("matter", "components.information.source_id"), "eq",
                          {"entity_id": "actor"}), arrived,
                   _check("the concern is open", _ref("matter", "components.concern.status"), "eq", "open")],
                  [_effect("matter", "components.concern.status", "set", "remedy_under_way"),
                   _effect("matter", "components.concern.remedy_ticks_left", "set", REMEDY_TICKS)]),
        # 2026-10-16 Waltzman inc15g: only the holder could resolve, but many remedies sit with the person the concern
        # reached (a country obtaining its own authorization). The legal group rightly refused to resolve another
        # country's gap, so no concern was ever resolved and every country could only keep raising it.
        _mechanic("resolve-own-concern",
                  f"The person a concern reached starts the remedy on their own side; {REMEDY_TICKS} rounds later it is resolved.",
                  {"matter": _MATTER_SEL},
                  [mine, arrived,
                   _check("the concern is open", _ref("matter", "components.concern.status"), "eq", "open")],
                  [_effect("matter", "components.concern.status", "set", "remedy_under_way"),
                   _effect("matter", "components.concern.remedy_ticks_left", "set", REMEDY_TICKS)]),
        _mechanic("reopen-concern",
                  "The person a resolved concern reached finds the remedy wanting and reopens it while the decision is open.",
                  {"matter": _MATTER_SEL, "decision": _DECISION_SEL},
                  [mine, is_open, _check("the concern is resolved", _ref("matter", "components.concern.status"), "eq",
                                         "resolved")],
                  [_effect("matter", "components.concern.status", "set", "open"),
                   _effect("matter", "components.concern.times_reopened", "add", 1)]),
    ]
    if not has_deadline:
        mechanics.append(_mechanic(
            "call-decision", "A decider calls the decision once enough deciders fully support it.", sd,
            [own, is_open, _check("enough deciders fully support it", _ref("decision", "components.group_decision.support"),
                                  "gte", _ref("decision", "components.group_decision.needed"))],
            [_effect("decision", "components.group_decision.status", "set", "authorized")]))
    fields = {"give-support": ["support", "decision"], "make-support-conditional": ["support", "decision", "matter"],
              "restore-full-support": ["support", "decision", "matter"], "resolve-concern": ["matter"], "resolve-own-concern": ["matter"],
              "reopen-concern": ["matter", "decision"], "call-decision": ["support", "decision"]}
    actions = [{"kind": m["action_kind"], "description": m["rationale"],
                "fields": [{"name": f, "type": "entity_ref"} for f in fields[m["action_kind"]]]} for m in mechanics]
    concern_it = lambda path: _ref("it", f"components.concern.{path}")  # noqa: E731
    concern_sel = {"categories": ["information"], "components": ["information", "concern"]}
    under_way = _check("a remedy is under way", concern_it("status"), "eq", "remedy_under_way")
    # Completion is listed before progress: processes apply in sequence within a tick, so the other order would
    # finish a remedy one round early.
    processes = [
        {"process_id": "remedy-completes", "rationale": "A remedy under way that has run its course resolves the concern.",
         "selector": concern_sel,
         "checks": [under_way, _check("the remedy is in its last round", concern_it("remedy_ticks_left"), "lte", 1)],
         "effects": [_effect("it", "components.concern.status", "set", "resolved"),
                     _effect("it", "components.concern.remedy_ticks_left", "set", 0),
                     _effect("it", "components.concern.times_resolved", "add", 1)]},
        {"process_id": "remedy-progresses", "rationale": "A remedy under way moves one round closer to done.",
         "selector": concern_sel,
         "checks": [under_way, _check("the remedy has rounds to go", concern_it("remedy_ticks_left"), "gt", 1)],
         "effects": [_effect("it", "components.concern.remedy_ticks_left", "subtract", 1)]},
    ]
    if has_deadline:
        it = lambda path: _ref("it", f"components.group_decision.{path}")  # noqa: E731
        sel = {"categories": ["group-decision"], "components": ["group_decision"]}
        deadline = {"deadline": {"link": "ref:group_decision.deadline_id",
                                 "selector": {"categories": ["moment"], "components": ["moment"]}}}
        due = [_check("the decision is still open", it("status"), "eq", "open"),
               _check("the deadline is happening now", _ref("deadline", "components.moment.happening_now"), "eq", True)]
        enough = lambda op: _check("enough deciders fully support it" if op == "gte" else  # noqa: E731
                                   "too few deciders fully support it", it("support"), op, it("needed"))
        processes += [
            {"process_id": "decision-authorized-at-deadline",
             "rationale": "At the deadline, enough full support authorizes the decision.", "selector": sel,
             "participants": deadline, "checks": [*due, enough("gte")],
             "effects": [_effect("it", "components.group_decision.status", "set", "authorized")]},
            {"process_id": "decision-rejected-at-deadline",
             "rationale": "At the deadline, too little full support with no postponements left rejects the decision.",
             "selector": sel, "participants": deadline,
             "checks": [*due, enough("lt"), _check("no postponements remain", it("postponements"), "gte",
                                                   it("max_postponements"))],
             "effects": [_effect("it", "components.group_decision.status", "set", "rejected")]},
            # after rejection: processes apply in order within a tick, so a postponement that used the last one
            # would otherwise let rejection fire in the same tick
            {"process_id": "decision-postponed-at-deadline",
             "rationale": "At the deadline, too little full support postpones the decision and sets a new deadline.",
             "selector": sel, "participants": deadline,
             "checks": [*due, enough("lt"), _check("postponements remain", it("postponements"), "lt",
                                                   it("max_postponements"))],
             "effects": [_effect("it", "components.group_decision.postponements", "add", 1),
                         _effect("deadline", "components.moment.ticks_until", "set", it("postpone_ticks"))]},
        ]
    return actions, mechanics, processes


def _eid(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _field_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    return "string"


def _moment_processes() -> list[dict[str, Any]]:
    it = lambda path: {"participant": {"name": "it", "path": f"components.moment.{path}"}}  # noqa: E731
    selector = {"categories": ["moment"], "components": ["moment"]}
    return [
        # Listed first, so it runs before moment-occurs in a tick: a moment that occurred last tick is over now.
        {"process_id": "moment-passes", "rationale": "A moment that happened last round is over.",
         "selector": selector,
         "checks": [{"label": "the moment is happening", "left": it("happening_now"), "op": "eq", "right": {"literal": True}}],
         "effects": [{"participant": "it", "path": "components.moment.happening_now", "op": "set",
                      "value": {"literal": False}}]},
        {"process_id": "moment-countdown", "rationale": "A scheduled moment's countdown falls by one each tick.",
         "selector": selector,
         "checks": [{"label": "the moment is still ahead", "left": it("ticks_until"), "op": "gt", "right": {"literal": 0}}],
         "effects": [{"participant": "it", "path": "components.moment.ticks_until", "op": "subtract",
                      "value": {"literal": 1}}]},
        {"process_id": "moment-occurs", "rationale": "At zero the moment happens once, then restarts its countdown.",
         "selector": selector,
         "checks": [{"label": "the moment is due", "left": it("ticks_until"), "op": "eq", "right": {"literal": 0}}],
         "effects": [{"participant": "it", "path": "components.moment.occurrences", "op": "add", "value": {"literal": 1}},
                     {"participant": "it", "path": "components.moment.happening_now", "op": "set",
                      "value": {"literal": True}},
                     {"participant": "it", "path": "components.moment.ticks_until", "op": "set",
                      "value": it("every_ticks")}]},
    ]


def compile_spec(spec: ScenarioSpecV1) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return (bundle, causal, coverage). Ids in the world are the spec ids with '_' turned into '-'."""
    entities: list[dict[str, Any]] = []
    components = [MEMBER, INFORMATION, DELIVERY]
    for p in spec.people:
        entities.append({"id": _eid(p.entity_id), "label": p.label, "categories": ["actor", "member"],
                         "components": {"member": {"role": p.position, "authorized": False, "approved": False,
                                                   "aware": False}}})
    for item in spec.information_items:
        for r in item.recipient_ids:
            info_id = f"info-{_eid(item.representation_id)}-to-{_eid(r)}"
            entities.append({"id": info_id, "label": f"{item.content[:60]} (to {r})", "categories": ["information"],
                             "components": {"information": {"content": item.content, "source_id": _eid(item.holder_id),
                                                            "channel_id": item.channel_id, "visibility": "direct",
                                                            "topic": item.representation_id, "active": False}}})
            entities.append({"id": f"delivery-{info_id}", "label": f"Delivery to {r}", "categories": ["delivery"],
                             "components": {"delivery": {"info_id": info_id, "recipient_id": _eid(r),
                                                         "channel_id": item.channel_id, "status": "pending"}}})
    for rec in spec.world_records:
        name = rec.record_id
        fields = [(e.key, e.value) for e in rec.public_state] + [(f"hidden_{e.key}", e.value) for e in rec.hidden_state]
        fields = [(k, v) for k, v in fields if not isinstance(v, list) and v is not None]
        components.append({"name": name, "fields": [{"name": k, "type": _field_type(v), "default": v} for k, v in fields]})
        # its own id as a category too, so a rule slot named after this record can be pinned to it (spec_pipeline.pin_named_slots)
        entities.append({"id": _eid(rec.record_id), "label": rec.label, "categories": [_eid(rec.kind), _eid(rec.record_id)],
                         "components": {name: dict(fields)}})
    if spec.scheduled_moments:
        components.append(MOMENT)
    for m in spec.scheduled_moments:
        entities.append({"id": _eid(m.moment_id), "label": m.description[:80], "categories": ["moment", _eid(m.moment_id)],
                         "components": {"moment": {"ticks_until": m.tick, "every_ticks": m.every_ticks or -1,
                                                   "occurrences": 0, "happening_now": False}}})
    decision_actions: list[dict[str, Any]] = []
    decision_mechanics: list[dict[str, Any]] = []
    decision_processes: list[dict[str, Any]] = []
    if d := spec.decision:
        components += [SUPPORT, CONCERN, GROUP_DECISION]
        for e in entities:  # every delivered item is a concern its recipient may wait on
            if "information" in e["categories"]:
                recipient = next(x for x in entities if x["id"] == f"delivery-{e['id']}")["components"]["delivery"][
                    "recipient_id"]
                e["components"]["concern"] = {"recipient_id": recipient, "status": "open", "remedy_ticks_left": 0, "times_resolved": 0,
                                              "times_reopened": 0}
        starting = set(d.supporters_at_start)
        for pid in dict.fromkeys(d.decider_ids):
            entities.append({"id": f"support-{_eid(pid)}", "label": f"Support of {pid}", "categories": ["support"],
                             "components": {"support": {"holder_id": _eid(pid),
                                                        "stance": "full" if pid in starting else "none",
                                                        "condition_id": _eid(pid)}}})
        entities.append({"id": _eid(d.decision_id), "label": d.question[:80],
                         "categories": ["group-decision", _eid(d.decision_id)],
                         "components": {"group_decision": {
                             "question": d.question, "status": "open", "support": len(starting), "conditional": 0,
                             "needed": d.support_needed, "postponements": 0,
                             "max_postponements": 0 if d.if_short_at_deadline == "reject" else d.max_postponements,
                             "postpone_ticks": d.postpone_ticks,
                             "deadline_id": _eid(d.deadline_moment_id) if d.deadline_moment_id else _eid(d.decision_id)}}})
        decision_actions, decision_mechanics, decision_processes = _decision_rules(bool(d.deadline_moment_id))
    bundle = {"schema_version": BUNDLE_SCHEMA,
              "world": {"id": _eid(spec.scenario_id), "label": spec.title, "summary": spec.description[:400],
                        "location": "scenario", "content_version": 1},
              "components": components, "entities": entities, "actions": [COMMUNICATE_ACTION, *decision_actions],
              "presentation": {"assets": {"participant": {"kind": "emoji", "value": "\U0001F464"},
                                          "information": {"kind": "emoji", "value": "✉️"},
                                          "delivery": {"kind": "text", "value": "→"}},
                               "category_assets": {"member": "participant", "information": "information",
                                                   "delivery": "delivery"}, "station_roles": {}}}
    communicate = json.loads(COORDINATION_CAUSAL.read_text())["mechanics"][0]
    causal = {"schema_version": "world-substrate-causal-model/v0", "mechanics": [communicate, *decision_mechanics],
              # deadline processes after the moment ones: they read happening_now, set this tick by moment-occurs
              "processes": (_moment_processes() if spec.scheduled_moments else []) + decision_processes}
    # Delivery alone is exact: a behavior whose subjects are only people and information items (and include an
    # item) is what communicate does. Anything that also involves a record or a moment (a meeting slowing, support
    # becoming conditional) needs rules of its own, so it goes to the generator even though it mentions an item.
    item_ids = {i.representation_id for i in spec.information_items}
    people_ids = {p.entity_id for p in spec.people}
    delivery = lambda b: bool(set(b.subject_refs) & item_ids) and set(b.subject_refs) <= item_ids | people_ids  # noqa: E731
    # A behavior naming the decision stays to_generate: it may also need rules of its own (a delay, a deployment);
    # the generated rules may read the decision's records but never write them (spec_pipeline.COMPILED_COMPONENTS).
    rows = [{"request_id": b.request_id, "behavior": b.behavior_description,
             "classification": "exact" if delivery(b) else "to_generate",
             "by": "communicate" if delivery(b) else None} for b in spec.behaviors]
    coverage = {"rows": rows, "unsupported": list(spec.unsupported)}
    return bundle, causal, coverage
