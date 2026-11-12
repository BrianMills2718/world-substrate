"""Ruling to rule: install a judge's checked ruling as a rule of the running world (ai-judge plan, slice J3).

A ruling the judge confirmed already passed the World Builder's rules check and was test-run on a copy of the world
(`scripts/judge.py`, `scripts/consequence_report.py`). Here it becomes a rule, by the world's setting
"Judge rulings during a run":

- **create** (default, "Approved by Create"): the rule is installed into the running engine at once. Installing is
  the same step the any-scenario spike's mid-run game master used (`spikes/any-scenario-2026-10/midrun.py`, `_install`:
  register the compiled action rule in the running engine's registry); here the rule first goes through the rules
  check again against the world as it is now, and the world's recorded rule versions follow it.
- **wait** ("Wait for my approval"): the rule is held and installs nothing; each attempt that needs it waits as
  pending. Approve installs it and settles each waiting attempt through it; Reject refuses each, naming the ruling.

The world's own bundle and rules stay as the visitor approved them (a shared run is identified by them). Installed
rules are run state: the list of rulings travels with the run, sealed by the server, and the effective world is the
original plus every installed ruling's rule (`effective`).

Nothing here writes an outcome. A rule is installed, and then the engine alone commits or refuses a move under it.

Implements: ai-judge/a-checked-ruling-is-installed-as-a-rule-during-the-run
Implements: ai-judge/the-world-s-setting-can-hold-a-ruling-until-the-owner-approves-it
Implements: ai-judge/a-ruling-the-language-cannot-express-is-refused-and-listed-as-a-language-gap
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts import consequence_report  # noqa: E402

CREATE, WAIT = "create", "wait"
MODES = (CREATE, WAIT)
DEFAULT_MODE = CREATE
INSTALLED, HELD, REJECTED, LANGUAGE_GAP, WITHDRAWN = "installed", "held", "rejected", "language_gap", "withdrawn"
NO_RULE = "no rule could express this"
MAX_RULINGS = 60
MAX_DECISIONS = 20
MAX_LISTED_ATTEMPTS = 40


def parse_mode(value: Any) -> str:
    """The world's setting: absent means the default; anything else but a known mode is an error."""
    if value is None or value == "":
        return DEFAULT_MODE
    if value not in MODES:
        raise ValueError(f"judge_rulings must be one of {list(MODES)}")
    return str(value)


def parse_rulings(value: Any) -> list[dict[str, Any]]:
    """The run's rulings as the page sends them back (the server's seal is checked by the caller)."""
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > MAX_RULINGS or not all(
            isinstance(r, dict) and isinstance(r.get("id"), str) and r.get("status") in
            (INSTALLED, HELD, REJECTED, LANGUAGE_GAP, WITHDRAWN) for r in value):
        raise ValueError(f"rulings must be a list of up to {MAX_RULINGS} rulings the server sent")
    return value


def parse_decisions(value: Any) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, list) or len(value) > MAX_DECISIONS or not all(
            isinstance(d, dict) and isinstance(d.get("id"), str) and d.get("decision") in ("approve", "reject")
            for d in value):
        raise ValueError(f"decisions must be a list of up to {MAX_DECISIONS} approve or reject answers")
    return [{"id": d["id"], "decision": d["decision"]} for d in value]


def kind_of(rule: dict[str, Any]) -> str:
    return str((rule.get("action") or {}).get("kind") or (rule.get("mechanic") or {}).get("action_kind") or "")


