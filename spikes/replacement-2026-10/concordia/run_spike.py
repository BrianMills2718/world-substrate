#!/usr/bin/env python3
"""Replacement-first spike: Concordia as host for World Substrate's governed-rules layer.

Variant 1 (compose): Concordia's Sequential engine, EntityAgentWithLogging
entities and SwitchAct game master own the loop; the GM resolution component
calls World Substrate's Engine.submit as the only consequence authority.
Variant 2 (replace): the same Concordia loop, but the rules-as-data mechanics
are interpreted inside a Concordia GM component with no World Substrate Engine.

Zero LLM spend: Concordia's NoLanguageModel is passed wherever a model object is
required; every model-dependent path is pre-empted by a component output.
Exit status is nonzero if any pass/fail check fails.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from concordia.agents import entity_agent_with_logging
from concordia.components.agent import scripted_act
from concordia.components.game_master import event_resolution, make_observation
from concordia.components.game_master import next_acting, switch_act, terminate
from concordia.environment.engines import sequential
from concordia.language_model import no_language_model
from concordia.typing import entity as entity_lib
from concordia.typing import entity_component

from scripts.run_authored_world import build_engine
from scripts.run_native_coordination import (
    _authorized_member,
    _entity_with_category,
    _report_plan,
    _required_approvals,
    run_native_coordination,
)
from scripts.scaffold_world import load_bundle

BUNDLE = REPO / "examples/native_coordination/constrained-handoff-v0.json"
CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"
class CountingNoLanguageModel(no_language_model.NoLanguageModel):
    """Concordia's no-op model, counting calls so the run proves no model path was taken."""

    calls = 0

    def sample_text(self, *args: Any, **kwargs: Any) -> str:
        CountingNoLanguageModel.calls += 1
        return super().sample_text(*args, **kwargs)

    def sample_choice(self, *args: Any, **kwargs: Any):
        CountingNoLanguageModel.calls += 1
        return super().sample_choice(*args, **kwargs)


MODEL = CountingNoLanguageModel()
CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    CHECKS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


# --- shared: scripted actor intents (same trajectory as run_native_coordination) ---
def scripted_plan(bundle: dict[str, Any]) -> list[tuple[str, dict[str, str], str]]:
    gate = _entity_with_category(bundle, "gate")
    prereqs = {f"prereq_{x}": _entity_with_category(bundle, f"prereq-{x}") for x in "abcd"}
    authorized = _authorized_member(bundle)
    reports = _report_plan(bundle)
    plan = [
        (src, {"kind": "communicate", "information": info, "delivery": dlv, "recipient": rcp}, "accepted")
        for src, info, dlv, rcp in reports
    ]
    voters = [rcp for *_, rcp in reports]
    plan.append((voters[0], {"kind": "approve", "gate": gate, **prereqs}, "precondition_failed"))
    plan.append((authorized, {"kind": "intervene", "resource": _entity_with_category(bundle, "restorable")}, "accepted"))
    for voter in voters[: _required_approvals(bundle)]:
        plan.append((voter, {"kind": "approve", "gate": gate, **prereqs}, "accepted"))
    plan.append((authorized, {"kind": "finalize", "gate": gate, **prereqs}, "accepted"))
    return plan


# --- concordia glue (used by both variants) ---
class _Component(entity_component.ContextComponent):
    def get_state(self) -> dict[str, Any]:
        return {}

    def set_state(self, state: dict[str, Any]) -> None:
        pass


class ResolveViaAuthority(_Component):
    """GM resolution step: hand the putative event to an authority; narrate its verdict only."""

    def __init__(self, authority: Any):
        super().__init__()
        self._authority, self._putative, self.records = authority, "", []

    def pre_observe(self, observation: str) -> str:
        if observation.startswith(event_resolution.PUTATIVE_EVENT_TAG):
            self._putative = observation[len(event_resolution.PUTATIVE_EVENT_TAG):].strip()
        return ""

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        if action_spec.output_type != entity_lib.OutputType.RESOLVE:
            return ""
        actor, _, payload = self._putative.partition(" ")
        record = self._authority(actor, json.loads(payload))
        self.records.append(record)
        return (f"{actor} {record['kind']}: {record['status']}; failed={record['failed']}; "
                f"event={record['event_id']} cause={record['cause']}")


