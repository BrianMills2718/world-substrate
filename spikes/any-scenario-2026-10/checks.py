#!/usr/bin/env python3
"""Layer 1 checks (Decision 007) on a compiled world model, by simulation, not by reading code.

Established check categories, applied generically to any bundle + causal model:
- extreme conditions (system dynamics, Forrester & Senge 1980; Sterman ch. 21): set each depletable
  stock to zero and run; if every run is identical to the baseline, the stock running out has no
  consequence -> a rule is missing;
- boundedness / conservation (Petri-net style): no stock may become negative under any sequence
  of offered actions;
- liveness: every rule fires in at least one random run;
- deadlock: a run reaches a state where nobody can act and nothing is due, before the terminal;
- reachability: the terminal predicate is reached in at least one random run;
- random-action testing drives all of the above (seeded, bounded).

Every run uses the ordinary Engine (discover/submit/advance); nothing is evaluated outside it.
Output: a findings list with per-check counts; exit 1 if any blocking finding.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.run_authored_world import build_engine  # noqa: E402
from world_substrate.mechanisms.time import ClockAdvanceProcess  # noqa: E402

CLOCK = ClockAdvanceProcess.rule_id


def numeric_stocks(bundle: dict[str, Any]) -> list[tuple[str, str, str]]:
    """(entity_id, component, field) for every numeric field."""
    out = []
    for e in bundle["entities"]:
        for comp, fields in (e.get("components") or {}).items():
            if isinstance(fields, dict):
                for k, v in fields.items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        out.append((e["id"], comp, k))
    return out


def depletable(bundle: dict[str, Any], causal: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Stocks that some rule subtracts from: the ones whose running out must matter."""
    subtracted = set()
    for rule in [*causal.get("mechanics", []), *causal.get("processes", [])]:
        for eff in rule.get("effects", []):
            if eff.get("op") == "subtract":
                subtracted.add(eff.get("path", "").removeprefix("components."))
    return [s for s in numeric_stocks(bundle) if f"{s[1]}.{s[2]}" in subtracted]


def _changes(event: dict[str, Any]) -> str:
    rows = [c for c in event.get("changes", []) if ".components." in c["path"]]
    return "; ".join(f"{c['path'].split('entities.', 1)[-1].replace('.components.', '.')} {c['before']}->{c['after']}" for c in rows)


def _dead_end(engine: Any, actors: list[str], model: Any, action: dict[str, Any]) -> bool:
    """One-step lookahead on a copy: does this action leave nobody able to act and nothing due?"""
    probe = deepcopy(engine)
    probe.submit(dict(action, controller="checks-lookahead"))
    adv = probe.advance(1)
    if model.terminal is not None and model.terminal.reached(probe.world):
        return False
    if [e for e in adv["events"] if e["rule_id"] != CLOCK]:
        return False
    return not any(probe.discover(a)["available"] for a in actors)


