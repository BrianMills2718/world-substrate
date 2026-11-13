"""The consequence report: what the engine works out for an attempt no rule covers (ai-judge plan, slice J1).

An attempt no installed rule covers commits no event, and knock-on effects start only from a committed event
(`Engine._settle`), so the report comes in two passes (docs/plans/ai_judge.md, Canonical example; ledger Q78):

- **Pass 1, before any rule exists** (`pass_one`): `Engine.discover` for the person acting and for each person the
  attempt names, keeping every available and blocked move with its checks, plus the current values of the person
  acting and of every person and thing the attempt names. `discover` lists only the moves of the person asked, so an
  officer's "sign release: blocked, the crate is inspected (false)" appears on the officer's page, never the trader's.
  The names come from the interpreter's reading (`world_substrate.attempt`, `names`).
- **Pass 2, a proposed rule** (`pass_two`): the rule, written in the declaration language every World Builder rule
  uses (`action-mechanic/v0`), goes through the same rules check a build's rules go through (`validate_bundle`, the
  causal compiler `CausalModel.from_dict`, the mechanic installer: `build_engine`), and is then test-run on a copy of
  the world as it is now, with the attempt submitted as the rule's typed move. The report gives the net changes, the
  blockers, the chain's length and where it stopped, and keeps the full chain for the run record. `summary` drops the
  full chain: what a judge reads (plan, "LLM call boundary and cost": a 5,000-step chain is about 500,000 tokens).

Nothing here calls a model or changes the real world: pass 1 reads it, pass 2 runs on a copy.

Implements: ai-judge/pass-1-reports-what-installed-rules-compute-for-the-people-an-attempt-involves
Implements: ai-judge/pass-2-test-runs-a-proposed-rule-on-a-copy-of-the-world
Implements: ai-judge/a-proposed-rule-goes-through-the-world-builder-s-rules-check
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from world_substrate.engine import Engine  # noqa: E402

CONTROLLER = "judge:test-run"
# Identity and the engine's own bookkeeping (which event last changed a thing) are not world state a rule changes.
_IDENTITY = {"entity_id", "label", "category_ids", "source_pack_id", "source_entity_id", "last_cause_event_id"}


def _row(row: dict[str, Any]) -> dict[str, Any]:
    """One discover row with what the judge needs: the move, every check with its values, and why it is blocked."""
    out = {"action_id": row["action_id"], "action": dict(row["action"]), "checks": [dict(c) for c in row["checks"]]}
    if "reason" in row:
        out["reason"] = row["reason"]
    return out


def _values(entity: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": entity.get("label"),
        "categories": list(entity.get("category_ids") or []),
        "location": (entity.get("location") or {}).get("location_id"),
        "components": deepcopy(entity.get("components") or {}),
    }


def _named(engine: Engine, actor: str, named: Iterable[str]) -> list[str]:
    out: list[str] = []
    for eid in named:
        if eid in engine.world.entities and eid != actor and eid not in out:
            out.append(eid)
    return out


def pass_one(engine: Engine, actor: str, named: Iterable[str], *, people: Iterable[str]) -> dict[str, Any]:
    """What the engine computes for an attempt with no new rule: the moves of the person acting and of each person
    named (`people` says who can act), and the current values of the person acting and everything named."""
    names = _named(engine, actor, named)
    people = set(people)
    entities = engine.world.material_dict()["entities"]
    moves: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for person in [actor] + [n for n in names if n in people]:
        page = engine.discover(person)
        moves[person] = {"available": [_row(r) for r in page.get("available") or []],
                         "blocked": [_row(r) for r in page.get("blocked") or []]}
    return {
        "actor": actor,
        "named": names,
        "moves": moves,
        "values": {eid: _values(entities[eid]) for eid in [actor] + names},
    }


# Implements: native-coordination/independent-generated-concern-procedure
_INDEPENDENT_COMPONENTS = frozenset({"information", "delivery", "technical_condition", "validation_decision", "actor_position", "technical_role", "claim_provenance", "report_log"})


class IndependentRuleAuthorityError(ValueError):
    """A proposed rule attempted to replace a compiled procedural authority."""


def _independent(bundle: dict[str, Any]) -> bool:
    return any("validation_decision" in e.get("components", {}) for e in bundle.get("entities", []))


def _protected_writer(declaration: dict[str, Any]) -> bool:
    return any(str(effect.get("path", "")).split(".")[1:2] and
               str(effect.get("path", "")).split(".")[1] in _INDEPENDENT_COMPONENTS
               for effect in declaration.get("effects", []))


def _check_independent_writers(bundle: dict[str, Any], causal: dict[str, Any]) -> None:
    """Raw candidate validation accepts only exact compiler-owned procedural writers, never names alone."""
    if not _independent(bundle):
        return
    from types import SimpleNamespace
    from scripts.people_world import _pipeline
    compiler, _ = _pipeline()
    entities = bundle["entities"]
    decision = next(e for e in entities if "validation_decision" in e.get("components", {}))
    state = decision["components"]["validation_decision"]
    condition = next(e for e in entities if e["id"] == state["condition_id"])["components"]["technical_condition"]
    roles = [e["components"]["technical_role"] for e in entities if "technical_role" in e.get("components", {})]
    procedure = SimpleNamespace(decision_id=decision["id"], question=decision["label"],
        required_actor_ids=[e["components"]["actor_position"]["holder_id"] for e in entities if "actor_position" in e.get("components", {})],
        validator_ids=[r["holder_id"] for r in roles if r["validator"]],
        repairer_ids=[r["holder_id"] for r in roles if r["repairer"]],
        condition_initially_passing=condition["passing"], initial_validation=state["validation"])
    _, mechanics, processes = compiler._independent_family(SimpleNamespace(independent_decision=procedure), [], [])
    import json
    mechanics = [json.loads(compiler.COORDINATION_CAUSAL.read_text())["mechanics"][0], *mechanics]
    for declarations, allowed in ((causal.get("mechanics", []), mechanics), (causal.get("processes", []), processes)):
        for declaration in declarations:
            if _protected_writer(declaration) and declaration not in allowed:
                raise IndependentRuleAuthorityError("independent procedural state may only be written by its exact compiled rules")


def with_rule(bundle: dict[str, Any], causal_value: dict[str, Any],
              rule: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Copies of the world's bundle and rules with the proposed rule added: its action to the bundle's actions and its
    mechanic to the rules, the same two places a build writes every rule."""
    if _independent(bundle) and _protected_writer(rule.get("mechanic") or {}):
        raise IndependentRuleAuthorityError("a proposed rule cannot write independent procedural state; use its actor-owned installed actions")
    bundle2, causal2 = deepcopy(bundle), deepcopy(causal_value)
    bundle2.setdefault("actions", []).append(deepcopy(rule.get("action")))
    causal2.setdefault("mechanics", []).append(deepcopy(rule.get("mechanic")))
    return bundle2, causal2


