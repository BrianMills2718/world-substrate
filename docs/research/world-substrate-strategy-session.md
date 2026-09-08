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

# World Substrate Theory and Strategy — Working Memo

**Status:** Living discussion document; not yet repository authority  
**Last updated:** 2026-09-02  
**Purpose:** Preserve the project's evolving theory, decisions, hypotheses, requirements, risks, and open questions before changing the World Substrate repository.

**Follow-on research:** [Competitive landscape — generative agents, social simulation, and governed worlds](competitive-landscape-2026-09.md) compares the project's causal-authoring layer with adjacent systems. Subsequent accepted procurement is recorded in [technology procurement](technology-procurement-2026-09.md), and the current visual product target is recorded in [living-world projection](living-world-projection-2026-09.md). This memo remains historical/non-authoritative.

## 1. Product thesis

World Substrate is intended to support persistent worlds in which agents and non-agent processes have causal effects. Its vocabulary should draw heavily from existing linguistic and ontological resources, while executable mechanics should be added only where a selected world needs them.

The project should not attempt to implement one bespoke mechanic for every linguistic predicate or every combination of predicates. A predicate supplies a way to describe something; it does not by itself establish that the thing is an executable primitive. The central design problem is to bind a relatively small set of causal primitives and world processes to a much larger semantic vocabulary, then let higher-order patterns be composed or observed.

A promising long-term hypothesis is that LLM-agent teams can inspect a desired world, identify missing mechanics, author and test them, and produce a frozen mechanics profile for a simulation run. Runtime invention of mechanics is a separate, later problem and is not required to test the core thesis.

## 2. Current decisions and strong directions

### Confirmed requirements

- **Observability is a core product requirement.** It must be possible to inspect what an agent perceived, what it attempted, which causal rule or process applied, what state changed, and why an attempted action failed.
- **Persistence is fundamental.** Actions occur in and alter an actual world state that survives across steps. Agents, objects, processes, and the consequences of prior actions remain part of that world until mechanics change them.
- **Existing ontologies and vocabularies should be adopted before new taxonomies are invented.** Linguistic Core, SUMO and its sources, FrameNet, PropBank, Wikidata properties, QUDT, and other appropriate donors should be audited before defining a new event or process classification.
- **Linguistic predicates are not automatically engine actions.** Some describe primitive actions; others describe composites, plans, states, processes, institutions, or analytic interpretations.
- **Only representations with independent causal force should directly write canonical state.** Composite and emergent descriptions should ordinarily be derived from primitive events rather than implemented again as separate causal mechanisms.
- **One enclosing transition owns each causally coupled commit.** Applicability rules, contracts, and mechanics may inspect state and propose effects, but they must not independently commit effects that belong to an action or process which may still fail.
- **Universal conservation of mass or energy is not a product requirement.** A world or mechanic should enforce only the accounting invariants that matter to the purpose and abstraction level of that simulation.

### Explicit non-goals

- Exact reproducibility of a run
- Deterministic execution
- Bit-for-bit replay as a promotion gate
- Reconstructing the entire world from an event log
- Comprehensive real-world physics
- Making every Linguistic Core predicate executable
- Defining all possible mechanics before constructing a world

Randomness, LLM nondeterminism, and stochastic agent decisions are acceptable. Snapshots and traces may be useful for inspection and debugging, but they must not silently turn exact replay into a product requirement.

### Strong provisional directions

- Begin with agent-assisted, **pre-run** expansion of a small world. Freeze the selected mechanics for the actual simulation run.
- Treat between-run, gap-driven enrichment as a later extension.
- Defer runtime installation or revision of underlying world laws. Prospective installation, retroactive correction, branching, and law-version semantics are later research topics, not early architecture requirements.
- Use a small interaction surface and grow it through observed needs rather than attempting broad semantic coverage.
- Distinguish four causal layers: substrate physics, installed world institutions, resident-agent cognition, and non-causal analytic interpretation.

## 3. Semantic descriptions versus causal mechanics

The system needs an explicit boundary between describing an occurrence and causing a state transition.

| Semantic/mechanical role | Meaning | Example | Writes canonical state? |
| --- | --- | --- | --- |
| Primitive intentional action | An action an agent can independently attempt | `give(Robin, spear, Friday)` | Yes, through its bound mechanic |
| Autonomous or environmental process | A world process not selected as an agent action | Fire consumes available fuel | Yes |
| State relation | A fact holding over some interval | Friday possesses the spear | The underlying relation is state; mechanics may change it |
| Composite event | A pattern made from multiple events | Two reciprocal gives described as an exchange | Normally no |
| Analytic or emergent pattern | An interpretation of histories or structures | Cooperation, trust, collective competence | Normally no |
| Plan, intention, or declaration | A commitment or desired future action | Robin proposes an exchange | No direct transfer; it may affect agent policy or communication state |
| Institutionally enforced transition | A rule, registry, court, contract, or ledger with causal power | Escrow atomically releases two assets | Yes, if the institution exists in the world |

