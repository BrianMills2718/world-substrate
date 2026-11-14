"""Author the small inhabited pump facility (laboratory, corridor, control room, two doors).

Implements: information-delivery/place-scoped-perception-with-distinct-inputs
The output is a deterministic authored bundle plus rules for the existing runner; nothing here is an engine,
scheduler or renderer. Run `python scripts/build_pump_facility_example.py` to rewrite the two example files.
Places are topology (rooms joined by doors), not coordinates. Each door is two directed boundaries so a person can
walk either way; opening a door sets both halves.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "examples/world_authoring"

PLACES = {"laboratory": "Laboratory", "corridor": "Corridor", "control-room": "Control room"}
# door id -> (label, from place, to place, partner id)
DOORS = {
    "lab-door-out": ("Laboratory door", "laboratory", "corridor", "lab-door-in"),
    "lab-door-in": ("Laboratory door (corridor side)", "corridor", "laboratory", "lab-door-out"),
    "control-door-out": ("Control room door (corridor side)", "corridor", "control-room", "control-door-in"),
    "control-door-in": ("Control room door", "control-room", "corridor", "control-door-out"),
}
PEOPLE = {  # id: (label, role, place, brief)
    "ari": ("Ari", "validation engineer", "laboratory",
            "You are Ari, the validation engineer. You work in the laboratory with the prototype pump and report to Bo."),
    "mara": ("Mara", "coordinator", "corridor",
             "You are Mara, the coordinator. You walk the corridor and relay what people tell you."),
    "bo": ("Bo", "pump operator", "control-room",
           "You are Bo, the pump operator. You stay at the control room console and decide whether to start the pump."),
}
SHARED = ("Ari, Mara and Bo work in a small pump facility: a laboratory with the prototype pump, a corridor, and a "
          "control room. The laboratory door and the control room door start closed. Everyone knows the layout.")
KNOWLEDGE = {"bo": "The pump was last started two weeks ago and has not been calibrated since.",
             "ari": "The pump needs calibration before anyone starts it."}


def ref(name: str, path: str) -> dict:
    return {"participant": {"name": name, "path": path}}


def check(label: str, left: dict, right: dict, op: str = "eq") -> dict:
    return {"label": label, "left": left, "op": op, "right": right}


def mechanic(kind: str, rationale: str, participants: dict, checks: list, effects: list, limits: list,
             parameters: dict | None = None) -> dict:
    return {"schema_version": "world-substrate-action-mechanic/v0", "mechanic_id": "facility." + kind, "version": "1",
            "action_kind": kind, "rationale": rationale,
            "actor_selector": {"categories": ["actor"], "components": []},
            "participants": participants, "parameters": parameters or {}, "checks": checks, "effects": effects,
            "limits": limits, "tests": ["tests/test_inhabited_facility.py"], "semantic_bindings": []}


def build() -> tuple[dict, dict]:
    components = [
        {"name": "person", "fields": [{"name": "role", "type": "string", "default": "worker"}]},
        {"name": "report_log", "fields": [{"name": "entries", "type": "string_list", "default": []}]},
        {"name": "boundary", "fields": [{"name": "place_a", "type": "entity_ref", "default": "corridor"},
                                        {"name": "place_b", "type": "entity_ref", "default": "laboratory"},
                                        {"name": "state", "type": "string", "default": "closed"}]},
        {"name": "pump", "fields": [{"name": "calibrated", "type": "boolean", "default": False},
                                    {"name": "status", "type": "string", "default": "uncalibrated"}]},
    ]
    entities = [{"id": pid, "label": label, "categories": ["place"], "components": {}} for pid, label in PLACES.items()]
    for did, (label, a, b, _) in DOORS.items():
        entities.append({"id": did, "label": label, "categories": ["boundary"], "location": a,
                         "components": {"boundary": {"place_a": a, "place_b": b, "state": "closed"}}})
    entities.append({"id": "prototype-pump", "label": "Prototype pump", "categories": ["equipment", "pump"],
                     "location": "laboratory", "components": {"pump": {"calibrated": False, "status": "uncalibrated"}}})
    for pid, (label, role, place, _) in PEOPLE.items():
        entities.append({"id": pid, "label": label, "categories": ["actor"], "location": place,
                         "components": {"person": {"role": role}, "report_log": {"entries": []}}})
    actions = [
        {"kind": "open-door", "description": "Open a door you are standing at, which opens both of its sides.",
         "fields": [{"name": "way", "type": "entity_ref"}, {"name": "partner", "type": "entity_ref"}]},
        {"kind": "move", "description": "Walk through a door that is open into the next room.",
         "fields": [{"name": "to", "type": "entity_ref"}, {"name": "way", "type": "entity_ref"}]},
        {"kind": "calibrate-pump", "description": "Calibrate the prototype pump while standing in the laboratory.",
         "fields": [{"name": "pump", "type": "entity_ref"}]},
        {"kind": "send-report", "description": "Send your own words to one person, wherever they are.",
         "fields": [{"name": "recipient", "type": "entity_ref"}, {"name": "content", "type": "string"}]},
    ]
    here = lambda who, other: check("you are where it is", ref(who, "location.location_id"), ref(other, "location.location_id"))
    mechanics = [
        mechanic("open-door", "Opening a door makes both of its directed halves passable; you must be at the door.",
                 {"way": {"categories": ["boundary"], "components": ["boundary"]},
                  "partner": {"categories": ["boundary"], "components": ["boundary"]}},
                 [check("you are at the door", ref("actor", "location.location_id"), ref("way", "location.location_id")),
                  check("the partner is the same door's other side", ref("partner", "components.boundary.place_a"),
                        ref("way", "components.boundary.place_b"))],
                 [{"participant": "way", "path": "components.boundary.state", "op": "set", "value": {"literal": "open"}},
                  {"participant": "partner", "path": "components.boundary.state", "op": "set", "value": {"literal": "open"}}],
                 ["No key, lock or force is modeled; a closed door only needs someone at it to open it."]),
        mechanic("move", "Movement changes the actor's room only through a passable door whose near side they stand in.",
                 {"to": {"categories": ["place"], "components": []},
                  "way": {"categories": ["boundary"], "components": ["boundary"]}},
                 [check("the door must be open", ref("way", "components.boundary.state"), {"literal": "open"}),
                  check("you are in the room this door leaves", ref("actor", "location.location_id"),
                        ref("way", "components.boundary.place_a")),
                  check("the destination is the room this door enters", {"action_field": "to"},
                        ref("way", "components.boundary.place_b"))],
                 [{"participant": "actor", "path": "location.location_id", "op": "set", "value": {"action_field": "to"}}],
                 ["Rooms are topology: no distance, travel time or collision is modeled."]),
        mechanic("calibrate-pump", "Calibrating needs the actor in the room where the pump stands.",
                 {"pump": {"categories": ["pump"], "components": ["pump"]}},
                 [here("actor", "pump")],
                 [{"participant": "pump", "path": "components.pump.calibrated", "op": "set", "value": {"literal": True}},
                  {"participant": "pump", "path": "components.pump.status", "op": "set", "value": {"literal": "calibrated"}}],
                 ["Calibration is binary; no measurement quality is modeled."]),
        mechanic("send-report", "Words reach the recipient's own log wherever they stand; this is a delivered "
                 "communication, not something the recipient could see or hear in a room.",
                 {"recipient": {"categories": ["actor"], "components": ["report_log"]}},
                 [check("the sender supplies words", {"action_field": "content"}, {"literal": ""}, "ne")],
                 [{"participant": "recipient", "path": "components.report_log.entries", "op": "append_report",
                   "value": {"action_field": "content"}}],
                 ["Delivery is instant and certain; channel delay or loss is not modeled."],
                 {"content": ["Report content supplied by the sender."]}),
    ]
    forms = []
    for did, (label, a, b, partner) in DOORS.items():
        forms.append({"kind": "open-door", "description": f"Open the {label.lower()}.", "fields": {"way": did, "partner": partner},
                      "unobserved_refs": ["partner"]})
        forms.append({"kind": "move", "description": f"Walk through the {label.lower()} to the {PLACES[b].lower()}.",
                      "fields": {"to": b, "way": did}})
    forms.append({"kind": "calibrate-pump", "description": "Calibrate the prototype pump.", "fields": {"pump": "prototype-pump"}})
    for other in ("ari", "mara", "bo"):
        forms.append({"kind": "send-report", "description": f"Tell {PEOPLE[other][0]} the pump is calibrated.",
                      "fields": {"recipient": other, "content": "The pump is calibrated."},
                      "not_self": ["recipient"]})
    public = [{"id": pid, "label": label, "fields": ["person.role"], "scope": "place"} for pid, (label, *_ ) in PEOPLE.items()]
    public += [{"id": pid, "label": label, "fields": []} for pid, label in PLACES.items()]
    public += [{"id": did, "label": label, "fields": ["boundary.state"], "scope": "place"} for did, (label, *_ ) in DOORS.items()]
    public.append({"id": "prototype-pump", "label": "Prototype pump", "fields": ["pump.status"], "scope": "place"})
    actors = {pid: {"brief": brief, "initial_knowledge": (
                  [{"id": f"{pid}-knows", "text": KNOWLEDGE[pid], "source": "own experience"}] if pid in KNOWLEDGE else []),
              "observable_fields": [{"entity": pid, "paths": ["report_log.entries"]}]} for pid, (_, _, _, brief) in PEOPLE.items()}
    bundle = {"schema_version": "world-substrate-authoring-bundle/v0",
              "world": {"id": "pump-facility", "label": "Pump Facility",
                        "summary": SHARED, "location": "corridor", "content_version": 1},
              "components": components, "entities": entities, "actions": actions,
              "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
              "actor_information": {"version": 1, "public_summary": SHARED, "public_entities": public,
                                    "actors": actors, "public_actions": forms}}
    return bundle, {"schema_version": "world-substrate-causal-model/v0", "mechanics": mechanics}


def main() -> int:
    bundle, causal = build()
    (OUT / "pump-facility-v0.json").write_text(json.dumps(bundle, indent=2) + "\n")
    (OUT / "pump-facility-causal-v0.json").write_text(json.dumps(causal, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
