#!/usr/bin/env python3
"""C2: the extreme-conditions check (a needed resource set to zero) on the full model and on the same model
with its harm/death rule removed.

The rule to remove is named explicitly (--remove-rule): which generated rule represents harm is read from the
model by a person or the caller, never inferred from rule names by regex. The resource is named explicitly too
(--stock entity.component.field). Both runs use checks.run_checks with the expert-expectation anomaly reviewer;
the report records each run's extreme-condition and anomaly findings for that stock, with trace ids.
Exit 0 only when the full model has no blocking finding for the stock and the reduced model has at least one.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1]), str(HERE.parents[1] / "src")]

from checks import run_checks  # noqa: E402
from model_scenario import anomaly_reviewer, outflow_coverage  # noqa: E402


def stock_findings(report: dict, stock: str) -> list[dict]:
    return [f for f in report["findings"] if f["blocking"] and f.get("stock") == stock
            and f["check"] in ("extreme_conditions", "behavior_anomaly")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, required=True)
    ap.add_argument("--stock", required=True, help="entity.component.field set to zero, e.g. ventilators")
    ap.add_argument("--remove-rule", required=True, help="mechanic_id or process_id of the harm/death rule")
    ap.add_argument("--harm-outflow", action="append", required=True,
                    help="ODD outflow name(s) that represent harm, copied exactly from the model's ODD stocks")
    args = ap.parse_args()
    d = args.model_dir
    bundle = json.loads((d / "bundle.json").read_text())
    causal = json.loads((d / "causal.json").read_text())
    causal.pop("review", None)
    model = json.loads((d / "model.json").read_text())
    ids = [m["mechanic_id"] for m in causal["mechanics"]] + [p["process_id"] for p in causal.get("processes", [])]
    if args.remove_rule not in ids:
        raise SystemExit(f"rule {args.remove_rule!r} not in model: {ids}")
    reduced = deepcopy(causal)
    reduced["mechanics"] = [m for m in reduced["mechanics"] if m["mechanic_id"] != args.remove_rule]
    reduced["processes"] = [p for p in reduced.get("processes", []) if p["process_id"] != args.remove_rule]
    stamp = time.strftime("%Y%m%dT%H%M%S")
    out = {"stock": args.stock, "removed_rule": args.remove_rule, "runs": {}}
    for label, c in (("full", causal), ("without_harm_rule", reduced)):
        trace = f"any-scenario-c2-{label}-{stamp}"
        coverage, _ = outflow_coverage(model["odd"], c, trace_id=f"{trace}-coverage")
        report = run_checks(bundle, c, stocks=model.get("stock_map") or [],
                            anomaly_review=anomaly_reviewer(model["scenario_text"], trace_id=trace), coverage=coverage)
        hits = stock_findings(report, args.stock)
        harm = [f for f in report["findings"] if f["check"] == "structure" and f.get("rule") in args.harm_outflow]
        out.setdefault("outflow_coverage", {})[label] = coverage
        out["runs"][label] = {"trace_prefix": trace, "blocking_for_stock": len(hits),
                              "missing_harm_outflow": [f["finding"] for f in harm],
                              "findings": [h["finding"] for h in hits], "all_counts": report["counts"],
                              "extreme_row": [r for r in report["extreme_conditions"] if r["stock"] == args.stock]}
        print(f"[{label}] extreme/anomaly findings for {args.stock}: {len(hits)}; missing harm outflow: "
              f"{len(harm)} trace={trace}")
        for h in harm:
            print(f"   * {h['finding'][:300]}")
        for h in hits:
            print(f"   - {h['finding'][:300]}")
    (d / f"c2-{stamp}.json").write_text(json.dumps(out, indent=2))
    full, reduced = out["runs"]["full"], out["runs"]["without_harm_rule"]
    ok_structure = not full["missing_harm_outflow"] and bool(reduced["missing_harm_outflow"])
    ok_extreme = full["blocking_for_stock"] == 0 and reduced["blocking_for_stock"] > 0
    out["result"] = {"outflow_coverage_detects": ok_structure, "extreme_review_detects": ok_extreme}
    (d / f"c2-{stamp}.json").write_text(json.dumps(out, indent=2))
    print(f"[result] outflow coverage separates full/reduced: {ok_structure}; extreme review separates them: {ok_extreme}")
    ok = ok_structure
    print(f"RESULT c2={'PASS' if ok else 'FAIL'} report={d / f'c2-{stamp}.json'} exit={0 if ok else 1}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
