#!/usr/bin/env python3
"""Run an authored world from a bundle plus reviewed causal declarations."""
from __future__ import annotations

import argparse
import contextvars
import json
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import make_dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts import attempts
from scripts.bootstrap_scene_profile import _merge, bootstrap_profile
from scripts.render_scene_replay import render_html
from scripts.scaffold_world import _render_model, load_bundle, validate_bundle
from world_substrate.action_authoring import CausalModel, CompiledActionMechanic, CompiledProcessMechanic
from world_substrate.engine import ENGINE_OWNED_PATHS, Engine
from world_substrate.model import Entity, LocationState, OwnershipState, PortableState, World
from world_substrate import attempt as open_attempt
from world_substrate.policy import CHOICE_SCHEMA, WAIT, present, resolve_choice

# Concordia residents (scripts/concordia_residents.py, imported lazily: Concordia is a live-play dependency).
MOVER = "llm-resident (Concordia)"
MEMORY_ITEMS = 12  # notes each resident remembers: a round's news and its own move are one note each
MEMORY_ITEM_CHARS = 600
from world_substrate.profile import MechanicProfile
from world_substrate.rules import RuleRegistry

DEFAULT_MODEL = "openrouter/openai/gpt-6-luna"
DEFAULT_POLICY_BUDGET = 0.12
MAX_TURNS = 30
MAX_BLOCKED_RECORDED = 3
# A whole supply chain needs several specialists; each run's spend is capped by
# DEFAULT_POLICY_BUDGET regardless of how many act.
MAX_ACTORS = 12


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
    for order, declared_process in enumerate(model.processes, start=1):
        compiled_process = CompiledProcessMechanic(declared_process, order)
        findings = profile.install(declared_process.package(), compiled_process)
        rejects = [f for f in findings if f.severity == "reject"]
        if rejects:
            raise ValueError(f"mechanic installer rejected {declared_process.process_id}: {rejects[0].code}")
        registry.register_process(compiled_process)
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


# Other people's `work` records (compile_spec.add_work_cycle: one done-flag per action) are bookkeeping that limits
# repeats, not something a person sees or acts on. 2026-10-18 live Waltzman 1nEGWZzSwHFA: nine of them were 4,500 of
# a resident prompt's 15,000 characters.
PRIVATE_TO_HOLDER = ("work",)


def _view(engine: Engine, actor: str, page: dict[str, Any]) -> dict[str, Any]:
    """present() without other people's private bookkeeping records."""
    entities = {
        eid: (rec if eid == actor else {**rec, "components": {k: v for k, v in (rec.get("components") or {}).items()
                                                               if k not in PRIVATE_TO_HOLDER}})
        for eid, rec in page["observation"]["entities"].items()
    }
    return present(engine, actor, {**page, "observation": {**page["observation"], "entities": entities}})


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


WORLD = "world"  # who started a task a world process started (attempts.world_watchers)


def _run_event_id(turn: int, event_id: str | None) -> str | None:
    """An event id unique across the whole run. Live play runs each round in a fresh Engine restored from the last
    snapshot, so the Engine's own ids start again every round (2026-10-16 Waltzman: e00001 named 40 different moves,
    and the readout's checked citations pointed at the wrong ones)."""
    return f"r{turn}-{event_id}" if event_id else None


def _state_changes(event: dict[str, Any]) -> list[dict[str, Any]]:
    """An event's changes minus the engine's own bookkeeping (revision, cause stamps)."""
    return [
        c for c in event.get("changes") or []
        if c.get("path") not in ENGINE_OWNED_PATHS and not str(c.get("path", "")).endswith(".last_cause_event_id")
    ]


def _round_reactions(events: list[dict[str, Any]], turn: int) -> dict[str, Any]:
    """This round's knock-on effects (open_attempt S2), each naming the event and rule that set it off.

    Returns {} when there were none, so transcripts of worlds without immediate processes are unchanged."""
    rules = {e["event_id"]: e["rule_id"] for e in events}
    reactions = [
        {"event_id": _run_event_id(turn, e["event_id"]), "rule_id": e["rule_id"], "wave": e["reaction_wave"],
         "caused_by": [_run_event_id(turn, p) for p in e.get("causal_parent_event_ids") or []],
         "caused_by_rule": [rules.get(p, p) for p in e.get("causal_parent_event_ids") or []],
         "changes": _state_changes(e)}
        for e in events if "reaction_wave" in e
    ]
    return {"reactions": reactions} if reactions else {}


