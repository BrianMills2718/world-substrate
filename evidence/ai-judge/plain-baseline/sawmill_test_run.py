"""Deterministic scripted test run of the plain version's accepted sawmill rule, plus one 3-log attempt (no model call)."""
import json, sys
from copy import deepcopy
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.run_authored_world import run_world, build_engine
OUT = REPO / "evidence/ai-judge/plain-baseline"
rec = json.loads((OUT / "pencil-sawmill-buys-logs.json").read_text())
lines = (REPO / "evidence/declared-laws/s2-pencil-2/run-log.jsonl").read_text().splitlines()
build = json.loads(lines[0])["result"]
bundle, model = deepcopy(build["bundle"]), deepcopy(build["causal_model"])
rule = json.loads(rec["output"]["proposed_rule"])
bundle["actions"].append(rule["action"]); model["mechanics"].append(rule["mechanic"])
def biz(world, eid):
    c = world.material_dict()["entities"][eid]["components"]["business"]
    return {"logs": c["logs"], "cash": c["cash"]}
out = {
    "what": "The plain version's accepted sawmill rule (buy-cedar-logs) run through the existing deterministic test run, then one 3-log attempt. No model call.",
    "source_world": "evidence/declared-laws/s2-pencil-2/run-log.jsonl line 1 (result.bundle, result.causal_model) plus the rule in pencil-sawmill-buys-logs.json",
    "script": "evidence/ai-judge/plain-baseline/sawmill_test_run.py",
}
# 1. The test run the rules check uses (world_builder_service.py:1797): run_world(policy="scripted") from the starting state.
dry, engine, _ = run_world(deepcopy(bundle), deepcopy(model), policy="scripted", max_turns=12, trace_id="ai-judge-sawmill-testrun")
buys = []
for t in dry["transcript"]:
    for actor, row in t["actors"].items():
        did = row.get("did") or {}
        if did.get("kind") == "buy-cedar-logs":
            buys.append({"turn": t.get("turn"), "actor": actor, "logger": did.get("logger"), "quantity": did.get("quantity"), "changed": row.get("changed")})
s = dry["summary"]
out["scripted_test_run"] = {
    "turns": s["turns"], "accepted_actions": s["accepted_actions"],
    "buy_cedar_logs_moves": buys,
    "quantities_tried": sorted({b["quantity"] for b in buys if b["quantity"] is not None}),
    "law_breaches": s.get("law_breaches") or [],
    "never_offered_keys": sorted((s.get("never_offered") or {}).keys()),
    "flags_buy_cedar_logs": any(b.get("rule_id") == "buy-cedar-logs" for b in s.get("law_breaches") or []) or "buy-cedar-logs" in (s.get("never_offered") or {}),
}
# 2. One 3-log attempt: the logger starts with 3 logs (as in the saved run before the attempt); the sawmill submits quantity 3.
b3 = deepcopy(bundle)
for e in b3["entities"]:
    if e["id"] == "logger":
        e["components"]["business"]["logs"] = 3
engine, _, _ = build_engine(b3, deepcopy(model))
page = engine.discover("sawmill", "buy-cedar-logs")
out["offered_to_sawmill"] = [{"action": r["action"], "ok": "reason" not in r, "reason": r.get("reason")} for r in page["available"] + page["blocked"]]
before = {"logger": biz(engine.world, "logger"), "sawmill": biz(engine.world, "sawmill")}
result = engine.submit({"actor": "sawmill", "kind": "buy-cedar-logs", "controller": "test", "base_revision": engine.world.revision,
                        "logger": "logger", "quantity": 3})
after = {"logger": biz(engine.world, "logger"), "sawmill": biz(engine.world, "sawmill")}
out["three_log_attempt"] = {
    "submitted": {"actor": "sawmill", "kind": "buy-cedar-logs", "logger": "logger", "quantity": 3},
    "status": result["status"],
    "failed_checks": [c["label"] for c in (result.get("event") or {}).get("checks", []) if not c["ok"]],
    "before": before, "after": after,
    "logs_moved": before["logger"]["logs"] - after["logger"]["logs"],
    "cash_paid": before["sawmill"]["cash"] - after["sawmill"]["cash"],
    "price_per_log": 10,
}
t = out["three_log_attempt"]
out["finding"] = (
    f"The scripted test run tried quantities {out['scripted_test_run']['quantities_tried']} only and flagged nothing on buy-cedar-logs. "
    f"The 3-log attempt was {t['status']}: {t['logs_moved']} logs moved for {t['cash_paid']} coins (3 x 10 = 30 expected). "
    "No deterministic check flags the single-price charge; the rules check catches malformed rules only."
)
print(out["finding"])
(OUT / "sawmill-test-run.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