This classification should be a binding layer over donor vocabulary, not a replacement ontology. A Linguistic Core `exchange` or `barter` sense can remain useful for language understanding and historical analysis even when the engine exposes only `give` as the relevant primitive.

### The causal-force test

Before implementing a named phenomenon as a mechanic, ask:

> If all lower-level events were held fixed and this named phenomenon were removed, would the world's subsequent state transitions or action affordances change?

- If **no**, it is probably a derived description and should not become another state-writing mechanic.
- If **yes**, identify the actual causal bearer: an agent policy, physical disposition, contract, registry, enforcement institution, material property, or other mechanism.

This is the anti-double-counting rule. It imports a central lesson from Collective Competence: mechanism, capability, observed dynamic, and achieved outcome are different claim roles. An outcome or emergent pattern must not be inserted back into the model as an additional mechanism merely because it has a convenient name.

## 4. Exchange as a worked social example

In the ordinary initial world, exchange should not be a primitive atomic action.

1. Robin can communicate a proposal or form an intention to exchange.
2. Robin independently attempts `give(Robin, spear, Friday)`.
3. Friday observes whatever the world makes observable and independently decides whether to attempt `give(Friday, coconuts, Robin)`.
4. Friday may reciprocate, delay, fail, or renege.
5. An observer or analytic layer may classify the two transfers and their context as an `exchange`.

Declaring participation in an exchange may map a participant role to a planned `give`, but it does not manufacture the other participant's action. This preserves agency and permits the bad-but-real intermediate outcome in which Robin has transferred the spear and Friday does not transfer the coconuts.

An escrow contract or smart contract changes the analysis. It has independent causal force: it can hold assets, test conditions, and release or return them. In that world, an atomic or conditionally coupled exchange mechanic may be warranted. The causal primitive is the contract's enforcement behavior, not the abstract word *exchange*.

The same rule applies to trust, cooperation, organization, status, and collective competence. They may first be measurements or interpretations of primitive histories. They become substrate mechanics only when a represented bearer gives them causal effects—for example, a registry makes status alter permissions, or an agent's memory-derived trust assessment changes its action selection.

## 5. Why global coherence is hard

Global coherence is not primarily the problem of writing individually plausible equations. It is the problem of ensuring that mechanics share the same meaning of state, order their effects consistently, and do not each claim authority over the same occurrence.

### Concrete physical example: a sealed clay pot over a fire

Suppose five mechanics pass their standalone tests:

- heat raises the temperature of a pot and its contents;
- water can vaporize;
- vapor raises pressure inside a sealed container;
- pressure above material strength damages or ruptures the pot;
- fluid flows through an opening.

They can still fail together in several concrete ways:

1. **Duplicated water.** The vaporization rule creates 100 ml-equivalent of vapor but fails to subtract the corresponding liquid. Each local rule looks plausible, but the combined state now contains both the original water and its vapor.
2. **Stale enclosure state.** At the start of a step, the pressure rule sees `sealed = true`. During the same step, damage creates a crack. The flow rule sees the crack, but the pressure rule continues accumulating pressure because mechanics disagree about when enclosure state changes become visible.
3. **Two owners of leakage.** Rupture removes water from the container and creates a puddle. Fluid flow also sees the new opening and removes the same water into a second puddle. The same causal occurrence is implemented twice.
4. **A broken container that still contains.** The damage mechanic marks the pot `broken`, but nothing revokes its container capability. It therefore continues to hold contents and build pressure while simultaneously leaking.
5. **Contradictory thresholds.** The material-strength rule compares pressure in kilopascals with a strength value authored in pascals, so the pot never ruptures—or ruptures immediately.
6. **Lost causal attachment.** The pot becomes fragments, but heat and contents remain attached to the now-nonexistent intact pot because no mechanic owns the handoff of those relations.

No individual rule necessarily contains an absurd equation. The incoherence arises at their boundaries: units, update timing, shared state ownership, capability revocation, identity, and double application.

### Concrete social example: double-counting an exchange

Suppose `give` changes possession, an `exchange` mechanic separately transfers both assets, and a registry mechanic also changes legal ownership when it observes the exchange. One real sequence can then be applied two or three times. The model may duplicate assets, transfer an asset back accidentally, or infer cooperation as a cause after cooperation was already the label assigned to the outcome.

The remedy is not to author every possible interaction in advance. It is to give each mechanic an explicit boundary, declare which state it may read and write, and make composite phenomena derived unless they introduce a new causal bearer.

### Concrete implementation example from Agent Ecology 2 and 3

AE3's priced-artifact read is a legitimate institutionally enforced transaction: the kernel authorizes the read, transfers scrip to the artifact's rights holder, and returns the content. Unlike ordinary barter, this coupling has causal force because the platform enforces it.

