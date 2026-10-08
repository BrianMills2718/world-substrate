---
plan_id: "scenario-spec-adoption"
dependencies: ["waltzman-scenario-run", "system-model-pipeline"]
dependencies_reviewed: "2026-10-08"
planning_path: durable_solo
planning_path_ref: docs/plans/scenario_spec_adoption/path-decision.json
method_conformance_receipt: docs/plans/scenario_spec_adoption/conformance-receipt.json
supersedes: ["scenario-actors-kept"]
goal:
  outcome: "The describe-any-scenario pipeline defines each world in a typed scenario spec ported from Cybernetic Influence v3's world schema (people with behavioral profiles, information items with a source, channel and recipients, scheduled moments, world records with visibility, and a coverage report), compiles it into World Substrate state using the existing information module and the reviewed communicate rule, briefs each agent with its own person profile, and reruns Rand Waltzman's scenario with a fresh assessment of the paper's four mechanisms."
  canonical_example: "Running spikes/any-scenario-2026-10/model_scenario.py on the Waltzman scenario text produces a scenario_spec.json whose people include the technical, legal, logistics and community groups with profiles, and whose information items each name a source person, a channel and recipient members; the compiled world holds those items as information and delivery components; run_scenario.py briefs every agent with its own profile; the recorded run contains communicate events that deliver an item to exactly the named recipient; docs/plans/scenario_spec_adoption.md (Assessment) gives, per mechanism, event ids and rule ids or the plain reason it is missing."
  forbidden_substitutes: "hand-edited generated specs or worlds presented as generated; scripted agents presented as AI choices; profiles or information items written by hand instead of produced by the pipeline from the scenario text; the hand-authored reference_worlds/waltzman or the fixed native-coordination template presented as the generated world; a mechanism marked represented without an event id from the recorded run; rerunning until a mechanism appears and reporting only that run."
  boundaries: "world-substrate only; Cybernetic Influence v3 read-only and not a runtime dependency (Decision 005): its schema is ported with a pinned revision, not imported; work merges through pull requests after scripts/check_project.py passes on the merge commit with no test skipped; the public World Builder unchanged; no deploy, no outreach to Waltzman; model spend capped at $2 for this plan, measured by spikes/any-scenario-2026-10/spend.py from its value at the plan's start; raising it needs Brian's yes."
  done_when: "Acceptance checks S1-S6 in docs/plans/scenario_spec_adoption.md pass, each judged from the full trace of its named run (unit test output, llm_client trace ids, scenario_spec.json, compiled bundle, Engine event lists with event ids, agent attempt records with their briefs, frames with screenshots, the system-model drift test, project gate output on the merge commit); report the trace ids and evidence for each, and report every pipeline and agent run made."
  do_not_gate_on: "whether any particular mechanism appears; Brian's review; Waltzman's reaction or any outreach; the hospital pipeline-only result; the pencil comparison; the AES repository-model plan; issue BrianMills2718/company-planning#66."
  stop_after: 3
---
# Plan: define generated worlds in Cybernetic Influence's scenario schema

## Goal

**Mission:** a demo in which Rand Waltzman describes any scenario and watches it play out. When his scenario was run, nothing he describes happened. The describe-any-scenario pipeline defines worlds as plain entities with numbers, so it has no place for "the legal group holds a concern and sends it to Country B". World Substrate's own system model now records this gap (`docs/model/ODD.md`, section 4.2). Cybernetic Influence v3 already has a world schema that represents exactly these things. This plan adopts that schema as the pipeline's world definition and connects it to World Substrate mechanisms that already exist.

**What exists and is reused:**

- **Cybernetic Influence v3's world schema:** `GeneralSimulationProposalV1` (`cybernetic_influence_v3/src/cybernetic_influence/general_simulation/authoring_models.py:284`, revision `1c1c207`). Its system model is in `cybernetic_influence_v3/docs/model/ODD.md`.
- **World Substrate's information module:** `src/world_substrate/information.py`, with an `information` component (content, source, channel) and a `delivery` component per recipient.
- **The reviewed declarative `communicate` rule:** in `examples/native_coordination/coordination-causal-v0.json`. A member delivers one information item through its declared delivery record to its declared recipient.
- **The rest of the pipeline:** the mechanics generator, checks, repair loop, Concordia agents, game master and replay (`spikes/any-scenario-2026-10/`).

