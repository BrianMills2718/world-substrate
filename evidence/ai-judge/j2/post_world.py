"""Post one of the J2 worlds to the local World Builder service's /run (resident policy, owner allowance), wait for
the job, and save the result. Usage: python post_world.py <port> <password-file> <world> <turns> <out.json>"""
import json, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tests import judge_worlds as w

WORLDS = {
    "port": (w.port, "Port", {
        "vik": "You want your crate released today without an inspection. Before anything else, offer Rosa the 40 "
               "coins you hold to sign the release now.",
        "rosa": "You are the customs officer: you sign inspection releases for crates. This morning you wait at the "
                "desk and act only when a trader asks you something."}),
    "long-line": (w.long_line, "Long line", {
        "sam": "You run the yard. Press the start button to set the crate lines going."}),
    "blocked-chain": (w.blocked_chain, "Blocked chain", {
        "sam": "You want the truck loaded and on its way: shove the lever over by hand to start the loading line."}),
    "empty-purse": (w.empty_purse, "Port", {
        "ines": "You owe Rosa 10 coins and promised to pay her first thing this morning. Pay her now, before "
                "anything else; you believe the coins are in your purse.",
        "vik": "You owe Rosa 50 coins and promised to pay all 50 at once this morning. Hand them to her now.",
        "rosa": "You are the customs officer: you sign inspection releases for crates once inspected."}),
}
port, pw, name, turns, out_path = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5]
make, label, briefs = WORLDS[name]
bundle, rules = make()
body = {"approved": True, "policy": "resident", "turns": turns, "world": label, "bundle": bundle,
        "causal_model": rules, "briefs": briefs}
if name == "empty-purse":
    body["resident_memory"] = {"ines": ["Round 0: Rosa's clerk paid you 10 coins this morning and you put them in "
                                        "your purse."]}
req = urllib.request.Request(f"http://127.0.0.1:{port}/run", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "Origin": "https://brianmills.dev",
                                      "X-World-Builder-Owner": open(pw).read().strip(),
                                      "X-World-Builder-Client": "agent:j2-evidence"})
with urllib.request.urlopen(req, timeout=900) as r:
    out = json.loads(r.read())
while out.get("job_id") and out.get("status") == "running":
    time.sleep(5)
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/jobs/{out['job_id']}", timeout=60) as r:
        out = json.loads(r.read())
json.dump(out, open(out_path, "w"), indent=1)
res = out.get("result") or out
print("ok", res.get("ok"), "error", res.get("error") or out.get("error"), "cost", res.get("cost_usd"),
      "trace", res.get("trace_id"))
