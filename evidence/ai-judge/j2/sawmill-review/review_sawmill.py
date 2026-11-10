"""J2 measurement (docs/plans/ai_judge.md, "LLM call boundary and cost"): does the existing model rules review flag the
plain version's sawmill rule, which charges the price once rather than per log? One paid call on the review model.

Input: the sawmill world as built (evidence/declared-laws/s2-pencil-2/run-log.jsonl line 1) with the plain version's
accepted rule added (evidence/ai-judge/plain-baseline/pencil-sawmill-buys-logs.json). Output: review.json beside this.
"""
import json
import sys
import uuid
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.review_rules import REVIEW_MODEL, review_rules  # noqa: E402

OUT = Path(__file__).resolve().parent
rec = json.loads((REPO / "evidence/ai-judge/plain-baseline/pencil-sawmill-buys-logs.json").read_text())
build = json.loads((REPO / "evidence/declared-laws/s2-pencil-2/run-log.jsonl").read_text().splitlines()[0])["result"]
bundle, model = deepcopy(build["bundle"]), deepcopy(build["causal_model"])
rule = json.loads(rec["output"]["proposed_rule"])
bundle["actions"].append(rule["action"])
model["mechanics"].append(rule["mechanic"])
description = bundle["world"].get("summary") or ""
trace_id = f"world-substrate/ai-judge-j2/sawmill-review/{uuid.uuid4().hex}"
findings, cost = review_rules(description, bundle, model, trace_id=trace_id, max_budget=0.25)
on_rule = [f for f in findings if f["rule_id"] == rule["mechanic"]["mechanic_id"]]
out = {
    "what": __doc__.strip(),
    "review_model": REVIEW_MODEL, "trace_id": trace_id, "cost_usd": cost,
    "rule_id": rule["mechanic"]["mechanic_id"],
    "findings": findings,
    "findings_on_the_rule": on_rule,
}
(OUT / "review.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({"cost_usd": cost, "trace_id": trace_id, "findings": len(findings), "on_rule": on_rule}, indent=1))
