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

# Agent Ecology 2 — Targeted Review for World Substrate

**Status:** Working architectural review  
**Repository reviewed:** `BrianMills2718/agent_ecology2`, default branch at `c285cae8cdd30a47269acc467eb9073467e99231`  
**Review date:** 2026-09-02  
**Purpose:** Determine which Agent Ecology 2 ideas should inform World Substrate, which need adaptation, and which are warnings rather than donors.

## Executive conclusion

A deeper review was worthwhile. Agent Ecology 2 is more relevant than Agent Ecology 3 to World Substrate's theory. AE3 is a cleaner executable reference and counterexample corpus, but neither repository should be treated as a code donor by default.

AE2's most valuable idea is not “everything is an artifact.” It is the distinction between:

1. **system physics** that the running world enforces;
2. **installed institutions** that are represented in the world and can acquire causal force;
3. **agent cognition** that should remain owned by resident agents; and
4. **analytic descriptions** that interpret histories without writing world state.

AE2 also provides a strong negative result. Local mechanisms can each look reasonable while the complete transition is incoherent. Its current permission system claims that contract state updates are atomic, but applies them during permission checking, before the enclosing action has validated or succeeded. It simultaneously contains kernel-enforced and artifact-self-enforced authorization paths, multiple pricing authorities, and historically inconsistent meanings of creator, controller, access authority, and beneficiary. This is a concrete example of the global-coherence problem World Substrate needs to solve.

The right disposition is therefore:

- adopt AE2's physics/institution distinction, orthogonal capability intuition, semantic interface/discovery ideas, and observability orientation;
- adapt its contract model into a general proposed-transition/commit boundary;
- reject “everything is an artifact” as World Substrate's general ontology and reject advisory string types as its semantic layer;
- keep agent cognition outside the substrate even if its state is compositional and persistent;
- use AE2's implementation conflicts as test cases for World Substrate's mechanic-authoring and integration contracts;
- reimplement any selected pattern against World Substrate's own semantic, causal-authority, and transition contracts rather than extracting Agent Ecology code.

## 1. How to read AE2

AE2 is not one settled architecture. It contains at least four evidence classes:

| Evidence class | Examples | How this review treats it |
| --- | --- | --- |
| Current implementation | `src/world/*`, `docs/ONTOLOGY.yaml`, current architecture docs | Evidence of actual semantics and defects |
| Accepted decisions | ADRs | Intended constraints, subject to later supersession |
| Target architecture | `docs/architecture/target/*` | Design hypotheses, not proof of implementation |
| Drafts, explorations, and completed plans | domain models, explorations, plan records | Rationale and history; often mutually inconsistent |

This distinction matters. For example:

- ADR-0019 says the kernel checks every artifact operation through `access_contract_id`.
- The later access-control exploration and ADR-0024 select artifact self-handled authorization and reject a hybrid.
- The current executor nevertheless supports both, selecting a path by searching artifact code for `def handle_request(`.

The repository is therefore useful as an architectural laboratory, not as a single specification to copy.

## 2. AE2's real architectural contribution

### 2.1 System physics versus installed institutions

The target architecture distinguishes hardcoded system mechanisms from replaceable “genesis” infrastructure. Although the genesis design was later removed, the distinction is durable:

| Layer | Causal status | World Substrate interpretation |
| --- | --- | --- |
| System physics | Unaddressable enforcement boundary | Persistent state, identity, resource accounting, scheduling/commit semantics, authorized effect application |
| Installed institution | Addressable and potentially replaceable | Contract, registry, court, escrow, norm-enforcement system, title system |
| Agent cognition | Produces intentions and actions | Resident runtime's memory, beliefs, goals, planning, strategy, skills |
| Analytic interpretation | Describes state or history | Exchange, cooperation, trust, organization, collective competence unless a represented bearer makes it causal |

This is a better starting model than “primitive versus composite” alone. It explains how a concept can change categories. An exchange is normally a derived description of two independent gives. An escrow institution can instead enforce a coupled transfer. The word does not create causal force; the installed institution does.

AE2 later collapsed many genesis services into an eleven-action kernel. That history is also instructive: moving a mechanism into the kernel is not neutral simplification. It grants the mechanism universal, privileged causal status. World Substrate should require an explicit justification whenever a mechanism crosses that boundary.

### 2.2 Labels should not create mechanics

AE2's ontology says labels are conceptual and the kernel should not branch on them. This aligns closely with the role of Linguistic Core: a semantic classification should not automatically become an executable rule.

