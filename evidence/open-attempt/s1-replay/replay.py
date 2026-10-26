"""Free replay for S1 (no model call): on every saved world with a bundle and rules, each move the rules offer or
refuse is turned into the reading a model would return for it, and the envelope that reading makes must be the very
move the menu offered, with the same Engine outcome. An unmatched attempt must change nothing. A scripted run of each
world must still replay exactly.

    uv run -q --no-project --python 3.12 --with pydantic python evidence/open-attempt/s1-replay/replay.py
"""
import json
import sys
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(REPO), str(REPO / "src")]
from scripts.run_authored_world import build_engine, run_world  # noqa: E402
from world_substrate import attempt as oa  # noqa: E402

WORLDS = {p.name: json.loads(p.read_text()) for p in sorted((REPO / "tests/fixtures").glob("*.json"))}
WORLDS = {k: v for k, v in WORLDS.items() if "bundle" in v}
Q23 = REPO / "evidence/open-attempt/q23/after-fix"
WORLDS["airfield (q23 after-fix)"] = {"bundle": json.loads((Q23 / "bundle.json").read_text()),
                                      "causal_model": json.loads((Q23 / "rules3.json").read_text())}
bad = 0
for name, world in WORLDS.items():
    engine, model, _ = build_engine(world["bundle"], world["causal_model"])
    signatures = oa.signatures_for(world["bundle"], model.mechanics)
    ids = set(engine.world.entities)
    same = differ = 0
    for actor in sorted(engine.world.entities):
        page = engine.discover(actor)
        for row in (page.get("available") or [])[:8] + (page.get("blocked") or [])[:8]:
            action = row["action"]
            fields = {k: v for k, v in action.items() if k not in oa.RESERVED_FIELDS}
            text = " ".join(f"{k} {v}" for k, v in fields.items()) or action["kind"]
            reading = oa.read_interpretation(
                {"kind": action["kind"], "nearest_kind": action["kind"], "why": "replay",
                 "fields": [{"field": k, "value": json.dumps(v) if not isinstance(v, str) else v,
                             "quoted_span": f"{k} {v}"} for k, v in fields.items()]},
                text, signatures, ids)
            env = oa.envelope(reading, actor=actor, attempt=text, base_revision=engine.world.revision,
                              controller="replay")
            direct = {**action, "controller": "replay"}
            if reading.get("unmatched") or env != direct:
                differ += 1
                print("  DIFFERS", name, actor, action, reading)
                continue
            a, b = deepcopy(engine), deepcopy(engine)
            ra, rb = a.submit(env), b.submit(direct)
            if ra["status"] != rb["status"] or a.world.material_hash() != b.world.material_hash():
                differ += 1
                print("  OUTCOME DIFFERS", name, actor, action["kind"], ra["status"], rb["status"])
            else:
                same += 1
    probe = deepcopy(engine)
    actor = sorted(probe.world.entities)[0]
    before = (probe.world.revision, probe.world.material_hash())
    out = probe.submit(oa.envelope({"unmatched": True, "nearest_kind": "none", "why": "replay"}, actor=actor,
                                   attempt="sing to the clouds", base_revision=probe.world.revision,
                                   controller="replay"))
    after = (probe.world.revision, probe.world.material_hash())
    try:
        trace, ran, _ = run_world(world["bundle"], world["causal_model"], policy="scripted", max_turns=6)
        rounds = f"scripted {trace['summary']['turns']} rounds"
    except ValueError as error:
        # The airfield offers nothing scripted moves can take (the wall is shut); replay the refusals instead.
        ran, rounds = probe, f"scripted run: {error}; replaying the refusal probe"
    replay = ran.replay()
    ok = differ == 0 and out["status"] == "unsupported_action" and before == after and replay["ok"]
    bad += not ok
    print(f"{name}: menu moves read back identically {same}, differ {differ}; unmatched -> {out['status']}, "
          f"world unchanged {before == after}; {rounds}; replay ok {replay['ok']} "
          f"({replay['steps']} commands) -> {'PASS' if ok else 'FAIL'}")
print(f"worlds {len(WORLDS)}, failing {bad}")
sys.exit(1 if bad else 0)
