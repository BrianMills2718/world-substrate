"""The "What happened" readout: a detachable analysis of one finished run.

A lens names the patterns a reader wants found (here, the four coordination mechanisms of the Waltzman paper). One
light model call reads the run's recorded Engine events and says, for each pattern, which events show it or why it
is missing. Every event id it cites is checked against the recording; a pattern the model calls present without a
real event id is reported missing. The analysis never changes the world (AGENTS.md: post-run analysis stays separate
from canonical truth), and its result is saved with a shared run, so a replay needs no AI call.
"""

from __future__ import annotations

import json
from typing import Any

READOUT_SCHEMA = "world-builder-readout/v1"
MAX_EVIDENCE_EVENTS = 700
MAX_TEXT = 160

# The lens is data, not code: any people world is read through the same patterns, and none of them names a
# particular scenario's people, records or rules.
LENSES: dict[str, dict[str, Any]] = {
    "coordination": {
        "title": "How coordination slowed (the four mechanisms of the Waltzman paper)",
        "mechanisms": [
            {"id": "separate-channels", "name": "Local concerns through separate channels",
             "meaning": "Different people raise their own local concern, each through their own route to a "
                        "particular decision maker, so the decision makers hear different things."},
            {"id": "slowed-meetings", "name": "Slowed meetings",
             "meaning": "Meetings, reviews or decision deadlines are delayed, extended or used up without "
                        "producing a decision."},
            {"id": "reopened-issues", "name": "Reopened settled issues",
             "meaning": "Something already settled (a concern resolved, a readiness met, an approval given) is "
                        "undone or put back up for discussion."},
            {"id": "conditional-support", "name": "Conditional support delaying deployment",
             "meaning": "Someone's support depends on a condition; while the condition is unmet their support is "
                        "withheld or withdrawn, and that holds back the final decision or deployment."},
        ],
    },
}


def _short(value: Any, limit: int = 160) -> str:
    """A value as the trace has it; only a very long one (a list or record) is cut. 2026-10-18 live Waltzman
    WtCqXpKjI3Bs: a 40-character cut clipped entity ids ("info-logistics-backup-power-concern-t..."), so a reader
    could not find the claimed change in the trace."""
    text = value if isinstance(value, str) else json.dumps(value, separators=(",", ":"), default=str)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _change_text(changes: list[dict[str, Any]], limit: int = 400) -> str:
    """Whole changes up to about `limit` characters, then how many more. 2026-10-18 live Waltzman 1nEGWZzSwHFA: a
    plain [:400] cut a claim mid-path ("entities.info-logi"), so the readout showed a change no event made."""
    parts = [f"{c.get('path')}: {_short(c.get('before'))} -> {_short(c.get('after'))}" for c in changes]
    kept: list[str] = []
    for part in parts:
        if kept and len("; ".join(kept + [part])) > limit:
            break
        kept.append(part)
    more = len(parts) - len(kept)
    return "; ".join(kept) + (f"; and {more} more change{'s' if more > 1 else ''}" if more else "")


