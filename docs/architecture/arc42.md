---
description: World Substrate architecture in arc42 form - goals, constraints, context, strategy, building blocks, runtime, deployment, concepts, decisions, quality, risks and glossary.
---

# World Substrate architecture (arc42)

This is the architecture entry point. It states what exists, what is targeted and what is missing, keeping those apart. The exact submodels (every rule, its owner and its test) are in [the system model](../model/ODD.md) and [trace.yaml](../model/trace.yaml); required behavior is in the [OpenSpec capability specs](../../openspec/specs/); current sequencing is in [the roadmap](../../roadmap/README.md); what is not yet known is in [the open questions ledger](../planning/open-questions.json).

On 2026-11-09 this page took over from `docs/architecture.md`, `docs/architecture/GOAL.md` and `docs/source-dispositions.md` and carries their current facts, plus current facts from the audits, research notes and plans named in section 8. Those files were compared with this page and retired on 2026-11-09; section 8, "Provenance of retired material", lists each with its successor and the commit that restores it.

## 1. Introduction and goals

### Architectural thesis

A rich world comes from **shared persistent state, semantic grounding, and installed mechanics with explicit local causal authority**. LLM sophistication is useful for policy, cognition, and mechanic proposal, but model prose must not compensate for missing world law or directly mutate canonical state.

**Why (Brian's reason).** The point is scale, not determinism. Brian, 2026-11-09: "an ai adjudicator doesnt really scale and that we need to facts to have implications and blockers. like 50 things could propagate down a causal chain 100 links deep taht the llm would not be able to understand so we need that causal chain to automaticlaly rpogate and to deliver the resutls of that propagation to he ai judge along with blockers." Brian, 2026-07-22: "in general i dont care about determinism. oftne it is better to have simulations that vary to give you more snese of the possiblity space of outcomes. what i am concerned with is an understanable trace of any simulation and general reasonability/fidelity."

Where the code stands against that reason (2026-11-09):

- **Propagation exists.** A change that follows at once runs as a knock-on process, in waves inside the same moment ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)). The cap is 32 reactions per moment (`REACTION_LIMIT`, `src/world_substrate/engine.py`), and a moment that passes it is refused whole. Slower effects run once per round.
- **Blockers reach only the person who tried.** A refused move tells that person which check failed. It does not name the earlier change behind the failure.
- **There is no AI judge.** The Concordia game master is kept off (`scripts/concordia_residents.py`, module docstring). An attempt outside the rulebook changes nothing, apart from a request to another person, which is passed on to that person.

### What the system is for

World Substrate lets a person describe a bounded world in plain language, review the rules the system compiles from that description, approve them, and then run residents (scripted, human or LLM policies) through the world. Residents only express intents. Installed, reviewed mechanics alone decide what changes in the canonical world, and every change or refusal leaves an inspectable record. Per [Decision 006](../decisions/006-governed-rules-layer-scope.md), the repository owns only the governed-rules layer; agent minds, generic schedulers and planners are hosted on off-the-shelf runtimes that call into it. Today that means Concordia hosts the live residents (`scripts/concordia_residents.py`, since 2026-10-16, commit `477b209`); Mesa and a PDDL toolchain were shown to compose in the replacement-first spikes (`spikes/replacement-2026-10/`) and are not used on any live path.

North star: generative worlds with executable laws. A person describes any bounded world in plain words, approves the laws the system proposes, and watches residents live in it while every consequence traces back to an approved, installed rule.

### Requirements overview

These five requirements carry over from the former goal page; each names how it is checked and what would disprove it. Detailed required behavior is in the capability specs.

#### REQ-INTENT-NOT-CONSEQUENCE

A policy (scripted, human or LLM) can only submit an action envelope; it never writes canonical state. The Engine validates the envelope, runs the installed rule and commits all of its writes or none of them.
Success: a malformed or stale envelope, or a rule that reaches outside its declared write scope, is refused with the world's material hash unchanged and the refusal recorded (`tests/test_action_envelopes.py`, `tests/test_first_fill.py`, `tests/test_write_scope.py`).
Disproof: any test or retained run where a refused transition changed canonical state, or where model prose rather than an installed rule produced a committed change.

#### REQ-REVIEWED-AUTHORITY

The authority a rule has (what it reads, writes and when it fires) is derived by the compiler from the rule itself and shown to the reviewer; it is never taken from what the model claims.
Success: the review payload lists compiler-derived read and write paths, unknown effect paths are rejected before installation, and the compiled profile is frozen before the first run step (`tests/test_action_authoring.py`, `tests/test_run_authored_world.py`).
Disproof: a run whose installed rule wrote a path the review did not show, or a profile that changed between approval and execution.

#### REQ-APPROVAL-AND-BUDGET-BEFORE-SPEND

No mechanics run and no model call is made until the person has explicitly approved the mechanics and the request fits the daily budget.
Success: the World Builder service refuses a run without approval (HTTP 409), refuses an unapproved model before any spend, and fails closed on a corrupt budget ledger (`tests/test_world_builder_service.py`).
Disproof: a logged model call or run step that precedes approval, or a day whose recorded spend exceeds the configured cap.

