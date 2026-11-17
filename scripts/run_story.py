"""The plain "what happened, round by round" story of a run, for the Simple view of the World Builder page.

Implements: world-builder-page/simple-view-story

One light AI call (a few when the run is long) reads the recorded events of a finished run and writes one to three
plain sentences per round. Each sentence must cite events that exist in the recording; a sentence that cites none is
dropped and counted. Post-run analysis only: nothing here writes into the run or its checkpoints. Prose is never read
back with regex; rounds and event ids are structured JSON fields.
"""

from __future__ import annotations

import json
from typing import Any

STORY_SCHEMA = "world-builder-story/v1"
# About 40k tokens is a 40-round ten-person run (scripts/world_builder_service.py, READOUT_BUDGET comment); a slice
# stays near 15 rounds so one call always fits, and the characters figure keeps the estimate checkable before the call.
MAX_PROMPT_CHARS = 90_000
SLICE_ROUNDS = 15
MAX_TEXT = 220
_QUIET = {"no_action"}


def _clip(value: Any, limit: int = MAX_TEXT) -> str:
    text = value if isinstance(value, str) else json.dumps(value, separators=(",", ":"), default=str)
    return text if len(text) <= limit else text[: limit - 3] + "..."


def story_events(rounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One row per actor per round for every recorded status except no_action, with the reason a refused or
    unmatched try gives. (evidence_events in run_readout.py keeps only moves that changed the world; the readout
    depends on that, so this is a separate list.)"""
    out: list[dict[str, Any]] = []
    for row in rounds:
        turn = row.get("turn")
        for actor, move in sorted((row.get("actors") or {}).items()):
            status = move.get("status")
            if status in _QUIET or not move.get("event_id"):
                continue
            did = move.get("did") or move.get("wanted") or {}
            event = {"event_id": move["event_id"], "round": turn, "by": actor, "status": status,
                     "move": did.get("kind")}
            if did.get("kind") == "unmatched-attempt":
                # The reason an unmatched try went nowhere is did.why; refused_because is blank for these rows.
                event.update(attempt=_clip(did.get("attempt")), nearest_kind=did.get("nearest_kind"),
                             why=_clip(did.get("why")))
            else:
                attempt = (move.get("attempt") or {}).get("text")
                if attempt:
                    event["attempt"] = _clip(attempt)
                if move.get("refused_because"):
                    event["checks"] = _clip("; ".join(map(str, move["refused_because"])), 400)
                changes = [f"{c.get('path')}: {_clip(c.get('before'), 60)} -> {_clip(c.get('after'), 60)}"
                           for c in (move.get("changes") or [])[:3]]
                if changes:
                    event["changed"] = "; ".join(changes)
            if move.get("said"):
                event["said"] = _clip(move["said"])
            ruling = (move.get("ruling") or {}).get("state")
            if ruling:
                event["ruling"] = ruling
            out.append(event)
    return out


def slices(rounds: list[dict[str, Any]], events: list[dict[str, Any]], people: list[dict[str, Any]] | None
           ) -> list[list[dict[str, Any]]]:
    """One slice when the whole event list fits in one call, else blocks of about SLICE_ROUNDS rounds."""
    if len(json.dumps(events, separators=(",", ":"))) + len(json.dumps(people or [])) <= MAX_PROMPT_CHARS:
        return [events]
    numbers = sorted({e["round"] for e in events})
    blocks = [numbers[i:i + SLICE_ROUNDS] for i in range(0, len(numbers), SLICE_ROUNDS)]
    return [[e for e in events if e["round"] in set(block)] for block in blocks]


def story_prompt(people: list[dict[str, Any]] | None, events: list[dict[str, Any]], world_sentence: str,
                 rounds_wanted: list[int]) -> list[dict[str, str]]:
    cast = "\n".join(f"- {p.get('id') or p.get('entity_id')}: {p.get('label') or ''} ({p.get('position') or p.get('role') or ''})"
                     for p in (people or []))
    system = (
        "You tell a person who has never seen this simulation what happened in each round of one recorded run, in "
        "plain words. Use only the events given; never invent one. Name the people by their labels. Say what each "
        "tried to do. When a try did not work, say why in everyday words: for a refused move, translate the check "
        "names (for example 'Information is not active yet' means the message was not available to send yet); for "
        "an unmatched attempt, say the world has no rule for what they tried and use the plain reason given. Never "
        "show ids, check names, field names or the words 'precondition' or 'unsupported'. Write one to three short "
        "sentences per round, only for the rounds listed. Put ids only in the event_ids field, never in the text. Every sentence must cite at least one event_id from the "
        "events that shows it. "
        'Return only JSON: {"rounds": [{"round": int, "sentences": [{"text": str, "event_ids": [str]}]}]}.'
    )
    user = (f"The world: {world_sentence or '(not recorded)'}\n\nPeople:\n{cast or '- (not recorded)'}\n\n"
            f"Rounds to tell: {rounds_wanted}\n\nEvents ({len(events)}, in order):\n" + "\n".join(
                json.dumps(e, separators=(",", ":")) for e in events))
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def plain_text(text: str, event_ids: list[str]) -> str:
    """The sentence without the event ids the model wrote into it (2026-11-17 live Waltzman: "(r1-e00002, r1-e00010)"
    after each sentence). Only the ids the sentence itself cites are removed, as plain strings; the ids stay on the
    sentence as its evidence."""
    for event_id in sorted(event_ids, key=len, reverse=True):
        text = text.replace(event_id, "")
    for empty in ("(, , , , )", "(, , , )", "(, , )", "(, )", "( )", "()", "[]"):
        text = text.replace(empty, "")
    return " ".join(text.replace(" ,", ",").replace(" .", ".").replace(" ;", ";").split())


def clean_story(story: dict[str, Any]) -> dict[str, Any]:
    """A saved story with ids taken out of its sentences, so one saved before this existed reads the same."""
    for item in story.get("rounds") or []:
        for sentence in item.get("sentences") or []:
            sentence["text"] = plain_text(sentence["text"], sentence.get("event_ids") or [])
    return story


def validate_story(parsed: Any, events: list[dict[str, Any]], rounds_wanted: list[int]) -> dict[str, Any]:
    """Keep only sentences that cite real events of the rounds asked for. A round with no recorded non-quiet row is
    marked empty from the recording itself, never from the model's silence."""
    if not isinstance(parsed, dict):
        raise ValueError("the story reply was not an object")
    known = {e["event_id"]: e for e in events}
    given: dict[int, list[Any]] = {}
    for item in parsed.get("rounds") or []:
        if isinstance(item, dict) and isinstance(item.get("round"), int):
            given.setdefault(item["round"], []).extend(item.get("sentences") or [])
    with_events = {e["round"] for e in events}
    out, dropped = [], 0
    for number in rounds_wanted:
        kept = []
        for sentence in given.get(number, []):
            if not isinstance(sentence, dict):
                dropped += 1
                continue
            cited = [str(i) for i in sentence.get("event_ids") or []]
            real = [i for i in dict.fromkeys(cited) if i in known and known[i]["round"] == number][:6]
            text = plain_text(str(sentence.get("text") or "").strip()[:400], real)
            if text and real:
                kept.append({"text": text, "event_ids": real})
            else:
                dropped += 1
        out.append({"round": number, "sentences": kept[:3],
                    "recorded": number in with_events, "told": bool(kept)})
    return {"rounds": out, "dropped_sentences": dropped}


def tell_run(rounds: list[dict[str, Any]], *, people: list[dict[str, Any]] | None, world_sentence: str, model: str,
             trace_id: str, max_budget: float) -> tuple[dict[str, Any], list[Any]]:
    """The story of a run: one call, or one per slice of about 15 rounds when the events are too long for one.
    A slice that fails is reported as not told, never skipped silently."""
    from llm_client import call_llm, safe_json_loads

    events = story_events(rounds)
    all_rounds = [r.get("turn") for r in rounds if isinstance(r.get("turn"), int)]
    if not events:
        raise ValueError("this run recorded no events with their ids (it was made before the story existed), "
                         "so there is nothing to tell; run the world again")
    parts = slices(rounds, events, people)
    told: dict[int, dict[str, Any]] = {}
    results, failed_rounds, dropped = [], [], 0
    per_call = max_budget / len(parts)
    for index, block in enumerate(parts):
        wanted = [n for n in all_rounds if n in {e["round"] for e in block}] if len(parts) > 1 else all_rounds
        try:
            result = call_llm(model, story_prompt(people, block, world_sentence, wanted), task="world-substrate-run-story",
                              trace_id=trace_id, max_budget=per_call,
                              reasoning_effort="low", num_retries=1)
            results.append(result)
            checked = validate_story(safe_json_loads(result.content), block, wanted)
        except Exception:  # noqa: BLE001 - reported on the page as rounds not told
            failed_rounds.extend(wanted)
            continue
        dropped += checked["dropped_sentences"]
        told.update({r["round"]: r for r in checked["rounds"]})
    if not results:
        raise RuntimeError("the story could not be written for any round")
    return {"schema": STORY_SCHEMA, "rounds": [told[n] for n in all_rounds if n in told],
            "not_told_rounds": sorted(failed_rounds), "dropped_sentences": dropped,
            "events_read": len(events), "calls": len(parts)}, results
