---
plan_id: "any-scenario-poc"
dependencies: []
dependencies_reviewed: "2026-10-07"
planning_path: durable_solo
planning_path_ref: docs/plans/any_scenario_poc/path-decision.json
method_conformance_receipt: docs/plans/any_scenario_poc/conformance-receipt.json
goal:
  outcome: "Prove the Decision 007 describe-any-scenario path end to end in world-substrate: plain-language scenario -> checked model -> LLM residents on Concordia with the World Substrate Engine as sole consequence authority -> attempts resolved over time -> game master writes checked rules mid-run -> structured changes rendered as living-scene frames."
  canonical_example: "Typing 'A delivery driver with a quarter tank must reach a town 120 miles away; there is one gas station at mile 60' yields a run where the LLM driver skips the station, the Engine commits 'out of fuel' partway, the driver's next decision cites the observation 'engine stopped', and a rendered frame shows the stopped truck; and the hospital ventilator scenario with 'patients can die' removed is flagged by the extreme-conditions check."
  forbidden_substitutes: "hand-written rules or models presented as generated; a game master that narrates without calling Engine.submit; scripted residents in the attempt-over-time claim; checks run on a model that never ran; narrative logs in place of structured state changes; mock-ups in place of frames rendered from run data."
  boundaries: "world-substrate only, sole writer, PRs merged after local checks; Concordia, YuLan-OneSim, cybernetic_influence_v3 and observation-to-action-metamodel read-only; no deploy, no change to live /waltzman/ or World Builder, no outreach; model spend capped at $5 via llm_client max_budget, and raising it needs Brian's yes."
  done_when: "Acceptance checks C1-C6 in docs/plans/any_scenario_poc.md pass, each judged from the full trace of its named run (llm_client trace IDs, Engine event lists, check logs, rendered frame plus screenshot, pytest counts and exit code), and the parallel-implementation test passes; report the trace IDs and evidence for each."
  do_not_gate_on: "Brian's review of the result; the decision to build the Waltzman demo on this path; the Waltzman outreach email; Simudyne's reply."
  stop_after: 3
---
# Plan: describe-any-scenario proof of concept (Decision 007)

## Goal

**Mission:** Prove the [Decision 007](../decisions/007-any-scenario-path.md) path end to end. A plain-language scenario becomes a checked model. The scenario runs with LLM residents on Concordia, and the World Substrate Engine stays the sole consequence authority. Attempts play out over time. When a resident attempts something no rule covers, the game master writes a rule mid-run and the checks decide whether it is applied. Every change is structured data that the living scene can draw. This settles whether a "describe any scenario" demo for Rand Waltzman is weeks or months away.

**Execution profile:** `continuous-light`

One writer, reversible proof of concept, one repository.

**Stage and investment boundary:** proof of concept, about one to two days of agent work. Model calls go through the shared `llm_client` on the OpenRouter route and are traced.

**Canonical examples:**

1. **Hospital.** Input: "A 40-bed hospital with 6 ventilators faces a flu surge; staff decide who gets ventilated and whether to order more."
   - Phase A, a deliberate omission. The modeling step's output is edited to remove the "patients can die" rule. The extreme-conditions check (ventilators = 0) must then report that no patient is harmed and flag the model as missing a rule.
   - Phase B, the full run. The run completes with every state change recorded as structured data.
2. **Truck.** Input: "A delivery driver with a quarter tank must reach a town 120 miles away; there is one gas station at mile 60."
   - In one run the driver starts without refueling and runs dry partway.
   - The driver learns this only through an observation, such as the engine stopping, not from a refused menu option.
   - In a run where the driver stops at mile 60, the driver arrives.
3. **Mid-run rule.** In either scenario, at least one resident attempt not covered by any rule makes the game master write a general rule in the World Substrate rule language. The rule passes the checks, is applied through `Engine.submit`, and is marked "written mid-run". A second, deliberately invalid generated rule (for example, one that creates fuel from nothing) fails the conservation check and falls back to a recorded one-off ruling.

**Forbidden substitutes:**

- hand-written rules or models presented as generated;
- a game master that narrates outcomes without calling the Engine;
- a scripted resident standing in for an LLM resident in the attempt-over-time claim;
- checks shown passing on a model that never ran;
- a narrative log in place of structured state changes;
- a mock-up in place of a living-scene frame rendered from run data.

**Repository / working scope:**

- Work happens in `~/code/world-substrate` on a claimed branch or worktree, under its `AGENTS.md`.
- New code goes under `spikes/any-scenario-2026-10/`.
- Engine changes are only those needed for attempt-over-time resolution, each covered by tests.

