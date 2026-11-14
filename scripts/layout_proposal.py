#!/usr/bin/env python3
"""Ask a model to place a built world's places on a prepared room map, so a share link can show it as a room map.

Implements: scene-viewer/builder-proposes-layout
A second, optional step after the world's structure is built: one small call that returns a `layout` (see
`scene_layout.py`) or null when the world has no places to draw. The local validator is the judge; a layout that does
not pass (after one repair) is dropped and the world is built exactly as before. It never fails a build.
"""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from scripts.scene_layout import LayoutError, prepared_maps, validate_layout

DEFAULT_MODEL = "openrouter/openai/gpt-6-luna"
MAX_OUTPUT_TOKENS = 1500
MAX_BUDGET = 0.03


def _map_menu() -> dict[str, Any]:
    """The public maps, as slots and which slots touch (names only)."""
    return {name: {"slots": sorted(m["slots"]), "connected_slot_pairs": m["connections"]}
            for name, m in prepared_maps().items() if m.get("kind") == "generated"}


def _messages(bundle: dict[str, Any]) -> list[dict[str, str]]:
    info = bundle["actor_information"]
    by_id = {e["id"]: e for e in bundle.get("entities", [])}
    entities = [{"id": e["id"], "label": e["label"], "categories": by_id.get(e["id"], {}).get("categories", [])}
                for e in info["public_entities"]]
    return [
        {"role": "system", "content": (
            "You place the rooms of a small simulated world on a prepared room map. Return exactly one JSON object and no prose. "
            "If the world has fewer than two places that people move between, return {\"layout\": null}.")},
        {"role": "user", "content": json.dumps({
            "world": bundle["world"]["label"], "summary": info.get("public_summary", ""),
            "entities": entities, "people": sorted(info["actors"]),
            "maps": _map_menu(),
            "answer_shape": {"layout": {
                "version": 1, "map": "one of the map names above",
                "rooms": "{place entity id: slot}, one slot per place, only slots that map has; put the place most others connect to in the hub slot",
                "doors": ("{door id: {between: [place id, place id], halves: [door entity ids]}}: one per way between two places, between places whose slots "
                          "are a connected pair. If the world models doors, halves are the entity ids of that door's two sides; if people just "
                          "walk between the places, halves is []. Every place must be reachable from every other through these."),
                "people": "{person id from `people`: {start: place id}}"}},
            "rule": "Use public entity ids only. Choose the smaller map when the places fit.",
        }, indent=1)},
    ]


def propose_layout(bundle: dict[str, Any], *, model: str = DEFAULT_MODEL, trace_id: str, max_budget: float = MAX_BUDGET) -> dict[str, Any] | None:
    """The bundle with a validated `layout`, or None (no places to draw, or the model's layout did not validate)."""
    from llm_client import call_llm, safe_json_loads

    if not bundle.get("actor_information"):
        return None
    messages = _messages(bundle)
    for attempt in range(2):
        result = call_llm(model, messages, task="world-substrate-layout", trace_id=trace_id, max_budget=max_budget,
                          max_tokens=MAX_OUTPUT_TOKENS, reasoning_effort="low", num_retries=1)
        try:
            parsed = safe_json_loads(result.content)
            if not isinstance(parsed, dict) or "layout" not in parsed:
                raise LayoutError("reply must be an object with a layout")
            if parsed["layout"] is None:
                return None
            candidate = deepcopy(bundle)
            candidate["layout"] = parsed["layout"]
            validate_layout(candidate)
            return candidate
        except (LayoutError, ValueError, TypeError, KeyError) as error:
            if attempt:
                return None
            messages = [*messages, {"role": "assistant", "content": result.content},
                        {"role": "user", "content": f"The local validator rejected that layout: {type(error).__name__}: {error}. Return a corrected JSON object only."}]
    return None
