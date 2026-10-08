#!/usr/bin/env python3
"""Layer 1 modeling step (Decision 007): plain-language scenario -> checked world model.

Reuses the World Builder's two traced generators unchanged (bundle, then causal
mechanics). The only addition is generic author guidance that separates
permissibility (action checks) from feasibility (autonomous processes), and a
stock-and-flow summary derived mechanically from the compiled model, which the
layer-1 checks consume. Nothing here is scenario-specific.

Usage:
  python3 spikes/any-scenario-2026-10/model_scenario.py --name truck --text "..." [--kind task]
Writes runs/<name>-<stamp>/{bundle.json,causal.json,flows.json,model.json} and prints trace ids.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.generate_causal_model import DEFAULT_MODEL, generate_causal_model  # noqa: E402
from scripts.generate_world_bundle import generate_world_bundle  # noqa: E402
from scripts.run_authored_world import build_engine  # noqa: E402

sys.path.insert(0, str(HERE))
from checks import run_checks  # noqa: E402
from rule_writer import propose_rule  # noqa: E402
from spend import CAP, plan_spend  # noqa: E402

MAX_REPAIRS = 8
RULE_MODEL = "openrouter/openai/gpt-5.6-sol"
RULE_MODEL_WHY = ("Rule writing needs the stronger tier: eight gpt-5.6-luna attempts on 2026-10-07 produced rules with "
                  "non-actor actors, wrong location checks and missing depletion rules that repairs could not fix.")

ATTEMPT_GUIDANCE = (
    "Separate permissibility from feasibility. An action's checks say only whether the actor is allowed "
    "or positioned to begin it (rules of the game, location, possession). Never check whether the attempt "
    "will succeed: do not refuse an action because a resource is too low to finish it. Starting a "
    "multi-step activity sets the actor's or object's activity state. Autonomous processes then advance "
    "that activity every tick, consume or produce stocks, and switch the activity to a stopped or failed "
    "state when a needed stock runs out, or to a finished state when it completes. Every numeric stock "
    "needs a process or action for each way it can rise and each way it can fall."
)


ODD_SYSTEM = (
    "You are a simulation modeler following the ODD protocol (Overview, Design concepts, Details; Grimm et al.). "
    "Given a plain-language scenario, write the conceptual model that a simulation needs before any rules are written. "
    "Return exactly one JSON object, no prose. Be quantitative: every quantity the scenario implies (distances, "
    "positions, amounts, rates, capacities, counts) becomes a state variable with a unit and an initial value; "
    "estimate typical values when the text does not give them and list each estimate under assumptions. "
    "Choose one time step and say what it means in world units."
)
ODD_CONTRACT = {
    "purpose": "one sentence: what question the simulation answers",
    "time_step": "what one tick means, e.g. '1 tick = 10 miles of driving'",
    "entities": "[{name, kind: actor|object|place, state: [{variable, unit, initial}]}]",
    "processes_each_tick": "[plain sentences: what changes every tick without anyone choosing, including depletion, harm and failure]",
    "actor_decisions": "[{actor, may_attempt: [plain sentences], allowed_only_when: [rules-of-the-game conditions only]}]",
    "sensing": "[{actor, can_observe: [...], cannot_observe: [...]}]",
    "stocks": "[{stock, inflows: [...], outflows: [...]}] -- every way each quantity rises and falls; use [] (never 'none') when there is no way",
    "assumptions": "[every estimated value or simplification]",
}


def odd_model(text: str, *, trace_id: str, max_budget: float = 0.06) -> tuple[dict[str, Any], Any]:
    from llm_client import call_llm, safe_json_loads

    result = call_llm(
        DEFAULT_MODEL,
        [{"role": "system", "content": ODD_SYSTEM},
         {"role": "user", "content": json.dumps({"scenario": text, "contract": ODD_CONTRACT}, indent=2)}],
        task="world-substrate-odd-modeling", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort="low", num_retries=1,
    )
    odd = safe_json_loads(result.content)
    if not isinstance(odd, dict) or not odd.get("entities"):
        raise ValueError("ODD model returned no entities")
    return odd, result


def odd_brief(odd: dict[str, Any], limit: int = 1500) -> str:
    """Compact plain-text rendering of the ODD model, to fit the bundle generator's description limit."""
    parts = [f"Time step: {odd.get('time_step', '')}."]
    for e in odd.get("entities", []):
        state = "; ".join(f"{v.get('variable')}={v.get('initial')} {v.get('unit', '')}".strip() for v in e.get("state", []))
        parts.append(f"{e.get('name')} ({e.get('kind')}): {state}.")
    parts += [f"Each tick: {p}" for p in odd.get("processes_each_tick", [])]
    for d in odd.get("actor_decisions", []):
        parts.append(f"{d.get('actor')} may: {'; '.join(d.get('may_attempt', []))}.")
    out = " ".join(parts)
    return out[:limit]


