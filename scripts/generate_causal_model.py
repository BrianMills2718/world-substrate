#!/usr/bin/env python3
"""Generate a constrained causal model proposal for a world-authoring bundle.

The model returns JSON only.  Its output is then compiled by
``world_substrate.action_authoring``; arbitrary source code is never executed.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.scaffold_world import load_bundle, validate_bundle
from world_substrate.action_authoring import (
    ACTION_MECHANIC_SCHEMA_VERSION,
    CAUSAL_MODEL_SCHEMA_VERSION,
    CausalModel,
)

DEFAULT_MODEL = "openrouter/openai/gpt-6-luna"
DEFAULT_BUDGET = 0.12
MAX_MECHANICS_OUTPUT_TOKENS = 16000


def _primitive_schema(kind: str) -> dict[str, Any]:
    return {
        "string": {"type": "string", "minLength": 1},
        "entity_ref": {"type": "string", "minLength": 1},
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "boolean": {"type": "boolean"},
    }[kind]


def _selector_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "categories": {"type": "array", "items": {"type": "string"}},
            "components": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["categories", "components"],
        "additionalProperties": False,
    }


def _expr_schema(participants: list[str], fields: list[str]) -> dict[str, Any]:
    names = ["actor", *participants]
    return {
        "anyOf": [
            {
                "type": "object",
                "properties": {
                    "literal": {
                        "anyOf": [
                            {"type": "string"},
                            {"type": "integer"},
                            {"type": "number"},
                            {"type": "boolean"},
                            {"type": "null"},
                        ]
                    }
                },
                "required": ["literal"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"action_field": {"enum": fields}},
                "required": ["action_field"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {
                    "participant": {
                        "type": "object",
                        "properties": {
                            "name": {"enum": names},
                            "path": {"type": "string", "minLength": 1},
                        },
                        "required": ["name", "path"],
                        "additionalProperties": False,
                    }
                },
                "required": ["participant"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"entity_id": {"enum": names}},
                "required": ["entity_id"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"owner_ref": {"enum": names}},
                "required": ["owner_ref"],
                "additionalProperties": False,
            },
            {
                "type": "object",
                "properties": {"event_id": {"const": True}},
                "required": ["event_id"],
                "additionalProperties": False,
            },
        ]
    }


def _mechanic_schema(action: dict[str, Any]) -> dict[str, Any]:
    fields = action.get("fields") or []
    field_names = [row["name"] for row in fields]
    entity_fields = [row["name"] for row in fields if row["type"] == "entity_ref"]
    scalar_fields = [row for row in fields if row["type"] != "entity_ref"]
    expr = _expr_schema(entity_fields, field_names)
    participant_properties = {name: _selector_schema() for name in entity_fields}
    parameter_properties = {
        row["name"]: {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": _primitive_schema(row["type"]),
        }
        for row in scalar_fields
    }
    participant_object: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
    }
    if participant_properties:
        participant_object["properties"] = participant_properties
        participant_object["required"] = entity_fields
    parameter_object: dict[str, Any] = {
        "type": "object",
        "additionalProperties": False,
    }
    if parameter_properties:
        parameter_object["properties"] = parameter_properties
        parameter_object["required"] = [row["name"] for row in scalar_fields]
    return {
        "type": "object",
        "properties": {
            "schema_version": {"const": ACTION_MECHANIC_SCHEMA_VERSION},
            "mechanic_id": {"type": "string", "minLength": 1},
            "version": {"type": "string", "minLength": 1},
            "action_kind": {"const": action["kind"]},
            "rationale": {"type": "string", "minLength": 1},
            "actor_selector": _selector_schema(),
            "participants": participant_object,
            "parameters": parameter_object,
            "checks": {
                "type": "array",
                "minItems": 1,
                "maxItems": 12,
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "minLength": 1},
                        "left": expr,
                        "op": {"enum": ["eq", "ne", "lt", "lte", "gt", "gte", "contains"]},
                        "right": expr,
                    },
                    "required": ["label", "left", "op", "right"],
                    "additionalProperties": False,
                },
            },
            "effects": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "properties": {
                        "participant": {"enum": ["actor", *entity_fields]},
                        "path": {"type": "string", "minLength": 1},
                        "op": {"enum": ["set", "add", "subtract"]},
                        "value": expr,
                    },
                    "required": ["participant", "path", "op", "value"],
                    "additionalProperties": False,
                },
            },
            "limits": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
            "tests": {
                "type": "array",
                "minItems": 1,
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
            "semantic_bindings": {
                "type": "array",
                "maxItems": 8,
                "items": {"type": "string", "minLength": 1},
            },
        },
        "required": [
            "schema_version",
            "mechanic_id",
            "version",
            "action_kind",
            "rationale",
            "actor_selector",
            "participants",
            "parameters",
            "checks",
            "effects",
            "limits",
            "tests",
            "semantic_bindings",
        ],
        "additionalProperties": False,
    }


WORLD_KINDS = ("task", "ongoing", "open")
WORLD_KIND_RULES = {
    "task": (
        "World kind: task. Propose a terminal condition derived from represented state; the run "
        "stops when it is reached. Processes are optional: only for things the description says "
        "happen by themselves."
    ),
    "ongoing": (
        "World kind: keeps running. terminal must be null. Add 1-4 processes so the world never runs down. "
        "If the description is about work or production: keep raw materials renewing at their source and demand arriving (raw materials regrow or are mined each round, customers want more, a served "
        "order becomes a new waiting order), so goods keep flowing through the chain and every actor "
        "role has something useful to do in most rounds, forever. A process never adds a good that an action "
        "makes from other goods (boards, parts, finished products): those come only from that action. A process "
        "never moves goods from one holder to another: carrying is an actor's action. "
        "A raw material has one source: if an actor's action gathers it (mining, cutting), that action takes it "
        "from a reserve and the process renews the reserve, not the gatherer's stock. "
        "Each actor's actions should be limited "
        "to its own step by checks on its role, and moving goods should add to the next holder's stock "
        "and subtract from the previous one's. If it is about people living their lives: change needs and "
        "resources every round in a cycle (for example hunger rises AND food regrows, supplies run down AND "
        "are restocked), never only decay, so they keep acting on their own needs with no goal imposed."
    ),
}
# 'open' is an older name for the same kind (merged 2026-10-06: Brian asked whether they
# really needed to be different; nothing but this advice ever differed).
WORLD_KIND_RULES["open"] = WORLD_KIND_RULES["ongoing"]


def _process_schema() -> dict[str, Any]:
    expr = _expr_schema(["it"], [])
    # Processes may name linked participants (see "participants" below), so a participant reference
    # inside a process expression is any declared name, not only `it`.
    for option in expr["anyOf"]:
        name = option.get("properties", {}).get("participant", {}).get("properties", {}).get("name")
        if isinstance(name, dict) and "enum" in name:
            option["properties"]["participant"]["properties"]["name"] = {"type": "string", "minLength": 1}
    return {
        "type": "object",
        "properties": {
            "process_id": {"type": "string", "minLength": 1},
            "rationale": {"type": "string", "minLength": 1},
            "selector": _selector_schema(),
            "timing": {
                "description": (
                    "each_round (default): runs once per round. immediately: a knock-on effect that runs in the same "
                    "moment as the change that makes its checks hold (a pushed glass falls, then breaks, then spills), "
                    "repeating until nothing more is due."
                ),
                "enum": ["each_round", "immediately"],
            },
            "participants": {
                "description": (
                    "Optional linked entities this process also changes in the same transition, each resolved from "
                    "the matching entity `it`: link owner_of_it (the entity named by it's ownership.owner_ref), "
                    "owned_by_it, co_located (same location), or ref:<component>.<field> (an entity_ref field on it)."
                ),
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "properties": {"link": {"type": "string", "minLength": 1}, "selector": _selector_schema()},
                    "required": ["link", "selector"],
                    "additionalProperties": False,
                },
            },
            "checks": {
                "type": "array",
                "maxItems": 6,
                "items": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "minLength": 1},
                        "left": expr,
                        "op": {"enum": ["eq", "ne", "lt", "lte", "gt", "gte", "contains"]},
                        "right": expr,
                    },
                    "required": ["label", "left", "op", "right"],
                    "additionalProperties": False,
                },
            },
            "effects": {
                "type": "array",
                "minItems": 1,
                "maxItems": 6,
                "items": {
                    "type": "object",
                    "properties": {
                        "participant": {"type": "string", "minLength": 1},
                        "path": {"type": "string", "minLength": 1},
                        "op": {"enum": ["set", "add", "subtract"]},
                        "value": expr,
                    },
                    "required": ["participant", "path", "op", "value"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["process_id", "rationale", "selector", "checks", "effects"],
        "additionalProperties": False,
    }


def causal_model_schema(bundle: dict[str, Any]) -> dict[str, Any]:
    actions = bundle.get("actions") or []
    return {
        "type": "object",
        "properties": {
            "schema_version": {"const": CAUSAL_MODEL_SCHEMA_VERSION},
            "mechanics": {
                "type": "array",
                "minItems": len(actions),
                "maxItems": len(actions),
                "items": {"anyOf": [_mechanic_schema(action) for action in actions]},
            },
            "processes": {
                "description": (
                    "Things the world does by itself, with no actor: every entity matching the selector whose "
                    "checks hold (participant 'it') gets the effects, once per round, or at once as a knock-on "
                    "effect when timing is immediately."
                ),
                "type": "array",
                "maxItems": 6,
                "items": _process_schema(),
            },
            "terminal": {
                "anyOf": [
                    {"type": "null"},
                    {
                        "type": "object",
                        "properties": {
                            "mode": {"enum": ["all", "any"]},
                            "selector": _selector_schema(),
                            "checks": {
                                "type": "array",
                                "minItems": 1,
                                "maxItems": 8,
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string", "minLength": 1},
                                        "op": {"enum": ["eq", "ne", "lt", "lte", "gt", "gte", "contains"]},
                                        "value": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "integer"},
                                                {"type": "number"},
                                                {"type": "boolean"},
                                            ]
                                        },
                                    },
                                    "required": ["path", "op", "value"],
                                    "additionalProperties": False,
                                },
                            },
                        },
                        "required": ["mode", "selector", "checks"],
                        "additionalProperties": False,
                    },
                ]
            },
        },
        "required": ["schema_version", "mechanics", "terminal"],
        "additionalProperties": False,
    }


def _context(bundle: dict[str, Any]) -> dict[str, Any]:
    paths: list[str] = [
        "location.location_id",
        "ownership.owner_ref",
        "portable.portable",
    ]
    for comp in bundle.get("components") or []:
        for field in comp.get("fields") or []:
            paths.append(f"components.{comp['name']}.{field['name']}")
    # Built-in state is not written in the bundle's component values, so state
    # it exactly as build_engine will initialise it. Without this a proposer
    # guesses (e.g. "the can is in the garden" when every entity starts at the
    # world location) and every action is refused from the first round.
    initial_builtin_state = {
        row["id"]: {
            "location.location_id": row.get("location") or bundle["world"]["location"],
            "ownership.owner_ref": row.get("owner_ref"),
            "portable.portable": row.get("portable"),
        }
        for row in bundle.get("entities", [])
    }
    return {
        "world": bundle["world"],
        "components": bundle.get("components", []),
        "entities": bundle.get("entities", []),
        "initial_builtin_state": initial_builtin_state,
        "actions": bundle.get("actions", []),
        "allowed_state_paths": paths,
        # declared-laws plan S1: the world designer's own laws, written for this world (docs/plans/declared_laws.md).
        "resources": bundle.get("resources", []),
        "laws": bundle.get("laws", []),
        "authority_rules": [
            "Every move and process must keep the world's laws: a resource with a total law changes in total only "
            "through the moves listed in may_change_by and through processes whose process_id is listed there as "
            "'process:<process_id>'; every other effect on it subtracts from one holder exactly what it adds to "
            "another. A pairing law's move hands over its 'gives' and its 'pays' in the same move, with a check "
            "that each giver has enough. A process the laws name as 'process:<id>' must have exactly that "
            "process_id. The engine refuses any step that breaks a law. When there are no laws, this rule says "
            "nothing.",
            "Use only action participants as effect targets.",
            # Airfield s2 (evidence/open-attempt/s2-airfield/): six rules answers wrote no knock-on process at all.
            "Go through the represented things and moves for consequences that follow physically at once (a "
            "spill wets what is under it, a loud change such as an engine starting is heard by people in the same "
            "place) and write each one the represented state can hold as a process with timing immediately.",
            # #254 (same evidence): fly added 0 flights and drink set the drinker's place to itself.
            "Every effect must be able to change state: never add or subtract 0 and never set a field to its own "
            "value. If a move has no represented field it would change, set a stage or add 1 to a count that the "
            "description implies, or say in limits what is left out.",
            # #259 pencil build (evidence/model-more/): the world had a price but a sale moved no money.
            "When a move exchanges something for a price and both sides have a represented amount of money, the "
            "same move subtracts the price from the payer and adds it to the payee, with a check that the payer "
            "has at least the price. Effects cannot multiply, so a priced move hands over exactly one unit (add "
            "and subtract the literal 1, ignoring any quantity field) and charges the price once; selling more takes "
            "more moves. (2026-10-26 pencil build NZD33sh3iX29: a sale of several pencils charged for one.)",
            "A process acts on each matching entity `it`. When one physical change moves or changes a linked entity "
            "too (a driver riding in a vehicle, a hospital whose bed a dying patient frees), declare that entity in "
            "the process's participants (link owner_of_it, owned_by_it, co_located, or ref:<component>.<field>) and "
            "target it by that name in the same process; never split one physical change across two processes.",
            # open_attempt S2 (docs/plans/open_attempt.md piece 2): consequences of a change that physically follow
            # at once are knock-on processes, so a person sees the whole chain in the round they acted.
            "When a consequence follows physically at once from another change (something unsupported falls, a "
            "fragile thing that fell breaks, a broken container spills, a breaking thing makes a sound), make it a "
            "process with timing immediately whose checks name the state that change leaves; each step of a chain "
            "is its own process. Keep timing each_round for what takes time (drying, growing, travelling, fuel).",
            # 2026-10-26 cafe samples (evidence/knock-on-targets/): the world had upright, full, spilled, broken
            # and 'on' fields, yet knock-over only set upright false, citing caution ("not inferred from a bump").
            "Fields such as upright, full, spilled, broken and wet, with an entity_ref 'on' naming what a thing "
            "rests on, already state the physics; using them is not an assumption. When a world has them, write "
            "the ordinary consequences as processes with timing immediately: a full container that is no longer "
            "upright spills (full false, spilled true); a spill wets what its 'on' names (participant linked by "
            "ref:<component>.on); a fragile thing that falls breaks. Keep the move itself to its direct change.",
            # 2026-10-26 (evidence/model-more/): a pencil world's truck had a rounds_left field, but deliver-boxes
            # handed the boxes over at once and no process counted it down, so the journey took no time.
            "When an entity has an integer field counting rounds left (a delivery on the road, a journey, a job "
            "under way, a deadline), the action that starts it sets that count and does not finish it at once; add "
            "a process with timing each_round that lowers the count by 1 while it is above 0, and make the arrival "
            "or completion (goods reaching their destination, the job done) depend on the count being 0.",
            "Checks on location/ownership/portable paths must agree with initial_builtin_state "
            "(null means unset), so that at least one action is possible from the starting state.",
            "Never check ownership.owner_ref or portable.portable on an entity whose initial_builtin_state "
            "value is null, unless one of your own effects sets that value first; use component fields instead.",
            "A participant's selector must list in `components` every component whose fields that participant's checks or effects read or write.",
            # open_attempt Q23, 2026-10-25 (evidence/open-attempt/q23/after-fix/): fly checked the helicopter was in
            # the hangar but not that Sam was, so Sam could take off from the office on the far side of a brick wall.
            "When entities start in different places (initial_builtin_state location values differ), an action that "
            "uses, takes, operates or talks to a thing or person must check that the actor's location.location_id "
            "equals that participant's location.location_id.",
            # 2026-10-27 pencil czt5uoGw5t3L (evidence/pencil7-trace-audit/): the rule above gave buy-leads and
            # buy-slats a same-place check between a factory and suppliers on other continents; nothing moved anyone,
            # so the factory never got leads or slats and no pencil was made.
            "Except: an order or purchase between parties in different places is sent from afar. Give it no "
            "same-place check unless one of your moves or processes can bring them together; when the goods "
            "travel, start a delivery that counts down rounds instead.",
            # Q23 rules2: move required the destination to equal both sides of the wall at once, so it could never pass.
            "Every check must hold at the same time; there is no 'or'. Never require one value to equal two different "
            "fields. For a way between two places, require the actor's location to equal the way's first place "
            "field and the destination to equal its second, and name the reverse direction in limits.",
            "Checks and effects must use only allowed_state_paths.",
            "Do not invent source code, hidden state, or new entities.",
            "An action should change only state causally implied by its description and represented world.",
            "Use owner_ref expressions for actor ownership rather than hard-coded actor ids. "
            "{owner_ref: P} is the string 'actor:<id of P>', meaning 'owned by P'; it is NOT the owner of P. "
            "To require that thing X belongs to the acting actor, compare "
            "{participant: {name: X, path: ownership.owner_ref}} with {owner_ref: actor}. Never put "
            "{owner_ref: X} for a thing X on the left of a check (that would ask whether X owns itself).",
            "Terminal, if present, must be derivable from represented state and must not duplicate a completion flag.",
            "Limits and tests must name omissions and refusal/boundary cases honestly.",
            "Every check label is a short plain-English condition a visitor understands, using entity labels "
            "(e.g. \"the watering can is free\", \"Ava is holding the knife\"); never jargon such as actor, "
            "owner_ref, context, entity, component or participant.",
        ],
    }


def tidy_proposal(causal: dict[str, Any], bundle: dict[str, Any]) -> list[str]:
    """Fix, in place, two slips the compiler would reject whole, and say what was fixed.

    pencil11 (stBKjmj-sgiE): three of four rule sets were thrown away, about 70 s each. Twice a check read a
    participant's ``components.business.cash`` while its selector did not require ``business``; adding the
    requirement only states what the rule already reads, since an entity without the component could never pass.
    Once the moves did not match the world's list; a move the world does not have, or a second copy of one, is
    dropped here. A missing move is left for the compiler, because writing it needs the rules writer."""
    fixed: list[str] = []

    def paths(node: Any, out: list[tuple[str, str]]) -> None:
        if isinstance(node, dict):
            ref = node.get("participant")
            if isinstance(ref, dict) and isinstance(ref.get("name"), str) and isinstance(ref.get("path"), str):
                out.append((ref["name"], ref["path"]))
            elif isinstance(ref, str) and isinstance(node.get("path"), str):
                out.append((ref, node["path"]))
            for value in node.values():
                paths(value, out)
        elif isinstance(node, list):
            for value in node:
                paths(value, out)

    def require(selectors: dict[str, Any], used: list[tuple[str, str]], where: str) -> None:
        for name, path in used:
            parts = path.split(".")
            selector = selectors.get(name)
            if len(parts) != 3 or parts[0] != "components" or not isinstance(selector, dict):
                continue
            components = selector.setdefault("components", [])
            if isinstance(components, list) and parts[1] not in components:
                components.append(parts[1])
                fixed.append(f"{where}: {name} must have {parts[1]} (a rule reads {path})")

    expected = {row.get("kind") for row in bundle.get("actions") or [] if isinstance(row, dict)}
    kept, seen = [], set()
    for row in causal.get("mechanics") or []:
        kind = row.get("action_kind") if isinstance(row, dict) else None
        if isinstance(row, dict) and (kind not in expected or kind in seen):
            fixed.append(f"dropped {'a second ' if kind in seen else ''}move {kind!r}"
                         + ("" if kind in seen else ", which the world does not have"))
            continue
        seen.add(kind)
        kept.append(row)
    if isinstance(causal.get("mechanics"), list):
        causal["mechanics"] = kept
    for row in kept:
        if not isinstance(row, dict):
            continue
        participants = row.get("participants") if isinstance(row.get("participants"), dict) else {}
        selectors = {"actor": row.get("actor_selector"), **participants}
        used: list[tuple[str, str]] = []
        paths([row.get("checks"), row.get("effects")], used)
        require(selectors, used, str(row.get("action_kind")))
    for row in causal.get("processes") or []:
        if not isinstance(row, dict):
            continue
        linked = row.get("participants") if isinstance(row.get("participants"), dict) else {}
        selectors = {"it": row.get("selector"),
                     **{n: r.get("selector") for n, r in linked.items() if isinstance(r, dict)}}
        used = []
        paths([row.get("checks"), row.get("effects")], used)
        require(selectors, used, str(row.get("process_id")))
    terminal = causal.get("terminal")
    if isinstance(terminal, dict):
        require({"it": terminal.get("selector")},
                [("it", c["path"]) for c in terminal.get("checks") or [] if isinstance(c, dict) and isinstance(c.get("path"), str)],
                "finish line")
    return fixed


def no_op_effects(causal: dict[str, Any]) -> list[str]:
    """Effects that can never change anything: add or subtract 0, or set a field to its own value.

    A move whose only effects are these does nothing, and the runner hides moves that change nothing, so nobody is
    ever offered it (#254, 2026-10-26 airfield: fly added 0 flights, drink set the drinker's place to itself).
    Checked when rules are written, not in the compiler, so saved worlds keep loading.
    """
    found = []
    for kind, rows in (("mechanic", causal.get("mechanics") or []), ("process", causal.get("processes") or [])):
        for row in rows:
            name = row.get("mechanic_id") or row.get("process_id") or "?"
            for effect in row.get("effects") or []:
                value = effect.get("value") if isinstance(effect.get("value"), dict) else {}
                literal, own = value.get("literal"), value.get("participant")
                zero = (effect.get("op") in {"add", "subtract"} and isinstance(literal, (int, float))
                        and not isinstance(literal, bool) and literal == 0)
                itself = (effect.get("op") == "set" and isinstance(own, dict)
                          and own.get("name") == effect.get("participant") and own.get("path") == effect.get("path"))
                if zero or itself:
                    found.append(f"{kind} {name}: {effect.get('op')} {effect.get('path')} on {effect.get('participant')}"
                                 + (" by 0" if zero else " to its own value"))
    return found


def merge_revision(previous: dict[str, Any], change: dict[str, Any]) -> dict[str, Any]:
    """previous with a revision's changed rows written over it, matched by id; rows not named are kept.

    A mechanic whose id is new but whose move has exactly one mechanic in previous replaces that one, so a renamed
    rewrite of a move does not leave two mechanics for it. Raises ValueError when nothing changes, since the same
    rules would fail the same way again.
    """
    merged = deepcopy(previous)
    for key, id_key in (("mechanics", "mechanic_id"), ("processes", "process_id")):
        if key not in merged and not change.get(key):
            continue
        rows = [row for row in merged.get(key) or [] if isinstance(row, dict)]
        removed = {str(x) for x in change.get(f"remove_{key}") or []}
        rows = [row for row in rows if str(row.get(id_key)) not in removed]
        for new in change.get(key) or []:
            if not isinstance(new, dict):
                continue
            at = [i for i, row in enumerate(rows) if row.get(id_key) == new.get(id_key)]
            if not at and key == "mechanics":
                at = [i for i, row in enumerate(rows) if row.get("action_kind") == new.get("action_kind")]
                at = at if len(at) == 1 else []
            if at:
                rows[at[0]] = new
            else:
                rows.append(new)
        merged[key] = rows
    if "terminal" in change:
        merged["terminal"] = change["terminal"]
    if merged == previous:
        raise ValueError("the revision changed nothing; change what author_guidance names")
    return merged


def generate_causal_model(
    bundle: dict[str, Any],
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    reasoning_effort: str = "low",
    guidance: str = "",
    model_justification: str | None = None,
    world_kind: str = "task",
    previous: dict[str, Any] | None = None,
    max_output_tokens: int = MAX_MECHANICS_OUTPUT_TOKENS,
    route_policy: Any = None,
) -> tuple[dict[str, Any], Any]:
    bundle = validate_bundle(bundle)
    if world_kind not in WORLD_KINDS:
        raise ValueError(f"world_kind must be one of {WORLD_KINDS}")
    if not bundle.get("actions"):
        raise ValueError("bundle has no action signatures to generate mechanics for")
    # Do not depend on provider-native JSON Schema here. Some routes accept the
    # policy-choice schema but reject richer nested unions. The model remains a
    # proposer only: ordinary text is parsed as JSON and the local causal
    # compiler below is the authority gate. No returned source code is executed.
    from llm_client import call_llm, safe_json_loads

    trace_id = trace_id or f"world-builder-mechanics-{uuid.uuid4().hex}"
    context = _context(bundle)
    context["response_contract"] = causal_model_schema(bundle)
    context["world_kind"] = world_kind
    context["authority_rules"] = [*context["authority_rules"], WORLD_KIND_RULES[world_kind]]
    if guidance.strip():
        context["author_guidance"] = guidance.strip()[:4000]
    if previous and guidance.strip():
        # A retry revises the rules the guidance is about instead of starting over: told only
        # "your previous rules had X", the writer wrote fresh rules that lost earlier fixes and
        # kept the named defect (pencil10 5UGnK9L0Iulf: "make-pencils needs slats at factory"
        # on all four attempts).
        context["previous_proposal"] = previous
        # Only the changed rows come back: rewriting the whole proposal made every retry a 42-60 s call of
        # 4k-7k output tokens (pencil13 3SogfsdEGx9M, five such calls in a row).
        context["revision_rule"] = (
            "previous_proposal is your last proposal and author_guidance says what was wrong with it. "
            "Return only what changes: in mechanics, each mechanic you change or add, written out in full, "
            "with the mechanic_id it has in previous_proposal; in processes, likewise by process_id; "
            "remove_mechanics and remove_processes list ids to delete; include terminal only if it changes. "
            "Change what the guidance names, and keep every other mechanic, process and terminal: anything "
            "you leave out is kept from previous_proposal unchanged. Returning nothing changed is rejected."
        )
    moves = [str(row.get("kind")) for row in bundle["actions"] if isinstance(row, dict)]
    revising = "previous_proposal" in context
    coverage = (
        "Return only the mechanics and processes revision_rule asks you to change. " if revising else
        # pencil12 (share oRfOptv0O3f3): 4 of 8 first replies were {"mechanics": []}, each costing a
        # 7 s call and a repair before any rules were written.
        f"mechanics must hold one mechanic for each of these moves: {', '.join(moves)}; "
        "an empty mechanics list is always rejected. "
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are proposing causal mechanics for a governed world model. "
                "Return exactly one JSON object and no prose or markdown. You are not writing code. "
                + coverage +
                "The response must satisfy response_contract. Every effect must be justified by "
                "represented state and the action description. Prefer conservative refusal checks "
                "over assumptions. Do not add reads/writes fields; the local compiler derives authority. "
                "Whenever you name a state path, copy it EXACTLY from allowed_state_paths. "
                "Where one change physically sets off another at once (a fall, a break, a spill, a noise heard "
                "nearby), write that consequence as a process with timing immediately."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(context, indent=2, sort_keys=True),
        },
    ]
    result = None
    value: dict[str, Any] | None = None
    last_error: Exception | None = None
    # One compiler-guided repair is enough to recover common notation mistakes
    # without turning generation into an open-ended autonomous loop. Both calls
    # share the same trace id and hard budget ceiling.
    for attempt in range(2):
        result = call_llm(
            model,
            messages,
            task="world-substrate-mechanic-authoring",
            trace_id=trace_id,
            max_budget=max_budget,
            max_tokens=max_output_tokens,
            reasoning_effort=reasoning_effort,
            num_retries=1,
            # The shared client requires a stated reason for any non-default route.
            **({"model_justification": model_justification} if model_justification else {}),
            # An llm_client OpenRouterRoutePolicyV1, e.g. the World Builder's fastest-provider route.
            **({"openrouter_route_policy": route_policy} if route_policy else {}),
        )
        try:
            parsed = safe_json_loads(result.content)
            if not isinstance(parsed, dict):
                raise ValueError("model returned a non-object causal model")
            value = merge_revision(previous, parsed) if revising else parsed
            tidied = tidy_proposal(value, bundle)
            compiled = CausalModel.from_dict(value, bundle=bundle)
            no_ops = no_op_effects(value)
            if no_ops:
                raise ValueError(
                    "these effects change nothing, so their moves would never be offered to anyone: "
                    + "; ".join(no_ops) + ". Give each an effect that changes represented state as its description "
                    "says (for example add 1 to a count or set a stage), or remove the effect"
                )
            review = compiled.as_review()
            out = deepcopy(value)
            out["review"] = review
            if tidied:
                out["review"]["tidied"] = tidied
            return out, result
        except (ValueError, TypeError, KeyError) as error:
            last_error = error
            if attempt == 1:
                break
            messages = [
                *messages,
                {"role": "assistant", "content": result.content},
                {
                    "role": "user",
                    "content": (
                        "The local causal compiler rejected that proposal. "
                        f"Compiler error: {type(error).__name__}: {error}. "
                        + ("Return a corrected JSON object only, again holding only what changes from "
                           "previous_proposal. " if revising else "Return a corrected JSON object only. ")
                        + "State paths in participant/path and "
                        "effect/path fields must be copied EXACTLY from allowed_state_paths; do not "
                        "abbreviate component containers (for example use portable.portable, not portable)."
                    ),
                },
            ]
    assert last_error is not None
    raise ValueError(f"causal proposal remained invalid after one repair: {last_error}") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--trace-id")
    parser.add_argument("--max-budget", type=float, default=DEFAULT_BUDGET)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bundle = load_bundle(args.bundle)
    value, result = generate_causal_model(
        bundle,
        model=args.model,
        trace_id=args.trace_id,
        max_budget=args.max_budget,
    )
    rendered = json.dumps(value, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
        print(args.output)
    else:
        print(rendered, end="")
    cost = getattr(result, "cost", None)
    if cost is not None:
        print(f"cost_usd={cost}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
