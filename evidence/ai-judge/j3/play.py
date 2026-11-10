"""Play one of the J3 worlds round by round against a World Builder service, the way the run page does: one round per
/run request, carrying back the sealed state each round returns (continue_from, continue_seal, approval, turn_offset,
resident_memory, underway, stop_history, rulings), and sending the owner's Approve or Reject as `decisions` with the
round that follows. Resident policy, owner allowance. Saves every response and prints each round's moves.

Usage: python play.py <base-url> <password-file> <case> <out.json> [--share] [--branch earlier.json:N]
  base-url: http://127.0.0.1:8795 (local branch) or https://brianmills.dev/world-builder/api (live)
  --share: after the rounds, save the run as a share link (POST /share) and print its id.
  --branch earlier.json:N: keep the first N rounds of an earlier run of this script (same rounds, same traces) and play
    the rest from that run's state, so one held ruling can be both approved and rejected.
"""
import json, sys, time, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from tests import judge_worlds as w

PORT_BRIEFS = {
    "vik": "You want your crate released today without an inspection. Before anything else, offer Rosa the 40 coins you "
           "hold to sign the release now.",
    "ines": "You are another trader at the customs desk, with 30 coins and a crate of your own. In the first round only "
            "wait and watch. From the second round on, you want your own crate released without an inspection: hand "
            "Rosa 10 coins from your purse. Say it as a plain move: hand Rosa 10 coins.",
    "rosa": "You are the customs officer: you sign inspection releases for crates once inspected. You wait at the desk "
            "and act only when a trader asks you something.",
}
LUMBER_BRIEFS = {
    "bo": "You want every log in the pile today. In the first round, buy them all: tell Sam you take every log in the "
          "pile and pay the posted price for each log.",
    "sam": "You run the log yard and sell logs from the pile at the posted price. Wait at the yard and act only when "
           "a buyer asks you something.",
}
# case -> (world, label, briefs, setting, one entry per round: the owner's answers sent with that round)
CASES = {
    "default": (w.port_two_traders, "Port", PORT_BRIEFS, "create", [[], [], []]),
    "wait-hold": (w.port_two_traders, "Port", PORT_BRIEFS, "wait", [[], []]),
    "wait-approve": (w.port_two_traders, "Port", PORT_BRIEFS, "wait", [[], [], [("R1", "approve")], []]),
    "wait-reject": (w.port_two_traders, "Port", PORT_BRIEFS, "wait", [[], [], [("R1", "reject")], []]),
    "price-times-quantity": (w.lumberyard, "Lumberyard", LUMBER_BRIEFS, "create", [[], []]),
}
base, pwfile, name, out_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
make, label, briefs, setting, answers = CASES[name]
bundle, rules = make()
headers = {"Content-Type": "application/json", "Origin": "https://brianmills.dev",
           "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) j3-evidence",
           "X-World-Builder-Owner": open(pwfile).read().strip(), "X-World-Builder-Client": "agent:j3-evidence"}


def call(path, body=None):
    req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET", headers=headers)
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())


def carry(res):
    trace = res["trace"]
    state = {"continue_from": trace["final_snapshot"], "continue_seal": res["snapshot_seal"], "approval": res["approval"],
             "turn_offset": res["summary"]["last_turn"], "resident_memory": trace.get("resident_memory"),
             "underway": trace.get("underway") or [], "stop_history": trace.get("stop_history")}
    if trace.get("rulings"):
        state["rulings"] = trace["rulings"]
    return {k: v for k, v in state.items() if v is not None}


responses, state, total, skip = [], {}, 0.0, 0
if "--branch" in sys.argv:
    earlier, keep = sys.argv[sys.argv.index("--branch") + 1].rsplit(":", 1)
    skip = int(keep)
    responses = json.load(open(earlier))[:skip]
    state = carry(responses[-1].get("result") or responses[-1])
    total = sum((r.get("result") or r).get("cost_usd") or 0.0 for r in responses)
for number, decided in enumerate(answers, 1):
    if number <= skip:
        continue
    body = {"bundle": bundle, "causal_model": rules, "approved": True, "policy": "resident", "turns": 1,
            "world": label, "briefs": briefs, "judge_rulings": setting,
            "run_stop": {"mode": "quiet", "quiet_rounds": 6}, **state}
    if decided:
        body["decisions"] = [{"id": i, "decision": d} for i, d in decided]
    out = call("/run", body)
    while out.get("job_id") and out.get("status") == "running":
        time.sleep(4)
        out = call("/jobs/" + out["job_id"])
    res = out.get("result") or out
    responses.append(out)
    if not res.get("trace"):
        print("round", number, "failed:", res.get("error") or out.get("error"), flush=True)
        break
    cost = res.get("cost_usd") or 0.0
    total += cost
    trace = res["trace"]
    state = carry(res)
    print(f"round {number}: trace {res['trace_id']} cost {cost:.6f}", flush=True)
    for turn in trace["transcript"]:
        for actor, row in turn["actors"].items():
            j = row.get("judge") or {}
            print(f"   {actor}: status={row.get('status')} did={(row.get('did') or {}).get('kind')} "
                  f"judge={j.get('outcome')}/{(j.get('disposition') or {}).get('status')} ruling={row.get('ruling')}", flush=True)
        for e in turn.get("ruling_events") or []:
            print("   decision:", json.dumps(e)[:300], flush=True)
        for r in turn.get("rulings") or []:
            print(f"   {r['id']}: {r['status']} {r.get('kind')} attempts={[(a['actor'], a['state']) for a in r['attempts']]}", flush=True)
json.dump(responses, open(out_path, "w"), indent=1)
print("total cost", round(total, 6), flush=True)
if "--share" in sys.argv:
    ids = [(r.get("result") or r)["trace_id"] for r in responses if (r.get("result") or r).get("trace_id")]
    shared = call("/share", {"build_trace_id": None, "run_trace_ids": ids})
    print("share", shared.get("share_id"), "rounds", shared.get("rounds"), flush=True)
