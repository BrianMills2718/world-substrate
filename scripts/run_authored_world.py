#!/usr/bin/env python3
"""Run an authored world from a bundle plus reviewed causal declarations."""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from copy import deepcopy
from dataclasses import make_dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.bootstrap_scene_profile import _merge, bootstrap_profile
from scripts.render_scene_replay import render_html
from scripts.scaffold_world import _render_model, load_bundle, validate_bundle
from world_substrate.action_authoring import CausalModel, CompiledActionMechanic
from world_substrate.engine import Engine
from world_substrate.model import Entity, LocationState, OwnershipState, PortableState, World
from world_substrate.policy import CHOICE_SCHEMA, WAIT, present, resolve_choice
from world_substrate.profile import MechanicProfile
from world_substrate.rules import RuleRegistry

DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
DEFAULT_POLICY_BUDGET = 0.12
MAX_TURNS = 30
MAX_ACTORS = 6


def _component_types(bundle: dict[str, Any]) -> dict[str, type]:
    result: dict[str, type] = {}
    for comp in bundle.get("components") or []:
        fields = [(row["name"], object) for row in comp.get("fields") or []]
        cls_name = "".join(x.capitalize() for x in comp["name"].split("_")) + "LiveState"
        result[comp["name"]] = make_dataclass(cls_name, fields)
    return result


def build_engine(bundle: dict[str, Any], causal_value: dict[str, Any]) -> tuple[Engine, CausalModel, str]:
    bundle = validate_bundle(bundle)
    model = CausalModel.from_dict(causal_value, bundle=bundle)
    registry = RuleRegistry()
    profile = MechanicProfile()
    for declared in model.mechanics:
        compiled = CompiledActionMechanic(declared)
        findings = profile.install(declared.package(), compiled)
        rejects = [f for f in findings if f.severity == "reject"]
        if rejects:
            raise ValueError(f"mechanic installer rejected {declared.mechanic_id}: {rejects[0].code}")
        registry.register_action(compiled)
    profile_id = profile.freeze()

    types = _component_types(bundle)
    world_spec = bundle["world"]
    entities: dict[str, Entity] = {}
    for row in bundle["entities"]:
        components = {
            name: types[name](**deepcopy(values))
            for name, values in (row.get("components") or {}).items()
        }
        location_id = row.get("location") or world_spec["location"]
        entity = Entity(
            entity_id=row["id"],
            label=row["label"],
            category_ids=tuple(row["categories"]),
            location=LocationState(location_id) if location_id else None,
            ownership=OwnershipState(row["owner_ref"]) if row.get("owner_ref") is not None else None,
            portable=PortableState(bool(row["portable"])) if row.get("portable") is not None else None,
            source_pack_id=f"world-substrate-{world_spec['id']}@{world_spec.get('content_version', 1)}",
            source_entity_id=row["id"],
            components=components,
        )
        entities[entity.entity_id] = entity
    world = World(
        world_id=f"{world_spec['id']}-live",
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id=f"world-substrate-{world_spec['id']}@{world_spec.get('content_version', 1)}",
        rule_versions=registry.versions(),
    )
    world.validate()
    return Engine(world, registry), model, profile_id


def _selector_matches(entity: Entity, selector: dict[str, Any]) -> bool:
    return all(x in entity.category_ids for x in selector.get("categories", [])) and all(
        entity.component(x) is not None for x in selector.get("components", [])
    )


def actor_ids(engine: Engine, model: CausalModel) -> list[str]:
    selectors = [m.actor_selector for m in model.mechanics]
    actors = [
        entity.entity_id
        for entity in sorted(engine.world.entities.values(), key=lambda e: e.entity_id)
        if any(_selector_matches(entity, selector) for selector in selectors)
    ]
    if not actors:
        raise ValueError("causal model selects no actors in this world")
    if len(actors) > MAX_ACTORS:
        raise ValueError(f"causal model selects {len(actors)} actors; live limit is {MAX_ACTORS}")
    return actors


def _recent_for(engine: Engine, actor: str, seen: dict[str, int]) -> list[str]:
    start = seen.get(actor, 0)
    lines: list[str] = []
    for event in engine.world.events[start:]:
        bearer = (event.get("causal_bearer") or {}).get("id")
        if event.get("status") != "accepted" or not bearer:
            continue
        who = "you" if bearer == actor else bearer
        lines.append(f"{who}: {event.get('rule_id', '?')}")
    seen[actor] = len(engine.world.events)
    return lines[-6:]