**Superseded:** plan `scenario-actors-kept` (`docs/plans/scenario_actors_kept.md`). It patched the free-form outline step, which is the wrong layer. Its causes stay recorded there.

**Execution profile:** `continuous-light`. One writer, reversible, one repository.

**Stage and investment boundary:** about one day of agent work and at most $2 of model spend.

## Actor, result and authority

- **Actor:** Brian, deciding whether describe-any-scenario can play out Waltzman's scenario.
- **Result:** generated worlds defined in the ported scenario spec, and a rerun of Waltzman's scenario with an assessment.
- **Stable example of the result:** for the Waltzman text, `scenario_spec.json` has a person `legal-group`, with goals and decision tendencies taken from the text. It has an information item with source `legal-group`, channel `legal-channel` and recipients `["country-b"]`. The compiled bundle has an entity with an `information` component for that item, and a `delivery` component with `status: "pending"` for `country-b`. When the legal group's agent sends it, one `communicate` event sets that delivery to `delivered`, and Country B's next attempt record cites it. The real ids come from the recorded run.
- **Authority:** Brian, 2026-10-08. He was concerned that "cybernetic_v3 and what was learned developing there is not being used", and answered "yea" to adopting its schema. The implementing agent is the sole writer.
- **Non-goals:**
  - porting Cybernetic Influence's runtime, stores, API or pages;
  - spatial, resource and transport parts of the schema (not needed for this scenario; listed as unsupported in the coverage report);
  - changing the public World Builder;
  - contacting Waltzman or deploying anything.

## System model

**System model:** `docs/model/ODD.md`, with `docs/model/world_substrate_model.toml`, `docs/model/VIEW_COVERAGE.md` and the drift test `tests/test_system_model.py`.

Model elements this plan adds, changes or relies on, and what the examined run must show of each:

