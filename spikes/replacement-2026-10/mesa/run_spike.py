#!/usr/bin/env python3
"""Mesa replacement spike for the constrained-handoff world. Exits nonzero on any failed check."""
from __future__ import annotations

import hashlib
import inspect
import json
import sys
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path[:0] = [str(REPO), str(REPO / "src"), str(HERE)]

import mesa  # noqa: E402

from scripts.run_native_coordination import run_native_coordination  # noqa: E402
from scripts.scaffold_world import load_bundle  # noqa: E402
from world_substrate.action_authoring import CausalModel  # noqa: E402
from v1_compose import HandoffModel  # noqa: E402
from v2_native import NativeHandoffModel, NativeMember  # noqa: E402

BUNDLE = load_bundle(REPO / "examples/native_coordination/constrained-handoff-v0.json")
CAUSAL = json.loads((REPO / "examples/native_coordination/coordination-causal-v0.json").read_text())
FAILURES: list[str] = []


def check(label: str, ok: bool, detail: object = "") -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f" -- {detail}" if detail != "" else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def sha(material: dict) -> str:
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()


def loc(path: Path) -> int:
    return sum(1 for line in path.read_text().splitlines()
               if line.strip() and not line.strip().startswith(("#", '"""')))


def run_v1(max_steps: int = 20) -> HandoffModel:
    model = HandoffModel(deepcopy(BUNDLE), deepcopy(CAUSAL))
    while not model.terminal() and model.steps < max_steps:
        model.step()
    return model


def v1_at(steps: int) -> HandoffModel:
    model = HandoffModel(deepcopy(BUNDLE), deepcopy(CAUSAL))
    for _ in range(steps):
        model.step()
    return model


def v2_at(steps: int | None = None) -> NativeHandoffModel:
    model = NativeHandoffModel(deepcopy(BUNDLE))
    target = model.plan_length if steps is None else steps
    while model.steps < target:
        model.step()
    return model


def variant1() -> HandoffModel:
    print("== Variant 1 (compose): Mesa loop + DataCollector, WS Engine is sole consequence authority")
    model = run_v1()
    events = model.engine.world.events
    refused = [(a, k, o) for a, k, o in model.outcomes if o["status"] != "accepted"]
    check("exactly one refused attempt", len(refused) == 1, [(a, k, o["status"]) for a, k, o in refused])
    if refused:
        actor, kind, outcome = refused[0]
        ev = outcome["event"]
        failed = [c["label"] for c in ev["checks"] if not c["ok"]]
        check("refused approval names failed check and cause",
              kind == "approve" and failed == ["Prerequisite A is healthy"] and bool(ev.get("cause")),
              f"actor={actor} status={ev['status']} failed={failed} cause={ev['cause']} rule={ev['rule_id']} event={ev['event_id']}")
    check("gate reaches ready", model._gate()["status"] == "ready", f"mesa steps={model.steps}")
    ref = run_native_coordination(deepcopy(BUNDLE), deepcopy(CAUSAL))["engine"]
    mesa_hash, ref_hash = sha(model.engine.world.material_dict()), sha(ref.world.material_dict())
    check("final event count equals reference", len(events) == len(ref.world.events),
          f"mesa={len(events)} reference={len(ref.world.events)}")
    check("material_dict sha256 equals reference", mesa_hash == ref_hash, f"mesa={mesa_hash} reference={ref_hash}")
    def strip(evs):
        out = deepcopy(evs)
        for e in out:
            if isinstance(e.get("causal_bearer"), dict):
                e["causal_bearer"].pop("controller", None)
        return out
    check("event log equals reference (controller label ignored)", strip(events) == strip(ref.world.events))
    rep = model.engine.replay()
    check("Engine.replay() reproduces Mesa-driven run", rep["ok"], f"steps={rep['steps']}")
    df = model.datacollector.get_model_vars_dataframe()
    print("  DataCollector model vars:\n" + "\n".join("    " + r for r in df.to_string().splitlines()))
    return model


def native_defect(model: NativeHandoffModel, actor: str, extra) -> None:
    """Run the native approve rule with a defect injected after its first write."""
    member = model.by_actor[actor]
    prereqs = member.intents[5][1]
    def defective(self, gate, **p):
        me, g = self._c(self.actor_id, "member"), self._c(gate, "gate")
        self._require([("Prerequisite A is healthy", True)])
        me["approved"] = True
        extra(self)  # defect point
        g["approval_count"] += 1
    defective(member, **prereqs)