class LastEventObservation(_Component):
    def __init__(self, resolver: ResolveViaAuthority):
        super().__init__()
        self._resolver = resolver

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        if action_spec.output_type != entity_lib.OutputType.MAKE_OBSERVATION or not self._resolver.records:
            return ""
        return json.dumps(self._resolver.records[-1], sort_keys=True)


class TerminalPredicate(_Component):
    def __init__(self, reached: Any):
        super().__init__()
        self._reached = reached

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        if action_spec.output_type != entity_lib.OutputType.TERMINATE:
            return ""
        return "Yes" if self._reached() else "No"


def run_concordia_loop(plan, authority, reached) -> tuple[list[dict[str, Any]], list[Any]]:
    script = [{"name": actor, "line": json.dumps(intent, sort_keys=True)} for actor, intent, _ in plan]
    actors = sorted({actor for actor, _, _ in plan})
    entities = [
        entity_agent_with_logging.EntityAgentWithLogging(
            agent_name=name, act_component=scripted_act.ScriptedActComponent(MODEL, script))
        for name in actors
    ]
    resolver = ResolveViaAuthority(authority)
    gm = entity_agent_with_logging.EntityAgentWithLogging(
        agent_name="governed-gm",
        act_component=switch_act.SwitchAct(MODEL, entity_names=actors),
        context_components={
            next_acting.DEFAULT_NEXT_ACTING_COMPONENT_KEY: next_acting.NextActingInFixedOrder([a for a, _, _ in plan]),
            next_acting.DEFAULT_NEXT_ACTION_SPEC_COMPONENT_KEY: next_acting.FixedActionSpec(
                entity_lib.ActionSpec(call_to_action="Intent JSON for {name}?", output_type=entity_lib.OutputType.FREE)),
            event_resolution.DEFAULT_RESOLUTION_COMPONENT_KEY: resolver,
            make_observation.DEFAULT_MAKE_OBSERVATION_COMPONENT_KEY: LastEventObservation(resolver),
            terminate.DEFAULT_TERMINATE_COMPONENT_KEY: TerminalPredicate(reached),
        },
    )
    log: list[Any] = []
    sequential.Sequential().run_loop(game_masters=[gm], entities=entities, max_steps=len(plan) + 2, log=log)
    return resolver.records, log
# --- end concordia glue ---


# --- variant 1 glue: World Substrate Engine is the sole consequence authority ---
def engine_authority(engine: Any):
    def submit(actor: str, intent: dict[str, str]) -> dict[str, Any]:
        page = engine.discover(actor, kind=intent["kind"])
        fields = {k: v for k, v in intent.items() if k != "kind"}
        rows = [r for r in [*page["available"], *page["blocked"]]
                if all(r["action"].get(k) == v for k, v in fields.items())]
        if len(rows) != 1:
            raise AssertionError(f"intent matched {len(rows)} discovered actions: {actor} {intent}")
        action = dict(rows[0]["action"], controller="native-coordination-fixture")
        outcome = engine.submit(action)
        event = outcome["event"]
        return {"actor": actor, "kind": intent["kind"], "status": outcome["status"],
                "failed": [c["label"] for c in event.get("checks", []) if not c.get("ok")],
                "event_id": event["event_id"], "cause": event.get("cause")}
    return submit
# --- end variant 1 glue ---


