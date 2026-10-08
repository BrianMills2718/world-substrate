---
plan_id: "linked-process-participants"
dependencies: []
dependencies_reviewed: "2026-10-08"
planning_path: durable_solo
planning_path_ref: docs/plans/linked_process_participants/path-decision.json
method_conformance_receipt: docs/plans/linked_process_participants/conformance-receipt.json
goal:
  outcome: "World Substrate processes can change linked entities in one atomic transition: a process names participants resolved from its own entity (ownership, an entity_ref field, or shared location), so the truck's driver moves with the truck and a dying patient frees the ventilator and bed, proven on the generated truck and hospital worlds."
  canonical_example: "Re-running the any-scenario truck pipeline on 'A delivery driver with a quarter tank must reach a town 120 miles away; there is one gas station at mile 60' yields a world whose driving process moves both the vehicle and its owner-driver each tick (driver.road_position equals vehicle.road_position in the recorded Engine events), and the hospital pipeline yields a death process that in one Engine event lowers patient_count and occupied_beds and frees an in-use ventilator."
  forbidden_substitutes: "hand-edited generated worlds presented as generated; a runner or Concordia component that moves the second entity outside Engine.submit/advance; two separate single-entity processes presented as one linked transition; tests that only exercise a hand-written fixture without a generated world; claims from code reading without a run."
  boundaries: "world-substrate only, sole writer, PRs merged after scripts/check_project.py passes; the new process field is optional and backward compatible (all existing tests unchanged and passing); Concordia, Mesa and other repositories read-only; no deploy, no change to the live World Builder or /waltzman/; model spend capped at $3 via llm_client max_budget, and raising it needs Brian's yes."
  done_when: "Acceptance checks L1-L6 in docs/plans/linked_process_participants.md pass, each judged from the full trace of its named run (llm_client trace IDs, Engine event lists with event IDs, check logs, unittest counts and exit code, project gate output); report the trace IDs and evidence for each."
  do_not_gate_on: "Brian's review of the result; the Waltzman bio-surveillance scenario run (next step); distance-limited sensing; wiring checks into the live World Builder; Simudyne's reply."
  stop_after: 3
---
# Plan: linked participants for processes (Decision 007 follow-up)

## Goal

**Mission:** In World Substrate, a process changes only its own entity ("it"). That limit broke both proof-of-concept worlds: the driver stayed at mile 0 while the truck drove, and a patient's death never freed a ventilator or bed (`docs/plans/any_scenario_poc.md`, Current State). Actions already change several bound participants atomically. This plan gives processes the same ability: participants resolved from "it" through links the world already records, with the same checks, write-scope enforcement and atomic commit.

**Execution profile:** `continuous-light`

One writer, reversible, one repository.

**Stage and investment boundary:** working increment, about one to two days of agent work. Model calls go through the shared `llm_client` on the OpenRouter route and are traced. Spend is capped at $3.

**Canonical examples:**

1. **Truck.** The generated truck world's driving process moves the vehicle *and* its owner-driver in one Engine event per tick: in the recorded events, `driver.road_position` always equals `vehicle.road_position`.
2. **Hospital.** The generated hospital world's death process, in one Engine event, lowers `patient_count`, lowers `occupied_beds` and raises `available_beds`. When the patient was ventilated, it also lowers `in_use_count`.

**Forbidden substitutes:** see the goal block. In short: no hand edits presented as generated; no second mutation path outside the Engine; no pair of single-entity processes presented as one linked transition.

**Repository / working scope:** `~/code/world-substrate`, under its `AGENTS.md`.

## Actor, result and authority

- **Actor:** Brian, deciding how far the "describe any scenario" Waltzman demo can go on World Substrate.
- **Result:** generated worlds where linked things change together, shown on the two proof-of-concept scenarios.
- **Concrete example of the result:** in a re-run of the truck scenario, the recorded event for the drive process at tick 5 changes both `Delivery vehicle.road_position` and `Delivery driver.road_position` from 40 to 50, under one event ID and one cause ID. The rendered frame's state panel shows both at mile 50.
- **Authority:** Brian approved this work on 2026-10-08 ("i approve. give me the new /goal text"). The implementing agent is the sole writer in world-substrate. Concordia, Mesa and the other repositories are read-only.
- **Non-goals:**
  - linked participants for actions (they already have them);
  - randomness in the rule language;
  - distance-limited sensing;
  - running the Waltzman scenario;
  - any change to the live World Builder or `/waltzman/`;
  - a deploy;
  - a benchmark between alternatives.