def _read_attempt(engine: Engine, actor: str, text: str | None, signatures: list[dict[str, Any]], *, model: str,
                  trace_id: str, max_budget: float) -> tuple[dict[str, Any], float]:
    """One person's words read into a typed move (world_substrate.attempt). A wait costs no call."""
    if not text or text.strip().lower() in {WAIT, "wait."}:
        return {"kind": open_attempt.WAIT_KIND, "fields": {}, "quoted_spans": {}, "nearest_kind": open_attempt.NONE,
                "why": "the person waited"}, 0.0
    labels = {eid: entity.label for eid, entity in sorted(engine.world.entities.items())}
    return open_attempt.interpret(text, actor=actor, signatures=signatures, entities=labels, model=model,
                                  trace_id=trace_id, max_budget=max_budget)


def _same_move(one: dict[str, Any] | None, other: dict[str, Any] | None) -> bool:
    """The same action, ignoring the world revision it was chosen against."""
    if one is None or other is None:
        return one is other
    drop = ("base_revision", "controller")
    return {k: v for k, v in one.items() if k not in drop} == {k: v for k, v in other.items() if k not in drop}


def _field(path: str) -> str:
    """"entities.<x>.components.work.done" -> "components.work.done"."""
    parts = path.split(".")
    return ".".join(parts[2:]) if parts[:1] == ["entities"] and len(parts) > 2 else path


def _paths_in(value: Any) -> set[str]:
    if isinstance(value, dict):
        found = {value["path"]} if isinstance(value.get("path"), str) else set()
        for item in value.values():
            found |= _paths_in(item)
        return found
    if isinstance(value, (list, tuple)):
        return set().union(*(_paths_in(item) for item in value)) if value else set()
    return set()


def bookkeeping_fields(model: CausalModel) -> dict[str, set[str]]:
    """Per action kind, the fields it writes that only its own checks ever read.

    A generated move often carries a "not already done this meeting" flag. When
    that flag is all the move changes and no other rule (nor the ending) reads it,
    the move does nothing, yet it looked useful to the no-op filter. In one live
    run members chose such a move ("discuss concern at meeting") in 88% of rounds
    10-40 (2026-10-16, deploy10). Fields read by any other rule stay real effects;
    so do fields no rule reads at all, since a person or the readout may.
    """
    readers: dict[str, set[str]] = {}
    def note(rule_id: str, paths: Any) -> None:
        for path in paths:
            field = _field(path)
            if field.count(".") >= 2:  # a field, not just "has this component"
                readers.setdefault(field, set()).add(rule_id)
    for m in model.mechanics:
        note(m.mechanic_id, m.read_paths)
    for p in model.processes:
        note(p.process_id, p.read_paths)
    if model.terminal is not None:
        note("terminal", _paths_in(list(model.terminal.checks)))
    return {
        m.action_kind: {f for f in map(_field, m.write_paths) if readers.get(f) == {m.mechanic_id}}
        for m in model.mechanics
    }


def _without_no_ops(engine: Engine, page: dict[str, Any], *, bookkeeping: dict[str, set[str]] | None = None) -> dict[str, Any]:
    """Drop allowed actions that would change nothing right now.

    A rule can allow a move whose effects leave the world exactly as it was (for
    example "set the order to waiting" on an order that is already waiting).
    Choosing it forever looked like a busy world (2026-10-06: two cooks did
    nothing but "record salad order" every round). Each candidate is tried on a
    scratch copy of the world; only moves that change something stay on offer.
    """
    useful = []
    scratch = None
    for row in page.get("available") or []:
        # A refused move leaves the world unchanged, so one scratch copy serves until a move is accepted.
        scratch = scratch or engine.scratch()
        outcome = scratch.submit({**row["action"], "controller": "preview"})
        own = (bookkeeping or {}).get(row["action"].get("kind", ""), set())
        if outcome.get("status") == "accepted":
            scratch = None
            if any(_field(c.get("path", "")) not in own for c in _state_changes(outcome["event"])):
                useful.append(row)
    return {**page, "available": useful}


