"""Worlds and proposed rules for the ai-judge plan's J1 checks (A2 data): the port of the canonical example.

The port (docs/plans/ai_judge.md, Canonical example): Rosa, the customs officer, signs inspection releases; Vik, a
trader, has 40 coins and a crate he has not declared. No installed rule covers handing coins to anyone, so Vik's
"I offer Rosa 40 coins to sign the release without inspecting" is an unmatched attempt. `coin_rule()` is the rule
the canonical example's judge proposes for it ("a person may hand coins they hold to a person at the same place"),
written by hand in the declaration language the judge must use; `shove_rule()` sets off the J0 truck world's
40-step loading line, which a truck with no fuel stops ("blocked chain ruling").

Each is plain authoring-bundle and causal-model data, the same shape a World Builder build produces.
"""
from __future__ import annotations

from typing import Any

BRIBE = "I offer Rosa 40 coins to sign the release for my crate without inspecting it."


def _lit(value: Any) -> dict[str, Any]:
    return {"literal": value}


def _field(participant: str, path: str) -> dict[str, Any]:
    return {"participant": {"name": participant, "path": path}}


def _officer_move(kind: str, rationale: str, checks: list[dict[str, Any]], effect: dict[str, Any],
                  actor: str = "officer") -> dict[str, Any]:
    return {
        "schema_version": "world-substrate-action-mechanic/v0",
        "mechanic_id": kind, "version": "1", "action_kind": kind, "rationale": rationale,
        "actor_selector": {"categories": [actor], "components": []},
        "participants": {"crate": {"categories": ["crate"], "components": ["cargo"]}}, "parameters": {},
        "checks": checks, "effects": [effect], "limits": [rationale], "tests": [rationale],
        "semantic_bindings": ["crate is the crate acted on"],
    }


def port() -> tuple[dict[str, Any], dict[str, Any]]:
    bundle = {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {"id": "port", "label": "Port", "location": "customs-desk",
                  "summary": "A small port: Rosa, the customs officer, signs inspection releases. Vik, a trader, has "
                             "40 coins and a crate he has not declared."},
        "components": [
            {"name": "purse", "fields": [{"name": "coins", "type": "integer", "default": 0}]},
            {"name": "cargo", "fields": [
                {"name": "inspected", "type": "boolean", "default": False},
                {"name": "declared", "type": "boolean", "default": False},
                {"name": "released", "type": "boolean", "default": False},
            ]},
        ],
        "actions": [
            {"kind": "sign-release", "description": "The officer signs the inspection release for a crate.",
             "fields": [{"name": "crate", "type": "entity_ref"}]},
            {"kind": "inspect-crate", "description": "The officer inspects a crate.",
             "fields": [{"name": "crate", "type": "entity_ref"}]},
            {"kind": "declare-crate", "description": "The trader declares a crate.",
             "fields": [{"name": "crate", "type": "entity_ref"}]},
        ],
        "entities": [
            {"id": "customs-desk", "label": "customs desk", "categories": ["place"], "components": {}},
            {"id": "vik", "label": "Vik", "categories": ["actor", "trader"], "location": "customs-desk",
             "components": {"purse": {"coins": 40}}},
            {"id": "rosa", "label": "Rosa", "categories": ["actor", "officer"], "location": "customs-desk",
             "components": {"purse": {"coins": 0}}},
            {"id": "crate", "label": "crate", "categories": ["crate"], "location": "customs-desk",
             "components": {"cargo": {"inspected": False, "declared": False, "released": False}}},
        ],
        "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
    }
    rules = {
        "schema_version": "world-substrate-causal-model/v0",
        "mechanics": [
            _officer_move(
                "sign-release", "The officer signs the release once the crate is inspected.",
                [{"label": "the crate is inspected", "left": _field("crate", "components.cargo.inspected"),
                  "op": "eq", "right": _lit(True)},
                 {"label": "the release is not signed yet", "left": _field("crate", "components.cargo.released"),
                  "op": "eq", "right": _lit(False)}],
                {"participant": "crate", "path": "components.cargo.released", "op": "set", "value": _lit(True)}),
            _officer_move(
                "inspect-crate", "The officer inspects a crate not yet inspected.",
                [{"label": "the crate is not inspected yet", "left": _field("crate", "components.cargo.inspected"),
                  "op": "eq", "right": _lit(False)}],
                {"participant": "crate", "path": "components.cargo.inspected", "op": "set", "value": _lit(True)}),
            _officer_move(
                "declare-crate", "The trader declares a crate not yet declared.",
                [{"label": "the crate is not declared yet", "left": _field("crate", "components.cargo.declared"),
                  "op": "eq", "right": _lit(False)}],
                {"participant": "crate", "path": "components.cargo.declared", "op": "set", "value": _lit(True)},
                actor="trader"),
        ],
        "processes": [],
    }
    return bundle, rules


