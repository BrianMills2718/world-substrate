---
description: "Describe-any-scenario path: model up front, attempt over time, rules written mid-run."
---

# Decision 007: "Describe any scenario" path — model up front, attempt over time, rules written mid-run

Governs: RULE-FROZEN-PROFILE, spikes/any-scenario-2026-10

**Status:** accepted
**Date:** 2026-10-07
**Decided by:** Brian (approved option A in session, 2026-10-07: "i approve")
**Related:** [Decision 005](005-native-waltzman-delivery.md), [Decision 006](006-governed-rules-layer-scope.md), [issue #128](https://github.com/BrianMills2718/world-substrate/issues/128), Concordia and PDDL spikes in `spikes/replacement-2026-10/`

## Context

The goal is a demo for Rand Waltzman in which he describes any situation in plain words and watches it play out. The current path cannot reach "any" soon. Every outcome needs an approved rule written in advance, and a rule the authoring AI forgets (patients can die) silently never happens. Five weeks of native work produced one situation shape (Decision 005, `docs/contracts/native-coordination-authoring-v0.md`).

Brian raised two objections on 2026-10-07:

1. **"God doesn't tell you."** Today each actor is offered only actions whose checks already pass against true state. In the real world a driver with too little gas can start driving and then either runs dry or refuels on the way.
2. **Missing rules.** The game master should be able to write new rules mid-run, not just make one-off rulings. Up front there should be a formal modeling process, with established automatic checks, to account for everything.

Decision 006 already puts LLM residents on Concordia, with the Engine as sole consequence authority, and uses a PDDL export for validation and reachability. This decision extends it.

## Decision

Build toward the demo in three layers.

1. **Before the run: formal model, then checks.**
   - Use an established modeling method. Candidates: ODD protocol, stock-and-flow, PDDL for action rules, SysML v2 if mature enough.
   - The modeling step records what exists, how each thing enters and leaves, who decides what, and what each actor can sense.
   - Then run established check categories:
     - extreme conditions (zero ventilators must harm someone);
     - boundary adequacy;
     - units consistency (QUDT);
     - conservation;
     - deadlock;
     - liveness (every rule can fire);
     - reachability (existing PDDL/ENHSP path);
     - random-action testing.
   - The person approves the model in plain words.
2. **During the run: attempts, not a pre-checked menu.**
   - The pre-filtered menu is kept only for **permissibility**, the rules of the game, such as not voting twice.
   - **Feasibility** is attempted and resolved over time against then-current state (running out of gas partway). Actors learn the result only through their own observations.
   - Attempts are recorded in the observation-to-action vocabulary: belief (as of when) → decision → performed → expected vs observed.
3. **Rules written mid-run, then reviewed.**
   - When an attempt has no rule, the Concordia game master writes a general rule in the same rule language.
   - The rule runs through the layer-1 checks. If it passes, it is applied through the Engine and marked "written mid-run". If it fails, it falls back to a one-off ruling, also recorded through the Engine and flagged.
   - After the run, the person keeps or drops each new rule for future runs.

Every state change is structured data, so World Substrate's living-scene projection can animate it.

This reverses the deferral of "runtime invention or revision of laws" in `docs/research/cybernetic-influence-lineage-review.md`. It also amends Decision 006's pre-run human approval: rules written mid-run are applied after automatic checks and reviewed by a person after the run.

## First step

Run a one-to-two-day test on Concordia with two scenarios, a hospital ventilator shortage and a truck with low fuel. It passes when:

- the layer-1 checks catch a deliberately omitted "patients can die" rule;
- the truck can start driving and run dry partway;
- at least one uncovered attempt produces a game-master-written rule that passes the checks and is applied through the Engine;
- every change appears as structured data that one living-scene frame can render.

## Landscape check (2026-10-07)

No existing system does most of this. Every claim below was spot-checked against PyPI and GitHub.

What we adopt or borrow, layer by layer:

- **Base:** Concordia 2.4.0 (latest on PyPI) with the Engine, as in the spike. Connect the Engine and the checks through `InteractiveDocument` tool-use. Limit what each actor sees with `event_filter_fn`. Use `examples/concordia_island` (map, marketplace and fiscal game masters) as the starting template.
- **Layer 1:** [YuLan-OneSim](https://github.com/RUC-GSAI/YuLan-OneSim) for the modeling prompt chain: plain language, then an ODD description, then a behavior graph, then code. Apache-2.0. It has no formal checks.
- **Layer 1 checks:** unified-planning and ENHSP, which we already use, plus [Text2World](https://arxiv.org/abs/2502.13092)-style scoring for generated PDDL. For stock-and-flow models, the Code-First system dynamics model constraints (System Dynamics Conference 2026), and pint/QUDT for units.
- **Layer 3:** the repair loop from [WALL-E 2.0](https://arxiv.org/abs/2504.15785) and [Code World Models](https://arxiv.org/abs/2510.04542): predict, compare with what actually happened, write or repair the rule, then test it.

What nothing covers yet, and why we build it:

- **Rules written mid-run behind a check gate, with a fallback ruling and a human review afterwards.** Existing rule learning runs offline or between episodes, with no check gate.
- **Outcomes that play out over time, which actors learn only through what they observe.** Concordia and EpisodeSim resolve each action in the same step, in prose.
- **Standard system-dynamics confidence tests run automatically on an LLM-built model.** Published work checks only that the code runs. A [2026 study](https://arxiv.org/abs/2602.10140) found that "executability alone is insufficient", which is why layer 1's checks gate the run.

Dropped:

- Snow Globe, which is archived.
- Simudyne, which has no public trace of its lab and has not answered the 2026-09-30 access request.
- AgentTorch, which is AGPL-licensed.
- OASIS, TinyTroupe, Mesa-LLM and AI Town, each of which is single-purpose or has no world engine.

## Wrong when

- The game master's mid-run rules fail the layer-1 checks in most attempts on the two test scenarios, so the fallback rulings carry the run. Then the rule language is too narrow for runtime authoring.
- Two runs of the same scenario with the same seed produce game-master rules that contradict each other.
- An existing system covers layers 1–3 with structured state changes. Then adopt it, and keep only the parts it lacks.
- The extreme-conditions check fails to flag the omitted-death rule on the hospital scenario.

## Observed (2026-10-07, proof of concept)

Evidence: `docs/plans/any_scenario_poc.md` (Current State), PRs #131–#133, and `spikes/any-scenario-2026-10/evidence/`. The four conditions under "Wrong when":

- **Mid-run rules mostly failing: borderline.** On the final truck run, 2 of 3 game-master proposals failed conservation and became rulings. The third (a tow) passed and resolved. Three proposals is too few to judge.
- **Contradictory same-seed rules: not tested.** Only one game-master run was made under the final checks.
- **An existing system covering layers 1–3: not found** (landscape check above).
- **The extreme-conditions check failing to flag the omitted death rule: fired, then fixed.** The open AI review missed it in one run. The closed-question version (expected consequence, majority of 3) flagged it in two runs, and an outflow-coverage check also catches it deterministically.

Separately, the rule language limits what the path can model. A process changes only its own entity, and there is no randomness. These limits, not the attempt-over-time loop, were the main blockers to richer worlds.
