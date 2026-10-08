#!/usr/bin/env python3
"""Layer 3 (Decision 007): the game master writes a rule mid-run when a resident attempts something no rule covers.

Flow for one uncovered attempt:
1. the rule writer proposes a general rule (or rules) for that KIND of attempt, in the World Substrate rule language;
2. the proposal is checked with the layer-1 checks on the whole model (static + simulation; conservation included);
3. pass  -> the new rule is compiled, installed into the RUNNING Engine's registry, and the attempt is submitted
            through Engine.submit; the event is marked "written mid-run";
   fail  -> one-off ruling: the attempt is recorded through Engine.submit as an unsupported action (no state change),
            with the game master's stated reason and the failing findings.
Every rule written is kept in the run record for human review after the run (keep or drop).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src"), str(HERE)]

from checks import run_checks  # noqa: E402
from rule_writer import propose_rule  # noqa: E402
from world_substrate.action_authoring import (  # noqa: E402
    CausalModel,
    CompiledActionMechanic,
    CompiledProcessMechanic,
)

RULE_MODEL = "openrouter/openai/gpt-5.6-sol"
RULE_MODEL_WHY = "Mid-run rule writing uses the same stronger tier as layer-1 repairs (luna rules failed to compile)."


class MidRunGameMaster:
    def __init__(self, bundle: dict[str, Any], causal: dict[str, Any], stocks: list[dict[str, Any]], *,
                 scenario: str, trace_id: str):
        self.bundle, self.causal, self.stocks = bundle, causal, stocks
        self.scenario, self.trace_id = scenario, trace_id
        self.baseline = run_checks(bundle, causal, stocks=stocks)["counts"]["blocking"]
        self.written: list[dict[str, Any]] = []

    def _install(self, engine: Any, new_bundle: dict[str, Any], new_causal: dict[str, Any]) -> list[str]:
        model = CausalModel.from_dict(new_causal, bundle=new_bundle)
        have_actions = set(engine.registry.action_kinds())
        have_processes = {p.rule_id for p in engine.registry.processes()}
        installed = []
        for declared in model.mechanics:
            if declared.action_kind not in have_actions:
                engine.registry.register_action(CompiledActionMechanic(declared))
                installed.append(declared.mechanic_id)
        for order, declared in enumerate(model.processes, start=100):
            if declared.process_id not in have_processes:
                engine.registry.register_process(CompiledProcessMechanic(declared, order))
                installed.append(declared.process_id)
        return installed

    def __call__(self, engine: Any, actor: str, intent: str, events: list[dict[str, Any]]) -> dict[str, Any]:
        n = len(self.written) + 1
        trace = f"{self.trace_id}-gm{n}"
        problem = (f"During a run of the scenario '{self.scenario}', resident {actor} attempted something no rule "
                   f"covers: '{intent}'. Add the general rule(s) for this kind of attempt so any actor in the same "
                   "situation is handled the same way. Prefer add_action (a new action the actor can attempt) and, if "
                   "the outcome takes time, add_process. Use only entities and fields that exist.")
        record: dict[str, Any] = {"intent": intent, "trace_id": trace}
        try:
            new_bundle, new_causal, rec = propose_rule(self.bundle, self.causal, problem, trace_id=trace,
                                                       model=RULE_MODEL, model_justification=RULE_MODEL_WHY)
            record["proposal"] = rec["proposal"]
            report = run_checks(new_bundle, new_causal, stocks=self.stocks)
            new_ids = {c.get("rule", {}).get("mechanic_id") or c.get("rule", {}).get("process_id")
                       for c in rec["proposal"].get("changes", [])}
            own = [f for f in report["findings"] if f["blocking"] and (f.get("rule") in new_ids or f["check"] == "conservation")]
            passed = report["counts"]["blocking"] <= self.baseline and not own
            record["checks"] = {"blocking": report["counts"]["blocking"], "baseline_blocking": self.baseline,
                                "findings_on_new_rule": [f["finding"] for f in own]}
        except ValueError as error:
            passed, record["error"] = False, str(error)
        if passed:
            installed = self._install(engine, new_bundle, new_causal)
            self.bundle, self.causal = new_bundle, new_causal
            kinds = [c["action_signature"]["kind"] for c in rec["proposal"]["changes"] if c.get("change") == "add_action"]
            outcome = None
            for kind in kinds:
                page = engine.discover(actor, kind=kind)
                if page["available"]:
                    outcome = engine.submit(dict(page["available"][0]["action"], controller="llm-resident"))
                    break
            if outcome is None:  # the new rule exists but this actor may not begin it now: recorded refusal
                outcome = engine.submit({"actor": actor, "kind": kinds[0] if kinds else "unlisted", "base_revision":
                                         engine.world.revision, "controller": "llm-resident"})
            events.append(outcome["event"])
            entry = {"status": outcome["status"], "event_id": outcome["event"]["event_id"], "written_mid_run": True,
                     "action_record": {k: v for k, v in (outcome["event"].get("observation") or {}).items()} or None,
                     "action_kind": kinds[0] if kinds else None,
                     "rules_installed": installed, "gm_trace": trace}
        else:
            ruling = engine.submit({"actor": actor, "kind": "gm-ruling", "base_revision": engine.world.revision,
                                    "controller": "game-master"})
            events.append(ruling["event"])
            why = (record.get("checks") or {}).get("findings_on_new_rule") or [record.get("error") or "the checks got worse"]
            entry = {"status": "ruling", "event_id": ruling["event"]["event_id"], "written_mid_run": False,
                     "ruling": "No rule could be added that passes the checks, so the attempt has no effect in this "
                               "world. The proposed rule failed because: " + " ".join(why)[:400],
                     "gm_trace": trace}
        record.update(entry)
        self.written.append(record)
        print(f"[gm] {actor} '{intent[:60]}' -> {entry['status']} written_mid_run={entry['written_mid_run']}", flush=True)
        return entry
