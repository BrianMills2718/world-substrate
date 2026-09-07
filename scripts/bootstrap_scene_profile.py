#!/usr/bin/env python3
"""Bootstrap a reviewable scene profile from world facts, a trace and an asset catalog.

The bootstrapper deliberately stops where presentation becomes a choice. It can
infer entity identity, actors, initial ownership, asset bindings, portable
objects, canonical station candidates and some action-field structure. It does
not invent coordinates or claim ambiguous action motion as world truth.
"""
from __future__ import annotations

import argparse
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

PROFILE_SCHEMA = "world-substrate-scene-profile/v0"
CATALOG_SCHEMA = "world-substrate-scene-asset-catalog/v0"
TRACE_SCHEMA = "world-substrate-contested-run/v3"


def _lookup(value: object, path: str) -> object:
    current = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _merge(out[key], value)
        else:
            out[key] = deepcopy(value)
    return out


def _load_json(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _entity_binding(entity: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    entity_id = str(entity.get("entity_id") or "")
    direct = catalog.get("entity_bindings", {}).get(entity_id)
    if isinstance(direct, dict):
        result = deepcopy(direct)
    else:
        result = {}
    for rule in catalog.get("component_value_bindings") or []:
        if not isinstance(rule, dict) or not isinstance(rule.get("path"), str):
            continue
        current = _lookup(entity, rule["path"])
        match = (rule.get("values") or {}).get(str(current))
        if isinstance(match, dict):
            result = _merge(result, match)
            if isinstance(rule.get("state_path"), str):
                result.setdefault("state_path", rule["state_path"])
    return result


def _station_binding(entity: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any] | None:
    bindings = catalog.get("category_station_bindings") or {}
    for category in entity.get("category_ids") or []:
        row = bindings.get(category)
        if isinstance(row, dict):
            return deepcopy(row)
    return None


def _action_signatures(trace: dict[str, Any]) -> dict[str, dict[str, set[str]]]:
    world_values: dict[str, dict[str, set[str]]] = {}
    for turn in trace.get("transcript") or []:
        for record in (turn.get("actors") or {}).values():
            action = record.get("did") if isinstance(record, dict) else None
            if not isinstance(action, dict) or not isinstance(action.get("kind"), str):
                continue
            kind = action["kind"]
            fields = world_values.setdefault(kind, {})
            for key, value in action.items():
                if key in {"kind", "actor", "base_revision", "controller"}:
                    continue
                if isinstance(value, (str, int, float)):
                    fields.setdefault(key, set()).add(str(value))
    return world_values


def _default_label_template(kind: str, item_field: str | None, station_field: str | None) -> str:
    words = kind.replace("_", " ")
    if item_field and station_field and item_field != station_field:
        return f"{words} {{{item_field}}} at {{{station_field}}}"
    if item_field:
        return f"{words} {{{item_field}}}"
    if station_field:
        return f"{words} at {{{station_field}}}"
    return words


def _initial_owner(entity: dict[str, Any]) -> str | None:
    owner_ref = _lookup(entity, "ownership.owner_ref")
    if isinstance(owner_ref, str) and owner_ref.startswith("actor:"):
        return owner_ref.partition(":")[2]
    return None


def bootstrap_profile(
    world_model: dict[str, Any],
    trace: dict[str, Any],
    catalog: dict[str, Any],
    *,
    world_model_ref: str,
    review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if trace.get("schema_version") != TRACE_SCHEMA:
        raise ValueError(f"trace must use {TRACE_SCHEMA}")
    if catalog.get("schema_version") != CATALOG_SCHEMA:
        raise ValueError(f"asset catalog must use {CATALOG_SCHEMA}")
    world = trace.get("world")
    actors = trace.get("actors")
    entities = world_model.get("entities")
    if not isinstance(world, str) or not world:
        raise ValueError("trace must name its world")
    if not isinstance(actors, list) or not actors or any(not isinstance(a, str) for a in actors):
        raise ValueError("trace must name actors")
    if not isinstance(entities, list):
        raise ValueError("world model must contain entities")
    by_id = {e["entity_id"]: e for e in entities if isinstance(e, dict) and isinstance(e.get("entity_id"), str)}
    missing = [a for a in actors if a not in by_id]
    if missing:
        raise ValueError(f"trace actors absent from world model: {missing}")

    world_asset_keys = (catalog.get("world_assets") or {}).get(world)
    if not isinstance(world_asset_keys, list):
        raise ValueError(f"asset catalog has no world_assets entry for {world!r}")
    assets = catalog.get("assets") or {}
    selected_assets = {}
    for key in world_asset_keys:
        if key not in assets:
            raise ValueError(f"world asset {key!r} is absent from catalog")
        selected_assets[key] = deepcopy(assets[key])

    actor_visuals: dict[str, Any] = {}
    inferred_owners: dict[str, str] = {}
    for actor in actors:
        binding = _entity_binding(by_id[actor], catalog)
        asset = binding.get("asset")
        if not isinstance(asset, str):
            raise ValueError(f"no asset binding for actor {actor!r}")
        actor_visuals[actor] = {"asset": asset}

    station_visuals: dict[str, Any] = {}
    station_ids: set[str] = set()
    for entity_id, entity in by_id.items():
        binding = _station_binding(entity, catalog)
        if binding is None:
            continue
        station_ids.add(entity_id)
        station_visuals[entity_id] = {"label": entity.get("label") or entity_id, **binding}

    signatures = _action_signatures(trace)
    referenced_ids: set[str] = set()
    field_values: dict[str, set[str]] = {}
    for fields in signatures.values():
        for field, values in fields.items():
            field_values.setdefault(field, set()).update(values)
            referenced_ids.update(v for v in values if v in by_id)

    entity_visuals: dict[str, Any] = {}
    progress_assets: dict[str, str] = {}
    for entity_id, entity in by_id.items():
        if entity_id in actors or entity_id in station_ids:
            continue
        binding = _entity_binding(entity, catalog)
        asset = binding.get("asset")
        is_referenced = entity_id in referenced_ids
        owner = _initial_owner(entity)
        portable = _lookup(entity, "portable.portable") is True or binding.get("portable") is True
        if not isinstance(asset, str) or not (is_referenced or owner or portable):
            continue
        row: dict[str, Any] = {"asset": asset, "label": entity.get("label") or entity_id}
        if portable:
            row["portable"] = True
        if isinstance(binding.get("state_path"), str):
            row["state_path"] = binding["state_path"]
        if isinstance(binding.get("initial_state"), str):
            row["initial_state"] = binding["initial_state"]
        entity_visuals[entity_id] = row
        if owner in actors:
            inferred_owners[entity_id] = owner
        progress_key = binding.get("progress_key")
        if isinstance(progress_key, str):
            progress_assets[progress_key] = asset

    # Actor -> goal links are canonical in the kitchen model and safe to infer.
    for actor in actors:
        order_id = _lookup(by_id[actor], "components.cook.order_id")
        if isinstance(order_id, str) and order_id in station_visuals:
            station_visuals[order_id]["progress_actor"] = actor

    action_visuals: dict[str, Any] = {}
    inferred_action_fields: dict[str, Any] = {}
    for kind, fields in signatures.items():
        entity_fields = [
            field for field, values in fields.items()
            if values and all(value in entity_visuals for value in values)
        ]
        station_fields = [
            field for field, values in fields.items()
            if values and all(value in station_visuals for value in values)
        ]
        item_field = entity_fields[0] if len(entity_fields) == 1 else None
        station_field = station_fields[0] if len(station_fields) == 1 else None
        row: dict[str, Any] = {}
        if item_field:
            row["item_field"] = item_field
        if station_field:
            row["actor_target"] = {"action_field": station_field}
        row["label_template"] = _default_label_template(kind, item_field, station_field)
        action_visuals[kind] = row
        inferred_action_fields[kind] = {"item_field": item_field, "station_field": station_field}

    base: dict[str, Any] = {
        "schema_version": PROFILE_SCHEMA,
        "world": world,
        "world_model": world_model_ref,
        "assets": selected_assets,
        "actors": actor_visuals,
        "stations": station_visuals,
        "entities": entity_visuals,
        "action_visuals": action_visuals,
        "progress_assets": progress_assets,
    }
    catalog_styles = (catalog.get("world_state_styles") or {}).get(world)
    if isinstance(catalog_styles, dict):
        base["state_styles"] = deepcopy(catalog_styles)

    review = deepcopy(review or {})
    reviewed_actions = review.pop("reviewed_actions", [])
    if not isinstance(reviewed_actions, list):
        raise ValueError("reviewed_actions must be a list")
    profile = _merge(base, review)

    todos: list[dict[str, str]] = []
    for actor in actors:
        if not isinstance(profile.get("actors", {}).get(actor, {}).get("home"), list):
            todos.append({"kind": "geometry", "target": f"actors.{actor}.home", "reason": "actor screen position is illustrative"})
    for station_id in profile.get("stations", {}):
        if not isinstance(profile["stations"][station_id].get("rect"), list):
            todos.append({"kind": "geometry", "target": f"stations.{station_id}.rect", "reason": "station rectangle is illustrative"})
    for entity_id in profile.get("entities", {}):
        if not isinstance(profile["entities"][entity_id].get("home"), list):
            todos.append({"kind": "geometry", "target": f"entities.{entity_id}.home", "reason": "entity home position is illustrative"})
    for kind in signatures:
        if kind not in reviewed_actions:
            todos.append({"kind": "action_projection", "target": f"action_visuals.{kind}", "reason": "motion/state projection needs review"})

    profile["bootstrap"] = {
        "schema_version": "world-substrate-scene-profile-bootstrap/v0",
        "inferred_initial_owners": inferred_owners,
        "inferred_action_fields": inferred_action_fields,
        "reviewed_actions": sorted(set(str(x) for x in reviewed_actions)),
        "todos": todos,
    }
    return profile


def is_complete(profile: dict[str, Any]) -> bool:
    bootstrap = profile.get("bootstrap") or {}
    return not bool(bootstrap.get("todos"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("world_model", type=Path)
    parser.add_argument("trace", type=Path)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--review", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    world_model = _load_json(args.world_model, "world model")
    trace = _load_json(args.trace, "trace")
    catalog = _load_json(args.catalog, "asset catalog")
    review = _load_json(args.review, "review overlay") if args.review else None
    args.output.parent.mkdir(parents=True, exist_ok=True)
    world_model_ref = os.path.relpath(args.world_model.resolve(), args.output.parent.resolve())
    profile = bootstrap_profile(world_model, trace, catalog, world_model_ref=world_model_ref, review=review)
    args.output.write_text(json.dumps(profile, indent=2) + "\n")
    if args.require_complete and not is_complete(profile):
        todos = profile["bootstrap"]["todos"]
        print(f"profile is incomplete: {len(todos)} review TODOs", file=__import__('sys').stderr)
        return 2
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
