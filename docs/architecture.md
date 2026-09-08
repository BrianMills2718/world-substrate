# World Substrate architecture

## Architectural thesis

A rich world comes from **shared persistent state, semantic grounding, and installed mechanics with explicit local causal authority**. LLM sophistication is useful for policy, cognition, and mechanic proposal, but model prose must not compensate for missing world law or directly mutate canonical state.

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

The product direction in [Decision 004](decisions/004-product-and-adoption-strategy.md) is a Generative-World Builder front end over this causal engine. Product frameworks may surround the engine; they do not replace its consequence authority.

## Architecture-description discipline

Architecture documents answer stable concerns rather than narrate milestones. A maintained view must identify its authority source, use implementation IDs where code exists, state material omissions, and agree with contracts/tests/evidence.

The recurring viewpoints are:

| Viewpoint | Concern | Authority |
| --- | --- | --- |
| Boundary | who owns state/decisions/effects/failure containment? | this document + accepted decisions |
| Transition | how can state change or refuse? | [core contract](contracts/core-v0.md) + Engine |
| Actor information | what may an actor observe/select? | core contract + policy/observation code |
| Observability | how is an attempt/outcome explained? | Decision 002 + causal events/evidence |
| Adoption | when does a donor/framework become a project capability? | [source dispositions](source-dispositions.md) + Decision 004 |

Standards such as ISO/IEC/IEEE 42010, UML, SysML, or KerML may supply useful notation; the project does not claim conformance or require those toolchains.

## Authority boundaries

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
| Persistence | canonical snapshots/history/profile IDs and future user-world storage | alternate effects |
| Replay/observer surface | visual/historical projection of represented truth | hidden or invented causal state |
| Analysis | derived interpretation/measurement | rewriting canonical history |

## Composition model

Entities have stable identity and typed components. Independent mechanics operate on shared component state under declared authority.

A vessel, for example, may simultaneously carry location, owner, material, capacity, contents, temperature, condition, and heat-source relation. Transfer moves the same vessel with its contents/temperature intact because identity is shared across mechanics.

Adding another vessel is a **content extension** when existing components/mechanics suffice. Adding pressure is a **mechanism extension** because it requires represented pressure/sealed-volume state, heating interaction, failure behavior, and evidence.

The system should grow by composing reusable state/mechanics, not by enumerating every natural-language command.

## Action and affordance model

Rules generate finite action instances from current local state. A policy selects among concrete offered actions; it does not receive an abstract promise that anything describable is executable.

For a parameterized action such as `pour(source, target, amount)`, discovery enumerates bounded candidate values and checks state-dependent constraints. Generated live mechanics likewise require finite scalar choices so the action space remains bounded.

Candidate/action-space size and observation size are separate scaling concerns and should be measured only when a real world makes them limiting.

## Process and institution model

Autonomous processes use the same canonical state and transition authority as actions. A process must declare activation/reads/writes/timing/sources/sinks/interruption semantics and emit causal evidence.

Installed institutions are represented causal bearers whose rules alter future transitions or affordances. They are not special because of their name; they become causal because the world consults and enforces them.

## Semantic and causal layers

The architecture distinguishes four causal layers:

1. substrate physics and autonomous processes;
2. installed institutions;
3. resident-agent cognition; and
4. derived analytic interpretation.

A semantic predicate does not choose its causal layer by name. Apply the causal-force test:

> If lower-level events were held fixed and this named phenomenon were removed, would later transitions or affordances change?

If not, it is normally a derived description rather than a new mechanic.

`exchange`, for example, can describe two reciprocal `give` events without reapplying transfer. Escrow can become causal if a represented institution actually couples release conditions and transfers.

## Semantic–mechanical binding

Linguistic Core contributes predicate senses, participant roles, specializations, and semantic relationships. It does **not** determine persistence, quantities, effects, scheduling, authority, invariants, or commit semantics.

A causally meaningful attempt should ultimately carry:

- one reviewed predicate sense;
- participant roles bound to canonical references;
- a causal classification;
- a represented causal bearer; and
- one installed mechanic/profile identity.

Free text may accompany this binding but cannot substitute for it. The implemented M1 path has reviewed bindings for six of seven action kinds; generic live authoring currently permits causal declarations before this semantic loop is fully closed. That gap is explicit in the roadmap, not a change to the doctrine. See [Decision 003](decisions/003-semantic-mechanical-boundary.md) and [semantic–mechanical binding v0](contracts/semantic-mechanical-binding-v0.md).

