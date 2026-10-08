---
plan_id: "scenario-actors-kept"
dependencies: ["waltzman-scenario-run"]
dependencies_reviewed: "2026-10-08"
planning_path: durable_solo
planning_path_ref: docs/plans/scenario_actors_kept/path-decision.json
method_conformance_receipt: docs/plans/scenario_actors_kept/conformance-receipt.json
goal:
  outcome: "Every actor a scenario names reaches the generated world as an autonomous agent with a role brief taken from the scenario text, so that Rand Waltzman's scenario, rerun through the any-scenario pipeline, has the technical, legal, logistics and community groups acting in it; a fresh assessment states with event-level evidence which of the paper's four mechanisms now appear."
  canonical_example: "Running spikes/any-scenario-2026-10/model_scenario.py on the Waltzman scenario text yields a world whose actor entities include the technical, legal, logistics and community groups (each mapped from an ODD actor, recorded in model.json with its role brief), and run_scenario.py runs AI agents for all of them, each briefed with its own role; docs/plans/scenario_actors_kept.md (Assessment) gives, for each of the four mechanisms, the Engine event ids and rules that show it, or the plain reason it is still missing."
  forbidden_substitutes: "hand-edited generated models presented as generated; scripted agents presented as AI choices; role briefs written by hand rather than taken from the scenario text by the pipeline; a mechanism marked represented without an event id from the recorded run; rerunning until a mechanism appears and reporting only that run (every run made is reported); a hand-chosen world kind for this scenario in place of the pipeline's own choice."
  boundaries: "world-substrate only; work merges through pull requests after scripts/check_project.py passes; the public World Builder's description limit and behavior unchanged; cybernetic_influence_v3 and other repositories read-only; no deploy, no outreach to Waltzman, no change to the live World Builder or /waltzman/; model spend capped at $2 for this plan, measured by spikes/any-scenario-2026-10/spend.py from its value at the plan's start; raising it needs Brian's yes."
  done_when: "Acceptance checks K1-K6 in docs/plans/scenario_actors_kept.md pass, each judged from the full trace of its named run (llm_client trace ids, model.json actor map and role briefs, Engine event lists with event ids, agent attempt records, frames with screenshots, project gate output on the merge commit); report the trace ids and evidence for each, and report every pipeline and member run made, not only the best."
  do_not_gate_on: "whether any particular mechanism appears (the assessment reports what happened); Brian's review; Waltzman's reaction or any outreach; the hospital pipeline-only result; distance-limited sensing; the pencil comparison with Cybernetic Influence."
  stop_after: 3
---
# Plan: keep every actor a scenario names, and brief each with its role

## Goal

**Mission:** The point of the any-scenario work is a demo in which Rand Waltzman describes a situation and watches it play out. When his scenario was run (plan `waltzman-scenario-run`), nothing he describes happened: the four countries and the health network all approved at once, because the groups that raise concerns were not in the world. This plan fixes why they were lost and gives every agent its role from the scenario text, then reruns his scenario.

**What the previous run showed** (evidence: `spikes/any-scenario-2026-10/evidence/waltzman/`):

- The conceptual-modeling step did model the four groups as actors with decisions (`model.json`, `odd.entities` and `odd.actor_decisions`).
- The step that hands that model to the world builder cut its summary to 1,500 of 6,188 characters (`model_scenario.py`, `odd_brief`), to fit the public World Builder's 2,000-character description limit (`scripts/generate_world_bundle.py:29`). The cut fell after Country D, so the groups never reached the world builder.
- The run also used the "task" world kind, which allows 2 to 10 entities and 1 to 4 actions (`scripts/generate_world_bundle.py:78`); the conceptual model had 13 entities.
- Each agent was briefed only with the whole scenario text, not with its own part in it. Members said they had "no observed concerns".

**Execution profile:** `continuous-light`. One writer, reversible, one repository.

**Stage and investment boundary:** a fix-and-rerun. About 3 to 5 hours of agent work and at most $2 of model spend.

**Canonical example:** see the goal block.

**Repository / working scope:** `world-substrate`: `spikes/any-scenario-2026-10/` and one optional argument in `scripts/generate_world_bundle.py`.

## Actor, result and authority

