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

import contextvars
import json
import os
import sys
import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable

from scripts.generate_causal_model import DEFAULT_MODEL, generate_causal_model
from scripts.run_authored_world import build_engine

PIPELINE = Path(__file__).resolve().parents[1] / "spikes/any-scenario-2026-10"
# Brian, 2026-10-16: "we need to switch to gpt6 luna for everything ... because the bills you are running up is too
# high. we can switch to sol when we share with waltzman". One setting, WORLD_BUILDER_STRONG_MODEL, picks the model
# for the people and their rules (and the rules retry in world_builder_service); set it to
# openrouter/openai/gpt-5.6-sol to go back. On 2026-10-07 eight luna rule attempts failed where sol succeeded, before
# the compiled decision and moments existed; whether luna now suffices is what the next runs test. gpt-6-luna since
# 2026-10-16 (Brian asked for "gpt6 luna"; half the price of gpt-5.6-luna, and llm_client's default).
PEOPLE_MODEL = os.environ.get("WORLD_BUILDER_STRONG_MODEL") or "openrouter/openai/gpt-6-luna"
PEOPLE_MODEL_WHY = (
    "World Builder people world: the scenario spec and its rules are the whole world definition; the model is set "
    "by WORLD_BUILDER_STRONG_MODEL (luna by default for cost, sol for shared demos)."
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
# Thinking effort of the people, actions and rules calls. "medium" took 105 s (people) and 90 s (rules) on Waltzman's
# text with sol (2026-10-15). Brian (2026-10-16): "you can also use max thinking for luna"; tried on gpt-6-luna
# (inc15l): xhigh cost only $0.03 but took 447 s (people), 136 s (actions) and 226 s (rules) against 48/10/38 s at
# medium, far past the visitor's short wait. WORLD_BUILDER_PEOPLE_EFFORT overrides all three, for comparing.
EFFORT = os.environ.get("WORLD_BUILDER_PEOPLE_EFFORT") or "medium"
# The people step alone: medium 103 s (deploy1), low 47 s (deploy2) but low 98 s again (deploy3), so the time was the
# provider's speed, not the effort (see fast_route). Low also built worlds that went silent after round 9-10 (deploy2,
# deploy3), so medium stays; WORLD_BUILDER_SPEC_EFFORT sets only the people step, for comparing.
SPEC_EFFORT = os.environ.get("WORLD_BUILDER_SPEC_EFFORT") or EFFORT
# A people world's rules name every record slot, so 20-26 rules ran past the plain generator's 16000-token cap
# (2026-10-16 Waltzman inc15b: "LLM response truncated (65955 chars)"). The build's budget still bounds the cost.
RULES_OUTPUT_TOKENS = 32000
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
# (4): 2026-10-16 local Waltzman run inc15c: only Country One could change its support (actor == country-one), so
# Countries Two to Four and the health network sat idle for 40 rounds.
# (5), (6): 2026-10-16 local Waltzman run inc15d: all ten acted every round, but addressing a concern only reset the
# meeting pace, so no record ever showed a country's condition met and none restored its support in 30 rounds; and
# the decision could end only if the partnership chose to reject in the one round the deadline was happening.
# (8): 2026-10-17 live Waltzman run umwwKYrbOVGR (Concordia residents): after deployment completed in round 29 nothing
# new reached anyone, so the residents rightly waited ("the system is deployed, my concern is resolved"): 2-3 moves
# per 10 rounds, 2 kinds, for the last 16 rounds. Rules cannot write concerns or the decision, so the review itself is
# compiled (compile_spec REVIEW_TICKS, 2026-10-18 _q9oVz-QlJ3S).
LIVENESS_GUIDANCE = (
    "This world keeps running with people acting every round, so: (1) no action may be repeatable without limit by "
    "the same actor on the same thing; record that it was done (for example a concern's status becomes raised) and "
    "check that it was not done already, but never forever: something that recurs must clear that record so the "
    "work can be done again later (a scheduled moment occurring, new information arriving, another person's action, "
    "a concern being reopened), for example each meeting lets every group report again. A person whose every action "
    "is done once and never cleared has nothing to do for the rest of the run. (2) Every state a rule can push one way needs a rule that can push it back "
    "(a raised concern can be addressed or resolved, conditional support can become full support again, a postponed "
    "or withheld decision can be reconsidered, a slowed pace can recover). (3) Progress toward the scenario's "
    "decision must stay possible while concerns are open. (4) When several people share a position (for example "
    "member countries), an action the position allows is open to each of them: check the actor's position, not one "
    "person's id, unless the description says only that person may do it, and give each of them their own record "
    "where the action changes one (each member's own support, not only the one the description happens to name). (5) "
    "A deadline that the group decision does not already settle must settle by itself: write a process that, when the deadline arrives, applies the description's rule "
    "for the decision (for example authorized when enough support exists, otherwise postponed with a new deadline, or "
    "rejected), so the outcome never waits on someone choosing to act in that one round. (6) A condition someone "
    "places on their support names what would meet it, as a record the remedy changes (that concern resolved, that "
    "issue cleared, that assurance given); restoring support checks that record, so the person can see their "
    "condition was met. Work that is finished stays finished until new information or another person reopens it; "
    "the person who just finished it does not undo it themselves. (7) Never write an action whose only effect is to add "
    "to a count (for example a tally of concerns raised): repeating it changes a number, not the situation, so people "
    "repeat it forever. An action changes a named record (this concern, this review, this person's readiness). (8) "
    "Reaching or carrying out the decision does not end this world: write what follows it. Once the decision is in "
    "effect a compiled operating review reopens its resolved concerns every few rounds; write the specialist and "
    "practical work that goes on around it (monitoring, reporting, operating, reviewing), limited by the work cycle, "
    "so each group has something real to do while the decision is in effect."
)


# 2026-10-15 live Waltzman run (world-builder-live, 31 rounds): the actions covered only the paper's slowing moves
# (raise a concern, request a delay, withhold support); none fixed a concern, made a readiness true or restored
# support, so after one delay request each, 7 of 10 members had nothing left to do. Rules cannot add actions, so the
# reverse moves must be asked for here.
ACTION_LIVENESS_GUIDANCE = (
    "This world keeps running for many rounds, so also propose the actions that move things back and forward: for "
    "every action that raises, blocks, delays, withholds or reopens something, an action someone can take to address, "
    "resolve, restore or reconsider it (for example addressing a raised concern, making a readiness complete, giving "
    "full support again, reconsidering a postponed decision). Every person listed must have at least one action that "
    "fits their position and that they could take more than once over the run; specialist groups need actions that "
    "do their specialist work. List such an action under the behavior whose state it moves back. When several "
    "people share a position (for example member countries), what the description says one of them does is an "
    "example of what the position allows, not a limit: write the action so any of them can take it. When "
    "existing_actions already cover something (a group decision's giving, conditioning and restoring support, "
    "resolving and reopening concerns, and its deadline settling it), do not propose another action for it; "
    "propose the practical and specialist work instead."
)


# OpenAI's own endpoint tiers on OpenRouter, fastest first. 2026-10-16 route test on the people-step prompt
# (~/code/.scratch/waltzman-demo/route-test/run1.log, two tries each): openai/fast 200 tokens/s (21-27 s), azure
# 122-130 (36-43 s), openai 97-102 (41 s), openai/flex 35 (121-132 s). Sorting by throughput alone still landed both
# hedged copies on a slow endpoint (deploy9: 96 and 98 s for the people step). The fast tier costs about twice as
# much per call (about $0.005 for the people step).
FAST_OPENAI_ENDPOINTS = ("openai/fast", "azure", "openai")


def fast_route(model: str = "") -> Any:
    """The fastest OpenRouter route for a build call: an OpenAI model only on its fast endpoints (never the slow
    flex tier), any other model on the provider with the highest throughput. The build has to reach its first
    round within 150 s."""
    try:
        from llm_client import OpenRouterRoutePolicyV1
    except ImportError:  # only where no model call can run anyway (tests with the calls stubbed)
        return None
    if "openai/" in model:
        return OpenRouterRoutePolicyV1(allowed_providers=FAST_OPENAI_ENDPOINTS, sort="throughput")
    return OpenRouterRoutePolicyV1(sort="throughput")


# Identical copies of each long build call, sent at once; the first good answer is used. 2026-10-16: the same
# people-step call took 42-53 s on some tries and 87-104 s on others, at random, even sorted by throughput (deploy1-6,
# speed test), and the build has to reach its first round within 150 s. Each copy is charged like any call; the
# service keeps a reservation for a copy still running when the build ends (unfinished_hedges). 1 turns it off.
# The general fix belongs in llm_client (BrianMills2718/llm_client#286).
HEDGE_COPIES = max(1, int(os.environ.get("WORLD_BUILDER_HEDGE_COPIES") or 2))
_HEDGES: dict[str, list[Future]] = {}
_HEDGE_LOCK = threading.Lock()


def hedged(trace_id: str, call: Callable[[], Any]) -> Any:
    """call() HEDGE_COPIES times at once; return the first that succeeds, raise the first error if none does."""
    if HEDGE_COPIES < 2:
        return call()
    pool = ThreadPoolExecutor(HEDGE_COPIES, thread_name_prefix="hedge")
    futures = [pool.submit(contextvars.copy_context().run, call) for _ in range(HEDGE_COPIES)]  # keep the caller's context
    pool.shutdown(wait=False)
    errors: list[BaseException] = []
    for done in as_completed(futures):
        try:
            result = done.result()
        except Exception as error:  # the other copy may still succeed
            errors.append(error)
            continue
        with _HEDGE_LOCK:
            _HEDGES.setdefault(trace_id, []).extend(f for f in futures if f is not done)
        return result
    raise errors[0]


def unfinished_hedges(trace_id: str) -> list[Future]:
    """The copies of this build's calls still running (their cost is not in the trace yet); forgets the rest."""
    with _HEDGE_LOCK:
        return [f for f in _HEDGES.pop(trace_id, []) if not f.done()]


def prepare_people_world(description: str, *, trace_id: str, max_budget: float, progress: Progress) -> dict[str, Any]:
    """Description -> ScenarioSpecV1 -> compiled bundle and the attempts people can make (no rules yet)."""
    compile_spec, sp = _pipeline()
    progress("doing", "Working out who is involved and what each of them wants")
    spec, _ = hedged(trace_id, lambda: sp.scenario_spec(description, model=PEOPLE_MODEL, trace_id=trace_id,
                                                        max_budget=max_budget, reasoning_effort=SPEC_EFFORT,
                                                        route_policy=fast_route(PEOPLE_MODEL)))
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
    sigs, _ = hedged(trace_id, lambda: sp.action_signatures(
        spec, bundle, coverage, model=DEFAULT_MODEL, trace_id=trace_id, max_budget=max_budget,
        guidance=ACTION_LIVENESS_GUIDANCE, reasoning_effort=EFFORT, route_policy=fast_route(DEFAULT_MODEL)))
    sigs = sp.record_fields(spec, sigs)
    bundle["actions"] = bundle["actions"] + [{k: a[k] for k in ("kind", "description", "fields")} for a in sigs]
    work_cycle = compile_spec.add_work_cycle(spec, bundle, compiled, [a["kind"] for a in sigs])
    progress("done", "Things people can try", "", [_words(a["kind"]) for a in bundle["actions"]])
    return {"spec": spec, "bundle": bundle, "compiled": compiled, "coverage": coverage, "sigs": sigs,
            "work_cycle": work_cycle}


def write_people_rules(prepared: dict[str, Any], *, trace_id: str, max_budget: float, progress: Progress,
                       guidance: str = "") -> dict[str, Any]:
    """The rules for what people's attempts cause, merged with the compiled ones. Raises on a rule set the compiler
    rejects, like the plain generator."""
    progress("doing", "Writing the rules for what those attempts cause", "this is the longest step")
    rule_guidance = rules_guidance(prepared, guidance)
    # The writer gets only the actions no compiled rule covers. 2026-10-16 inc15h (luna): asked for one rule per
    # action including the compiled ones (discarded at merge anyway), it returned a mismatched action list twice and
    # the build failed. Fewer rules to write also means fewer output tokens.
    to_write = actions_to_write(prepared)
    generated: dict[str, Any] = {"mechanics": [], "processes": [], "terminal": None}
    if to_write["actions"]:
        generated, _ = hedged(trace_id, lambda: generate_causal_model(
            to_write, trace_id=trace_id, guidance=rule_guidance, world_kind="ongoing", reasoning_effort=EFFORT,
            model=PEOPLE_MODEL, model_justification=PEOPLE_MODEL_WHY, max_budget=max_budget,
            max_output_tokens=RULES_OUTPUT_TOKENS, route_policy=fast_route(PEOPLE_MODEL),
        ))
    return assemble_people_world(prepared, generated)


def rules_guidance(prepared: dict[str, Any], guidance: str = "") -> str:
    """What the rule writer is told beyond the response contract (also the harness workspace's instructions)."""
    behaviors = [r["behavior"] for r in prepared["coverage"]["rows"] if r["classification"] == "to_generate"]
    return (
        ATTEMPT_GUIDANCE + " " + LIVENESS_GUIDANCE + " The `communicate` action is already defined by a reviewed "
        "rule and is not in your list. When the world has a group decision (entity category `group-decision`), support, concerns "
        "and the decision are exact compiled rules (give-support, make-support-conditional, restore-full-support, "
        "resolve-concern, resolve-own-concern, reopen-concern, and the deadline processes): rules may read the `support`, `concern` and "
        "`group_decision` components but never write them, with one exception: `group_decision.agenda_items` counts the "
        "matters put before the decision and not yet settled (compiled put-matter-on-agenda and settle-agenda-matter "
        "already add and subtract it; a rule of yours for discussing a matter or settling one at a meeting may too, "
        "checking it is above 0 before subtracting). At a deadline, open agenda items postpone a decision that has "
        "the support, until no postponements remain. Every rule must change something another rule or the deadline "
        "reads (a person's own done flag alone changes nothing); work by people outside the decision can change their "
        "own records or the agenda. Scheduled moments are entities in category `moment` whose `occurrences` rises when they "
        "happen; rules may read `ticks_until`, `occurrences` and `happening_now` (true only in the round right after "
        "the moment occurs, which is when people act; `ticks_until` is never 0 then, so to require that a meeting is on, "
        "check `happening_now` is true). " + work_cycle_guidance(prepared.get("work_cycle"))
        + "Make these behaviors possible: " + " | ".join(behaviors)
        + (" " + guidance if guidance else "")
    )


def work_cycle_guidance(cycle: dict[str, Any] | None) -> str:
    """How the rule writer limits repeated work: the compiled per-person `work` flags (compile_spec.add_work_cycle)."""
    if not cycle:
        return ""
    flags = ", ".join(f"{kind} -> components.work.{flag}" for kind, flag in cycle["flags"].items())
    return (
        "Every person has a `work` component with one false flag per action (" + flags + "); a compiled process "
        f"clears all of them each time {cycle['cycle_label'][:80].rstrip('.')} comes round (moment "
        f"{cycle['cycle_id']}). To stop an action being repeated every round, check that the actor's own flag for "
        "that action is false and set it true; never use `member` fields or another action's flag as a done-record. "
        "Routine work (monitoring, reporting, operating, reviewing) goes on after any decision, so do not require "
        "the decision to be open or a system to be undeployed unless the work only makes sense before it. "
    )


def actions_to_write(prepared: dict[str, Any]) -> dict[str, Any]:
    """The bundle with only the actions no compiled rule covers: what the rule writer must give rules to."""
    compiled_kinds = {m["action_kind"] for m in prepared["compiled"]["mechanics"]}
    return {**prepared["bundle"], "actions": [a for a in prepared["bundle"]["actions"] if a["kind"] not in compiled_kinds]}


def assemble_people_world(prepared: dict[str, Any], generated: dict[str, Any]) -> dict[str, Any]:
    """Generated rules + compiled rules -> the finished world. Raises on a rule set the compiler rejects."""
    compile_spec, sp = _pipeline()
    spec, bundle, compiled = prepared["spec"], prepared["bundle"], prepared["compiled"]
    coverage = json.loads(json.dumps(prepared["coverage"]))  # behavior_coverage edits rows; keep the prepared copy
    generated = {k: v for k, v in generated.items() if k != "review"}
    generated["mechanics"], impossible = compile_spec.drop_impossible_checks(generated.get("mechanics") or [], bundle)
    generated["mechanics"] = compile_spec.limit_to_work_cycle(generated["mechanics"], prepared.get("work_cycle"))
    causal, dropped = sp.merge_causal(compiled, generated)
    dropped = impossible + dropped
    # An action whose whole generated rule was dropped (every effect wrote a compiled component) leaves the world, so
    # bundle and rules still match. 2026-10-16 inc15j (luna): reconsider-settled-issue only set a concern's status,
    # the merge removed it, and the build failed with "action kinds must exactly match the authoring bundle".
    ruled = {m["action_kind"] for m in causal["mechanics"]}
    unruled = [a["kind"] for a in bundle["actions"] if a["kind"] not in ruled]
    if unruled:
        bundle = {**bundle, "actions": [a for a in bundle["actions"] if a["kind"] in ruled]}
        dropped = dropped + [f"action {k} removed: its rule only wrote what compiled rules own" for k in unruled]
    causal, pinned = sp.pin_named_slots(spec, causal)
    causal, due = sp.fix_moment_due_checks(causal)
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
        "dropped_generated_rules": dropped + [f"slot pinned: {x}" for x in pinned] + [f"check fixed: {x}" for x in due],
        "scenario_spec": json.loads(spec.model_dump_json()),
    }


def build_people_world(description: str, *, trace_id: str, max_budget: float, progress: Progress,
                       guidance: str = "") -> dict[str, Any]:
    prepared = prepare_people_world(description, trace_id=trace_id, max_budget=max_budget, progress=progress)
    return write_people_rules(prepared, trace_id=trace_id, max_budget=max_budget, progress=progress, guidance=guidance)
