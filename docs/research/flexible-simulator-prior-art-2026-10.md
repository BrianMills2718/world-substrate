---
role: research
status: survey-complete-recommendation-proposed
reviewed_through: 2026-10-25
---

# Prior art for a flexible world simulator (2026-10)

> **Research, not a decision.** This survey answers one question Brian asked on 2026-10-24: are we inventing our own framework for a simulator where agents may *try anything*, the world decides what happens, and effects spread on their own? Accepted doctrine stays in [the decisions](../decisions/). The three detailed reports are in [flexible-simulator-prior-art-2026-10/](flexible-simulator-prior-art-2026-10/): [formal theory](flexible-simulator-prior-art-2026-10/formal.md), [games and interactive fiction](flexible-simulator-prior-art-2026-10/games.md), [LLM-agent platforms](flexible-simulator-prior-art-2026-10/llm-sims.md). Each one has a per-framework coverage table, its sources, and a list of claims it could not verify.

Clickable version: [the loop page](https://hive.brianmills.dev/plans/world-substrate/main/proposals/flexible-simulator/review-page/) (source `proposals/flexible-simulator/review-page/index.html`) traces each example through one attempt-to-commit loop.

## Bottom line

No single framework does the whole job, but almost every *part* has a well-developed standard. We should take those parts' names and rules and not invent our own. World Substrate's existing rule (agents state intents; only installed mechanics decide consequences; one atomic commit or refusal with recorded cause) is the same shape as the newest published work (Orchestrated Reality, [arXiv 2606.16014](https://arxiv.org/abs/2606.16014); IVIE, [arXiv 2606.13348](https://arxiv.org/abs/2606.13348)). So starting over is not needed. Three things are missing, and each has prior art to copy:

1. **The open attempt.** Today a resident picks an `action_id` from an offered list (`scripts/concordia_residents.py:32-35`, `:81`). An attempt instead needs to be free, with a fixed way to handle an attempt no installed mechanic matches. Copy: Inform 7's *check / carry out / report* rulebooks, where a refusal with a reason is a normal outcome, and tabletop adjudication (Blades in the Dark).
2. **Automatic knock-on effects** (ramifications). World Substrate already lets process rules react on the next time step (`Engine.advance`), each with recorded causes; what is missing is chaining within one step until nothing new fires. Copy: action-language causal laws (C+ / BC+ *static laws* and *dynamic laws*) and Event Calculus *trigger axioms*, run to a fixed point inside the same commit.
3. **Skill-shaped outcomes.** An untrained person may try to fly a helicopter and probably crashes. Copy: the Blades in the Dark action roll (the game master sets position and effect, and code rolls against the recorded rating) and GURPS skill *defaults* (untrained means a penalised roll, not a refusal).

## The ten test examples and what covers each

"Ours" means what World Substrate or Cybernetic Influence v3 already has, judged from documents and the cited code.

| Example | Best prior art | What to take | Ours today | Still no prior art |
| --- | --- | --- | --- | --- |
| Door: opens only when unlocked and handle pulled; a person triggers it | DEVS *external transition*; BFO *disposition realized by a trigger*; Inform 7 door kind; TADS 3 `preCond` | A door is a mechanism with an external transition only | Mechanic `checks` + refusal (WS); ADR-013 inert things | none |
| Chair: affords sitting, never acts, holds weight to a limit | BFO *disposition* / *function*; Sims *advertisements* (as a hint only) | Affordance is derived from agent × thing; never a gate | `Engine.discover(actor_id)` builds a derived affordance page per actor (`src/world_substrate/engine.py:351`) | none; corrected 2026-10-25, an earlier version of this row said we had no affordance view |
| Wall: a person tries to walk through and simply fails | C+ / Event Calculus inertia; Inform 7 check rule failing with a reason | The attempt is recorded and fails; nothing is blocked beforehand | Refusal recorded with cause (WS invariant) | Planners treat it as "not in the menu", which is the opposite |
| Voice across the world: only nearby listeners hear | Russell & Norvig sensors/actuators; DEVS port coupling; TADS 3 sense connectors (unverified) | Effects travel along channels with reach; intent is a field no rule reads | Information delivery semantics (`world_substrate.information`) | "Intent logged, never read by rules" is our own policy |
| Helicopter: untrained flight crashes; held facts are a hard gate; learning takes rounds | Blades in the Dark action roll and clocks; GURPS defaults; BFO *capability* (Beverley et al., [arXiv 2405.00183](https://arxiv.org/abs/2405.00183)) | Code rolls from a recorded skill; a hard gate (a phone number) is checked before any roll; a clock tracks learning | Information items as hard gate (WS) | Stochastic skill-gated outcomes for LLM deciders |
| Clock: acts on its own on a schedule | DEVS *internal transition*; PDDL+ *process* | Self-scheduled wake | Registered process rules that fire when `due(world)` on each time step (`ProcessRule`, `src/world_substrate/rules.py:333`); `ActiveSystemSpec` wake triggers (CI v3); SimPy selected for scheduling | none |
| Organisation: one agent or a boundary over members, chosen per run | DEVS closure under coupling; ADR-006 boundaries; Blades factions | A coupled model behaves as one model | ADR-006 (boundaries only) | Choosing the level per run and checking coarse vs fine agree |
| In-world AI / animal / computer: decider is LLM, fast model, or code | Russell & Norvig agent types; Levin *axis of persuadability*; Concordia pluggable acting component; GenAgents-1000 measured fidelity ([arXiv 2411.10109](https://arxiv.org/abs/2411.10109)) | One decider interface; fidelity is declared and, where possible, measured | `CognitionAdapter` (WS Decision 004); fidelity per authority (ADR-013) | A standard fidelity declaration |
| Thinking is an action aimed at oneself | Epistemic situation calculus (knowledge-producing actions) | Thinking changes only the thinker's state | not modelled | none needed beyond the convention |
| Pushing a glass off a table makes it fall and break | C+ / BC+ static laws; Event Calculus triggers; PDDL+ events; ECS observers (Flecs) | Ramification rules propose changes; the commit validates them all at once | Partly: process rules fire on the next time step when `due`, each as its own event with declared causal parents (`Engine.advance`, `src/world_substrate/engine.py:786`; e.g. `mechanisms/liquid.py`). Each process is checked once per step in a fixed order, not repeated until quiet, and not inside the attempt's own commit (`synthesis.md` notes there is no global causal closure) | An incremental fixed-point engine over our typed changes |

## What to adopt, ranked

1. **Ramification layer** from C+ / BC+ causal laws plus Event Calculus triggers. Run natively as rules that propose further changes after an attempt, repeated until nothing new fires, inside the same atomic commit so write scopes and recorded cause still apply. Use clingo (MIT, maintained) only as an offline cross-check, as the PDDL spike did. Acceptance tests come ready-made: World of Workflows ([arXiv 2601.22130](https://arxiv.org/abs/2601.22130), hidden cascading side effects) and SIMMER ([arXiv 2606.14574](https://arxiv.org/abs/2606.14574), latent failure classes).
2. **Inform 7 rule shape for every mechanic**: before / instead / check / carry out / after / report, plus `try` so a consequence re-enters the same pipeline. A failed check is a recorded refusal with a reason.
3. **Blades in the Dark adjudication contract for the LLM game master**: it sets position and effect, code rolls from the recorded rating, outcomes follow a fixed table, hard gates are checked first, and no roll happens without stakes (a wall needs none). Add GURPS defaults for untrained attempts. Make the exploit IVIE reports, where players got past puzzles by claiming they had solved them, a named regression test.
4. **Vocabulary, zero code**: DEVS (external, internal and confluent transitions, ports, coupling) for agent versus mechanism and for organisations; BFO (disposition, function, role, capability, realization) for the door, chair and helicopter; PDDL+ (action, event, process) for kinds of mechanic.
5. **Fallback for unmatched attempts**: classify as (a) fails by an existing world rule (wall), or (b) unmodelled, so the game master decides with fidelity marked "coarse" and the case is flagged so a mechanic can be written later. No surveyed system has this except tabletop play; text-adventure parsers just print "I don't understand".
6. **Metadata cards**: ODD 2020 for each world's description, plus a fidelity field per decider using Levin's persuadability rungs and, where a baseline exists, the GenAgents-1000 measured-fidelity pattern.

Do not adopt as runtimes: Inform 7, TADS, Dwarf Fortress, Caves of Qud (closed or parser-bound); an ECS engine (none has validated atomic commit); OASIS or AgentSociety (closed action menus); Jericho (GPL-2.0, Z-machine only); CCalc or the DEC reasoner (batch tools, barely maintained). Concordia stays the host for the loop and minds (Decision 006). Its `interrupt_*` scheduling is on Concordia `main` only, not in release 2.4.0, which this repository pins.

## Fit with Decision 006

[Decision 006](../decisions/006-governed-rules-layer-scope.md) limits World Substrate to the governed-rules layer and forbids adding an engine, scheduler, renderer or cognition of our own. All three missing pieces sit inside the rules layer (what an attempt does, what follows from it, how skill shapes it), so none conflicts with it. Scheduling stays with SimPy or Concordia, and minds stay with Concordia.

## What earlier work covered, and what it missed

Brian recalled an earlier survey that was never written up. The record shows several partial ones, none asked this question:

- **Concordia versus Cybernetic Influence** (July 2026): `cybernetic_influence_v3/docs/plans/026-concordia-foundation-research.md`, which led to ADR-013. It compared Concordia only.
- **Dwarf Fortress-style substrates** (Deep Research, 2026-08-31): `castaway-world/docs/research/deep-research-report-dwarf-fortress.md`, sha256 `f1cdd031…`, matching `references/sources.json:56`; that file's recorded path, a castaway-world worktree, no longer exists. It ranks game environments (fort-gym, DFHack, Melting Pot, NetHack Learning Environment, Neural MMO, Craftium, Mesa, Agents.jl) by mechanical depth and ML interface. Every one of them binds the agent to a fixed action vocabulary. It did not cover formalisms for attempts, affordances or ramifications.
- **Competitive landscape** (2026-09-08, addendum 2026-10-04): [competitive-landscape-2026-09.md](competitive-landscape-2026-09.md). It positions Concordia, AgentSociety, OASIS, SOTOPIA, PettingZoo and Melting Pot. The addendum names Inform 7, MUDs, PDDL, GGP-GDL, NetLogo, Mesa, SimPy and ECS in one line each, without verdicts.
- **Replacement-first reviews**: `cybernetic_influence_v3/docs/research/030-replacement-first-simulation-platform-review-2026-09-30.md` (Simudyne, Concordia, GAMA, AnyLogic, docs only), and `spikes/replacement-2026-10/` (Concordia, Mesa and PDDL executed on one scripted world; each "composes", none replaces the rules layer).

Never examined before this survey: DEVS, event calculus or action languages, the frame and ramification problems, BFO, Sims smart objects, tabletop adjudication, and the 2025-26 LLM-plus-validator papers.

## Limits

The detailed reports mark what was read from primary sources and what came from search snippets or background knowledge. The Zeigler, Reiter, Mueller and AIMA books, ISO 21838-2, the Forbus and Wright Sims paper body, the Dark Engine stimulus/response details and the TADS 3 sense chapter were not read; claims resting on them are marked unverified there. All eight arXiv identifiers cited above were checked against the arXiv API on 2026-10-25 and match their titles. Nothing here was run against World Substrate code. Coverage of "ours" comes from documents plus the two cited code lines.
