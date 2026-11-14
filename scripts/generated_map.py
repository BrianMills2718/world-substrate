#!/usr/bin/env python3
"""A room map made from code, so it carries no one's art or map data: walls, floors and door gaps on a grid of Kenney Tiny Dungeon tiles (CC0).

Implements: scene-viewer/public-generated-map
Shape: one hub room across the middle; slots a and b open off its top wall, c and d off its bottom wall (only the slots a prepared map names are drawn).
Returns the same maze dict the exporter reads from Smallville's matrix (`collision`, `arena`, `sector`, `names`, `sectors`) plus the tile grid the viewer draws.
"""
from __future__ import annotations

from typing import Any

BLOCKED = "32125"  # the collision value the exporter treats as a wall (Smallville's own)
WALL, OUTSIDE = 40, 0  # tile numbers in the packed 12-column Tiny Dungeon sheet
FLOOR = {"hub": 53, "a": 30, "b": 30, "c": 30, "d": 30}
BOOKCASE, TABLE, CHEST, ANVIL, STOOL = 63, 72, 89, 74, 73  # furniture tiles, drawn over the floor and blocking it
BOX_W, SPOKE_H, HUB_H = 9, 7, 8
GAPS = {"a": (3, 4), "b": (11, 12), "c": (3, 4), "d": (11, 12)}


def build(map_id: str, slots: list[str]) -> dict[str, Any]:
    if "hub" not in slots or set(slots) - set(FLOOR):
        raise ValueError(f"generated map slots must be hub plus any of a, b, c, d; got {sorted(slots)}")
    top, bottom = [s for s in ("a", "b") if s in slots], [s for s in ("c", "d") if s in slots]
    hub_y = SPOKE_H - 1 if top else 0
    height = hub_y + HUB_H + (SPOKE_H - 1 if bottom else 0)
    width = 2 * (BOX_W - 1) + 1
    tiles = [[OUTSIDE] * width for _ in range(height)]
    collision = [["0"] * width for _ in range(height)]
    arena = [["0"] * width for _ in range(height)]
    ids = {slot: str(i + 1) for i, slot in enumerate(["hub", "a", "b", "c", "d"])}

    def box(slot: str, x0: int, y0: int, w: int, h: int) -> None:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                edge = x in (x0, x0 + w - 1) or y in (y0, y0 + h - 1)
                tiles[y][x] = WALL if edge else FLOOR[slot]
                collision[y][x] = BLOCKED if edge else "0"
                arena[y][x] = "0" if edge else ids[slot]

    box("hub", 0, hub_y, width, HUB_H)
    for slot in top:
        box(slot, 0 if slot == "a" else BOX_W - 1, 0, BOX_W, SPOKE_H)
    for slot in bottom:
        box(slot, 0 if slot == "c" else BOX_W - 1, hub_y + HUB_H - 1, BOX_W, SPOKE_H)
    for slot in top + bottom:  # a two-tile gap in the wall the room shares with the hub
        gap_y = hub_y if slot in top else hub_y + HUB_H - 1
        for x in GAPS[slot]:
            tiles[gap_y][x] = FLOOR["hub"]
            collision[gap_y][x] = "0"
            arena[gap_y][x] = "0"
    props: list[list[int]] = []

    def prop(x: int, y: int, tile: int) -> None:
        props.append([x, y, tile])
        collision[y][x] = BLOCKED

    for slot in top:  # shelves along the top wall of the rooms above the hub
        x0 = 0 if slot == "a" else BOX_W - 1
        for dx in (1, 2, 3, 5, 6):
            prop(x0 + dx, 1, BOOKCASE)
        prop(x0 + 6, 3, TABLE)
    for slot in bottom:  # chests and a table along the bottom wall of the rooms below
        x0 = 0 if slot == "c" else BOX_W - 1
        for dx in (1, 2, 6, 7):
            prop(x0 + dx, hub_y + HUB_H + SPOKE_H - 3, CHEST)
        prop(x0 + 5, hub_y + HUB_H + SPOKE_H - 3, ANVIL)
    for x in (1, 6, 9, 14):  # the hub: a stool, an anvil and a table clear of the door gaps
        prop(x, hub_y + HUB_H - 2, (STOOL, ANVIL, TABLE, STOOL)[(1, 6, 9, 14).index(x)])
    return {"maze": {"w": width, "h": height, "collision": collision, "arena": arena, "sector": [["1"] * width for _ in range(height)],
                     "names": {ids[s]: s for s in slots}, "sectors": {"1": map_id}},
            "grid": {"tile": 16, "sheet": "tinydungeon.png", "columns": 12, "data": tiles, "props": props}}
