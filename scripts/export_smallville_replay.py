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
import sys
from collections import deque
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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


def spots(maze: dict[str, Any], arena_name: str, count: int) -> list[tuple[int, int]]:
    """`count` distinct tiles of a room nearest its centre, so people sent to one room do not stack."""
    tiles = room_tiles(maze, arena_name)
    if len(tiles) < count:
        raise ValueError(f"{arena_name!r} has fewer than {count} walkable tiles")
    cx, cy = sum(t[0] for t in tiles) / len(tiles), sum(t[1] for t in tiles) / len(tiles)
    return sorted(tiles, key=lambda t: ((t[0] - cx) ** 2 + (t[1] - cy) ** 2, t))[:count]


def doorway(maze: dict[str, Any], path: list[tuple[int, int]], max_width: int = 2) -> list[tuple[int, int]]:
    """The first run of at most `max_width` walkable tiles that a path squeezes through (a doorway in a wall).

    Looks across the direction of travel at each tile of the path; open floor is wider and is skipped."""
    def free(x: int, y: int) -> bool:
        return 0 <= x < maze["w"] and 0 <= y < maze["h"] and maze["collision"][y][x] == "0"

    for before, tile in zip(path, path[1:]):
        px, py = (0, 1) if tile[0] != before[0] else (1, 0)
        run = [tile]
        for sign in (1, -1):
            x, y = tile[0] + sign * px, tile[1] + sign * py
            while free(x, y) and len(run) <= max_width:
                run.append((x, y))
                x, y = x + sign * px, y + sign * py
        if len(run) <= max_width:
            return sorted(run)
    raise ValueError("path never passes through a doorway")


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


def _effect_words(effect: dict[str, Any]) -> str:
    """One effect of a rule in plain words, from its recorded shape (who, which field, what is done)."""
    who, field = effect.get("participant", "?"), str(effect.get("path", "")).split(".")[-1].replace("_", " ")
    value = effect.get("value") or {}
    if effect.get("op") == "set" and "literal" in value:
        return f"sets the {who}'s {field} to {json.dumps(value['literal']).strip(chr(34))}"
    if effect.get("op") == "set":
        return f"sets the {who}'s {field} from the action"
    if str(effect.get("op", "")).startswith("append"):
        return f"adds the words to the {who}'s {field}"
    return f"{effect.get('op', 'changes')} the {who}'s {field}"


def rules_of(causal: dict[str, Any] | None) -> list[dict[str, Any]]:
    """The world's rules (one per action kind) as the overlay shows them: why it exists, what it requires, what it changes."""
    out = []
    for m in (causal or {}).get("mechanics") or []:
        participants = json.dumps(m.get("checks") or [])
        out.append({"kind": m["action_kind"], "rationale": m.get("rationale", ""),
                    "needs": [c["label"] for c in m.get("checks") or [] if c.get("label")],
                    "changes": [_effect_words(e) for e in m.get("effects") or []], "limits": list(m.get("limits") or []),
                    "at_doors": '"way"' in participants or any(e.get("participant") == "way" for e in m.get("effects") or [])})
    return out