Since 2026-10-15 pressing Create simulation on the landing page is the approval (Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve"; [Decision 005](../decisions/005-native-waltzman-delivery.md)).

#### REQ-OBSERVABLE-RUNS

Every build and run leaves a durable record from which the person can see what happened and why: events with stable ids, mechanic-declared causal parents, and a live view rebuilt only from canonical state ([Decision 002](../decisions/002-observability-and-replay.md)).
Success: snapshot plus event deltas reconstruct each canonical branch exactly, and every build and run writes its record (`tests/test_waltzman_projection.py`, `tests/test_world_builder_service.py`).
Disproof: a view showing a state the canonical event log cannot reconstruct, or a run with no durable record.

#### REQ-ANY-SCENARIO

A person can describe a scenario outside the reference worlds and get a modelled world up front, attempts over time, and rules written mid-run under the same review and approval gates ([Decision 007](../decisions/007-any-scenario-path.md)).
Success: a fresh description produces a reviewable draft, an approved run on the native Engine, and the automatic living view, with mid-run rules passing the same compiler review as up-front ones (evidence under `spikes/any-scenario-2026-10/evidence/`).
Disproof: a described scenario that can only run after hand-written Python mechanics, or a mid-run rule installed without compiler review.

### Quality goals

1. Truthfulness of consequence: what the world records is what installed mechanics did, never what a model asserted.
2. Inspectability: a person can answer "why did this happen" from the retained record alone; observability is required, exact replay is not ([Decision 002](../decisions/002-observability-and-replay.md)).
3. Generality: the same engine and authoring path serve materially different worlds (Kitchen, Orchard, Repair Bay, Waltzman) without per-world engine code.
4. Small owned surface: anything a commodity runtime already does is adopted, not rebuilt ([Decision 004](../decisions/004-product-and-adoption-strategy.md), [Decision 006](../decisions/006-governed-rules-layer-scope.md)).

### Stakeholders

| Who | What they need from World Substrate |
| --- | --- |
| Brian (owner) | A working builder and demo that show generated worlds with executable laws, and an engine other projects can host. |
| Demo visitors and stakeholders | One click from a description to a running world they can watch and question (World Builder, Waltzman Coordination Lab). |
| Researchers using Waltzman's coordination model | A reference world whose trust, risk and coordination dynamics run under inspectable mechanics. |
| Coding agents working in the repository | Clear owners, invariants and checks for every enforced rule (this page, the system model and `trace.yaml`). |

### Thesis and how it would fail

A world built by LLMs stays trustworthy only if consequences come from reviewed, installed mechanics with explicit local authority, and the canonical state they write is the single place truth lives: views, cognition and analysis read it but never become alternate truth.

The thesis fails if a reviewed, approved world still produces consequences the person cannot trace to an installed rule, or if keeping consequences in reviewed mechanics makes describing a new scenario so slow that a direct LLM narration (for example YuLan-OneSim or Concordia's game master) gives users equally trustworthy worlds at a fraction of the effort, as measured in `spikes/any-scenario-2026-10/evidence/onesim-comparison.md`.

## 2. Architecture constraints

| Constraint | Authority |
| --- | --- |
| This repository is the canonical executable-consequence authority; related repositories are donors, not bulk-copied. | [Decision 001](../decisions/001-project-scope.md) (decision owner: the user, 2026-08-31) |
| Observability of every transition is required; exact replay is an M1 fact, not a universal requirement. | [Decision 002](../decisions/002-observability-and-replay.md) |
| Semantic description never implies effects; cognition and analysis are separate layers. | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) |
| Own causal reality; borrow commodity cognition, rendering, scheduling and graph tools. Novel uncertainty earns an experiment; commodity uncertainty is research, reason, select; integration uncertainty is a bounded conformance test. | [Decision 004](../decisions/004-product-and-adoption-strategy.md) |
| Waltzman is delivered natively on this engine; the Cybernetic V3 donor path is regression and fallback only. | [Decision 005](../decisions/005-native-waltzman-delivery.md) |
| World Substrate owns only the governed-rules layer; no native engine, scheduler, renderer or cognition growth. | [Decision 006](../decisions/006-governed-rules-layer-scope.md) (Brian, 2026-10-05: "i approve") |
| Describe-any-scenario: model up front, attempts over time, rules written mid-run under the same review. | [Decision 007](../decisions/007-any-scenario-path.md) (Brian, 2026-10-07: "i approve") |
| World building runs in an agent harness that builds, tests and repairs step by step (implementation in progress). | [Decision 008](../decisions/008-build-worlds-in-an-agent-harness.md) |
| A bounded same-moment fixpoint inside the one existing commit is rule semantics, not new engine capability. | [Decision 009](../decisions/009-same-moment-knock-on-effects.md) (Brian, 2026-10-26: "i approve") |
| Prototype stage, one agent at a time, this repository and its own deploy only; visitor spend capped at $3/day and the owner allowance at $5/day; no new service, engine or repository without Brian's yes. | [roadmap](../../roadmap/README.md), "Actor, recurring job and investment boundary" |

Architecture views name their authority source, cite code ids and state material omissions; the project uses arc42 and does not claim ISO/IEC/IEEE 42010, UML, SysML or KerML conformance (carried from the retired `docs/architecture.md`).

### Causal claim boundary

A World Substrate causal claim is **internal to a represented world under its installed mechanics**. If an installed rule says an overloaded bridge collapses and that rule commits, the system should be able to explain that the represented overload was consumed by the installed collapse mechanic and produced the represented consequence.

That does not by itself establish that the rule is scientifically or empirically correct for a real bridge. Real-world predictive validity, calibration, and causal identification require separate evidence. The substrate's core guarantee is therefore about **explicit consequence authority and inspectable modeled dependencies**, not automatic truth of the model's assumptions.

Current hard parent event IDs are mechanic-declared and validated against retained canonical history. They are stronger than temporal proximity or prompt/context inclusion, but the runtime does not yet derive them from instrumented reads. Use the precise phrase **mechanic-declared hard causal ancestry** when that distinction matters.

Likewise, the current bounded causal-adequacy surface is a dependency inventory mapped to represented state and installed enforcement surfaces plus explicit residual risk. It does not yet provide automatic counterfactual proof of necessity/sufficiency.

### Non-goals

- Recreating Dwarf Fortress, or a universal real-world ontology or physics engine.
- LLM-generated consequences, or unrestricted natural-language world mutation.
- Owning agent cognition, generic scheduling or planning that Concordia, Mesa or a PDDL planner already provides ([Decision 006](../decisions/006-governed-rules-layer-scope.md)).
- Claiming predictive or empirical validity for social or physical systems; causal claims hold inside the represented world under its installed mechanics only.
- Bulk-copying related repositories into this one ([Decision 001](../decisions/001-project-scope.md)).

## 3. Context and scope

```text
visitor / owner (browser)
   |  https://brianmills.dev/world-builder/  (Cloudflare Worker world-builder-pages, built by deploy/cloudflare/world-builder/build.sh)
   v
World Builder API (Worker world-builder-api -> container on the personal VPS, image deploy/vps/Dockerfile)
   |-- llm_client --> model providers (OpenRouter models; default gpt-6-luna)
   |-- Concordia (gdm-concordia 2.4.0) --> resident agents, game master off
   |-- spikes/any-scenario-2026-10 --> people-world (scenario-spec) pipeline, imported at run time
   v
World Substrate engine (src/world_substrate) --> run log, budget ledger, saved worlds and share links on the VPS
```

Upstream semantic input is the pinned Linguistic Core extraction; review pages for planning packages are served from `hive.brianmills.dev/plans/world-substrate/main/proposals/`. The promoted stakeholder demo at `https://brianmills.dev/waltzman/` runs through the Cybernetic V3 donor path on the same VPS (moved 2026-09-16), and `https://brianmills.dev/world-substrate-visualization/` still serves the synthetic prototype as legacy design evidence.

### Source dispositions

Related projects are donors, not competing authorities. Exact reviewed revisions and hashes are recorded in [the source manifest](../../references/sources.json). A donor classification is not an instruction to adopt its code.

| Source | What it contributes | Disposition | Adoption proof required | Authority limit |
| --- | --- | --- | --- | --- |
| Castaway `world-systems` | Deterministic engine behavior, physical rules, discovery, persistence, replay, browser evidence, reviewed linguistic subset | **Extract** bounded implementation seams | Same semantic behavior through World Substrate contracts with donor behavior retained | The positive freshwater path is adopted; donor remains authority for unextracted physical mechanisms |
| Castaway `main` | Earlier survival world, needs, weather, fire, spoilage, regrowth, genuine agent trace | **Historical reference** | None until a later mechanism selects it | Not current substrate architecture |
| Linguistic Core (`linguistic-core` repository, split out of onto-canon6 on 2026-09-04) | Predicate senses, semantic roles, entity types, hierarchy, and source-native provenance | **Pinned semantic dependency** | Reproducible extraction, sense/role review, and coverage audit | Vocabulary and ontology structure never imply executable effects |
| Cybernetic Influence V3 | Canonical world/intent/authority/patch/commit boundary, derived macro-levels, analysis isolation, observability, generated-configuration closure problem, promoted Waltzman funnel/replay UX | **Major architecture, failure-analysis, and UX donor; temporary promoted-demo implementation lineage** | A named World Substrate seam survives local-authority and consumer-path tests or a Waltzman-blocking product need justifies a narrow reimplementation | Its simulator runtime, joint full-world LLM authority, three exact contract families, Concordia choice, and replay-heavy product constraints are not inherited; Decision 005 does not make it a required native runtime dependency |
| Cybernetic Influence V2 | Grounded things versus transitions, local bounded resolvers, attempts versus outcomes, perception/effectors | **Major idea donor** | Reimplement a selected pattern behind World Substrate contracts | Its bespoke runtime, universal port/effect graph, and replay motivations are not inherited |
| Original Cybernetic Influence | Thin-ontology translation gate, perception/provenance distinctions, composed-entity warnings | **Selective semantic donor** | A selected distinction changes runtime meaning or observability | Its influence-specific cognition schema is not a required kernel model |
| Agent Ecology 2 | Executable institutions, rights/authority distinctions, discovery, and concrete premature-effect failures | **Design and failure corpus** | A pattern is respecified and tested locally; no default extraction | Its code and competing authorization paths are not adopted |
| Agent Ecology and Agent Ecology 3 | Ecology experiments, hardcoded-policy/emergence warnings, artifact and institutional experiments, observability/evidence tradeoffs | **Lineage idea donors** | A claim is tied to a pinned example and used to test a World Substrate contract | Installed social dynamics are not evidence that those dynamics emerged |
| Data Contracts | Composition, explicit boundary contracts, validation, and compact boundary observability | **Contract-design donor** | A selected contract pattern reduces authority ambiguity in an implemented slice | Its domain model is not the substrate ontology |
| Collective Competence | Anti-double-counting across mechanism, capability, observed dynamics, and outcomes; coarse-graining tests | **Theory and evaluation donor** | A selected distinction changes a causal or analytic boundary | Macro-level labels do not gain causal force by being measurable |
| Dynamical Laboratory specification | Trajectories, perturbations, recurrence, recovery, and representation comparison | **Research input** | A later evaluation uses a named method and reports its limits | Not the runtime architecture |
| Dwarf Fortress research report | Materials, reactions, shared objects, ongoing processes, persistence, and scale | **Research input** | Claims remain traceable to the preserved report | Not executable code or proof of a universal ontology |
| Shared `llm_client` | Authenticated model invocation and usage evidence | **Conditional policy dependency** | One explicitly authorized traced consumer call | No provider client in the consequence engine |
| Compositional Viable Systems (CVS) | Declared strategic/organizational Situation IR and candidate structural interventions | **Bounded structural input** | One explicit adapter preserves source identity, rejects unsupported semantics, and enters the ordinary causal-review path | CVS structure/interventions do not define installed mechanics or canonical simulated consequences |
| Project Meta policies | Progressive disclosure, one-copy authority, root/subtree instruction surfaces | **Governance dependency** | Repository navigation and structural checks | Does not define simulation behavior |

Only the bounded Castaway fill-through-transfer consumer path has been adopted as implementation; its evidence remains in the M1 traces and receipts. The other repositories are idea, theory, contract, or failure donors, and their source code must not be copied merely because a concept is promoted into World Substrate.

Source findings that still hold:

- Linguistic Core is the central semantic interface but still requires a coverage audit for persistent state relations, qualities, quantities/units, rights, and institutional relations.
- V3 supplies the strongest canonical intent/proposed-patch/commit boundary reviewed so far, but its current general path does not bind Linguistic Core senses or enforce declared state-path reads/writes at commit.
- V2's one-local-resolver-per-attempt principle is the stronger donor for bounded mechanics authority.
- Agent Ecology 2 demonstrates why permission and contract checks must not commit effects before the enclosing action succeeds.
- Agent Ecology lineages warn against calling installed social policy emergent behavior.
- Collective Competence supplies the anti-double-counting rule: a measured outcome or macro-pattern must not be inserted back as another mechanism.
- Data Contracts supports explicit composition and observability surfaces, not code adoption.

Cautions: donor revisions identify the inspected evidence, and later donor changes do not silently change World Substrate doctrine; local paths are conveniences while revisions and hashes identify content; Castaway's `world-systems` branch is a linked worktree of `castaway-world`, pushed to `github.com/BrianMills2718/castaway-world`; worktree changes outside a pinned donor revision are excluded from the inspected evidence; a compiler can audit declared dependencies only and cannot prove that a mechanic author named every consequential dependency. The donor lineage reasoning is in the [Cybernetic Influence lineage review](../research/cybernetic-influence-lineage-review.md) and the [November 7 Waltzman lineage review](../audits/waltzman-lineage-review-2026-11-07.md).

### External analytical-model imports

An upstream analytical model may seed **represented structure** through a bounded adapter without acquiring causal authority. The first exercised path is the [CVS situation import](../../openspec/specs/cvs-situation-import/spec.md): a CVS role/pool/capability/action/rule/scenario slice becomes a `world-substrate-authoring-bundle/v0`, with source identity retained and unsupported semantics rejected, and still enters the ordinary causal-model, compiler, review and approval path. Do not generalize it into a universal architecture schema.

## 4. Solution strategy

```text
represented state
      |
      v
semantic intent / autonomous trigger
      |
      v
Linguistic Core sense + participant roles
      |
      v
installed / constrained mechanic
      |
      v
checks + proposed effects
      |
      v
one Engine commit or refusal
      |
      +--> canonical state + causal event
      |
      +--> replay / analysis / observer views
```

- **Structure and law are authored separately.** A model proposes an authoring bundle (what exists) and a causal model (what actions may read, check and change) as data. A local compiler derives each rule's reads and writes; unknown paths, operators and participants are rejected; model-written source is never executed. Approval freezes a `MechanicProfile`, then ordinary Engine execution runs it ([causal-model authoring](../../openspec/specs/causal-model-authoring/spec.md), [mechanic installation](../../openspec/specs/mechanic-installation/spec.md)).
- **One coordinator commits.** Every action or process runs through the Engine, which commits all writes or none, compares candidate changes with declared write paths and records the event with its declared causes ([transition engine](../../openspec/specs/transition-engine/spec.md)).
- **Everything else is a projection.** Views, residents' memories and analyses read canonical state and events and never write back ([live projection](../../openspec/specs/live-projection/spec.md), [living scene](../../openspec/specs/living-scene/spec.md)).
- **Borrow minds and loops.** The replacement-first gate (recorded 2026-10-05) found that Concordia, Mesa and a PDDL toolchain each compose with the governed-rules layer and none replaces it; the details are in the roadmap's "Replacement-first gate disposition".

What is actually integrated, against what Decision 004 selected in 2026-09: Concordia hosts live residents; deck.gl 9.4.0 is loaded only by the Waltzman reference client (`scripts/render_waltzman_demo.py`); the World Builder draws its network with the vendored graph viewer (`scripts/vendor/`). Pydantic AI, SimPy, Cytoscape.js, PettingZoo and Mesa are not used anywhere in `src/` or `scripts/`; they remain selections, and Decision 006 now routes resident loops and scheduling to Concordia or Mesa when a world needs them.

## 5. Building block view

The diagram source is [model.c4](model.c4) (LikeC4); its arrows follow each module's imports as of 2026-11-09 and are not yet enforced as import contracts. Each block names its spec.

| Block | Code | Responsibility | Spec |
| --- | --- | --- | --- |
| Canonical model | `src/world_substrate/model.py` | `World`, entities with an open typed component registry, material hash and revision; `owner_ref` | [transition-engine](../../openspec/specs/transition-engine/spec.md) |
| Engine | `src/world_substrate/engine.py`, `rules.py` | discover, apply, advance; write-scope enforcement; same-moment settling (`_settle`, `REACTION_LIMIT` 32); causal events | transition-engine |
| Open attempts | `src/world_substrate/attempt.py` | a person's own words read into one typed move, or an unmatched attempt that changes nothing | transition-engine; ODD 11.3 |
| Declared laws | `src/world_substrate/laws.py` | a world's own laws checked at every commit; a breaching step is refused | world-authoring-bundle |
| Rule compiler | `src/world_substrate/action_authoring.py` | compile a causal model into rules and processes with derived authority; discovery cap 256 | [causal-model-authoring](../../openspec/specs/causal-model-authoring/spec.md) |
| Mechanic profile and assays | `src/world_substrate/profile.py`, `assay.py`, `authoring.py` | package, installer checks, freeze, interaction assays | [mechanic-installation](../../openspec/specs/mechanic-installation/spec.md) |
| Semantic binding | `src/world_substrate/semantic.py`, `semantic_relation.py` | cite pinned Linguistic Core senses and roles; six of seven M1 kinds bound | [semantic-binding](../../openspec/specs/semantic-binding/spec.md) |
| Information | `src/world_substrate/information.py` | represented information, delivery and per-observer visibility | [information-delivery](../../openspec/specs/information-delivery/spec.md) |
| Projection and scenes | `src/world_substrate/projection.py`, `living_scene.py`, `living_scene_layout.py` | snapshot plus event deltas; logical scene frames | [live-projection](../../openspec/specs/live-projection/spec.md), [living-scene](../../openspec/specs/living-scene/spec.md) |
| Policies | `src/world_substrate/policy.py` | scripted and LLM selection among Engine-minted action ids | transition-engine |
| World Builder service | `scripts/world_builder_service.py`, `world_builder_runs.py`, `world_dialogue.py` | same-origin HTTP API: generate, approve, run, jobs, budget ledger, run log, share links | [world-builder-page](../../openspec/specs/world-builder-page/spec.md) |
| World Builder page | `scripts/world_builder_home.html`, `world_builder_app.js`, `world_builder_core.js`, `render_world_builder.py` | one box and Create simulation; live play; build record | world-builder-page |
| World generation | `scripts/generate_world_bundle.py`, `generate_causal_model.py`, `scaffold_world.py`, `review_rules.py` | propose structure, propose rules, validate the bundle, independent rules review | [world-authoring-bundle](../../openspec/specs/world-authoring-bundle/spec.md), causal-model-authoring |
| Run driver | `scripts/run_authored_world.py`, `attempts.py`, `concordia_residents.py`, `run_stop.py` | install and run a world; tasks under way; Concordia residents; when a run stops by itself | transition-engine |
| People-world path | `scripts/people_world.py` plus `spikes/any-scenario-2026-10/` (`compile_spec`, `spec_pipeline`, imported at `people_world.py:26,76-77`) | build a world about people through the scenario-spec pipeline | ODD 11 |
| Agent harness | `scripts/world_harness.py` | Decision 008 harness; not called by the live service | none yet |
| Replay and studios | `scripts/render_scene_replay.py`, `render_replay_studio.py`, `render_living_scene.py`, `render_composed_living_scene.py`, `bootstrap_scene_profile.py` | read-only replays over retained traces; Replay Studio builds `evidence/renders/world-replay-studio-v0.html` from `evidence/replay-studio-v0.json`, served at `/world-builder/play/` (`deploy/cloudflare/world-builder/build.sh:11`), with no simulation authority | [scene-replay](../../openspec/specs/scene-replay/spec.md) |
| Native coordination | `scripts/native_coordination_authoring.py`, `native_coordination_comparison.py`, `run_native_coordination.py`, `check_native_coordination.py` | Waltzman-class coordination worlds on one shared profile | [native-coordination](../../openspec/specs/native-coordination/spec.md) |
| Waltzman reference world | `reference_worlds/waltzman/`, `scripts/run_waltzman_demo.py`, `waltzman_demo_service.py`, `render_waltzman_demo.py` | blocked baseline plus exact-history intervention; JSON/SSE projection | live-projection |
| CVS import | `scripts/import_cvs_situation.py`, `reference_worlds/cvs_sustainment/` | CVS Situation IR to authoring bundle | cvs-situation-import |
| Checks | `scripts/check_project.py`, `check_saved_worlds.py`, `check_trace_reads.py`, `deploy_world_builder.sh` | project gate, free replay of saved worlds, trace-read coverage, gated deploy | none |

Reference worlds under `reference_worlds/` (Castaway, Kitchen, Greenhouse, Workshop, Waltzman, CVS sustainment) are fixtures, not engine code. The Workshop world showed the machinery-versus-content split (M6): components are an open typed registry (`model.py:188`), observation needs a location rather than a special actor state (`engine.py:263-270`), and the Workshop keeps its own `pick_up` rule. Only revision-currency and entity-existence checks are substrate-universal; a materially different world re-specifies nearly all other checks (M2 give-path audit).

## 6. Runtime view

### A visitor's build and run

1. The visitor types a description and presses Create simulation; that press is the approval.
2. `/generate-world` runs as a background job (`{"async": true}`, then `GET /jobs/<id>`; Cloudflare cuts requests at 100 seconds). A short call decides whether the description is about people (`world_def: auto`). A world of things goes through `generate_world_bundle.py` (structure, declared resources and laws), `generate_causal_model.py` (rules) and the independent rules review (`review_rules.py`); a zero-cost scripted test run checks that the rules let something happen, with guided retries. A people world goes through `people_world.py` and the scenario-spec pipeline, declares laws over the counts it keeps and gets the same review.
3. `/run` installs the frozen profile and plays one round per request. Concordia residents pick among the actions the rules offer or write an open attempt; the Engine commits or refuses each; same-moment knock-on processes settle inside the moment; `each_round` processes run once per round.
4. Live play pauses at a finish line, after 4 quiet rounds, on an error and every 100 rounds, and says why. A world built since 2026-11-10 also carries a stop setting chosen on the Create page (`run_stop`, Q12): by default the run stops once nothing is changing for 6 rounds (with a group decision, once it is deployed or rejected and the state is back where it was 6 rounds earlier), or it always runs every round, and optionally after N rounds (`max_rounds`) or once the run's recorded AI spending reaches a dollar limit (`max_spend_usd`, carried across one-round requests as `run_spent_usd`), whichever fires first; `scripts/run_stop.py` checks it after each round, the run summary records `stopped`, and the page says why. Worlds saved without it run every round. The page shows each round's moves, refusals with the failing check, and the build record.
5. A share link stores the run and replays it for free (`scripts/world_builder_service.py:570-720`, since commit `4d58941`).

### Waltzman reference world

`scripts/run_waltzman_demo.py` produces a blocked baseline and a represented exact-history intervention fork (`evidence/waltzman/demo-*.json`); snapshot plus deltas reconstruct both branches. Information context is kept separate from causal parents. The adequacy report is a bounded dependency inventory with no global completeness claim (`reference_worlds/waltzman/adequacy.py:75-85`). Waltzman trust, risk and readiness proxies are detachable analysis over evidence.

### Time and cadence

One canonical simulated timeline with independently scheduled mechanisms is the target; render time, process cadence, resident cognition cadence, institution cadence and analysis cadence are distinct concerns, and only represented simulation time is canonical. What exists: `World.tick` is an integer, `Engine.advance()` checks every registered process each step through `due(world)`, World Builder processes run `each_round` or `immediately`, and the Waltzman fixture has scenario-specific trigger ticks and one represented two-tick meeting (`ActivityState`) whose completion rechecks current state. What does not exist: a first-class future-event scheduler; duration-bearing activities in generated worlds are modelled as tasks under way (`scripts/attempts.py`, ODD 11.4). Target rules carried from the multi-timescale note (`docs/research/multi-timescale-execution-2026-09.md`): a wakeup only creates a process opportunity and the installed mechanic still checks and commits; completion of a duration-bearing activity is a new transition opportunity that rechecks then-current state; resident cognition wakes on meaningful observations rather than every low-level event; render interpolation and analysis sampling never advance canonical time; cadence is separate from fidelity. The generic simulation-time and activity schema stays uncommitted: `ActivityState` is scenario-specific (`reference_worlds/waltzman/components.py`) and must not become a universal contract without a second use case.

## 7. Deployment view

| Piece | Where | Notes |
| --- | --- | --- |
| Pages | Cloudflare Worker `world-builder-pages`, built from this repository by `deploy/cloudflare/world-builder/build.sh` | `/world-builder/` landing page, `/world-builder/build/` advanced editor, `/world-builder/play/` Replay Studio |
| API edge | Cloudflare Worker `world-builder-api` | tunnels to the container by container name |
| Service | container from `deploy/vps/Dockerfile` on the personal Netcup VPS (personal-vps `apps/world-builder`), since 2026-10-05 | binds `0.0.0.0:8813` inside the container (`Dockerfile:50`); the CLI default when run locally is `127.0.0.1` (`world_builder_service.py:2612`); `LLM_CLIENT_TIMEOUT_POLICY=ban` (`Dockerfile:41`) |
| Native runs page | `deploy/cloudflare/native-runs/` | static page for native coordination runs |
| Waltzman donor demo | Cybernetic V3 on the same VPS since 2026-09-16 | regression and fallback surface |

Shipping is one command, `scripts/deploy_world_builder.sh [rev]`: it runs the gate, deploys the backend and pages, checks the live page matches the build and reports the backend commit. Browser and measurement checks in `scripts/e2e/` and `scripts/measure_world_builder.py` spend the owner allowance, never the public budget.

The public service boundary (from the live-authoring audit `docs/audits/live-world-authoring.md`, checked against today's code): public calls must be same-origin, are rate-limited and have a 512,000-byte body cap (`world_builder_service.py:46`, `:306-314`); every model call reserves its whole cap from the `world-builder-llm-budget/v1` ledger under one lock before it runs and settles afterwards (`:129-203`), so concurrent jobs cannot overspend; visitors share $3.00 a day (`DAILY_LLM_BUDGET`, `:52`) and the owner, by password, has $5.00 a day (`OWNER_DAILY_BUDGET`, `:60`); up to four AI jobs run at once (`:142-146`); trace ids are `world-builder-live/<kind>/<uuid hex>` (`TRACE_ROOT` at `world_builder_service.py:128`, built at `:522`).

## 8. Crosscutting concepts

### Authority boundaries

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Canonical world | material state, revision, time, identity | policy prose, UI state, private cognition |
| Engine / transition coordinator | validation, singular commit/refusal, causal-history attachment | undeclared mechanic effects |
| Mechanic/profile | applicability, checks, declared reads/writes, effects, processes, limits | direct canonical commit |
| Content/authoring bundle | entities, typed properties, starting relations, action signatures, presentation declarations | executable consequences merely by description |
| Semantic binding | sense/role identity and causal classification | persistence, quantities, effects, scheduling |
| Affordance discovery | actor-local instantiation/filtering of installed mechanics | consequence calculation |
| Policy adapter | scripted/human/LLM selection and explanation | canonical mutation |
| Resident cognition | memory, beliefs, goals, reflection, plans | alternate world truth |
| Persistence | canonical snapshots/history/profile IDs and user-world storage | alternate effects |
| Replay/observer surface | visual/historical projection of represented truth | hidden or invented causal state |
| Analysis | derived interpretation/measurement | rewriting canonical history |

When the mechanic or institution named as causal authority for a transition is missing, the transition refuses with a visible diagnostic (an unregistered action kind is recorded as `unsupported_action`, `engine.py:624-637`) unless the world profile defines the fallback; a silent permissive default is forbidden. Reputation or selection pressure cannot repair corrupted canonical state; transition integrity is the Engine's job (Agent Ecology 2 review).

### Composition, actions and processes

Entities have stable identity and typed components; independent mechanics operate on shared component state under declared authority. Adding another vessel is a **content extension** when existing components and mechanics suffice; adding pressure is a **mechanism extension** because it needs represented state, interactions, failure behavior and evidence. Rules generate finite action instances from current local state; a policy selects among concrete offered actions. Autonomous processes use the same canonical state and transition authority as actions. Installed institutions are causal because the world consults and enforces them, not because of their name.

### The causal-force test and global coherence

Before implementing a named phenomenon as a mechanic, ask: if all lower-level events were held fixed and this named phenomenon were removed, would the world's later transitions or affordances change? If not, it is a derived description, not a new state-writing mechanic. `exchange` can describe two reciprocal `give` events without reapplying transfer; an escrow contract becomes causal because it holds assets and couples release conditions (unbuilt).

Global coherence fails at the boundaries between individually plausible mechanics, not inside them. The sealed-pot example from the strategy session (`docs/research/world-substrate-strategy-session.md`): heat, vaporization, pressure, rupture and flow can each pass their own tests and still duplicate water, read stale enclosure state, implement leakage twice, keep a broken pot containing, compare kilopascals with pascals, or leave heat attached to a pot that no longer exists. The remedy is an explicit boundary per mechanic with declared reads and writes, and composites kept derived unless they add a causal bearer.

### Information, cognition and causal ancestry

Keep five relationships apart: the world interaction; information representation, delivery and observation lineage; cognition context (what a resident was shown); mechanic-declared hard causal parentage; and derived analytic interpretation. Prompt inclusion or temporal order is never enough to call information a hard cause of a decision. The implemented information v0 is deliberately not a belief, reputation or channel-fidelity model ([information-delivery](../../openspec/specs/information-delivery/spec.md)).

### Write scopes, read scopes and placeholders

Write declarations are enforced at state paths: the Engine compares every candidate change with the mechanic's declared `write_paths` and refuses out-of-scope writes; rule-facing hooks run against detached state. For actions, placeholder enforcement restricts writes to entities named by the attempt but does not bind each placeholder to one specific role (`engine.py:110-133`). Declared read paths are recorded on events and not enforced; the proposed recording proxy is in the transition-engine spec, and the `read_scopes_enforced` status fact is a constant in `scripts/check_project.py`, not a measurement. This is not universal ACID: independent attempts commit independently.

### Ownership means custody

`owner_ref` names custody (who holds a thing), not legal title. It is a typed, prefixed reference, and `unowned` is reserved (`src/world_substrate/model.py:12-60`). Reading it as "the owner of" once left six of eight businesses in a generated pencil chain unable to act (World Builder feedback log, 2026-10-06).

### Approval and law provenance

`MechanicProfile.freeze()` gives the reviewed set a stable declaration identity before a run. The law fingerprint does not include a compiler or interpreter version (`profile.py:266-279`), so approval does not yet point at one exact executable law; this matters before long-lived user law is treated as reproducible.

### Observability and presentation

Every attempted transition exposes enough to reconstruct its story: observation where applicable, bearer, semantic binding when available, mechanic, checks, declared authority, committed changes, failure status and resulting state. Refused actions never partially commit. Presentation is downstream: scene profiles, assets, layout, camera, filters and possible/enabled/active/realized relationship states are visualization classifications over installed structure, current state and history, never new world variables. Every live World Builder diagnosis starts from complete request/response logs and retained traces.

### Design consequences carried from the research synthesis

Build the smallest persistent, observable vertical that tests one uncertainty; separate vocabulary, content, mechanics, policy, cognition, canonical state and analysis; require a represented causal bearer and one locally scoped transition authority for every canonical write; keep entities open to unrelated components while each mechanic's reads and writes stay closed; apply only goal-relative accounting and conservation invariants; make unsupported mechanics and residual closure risk visible; prove reuse with a materially different second world before claiming generality.

### Provenance of retired material

On 2026-11-09 the documents below were compared with their successors and retired with `git rm`; any still-true fact not already carried was folded into the successor first. Restore one with `git show <last commit>:<path>`. The sixteen contracts that were under `docs/contracts/` were folded line for line into the OpenSpec specs, each of which names its source contract and last commit.

| Retired path | Reason | Successor | Last commit |
| --- | --- | --- | --- |
| `docs/architecture.md` | superseded by arc42 (facts compared; two still-true rules folded) | `docs/architecture/arc42.md` | `9cefeee` |
| `docs/architecture/GOAL.md` | superseded by arc42 section 1 (carried nearly verbatim) | `docs/architecture/arc42.md` | `9cefeee` |
| `docs/source-dispositions.md` | superseded by arc42 section 3 (all rows carried; donor-worktree caution folded) | `docs/architecture/arc42.md` | `9cefeee` |
| `docs/research/synthesis.md` | conclusions carried by arc42 sections 3, 8, 11 (M1 candidate-count measurement folded) | `docs/architecture/arc42.md` | `75f32bb` |
| `docs/research/world-substrate-strategy-session.md` | conclusions carried by arc42 (missing-authority fallback rule folded into section 8) | `docs/architecture/arc42.md` | `42a82f8` |
| `docs/research/multi-timescale-execution-2026-09.md` | target rules carried in arc42 section 6 Time and cadence | `docs/architecture/arc42.md` | `75f32bb` |
| `docs/research/living-world-projection-2026-09.md` | projection states in arc42 section 8; no-write rule in specs | `docs/architecture/arc42.md` | `bcb2fa2` |
| `docs/research/agent-ecology2-review.md` | findings in arc42 section 3 and semantic-binding spec (reputation rule folded into section 8) | `docs/architecture/arc42.md` | `8b9c1f9` |
| `docs/research/jev-world-modeling-exploration-2026-09.md` | exploratory, not adopted; estimate rules folded into open question Q63 | `tools/planning/questions_src.py (Q63)` | `69cc0b6` |
| `docs/audits/live-world-authoring.md` | service boundary and budget in arc42 section 7; compiler refusals in causal-model-authoring spec | `docs/architecture/arc42.md` | `434141b` |
| `docs/audits/m2-give-path-audit.md` | custody point in arc42 section 8; universal-checks finding folded into section 5 | `docs/architecture/arc42.md` | `fa725a6` |
| `docs/audits/waltzman-coordination-lab-v0.md` | carried by arc42 section 6 Waltzman reference world | `docs/architecture/arc42.md` | `2732aac` |
| `docs/audits/waltzman-kitchen-quality-v2.md` | asset provenance in arc42 section 10; visibility rule in living-scene spec | `docs/architecture/arc42.md` | `b094e24` |
| `docs/audits/world-replay-studio.md` | carried by scene-replay spec and arc42 section 5 | `openspec/specs/scene-replay/spec.md` | `b42ce05` |
| `docs/audits/repair-bay-live-preflight.md` | authored-presentation override carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `c7d65e1` |
| `docs/audits/castaway-zero-review.md` | Castaway fill/drink proof carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `a1df86a` |
| `docs/audits/kitchen-zero-review.md` | Kitchen breadth proof carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `b770059` |
| `docs/audits/scene-profile-bootstrap.md` | bootstrap rules carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `7ea1955` |
| `docs/audits/scene-action-presentation-bindings.md` | action bindings carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `e1a869b` |
| `docs/audits/scene-profile-auto-layout.md` | role-grid-v0 and proposed_geometry carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `e1a869b` |
| `docs/audits/workshop-scene-greenfield.md` | item_layout and Workshop proof carried by scene-replay spec | `openspec/specs/scene-replay/spec.md` | `81540cb` |
| `docs/audits/greenhouse-authoring-proof.md` | Greenhouse zero-review proof folded into scene-replay spec | `openspec/specs/scene-replay/spec.md` | `b42ce05` |
| `docs/audits/living-scene-embodied-renderer.md` | carried by living-scene spec | `openspec/specs/living-scene/spec.md` | `9494375` |
| `docs/audits/living-scene-information-feedback.md` | carried by living-scene spec (textContent rule folded) | `openspec/specs/living-scene/spec.md` | `dacc318` |
| `docs/audits/waltzman-living-scene-profile-v1.md` | checkpoints in evidence/waltzman/living-replay-manifest-v1.json; generic parts in living-scene spec | `openspec/specs/living-scene/spec.md` | `dcd93c3` |
| `docs/audits/waltzman-living-replay-v1.md` | manifest plus tests enforce it; multi-branch wrapper in living-scene spec | `openspec/specs/living-scene/spec.md` | `2716435` |
| `docs/audits/waltzman-m1-acceptance-2026-09-09.md` | promotion in roadmap; pending human review folded into roadmap | `roadmap/README.md` | `9c316a3` |
| `docs/audits/native-waltzman-release-static-readiness-2026-09-19.md` | static review of draft PRs, blockers stale; Decision 005 steps in native-coordination spec | `openspec/specs/native-coordination/spec.md` | `91878f4` |
| `docs/audits/world-authoring-starter.md` | carried by world-authoring-bundle spec | `openspec/specs/world-authoring-bundle/spec.md` | `d7319ad` |
| `docs/audits/world-authoring-builder.md` | eight-section UI superseded by world-builder-page spec; stale-mechanics rule in causal-model-authoring spec | `openspec/specs/world-builder-page/spec.md` | `807053e` |
| `docs/plans/any_scenario_poc.md` | finished plan (C1-C6 met 2026-10-07); outcome folded into Decision 007 | `docs/decisions/007-any-scenario-path.md` | `222e73d` |
| `docs/plans/any-scenario-poc.goal.md` | finished /goal launcher | `docs/decisions/007-any-scenario-path.md` | `222e73d` |
| `docs/plans/any_scenario_poc` | plan machinery of the finished plan | `docs/decisions/007-any-scenario-path.md` | `222e73d` |
| `docs/plans/best-of-all-worlds.goal.md` | finished goal (C1-C6 passed at b7d1dc5); first-round target folded into roadmap | `docs/decisions/008-build-worlds-in-an-agent-harness.md` | `e332eb7` |
| `docs/plans/linked_process_participants.md` | finished plan (L1-L6 met 2026-10-08); facts in ODD 4 and 8.17 | `docs/model/ODD.md` | `43e1dca` |
| `docs/plans/linked-process-participants.goal.md` | finished /goal launcher | `docs/model/ODD.md` | `4d2f65b` |
| `docs/plans/linked_process_participants` | plan machinery of the finished plan | `docs/model/ODD.md` | `4d2f65b` |
| `docs/plans/run-loop-contention.goal.md` | superseded 2026-10-26 by open_attempt.md, never adopted | `docs/plans/open_attempt.md` | `389f3f8` |
| `docs/plans/scenario_actors_kept.md` | superseded 2026-10-08 before any work; odd_brief defect folded into ODD 10 | `docs/model/ODD.md` | `49da160` |
| `docs/plans/scenario-actors-kept.goal.md` | superseded /goal launcher | `docs/model/ODD.md` | `2e409ab` |
| `docs/plans/scenario_actors_kept` | plan machinery | `docs/model/ODD.md` | `2e409ab` |
| `docs/plans/scenario_metamodel.md` | never built; Commitment idea carried by open question Q58 | `tools/planning/questions_src.py (Q58)` | `179e519` |
| `docs/plans/scenario-metamodel.goal.md` | unbuilt /goal launcher | `tools/planning/questions_src.py (Q58)` | `179e519` |
| `docs/plans/scenario_metamodel` | plan machinery | `tools/planning/questions_src.py (Q58)` | `179e519` |
| `docs/plans/scenario_spec_adoption.md` | finished plan (S1-S6 met, adopted 2026-10-15); check meanings folded into ODD 10 | `docs/model/ODD.md` | `e092968` |
| `docs/plans/scenario-spec-adoption.goal.md` | finished /goal launcher | `docs/model/ODD.md` | `757b35c` |
| `docs/plans/scenario_spec_adoption` | plan machinery | `docs/model/ODD.md` | `757b35c` |
| `docs/plans/system_model_pipeline.md` | finished plan (M1-M3 done); ODD 10 is the result | `docs/model/ODD.md` | `8232c22` |
| `docs/plans/system-model-pipeline.goal.md` | finished /goal launcher | `docs/model/ODD.md` | `8232c22` |
| `docs/plans/system_model_pipeline` | plan machinery | `docs/model/ODD.md` | `8232c22` |
| `docs/plans/waltzman-belief-and-traces.goal.md` | finished goal (D1-D5 done); trace-read rule in root AGENTS.md | `docs/model/ODD.md` | `352eba6` |
| `docs/plans/waltzman_scenario_run.md` | finished plan (W1-W5 met); scenario text and first run folded into ODD 10 | `docs/model/ODD.md` | `cb24858` |
| `docs/plans/waltzman-scenario-run.goal.md` | finished /goal launcher | `docs/model/ODD.md` | `b1d506f` |
| `docs/plans/waltzman_scenario_run` | plan machinery | `docs/model/ODD.md` | `b1d506f` |
| `docs/plans/waltzman-tasks-slice2.goal.md` | finished goal (E1-E5 done); check meanings folded into ODD 11.4 | `docs/model/ODD.md` | `6a8e37e` |

## 9. Architecture decisions

| Decision | Date | What it settles |
| --- | --- | --- |
| [001](../decisions/001-project-scope.md) | 2026-08-31 | one canonical world-substrate repository |
| [002](../decisions/002-observability-and-replay.md) | 2026-09-02 | observability required, exact replay not |
| [003](../decisions/003-semantic-mechanical-boundary.md) | 2026-09-02 | semantics separate from causal mechanics |
| [004](../decisions/004-product-and-adoption-strategy.md) | 2026-09-07 | Generative-World Builder product; adoption method |
| [005](../decisions/005-native-waltzman-delivery.md) | 2026-09-18 | native Waltzman delivery; Create simulation as approval (2026-10-15) |
| [006](../decisions/006-governed-rules-layer-scope.md) | 2026-10-05 | governed-rules layer only, hosted on commodity runtimes |
| [007](../decisions/007-any-scenario-path.md) | 2026-10-07 | describe-any-scenario path |
| [008](../decisions/008-build-worlds-in-an-agent-harness.md) | 2026-10-16 | build worlds in an agent harness (in progress) |
| [009](../decisions/009-same-moment-knock-on-effects.md) | 2026-10-26 | same-moment knock-on effects are rule semantics |

Decision 006's "wrong when" names a `CognitionAdapter` path that does not exist in the code (open questions ledger).

## 10. Quality requirements

| Quality | Scenario | Evidence |
| --- | --- | --- |
| Truthfulness | a refused or out-of-scope transition leaves the material hash unchanged and is recorded | `tests/test_write_scope.py`, `tests/test_action_envelopes.py`; trace.yaml `RULE-ATOMIC-COMMIT-OR-REFUSAL`, `RULE-WRITE-SCOPE` |
| Inspectability | snapshot plus deltas reconstruct baseline and intervention branches | `tests/test_waltzman_projection.py` |
| Reproducible behavior where claimed | three fresh Kitchen runs reproduced Bo's fill at t9, the handoff at t10, Ama taking the knife at t11 and the terminal at t17 (`evidence/kitchen/full-service-replication-v1-summary.json`) | Kitchen replication |
| Generality | Kitchen, Greenhouse, Orchard, Repair Bay, Workshop and Waltzman run on the same engine; generated worlds build from descriptions | 23 of 24 builds reached their finish line on 2026-10-23 with gpt-6-luna, 19 of 24 both faithful and finished ([trace read](../../evidence/luna-rules-2026-10-23/TRACE_READ.md)) |
| Cost | visitor builds within the daily cap | $0.0032 per build measured 2026-10-23 (same trace read) |
| Asset provenance | Waltzman assets-v2 SVGs under `reference_worlds/waltzman/assets-v2/` were authored for this repository; third-party UI screenshots were inspiration only | Kitchen quality v2 audit (`docs/audits/waltzman-kitchen-quality-v2.md`) |

## 11. Risks and technical debt

Each item has an entry in [the open questions ledger](../planning/open-questions.json) with the decision it blocks and what would settle it.

- Blockers do not name the earlier change behind a refusal, so a long causal chain is not explained to the person or to any AI judge (section 1).
- The live path imports code from `spikes/any-scenario-2026-10/`, so spike code is production code.
- Semantic binding is looked up by bare action kind (`engine.py:224-226`), so generated worlds' `take` and `fill` events carry Castaway mechanic ids that are not installed.
- `schemas/world-authoring-bundle-v0.schema.json` rejects every bundle that declares laws.
- Placeholder write scopes are participant-bounded, not role-specific (`engine.py:110-133`).
- The discovery cap of 256 truncates silently (`action_authoring.py:31`). Bounded presentation does not bound candidate generation: measured at M1, Castaway's 69 colocated vessels yielded 4,927 candidate actions and a 73.3 KB prompt (research synthesis).
- A mechanic exception is rolled back and re-raised, not recorded as a refusal event (`engine.py:785-788`).
- The law fingerprint omits the compiler version (`profile.py:266-279`).
- No lockfile or `pyproject.toml`; the project check pins its tools on the command line.
- Concurrency semantics between concurrent deliberation and contended writes are undefined; indexing and observation selection at scale are unmeasured.

## 12. Glossary

| Term | Meaning |
| --- | --- |
| Canonical state | the only material world truth; prompts, UI state, resident beliefs and analyses do not compete with it |
| Mechanic | installed rule or process with applicability, checks, declared reads and writes, effects, limits and trace behavior |
| Mechanic profile | the validated, frozen declaration set for one run |
| Affordance | one currently available action instance derived from canonical state |
| Observation | an actor-authorized projection of world state and information |
| Authoring bundle | represented entities, components, action signatures and presentation intent; not executable law |
| Causal model | constrained, reviewable declaration of executable law; data, not model-written code |
| Causal bearer | the represented actor, process, institution, disposition or input whose presence changes possible transitions |
| Semantic binding | a profile over a pinned Linguistic Core sense and roles, plus specialization, causal class, bearer, mechanic id and interpretation limits |
| Open attempt | a person's own words for what they try, read into one typed move or kept as an unmatched attempt that changes nothing |
| Same-moment knock-on | an `immediately` process that reacts inside the same moment, up to 32 reactions |
| Task under way | a move that starts a duration-bearing activity that later rounds' processes advance and end |
| Declared law | a world's own law, checked at every commit; a breaching step is refused and names the law |
| `owner_ref` | custody, not title |
| Mechanic-declared hard causal ancestry | parent events an installed transition names, validated against history; not derived from instrumented reads |
| Bounded causal adequacy | a scoped inventory mapping consequential assumptions to represented state and enforcement surfaces, with residual risk; not counterfactual proof |
| Declared enforcement coverage | whether explicitly declared behavior is mapped to enforceable interfaces |
| Projection state | possible, enabled, active or realized, derived for visualization only |
| People world | a world about people with their own goals, built through the scenario-spec path (ODD 11) |
