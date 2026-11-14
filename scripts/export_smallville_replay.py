#!/usr/bin/env python3
"""Export a retained World Substrate run as a Smallville replay (`master_movement.json` plus `meta.json`).

Implements: scene-viewer/smallville-replay-export (spike; Brian, 2026-11-14, "yes" to the viewer spike).

The substrate knows rooms, not coordinates. A map file (here the Smallville "Ville" maze) supplies each room's tiles;
this exporter picks an anchor tile per room, finds each walk with a breadth-first search over the map's walkable tiles,
and expands every round into steps (one tile per step). The rules never see a coordinate. Door state, messages and
refusals ride in each step's `description` and `chat`, because Smallville has no door object.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import deque
from pathlib import Path
from typing import Any

EMOJI = {"calibrate-pump": "🔧", "open-door": "🚪", "move": "🚶", "send-report": "💬", "wait": "💤", "refused": "⛔"}


def load_maze(maze_dir: Path) -> dict[str, Any]:
    meta = json.loads((maze_dir / "maze_meta_info.json").read_text())
    width, height = int(meta["maze_width"]), int(meta["maze_height"])

    def grid(name: str) -> list[list[str]]:
        flat = [c.strip() for c in next(csv.reader((maze_dir / "maze" / name).open()))]
        return [flat[y * width:(y + 1) * width] for y in range(height)]

    names = {row[0].strip(): row[-1].strip() for row in csv.reader((maze_dir / "special_blocks" / "arena_blocks.csv").open())}
    sectors = {row[0].strip(): row[-1].strip() for row in csv.reader((maze_dir / "special_blocks" / "sector_blocks.csv").open())}
    return {"w": width, "h": height, "collision": grid("collision_maze.csv"), "arena": grid("arena_maze.csv"),
            "sector": grid("sector_maze.csv"), "names": names, "sectors": sectors}


def room_tiles(maze: dict[str, Any], arena_name: str) -> list[tuple[int, int]]:
    """Walkable tiles of one room, named "<sector>|<arena>" (arena names repeat across buildings)."""
    sector, arena = arena_name.split("|")
    return [(x, y) for y in range(maze["h"]) for x in range(maze["w"])
            if maze["names"].get(maze["arena"][y][x]) == arena and maze["sectors"].get(maze["sector"][y][x]) == sector
            and maze["collision"][y][x] == "0"]


def anchor(maze: dict[str, Any], arena_name: str) -> tuple[int, int]:
    tiles = room_tiles(maze, arena_name)
    if not tiles:
        raise ValueError(f"map has no walkable tile in {arena_name!r}")
    cx, cy = sum(t[0] for t in tiles) / len(tiles), sum(t[1] for t in tiles) / len(tiles)
    return min(tiles, key=lambda t: (t[0] - cx) ** 2 + (t[1] - cy) ** 2)


def walk(maze: dict[str, Any], start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
    """Shortest 4-neighbour path over walkable tiles, start excluded."""
    seen = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = []
            while cur != start:
                path.append(cur)
                cur = seen[cur]
            return path[::-1]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cur[0] + dx, cur[1] + dy)
            if 0 <= nxt[0] < maze["w"] and 0 <= nxt[1] < maze["h"] and nxt not in seen and maze["collision"][nxt[1]][nxt[0]] == "0":
                seen[nxt] = cur
                queue.append(nxt)
    raise ValueError(f"no walkable path from {start} to {goal}")


def describe(actor: str, row: dict[str, Any], labels: dict[str, str]) -> tuple[str, str, str | None]:
    """(emoji, description, chat line) for one person's attempt in a round, from the recorded did/status."""
    did = row.get("did") or {}
    kind = did.get("kind")
    if not kind:
        return EMOJI["wait"], "waiting", None
    name = lambda key: labels.get(did.get(key), did.get(key))
    what = {"move": lambda: f"walking to the {name('to')}", "open-door": lambda: f"opening the {str(name('way')).lower()}",
            "calibrate-pump": lambda: "calibrating the pump",
            "send-report": lambda: f"telling {name('recipient')} the pump status"}.get(kind, lambda: str(kind))()
    if row.get("status") != "accepted":
        why = "; ".join(row.get("refused_because") or []) or row.get("status")
        return EMOJI["refused"], f"{what.replace('walking', 'trying to walk')} - refused: {why}", None
    chat = f"to {name('recipient')}: {did.get('content')}" if kind == "send-report" else None
    return EMOJI[kind], what, chat