## Transition envelope and local authority

Only the enclosing coordinator commits effects belonging to one causal transition.

Write declarations are enforced at state paths: the engine compares every candidate change with the mechanic's declared `write_paths` and refuses/raises on out-of-scope writes. Rule-facing hooks run against detached state, and revision/commands/events are engine-owned.

Declared read paths are retained on events but are not currently runtime-enforced; enforcing reads requires an observation/recording mechanism rather than before/after state comparison. See [read-scope enforcement v0](contracts/read-scope-enforcement-v0.md).

This is not universal ACID. Independent attempts may commit independently. A represented institution may instead define one broader transition that legitimately couples multiple writes.

## Causal authoring and installation

Structural authoring and causal law are separate:

```text
world-substrate-authoring-bundle/v0
        |
        | represented entities/components/action signatures
        v
world-substrate-causal-model/v0
        |
        | constrained checks/effects/terminal
        v
local causal compiler derives reads/writes and validates types/paths/selectors
        |
        v
human review + explicit approval
        |
        v
MechanicProfile install/freeze
        |
        v
normal Engine execution
```

The proposer never supplies its own authority. Unknown paths/operators/participants are rejected; model-written source is not executed. One compiler-guided repair may be attempted under the same bounded model trace.

Compiler/installer acceptance proves **declared enforcement coverage**, not completeness. The project therefore keeps causal-closure assays, counterexamples, overlapping-write checks, and residual-risk statements separate from schema validity.

## Observability, replay, and presentation

Every attempted transition should expose enough evidence to reconstruct the causal story: delivered observation when applicable, bearer, semantic binding when available, selected mechanic, checks, declared authority, committed changes, failure status, and resulting state identity.

Rejected/unsupported/invalid actions do not partially commit their claimed transition.

Exact replay is an implemented M1/debugging capability, not a universal requirement. Stable snapshots/profile identities and causal traces are the broader observability requirement.

Presentation is downstream of world truth. Scene profiles/assets/auto-layout may choose where/how an entity appears, but presentation coordinates or animation state never become canonical causal state merely because the UI renders them.

## Agent and observer separation

Actors receive bounded observations and offered actions. Observer surfaces may inspect broader canonical/history/provenance data. Resident memory, beliefs, uncertainty, planning, schedules, and reflection remain private agent-runtime state unless a selected mechanic explicitly represents and reads them.

This boundary is what allows an off-the-shelf cognition framework to be integrated safely: it may decide **what the resident wants to attempt**; the Engine still decides what the world says happened.

## Product and off-the-shelf adoption posture

[Decision 004](decisions/004-product-and-adoption-strategy.md) makes the division explicit.

Keep project-owned:

- canonical world/identity;
- transition authority;
- semantic/mechanical binding;
- causal declaration/compiler;
- mechanic authority/profile semantics;
- causal trace; and
- declarative scene semantics.

Selected commodity defaults at the boundary are:

- **deck.gl 9.4.x** for the living spatial/semantic projection client; `OrthographicView` is the default for schematic worlds, with MapLibre available when the canonical world uses real geography;
- **Pydantic AI 2.41.x** behind `CognitionAdapter` for resident memory/planning/tool orchestration while the Engine retains consequence authority;
- **SimPy 4.1.2** as a scheduling primitive only: it may advance simulated time and wake processes, but it does not own canonical resources or effects;
- **Cytoscape.js 3.34.x** for expanded causal/institutional graph inspection when needed;
- **PettingZoo** for future multi-agent evaluation/interoperability; and
- standard persistence/auth for durable user worlds/runs/access.

Commodity selection follows research → reason → select; local tests are boundary-conformance tests, not framework bake-offs. Novel World Substrate uncertainty still earns experiments. All external systems remain replaceable adapters and must preserve canonical consequence authority.

## Dependency posture

- Linguistic Core is the pinned semantic interface.
- Shared `llm_client` is the model-provider seam.
- Castaway, Cybernetic Influence, Agent Ecology, Data Contracts, and Collective Competence remain bounded donors according to [source dispositions](source-dispositions.md).
- Selected product dependencies are governed by Decision 004 and remain replaceable adapters; exact versions are pinned in implementation lockfiles and upgraded deliberately.
