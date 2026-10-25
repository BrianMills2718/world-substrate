# LLM-agent simulation platforms 2023-2026: prior-art survey (scope: llm-sims)

Date of survey: 2026-10-24. "Verified" = read in this session from the cited primary page or from the local checkout. "Unverified" = recalled from background knowledge or seen only in a search snippet.
Local evidence: `~/code2/concordia` (gdm-concordia 2.4.0 per `setup.py` and `CHANGELOG.md` dated 2026-03-06; HEAD commit 2026-10-20, so the checkout is current).

## 0. What we already have (so this survey adds only the delta)

- **ADR-013** (cybernetic_influence_v3, accepted 2026-07-31, boundary clarification 2026-08-11): Concordia owns the outer lifecycle. A project-owned canonical world lives in game-master components. The standard path is: canonical truth -> actor-authorized observation -> open semantic intent -> declared *transition authority* (deterministic, stochastic, LLM, external, scripted or replayed) -> structured patch proposal -> generic reference/authority/topology/invariant checks -> atomic commit or visible rejection -> observation + evidence. Inert things (truck, computer, record) are world records with affordances and get no `act` lifecycle. Only autonomous processes are entities. Capability / permission / attempt / adjudication / outcome are distinguished "where the question requires".
- **ADR-006:** an organisation is a derived, reversible coarse-graining (boundary) over member entities. It never acts, and boundary I/O is derived from routed effects. ADR-013 also allows a coarse organisational surrogate as an active entity, but not at the same time as the detailed members for the same causal function.
- **ADR-017 (2026-09-30):** replacement-first gate. Simudyne, then Concordia, then GAMA/AnyLogic. Nothing new is built where a mature platform fits.
- **`active_runtime/models.py`:** `ActiveSystemSpec` has observation ports, activation ports (declared wake triggers), output ports (required outputs), `output_port_unavailable_when` (technical availability, explicitly not permission), `initial_next_update_at`, and private state with byte caps. Source: `~/code2/cybernetic_influence_v3/src/cybernetic_influence/active_runtime/models.py` (the BRIEF path omits `src/cybernetic_influence/`).
- **world-substrate** (AGENTS.md invariants; Decision 006 governed-rules layer only): policies never mutate state; mechanics propose; one enclosing transition validates and commits or refuses; write scopes enforced, read scopes recorded only; "Linguistic Core supplies senses/roles, mechanics supply effects".
- **Spike 2026-10 (`spikes/replacement-2026-10/concordia/README.md`):** Concordia 2.4.0 *composes* with the Engine and cannot hold the governed-rules layer. Concordia has no typed rule/check/authority/atomic-commit primitive, so the replace variant had 51 lines of our code and zero Concordia contribution. Friction: every component needs `get_state`/`set_state`, values are strings, and a missing key makes `SwitchAct` silently fall back to the LLM. LLM residents were not exercised. Mesa and PDDL spikes are siblings.
- **competitive-landscape-2026-09.md** already covered: Concordia, AgentSociety 2, OASIS, SOTOPIA, Generative Agents, PettingZoo, Melting Pot. Its 2026-10-04 addendum named: Dreamer/Genie/JEPA, Tsividis theory-based RL, DreamCoder, Voyager (one line), GGP-GDL, PDDL, NetLogo/Mesa/SimPy, ECS, Inform 7 and MUDs, and Pearl SCMs.
- **technology-procurement:** the Jev "System One" hybrid cognition adapter is already recorded as a *deferred provider pattern*. **jev-world-modeling-exploration-2026-09.md** already has four uses of a fast typed model (estimator, stochastic kernel, latent property, candidate ranker) with an analytic / evidentiary / causal latent discipline.
- **Not yet covered by earlier surveys (new here):** AI Town, GenAgents-1000, Project Sid/PIANO, MineDojo, TextWorld/ALFWorld/Jericho in detail, the "LLM as text world simulator" literature (Wang et al. 2024), code-world-model papers (WorldCoder, GIF-MCTS, CWM-GGP, OneLife), 2026 hybrids (Orchestrated Reality, PAYADOR/IVIE, World of Workflows, SIMMER, Hybrid-WM), and the Concordia v2 entity/GM/engine details.

## 1. Cross-cutting finding

