# World Substrate architecture

## Architectural thesis

A rich world comes from shared persistent state, semantic grounding, and installed mechanics with explicit local causal authority. LLM sophistication is useful for resident policy and offline mechanics authoring, but policy prose must not compensate for missing world mechanics or directly mutate canonical state.

```text
semantic intent or autonomous trigger
        |
        v
Linguistic Core sense + role binding
        |
        v
installed local mechanic -> proposed effects -> validation -> commit/refusal
        |                                              |
        v                                              v
bounded observation                         persistent state + causal trace
                                                       |
                                                       v
                                            detachable analytic views
```

## Architecture-description discipline

This project uses a small architecture-description discipline to keep different
representations of the same substrate consistent. It selectively borrows the
distinction between concerns, reusable viewpoints, and project-specific views
from [ISO/IEC/IEEE 42010](https://www.iso.org/standard/74393.html).
[UML](https://www.omg.org/uml/),
[SysML v2](https://www.omg.org/sysml/sysmlv2/), and
[KerML](https://www.omg.org/spec/KerML/1.0/About-KerML) may supply useful
notations or semantic patterns, but the project does not claim conformance and
does not require their toolchains.

- A **concern** is a question that a representation must answer.
- A **viewpoint** defines the conventions for answering a recurring concern.
- A **view** applies a viewpoint to a particular project revision.
- A **model kind** is the form used by a view, such as a boundary table,
  transition specification, sequence, or evidence trace.

The maintained viewpoints are deliberately few:

| Viewpoint | Concern | Model kind and maintained view | Current authority |
| --- | --- | --- | --- |
| `VP-BOUNDARY` | Who owns state, decisions, effects, and failure containment? | boundary/component table in this document | M1 path and explicit envelope negatives implemented and promoted |
| `VP-TRANSITION` | How can an action or process change state, and how does it fail? | transition kernel and operation contracts in [core contract v0](contracts/core-v0.md) | fill, heat, unheat, pour, drink, take, give, processes, rejection, and replay implemented |
| `VP-ACTOR-INFORMATION` | What can an actor observe and select versus what an observer can inspect? | projection and information-flow descriptions here and in the core contract | minimal full-path observation/discovery implemented; broader authorization and paging open |
| `VP-OBSERVABILITY` | How is each attempt, refusal, and consequence explained? | causal trace, check results, state-path operations, snapshots, and optional replay | M1 evidence and replay established; the broader observability contract is proposed |
| `VP-ADOPTION` | When has a donor capability actually become a project capability? | source disposition plus consumer-path evidence | [source dispositions](source-dispositions.md) and revision-bound evidence |

A view need not be a diagram. Every maintained view must use the native stable
IDs and terms of the contract or implementation it represents, state its source
revision and claim status, label the meaning of edges or arrows, and identify
material omissions. Corresponding views must agree on authority boundaries,
rule and operation identities, accepted/rejected status, and evidence links.
After code exists, views that describe implementation must bind to real modules,
interfaces, and tests. Visual agreement or standards-shaped notation is not
evidence that the runtime behaves as shown.

## Authority boundaries

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Canonical world | state, revision, authoritative time, atomic commit | policy or narrative |
| Mechanic registry | semantic bindings, applicability, local reads/writes, proposed effects, processes, invariants, and limits | world instances or undeclared authority |
| Content packs | objects, properties, recipes, starting state, ontology bindings | new effects without rules |
| Affordance discovery | actor-local rule instantiation, filtering, paging | consequence calculation |
| Policy adapter | LLM, human, or scripted selection and explanation | state mutation |
| Persistence | canonical state, versions, snapshots, and causal traces | alternate effects or resident-agent private cognition |
| Authoring and installer | reference integrity, semantic/mechanic binding, scope validation, declared coverage, tests, and frozen profiles | unreviewed runtime law changes or direct canonical mutation |
| Observer surfaces | canonical and historical projections | hidden simulation state |

## Composition model

An object has stable identity and typed components or properties. Rule families declare which components they read and write.

For example, a vessel may have:

- location and owner;
- material and mass;
- capacity and condition;
- liquid contents with extensive quantities;
- temperature;
- attachment to a heat source.

Independent rules can therefore transfer the vessel, transfer its contents, heat it, cool it, damage it, or include its mass in carrying capacity. Giving away a hot vessel transfers the same object with its heat and contents intact.

Adding a stone beaker is a content extension when all required properties already exist. Adding pressure is a mechanism extension because the substrate needs pressure state, sealed-volume rules, heating interaction, failure behavior, and evidence.

## Action model

A rule schema generates finite action instances from current local state. A policy never receives an abstract promise that it can “do anything.”

`pour(source, target, amount)`, for example, requires accessible compatible vessels, positive contents, free target capacity, and an allowed integer amount. The effect moves every conserved liquid component proportionally and emits before/after evidence.

The possible action space grows through combinations of objects, relations, parameters, and rules. Presentation may be bounded even when candidate generation is large. Candidate enumeration and observation size must be measured separately.

## Process model

Processes use the same objects and advance only under canonical time. Each declares:

- activation conditions;
- state read/write surface;
- timing;
- sources and sinks;
- ordering or conflict semantics;
- termination/interruption behavior; and
- causal events.

A fire checking for fuel but never deducting it is an incomplete rule. It is not an ontology failure.

## Semantic and causal layers

The architecture distinguishes four layers:

1. **substrate physics and autonomous processes** that enforce selected world behavior;
2. **installed institutions** whose represented rules alter transitions or affordances;
3. **resident-agent cognition** owned by agent runtimes; and
4. **analytic interpretation** that classifies or measures history without writing it.

A semantic predicate does not select its layer by name alone. A Linguistic Core `exchange` sense can describe two reciprocal gives without becoming another transfer mechanic. An escrow institution can instead acquire causal force because the world consults and enforces it.

Use the causal-force test before adding a mechanic: if lower-level events are held fixed and removing the named phenomenon changes no later transition or affordance, it is normally derived.

## Semantic–mechanical binding

Linguistic Core is the semantic compiler interface. It contributes predicate senses, roles, specializations, and relationships among meanings. It does not determine persistence, quantities, effects, scheduling, authority, invariants, or commit semantics.

A state-changing attempt must bind:

- one reviewed predicate sense;
- participant roles to canonical references;
- a provisional causal class;
- a represented causal bearer; and
- one mechanic installed in the active profile.

Free text may accompany the binding but cannot substitute for these fields. See the proposed [semantic–mechanical binding contract](contracts/semantic-mechanical-binding-v0.md).

The initial causal classifications—primitive action, autonomous process, state relation, composite event, analytic pattern, declaration, and installed institution—are a binding vocabulary, not a new upper ontology. Donor review may revise them.

## Transition envelope and local authority

A mechanic, permission rule, pricing rule, or institution may inspect state and propose effects. Only the enclosing action or process coordinator commits effects that belong to the same claimed causal transition.

The transition path is:

```text
observation or trigger
  -> sense and role binding
  -> selected local mechanic
  -> applicability and authorization
  -> proposed effects
  -> resource and invariant checks
  -> one commit or refusal
  -> causal trace
```

Write declarations are enforced at state paths, independently of implementation
language: the engine compares every committed change against the mechanic's
declared `write_paths` and refuses the transition otherwise (`scope_violation`
for an action, `ScopeViolation` for a process). Read declarations are recorded
on every causal event but are **not** enforced at runtime — a read leaves no
trace in state, so enforcing it needs a different mechanism than comparing
before and after. State outside a mechanic's contract may coexist on an entity
but remains outside that mechanic's authority.

This is not universal ACID. Independent gives may commit independently, allowing reneging. An installed escrow release may instead couple two asset transfers and its own state update in one commit.

## Authoring, installation, and causal closure

Scenario and content authoring instantiate installed mechanics. Offline mechanics authoring may produce declarative packages or executable source, but the output is not installed merely because it parses or passes isolated unit tests.

A mechanic package declares semantic bindings, causal bearer, required state, optional modifiers, incompatibilities, reads, writes, effects, scheduling, goal-relative invariants, dependencies, unsupported interactions, representation, limits, tests, and trace behavior. The installer validates these surfaces and freezes a mechanics profile before the run.

The compiler can establish **declared enforcement coverage**: every consequence and dependency the author named is bound to an enforceable interface. It cannot prove that the author remembered every consequential dependency.

A **causal-closure assay** therefore combines semantic inspection, dependency comparison, overlapping-write analysis, counterexamples, and interaction tests. Its output is evidence and residual risk, not a universal-completeness boolean.

### Concrete coherence case

A sealed clay pot may individually support heat, pressure, material strength, container damage, and fluid flow while the composition remains incoherent. Failure modes include pressure continuing after rupture, a broken container remaining sealed, water being both retained and leaked, incompatible units, duplicated or lost quantity, or heat and contents remaining attached to a replaced object.

No individual equation must be absurd. The incoherence appears at shared meanings, update order, capability revocation, identity handoff, and overlapping authority.

## Observability, persistence, and replay

Each attempted transition exposes what was observed or read, the semantic binding, selected mechanic, checks, proposed effects, committed state paths, failures or unsupported interactions, and resulting persistent state identity at the resolution required by the world.

Snapshots and stable mechanic/profile identities support inspection and debugging. Exact replay is optional.

M1 remains deterministic and exactly replayable for its pinned engine, content, initial state, registry, and command sequence. `World.snapshot()`, `World.from_snapshot()`, and `Engine.replay_commands()` are implemented M1 capabilities and the retained replay receipt remains valid evidence. They are not requirements imposed on future mechanics.

Rejected, invalid, and unsupported actions do not partially commit their claimed transition. Their checks and reasons remain inspectable.

## Agent and observer separation

Actors see only authorized observations, known definitions, and bounded affordances. The observer may inspect the selected world truth, histories, provenance, and traces. Agent memory, beliefs, uncertainty, planning, and private reasoning remain inside the resident-agent runtime unless a selected world explicitly represents a belief-like state for a mechanic to read. The substrate records delivered observations, attempts, and causal results; analysis cannot overwrite canonical truth.

## Dependency posture

- Castaway donates the first behavior and evidence vertical.
- Cybernetic Influence V3 donates a canonical intent/proposed-patch/commit boundary and observability patterns; V2 donates bounded local authority.
- Linguistic Core is the pinned semantic interface, subject to a persistent-state and quantities coverage audit.
- Agent Ecology, Data Contracts, and Collective Competence are idea, contract, and failure-analysis donors rather than code-adoption decisions.
- Shared `llm_client` is the only planned model-provider seam.
- Concordia remains an evaluated optional lifecycle dependency, not a foundational commitment.