def variant2() -> None:
    print("== Variant 2 (replace): rules hand-written in Mesa agents, no WS Engine")
    model = v2_at()
    gate = model.state[model.gate_id]["gate"]
    refused = [o for o in model.outcomes if o[2] != "accepted"]
    check("gate reaches ready", gate["status"] == "ready", gate)
    check("bad approval refused", len(refused) == 1 and refused[0][1] == "approve"
          and refused[0][3] == ["Prerequisite A is healthy"], refused)
    ws_final = v1_at(7).engine.world.material_dict()["entities"]
    same = all(ws_final[e]["components"] == model.state[e] for e in model.state)
    check("native final components equal WS final components", same)

    print("  -- governed properties (each demonstrated by code) --")
    results = {}

    # P1 atomic commit/refusal: a defect raises after the first write.
    m2 = v2_at(4)
    def boom(_self):
        raise RuntimeError("defect after first write")
    try:
        native_defect(m2, "bo", boom)
    except RuntimeError:
        pass
    partial = m2.state["bo"]["member"]["approved"] is True and m2.state[m2.gate_id]["gate"]["approval_count"] == 0
    ws = v1_at(4).engine
    rule = ws.registry.action("approve")
    orig = rule.apply
    def ws_boom(world, action, event_id):
        orig(world, action, event_id)
        raise RuntimeError("defect after first write")
    rule.apply = ws_boom
    before = sha(ws.world.material_dict())
    action = next(r["action"] for r in ws.discover("bo", kind="approve")["available"])
    try:
        ws.submit(dict(action, controller="mesa-spike"))
    except RuntimeError:
        pass
    ws_atomic = sha(ws.world.material_dict()) == before and not ws.world.entities["bo"].components["member"].approved
    print(f"    P1 atomic: mesa partial mutation persisted={partial}; WS world unchanged after same defect={ws_atomic}")
    results["atomic commit/refusal"] = (not partial, ws_atomic)

    # P2 declared write scope: approve also zeroes link-health (undeclared write).
    m3 = v2_at(4)
    def sabotage(self):
        self.model.state["link-health"]["resource"]["current"] = 0
    native_defect(m3, "bo", sabotage)
    mesa_stopped = m3.state["link-health"]["resource"]["current"] == 1
    ws = v1_at(4).engine
    rule = ws.registry.action("approve")
    orig = rule.apply
    def ws_sabotage(world, action, event_id):
        orig(world, action, event_id)
        world.entities["link-health"].components["resource"].current = 0
    rule.apply = ws_sabotage
    before = sha(ws.world.material_dict())
    action = next(r["action"] for r in ws.discover("bo", kind="approve")["available"])
    out = ws.submit(dict(action, controller="mesa-spike"))
    ws_stopped = out["status"] == "scope_violation" and sha(ws.world.material_dict()) == before
    print(f"    P2 write scope: mesa stopped out-of-scope write={mesa_stopped} (link-health now "
          f"{m3.state['link-health']['resource']['current']}); WS status={out['status']} world unchanged={ws_stopped}")
    results["declared write-scope enforcement"] = (mesa_stopped, ws_stopped)

    # P3 recorded cause: who/what rule/which checks made the gate ready?
    cols = list(model.datacollector.get_model_vars_dataframe().columns)
    mesa_cause = any(k in model.state[model.gate_id] for k in ("last_cause_event_id", "cause")) or "rule_id" in cols
    wsm = v1_at(7).engine
    ent = wsm.world.entities[model.gate_id]
    ev = next(e for e in wsm.world.events if e["event_id"] == ent.last_cause_event_id)
    ws_cause = ev["rule_id"] == "coordination.action.finalize" and ev["cause"] == "c00007"
    print(f"    P3 cause: mesa state/DataCollector carry cause={mesa_cause} (collector columns={cols}); "
          f"WS gate.last_cause_event_id={ent.last_cause_event_id} rule={ev['rule_id']} cause={ev['cause']} "
          f"bearer={ev['causal_bearer']['id']} checks={len(ev['checks'])}")
    results["recorded cause / causal parents"] = (mesa_cause, ws_cause)

    # P4 rules-as-data: an LLM-proposed bad rule must be rejected by a compiler.
    bad = deepcopy(CAUSAL)
    approve = next(m for m in bad["mechanics"] if m["action_kind"] == "approve")
    approve["effects"].append({"participant": "ghost", "path": "components.resource.current",
                               "op": "set", "value": {"literal": 0}})
    try:
        CausalModel.from_dict(bad, bundle=BUNDLE)
        ws_reject, reason = False, "accepted"
    except ValueError as error:
        ws_reject, reason = True, str(error)[:110]
    mesa_data = not inspect.isfunction(NativeMember.approve)
    print(f"    P4 rules-as-data: mesa rule is data={mesa_data} (it is Python source, "
          f"{len(inspect.getsource(NativeMember.approve).splitlines())} lines; a proposal would need exec); "
          f"WS compiler rejected bad proposal={ws_reject}: {reason}")
    results["rules-as-data, compiler-checkable"] = (mesa_data, ws_reject)

    # P5 exact replay: re-execution vs recorded-command replay with status verification.
    rerun_same = v2_at().state_hash() == model.state_hash()
    mesa_log = any(hasattr(model, a) for a in ("commands", "events"))
    rep = wsm.replay()
    print(f"    P5 replay: mesa same-seed re-execution identical={rerun_same}; recorded command log to replay="
          f"{mesa_log}; WS Engine.replay ok={rep['ok']} steps={rep['steps']} event_match={rep['event_match']}")
    results["exact replay of recorded run"] = (rerun_same and mesa_log, rep["ok"])

    print("  property                              | native Mesa | WS Engine")
    for name, (m, w) in results.items():
        print(f"  {name:<37} | {'REPRODUCED' if m else 'LACKING':<11} | {'yes' if w else 'NO'}")
        check(f"WS Engine demonstrates: {name}", w)
    lacking = [n for n, (m, _) in results.items() if not m]
    print(f"  native Mesa lacks {len(lacking)}/{len(results)}: {lacking}"
          + ("  (P5: same-seed re-execution is reproducible, but no recorded log)" if rerun_same and not mesa_log else ""))


def main() -> int:
    print(f"mesa version: {mesa.__version__}")
    variant1()
    variant2()
    print("== Concerns Mesa took over (variant 1): agent objects/registry (AgentSet), activation order "
          "(model.agents.do), step clock (model.steps), seeded RNG (rng=), per-step data collection (DataCollector).")
    print("   WS Engine kept: discover/validate/atomic commit or refusal, write-scope enforcement, events+cause, replay.")
    print(f"== Glue LOC (non-blank, non-comment): v1_compose.py={loc(HERE / 'v1_compose.py')} "
          f"v2_native.py={loc(HERE / 'v2_native.py')}")
    print(f"RESULT: {'PASS' if not FAILURES else 'FAIL'} failures={len(FAILURES)} {FAILURES}")
    return 1 if FAILURES else 0


if __name__ == "__main__":
    sys.exit(main())
