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

## Causal claim boundary

A World Substrate causal claim is **internal to a represented world under its installed mechanics**. If an installed rule says an overloaded bridge collapses and that rule commits, the system should be able to explain that the represented overload was consumed by the installed collapse mechanic and produced the represented consequence.

That does not by itself establish that the rule is scientifically or empirically correct for a real bridge. Real-world predictive validity, calibration, and causal identification require separate evidence. The substrate's core guarantee is therefore about **explicit consequence authority and inspectable modeled dependencies**, not automatic truth of the model's assumptions.

Current hard parent event IDs are mechanic-declared and validated against retained canonical history. They are stronger than temporal proximity or prompt/context inclusion, but the runtime does not yet derive them from instrumented reads. Use the precise phrase **mechanic-declared hard causal ancestry** when that distinction matters.

Likewise, the current bounded causal-adequacy surface is a dependency inventory mapped to represented state and installed enforcement surfaces plus explicit residual risk. It does not yet provide automatic counterfactual proof of necessity/sufficiency. Stronger counterfactual or mutation verification is a later research option, not a prerequisite for the first public Waltzman demo.

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

Candidate/action-space size and observation size are separate scaling concerns and should be measured only when a real world makes them limiting. A bounded implementation must not silently hide valid actions when a candidate cap is reached; overflow should become explicit refusal, paging, or another visible bounded representation when this limit is hardened.

## Process and institution model

Autonomous processes use the same canonical state and transition authority as actions. A process must declare activation/reads/writes/timing/sources/sinks/interruption semantics and emit causal evidence.

Installed institutions are represented causal bearers whose rules alter future transitions or affordances. They are not special because of their name; they become causal because the world consults and enforces them.

## Time, cadence, and duration model

World Substrate should converge on **one canonical simulated timeline with independently scheduled mechanisms**, not one universal resident turn rate. Render time, process cadence, resident cognition cadence, institution cadence, and analysis cadence are distinct concerns. Only represented simulation time belongs to canonical world truth.

The generic runtime remains narrower: `World.tick` is an integer and `Engine.advance()` checks every registered process on each step through `due(world)`. The Waltzman first gate now proves that this canonical timeline can support scenario-specific trigger ticks and a represented duration-bearing meeting whose completion rechecks current time/state. That does **not** make the core a first-class future-event scheduler; richer scheduling remains an explicit target only when a real world outgrows the current seam.

Target rules:

- autonomous processes and institutions may operate at different cadences on the same canonical timeline;
- SimPy may schedule future wakeups/timeouts, but a wakeup only creates a World Substrate process opportunity—the installed mechanic still checks and commits/refuses consequences;
- duration-bearing activities such as travel, repair, testing, transport, or meetings should remain represented while underway when that duration matters to other mechanics; completion is a new transition opportunity that rechecks then-current state, not a guaranteed delayed write;
- resident cognition should normally wake on meaningful observations, interaction requests, task completion/failure, explicit schedules, or other bounded triggers rather than on every low-level world event;
- render interpolation/playback speed and analysis sampling never advance canonical simulation time; and
- cadence/resolution is separate from fidelity: a high-frequency mechanism can be coarse and a low-frequency mechanism can be detailed.

The Waltzman fixture has now earned one scenario-specific `ActivityState` for its two-tick meeting, while the generic simulation-time/activity schema remains uncommitted. Do not promote that world component into a universal contract without another use case. See [multi-timescale execution](research/multi-timescale-execution-2026-09.md).

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

## Information, cognition evidence, and causal ancestry

A represented communication is a world interaction first. When a selected world models information, the system should retain the representation, source, recipient, channel, provenance, delivery/observation, and visibility semantics needed by that world. Those records are canonical only to the extent the world represents them.

Information lineage is not automatically the same as hard causal ancestry. A resident may receive a report and later choose an action; the report may be retained as observation/context evidence without claiming that it mechanically caused the choice. Hard causal parentage is reserved for dependencies an installed transition explicitly declares as mechanically consumed or otherwise justified. Current parent IDs are validated against retained history but are not automatically derived from runtime read provenance. Derived analysis may make narrower claims later, but it cannot rewrite either history.