The current implementation does not fully honor that aspiration. It still branches on local types such as `config`, uses `kernel_protected`, and recognizes executable behavior through flags and source-code signatures. The principle is useful; the implementation shows how easily semantic labels leak into causal control flow.

### 2.3 Orthogonal properties, not a class explosion

`has_standing`, `has_loop`, and `executable` are useful evidence for the user's attributes intuition. They let one entity independently have capacities such as holding value, being scheduled, or being invokable.

However, three booleans are not a general attribute model. Their meanings drift:

- `has_loop` sometimes means runnable code and elsewhere means autonomous scheduling;
- an agent artifact can have `has_loop=True` while `executable=False`, because a special runtime executes it;
- `agent = has_standing and has_loop` is a local operational definition, not an ontological account of agency.

World Substrate should preserve the orthogonality but model it through explicit types, components, capabilities, dispositions, and mechanic bindings grounded in Linguistic Core and complementary donors. It should not inherit AE2's universal artifact type or Boolean taxonomy.

## 3. What AE2 says about primitives, composites, and emergence

AE2's narrow action waist is infrastructure-specific:

- artifact read/write/edit/delete;
- invocation;
- scrip transfer and privileged minting;
- kernel query;
- subscription and unsubscription;
- several submission and configuration actions.

This is not a candidate universal action vocabulary for World Substrate. It is an API for a persistent information economy. It contains no semantic roles for physical actions such as giving, carrying, breaking, heating, enclosing, or moving.

It nevertheless demonstrates three relevant principles:

1. **A small causal waist can support many higher-level patterns.** Escrow, firms, markets, memory services, and auctions can be composed above storage, invocation, standing, and transfer.
2. **Composition requires genuine enabling primitives.** Plan 312 records that agents could not build escrow because artifacts could not acquire standing, transfer was not exposed, and nested invocation was broken. Telling agents to “build institutions” was meaningless until those causal affordances existed end to end.
3. **Installed primitives are not evidence of emergent behavior.** The simulation records correctly diagnose that hardcoded cooperation tasks, cognitively identical agents, self-contained goals, and non-binding scarcity did not produce meaningful cooperation.

This supports a sharper World Substrate hypothesis:

> A mechanics agent can close a semantic affordance gap only when the substrate already supplies a safe meta-mechanism for declaring applicability, reading state, proposing effects, validating invariants, committing changes, and exposing the new affordance to resident agents.

The mechanics agent does not escape mechanics. It uses a smaller, more general authoring and installation mechanism.

## 4. Contracts, rights, and institutions

### 4.1 The useful seed

AE2 treats contracts as executable entities that can answer permission questions, charge for access, keep state, and sometimes govern themselves. This is a strong example of an abstraction acquiring independent causal force. A contract is not merely an analyst's description: the platform consults it and enforces its result.

The Ostrom mapping is especially helpful because it decomposes “ownership” into access, withdrawal, management, exclusion, and alienation. This is a better direction than a single owner field.

### 4.2 The ownership lesson is a warning

AE2 repeatedly conflated or disconnected distinct relations:

| Relation | AE2 representation at different points |
| --- | --- |
| Creator/provenance | immutable `created_by` |
| Authorization/controller | creator checks, metadata `controller`, later `state.writer` or `state.principal` |
| Access policy | legacy `policy`, `access_contract_id`, or artifact `handle_request` |
| Economic beneficiary | artifact state, contract `scrip_recipient`, or historical creator routing |
| Possession/custody | ledger balance or escrow-internal records |
| Alienation | editing metadata, editing authorization state, or escrow protocol |

ADR-0028 eventually states the correct principle: `created_by` is historical and must not decide access or payment. But completed Plan 254 still says ownership transfer is an edit to metadata, while later documents say metadata is forgeable and authorization must live in contract-governed state. This is not merely stale terminology. It shows that a generic word such as “ownership” hid several causal relations with different transition rules.

World Substrate should model at least these separately when they matter:

- creation/provenance;
- physical possession or custody;
- use/access rights;
- control or authority to modify;
- legal title/ownership;
- economic beneficiary;
- authority to transfer each of the above.

Not every initial world needs all seven. But no mechanic should silently substitute one for another.

### 4.3 One contract per artifact is too narrow

`access_contract_id` is an elegant local permission pattern, but not a general institution model. Real or fictional institutions may govern:

- a class of entities;
- a territory;
- a role relationship;
- a transaction type;
- a registry namespace;
- a temporally scoped situation;
- several participants and assets together.

World Substrate can reuse the idea that represented rules may be executable and stateful, but it should not make “one attached access contract” the universal shape of institutional causation.

## 5. The concrete coherence failure