def coin_rule() -> dict[str, Any]:
    """The canonical example's ruling: a person may hand coins they hold to a person at the same place."""
    return {
        "action": {"kind": "hand-coins", "description": "A person hands coins they hold to a person at the same place.",
                   "fields": [{"name": "to", "type": "entity_ref"}, {"name": "amount", "type": "integer"}]},
        "mechanic": {
            "schema_version": "world-substrate-action-mechanic/v0",
            "mechanic_id": "hand-coins", "version": "1", "action_kind": "hand-coins",
            "rationale": "Coins a person holds can be handed to a person at the same place.",
            "actor_selector": {"categories": ["actor"], "components": ["purse"]},
            "participants": {"to": {"categories": ["actor"], "components": ["purse"]}},
            "parameters": {"amount": [1]},
            "checks": [
                {"label": "the amount is more than nothing", "left": {"action_field": "amount"}, "op": "gt",
                 "right": _lit(0)},
                {"label": "the giver holds that many coins", "left": _field("actor", "components.purse.coins"),
                 "op": "gte", "right": {"action_field": "amount"}},
                {"label": "they are at the same place", "left": _field("actor", "location.location_id"),
                 "op": "eq", "right": _field("to", "location.location_id")},
            ],
            "effects": [
                {"participant": "actor", "path": "components.purse.coins", "op": "subtract",
                 "value": {"action_field": "amount"}},
                {"participant": "to", "path": "components.purse.coins", "op": "add",
                 "value": {"action_field": "amount"}},
            ],
            "limits": ["Whether the one handed the coins agrees is their own decision, not part of this rule."],
            "tests": ["Handing 40 coins moves 40 coins from the giver to the one handed them."],
            "semantic_bindings": ["actor is the giver", "to is the one handed the coins"],
        },
    }


def shove_rule() -> dict[str, Any]:
    """A ruling for the J0 truck world: a person may shove the lever over by hand, which starts the loading line."""
    return {
        "action": {"kind": "shove-lever", "description": "Shove the lever over by hand.",
                   "fields": [{"name": "thing", "type": "entity_ref"}]},
        "mechanic": {
            "schema_version": "world-substrate-action-mechanic/v0",
            "mechanic_id": "shove-lever", "version": "1", "action_kind": "shove-lever",
            "rationale": "A set lever can be shoved over by hand.",
            "actor_selector": {"categories": ["actor"], "components": []},
            "participants": {"thing": {"categories": ["lever"], "components": ["link"]}}, "parameters": {},
            "checks": [{"label": "the lever is set", "left": _field("thing", "components.link.fallen"), "op": "eq",
                        "right": _lit(False)}],
            "effects": [{"participant": "thing", "path": "components.link.fallen", "op": "set", "value": _lit(True)}],
            "limits": ["Only a set lever can be shoved over."],
            "tests": ["Shoving the lever trips it."], "semantic_bindings": ["thing is what is shoved"],
        },
    }


def unwritable_rule() -> dict[str, Any]:
    """A ruling the declaration language rejects: a field named "from" is not an identifier (the plain baseline's
    cafe rule, evidence/ai-judge/plain-baseline/rules-check.json)."""
    rule = coin_rule()
    rule["action"]["fields"][0]["name"] = "from"
    mechanic = rule["mechanic"]
    mechanic["participants"] = {"from": mechanic["participants"].pop("to")}
    for row in mechanic["checks"] + mechanic["effects"]:
        if row.get("participant") == "to":
            row["participant"] = "from"
        for side in ("left", "right"):
            if isinstance(row.get(side), dict) and (row[side].get("participant") or {}).get("name") == "to":
                row[side]["participant"]["name"] = "from"
    return rule