- **Actor:** Brian, deciding whether the "describe any scenario" path can play out Waltzman's scenario, and what to fix next.
- **Result:** a rerun of Waltzman's scenario in which the groups are agents, with frames and an assessment.
- **Stable example of the result:** the input is the recorded Waltzman conceptual model (`spikes/any-scenario-2026-10/evidence/waltzman/model.json`). Its ODD names the actor "Legal group" with the decision to raise concerns. Today that actor is absent from the world that was built. After this plan, the pipeline's actor map for the same scenario text has a row whose `odd_actor` is "Legal group", whose `entity_id` is an actor entity in the bundle, and whose `role` is a sentence taken from the scenario (raising small, true, local legal concerns through its own channel). The agent for that entity is briefed with that role. The same holds for the technical, logistics and community groups. The Assessment then reports, per mechanism, either event ids and rules from the recorded run or the reason it is missing.
- **Authority:** Brian, 2026-10-08, after the Waltzman run: the scenario text "is telling people what to do which i am fine with us having this capability". The implementing agent is the sole writer.
- **Non-goals:**
  - contacting Waltzman or deploying anything;
  - changing the public World Builder's description limit or its pages;
  - tuning the pipeline until the mechanisms appear;
  - comparing models or pipeline variants.

## Design

1. **No silent cut between modeling and world building.** `odd_brief` renders actors and their decisions first, and never truncates: when the full summary exceeds the limit, the pipeline passes a larger limit. `generate_world_bundle` gains an optional `max_description_chars` argument, defaulting to today's 2,000, so the public World Builder is unchanged.
2. **World kind follows the model.** When the conceptual model has more than 10 entities or more than 4 acting parties, the pipeline asks for an `ongoing` world (up to 30 entities and 12 actors), and records why in `model.json`.
3. **Actor coverage check.** One structured call maps each ODD actor to a bundle actor entity, or to none, validated client-side against the bundle's actor ids. An ODD actor mapped to none is a blocking `structure` finding, so the repair loop targets it.
4. **Role briefs from the scenario text.** The same call returns, for each mapped actor, one or two sentences of its role taken from the scenario text and the ODD's `actor_decisions`. They are stored in `model.json`. `run_scenario.py` briefs each agent with the scenario, then "Your role: …".

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| K1 | The summary passed to the world builder contains every ODD entity and actor decision. Nothing is cut silently: an over-limit summary raises the limit or fails loudly. | a unit test on the recorded Waltzman ODD (`evidence/waltzman/model.json`) showing all 9 ODD actors in the summary; the public default limit is still 2,000 |
| K2 | World kind is chosen from the conceptual model, and the reason is recorded | `model.json` `world_kind` and `world_kind_reason` of the K4 run, plus a unit test |
| K3 | The actor coverage check maps ODD actors to world actors and blocks on a missing one | a unit test with the recorded Waltzman bundle, which has no group actors, yielding blocking findings; the K4 run's actor map |
| K4 | A fresh pipeline run of the Waltzman text yields a world whose actors include the four groups, each with a role brief from the pipeline | the trace ids in `model.json`, the actor map and role briefs, final check counts, and every pipeline run made |
| K5 | AI agents run on that world on Concordia, each briefed with its role, with the Engine as the only state authority and the game master on; frames are rendered with a screenshot of a round that shows a group agent acting | run summary, event count, trace id, the attempt records showing each agent's role brief, the screenshot path and that round's event ids |
| K6 | An assessment gives, for each of the four mechanisms, "represented" with event ids and rule ids from the K5 run, or "missing" with the reason. Evidence is committed, and the project gate passes on the merge commit with no test skipped. | `docs/plans/scenario_actors_kept.md` section "Assessment"; the gate output saved beside the evidence |

## Trace review per criterion