## Boundaries

- **In scope:** Concordia 2.4.0 (pinned) game master and residents; the Engine as consequence authority; a modeling step that borrows YuLan-OneSim's ODD-first prompt chain; the checks (extreme conditions, conservation, units via pint, deadlock and liveness, reachability via the existing unified-planning/ENHSP path); attempts recorded as belief → decision → performed → expected vs observed; one living-scene frame per scenario.
- **Out of scope:** public deployment; changing the live `/waltzman/` or World Builder sites; UI polish; scenarios beyond the two named; sending anything to Waltzman.
- **Writes allowed:** world-substrate branch work, merged through pull requests after local checks pass.
- **Read-only:** Concordia and YuLan-OneSim upstream; `cybernetic_influence_v3`; `observation-to-action-metamodel` (vocabulary reused, not edited).
- **Irreversible actions:** none expected. Deploys and outreach are out of scope.

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| C1 | The modeling step turns the hospital text into a structured model without hand edits | The model file plus the trace ID of the LLM call that produced it |
| C2 | The extreme-conditions check flags the model with "patients can die" removed, and passes the full model | Check output with counts and exit status for both models |
| C3 | The truck runs dry partway in one run, the resident learns it only by observation, and the refuel run arrives | Structured event list for both runs, with tick numbers and the resident's observation records |
| C4 | A game-master-written rule passes the checks and is applied through `Engine.submit`; an invalid one fails conservation and falls back to a recorded ruling | Rule text, check output, and the Engine event IDs carrying the "written mid-run" or "ruling" flag |
| C5 | Each scenario's run renders one living-scene frame from its recorded data | Rendered file path plus a screenshot taken through `agent-browser` or `npx playwright screenshot` |
| C6 | The local verbose pytest run (`pytest -v` over the touched tests) | Terminal output saved to the run folder | Every test named in the trace is listed: the Engine attempt-over-time tests, the parallel-implementation test, and the existing Engine and Concordia-spike tests. None is skipped or deselected, and the totals line matches those names, along with the exit code. |

For every LLM behavior claim (C1, C3, C4), inspect the full trace directly and report the trace IDs.

## Actor, result and authority

- **Actor:** Brian, deciding whether to build the Waltzman demo on this path. Rand Waltzman is the eventual viewer, but he is not part of this plan.
- **Result:** the canonical examples above run end to end from plain-language input. Brian can look at one rendered living-scene frame per scenario and the list of rules written mid-run.
- **Concrete example of the result:**
  - Brian types "A delivery driver with a quarter tank must reach a town 120 miles away; there is one gas station at mile 60."
  - In the run, the LLM-driven driver decides to skip the station.
  - The Engine lowers the fuel each tick and commits an "out of fuel" event about two-thirds of the way along.
  - The driver's next decision quotes the observation "engine stopped" and chooses to walk back for fuel.
  - The rendered living-scene frame shows the truck stopped on the road, its fuel bar empty, and that event highlighted.
  - In the second run, where the driver stops at mile 60, the frame shows the truck in town.
- **Authority:** Brian approved the path and this test on 2026-10-07 ("i approve"), which is recorded in Decision 007. The implementing agent is the sole writer in world-substrate. Concordia, YuLan-OneSim, `cybernetic_influence_v3` and `observation-to-action-metamodel` are read-only.
- **Non-goals:** a public deployment; any change to the live `/waltzman/` or World Builder sites; UI polish; scenarios beyond the two named; general rule-language expressiveness; contact with Waltzman; any benchmark or comparison between candidate platforms.

## Success and disproof

- **Success:** all of the following are shown, with the run traces named in the next section:
  - (C1) the hospital text becomes a typed model by a traced model call, with no hand edits;
  - (C2) the extreme-conditions check (ventilators = 0) flags the model with "patients can die" removed, and passes the full model;
  - (C3) the truck runs dry partway as a committed Engine event, the resident learns it only through an observation, and the refuel run arrives;
  - (C4) one game-master-written rule passes the checks and is committed through `Engine.submit` marked "written mid-run", and one invalid rule fails the conservation check and becomes a recorded ruling;
  - (C5) one living-scene frame per scenario is rendered from recorded Engine events and screenshotted;
  - (C6) the touched tests pass, reported with counts and exit code.
- **Disproof:** Decision 007's "wrong when" conditions, evaluated on these two scenarios. The approach is disproved if any of the following happens:
  - most generated mid-run rules fail the checks, so fallback rulings carry the run;
  - same-seed runs produce contradictory generated rules;
  - the extreme-conditions check fails to flag the omitted death rule.