def long_line(chains: int = 50, crates: int = 4, stages: int = 25) -> tuple[dict[str, Any], dict[str, Any]]:
    """Brian's "50 things ... down a causal chain 100 links deep" as a world small enough to read whole (the plan's
    "long chain ruling"): 50 lines of 4 crates, each crate passing 25 stages in order (one process per stage), the first
    stage of a crate once the crate before it has passed its last stage, and the first crate's once the start button
    is pressed. No installed move presses it. Pressing it sets off 50 chains 100 steps deep: 5,000 steps."""
    fields = [{"name": "prev", "type": "entity_ref", "default": "button"}] + [
        {"name": f"s{n}", "type": "boolean", "default": False} for n in range(1, stages + 1)]
    entities = [
        {"id": "yard", "label": "yard", "categories": ["place"], "components": {}},
        {"id": "sam", "label": "Sam", "categories": ["actor"], "location": "yard", "components": {}},
        {"id": "button", "label": "start button", "categories": ["button"], "location": "yard",
         "components": {"switch": {"pressed": False, "dusted": False}}},
    ]
    for c in range(1, chains + 1):
        for k in range(1, crates + 1):
            entities.append({"id": f"l{c}c{k}", "label": f"line {c} crate {k}",
                             "categories": ["crate", "first" if k == 1 else "next"],
                             "components": {"line": {"prev": "button" if k == 1 else f"l{c}c{k - 1}",
                                                     **{f"s{n}": False for n in range(1, stages + 1)}}}})
    bundle = {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {"id": "long-line", "label": "Long line", "location": "yard",
                  "summary": f"A packing yard: {chains} lines of {crates} crates. Each crate passes {stages} stages in "
                             "order, each stage done once the stage before it is; a crate's first stage starts once the "
                             "crate before it in its line has passed its last stage, and the first crate's once the "
                             "start button is pressed. Sam stands by the start button."},
        "components": [{"name": "switch", "fields": [{"name": "pressed", "type": "boolean", "default": False},
                                                     {"name": "dusted", "type": "boolean", "default": False}]},
                       {"name": "line", "fields": fields}],
        "actions": [{"kind": "dust-button", "description": "Dust the start button.",
                     "fields": [{"name": "thing", "type": "entity_ref"}]}],
        "entities": entities,
        "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
    }

    def process(pid: str, rationale: str, category: str, label: str, before: dict[str, Any], n: int,
                prev: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "process_id": pid, "rationale": rationale,
            "selector": {"categories": [category], "components": ["line"]}, "timing": "immediately",
            **({"participants": {"prev": {"link": "ref:line.prev", "selector": prev}}} if prev else {}),
            "checks": [{"label": label, "left": before, "op": "eq", "right": _lit(True)},
                       {"label": f"stage {n} is not done yet", "left": _field("it", f"components.line.s{n}"),
                        "op": "eq", "right": _lit(False)}],
            "effects": [{"participant": "it", "path": f"components.line.s{n}", "op": "set", "value": _lit(True)}],
        }

    processes = [
        process("first-crate-starts", "A line's first crate starts once the start button is pressed.", "first",
                "the start button is pressed", _field("prev", "components.switch.pressed"), 1,
                {"categories": ["button"], "components": ["switch"]}),
        process("next-crate-starts", "A crate starts once the crate before it has passed its last stage.", "next",
                "the crate before it is done", _field("prev", f"components.line.s{stages}"), 1,
                {"categories": ["crate"], "components": ["line"]}),
    ] + [process(f"stage-{n}", f"Stage {n} is done once stage {n - 1} is.", "crate", f"stage {n - 1} is done",
                 _field("it", f"components.line.s{n - 1}"), n) for n in range(2, stages + 1)]
    rules = {
        "schema_version": "world-substrate-causal-model/v0",
        "mechanics": [{
            "schema_version": "world-substrate-action-mechanic/v0",
            "mechanic_id": "dust-button", "version": "1", "action_kind": "dust-button",
            "rationale": "Dusting the start button cleans it and does not press it.",
            "actor_selector": {"categories": ["actor"], "components": []},
            "participants": {"thing": {"categories": ["button"], "components": ["switch"]}}, "parameters": {},
            "checks": [{"label": "the button is not dusted yet", "left": _field("thing", "components.switch.dusted"),
                        "op": "eq", "right": _lit(False)}],
            "effects": [{"participant": "thing", "path": "components.switch.dusted", "op": "set", "value": _lit(True)}],
            "limits": ["Dusting never presses the button."], "tests": ["Dusting sets the button dusted."],
            "semantic_bindings": ["thing is what is dusted"],
        }],
        "processes": processes,
    }
    return bundle, rules


