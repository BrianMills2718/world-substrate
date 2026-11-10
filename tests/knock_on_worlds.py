"""Worlds for the ai-judge plan's J0 checks (A1, A7): long knock-on chains, a loop and a chain a blocker stops.

Each is a plain authoring bundle and causal model, the same data a World Builder build produces, so the same
worlds run in the tests, through the service's /run for the saved runs (evidence/ai-judge/j0/), and on the run page.

- fifty_chains(50, 100): Sam pulls one lever; 50 chains of 100 links each fall in one moment, each link because the
  link before it fell.
- loop(40): a ring of 40 dominoes; each knocks over the next, so the last would knock over the first again; the
  once-per-(rule, thing)-per-moment rule ends the moment.
- truck_without_fuel(40): a 40-step chain whose last step loads the truck; the truck leaves only if it has fuel,
  and it has none.
"""
from __future__ import annotations

from typing import Any

LINK_SELECTOR = {"categories": ["link"], "components": ["link"]}


def _lit(value: Any) -> dict[str, Any]:
    return {"literal": value}


def _base(world_id: str, label: str, summary: str) -> dict[str, Any]:
    return {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {"id": world_id, "label": label, "location": "yard", "summary": summary},
        "components": [
            {"name": "link", "fields": [
                {"name": "fallen", "type": "boolean", "default": False},
                {"name": "prev", "type": "entity_ref", "default": "lever"},
            ]},
        ],
        "actions": [{"kind": "pull", "description": "Pull the lever.", "fields": [{"name": "thing", "type": "entity_ref"}]}],
        "entities": [
            {"id": "yard", "label": "yard", "categories": ["place"], "components": {}},
            {"id": "sam", "label": "Sam", "categories": ["actor"], "location": "yard", "components": {}},
            {"id": "lever", "label": "lever", "categories": ["lever", "link"], "location": "yard",
             "components": {"link": {"fallen": False, "prev": "lever"}}},
        ],
        "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
    }


def _rules(processes: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "world-substrate-causal-model/v0",
        "mechanics": [{
            "schema_version": "world-substrate-action-mechanic/v0",
            "mechanic_id": "pull-lever", "version": "1", "action_kind": "pull",
            "rationale": "Pulling the lever trips it.",
            "actor_selector": {"categories": ["actor"], "components": []},
            "participants": {"thing": {"categories": ["lever"], "components": ["link"]}}, "parameters": {},
            "checks": [{"label": "the lever is set", "left": {"participant": {"name": "thing",
                        "path": "components.link.fallen"}}, "op": "eq", "right": _lit(False)}],
            "effects": [{"participant": "thing", "path": "components.link.fallen", "op": "set", "value": _lit(True)}],
            "limits": ["Only a set lever can be pulled."],
            "tests": ["Pulling the lever trips it."], "semantic_bindings": ["thing is what is pulled"],
        }],
        "processes": processes,
    }


def _falls_after_prev(process_id: str = "falls-after-the-one-before", selector: dict[str, Any] | None = None):
    return {
        "process_id": process_id, "rationale": "A link falls once the link before it has fallen.",
        "selector": selector or {"categories": ["chain"], "components": ["link"]}, "timing": "immediately",
        "participants": {"prev": {"link": "ref:link.prev", "selector": LINK_SELECTOR}},
        "checks": [
            {"label": "the one before it fell", "left": {"participant": {"name": "prev", "path": "components.link.fallen"}},
             "op": "eq", "right": _lit(True)},
            {"label": "it is still standing", "left": {"participant": {"name": "it", "path": "components.link.fallen"}},
             "op": "eq", "right": _lit(False)},
        ],
        "effects": [{"participant": "it", "path": "components.link.fallen", "op": "set", "value": _lit(True)}],
    }


def _link(entity_id: str, prev: str, categories: list[str] | None = None) -> dict[str, Any]:
    return {"id": entity_id, "label": entity_id, "categories": categories or ["chain", "link"], "location": "yard",
            "components": {"link": {"fallen": False, "prev": prev}}}


def fifty_chains(chains: int = 50, length: int = 100) -> tuple[dict[str, Any], dict[str, Any]]:
    bundle = _base("fifty-chains", "Fifty chains",
                   f"Sam can pull one lever; {chains} chains of {length} links start at it, and each link falls "
                   "once the link before it has fallen.")
    for c in range(1, chains + 1):
        prev = "lever"
        for n in range(1, length + 1):
            link_id = f"c{c}-{n}"
            bundle["entities"].append(_link(link_id, prev))
            prev = link_id
    return bundle, _rules([_falls_after_prev()])