def rules_check(bundle: dict[str, Any], causal_value: dict[str, Any]) -> tuple[dict[str, Any], Engine | None]:
    """The World Builder's rules check on a bundle and rules: validation, the causal compiler and the installer.
    Returns ({"ok": True}, engine) or ({"ok": False, "error": ...}, None)."""
    from scripts.run_authored_world import build_engine

    try:
        _check_independent_writers(bundle, causal_value)
        engine, _, _ = build_engine(bundle, causal_value, reaction_limit=None)
    except Exception as error:  # every rejection is data for the judge, whatever raised it
        return {"ok": False, "error": f"{type(error).__name__}: {error}"}, None
    return {"ok": True}, engine


def _flat(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict) and value:
        out: dict[str, Any] = {}
        for key, inner in value.items():
            out.update(_flat(inner, f"{prefix}.{key}" if prefix else str(key)))
        return out
    return {prefix: value}


def net_changes(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    """Every entity field whose value differs between two material states, sorted by entity and path."""
    rows = []
    for eid in sorted(set(before) | set(after)):
        old = _flat({k: v for k, v in (before.get(eid) or {}).items() if k not in _IDENTITY})
        new = _flat({k: v for k, v in (after.get(eid) or {}).items() if k not in _IDENTITY})
        for path in sorted(set(old) | set(new)):
            if old.get(path) != new.get(path):
                rows.append({"entity": eid, "path": path, "before": old.get(path), "after": new.get(path)})
    return rows


def _failed(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"check": c.get("label"), "actual": c.get("actual"), "required": c.get("required")}
            for c in checks if c.get("ok") is False and c.get("label") != "Base revision is current"]


def _copy(engine: Engine, trial: Engine) -> Engine:
    """The real world as it is now, under the trial registry (the installed rules plus the proposed one)."""
    world = deepcopy(engine.world)
    world.rule_versions = trial.registry.versions()
    return Engine(world, trial.registry, reaction_limit=None)


