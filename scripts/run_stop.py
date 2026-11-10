"""When a World Builder run stops by itself: a per-world setting and the check run after each round.

Implements: world-builder-page/a-run-stops-once-nothing-is-changing

Brian, 2026-11-10: "on d1. stop condition should be configurable." (open question Q12). A world carries
`run_stop`, chosen on the Create page and saved with the world like "Simulate as":

- `{"mode": "quiet", "quiet_rounds": N}`: stop once nothing is changing. The default for new worlds, N = 6
  (one operating-review period, spikes/any-scenario-2026-10/compile_spec.py:133 REVIEW_TICKS).
- `{"mode": "every_round"}`: always run every round asked for.

A world or run saved without the setting runs every round and records nothing new, so old worlds and runs replay
exactly as before.

"Nothing is changing" is judged on the fields people's moves can change (every `components.<c>.<f>` some rule's
move writes) plus each group decision's status. Fields only the world's own processes write are clocks (a weekly
meeting's countdown, the next operating review) and tick every round whether or not anything happens, so they do
not count.

- A world without a group decision stops after N rounds in a row in which no person's move changed anything and
  those fields stayed the same.
- A world with a group decision first needs every decision settled (deployed or rejected). After that only the
  net change counts: the run stops at round t when those fields at the end of round t are what they were at the
  end of round t - N, whatever was done and undone in between. In the Waltzman run of 2026-10-23
  (evidence/waltzman-tasks-slice2/c1r24) people kept putting a matter on the agenda and settling it again (Q3)
  after everything was resolved, so some move changed a count in almost every round and a strict rule would never
  have stopped it; the net rule stops it at round 30 of 46.

Two more conditions can be added to either mode; each is optional and the run stops at whichever fires first.
Brian, 2026-11-10: "i should be able to stop a world based on budget or number of rounds or a natural langue stopping
potin that the judge assesses once we build him".

- `"max_rounds": N` (1 to 500): stop once round N has been played (`reason: round_limit`). Unlike `round_cap`, which
  only says a request played every round it asked for (live play asks for one at a time), this is the visitor's own
  limit for the whole run.
- `"max_spend_usd": X` (0.01 to 100): stop once this run's AI spending reaches $X (`reason: budget`). The spending is
  the cost llm_client recorded for this run's own calls (`llm_client.get_cost(trace_id=...)`, the same number the
  daily budget ledger is settled with), carried across live play's one-round requests in `run_spent_usd`; never an
  estimate. It is checked before each round: a round already under way always finishes, so a run can go over its
  limit by up to one round's spending (one round's AI calls are themselves capped by the service's per-request
  allowance, `RUN_BUDGET`), and the run page line says so when it did.

The third condition Brian named, a stopping point written in plain words that the AI judge assesses after each
round, waits for the judge (docs/plans/ai_judge.md) and will plug in here as another optional key.

This is a run-loop stopping rule over recorded state, not engine capability (Decision 006).
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

DEFAULT_QUIET_ROUNDS = 6
MAX_QUIET_ROUNDS = 100
DEFAULT_RUN_STOP = {"mode": "quiet", "quiet_rounds": DEFAULT_QUIET_ROUNDS}
SETTLED = ("deployed", "rejected")
DECISION_STATUS = "components.group_decision.status"
MAX_ROUND_LIMIT = 500
MIN_SPEND_USD = 0.01
MAX_SPEND_USD = 100.0
LIMIT_KEYS = ("max_rounds", "max_spend_usd")


def parse_run_stop(value: Any, *, default: dict[str, Any] | None = None) -> dict[str, Any] | None:
    """The validated setting, or `default` when none was given (None: run every round, record nothing)."""
    if value is None:
        return None if default is None else dict(default)
    if not isinstance(value, dict):
        raise ValueError("run_stop must be an object")
    limits = _parse_limits(value)
    mode = value.get("mode")
    rest = set(value) - set(LIMIT_KEYS)
    if mode == "every_round" and rest == {"mode"}:
        return {"mode": "every_round", **limits}
    if mode == "quiet" and rest <= {"mode", "quiet_rounds"}:
        n = value.get("quiet_rounds", DEFAULT_QUIET_ROUNDS)
        if type(n) is not int or not 1 <= n <= MAX_QUIET_ROUNDS:
            raise ValueError(f"run_stop.quiet_rounds must be a whole number from 1 to {MAX_QUIET_ROUNDS}")
        return {"mode": "quiet", "quiet_rounds": n, **limits}
    raise ValueError('run_stop must be {"mode": "quiet", "quiet_rounds": N} or {"mode": "every_round"}, '
                     'optionally with "max_rounds" and "max_spend_usd"')


def _parse_limits(value: dict[str, Any]) -> dict[str, Any]:
    limits: dict[str, Any] = {}
    if value.get("max_rounds") is not None:
        n = value["max_rounds"]
        if type(n) is not int or not 1 <= n <= MAX_ROUND_LIMIT:
            raise ValueError(f"run_stop.max_rounds must be a whole number from 1 to {MAX_ROUND_LIMIT}")
        limits["max_rounds"] = n
    if value.get("max_spend_usd") is not None:
        x = value["max_spend_usd"]
        if type(x) not in (int, float) or x != x or not MIN_SPEND_USD <= x <= MAX_SPEND_USD:
            raise ValueError(f"run_stop.max_spend_usd must be a dollar amount from {MIN_SPEND_USD} to "
                             f"{MAX_SPEND_USD:g}")
        limits["max_spend_usd"] = round(float(x), 2)
    return limits


def limit_check(run_stop: dict[str, Any] | None, round_no: int, spent_usd: float | None) -> dict[str, Any] | None:
    """The stop record if this run's spending or round limit is reached after round `round_no`, else None.

    Spending is checked first: when both are reached in the same round, the money is the reason given."""
    if not run_stop:
        return None
    limit = run_stop.get("max_spend_usd")
    if limit is not None and spent_usd is not None and spent_usd >= limit:
        return budget(round_no, spent_usd, limit)
    n = run_stop.get("max_rounds")
    if n is not None and round_no >= n:
        return round_limit(round_no, n)
    return None


def round_limit(round_no: int, n: int) -> dict[str, Any]:
    return {"reason": "round_limit", "round": round_no, "max_rounds": n,
            "why": f"Stopped at round {round_no}: the limit of {n} round{'s' if n != 1 else ''} you set."}


def budget(round_no: int, spent_usd: float, limit: float) -> dict[str, Any]:
    why = f"Stopped at round {round_no}: this run had spent ${spent_usd:.2f} of its ${limit:.2f} limit."
    if spent_usd > limit:
        why += " A round already under way always finishes, so it went a little over."
    return {"reason": "budget", "round": round_no, "spent_usd": round(spent_usd, 6), "max_spend_usd": limit,
            "why": why}


def movable_fields(model: Any) -> frozenset[str]:
    """Every "<component>.<field>" some move writes, plus the group decision status."""
    fields = {DECISION_STATUS}
    for mechanic in model.mechanics:
        for path in mechanic.write_paths:
            parts = str(path).split(".")
            if len(parts) >= 5 and parts[0] == "entities" and parts[2] == "components":
                fields.add(".".join(parts[2:5]))
    return frozenset(fields)


def _entities(world: dict[str, Any]) -> dict[str, Any]:
    return world.get("entities") or {}


def state_key(world: dict[str, Any], fields: frozenset[str]) -> str:
    """A short fingerprint of the movable fields of a world's material dict (World.material_dict())."""
    picked: dict[str, Any] = {}
    for eid, entity in sorted(_entities(world).items()):
        for cname, comp in sorted(((entity or {}).get("components") or {}).items()):
            for fname, value in sorted((comp or {}).items()):
                if f"components.{cname}.{fname}" in fields:
                    picked[f"{eid}.{cname}.{fname}"] = value
    return hashlib.sha256(json.dumps(picked, sort_keys=True, default=str).encode()).hexdigest()[:16]