AE2's source provides a precise example of individually plausible mechanisms failing as a system.

The intended sequence is conceptually:

1. evaluate permission and proposed contract-state effects;
2. validate the requested operation and its arguments;
3. verify resources and payment authority;
4. execute the operation;
5. atomically commit the operation, payment, and contract-state changes.

The implemented sequence is different:

- `check_permission_via_contract` immediately merges `PermissionResult.state_updates` into the target artifact;
- top-level invocation then performs interface and argument validation;
- paid paths check affordability or perform execution later;
- nested invocation performs a general permission check and then a second contract permission check, which can evaluate or apply state changes twice;
- the nested path derives the recipient from `state.writer` or `state.principal`, even though ADR-0028 says the contract's `scrip_recipient` is authoritative;
- top-level reads retain a legacy `policy.read_price` while contract results independently carry `scrip_cost` and recipient fields.

Consequences include:

- authority can transfer although the requested action fails;
- counters or quotas can advance twice for one attempted nested call;
- a price can be calculated by one authority and paid to a beneficiary selected by another;
- permission, validation, payment, and mutation do not share one commit boundary;
- the trace may describe a failed operation while persistent authorization state has changed.

This is the global-coherence problem in miniature. Every local object has a plausible job—permission checker, interface validator, ledger, executor—but there is no singular owner of the complete transition.

The World Substrate rule should be:

> Applicability and authorization may inspect state and propose effects, but only the enclosing transition coordinator commits canonical writes after all guards, resource checks, and invariants succeed.

This does not imply universal ACID transactions or deterministic replay. It implies a single commit boundary for one causally coupled transition.

## 6. Agent boundary and cognitive architecture

AE2 contains two competing accounts of an agent:

- an agent is a persistent artifact with `has_standing` and `has_loop`;
- an agent is a pattern of activity across a constellation of goal, task, world-model, self-model, strategy, and memory artifacts.

The compositional cognition idea is useful. It allows memory, skills, plans, and strategy to be persistent, inspectable, replaceable, or shareable. But “agent is only a pattern” is a poor default for World Substrate because resident agents need stable identity, causal affordances, location or embodiment where applicable, resource relations, and continuity across actions.

Recommended boundary:

- the world contains a stable agent entity or principal with world-facing state and affordances;
- the resident runtime owns beliefs, uncertainty, memory, goals, planning, reflection, and model calls;
- cognitive state may be internally compositional and persistent without becoming canonical world belief state;
- the substrate records actions, communications, and world-visible consequences, not private chain-of-thought;
- a belief becomes world state only when represented through an observable bearer, such as an assertion, note, memory artifact, testimony, or institutional record.

AE2's simulations reinforce this. Prompt scaffolding and cognitive architecture materially determined observed behavior. If World Substrate owns those systems, it risks measuring its wrapper rather than the resident agents.

## 7. Observability, persistence, and reproducibility

AE2 explicitly states that deterministic behavior and research reproducibility are non-goals. That aligns with the World Substrate direction and corrects the overbuilt evidence/replay emphasis found later in AE3.

Its useful observability ideas are narrower:

- stable persistent identifiers;
- action intent and normalized action;
- permission result and failure reason;
- resource and payment effects;
- state before/after or a bounded diff;
- nested caller identity;
- contract or mechanic selected;
- fallback use and dangling references;
- capability requests and usage.

The event log should explain causal behavior. It need not prove that the same run can be reconstructed.

One AE2 choice should not be copied: dangling access contracts fail open to a configurable fallback. That preserves liveness but silently changes authority when an institution disappears. For a world substrate, unresolved causal authority should ordinarily refuse the affected transition and emit a conspicuous diagnostic unless the selected world profile explicitly defines a fallback.

## 8. Agent-authored expansion: the strongest seed

AE2's external-capability system provides a useful pattern for future mechanics authoring:

1. an agent discovers a missing capability;
2. it produces an explicit request with a reason;
3. an authorized process reviews and installs an implementation plus limits;
4. the capability becomes discoverable through one generic boundary;
5. uses are metered and observed.

For World Substrate's early pre-run workflow, replace “human approves a paid API” with “mechanics team validates and installs a mechanic into the frozen world profile.” The proposed mechanic should declare:

- semantic predicates and roles it realizes;
- applicability and required components;
- reads, proposed writes, and emitted observations;
- units/value types where relevant;
- invariants and conflict policy;
- dependencies on other mechanics;
- known unsupported interactions;
- examples and integration tests;
- discoverable affordance/interface metadata.