The implementations also illustrate a coherence hazard. An executable access contract may return `state_updates`; the permission path immediately writes them into the artifact's authorization state. The calling action may subsequently fail because the reader cannot afford the price, argument or interface validation fails, execution fails, or another downstream condition is not met. Contract state can therefore change even though the transaction never completed.

AE2 makes the boundary failure especially clear. Its permission checker mutates artifact state during authorization. Top-level invocation validates the requested method afterward. Nested invocation can perform a general permission check and then a second contract check, potentially evaluating or applying effects twice. Its nested payment path selects a beneficiary from artifact authorization state even though the accepted ADR says the contract's returned recipient is authoritative. Individually plausible subsystems therefore disagree about when effects become real and which representation owns payment authority.

This is not a demand for universal ACID machinery. It is evidence for a narrower rule: validation and proposed effects should remain provisional until the complete causally coupled transition succeeds. A permission check should not independently commit state that belongs to the enclosing action.

## 6. Mechanic component and interaction contracts

A globally closed component schema—“required, optional, and everything else forbidden”—would make composition brittle. An entity must be allowed to carry components that are irrelevant to a particular mechanic.

The better rule is:

> The world is open to additional components, but each mechanic has a closed authority boundary.

A mechanic contract should be able to declare:

| Field | Purpose |
| --- | --- |
| `requires` | Components, relations, or conditions that must exist for applicability |
| `optional_modifiers` | Recognized properties that alter behavior when present |
| `forbids` | Explicit incompatible conditions, used only where absence matters |
| `reads` | State paths the mechanic is permitted to inspect |
| `writes` | State paths the mechanic is permitted to mutate |
| `emits` | Observable events, facts, or diagnostic traces it may produce |
| `invariants` | Local accounting or validity conditions the transition must preserve |
| `unsupported_interactions` | Known combinations for which the mechanic should refuse or warn rather than guess |

Anything outside the contract is not forbidden from existing on the entity; it is outside that mechanic's authority. For example, a heat mechanic may ignore ownership and color. It should not be allowed to mutate either merely because they are present.

Required and optional component declarations are therefore useful, but insufficient by themselves. Read/write authority and explicit incompatibilities are more important for preventing mechanics from silently colliding.

This shape is compatible with ideas already present in Data Contracts: applicability, candidate binding, proposed transitions, guards, and governed application. It also resembles the capability contract in Collective Competence and the boundary/dependency/acceptance structure of Company Planning work units.

## 7. Invariants without universal physics

Full conservation of mass and energy should not be imposed on every simulation. It is expensive, may be meaningless at a coarse abstraction, and could distort the product around a goal it does not have.

Use **goal-relative accounting invariants** instead:

- If possession and scarcity matter, an object should not be simultaneously possessed by two agents unless shared possession is explicitly modeled.
- If inventory matters, transfers should not create negative inventory or duplicate a unique item.
- If resource competition matters, declared sources and sinks should balance at the chosen abstraction level.
- If fluid quantities materially affect outcomes, a water mechanic may conserve modeled water or name explicit creation/loss boundaries.
- If energy flows are not represented, energy conservation is not a useful validation condition.

The relevant question is not “Does this world satisfy all real physics?” It is “Which invariants must hold for this world's intended conclusions and agent affordances to remain meaningful?”

## 8. The role of LLM mechanics agents

LLMs can be the default authors of missing mechanics. The user should not be expected to supply equations, and every mechanic does not require a human subject-matter expert.

Agents may retrieve existing equations, libraries, ontologies, and documented models when that is useful; select a suitable resolution; adapt them; or propose a deliberately simplified rule. Real-world empirical validation is outside the current product goal and does not need to be repeated as a generic disclaimer. The engineering concern is whether independently authored mechanics integrate coherently inside the selected world.

An early mechanics-authoring output should therefore include a lightweight evidence package:

- the intended behavior and abstraction level;
- modeling assumptions;
- required inputs, outputs, reads, and writes;
- units or value types where quantities matter;
- a few behavioral examples and boundary cases;
- known unsupported interactions;
- observable traces explaining application or refusal.

Source retrieval should be proportional to consequence. It may be worthwhile for a central pressure or disease model and unnecessary for a fictional door-opening rule. The purpose of the package is to expose assumptions and integration risks, not to demand scientific reproducibility.

### Central research hypothesis

> Can an LLM-agent team grow the set of useful mechanics faster than the integration and interaction burden grows, for bounded target worlds?

If the answer is partially negative, the consequence is not merely slower simulation runtime. Mechanics construction, integration testing, and coherence repair may dominate world-building cost; some requested actions may remain unavailable; and adding coverage could make existing behavior less trustworthy. This is still testable. It argues for measuring authoring throughput, interaction defects, and unsupported action demand—not for abandoning incremental mechanics.

## 9. Observability contract

The engine should optimize for an intelligible causal trace, not a replay proof. For an important transition, an observer should be able to inspect:

- relevant state before and after the transition;
- the triggering action, condition, or process;
- the agent's available observation and submitted action;
- the semantic predicate and roles, if used;
- the mechanic or process binding selected;
- applicability checks and reasons for rejection;
- declared reads and actual writes;
- invariant checks and warnings;
- unsupported interaction notices;
- the resulting state changes and emitted events.

Stable IDs and mechanic versions can make a trace interpretable without promising that the same run can be reproduced. Snapshots can support debugging and analysis without becoming an event-sourcing mandate.

## 10. Candidate thin vertical slices

The earlier pre-run/between-run/runtime sequence describes capability maturity, but it is not by itself the best product slicing. Each early slice should exercise a complete path from semantic description through causal execution to observable persistent consequences, while answering one major design question.

The following is a candidate sequence, not an accepted roadmap.

### Slice 0 — Semantic and causal audit of one micro-world

Choose a tiny scenario. Map its desired entities, state relations, quantities, action predicates, roles, and processes to the actual Linguistic Core/OntoCanon assets and donors. Classify each predicate as primitive, state, process, composite, analytic pattern, or institutional transition. Record gaps without trying to close the whole ontology.

**Question answered:** What does Linguistic Core already supply, and what additional binding or state vocabulary is actually missing?

### Slice 1 — One primitive action in a persistent world

Implement or expose `give` end to end: agent intent, role binding, applicability, transition of possession, failure reasons, persistence, and causal trace. Reuse a real Linguistic Core sense rather than minting a synonym.

**Question answered:** Can semantic roles bind cleanly to a minimal executable mechanic and persistent state?

### Slice 2 — Independent reciprocity and a derived composite

Run two agents. Robin gives a spear; Friday may or may not give coconuts. Recognize a successful pair of gives as an exchange analytically, without making the label perform either transfer.

**Question answered:** Can the substrate preserve independent agency while higher-level semantic descriptions emerge from primitive histories?

### Slice 3 — Agent-authored missing mechanic before a run

Give a mechanics agent one deliberately unsupported, bounded capability adjacent to `give`. Have it select donor vocabulary, declare applicability and effect authority, author positive and refusal tests, install the mechanic into a world profile, and then freeze that profile for the simulation.

**Question answered:** Can agents close a real mechanics gap through the same generic transition envelope used by the hand-built reference mechanic?

### Slice 4 — Causal-closure and adjacent-mechanics assay

Combine the hand-built and agent-authored mechanics. Search the semantic world for consequential state that neither mechanic reads, inspect overlapping writes, and test one intentionally difficult interaction. Add explicit precedence, refusal, or warning behavior where the interaction is unsupported.

**Question answered:** Can the project detect undeclared dependencies and integration failures early enough for agent-authored mechanics to remain trustworthy?

### Slice 5 — Rights decomposition for one asset

For the spear, distinguish only the relations the scenario needs: provenance, physical possession, permission to use or modify, economic beneficiary, and authority to transfer. Do not create a universal legal ontology. Make the distinctions explicit enough that no mechanic can silently substitute creator, possessor, controller, or beneficiary for another.

**Question answered:** Can the substrate represent orthogonal state and authority relations without collapsing them into a generic `owner` or opaque metadata?

### Slice 6 — One installed institution and a singular commit boundary

Add one escrow-like institution that can hold or conditionally release assets. Deliberately exercise insufficient payment, invalid arguments, failed downstream execution, and cancellation. Authorization and institution logic may propose state effects, but the enclosing transition must commit coupled effects together or none of them.

**Question answered:** Can a represented institution acquire causal force without leaking provisional effects or overriding independent action outside its declared scope?

### Slice 7 — One non-agent causal process

Add one bounded process such as fire consuming fuel or a storm moving and affecting exposed objects. First audit donor ontologies for its classification. Use the same persistent-state, transition-authority, and observability contracts as intentional actions.

**Question answered:** Can intentional actions, autonomous processes, and installed institutions coexist under a common causal boundary without inventing a large new event taxonomy?

### Slice 8 — Second micro-world

Build a different small world using the same contracts. Measure what was reused, what had to be authored, and whether prior mechanics created hidden coupling.

**Question answered:** Is the architecture generalizing, or is it accumulating scenario-specific machinery?

### Deferred maturity capabilities

Only after these slices provide evidence should the project consider:

- gap-driven enrichment between simulation runs;
- mechanics-agent teams expanding larger game spaces;
- runtime construction or installation of mechanics;
- prospective versus retroactive law changes;
- corrected branches or historical reinterpretation.

### Alternative starting point

The existing World Substrate freshwater milestone is already an implemented vertical. The project need not rebuild from zero. The immediate sequence may instead be:

1. audit the existing freshwater slice against the theory in this memo;
2. add the independent `give`/derived-exchange slice;
3. run one pre-run mechanics-authoring experiment;
4. decide the next slice from observed gaps.

This uses the current repository as evidence while testing the social/emergent boundary that freshwater does not address.

## 11. Seeds from the existing projects

### Linguistic Core / OntoCanon