def press_rule() -> dict[str, Any]:
    """A ruling for the long line: a person may press a start button that is not pressed yet."""
    return {
        "action": {"kind": "press-button", "description": "Press a start button.",
                   "fields": [{"name": "button", "type": "entity_ref"}]},
        "mechanic": {
            "schema_version": "world-substrate-action-mechanic/v0",
            "mechanic_id": "press-button", "version": "1", "action_kind": "press-button",
            "rationale": "A start button that is not pressed can be pressed by a person.",
            "actor_selector": {"categories": ["actor"], "components": []},
            "participants": {"button": {"categories": ["button"], "components": ["switch"]}}, "parameters": {},
            "checks": [{"label": "the button is not pressed yet", "left": _field("button", "components.switch.pressed"),
                        "op": "eq", "right": _lit(False)}],
            "effects": [{"participant": "button", "path": "components.switch.pressed", "op": "set",
                         "value": _lit(True)}],
            "limits": ["Only a button not yet pressed can be pressed."],
            "tests": ["Pressing the button sets it pressed."], "semantic_bindings": ["button is what is pressed"],
        },
    }


def empty_purse() -> tuple[dict[str, Any], dict[str, Any]]:
    """The port once the coin rule is installed (plan A3), with a second trader, Ines, who holds no coins."""
    bundle, rules = port()
    rule = coin_rule()
    bundle["actions"].append(rule["action"])
    rules["mechanics"].append(rule["mechanic"])
    bundle["world"]["summary"] += " Ines, another trader, holds no coins."
    bundle["entities"].append({"id": "ines", "label": "Ines", "categories": ["actor", "trader"],
                               "location": "customs-desk", "components": {"purse": {"coins": 0}}})
    return bundle, rules


def blocked_chain(length: int = 40) -> tuple[dict[str, Any], dict[str, Any]]:
    """The J0 truck world with no move for the lever (plan A2, "blocked chain ruling"): Sam's one installed move is to
    honk the truck's horn, so moving the lever is an attempt no rule covers. A ruling that lets Sam shove the lever
    over sets off the loading line, which stops at step `length` because the truck has no fuel."""
    from tests.knock_on_worlds import truck_without_fuel

    bundle, rules = truck_without_fuel(length)
    bundle["world"]["id"], bundle["world"]["label"] = "blocked-chain", "Blocked chain"
    bundle["world"]["summary"] = (
        f"A lever in the yard starts a {length}-step loading line; when its last step is done the truck is loaded, "
        "and a loaded truck leaves if it has fuel. The truck has no fuel. Sam works in the yard. No one has a move "
        "for the lever yet; Sam can honk the truck's horn.")
    [truck] = [c for c in bundle["components"] if c["name"] == "truck"]
    truck["fields"].append({"name": "honked", "type": "boolean", "default": False})
    bundle["entities"][-1]["components"]["truck"]["honked"] = False
    bundle["actions"] = [{"kind": "honk-horn", "description": "Honk the truck's horn.",
                          "fields": [{"name": "truck", "type": "entity_ref"}]}]
    rules["mechanics"] = [{
        "schema_version": "world-substrate-action-mechanic/v0",
        "mechanic_id": "honk-horn", "version": "1", "action_kind": "honk-horn",
        "rationale": "Anyone in the yard can honk the truck's horn.",
        "actor_selector": {"categories": ["actor"], "components": []},
        "participants": {"truck": {"categories": ["truck"], "components": ["truck"]}}, "parameters": {},
        "checks": [{"label": "the horn has not been honked", "left": _field("truck", "components.truck.honked"),
                    "op": "eq", "right": _lit(False)}],
        "effects": [{"participant": "truck", "path": "components.truck.honked", "op": "set", "value": _lit(True)}],
        "limits": ["The horn is honked once."], "tests": ["Honking sets the horn honked."],
        "semantic_bindings": ["truck is the truck whose horn is honked"],
    }]
    return bundle, rules
