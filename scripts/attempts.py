"""Attempts from belief (#128, docs/plans/attempt-from-belief/): tasks that take several rounds.

A person starts a task with an ordinary move whose rule only checks the rules of the game (place, turn,
possession). The move sets a field to a value that a world process then watches (`status == "attempting to
drive"`); later rounds' processes advance it and end it from whatever is true then. Nothing here changes the
world: this module only finds those starts and endings in the Engine's own events, so the run log, the person's
memory and the page can say what is under way.

How a task ends is read from the ending event, never from its words: it stopped (failed) when that event changed
nothing but the task's field, or put the field back to its value before the start; otherwise it finished.
"""
from __future__ import annotations

from typing import Any

MAX_OPEN_TASKS = 24
TASK_KEYS = {"person", "action", "entity", "field", "value", "before", "started_round", "started_event_id", "expects"}


def _eq_literals(check: dict[str, Any]) -> list[tuple[str, Any]]:
    """(path, literal) for an `eq` check of a participant's field against a literal."""
    if check.get("op") != "eq":
        return []
    out = []
    for a, b in (("left", "right"), ("right", "left")):
        ref, lit = check.get(a), check.get(b)
        if isinstance(ref, dict) and isinstance(ref.get("participant"), dict) and isinstance(lit, dict) and "literal" in lit:
            out.append((str(ref["participant"].get("path")), lit["literal"]))
    return out


def task_watchers(causal: dict[str, Any]) -> dict[tuple[str, str], list[str]]:
    """(field, value as text) -> the world processes that act while a field holds that value.

    A watched value is a task only when a process can end it (moves the field on from that value) and the task
    either makes progress by itself meanwhile (a process acts on it without ending it, as a remedy counts down) or
    can end two different ways (the truck arrives or runs dry). A stance that one rule can knock back, or a done
    flag the work cycle clears, is not a task.
    """
    watching: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for p in causal.get("processes") or []:
        for check in p.get("checks") or []:
            for path, literal in _eq_literals(check):
                watching.setdefault((path, repr(literal)), []).append(p)
    out: dict[tuple[str, str], list[str]] = {}
    for (path, literal), procs in watching.items():
        enders = [p for p in procs if any(e.get("path") == path for e in p.get("effects") or [])]
        progress = [p for p in procs if p not in enders and p.get("effects")]
        if enders and (progress or len(endings(causal).get((path, literal), set())) >= 2):
            out[(path, literal)] = [p["process_id"] for p in procs]
    return out


def endings(causal: dict[str, Any]) -> dict[tuple[str, str], set[str]]:
    """(field, started value) -> the distinct values the world's processes can move it to from there."""
    out: dict[tuple[str, str], set[str]] = {}
    for p in causal.get("processes") or []:
        watched = [pv for c in p.get("checks") or [] for pv in _eq_literals(c)]
        for e in p.get("effects") or []:
            value = e.get("value") or {}
            if e.get("op") != "set" or "literal" not in value:
                continue
            for path, literal in watched:
                if path == e.get("path") and value["literal"] != literal:
                    out.setdefault((path, repr(literal)), set()).add(repr(value["literal"]))
    return out


def _ways(causal: dict[str, Any], key: tuple[str, str]) -> set[str]:
    """The values a task's field can move to while it is under way: by the world's processes, or by any person's
    move that can act then (a move whose own checks require the field to hold some other value cannot)."""
    ways = set(endings(causal).get(key, set()))
    for other in causal.get("mechanics") or []:
        needs = [lit for c in other.get("checks") or [] for path, lit in _eq_literals(c) if path == key[0]]
        if any(repr(lit) != key[1] for lit in needs):
            continue
        ways |= {repr((o.get("value") or {}).get("literal")) for o in other.get("effects") or []
                 if o.get("op") == "set" and o.get("path") == key[0] and "literal" in (o.get("value") or {})
                 and repr(o["value"]["literal"]) != key[1]}
    return ways


def _starts(rule: dict[str, Any], watchers: dict[tuple[str, str], list[str]]) -> list[tuple[str, str, Any]]:
    """(field, value as text, value) for each watched value a rule's effects set."""
    out = []
    for e in rule.get("effects") or []:
        value = e.get("value") or {}
        key = (e.get("path"), repr(value.get("literal")))
        if e.get("op") == "set" and "literal" in value and key in watchers:
            out.append((key[0], key[1], value["literal"]))
    return out


