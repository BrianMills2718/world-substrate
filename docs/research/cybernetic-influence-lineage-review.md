---
role: research-ledger
status: non-authoritative
reviewed: 2026-09-02
authority_refs:
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
---

> **Research record, not project authority.** This document preserves the reasoning, alternatives, objections, and donor findings developed during the 2026-09-02 World Substrate strategy session. Accepted doctrine lives in the linked decisions; current sequence lives in the roadmap; implemented behavior lives in code, tests, and evidence.

# Cybernetic Influence Lineage Review for World Substrate

**Reviewed:** 2026-09-02  
**Scope:** `cybernetic_influence_v3` in depth; `cybernetic_influence_v2` and the original `cybernetic_influence` as idea donors  
**Use:** Strategy and architecture input for World Substrate, not a proposal to adopt any repository's code

## Executive judgment

Cybernetic Influence V3 is the closest donor reviewed so far to World Substrate's **causal discipline**, but it is not yet a donor for World Substrate's **semantic substrate** or for a generally extensible mechanics system.

Its best ideas are:

- one canonical persistent world, separate from agent cognition;
- open semantic attempts separated from successful state transitions;
- transition authorities that propose patches rather than directly mutate the world;
- one atomic validation-and-commit boundary;
- organizations and other macro-entities treated as derived coarse-grainings unless a concrete controller is modeled;
- topology, routing, permission, perception, and success kept distinct;
- representation depth chosen relative to the question;
- simulation authority separated from post-run analysis authority.

Those ideas should be promoted into the World Substrate design.

The central negative finding is equally important: V3 has identified but not solved the problem World Substrate most cares about. Its current general path accepts open natural-language action strings, but exact execution is limited to three hard-coded contract families—sensing, resource transformation, and resource transport. Other effects can be delegated to one joint LLM adjudicator. The path does not use Linguistic Core senses or roles, does not enforce an authority's declared read/write paths at commit, and cannot prove that an authored mechanic includes every consequential dependency. Its own relief-port example calls this the **generated-configuration causal-closure problem**.

In short:

> V3 supplies a strong transition envelope and a very useful statement of the closure problem. Linguistic Core plus an agent-extensible mechanics layer would need to supply the missing semantic and mechanical middle.

V2 deserves more than a brief historical note. In some respects it contains the stronger donor for agent-authored mechanics: each attempted interface is supposed to bind to a local, bounded resolver or mechanism with its own input, read, write, and effect scope. The original repository is mainly a cognition, perception, and semantic-translation donor; its nine-field mediation model is too prescriptive for the world kernel but potentially useful for optional agent architectures and influence analysis.

## Lineage at a glance

