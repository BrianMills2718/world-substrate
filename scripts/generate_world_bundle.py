#!/usr/bin/env python3
"""Propose a world-authoring bundle from a plain-English description.

This is the first half of natural-language building in the World Builder. The
model proposes *represented structure only* (components, entities, action
signatures, presentation hints). It does not author consequences: executable
law still comes from `generate_causal_model`, is compiled locally, and must be
explicitly approved before any run. `validate_bundle` is the authority gate
here; up to two validator-guided repairs are allowed.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.scaffold_world import FIELD_TYPES, SCHEMA_VERSION, BundleError, validate_bundle

DEFAULT_MODEL = "openrouter/openai/gpt-6-luna"
DEFAULT_BUDGET = 0.08
MAX_BUNDLE_OUTPUT_TOKENS = 16000
MAX_DESCRIPTION_CHARS = 2000
EXAMPLE = REPO / "examples/world_authoring/orchard-v0.json"

# Task worlds stay small enough to watch finish; ongoing and open worlds may be
# whole systems (Brian, 2026-10-06, testing the "I, Pencil" supply chain: "i want
# to see a full kind of continually running system").
SIZE_RULES = [
    "Size: follow world_size_rule.",
    "At least one entity is an actor that can act (give it a component such as worker/person and a clear category).",
    "Every action must be something an actor in this world could plausibly do repeatedly until the situation resolves.",
    "Represent the state the actions change (e.g. stage, count, location) as component fields with typed defaults.",
    # Brian, 2026-10-26, on an I, Pencil world that left out revenue, prices, distances, delivery times and
    # packaging: "why are we leaving these out". Each is ordinary represented state.
    "Represent money and value the description mentions or implies (any selling, buying, paying, wages or "
    "prices): a number field for each actor's or business's cash, "
    "and a price field on what is sold; a sale or purchase action moves the goods one way and the money the "
    "other. Represent feelings or relationships (mood, trust, hunger) as number fields when they change what "
    "people do.",
    # 2026-10-27 pencil1 live build (share Y-OQRAo16ekn): every specialist had a make step but none could pass
    # its output on, so the mill asked the logger for logs and the lead works asked the miner for graphite for
    # six rounds, matched no action, and the chain never got past cutting and mining; only the shop and the
    # customer held cash.
    # 2026-10-26 pencil build (share NZD33sh3iX29): clay, paint, erasers and ferrules had no maker and started at 0.
    "Every material a step uses must come from somewhere in the world: an actor who makes, mines or supplies it "
    "(a clay pit, a paint supplier) or a starting stock large enough for many rounds; never leave an input that "
    "nobody makes and nobody holds.",
    "Every step that turns things into something else needs a field for what it makes (packing pencils needs a "
    "packed_pencils count, and the next move carries packed pencils), and every move that answers a waiting need "
    "(serving an order, treating a patient) needs a field naming where that need is counted, so the move can lower it.",
    "Wherever one actor's output is another actor's input, declare an action that moves it from the one to "
    "the other (deliver, sell to, buy from), with entity_ref fields naming both, so goods can travel the whole "
    "chain; give every actor that buys a starting cash amount large enough for several purchases.",
    # 2026-10-27 pencil5 live build (share c_SrKPfa3rpE): every hand-over was a give move (supply-clay, saw-logs
    # ... to), so the lead-maker and the factory tried to "buy 100 graphite" in 28 rounds and matched nothing, and
    # every move required the two sides to be together although each business sat in its own place. pencil
    # czt5uoGw5t3L asked for price times quantity, which rules cannot write: 8 clay cost the price of one.
    "When the actors hold cash, goods change hands by purchase: for each good one actor needs from another, "
    "declare a buy move the receiver starts (buy graphite from the miner) with entity_ref fields for the buyer "
    "and seller and a quantity, which moves the goods to the buyer and the seller's price for the order to the "
    "seller (rules cannot multiply, so a price is per order), and refuses when the buyer cannot pay or the "
    "seller has too few. A hand-over between "
    "actors in different places must not require them to be together: it is an order sent from afar, and "
    "the goods arrive by a delivery that counts down rounds.",
    "Represent anything that takes several rounds (a delivery on the road, a shipment, a journey, a "
    "deadline) as an integer field counting the rounds left, set by the action that starts it, so a rule "
    "process can count it down each round and finish it at zero; a longer distance is a larger starting count.",
    "Represent packaging, containers and small materials the description names as their own entities or "
    "counted stock rather than dropping them.",
    # 2026-10-26 (evidence/build-quality/README.md, #260 airfield build): three rule attempts wrote no same-moment
    # knock-on process because no action could knock, drop or spill anything, so nothing could set one off.
    "Besides their job steps, give the actors at least one ordinary physical move that can upset the things "
    "around them, whenever the world has loose objects (stacks, cups, trays, lamps, crates): knocking over, "
    "dropping, pushing, pouring or breaking, each with an entity_ref field naming the thing it acts on. Represent where things rest and what state "
    "they are in as fields (an entity_ref 'on' or 'under', booleans such as upright, wet, broken, lit), so a "
    "rule can make one change set off another at once (a tipped cup wets what is under it).",
    # 2026-10-26 live cafe build (share dI4j2qUYPBBZ): tip-stack set the plates' upright to false, but the
    # plates had no broken field and nothing under them, so no knock-on could follow and none was written.
    "For each such move, represent what it would set off, not only the move itself: give fragile things a "
    "broken boolean, containers a full or spilled boolean, and set each loose object's 'on' to the thing it "
    "starts on (a table, a laptop, the floor), so that a fall or spill has something to break or wet.",
    "Follow world_kind_rule: a task world must be able to finish (represented state from which 'done' can be read); ongoing and open worlds must have state that keeps changing.",
]


def _contract() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "world": "{id (lowercase-slug), label, summary (one sentence), location (slug), content_version: 1}",
        "components": "[{name (python identifier), fields: [{name, type, default}]}]",
        "field_types": sorted(FIELD_TYPES),
        "entities": (
            "[{id (lowercase-slug), label, categories: [nonempty strings], components: {component: {every declared field}},"
            " optional portable: bool, optional owner_ref: 'actor:<id>'|'place:<id>'|'entity:<id>'|'unowned',"
            " optional location: <id of the place entity it starts in>}]"
            " (owner_ref: use 'actor:<id>' when the owner is a person or business that acts; 'entity:<id>' only for"
            " a thing held inside another thing)"
        ),
        "actions": "[{kind (lowercase-slug), description, fields: [{name, type in string|integer|number|boolean|entity_ref}]}]",
        "reserved_action_field_names": ["actor", "kind", "base_revision", "controller"],
        "presentation": (
            "{assets: {asset_id: {kind: 'emoji', value}}, category_assets: {category: asset_id},"
            " station_roles: {category: one of source|workstation|surface|goal}} (station_roles may be {})"
        ),
        # declared-laws plan S1, 2026-10-28: the world states its own conservation laws in its own terms, so the
        # engine can later keep them and name the one a move would break (docs/plans/declared_laws.md).
        "resources": (
            "Optional top-level list of the things this world keeps count of that must never appear or vanish "
            "except in the ways its laws allow: [{resource_id (lowercase-slug), says (one plain sentence), "
            "kept_in: [{component, field}] naming every integer or number field that holds an amount of it}]. "
            "Money, stock of goods and stored materials are typical; feelings and scores are not."
        ),
        "laws": (
            "Optional top-level list of what must stay true about those resources, in this world's own terms. "
            "Two shapes. A total law: {law_id (lowercase-slug), says, resource, may_change_by: [action kinds, or "
            "'process:<name>' for something the world does by itself]} means the resource's world total changes "
            "only through those; every other move only moves it between holders. List every move that makes the "
            "resource AND every move that uses it up: logs are made by cutting and used up by sawing them into "
            "slats, so a logs law lists both cut-cedar and saw-slats; a pencils law lists the move that makes "
            "pencils and the move that packs them into boxes or a customer uses them. If the world itself adds or "
            "removes some each round (trees regrow, bread goes stale), list it as 'process:<a short slug>'; the "
            "rules writer will give that process exactly this id. A move you leave out will be refused whenever it "
            "changes the total. A pairing law: {law_id, says, move: action kind, "
            "gives: {resource, from, to}, pays: {resource, from, to}} means that move always hands one thing over "
            "in return for another, where from and to are 'actor' or one of that action's entity_ref field names "
            "and whoever gives is whoever is paid (a sale: gives pencils shop->customer, pays money customer->shop). "
            "Use [] for both when nothing in the description is kept count of."
        ),
        "not_modeled": (
            "Top-level list of short plain-English strings naming every part of the description you could NOT "
            "represent with this format. Almost everything can be: money, prices, revenue, wages, feelings and "
            "distances are number fields; places are entities; packaging and small materials are entities or "
            "counted stock; delivery and travel times and deadlines are round counts. List only what truly cannot "
            "be (dice-roll chance, real clock time). Use [] when everything was represented."
        ),
        "rules": [
            "Every entity component object must list exactly the component's declared fields, with values of the declared type.",
            "entity_ref values must name an entity id that exists in this bundle.",
            # #179, 2026-10-19 (pencil c4-run10, trace world-builder-live/world/299ad248382d414ba7b65867475a002f):
            # deliver-pencils had only a quantity field, so its rules could change nobody but the carrier and
            # pencils never reached the shop, however often the rules were rewritten.
            # 2026-10-19 c4-run11 (trace world-builder-live/world/98ca1f40...): naming 'from' as an example made the
            # first draft fail validation ('from' is a Python keyword), costing one retry.
            "An action that passes something to, or takes something from, another entity (hand over, deliver, "
            "carry to, supply, sell to, buy from) must have an entity_ref field naming that other entity (for "
            "example 'to', 'source' or 'customer'; field names are Python identifiers, so never 'from'); rules can "
            "only change the actor and the entities its fields name.",
            # 2026-10-19 c4-run12 (trace world-builder-live/world/0b7b5626...): serve-pencil-order named only the
            # customer, so its rules checked pencils on the customer instead of the shop and the shopkeeper never
            # acted through four rule rewrites; rules cannot add the missing field, only this step can.
            "When goods move between two entities and neither is the actor (a shopkeeper selling the shop's pencils "
            "to a customer, a carrier moving stock from the factory to the shop), the action needs an entity_ref "
            "field for each of them (for example 'shop' and 'customer', or 'source' and 'to').",
            # 2026-10-20 c4-run13 (trace world-builder-live/world/fc37d615...): one carry-goods action with a text
            # 'goods' field could only ever move boards, since a rule names fixed quantities; logs never reached the
            # sawmill and five workers stayed idle through three rule rewrites.
            "Rules change fixed, named quantities and cannot choose which one from a text field, so when different "
            "goods move, declare one action per kind of goods (carry-logs, carry-boards), never one carry-goods "
            "action with a field naming the goods.",
            # open_attempt Q23, 2026-10-25 (evidence/open-attempt/q23/): the airfield office and hangar were plain
            # entities while everyone stood at the one world location, so 'Sam and the helicopter are in the same
            # place' was always true, nobody could move, and the brick wall between them limited nothing.
            "When the description names separate places (rooms, buildings, fields, towns), make each place an "
            "entity with category 'place', set every other entity's location to the place it starts in, and give "
            "the actors a move action with an entity_ref field 'to' naming the destination place and an "
            "entity_ref field 'way' naming what they go through. Represent what lies between two places (a door, "
            "a corridor, a wall, a river) as an entity whose component has entity_ref fields naming both places "
            "and a boolean saying whether it can be passed (a brick wall: false; an open door: true).",
            "Labels and descriptions are plain English a visitor would use (\"Ava\", \"watering can\"), never internal jargon.",
            *SIZE_RULES,
        ],
    }


WORLD_KINDS = ("task", "ongoing", "open")
SIZE_BY_KIND = {
    "task": "2 to 16 entities; 1 to 6 components; 1 to 6 actions.",
    "ongoing": (
        "A whole working system, typically 10 to 40 entities with at most 12 that can act, up to 10 components and 3 to 12 actions. Model it "
        "as a chain or web of specialists: several actors, each with their own role who can only do their own "
        "step (for a supply chain: raw-material producers, processors, makers of parts, assembly, transport, "
        "shops, customers), with intermediate goods passed between them as counted stock (integer quantity "
        "fields), so goods flow from one specialist to the next. If the description is about people living "
        "rather than producing, model several residents with their own needs and stocks and the resources "
        "they depend on, as counted quantities that can be produced, traded or consumed."
    ),
}
KIND_RULES = {
    "task": "World kind: task. There is a job to finish; make sure 'done' can be read from represented state.",
    "ongoing": (
        "World kind: keeps running. Nothing is ever finally done: work keeps arriving, or people keep living. Represent the state that "
        "lets work recur (for example an order's stage that can return to waiting, a plant's thirst counter, a "
        "count of waiting items) so the world can keep generating things to do. If it is about people living "
        "rather than working, give them needs or resources that change over time (hunger, energy, supplies, "
        "growth) as component fields, and several actions to look after them."
    ),
}
# 'open' is an older name for the same kind (merged 2026-10-06: Brian asked whether they
# really needed to be different; nothing but this advice ever differed).
SIZE_BY_KIND["open"] = SIZE_BY_KIND["ongoing"]
KIND_RULES["open"] = KIND_RULES["ongoing"]


def _messages(description: str, world_kind: str = "task") -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": (
                "You turn a plain-English description of a small situation into the represented structure "
                "of a governed simulation. Return exactly one JSON object and no prose or markdown. "
                "You are describing what exists and what actors may attempt, not what happens: do not "
                "describe consequences or rules, beyond the resources and laws the contract asks for. Follow the contract exactly; the example shows the format."
            ),
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "description": description,
                    "world_kind": world_kind,
                    "world_kind_rule": KIND_RULES[world_kind],
                    "world_size_rule": SIZE_BY_KIND[world_kind],
                    "contract": _contract(),
                    "example_bundle": json.loads(EXAMPLE.read_text()),
                },
                indent=2,
            ),
        },
    ]


MAX_REPAIRS = 2


def generate_world_bundle(
    description: str,
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    reasoning_effort: str = "low",
    world_kind: str = "task",
    feedback: str = "",
    previous: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str], Any]:
    """Return (validated bundle, parts of the description not represented, last LLM result).

    With ``feedback`` and the ``previous`` bundle, the model redesigns that structure from what a test run of
    rules written for it showed; rule rewrites alone cannot add a missing action or field.
    """
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a nonempty string")
    if len(description) > MAX_DESCRIPTION_CHARS:
        raise ValueError(f"description must be at most {MAX_DESCRIPTION_CHARS} characters")
    from llm_client import call_llm, safe_json_loads

    trace_id = trace_id or f"world-builder-bundle-{uuid.uuid4().hex}"
    if world_kind not in WORLD_KINDS:
        raise ValueError(f"world_kind must be one of {WORLD_KINDS}")
    messages = _messages(description.strip(), world_kind)
    if feedback and previous is not None:
        messages += [
            {"role": "assistant", "content": json.dumps(previous)},
            {
                "role": "user",
                "content": (
                    "Rules were written for that structure and test-run, and this is what happened: "
                    f"{feedback.strip()[:3000]} Rules can only change the actor and the entities its fields name, and "
                    "cannot add actions or fields. Return a corrected structure (JSON object only) whose actions and "
                    "fields let every step and every actor happen, keeping what already worked. Keep the world's "
                    "resources and laws, updated for every action you add, rename or change: a move that makes or "
                    "uses up a resource belongs in that law's may_change_by, and a trade its pairing law names must "
                    "still exist."
                ),
            },
        ]
    last_error: Exception | None = None
    for attempt in range(MAX_REPAIRS + 1):
        result = call_llm(
            model,
            messages,
            task="world-substrate-world-authoring",
            trace_id=trace_id,
            max_budget=max_budget,
            max_tokens=MAX_BUNDLE_OUTPUT_TOKENS,
            reasoning_effort=reasoning_effort,
            num_retries=1,
        )
        try:
            parsed = safe_json_loads(result.content)
            if not isinstance(parsed, dict):
                raise BundleError("model returned a non-object bundle")
            not_modeled = parsed.pop("not_modeled", [])
            if not isinstance(not_modeled, list) or not all(isinstance(x, str) for x in not_modeled):
                raise BundleError("not_modeled must be a list of strings")
            bundle = validate_bundle(parsed)
            if not bundle["actions"]:
                raise BundleError("bundle must declare at least one action")
            if previous is not None and previous.get("laws") and not bundle.get("laws"):
                # S2 pencil build Fw7SHbEtW3Un: the redesign returned no laws at all though the design it revised
                # declared 17, so the kept world ran with none (evidence/declared-laws/s2-pencil/).
                raise BundleError(
                    "the redesign dropped the world's resources and laws; return them, updated for the new actions"
                )
            return bundle, [x.strip() for x in not_modeled if x.strip()][:8], result
        except (BundleError, ValueError, TypeError, KeyError) as error:
            last_error = error
            if attempt == MAX_REPAIRS:
                break
            messages = [
                *messages,
                {"role": "assistant", "content": result.content},
                {
                    "role": "user",
                    "content": (
                        "The local bundle validator rejected that proposal. "
                        f"Validator error: {type(error).__name__}: {error}. "
                        "Return a corrected JSON object only."
                    ),
                },
            ]
    assert last_error is not None
    raise ValueError(f"world proposal remained invalid after {MAX_REPAIRS} repairs: {last_error}") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-budget", type=float, default=DEFAULT_BUDGET)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bundle, not_modeled, result = generate_world_bundle(args.description, model=args.model, max_budget=args.max_budget)
    rendered = json.dumps(bundle, indent=2) + "\n"
    if not_modeled:
        print("not modeled: " + "; ".join(not_modeled), file=sys.stderr)
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    print(f"model={getattr(result, 'model', args.model)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