def export(rows: list[dict[str, Any]], maze: dict[str, Any], rooms: dict[str, str], people: dict[str, str],
           start_rooms: dict[str, str], labels: dict[str, str], doors: dict[str, dict[str, Any]] | None = None,
           sprites: dict[str, str] | None = None, hold: int = 2, causal: dict[str, Any] | None = None) -> dict[str, Any]:
    """The replay as one dict: `steps` (Smallville's master_movement shape), `meta`, `doors`, `door_changes`, `rounds`, `view`, `sprites`.

    `rows` are server run-log rows (one saved round each); `rooms` maps room id to "<sector>|<arena>" on the map;
    `people` maps person id to the persona name shown; `doors` maps a door id to {"between": [room, room], "halves":
    [entity ids that open together]} (the doorway tiles are found on the path between the two rooms)."""
    order = list(people)
    spot = {room: spots(maze, arena, len(order)) for room, arena in rooms.items()}
    place = lambda room, person: spot[room][order.index(person)]
    pos = {p: place(start_rooms[p], p) for p in people}
    door_rows: dict[str, Any] = {}
    for door_id, door in (doors or {}).items():
        a, b = door["between"]
        centre = lambda room: anchor(maze, rooms[room])
        door_rows[door_id] = {"tiles": [list(t) for t in doorway(maze, [centre(a)] + walk(maze, centre(a), centre(b)))],
                              "between": [a, b], "halves": list(door["halves"])}
    half_of = {h: d for d, row in door_rows.items() for h in row["halves"]}
    steps: dict[str, Any] = {}
    changes: list[dict[str, Any]] = [{"step": 0, "door": d, "state": "closed" if row["halves"] else "open"} for d, row in door_rows.items()]  # no halves: always open
    round_index: list[dict[str, int]] = []
    n = 0
    rounds = sorted(((t["turn"], t) for r in rows for t in r["result"]["transcript"]), key=lambda x: x[0])
    steps["0"] = {people[p]: {"movement": list(pos[p]), "pronunciatio": EMOJI["wait"], "description": "waiting", "chat": None} for p in people}
    for number, turn in rounds:
        info = {p: describe(p, turn["actors"].get(p, {}), labels) for p in people}
        paths: dict[str, list[tuple[int, int]]] = {}
        for p in people:
            did = (turn["actors"].get(p) or {}).get("did") or {}
            if did.get("kind") == "move" and turn["actors"][p].get("status") == "accepted":
                paths[p] = walk(maze, pos[p], place(did["to"], p))
        length = max([len(v) for v in paths.values()] + [0]) + hold
        start = n + 1
        for p in people:
            did = (turn["actors"].get(p) or {}).get("did") or {}
            if did.get("kind") == "open-door" and turn["actors"][p].get("status") == "accepted" and did.get("way") in half_of:
                changes.append({"step": start, "door": half_of[did["way"]], "state": "open"})
        for i in range(length):
            n += 1
            frame = {}
            for p in people:
                if p in paths and i < len(paths[p]):
                    pos[p] = paths[p][i]
                emoji, text, chat = info[p]
                frame[people[p]] = {"movement": list(pos[p]), "pronunciatio": emoji, "description": text,
                                    "chat": [[people[p], chat]] if chat else None}
                tried = turn["actors"].get(p) or {}
                kind = (tried.get("did") or {}).get("kind")
                if kind and causal is not None:  # which rule this person's attempt met, and whether it let it through
                    way = (tried["did"].get("way"))
                    frame[people[p]]["rule"] = {"kind": kind, "ok": tried.get("status") == "accepted",
                                                "why": list(tried.get("refused_because") or []), "door": half_of.get(way)}
            steps[str(n)] = frame
        round_index.append({"round": number, "start": start, "end": n})
    meta = {"fork_sim_code": "world-substrate", "start_date": "February 13, 2023", "curr_time": "February 13, 2023, 00:00:00",
            "sec_per_step": 1, "maze_name": "the_ville", "persona_names": list(people.values()), "step": n}
    xs = [t[0] for r in rooms.values() for t in room_tiles(maze, r)] + [t[0] for d in door_rows.values() for t in d["tiles"]]
    ys = [t[1] for r in rooms.values() for t in room_tiles(maze, r)] + [t[1] for d in door_rows.values() for t in d["tiles"]]
    view = {"x": min(xs) - 1, "y": min(ys) - 1, "w": max(xs) - min(xs) + 3, "h": max(ys) - min(ys) + 3}
    return {"steps": steps, "meta": meta, "doors": door_rows, "door_changes": changes, "rounds": round_index, "view": view,
            "sprites": sprites or {}, **({"rules": rules_of(causal)} if causal is not None else {})}


def withhold_words(replay: dict[str, Any]) -> dict[str, Any]:
    """Replace the words of every report with a note, for a replay shown to someone who may not read them."""
    for frame in replay["steps"].values():
        for who in frame.values():
            if who.get("chat"):
                who["chat"] = [[name, text.split(": ", 1)[0] + ": (words not shown)"] for name, text in who["chat"]]
    return replay


def export_from_rows(rows: list[dict[str, Any]], bundle: dict[str, Any], maze_dir: Path, causal: dict[str, Any] | None = None) -> dict[str, Any]:
    """A replay for run-log `rows` of the world described by `bundle`, using the bundle's own `layout`."""
    from scripts.scene_layout import resolve

    layout = resolve(bundle)
    generated = None
    if layout["prepared"].get("kind") == "generated":  # a map made from code: no clone, no private art
        from scripts.generated_map import build
        generated = build(layout["map"], list(layout["prepared"]["slots"]))
    replay = export(rows, generated["maze"] if generated else load_maze(maze_dir), rooms=layout["rooms"], people=layout["people"], start_rooms=layout["start_rooms"],
                    labels=layout["labels"], doors=layout["doors"], sprites=layout["sprites"], causal=causal)
    replay["map"], replay["title"] = layout["map"], layout["title"]
    if generated:
        replay["grid"] = generated["grid"]
        replay["meta"]["maze_name"] = layout["map"]  # no Smallville name in a public replay
    return replay


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run_log", type=Path)
    ap.add_argument("bundle", type=Path, help="the world's authoring bundle JSON (carries the `layout` declaration)")
    ap.add_argument("maze_dir", type=Path, help="the Smallville the_ville matrix folder")
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    rows = [json.loads(line) for line in args.run_log.read_text().splitlines() if line.strip()]
    replay = export_from_rows(rows, json.loads(args.bundle.read_text()), args.maze_dir)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "master_movement.json").write_text(json.dumps(replay["steps"]))
    (args.out_dir / "meta.json").write_text(json.dumps(replay["meta"]))
    (args.out_dir / "replay.json").write_text(json.dumps(replay))
    print(f"{len(replay['steps'])} steps, {len(replay['meta']['persona_names'])} people, {len(replay['doors'])} doors -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