def loop(size: int = 40) -> tuple[dict[str, Any], dict[str, Any]]:
    """A ring: the lever leans on d1, each domino on the one before, and d1 also on the last. The rule has no
    "still standing" check, so it stays due after it fires; only once-per-(rule, thing)-per-moment ends the moment."""
    bundle = _base("loop", "Loop",
                   f"Sam can pull a lever that knocks over the first of {size} dominoes in a ring; each domino is "
                   "knocked by the one before it, and the first is knocked again by the last.")
    bundle["components"][0]["fields"].append({"name": "knocks", "type": "integer", "default": 0})
    ring = [f"d{n}" for n in range(1, size + 1)]
    for n in range(size):
        bundle["entities"].append(_link(ring[n], ring[n - 1]))  # ring[-1] for d1: the ring closes
    for entity in bundle["entities"]:
        if "link" in entity["components"]:
            entity["components"]["link"]["knocks"] = 0
    rules = _rules([{
        "process_id": "knocked-by-the-one-before", "rationale": "A domino is knocked each time the one before it has "
        "fallen.", "selector": {"categories": ["chain"], "components": ["link"]}, "timing": "immediately",
        "participants": {"prev": {"link": "ref:link.prev", "selector": LINK_SELECTOR}},
        "checks": [{"label": "the one before it fell",
                    "left": {"participant": {"name": "prev", "path": "components.link.fallen"}}, "op": "eq",
                    "right": _lit(True)}],
        "effects": [{"participant": "it", "path": "components.link.fallen", "op": "set", "value": _lit(True)},
                    {"participant": "it", "path": "components.link.knocks", "op": "add", "value": _lit(1)}],
    }])
    # The lever trips d1 directly: d1 counts as the lever here.
    lever = rules["mechanics"][0]
    lever["participants"] = {"thing": {"categories": ["first"], "components": ["link"]}}
    bundle["entities"][3]["categories"] = ["chain", "link", "first"]
    return bundle, rules


def truck_without_fuel(length: int = 40) -> tuple[dict[str, Any], dict[str, Any]]:
    bundle = _base("truck-without-fuel", "Truck without fuel",
                   f"Sam can pull a lever that starts a {length}-step loading line; when its last step is done the "
                   "truck is loaded, and a loaded truck leaves if it has fuel. The truck has no fuel.")
    bundle["components"].append({"name": "truck", "fields": [
        {"name": "fuel", "type": "integer", "default": 0},
        {"name": "left_yard", "type": "boolean", "default": False},
        {"name": "load", "type": "entity_ref", "default": "lever"},
    ]})
    prev = "lever"
    for n in range(1, length + 1):
        bundle["entities"].append(_link(f"step-{n}", prev))
        prev = f"step-{n}"
    bundle["entities"].append({"id": "truck", "label": "truck", "categories": ["truck"], "location": "yard",
                               "components": {"truck": {"fuel": 0, "left_yard": False, "load": prev}}})
    rules = _rules([
        _falls_after_prev("loading-step-done"),
        {"process_id": "truck-leaves", "rationale": "A loaded truck leaves the yard if it has fuel.",
         "selector": {"categories": ["truck"], "components": ["truck"]}, "timing": "immediately",
         "participants": {"load": {"link": "ref:truck.load", "selector": LINK_SELECTOR}},
         "checks": [
             {"label": "the last loading step is done",
              "left": {"participant": {"name": "load", "path": "components.link.fallen"}}, "op": "eq",
              "right": _lit(True)},
             {"label": "the truck has fuel", "left": {"participant": {"name": "it", "path": "components.truck.fuel"}},
              "op": "gt", "right": _lit(0)},
             {"label": "the truck is still in the yard",
              "left": {"participant": {"name": "it", "path": "components.truck.left_yard"}}, "op": "eq",
              "right": _lit(False)},
         ],
         "effects": [{"participant": "it", "path": "components.truck.left_yard", "op": "set", "value": _lit(True)}]},
    ])
    return bundle, rules


WORLDS = {"fifty-chains": fifty_chains, "loop": loop, "truck-without-fuel": truck_without_fuel}