Every LLM-agent platform in scope answers "who decides the effect of a free-form action?" in one of four ways:
(a) the LLM game master decides in prose (Concordia `EventResolution`, Smallville, AI Town; unverified for the last two);
(b) a fixed platform with a closed action menu decides (OASIS, AgentSociety environment modules);
(c) a real game engine decides because agents emit *code* against its API (Voyager/Mineflayer, Project Sid; this is the only existing way to have unbounded attempts adjudicated by a world); or
(d) an LLM *proposes* a structured delta and a validator commits it (Orchestrated Reality 2026, PAYADOR/IVIE 2026, our ADR-013).
Nothing found combines open-ended attempts with a *rules engine that propagates effects*. The nearest are World of Workflows (4,000 ServiceNow business rules propagating, but as a benchmark of prediction, not a framework) and SIMMER (a state machine over 77 actions / 262 objects, again a benchmark). That gap is exactly where ADR-013 and world-substrate sit, so there is no framework to adopt wholesale for examples 3, 4, 5, 10. There are vocabulary and code to borrow (below).

## 2. Frameworks

Coverage legend: covers / partly / no. Example numbers are from the BRIEF.

### 2.1 Google DeepMind Concordia (v2.4.0, Apache-2.0, Python)
**What it is.** A library for generative social simulation. Entities are built from components, and a Game Master (GM) is itself an entity that turns natural-language putative actions into outcomes. Sources: https://github.com/google-deepmind/concordia ; original paper https://arxiv.org/abs/2312.03664 ; v2 tech report "Multi-Actor Generative AI as a Game Engine" https://arxiv.org/abs/2507.08892 ; v2.0 announcement https://www.cooperativeai.com/post/google-deepmind-releases-concordia-library-v2-0 (GMs are entities, clocks optional, prefabs replace factories, an engine structures actor/GM interaction, serialization and checkpointing added).

Verified in the local 2.4.0 code:
- `concordia/typing/entity.py`: one `Entity` interface. Player output types are FREE/CHOICE/FLOAT. GM output types are MAKE_OBSERVATION, NEXT_ACTING, NEXT_ACTION_SPEC, RESOLVE, TERMINATE, NEXT_GAME_MASTER, SKIP_THIS_STEP. The engine assigns player vs GM roles per `run_loop` call (README: "roles in that call, rather than intrinsic entity classes").
- Engines: `sequential`, `simultaneous`, `asynchronous`.
- GM components (`concordia/components/game_master/`): `event_resolution` (LLM judge with thought chains), `inventory` (tracked in code but changes are LLM-judged), `payoff_matrix`, `world_state`, `scene_tracker`, `next_acting`, `switch_act`, `terminate`, and the *interrupt family* (`interrupt_scheduling`, `interrupt_time_model`, `interrupt_resolution`, `interrupt_next_acting`, `interrupt_make_observation`).
- **Correction (checked 2026-10-25):** the `interrupt_*` family is on Concordia's `main` branch only; it is not in any release (latest `v2.4.0`, 2026-03-06, the version this repository pins, ships `event_resolution`, `next_acting`, `switch_act`, `world_state` and others but no `interrupt_*` file). Adopting it means pinning a main-branch commit or waiting for a release.
- `interrupt_scheduling.py`: a deterministic totally ordered event queue (`Event(timestamp, tag, source, description)`), per-entity `InterruptMask` (tag-prefix filters), and per-entity non-maskable private `Timer` events (`timer.expired.<entity>`). An entity can sleep until a timer or a matching event wakes it.
- v2 paper (verified from the HTML): the GM "can be constrained to stay very close to established, and hard-coded, guardrails"; flexible resolution "can undermine physical consistency for Simulationist goals". Designers are told to pick one primary goal (Evaluationist / Dramatist / Simulationist).