## Design

- **Process declaration.** It gains an optional `participants` object: `{name: {link, selector}}`. `link` is one of:
  - `owner_of_it`: the entity named by `it.ownership.owner_ref`;
  - `owned_by_it`: entities whose `owner_ref` names `it`;
  - `ref:<component.field>`: the entity named by an `entity_ref` field on `it`;
  - `co_located`: same `location.location_id`.

  `selector` (categories and components) narrows the result. A link that resolves to no entity makes the process not due for that `it`. A link that resolves to more than one entity applies to each, in sorted order, inside the same event.
- **Compiler.** It derives read and write paths for linked participants exactly as it does for action participants. Engine write-scope enforcement then covers every entity a process changes.
- **Engine.** No new commit path. A due process still produces one event; its changes may now span the linked entities.
- **Generator.** The causal-model schema and prompt gain the optional field, so generated worlds can use it. The layer-1 checks treat linked writes like any other write.
- **Backward compatibility.** A process without `participants` behaves exactly as today. All existing tests must pass unchanged.

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| L1 | Compiler accepts `participants` on processes, rejects unknown links or unresolvable fields with clear errors, and derives write paths that include linked entities | unittest names and counts, with exit code |
| L2 | Engine applies a linked process as one event whose changes span `it` and its linked entities. A write outside the derived scope is refused with nothing partially changed | unittest on a small world: the event ID, its changes, and a refusal case |
| L3 | Backward compatibility: every existing test passes unchanged | `scripts/check_project.py` output: test count at least 530, OK, exit 0 |
| L4 | Generated truck world uses a linked process, and the driver moves with the truck | model-step traces (`any-scenario-truck-*`), plus an Engine event list where every drive-process event changes both positions with equal values |
| L5 | Generated hospital world's death process changes the patient group and the hospital (and the ventilator stock when the patient was ventilated) in one event | model-step traces (`any-scenario-hospital-*`), plus an Engine event list with the death event's changes across the entities |
| L6 | Frames show the linked change | screenshots of the replay with the state panel at the drive tick and the death tick |

## Trace review per criterion

| ID | Run whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| L1 | Local unittest run of the new compiler tests | Terminal output saved to the run folder | Each named test, including the rejection cases, is listed as run. None is skipped, and the totals match the names. |
| L2 | Local unittest run of the new Engine tests | Terminal output | The single event's change list includes paths on both entities. The refusal case shows `status` refused and identical before/after hashes. |
| L3 | `scripts/check_project.py` in a git checkout | Terminal output | The total test count; no existing test was edited (`git diff --stat` on `tests/` shows only new files). |
| L4 | Truck pipeline run (model step plus a scripted-free AI-resident run) | `llm_client` traces by ID; run folder packed with `run-artifacts` | The generated process declares a linked participant. Every drive event changes both entities' positions under one event ID. |
| L5 | Hospital pipeline run | `llm_client` traces by ID; run folder | The death event's changes include the patient group, the hospital and, where applicable, the ventilator stock. |
| L6 | Replay render of L4 and L5 runs | Rendered HTML plus screenshots | The state panel round shows the linked changes under the same event ID. |

## Success and disproof

- **Success:** L1–L6 pass with the evidence above.
- **Disproof:** the approach is wrong if any of the following holds:
  - linked writes cannot be scope-checked without a second commit path;
  - generated worlds still fall back to two single-entity processes in both scenarios after the schema and prompt change;
  - an existing test has to be edited to pass.

## Model calls

- **Call graph and result boundaries,** in pipeline order. Each call returns:
  - **ODD:** a JSON object (purpose, time step, entities with state variables, processes, decisions, sensing, stocks).
  - **Bundle:** a JSON world bundle validated by `validate_bundle`.
  - **Mechanics:** a JSON causal model compiled by `CausalModel.from_dict`. Its process schema gains the optional `participants` field.
  - **Stock map, sensing map, outflow coverage:** Pydantic records, validated against the world's own fields and rule IDs.
  - **Extreme-conditions and anomaly reviews:** Pydantic verdicts, each requiring a verbatim log quote.
  - **Rule writer:** a JSON change list, compiled locally.
  - **Residents:** the Pydantic `Attempt`.