def evidence_events(rounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every recorded event of a run that changed the world, in order: people's moves and the world's own changes."""
    out: list[dict[str, Any]] = []
    for row in rounds:
        turn = row.get("turn")
        for actor, move in sorted((row.get("actors") or {}).items()):
            if move.get("status") != "accepted" or not move.get("event_id") or not move.get("changes"):
                continue
            out.append({"event_id": move["event_id"], "round": turn, "by": actor,
                        "move": (move.get("did") or {}).get("kind"),
                        "changed": _change_text(move["changes"]),
                        "said": str(move.get("said") or "")[:MAX_TEXT]})
        for event in row.get("world_events") or []:
            if event.get("event_id") and event.get("changes"):
                out.append({"event_id": event["event_id"], "round": turn, "by": "the world (a rule)",
                            "move": event.get("rule_id"), "changed": _change_text(event["changes"])})
    return out[:MAX_EVIDENCE_EVENTS]


def readout_prompt(lens_id: str, people: list[dict[str, Any]] | None, events: list[dict[str, Any]]) -> list[dict[str, str]]:
    lens = LENSES[lens_id]
    mechanisms = "\n".join(f"- {m['id']}: {m['name']}. {m['meaning']}" for m in lens["mechanisms"])
    cast = "\n".join(f"- {p.get('id') or p.get('entity_id')}: {p.get('label') or ''} ({p.get('position') or p.get('role') or ''})"
                     for p in (people or []))
    system = (
        "You read the recorded events of one finished simulation and say plainly what happened, through a fixed "
        "lens. Use only the events given; never invent an event. For each mechanism, say present only when you can "
        "cite at least one event_id from the list that shows it, and name the events that show it best (at most "
        "eight). Otherwise say missing and give the plain reason (for example: nobody's support ever depended on a "
        "condition; no settled item was ever undone). Write for someone who has never seen the simulation: short "
        "sentences, the people's names, no ids in the prose. "
        'Return only JSON: {"summary": str (two or three sentences on what happened overall), "mechanisms": '
        '[{"id": str, "status": "present" | "missing", "event_ids": [str], "explanation": str (one or two '
        'sentences), "missing_reason": str (empty when present)}]}.'
    )
    user = (f"Lens: {lens['title']}\nMechanisms:\n{mechanisms}\n\nPeople:\n{cast or '- (not recorded)'}\n\n"
            f"Events ({len(events)}, in order):\n" + "\n".join(json.dumps(e, separators=(",", ":")) for e in events))
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def validate_readout(lens_id: str, parsed: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep only what the recording supports: cited ids must be events of this run."""
    if not isinstance(parsed, dict):
        raise ValueError("the readout reply was not an object")
    known = {e["event_id"]: e for e in events}
    given = {m.get("id"): m for m in parsed.get("mechanisms") or [] if isinstance(m, dict)}
    out = []
    for mechanism in LENSES[lens_id]["mechanisms"]:
        claim = given.get(mechanism["id"]) or {}
        cited = [str(i) for i in claim.get("event_ids") or []]
        real = [i for i in dict.fromkeys(cited) if i in known][:8]
        unknown = [i for i in cited if i not in known]
        present = claim.get("status") == "present" and bool(real)
        reason = str(claim.get("missing_reason") or "").strip()[:300]
        if claim.get("status") == "present" and not real:
            reason = "The analysis named no event from this run that shows it, so it is counted as missing."
        out.append({
            "id": mechanism["id"], "name": mechanism["name"],
            "status": "present" if present else "missing",
            "event_ids": real if present else [],
            "events": [{k: known[i][k] for k in ("event_id", "round", "by", "move", "changed")} for i in real]
            if present else [],
            "explanation": str(claim.get("explanation") or "").strip()[:400] if present else "",
            "missing_reason": "" if present else (reason or "The analysis found no event that shows it."),
            "dropped_event_ids": unknown[:8],
        })
    return {"schema": READOUT_SCHEMA, "lens": lens_id, "title": LENSES[lens_id]["title"],
            "summary": str(parsed.get("summary") or "").strip()[:700], "mechanisms": out,
            "events_read": len(events)}


def read_run(
    rounds: list[dict[str, Any]],
    *,
    people: list[dict[str, Any]] | None,
    model: str,
    trace_id: str,
    max_budget: float,
    lens_id: str = "coordination",
) -> tuple[dict[str, Any], Any]:
    from llm_client import call_llm, safe_json_loads

    events = evidence_events(rounds)
    if not events:
        raise ValueError("this run recorded no events with their ids (it was made before the readout existed), "
                         "so there is nothing to read; run the world again")
    result = call_llm(
        model,
        readout_prompt(lens_id, people, events),
        task="world-substrate-run-readout",
        trace_id=trace_id,
        max_budget=max_budget,
        reasoning_effort="low",
        num_retries=1,
    )
    return validate_readout(lens_id, safe_json_loads(result.content), events), result