| # | Example | Verdict | Why |
|---|---|---|---|
| 1 | Door | partly | No ability/precondition primitive. We would write a GM component. `EventResolution` asks an LLM whether the door opens. |
| 2 | Chair | no | No affordance or load model. Inert objects are only prose or `inventory` counts. (ADR-013 keeps them as world records.) |
| 3 | Wall | partly | Attempt is free text, so the attempt is never blocked, but the failure comes from LLM plausibility judgment, not a solid rule. |
| 4 | Voice | partly | `make_observation` and the `InterruptMask` tags route who is told. Reach is decided by GM code or LLM. Intent vs effect separation is possible but not enforced. |
| 5 | Helicopter | no | No skill record or hard fact gate. Outcome depends on the LLM judge. |
| 6 | Clock | covers (for scheduling) | `Timer` plus ordered event queue is a deterministic internal wake. A clock acting on world state still needs custom code. |
| 7 | Org granularity | partly | An org can be an entity or a GM component. There is no boundary-over-members concept (ours: ADR-006). |
| 8 | Deciders | partly | Any entity can have a scripted/puppet/LLM acting component (`scripted_act`, `puppet_act`, `human_act_component`). No declared fidelity field. A fast typed model fits as an acting component. |
| 9 | Thinking = self-action | partly | `plan`, `question_of_recent_memories`, and the "thought chains" step are internal component calls, not world actions with a target. |
| 10 | Ramifications | no | The LLM GM writes one event. Nothing propagates. Our spike confirms there is no typed rule or atomic commit. |

**ADOPT.** (1) The entity-component split and "GM is an entity", already adopted by ADR-013. (2) The `interrupt_*` scheduling design as the model for examples 6 and 8: deterministic ordered queue, tag masks for what wakes whom, private timers. It is stock code, so use it rather than SimPy-plus-glue where Concordia hosts the loop (reconcile with technology-procurement, which selected SimPy for scheduling only; unverified whether the two are compatible). (3) Vocabulary: *putative event*, *prefab*, *engine roles per call*. (4) Checkpoint/serialization hooks.
**GAP.** No typed transition, no commit/refusal, no skill or gate, no propagation, no affordance model, string-typed values, and a silent LLM fallback in `SwitchAct`. This is all already known from the spike (verdict "compose").
**Maturity.** Maintained (HEAD 2026-10-20), Apache-2.0, Python, 34-package install.

### 2.2 Stanford Generative Agents / Smallville
**What it is.** 25 agents with a memory stream, reflection and planning in a Sims-like sandbox. Primary: https://arxiv.org/abs/2304.03442 (abstract verified); code https://github.com/joonspk-research/generative_agents (Apache-2.0, Python, Django environment server; verified. Activity status not shown on the page: 31 commits, last-activity date not visible).
Mechanism (unverified in this session, from background knowledge of the paper): the LLM turns each agent's action into a short description plus an emoji, and then updates the state string of the affected object (e.g. "coffee machine: brewing"). The world adjudicates nothing; there are no rules.

| # | Verdict | Why |
|---|---|---|
| 1,2,3 | no | Objects have a state string set by LLM. No preconditions, solidity from a tile collision map only (unverified). |
| 4 | partly | Perception radius is a hard spatial rule; speech goes to nearby agents (unverified detail). |
| 5 | no | No skills. |
| 6 | no | Schedules are agent plans, not world clocks. |
| 7 | no | |
| 8 | no | LLM only. |
| 9 | partly | Reflection is an internal act that writes memory. |
| 10 | no | |

**ADOPT.** Memory stream, reflection, and planning as the cognition pattern, already available inside Concordia. The tile/perception-radius idea as a hard rule for example 4.
**GAP.** Everything about world adjudication.
**Maturity.** Research artifact. Superseded in practice by Concordia and AI Town.

### 2.3 GenAgents / "1000 people" (Park et al. 2024)
**What it is.** Agents built from two-hour interviews of 1,052 people. They predict held-out survey and experiment responses at 83% (interview), 82% (survey), 86% (combined) of a participant's own test-retest consistency, versus 74% for demographics-only. Primary: https://arxiv.org/abs/2411.10109 (verified; the "85%" figure often quoted is not in the abstract).
Relevance: this is a *fidelity-calibration* method for a person-agent, not a world engine. It matters for example 8 ("each declares its fidelity"): it is the model of a measured fidelity statement ("X% of test-retest").
**Coverage.** no on all ten, except 8 partly (an identity-grounded LLM decider with a *measured* fidelity).
**ADOPT.** The reporting pattern: a decider's declared fidelity should be a measured number against a stated benchmark, not an adjective. Compatible with ADR-013's "no predictive claim without calibration".
**GAP.** Not a simulator. Whether the released agent bank is available is unverified (access-controlled, per recollection).
**Maturity.** Paper plus restricted data (unverified).