| Repository | Primary contribution | Main limitation for World Substrate | Disposition |
| --- | --- | --- | --- |
| [`cybernetic_influence_v3`](https://github.com/BrianMills2718/cybernetic_influence_v3) | Canonical world/intent/authority/patch/commit boundary; derived macro-levels; analysis isolation; explicit causal-closure problem | No Linguistic Core binding; only three exact general-contract families; broad joint LLM authority; heavy replay/evidence machinery | Major architecture and failure-analysis donor |
| [`cybernetic_influence_v2`](https://github.com/BrianMills2718/cybernetic_influence_v2) | Grounded things versus transitions; local mechanism authority; attempt versus outcome; perception/effectors; organizations as derived | Large bespoke runtime; many guarantees motivated by replay and evidence custody; authoring still not general | Major idea donor, especially for mechanics locality |
| [`cybernetic_influence`](https://github.com/BrianMills2718/cybernetic_influence) | Thin-ontology translation gate; perception and provenance; carrier/signal/interpretation distinctions; composed-entity warnings | Runtime was mainly static review over notebook outputs; cognition model is influence-specific and overstructured for the kernel | Selective semantic/cognition donor |

## V3 in depth

### What V3 is trying to become

The active goal is a conversational laboratory in which a user describes a bounded sociotechnical world, reviews a compiled configuration, runs agents through Concordia, and inspects the trajectory, assumptions, state, provenance, and optional analyses. It explicitly presents results as conditional pathways under declared assumptions, not predictions.

The adopted architecture gives Concordia the outer actor/component lifecycle, scheduling, and game-master loop. A project-owned canonical-world component retains typed world truth, projects actor-specific context, receives semantic intents, invokes declared transition authority, validates structured patches, and atomically commits or rejects them. The architecture is described in [ADR-013](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/main/docs/adr/013-generalized-simulator-foundation.md).

The project also separates:

- `ScenarioSpec`: what exists and how it may change;
- `RunSpec`: execution controls and scheduled moments;
- `AnalysisSpec`: detachable read-only interpretation;
- a future `ExperimentSpec`: forks, interventions, repetitions, and comparisons.

That separation was introduced after an earlier design injected the analyst's question into actor and adjudicator prompts, making the simulated behavior partly a response to the research objective. [ADR-014](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/main/docs/adr/014-separate-simulation-and-analysis-authority.md) is a strong donor: a world transition authority should decide what happens under the world's mechanics, not whether the analyst's desired outcome was achieved.

### The strongest theoretical contributions

#### 1. Open intent, closed causal authority

V3 correctly rejects exhaustive action enumeration. An actor can express an open semantic intent, but intent does not itself mutate the world. A transition authority produces a patch; the canonical component validates and commits it.

This matches the World Substrate distinction between a Linguistic Core predicate and an executable mechanic. It also supports the user's point that actions belong to things with causal force: an agent can attempt `give`; a storm can be an active world process; a brittle-pot disposition can be triggered by pressure; an escrow institution can couple multiple transfers. The commonality is not an event taxonomy. It is that each causal bearer submits or produces a transition through an authority boundary.

#### 2. Derived organizations and reversible coarse-graining

[ADR-006](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/main/docs/adr/006-boundaries-are-reversible-derived-coarse-grainings.md) is one of the best donors in the lineage. An analytical boundary does not act or own state. “The organization approved the purchase” is normally a coarse projection of member actions, artifacts, and mechanisms. If a coarse organizational surrogate is intentionally used instead of those details, its representation depth and causal responsibility must be explicit; it must not coexist as a second executor for the same behavior.

This is consistent with Collective Competence and the user's anti-double-counting requirement. V3 adds a useful evaluation idea: whether a higher-scale entity is causally useful should be tested through perturbations, member replacement, feedback interruption, and compression/prediction assays, not asserted because a collective noun exists.

#### 3. Orthogonal relations rather than overloaded edges

[ADR-008](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/main/docs/adr/008-separate-spatial-topology-from-routing-and-permission.md) separates spatial containment and adjacency from routing, operability, permission, reachability, perception, and successful traversal. This is directly applicable to World Substrate. The same design rule should apply to ownership: provenance, possession, custody, access, control, legal title, beneficiary status, and authority to transfer must not be hidden behind one relation.

#### 4. Question-relative representation depth

[ADR-011](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/main/docs/adr/011-declared-representation-depth.md) treats exact, empirical, stochastic, LLM-mediated, scripted, and externally supplied implementations as alternative representations of a typed subsystem. A coarse surrogate can be more honest than a detailed but badly misspecified model. Each representation should state what it preserves, omits, assumes, and cannot answer.

World Substrate should retain this idea but simplify its evidence burden. A mechanics agent needs to declare abstraction level, preserved distinctions, dependencies, unsupported interactions, and local invariants. It does not need to establish exact replay.

#### 5. Cognition is local to the agent, not canonical world truth

The current general path keeps an actor's natural-language memory in the actor context and exposes only authorized observations and records. Trust and belief are not universal global variables. This is close to the user's intuition: the world contains Robin, the pot, delivered information, and Robin's actions; Robin's private interpretation belongs to Robin's resident agent process. Conflicting beliefs are not contradictions in canonical truth—they are different agents' internal states.

The implementation still records memory and model receipts for checkpointing and inspection, but the conceptual separation is sound. World Substrate can adopt the boundary without adopting V3's checkpoint/replay apparatus.

### What the current implementation actually does

The present general contracts are much narrower than the surrounding theory.

#### Semantic intent is an ungrounded string

`SemanticActionIntent` contains:

- `action: str`;
- `target_refs: list[str]`;
- purpose, expected effect, and rationale prose;
- optional selections from available exact transition contracts.

The actor validator checks identity, world revision, selected contract IDs, structured contract arguments, and evidence references. It does not bind `action` to a Linguistic Core predicate sense, validate its semantic roles, classify it as action/process/state/composite, or validate `target_refs` against a sense signature. Consequently, “open semantic action” currently means trusted prose plus some IDs, not a semantic compiler boundary.

This is the most important missing connection to World Substrate. Linguistic Core could provide:

- sense identity and specialization;
- role signatures and participant typing;
- mappings among paraphrases and related frames;
- classification candidates for action, state, process, composite, or institutional event;
- a stable semantic key to which one or more mechanics can bind.

It would not provide the mechanic's state dependencies, write effects, scheduling, or integration invariants.

#### Exact execution is a closed set of three families

The general world spec defines exact contracts for:

1. sensing a declared hidden field into a public output record;
2. transforming specified resource quantities into another resource;
3. transporting a specified resource quantity along a declared route and writing an arrival record.

The compiler and runner contain family-specific code to materialize and attribute each operation. A fourth exact mechanic family would currently require new Pydantic contracts plus new compiler, runner, attribution, and validation paths. This is not yet a registry-driven general mechanics layer.

The design dossier recognizes that the authoring seam is much narrower than the old runtime. That diagnosis is correct. For World Substrate, mechanics-agent output cannot merely generate more instances of three schemas. It needs a general transition-authority contract or small mechanics DSL with reusable state-path, precondition, effect, invariant, and scheduling primitives.

#### The broad LLM authority is not actually read/write scoped

`TransitionAuthoritySpec` declares `reads` and `writes`, but the current canonical committer does not check an operation against those paths. It checks only broad patch grammar—operation kinds such as `replace`, and record categories such as `record` or `resource`—plus a few family-specific exact-contract attributions and generic invariants.

The joint adjudicator receives the whole serialized canonical state, including hidden state, and the current vertical requires exactly one LLM semantic authority. For state not claimed by an exact contract, that authority may propose a “coarse authority” edit anywhere its record-type grammar permits.

This is a material gap, not a stylistic complaint. A mechanics component's safety and composability depend more on precise read/write authority than on JSON shape. V2's “one bounded resolver per effector” is the better donor here. World Substrate should use a local authority selected by the semantic-mechanical binding, project only its declared context, and validate every write path independently of the LLM or code implementation.

#### Non-agent processes are stronger in the theory than in the current general path

The V3 ADRs distinguish intentional action, autonomous processes, environmental processes, triggered dispositions, and exogenous events without insisting on a new taxonomy. The older causal/active runtime contains richer multirate process machinery.

The current Concordia general runner, however, instantiates configured people as actors, collects one intent from every actor at a scheduled moment, and sends the joint batch to one LLM authority. The generalized active-system declarations do not yet amount to a cross-domain scheduler for fire, storms, degradation, queues, or other non-agent processes.

World Substrate should therefore adopt the conceptual distinction but not infer that V3 has solved non-agent causation. A thin vertical with one autonomous process remains necessary.

### Causal closure: the central shared research problem

V3's most valuable failure example is the relief-port transport path. A cargo transport can be locally well-formed:

- source cargo decreases;
- destination cargo increases;
- a route exists and is operational;
- no resource goes negative;
- the patch commits atomically.

It can still be globally incoherent if it does not consume or check the modeled truck, fuel, berth capacity, customs clearance, or labor. The surrounding world contains those facts, but the transport contract does not read them. Their only effect may be through an LLM actor or adjudicator “remembering” that they matter.

This is a cleaner example of global incoherence than a vague warning about interacting physics. Each component is individually valid; the failure is that the executable dependency graph does not match the world description.

V3 now supports declared `required_reads`, reports whether each is exact/coarse/descriptive/unsupported, and can install exact guards on the selected transport vertical. This is useful. It does not prove causal closure because the compiler can audit only dependencies the author declared. A semantic reviewer may notice missing fuel or customs, but there is no general proof that all consequential dependencies were named.

For World Substrate, causal closure should therefore be treated as an **assay and risk label**, not a binary theorem:

1. Extract candidate dependencies from the semantic world, Linguistic Core roles, entity components, dispositions, and installed institutions.
2. Compare them with each mechanic's declared reads, writes, preconditions, and downstream effects.
3. Search for nearby state that appears consequential but is not in the mechanic graph.
4. Generate counterexamples and interaction tests.
5. Mark the mechanic profile's known coverage and unsupported interactions.
6. Freeze the reviewed profile for the run.

LLM mechanics agents are well suited to this work, but “the agent generated code that passes unit tests” is insufficient. The hard task is dependency discovery and cross-mechanic integration.

### Observability: take the causal explanation, leave the replay mandate

V3 records excellent explanatory material: actor context, intent, authority, operations, preconditions, validation errors, before/after revisions, operation attribution, model receipts, and resulting state. This is a strong observability donor.

It also devotes substantial complexity to digests, exact checkpoints, strict restore, replayability flags, state hashes, provider receipts, and matched-run evidence. Those requirements are rational for V3's wargaming and experiment goals, but they conflict with World Substrate's explicit non-goals.

World Substrate should retain:

- what the causal bearer perceived or read;
- what it attempted;
- which semantic sense and roles were bound;
- which mechanic or process had authority;
- which applicability and invariant checks passed or failed;
- which effects committed;
- which interactions were unsupported or approximated.

It should not make exact restoration or re-execution a promotion gate.

### Concordia is not the main donor

V3's switch from a bespoke runtime to Concordia is a lineage-specific product decision. It does not establish that World Substrate should use Concordia. The portable value is the ownership boundary: an agent framework may own cognition and deliberation while a project-owned world component owns persistent truth and validated transitions.

World Substrate should evaluate its current runtime and agent integration on that boundary. Adopting Concordia, or any other framework, is a later implementation choice.

## Earlier versions as idea donors

### V2: promote several ideas that V3 partially obscures

V2's accepted target architecture is unusually aligned with the mechanics problem:

- persistent things are distinct from mechanisms and events;
- an action interface permits an attempt, not an outcome;
- capability, technical reach, credentials, knowledge, normative permission, attempted action, and accepted effect are distinct;
- effects begin at a local invoked interface or explicit exogenous input;
- each mechanism declares inputs, read surface, write surface, outputs, effect vocabulary, granularity, and timing;
- routing follows explicit local structure rather than a universal semantic search;
- organizations are derived unless a concrete controller is intentionally represented;
- exact, procedural/stochastic, bounded model-mediated, and agent-mediated implementations are fidelity choices, not different ontologies.

The most useful V2 contribution for mechanics agents is its [bounded resolver contract](https://github.com/BrianMills2718/cybernetic_influence_v2/blob/main/docs/adr/ADR-004-bounded-resolver-contract.md): one resolver per effector or attempted interface, with a scoped output envelope that cannot express unrelated effects. The original justification was to make it structurally impossible for an LLM resolving a door attempt to also open a vault or rewrite an unrelated light switch.

World Substrate should generalize that pattern:

> One semantic-mechanical binding selects one local transition authority. The authority may be deterministic, stochastic, LLM-mediated, external, or agent-authored, but it receives only declared inputs and can propose only declared effects.

V2 also supplies a useful distinction between an information carrier, the representation encoded on it, delivery to an agent, interpretation by an agent, and belief. This may be needed when information itself has world effects, but it should remain optional and question-relative rather than become mandatory reification for every claim.

What not to import from V2:

- the custom runtime as a whole;
- exact causal replay and evidence-custody requirements;
- a universal port/effect graph at maximal granularity;
- the assumption that all meaningful actor behavior fits a synchronous turn model;
- scenario-specific ontology promoted to kernel vocabulary.

### Original repository: retain translation and perception ideas selectively

The original lineage's [canonical translation](https://github.com/BrianMills2718/cybernetic_influence/blob/master/wiki/wiki/concepts/canonical-translation.md) contains a valuable complexity gate: before promoting a source term into the runtime ontology, ask whether it changes what exists, what can be perceived, what can be attempted, or what the world does next. Otherwise it belongs in prompt semantics, scenario metadata, or analysis.

That is strongly compatible with the causal-force test and Linguistic Core. World Substrate can retain a rich donor vocabulary without turning every donor category into a kernel class.

The original also sharply distinguishes:

- actual world cause;
- received sign or carrier;
- the object an interpreter thinks the sign concerns;
- the interpreter's hypothesis or “interpretant”;
- the resulting external action or internal learning.

This is useful for optional agent cognition and influence-analysis modules. The false-independence example—several apparent confirmations sharing one hidden source—is a good demonstration of why provenance and delivery can matter without making beliefs world truth.

The nine-field “mediation bundle,” however, should not be a required World Substrate agent contract. It encodes an influence-analysis theory of cognition: object maps, causal templates, trust priors, salience, values, affordances, and update rules. Resident agent systems should be free to use an LLM, planner, state machine, learned policy, or their own memory architecture. World Substrate should standardize only the observation/attempt boundary needed to interact with the world.

Likewise, the original composed-entity model sometimes treats a group as a node with an aggregation rule. The later V2/V3 formulation is safer: use that only as an explicit coarse surrogate, or derive the group action from constituent mechanisms. Do not let both levels cause the same outcome.

## Implications for Linguistic Core

Cybernetic Influence confirms why Linguistic Core matters. V3's `action: str` gives agents expressive freedom, but it supplies no stable semantic contract for mechanics discovery or reuse. Exact contract IDs then become hand-authored action catalogues under another name.

A better World Substrate path is:

```text
natural-language proposal
    -> Linguistic Core sense and role binding
    -> causal-role classification
    -> mechanic/disposition/institution lookup
    -> local transition-authority invocation
    -> validated proposed effects
    -> one canonical commit
    -> derived composite descriptions and analysis
```

For a concrete `give` example, Linguistic Core might supply the sense and roles:

- predicate sense: `give`;
- giver: Robin;
- theme: spear;
- recipient: Friday.

The installed mechanic must add what language alone does not determine:

- which persistent relation represents possession or custody;
- whether Robin currently bears that relation to the spear;
- whether the spear is transferable under this world's rules;
- whether quantity, location, reach, consent, or institutional authorization matter;
- which state paths are read and written;
- what counts as success, refusal, loss, or partial completion;
- which local invariants must hold after commit.

An analyst can later bind two independent `give` events to an `exchange` sense without applying another transfer. If an escrow institution exists, its release mechanic is the new causal bearer.

This is exactly the layer V3 lacks: semantics richer than free text, mechanics more general than three hard-coded schemas, and composition disciplined enough not to infer that a semantic relation automatically causes an effect.

## Recommended World Substrate response

### Promote now

1. **Canonical transition envelope**  
   Semantic binding → attempt → selected local authority → proposed effects → applicability/invariant checks → atomic commit or refusal → causal trace.

2. **Authority locality**  
   Enforce declared read and write paths independently of implementation. Prefer one resolver/mechanic per binding over one omniscient joint adjudicator.

3. **Analysis isolation**  
   Exchange, trust, cooperation, organizational action, and collective competence remain detachable derived views unless a represented causal bearer changes future affordances.

4. **Derived macro-levels with step-down**  
   A coarse organization or collective representation must identify the lower-level mechanisms it replaces or summarizes. It must not duplicate them.

5. **Orthogonal state relations**  
   Separate location/topology/routing/permission/success and provenance/possession/custody/control/title/benefit/transfer authority.

6. **Question-relative fidelity**  
   Mechanics agents declare preserved distinctions, assumptions, unsupported interactions, and refinement conditions rather than claiming universal physics.

7. **Causal-closure assay**  
   Treat closure as a continuing dependency and interaction review, not a compiler boolean.

### Do not promote

- a single joint LLM game master with full-world access;
- free-text semantic actions as the only cross-domain interface;
- hard-coded exact-contract families as the extensibility mechanism;
- exact replay, deterministic restoration, provider receipts, or state hashes as product requirements;
- a required universal belief or mediation schema;
- Concordia as an architectural conclusion from this review;
- an organization agent plus detailed member mechanics for the same causal responsibility.

### Move offline mechanics authoring earlier in the learning sequence

The current memo places the first mechanics-agent experiment after several manually built slices. V3's experience suggests testing the central hypothesis earlier. A revised sequence should be considered:

1. audit one micro-world against Linguistic Core and persistent-state needs;
2. implement one primitive `give` vertical and the generic transition envelope by hand;
3. verify that two independent gives can be derived as exchange without double application;
4. ask a mechanics agent to author one adjacent, bounded mechanic before the run;
5. immediately run a causal-closure and interaction assay against the hand-built mechanic;
6. then test rights decomposition, an enforcing institution, and a non-agent autonomous process;
7. build a second micro-world using the same semantic and mechanical contracts.

This sequence still establishes one trusted reference mechanic before asking agents to extend the system. It does not postpone the project's central hypothesis until after most foundational choices have been made.

## Suggested mechanics-agent artifact

For one missing mechanic, an agent should produce a reviewable package containing:

| Part | Required content |
| --- | --- |
| Semantic binding | Linguistic Core sense(s), roles, specialization, and classification |
| Causal bearer | Agent action, autonomous process, disposition, institution, or exogenous injection |
| Applicability | Required components/relations, optional modifiers, explicit incompatibilities |
| Authority | Declared reads, writes, emitted observations/events, and scheduling behavior |
| Effects | Proposed state changes; no direct mutation during validation |
| Invariants | Goal-relative accounting and referential rules |
| Dependency closure | Other mechanics and state surfaces believed consequential |
| Interaction cases | Positive, refusal, boundary, interference, and double-application tests |
| Limits | Unsupported interactions, approximation, and refinement conditions |
| Trace contract | What a builder can inspect when it applies, refuses, or fails |

The installer should validate and freeze this package into a world profile before the simulation. Runtime invention or revision of laws was deferred here; [Decision 007](../decisions/007-any-scenario-path.md) (2026-10-07) reverses that: a game master may write checked rules mid-run, reviewed after the run.

## Decisions and open questions added by this review

### Strong recommendations

- Use V3's canonical intent/patch/commit boundary as a design donor, not its current contract inventory.
- Use V2's local bounded-authority principle to constrain mechanics and mechanics agents.
- Make Linguistic Core the semantic compiler interface that V3 currently lacks.
- Treat causal closure as the primary mechanics-integration assay.
- Keep agent cognition resident and private; expose only observation and action interfaces to the substrate.
- Preserve explanatory evidence while rejecting replay-driven architecture.

### Still open

- What is the smallest declarative mechanics language that can express `give`, containment, damage, resource transformation, sensing, and an installed institution without adding a new compiler branch per family?
- How should Linguistic Core classify a predicate whose causal status varies by world—for example, voluntary exchange versus escrow-enforced exchange?
- Which persistent-state relations should come from SUMO, Wikidata, QUDT, or a curated state pack?
- How should mechanics declare cross-mechanic precedence, simultaneous-write conflict, capability revocation, and entity replacement?
- What evidence is sufficient to freeze an agent-authored mechanic profile for an exploratory run?

## Bottom line

Cybernetic Influence V3 does not remove the need for World Substrate. It provides a disciplined partial answer to a narrower question: how can open agent intent be placed behind a canonical state-transition boundary and later analyzed without giving prose direct causal force?

Its unresolved answer is the core of World Substrate:

> How do a broad semantic vocabulary, persistent state, reusable local mechanics, and agent-authored extensions compose into a coherent world without hand-writing a new runtime path for every domain?

The most promising synthesis is Linguistic Core for semantic normalization, V2/V3-style local transition authority for causation, Data Contracts-style governed installation, Collective Competence's anti-double-counting rule, and a pre-run mechanics-agent workflow whose main acceptance test is causal closure under adjacent interactions.
