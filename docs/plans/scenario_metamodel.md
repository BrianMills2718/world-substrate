---
plan_id: "scenario-metamodel"
dependencies: ["scenario-spec-adoption"]
dependencies_reviewed: "2026-10-08"
planning_path: durable_solo
planning_path_ref: docs/plans/scenario_metamodel/path-decision.json
method_conformance_receipt: docs/plans/scenario_metamodel/conformance-receipt.json
goal:
  outcome: "The describe-any-scenario world definition becomes one metamodel joined from Brian's existing pieces rather than a further reinvention: Cybernetic Influence's scenario kinds mapped onto the scientific-hypergraph kernel (concepts and n-ary relations) and the observation-to-action vocabulary (observation, belief, decision, affordance, action, effect), plus two new kinds the Waltzman run showed are missing, commitments (debtor, creditor, condition, state conditional/met/broken) and issues (open, resolved, reopened). Brian reviews it as a diagram first; then the pipeline compiles commitments and issues with reviewed rules, and Waltzman's scenario is rerun and reassessed."
  canonical_example: "docs/model/scenario-metamodel.typed-graph.json renders in Representation Router's graph viewer as a diagram where 'Country Two supports activation on condition that the legal issue is resolved' is one Commitment node with debtor, creditor, condition and consequent roles, mapped to the hypergraph kernel's relation/role-binding types and to observation-to-action's Decision and Effect; and a fresh Waltzman agent run records a commitment going conditional -> met when its issue is resolved (or broken at the real deadline), with Engine event ids, and meeting progress slowed by open issues."
  forbidden_substitutes: "a new metamodel invented without mapping to the hypergraph kernel and the observation-to-action vocabulary; a diagram drawn by hand outside the router's graph viewer; commitments or issues as free-text fields or counters; hand-edited generated specs or worlds presented as generated; scripted agents presented as AI choices; a mechanism marked represented without an event id from the recorded run; rerunning until a result appears and reporting only that run."
  boundaries: "world-substrate only for writes; scientific-hypergraph, observation-to-action-metamodel, cybernetic_influence_v3 and representation-router are read-only and pinned by revision; work merges through pull requests after scripts/check_project.py passes on the merge commit with no test skipped; the public World Builder unchanged; no deploy, no outreach to Waltzman; model spend capped at $2 for this plan, measured by spikes/any-scenario-2026-10/spend.py from its value at the plan's start; raising it needs Brian's yes."
  done_when: "Acceptance checks M1-M5 in docs/plans/scenario_metamodel.md pass, each judged from the full trace of its named run or test (mapping and drift tests, the rendered diagram screenshot, llm_client trace ids, Engine event lists with event ids, agent attempt records, project gate on the merge commit); report the evidence for each and every pipeline and agent run made."
  do_not_gate_on: "Brian's review of the diagram (it is shown to him, not awaited); whether the commitment is met or broken in the run; Waltzman's reaction or outreach; OneSim adoption; the public World Builder; company-planning issues #66 and #72."
  stop_after: 3
---
# Plan: one scenario metamodel joined from existing pieces

**Authority:** Brian, 2026-10-08. He was concerned that "cybernetic_v3 and what was learned developing there is not being used" and wanted "a systematic way of building these worlds… what are all the concepts, how do they relate, how do they change, what can they do". Then: "ok if its planed otu with company plannign then give m the /goal ext", replying to the recommendation to join his modeling pieces.
**Selected controls:** one writer; reversible; model spend capped at $2; other repositories read-only.
**Artifact consumer / decision value:** Brian decides whether describe-any-scenario has a stable world model to build the Waltzman demo on. The diagram is what he judges.
**Stage / investment boundary:** prototype. About one day of agent work.
**Last outcome-bearing update:** the scenario-spec-adoption run (`757b35c`, 2026-10-08). All four mechanisms appeared, but conditional support was only a count and meeting slowing was not driven by concerns.

## Outcome And Boundaries

**Outcome:** Brian, and the agents that build worlds, get one documented metamodel: concepts, relations, change and capabilities. Generated worlds are compiled from it, so "support on condition X" and "a reopened issue" become real objects with states that the Engine changes.

**System model:** `docs/model/ODD.md`, with `docs/model/world_substrate_model.toml`, `docs/model/VIEW_COVERAGE.md` and the drift test `tests/test_system_model.py`.

**Model elements:**

