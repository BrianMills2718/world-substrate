"""Judge a live people-world share record for C1 and increment 2 (Concordia residents)."""
import collections
import json
import sys

rec = json.load(open(sys.argv[1]))
world, rounds, runs = rec["world"], rec["rounds"], rec["runs"]
people = sorted({a for t in rounds for a in t["actors"]})
print("build trace", world.get("trace_id"), "kind", world.get("world_kind"), "people", len(people), people)
print("rounds", len(rounds), "first", rounds[0]["turn"], "last", rounds[-1]["turn"])
movers = collections.Counter(r.get("mover") for r in runs)
print("runs", len(runs), "movers", dict(movers), "policies", dict(collections.Counter(r.get("policy") for r in runs)))
print("cost", round(sum(r.get("cost_usd") or 0 for r in runs), 4))

accepted = [(t["turn"], a, row) for t in rounds for a, row in t["actors"].items() if row.get("status") == "accepted"]
asked = [(t["turn"], a, row) for t in rounds for a, row in t["actors"].items() if row.get("wanted")]
no_belief = [(n, a) for n, a, row in asked if not row.get("belief") or not row.get("expects")]
print(f"moves attempted {len(asked)}; accepted {len(accepted)}; attempted moves missing belief or expected effect: {len(no_belief)}",
      no_belief[:5])
first = {p: min((n for n, a, row in accepted if a == p and row.get("changed")), default=None) for p in people}
print("first real move per person", first, "all within 20:", all(v is not None and v <= 20 for v in first.values()))
for lo in range(1, rounds[-1]["turn"] + 1, 10):
    window = [(row.get("did") or {}).get("kind") for n, a, row in accepted if lo <= n < lo + 10 and row.get("changed")]
    c = collections.Counter(window)
    print(f"rounds {lo}-{lo + 9}: {len(window)} real moves, {len(c)} distinct, top {c.most_common(3)}")
kinds = collections.defaultdict(list)
for n, a, row in accepted:
    if row.get("changed"):
        kinds[(row.get("did") or {}).get("kind")].append((row.get("event_id"), a))
for k, v in sorted(kinds.items()):
    print(k, len(v), v[:4])
for t in rounds:
    for e in t.get("world_events") or []:
        print("world", t["turn"], e["event_id"], e["rule_id"])
print("--- sample beliefs (first accepted move per person) ---")
for p in people:
    row = next((row for n, a, row in accepted if a == p), None)
    if row:
        print(p, "|", (row.get("did") or {}).get("kind"), "| believed:", row.get("belief"), "| expected:", row.get("expects"))
print("--- readout ---")
print(json.dumps(rec.get("readout"), indent=1)[:4000])