## Trace review per criterion

Each criterion is judged from a full run trace, not only from its outcome. Run folders are packed into `artifacts.sqlite` with `run-artifacts pack` when the run ends.

| ID | Run whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| C1 | The hospital modeling run | `llm_client` observability (`calls_<date>.jsonl`, by trace ID) plus the run folder | The prompt received the user's text unedited. Each ODD section in the model traces back to a model-call output, not to a hand edit. |
| C2 | Check runs on the full and the omitted models | The run folder's check log | The extreme-conditions case was actually simulated (ventilators = 0, with steps listed), and the flag names the missing harm path. |
| C3 | Both truck runs | The Engine event list plus Concordia structured log and resident observation records | Fuel decreases tick by tick. The "out of fuel" event is committed by the Engine mid-route. The resident's next decision cites an observation, not a refusal. |
| C4 | The run containing the uncovered attempt | The game-master model-call trace, the check log and the Engine events | The uncovered attempt, the generated rule text, each check's verdict, then a commit or a fallback ruling, in that order. |
| C5 | The rendering of each run | Rendered HTML plus a screenshot | Frame content matches committed Engine events by entity and event ID. |
| C6 | The local pytest run | Terminal output | Passed, failed and skipped counts, and the exit code. |

## Model calls

- **Call graph:**
  1. The modeling call takes the scenario text and returns a typed model (a Pydantic ODD-plus-stock-and-flow record).
  2. Resident calls, one per resident per decision point. Each takes the observations delivered to that resident and returns a typed attempt (belief, decision, expected effect).
  3. The game-master rule call takes the uncovered attempt and the current rule set, and returns a typed rule in the World Substrate rule language or an explicit "ruling only".
- **Result boundaries:** every call returns a structured result that is validated client-side. Prose never mutates state, and only the Engine commits.
- **Tracing:** all calls go through the shared `llm_client` with a trace ID per run.

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's configured key, authorized by his 2026-10-07 approval of this test.
  - The cap is $5 for the whole plan, enforced through `llm_client`'s `max_budget`.
  - Each run's observed cost is logged.
  - Exceeding the cap stops the run visibly. Raising it needs Brian's yes.
- **Irreversible actions:** none. Deploy, publication and outreach are non-goals.
- **Promotion condition:** this plan promotes nothing; a public demo is a non-goal. Promotion happens only through a separate later plan, and only after one full authentic hospital run passes C1–C5 on a real model, with its trace IDs reported. That later deploy falls under Brian's standing rule for his own sites: no private information, checks run first, then deploy. It is contained by the same per-visitor and daily run caps and the monthly spend stop the live `/waltzman/` backend already uses (`personal-vps/apps/waltzman/README.md`).

## Uncertainties

Each of these is material: if it resolves badly, this approach fails or needs a different design.

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether Concordia 2.4.0's tool use can route every resident attempt through `Engine.submit` | Implementing agent | The C3 truck-run trace. Every resident attempt appears as a Concordia tool call followed by an Engine event ID, with no state change lacking one. |
| Whether a small model can write rules in the World Substrate rule language that pass the checks | Implementing agent | The C4 check log: generated rules counted by pass and fail. Disproved if most fail. |
| Whether the extreme-conditions check can be automated generically, or only per scenario | Implementing agent | The C2 check log for the hospital run. The check runs from the model's declared stocks without hand-written per-scenario code. A second scenario is a later step. |
| Whether the Engine needs a duration or attempt primitive, or whether Concordia's async engine can hold in-flight attempts | Implementing agent | Increment 1's truck run: the trace either shows Concordia's async engine holding the drive across ticks while the Engine commits each fuel decrement, or shows that this fails and an Engine attempt record (with a test) was required. |

## Prior art and parallel-implementation check

Existing ownership was searched in world-substrate's decisions 004–006, the roadmap and the `spikes/replacement-2026-10/` results. The work belongs to world-substrate under Decision 006, and no other repository or active claim owns attempt-over-time or runtime rule writing (the claim check reported no active claims on 2026-10-07). Internal lineage was searched in cybernetic_influence_v3, observation-to-action-metamodel and scientific-hypergraph. External prior art comes from the 2026-10-07 landscape check, recorded in [Decision 007](../decisions/007-any-scenario-path.md#landscape-check-2026-10-07). Each candidate gets exactly one disposition: reuse, extend, compose, supersede, or bounded exception.

