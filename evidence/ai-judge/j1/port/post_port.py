"""Post the J1 port world to the local World Builder service's /run (resident policy, owner allowance) and print the
result summary. Usage: python post_port.py <port> <password-file> <turns>"""
import json, sys, urllib.request
sys.path.insert(0, "/home/brian/code2/worktrees/ws-judge-j1")
from tests.judge_worlds import port
bundle, rules = port()
body = {"approved": True, "policy": "resident", "turns": int(sys.argv[3]), "world": "Port", "bundle": bundle,
        "causal_model": rules,
        "briefs": {"vik": "You want your crate released today without an inspection, and you are willing to pay Rosa "
                          "for that with the coins you hold.",
                   "rosa": "You are the customs officer: you sign inspection releases for crates."}}
req = urllib.request.Request(f"http://127.0.0.1:{sys.argv[1]}/run", data=json.dumps(body).encode(), method="POST",
                             headers={"Content-Type": "application/json", "Origin": "https://brianmills.dev",
                                      "X-World-Builder-Owner": open(sys.argv[2]).read().strip(),
                                      "X-World-Builder-Client": "agent:j1-evidence"})
with urllib.request.urlopen(req, timeout=900) as r:
    out = json.loads(r.read())
if out.get("job_id") and out.get("status") == "running":
    import time
    while True:
        time.sleep(5)
        with urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/jobs/{out['job_id']}", timeout=60) as r:
            out = json.loads(r.read())
        if out.get("status") != "running":
            break
json.dump(out, open(sys.argv[4] if len(sys.argv) > 4 else "/dev/stdout", "w"), indent=1)
res = out.get("result") or out
print("\nok", out.get("ok"), "error", out.get("error"), "cost", res.get("cost_usd") or out.get("cost_usd"), file=sys.stderr)
