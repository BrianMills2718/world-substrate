#!/usr/bin/env python3
"""Layer 2 runtime (Decision 007): LLM residents on Concordia, World Substrate Engine as sole authority.

Each resident is a Concordia EntityAgentWithLogging whose acting component makes
one typed, traced llm_client call. Residents wake only when a categorical field
in their own observation changes or their offered actions change (architecture:
cognition wakes on meaningful observations, not every tick). An attempt is an
Engine action offered by discovery, whose checks express permissibility only;
feasibility plays out through autonomous processes on later ticks. Residents
learn outcomes only through their next observation. Every state change is an
Engine event (submit or advance); nothing else mutates the world.

Attempt records use the observation-to-action vocabulary: belief + belief_as_of,
decision, performed (event id/status), expected effect, and observed effect
(filled from the next observation).

Run (from repo root):
  PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 --with gdm-concordia==2.4.0 \
    --with-editable ~/code/llm_client python spikes/any-scenario-2026-10/run_scenario.py --model-dir <run dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from concordia.agents import entity_agent_with_logging  # noqa: E402
from concordia.typing import entity as entity_lib  # noqa: E402
from concordia.typing import entity_component  # noqa: E402

from scripts.run_authored_world import build_engine  # noqa: E402
from world_substrate.mechanisms.time import ClockAdvanceProcess  # noqa: E402

sys.path.insert(0, str(HERE))
from spend import CAP, plan_spend as plan_spend_total  # noqa: E402

RESIDENT_MODEL = "openrouter/openai/gpt-5.6-luna"


class Attempt(BaseModel):
    belief: str = Field(description="What you believe about your situation right now, in one or two sentences.")
    cited_observations: list[str] = Field(description="The exact observed facts (label.field: value) your belief rests on.")
    choice: Literal["offered", "continue", "unlisted"] = Field(
        description="'offered' to attempt one offered action, 'continue' to keep doing what you are doing, "
        "'unlisted' to attempt something not in the offered list.")
    offered_index: int | None = Field(default=None, description="Index into offered actions when choice is 'offered'.")
    unlisted_intent: str | None = Field(default=None, description="Plain description of the attempt when choice is 'unlisted'.")
    expected_effect: str = Field(description="What you expect to happen as a result.")


def flat_fields(observation: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for eid, ent in observation.get("entities", {}).items():
        label = ent.get("label", eid)
        for comp, fields in (ent.get("components") or {}).items():
            if isinstance(fields, dict):
                for k, v in fields.items():
                    out[f"{label}.{k}"] = v
    return out


def wake_signature(fields: dict[str, Any], offered: list[dict[str, Any]]) -> str:
    categorical = sorted((k, v) for k, v in fields.items() if isinstance(v, (str, bool)))
    kinds = sorted(r["action"]["kind"] for r in offered)
    return hashlib.sha256(json.dumps([categorical, kinds]).encode()).hexdigest()


def describe_action(row: dict[str, Any], labels: dict[str, str]) -> str:
    a = row["action"]
    args = {k: labels.get(v, v) for k, v in a.items() if k not in {"actor", "kind", "base_revision", "controller"}}
    return f"{a['kind']}({', '.join(f'{k}={v}' for k, v in args.items())})"


class ObservationLog(entity_component.ContextComponent):
    """Concordia context component: keeps the resident's own observations, newest last."""

    def __init__(self, keep: int = 6):
        super().__init__()
        self._items: list[str] = []
        self._keep = keep

    def pre_observe(self, observation: str) -> str:
        self._items.append(observation)
        self._items = self._items[-self._keep:]
        return ""

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        return "\n---\n".join(self._items)

    def get_state(self) -> dict[str, Any]:
        return {"items": list(self._items)}

    def set_state(self, state: dict[str, Any]) -> None:
        self._items = list(state.get("items", []))


class LLMAttemptAct(entity_component.ActingComponent):
    """Concordia acting component: one typed llm_client call returns an Attempt as JSON."""

    def __init__(self, actor_label: str, trace_id: str, max_budget: float, situation: str = ""):
        super().__init__()
        self._label, self._trace, self._budget, self._situation = actor_label, trace_id, max_budget, situation
        self.cost = 0.0
        self.calls = 0

    def get_action_attempt(self, context: Any, action_spec: entity_lib.ActionSpec) -> str:
        from llm_client import call_llm_structured

        memory = "\n".join(str(v) for v in context.values())
        messages = [
            {"role": "system", "content": (
                f"You are {self._label}, a person inside this situation: {self._situation} You know only what you have "
                "observed. Decide what to attempt now. You may attempt an offered action, keep doing what you "
                "are already doing ('continue'), or attempt something not offered ('unlisted'). Offered actions "
                "are only those you are allowed to begin; whether they succeed is not guaranteed.")},
            {"role": "user", "content": f"Your observations (newest last):\n{memory}\n\n{action_spec.call_to_action}"},
        ]
        attempt, result = call_llm_structured(
            RESIDENT_MODEL, messages, Attempt, task="world-substrate-resident-attempt",
            trace_id=self._trace, max_budget=self._budget, reasoning_effort="low", num_retries=1)
        self.cost += float(getattr(result, "cost", 0.0) or 0.0)
        self.calls += 1
        return attempt.model_dump_json()

    def get_state(self) -> dict[str, Any]:
        return {}

    def set_state(self, state: dict[str, Any]) -> None:
        pass


