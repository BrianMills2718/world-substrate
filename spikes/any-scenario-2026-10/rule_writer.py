#!/usr/bin/env python3
"""Single-rule writer (Decision 007 layer 3, also used for layer 1 repairs).

Given the current world (bundle + causal model) and one stated problem (a check
finding, or a resident attempt no rule covers), an LLM proposes ONE rule change
in World Substrate's rule language: replace an action mechanic, add or replace a
process, or add a new action (signature + mechanic). The change is merged into a
copy, compiled by the ordinary local compiler (build_engine), and returned; the
caller decides keep-or-revert from the checks. The LLM never writes code and
never mutates state; only the Engine commits.

Method borrowed from WALL-E 2.0 / Code World Models: propose -> compile -> test ->
keep or revert, one rule at a time.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.generate_causal_model import (  # noqa: E402
    DEFAULT_MODEL,
    _context,
    _mechanic_schema,
    _process_schema,
)
from scripts.run_authored_world import build_engine  # noqa: E402

CHANGES = ("replace_mechanic", "add_process", "replace_process", "add_action")


def _contract(bundle: dict[str, Any]) -> dict[str, Any]:
    return {
        "changes": ("list of 1 to 3 rule changes applied together, each an object with the fields below; use more "
                    "than one only when a single change cannot fix the problem without breaking something else"),
        "change": f"one of {list(CHANGES)}",
        "target_id": "mechanic_id or process_id being replaced (null for add_*)",
        "action_signature": ("for add_action only: {kind (lowercase-slug), description, fields: [{name, type in "
                             "string|integer|number|boolean|entity_ref}]}"),
        "rule": "the full mechanic (for replace_mechanic/add_action) or process (for add_/replace_process)",
        "mechanic_schema_examples": [_mechanic_schema(a) for a in (bundle.get("actions") or [])[:1]],
        "process_schema": _process_schema(),
        "why": "one sentence: how this change fixes the stated problem",
    }


def propose_rule(bundle: dict[str, Any], causal: dict[str, Any], problem: str, *, trace_id: str,
                 max_budget: float = 0.20, guidance: str = "", model: str = DEFAULT_MODEL,
                 model_justification: str | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return (new_bundle, new_causal, record). Raises ValueError if no compilable change is produced."""
    from llm_client import call_llm, safe_json_loads

    context = _context(bundle)
    context["current_mechanics"] = causal.get("mechanics", [])
    context["current_processes"] = causal.get("processes", [])
    context["problem"] = problem
    context["contract"] = _contract(bundle)
    if guidance:
        context["author_guidance"] = guidance
    messages = [
        {"role": "system", "content": (
            "You repair or extend a governed world model with the fewest rule changes that fix the stated problem "
            "(at most 3, applied together). Return one JSON object {changes: [...], why} matching contract, no "
            "prose. Keep every other rule as it is. Copy state paths exactly from "
            "allowed_state_paths. You are not writing code; the local compiler is the authority.")},
        {"role": "user", "content": json.dumps(context, indent=1, sort_keys=True)},
    ]
    last_error: Exception | None = None
    total_cost = 0.0
    for attempt in range(2):
        result = call_llm(model, messages, task="world-substrate-rule-writer", trace_id=trace_id,
                          max_budget=max_budget, reasoning_effort="medium", num_retries=1,
                          **({"model_justification": model_justification} if model_justification else {}))
        total_cost += float(getattr(result, "cost", 0.0) or 0.0)
        try:
            proposal = safe_json_loads(result.content)
            changes = proposal.get("changes") if isinstance(proposal, dict) and "changes" in proposal else [proposal]
            if not isinstance(changes, list) or not 1 <= len(changes) <= 3:
                raise ValueError("changes must be a list of 1 to 3 rule changes")
            new_bundle, new_causal = bundle, causal
            for change in changes:
                new_bundle, new_causal = apply_change(new_bundle, new_causal, change)
            proposal = {"changes": changes, "why": proposal.get("why"),
                        "change": "+".join(str(c.get("change")) for c in changes),
                        "target_id": ",".join(str(c.get("target_id")) for c in changes)}
            build_engine(new_bundle, new_causal)  # compile + install, raises on rejection
            return new_bundle, new_causal, {"proposal": proposal, "trace_id": trace_id, "cost": total_cost,
                                            "compile_attempts": attempt + 1}
        except (ValueError, TypeError, KeyError) as error:
            last_error = error
            messages += [{"role": "assistant", "content": result.content},
                         {"role": "user", "content": f"The local compiler rejected that change: {type(error).__name__}: "
                                                     f"{error}. Return a corrected JSON object only."}]
    raise ValueError(f"rule writer produced no compilable change: {last_error}")


def apply_change(bundle: dict[str, Any], causal: dict[str, Any], proposal: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(proposal, dict) or proposal.get("change") not in CHANGES:
        raise ValueError(f"change must be one of {CHANGES}")
    b, c = deepcopy(bundle), deepcopy(causal)
    c.pop("review", None)
    rule = proposal.get("rule")
    if not isinstance(rule, dict):
        raise ValueError("rule must be an object")
    change, target = proposal["change"], proposal.get("target_id")
    if change == "replace_mechanic":
        idx = [i for i, m in enumerate(c["mechanics"]) if m.get("mechanic_id") == target]
        if not idx:
            raise ValueError(f"no mechanic {target!r} to replace")
        c["mechanics"][idx[0]] = rule
    elif change == "add_process":
        c.setdefault("processes", []).append(rule)
    elif change == "replace_process":
        idx = [i for i, p in enumerate(c.get("processes", [])) if p.get("process_id") == target]
        if not idx:
            raise ValueError(f"no process {target!r} to replace")
        c["processes"][idx[0]] = rule
    elif change == "add_action":
        sig = proposal.get("action_signature")
        if not isinstance(sig, dict) or not sig.get("kind"):
            raise ValueError("add_action needs action_signature with kind")
        if any(a["kind"] == sig["kind"] for a in b.get("actions", [])):
            raise ValueError(f"action kind {sig['kind']!r} already exists")
        b.setdefault("actions", []).append(sig)
        c["mechanics"].append(rule)
    return b, c
