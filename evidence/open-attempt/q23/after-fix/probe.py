import json, sys
sys.path[:0] = [".", "src"]
from scripts.run_authored_world import build_engine
O = "evidence/open-attempt/q23/after-fix"
bundle = json.load(open(f"{O}/bundle.json")); rules = json.load(open(f"{O}/rules3.json"))
import copy
if len(sys.argv) > 1 and sys.argv[1] == "passable":
    bundle = copy.deepcopy(bundle)
    for e in bundle["entities"]:
        if "barrier" in e["components"]: e["components"]["barrier"]["passable"] = True
    print("CONTROL: wall made passable in an in-memory copy")
engine, _, _ = build_engine(bundle, rules)
def act(kind, **fields):
    env = {"actor": "sam", "kind": kind, "controller": "probe", "base_revision": engine.world.revision, **fields}
    out = engine.submit(env)
    ev=out.get("event",{}); print(kind, out.get("status"), "failed:", [c["label"] for c in ev.get("checks", []) if not c["ok"]])
    return out
act("move", to="hangar", way="brick-wall")
act("fly", aircraft="helicopter")
if len(sys.argv) > 1: act("move", to="hangar", way="brick-wall"); act("fly", aircraft="helicopter")
print("sam at", engine.world.entities["sam"].location.location_id)