def observable_keys(bundle: dict[str, Any]) -> list[str]:
    keys = []
    for e in bundle["entities"]:
        for comp, fields in (e.get("components") or {}).items():
            if isinstance(fields, dict):
                keys += [f"{e.get('label', e['id'])}.{k}" for k in fields]
    return sorted(set(keys))


def sensing_map(bundle: dict[str, Any], odd: dict[str, Any], *, trace_id: str, max_budget: float = 0.04):
    """Map the ODD's plain-language sensing onto exact observable fields per actor (one traced call)."""
    from pydantic import BaseModel
    from llm_client import call_llm_structured

    class ActorSensing(BaseModel):
        actor_id: str
        observable: list[str]

    class Sensing(BaseModel):
        actors: list[ActorSensing]

    keys = observable_keys(bundle)
    actors = [e["id"] for e in bundle["entities"] if "actor" in e.get("categories", [])]
    sensing, result = call_llm_structured(
        DEFAULT_MODEL,
        [{"role": "system", "content": (
            "Map each actor's plain-language sensing onto the exact state fields it can observe. "
            "Choose only from allowed_fields, copying them exactly. Include a field only if the sensing text "
            "says the actor can perceive it directly; exclude anything listed as cannot_observe or not mentioned.")},
         {"role": "user", "content": json.dumps({"actors": actors, "sensing": odd.get("sensing", []),
                                                 "allowed_fields": keys}, indent=2)}],
        Sensing, task="world-substrate-sensing-map", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort="low", num_retries=1)
    out = {}
    for row in sensing.actors:
        if row.actor_id in actors:
            out[row.actor_id] = sorted(k for k in row.observable if k in keys)  # client-side validation
    missing = [a for a in actors if a not in out]
    for a in missing:  # fallback, recorded: an actor the mapping left out senses only its own entity
        label = next(e.get("label", e["id"]) for e in bundle["entities"] if e["id"] == a)
        out[a] = sorted(k for k in keys if k.startswith(f"{label}."))
    if missing:
        out["_fallback_own_fields_only"] = missing
    return out, result


