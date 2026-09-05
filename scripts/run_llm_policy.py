#!/usr/bin/env python3
"""Let a policy drive the Castaway world, and record what it did.

Success criterion 2 of the roadmap: the same semantic action interface should be
exercisable by scripted, human, or LLM policies without giving policy prose
consequence authority. Every run before this one used a scripted controller.

The policy only ever returns an `action_id`. `world_substrate.policy` matches it
against the engine's own discovered actions for the current revision, and
anything unmatched is refused and recorded rather than executed. Spend is capped
twice: `max_budget` on every call through the shared client, and a soft ceiling
checked between turns so the run stops before the cap rather than at it.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts._display import display_path

sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.policy import (
    LlmPolicy,
    ScriptedPolicy,
    ThirstyPolicy,
    apply_choice,
    present,
    resolve_choice,
)

OUTPUT = REPO / "evidence/m5/llm-policy-v0.json"
DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"
ACTOR = "robinson"


def _recent(engine, seen: int) -> list[str]:
    lines = []
    for event in engine.world.events[seen:]:
        if event["status"] != "accepted":
            lines.append(f"your {event['rule_id'].split('.')[-1]} was refused")
            continue
        for change in event["changes"]:
            if change["path"].endswith("actor.hydration") and ACTOR in change["path"]:
                lines.append(f"hydration {change['before']} -> {change['after']}")
            if change["path"].endswith("actor.health") and ACTOR in change["path"]:
                lines.append(f"health {change['before']} -> {change['after']}")
            if change["path"].endswith("liquid.pathogens") and change["after"] == 0:
                lines.append("the water in the pot is no longer contaminated")
    return lines[-4:]


def run(policy, turns: int, soft_cap: float | None, trace_id: str) -> dict[str, object]:
    engine = build_transfer_engine(REPO)
    transcript: list[dict[str, object]] = []
    seen_events = 0
    stopped = "completed turns"

    for turn in range(1, turns + 1):
        if soft_cap is not None:
            from llm_client import get_cost

            spent = get_cost(trace_id=trace_id)
            if spent >= soft_cap:
                stopped = f"soft cost ceiling reached at ${spent:.4f}"
                break

        page = engine.discover(ACTOR)
        context = present(engine, ACTOR, page)
        context["recent"] = _recent(engine, seen_events)
        seen_events = len(engine.world.events)

        action_id, reasoning = policy.select(page, context)
        choice = resolve_choice(page, action_id, reasoning)
        result = apply_choice(engine, choice, controller=f"policy:{policy.name}")
        engine.advance(1)

        actor = engine.world.entities[ACTOR]
        transcript.append(
            {
                "turn": turn,
                "tick": engine.world.tick,
                "offered": len(page["available"]),
                "choice": choice.as_dict(),
                "engine_status": result["status"] if result else "no_action",
                "health": actor.actor.health,
                "hydration": actor.actor.hydration,
            }
        )
        if not actor.actor.alive:
            stopped = "actor died"
            break

    actor = engine.world.entities[ACTOR]
    refusals = [row for row in transcript if row["choice"]["kind"] == "refused"]
    accepted = [row for row in transcript if row["engine_status"] == "accepted"]
    return {
        "schema_version": "world-substrate-policy-run/v0",
        "policy": policy.name,
        "trace_id": trace_id,
        "turns_run": len(transcript),
        "stopped_because": stopped,
        "final": {
            "tick": engine.world.tick,
            "health": actor.actor.health,
            "hydration": actor.actor.hydration,
            "alive": actor.actor.alive,
        },
        "accepted_actions": len(accepted),
        "policy_answers_refused": len(refusals),
        "refusals": [row["choice"] for row in refusals],
        "transcript": transcript,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=14)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-budget", type=float, default=2.0)
    parser.add_argument("--soft-cap", type=float, default=1.20)
    parser.add_argument("--scripted", action="store_true", help="no model calls")
    parser.add_argument("--thirsty", action="store_true", help="no-foresight baseline, no model calls")
    parser.add_argument("--compare", action="store_true", help="run baseline then LLM and record both")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    trace_id = f"world-substrate-policy-{uuid.uuid4().hex[:10]}"
    if args.compare:
        baseline = run(ThirstyPolicy(), args.turns, None, trace_id + "-baseline")
        llm = LlmPolicy(
            model=args.model,
            trace_id=trace_id,
            max_budget=args.max_budget,
            template=str(REPO / "prompts/castaway_policy.yaml"),
        )
        llm_payload = run(llm, args.turns, args.soft_cap, trace_id)
        from llm_client import get_cost

        llm_payload["model"] = args.model
        llm_payload["cost_usd"] = round(get_cost(trace_id=trace_id), 6)
        llm_payload["model_calls"] = len(llm.calls)
        payload = {
            "schema_version": "world-substrate-policy-comparison/v0",
            "claim": (
                "The same semantic action interface was driven by two different "
                "policies over the same world and rules. Neither policy computed "
                "any consequence: each returned only an action_id, which the "
                "engine matched against actions it had itself offered. The "
                "difference in outcome is produced by installed mechanics."
            ),
            "turns": args.turns,
            "max_budget_usd": args.max_budget,
            "soft_cap_usd": args.soft_cap,
            "baseline": baseline,
            "llm": llm_payload,
            "outcome_differs": baseline["final"] != llm_payload["final"],
        }
    elif args.thirsty:
        payload = run(ThirstyPolicy(), args.turns, None, trace_id)
    elif args.scripted:
        policy = ScriptedPolicy(["wait"] * args.turns)
        payload = run(policy, args.turns, None, trace_id)
    else:
        policy = LlmPolicy(
            model=args.model,
            trace_id=trace_id,
            max_budget=args.max_budget,
            template=str(REPO / "prompts/castaway_policy.yaml"),
        )
        payload = run(policy, args.turns, args.soft_cap, trace_id)
        from llm_client import get_cost

        payload["model"] = args.model
        payload["cost_usd"] = round(get_cost(trace_id=trace_id), 6)
        payload["max_budget_usd"] = args.max_budget
        payload["soft_cap_usd"] = args.soft_cap
        payload["model_calls"] = len(policy.calls)

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        print(f"wrote {display_path(args.output, REPO)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
