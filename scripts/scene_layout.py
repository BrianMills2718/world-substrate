#!/usr/bin/env python3
"""A world's `layout` declaration: which prepared map slot each place sits in, and which places each door joins.

Implements: scene-viewer/world-layout-declaration
The rules never see a coordinate. A bundle may declare `layout` = {"version": 1, "map": <prepared map id>,
"rooms": {place id: slot}, "doors": {door id: {"between": [place, place], "halves": [entity ids]}},
"people": {actor id: {"start": place, "sprite": optional name}}}. Prepared maps (names only, no art) are in
`viewer/maps/maps.json`: each lists slots (map room names), which slots connect, and a pool of sprite names.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MAPS_PATH = Path(__file__).resolve().parents[1] / "viewer" / "maps" / "maps.json"


class LayoutError(ValueError):
    pass


def prepared_maps() -> dict[str, dict[str, Any]]:
    return json.loads(MAPS_PATH.read_text())


def _need(cond: bool, message: str) -> None:
    if not cond:
        raise LayoutError(message)


def validate_layout(bundle: dict[str, Any]) -> None:
    """Reject a layout that cannot be drawn: unknown map or slot, two places in one slot, a door joining unconnected slots."""
    if "layout" not in bundle:
        return
    layout = bundle["layout"]
    _need(isinstance(layout, dict) and set(layout) == {"version", "map", "rooms", "doors", "people"}, "layout must have exactly version, map, rooms, doors, people")
    _need(layout["version"] == 1 and type(layout["version"]) is int, "unsupported layout version")
    maps = prepared_maps()
    _need(layout["map"] in maps, f"layout.map {layout['map']!r} is not a prepared map ({sorted(maps)})")
    prepared = maps[layout["map"]]
    declaration = bundle.get("actor_information") or {}
    public = {row["id"] for row in declaration.get("public_entities", [])}
    actors = set(declaration.get("actors", {}))
    _need(isinstance(layout["rooms"], dict) and layout["rooms"], "layout.rooms must name at least one place")
    for place, slot in layout["rooms"].items():
        _need(place in public, f"layout room {place!r} is not a declared public entity")
        _need(slot in prepared["slots"], f"layout room {place!r} uses slot {slot!r}; map {layout['map']} has {sorted(prepared['slots'])}")
    _need(len(set(layout["rooms"].values())) == len(layout["rooms"]), "two places share one map slot")
    joined = {frozenset(pair) for pair in prepared["connections"]}
    _need(isinstance(layout["doors"], dict), "layout.doors must be an object")
    for door, row in layout["doors"].items():
        _need(isinstance(row, dict) and set(row) == {"between", "halves"}, f"layout door {door!r} needs between and halves")
        a, b = row["between"]
        _need(a in layout["rooms"] and b in layout["rooms"] and a != b, f"layout door {door!r} joins places that are not laid out")
        _need(frozenset((layout["rooms"][a], layout["rooms"][b])) in joined,
              f"layout door {door!r} joins {a} and {b}, whose slots {layout['rooms'][a]} and {layout['rooms'][b]} are not connected on map {layout['map']}")
        _need(row["halves"] and all(h in public for h in row["halves"]), f"layout door {door!r} halves must be declared public entities")
    _need(isinstance(layout["people"], dict) and layout["people"], "layout.people must name at least one actor")
    _need(len(layout["people"]) <= len(prepared["sprites"]), "more people than the map has sprites")
    for person, row in layout["people"].items():
        _need(person in actors, f"layout person {person!r} is not a declared actor")
        _need(isinstance(row, dict) and set(row) <= {"start", "sprite"} and "start" in row, f"layout person {person!r} needs start (and optional sprite)")
        _need(row["start"] in layout["rooms"], f"layout person {person!r} starts in a place that is not laid out")
        _need(row.get("sprite", prepared["sprites"][0]) in prepared["sprites"], f"layout person {person!r} sprite is not in the map's pool")
    # Every laid-out door must be walkable in the story: all laid-out places reachable from each other through declared doors.
    reach, todo = set(), [next(iter(layout["rooms"]))]
    while todo:
        cur = todo.pop()
        if cur in reach:
            continue
        reach.add(cur)
        todo += [x for d in layout["doors"].values() for x in d["between"] if cur in d["between"] and x != cur]
    _need(reach == set(layout["rooms"]), "some laid-out places are not joined to the rest by any door")


def resolve(bundle: dict[str, Any]) -> dict[str, Any]:
    """What the exporter needs: rooms -> '<sector>|<arena>', people -> display name, start rooms, labels, doors, sprites."""
    validate_layout(bundle)
    layout = bundle["layout"]
    prepared = prepared_maps()[layout["map"]]
    people = set(layout["people"])
    # Names of people stay as written; places and doors read mid-sentence ("walking to the corridor"), so drop the capital and any "(...)".
    labels = {row["id"]: row["label"] if row["id"] in people else row["label"].split(" (")[0][:1].lower() + row["label"].split(" (")[0][1:]
              for row in bundle["actor_information"]["public_entities"]}
    sprites = {}
    for index, (person, row) in enumerate(layout["people"].items()):
        sprites[labels[person]] = row.get("sprite") or prepared["sprites"][index]
    return {"rooms": {p: prepared["slots"][s] for p, s in layout["rooms"].items()},
            "people": {p: labels[p] for p in layout["people"]},
            "start_rooms": {p: row["start"] for p, row in layout["people"].items()},
            "labels": labels, "doors": layout["doors"], "sprites": sprites, "map": layout["map"], "title": bundle["world"]["label"], "tiles": prepared["tiles"], "prepared": prepared}