def simulate(bundle: dict[str, Any], causal: dict[str, Any], *, seed: int, ticks: int,
             override: tuple[str, str, str, Any] | None = None, guided: bool = False,
             prefer_kind: str | None = None) -> dict[str, Any]:
    b = deepcopy(bundle)
    if override is not None:
        eid, comp, field, value = override
        for e in b["entities"]:
            if e["id"] == eid:
                e["components"][comp][field] = value
    engine, model, _ = build_engine(b, causal)
    engine.registry.register_process(ClockAdvanceProcess())
    rng = random.Random(seed)
    actors = sorted(e["id"] for e in b["entities"] if "actor" in e.get("categories", []))
    fired: set[str] = set()
    log: list[str] = []
    negatives: list[dict[str, Any]] = []
    trajectory: list[Any] = []
    deadlock_at = None
    blocked: list[str] = []
    in_progress = in_progress_values(causal)
    since: dict[tuple[str, str], tuple[Any, int]] = {}
    stuck: list[str] = []
    reached = False
    for _ in range(ticks):
        acted = False
        for a in actors:
            offered = engine.discover(a)["available"]
            if guided:  # lookahead on at most 4 sampled candidates: copying the world per action is the cost
                sample = rng.sample(offered, min(4, len(offered)))
                offered = [r for r in sample if not _dead_end(engine, actors, model, r["action"])]
            preferred = [r for r in offered if prefer_kind and r["action"]["kind"] == prefer_kind]
            if preferred:  # repeated-action test: keep doing this kind whenever it is offered
                row = preferred[0]
                out = engine.submit(dict(row["action"], controller=f"checks-repeat-{prefer_kind}"))
                if out["status"] == "accepted":
                    fired.add(out["event"]["rule_id"])
                    acted = True
                    log.append(f"t{engine.world.tick} {a} did {out['event']['rule_id']}: " + _changes(out["event"]))
                continue
            if offered and rng.random() < 0.8:
                row = rng.choice(offered)
                out = engine.submit(dict(row["action"], controller=f"checks-seed-{seed}"))
                if out["status"] == "accepted":
                    fired.add(out["event"]["rule_id"])
                    acted = True
                    log.append(f"t{engine.world.tick} {a} did {out['event']['rule_id']}: " + _changes(out["event"]))
        adv = engine.advance(1)
        material = [e for e in adv["events"] if e["rule_id"] != CLOCK]
        fired.update(e["rule_id"] for e in material)
        log += [f"t{engine.world.tick} process {e['rule_id']}: " + _changes(e) for e in material]
        for eid, comp, field in numeric_stocks(b):
            value = (engine.world.entities[eid].as_dict().get("components") or {}).get(comp, {}).get(field)
            if isinstance(value, (int, float)) and value < 0:
                negatives.append({"stock": f"{eid}.{comp}.{field}", "value": value, "tick": engine.world.tick})
        trajectory.append(engine.world.material_dict() if hasattr(engine.world, "material_dict") else None)
        for eid, ent in engine.world.entities.items():
            for comp, fields in (ent.as_dict().get("components") or {}).items():
                for field, value in (fields or {}).items():
                    key = (eid, f"{comp}.{field}")
                    if since.get(key, (None,))[0] != value:
                        since[key] = (value, engine.world.tick)
                    elif (f"{comp}.{field}", value) in in_progress and engine.world.tick - since[key][1] >= 10:
                        msg = f"{eid} {comp}.{field} stays '{value}' for 10+ ticks with nothing resolving it"
                        if msg not in stuck:
                            stuck.append(msg)
        if model.terminal is not None and model.terminal.reached(engine.world):
            reached = True
            break
        if not acted and not material and deadlock_at is None:
            if not any(engine.discover(a)["available"] for a in actors):
                deadlock_at = engine.world.tick
                for eid, ent in engine.world.entities.items():  # an activity under way when nothing can happen is stuck
                    for comp, fields in (ent.as_dict().get("components") or {}).items():
                        for field, value in (fields or {}).items():
                            if (f"{comp}.{field}", value) in in_progress:
                                msg = f"{eid} {comp}.{field} stays '{value}' at a dead end with nothing resolving it"
                                if msg not in stuck:
                                    stuck.append(msg)
                blocked = []
                for a in actors:
                    for row in engine.discover(a)["blocked"][:6]:
                        bad = [f"{c['label']} (actual {c.get('actual')!r}, needs {c.get('required')!r})"
                               for c in row.get("checks", []) if not c.get("ok")]
                        blocked.append(f"{a} cannot {row['action']['kind']}: " + "; ".join(bad[:2]))
                break
    return {"stuck": stuck, "blocked_at_deadlock": blocked, "log": log, "fired": fired, "negatives": negatives, "reached": reached, "deadlock_at": deadlock_at,
            "trajectory_hash": hash(json.dumps(trajectory, sort_keys=True, default=str))}


