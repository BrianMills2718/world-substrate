"""Replay recorded attempt-interpreter calls through today's prompt, with the same inputs (paid: about $0.0003 a call).

Usage: LLM_CLIENT_PROJECT=world-substrate python scripts/replay_interpreter.py . <llm-calls.jsonl> <out.jsonl> <call_id>[:times] ...
Used to check a prompt change against recorded failures and controls before any live build (evidence/declared-laws/seller-wording/)."""
import json, re, sys, uuid
from pathlib import Path
repo, calls_path, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
sys.path[:0] = [str(repo / "src"), str(repo)]
from world_substrate import attempt as A
calls = {json.loads(l)["id"]: json.loads(l) for l in open(calls_path)}
trace = f"world-substrate-interpreter-replay-{uuid.uuid4().hex[:8]}"  # seller-wording (2026-10-30) and unmatched-replay (2026-10-31) ran under world-substrate-seller-wording-*
rows = []
for spec in sys.argv[4:]:
    cid, n = (spec.split(":") + ["1"])[:2]
    c = calls[int(cid)]; m = c["messages"]; m = json.loads(m) if isinstance(m, str) else m
    t = m[-1]["content"]
    actor = re.search(r"^Person: (\S+)", t, re.M).group(1)
    attempt = re.search(r"^Attempt: (.*)$", t, re.M).group(1)
    kinds = json.loads(t.split("Action kinds in this world (kind, description, fields):", 1)[1].split("Entities (id: label):")[0])
    entities = json.loads(t.split("Entities (id: label):", 1)[1])
    for i in range(int(n)):
        reading, cost = A.interpret(attempt, actor=actor, signatures=kinds, entities=entities, model=c["model"],
                                    trace_id=trace, max_budget=0.05)
        rows.append({"call_id": int(cid), "try": i, "actor": actor, "attempt": attempt,
                     "was": json.loads(c["response"]).get("kind"), "now": reading.get("kind") or "unmatched",
                     "fields": reading.get("fields"), "why": reading.get("why"), "cost": cost})
        print(cid, i, actor, "was", rows[-1]["was"], "now", rows[-1]["now"], rows[-1]["fields"], flush=True)
Path(out).write_text("\n".join(json.dumps(r) for r in rows) + "\n")
print("trace", trace, "cost", round(sum(r["cost"] for r in rows), 4))