| Element | Kind | Change | What the examined run must show |
| --- | --- | --- | --- |
| Scenario spec (`scenario_spec.json`) | record | adds | The S4 pipeline run folder holds `scenario_spec.json`, validated by the `ScenarioSpecV1` contract, with its trace id in `model.json`. |
| Person with behavioral profile | entity kind | adds | Every person in the spec is an actor entity in the S4 bundle, and each S5 attempt record carries that person's profile brief. |
| Information item and delivery (`information`, `delivery` components) | entity kind | relies on; the pipeline now produces it | The S4 bundle holds one `information` entity per spec item and one pending `delivery` per recipient. The S5 events include `communicate` events whose changes set one delivery's status to `delivered`. |
| Scheduled moment | entity kind | adds | Each spec moment compiles to a countdown entity with a due process. The S5 events show that process firing at the scheduled tick (an event of the moment's rule id). |
| Coverage report (`coverage.json`) | record | adds | The S4 folder holds `coverage.json`, with one row per spec behavior marked exact, coarse, descriptive or unsupported, and every unsupported row shown in the assessment. |
| `communicate` rule | process (action) | relies on | Rule `communicate`, taken from the reviewed coordination model, is present in the S4 `causal.json` and fires in S5. |
| Scenario model step (`model_scenario.py` model step) | process | changes | Its trace in S4 is a structured `ScenarioSpecV1` call. The free-form outline handoff (`odd_brief`) is no longer on the path. |
| Scenario replay (`frames.html`) | view | changes | The S5 screenshot shows a delivery: the state panel lists the `communicate` event id and the delivery status change. |

The system model's files, its drift test and VIEW_COVERAGE are updated in the same change as the code (S3).

## Design

1. **Port the contract.** Port a Pydantic `ScenarioSpecV1` into the spike, carrying a provenance header with the Cybernetic Influence revision `1c1c207` and the source classes. It covers:
   - people: id, label, position, disposition, memories, and a profile with goals, beliefs, decision tendencies, capabilities and limitations;
   - information items: id, content, apparent source, the true source person, channel, recipient ids, and the initial holder;
   - scheduled moments: id, tick, description, participant ids;
   - world records: id, kind, state, and the actor ids that can see them;
   - behaviors (component requests): description, subjects, fidelity need;
   - fidelity assumptions and unresolved questions.

   Client-side validation checks that every reference names a declared id.
2. **Model step.** One structured call fills `ScenarioSpecV1` from the scenario text. It replaces the free-form ODD call and its 1,500-character summary.
3. **Compiler (deterministic, no model call).** The compiler produces:
   - people as actor entities;
   - information items as `information` components with one pending `delivery` per recipient, plus the reviewed `communicate` rule;
   - scheduled moments as a countdown entity with a due process;
   - world records as entities with their state;
   - a coverage report row per behavior.
4. **Mechanics for the remaining behaviors.** The existing generator writes rules for the behaviors the compiler does not cover, such as meetings that slow, reopened issues and conditional support, against the compiled bundle. The checks and repair loop run as today.
5. **Agent briefs.** `run_scenario.py` briefs each agent with the scenario text, then its own person profile.

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| S1 | `ScenarioSpecV1` is ported with provenance. Its unit tests accept a spec built from the Cybernetic Influence pencil draft's people, and reject dangling references. | test output; provenance header |
| S2 | The compiler turns a recorded spec into a bundle with person actors, information and delivery components, countdown moments and a coverage report, with the `communicate` rule compiled by `CausalModel.from_dict`. An Engine test delivers one item to exactly its recipient in one event. | test output with event id and changes |
| S3 | The system model, its drift test and VIEW_COVERAGE are updated for the elements in the System model table, and the drift test bites once | drift-test output, before and after the bite |
| S4 | A fresh pipeline run on the Waltzman text yields a validated spec with the four groups as people with profiles and information items with recipients, a compiled bundle, a coverage report and checks | trace ids in `model.json`; the spec's people and items; coverage rows; check counts; every pipeline run made |
| S5 | AI agents run on that world on Concordia, each briefed with its own profile, with the Engine as sole authority and the game master on. Frames are rendered with a screenshot of a round with a `communicate` event. | run summary; trace id; attempt records showing briefs; `communicate` event ids; screenshot path |
| S6 | An assessment gives each of the four mechanisms an event id and rule id from the S5 run, or a reason it is missing. Evidence is committed, and the project gate passes on the merge commit with no test skipped. | the Assessment section; gate output saved beside the evidence |

## Trace review per criterion

| ID | Run whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| S1 | The `ScenarioSpecV1` unit-test run on the recorded Cybernetic Influence pencil draft (`personal-vps:/srv/apps/waltzman/data/authoring_drafts/draft_49524bf20017.json`, copied to `evidence/scenario-spec/pencil_draft.json`) | `tests/test_scenario_spec.py` output | The contract accepts the draft's 3 people and their profiles, and rejects a spec whose information item names an undeclared recipient. |
| S2 | The compiler and Engine unit-test run on the recorded spec | `tests/test_scenario_spec.py` output | One Engine event changes exactly one `delivery` status to `delivered` for the named recipient, and no other delivery. |
| S3 | The drift-test run before and after the bite | test output in the PR | It fails naming the renamed record, then passes. |
| S4 | Pipeline run `runs/waltzman-spec-<stamp>/`, made by `model_scenario.py --name waltzman-spec`; every run made is listed | traces `any-scenario-waltzman-spec-*-<stamp>`; `scenario_spec.json`, `bundle.json`, `coverage.json`, `causal.json`, `checks.json`; copied to `evidence/waltzman-spec/` | Each System model row's S4 mark holds. The spec is not hand-edited. |
| S5 | Agent run `runs/waltzman-spec-<stamp>/run-<stamp2>/`; every run made is listed | trace `any-scenario-run-waltzman-spec-<stamp>-<stamp2>`; `events.jsonl`, `attempts.jsonl`, `summary.json`, frames; packed with `run-artifacts` | Each System model row's S5 mark holds: briefs, `communicate` events, moment events, and the screenshot. |
| S6 | The full trace of the S5 run, and the project gate on the merge commit | as S5, plus `causal.json` and `coverage.json`; `evidence/waltzman-spec/gate-merge-<commit>.log` | Every "represented" cell cites ids that exist in those files. The gate runs with `node` and `llm_client` available, with no test skipped. |

## Success and disproof

- **Success,** with the recorded evidence that establishes each check:
  - **S1:** `tests/test_scenario_spec.py` passes on the recorded pencil draft (3 people accepted) and refuses a dangling recipient.
  - **S2:** the compiler test shows one `communicate` Engine event setting exactly one `delivery` to `delivered`.
  - **S3:** the drift test fails on the bite, then passes.
  - **S4:** `evidence/waltzman-spec/scenario_spec.json` lists the four groups as people with profiles, and information items with recipients. Its trace ids are in `model.json`.
  - **S5:** the agent run's `events.jsonl` holds at least one `communicate` event, and `attempts.jsonl` shows each agent's profile brief, with a screenshot of that round.
  - **S6:** the Assessment cites only ids found in those files, and `gate-merge-<commit>.log` shows exit 0 with no test skipped.

  The assessment must be accurate against the recorded files.
- **Disproof** (of the claim that the missing world schema was the main reason nothing happened): the spec holds the groups and their concerns, the concerns are deliverable, and agents still deliver none, or deliver them and none of the four mechanisms appears. That points the next step at agent behavior or mechanics.

## Model calls

- **Call graph and result boundaries,** in pipeline order:
  - **Scenario spec (changed):** one structured call returning `ScenarioSpecV1`, validated client-side (ids and references).
  - **Compiler:** code only, no call.
  - **Mechanics:** a JSON causal model for the remaining behaviors, compiled by `CausalModel.from_dict`.
  - **Stock map, sensing map, outflow coverage:** Pydantic records validated against the world's own fields and rule ids.
  - **Extreme-conditions and anomaly reviews:** Pydantic verdicts with verbatim quotes.
  - **Rule writer:** a JSON change list, compiled locally.
  - **Agents:** the Pydantic `Attempt`, with the person's profile in the prompt.
  - **Game-master rules:** the same rule-writer call as above, returning a JSON change list `{changes: [{change: add_action|add_process|replace_*, rule: <CausalModel mechanic or process>}], why}` (`midrun.py`, via `rule_writer.propose_rule`). It is compiled locally by `CausalModel.from_dict` and judged by `static_checks`: the checks that need no simulation (structure, selectors, attempt-vs-outcome, conservation, unresolved activity, co-located links). The simulated `run_checks` took over 4 minutes per call on the 10-agent world. A rule is installed only if no blocking finding names it and the blocking count does not rise. Otherwise the attempt is recorded as an `unsupported.gm-ruling` Engine event with no changes. Each attempt leaves a record `{intent, trace_id, proposal, checks: {baseline_blocking, blocking, findings_on_new_rule}, event_id}` in `summary.json` under `rules_written_mid_run`.
- **Prose never mutates state.** Profiles shape attempts only; the Engine decides every consequence.
- **Tracing:** every call goes through `llm_client` with an `any-scenario-` trace id, summed by `spend.py`.

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's key.
  - **Authorizer:** Brian, 2026-10-08. The cap is $2, measured from `spend.py` at the plan's start.
  - **Raising the cap:** needs his explicit yes.
  - **Containment**, as enforced in code since 2026-10-08, after one run overshot the cap by $1.86 because game-master calls were not counted:
    - `model_scenario.py` and `run_scenario.py` refuse to start when `spend.py`'s logged total plus the run budget exceeds `CAP`;
    - during an agent run, spend is re-read from the call logs every tick, and the run stops (`ended: run_budget` or `plan_spend_cap`) when the run's logged spend exceeds its budget or the plan total exceeds `CAP`;
    - the game master is limited to 6 rule-writing attempts per run (`midrun.GM_MAX_ATTEMPTS`);
    - every model call goes through `llm_client` with a per-call `max_budget`.
  - **Expected cost:** about $0.60 to $1.20.
- **Irreversible actions:** none. There is no deploy and no outreach.
- **Promotion condition:** nothing is shown to Waltzman or deployed from this plan. Before any promotion, a fresh pipeline run of his text on a real model, with trace ids reported, must have an agent run showing at least three of the four mechanisms with Engine event ids.

## Uncertainties

This is the complete list of material uncertainties; each, resolving badly, changes the conclusion about how close the demo is.

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether one structured call fills a rich `ScenarioSpecV1` for the Waltzman text without dropping the groups | Implementing agent | S4 spec contents and trace |
| Whether countdown entities give the mechanics generator a usable meeting schedule, since declarative rules cannot read the world clock | Implementing agent | S2 test; S5 moment events |
| Whether agents briefed with profiles choose to send their concerns | Implementing agent | S5 attempt records and `communicate` events |
| Whether the generator writes slowing, reopening and conditional-support rules over the compiled world | Implementing agent | S4 `causal.json` and coverage rows |

## Prior art and parallel-implementation check

**Existing ownership.** The any-scenario pipeline, the information module and the native coordination model are owned by world-substrate, which Brian owns alone. Cybernetic Influence v3 is owned by Brian too, and is a read-only donor under Decision 005. No open plan claims a scenario spec for the pipeline.

**Internal lineage.**
- Cybernetic Influence v3's world schema and its system model (`docs/model/ODD.md`, PR #50).
- World Substrate's system model, section 4.2, which compares World Substrate kind by kind with that schema (PR #144).
- `src/world_substrate/information.py`, and the hand-authored `reference_worlds/waltzman` mechanics: `CommunicateRule`, `ReassessCommitmentRule`, `StartMeetingAction`.
- The native coordination authoring path, `scripts/native_coordination_authoring.py`, with its reviewed `examples/native_coordination/coordination-causal-v0.json`.
- The superseded plan `scenario-actors-kept`.

**External prior art.**
- The ODD protocol, which describes entities and processes and which the pipeline uses today.
- Generative Agents (Park et al., 2023), which seeds each agent with a natural-language identity.
- Concordia, whose per-player context holds a player's profile.

| Candidate | Disposition |
| --- | --- |
| Cybernetic Influence v3 `GeneralSimulationProposalV1` | **reuse (port)**: the subset above, with pinned provenance; not imported (Decision 005) |
| `world_substrate.information` components | **reuse** as the compiled form of information items |
| Native coordination `communicate` rule | **reuse** as the delivery mechanic |
| Hand-authored Waltzman meeting and commitment mechanics | **bounded exception**: Waltzman-specific; used as a reference for what the generator should produce, not compiled in |
| Native coordination authoring (fixed family) | **bounded exception**: a fixed template; the point here is any scenario |
| Free-form ODD step and `odd_brief` | **supersede** on this path by the scenario spec |
| ODD protocol (Grimm et al.) | **reuse**: it remains the format of the system model (`docs/model/ODD.md`); in the pipeline, the scenario spec replaces the ODD-shaped outline as the world definition |
| World Substrate system model, section 4.2 donor comparison | **extend**: it gains the scenario spec, person, scheduled moment and coverage report elements (S3) |
| Cybernetic Influence v3 system model (`docs/model/ODD.md`, PR #50) | **reuse** as the source description of the ported kinds (read-only) |
| Plan `scenario-actors-kept` | **supersede** |
| Generative Agents and Concordia per-player context | **reuse the idea**: the person profile is the agent's brief |

**Check for a silent parallel implementation:** `git diff --stat origin/main` at the end touches only `spikes/any-scenario-2026-10/`, `tests/test_scenario_spec.py`, the system-model files, the evidence folders, and this plan and the superseded one. No second information or delivery component is defined: a grep for `register_component("information"` finds only `src/world_substrate/information.py`.

## Activation facts

The machine record is `scenario_spec_adoption/activation-facts.json`.

- **`llm_central`: true.** World generation and agents are model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $2. Nothing is irreversible.
- **`shared_mechanism`: true.** The plan adds a typed scenario contract and a compiler that other paths could consume, and it changes the system model. It reuses `world_substrate.information` and the reviewed `communicate` rule without changing them.
- **`empirical_comparison_proposed`: false.** One rerun, not a comparison of alternatives.

## Increments

1. Contract, compiler, briefs and system model, with unit tests and no model calls (S1-S3).
2. Pipeline run (S4).
3. Agent run, frames, assessment, evidence and gate (S5, S6).

## Loop Bounds

- **No-progress stop:** three attempts on the same reproduced blocker without new evidence.
- **Finite bound:** at most 2 pipeline runs and 3 agent runs, all reported.
- **Revalidation:** after three increments or about four hours.

## Non-Gating Next Actions

- Offer the scenario spec to the public World Builder.
- Spatial, resource and transport parts of the schema.
- The AES repository-model plan.

## Assessment

From pipeline run `waltzman-spec-20261008T174927` (world defined by `scenario_spec.json`, spec trace `any-scenario-waltzman-spec-spec-20261008T163904`, rules trace `any-scenario-waltzman-spec-mechanics-20261008T174927`) and agent run `run-20261008T184545` (trace `any-scenario-run-waltzman-spec-20261008T174927-20261008T184545`). The agent run went 12 ticks with 105 Engine events and 74 attempts, and spent $0.66 by the call logs. Evidence is in `spikes/any-scenario-2026-10/evidence/waltzman-spec/run2/`, and the tests are `RecordedWaltzmanRunTests`.

**Bottom line:** all four of the paper's mechanisms appear as Engine events, driven by the AI agents' own choices. Two are only roughly represented. The run's one "deployment blocked" event is not valid; the bug behind it is fixed.

| Mechanism | Verdict | Evidence | What is missing |
| --- | --- | --- | --- |
| Concerns delivered to different members through separate channels | represented | `e00005`–`e00008`, rule `coordination.action.communicate` (the reviewed rule). Each event delivers one group's concern to exactly one country, for example `e00006`: legal group to Country Two, delivery `pending`→`delivered`. At tick 1, Country Two's attempt cites that concern ("…(to country_two).topic: legal_concern") and makes its support conditional on it (`e00015`). | — |
| Meetings that slow | represented roughly | `hold-scheduled-member-meeting` was held 7 times (`e00013`, `e00024`, …, `e00090`). Reopened issues set meeting progress back, for example `e00025` takes progress from 60 to 50. | The generated meeting rule adds to `meetings_delayed` at every meeting, whatever the concerns, so that counter is not evidence of slowing. The slowing that is evidenced is progress lost to reopened issues. |
| Settled issues that reopen | represented | 14 events of `reopen-issue-for-known-concern`, for example `e00025` (Country Two, `settled_issues_reopened` 0→1) and `e00026` (Country Four). | — |
| Support that becomes conditional | represented roughly | `declare-conditional-support` `e00014`–`e00017`, with `conditional_support_count` 0→4. By round 5 every member's support is `conditional` (`run/frame-round5-state.png`). | The condition is a status and a count; it does not record which concern the support depends on. Resolving a concern cannot restore support automatically. |

**The block that was not valid:** `e00047` (`block-at-deadline-for-missing-support`, tick 5) blocked deployment. But its "the decision deadline has occurred" check read the *weekly meeting's* occurrence count (5), not the deadline's (0). The slot named `activation_decision_deadline` accepted any moment. This is fixed by `pin_named_slots`: a slot named after a specific record or moment accepts only that entity, and the test `test_pinned_slots_refuse_the_meeting_as_the_deadline` covers it. No valid run of the deadline outcome exists yet.

**What to fix next** (from this run): store conditional support as a commitment linked to the concern it depends on, with states conditional, met and broken (Singh's commitments; see the research in this session). Make meeting slowing depend on open concerns. Both belong in the metamodel integration discussed with Brian, not in more spike patches.

## Current State

- **S1-S3 met** (commits `9c03de6`, `a743a64`, `f59ff66`): the contract, the compiler with its Engine test, and the system model. The drift test failed twice before the model update and passes 14 of 14 after it (`evidence/scenario-spec/drift-*.log`).
- **Pipeline run 1** (`waltzman-spec-20261008T163904`, trace `any-scenario-waltzman-spec-spec-20261008T163904`) stopped at a bundle naming error: action kinds need hyphens.
- **Run 1b** (`--from-spec`, same spec) wrote the rules. Its repair loop was stopped before its first check finished.
- **Agent runs on that world:**
  - Two launches stalled with no model calls: discovery took about 1 second per agent, and the game master's simulated baseline check took over 4 minutes.
  - One run, `run-20261008T174222`, was stopped at the audit after its first tick.
- **Audit, 2026-10-08:**
  - Generated rules never changed the world's records, because action signatures had no fields for them.
  - Coverage counted an action's existence as coverage.
  - Generated processes double-counted the meeting countdown.
  - All three are repaired and tested against the recorded files: `RecordedPipelineRepairTests`, with evidence in `evidence/waltzman-spec/pipeline1/`.
- **Deviation from the declared diff scope:** `src/world_substrate/engine.py`. `Engine.discover` now checks the read-only view once per page and re-runs hook by hook only when it changed, which is 12 times faster with the same errors. Also changed: `spikes/any-scenario-2026-10/checks.py` (`static_checks`) and `midrun.py`. These are needed to run 10 agents. The project gate passes 572 of 572.
- **Pipeline run 2** (`waltzman-spec-20261008T174927`, `--from-spec`, after the audit repairs): every behavior is now covered by a rule that changes its records. Its simulated check was stopped after about 25 minutes. `checks.json` holds the static checks: 1 blocking finding, liveness on `authorize-supported-ready-deployment`.
- **Agent run on pipeline run 2** (`run-20261008T181230`): it crashed at tick 10 when OpenRouter credit ran out. The run folder is empty, because events were written only at the end. The progress log is kept at `evidence/waltzman-spec/run1-crashed/members.log`. In it:
  - all four groups delivered their concerns to their own country at tick 0 (`e00002`-`e00005`);
  - the countries made support conditional at tick 1 (`e00011`-`e00014`);
  - meetings were held each tick;
  - Country Two reopened a settled issue at tick 10.

  Those event ids appear only in the log; the Engine's change records are lost.
- **Spend over the cap:**
  - The game master's rule writing cost $3.30 (32 calls) in that run.
  - The run budget counted only the residents' $0.23.
  - The plan total reached $11.45 against the $9.59 cap: $1.86 over, without Brian's yes.
- **Fixed:**
  - the run budget now comes from the call logs, and the plan cap is checked every tick;
  - the game master is limited to 6 rule-writing attempts per run;
  - events and attempts are written every tick, and a failure writes a summary naming the error, then re-raises (verified with a failing model id).
- **Blocked:** S5 and S6 need one more agent run. That needs more credit on the OpenRouter account ($0.57 left) and Brian's yes to raise the cap.
- **Credit and cap:** Brian added credit and approved $2 more from $11.45 ("yeah i added mroe money"), so `CAP` = $13.45.
- **Agent run `run-20261008T184545`** (complete): 12 ticks, $0.66 by the logs, game master stopped at 6 attempts. Its block event was found invalid during the assessment and the slot-pinning fix was added.
- **Every run made in this plan:**
  - pipeline runs: 1 (stopped at a naming error), 1b (repair loop stopped), and 2 (static checks);
  - agent launches stalled with no model calls: two;
  - agent runs: `run-20261008T174222` (stopped at the audit after tick 1), `run-20261008T181230` (credit ran out at tick 10, log only), and `run-20261008T184545` (complete);
  - plus one run that tested the failure path with a fake model id and made no calls.

