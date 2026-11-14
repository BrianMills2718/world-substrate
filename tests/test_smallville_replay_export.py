"""Smallville replay export: rooms become tiles, rounds become walking steps, refusals and reports stay visible.

Implements: scene-viewer/smallville-replay-export
The map here is a tiny made-up maze, not Smallville's art or data; the export is checked on what it must preserve.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import export_smallville_replay as ex  # noqa: E402


def maze():
    # Two rooms joined by a one-tile doorway at x=3; '#' is blocked (collision 32125).
    rows = ["#######", "#a.#b.#", "#a..b.#", "#a.#b.#", "#######"]
    w, h = 7, 5
    coll = [["32125" if c == "#" else "0" for c in r] for r in rows]
    arena = [[{"a": "1", "b": "2"}.get(c, "0") for c in r] for r in rows]
    arena[2][3] = "0"
    return {"w": w, "h": h, "collision": coll, "arena": arena, "sector": [["9"] * w for _ in range(h)],
            "names": {"1": "left", "2": "right"}, "sectors": {"9": "hall"}}


def row(kind=None, status="accepted", **fields):
    return {"did": ({"kind": kind, **fields} if kind else None), "status": status, "refused_because": ["the door must be open"] if status != "accepted" else []}


@pytest.mark.req("scene-viewer/smallville-replay-export")
def test_rounds_become_walking_steps_and_refusals_and_reports_stay_visible():
    rows = [{"result": {"transcript": [
        {"turn": 1, "actors": {"ari": row("move", "precondition_failed", to="right"), "bo": row()}}]}},
        {"result": {"transcript": [
            {"turn": 2, "actors": {"ari": row("move", to="right"), "bo": row()}}]}},
        {"result": {"transcript": [
            {"turn": 3, "actors": {"ari": row("send-report", recipient="bo", content="Ready."), "bo": row()}}]}}]
    replay = ex.export(rows, maze(), rooms={"left": "hall|left", "right": "hall|right"}, people={"ari": "Ari", "bo": "Bo"},
                            start_rooms={"ari": "left", "bo": "right"}, labels={"right": "right room", "bo": "Bo"}, hold=1)
    steps, meta = replay["steps"], replay["meta"]
    first = steps["1"]["Ari"]
    assert first["pronunciatio"] == ex.EMOJI["refused"] and "refused: the door must be open" in first["description"]
    assert first["movement"] == steps["0"]["Ari"]["movement"]  # a refused walk does not move
    walk = [steps[k]["Ari"]["movement"] for k in sorted(steps, key=int)]
    moves = [b for a, b in zip(walk, walk[1:]) if a != b]
    assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 1 for a, b in zip(walk, walk[1:]))  # at most one tile per step
    assert (3, 2) in [tuple(m) for m in moves]  # through the doorway
    assert tuple(walk[-1]) == ex.anchor(maze(), "hall|right") or steps[str(meta["step"])]["Ari"]["chat"]
    chats = [steps[k]["Ari"]["chat"] for k in steps if steps[k]["Ari"]["chat"]]
    assert chats == [[["Ari", "to Bo: Ready."]]]
    assert meta["persona_names"] == ["Ari", "Bo"] and meta["step"] == len(steps) - 1


@pytest.mark.req("scene-viewer/smallville-replay-export")
def test_an_unreachable_room_fails_loudly():
    m = maze()
    m["collision"][2][3] = "32125"
    with pytest.raises(ValueError, match="no walkable path"):
        ex.walk(m, ex.anchor(m, "hall|left"), ex.anchor(m, "hall|right"))


@pytest.mark.req("scene-viewer/smallville-replay-export")
def test_doors_open_when_opened_and_people_in_one_room_do_not_stack():
    m = maze()
    m["collision"][1][4] = "0"
    rows = [{"result": {"transcript": [{"turn": 1, "actors": {"ari": row("open-door", way="d-in", partner="d-out"), "bo": row()}}]}},
            {"result": {"transcript": [{"turn": 2, "actors": {"ari": row("move", to="right"), "bo": row()}}]}}]
    replay = ex.export(rows, m, rooms={"left": "hall|left", "right": "hall|right"}, people={"ari": "Ari", "bo": "Bo"},
                       start_rooms={"ari": "left", "bo": "right"}, labels={}, hold=1,
                       doors={"door": {"between": ["left", "right"], "halves": ["d-in", "d-out"]}})
    assert replay["doors"]["door"]["tiles"] == [[3, 2]]
    assert replay["door_changes"] == [{"step": 0, "door": "door", "state": "closed"}, {"step": 1, "door": "door", "state": "open"}]
    last = replay["steps"][str(replay["meta"]["step"])]
    assert last["Ari"]["movement"] != last["Bo"]["movement"]  # both in the right room, on different tiles
    assert [r["round"] for r in replay["rounds"]] == [1, 2]