- **Prose never mutates state.**
- **Tracing:** every call goes through `llm_client` with its own trace ID under the `any-scenario-` prefix (one per step, review and run). The calls are stored in the project's `calls_<date>.jsonl` and summed by `spikes/any-scenario-2026-10/spend.py`.

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's key. Brian is the authorizer: he approved this spend on 2026-10-08 ("i approve. give me the new /goal text"), on the recommendation that named a $3 budget.
  - The cap is $3 for this plan, tracked by trace prefix and baselined at the plan's start.
  - Raising it needs Brian's yes.
- **Irreversible actions:** none. Deploys are non-goals.
- **Promotion condition:** nothing is promoted to the live World Builder until a separate plan, and only after L4 and L5 pass on real model runs with trace IDs reported. That later deploy falls under Brian's standing rule for his own sites (no private information; checks first), contained by the Builder's existing run caps.

## Uncertainties

Each of these is material: if it resolves badly, the approach fails or needs a different design.

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether linked writes fit the existing write-scope enforcement without a new commit path | Implementing agent | L2: a refusal test shows an out-of-scope linked write refused with identical before/after hashes |
| Whether the generator uses the new field when the scenario needs it | Implementing agent | L4 and L5 generated declarations contain process `participants` |
| Whether ownership, `entity_ref` and location links suffice for both scenarios | Implementing agent | L4 (ownership: the vehicle's owner is the driver) and L5 (a `ref:` or location link to the hospital and ventilators) |

## Prior art and parallel-implementation check

Existing ownership was searched in world-substrate (Decisions 004–007, the any-scenario plan and the replacement spikes). Internal lineage was searched in the World Substrate source (`action_authoring.py` action participants, `engine.py` scope enforcement), in `reference_worlds/waltzman` (multi-entity effects via actions only), and in Cybernetic Influence v3's intent/patch/commit boundary, already dispositioned in the lineage review. None has process-level linked participants. Process mechanics belong to world-substrate under Decision 006, and the claim check reported no active claims. External prior art was checked in Decision 007's landscape review and the 2026-10-05 replacement spikes. Each candidate gets one disposition: reuse, extend, compose, supersede, or bounded exception.

| Candidate | Disposition |
| --- | --- |
| World Substrate action mechanics' bound participants (`action_authoring.py`) | **reuse**: the same selector, derived-path and effect machinery, applied to process participants |
| Engine write-scope enforcement and atomic commit (`engine.py`) | **reuse**: unchanged authority; linked writes are just more declared paths |
| Petri-net transitions (one firing consumes and produces across several places) | **reuse** the semantics: one transition, several places, atomic |
| Mesa / NetLogo (`ask` linked agents in one step) | **bounded exception**: Python-level mutation with no declared write scope, so it cannot keep the Engine's authority (Decision 006) |
| Concordia game master (multi-entity narrated outcomes) | **bounded exception**: prose resolution; the spike showed no typed rule or commit primitive |

**Check for a silent parallel implementation.** A test fails if either of the following holds:

- any process effect is applied outside `Engine.advance`;
- the codebase gains a second process-participant mechanism. Concretely, `rg -n "participants" src/world_substrate/action_authoring.py` shows that process participants reuse `_selector` and `_derived_writes` instead of new parallel functions, and replaying a linked run's Engine events reproduces its final world.

## Activation facts

The machine record is `linked_process_participants/activation-facts.json`.

- **`llm_central`: true.** The generated worlds come from model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $3. Nothing is irreversible.
- **`shared_mechanism`: true.** The process declaration and Engine are used by every world.
- **`empirical_comparison_proposed`: false.** No comparison between alternatives. L1–L6 check the built result.

## Increments

1. Compiler and Engine support with unit tests (L1, L2, L3).
2. Generator schema and prompt mention the field; regenerate the truck world (L4).
3. Regenerate or repair the hospital world (L5).
4. Render and screenshot (L6); update the plan's Current State.

## Loop Bounds

- **No-progress stop:** three attempts on the same reproduced blocker without new evidence.
- **Finite bound:** at most 10 substantive increments.
- **Revalidation:** after three increments or about four hours.

## Non-Gating Next Actions

- Running the Waltzman bio-surveillance scenario through the pipeline.
- Distance-limited sensing.
- Wiring checks into the World Builder.

## Current State

- Demonstrated: none yet. Plan authored on 2026-10-08.