def pass_two(bundle: dict[str, Any], causal_value: dict[str, Any], engine: Engine, rule: dict[str, Any],
             move: dict[str, Any]) -> dict[str, Any]:
    """Rules-check a proposed rule, then test-run `move` (the attempt as the rule's typed move: actor, kind, fields) on
    a copy of `engine`'s world with the rule installed. The real world, bundle and rules are left unchanged."""
    try:
        bundle2, causal2 = with_rule(bundle, causal_value, rule)
    except IndependentRuleAuthorityError as error:
        return {"rules_check": {"ok": False, "error": f"IndependentRuleAuthorityError: {error}"}, "test_run": None}
    check, trial = rules_check(bundle2, causal2)
    if trial is None:
        return {"rules_check": check, "test_run": None}
    copy = _copy(engine, trial)
    start = copy.world.material_dict()["entities"]
    from_revision = copy.world.revision
    outcome = copy.submit({**move, "base_revision": from_revision, "controller": CONTROLLER})
    event = outcome.get("event") or (outcome.get("events") or [{}])[0]
    reactions = list(outcome.get("reactions") or [])
    chain_length = sum(len(r.get("reaction_steps") or []) for r in reactions)
    blocked = [dict(b) for b in outcome.get("blocked_reactions") or []]
    if outcome["status"] != "accepted":
        failed = _failed(event.get("checks") or [])
        check_row = outcome.get("check")
        if not failed and isinstance(check_row, dict):  # a law breach or a refused moment names one check
            failed = _failed([check_row])
        blocker = {"rule_id": event.get("rule_id") or move.get("kind"), "it": move.get("actor"),
                   "after": None, "failed": failed}
        stop = {"kind": "law_breach" if outcome["status"] == "law_breach" else "refused", "status": outcome["status"],
                "after_step": 0, "failed": failed, "blocker": blocker}
        blockers = [blocker]
    elif blocked:
        first = blocked[0]
        steps = [s["it"] for r in reactions for s in r.get("reaction_steps") or []]
        after_event = next((r for r in reactions if r.get("event_id") == first.get("after")), None)
        after_step = (max(steps.index(s["it"]) for s in after_event["reaction_steps"]) + 1) if after_event else 0
        failed = [{"check": f.get("label"), "actual": f.get("actual"), "required": f.get("required")}
                  for f in first.get("failed") or []]
        stop = {"kind": "blocked", "after_step": after_step, "rule_id": first.get("rule_id"), "it": first.get("it"),
                "failed": failed, "blocker": first}
        blockers = blocked
    else:
        stop = {"kind": "settled", "after_step": chain_length}
        blockers = []
    return {
        "rules_check": check,
        "test_run": {
            "move": {k: v for k, v in move.items() if k not in {"base_revision", "controller"}},
            "from_revision": from_revision,
            "status": outcome["status"],
            "net_changes": net_changes(start, copy.world.material_dict()["entities"]),
            "blockers": blockers,
            "chain_length": chain_length,
            "stopping_point": stop,
            "chain": [event] + reactions if event else reactions,
        },
    }


GROUP_OVER = 40  # more net changes than this are read grouped (a 5,000-step chain changes 5,000 fields)


def grouped(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Net changes grouped: the fields that went from the same value to the same value on the same things become
    one row naming the things, the fields and how many changes it stands for, in the order changes first appear."""
    by_change: dict[tuple[str, str], tuple[Any, Any, dict[str, list[str]]]] = {}
    for row in rows:
        key = (repr(row["before"]), repr(row["after"]))
        by_change.setdefault(key, (row["before"], row["after"], {}))[2].setdefault(row["path"], []).append(row["entity"])
    out: list[dict[str, Any]] = []
    for before, after, paths in by_change.values():
        by_things: dict[tuple[str, ...], list[str]] = {}
        for path, things in paths.items():
            by_things.setdefault(tuple(things), []).append(path)
        for things, fields in by_things.items():
            out.append({"things": list(things), "fields": fields, "before": before, "after": after,
                        "changes": len(things) * len(fields)})
    return out


def summary(report: dict[str, Any]) -> dict[str, Any]:
    """The report without the full chain: what the judge reads. The chain stays in the run record. More than
    GROUP_OVER net changes are given grouped (`grouped`), with their count."""
    out = deepcopy(report)
    run = out.get("test_run")
    if isinstance(run, dict):
        run.pop("chain", None)
        changes = run.get("net_changes") or []
        if len(changes) > GROUP_OVER:
            run["net_changes"] = grouped(changes)
            run["net_changes_grouped"] = True
            run["net_change_count"] = len(changes)
    return out


__all__ = ["grouped", "net_changes", "pass_one", "pass_two", "rules_check", "summary", "with_rule"]