### 2.4 AgentSociety (Tsinghua FIB lab) and AgentSociety 2
**What it is.** Large-scale LLM-agent social simulator. The ACL 2025 industry paper reports 10k+ agents and about 5M interactions (search snippet, https://preview.aclanthology.org/landing_page/2025.acl-industry.94.pdf, unverified numbers). Repo https://github.com/tsinghua-fib-lab/agentsociety, Apache-2.0 (the `packages/agentsociety/commercial` folder excepted), Python 3.11+. Verified from the README: AgentSociety 2 has "workspace-bound stateless records driven by Ray Tasks", an environment of "modular components with hot-pluggable tools" (e.g. a `CodeGenRouter` over modules like `SimpleSocialSpace`), MCP tool support, routers (CodeGen default, ReAct, Plan-Execute, Two-Tier, Search), a `ServiceProxy` for env/LLM/tracing/replay, and DuckDB replay. The README does not say how the environment adjudicates actions.

| # | Verdict | Why |
|---|---|---|
| 1-3 | no | Environment modules expose tools; an attempt outside the tool set cannot be made. |
| 4 | partly | Social-space modules deliver messages by the graph; unverified. |
| 5 | no | |
| 6 | no | |
| 7 | no | |
| 8 | partly | Agent reasoning is pluggable (routers); no fidelity declaration. |
| 9 | partly | ReAct/Plan routers are internal steps. |
| 10 | no | |

**ADOPT.** The *environment module + tool* idea, where a CodeGen agent emits code against module APIs. It is a cheap way to get "attempt anything the API permits, the module decides". Do not adopt the platform (ADR-017: no second runtime). Worth rechecking that "CodeGenRouter" semantics before borrowing (unverified).
**GAP.** No semantic adjudication for out-of-API attempts.
**Maturity.** Active, Apache-2.0, Python/Ray, no tagged release shown on the repo page.

### 2.5 OASIS (CAMEL-AI)
**What it is.** Social-media simulator, up to 1M agents, with a recommendation system and a platform database. Primary: https://arxiv.org/abs/2411.11581 ; code https://github.com/camel-ai/oasis, Apache-2.0, Python (`pip install camel-oasis`), active (news through 2026-08-19, 973 commits).
Verified: `env.step()` takes `ManualAction` or `LLMAction` per agent; 23 actions total; the platform executes them (backing store appears to be SQLite, not stated).
**Coverage.** no on 1-3 and 5 (closed 23-action menu, so "attempt anything" is impossible by design), partly on 4 (platform delivers posts by network and recommender, never by free speech), no on 6, 7, 10, partly on 8 (`ManualAction` vs `LLMAction` is a per-agent decider switch, nice and small).
**ADOPT.** The `ManualAction | LLMAction` per-agent switch as a minimal precedent for example 8. Already positioned in the earlier survey as scale benchmark; nothing more.
**GAP.** Closed menu is the opposite of the goal.

### 2.6 Project Sid / PIANO (Altera)
**What it is.** 10 to 1,000+ agents in Minecraft. PIANO = Parallel Information Aggregation via Neural Orchestration, concurrent modules around a shared state with a cognitive controller. Primary: https://arxiv.org/abs/2411.00114 (verified abstract: roles, collective rules, culture, "preliminary"). No evidence found that code is open (search found none): treat as closed (unverified).
Key lesson for us (inference from the abstract plus the Minecraft setting): the *world is Minecraft*, so adjudication is a real engine, and the paper's contribution is cognition concurrency, not world rules.

| # | Verdict | Why |
|---|---|---|
| 1-3, 5 | partly | Minecraft engine enforces blocks and doors (as a game), but attempts are limited to what the bot API can express. |
| 4 | partly | Chat range in game. |
| 6 | partly | Day/night, mob spawns run on engine ticks. |
| 7 | no | Roles emerge in agents, not boundary structures. |
| 8 | partly | Multiple concurrent modules inside an agent. |
| 9 | partly | Modules include reflection and goal generation (from background; unverified). |
| 10 | partly | Minecraft's own physics propagates (falling blocks, water), not authored by the project. |

**ADOPT.** The concurrency idea: separate fast and slow streams inside one agent with a bottleneck/controller so output channels stay coherent. This is a design reference for the System-1/System-2 adapter already parked in technology-procurement.
**GAP.** Not reusable code. Not a general rules substrate.

### 2.7 AI Town (a16z-infra)
**What it is.** Deployable Generative-Agents-style starter kit. https://github.com/a16z-infra/ai-town (verified): MIT, TypeScript on Convex (game engine, DB, vector search), 10.7k stars, 1,147 commits, Ollama/OpenAI/Together models, PixiJS. The README does not describe action validation (unverified; ARCHITECTURE.md not read).
**Coverage.** no on all ten, with partly on 6 (cron-driven engine ticks) and 8 (pluggable LLM).
**ADOPT.** Nothing for the substrate. It is a possible *front end/demo* shell. Transactional shared state in Convex is the one useful idea (atomic world commits in a hosted DB).
**Maturity.** Active, MIT, TypeScript.

### 2.8 Voyager and MineDojo (Minecraft as a world that adjudicates free-written actions via code)
**What they are.** Voyager (https://arxiv.org/abs/2305.16291, verified abstract): automatic curriculum, a skill library of *executable code* retrieved and reused, and iterative prompting with environment feedback, execution errors, and self-verification. MineDojo (https://arxiv.org/abs/2206.08853): thousands of open-ended Minecraft tasks given as language, plus an internet knowledge base and a learned video-language reward (MineCLIP). Licenses and activity of the repos are unverified (recalled as MIT; not checked).

This is the cleanest existing demonstration of examples 3, 5 and 10 *in a real engine*: the agent writes arbitrary JavaScript, the game engine executes it, the engine refuses what it refuses (a wall does not let you through, a skill you lack does not exist), and engine rules propagate effects (falling blocks, flowing water, crops). No narrator needs to decide.

| # | Verdict | Why |
|---|---|---|
| 1 | covers (inside Minecraft) | Doors have state and need an interaction; engine owns it. |
| 2 | partly | Blocks hold entities; "affordance" is implicit in code. |
| 3 | covers | Collision is engine-enforced and no menu is involved. |
| 4 | partly | Chat is global/local depending on server config. |
| 5 | partly | Skill is the *agent's code library*, not a recorded world-side skill. A failed script gives engine error feedback, which is the useful loop. |
| 6 | covers | Engine ticks and day cycle. |
| 7 | no | |
| 8 | partly | Agent is LLM, mobs are plain code; no declared fidelity. |
| 9 | no | |
| 10 | covers | Game physics and rules propagate. |

**ADOPT.** (1) The *execution-feedback loop*: attempt -> engine result or error -> next attempt, with the error as an observation to the actor, exactly the "visible rejection" of ADR-013. (2) *Skills as retrieved code* distinguishes agent knowledge from world capability, which supports example 5's hard gate (the world checks a recorded skill, not the code's eloquence). (3) Minecraft-class engines show the right division of labour: LLM writes intent, a deterministic engine decides.
**GAP.** The action surface is the bot API; it is not semantic ("shout to someone overseas" cannot be attempted); engine rules are hand-coded by Mojang, not authored per world.
**Maturity.** Research code, 2023; not a substrate. Mineflayer (the control library, unverified) is the maintained piece.

### 2.9 TextWorld, ALFWorld, Jericho (text games as world engines)
**What they are.**
- TextWorld, https://arxiv.org/abs/1806.11532 (verified abstract): handles "state tracking and reward assignment", builds games by hand or automatically from knobs (`tw-make custom --world-size --nb-objects --quest-length --seed`). Repo https://github.com/microsoft/TextWorld: MIT, Python 3.9-3.12, 664 commits, Inform7 (Artistic-2.0), Jericho (GPL-2.0) and Fast Downward (GPL-3.0) bundled. No releases shown, last activity unverified.
- ALFWorld, https://arxiv.org/abs/2010.03768 (verified abstract): aligns TextWorld text environments with the visual ALFRED environment so abstract policies learned in text transfer to embodied tasks. License unverified.
- Jericho, https://github.com/microsoft/jericho (verified): "lightweight python-based interface connecting learning agents with interactive fiction games", Z-machine only, **GPL-2.0**, v4 documented, 323 commits. It exposes an object tree, template action generator and game dictionary (names only seen in links; mechanism unverified).

These are the closest existing *world-engine-with-rules* family: a text world model whose rules decide effects, with a parser mapping free text to the rule set. The parser is the limit: input outside its grammar is "I don't understand", so the menu is merely hidden.

| # | Verdict | Why |
|---|---|---|
| 1 | covers | Lock/open with a key is the canonical TextWorld rule (precondition: locked -> unlocked via key; unverified in this session but stated in the paper's examples as I recall). |
| 2 | partly | Supporters and containers exist; weight limits unverified. |
| 3 | partly | Closed exits block movement; a free "walk through wall" is a parse failure, not an attempt. |
| 4 | no | No audible space. |
| 5 | no | No skill model; gating is by possession and state. |
| 6 | no | World changes only on a player command (turn-based). |
| 7,8 | no | Single player. |
| 9 | no | |
| 10 | partly | Rule effects chain within one action; no ambient propagation. |

**ADOPT.** TextWorld's *state-tracking + logic-rule* representation is one source for typed preconditions/effects (it is the same family as PDDL, already spiked). `tw-make` as a generator of test worlds for the door/lock case. Do not take Jericho into a product because of GPL-2.0 (and Z-machine only).
**GAP.** No concurrent actors, no autonomous processes, parser-bound attempts.
**Maturity.** TextWorld is a maintained-looking, MIT, Python, Inform7-backed library (activity date unverified).

### 2.10 "LLM as world simulator" literature (the unreliable-narrator evidence)
- Wang et al., "Can Language Models Serve as Text-Based World Simulators?" (ACL 2024), https://arxiv.org/abs/2406.06485 (abstract verified): the benchmark is ByteSized32-State-Prediction (state transitions of text games). Conclusion: GPT-4 is "still an unreliable world simulator without further innovations". Specific accuracy figures were not on the abstract page, so I give none. The earlier ByteSized32 paper (https://arxiv.org/abs/2305.14879, verified): GPT-4 produced runnable games in 28% of cases single-shot and 57% with self-reflection.
- Wu et al., Instruction-Driven Game Engines, https://arxiv.org/abs/2404.00276 (verified abstract): train an LLM for "Next State Prediction" under free-form rules; initial target is poker; no quantitative results on the abstract page.
- World of Workflows (ServiceNow-based, 4,000+ business rules, 55 workflows, 234 tasks), https://arxiv.org/abs/2601.22130 (verified): frontier LLMs show "dynamics blindness", failing to predict hidden cascading side effects, leading to silent constraint violations.
- SIMMER, https://arxiv.org/abs/2606.14574 (verified abstract): a symbolic kitchen world (77 actions, 262 objects, ~46,800 interactions) and a state-machine executor; at most 17% error-free plans across six LLMs, up to 56% with latent failures; explicit state reasoning cut latent failures by up to 72%. Code link not found.
- Hybrid-WM, https://arxiv.org/pdf/2606.27806 (snippet only, unverified): an LLM planner plus a small parametric transition model with a consistency gate.

Reading for us: this is direct evidence for the premise of the project: the narrator cannot hold the cascade in its head (example 10), and measured failure rates are large. It also supports the "ramification" requirement being met by a rules layer, not by prompting.
**ADOPT.** These are *benchmarks to borrow*: World of Workflows-style cascade tests and SIMMER's latent-failure classes (precondition violation, hidden hazard, irreversible) as acceptance tests for our propagation (glass off table -> falls -> breaks).
**GAP.** None provide a framework.

### 2.11 Code world models (LLM writes the rules, a program executes them)
- WorldCoder (Tang, Key, Ellis), https://arxiv.org/abs/2402.12275 (via search snippet, unverified beyond that): LLM builds a Python program of the environment from interactions.
- Code World Models / GIF-MCTS (Dainese et al., NeurIPS 2024), https://arxiv.org/abs/2405.15383 (snippet only).
- Code World Models for General Game Playing, https://arxiv.org/abs/2510.04542 (verified): DeepMind (Lehrach, ..., Murphy). The LLM converts natural-language rules and trajectories into an executable Python model with transitions, legal moves and termination; matched or beat Gemini 2.5 Pro in 9 of 10 games (the "85% vs 30%" figure came from a secondary site, not the abstract; not used).
- OneLife, https://arxiv.org/abs/2510.12088 (verified; ICLR 2026): dynamics as conditionally activated programmatic laws, each with a precondition and an effect; beats a baseline in 16 of 23 scenarios on Crafter-OO.

**Relevance.** These are the machine-authored-mechanics lineage already named in the 2026-10-04 addendum, now with ICLR 2026 and DeepMind confirmation. OneLife's "law = precondition + effect, only relevant laws activate in a state" matches the world-substrate mechanic model closely and could give an independent, published term for it. Coverage of the 10 examples: no (research method), but strong support for 3, 5, 10 *if* laws are authored first.
**ADOPT.** "Conditionally activated law" vocabulary and OneLife's state-ranking / state-fidelity metrics as evaluation of a generated mechanics bundle. Use the CWM-GGP pattern (LLM generates, then a verifier checks against trajectories) for the World Builder approval loop.
**GAP.** Domain-specific, small worlds.

### 2.12 2025-26 work combining free-form LLM action with a validating or rule layer
| Work | What | Verified? |
|---|---|---|
| Orchestrated Reality, https://arxiv.org/abs/2606.16014 (Huang, Li, Fang; 14 Jun 2026) | World is a canonical JSON-entity tree owned by one orchestration agent (GM). Parameterized-Action POMDP. Transition = Plan -> Diff -> Validate -> Apply as content-hashed JSON deltas, and narrative is generated *from* validated state. 15 incident case studies; no player study; code release not stated. | abstract verified |
| PAYADOR / IVIE, https://arxiv.org/html/2606.13348v1 (Vaucher et al., 11 Jun 2026), code https://github.com/micaelavaucher/IVIE (licence not stated) | Reasoning LLM predicts the effects of a player action; predictions are validated before updating an OO Python world (Location/Item/Character/Puzzle/Objective). Players bypassed puzzles by *claiming* to have solved them and the model accepted it (this is exactly example 5's failure). | verified |
| CriticaLLM, https://arxiv.org/abs/2610.21525 (Oct 2026) | Autonomous TTRPG GM with a separate Judge LLM. Method not readable from the abstract page. | abstract only |
| RuleSmith, https://arxiv.org/html/2602.06232 | Engine validates and executes actions; LLM players supply behaviour. | snippet only |

**ADOPT.** Orchestrated Reality's Plan-Diff-Validate-Apply with content-hashed deltas is the same shape as our ADR-013 path (independent confirmation, nothing to import). IVIE's observed "claim-to-have-solved" exploit is a ready-made regression test for the "hard gate" principle (examples 4/5): nothing a speaker asserts can change a gated fact.
**GAP.** All are single-GM, single-player narrative systems; none has autonomous processes, multiple concurrent actors, or propagation rules.
**Maturity.** Preprints from June-Oct 2026; code status unclear. Treat as confirmation, not dependencies.

### 2.13 Typed fast models ("System 1") for animal-like or routine agents
- **Jev** (TypeSafe AI "System One" model): per search-result summaries (https://www.datacamp.com/blog/system-one-models-jev, https://datanorth.ai/blog/jev-what-it-is-and-why-this-new-model-matters; secondary sources, vendor numbers unverified), it takes state plus typed questions (yes/no, choice, score) and returns typed answers with calibrated probabilities, trained with "Reinforcement Learning for Calibrated Decisions". None of the results mention animals. Already recorded in our jev-world-modeling note and technology-procurement as a deferred adapter. No new finding except confirming the interface shape.
- **pymdp** (active inference in discrete POMDPs), https://pypi.org/project/inferactively-pymdp , docs https://pymdp-rtd.readthedocs.io/ : v1.0.0 moved to JAX with batching over many agents; the docs' own examples use a foraging agent (search snippet; unverified for licence, which I recall as MIT). This is the nearest *established, non-LLM, typed, probabilistic* decider for animal-like agents (a mouse foraging for cues). It declares generative-model matrices (A/B/C/D), which are a typed, inspectable fidelity declaration.
- Other established fast deciders for animals and routine NPCs, not searched (inference from general knowledge, mark unverified): behaviour trees, utility AI, GOAP, and NetLogo/Mesa animal-movement models. Mesa is already spiked in world-substrate.

| # | Verdict | Why |
|---|---|---|
| 8 | covers | A fast typed decider is the "implemented by fast typed model" option. |
| 1-7, 9, 10 | no | A decider only; the world must adjudicate its attempts. |

**ADOPT.** For animals: a decider interface of *typed observation in, typed distribution over a closed intent set out*, plus a fidelity record (model id, calibration source). pymdp is the best off-the-shelf animal-like option; Jev is the LLM-adjacent one but is a vendor product with unverified claims.
**GAP.** Calibration of either on animal behaviour is not in any source I read.

## 3. Summary matrix (10 examples x frameworks)

C = covers, P = partly, N = no. Entries for engine-in-the-loop systems say "(engine)" when the credit comes from a host game engine, not the framework.

| Framework | 1 Door | 2 Chair | 3 Wall | 4 Voice | 5 Heli | 6 Clock | 7 Org | 8 Deciders | 9 Think | 10 Ripples |
|---|---|---|---|---|---|---|---|---|---|---|
| Concordia 2.4 | P | N | P | P | N | C | P | P | P | N |
| Smallville | N | N | N | P | N | N | N | N | P | N |
| GenAgents-1000 | N | N | N | N | N | N | N | P | N | N |
| AgentSociety 2 | N | N | N | P | N | N | N | P | P | N |
| OASIS | N | N | N | P | N | N | N | P | N | N |
| Project Sid | P (engine) | P | P (engine) | P | P | P | N | P | P | P (engine) |
| AI Town | N | N | N | N | N | P | N | P | N | N |
| Voyager/MineDojo | C (engine) | P | C (engine) | P | P | C (engine) | N | P | N | C (engine) |
| TextWorld/Jericho | C | P | P | N | N | N | N | N | N | P |
| LLM-sim papers (WoW, SIMMER) | benchmark only | | | | | | | | | benchmark of 10 |
| Code world models | method only; supports 1, 3, 5, 10 if laws exist | | | | | | | | | |
| Orchestrated Reality / IVIE | P | P | P | N | P (IVIE shows the exploit) | N | N | N | N | P |
| Our ADR-013 + world-substrate | see note | | | | | | | | | |

Note on our own stack (judged from the documents read, not retested): the transition-authority path covers 1, 3, 5 (hard gate via write-scope plus checks), 6 (ADR-010 multirate process time and `ActiveSystemSpec` wake), 7 (ADR-006), 8 (ports; fidelity declared per authority), and 10 only as far as mechanics chain (the "no global causal closure" caveat in synthesis.md applies). Examples 2, 4 and 9 are the least-evidenced in our own docs (affordance without action, intent-vs-effect for sound, thought as self-directed action). I did not check the code for them.

## 4. Ranked recommendation

1. **Keep ADR-013 / world-substrate as the consequence layer; do not adopt any LLM-sim platform as the rules layer.** The survey found no framework that adjudicates open attempts with propagated effects. Every platform in scope uses LLM prose, a closed menu, or a host game engine. The 2026 hybrids (Orchestrated Reality, IVIE) are independent confirmation of the Plan-Diff-Validate-Apply shape, which we already have.
2. **Concordia stays the host for loop and cognition only** (consistent with the spike verdict "compose"). Use specifically its `interrupt_*` scheduling (ordered event queue, masks, private timers) for examples 6 and 8, and entity-with-pluggable-acting-component for deciders (scripted, puppet, LLM, fast model). Re-check the spike's "wrong when" conditions on the first LLM-resident run.
3. **Adopt the Minecraft/Voyager division of labour as the design test**: actors submit attempts (even code or free text), a deterministic engine decides, and the refusal/error returns to the actor as an observation. Adopt "skills are world-recorded, not asserted" for example 5, with the IVIE "claimed to have solved it" exploit as a named regression test.
4. **Adopt published evaluation, not code:** World of Workflows (cascading side effects) and SIMMER (latent failure classes) for example 10; OneLife's "conditionally activated law" terminology and state-ranking/fidelity metrics for generated mechanics; the GenAgents-1000 pattern (measured fidelity relative to a baseline) for example 8's declared fidelity.
5. **For animal and routine deciders, use a typed decider interface (typed observation in, distribution over a closed intent set out) and evaluate pymdp first**, with Jev as a parked option (vendor claims unverified). Do not build a System-1 framework.
6. **Do not adopt:** OASIS/AgentSociety runtimes (closed menus or second runtime, ADR-017), Jericho (GPL-2.0, Z-machine only), AI Town (demo shell at most), Project Sid (closed, unverified).

## 5. Unverified items, collected
Smallville's emoji/object-state mechanism; Smallville and AI Town maintenance dates; Voyager, MineDojo, ALFWorld repo licences and activity; Mineflayer; TextWorld lock/key and weight rules and its last release; Jericho object-tree internals; Project Sid code availability; Concordia v2 report details beyond the HTML summary; AgentSociety adjudication internals and its ACL numbers (search snippet); WorldCoder / GIF-MCTS / Hybrid-WM / RuleSmith details (snippets); CriticaLLM method; pymdp licence; Jev performance claims (vendor); whether Concordia `interrupt_*` and SimPy can coexist.