| ID | Run whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| K1-K3 | No new run: these checks read the full recorded trace of the previous Waltzman pipeline run, `waltzman-20261008T123134` (its ODD, the summary handed to the world builder, and the bundle) | `spikes/any-scenario-2026-10/evidence/waltzman/` (`model.json`, `bundle.json`, `pipeline.log`), read by `tests/test_scenario_actors_kept.py` | In that recorded trace, all 9 ODD actors are present, and the old summary is cut after Country D. The new summary contains all 9, the kind rule picks `ongoing` for that ODD, and the coverage check finds the 4 groups missing from the recorded bundle. The tests read these recorded files, not a hand-written fixture. |
| K4 | The pipeline run `runs/waltzman-actors-<stamp>/`, made by `model_scenario.py --name waltzman-actors` on the Waltzman text; every such run made is listed by its folder name | `llm_client` traces `any-scenario-waltzman-actors-*-<stamp>`; that folder's `model.json`, `bundle.json`, `checks.json`; copied to `spikes/any-scenario-2026-10/evidence/waltzman-actors/` | The groups come from the pipeline; the role briefs come from the mapping call; there are no hand edits. |
| K5 | The agent run `runs/waltzman-actors-<stamp>/run-<stamp2>/`, made by `run_scenario.py --model-dir` on the K4 folder; every such run made is listed by its folder name | trace `any-scenario-run-waltzman-actors-<stamp>-<stamp2>`; that folder's `events.jsonl`, `attempts.jsonl`, `summary.json`, frames; copied to `evidence/waltzman-actors/run/` and packed with `run-artifacts` | Each group's agent was briefed with its role. Each state change has an Engine event id. Rules written mid-run carry checks verdicts. |
| K6 | The full trace of the agent run `runs/waltzman-actors-<stamp>/run-<stamp2>/` (K5), and the project gate on the merge commit | As for K5, plus that folder's `causal.json`; the gate output saved as `evidence/waltzman-actors/gate-merge-<commit>.log` | Each "represented" cell cites an event id and rule id that exist in those files, plus the attempt records that show the effect. The gate runs with `node` and `llm_client` available, so no test is skipped. |

## Success and disproof

- **Success:** K1-K6 pass. The assessment is accurate against the recorded files.
- **Disproof** (of the claim that losing the actors was the main reason nothing happened): the groups are present and briefed, and still none of the four mechanisms appears. That is a valid result to report, and it points the next step at the agents or rules rather than world building.

## Model calls

- **Call graph and result boundaries,** in pipeline order. Each call returns:
  - **ODD:** a JSON object (entities, processes, actor decisions, sensing, stocks).
  - **Summary handoff (code, no call):** the ODD rendered whole, actors first, never cut.
  - **Bundle:** a JSON world bundle validated by `validate_bundle`, generated at the world kind the code chose from the ODD.
  - **Actor map and role briefs (new):** a Pydantic record, `[{odd_actor, entity_id or null, role}]`, validated client-side against the bundle's actor ids (unknown ids rejected). It feeds the coverage check and the agents' briefs.
  - **Mechanics:** a JSON causal model compiled by `CausalModel.from_dict`.
  - **Stock map, sensing map, outflow coverage:** Pydantic records validated against the world's own fields and rule ids.
  - **Extreme-conditions and anomaly reviews:** Pydantic verdicts with verbatim log quotes.
  - **Rule writer:** a JSON change list, compiled locally.
  - **Agents:** the Pydantic `Attempt`, with the agent's role brief in its prompt.
  - **Game-master rules:** compiled and checked before installation.
- **Prose never mutates state.** Role briefs only shape what an agent attempts; the Engine decides every consequence.
- **Tracing:** every call goes through `llm_client` with an `any-scenario-` trace id, and `spend.py` sums them.

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's key.
  - **Authorizer:** Brian, 2026-10-08. The cap is $2, measured from `spend.py` at the plan's start.
  - **Raising the cap:** needs his explicit yes.
  - **Expected cost:** about $0.60 to $1.20 (one ongoing-world pipeline run with repairs, and one agent run with 9 agents).
- **Irreversible actions:** none. There is no deploy and no outreach.
- **Promotion condition:** nothing is shown to Waltzman or deployed from this plan. Before any promotion, one authentic run must hold: a fresh pipeline run of his scenario text on a real model, with its trace ids reported, whose agent run shows at least three of the four mechanisms with Engine event ids.

## Uncertainties

This is the complete list of material uncertainties: each one, if it resolves badly, changes the conclusion about how close the demo is. The other parts of the path are already demonstrated (the pipeline, agents and frames ran end to end in the previous plan).

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether an ongoing-kind world keeps the groups and their concerns as state | Implementing agent | K4 bundle and actor map |
| Whether role briefs lead group agents to raise concerns, and members to slow, reopen or condition | Implementing agent | K5 attempt records and events |
| Whether the bundle generator accepts a longer description without losing quality | Implementing agent | K4 bundle trace and check counts |

## Prior art and parallel-implementation check