- Supplies a large predicate-and-role inventory and substantial PropBank/FrameNet sense alignment.
- Includes `give`, `exchange`, `barter`, and related senses, but semantic availability does not decide executability.
- Appears much stronger in event vocabulary than persistent state relations and quantitative value modeling.
- Likely needs complementary donors and a binding/classification layer rather than wholesale reinvention.
- Multi-pack composition or a compiled combined profile may be needed if state, quantity, and domain packs must coexist.

### Data Contracts

- Applicability, binding, reference resolution, proposed transitions, guards, governed application, and receipts are useful seeds for mechanics installation.
- Immutable ActionPacks may inform frozen per-run mechanics profiles.
- The observation-to-application lifecycle is relevant, but it should be simplified around World Substrate's actual needs rather than copied wholesale.

### Collective Competence

- Provides the strongest conceptual warning against double counting: mechanisms enable capabilities; capabilities permit dynamics; dynamics or outcomes are not automatically additional mechanisms.
- Its capability contract suggests explicit system boundary, inputs, transformations, outputs, operating conditions, resource bounds, failure semantics, and evidence.
- Social patterns should remain emergent unless a represented institution, policy, or artifact supplies independent causal force.

### Company Planning

- Work-unit fields—outcome, inputs, outputs, boundary rules, dependencies, acceptance evidence, integration surface, and non-scope—are promising for bounded mechanics-authoring tasks.
- The project may help structure agent work without dictating the substrate's ontology.

### Current World Substrate

- Already demonstrates a narrow end-to-end world slice and distinguishes actions from processes.
- Its emphasis on deterministic authority and exact replay should be reevaluated because those are not product goals.
- Its existing traces, snapshots, and receipts should be judged by how well they support observability, not exact reproduction.

### Agent Ecology 1

- Provides a compact deterministic counterexample harness: a hypergraph of agents, tools, actions, decisions, and role-bearing relations; private outcome memory; rate limits; and heuristic action selection.
- Its second world directly installs grudge memory and reciprocity refusal. The resulting feud dynamics demonstrate the consequences of that mechanic, not the emergence of reciprocity.
- The early reified relation-and-role representation is conceptually relevant to Linguistic Core binding, but the copied `world_v1.py`/`world_v2.py` authority surfaces and fixed policies should not be reused.

### Agent Ecology 2

- Articulates a directly relevant thesis: start with scarcity, costs, consequences, ownership/access primitives, and contracts; let specialization, cooperation, markets, and organizations emerge when useful.
- Its most useful distinction is between hardcoded **system physics** and represented, replaceable **institutions**. Combined with the agent boundary and causal-force test, this yields four layers: substrate physics, installed institutions, resident-agent cognition, and analytic interpretation.
- Its `artifact` plus `has_standing`, `has_loop`, `executable`, contract, and resource properties demonstrate orthogonal capabilities/attributes rather than a deep class for every entity combination. The intuition should be retained, but the Boolean taxonomy and universal artifact type should not replace Linguistic Core, explicit state relations, components, dispositions, or mechanic bindings.
- It gives a concrete model of institutions acquiring causal force: executable contracts and escrow can enforce access and coupled transfers, while voluntary agreements can still permit defection. The one-attached-access-contract pattern is not general enough for institutions governing territories, roles, classes, or multi-party situations.
- Its Ostrom exploration usefully decomposes `ownership` into rights. Its implementation history is a stronger warning: `created_by`, metadata controller, contract-governed writer/principal state, custody, and payment recipient repeatedly diverged. World mechanics must not conflate provenance, possession, access, control, legal title, beneficiary, or authority to transfer.
- Its ontology correctly states that labels should not cause kernel branching. The running system only partially honors that rule, which demonstrates how easily semantic classifications leak into causal authority.
- Its layered artifact discovery and interface descriptions are good seeds for mechanics discovery: an agent should be able to discover an affordance, inspect applicability and roles, and understand required inputs before attempting it.
- Its external-capability request flow is a useful seed for pre-run mechanics expansion: identify a missing capability, submit an explicit request, validate and authorize an implementation, install it into a profile, and observe its use through one generic boundary.
- It explicitly rejects deterministic behavior and research reproducibility as goals. Its useful logs should be evaluated as causal explanations, not replay proofs.
- It also demonstrates the danger of substrate breadth outgrowing a stable vertical. Its V1 gate established plumbing—multiple agents, artifacts, transfers, constraints, escrow, and logs—but did not establish emergent collective capability.
- Its agent/runtime APIs became conceptually confusing even to agents, especially the distinction between kernel action types and artifact invocation. Linguistic alignment and a single action boundary are therefore usability requirements, not cosmetic improvements.
- It contains competing current architectures: kernel-enforced `access_contract_id`, artifact-self-handled `handle_request`, and an implemented hybrid even though the design exploration rejected the hybrid. It should be treated as a design and failure corpus, not code to extract wholesale.
- Its current permission path independently confirms AE3's premature-effects defect and adds double-check and payment-authority inconsistencies. Selection pressure or reputation cannot repair canonical state corruption after the fact.