def decision_status(world: dict[str, Any]) -> str | None:
    """None when the world has no group decision; "settled:<status>" or "open:<status>" otherwise."""
    statuses = [((e or {}).get("components") or {}).get("group_decision", {}).get("status")
                for e in _entities(world).values()
                if "group_decision" in (((e or {}).get("components")) or {})]
    if not statuses:
        return None
    if all(s in SETTLED for s in statuses):
        return "settled:" + ",".join(sorted(set(statuses)))
    return "open:" + ",".join(sorted({str(s) for s in statuses}))


def history_entry(world: dict[str, Any], fields: frozenset[str], moved: bool) -> str:
    """One round's entry: the state key, marked "*" when some person's move changed something that round."""
    return state_key(world, fields) + ("*" if moved else "")


def check(run_stop: dict[str, Any] | None, history: list[str], decision: str | None,
          round_no: int) -> dict[str, Any] | None:
    """The stop record if this round ends the run, else None. `history` ends with this round's entry.

    Without a group decision, a quiet round is strict: no person's move changed anything and the state is what it
    was a round before. Once a group decision is settled, only the net change counts: the state is back to what
    it was N rounds before, whatever was done and undone in between."""
    if not run_stop or run_stop.get("mode") != "quiet":
        return None
    n = run_stop["quiet_rounds"]
    if len(history) < n + 1:
        return None
    window = history[-1 - n:]
    keys = [entry.rstrip("*") for entry in window]
    still = len(set(keys)) == 1 and not any(entry.endswith("*") for entry in window[1:])
    if decision is None:
        if not still:
            return None
    elif not decision.startswith("settled:") or keys[0] != keys[-1]:
        return None
    settled = None if decision is None else decision.split(":", 1)[1]
    return {"reason": "quiet_rounds", "round": round_no, "quiet_rounds": n, "decision": settled,
            "unchanged_every_round": still, "why": stop_line(round_no, n, settled, still)}


def stop_line(round_no: int, n: int, settled: str | None, still: bool) -> str:
    """One plain sentence for the run page."""
    rounds = f"{n} round{'s' if n != 1 else ''}"
    after = f" after the decision was {settled.replace(',', ' or ')}" if settled else ""
    if still:
        return f"Stopped at round {round_no}: nothing had changed for {rounds}{after}."
    return (f"Stopped at round {round_no}: nothing had changed for good for {rounds}{after} "
            f"(the moves made in them were undone again).")


def round_cap(round_no: int) -> dict[str, Any]:
    return {"reason": "round_cap", "round": round_no}


def finish_line(round_no: int) -> dict[str, Any]:
    return {"reason": "finish_line", "round": round_no}
