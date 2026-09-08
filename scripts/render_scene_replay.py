#!/usr/bin/env python3
"""Render a contested-run trace through a declarative scene profile.

The trace owns what happened. The scene profile owns only presentation:
geometry, asset bindings, action-to-motion rules, state appearance, and
milestone labels. The renderer contains no world-specific entity or action ids.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

PROFILE_SCHEMA = "world-substrate-scene-profile/v0"
TRACE_SCHEMA = "world-substrate-contested-run/v3"


def _lookup(value: object, path: str) -> object:
    current = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _point(value: object, label: str) -> list[float]:
    if not isinstance(value, list) or len(value) != 2 or any(type(x) not in (int, float) for x in value):
        raise ValueError(f"{label} must be [x, y]")
    return [float(value[0]), float(value[1])]


def _rect(value: object, label: str) -> list[float]:
    if not isinstance(value, list) or len(value) != 4 or any(type(x) not in (int, float) for x in value):
        raise ValueError(f"{label} must be [x, y, width, height]")
    return [float(x) for x in value]


def load_trace(path: Path, *, expected_world: str | None = None) -> dict[str, Any]:
    trace = json.loads(path.read_text())
    if trace.get("schema_version") != TRACE_SCHEMA:
        raise ValueError(f"scene renderer requires {TRACE_SCHEMA}")
    if expected_world is not None and trace.get("world") != expected_world:
        raise ValueError(f"trace world {trace.get('world')!r} does not match scene profile {expected_world!r}")
    actors = trace.get("actors")
    transcript = trace.get("transcript")
    if not isinstance(actors, list) or not actors or any(not isinstance(a, str) or not a for a in actors):
        raise ValueError("trace must name one or more actors")
    if not isinstance(transcript, list) or not transcript:
        raise ValueError("trace must contain a transcript")
    return trace


def load_scene_profile(path: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    profile = json.loads(path.read_text())
    if profile.get("schema_version") != PROFILE_SCHEMA:
        raise ValueError(f"scene profile must use {PROFILE_SCHEMA}")
    if not isinstance(profile.get("world"), str) or not profile["world"]:
        raise ValueError("scene profile must name its trace world")
    for key in ("actors", "stations", "entities", "assets", "action_visuals"):
        if not isinstance(profile.get(key), dict):
            raise ValueError(f"scene profile {key!r} must be an object")

    stations = profile["stations"]
    for station_id, station in stations.items():
        if not isinstance(station, dict):
            raise ValueError(f"station {station_id!r} must be an object")
        station["rect"] = _rect(station.get("rect"), f"station {station_id}.rect")
        if "actor_anchor" in station:
            station["actor_anchor"] = _point(station["actor_anchor"], f"station {station_id}.actor_anchor")
        if "actor_anchors" in station:
            if not isinstance(station["actor_anchors"], dict):
                raise ValueError(f"station {station_id}.actor_anchors must be an object")
            station["actor_anchors"] = {
                actor: _point(point, f"station {station_id}.actor_anchors.{actor}")
                for actor, point in station["actor_anchors"].items()
            }
        if "item_anchor" in station:
            station["item_anchor"] = _point(station["item_anchor"], f"station {station_id}.item_anchor")
        layout = station.get("item_layout")
        if layout is not None:
            if not isinstance(layout, dict):
                raise ValueError(f"station {station_id}.item_layout must be an object")
            slots = layout.get("slots", [])
            if not isinstance(slots, list):
                raise ValueError(f"station {station_id}.item_layout.slots must be a list")
            checked_slots = []
            for index, slot in enumerate(slots):
                point = _point(slot, f"station {station_id}.item_layout.slots[{index}]")
                if any(value < 0 or value > 1 for value in point):
                    raise ValueError(f"station {station_id}.item_layout slots use relative 0..1 coordinates")
                checked_slots.append(point)
            layout["slots"] = checked_slots
            overflow = layout.get("overflow", "grid")
            if overflow not in {"grid", "anchor"}:
                raise ValueError(f"station {station_id}.item_layout.overflow must be grid or anchor")
            layout["overflow"] = overflow

    for action_kind, visual in profile["action_visuals"].items():
        if not isinstance(visual, dict):
            raise ValueError(f"action visual {action_kind!r} must be an object")
        state_effects = visual.get("state_effects")
        if state_effects is not None:
            if not isinstance(state_effects, list):
                raise ValueError(f"action visual {action_kind}.state_effects must be a list")
            for index, effect in enumerate(state_effects):
                if not isinstance(effect, dict):
                    raise ValueError(
                        f"action visual {action_kind}.state_effects[{index}] must be an object"
                    )
                entity_field = effect.get("entity_field")
                set_state = effect.get("set_state")
                if not isinstance(entity_field, str) or not entity_field:
                    raise ValueError(
                        f"action visual {action_kind}.state_effects[{index}].entity_field must be a nonempty string"
                    )
                if not isinstance(set_state, str) or not set_state:
                    raise ValueError(
                        f"action visual {action_kind}.state_effects[{index}].set_state must be a nonempty string"
                    )

    for actor_id, actor in profile["actors"].items():
        if not isinstance(actor, dict):
            raise ValueError(f"actor visual {actor_id!r} must be an object")
        actor["home"] = _point(actor.get("home"), f"actor {actor_id}.home")
        actor["carry_offset"] = _point(actor.get("carry_offset", [5, 3]), f"actor {actor_id}.carry_offset")
        actor["carry_spacing"] = _point(actor.get("carry_spacing", [0, 5]), f"actor {actor_id}.carry_spacing")

    for entity_id, entity in profile["entities"].items():
        if not isinstance(entity, dict):
            raise ValueError(f"entity visual {entity_id!r} must be an object")
        entity["home"] = _point(entity.get("home"), f"entity {entity_id}.home")

    world_entities: dict[str, dict[str, Any]] = {}
    world_model_ref = profile.get("world_model")
    if world_model_ref is not None:
        if not isinstance(world_model_ref, str) or not world_model_ref:
            raise ValueError("world_model must be a relative path")
        world_model_path = (path.parent / world_model_ref).resolve()
        world_model = json.loads(world_model_path.read_text())
        rows = world_model.get("entities")
        if not isinstance(rows, list):
            raise ValueError("world_model must contain entities")
        world_entities = {
            str(row["entity_id"]): row for row in rows if isinstance(row, dict) and isinstance(row.get("entity_id"), str)
        }
        for entity_id in profile["entities"]:
            if entity_id not in world_entities:
                raise ValueError(f"visual entity {entity_id!r} is absent from world_model")
        for station_id, station in profile["stations"].items():
            if not station.get("presentation_only") and station_id not in world_entities:
                raise ValueError(f"station {station_id!r} is absent from world_model")

    return profile, world_entities


def action_label(action: object, visual: dict[str, Any] | None = None) -> str:
    if not isinstance(action, dict):
        return "wait"
    template = visual.get("label_template") if isinstance(visual, dict) else None
    if isinstance(template, str):
        return re.sub(r"\{([A-Za-z][A-Za-z0-9_]*)\}", lambda m: str(action.get(m.group(1), "?")), template)
    kind = str(action.get("kind", "act")).replace("_", " ")
    ignore = {"kind", "actor", "base_revision", "controller"}
    referents = [str(v) for k, v in action.items() if k not in ignore and isinstance(v, (str, int, float))]
    if not referents:
        return kind
    return f"{kind} " + " / ".join(referents)


def _station_anchor(profile: dict[str, Any], station_id: str, actor: str | None, *, item: bool = False) -> list[float]:
    station = profile["stations"].get(station_id)
    if not isinstance(station, dict):
        raise ValueError(f"action references unknown scene station {station_id!r}")
    if item and "item_anchor" in station:
        return list(station["item_anchor"])
    if actor is not None:
        anchors = station.get("actor_anchors") or {}
        if actor in anchors:
            return list(anchors[actor])
    if "actor_anchor" in station:
        return list(station["actor_anchor"])
    x, y, w, h = station["rect"]
    return [x + w / 2, y + h / 2]


def _target_station(spec: object, action: dict[str, Any]) -> str | None:
    if not isinstance(spec, dict):
        return None
    station = spec.get("station")
    if isinstance(station, str):
        return station
    field = spec.get("action_field")
    if isinstance(field, str):
        value = action.get(field)
        return value if isinstance(value, str) else None
    return None



def _actor_target_point(
    profile: dict[str, Any],
    spec: object,
    action: dict[str, Any],
    actor: str,
    item_state: dict[str, dict[str, Any]],
) -> list[float] | None:
    station = _target_station(spec, action)
    if station:
        return _station_anchor(profile, station, actor)
    if not isinstance(spec, dict):
        return None
    entity_field = spec.get("entity_field")
    entity_id = action.get(entity_field) if isinstance(entity_field, str) else None
    if not isinstance(entity_id, str) or entity_id not in profile.get("entities", {}):
        return None
    state = item_state.get(entity_id) or {}
    placed_at = state.get("placed_at")
    if isinstance(placed_at, str) and placed_at in profile.get("stations", {}):
        return _station_anchor(profile, placed_at, actor)
    return list(profile["entities"][entity_id]["home"])

def _accepted_actions(raw: dict[str, Any], actors: list[str]) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    first = raw.get("committed_first")
    order = [first, *[a for a in actors if a != first]] if first in actors else actors
    result: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    rows = raw.get("actors") or {}
    for actor in order:
        record = rows.get(actor) or {}
        action = record.get("did")
        if record.get("status") == "accepted" and isinstance(action, dict):
            result.append((actor, record, action))
    return result


def _moment_ids(
    profile: dict[str, Any],
    raw: dict[str, Any],
    accepted: list[tuple[str, dict[str, Any], dict[str, Any]]],
    previous_release_by: dict[str, str],
) -> list[str]:
    progress = raw.get("progress") or {}
    records = raw.get("actors") or {}
    moments: list[str] = []
    for rule in profile.get("moment_rules") or []:
        if not isinstance(rule, dict) or not isinstance(rule.get("id"), str):
            continue
        when = rule.get("when")
        matched = False
        if when == "retry_unavailable":
            matched = any(
                isinstance(records.get(actor), dict)
                and records[actor].get("retried") is True
                and records[actor].get("plan_still_available") is False
                for actor in records
            )
        elif when == "filled_release":
            for actor, _, action in accepted:
                item_field = str(rule.get("item_field") or "item")
                if action.get("kind") == rule.get("action_kind") and action.get(item_field) == rule.get("item"):
                    matched = (progress.get(actor) or {}).get("filled") is True
                    if matched:
                        break
        elif when == "take_after_release":
            for actor, _, action in accepted:
                item = rule.get("item")
                item_field = str(rule.get("item_field") or "item")
                if action.get("kind") == rule.get("action_kind") and action.get(item_field) == item:
                    prior = previous_release_by.get(str(item))
                    matched = prior is not None and prior != actor
                    if matched:
                        break
        elif when == "all_progress_filled":
            matched = bool(progress) and all((progress.get(actor) or {}).get("filled") is True for actor in progress)
        if matched:
            moments.append(rule["id"])
    return moments



def _station_layout_positions(profile: dict[str, Any], item_state: dict[str, dict[str, Any]]) -> dict[str, list[float]]:
    """Resolve presentation-only multi-item station placement for one frame."""
    positions: dict[str, list[float]] = {}
    entity_order = list(profile["entities"])
    for station_id, station in profile["stations"].items():
        layout = station.get("item_layout")
        if not isinstance(layout, dict):
            continue
        placed = [
            entity_id for entity_id in entity_order
            if (item_state.get(entity_id) or {}).get("placed_at") == station_id
        ]
        if not placed:
            continue
        x, y, width, height = station["rect"]
        slots = layout.get("slots") or []
        overflow = layout.get("overflow", "grid")
        extra_count = max(0, len(placed) - len(slots))
        grid_columns = max(1, min(3, int(extra_count ** 0.5 + 0.999))) if extra_count else 1
        grid_rows = max(1, (extra_count + grid_columns - 1) // grid_columns)
        for index, entity_id in enumerate(placed):
            if index < len(slots):
                rel_x, rel_y = slots[index]
                positions[entity_id] = [x + width * rel_x, y + height * rel_y]
                continue
            if overflow == "anchor":
                positions[entity_id] = _station_anchor(profile, station_id, None, item=True)
                continue
            grid_index = index - len(slots)
            column = grid_index % grid_columns
            row = grid_index // grid_columns
            rel_x = (column + 1) / (grid_columns + 1)
            rel_y = (row + 1) / (grid_rows + 1)
            positions[entity_id] = [x + width * rel_x, y + height * rel_y]
    return positions

def build_frames(trace: dict[str, Any], profile: dict[str, Any], world_entities: dict[str, dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    if trace.get("world") != profile.get("world"):
        raise ValueError("trace and scene profile name different worlds")
    actors = list(trace["actors"])
    if any(actor not in profile["actors"] for actor in actors):
        raise ValueError("every trace actor needs a scene-profile actor visual")
    world_entities = world_entities or {}

    holders: dict[str, str] = {}
    item_state: dict[str, dict[str, Any]] = {}
    for entity_id, visual in profile["entities"].items():
        raw_entity = world_entities.get(entity_id) or {}
        state = _lookup(raw_entity, str(visual.get("state_path") or "")) if visual.get("state_path") else None
        item_state[entity_id] = {"state": state or visual.get("initial_state") or "default", "placed_at": None}
        owner_ref = _lookup(raw_entity, "ownership.owner_ref")
        if isinstance(owner_ref, str) and owner_ref.startswith("actor:"):
            owner = owner_ref.partition(":")[2]
            if owner in actors:
                holders[entity_id] = owner

    last_release_by: dict[str, str] = {}
    frames: list[dict[str, Any]] = []
    for raw in trace["transcript"]:
        accepted = _accepted_actions(raw, actors)
        previous_release_by = dict(last_release_by)
        active_stations: list[str] = []
        actor_positions = {actor: list(profile["actors"][actor]["home"]) for actor in actors}

        for actor, _, action in accepted:
            visual = profile["action_visuals"].get(action.get("kind"))
            if not isinstance(visual, dict):
                continue
            target_point = _actor_target_point(
                profile, visual.get("actor_target"), action, actor, item_state
            )
            if target_point:
                actor_positions[actor] = target_point
            item_field = visual.get("item_field", "item")
            item = action.get(item_field) if isinstance(item_field, str) else None
            if isinstance(item, str) and item in item_state:
                if visual.get("ownership") == "take":
                    holders[item] = actor
                    if visual.get("clear_item_station"):
                        item_state[item]["placed_at"] = None
                elif visual.get("ownership") == "release":
                    holders.pop(item, None)
                    last_release_by[item] = actor
                if isinstance(visual.get("set_state"), str):
                    item_state[item]["state"] = visual["set_state"]
                item_target = visual.get("item_target")
                station = _target_station(item_target, action)
                unless = item_target.get("unless_state") if isinstance(item_target, dict) else None
                blocked = isinstance(unless, list) and item_state[item].get("state") in unless
                if station and not blocked:
                    item_state[item]["placed_at"] = station
            for effect in visual.get("state_effects") or []:
                entity_id = action.get(effect["entity_field"])
                if not isinstance(entity_id, str) or entity_id not in item_state:
                    raise ValueError(
                        f"action {action.get('kind')!r} state effect references unknown visual entity via "
                        f"{effect['entity_field']!r}: {entity_id!r}"
                    )
                item_state[entity_id]["state"] = effect["set_state"]
            active_field = visual.get("activate_station_from")
            if isinstance(active_field, str) and isinstance(action.get(active_field), str):
                active_stations.append(action[active_field])

        records = raw.get("actors") or {}
        actor_rows = {}
        for actor in actors:
            record = records.get(actor) or {}
            action = record.get("did") or record.get("wanted")
            actor_rows[actor] = {
                "status": record.get("status"),
                "action": action_label(action, profile["action_visuals"].get(action.get("kind")) if isinstance(action, dict) else None),
                "reasoning": record.get("said_on_retry") or record.get("said") or "",
                "retried": bool(record.get("retried")),
                "did": record.get("did"),
            }
        frame = {
            "turn": raw.get("turn"),
            "actors": actor_rows,
            "actor_positions": actor_positions,
            "holdings": {actor: sorted(item for item, holder in holders.items() if holder == actor) for actor in actors},
            "holders": dict(holders),
            "progress": deepcopy(raw.get("progress") or {}),
            "items": deepcopy(item_state),
            "active_stations": sorted(set(active_stations)),
            "moments": _moment_ids(profile, raw, accepted, previous_release_by),
        }
        placed_positions = _station_layout_positions(profile, item_state)
        if placed_positions:
            frame["placed_positions"] = placed_positions
        frames.append(frame)
    return frames


def _asset_html(asset: dict[str, Any], profile_dir: Path) -> str:
    kind = asset.get("kind")
    if kind == "emoji" or kind == "text":
        return html.escape(str(asset.get("value") or ""))
    if kind == "image":
        path_value = asset.get("path")
        if not isinstance(path_value, str) or not path_value:
            raise ValueError("image asset requires path")
        path = (profile_dir / path_value).resolve()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"<img alt='' src='data:{mime};base64,{data}'>"
    raise ValueError(f"unsupported asset kind {kind!r}")


def _entity_label(entity_id: str, visual: dict[str, Any], world_entities: dict[str, dict[str, Any]]) -> str:
    if isinstance(visual.get("label"), str):
        return visual["label"]
    raw = world_entities.get(entity_id) or {}
    return str(raw.get("label") or entity_id)


def render_html(trace: dict[str, Any], profile: dict[str, Any], world_entities: dict[str, dict[str, Any]], profile_dir: Path) -> str:
    frames = build_frames(trace, profile, world_entities)
    scene = profile.get("scene") or {}
    assets = {key: _asset_html(value, profile_dir) for key, value in profile["assets"].items()}
    payload = json.dumps(frames, separators=(",", ":")).replace("</", "<\\/")
    profile_payload = deepcopy(profile)
    profile_payload["resolved_assets"] = assets
    profile_json = json.dumps(profile_payload, separators=(",", ":")).replace("</", "<\\/")

    decor_html = []
    for row in scene.get("decor") or []:
        if isinstance(row, dict) and row.get("kind") == "rect":
            style = (
                f"left:{float(row.get('x',0))}%;top:{float(row.get('y',0))}%;"
                f"width:{float(row.get('w',0))}%;height:{float(row.get('h',0))}%;"
                f"background:{html.escape(str(row.get('fill','#ddd')), quote=True)};"
            )
            if row.get("border_bottom"):
                style += f"border-bottom:5px solid {html.escape(str(row['border_bottom']), quote=True)};"
            decor_html.append(f"<div class='decor' style='{style}'></div>")

    stations_html = []
    for station_id, station in profile["stations"].items():
        x, y, w, h = station["rect"]
        style = f"left:{x}%;top:{y}%;width:{w}%;height:{h}%;background:{html.escape(str(station.get('fill','#aaa')), quote=True)}"
        active_asset = assets.get(station.get("active_asset"), "") if station.get("active_asset") else ""
        progress_actor = station.get("progress_actor")
        progress = ""
        if isinstance(progress_actor, str):
            progress = f"<div class='goal-progress' data-progress-actor='{html.escape(progress_actor, quote=True)}'><div class='progress-items'></div><div class='progress-needs'></div></div>"
        stations_html.append(
            f"<div class='station role-{html.escape(str(station.get('role','surface')), quote=True)}' data-station='{html.escape(station_id, quote=True)}' style='{style}'>"
            f"<div class='station-label'>{html.escape(str(station.get('label') or station_id))}</div>"
            f"<div class='active-asset'>{active_asset}</div>{progress}</div>"
        )

    actors_html = []
    for actor_id, actor in profile["actors"].items():
        asset = assets[actor["asset"]]
        accent = html.escape(str(actor.get("accent") or "#777"), quote=True)
        label = html.escape(str((world_entities.get(actor_id) or {}).get("label") or actor_id))
        actors_html.append(
            f"<div class='actor' data-actor='{html.escape(actor_id, quote=True)}'><div class='avatar' style='--accent:{accent}'>{asset}</div><div class='name'>{label}</div></div>"
            f"<div class='thought' data-thought='{html.escape(actor_id, quote=True)}'></div>"
        )

    entities_html = []
    for entity_id, entity in profile["entities"].items():
        asset = assets[entity["asset"]]
        label = html.escape(_entity_label(entity_id, entity, world_entities))
        entities_html.append(
            f"<div class='entity' data-entity='{html.escape(entity_id, quote=True)}'>{asset}<small>{label}</small></div>"
        )

    title = html.escape(str(profile.get("title") or profile.get("scene_id") or "Scene replay"))
    subtitle = html.escape(str(profile.get("subtitle") or ""))
    note = html.escape(str(profile.get("note") or ""))
    model = html.escape(str(trace.get("model") or "unknown"))
    cost = float(trace.get("cost_usd") or 0)
    aspect = html.escape(str(scene.get("aspect_ratio") or "16 / 9"), quote=True)
    background = html.escape(str(scene.get("background") or "#ddd"), quote=True)
    shell_background = html.escape(str(scene.get("shell_background") or "#171b1d"), quote=True)
    grid_color = html.escape(str(scene.get("grid_color") or "#0000"), quote=True)
    grid_size = int(scene.get("grid_size_px") or 64)
    autoplay_ms = max(250, int(float(profile.get("autoplay_seconds") or 2.0) * 1000))
    has_item_layout = any(isinstance(station.get("item_layout"), dict) for station in profile["stations"].values())
    if has_item_layout:
        position_js = (
            "function stationPoint(id,entityId,f){if(entityId&&f?.placed_positions?.[entityId])return f.placed_positions[entityId];const s=PROFILE.stations[id];if(!s)return null;if(s.item_anchor)return s.item_anchor;const r=s.rect;return[r[0]+r[2]/2,r[1]+r[3]/2]}\n"
            "function itemPos(id,f){const state=f.items[id]||{},preferStation=(PROFILE.station_precedence_states||[]).includes(state.state);if(preferStation&&state.placed_at){const p=stationPoint(state.placed_at,id,f);if(p)return p}for(const a of Object.keys(PROFILE.actors)){const held=f.holdings[a]||[];const n=held.indexOf(id);if(n>=0){const base=f.actor_positions[a],av=PROFILE.actors[a],j=held.indexOf(id);return[base[0]+av.carry_offset[0]+av.carry_spacing[0]*j,base[1]+av.carry_offset[1]+av.carry_spacing[1]*j]}}if(state.placed_at){const p=stationPoint(state.placed_at,id,f);if(p)return p}return PROFILE.entities[id].home}\n"
        )
    else:
        position_js = (
            "function stationPoint(id){const s=PROFILE.stations[id];if(!s)return null;if(s.item_anchor)return s.item_anchor;const r=s.rect;return[r[0]+r[2]/2,r[1]+r[3]/2]}\n"
            "function itemPos(id,f){const state=f.items[id]||{},preferStation=(PROFILE.station_precedence_states||[]).includes(state.state);if(preferStation&&state.placed_at){const p=stationPoint(state.placed_at);if(p)return p}for(const a of Object.keys(PROFILE.actors)){const held=f.holdings[a]||[];const n=held.indexOf(id);if(n>=0){const base=f.actor_positions[a],av=PROFILE.actors[a],j=held.indexOf(id);return[base[0]+av.carry_offset[0]+av.carry_spacing[0]*j,base[1]+av.carry_offset[1]+av.carry_spacing[1]*j]}}if(state.placed_at){const p=stationPoint(state.placed_at);if(p)return p}return PROFILE.entities[id].home}\n"
        )

    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title><style>
:root{{--scene-bg:{background};--shell-bg:{shell_background};--grid:{grid_color}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--shell-bg);font:15px/1.35 system-ui,-apple-system,sans-serif;color:#182126;overflow-x:hidden}}
.shell{{max-width:1240px;margin:auto;padding:18px}}.top{{color:white;display:flex;justify-content:space-between;align-items:end;gap:18px;margin-bottom:12px}}h1{{font-size:clamp(24px,3vw,42px);margin:0;letter-spacing:-.03em}}.sub{{color:#b8c1c5;max-width:700px;margin:4px 0 0}}.badge{{font-size:12px;color:#dbe2e5}}
.stage{{position:relative;aspect-ratio:{aspect};border:4px solid #090b0c;border-radius:18px;overflow:hidden;background:var(--scene-bg);box-shadow:0 20px 60px #0008}}.stage::before{{content:'';position:absolute;inset:0;background:linear-gradient(90deg,#0000 49%,var(--grid) 50%,#0000 51%),linear-gradient(#0000 49%,var(--grid) 50%,#0000 51%);background-size:{grid_size}px {grid_size}px}}.decor{{position:absolute}}
.station{{position:absolute;border:4px solid #47382c;border-radius:10px;box-shadow:inset 0 0 0 5px #ffffff18,0 5px 0 #0003;text-align:center;overflow:hidden}}.station-label{{font-size:11px;text-transform:uppercase;letter-spacing:.08em;font-weight:800;padding:5px;color:#221c17}}.role-workstation{{border-color:#282c2e}}.active-asset{{font-size:30px;display:none}}.station.active .active-asset{{display:block}}
.role-goal{{border-color:#79634c}}.goal-progress{{font-size:12px;padding:4px}}.progress-items{{font-size:26px;min-height:34px}}.progress-needs{{color:#665d54;font-size:11px}}
.actor{{position:absolute;width:92px;height:110px;transition:left .65s ease,top .65s ease;z-index:8;text-align:center}}.avatar{{width:62px;height:62px;margin:auto;border-radius:50%;border:4px solid #24292c;outline:6px solid var(--accent);background:white;display:flex;align-items:center;justify-content:center;font-size:34px;box-shadow:0 5px 0 #0003}}.avatar img,.entity img,.active-asset img{{max-width:100%;max-height:100%;object-fit:contain}}.name{{background:#16191be8;color:white;border-radius:9px;margin:6px auto 0;padding:3px 8px;width:max-content;font-weight:800}}
.thought{{position:absolute;z-index:12;width:min(310px,34vw);background:#fffffff2;border:3px solid #30383c;border-radius:14px;padding:9px 11px;box-shadow:0 8px 22px #0004;font-size:13px}}.thought strong{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#657078;margin-bottom:3px}}
.entity{{position:absolute;z-index:7;font-size:34px;transition:left .6s ease,top .6s ease,transform .3s ease,filter .3s ease;filter:drop-shadow(0 4px 2px #0004)}}.entity small{{position:absolute;left:50%;top:34px;transform:translateX(-50%);background:#fffddd;border:1px solid #695a44;border-radius:6px;padding:1px 4px;font-size:9px;white-space:nowrap}}.entity img{{width:40px;height:40px}}
.hud{{position:absolute;left:50%;top:18%;transform:translateX(-50%);z-index:20;background:#15191de8;color:white;border-radius:12px;padding:7px 12px;text-align:center;min-width:190px}}.turn{{font-size:22px;font-weight:900}}.moment{{display:inline-block;margin:4px 3px 0;background:#f0b448;color:#251b0b;border-radius:999px;padding:2px 8px;font-size:10px;font-weight:900;text-transform:uppercase}}.moment.terminal{{background:#5da46d;color:white}}
.action{{position:absolute;left:50%;bottom:2%;transform:translateX(-50%);z-index:20;background:#111d;color:white;border-radius:999px;padding:8px 15px;font-size:12px;white-space:nowrap;max-width:90%;overflow:hidden;text-overflow:ellipsis}}.controls{{display:flex;gap:10px;align-items:center;margin-top:12px;color:white}}button{{background:#f1eadc;border:0;border-radius:10px;padding:9px 13px;font-weight:800;cursor:pointer}}.bar{{height:8px;background:#ffffff24;border-radius:99px;flex:1;overflow:hidden}}.bar>i{{display:block;height:100%;background:#f0b448;width:0;transition:width .25s}}.note{{color:#aeb8bd;font-size:12px;margin-top:8px}}@media(max-width:800px){{.thought{{font-size:11px;width:38vw}}.actor{{transform:scale(.82);transform-origin:center}}.entity{{font-size:28px}}}}
</style></head><body><div class='shell'><div class='top'><div><h1>{title}</h1><p class='sub'>{subtitle}</p></div><div class='badge'>{model} · ${cost:.5f}</div></div>
<div class='stage'>{''.join(decor_html)}{''.join(stations_html)}{''.join(actors_html)}<div class='hud'><div class='turn' id='turn'></div><div id='moments'></div></div><div class='action' id='action'></div>{''.join(entities_html)}</div>
<div class='controls'><button id='restart'>↺ Replay</button><button id='prev'>←</button><button id='toggle'>Pause</button><button id='next'>→</button><div class='bar'><i id='progressbar'></i></div></div><div class='note'>{note}</div></div>
<script>const FRAMES={payload};const PROFILE={profile_json};const ASSETS=PROFILE.resolved_assets;let idx=0,timer=null,playing=true;
function setXY(el,p){{el.style.left=p[0]+'%';el.style.top=p[1]+'%'}}
{position_js}function styleEntity(el,state){{const s=PROFILE.state_styles?.[state]||{{}};el.style.transform='scale('+(s.scale??1)+') rotate('+(s.rotate_deg??0)+'deg)';el.style.filter='drop-shadow(0 4px 2px #0004) brightness('+(s.brightness??1)+') saturate('+(s.saturation??1)+')'}}
function progressIcon(kind){{const key=PROFILE.progress_assets?.[kind];return key?ASSETS[key]:(kind||'')}}
function render(i){{idx=Math.max(0,Math.min(FRAMES.length-1,i));const f=FRAMES[idx];document.getElementById('turn').textContent='Turn '+f.turn+' / '+FRAMES.length;document.getElementById('progressbar').style.width=((idx+1)/FRAMES.length*100)+'%';
 for(const a of Object.keys(PROFILE.actors)){{const el=document.querySelector('[data-actor="'+a+'"]');setXY(el,f.actor_positions[a]);const th=document.querySelector('[data-thought="'+a+'"]');const rec=f.actors[a]||{{}};th.innerHTML='<strong>'+a+' · '+(rec.action||'wait')+'</strong>'+(rec.reasoning||'');const n=Object.keys(PROFILE.actors).indexOf(a);th.style.left=(n%2===0?'2%':'72%');th.style.top=(18+Math.floor(n/2)*18)+'%'}}
 for(const id of Object.keys(PROFILE.entities)){{const el=document.querySelector('[data-entity="'+id+'"]');setXY(el,itemPos(id,f));styleEntity(el,(f.items[id]||{{}}).state)}}
 document.querySelectorAll('[data-station]').forEach(el=>el.classList.toggle('active',f.active_stations.includes(el.dataset.station)));
 document.querySelectorAll('[data-progress-actor]').forEach(el=>{{const a=el.dataset.progressActor,p=f.progress[a]||{{}};el.querySelector('.progress-items').innerHTML=(p.plated||[]).map(progressIcon).join('');el.querySelector('.progress-needs').textContent=p.filled?'✓ complete':'still needs: '+((p.still_wants||[]).join(', ')||'nothing')}});
 const labels=Object.fromEntries((PROFILE.moment_rules||[]).map(r=>[r.id,r.label||r.id]));const terminalIds=new Set((PROFILE.moment_rules||[]).filter(r=>r.terminal).map(r=>r.id));document.getElementById('moments').innerHTML=f.moments.map(m=>'<span class="moment '+(terminalIds.has(m)?'terminal':'')+'">'+(labels[m]||m)+'</span>').join('');document.getElementById('action').textContent=Object.keys(PROFILE.actors).map(a=>a+': '+(f.actors[a]?.action||'wait')).join(' · ')}}
function schedule(){{clearInterval(timer);if(playing)timer=setInterval(()=>{{if(idx>=FRAMES.length-1){{playing=false;document.getElementById('toggle').textContent='Play';clearInterval(timer)}}else render(idx+1)}},{autoplay_ms})}}
document.getElementById('toggle').onclick=()=>{{playing=!playing;document.getElementById('toggle').textContent=playing?'Pause':'Play';schedule()}};document.getElementById('prev').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx-1)}};document.getElementById('next').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx+1)}};document.getElementById('restart').onclick=()=>{{playing=true;document.getElementById('toggle').textContent='Pause';render(0);schedule()}};const q=new URLSearchParams(location.search);const start=Math.max(0,Math.min(FRAMES.length-1,(parseInt(q.get('turn')||'1',10)||1)-1));render(start);if(start>0){{playing=false;document.getElementById('toggle').textContent='Play'}}schedule();
</script></body></html>"""


def render_file(trace_path: Path, profile_path: Path, output_path: Path) -> None:
    profile, world_entities = load_scene_profile(profile_path)
    trace = load_trace(trace_path, expected_world=profile["world"])
    output_path.write_text(render_html(trace, profile, world_entities, profile_path.parent))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render_file(args.input, args.profile, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