### Agent Ecology 3

- Is the clearest concrete reference for a narrow kernel pattern: persistent entities, a ledger, typed action intents, one action executor, contract-governed access, resource constraints, autonomous actors, and JSONL causal traces. This is a source of ideas and executable counterexamples, not a recommendation to adopt its code.
- Is not a donor for the general World Substrate ontology. Almost everything is an `Artifact` with an arbitrary `type`, opaque `content`, and untyped `metadata`. This works for an abstract information economy but cannot represent the semantic breadth of a physical and social world.
- Demonstrates the causal-force distinction. A paid artifact read is a platform-enforced transaction; a later analyst's description of reciprocal behavior is not another mechanic.
- Demonstrates goal-relative accounting. It preserves scrip and selected scarce-resource balances without pretending to implement mass or energy conservation.
- Provides valuable observability fields: submitted intent, result, error, decision origin, raw versus normalized decision, payments, resource use, and persistent consequences. World Substrate should adopt the explanatory content without importing AE3's exact-replay, evidence-custody, matched-seed, or no-rerun machinery.
- Currently violates the desired agent boundary. `World` owns role profiles, strategy prompts, memory/state/notebook scaffolding, action gates, fallbacks, provider branches, and parts of the agent lifecycle. World Substrate should let resident agent runtimes own cognition, memory, planning, skills, and recovery; the kernel should own world state, affordances, authorization, scheduling semantics, and committed transitions.
- Its current minimal-mode Plan 23 candidate is appropriately narrow: two agents produced a trace-grounded reciprocal read-create-buy chain. The result is a useful local example, not evidence for a general emergence claim.
- Its global execution lock makes world mutation serial and can make provider latency part of ecology timing. World Substrate does not need deterministic scheduling, but it still needs explicit concurrency semantics and an observable commit order.
- Its contract permission path exposes a real coherence risk because contract `state_updates` can commit before the enclosing paid read or invocation succeeds. World Substrate mechanics should propose effects and commit them together at the enclosing transition boundary.
- Agent-authored executable contracts are not yet an adequate sandbox for general agent-authored mechanics. The current contract path executes code with broad built-ins and lacks declared read/write authority. A mechanics authoring path needs stronger isolation and explicit effect boundaries.

### Cybernetic Influence V3

- Supplies the strongest transition-envelope donor so far: authorized actor context, open semantic intent, declared transition authority, structured proposed patch, generic and subsystem checks, and one canonical commit or refusal.
- Correctly separates scenario, run, and detachable analysis authority. The analyst's objective should not enter actor or world-transition prompts and thereby change the behavior being analyzed.
- Treats organizations and other macro-levels as derived reversible coarse-grainings unless a coarse surrogate explicitly replaces lower-level detail. This reinforces the anti-double-counting rule from Collective Competence.
- Separates spatial containment and adjacency from routing, operability, permission, perception, and successful traversal. The same orthogonality should govern possession, custody, access, control, title, beneficiary status, and transfer authority.
- Makes representation depth question-relative. Exact, stochastic, empirical, scripted, external, and LLM-mediated mechanics can implement the same typed interface at different fidelities if their omissions and invalid questions are declared.
- Identifies generated-configuration **causal closure** as a central unresolved problem. A locally valid cargo transfer may ignore modeled truck, fuel, berth, customs, or labor dependencies. Checking only declared dependencies cannot prove that the author declared everything consequential.
- Its present general path is not yet a general mechanics layer. Exact behavior is hard-coded around sensing, resource transformation, and resource transport; a new family requires new compiler and runner code.
- Its `SemanticActionIntent.action` is free text rather than a Linguistic Core sense-and-role binding. This preserves expressiveness but gives mechanics discovery no stable semantic key and leaves `target_refs` without a predicate signature.
- Its current joint LLM adjudicator receives the entire canonical world. Declared authority `reads` and `writes` are not enforced as state paths at commit; only broad operation and record-type grammar plus special exact-contract checks are enforced. World Substrate should prefer V2-style local authority and independently validated state-path scope.
- The Concordia decision is specific to that project's product lineage. The portable idea is that an agent framework may own cognition while a project-owned world component owns persistent truth and transitions; Concordia itself is not adopted by this memo.
- Its transition evidence is a strong observability donor. Its state hashes, strict checkpoint restoration, replay flags, and provider-receipt emphasis should not be imported as requirements.

### Cybernetic Influence V2

