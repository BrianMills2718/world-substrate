#!/usr/bin/env python3
"""Every saved run must come with a read-through of its whole trace.

Brian, 2026-10-16: "every plan should have a requirement to have visibility for the full trace and that you
should be examining this". On 2026-10-22 an agent described a run's analysis as a round-by-round reading when
it was a counting script's output naming 1 of the run's 111 AI trace ids. Nothing checked it.

A saved run is a folder holding `run-log.jsonl`: that run's lines from the server run log (GET /runs --full).
Next to it, `TRACE_READ.md` must have:
  - a `## Round N` section for every round, naming every person who tried a move that round and citing at
    least one of that round's event ids (`rN-e...`);
  - for every task that takes several rounds (`underway` in a round, #128), its start event id in the round it
    started and its ending event id in the round it ended, so the read says how each one turned out;
  - every llm_client trace id the log names (open each one; say what it showed);
  - a non-empty `## Findings` section.
This proves coverage, not care: it cannot tell a careful note from a careless one.

    python3 scripts/check_trace_reads.py [--root evidence]       # check every saved run
    python3 scripts/check_trace_reads.py --skeleton <run folder>  # print empty headings to fill in
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROUND_HEADING = re.compile(r"^## Round (\d+)\s*$", re.M)
ANY_HEADING = re.compile(r"^## ", re.M)


def _rows(log: Path) -> list[dict]:
    return [json.loads(line) for line in log.read_text().splitlines() if line.strip()]


def required(rows: list[dict]) -> tuple[set[str], dict[int, dict[str, set[str]]]]:
    """Trace ids, and per round: who tried a move and which event ids that round produced."""
    trace_ids: set[str] = set()
    rounds: dict[int, dict[str, set[str]]] = {}
    for row in rows:
        trace_ids.update(t for t in [row.get("trace_id"), *(row.get("trace_ids") or [])] if t)
        result = row.get("result") or {}
        for turn in result.get("transcript") or []:
            n = int(turn["turn"])
            entry = rounds.setdefault(n, {"actors": set(), "events": set(), "tasks": set()})
            for task in turn.get("underway") or []:
                if task.get("started_round") == n and task.get("started_event_id"):
                    entry["tasks"].add(task["started_event_id"])
                if task.get("status") in ("failed", "finished") and task.get("ending_event_id"):
                    entry["tasks"].add(task["ending_event_id"])
            for actor, act in (turn.get("actors") or {}).items():
                if act.get("status") != "no_action" or act.get("wanted"):
                    entry["actors"].add(actor)
                if act.get("event_id"):
                    entry["events"].add(act["event_id"])
        for event in result.get("engine_events") or []:
            match = re.match(r"r(\d+)-", str(event.get("event_id") or event.get("id") or ""))
            if match:
                rounds.setdefault(int(match.group(1)), {"actors": set(), "events": set(), "tasks": set()})["events"].add(
                    event.get("event_id") or event.get("id"))
    return trace_ids, rounds


def sections(text: str) -> dict[str, str]:
    """`## Heading` -> body, up to the next `## ` heading."""
    starts = [m.start() for m in ANY_HEADING.finditer(text)] + [len(text)]
    out = {}
    for a, b in zip(starts, starts[1:]):
        head, _, body = text[a:b].partition("\n")
        out[head[3:].strip()] = body.strip()
    return out


def check_run(folder: Path) -> list[str]:
    log = folder / "run-log.jsonl"
    read = folder / "TRACE_READ.md"
    if not read.is_file():
        return [f"{folder}: no TRACE_READ.md beside run-log.jsonl"]
    trace_ids, rounds = required(_rows(log))
    text = read.read_text()
    found = sections(text)
    problems = [f"{folder}: trace id never named: {t}" for t in sorted(trace_ids) if t not in text]
    for n, need in sorted(rounds.items()):
        body = found.get(f"Round {n}")
        if body is None:
            problems.append(f"{folder}: no '## Round {n}' section")
            continue
        missing = sorted(a for a in need["actors"] if a not in body)
        if missing:
            problems.append(f"{folder}: Round {n} does not mention {', '.join(missing)}")
        if need["events"] and not any(e in body for e in need["events"]):
            problems.append(f"{folder}: Round {n} cites none of its event ids")
        unnamed = sorted(e for e in need.get("tasks", set()) if not re.search(rf"{re.escape(e)}(?!\d)", body))
        if unnamed:
            problems.append(f"{folder}: Round {n} does not name the start or end of a task under way: {', '.join(unnamed)}")
    if not found.get("Findings"):
        problems.append(f"{folder}: '## Findings' is missing or empty")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=REPO / "evidence")
    parser.add_argument("--skeleton", type=Path)
    args = parser.parse_args()
    if args.skeleton:
        _, rounds = required(_rows(args.skeleton / "run-log.jsonl"))
        print("# Trace read\n\n## Findings\n\n" + "".join(f"## Round {n}\n\n" for n in sorted(rounds)))
        return 0
    runs = sorted(p.parent for p in args.root.rglob("run-log.jsonl"))
    problems = [p for run in runs for p in check_run(run)]
    for problem in problems:
        print(problem)
    print(f"RESULT runs={len(runs)} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
