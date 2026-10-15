"""People worlds for the World Builder: the scenario-spec path (docs/plans/scenario_spec_adoption.md).

A description about people (who wants what, who knows what, meetings, decisions) is built through ScenarioSpecV1
instead of the plain things-and-actions generator: one structured call writes the people with their goals, beliefs
and information, the compiler turns them into exact rules (the reviewed `communicate` rule, scheduled moments), and
the mechanics generator writes rules only for the behaviors the compiler leaves open. Each person also gets a brief
from their own profile, which the AI that chooses their moves reads.

The pipeline modules live in spikes/any-scenario-2026-10/ (run there on 2026-10-08 against Waltzman's scenario);
this module is the World Builder's entry to them and changes none of their behavior.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

from scripts.generate_causal_model import DEFAULT_MODEL, generate_causal_model
from scripts.run_authored_world import build_engine

PIPELINE = Path(__file__).resolve().parents[1] / "spikes/any-scenario-2026-10"
PEOPLE_MODEL = "openrouter/openai/gpt-5.6-sol"
PEOPLE_MODEL_WHY = (
    "World Builder people world: the scenario spec and its rules are the whole world definition; on 2026-10-07 eight "
    "gpt-5.6-luna rule attempts produced rules that repairs could not fix, so the stronger tier writes them."
)
# Same wording as the spike's ATTEMPT_GUIDANCE (spikes/any-scenario-2026-10/model_scenario.py), kept here so the
# service does not import that script's command-line module.
ATTEMPT_GUIDANCE = (
    "Separate permissibility from feasibility. An action's checks say only whether the actor is allowed "
    "or positioned to begin it (rules of the game, location, possession). Never check whether the attempt "
    "will succeed: do not refuse an action because a resource is too low to finish it. Starting a "
    "multi-step activity sets the actor's or object's activity state. Autonomous processes then advance "
    "that activity every tick, consume or produce stocks, and switch the activity to a stopped or failed "
    "state when a needed stock runs out, or to a finished state when it completes. Every numeric stock "
    "needs a process or action for each way it can rise and each way it can fall."
)
# Thinking effort of the two stronger-model calls. "medium" took 105 s (people) and 90 s (rules) on Waltzman's text
# (2026-10-15); WORLD_BUILDER_PEOPLE_EFFORT overrides both, for comparing.
EFFORT = os.environ.get("WORLD_BUILDER_PEOPLE_EFFORT") or "medium"
KIND_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["about_people", "why"],
    "properties": {"about_people": {"type": "boolean"}, "why": {"type": "string"}},
}

Progress = Callable[..., None]


def _pipeline():
    if str(PIPELINE) not in sys.path:
        sys.path.insert(0, str(PIPELINE))
    import compile_spec
    import spec_pipeline
    return compile_spec, spec_pipeline


def about_people(description: str, *, trace_id: str, max_budget: float) -> tuple[bool, str]:
    """One small call: is this a world of people with their own goals and information, or of things and steps?"""
    from llm_client import call_llm_json_schema
    value, _ = call_llm_json_schema(
        DEFAULT_MODEL,
        [{"role": "system", "content": (
            "Decide how a described world should be simulated. about_people is true when the description is mainly "
            "about people, groups or organisations who want different things, know different things, pass "
            "information on, meet, argue, persuade or decide together. It is false when it is mainly about things, "
            "places, stocks and the steps of a process (a kitchen, a supply chain, a garden, a factory), even if "
            "workers do those steps. Give a one-sentence why.")},
         {"role": "user", "content": description}],
        KIND_SCHEMA, schema_name="world_builder_world_kind", task="world-builder-world-kind", trace_id=trace_id,
        max_budget=max_budget, reasoning_effort="low",
    )
    if not isinstance(value, dict) or not isinstance(value.get("about_people"), bool):
        return False, "the kind check returned nothing usable"
    return value["about_people"], str(value.get("why") or "")


def _words(value: str) -> str:
    return value.replace("_", " ").replace("-", " ")


# 2026-10-15 Waltzman run (trace world-builder-e2e/people/d231947f...): raise-concern could repeat every round and no
# rule resolved a concern or restored support, so from round 4 every member raised the same concern forever.
LIVENESS_GUIDANCE = (
    "This world keeps running with people acting every round, so: (1) no action may be repeatable without limit by "
    "the same actor on the same thing; record that it was done (for example a concern's status becomes raised) and "
    "check that it was not done already. (2) Every state a rule can push one way needs a rule that can push it back "
    "(a raised concern can be addressed or resolved, conditional support can become full support again, a postponed "
    "or withheld decision can be reconsidered, a slowed pace can recover). (3) Progress toward the scenario's "
    "decision must stay possible while concerns are open."
)


def prepare_people_world(description: str, *, trace_id: str, max_budget: float, progress: Progress) -> dict[str, Any]:
    """Description -> ScenarioSpecV1 -> compiled bundle and the attempts people can make (no rules yet)."""
    compile_spec, sp = _pipeline()
    progress("doing", "Working out who is involved and what each of them wants")
    spec, _ = sp.scenario_spec(description, model=PEOPLE_MODEL, trace_id=trace_id, max_budget=max_budget,
                               reasoning_effort=EFFORT)
    progress("done", f"Found {len(spec.people)} people or groups", "each with goals, beliefs and what they know",
             [p.label for p in spec.people])
    if spec.information_items or spec.scheduled_moments:
        progress("done", "Found what is known and when things happen",
                 f"{len(spec.information_items)} piece{'s' if len(spec.information_items) != 1 else ''} of "
                 f"information, {len(spec.scheduled_moments)} scheduled moment"
                 f"{'s' if len(spec.scheduled_moments) != 1 else ''}",
                 [_words(m.moment_id) for m in spec.scheduled_moments] + [i.content for i in spec.information_items])
    if spec.unsupported:
        progress("note", "Left out of the simulation", "", [str(x).rstrip(". ") for x in spec.unsupported])
    bundle, compiled, coverage = compile_spec.compile_spec(spec)
    progress("doing", "Working out what each person can try to do")
    sigs, _ = sp.action_signatures(spec, bundle, coverage, model=DEFAULT_MODEL, trace_id=trace_id,
                                   max_budget=max_budget)
    sigs = sp.record_fields(spec, sigs)
    bundle["actions"] = bundle["actions"] + [{k: a[k] for k in ("kind", "description", "fields")} for a in sigs]
    progress("done", "Things people can try", "", [_words(a["kind"]) for a in bundle["actions"]])
    return {"spec": spec, "bundle": bundle, "compiled": compiled, "coverage": coverage, "sigs": sigs}


def write_people_rules(prepared: dict[str, Any], *, trace_id: str, max_budget: float, progress: Progress,
                       guidance: str = "") -> dict[str, Any]:
    """The rules for what people's attempts cause, merged with the compiled ones. Raises on a rule set the compiler
    rejects, like the plain generator."""
    _, sp = _pipeline()
    spec, bundle, compiled = prepared["spec"], prepared["bundle"], prepared["compiled"]
    coverage = json.loads(json.dumps(prepared["coverage"]))  # behavior_coverage edits rows; keep the prepared copy
    behaviors = [r["behavior"] for r in coverage["rows"] if r["classification"] == "to_generate"]
    progress("doing", "Writing the rules for what those attempts cause", "this is the longest step")
    rule_guidance = (
        ATTEMPT_GUIDANCE + " " + LIVENESS_GUIDANCE + " The `communicate` action is already defined by a reviewed "
        "rule; keep it as is. Scheduled moments are entities in category `moment` whose `occurrences` rises when they "
        "happen; rules may read `ticks_until` and `occurrences`. Make these behaviors possible: " + " | ".join(behaviors)
        + (" " + guidance if guidance else "")
    )
    generated, _ = generate_causal_model(
        bundle, trace_id=trace_id, guidance=rule_guidance, world_kind="ongoing", reasoning_effort=EFFORT,
        model=PEOPLE_MODEL, model_justification=PEOPLE_MODEL_WHY, max_budget=max_budget,
    )
    generated = {k: v for k, v in generated.items() if k != "review"}
    causal, dropped = sp.merge_causal(compiled, generated)
    causal, pinned = sp.pin_named_slots(spec, causal)
    build_engine(bundle, causal)  # compile + install: raises if any rule is rejected
    coverage = sp.behavior_coverage(spec, prepared["sigs"], causal, coverage)
    not_modeled = list(spec.unsupported) + [
        f"{r['behavior']} ({r.get('why') or 'no rule for it'})" for r in coverage["rows"]
        if r["classification"] == "unsupported"]
    return {
        "bundle": bundle,
        "causal_model": causal,
        "briefs": sp.person_briefs(spec),
        "people": [{"id": p.entity_id, "label": p.label, "position": p.position} for p in spec.people],
        "coverage": coverage,
        "not_modeled": not_modeled,
        "dropped_generated_rules": dropped + [f"slot pinned: {x}" for x in pinned],
        "scenario_spec": json.loads(spec.model_dump_json()),
    }


def build_people_world(description: str, *, trace_id: str, max_budget: float, progress: Progress,
                       guidance: str = "") -> dict[str, Any]:
    prepared = prepare_people_world(description, trace_id=trace_id, max_budget=max_budget, progress=progress)
    return write_people_rules(prepared, trace_id=trace_id, max_budget=max_budget, progress=progress, guidance=guidance)
