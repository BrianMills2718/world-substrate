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
    {"name": "occurrences", "type": "integer", "default": 0}]}
COMMUNICATE_ACTION = {"kind": "communicate",
                      "description": "Deliver one represented information item to its declared recipient.",
                      "fields": [{"name": "information", "type": "entity_ref"},
                                 {"name": "delivery", "type": "entity_ref"},
                                 {"name": "recipient", "type": "entity_ref"}]}


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
        {"process_id": "moment-countdown", "rationale": "A scheduled moment's countdown falls by one each tick.",
         "selector": selector,
         "checks": [{"label": "the moment is still ahead", "left": it("ticks_until"), "op": "gt", "right": {"literal": 0}}],
         "effects": [{"participant": "it", "path": "components.moment.ticks_until", "op": "subtract",
                      "value": {"literal": 1}}]},
        {"process_id": "moment-occurs", "rationale": "At zero the moment happens once, then restarts its countdown.",
         "selector": selector,
         "checks": [{"label": "the moment is due", "left": it("ticks_until"), "op": "eq", "right": {"literal": 0}}],
         "effects": [{"participant": "it", "path": "components.moment.occurrences", "op": "add", "value": {"literal": 1}},
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
        entities.append({"id": _eid(rec.record_id), "label": rec.label, "categories": [_eid(rec.kind)],
                         "components": {name: dict(fields)}})
    if spec.scheduled_moments:
        components.append(MOMENT)
    for m in spec.scheduled_moments:
        entities.append({"id": _eid(m.moment_id), "label": m.description[:80], "categories": ["moment"],
                         "components": {"moment": {"ticks_until": m.tick, "every_ticks": m.every_ticks or -1,
                                                   "occurrences": 0}}})
    bundle = {"schema_version": BUNDLE_SCHEMA,
              "world": {"id": _eid(spec.scenario_id), "label": spec.title, "summary": spec.description[:400],
                        "location": "scenario", "content_version": 1},
              "components": components, "entities": entities, "actions": [COMMUNICATE_ACTION],
              "presentation": {"assets": {"participant": {"kind": "emoji", "value": "\U0001F464"},
                                          "information": {"kind": "emoji", "value": "✉️"},
                                          "delivery": {"kind": "text", "value": "→"}},
                               "category_assets": {"member": "participant", "information": "information",
                                                   "delivery": "delivery"}, "station_roles": {}}}
    communicate = json.loads(COORDINATION_CAUSAL.read_text())["mechanics"][0]
    causal = {"schema_version": "world-substrate-causal-model/v0", "mechanics": [communicate],
              "processes": _moment_processes() if spec.scheduled_moments else []}
    item_ids = {i.representation_id for i in spec.information_items}
    rows = [{"request_id": b.request_id, "behavior": b.behavior_description,
             "classification": "exact" if set(b.subject_refs) & item_ids else "to_generate",
             "by": "communicate" if set(b.subject_refs) & item_ids else None} for b in spec.behaviors]
    coverage = {"rows": rows, "unsupported": list(spec.unsupported)}
    return bundle, causal, coverage
