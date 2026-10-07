# Goal: describe-any-scenario proof of concept (Decision 007)

## Goal

**Mission:** Prove the [Decision 007](../decisions/007-any-scenario-path.md) path end to end. A plain-language scenario becomes a checked model. The scenario runs with LLM residents on Concordia, and the World Substrate Engine stays the sole consequence authority. Attempts play out over time. When a resident attempts something no rule covers, the game master writes a rule mid-run and the checks decide whether it is applied. Every change is structured data that the living scene can draw. This settles whether a "describe any scenario" demo for Rand Waltzman is weeks or months away.

**Execution profile:** `continuous-light`. One writer, reversible proof of concept, one repository.

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
| C6 | Tests touching the change pass | pytest output with passed/failed counts and exit code |

For every LLM behavior claim (C1, C3, C4), inspect the full trace directly and report the trace IDs.

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