| Element | Kind | Change | What the examined run must show |
| --- | --- | --- | --- |
| Scenario metamodel (`docs/model/scenario-metamodel.typed-graph.json`) | record | added | It validates against representation-router's `typed-graph` schema. Every kind maps to a hypergraph-kernel relation or role type and to an observation-to-action relation, or carries an explicit "no counterpart" row (mapping test). |
| Commitment | entity kind | added | The M4 bundle holds commitment entities. M4 events include a commitment's state changing (conditional to met, or conditional to broken) under a compiled rule. |
| Issue | entity kind | added | The M4 bundle holds one issue per concern. M4 events include an issue changing state: open, resolved or reopened. |
| ScenarioSpec | record | changed | `scenario_spec.json` from the M4 pipeline run lists commitments and issues. |
| Compiler (`compile_spec.py`) | process | changed | The M2 tests show commitments and issues compiled with reviewed rules: commitment-met, commitment-broken, issue-resolve and issue-reopen. |
| Scenario replay (`frames.html`) | view | relied on | The M4 screenshot shows a commitment state change, with its event id in the state panel. |
| Scenario metamodel diagram | view | added | The M1 screenshot of the graph viewer shows the joined metamodel. |

**Canonical probe:**
- **Starting state:** the recorded Waltzman spec, plus commitments and issues from the spec step.
- **Action:** agents run.
- **Inspectable result:** a commitment changes state from conditional to met when its issue is resolved, or to broken at the real deadline, with event ids.
- **Negative case:** a commitment whose issue is still open cannot be met. The M2 test refuses this.

**Success evidence:** M1-M5 below. M1 is the mapping test passing and the diagram rendering in the viewer. M2 is the Engine test showing conditional to met only when the issue is resolved. M4 is the recorded run's commitment and issue events. M5 is the assessment citing them, plus the merge-commit gate.

**Disproof** (of the claim that joining the existing pieces gives a usable world model):
- more than half of the scenario kinds map to "none" in both the kernel and observation-to-action, so the existing pieces don't describe these worlds; or
- with commitments and issues compiled, the agents' run shows no commitment or issue state change.

Either result is reported as the outcome, not hidden.

**Trace review:** for each model element, the run examined and what it must show:
- **Scenario metamodel record:** in the M1 mapping-test run, every kind's kernel and observation-to-action ids exist in the pinned files, or the row says "none".
- **Commitment:** in the M4 agent run's `events.jsonl`, at least one event changes a commitment entity's `state` (conditional to met, or conditional to broken) under a compiled rule id. The M2 test shows the refused case: a met attempt with its issue open leaves the state unchanged.
- **Issue:** in the M4 events, at least one event changes an issue's `status` (open to resolved, or resolved to reopened), with its event id.
- **ScenarioSpec:** the M4 pipeline run's `scenario_spec.json` lists commitments and issues, and its spec trace id is in `model.json`.
- **Compiler:** the M2 test output shows the four compiled rules.
- **Scenario replay:** the M4 screenshot's state panel lists a commitment event id that exists in `events.jsonl`.
- **Scenario metamodel diagram:** the M1 screenshot comes from the graph viewer rendering the metamodel file.

M4's full trace must also show meeting progress changing with the number of open issues (event ids). M5's assessment gives every missing mechanism an explicit reason, and is committed with the evidence in the merged pull request.

**Authority:** Brian holds authority over this work and approved it on 2026-10-08. The implementing agent is the sole writer and decides reversible implementation choices. Brian's yes is required to raise the spend cap, deploy anything, or contact Waltzman.

**Non-goals:**
- changing the other repositories;
- the public World Builder;
- OneSim adoption;
- a demo screen for Waltzman;
- tuning until a mechanism appears.

**Authority limits:** $2 of model spend; no deploy, no outreach.

## Architecture And Capability Invariants

- The Engine is the only writer of world state. Commitments and issues change only through compiled rules.
- Compiled rules own the components they write (`spec_pipeline.COMPILED_COMPONENTS`); generated rules may read them but not write them.
- Every metamodel kind maps to the hypergraph kernel and to observation-to-action, or says plainly that it has no counterpart.

```text
diagram (router graph viewer) <- scenario-metamodel.typed-graph.json <- mapping (kernel, O2A, CI kinds) <- sources pinned by revision
replay events <- Engine <- compiled commitment/issue rules <- ScenarioSpecV1 (+commitments, issues) <- scenario text
```

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| M1 | The joined metamodel exists as a typed graph. It maps every ScenarioSpecV1 kind, plus Commitment and Issue, to scientific-hypergraph kernel elements (`dbe2c72`) and observation-to-action relations (`d27d160`), each mapping marked exact, partial or none. It renders in Representation Router's graph viewer. | mapping test output; screenshot of the rendered diagram |
| M2 | ScenarioSpecV1 gains commitments and issues. The compiler emits reviewed rules for issue resolve and reopen and for commitment met and broken. Engine tests show conditional to met only when the issue is resolved, and conditional to broken when the deadline moment occurs. | test output with event ids |
| M3 | The system model and drift test are updated for the new elements, and the drift test bites once | drift test output, before and after |
| M4 | A fresh pipeline run on the Waltzman text produces commitments and issues. An agent run records commitment and issue state changes, and meeting progress affected by open issues. | trace ids; spec; event ids; screenshot; every run made |
| M5 | An assessment per mechanism gives event ids or the reason a mechanism is missing. Evidence is committed, and the project gate passes on the merge commit with no test skipped. | Assessment section; gate output |