- Is a major idea donor rather than merely an obsolete implementation. Its clearest positive pattern is one bounded resolver or mechanism per attempted interface, with a local input, read, write, output, and effect envelope.
- Strongly separates persistent things, mechanisms, action attempts, proposed effects, accepted effects, and events. Possibility, technical reach, credentials, knowledge, normative permission, attempt, and success are distinct facts.
- Routes effects through explicit local structure rather than an omniscient semantic search. Wide effects require a declared subsystem with a visibly wider authority surface.
- Distinguishes carriers, encoded representations, delivery, interpretation, memory, and belief. These distinctions should be installed only when information mechanics matter to the selected world, not required everywhere.
- Its bespoke runtime, maximal causal tracing, recovery guarantees, and replay/evidence-custody machinery should not be adopted wholesale.

### Original Cybernetic Influence

- Provides a useful semantic complexity gate: a donor term becomes runtime ontology only if it changes what exists, what can be perceived, what can be attempted, or what the world does next. Otherwise it remains prompt semantics, scenario metadata, or analysis.
- Its distinctions among actual cause, received sign, interpreted object, hypothesis, suppressed alternatives, and resulting action can inform optional cognition and influence-analysis modules.
- The false-independence example—several apparent confirmations with one hidden source—is a useful provenance test without making belief canonical world truth.
- Its nine-field mediation bundle is too theory-specific to become a required resident-agent or world-kernel contract. Agent systems should remain free to choose their own cognition and memory architecture.
- Its early composed-entity model should be used only as an explicit coarse surrogate or an analytic projection, never as a duplicate executor alongside its members.

## 12. Gaps and open questions

### Semantic and ontological gaps

- Which state relations, attributes, quantities, and units are absent from the currently published Linguistic Core profile?
- Does the current pack expose a useful predicate specialization hierarchy, or mainly sense inventory and role signatures?
- Which donor should supply state relations: SUMO, Wikidata properties, another upper ontology, or a curated combination?
- How should multiple ontology packs be composed into one executable world profile?
- Which existing ontology best supplies the minimum distinctions among intentional action, autonomous process, disposition-triggered change, and institutional transition?
- How should Linguistic Core supply a stable sense-and-role key for mechanics lookup while allowing the same predicate to be primitive, composite, or institutionally enforced in different worlds?

### Mechanical gaps

- What is the minimum executable primitive set for the first target world?
- How are conflicting writes, update visibility, capability revocation, and identity transitions handled?
- When should unsupported interaction cause refusal, approximation, or a mechanics-authoring task?
- How are agent actions distinguished from the observations and interpretations later applied to them?
- What belongs to the resident agent runtime versus the world kernel, and how is that boundary kept singular?
- What scheduling semantics are required when agent deliberation is concurrent but world mutations contend?
- Which transitions require coupled commit semantics, and how do mechanics propose effects without independently mutating canonical state?
- When an institution or mechanic referenced as causal authority is missing, should the affected action refuse, degrade explicitly, or use a world-profile-defined fallback?
- What is the smallest declarative mechanics language that can add a new family without adding family-specific compiler and runner branches?
- How are declared mechanic read and write paths enforced independently of an LLM or executable implementation?
- How should causal-closure review discover consequential dependencies that the mechanic author failed to declare?

### Product and evaluation gaps

- What is the first target micro-world and what claims must it support?
- Which vertical-slice ordering produces the most learning from the existing codebase?
- How should mechanics-authoring throughput and interaction defects be measured?
- What level of physical or social fidelity matters for the product's intended uses?
- Which observability views are useful to world builders, mechanics agents, simulation analysts, and participating agents?

## 13. Risks and concerns

- **Semantic-mechanical conflation:** treating every named predicate as a causal primitive creates duplicate and contradictory mechanics.
- **Interaction explosion:** even a modest mechanic inventory can have a much larger space of meaningful combinations. The relevant burden is not literally factorial in every case because many mechanics never interact, but unconstrained all-to-all composition grows too quickly to test or reason about.
- **Hidden shared-state ownership:** independently authored rules may mutate the same facts without an explicit conflict.
- **False physical confidence:** an LLM may produce a plausible local model with inconsistent units, resolution, timing, or assumptions.
- **Ontology reinvention:** creating event-source taxonomies locally may duplicate mature donor work and make later integration harder.
- **Premature runtime expansion:** solving changing laws during a run could consume the project before offline agent-authored mechanics are validated.
- **Replay-driven complexity:** preserving deterministic reconstruction could distort IDs, scheduling, logging, storage, and promotion criteria without serving a product requirement.
- **Analytics leaking into causation:** detected exchange, trust, cooperation, or competence may accidentally be applied again as causal state transitions.
- **Cognition leaking into the kernel:** substrate-owned prompts, memory, planning, and recovery can make measured behavior an artifact of the wrapper rather than of resident agents.
- **Premature effects during validation:** permission or applicability checks may mutate state even when the enclosing action later fails.
- **Authority collapse:** provenance, possession, access, control, title, beneficiary, and transfer authority may be hidden behind one `owner` field or opaque metadata.
- **Silent institutional fallback:** replacing a missing contract or mechanic with permissive defaults can change world law and rights while preserving apparent liveness.
- **Declared-closure false confidence:** a compiler may prove that all *named* dependencies are bound while the semantic world contains consequential dependencies the author never named.
- **Omniscient adjudicator:** one broad LLM authority with full-world context can silently become the actual physics, permissions system, and social theory despite typed patch output.
- **Hard-coded mechanics families:** adding one compiler and runner path per mechanic family can recreate the predicate-by-predicate authoring burden beneath a nominal registry.

