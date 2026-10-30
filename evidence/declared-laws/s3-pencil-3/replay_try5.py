"""Free replay: pencil s3p3 try 5 (call 22358, the redesign that added an arrival process) compiled against the
kept bundle with the nullable-ref fix, then the scripted dry run. No model call."""
import json, sys
from pathlib import Path
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]; sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.generate_causal_model import merge_revision, tidy_proposal
from scripts.run_authored_world import run_world
from world_substrate.action_authoring import CausalModel
D = Path(__file__).parent
g = json.loads((D / "run-log.jsonl").read_text().splitlines()[0])["result"]
call = next(json.loads(l) for l in open(D / "llm-calls.jsonl") if json.loads(l)["id"] == 22358)
prev = json.loads(json.loads(call["messages"])[1]["content"])["previous_proposal"]
value = merge_revision(prev, json.loads(call["response"]))
bundle = g["bundle"]
tidy_proposal(value, bundle)
CausalModel.from_dict(value, bundle=bundle)
print("compiled ok; processes:", [p["process_id"] for p in value.get("processes", [])])
dry, _, _ = run_world(bundle, value, policy="scripted", max_turns=24)
s = dry["summary"]
print({k: s.get(k) for k in ("turns", "accepted_actions", "never_offered", "idle_actors")})
sold = [e for e in dry.get("events", dry.get("engine_events", [])) if "sell-pencils" in json.dumps(e)[:400]]
print("events mentioning sell-pencils:", len(sold))
import collections
kinds = collections.Counter()
for t in dry.get("transcript") or []:
    for a, v in (t.get("actors") or {}).items():
        if v.get("status") == "accepted":
            kinds[(v.get("did") or {}).get("kind")] += 1
    for w in t.get("world_changes") or []:
        kinds["process:" + w] += 1
print(dict(kinds))