# --- variant 2: rules-as-data interpreted natively inside a Concordia GM component ---
class NativeRulesState:
    """Everything here is code we would have to write; Concordia supplies no rule/check/commit primitive."""

    OPS = {"eq": lambda a, b: a == b, "lt": lambda a, b: a < b, "gte": lambda a, b: a >= b}

    def __init__(self, bundle: dict[str, Any], causal: dict[str, Any]):
        self.state = {e["id"]: deepcopy(e) for e in bundle["entities"]}
        self.mechanics = {m["action_kind"]: m for m in causal["mechanics"]}
        self.terminal = causal["terminal"]
        self.events: list[dict[str, Any]] = []

    @staticmethod
    def _get(row: dict[str, Any], path: str) -> Any:
        for part in path.split("."):
            row = row[part]
        return row

    def _value(self, ref: dict[str, Any], state: dict[str, Any], binding: dict[str, str]) -> Any:
        if "literal" in ref:
            return ref["literal"]
        if "entity_id" in ref:
            return binding[ref["entity_id"]]
        p = ref["participant"]
        return self._get(state[binding[p["name"]]], p["path"])

    @staticmethod
    def _selected(row: dict[str, Any], selector: dict[str, Any]) -> bool:
        return set(selector["categories"]) <= set(row.get("categories", [])) and \
            set(selector["components"]) <= set(row.get("components", {}))

    def __call__(self, actor: str, intent: dict[str, str]) -> dict[str, Any]:
        mech = self.mechanics[intent["kind"]]
        binding = {"actor": actor, **{k: v for k, v in intent.items() if k != "kind"}}
        checks = [("Actor matches selector", self._selected(self.state[actor], mech["actor_selector"]))]
        checks += [(f"{name} matches selector", self._selected(self.state[binding[name]], sel))
                   for name, sel in mech["participants"].items()]
        checks += [(c["label"], self.OPS[c["op"]](self._value(c["left"], self.state, binding),
                                                   self._value(c["right"], self.state, binding)))
                   for c in mech["checks"]]
        failed = [label for label, ok in checks if not ok]
        event_id = f"n{len(self.events) + 1:04d}"
        if not failed:  # atomic commit: apply all effects to a copy, then swap
            draft = deepcopy(self.state)
            for eff in mech["effects"]:
                target, *head, last = [binding[eff["participant"]], *eff["path"].split(".")]
                holder = self._get(draft[target], ".".join(head))
                value = self._value(eff["value"], self.state, binding)
                holder[last] = holder[last] + value if eff["op"] == "add" else value
            self.state = draft
        record = {"actor": actor, "kind": intent["kind"], "status": "precondition_failed" if failed else "accepted",
                  "failed": failed, "event_id": event_id, "cause": f"intent:{actor}:{intent['kind']}"}
        self.events.append(record)
        return record

    def reached(self) -> bool:
        rows = [r for r in self.state.values() if self._selected(r, self.terminal["selector"])]
        return bool(rows) and all(self.OPS[c["op"]](self._get(r, c["path"]), c["value"])
                                  for r in rows for c in self.terminal["checks"])
# --- end variant 2 ---


def glue_loc() -> dict[str, int]:
    counts: dict[str, int] = {}
    section = None
    for line in Path(__file__).read_text().splitlines():
        s = line.strip()
        if s.startswith("# --- end"):
            section = None
        elif s.startswith("# --- "):
            section = s[6:].split(":")[0].split(" (")[0].strip(" -")
        elif section and s and not s.startswith("#"):
            counts[section] = counts.get(section, 0) + 1
    return counts