The durable distinction is therefore:

1. world interaction/event;
2. information representation/delivery/observation lineage;
3. cognition context or retained rationale/evidence;
4. mechanic-declared hard causal parentage; and
5. derived analytic interpretation.

The runtime now implements a bounded generic v0 for represented information and delivery: source, recipient, channel, visibility, delivery status, optional lineage, and actor-local asymmetric observation. Engine events may retain `information_context` separately from opt-in `causal_parent_event_ids`. It is deliberately not a belief/reputation/channel-fidelity model. See [information and delivery v0](contracts/information-delivery-v0.md) and [living-world projection research](research/living-world-projection-2026-09.md).

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

For actions, current placeholder enforcement restricts writes to entities named by the attempt, but it does not yet bind each placeholder name to one specific action role. Strengthening this to role-specific authority (for example, `<target>` means exactly the action's `target`) is a straightforward hardening task after the public demo rather than a reason to reopen the architecture.

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

The current `MechanicProfile.freeze()` gives the reviewed package set a stable declaration identity before a run. For future durable generated-law provenance, approval/run identity should be strengthened to fingerprint the exact executable law plus the compiler/interpreter version that gives the declaration meaning. That hardening matters before persistent long-lived user law is treated as cryptographically reproducible; it is not a blocker for publishing the current hand-authored Waltzman reference demo.

### External analytical-model structural imports

An upstream analytical or architecture model may seed **represented structure** through a bounded adapter without acquiring causal authority. The first exercised path is [CVS Situation IR structural import v0](contracts/cvs-situation-import-v0.md): a CVS role/pool/capability/action/rule/scenario slice becomes a `world-substrate-authoring-bundle/v0`, with source identity retained explicitly and unsupported semantics rejected. The imported bundle still enters the same separate causal-model/compiler/review/approval path shown above.

Do not generalize this into a universal architecture schema. Add another import distinction only when an authentic producer/consumer case demonstrates that the current projection loses decision-relevant meaning.

## Observability, replay, and presentation

Every attempted transition should expose enough evidence to reconstruct the causal story: delivered observation when applicable, bearer, semantic binding when available, selected mechanic, checks, declared authority, committed changes, failure status, and resulting state identity.

Rejected/unsupported/invalid actions do not partially commit their claimed transition.

Exact replay is an implemented M1/debugging capability, not a universal requirement. Stable snapshots/profile identities and causal traces are the broader observability requirement.

Presentation is downstream of world truth. Scene profiles/assets/auto-layout may choose where/how an entity appears, but presentation coordinates or animation state never become canonical causal state merely because the UI renders them.

The same rule applies to the living-world client. The implemented `world-substrate-live-projection/v0` seam combines an initial snapshot with incremental canonical events/deltas and may render derived **possible / enabled / active / realized** relationship states. These are visualization classifications over installed structure, current state, and retained history—not new world variables. Renderer selection, interpolation, camera state, filters, and overlay visibility remain client-local. The Waltzman client verifies one-way reconstruction for baseline and intervention branches and exposes the same observer data over JSON/SSE. See [live projection v0](contracts/live-projection-v0.md).

The first public Waltzman demo may publish the generated self-contained client because it embeds those canonical projection bundles; a continuously running public simulation service is not required to preserve this presentation boundary.

## Agent and observer separation

Actors receive bounded observations and offered actions. Observer surfaces may inspect broader canonical/history/provenance data. Resident memory, beliefs, uncertainty, planning, schedules, and reflection remain private agent-runtime state unless a selected mechanic explicitly represents and reads them.

A resident utterance may be returned by the cognition adapter, but it only becomes shared world information through an installed communication/information mechanic or process. The harness cannot make another resident know something merely by emitting prose.

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
- Selected product dependencies are governed by Decision 004 and remain replaceable adapters; implementation should pin exact versions before those dependencies become part of a reproducible production run manifest, and upgrades should be deliberate.
