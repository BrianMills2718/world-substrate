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
