#!/usr/bin/env python3
"""Conversation helpers in front of natural-language world building.

Two small, bounded model calls that only ever produce a plain-English
description; neither touches structure or law:

- `clarify`: one turn of a dialogue that helps a visitor flesh out and clarify
  a rough idea. It returns a short reply, at most three questions with
  suggested answers, and the best description so far.
- `surprise_description`: an "I'm feeling lucky" scenario for a server-chosen
  theme, so variety does not depend on the model's own favourites.

The description then goes through `/generate-world` exactly like typed text.
"""
from __future__ import annotations

import json
import random
import uuid
from typing import Any

DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
DEFAULT_BUDGET = 0.02
MAX_OUTPUT_TOKENS = 1200
MAX_TURNS = 12
MAX_MESSAGE_CHARS = 2000
MAX_DESCRIPTION_CHARS = 2000

SCOPE = (
    "The simulator handles small, turn-based situations: 2 to 10 named things, a few people or machines who "
    "act, things they share, use or move, simple counts and stages, and a clear finish line. It cannot "
    "represent clocks or deadlines, probabilities, money, distances or feelings."
)

WORLD_KINDS = ("task", "ongoing", "open")
KIND_HINTS = {
    "task": "The visitor wants a task world: a job with a clear finish line.",
    "ongoing": "The visitor wants an ongoing world: work keeps arriving or things keep needing attention, with no final finish line.",
    "open": "The visitor wants an open world: no goal, residents with needs that keep changing, living on indefinitely.",
}


def _kind(world_kind: Any) -> str:
    kind = world_kind or "task"
    if kind not in WORLD_KINDS:
        raise ValueError(f"world_kind must be one of {list(WORLD_KINDS)}")
    return kind


THEMES = [
    "a harbour unloading a ship", "a school science fair", "a community garden", "a hospital ward night shift",
    "a pizza kitchen rush", "a bike repair shop", "a library returns desk", "a small farm at harvest",
    "a theatre before curtain-up", "a moving day", "a lighthouse keeper's supply run", "a beekeeping season",
    "a recycling sorting line", "a camping trip setting up", "a newsroom before deadline", "a toy workshop",
    "a fire station drill", "an animal shelter feeding time", "a robot warehouse", "a wedding cake bakery",
]


def _clean_text(value: Any, label: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value.strip()[:limit]


def _validate_turns(turns: Any) -> list[dict[str, str]]:
    if not isinstance(turns, list) or not turns:
        raise ValueError("messages must be a nonempty list")
    if len(turns) > MAX_TURNS:
        raise ValueError(f"the conversation is limited to {MAX_TURNS} messages; build or start over")
    out = []
    for turn in turns:
        if not isinstance(turn, dict) or turn.get("role") not in {"user", "assistant"}:
            raise ValueError("each message needs role user or assistant")
        out.append({"role": turn["role"], "content": _clean_text(turn.get("content"), "message", MAX_MESSAGE_CHARS)})
    if out[-1]["role"] != "user":
        raise ValueError("the last message must be from the visitor")
    return out


def validate_clarify_reply(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("reply must be an object")
    reply = _clean_text(value.get("reply"), "reply", 600)
    description = _clean_text(value.get("description"), "description", MAX_DESCRIPTION_CHARS)
    questions = value.get("questions") or []
    if not isinstance(questions, list):
        raise ValueError("questions must be a list")
    cleaned = []
    for q in questions[:3]:
        if not isinstance(q, dict):
            raise ValueError("each question must be an object")
        options = [str(o).strip()[:120] for o in (q.get("options") or []) if str(o).strip()][:4]
        cleaned.append({"question": _clean_text(q.get("question"), "question", 200), "options": options})
    return {"reply": reply, "questions": cleaned, "description": description, "ready": bool(value.get("ready"))}


def _call(messages: list[dict[str, str]], *, model: str, trace_id: str, max_budget: float, task: str) -> tuple[dict[str, Any], Any]:
    from llm_client import call_llm, safe_json_loads

    result = call_llm(
        model,
        messages,
        task=task,
        trace_id=trace_id,
        max_budget=max_budget,
        max_tokens=MAX_OUTPUT_TOKENS,
        reasoning_effort="low",
        num_retries=1,
    )
    parsed = safe_json_loads(result.content)
    if not isinstance(parsed, dict):
        raise ValueError("model returned a non-object reply")
    return parsed, result


def clarify(
    turns: Any,
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    world_kind: str = "task",
) -> tuple[dict[str, Any], Any]:
    conversation = _validate_turns(turns)
    kind = _kind(world_kind)
    system = (
        "You help a visitor describe a small world for a rule-based simulator, in plain friendly English. "
        + SCOPE
        + " " + KIND_HINTS[kind]
        + " Each turn: briefly reflect what you understood, then ask at most three short questions that would "
        "most change the simulation (who acts, what they share or use, what blocks what, what counts as "
        "finished), each with two to four short suggested answers the visitor can click; every suggested answer "
        "must be something the simulator can represent (no money, clocks, chance or distances). Do not ask about "
        "things the simulator cannot represent; if the visitor mentions them, say plainly they will be left out. "
        "Always also write the best complete description so far (two to four sentences, concrete names and "
        "counts). Set ready true when the description has actors, the things they use, and (for a task world) a "
        "finish line or (for ongoing and open worlds) what keeps changing by itself. "
        'Return only JSON: {"reply": str, "questions": [{"question": str, "options": [str]}], '
        '"description": str, "ready": bool}.'
    )
    parsed, result = _call(
        [{"role": "system", "content": system}, *conversation],
        model=model,
        trace_id=trace_id or f"world-builder-clarify-{uuid.uuid4().hex}",
        max_budget=max_budget,
        task="world-substrate-world-dialogue",
    )
    return validate_clarify_reply(parsed), result


def surprise_description(
    *,
    model: str = DEFAULT_MODEL,
    trace_id: str | None = None,
    max_budget: float = DEFAULT_BUDGET,
    rng: random.Random | None = None,
    world_kind: str = "task",
) -> tuple[dict[str, str], Any]:
    kind = _kind(world_kind)
    theme = (rng or random).choice(THEMES)
    system = (
        "Invent one small, concrete situation for a rule-based simulator. " + SCOPE + " Use the given theme, "
        "give the people or machines names, include one thing they must share or take turns with so that some "
        "attempts get refused. " + KIND_HINTS[kind] + " For a task world end with a clear finish line; for "
        "ongoing and open worlds say what keeps changing by itself. Two to three sentences. "
        'Return only JSON: {"description": str}.'
    )
    parsed, result = _call(
        [{"role": "system", "content": system}, {"role": "user", "content": json.dumps({"theme": theme})}],
        model=model,
        trace_id=trace_id or f"world-builder-surprise-{uuid.uuid4().hex}",
        max_budget=max_budget,
        task="world-substrate-world-surprise",
    )
    return {"theme": theme, "description": _clean_text(parsed.get("description"), "description", MAX_DESCRIPTION_CHARS)}, result