| ID | Run or test whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| M1 | No model run is needed: the metamodel is data, so its full trace is the run of `tests/test_scenario_metamodel.py` on the metamodel file against the pinned source files (`hypergraph-kernel-v2.json` at `dbe2c72`, `03-VOCABULARY.jsonld` at `d27d160`), plus one render of the graph viewer | the test output saved as `evidence/scenario-metamodel/mapping-test.log`; `evidence/scenario-metamodel/diagram.png` | Each mapped id exists in the pinned source files, and the test fails when one is renamed (shown once). The screenshot comes from the viewer, not a hand drawing. |
| M2 | The compiler and Engine unit-test run on a recorded spec plus a test commitment | `tests/test_scenario_spec.py` output | The met event changes only the commitment's state. The refused case leaves the state hash unchanged. |
| M3 | The drift test run before and after | PR output | It fails naming the new record, then passes. |
| M4 | Pipeline run `runs/waltzman-meta-<stamp>/` and agent run `run-<stamp2>/`; every run made is listed | traces `any-scenario-waltzman-meta-*`; `events.jsonl`, `attempts.jsonl` and `summary.json`, copied to `evidence/waltzman-meta/` | The full trace shows commitment state changes and issue state changes, each with an event id, and meeting progress changing with open issues. An agent's attempt record names the commitment in its decision. |
| M5 | The M4 run's full trace, and the gate on the merge commit | as M4; `gate-merge-<commit>.log` | Every "represented" cell cites ids that exist in the run's files, and every missing mechanism has an explicit reason. The assessment and evidence are committed in the merged pull request. The gate runs with `node` and `llm_client` available, with no test skipped. |

## Milestone Horizon

| Milestone | Planning state | Inspectable output / stable boundary | Required capability and evidence | Promotion or replan trigger |
|---|---|---|---|---|
| 1. Metamodel and diagram | fully_specifiable_now | typed graph plus screenshot (M1) | the mapping test | a source kind with no counterpart in either vocabulary is recorded as "none", not invented |
| 2. Commitments and issues compiled | fully_specifiable_now | compiler and Engine tests (M2, M3) | unit tests, no spend | the generator cannot express slowing from open issues, which leads to a compiled rule |
| 3. Waltzman rerun and assessment | conditional | evidence plus assessment (M4, M5) | one pipeline run and one agent run, about $1 | over cap, which means stop and ask Brian |

## Active Slice

**Visible result:** the joined metamodel as a diagram Brian can open (M1).
**Input / output and affected boundaries:**
- inputs: `scenario_spec.py`, the kernel file (`hypergraph-kernel-v2.json` at `dbe2c72`), `03-VOCABULARY.jsonld` at `d27d160`, and representation-router's `typed-graph` schema;
- output: `docs/model/scenario-metamodel.typed-graph.json`.

**Implementation constraints:** the other repositories stay read-only; copy the ids, not their files.
**Focused check and authentic observation:** the mapping test, and the viewer screenshot.
**Failure / containment / rollback:** a mapping the sources do not support is marked "none". All changes revert by PR.

## Model calls

- **Call graph and result boundaries:**
  - **Scenario spec:** one structured call returning `ScenarioSpecV1`, now with `commitments[]` and `issues[]`, validated client-side (references and states).
  - **Compiler:** code only, no call.
  - **Action signatures:** a Pydantic list, validated.
  - **Mechanics:** a JSON causal model compiled by `CausalModel.from_dict`.
  - **Agents:** the Pydantic `Attempt`.
  - **Game-master rules:** a JSON change list judged by `static_checks`, at most 6 per run.
- **Prose never mutates state.**
- **Tracing:** every call goes through `llm_client` with an `any-scenario-` trace id. Spend is read from the call logs each tick (`run_scenario.py`).

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's key.
  - **Authorizer:** Brian, 2026-10-08.
  - **Cap:** $2 from `spend.py` at the plan's start.
  - **Containment:**
    - the start-up guard;
    - spend re-read from the logs every tick, stopping the run at its budget or the plan cap;
    - a limit of 6 game-master attempts per run;
    - a per-call `max_budget`.
  - **Raising the cap:** needs his yes.
  - **Expected cost:** about $1.