def export(rows: list[dict[str, Any]], maze: dict[str, Any], rooms: dict[str, str], people: dict[str, str],
           start_rooms: dict[str, str], labels: dict[str, str], hold: int = 2) -> tuple[dict[str, Any], dict[str, Any]]:
    """`rows` are server run-log rows (one saved round each); `rooms` maps room id to a map arena name; `people` maps person id to the persona name shown."""
    anchors = {room: anchor(maze, arena) for room, arena in rooms.items()}
    pos = {p: anchors[start_rooms[p]] for p in people}
    where = dict(start_rooms)
    steps: dict[str, Any] = {}
    n = 0
    rounds = sorted(((t["turn"], t) for r in rows for t in r["result"]["transcript"]), key=lambda x: x[0])
    steps[str(n)] = {people[p]: {"movement": list(pos[p]), "pronunciatio": EMOJI["wait"], "description": "waiting", "chat": None} for p in people}
    for _, turn in rounds:
        info = {p: describe(p, turn["actors"].get(p, {}), labels) for p in people}
        paths: dict[str, list[tuple[int, int]]] = {}
        for p in people:
            did = (turn["actors"].get(p) or {}).get("did") or {}
            if did.get("kind") == "move" and turn["actors"][p].get("status") == "accepted":
                paths[p] = walk(maze, pos[p], anchors[did["to"]])
                where[p] = did["to"]
        length = max([len(v) for v in paths.values()] + [0]) + hold
        for i in range(length):
            n += 1
            frame = {}
            for p in people:
                if p in paths and i < len(paths[p]):
                    pos[p] = paths[p][i]
                emoji, text, chat = info[p]
                frame[people[p]] = {"movement": list(pos[p]), "pronunciatio": emoji, "description": text,
                                    "chat": [[people[p], chat]] if chat and i == length - 1 else None}
            steps[str(n)] = frame
    meta = {"fork_sim_code": "world-substrate", "start_date": "February 13, 2023", "curr_time": "February 13, 2023, 00:00:00",
            "sec_per_step": 1, "maze_name": "the_ville", "persona_names": list(people.values()), "step": n}
    return steps, meta


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_log", type=Path)
    ap.add_argument("maze_dir", type=Path, help="the Smallville the_ville matrix folder")
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    rows = [json.loads(line) for line in args.run_log.read_text().splitlines() if line.strip()]
    maze = load_maze(args.maze_dir)
    steps, meta = export(
        rows, maze,
        rooms={"laboratory": "Dorm for Oak Hill College|Maria Lopez's room", "corridor": "Dorm for Oak Hill College|common room",
               "control-room": "Dorm for Oak Hill College|Klaus Mueller's room"},
        people={"ari": "Ari", "mara": "Mara", "bo": "Bo"},
        start_rooms={"ari": "laboratory", "mara": "corridor", "bo": "control-room"},
        labels={"laboratory": "laboratory", "corridor": "corridor", "control-room": "control room", "ari": "Ari", "mara": "Mara", "bo": "Bo",
                "lab-door-out": "Laboratory door", "lab-door-in": "Laboratory door", "control-door-in": "Control room door", "control-door-out": "Control room door"})
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "master_movement.json").write_text(json.dumps(steps))
    (args.out_dir / "meta.json").write_text(json.dumps(meta))
    print(f"{len(steps)} steps, {len(meta['persona_names'])} people -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