def _scripted_choice(page: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    if not page.get("available"):
        return None, "wait: no offered action"
    row = page["available"][0]
    return dict(row["action"]), "first available offered action"


def _llm_choice(
    engine: Engine,
    actor: str,
    page: dict[str, Any],
    *,
    world_summary: str,
    model: str,
    trace_id: str,
    max_budget: float,
    recent: list[str],
) -> tuple[dict[str, Any] | None, str, float]:
    from llm_client import call_llm_json_schema, render_prompt

    offered = [row["action_id"] for row in page["available"]]
    if not offered:
        return None, "wait: no offered action", 0.0
    schema = json.loads(json.dumps(CHOICE_SCHEMA))
    schema["properties"]["action_id"]["enum"] = offered + [WAIT]
    context = present(engine, actor, page)
    context["recent"] = recent
    context["world_summary"] = world_summary
    messages = render_prompt(REPO / "prompts/generic_world_policy.yaml", **context)
    value, result = call_llm_json_schema(
        model,
        messages,
        schema,
        schema_name="world_substrate_live_policy_choice",
        task="world-builder-live-policy",
        trace_id=trace_id,
        max_budget=max_budget,
        reasoning_effort="low",
    )
    reasoning = str(value.get("reasoning", "")) if isinstance(value, dict) else "model returned non-object"
    action_id = str(value.get("action_id", "")) if isinstance(value, dict) else ""
    choice = resolve_choice(page, action_id, reasoning)
    return (
        dict(choice.action) if choice.kind == "action" and choice.action is not None else None,
        reasoning,
        float(getattr(result, "cost", 0.0) or 0.0),
    )


def run_world(
    bundle: dict[str, Any],
    causal_value: dict[str, Any],
    *,
    policy: str = "scripted",
    model_name: str = DEFAULT_MODEL,
    max_turns: int = 12,
    max_budget: float = DEFAULT_POLICY_BUDGET,
    trace_id: str | None = None,
) -> tuple[dict[str, Any], Engine, CausalModel]:
    if policy not in {"scripted", "llm"}:
        raise ValueError("policy must be scripted or llm")
    if type(max_turns) is not int or not 1 <= max_turns <= MAX_TURNS:
        raise ValueError(f"max_turns must be between 1 and {MAX_TURNS}")
    engine, causal_model, profile_id = build_engine(bundle, causal_value)
    actors = actor_ids(engine, causal_model)
    trace_id = trace_id or f"world-builder-live-run-{uuid.uuid4().hex}"
    transcript: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    cost = 0.0

    for turn in range(1, max_turns + 1):
        if causal_model.terminal is not None and causal_model.terminal.reached(engine.world):
            break
        revision = engine.world.revision
        intents: dict[str, dict[str, Any] | None] = {}
        reasons: dict[str, str] = {}
        for actor in actors:
            page = engine.discover(actor)
            if policy == "scripted":
                intents[actor], reasons[actor] = _scripted_choice(page)
            else:
                intent, reason, call_cost = _llm_choice(
                    engine,
                    actor,
                    page,
                    world_summary=bundle["world"]["summary"],
                    model=model_name,
                    trace_id=trace_id,
                    max_budget=max_budget,
                    recent=_recent_for(engine, actor, seen),
                )
                intents[actor], reasons[actor] = intent, reason
                cost += call_cost

        if not any(intents.values()):
            break
        shift = (turn - 1) % len(actors)
        order = actors[shift:] + actors[:shift]
        rows: dict[str, Any] = {}
        for actor in order:
            wanted = intents[actor]
            if wanted is None:
                rows[actor] = {
                    "wanted": None,
                    "did": None,
                    "status": "no_action",
                    "retried": False,
                    "said": reasons[actor],
                    "refused_because": [],
                    "lost_what_it_wanted": False,
                }
                continue
            outcome = engine.submit({**wanted, "controller": f"live:{policy}"})
            did = wanted
            retried = False
            said_retry = None
            if outcome["status"] == "stale_revision":
                retried = True
                page = engine.discover(actor)
                if policy == "scripted":
                    again, said_retry = _scripted_choice(page)
                else:
                    again, said_retry, call_cost = _llm_choice(
                        engine,
                        actor,
                        page,
                        world_summary=bundle["world"]["summary"],
                        model=model_name,
                        trace_id=trace_id,
                        max_budget=max_budget,
                        recent=_recent_for(engine, actor, seen),
                    )
                    cost += call_cost
                if again is None:
                    did = None
                    outcome = {"status": "nothing_left", "event": {"checks": []}}
                else:
                    did = again
                    outcome = engine.submit({**again, "controller": f"live:{policy}"})
            row = {
                "wanted": wanted,
                "did": did,
                "status": outcome["status"],
                "retried": retried,
                "said": reasons[actor],
                "refused_because": [
                    c["label"]
                    for c in outcome.get("event", {}).get("checks", [])
                    if not c.get("ok") and c.get("label") != "Base revision is current"
                ],
                "lost_what_it_wanted": bool(retried and did != wanted),
            }
            if said_retry is not None:
                row["said_on_retry"] = said_retry
            rows[actor] = row
        engine.advance(1)
        transcript.append(
            {
                "turn": turn,
                "revision_when_decided": revision,
                "committed_first": order[0],
                "actors": rows,
                "progress": {},
            }
        )

    terminal_reached = bool(
        causal_model.terminal is not None and causal_model.terminal.reached(engine.world)
    )
    if not transcript:
        raise ValueError("run produced no actions; review actor selectors, checks, and parameter choices")
    trace = {
        "schema_version": "world-substrate-contested-run/v3",
        "world": bundle["world"]["id"],
        "actors": actors,
        "model": model_name if policy == "llm" else "scripted-first-available",
        "cost_usd": round(cost, 6),
        "mechanic_profile_id": profile_id,
        "summary": {
            "turns": len(transcript),
            "terminal_reached": terminal_reached,
            "accepted_actions": sum(
                1
                for t in transcript
                for row in t["actors"].values()
                if row.get("status") == "accepted"
            ),
        },
        "transcript": transcript,
    }
    return trace, engine, causal_model


def _runtime_catalog(bundle: dict[str, Any], causal_model: CausalModel | None = None) -> dict[str, Any]:
    catalog = json.loads((REPO / "reference_worlds/scene-asset-catalog-v0.json").read_text())
    world_id = bundle["world"]["id"]
    presentation = bundle.get("presentation") or {}
    assets = deepcopy(presentation.get("assets") or {})
    fallback = "live_default"
    assets.setdefault(fallback, {"kind": "text", "value": "●"})
    catalog["assets"].update(assets)
    catalog.setdefault("world_assets", {})[world_id] = sorted(assets)
    # Exact entity bindings in the shared catalog belong to retained reference
    # worlds, but their keys are bare entity ids. A fresh authored world may
    # legitimately reuse one of those ids (for example `bo`) without inheriting
    # another world's presentation identity. Its own category/presentation
    # declarations must win, so remove only collisions for entities it defines.
    exact_bindings = catalog.setdefault("entity_bindings", {})
    declared_category_assets = presentation.get("category_assets") or {}
    for entity in bundle.get("entities") or []:
        exact_bindings.pop(entity["id"], None)
        # An authored category asset is explicit world-local presentation
        # authority. Materialize it as an exact binding so broader shared
        # component-value defaults cannot override it later in bootstrap.
        for category in entity.get("categories") or []:
            if category in declared_category_assets:
                exact_bindings[entity["id"]] = {
                    "asset": declared_category_assets[category]
                }
                break
    category_bindings = catalog.setdefault("category_entity_bindings", {})
    for category, asset in declared_category_assets.items():
        category_bindings[category] = {"asset": asset}
    for entity in bundle.get("entities") or []:
        for category in entity.get("categories") or []:
            category_bindings.setdefault(category, {"asset": fallback})
    station_bindings = catalog.setdefault("category_station_bindings", {})
    for category, role in (presentation.get("station_roles") or {}).items():
        station_bindings[category] = {"role": role}

    # Derive only presentation consequences that are structurally explicit in
    # the causal declaration.  This does not guess from the action verb.  If an
    # effect says a represented participant's ownership becomes actor:<actor>,
    # the replay may safely visualize that participant as taken/carried.
    action_bindings = catalog.setdefault("action_visual_bindings", {})
    if causal_model is not None:
        for mechanic in causal_model.mechanics:
            projection: dict[str, Any] = {}
            for effect in mechanic.effects:
                if (
                    effect.get("participant") in mechanic.participants
                    and effect.get("path") == "ownership.owner_ref"
                    and effect.get("op") == "set"
                    and effect.get("value") == {"owner_ref": "actor"}
                ):
                    projection.update(
                        {
                            "item_field": effect["participant"],
                            "ownership": "take",
                            "clear_item_station": True,
                            "actor_target": {"entity_field": "$item_field"},
                        }
                    )
            if projection and mechanic.action_kind not in action_bindings:
                action_bindings[mechanic.action_kind] = {
                    "complete": True,
                    "projection": projection,
                }
    return catalog


def render_run(
    bundle: dict[str, Any],
    trace: dict[str, Any],
    causal_model: CausalModel | None = None,
) -> str:
    model = _render_model(bundle)
    catalog = _runtime_catalog(bundle, causal_model)
    profile = bootstrap_profile(
        model,
        trace,
        catalog,
        world_model_ref=f"{bundle['world']['id']}-v0.json",
        auto_layout=True,
    )
    # load_scene_profile normally supplies these presentation defaults. Fresh
    # runs bootstrap in memory, so normalize the same generic carry geometry
    # before handing the profile to render_html.
    for actor in profile.get("actors", {}).values():
        actor.setdefault("carry_offset", [5, 3])
        actor.setdefault("carry_spacing", [0, 5])
    by_id = {row["entity_id"]: row for row in model["entities"]}
    return render_html(trace, profile, by_id, REPO)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("causal_model", type=Path)
    parser.add_argument("--policy", choices=["scripted", "llm"], default="scripted")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--turns", type=int, default=12)
    parser.add_argument("--max-budget", type=float, default=DEFAULT_POLICY_BUDGET)
    parser.add_argument("--trace-output", type=Path)
    parser.add_argument("--html-output", type=Path)
    args = parser.parse_args()
    bundle = load_bundle(args.bundle)
    causal = json.loads(args.causal_model.read_text())
    causal.pop("review", None)
    trace, _, compiled = run_world(
        bundle,
        causal,
        policy=args.policy,
        model_name=args.model,
        max_turns=args.turns,
        max_budget=args.max_budget,
    )
    if args.trace_output:
        args.trace_output.write_text(json.dumps(trace, indent=2) + "\n")
    if args.html_output:
        args.html_output.write_text(render_run(bundle, trace, compiled))
    print(json.dumps(trace["summary"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