AE2's layered discovery is valuable here. Agents should be able to discover that a mechanic exists, inspect its scope and interface, estimate requirements or cost, and only then attempt an action. The repeated AE2 confusion between action types and artifact invocation shows that this semantic presentation is part of the architecture, not just documentation.

## 9. What the simulations actually establish

AE2's experiments provide useful negative and operational evidence, not validation of its broad thesis.

Established or strongly indicated:

- resource and affordance plumbing failures can completely block the behaviors being studied;
- stale or conceptually inconsistent interfaces can trap agents in retry loops;
- stronger models can mask architectural defects that weaker models expose;
- metacognitive framing can reduce error loops and improve stored-lesson quality;
- stored lessons do not guarantee correct later action;
- cognitively identical agents with self-contained goals and non-binding scarcity have little reason to specialize;
- prescribed cross-agent tasks test plumbing, not emergent cooperation;
- AE2's completed coordination primitives made institution-building possible in principle, but the recorded runs did not demonstrate agents autonomously building a coherent alternative institutional ecology.

Not established:

- that markets or organizations emerge from the kernel under meaningful conditions;
- that agent-authored contracts remain coherent as their interactions grow;
- that the “everything is an artifact” ontology improves semantic world modeling;
- that selection pressure reliably repairs cheating, buggy access control, or incoherent institutions;
- that observability alone makes violations tolerable.

The strongest pushback is on the last point. “Others will avoid bad contracts” cannot repair an irreversible state corruption, hidden rights transfer, or beneficiary mismatch after it occurs. Selection can shape future use; it is not a substitute for the substrate's transition integrity.

## 10. AE1, AE2, and AE3 compared

| Dimension | Agent Ecology 1 | Agent Ecology 2 | Agent Ecology 3 | World Substrate disposition |
| --- | --- | --- | --- | --- |
| Main value | Small behavioral counterexample harness | Broad mechanism-design laboratory | Narrower executable kernel | Use AE1 for falsification, AE2 for theory/history, and AE3 as a concrete reference—not as inherited code |
| Semantic model | Reified relations and roles | Universal artifacts plus flags/metadata | Universal artifacts plus typed action intents | Use Linguistic Core and donor ontologies instead |
| Causal breadth | Small and hardcoded | Very broad, many partially overlapping systems | Narrow information economy | Start narrow; expand through explicit mechanic contracts |
| Institutions | Heuristic policies | Contracts, escrow, ledger, rights experiments | Contract-governed paid access | Preserve institutions as represented causal bearers |
| Agent cognition | Fixed heuristics and memories | Extensive prompt/cognitive architecture | Kernel-owned scaffolding and gates | Resident agent owns cognition |
| Emergence evidence | Installed reciprocity/grudge dynamics | Mostly negative or plumbing evidence | One narrow reciprocal information-use chain | Do not claim more than the experiment installs and observes |
| Observability | Compact event/action traces | Rich logs and analysis tooling | Strong JSONL causal trace | Adopt explanatory trace, not replay bureaucracy |
| Primary warning | Hardcoded policy mistaken for emergence | Architectural breadth and conflicting authorities | Semantic poverty and premature contract effects | Make causal authority and commit boundaries explicit |

## 11. Disposition matrix

| AE2 element | Disposition | Reason |
| --- | --- | --- |
| Physics versus institution distinction | **Adopt** | Directly clarifies primitive, installed, and emergent causation |
| Orthogonal capacities/properties | **Adapt** | Good intuition; Boolean flags and meanings are too local |
| “Everything is an artifact” | **Reject as ontology** | Collapses agents, objects, processes, rights, and institutions into opaque records |
| Stable addressable entities | **Adopt** | Supports persistence and causal reference |
| Advisory free-form type/metadata | **Reject as semantic core** | Cannot supply Linguistic Core's role/type precision or reliable mechanics binding |
| Contract as executable causal bearer | **Adapt** | Useful institution pattern, too authorization-specific and locally attached |
| Semantic methods over raw edits | **Adopt** | Improves affordance clarity and makes authorization/mechanics meaningful |
| One transition coordinator | **Adopt more strongly than AE2 did** | Prevents provisional effects from escaping failed actions |
| Fail-open missing authority | **Reject by default** | Silently changes world law and rights |
| No kernel multi-step transaction support | **Qualify** | Independent actions need not be atomic; institutionally coupled transitions need one owned commit boundary |
| Agent cognitive constellation | **Adapt outside kernel** | Useful composition without making private cognition canonical world state |
| Layered discovery and interfaces | **Adopt** | Important for LLM agents choosing affordances safely |
| External capability request pattern | **Adapt for pre-run mechanics installation** | Generic expansion boundary avoids one primitive per new capability |
| Observability over determinism | **Adopt** | Matches explicit product goals |
| Selection pressure repairs bad contracts | **Reject as integrity mechanism** | Reputation cannot undo corrupted canonical state |