| Candidate | Disposition |
| --- | --- |
| Concordia 2.4.0 (game master, residents, `InteractiveDocument` tool use, `event_filter_fn`, `examples/concordia_island`) | **compose**: the runtime, with the Engine as consequence authority (as in `spikes/replacement-2026-10/concordia/`) |
| World Substrate Engine (`Engine.discover` / `Engine.submit`) | **extend**: the only commit path; attempt-over-time resolution is added here |
| Waltzman `ActivityState` (`reference_worlds/waltzman/components.py`), the only existing duration-bearing activity | **extend**: the new attempt primitive generalizes it, and Waltzman's meeting becomes one instance; it never runs as a second primitive alongside it |
| SimPy (selected in Decision 004 for scheduling wakeups only) | **compose** if the Engine needs scheduled wakeups; wakeups only create opportunities, and the Engine still commits |
| unified-planning + ENHSP PDDL path (`spikes/replacement-2026-10/pddl/`) | **reuse**: reachability and rule-precondition checks |
| YuLan-OneSim ODD-first prompt chain | **reuse**: modeling-step prompts (Apache-2.0) |
| WALL-E 2.0 / Code World Models repair loop | **reuse** the method (predict, compare, write or repair, test) for game-master rule writing |
| Text2World scoring | **reuse**: metric for generated PDDL rules |
| pint / QUDT | **reuse**: units check |
| `cybernetic_influence_v3` capability / attempt / adjudication / realized-outcome split (ADR-013) | **reuse** the distinction; no code import |
| observation-to-action vocabulary (`actDecision`, `actPerformed`, `beliefAsOf`, `effExpected`, `effObserved`) | **reuse** as the field names on attempt records |
| scientific-hypergraph | **bounded exception**, not used: it describes model structure, not a runtime; revisit only to persist models |
| Snow Globe, WarAgent, AgentTorch, OASIS, TinyTroupe, Mesa-LLM, AI Town, Simudyne | **bounded exception**: not adopted. Snow Globe is archived; WarAgent covers fixed scenarios only; AgentTorch is AGPL; OASIS, TinyTroupe, Mesa-LLM and AI Town have no world engine or are single-purpose; Simudyne has given no access. Revisit only if one ships typed rules with an atomic commit. |

**Check for a silent parallel implementation.** A test in the spike suite fails if either of the following holds:

- `rg -n "class .*(Activity|Attempt)State" src reference_worlds spikes` finds more than one duration or attempt primitive. The new one must replace or wrap Waltzman's `ActivityState`.
- Any state change in a C3 or C4 run lacks a matching Engine event ID. That would show a second mutation path, such as Concordia's own `WorldState` or `Inventory`, changing state outside `Engine.submit`.

## Activation facts

These facts decide which planning checks apply. The machine record is `any_scenario_poc/activation-facts.json`.

- **`llm_central`: true.** The modeling step, resident decisions and game-master rule writing are all model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $5. Nothing is irreversible.
- **`shared_mechanism`: true.** Attempt-over-time resolution may add a duration or attempt primitive to the Engine, which every world uses. That change is a shared mechanism and gets the shared-mechanism checks.
- **`empirical_comparison_proposed`: false.** No benchmark or comparison between alternatives. C1–C6 check the built result against expected outcomes, which is verification, not a comparison.

## Increments

1. **Truck vertical (C3).** Concordia LLM resident, Engine, an attempt that plays out over time, and observation-only learning. This retires the attempt-vs-outcome uncertainty first.
2. **Hospital modeling and checks (C1, C2).** Text to model, then the extreme-conditions check catching the omitted death rule.
3. **Mid-run rule writing (C4)** on whichever scenario first produces an uncovered attempt.
4. **Structured changes to the living scene (C5)** for both scenarios.

## Loop Bounds

- **No-progress stop:** three attempts on the same reproduced blocker without new evidence or a safe next action.
- **Finite bound:** at most 12 substantive increments, counting fixes, under this goal.
- **Strategy revalidation:** after three increments, about four hours, or four days elapsed. Report outcome, enabling and process progress, and recommend retain, replace or clear. If Decision 007's "wrong when" fires, stop and report it rather than working around it.
- **Exact blocked resume event:** the named blocker is cleared, such as a credential being stored or an upstream release.

## Non-Gating Next Actions

- Brian reviews the result as a working UI slice.
- Deciding whether to build the Waltzman demo on this path.
- Whether to send the Waltzman outreach email.
- Simudyne's reply, if it ever comes.

## Current State

- Demonstrated: none yet. The goal was authored on 2026-10-07.