def effective(bundle: dict[str, Any], causal: dict[str, Any],
              rulings: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    """The world's bundle and rules with every installed ruling's rule added, in the order they were installed."""
    out_bundle, out_causal = bundle, causal
    for ruling in rulings:
        if ruling.get("status") == INSTALLED and ruling.get("rule"):
            out_bundle, out_causal = consequence_report.with_rule(out_bundle, out_causal, ruling["rule"])
    return out_bundle, out_causal


class Rulebook:
    """The rulings of one run, and what to do with a new one. `bundle` and `causal` are the effective world."""

    def __init__(self, bundle: dict[str, Any], causal: dict[str, Any], rulings: list[dict[str, Any]] | None,
                 mode: str):
        self.rulings = deepcopy(rulings or [])
        self.mode = parse_mode(mode)
        self.bundle, self.causal = effective(bundle, causal, self.rulings)

    # -- reading
    def get(self, ruling_id: str) -> dict[str, Any] | None:
        return next((r for r in self.rulings if r["id"] == ruling_id), None)

    def covering(self, kind: str) -> dict[str, Any] | None:
        """The ruling, held or rejected, whose rule is of this kind: an attempt read as that kind waits on it or is
        refused by it. (An installed one is simply a rule of the engine and needs no help here.)"""
        return next((r for r in self.rulings if r.get("kind") == kind and r["status"] in (HELD, REJECTED)), None)

    def has_kind(self, kind: str) -> dict[str, Any] | None:
        return next((r for r in self.rulings if r.get("kind") == kind and r["status"] in (INSTALLED, HELD, REJECTED)),
                    None)

    def waiting_rules(self) -> list[dict[str, Any]]:
        """The rules of held and rejected rulings, so the attempt reader can read a later identical attempt as them."""
        return [r["rule"] for r in self.rulings if r["status"] in (HELD, REJECTED) and r.get("rule")]

    def shadow(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """The effective world with the held and rejected rules added too (for reading attempts, never for running)."""
        bundle, causal = self.bundle, self.causal
        for rule in self.waiting_rules():
            bundle, causal = consequence_report.with_rule(bundle, causal, rule)
        return bundle, causal

    # -- writing
    def new(self, *, status: str, round_no: int, actor: str, attempt: str, event_id: str | None,
            record: dict[str, Any]) -> dict[str, Any]:
        """A ruling entry from the judge's record."""
        rule = record.get("rule")
        entry: dict[str, Any] = {
            "id": f"R{len(self.rulings) + 1}", "status": status, "decision": None,
            "origin": {"round": round_no, "actor": actor, "attempt": attempt, "event_id": event_id},
            "kind": kind_of(rule) if rule else None,
            "description": ((rule or {}).get("action") or {}).get("description"),
            "ruling": record.get("ruling") or "", "why": record.get("why") or "",
            "whose_choice": record.get("whose_choice"),
            "rule": deepcopy(rule), "move": deepcopy(record.get("move")),
            "installed_round": None, "attempts": [],
        }
        if status == LANGUAGE_GAP:
            entry["error"] = next((t["rules_check"].get("error") for t in reversed(record.get("tests") or [])
                                   if not (t.get("rules_check") or {}).get("ok")), None)
        self.rulings.append(entry)
        return entry

    def install(self, engine: Any, ruling: dict[str, Any], round_no: int) -> dict[str, Any]:
        """Put a ruling's rule through the rules check against the world as it is now and register it in the running
        engine. Returns {"ok": True} or {"ok": False, "error": ...}; on success the effective world is updated."""
        rule = ruling.get("rule")
        if not rule:
            return {"ok": False, "error": "the ruling has no rule"}
        kind = kind_of(rule)
        if kind in engine.registry.action_kinds():
            return {"ok": False, "error": f"a rule for {kind} is already installed"}
        try:
            bundle2, causal2 = consequence_report.with_rule(self.bundle, self.causal, rule)
        except ValueError as error:
            return {"ok": False, "error": str(error)}
        check, trial = consequence_report.rules_check(bundle2, causal2)
        if trial is None:
            return {"ok": False, "error": check.get("error")}
        compiled = trial.registry.action(kind)
        if compiled is None:
            return {"ok": False, "error": f"the rules check built no rule for {kind}"}
        engine.registry.register_action(compiled)
        engine.world.rule_versions = engine.registry.versions()
        self.bundle, self.causal = bundle2, causal2
        ruling["status"], ruling["installed_round"] = INSTALLED, round_no
        return {"ok": True}

    def attempt(self, ruling: dict[str, Any], *, actor: str, attempt: str, event_id: str | None, round_no: int,
                state: str, move: dict[str, Any] | None, by_rule: bool = False) -> dict[str, Any]:
        """List an attempt under the ruling it waits on, was settled by, or (by_rule) was later decided by. The list is
        capped, since it travels with every round; `attempts_omitted` counts what no longer fits."""
        row = {"actor": actor, "attempt": attempt, "event_id": event_id, "round": round_no, "state": state,
               "move": deepcopy(move), **({"by_rule": True} if by_rule else {})}
        if len(ruling["attempts"]) >= MAX_LISTED_ATTEMPTS and by_rule:
            ruling["attempts_omitted"] = ruling.get("attempts_omitted", 0) + 1
        else:
            ruling["attempts"].append(row)
        return row

    def public(self) -> list[dict[str, Any]]:
        """Each ruling as the run page lists it (no rule bodies: the judge panel shows the rule)."""
        keep = ("id", "status", "decision", "origin", "kind", "description", "ruling", "why", "whose_choice",
                "installed_round", "error", "attempts_omitted")
        out = []
        for r in self.rulings:
            row = {k: deepcopy(r.get(k)) for k in keep if r.get(k) is not None}
            row["attempts"] = [{k: a[k] for k in ("actor", "attempt", "event_id", "round", "state", "by_rule") if k in a}
                               for a in r.get("attempts") or []]
            out.append(row)
        return out


__all__ = ["CREATE", "DEFAULT_MODE", "HELD", "INSTALLED", "LANGUAGE_GAP", "MODES", "NO_RULE", "REJECTED", "Rulebook",
           "WAIT", "WITHDRAWN", "effective", "kind_of", "parse_decisions", "parse_mode", "parse_rulings"]