## 12. Implications for the thin vertical slices

AE2 changes the recommended order slightly. The project should test transition integrity before asking agents to author new mechanics, because otherwise the authoring experiment cannot distinguish a bad mechanic from a broken commit boundary.

Recommended learning sequence:

1. **Semantic state and action binding:** one persistent agent, two objects, and `give`; Linguistic Core roles bind to possession change and an observable receipt.
2. **Independent action plus derived composite:** two voluntary gives may be recognized as exchange; either participant can renege.
3. **Rights decomposition:** distinguish possession, provenance, use authority, and beneficiary for one asset without yet building a general legal ontology.
4. **Installed institution and commit integrity:** add one escrow-like institution that couples effects. Deliberately fail payment, validation, and one downstream action to prove no provisional effect commits.
5. **Non-agent causal process:** add one bounded process such as fire or storm under the same transition contract.
6. **Offline agent-authored mechanic:** give a mechanics agent one missing bounded affordance, validate it, install it into a profile, and freeze the profile for a run.
7. **Second micro-world:** test reuse and interaction defects rather than simply adding predicate count.

This is a thin vertical sequence, not a promise that social mechanics precede all physical mechanics. Slices 3–5 can be reordered after selecting the first product scenario. The hard dependency is that semantic binding, persistent effects, observability, and a singular commit boundary exist before open-ended mechanics authoring.

## 13. Recommended decisions for the living memo

1. Add a four-layer causal model: kernel physics, installed institutions, resident cognition, and analytic interpretation.
2. Treat AE2's “properties over types” as evidence for orthogonal capabilities, not as the answer to Linguistic Core's missing attributes/state relations.
3. Require explicit separation of provenance, possession, access, control, title, beneficiary, and transfer authority only when selected-world goals make each relevant.
4. Add a singular transition-envelope rule: mechanics and institutions propose effects; the enclosing action/process coordinator commits them.
5. Make fail-closed-on-unresolved-authority the default, with world-profile-specific fallbacks allowed explicitly.
6. Include semantic affordance discovery in the observability and agent interface requirements.
7. Use the capability-request lifecycle as a seed for pre-run mechanics agents.
8. Do not extract Agent Ecology code into World Substrate by default. Use the repositories as a design and failure corpus. If a narrow pattern such as typed intents, a centralized commit coordinator, or causal trace fields survives the World Substrate design, reimplement it after the World Substrate contracts are specified. Code reuse should require a later, pattern-specific justification.

## 14. Principal sources reviewed

- [Thesis](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/THESIS.md)
- [Current ontology](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/ONTOLOGY.yaml)
- [Target architecture overview](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/architecture/target/01_README.md)
- [Current architecture](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/architecture/current/README.md)
- [Everything is an Artifact ADR](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/adr/0001-everything-is-artifact.md)
- [Unified Permission Architecture ADR](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/adr/0019-unified-permission-architecture.md)
- [Executor Design Principles ADR](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/adr/0021-executor-design-principles.md)
- [`created_by` is Informational ADR](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/adr/0028-created-by-informational.md)
- [Access-control exploration](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/explorations/access_control.md)
- [Ostrom rights mapping](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/explorations/ostrom_rights_mapping.md)
- [Escrow stress-test exploration](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/explorations/escrow_stress_test.md)
- [Genesis-removal plan](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/plans/254_remove_genesis_artifacts.md)
- [External-capability plan](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/plans/300_external_capabilities.md)
- [Kernel-primitives plan](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/plans/312_expose_kernel_primitives.md)
- [Cognitive-architecture plan](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/plans/313_cognitive_architecture.md)
- [Simulation learnings](https://github.com/BrianMills2718/agent_ecology2/blob/main/docs/SIMULATION_LEARNINGS.md)
- [Artifact implementation](https://github.com/BrianMills2718/agent_ecology2/blob/main/src/world/artifacts.py)
- [Permission checker](https://github.com/BrianMills2718/agent_ecology2/blob/main/src/world/permission_checker.py)
- [Action executor](https://github.com/BrianMills2718/agent_ecology2/blob/main/src/world/action_executor.py)
- [Nested invocation handler](https://github.com/BrianMills2718/agent_ecology2/blob/main/src/world/invoke_handler.py)
- [External capability manager](https://github.com/BrianMills2718/agent_ecology2/blob/main/src/world/capabilities.py)

No Agent Ecology repository was modified during this review.