def structure_findings(causal: dict[str, Any], stocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Structure assessment (Sterman ch. 21): every rise/fall the conceptual model declares has a rule."""
    ops: dict[str, set[str]] = {}
    for rule in [*causal.get("mechanics", []), *causal.get("processes", [])]:
        for eff in rule.get("effects", []):
            ops.setdefault(eff.get("path", "").removeprefix("components."), set()).add(eff.get("op"))
    out = []
    for row in stocks:
        if not row.get("field"):
            out.append({"check": "structure", "blocking": False, "stock": row["stock"],
                        "finding": f"the conceptual model's stock '{row['stock']}' could not be matched to a state field."})
            continue
        path = row["field"].split(".", 1)[1]
        have = ops.get(path, set())
        if row.get("has_outflows") and not ({"subtract", "set"} & have):
            out.append({"check": "structure", "blocking": True, "stock": row["stock"],
                        "finding": f"the conceptual model says '{row['stock']}' falls, but no rule ever decreases {row['field']}."})
        if row.get("has_inflows") and not ({"add", "set"} & have):
            out.append({"check": "structure", "blocking": False, "stock": row["stock"],
                        "finding": f"the conceptual model says '{row['stock']}' rises, but no rule ever increases {row['field']}."})
    return out


def in_progress_values(causal: dict[str, Any]) -> set[tuple[str, Any]]:
    """(field path, value) pairs set by an action that a process then waits on (checks field == value):
    the world treats them as an activity under way, which something must eventually resolve."""
    set_by_action = {(e["path"].removeprefix("components."), json.dumps((e.get("value") or {}).get("literal")))
                     for m in causal.get("mechanics", []) for e in m.get("effects", [])
                     if e.get("op") == "set" and isinstance(e.get("value"), dict) and "literal" in e["value"]}
    out = set()
    for p in causal.get("processes", []):
        for c in p.get("checks", []):
            left = (c.get("left") or {}).get("participant", {}).get("path", "") if isinstance(c.get("left"), dict) else ""
            right = c.get("right") if isinstance(c.get("right"), dict) else {}
            if c.get("op") == "eq" and "literal" in right:
                key = (left.removeprefix("components."), json.dumps(right["literal"]))
                if key in set_by_action:
                    out.add((key[0], right["literal"]))
    return out


def unresolved_findings(causal: dict[str, Any]) -> list[dict[str, Any]]:
    """Static: a status an action sets that no rule ever reads or changes again is started but never resolved."""
    reads, writers = set(), {}
    for r in [*causal.get("mechanics", []), *causal.get("processes", [])]:
        rid = r.get("mechanic_id") or r.get("process_id")
        for c in r.get("checks", []):
            for side in ("left", "right"):
                ref = (c.get(side) or {}).get("participant") if isinstance(c.get(side), dict) else None
                if ref:
                    reads.add(ref.get("path"))
        for e in r.get("effects", []):
            writers.setdefault(e.get("path"), set()).add(rid)
    out = []
    for m in causal.get("mechanics", []):
        for e in m.get("effects", []):
            v = e.get("value") if isinstance(e.get("value"), dict) else {}
            if e.get("op") == "set" and isinstance(v.get("literal"), str) and e["path"] not in reads \
                    and writers.get(e["path"], set()) <= {m["mechanic_id"]}:
                out.append({"check": "liveness", "blocking": True, "rule": m["mechanic_id"],
                            "finding": f"action {m['mechanic_id']} sets {e['path'].removeprefix('components.')} to "
                                       f"'{v['literal']}', but no rule ever reacts to it or changes it again: the "
                                       "activity is started and never resolved."})
    return out


def selector_findings(bundle: dict[str, Any], causal: dict[str, Any]) -> list[dict[str, Any]]:
    """Static liveness: every rule's actor and participant selectors match at least one entity."""
    def matches(sel: dict[str, Any], actors_only: bool = False) -> bool:
        return any(set(sel.get("categories", [])) <= set(e.get("categories", []))
                   and set(sel.get("components", [])) <= set(e.get("components", {}))
                   and (not actors_only or "actor" in e.get("categories", [])) for e in bundle["entities"])
    out = []
    for m in causal.get("mechanics", []):
        if matches(m.get("actor_selector", {})) and not matches(m.get("actor_selector", {}), actors_only=True):
            out.append({"check": "liveness", "blocking": True, "rule": m["mechanic_id"],
                        "finding": f"rule {m['mechanic_id']} can never be offered: its actor selector "
                                   f"{m.get('actor_selector')} matches only entities that cannot act; the actor must be "
                                   "an entity in category 'actor' (put the object it uses in participants)."})
        sels = [("actor", m.get("actor_selector", {}))] + list((m.get("participants") or {}).items())
        for name, sel in sels:
            if not matches(sel):
                out.append({"check": "liveness", "blocking": True, "rule": m["mechanic_id"],
                            "finding": f"rule {m['mechanic_id']} can never be offered: no entity has categories "
                                       f"{sel.get('categories')} and components {sel.get('components')} for its {name}."})
    for p in causal.get("processes", []):
        if not matches(p.get("selector", {})):
            out.append({"check": "liveness", "blocking": True, "rule": p["process_id"],
                        "finding": f"process {p['process_id']} can never run: no entity matches its selector {p.get('selector')}."})
    return out


def attempt_findings(bundle: dict[str, Any], causal: dict[str, Any]) -> list[dict[str, Any]]:
    """Decision 007 permissibility vs feasibility: an action must not refuse up front because of a stock that
    the actor itself (or something it owns) is about to consume; that outcome should play out over time."""
    def owned(sel: dict[str, Any]) -> bool:
        return any(set(sel.get("categories", [])) <= set(e.get("categories", []))
                   and set(sel.get("components", [])) <= set(e.get("components", {}))
                   and str(e.get("owner_ref", "")).startswith("actor:") for e in bundle["entities"])
    out = []
    for m in causal.get("mechanics", []):
        parts = dict(m.get("participants") or {})
        consumed_paths = {e.get("path") for r in [*causal.get("mechanics", []), *causal.get("processes", [])]
                          for e in r.get("effects", []) if e.get("op") == "subtract"}
        for chk in m.get("checks", []):
            for side in ("left", "right"):
                ref = (chk.get(side) or {}).get("participant") if isinstance(chk.get(side), dict) else None
                if not ref or ref.get("path") not in consumed_paths:
                    continue
                # only "is there enough" checks gate feasibility; an upper bound (room in a tank) is a fair rule
                enough = (side == "left" and chk.get("op") in ("gt", "gte")) or (side == "right" and chk.get("op") in ("lt", "lte"))
                if not enough:
                    continue
                name = ref.get("name")
                if name == "actor" or (name in parts and owned(parts[name])):
                    out.append({"check": "attempt_vs_outcome", "blocking": True, "rule": m["mechanic_id"],
                                "finding": (f"action {m['mechanic_id']} refuses up front with check '{chk.get('label')}' on "
                                            f"{name}.{ref.get('path')}, a stock the actor's own activity consumes. Fix with three changes: "
                                            "(1) the action only STARTS the activity (sets a status such as 'driving'), with no check "
                                            "on that stock and no progress or consumption effects; (2) add a process that, every tick "
                                            "while the status is active and the stock is above zero, makes one tick of progress and "
                                            "consumes the stock; (3) add a process that switches the status to a stopped/failed value "
                                            "when the stock is at or below zero, so the actor discovers it by observation.")})
    return out


def conservation_findings(causal: dict[str, Any]) -> list[dict[str, Any]]:
    """Conservation (Petri-net P-invariant style): a quantity that existing rules only ever move between
    entities (an add paired with a subtract of the same amount in one rule) must not be created from nothing."""
    def amount(eff: dict[str, Any]) -> str:
        return json.dumps(eff.get("value"), sort_keys=True)
    rules = [*causal.get("mechanics", []), *causal.get("processes", [])]
    conserved: set[str] = set()
    for r in rules:
        adds = [e for e in r.get("effects", []) if e.get("op") == "add"]
        subs = [e for e in r.get("effects", []) if e.get("op") == "subtract"]
        for a in adds:
            for s_ in subs:
                if amount(a) == amount(s_) and a.get("participant") != s_.get("participant"):
                    conserved.update({a["path"], s_["path"]})
    out = []
    for r in rules:
        rid = r.get("mechanic_id") or r.get("process_id")
        subs = {amount(e) for e in r.get("effects", []) if e.get("op") == "subtract"}
        for e in r.get("effects", []):
            if e.get("op") == "add" and e.get("path") in conserved and amount(e) not in subs:
                out.append({"check": "conservation", "blocking": True, "rule": rid,
                            "finding": f"rule {rid} creates {e['path'].removeprefix('components.')} from nothing; elsewhere "
                                       "that quantity only moves between things, so it must come from a stock that loses it."})
    return out


def run_checks(bundle: dict[str, Any], causal: dict[str, Any], *, seeds: int = 6, ticks: int = 80,
               stocks: list[dict[str, Any]] | None = None, anomaly_review: Any = None) -> dict[str, Any]:
    t0 = time.time()
    findings: list[dict[str, Any]] = structure_findings(causal, stocks or []) + selector_findings(bundle, causal) + attempt_findings(bundle, causal) + conservation_findings(causal) + unresolved_findings(causal)
    base = [simulate(bundle, causal, seed=s, ticks=ticks) for s in range(seeds)]
    # boundedness / conservation
    steps: dict[str, float] = {}
    for rule in [*causal.get("mechanics", []), *causal.get("processes", [])]:
        for eff in rule.get("effects", []):
            v = (eff.get("value") or {}).get("literal") if isinstance(eff.get("value"), dict) else None
            if eff.get("op") == "subtract" and isinstance(v, (int, float)):
                steps[eff["path"].removeprefix("components.")] = max(steps.get(eff["path"].removeprefix("components."), 0), v)
    worst: dict[str, float] = {}
    for r in base:
        for n in r["negatives"]:
            worst[n["stock"]] = min(worst.get(n["stock"], 0), n["value"])
    for stock, value in sorted(worst.items()):
        step = steps.get(stock.split(".", 1)[1], 0)
        overshoot = step > 0 and -value <= step + 1e-9  # discrete-time overshoot of at most one step
        findings.append({"check": "boundedness", "blocking": not overshoot, "stock": stock,
                         "finding": (f"{stock} dips to {value:g}, at most one step below zero (the rule language has no clamp)."
                                     if overshoot else
                                     f"{stock} becomes negative ({value:g}): no rule stops or blocks the activity when it runs out.")})
    rules = [m["mechanic_id"] for m in causal.get("mechanics", [])] + [p["process_id"] for p in causal.get("processes", [])]
    fired = set().union(*(r["fired"] for r in base))
    # reachability: random runs that avoid one-step dead ends (PDDL2.1/ENHSP cannot express processes)
    t_base = time.time() - t0
    guided = [simulate(bundle, causal, seed=100 + s, ticks=ticks * 2, guided=True) for s in range(2 * seeds)]
    t_guided = time.time() - t0 - t_base
    fired |= set().union(*(r["fired"] for r in guided))
    if causal.get("terminal") and not any(r["reached"] for r in [*base, *guided]):
        why = sorted({b for r in [*base, *guided] for b in r["blocked_at_deadlock"]})[:6]
        findings.append({"check": "reachability", "blocking": True,
                         "finding": f"the end condition was never reached in {2 * seeds} random runs"
                                    + (f"; runs got stuck where {' | '.join(why)}" if why else ".")})
    for rule in rules:  # liveness, over random and guided runs
        if rule not in fired:
            findings.append({"check": "liveness", "blocking": False, "rule": rule,
                             "finding": f"rule {rule} never fired in {2 * seeds} random runs."})
    stuck_runs = sorted({m for r in [*base, *guided] for m in r["stuck"]})
    dead = [r["deadlock_at"] for r in base if r["deadlock_at"] is not None]
    if dead:
        findings.append({"check": "deadlock", "blocking": False,
                         "finding": f"{len(dead)} of {seeds} runs stopped with nobody able to act before the end (ticks {dead})."})
    # extreme conditions: each depletable stock at zero must change something
    extreme_rows = []
    for msg in stuck_runs[:3]:
        findings.append({"check": "liveness", "blocking": True, "rule": msg.split(" stays")[0],
                         "finding": f"stuck activity: {msg}."})
    targets = depletable(bundle, causal)
    if stocks:  # test the conceptual model's stocks, not derived display fields
        conceptual = {r["field"] for r in stocks if r.get("field") and r.get("has_outflows")}
        targets = [t for t in targets if f"{t[0]}.{t[1]}.{t[2]}" in conceptual]
    anomaly_rows = []
    for eid, comp, field in targets:
        zero = [simulate(bundle, causal, seed=s, ticks=ticks, override=(eid, comp, field, 0)) for s in range(seeds)]
        identical = all(z["trajectory_hash"] == b_["trajectory_hash"] for z, b_ in zip(zero, base))
        for msg in sorted({m for z in zero for m in z["stuck"]})[:2]:
            findings.append({"check": "extreme_conditions", "blocking": True, "stock": f"{eid}.{comp}.{field}",
                             "rule": msg.split(" stays")[0],
                             "finding": f"with {eid} {field} at zero: {msg}; a rule for what happens when it runs out is missing."})
        consequence_free = identical or any(n["stock"] == f"{eid}.{comp}.{field}" for z in zero for n in z["negatives"])
        extreme_rows.append({"stock": f"{eid}.{comp}.{field}", "identical_to_baseline": identical,
                             "went_negative_from_zero": consequence_free and not identical})
        if consequence_free:
            findings.append({"check": "extreme_conditions", "blocking": True, "stock": f"{eid}.{comp}.{field}",
                             "finding": (f"with {eid} {field} set to zero the world behaves as if nothing were missing "
                                         f"({'identical runs' if identical else 'the stock just goes negative'}): "
                                         "a rule for what happens when it runs out is missing.")})
        elif anomaly_review is not None:  # behavior anomaly test on a guided run starting from zero
            run0 = simulate(bundle, causal, seed=100, ticks=ticks, override=(eid, comp, field, 0), guided=True)
            text = "\n".join(run0["log"][:120])
            for item in anomaly_review(f"{eid} {field}", text):
                anomaly_rows.append(item)
                findings.append({"check": "behavior_anomaly", "blocking": True, "stock": f"{eid}.{comp}.{field}",
                                 "finding": f"with {eid} {field} at zero: {item['why']} (run log: \"{item['quote']}\")"})
    if anomaly_review is not None:  # behavior anomaly test on an ordinary guided run (no stock changed)
        ordinary = simulate(bundle, causal, seed=200, ticks=ticks, guided=True)
        for item in anomaly_review("nothing (ordinary start)", "\n".join(ordinary["log"][:150])):
            anomaly_rows.append(item)
            findings.append({"check": "behavior_anomaly", "blocking": True, "stock": "ordinary-run", "rule": item["quote"][:60],
                             "finding": f"in an ordinary run: {item['why']} (run log: \"{item['quote']}\")"})
    if anomaly_review is not None:  # repeated-action test: each action kind done again and again
        for kind in sorted({a["kind"] for a in bundle.get("actions", [])}):
            rep = simulate(bundle, causal, seed=300, ticks=ticks, guided=True, prefer_kind=kind)
            for item in anomaly_review(f"nothing; the actor repeats '{kind}' whenever it can", "\n".join(rep["log"][:150])):
                anomaly_rows.append(item)
                findings.append({"check": "behavior_anomaly", "blocking": True, "stock": f"repeat-{kind}",
                                 "rule": item["quote"][:60],
                                 "finding": f"when '{kind}' is repeated: {item['why']} (run log: \"{item['quote']}\")"})
    merged: dict[str, dict[str, Any]] = {}  # one blocking finding per anomaly test, quoting up to three log lines
    rest = []
    for f in findings:
        if f["check"] != "behavior_anomaly":
            rest.append(f)
            continue
        key = f["stock"]
        if key not in merged:
            merged[key] = dict(f, rule=key)
        elif merged[key]["finding"].count("(run log:") < 3:
            merged[key]["finding"] += " ALSO: " + f["finding"].split(": ", 1)[-1]
    findings = rest + list(merged.values())
    return {"seconds": round(time.time() - t0, 1), "seeds": seeds, "ticks": ticks,
            "counts": {"blocking": sum(f["blocking"] for f in findings),
                       "advisory": sum(not f["blocking"] for f in findings),
                       "rules": len(rules), "rules_fired": len(fired & set(rules)),
                       "depletable_stocks": len(extreme_rows)},
            "step_seconds": {"random_runs": round(t_base, 1), "guided_runs": round(t_guided, 1),
                             "total": round(time.time() - t0, 1)},
            "extreme_conditions": extreme_rows, "behavior_anomalies": anomaly_rows, "findings": findings}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True, type=Path)
    ap.add_argument("--causal", default="causal.json")
    ap.add_argument("--out", default="checks.json")
    args = ap.parse_args()
    bundle = json.loads((args.model_dir / "bundle.json").read_text())
    causal = json.loads((args.model_dir / args.causal).read_text())
    model_path = args.model_dir / "model.json"
    stocks = json.loads(model_path.read_text()).get("stock_map") if model_path.exists() else None
    report = run_checks(bundle, causal, stocks=stocks)
    (args.model_dir / args.out).write_text(json.dumps(report, indent=2, sort_keys=True))
    for f in report["findings"]:
        print(f"[{'BLOCK' if f['blocking'] else 'note '}] {f['check']}: {f['finding']}")
    c = report["counts"]
    status = 1 if c["blocking"] else 0
    print(f"RESULT blocking={c['blocking']} advisory={c['advisory']} rules_fired={c['rules_fired']}/{c['rules']} "
          f"depletable_stocks={c['depletable_stocks']} seconds={report['seconds']} exit={status}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