Existing ownership was searched first. The any-scenario pipeline and `scripts/generate_world_bundle.py` are owned by world-substrate, with Brian as sole owner. Under Decision 007, no other repository or plan owns scenario-to-actor generation or agent role briefs, and no open plan in `docs/plans/` claims them. Internal prior art was searched in Decisions 004–007 and in the any-scenario, linked-participants and Waltzman-run plans. Internal lineage was searched too. `odd_brief` and its 1,500-character cut came in with the any-scenario proof of concept (commit `bb8899f`, PR #131) to fit the World Builder's 2,000-character limit. That limit dates from the public World Builder's input field (`scripts/world_dialogue.py:27`). Cybernetic Influence v3, the earlier Waltzman line, authors explicit people with per-person roles (`cybernetic_influence_v3/src/cybernetic_influence/api.py`, the authoring `people` records). That is the lineage for keeping named actors with roles, and it is read-only here. External prior art covers LLM agent-simulation frameworks that brief generated agents with roles (Generative Agents, Concordia) and the modeling protocol the pipeline already follows (ODD). None of them generates the world's actors from free text and checks them against a conceptual model, so the pipeline is extended rather than replaced. Each candidate gets one disposition.

| Candidate | Disposition |
| --- | --- |
| Any-scenario pipeline (`spikes/any-scenario-2026-10/`) | **extend**: summary handoff, kind choice, coverage check, role briefs |
| `scripts/generate_world_bundle.py` world kinds and description limit | **reuse**: the `ongoing` kind as is; add one optional limit argument, default unchanged |
| Concordia player context (per-player instructions in its prefabs) | **reuse the idea**: the role brief goes into the existing resident prompt, the same place as Concordia's per-player context |
| Cybernetic Influence v3 authored `people` with roles (read-only lineage) | **reuse the idea**: named people keep their roles from authoring to run; not imported as code, since that repository is read-only and not a runtime dependency (Decision 005) |
| `reference_worlds/waltzman` (hand-authored) | **bounded exception**: not used as input, because the point is generation from text |
| External: Generative Agents (Park et al., 2023), where each agent is seeded with a short natural-language identity and role description | **reuse the idea**: a per-agent role brief in natural language is the established way to give generated agents distinct parts; the role brief here follows it |
| External: Concordia (Google DeepMind), whose prefab entities take a per-player goal and context | **reuse**: Concordia already hosts the agents; the role brief is the per-player context Concordia expects, passed through the existing acting component |
| External: the ODD protocol (Grimm et al.), which requires every entity of the conceptual model to be accounted for in the implementation | **reuse**: the actor-coverage check is ODD's entity completeness applied to the generated world |

**Check for a silent parallel implementation:** no new runner, checker or renderer is added. `git diff --stat origin/main` at the end touches only `spikes/any-scenario-2026-10/`, `scripts/generate_world_bundle.py` (one optional argument), `tests/test_scenario_actors_kept.py`, the evidence folder and this plan.

## Activation facts

The machine record is `scenario_actors_kept/activation-facts.json`.

- **`llm_central`: true.** World generation and agents are model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $2. Nothing is irreversible.
- **`shared_mechanism`: true.** `generate_world_bundle` gains an optional `max_description_chars` argument. That function has another caller, the public World Builder, so this is a change to a shared interface. The default stays 2,000, so that caller's behavior is unchanged, and a unit test pins the default. The summary handoff, the world-kind rule, the actor-coverage check and the role-brief mapping stay inside the spike, which has one consumer. Prior art and the parallel-implementation check are in the section above.
- **`empirical_comparison_proposed`: false.** One rerun, not a comparison of alternatives.

## Increments

1. Summary handoff, kind choice, coverage check and role briefs, with unit tests on the recorded Waltzman artifacts (K1-K3).
2. Pipeline rerun (K4).
3. Agent run, frames, assessment, evidence and gate (K5, K6).

## Loop Bounds

- **No-progress stop:** three attempts on the same reproduced blocker without new evidence.
- **Finite bound:** at most 2 pipeline runs and 3 agent runs, all reported.
- **Revalidation:** after three increments or about four hours.

## Non-Gating Next Actions

- Automatic choice of world kind for the public World Builder.
- A demo UI slice for Brian to click through.
- The pencil comparison with Cybernetic Influence.

## Assessment

To be written from the recorded run (K6).

## Current State

- **Superseded on 2026-10-08 by `docs/plans/scenario_spec_adoption.md`, before any work.** This plan patched the free-form outline step. The better fix is to adopt Cybernetic Influence v3's world schema, which already represents people with profiles and information items with recipients. The causes recorded above (summary cut at 1,500 of 6,188 characters; task world size) still hold for the old path.
