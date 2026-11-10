"""J2 ruling on the saved sawmill case (docs/plans/ai_judge.md A5): the sawmill offers to pay the Oregon logger for its
three cedar logs and asks for them to be transferred. Plan A5: a ruling that would move another person's goods on the
buyer's move alone goes to that person as an offer instead. One judge run (paid, llm_client), no other model call.

The world is rebuilt exactly as the attempt found it: the saved build (evidence/declared-laws/s2-pencil-2/run-log.jsonl
line 1), the state at the end of round 3 (line 4, final_snapshot), then round 4's three moves made before the
sawmill's (line 5, r4-e00001, r4-e00003, r4-e00005, resubmitted as recorded). Output: ruling.json beside this.
"""
import json
import sys
import uuid
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts import consequence_report, judge  # noqa: E402
from scripts.run_authored_world import _component_types, actor_ids, build_engine  # noqa: E402
from world_substrate.engine import Engine  # noqa: E402
from world_substrate.model import World  # noqa: E402

OUT = Path(__file__).resolve().parent
lines = [json.loads(x) for x in (REPO / "evidence/declared-laws/s2-pencil-2/run-log.jsonl").read_text().splitlines()]
build = lines[0]["result"]
bundle, rules = deepcopy(build["bundle"]), deepcopy(build["causal_model"])
engine, model, _ = build_engine(bundle, rules)
engine = Engine(World.from_snapshot(lines[3]["result"]["final_snapshot"], component_types=_component_types(bundle)),
                engine.registry)
round4 = lines[4]["result"]["transcript"][0]["actors"]
replayed = []
for actor in ("graphite-mine", "lead-works", "logger"):
    did = round4[actor]["did"]
    out = engine.submit({**did, "controller": "j2-sawmill-rebuild", "base_revision": engine.world.revision})
    replayed.append({"actor": actor, "kind": did["kind"], "status": out["status"]})
saved = round4["sawmill"]
attempt = "I go to the Oregon logger and offer to pay for their three cedar logs, asking them to transfer the logs to my sawmill."
assert saved["did"]["attempt"] == attempt, saved["did"]
people = actor_ids(engine, model)
named = saved["did"].get("names") or ([saved["did"]["asks"]] if saved["did"].get("asks") else [])
one = consequence_report.pass_one(engine, "sawmill", named, people=set(people))
trace_id = f"world-substrate/ai-judge-j2/sawmill/{uuid.uuid4().hex}"
record = judge.judge(bundle, rules, engine, actor="sawmill", attempt=attempt, pass_one=one, people=people,
                     model="openrouter/openai/gpt-6-luna", trace_id=trace_id, max_budget=0.25)
values = engine.world.material_dict()["entities"]
out = {
    "what": __doc__.strip(), "trace_id": trace_id, "revision": engine.world.revision, "replayed": replayed,
    "named": named,
    "state": {e: values[e]["components"].get("business") or values[e]["components"] for e in ("sawmill", "logger")},
    "pass_one": one, "ruling": record,
}
(OUT / "ruling.json").write_text(json.dumps(out, indent=1, default=str) + "\n")
print(json.dumps({"trace_id": trace_id, "revision": engine.world.revision, "replayed": replayed, "named": named,
                  "outcome": record["outcome"], "whose_choice": record["whose_choice"], "ruling": record["ruling"],
                  "why": record.get("why"), "cost_usd": record["cost_usd"]}, indent=1))