def run(model_dir: Path, *, max_ticks: int, run_budget: float, quiet_ticks: int,
        unlisted_handler: Any = None, situation_override: str | None = None,
        conditions: list[str] | None = None, game_master: bool = True) -> Path:
    bundle = json.loads((model_dir / "bundle.json").read_text())
    causal = json.loads((model_dir / "causal.json").read_text())
    applied = []
    for cond in conditions or []:  # Decision 005 step 6: change one supported condition, recorded on the run
        target, value = cond.split("=", 1)
        eid, comp, field = target.split(".")
        ent = next(e for e in bundle["entities"] if e["id"] == eid)
        old = ent["components"][comp][field]
        ent["components"][comp][field] = type(old)(json.loads(value)) if not isinstance(old, str) else value
        applied.append({"field": target, "from": old, "to": ent["components"][comp][field]})
    sensing_path = model_dir / "sensing.json"
    sensing = json.loads(sensing_path.read_text()) if sensing_path.exists() else None
    spent = plan_spend_total()[1]
    if spent + run_budget > CAP:
        raise SystemExit(f"plan spend cap: spent ${spent:.4f} + run budget ${run_budget:.2f} > ${CAP:.2f}")
    engine, causal_model, profile_id = build_engine(bundle, causal)
    gm = None
    if game_master and unlisted_handler is None:
        from midrun import MidRunGameMaster
        model_json = json.loads((model_dir / "model.json").read_text()) if (model_dir / "model.json").exists() else {}
        gm = MidRunGameMaster(bundle, causal, model_json.get("stock_map") or [],
                              scenario=model_json.get("scenario_text", ""), trace_id=f"any-scenario-gm-{model_dir.name}")
        unlisted_handler = gm
    engine.registry.register_process(ClockAdvanceProcess())  # existing Engine clock: one tick per advance
    stamp = time.strftime("%Y%m%dT%H%M%S")
    out = model_dir / f"run-{stamp}"
    out.mkdir()
    run_id = f"{model_dir.name}/run-{stamp}"
    trace_id = f"any-scenario-run-{model_dir.name}-{stamp}"
    labels = {e["id"]: e.get("label", e["id"]) for e in bundle["entities"]}
    actors = [e["id"] for e in bundle["entities"] if "actor" in e.get("categories", [])]
    model_path = model_dir / "model.json"
    situation = json.loads(model_path.read_text()).get("scenario_text", "") if model_path.exists() else ""
    if situation_override:
        situation = situation_override
    acts = {a: LLMAttemptAct(labels[a], trace_id, run_budget, situation) for a in actors}
    residents = {
        a: entity_agent_with_logging.EntityAgentWithLogging(
            agent_name=labels[a], act_component=acts[a], context_components={"observations": ObservationLog()})
        for a in actors
    }
    events: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    last_sig: dict[str, str | None] = {a: None for a in actors}
    last_tick_sig: dict[str, str | None] = {a: None for a in actors}
    last_fields: dict[str, dict[str, Any]] = {a: {} for a in actors}
    pending_expect: dict[str, dict[str, Any]] = {}
    quiet = 0
    tick_rows: list[dict[str, Any]] = []
    ended = "max_ticks"
    t_run = time.time()
    for _ in range(max_ticks):
        n_events_before = len(events)
        tick = engine.world.tick
        woke = False
        for a in actors:
            page = engine.discover(a)
            offered = page["available"]
            fields = flat_fields(page["observation"])
            if sensing is not None:  # observation authority: only what the ODD says this actor can sense
                fields = {k: v for k, v in fields.items() if k in set(sensing.get(a, []))}
            sig = wake_signature(fields, offered)
            prev_sig, last_tick_sig[a] = last_tick_sig[a], sig
            if sig == prev_sig and a not in pending_expect:  # nothing changed and no attempt awaiting its outcome
                continue
            woke = True
            changed = {k: [last_fields[a].get(k), v] for k, v in fields.items() if last_fields[a].get(k) != v}
            if a in pending_expect:  # observed effect of the previous attempt, from this observation only
                pending_expect[a]["observed_effect"] = {
                    k: v for k, v in changed.items() if isinstance(v[1], (str, bool))} or "no categorical change"
                pending_expect.pop(a)
            last_sig[a], last_fields[a] = sig, fields
            obs_text = (f"Tick {tick}. What you observe: " + json.dumps(fields, sort_keys=True)
                        + "\nChanged since you last looked: " + json.dumps(changed, sort_keys=True))
            residents[a].observe(obs_text)
            menu = [describe_action(r, labels) for r in offered]
            spec = entity_lib.ActionSpec(
                call_to_action="Offered actions (index: action): " + json.dumps(dict(enumerate(menu))),
                output_type=entity_lib.OutputType.FREE)
            raw = residents[a].act(spec)
            attempt = json.loads(raw)
            record = {"tick": tick, "actor": a, "belief": attempt["belief"], "belief_as_of": tick,
                      "cited_observations": attempt["cited_observations"], "decision": attempt["choice"],
                      "expected_effect": attempt["expected_effect"], "offered": menu}
            if attempt["choice"] == "offered" and attempt.get("offered_index") is not None \
                    and 0 <= attempt["offered_index"] < len(offered):
                action = dict(offered[attempt["offered_index"]]["action"], controller="llm-resident")
                outcome = engine.submit(action)
                ev = outcome["event"]
                events.append(ev)
                record["performed"] = {"action": menu[attempt["offered_index"]], "status": outcome["status"],
                                       "event_id": ev["event_id"], "action_record": action}
            elif attempt["choice"] == "unlisted":
                record["unlisted_intent"] = attempt.get("unlisted_intent")
                if unlisted_handler is not None:
                    record["performed"] = unlisted_handler(engine, a, attempt.get("unlisted_intent") or "", events)
                else:
                    record["performed"] = {"status": "no_rule", "event_id": None}
            else:
                record["performed"] = {"status": "continue", "event_id": None}
            attempts.append(record)
            if record["performed"].get("event_id"):  # only real attempts await an observed outcome
                pending_expect[a] = record
            print(f"[tick {tick}] {labels[a]}: {record['decision']} -> {record['performed']}", flush=True)
        adv = engine.advance(1)
        events.extend(adv.get("events", []))
        tick_rows.append({"tick": tick, "world_changes": [e["rule_id"] for e in adv.get("events", [])
                                                           if e["rule_id"] != ClockAdvanceProcess.rule_id]})
        if causal_model.terminal is not None and causal_model.terminal.reached(engine.world):
            ended = "terminal"
            break
        material = [e for e in adv.get("events", []) if e.get("rule_id") != ClockAdvanceProcess.rule_id]
        # progress = the world changed (a process event, or an attempt whose event changed component state);
        # a resident repeating an action that changes nothing is not progress (audit finding: 178 such calls)
        changed_by_attempt = any(any(".components." in c["path"] for c in e.get("changes", []))
                                 for e in events[n_events_before:] if e.get("causal_bearer", {}).get("kind") != "process")
        quiet = 0 if (material or changed_by_attempt) else quiet + 1
        if quiet >= quiet_ticks:
            ended = "quiescent"
            break
        cost = sum(x.cost for x in acts.values())
        if cost > run_budget:
            ended = "run_budget"
            break
    cost = sum(x.cost for x in acts.values())
    summary = {"conditions_changed": applied, "situation_briefing": situation, "run_id": run_id, "trace_id": trace_id, "profile_id": profile_id, "ended": ended,
               "final_tick": engine.world.tick, "events": len(events), "attempts": len(attempts),
               "resident_calls": sum(x.calls for x in acts.values()), "cost": cost,
               "seconds": round(time.time() - t_run, 1), "plan_spend_after": plan_spend_total()[1]}
    (out / "events.jsonl").write_text("\n".join(json.dumps(e, sort_keys=True) for e in events) + "\n")
    (out / "attempts.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in attempts) + "\n")
    (out / "final_world.json").write_text(json.dumps(engine.observe(actors[0]), indent=2, sort_keys=True))
    if gm is not None:
        summary["rules_written_mid_run"] = gm.written
        (out / "causal_after_run.json").write_text(json.dumps(gm.causal, indent=2, sort_keys=True))
        (out / "bundle_after_run.json").write_text(json.dumps(gm.bundle, indent=2, sort_keys=True))
    (out / "ticks.json").write_text(json.dumps(tick_rows))
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))
    print("[done] " + json.dumps(summary, sort_keys=True))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True, type=Path)
    ap.add_argument("--max-ticks", type=int, default=200)
    ap.add_argument("--run-budget", type=float, default=0.50)
    ap.add_argument("--quiet-ticks", type=int, default=25)
    ap.add_argument("--situation", help="scenario text the residents are briefed on (default: the modeled text)")
    ap.add_argument("--set", action="append", default=[], help="entity.component.field=value initial-state change")
    ap.add_argument("--no-gm", action="store_true", help="disable mid-run rule writing (uncovered attempts do nothing)")
    args = ap.parse_args()
    run(args.model_dir, max_ticks=args.max_ticks, run_budget=args.run_budget, quiet_ticks=args.quiet_ticks,
        situation_override=args.situation, conditions=args.set, game_master=not args.no_gm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