def _scripted_choice(page: dict[str, Any], last_done: dict[str, int] | None = None) -> tuple[dict[str, Any] | None, str]:
    """The allowed move this actor has done least recently (never done first), ties in offered order.

    2026-10-21 live pencil runs at 183b47a: always taking the first allowed move kept a timber crew cutting logs
    forever and never loading them (c4-run17 -n_b5cczQ5wa: sawmill and pencil maker idle), and a shopkeeper
    ordering forever and never selling (c4-run18 hkoxuPW7HK7B). The build's dry run used the same rule, so it
    reported idle workers that no rewrite of the rules could fix.
    """
    if not page.get("available"):
        return None, "waited: the rules allowed nothing right now"
    last_done = last_done or {}
    row = min(page["available"], key=lambda r: last_done.get(r["action"].get("kind", ""), -1))
    return dict(row["action"]), "chose the allowed move it had done least recently"


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
    brief: str = "",
) -> tuple[dict[str, Any] | None, str, float]:
    from llm_client import call_llm_json_schema, render_prompt

    offered = [row["action_id"] for row in page["available"]]
    if not offered:
        return None, "wait: no offered action", 0.0
    schema = json.loads(json.dumps(CHOICE_SCHEMA))
    schema["properties"]["action_id"]["enum"] = offered + [WAIT]
    context = _view(engine, actor, page)
    context["recent"] = recent
    context["world_summary"] = world_summary
    context["brief"] = brief
    messages = render_prompt(REPO / "prompts/generic_world_policy.yaml", **context)
    value, result = call_llm_json_schema(
        model,
        messages,
        schema,
        schema_name="world_substrate_live_policy_choice",
        task="world-builder-live-policy",
        trace_id=trace_id,
        max_budget=max_budget,
        max_tokens=512,
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


def _never_why(kind: str, failed: list[dict[str, Any]], causal_value: dict[str, Any]) -> str:
    """Why a move was never possible: its closest refusal's failed checks, each with what raises the state it reads.
    2026-10-18 live pencil ML-LqyMAzAYo: assemble-pencils needed the assembler's own stock.slats, which only mill-slats
    raised, on the miller's own stock; nothing carried slats over, and the rewrite was never told so."""
    mechanics = causal_value.get("mechanics") or []
    rule = next((m for m in mechanics if m.get("action_kind") == kind), {})
    reasons = []
    for c in failed[:2]:
        text = f"{c.get('label')}: was {c.get('actual')!r}, needed {c.get('required')!r}"
        left = next(((x.get("left") or {}).get("participant") for x in rule.get("checks") or []
                     if x.get("label") == c.get("label")), None) or {}
        path = left.get("path", "")
        if path.startswith("components."):
            raises = lambda e: e.get("path") == path and e.get("op") in ("add", "set")  # noqa: E731
            raisers = [f"{m['action_kind']} (on its {e.get('participant')})" for m in mechanics if m is not rule
                       for e in m.get("effects") or [] if raises(e)]
            raisers += [f"process {p['process_id']}" for p in causal_value.get("processes") or []
                        for e in p.get("effects") or [] if raises(e)]
            field = path.removeprefix("components.")
            text += (f"; {field} is raised only by " + ", ".join(dict.fromkeys(raisers)) if raisers
                     else f"; nothing ever raises {field}")
            if raisers and left.get("name") == "actor" and all(r.endswith("(on its actor)") for r in raisers):
                text += f", each on the one who does it, so no action ever brings {field} to this actor"
        reasons.append(text)
    return "; ".join(reasons)


def run_world(
    bundle: dict[str, Any],
    causal_value: dict[str, Any],
    *,
    policy: str = "scripted",
    model_name: str = DEFAULT_MODEL,
    max_turns: int = 12,
    max_budget: float = DEFAULT_POLICY_BUDGET,
    trace_id: str | None = None,
    start_snapshot: dict[str, Any] | None = None,
    turn_offset: int = 0,
    prior_recent: list[dict[str, str]] | None = None,
    briefs: dict[str, str] | None = None,
    resident_memory: dict[str, list[str]] | None = None,
    underway: list[dict[str, Any]] | None = None,
    open_attempts: bool = False,
) -> tuple[dict[str, Any], Engine, CausalModel]:
    if policy not in {"scripted", "llm", "resident"}:
        raise ValueError("policy must be scripted, llm or resident")
    if open_attempts and policy != "resident":
        raise ValueError("open_attempts needs the resident policy")
    if type(max_turns) is not int or not 1 <= max_turns <= MAX_TURNS:
        raise ValueError(f"max_turns must be between 1 and {MAX_TURNS}")
    engine, causal_model, profile_id = build_engine(bundle, causal_value)
    bookkeeping = bookkeeping_fields(causal_model)
    if start_snapshot is not None:
        # Keep going: the same approved law over the world state a previous run
        # ended in. Identity and rule versions must match, so a continuation
        # can never swap in different law.
        fresh = engine.world
        resumed = World.from_snapshot(start_snapshot, component_types=_component_types(bundle))
        for name in ("world_id", "content_id", "rule_versions", "engine_id"):
            if getattr(resumed, name) != getattr(fresh, name):
                raise ValueError(f"continue_from does not belong to this world and rule set ({name} differs)")
        engine = Engine(resumed, engine.registry)
    if type(turn_offset) is not int or turn_offset < 0:
        raise ValueError("turn_offset must be a nonnegative integer")
    actors = actor_ids(engine, causal_model)
    trace_id = trace_id or f"world-builder-live-run-{uuid.uuid4().hex}"
    # Tasks that take several rounds (#128): started by a move, ended by whatever is true in a later round. A task a
    # world process starts (the rollout) is followed the same way, with "world" as the one who started it.
    watchers = attempts.task_watchers(causal_value)
    world_watchers = attempts.world_watchers(causal_value, bundle)
    open_tasks = attempts.carried(underway, engine.world.material_dict()["entities"]) if watchers else []
    transcript: list[dict[str, Any]] = []
    seen: dict[str, int] = {}
    cost = 0.0
    residents = None
    if policy == "resident":
        # Concordia residents play the people (increment 2, best-of-all-worlds.goal.md): each keeps its own memory,
        # carried between one-round requests, and names its belief and expected effect with every move.
        from scripts.concordia_residents import Residents

        residents = Residents(actors, model=model_name, trace_id=trace_id, max_budget=max_budget,
                              memory=resident_memory, open_attempts=open_attempts)
    # Open attempts (docs/plans/open_attempt.md): what each person says they try is read into one typed move against
    # the installed rules' kinds; a reading that fits none goes in as an unmatched attempt and changes nothing.
    signatures = open_attempt.signatures_for(bundle, causal_model.mechanics) if open_attempts else []
    readings: dict[str, dict[str, Any]] = {}
    unmatched: list[dict[str, Any]] = []
    beliefs: dict[str, dict[str, Any]] = {}
    # Every move the rules offered anyone at some point, and why each other move was refused, so a build's test run
    # can name a move that never once became possible (#166: the pencil wholesaler's only move never could).
    offered_kinds: set[str] = set()
    # Per actor, the round each move kind was last chosen (scripted policy).
    last_done: dict[str, dict[str, int]] = {}
    refused_why: dict[str, list[dict[str, Any]]] = {}
    # Every Engine event in full (checks, declared paths, changes, hash chain), under run-wide ids (#123, G1).
    engine_events: list[dict[str, Any]] = []
    run_ids: dict[str, str] = {}

    for turn in range(1, max_turns + 1):
        if causal_model.terminal is not None and causal_model.terminal.reached(engine.world):
            break
        revision = engine.world.revision
        events_seen = len(engine.world.events)
        intents: dict[str, dict[str, Any] | None] = {}
        reasons: dict[str, str] = {}
        blocked_by_rules: dict[str, list[dict[str, Any]]] = {}
        pages: dict[str, dict[str, Any]] = {}
        for actor in actors:
            raw = engine.discover(actor)
            offered_kinds.update(row["action"].get("kind", "") for row in raw.get("available") or [])
            for row in raw.get("blocked") or []:
                kind = row["action"].get("kind", "")
                failed = [c for c in row.get("checks") or [] if c.get("ok") is False]
                # Keep the refusal that came closest (fewest failed checks): the first one seen is usually another
                # person's ("this worker assembles pencils: was 'grows timber'"), which says nothing about the gap.
                if failed and (kind not in refused_why or len(failed) < len(refused_why[kind])):
                    refused_why[kind] = failed
            page = _without_no_ops(engine, raw, bookkeeping=bookkeeping)
            # What the installed rules refused this actor at this moment, and why.
            # Recorded for every policy so a viewer can see refusals even when the
            # policy itself only ever picks allowed actions.
            # One example per distinct (action kind, reason), so many targets
            # refused for the same reason read as one refusal, not a flood.
            distinct: dict[tuple[str, str], dict[str, Any]] = {}
            for row in page.get("blocked") or []:
                key = (row["action"].get("kind", ""), row.get("reason", ""))
                if key not in distinct and len(distinct) < MAX_BLOCKED_RECORDED:
                    distinct[key] = {
                        "action": dict(row["action"]),
                        "reason": row.get("reason", ""),
                        # The failed checks with the values the rules saw, so a
                        # viewer or a repair can see exactly why (2026-10-06:
                        # "belongs to the worker" hid actor:clay-stock vs actor:clay-producer).
                        "failed": [
                            {"check": c.get("label"), "actual": c.get("actual"), "required": c.get("required")}
                            for c in row.get("checks") or [] if c.get("ok") is False
                        ][:3],
                    }
            blocked_by_rules[actor] = list(distinct.values())
            pages[actor] = page
            if policy == "scripted":
                intents[actor], reasons[actor] = _scripted_choice(page, last_done.get(actor))
                if intents[actor] is not None:
                    last_done.setdefault(actor, {})[intents[actor].get("kind", "")] = turn
        if policy == "resident":
            recents = {actor: _recent_for(engine, actor, seen) for actor in actors}
            if turn == 1 and prior_recent:
                for actor in actors:
                    earlier = [f"{'you' if m['actor'] == actor else m['actor']}: {m['action']}" for m in prior_recent]
                    recents[actor] = (earlier + recents[actor])[-6:]

            def _resident_turn(actor: str) -> dict[str, Any]:
                page = pages[actor]
                context = _view(engine, actor, page)
                context.update(recent=recents[actor], world_summary=bundle["world"]["summary"],
                               brief=(briefs or {}).get(actor, ""))
                residents.observe(actor, f"Round {turn + turn_offset}. What just happened: "
                                  + ("; ".join(recents[actor]) or "nothing new") + ".")
                attempt = residents.choose(actor, [row["action_id"] for row in page["available"]], context)
                if open_attempts:
                    attempt["reading"], attempt["interpreter_cost"] = _read_attempt(
                        engine, actor, attempt.get("attempt"), signatures, model=model_name, trace_id=trace_id,
                        max_budget=max_budget)
                return attempt

            with ThreadPoolExecutor(max_workers=len(actors)) as pool:
                futures = {actor: pool.submit(contextvars.copy_context().run, _resident_turn, actor) for actor in actors}
                for actor in actors:
                    attempt = futures[actor].result()
                    beliefs[actor] = attempt
                    reasons[actor] = attempt.get("reasoning") or ""
                    if open_attempts:
                        cost += attempt.pop("interpreter_cost")
                        readings[actor] = attempt.pop("reading")
                        intents[actor] = open_attempt.envelope(
                            readings[actor], actor=actor, attempt=str(attempt.get("attempt") or ""),
                            base_revision=revision, controller=f"live:{policy}")
                        continue
                    choice = resolve_choice(pages[actor], attempt.get("action_id") or WAIT, attempt.get("reasoning") or "")
                    intents[actor] = dict(choice.action) if choice.kind == "action" and choice.action is not None else None
        if policy == "llm":
            # Every actor chooses against the same world revision before anything
            # is submitted, so the choices are independent: ask in parallel. A
            # 7-business pencil chain took ~7 minutes for 12 rounds asked one
            # at a time (2026-10-06).
            recents = {actor: _recent_for(engine, actor, seen) for actor in actors}
            if turn == 1 and prior_recent:
                # Moves from before this request (live play sends the last few).
                for actor in actors:
                    earlier = [
                        f"{'you' if m['actor'] == actor else m['actor']}: {m['action']}" for m in prior_recent
                    ]
                    recents[actor] = (earlier + recents[actor])[-6:]
            with ThreadPoolExecutor(max_workers=len(actors)) as pool:
                futures = {
                    actor: pool.submit(
                        contextvars.copy_context().run,
                        _llm_choice,
                        engine,
                        actor,
                        pages[actor],
                        world_summary=bundle["world"]["summary"],
                        model=model_name,
                        trace_id=trace_id,
                        max_budget=max_budget,
                        recent=recents[actor],
                        brief=(briefs or {}).get(actor, ""),
                    )
                    for actor in actors
                }
                for actor in actors:
                    intent, reason, call_cost = futures[actor].result()
                    intents[actor], reasons[actor] = intent, reason
                    cost += call_cost

        # Simple moves are deterministic: if nobody can act and nothing changes by
        # itself, every later round would be identical, so stop. AI moves may
        # differ next round, and live play needs every round recorded.
        if policy == "scripted" and not any(intents.values()) and not causal_model.processes:
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
                    "blocked_by_rules": blocked_by_rules.get(actor, []),
                }
                if actor in readings:
                    rows[actor]["attempt"] = {"text": beliefs[actor].get("attempt"), "reading": readings[actor]}
                continue
            outcome = engine.submit({**wanted, "controller": f"live:{policy}"})
            did = wanted
            retried = False
            said_retry = None
            if outcome["status"] == "stale_revision":
                retried = True
                page = _without_no_ops(engine, engine.discover(actor), bookkeeping=bookkeeping)
                # The same move is still allowed after the earlier moves: take it at the new revision
                # without asking again. Every accepted move bumps the revision, so asking again made
                # each round a chain of one-at-a-time AI calls (2026-10-16 Waltzman deploy8: 183
                # re-asks over 40 rounds, up to 9 in one round, about 17 s a round).
                still = next((row["action"] for row in page.get("available") or [] if _same_move(row["action"], wanted)), None)
                if open_attempts:
                    # What the person tried stays what they tried; the rules decide it at the new revision.
                    again = {**wanted, "base_revision": engine.world.revision}
                elif still is not None:
                    again = still
                elif policy == "scripted":
                    again, said_retry = _scripted_choice(page, last_done.get(actor))
                    if again is not None:
                        last_done.setdefault(actor, {})[again.get("kind", "")] = turn
                elif policy == "resident":
                    residents.observe(actor, f"Round {turn + turn_offset}: your choice was no longer allowed after "
                                      "earlier moves this round; choose again.")
                    attempt = residents.choose(actor, [r["action_id"] for r in page.get("available") or []],
                                               {**_view(engine, actor, page), "recent": _recent_for(engine, actor, seen),
                                                "world_summary": bundle["world"]["summary"],
                                                "brief": (briefs or {}).get(actor, "")})
                    if attempt.get("belief") is not None:
                        # Nothing left to choose keeps the belief behind the first choice (2026-10-17 live run
                        # bhE4uvdDzg78: 12 of 202 attempted moves lost it).
                        beliefs[actor] = attempt
                    choice = resolve_choice(page, attempt.get("action_id") or WAIT, attempt.get("reasoning") or "")
                    again = dict(choice.action) if choice.kind == "action" and choice.action is not None else None
                    said_retry = attempt.get("reasoning")
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
                        brief=(briefs or {}).get(actor, ""),
                    )
                    cost += call_cost
                if again is None:
                    did = None
                    outcome = {"status": "nothing_left", "event": {"checks": []}}
                else:
                    did = again
                    # A retry chooses from a fresh page, so its move was offered (2026-10-23 luna measurement R1.5:
                    # both fires were put out on retries, yet extinguish-fire was reported never possible).
                    offered_kinds.add(str(again.get("kind") or ""))
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
                    and not (did or {}).get("kind") == open_attempt.UNMATCHED_KIND
                ],
                "lost_what_it_wanted": bool(retried and not _same_move(did, wanted)),
                # Whether the accepted move actually changed the world.
                "changed": bool(outcome.get("status") == "accepted" and _state_changes(outcome.get("event") or {})),
                "blocked_by_rules": blocked_by_rules.get(actor, []),
                # The Engine event this move made and what it changed, so an analysis of the run (the "What
                # happened" readout) can cite the exact event behind each claim.
                "event_id": _run_event_id(turn + turn_offset, (outcome.get("event") or {}).get("event_id")),
                "changes": _state_changes(outcome.get("event") or {}) if outcome.get("status") == "accepted" else [],
            }
            if said_retry is not None:
                row["said_on_retry"] = said_retry
            if actor in readings:
                row["attempt"] = {"text": beliefs[actor].get("attempt"), "reading": readings[actor]}
                if (did or {}).get("kind") == open_attempt.UNMATCHED_KIND:
                    unmatched.append({"round": turn + turn_offset, "actor": actor, "attempt": did.get("attempt"),
                                      "nearest_kind": did.get("nearest_kind"), "why": did.get("why")})
            rows[actor] = row
        round_no = turn + turn_offset
        starting: dict[str, list[dict[str, Any]]] = {}
        for actor in actors:
            row = rows[actor]
            if row.get("status") == "accepted":
                expects = attempts.task_words(beliefs.get(actor) or {}) if residents is not None else None
                for task in attempts.started(watchers, actor, str((row.get("did") or {}).get("kind")),
                                             row.get("changes") or [], round_no, row.get("event_id")):
                    row["started_task"] = True
                    starting.setdefault(row["event_id"], []).append({**task, "expects": expects})
        if residents is not None:
            for actor in actors:
                row, attempt = rows[actor], beliefs.get(actor) or {}
                row["belief"], row["expects"] = attempt.get("belief"), attempt.get("expected_effect")
                did = (row.get("did") or {}).get("kind") or "waited"
                result = row["status"] + ("" if row.get("changed") or row["status"] != "accepted" else ", changed nothing")
                if row.get("refused_because"):
                    result += " (" + "; ".join(row["refused_because"])[:160] + ")"
                # The resident's own record of this move, kept in its Concordia memory for the next rounds.
                if row.get("started_task"):
                    # A started task says what was started, not whether it will work (#128): the ending reaches the
                    # person only through what they see in later rounds.
                    result = "you started it; it is now under way"
                if (row.get("did") or {}).get("kind") == open_attempt.UNMATCHED_KIND:
                    # Nothing in the world answers this kind of try yet (Q22 default: it changes nothing).
                    residents.observe(actor, f"Round {turn + turn_offset}: you believed: {row['belief']} You tried to "
                                      f"{row['did']['attempt']}; nothing came of it.")
                elif open_attempts and row["belief"] is not None:
                    tried = "waited" if row.get("did") is None else f"tried to {row['attempt']['text']}"
                    residents.observe(actor, f"Round {turn + turn_offset}: you believed: {row['belief']} You {tried}, "
                                      f"expecting: {row['expects']} Result: {result}.")
                elif row["belief"] is None:
                    residents.observe(actor, f"Round {turn + turn_offset}: nothing was open to you, so you waited.")
                else:
                    residents.observe(actor, f"Round {turn + turn_offset}: you believed: {row['belief']} You did {did}, "
                                      f"expecting: {row['expects']} Result: {result}.")
        advanced = engine.advance(1)
        # This round's events in order: each ends the open tasks whose field it moves on (a person's move or the
        # world's process), then opens the tasks it started. An earlier event cannot end a later start.
        this_round: list[dict[str, Any]] = []
        for event in engine.world.events[events_seen:]:
            run_id = _run_event_id(round_no, event.get("event_id"))
            changes = _state_changes(event)
            for task in list(open_tasks):
                done = attempts.ended(task, event, run_id, round_no, changes)
                if done is not None:
                    open_tasks.remove(task)
                    this_round.append(done)
            if run_id in starting:
                open_tasks.extend(starting.pop(run_id))
            elif run_id and world_watchers:
                open_tasks.extend(attempts.started(world_watchers, WORLD, str(event.get("rule_id")), changes,
                                                   round_no, run_id))
        underway_now = this_round + [{**t, "status": "underway"} for t in open_tasks]
        if residents is not None:
            # Each open or just-ended task, seen by the person who started it next round: their own expectation
            # beside the field as it is now. Nobody tells them it failed.
            entities = engine.world.material_dict()["entities"]
            for task in underway_now:
                if task["person"] == WORLD:  # everyone sees the world's own tasks in its state
                    continue
                component, name = task["field"].split(".")[1:]
                now = ((entities.get(task["entity"]) or {}).get("components") or {}).get(component, {}).get(name)
                residents.observe(task["person"], f"Round {round_no + 1}: " + attempts.memory_line(task, now))
            for actor, text in attempts.finished_notices(this_round, entities, actors, round_no):
                residents.observe(actor, text)
        transcript.append(
            {
                "turn": turn + turn_offset,
                # Changes the world made by itself this round (installed processes); knock-on effects are listed
                # apart, under "reactions", each with the event that set it off.
                "world_changes": [event["rule_id"] for event in advanced.get("events", [])
                                  if "reaction_wave" not in event],
                **_round_reactions(engine.world.events[events_seen:], turn + turn_offset),
                "world_events": [
                    {"event_id": _run_event_id(turn + turn_offset, event.get("event_id")), "rule_id": event["rule_id"],
                     "changes": _state_changes(event)}
                    for event in advanced.get("events", [])
                ],
                "revision_when_decided": revision,
                # Tasks started this round or earlier that were still open or ended this round (#128).
                "underway": [{k: t.get(k) for k in ("person", "action", "entity", "field", "started_round",
                                                    "started_event_id", "expects", "status", "ending_event_id",
                                                    "ended_by", "ended_with")} for t in underway_now],
                "committed_first": order[0],
                "actors": rows,
                "progress": {},
            }
        )
        for event in engine.world.events[events_seen:]:
            run_ids[event["event_id"]] = _run_event_id(turn + turn_offset, event["event_id"])
            kept = {**deepcopy(event), "event_id": run_ids[event["event_id"]]}
            if "causal_parent_event_ids" in kept:
                kept["causal_parent_event_ids"] = [run_ids.get(e, e) for e in kept["causal_parent_event_ids"]]
            engine_events.append(kept)

    terminal_reached = bool(
        causal_model.terminal is not None and causal_model.terminal.reached(engine.world)
    )
    if not transcript and start_snapshot is None:
        raise ValueError("run produced no actions; review actor selectors, checks, and parameter choices")
    trace = {
        "schema_version": "world-substrate-contested-run/v3",
        "world": bundle["world"]["id"],
        "actors": actors,
        "model": (f"{MOVER} {model_name}" if policy == "resident" else model_name if policy == "llm"
                  else "scripted-least-recent"),
        "cost_usd": round(cost + (residents.cost() if residents is not None else 0.0), 6),
        "mechanic_profile_id": profile_id,
        "engine_events": engine_events,
        "summary": {
            "turns": len(transcript),
            "terminal_reached": terminal_reached,
            "accepted_actions": sum(
                1
                for t in transcript
                for row in t["actors"].values()
                if row.get("status") == "accepted"
            ),
            "world_changes": sum(len(t["world_changes"]) for t in transcript),
            # Alive means people are still acting in the last third of the rounds.
            # Changes the world makes by itself do not count: a world where only
            # decay processes run (energy drains, stock runs out) and nobody can
            # act is dead, and was wrongly reported as alive (2026-10-06).
            # Moves that changed nothing do not count either.
            "active_at_end": any(
                any(row.get("changed") for row in t["actors"].values())
                for t in transcript[-max(1, len(transcript) // 3):]
            ),
            # Actors who never managed a single action: in a system world they
            # are dead weight (the pencil chain's delivery company, 2026-10-06).
            "idle_actors": sorted(
                actor for actor in actors
                if not any(
                    (t["actors"].get(actor) or {}).get("changed") for t in transcript
                )
            ),
            # Busy but stuck (2026-10-06 toy workshop: Mira held the glue pot with
            # no rule to put it down; the only move left was re-accepting the
            # same recurring order). Who made no real change in the last third,
            # and which moves were still happening there.
            "stalled_actors": sorted(
                actor for actor in actors
                if not any(
                    (t["actors"].get(actor) or {}).get("changed")
                    for t in transcript[-max(1, len(transcript) // 3):]
                )
            ),
            "moves_at_end": sorted({
                str((row.get("did") or {}).get("kind"))
                for t in transcript[-max(1, len(transcript) // 3):]
                for row in t["actors"].values() if row.get("changed")
            }),
            "never_offered": {
                kind: _never_why(kind, refused_why.get(kind) or [], causal_value)
                for kind in sorted({getattr(m, "action_kind", "") for m in causal_model.mechanics} - offered_kinds - {""})
            },
            # Open attempts that fit no installed rule: each changed nothing, and names the next rule a build could add.
            **({"unmatched_attempts": unmatched} if open_attempts else {}),
            "first_turn": turn_offset + 1,
            "last_turn": turn_offset + len(transcript),
        },
        "transcript": transcript,
        # Where a "keep going" continuation resumes.
        "final_snapshot": engine.world.snapshot(),
    }
    if residents is not None:
        # Each resident's Concordia memory after this request; live play sends it back with the next round.
        trace["resident_memory"] = residents.memory_state()
    # Open tasks, sent back with the next round so live play keeps following them.
    trace["underway"] = [{k: t[k] for k in sorted(attempts.TASK_KEYS)} for t in open_tasks]
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
    html = render_html(trace, profile, by_id, REPO)
    # Live play renders one round at a time, where "Turn 7 / 1" reads as broken;
    # label by round number instead. Saved evidence replays keep the old label.
    return html.replace(
        "'Turn '+f.turn+' / '+FRAMES.length",
        "'Round '+f.turn+(FRAMES.length>1?' ('+(idx+1)+' of '+FRAMES.length+')':'')",
    )


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