def main() -> int:
    print(f"concordia gdm-concordia=={importlib.metadata.version('gdm-concordia')}")
    bundle = load_bundle(BUNDLE)
    causal = json.loads(CAUSAL.read_text())
    plan = scripted_plan(bundle)

    # Reference: World Substrate's own scripted loop on the same inputs.
    ref = run_native_coordination(load_bundle(BUNDLE), json.loads(CAUSAL.read_text()))
    ref_world = ref["engine"].world
    ref_hash, ref_events = sha(ref_world.material_dict()), len(ref_world.events)
    print(f"reference run_native_coordination: events={ref_events} material_sha256={ref_hash}")

    print("\n== Variant 1 (compose): Concordia loop, World Substrate Engine as sole authority ==")
    engine, causal_model, _ = build_engine(bundle, causal)
    records, log = run_concordia_loop(plan, engine_authority(engine),
                                      lambda: causal_model.terminal.reached(engine.world))
    for r in records:
        print(f"  {r['actor']:>4} {r['kind']:<11} {r['status']:<19} event={r['event_id']} cause={r['cause']} failed={r['failed']}")
    refused = [r for r in records if r["status"] == "precondition_failed"]
    check("v1 statuses match scripted expectations", [r["status"] for r in records] == [e for *_, e in plan])
    check("v1 refused approval recorded with failed check + cause",
          len(refused) == 1 and refused[0]["kind"] == "approve" and refused[0]["failed"] and refused[0]["cause"],
          f"{refused[0]['actor']} failed={refused[0]['failed']} cause={refused[0]['cause']}" if refused else "none")
    gate = _entity_with_category(bundle, "gate")
    gate_status = engine.world.material_dict()["entities"][gate]["components"]["gate"]["status"]
    check("v1 gate reaches ready", gate_status == "ready", f"gate={gate_status}")
    v1_hash, v1_events = sha(engine.world.material_dict()), len(engine.world.events)
    print(f"  v1: events={v1_events} material_sha256={v1_hash} concordia_log_entries={len(log)}")
    check("v1 event count equals reference", v1_events == ref_events, f"{v1_events} vs {ref_events}")
    check("v1 material sha256 equals reference", v1_hash == ref_hash)
    check("v1 every Engine event came from a GM resolution call",
          [e["event_id"] for e in engine.world.events] == [r["event_id"] for r in records])

    print("\n== Variant 2 (replace): rules-as-data interpreted in a Concordia GM component, no Engine ==")
    native = NativeRulesState(load_bundle(BUNDLE), causal)
    records2, _ = run_concordia_loop(plan, native, native.reached)
    for r in records2:
        print(f"  {r['actor']:>4} {r['kind']:<11} {r['status']:<19} failed={r['failed']}")
    check("v2 statuses match scripted expectations", [r["status"] for r in records2] == [e for *_, e in plan])
    r2 = [r for r in records2 if r["status"] == "precondition_failed"]
    check("v2 refused approval names failed check", bool(r2) and r2[0]["failed"] == refused[0]["failed"] if refused else False,
          f"{r2[0]['failed'] if r2 else None}")
    check("v2 gate reaches ready", native.state[gate]["components"]["gate"]["status"] == "ready")
    ref_components = {k: v.get("components") for k, v in ref_world.material_dict()["entities"].items()}
    v2_components = {k: v.get("components") for k, v in native.state.items()}
    check("v2 final entity components equal reference Engine's", v2_components == ref_components,
          f"v2_sha={sha(v2_components)[:16]} ref_sha={sha(ref_components)[:16]}")
    print("  v2 NOT provided (absent from native component): revision/base_revision staleness check, "
          "declared write-scope enforcement, discover() available/blocked affordances, read-path recording, "
          "before/after material snapshots, mechanic profile id, compiler validation of rules data, "
          "projection/replay hooks")

    print("\n== Concern ownership (variant 1) ==")
    print("  Concordia: entities, game master, turn order (NextActingInFixedOrder), action-spec prompting, "
          "putative->resolve event flow, observation fan-out, termination polling, run log")
    print("  World Substrate: rules compilation, discovery/authority checks, approval threshold, atomic "
          "commit/refusal, causal event + cause ids, terminal predicate, material state")
    check("zero language-model calls (NoLanguageModel never sampled)", CountingNoLanguageModel.calls == 0,
          f"calls={CountingNoLanguageModel.calls}")
    print(f"\nglue_loc {json.dumps(glue_loc(), sort_keys=True)}")
    failed = [c for c in CHECKS if not c[1]]
    print(f"\nRESULT checks={len(CHECKS)} passed={len(CHECKS) - len(failed)} failed={len(failed)} "
          f"exit={1 if failed else 0}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