def _resting(bundle: dict[str, Any] | None) -> set[tuple[str, str]]:
    """(field, value as text) for every value a field holds when the world starts."""
    return {(f"components.{c}.{f}", repr(v)) for e in (bundle or {}).get("entities") or []
            for c, fields in (e.get("components") or {}).items() if isinstance(fields, dict) for f, v in fields.items()}


def world_watchers(causal: dict[str, Any], bundle: dict[str, Any] | None = None) -> dict[tuple[str, str], list[str]]:
    """The tasks a world process starts (the rollout an authorization starts), followed like a person's task.

    Only those that can end two ways count, and never a value the world starts in: a meeting being on (one way to
    end, when it passes) is a phase, and a decision open again is back where it rested (2026-10-23 c1r20: the
    rollout was authorized three times and never shown under way).
    """
    watchers, resting = task_watchers(causal), _resting(bundle)
    out = {}
    for p in causal.get("processes") or []:
        for path, text, _ in _starts(p, watchers):
            if (path, text) not in resting and len(_ways(causal, (path, text))) >= 2:
                out[(path, text)] = watchers[(path, text)]
    return out


def long_tasks(causal: dict[str, Any], bundle: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Every move or world process that starts a task, and whether it can end two ways (so it can fail part-way).
    `started_by` is "person" for a move and "world" for a process (see world_watchers; it needs the bundle)."""
    watchers, world = task_watchers(causal), world_watchers(causal, bundle)
    out = []
    for kind, rules, ok in (("person", causal.get("mechanics") or [], watchers),
                            ("world", causal.get("processes") or [], world)):
        for rule in rules:
            for path, text, literal in _starts(rule, ok):
                out.append({"action": rule.get("action_kind") or rule.get("mechanic_id") or rule.get("process_id"),
                            "started_by": kind, "field": path, "value": literal, "watched_by": watchers[(path, text)],
                            "can_fail_part_way": len(_ways(causal, (path, text))) >= 2})
    return out


def part_way_findings(causal: dict[str, Any]) -> list[dict[str, Any]]:
    """A world whose people start tasks that take several rounds, none of which can end two ways (#128 slice 2, E1).

    Every such task then finishes on schedule whatever happens meanwhile, so nobody can start something believing
    it will work and find out otherwise. 2026-10-23 c1r20: all 21 remedies finished one round after they started.
    """
    tasks = [t for t in long_tasks(causal) if t["started_by"] == "person"]
    if not tasks or any(t["can_fail_part_way"] for t in tasks):
        return []
    names = ", ".join(sorted({t["action"] for t in tasks}))
    fields = ", ".join(sorted({f"{t['field']} == {t['value']!r}" for t in tasks}))
    return [{"rule": names, "finding": (
        f"Every task people start ({names}) can only finish: nothing can stop it part-way. Add one process that "
        f"stops it part-way: it checks the task is under way ({fields}) and that something it needs has gone (a "
        "stock at or below zero, a state another person's move changed), and sets the field back to the value it "
        "had before the task started. The person finds out by seeing it in a later round.")}]


def _split(path: str) -> tuple[str, str] | None:
    """"entities.<id>.components.<c>.<f>" -> (id, "components.<c>.<f>")."""
    parts = str(path).split(".")
    if len(parts) == 5 and parts[0] == "entities" and parts[2] == "components":
        return parts[1], ".".join(parts[2:])
    return None


def started(watchers: dict[tuple[str, str], list[str]], person: str, action: str, changes: list[dict[str, Any]],
            round_no: int, event_id: str | None) -> list[dict[str, Any]]:
    """The tasks an accepted move started: each change that set a watched field to its watched value."""
    out = []
    for change in changes:
        where = _split(change.get("path", ""))
        if where and (where[1], repr(change.get("after"))) in watchers and change.get("before") != change.get("after"):
            out.append({"person": person, "action": action, "entity": where[0], "field": where[1],
                        "value": change.get("after"), "before": change.get("before"), "started_round": round_no,
                        "started_event_id": event_id, "expects": None})
    return out


def ended(task: dict[str, Any], event: dict[str, Any], run_event_id: str | None, round_no: int,
          changes: list[dict[str, Any]]) -> dict[str, Any] | None:
    """The task as ended by this event, or None when the event leaves the task's field alone."""
    full = f"entities.{task['entity']}.{task['field']}"
    mine = next((c for c in changes if c.get("path") == full), None)
    if mine is None or mine.get("after") == task["value"]:
        return None
    only_this = all(c.get("path") == full for c in changes)
    outcome = "failed" if only_this or mine.get("after") == task["before"] else "finished"
    return {**task, "status": outcome, "ended_round": round_no, "ending_event_id": run_event_id,
            "ended_by": event.get("rule_id"), "ended_with": mine.get("after")}


def carried(value: object, entities: dict[str, Any]) -> list[dict[str, Any]]:
    """Tasks sent back by the page for the next round, kept only while the world still shows them under way."""
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > MAX_OPEN_TASKS:
        raise ValueError(f"underway must be a list of at most {MAX_OPEN_TASKS} tasks")
    out = []
    for task in value:
        if not isinstance(task, dict) or set(task) != TASK_KEYS:
            raise ValueError(f"each underway task must have exactly {sorted(TASK_KEYS)}")
        for key in ("person", "action", "entity", "field", "started_event_id"):
            if not isinstance(task[key], str) or not 0 < len(task[key]) <= 120:
                raise ValueError(f"underway task {key} must be a short string")
        if type(task["started_round"]) is not int or not (task["expects"] is None or
                                                          (isinstance(task["expects"], str) and len(task["expects"]) <= 600)):
            raise ValueError("underway task started_round must be an integer and expects short text or null")
        entity = entities.get(task["entity"]) or {}
        _, component, name = task["field"].split(".", 2) if task["field"].count(".") == 2 else ("", "", "")
        if ((entity.get("components") or {}).get(component) or {}).get(name, object()) == task["value"]:
            out.append(task)
    return out


def memory_line(task: dict[str, Any], now: Any) -> str:
    """What the person who started a task sees of it in a later round: their own expectation and the field now."""
    name = task["field"].rsplit(".", 1)[-1].replace("_", " ")
    expected = f" You expected: {task['expects']}" if task.get("expects") else ""
    return (f"Your {task['action']} from round {task['started_round']}.{expected} What you see now: "
            f"{task['entity']} {name} is {now!r}.")


def attempt_findings(bundle: dict[str, Any], causal: dict[str, Any]) -> list[dict[str, Any]]:
    """A start that refuses up front on a stock its own task uses up over time (Decision 007, layer 2).

    From the spike's check (spikes/any-scenario-2026-10/checks.py), narrowed: only stocks a world process uses up
    count. A move that uses up a stock in one step (loading a log needs a log) checks possession, which is a rule
    of the game (2026-10-23: the spike's version flagged all 7 transfers in the saved pencil world).
    """
    def owned(sel: dict[str, Any]) -> bool:
        return any(set(sel.get("categories", [])) <= set(e.get("categories", []))
                   and set(sel.get("components", [])) <= set(e.get("components", {}))
                   and str(e.get("owner_ref", "")).startswith("actor:") for e in bundle["entities"])
    used_over_time = {e.get("path") for p in causal.get("processes") or [] for e in p.get("effects") or []
                      if e.get("op") == "subtract"}
    out = []
    for m in causal.get("mechanics") or []:
        parts = dict(m.get("participants") or {})
        for chk in m.get("checks") or []:
            for side in ("left", "right"):
                ref = (chk.get(side) or {}).get("participant") if isinstance(chk.get(side), dict) else None
                if not ref or ref.get("path") not in used_over_time:
                    continue
                # Only "is there enough" gates the outcome; an upper bound (room in a tank) is a fair rule.
                if not ((side == "left" and chk.get("op") in ("gt", "gte")) or
                        (side == "right" and chk.get("op") in ("lt", "lte"))):
                    continue
                name = ref.get("name")
                if name == "actor" or (name in parts and owned(parts[name])):
                    out.append({"rule": m["mechanic_id"], "finding": (
                        f"action {m['mechanic_id']} refuses up front with check '{chk.get('label')}' on "
                        f"{name}.{ref.get('path')}, a stock that a process uses up while the task goes on. Fix with "
                        "three changes: (1) the action only STARTS the activity (sets a status such as 'driving'), "
                        "with no check on that stock; (2) a process that, every round while the status is active "
                        "and the stock is above zero, makes one round of progress and uses up the stock; (3) a "
                        "process that switches the status to a stopped value when the stock is at or below zero, "
                        "so the person finds out by what they see.")})
    return out