def stock_map(bundle: dict[str, Any], odd: dict[str, Any], *, trace_id: str, max_budget: float = 0.03):
    """Map each ODD stock (plain language) onto the bundle field that represents it (one traced call)."""
    from pydantic import BaseModel
    from llm_client import call_llm_structured

    class StockField(BaseModel):
        stock: str
        field: str | None
        has_inflows: bool
        has_outflows: bool

    class StockMap(BaseModel):
        stocks: list[StockField]

    keys = [f"{e['id']}.{c}.{k}" for e in bundle["entities"] for c, fs in (e.get("components") or {}).items()
            if isinstance(fs, dict) for k, v in fs.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    mapped, result = call_llm_structured(
        DEFAULT_MODEL,
        [{"role": "system", "content": (
            "For each stock in the conceptual model, name the numeric state field that represents it, copied exactly "
            "from allowed_fields, or null if none does. has_inflows/has_outflows say whether the conceptual model "
            "lists any way the stock rises / falls.")},
         {"role": "user", "content": json.dumps({"stocks": odd.get("stocks", []), "allowed_fields": keys}, indent=2)}],
        StockMap, task="world-substrate-stock-map", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort="low", num_retries=1)
    rows = [r.model_dump() for r in mapped.stocks]
    declared = {str(x.get("stock")): x for x in odd.get("stocks", []) if isinstance(x, dict)}
    for r in rows:
        if r["field"] not in keys:
            r["field"] = None  # client-side validation
        src = declared.get(r["stock"])  # directions come from the ODD's own lists, not the mapper's judgment
        if src is not None:
            r["has_inflows"] = bool(src.get("inflows"))
            r["has_outflows"] = bool(src.get("outflows"))
    return rows, result


def anomaly_reviewer(scenario: str, *, trace_id: str, max_budget: float = 0.03):
    """Behavior anomaly test (Sterman ch. 21): an AI reviewer reads a zero-stock run log and quotes implausible lines."""
    from pydantic import BaseModel
    from llm_client import call_llm_structured

    class Anomaly(BaseModel):
        quote: str
        why: str

    class Review(BaseModel):
        expected_consequence: str
        anomalies: list[Anomaly]

    counter = {"n": 0}

    def review(stock: str, log: str) -> list[dict[str, str]]:
        if not log.strip():
            return []
        counter["n"] += 1  # one trace per review: the per-trace budget caps each review, not the sum
        out, _ = call_llm_structured(
            DEFAULT_MODEL,
            [{"role": "system", "content": (
                "You review a simulation run log for behavior a domain expert would call physically or socially "
                "implausible given the scenario, e.g. something keeps moving or progressing after what powers it "
                "has stopped, or a quantity changes with no cause. When the condition sets a resource to zero, first "
                "state in expected_consequence what a domain expert would expect to happen to the people or things "
                "that depend on it (Sterman's extreme-conditions test); if the log never shows that consequence, report "
                "it as an anomaly quoting the log line where it should have appeared. Quote exact log lines. Return an "
                "empty list if nothing is implausible. Do not flag style, naming or missing detail.")},
             {"role": "user", "content": json.dumps({"scenario": scenario, "condition": f"{stock} started at zero",
                                                     "run_log": log})}],
            Review, task="world-substrate-behavior-anomaly", trace_id=f"{trace_id}-{counter['n']}", max_budget=max_budget,
            reasoning_effort="low", num_retries=1)
        return [{"quote": a.quote, "why": a.why} for a in out.anomalies if a.quote and a.quote in log]

    return review


def rules_summary(causal: dict[str, Any], limit: int = 2400) -> str:
    """Compact text of the current rules, so a repair patches them instead of starting over."""
    rows = []
    for m in causal.get("mechanics", []):
        eff = ", ".join(f"{e['path'].removeprefix('components.')} {e['op']} {json.dumps(e.get('value'))}" for e in m.get("effects", []))
        rows.append(f"action {m['mechanic_id']} [{m.get('action_kind', '')}] if {'; '.join(c['label'] for c in m.get('checks', []))} then {eff}")
    for p in causal.get("processes", []):
        eff = ", ".join(f"{e['path'].removeprefix('components.')} {e['op']} {json.dumps(e.get('value'))}" for e in p.get("effects", []))
        rows.append(f"process {p['process_id']} then {eff}")
    return " | ".join(rows)[:limit]


def outflow_coverage(odd: dict[str, Any], causal: dict[str, Any], *, trace_id: str, max_budget: float = 0.03):
    """For each outflow the ODD declares, name the rule ids that implement it (closed question, one traced call)."""
    from pydantic import BaseModel
    from llm_client import call_llm_structured

    class Row(BaseModel):
        stock: str
        outflow: str
        rules: list[str]

    class Coverage(BaseModel):
        rows: list[Row]

    rules = [{"id": m["mechanic_id"], "kind": "action", "effects": m.get("effects", []), "rationale": m.get("rationale", "")}
             for m in causal.get("mechanics", [])]
    rules += [{"id": p["process_id"], "kind": "process", "effects": p.get("effects", []), "rationale": p.get("rationale", "")}
              for p in causal.get("processes", [])]
    wanted = [{"stock": st.get("stock"), "outflow": o} for st in odd.get("stocks", []) for o in st.get("outflows", [])]
    cov, result = call_llm_structured(
        DEFAULT_MODEL,
        [{"role": "system", "content": (
            "For each (stock, outflow) pair from a conceptual model, list the ids of the rules whose effects actually "
            "implement that outflow (the rule removes or reduces what the outflow describes). Use [] when no rule does. "
            "Copy ids exactly. Answer every pair, in order.")},
         {"role": "user", "content": json.dumps({"pairs": wanted, "rules": rules})}],
        Coverage, task="world-substrate-outflow-coverage", trace_id=trace_id, max_budget=max_budget,
        reasoning_effort="low", num_retries=1)
    return [r.model_dump() for r in cov.rows], result


def consequence_checker(scenario: str, *, trace_id: str, votes: int = 3, max_budget: float = 0.02):
    """Extreme-conditions test (Sterman ch. 21) as a closed question: with a resource at zero from the start,
    does the consequence a domain expert expects appear in the run log? Majority of `votes` independent calls."""
    from pydantic import BaseModel
    from llm_client import call_llm_structured

    class Verdict(BaseModel):
        expected_consequence: str
        consequence_observed: bool
        evidence_quote: str

    counter = {"n": 0}

    def check(stock: str, log: str) -> dict[str, Any]:
        rows = []
        for _ in range(votes):
            counter["n"] += 1
            v, _ = call_llm_structured(
                DEFAULT_MODEL,
                [{"role": "system", "content": (
                    "Extreme-conditions test. A resource starts at zero in a simulation. State the consequence a domain "
                    "expert would expect for the people or things that depend on it (harm, loss, failure, stopping). "
                    "Then answer strictly: does the run log show that consequence actually happening (a state change "
                    "that is that consequence)? Quote the log line that shows it, or '' if none does.")},
                 {"role": "user", "content": json.dumps({"scenario": scenario, "resource_at_zero": stock,
                                                         "run_log": log})}],
                Verdict, task="world-substrate-extreme-conditions", trace_id=f"{trace_id}-{counter['n']}",
                max_budget=max_budget, reasoning_effort="low", num_retries=1)
            observed = v.consequence_observed and bool(v.evidence_quote) and v.evidence_quote in log
            rows.append({"expected": v.expected_consequence, "observed": observed, "quote": v.evidence_quote})
        yes = sum(r["observed"] for r in rows)
        return {"observed": yes * 2 > votes, "votes": rows, "expected": rows[0]["expected"]}

    return check


def flows(bundle: dict[str, Any], causal: dict[str, Any]) -> dict[str, Any]:
    """Stock-and-flow view: every numeric component path, with each rule that adds to or subtracts from it."""
    stocks: dict[str, dict[str, Any]] = {}
    for entity in bundle["entities"]:
        for comp, fields in (entity.get("components") or {}).items():
            if not isinstance(fields, dict):
                continue
            for field, value in fields.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    stocks.setdefault(f"{comp}.{field}", {"initial": {}, "inflows": [], "outflows": [], "sets": []})
                    stocks[f"{comp}.{field}"]["initial"][entity["id"]] = value
    rules = [("action", m["mechanic_id"], m.get("effects", [])) for m in causal.get("mechanics", [])]
    rules += [("process", p["process_id"], p.get("effects", [])) for p in causal.get("processes", [])]
    for kind, rule_id, effects in rules:
        for eff in effects:
            path = eff.get("path", "")
            if path not in stocks:
                continue
            slot = {"add": "inflows", "subtract": "outflows", "set": "sets"}.get(eff.get("op"))
            if slot:
                stocks[path][slot].append({"rule": rule_id, "kind": kind})
    return {"stocks": stocks}


def repair_loop(bundle, causal, stocks, reviewer, out: Path, name: str, stamp: str):
    """Checks, then rule-writer repairs (keep only improvements). Returns (bundle, causal, report, repairs)."""
    repairs = []
    report = run_checks(bundle, causal, stocks=stocks, anomaly_review=reviewer)
    (out / "causal.r0.json").write_text(json.dumps(causal, indent=2, sort_keys=True))
    (out / "checks.r0.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    print(f"[step] checks r0 blocking={report['counts']['blocking']} advisory={report['counts']['advisory']}", flush=True)
    best = (report["counts"]["blocking"], 0, bundle, causal, report)
    for n in range(1, MAX_REPAIRS + 1):  # one rule at a time: propose -> compile -> check -> keep or revert
        blocking = [f for f in report["findings"] if f["blocking"]]
        if not blocking:
            break
        order = ["liveness", "reachability", "attempt_vs_outcome", "boundedness", "extreme_conditions",
                 "behavior_anomaly", "structure"]  # fix what stops the world running before what refines it
        blocking.sort(key=lambda f: order.index(f["check"]) if f["check"] in order else len(order))
        target = blocking[0] if not repairs or repairs[-1].get("kept") or len(blocking) == 1 else blocking[min(1, len(blocking) - 1)]
        repair_trace = f"any-scenario-{name}-repair{n}-{stamp}"
        t3 = time.time()
        try:
            cand_bundle, candidate, rec = propose_rule(bundle, causal, target["finding"], trace_id=repair_trace,
                                                       guidance=ATTEMPT_GUIDANCE, model=RULE_MODEL,
                                                       model_justification=RULE_MODEL_WHY)
        except ValueError as error:
            repairs.append({"round": n, "trace": repair_trace, "finding": target["finding"], "kept": False,
                            "error": str(error)})
            print(f"[step] repair {n} trace={repair_trace} no compilable rule: {error}", flush=True)
            continue
        cand_report = run_checks(cand_bundle, candidate, stocks=stocks, anomaly_review=reviewer)
        (out / f"causal.r{n}.json").write_text(json.dumps(candidate, indent=2, sort_keys=True))
        (out / f"checks.r{n}.json").write_text(json.dumps(cand_report, indent=2, sort_keys=True))
        same = lambda f: f["check"] == target["check"] and f.get("rule") == target.get("rule") and f.get("stock") == target.get("stock")
        resolved = not any(same(f) for f in cand_report["findings"] if f["blocking"])
        # keep an improvement, or a fix of the targeted finding that exposes at most two new ones (bounded search)
        kept = cand_report["counts"]["blocking"] < report["counts"]["blocking"] or (
            resolved and cand_report["counts"]["blocking"] <= report["counts"]["blocking"] + 2)
        if kept:
            bundle, causal, report = cand_bundle, candidate, cand_report
            if report["counts"]["blocking"] < best[0]:
                best = (report["counts"]["blocking"], n, bundle, causal, report)
        repairs.append({"round": n, "trace": repair_trace, "finding": target["finding"], "kept": kept,
                        "change": rec["proposal"].get("change"), "target_id": rec["proposal"].get("target_id"),
                        "why": rec["proposal"].get("why"), "candidate_blocking": cand_report["counts"]["blocking"],
                        "blocking_after": report["counts"]["blocking"], "cost": rec["cost"]})
        print(f"[step] repair {n} {time.time() - t3:.1f}s trace={repair_trace} {rec['proposal'].get('change')} "
              f"{rec['proposal'].get('target_id')} candidate_blocking={cand_report['counts']['blocking']} kept={kept} "
              f"blocking_now={report['counts']['blocking']}", flush=True)
    if best[0] < report["counts"]["blocking"]:  # return the best model seen, not the last one kept
        print(f"[step] returning best round r{best[1]} (blocking={best[0]})", flush=True)
        _, _, bundle, causal, report = best
    return bundle, causal, report, repairs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--kind", default="task", choices=("task", "ongoing", "open"))
    ap.add_argument("--out-root", default=str(HERE / "runs"))
    ap.add_argument("--repair-dir", type=Path, help="rerun checks + repairs on an existing model dir (no regeneration)")
    args = ap.parse_args()
    if args.repair_dir:
        d = args.repair_dir
        model = json.loads((d / "model.json").read_text())
        stamp = time.strftime("%Y%m%dT%H%M%S")
        out = d / f"repair-{stamp}"
        out.mkdir()
        reviewer = anomaly_reviewer(model["scenario_text"], trace_id=f"any-scenario-{args.name}-anomaly-{stamp}")
        bundle, causal, report, repairs = repair_loop(json.loads((d / "bundle.json").read_text()),
                                                      json.loads((d / "causal.json").read_text()),
                                                      model.get("stock_map") or [], reviewer, out, args.name, stamp)
        for nm, v in {"bundle": bundle, "causal": causal, "checks": report}.items():
            (d / f"{nm}.json").write_text(json.dumps(v, indent=2, sort_keys=True))
        if not (d / "sensing.json").exists():
            sensing, _ = sensing_map(bundle, model["odd"], trace_id=f"any-scenario-{args.name}-sensing-{stamp}")
            (d / "sensing.json").write_text(json.dumps(sensing, indent=2, sort_keys=True))
        model.setdefault("repairs", []).extend(repairs)
        model["final_check_counts"] = report["counts"]
        (d / "model.json").write_text(json.dumps(model, indent=2, sort_keys=True))
        print(f"[done] repaired {d} blocking={report['counts']['blocking']}")
        return 0
    if plan_spend()[1] > CAP - 0.25:
        raise SystemExit(f"plan spend cap: ${plan_spend()[1]:.4f} spent of ${CAP:.2f}")
    stamp = time.strftime("%Y%m%dT%H%M%S")
    out = Path(args.out_root) / f"{args.name}-{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    odd_trace = f"any-scenario-{args.name}-odd-{stamp}"
    odd, r0 = odd_model(args.text, trace_id=odd_trace)
    brief = odd_brief(odd, limit=1990 - len(args.text) - 20)
    print(f"[step] odd {time.time() - t0:.1f}s trace={odd_trace} cost={getattr(r0, 'cost', None)}", flush=True)
    t0 = time.time()
    bundle_trace = f"any-scenario-{args.name}-bundle-{stamp}"
    bundle, not_modeled, r1 = generate_world_bundle(f"{args.text}\nModel: {brief}", trace_id=bundle_trace, world_kind=args.kind)
    print(f"[step] bundle {time.time() - t0:.1f}s trace={bundle_trace} cost={getattr(r1, 'cost', None)}", flush=True)
    t1 = time.time()
    causal_trace = f"any-scenario-{args.name}-mechanics-{stamp}"
    causal, r2 = generate_causal_model(bundle, trace_id=causal_trace, guidance=ATTEMPT_GUIDANCE, world_kind=args.kind,
                                       reasoning_effort="medium", model=RULE_MODEL,
                                       model_justification=RULE_MODEL_WHY, max_budget=0.40)
    print(f"[step] mechanics {time.time() - t1:.1f}s trace={causal_trace} cost={getattr(r2, 'cost', None)}", flush=True)
    build_engine(bundle, causal)  # compile + install: raises if any mechanic is rejected
    stocks_trace = f"any-scenario-{args.name}-stocks-{stamp}"
    stocks, r4 = stock_map(bundle, odd, trace_id=stocks_trace)
    print(f"[step] stock map trace={stocks_trace} cost={getattr(r4, 'cost', None)} mapped={sum(1 for x in stocks if x['field'])}/{len(stocks)}", flush=True)
    early = {"scenario_text": args.text, "world_kind": args.kind, "odd": odd, "stock_map": stocks,
             "traces": {"odd": odd_trace, "bundle": bundle_trace, "mechanics": causal_trace, "stocks": stocks_trace}}
    for name_, value in {"bundle": bundle, "causal": causal, "model": early}.items():  # resumable with --repair-dir
        (out / f"{name_}.json").write_text(json.dumps(value, indent=2, sort_keys=True))
    reviewer = anomaly_reviewer(args.text, trace_id=f"any-scenario-{args.name}-anomaly-{stamp}")
    bundle, causal, report, repairs = repair_loop(bundle, causal, stocks, reviewer, out, args.name, stamp)
    (out / "checks.json").write_text(json.dumps(report, indent=2, sort_keys=True))
    t2 = time.time()
    sensing_trace = f"any-scenario-{args.name}-sensing-{stamp}"
    sensing, r3 = sensing_map(bundle, odd, trace_id=sensing_trace)
    print(f"[step] sensing {time.time() - t2:.1f}s trace={sensing_trace} cost={getattr(r3, 'cost', None)}", flush=True)
    flow = flows(bundle, causal)
    model = {
        "scenario_text": args.text,
        "world_kind": args.kind,
        "traces": {"odd": odd_trace, "bundle": bundle_trace, "mechanics": causal_trace, "sensing": sensing_trace,
                   "stocks": stocks_trace, "anomaly": f"any-scenario-{args.name}-anomaly-{stamp}"},
        "stock_map": stocks,
        "odd": odd,
        "repairs": repairs,
        "final_check_counts": report["counts"],
        "not_modeled": not_modeled,
        "guidance": ATTEMPT_GUIDANCE,
    }
    for name, value in {"bundle": bundle, "causal": causal, "flows": flow, "model": model, "sensing": sensing}.items():
        (out / f"{name}.json").write_text(json.dumps(value, indent=2, sort_keys=True))
    print(f"[done] {out} actions={len(causal.get('mechanics', []))} processes={len(causal.get('processes', []))} "
          f"stocks={len(flow['stocks'])} not_modeled={len(not_modeled)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
