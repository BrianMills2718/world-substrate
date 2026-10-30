"""Free replay: the pencil s3p4 kept world (run-log row 1, try 5) in a 24-round scripted dry run. No model call.
On a23bd63 (before the discovery fix) buy-logs and the seven moves after it are never offered; with the fix every
move is offered and pencils sell."""
import collections, json, sys
from pathlib import Path
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]; sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.run_authored_world import run_world
g = json.loads(Path(__file__).with_name("run-log.jsonl").read_text().splitlines()[0])["result"]
dry, _, _ = run_world(g["bundle"], g["causal_model"], policy="scripted", max_turns=24)
for k, v in dry["summary"]["never_offered"].items(): print("NEVER", k, "::", v[:260])
c = collections.Counter((v.get("did") or {}).get("kind") for t in dry["transcript"] for v in t["actors"].values() if v.get("status") == "accepted")
print(dict(c))