- **Irreversible actions:** none.
- **Promotion condition:** nothing is shown to Waltzman from this plan. Before any promotion, a fresh run of his text must show commitment and issue state changes with Engine event ids.

## Uncertainties

This is the complete list of material uncertainties; each, resolving badly, changes how close the demo is.

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether the kernel and observation-to-action ids cover the scenario kinds, or many map to "none" | Implementing agent | M1 mapping table |
| Whether one structured call fills commitments and issues from the Waltzman text | Implementing agent | M4 spec |
| Whether agents resolve issues, so that commitments become met, or only reopen them | Implementing agent | M4 events |

## Prior art and parallel-implementation check

**Existing ownership.** World Substrate owns the pipeline. scientific-hypergraph owns the kernel. observation-to-action-metamodel owns its vocabulary and states that it imports the kernel. Representation Router owns the graph viewer. All are owned by Brian. No open plan claims a scenario metamodel.

**Internal lineage.**
- Company planning's `typed-relational-metamodels.md` names world-substrate and observation-to-action as "still-unintegrated reinventions".
- World Substrate's system model, section 4.2.
- Cybernetic Influence v3's system model.
- The scenario-spec-adoption plan and its run.
- Cybernetic Influence v1's perceive/act/change admission test.

**External prior art.**
- Singh's commitments ("debtor owes creditor the consequent if the antecedent holds"; states such as conditional, detached, discharged and violated).
- BSPL information protocols (the `bspl` Python package).
- Moise organisations.
- ODD+D.
- YuLan-OneSim (tested 2026-10-08: `spikes/any-scenario-2026-10/evidence/onesim-comparison.md`).

| Candidate | Disposition |
| --- | --- |
| scientific-hypergraph kernel | **reuse**: the relation, role and binding types the metamodel maps to |
| observation-to-action vocabulary | **reuse**: the change and capability relations |
| Cybernetic Influence ScenarioSpecV1 port | **extend**: add commitments and issues |
| Representation Router graph viewer and typed-graph schema | **reuse**: the diagram |
| company-planning typed-relational-metamodels rules | **reuse**: the design contract |
| Singh commitments | **compose**: the Commitment kind and its states follow Singh's model, inside our own spec |
| BSPL `bspl` package | **bounded exception**: not used in this plan; the information layer already compiles to the reviewed communicate rule |
| YuLan-OneSim | **bounded exception**: interview step and behavior graph deferred; see the comparison note |
| ODD+D | **bounded exception**: the system model keeps ODD; the decision-making extension is deferred |
| World Substrate system model, section 4.2 | **extend**: gains Commitment, Issue and the metamodel record (M3) |
| Cybernetic Influence v3 system model | **reuse** as the source description of the ported kinds |
| scenario-spec-adoption plan and its run | **extend**: this plan builds on its pipeline and evidence |
| Cybernetic Influence v1 perceive/act/change test | **reuse** as the admission test for each metamodel kind (recorded per row in the typed graph) |

**Check for a silent parallel implementation:** no second metamodel file or schema; a grep for `typed-graph.json` under `docs/model/` finds exactly one. `git diff --stat origin/main` touches only the spike, `docs/model/`, the new test, the evidence and this plan.

## Activation facts

The machine record is `scenario_metamodel/activation-facts.json`.

- **`llm_central`: true.** World generation and agents are model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $2.
- **`shared_mechanism`: true.** It adds a metamodel and new spec kinds that other plans and repositories will rely on.
- **`empirical_comparison_proposed`: false.** One rerun, not a comparison.

## Decisions And Assumptions

| Choice | Disposition | Reason / evidence | Affected boundary |
|---|---|---|---|
| Join the existing pieces instead of patching the spec | human_set | Brian's reply asking for the plan's goal text, after the recommendation | the metamodel |
| Commitment states conditional, met and broken (a subset of Singh's) | agent_decided_reversible | enough for "support on condition X" | compiler |

## Evidence And Current State

| Claim or result | Exact evidence | Limitation | Status |
|---|---|---|---|
| All four mechanisms appeared roughly in the scenario-spec run | `evidence/waltzman-spec/run2/`; `RecordedWaltzmanRunTests` | conditional support was a count; meeting slowing was not driven by concerns | prior plan |

- Demonstrated: none yet. Plan authored on 2026-10-08.

## Human Decisions

- None. The diagram is shown to Brian when M1 is done, and work does not wait on it.

## Assessment

To be written from the recorded run (M5).

## Exact Next Action

Write `docs/model/scenario-metamodel.typed-graph.json` and `tests/test_scenario_metamodel.py` (M1).