## 14. Decisions still pending

- The exact order and acceptance criteria of the thin vertical slices
- The first social and non-agent scenarios after the existing freshwater work
- The minimum semantic-to-mechanical classification vocabulary
- The donor ontology or ontologies for persistent state and causal categories
- The mechanics profile/pack composition architecture
- The threshold for requiring external models versus accepting a declared LLM-authored simplification
- The minimum observability record and user-facing inspection interface
- Whether legal ownership, possession, memory, belief, intention, and communication belong in the initial world profile
- The concurrency boundary between agent deliberation and committed world mutation
- Which narrow Agent Ecology ideas survive World Substrate's own ontology and transition design. The default is reference and reimplementation, not code extraction; any code reuse would need a later pattern-specific justification.
- Whether V2-style one-authority-per-interface or a more general mechanics dispatcher is the primary runtime selection model. The default recommendation is local authority, not one joint world adjudicator.

## 15. Recommended next work before repository changes

1. Treat this memo as the current discussion ledger and mark each proposition as decided, provisional, hypothetical, or open as the conversation continues.
2. Audit the actual Linguistic Core/OntoCanon artifacts for the selected micro-world rather than reasoning from inventory counts alone.
3. Inspect the additional institutional-transition repositories before defining institutional mechanics.
4. Compare existing ontology donors for causal categories instead of adopting the provisional taxonomy in earlier discussion.
5. Review the existing World Substrate freshwater implementation specifically for observability, shared-state authority, and replay-driven complexity.
6. Specify the singular transition envelope before agent-authored mechanics: semantic binding, applicability, proposed effects, resource checks, invariant checks, commit, and causal trace.
7. Make state-path-scoped local authority and a causal-closure assay part of that envelope; broad typed JSON output is not a sufficient authority boundary.
8. Select the next vertical slice only after that audit; the independent-give/derived-exchange scenario remains the leading candidate, followed immediately by one offline mechanics-agent extension and its interaction assay.

## 16. Working change log

### 2026-09-02

- Elevated Linguistic Core from a supporting vocabulary to a central semantic substrate.
- Clarified that its semantic coverage does not remove the need for mechanical bindings.
- Separated offline mechanics expansion from later runtime law mutation.
- Established that exchange is normally a derived pattern of independent gives, unless an enforcing institution adds causal force.
- Added the causal-force test and anti-double-counting rule.
- Made observability a core requirement.
- Explicitly rejected determinism and exact reproducibility as product goals.
- Replaced universal mass/energy conservation with goal-relative accounting invariants.
- Added mechanic authority contracts and a concrete global-coherence failure example.
- Recast the version roadmap as candidate thin vertical learning slices rather than a fixed V1/V2/V3 sequence.
- Removed the unnecessary generic warning about treating simulation output as real-world empirical validation.
- Reviewed the Agent Ecology lineage and identified AE3 as a kernel/observability donor but not a general semantic-world model.
- Added a concrete AE3 coherence failure: contract state can mutate before the enclosing action successfully commits.
- Clarified that resident agent runtimes should own cognition while the substrate owns causal world transitions.
- Completed a deeper Agent Ecology 2 review and identified its physics/institution distinction as its strongest positive contribution.
- Added a four-layer causal model: substrate physics, installed institutions, resident cognition, and analytic interpretation.
- Added AE2's rights-history warning: creator, possessor, controller, beneficiary, and transfer authority must not be conflated.
- Confirmed the premature-effects defect in AE2 and identified double permission evaluation and inconsistent payment authority in nested invocation.
- Reordered the candidate learning slices so rights decomposition, institutional causal force, and singular commit integrity are tested before open-ended mechanics authoring.
- Clarified that the Agent Ecology repositories are idea, design-test, and failure-example donors. No code adoption or extraction is proposed by default.
- Reviewed the Cybernetic Influence lineage and identified V3 as a major transition-envelope, analysis-isolation, and causal-closure donor rather than a general semantic or mechanics implementation.
- Promoted V2's one-bounded-authority-per-interface model over V3's current full-world joint LLM adjudicator for mechanics locality.
- Confirmed that V3's open action strings do not replace Linguistic Core sense and role binding.
- Added the relief-port dependency example: a locally valid cargo transfer can remain globally incoherent when truck, fuel, berth, customs, or labor are modeled but unenforced.
- Distinguished declared-dependency coverage from actual causal closure.
- Moved the first offline mechanics-agent experiment and its adjacent-interaction assay earlier in the candidate slice sequence.
- Preserved the original Cybernetic Influence translation and perception ideas while rejecting its mediation bundle as a required substrate or agent schema.
