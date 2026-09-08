---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-08
---

# World Substrate living roadmap

**Authority:** [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md), and [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md).  
**Stage:** prototype substrate complete; deployed authoring/run alpha; deployed living-world visualization prototype; current phase is live-world product integration.
**Current frontier:** make the living-world prototype consume real World Substrate state/events through a read-only projection seam, then use the Coordination Lab/Waltzman target vertical to earn richer information, process, institution, cognition, and causal-closure capabilities.
**Deployment boundary:** the existing World Builder and standalone visualization prototype are authorized/public. New publication surfaces, provider spend outside the bounded Builder service, or runtime-generated-law installation outside the reviewed path still require explicit human authority.

## Outcome and success criteria

### End goal

Build a **generatively authored, reviewable, persistent simulation platform for plausible worlds**. A user describes a bounded world conversationally; the system compiles represented structure and executable law; the user reviews the important assumptions and causal coverage; residents/processes inhabit the world; the world evolves under installed mechanics; and the user watches and interrogates the result through a dynamic visual surface.

The product thesis remains:

> **Generative worlds with executable laws.**
> Generative-World Builder on top; rigorous causal world engine underneath.

The first serious application vertical is the **Coordination Environment Lab** inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*. It is a demanding target, not a new definition of the core. Waltzman trust/risk/readiness remain detachable analysis, not hidden universal state.

Predictive behavioral validity is not a current promotion gate. The current objective is internally coherent, inspectable worlds under explicit assumptions.

### Prototype phase — complete

The substrate phase has already established:

1. persistent typed canonical state;
2. bounded actor observations and state-derived affordances;
3. scripted/human/LLM selection outside consequence authority;
4. semantic/mechanical separation;
5. reviewed/frozen mechanic profiles;
6. atomic commit/refusal with write-scope enforcement;
7. retained causal evidence and full-log debugging; and
8. transfer to multiple materially different worlds.

### Product-phase success criteria

The next phase succeeds when:

- a useful nontrivial world can be created primarily through authoring/review rather than bespoke repository surgery;
- the graphical surface is a continuously updated world, not only generated replay HTML;
- core overlays (residents, information, resources, processes, authority, causal focus/history) are derived from real world semantics;
- residents can communicate through represented information channels while private cognition remains private;
- actions, autonomous processes, and institutions share one consequence-authority model;
- generated worlds expose a bounded dependency/causal-closure report with residual risk rather than a false completeness claim;
- off-the-shelf resident cognition can plug in without becoming world authority;
- analyses such as Waltzman can attach/detach without affecting the run; and
- worlds/runs can later persist without losing provenance or law/profile identity.

## Canonical outcome probe

M1 remains the neutral substrate baseline: persistent actors/vessels, finite resources, autonomous processes, atomic rejection, causal events, snapshots, and exact pinned replay. It proves the core seam; it is not the product destination.

Current product fixtures have narrower roles:

- **Kitchen** — replicated watched-world behavior and polished/Automatic presentation.
- **Greenhouse** — post-renderer new-world portability and multi-entity effects.
- **Orchard** — live authoring acceptance fixture.
- **Repair Bay** — first nontrivial deployed authoring world and current live-projection fixture candidate.
- **Warehouse Rush** — retained draft experiment showing scalar/physical semantic gaps and full-log-driven repair; not the active roadmap.

## Current truth

State, not milestone narrative:

- One `World` owns canonical material truth. Policy prose, UI animation state, resident private cognition, and analysis are not alternate authorities.
- Engine write scopes are enforced. Declared read scopes are retained but not runtime-enforced.
- Linguistic Core supplies semantic senses/roles, not effects. Generic live authoring can still compile actions before semantic closure is complete.
- The constrained causal declaration/compiler path is deployed: model proposes data, local compiler derives authority, a human explicitly approves, then an ordinary frozen `MechanicProfile` runs through the Engine.
- Every live Builder diagnosis must start from the complete request/response log and retained causal trace; summaries/replay are orientation surfaces only.
- Repair Bay proved nontrivial generated law can compile and a bounded LLM policy can reach terminal without a heavier cognition framework.
- Warehouse Rush v0 exposed a real law/representation omission (`route` did not enforce physical dock); v1 represents `target_dock`. Draft PR #37 retains the experiment and awaits a provider retry, but that retry is no longer the exact next action.
- The deployed World Builder is `https://brianmills.dev/world-builder/`.
- A standalone living-world visualization prototype is deployed at `https://brianmills.dev/world-substrate-visualization/` and versioned at `prototypes/living-world-overlay-v0.html`. It is currently synthetic UI data and is **not yet fed by World Substrate**.
- [Living-world projection research](../docs/research/living-world-projection-2026-09.md) defines the current visual semantics: one spatial world, dynamic core overlays, analytic plugins, and a strict distinction between information lineage and hard causal ancestry.
- Commodity procurement is settled by Decision 004: deck.gl 9.4.x for living projection; Pydantic AI 2.41.x behind `CognitionAdapter`; SimPy 4.1.2 for scheduling only; Cytoscape.js 3.34.x for expanded graph inspection.
- The selection doctrine is **novel uncertainty → experiment; commodity uncertainty → research/reason/select; integration uncertainty → conformance test**.
- The current time/process runtime is still the M1 integer-tick baseline: `Engine.advance()` checks registered processes each step through `due(world)`. It does not yet provide one canonical future-event timeline, duration-bearing activities, independently scheduled cadences, or event-driven cognition wakeups.
- The product does not yet have first-class generic information/conversation semantics, a generic multi-timescale process/activity authoring surface, generalized institutions/decision procedures, durable resident cognition, or saved user worlds/runs.
- Open PR #43 (CVS sustainment seam) is a separate integration track and does not define this roadmap. Rebase/review it against current main before any merge decision.

## Applicable context

- [Decision 001](../docs/decisions/001-project-scope.md): this repository is canonical executable-consequence authority.
- [Decision 002](../docs/decisions/002-observability-and-replay.md): important attempts/refusals/consequences remain inspectable; exact replay is not a universal goal.
- [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md): semantic predicates do not imply effects; cognition and analysis remain distinct causal layers.
- [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md): own causal reality, borrow commodity cognition/rendering/scheduling/graph infrastructure.
- [Technology procurement](../docs/research/technology-procurement-2026-09.md): selected external defaults and conformance boundaries.
- [Living-world projection](../docs/research/living-world-projection-2026-09.md): current visualization/overlay semantics and first vertical acceptance.
- [Competitive landscape](../docs/research/competitive-landscape-2026-09.md): adjacent systems and the "own reality; borrow minds" positioning.
- [Source dispositions](../docs/source-dispositions.md): neighboring repositories are donors/evidence unless explicitly adopted.

## Constraints and authorities

```text
conversational authoring
  -> represented state + dependency intent
  -> reviewed semantic/action structure
  -> constrained/generated mechanics
  -> local compiler + approval + frozen mechanic profile
  -> resident action OR autonomous process trigger
  -> Engine checks + one commit/refusal
  -> canonical state + causal/evidence history
  -> read-only live projection
  -> optional analytic plugins
```

Hard constraints:

- policy/model prose cannot mutate canonical state;
- a mechanic cannot enlarge its own write authority;
- generated source code is not a causal-law fallback;
- analysis cannot rewrite history or duplicate primitive effects;
- presentation/overlay state is downstream and read-only;
- resident harnesses may choose attempts/utterances but not adjudicate consequences;
- SimPy may schedule opportunities, never own resource truth/effects;
- information delivery/context must not be automatically promoted to hard causal parentage;
- commodity selection is not a reason for local framework bake-offs; and
- hardening/generic breadth must buy trustworthy evidence or immediate experiment/product throughput.

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it establishes |
| --- | --- | --- |
| M0–M7b substrate/generative mechanics | complete | persistent governed world + authoring/compiler/policy seams |
| Kitchen + generic replay | complete first gate | watched-world behavior + portable read-only visualization |
| Greenhouse/Orchard | complete first gate | new-world presentation + live generated-law authoring |
| Repair Bay | complete first gate | nontrivial deployed authoring and LLM inhabitant proof |
| Warehouse Rush | retained draft evidence | law/representation failure discovered and minimally repaired |
| Commodity procurement | **complete** | deck.gl / Pydantic AI / SimPy / Cytoscape defaults selected |
| Living-world visual prototype | **complete prototype** | desired interaction/overlay model is publicly inspectable |
| Live projection seam | **active / next** | real World Substrate run drives the living visual client |
| Information/conversation semantics | queued after live projection | represented utterances, source/recipient/channel/provenance/visibility |
| Multi-timescale processes + activities | queued after information semantics, earned by Coordination Lab | one canonical simulated timeline; independent cadences; duration-bearing activities; SimPy schedules opportunities only |
| Institutions | queued from Coordination-Lab pressure | meetings, deadlines, decision procedures, permissions/commitments on the same timeline |
| Generative causal closure | core research frontier | dependency inventory → enforcement mapping → counterexamples → residual risk |
| Cognition adapter | selected dependency, integrate when earned | Pydantic AI resident memory/planning; wake on meaningful events rather than every scheduler microstep |
| Coordination Lab vertical | target application | Waltzman scenario + detachable analysis + intervention/fork workflow |
| Persistence / second-domain proof | later | durable user worlds/runs and proof of generality beyond Waltzman |

### Active slice — real World Substrate → living world

Do **not** add a new toy world first. Use a real retained run (prefer Repair Bay) to replace the deployed prototype's synthetic timeline.

The minimal product vertical is:

```text
real World snapshot/run
      +
retained event stream/deltas
      +
existing scene semantics
      |
      v
read-only projection adapter
      |
      v
deck.gl living client
```

First acceptance:

1. canonical entity IDs, event IDs, revision/tick, accepted/refused outcomes, and state changes displayed in the client match the retained run exactly;
2. play/pause/step/scrub/select are presentation controls only;
3. visual movement/state changes come from scene/projection semantics, not Repair-Bay-specific renderer branches;
4. causal highlighting is limited to mechanically supported ancestry/evidence categories;
5. information/conversation overlays are hidden or explicitly unsupported until generic information semantics exist;
6. the projection seam is one-way/read-only and cannot mutate the World; and
7. full logs/full traces remain the debugging authority if UI and canonical history disagree.

Start with an initial snapshot plus incremental event/delta delivery. SSE is sufficient for the first one-way live stream. Do not introduce WebSocket, Pydantic AI, SimPy, Cytoscape, persistence, or a new causal DSL feature just to complete this slice.

After this slice, add **first-class information/conversation semantics**. A conversation is a world interaction plus an information representation/delivery; it becomes part of a causal explanation only where retained mechanics/evidence justify that stronger relation.

The next process/institution slice should then introduce **multi-timescale execution only when a real target world requires it**: one canonical simulated timeline, independently scheduled process/institution triggers, and the minimum duration-bearing activity representation needed for travel/tasks/meetings. SimPy may schedule wakeups; World Substrate still decides consequences. Resident cognition should normally wake on meaningful delivered information, interaction requests, task completion/failure, scheduled reflection, or other bounded triggers rather than every low-level scheduler event. See [multi-timescale execution](../docs/research/multi-timescale-execution-2026-09.md).

## Decisions and assumptions

### Product/adoption strategy

| Layer | Current posture |
| --- | --- |
| Canonical state / identity | keep project-owned |
| Transition kernel / authority / trace semantics | keep project-owned |
| Causal declaration/compiler | keep project-owned |
| Semantic/mechanical binding | keep project-owned with Linguistic Core |
| Dependency inventory / bounded causal closure | strategic research surface; keep project-owned |
| Scene/projection semantics | keep project-owned; renderer stays downstream |
| Living browser rendering | deck.gl 9.4.x selected; MapLibre optional for real geography |
| Resident cognition | Pydantic AI 2.41.x selected behind `CognitionAdapter`; integrate only when a world needs it |
| Simulated scheduling | SimPy 4.1.2 selected for event/time scheduling only; target is one canonical timeline with independent mechanism cadences |
| Activity duration | project-owned semantic/causal contract when earned; completion rechecks current world rather than applying a guaranteed delayed write |
| Expanded graph inspection | Cytoscape.js 3.34.x selected when a non-spatial inspector is needed |
| Multi-agent evaluation | PettingZoo later if useful; never alternate world authority |
| Persistence/auth | standard commodity infrastructure later |

### Information / causality rule

Do not collapse these relationships:

- **world interaction** — e.g. Mara speaks to Ari;
- **information lineage** — representation, source, recipient, channel, delivery/observation;
- **cognition context/evidence** — information the resident harness was shown;
- **hard causal ancestry** — dependencies mechanically consumed by an installed transition; and
- **analytic interpretation** — post-run or observer inference.

Temporal precedence or prompt inclusion is not sufficient to label an information event a hard cause of a resident decision.

### Experiment-selection rule

- **Novel uncertainty:** experiment. Primary example: bounded generative causal closure.
- **Commodity uncertainty:** research → reason → select. Renderer/model/harness/library selection normally lives here.
- **Integration uncertainty:** prove the adapter seam conforms; do not run a comparative architecture tournament.

## Evidence and review artifacts

Primary current artifacts:

- `https://brianmills.dev/world-builder/` — deployed authoring/run alpha;
- `https://brianmills.dev/world-substrate-visualization/` — deployed living-world interaction prototype;
- `prototypes/living-world-overlay-v0.html` — versioned source for that prototype;
- [Living-world projection research](../docs/research/living-world-projection-2026-09.md);
- [Technology procurement](../docs/research/technology-procurement-2026-09.md);
- [Repair Bay live proof](../docs/audits/repair-bay-live-preflight.md) + `evidence/repair-bay/live-experiment-v0-summary.json`;
- [Live authoring audit](../docs/audits/live-world-authoring.md);
- [Kitchen audit](../docs/audits/kitchen-contested-world.md) and retained renders;
- [Scene profile v0](../docs/contracts/scene-profile-v0.md);
- [World authoring bundle v0](../docs/contracts/world-authoring-bundle-v0.md); and
- [Action mechanic declaration v0](../docs/contracts/action-mechanic-declaration-v0.md).

Draft/open work that is useful but not roadmap authority:

- PR #37 — Warehouse Rush experiment; retained evidence, v1 retry pending, currently deferred behind live projection.
- PR #43 — bounded CVS sustainment integration from a separate track; rebase/review before merge.

## Risks and needs resolution

| Priority | Risk / open need | Current stance |
| --- | --- | --- |
| P1 | living prototype is disconnected from canonical runs | active slice: live read-only projection |
| P1 | information representation/delivery is not first-class generic world semantics | next generic capability after projection |
| P1 | causal ancestry can be overstated if observation/context is treated as hard cause | explicitly separate causal, delivery, evidence, analysis relations |
| P1 | generated world may name consequential dependencies that no mechanic enforces | build bounded dependency inventory + closure/counterexample loop |
| P2 | current integer-tick loop cannot express independent cadences/duration-bearing activities efficiently | add a canonical simulated timeline + minimal activity contract from Coordination-Lab pressure; use SimPy only as scheduler |
| P2 | generic authoring lacks rich scheduled processes/meetings/institutions | add from Coordination-Lab pressure, not schema completeness |
| P2 | generic live actions are not semantically closed against Linguistic Core | retain as explicit gap; close when it blocks richer authoring/review |
| P2 | no durable resident cognition | Pydantic AI selected; integrate when correct worlds need persistent minds |
| P2 | no saved user worlds/run history | use standard persistence after workflow earns it |
| P2 | mechanic/process exceptions are not yet first-class causal failure events | fix when it affects evidence trust/debugging |
| P2 | approval is not identity-bound and Builder is not authenticated | decide before consequential persistent user worlds |
| P3 | read scopes not runtime-enforced | optional measured verification, not current blocker |
| P3 | distributed/massive scale not demonstrated | defer; use mature systems/patterns when real pressure appears |
| upstream | `unheat` lacks suitable pinned Linguistic Core sense | donor-owned semantic gap |

## Human decisions

| Decision | Status |
| --- | --- |
| Canonical project is World Substrate | answered — Decision 001 |
| Observability required; exact replay not universal | answered — Decision 002 |
| Semantics do not imply effects | answered — Decision 003 |
| Product face | answered — generative living worlds over causal engine |
| First serious application vertical | answered — Coordination Environment Lab / Waltzman-inspired case |
| Waltzman constructs in core state? | answered — no; detachable analytic plugin |
| Behavioral predictive validity current goal? | answered — no; internal/plausible causal coherence first |
| Commodity selection method | answered — research/reason/select, not local bake-offs |
| Living renderer | answered — deck.gl 9.4.x |
| Resident cognition harness | answered — Pydantic AI 2.41.x behind adapter |
| Scheduler | answered — SimPy 4.1.2 for scheduling only |
| Time model direction | answered — one canonical simulated timeline; process/institution/activity cadences independent; render/cognition/analysis cadences separate |
| Cognition cadence | answered — event/meaning-driven wakeups by default, not one LLM deliberation per low-level simulation step |
| Graph inspector | answered — Cytoscape.js 3.34.x when needed |
| Deployed living-world prototype | explicitly authorized and live |
| Public demo vs authenticated authoring | still open |

## Refresh and reset triggers

Refresh this roadmap when:

- the living client consumes its first real World Substrate run;
- first-class information/conversation semantics are accepted;
- a scheduled process/institution authoring need produces a concrete multi-timescale/activity contract;
- the first real world uses independent process cadences or duration-bearing activities;
- a dependency/closure report detects and repairs a missing law;
- Pydantic AI is integrated behind the cognition seam;
- the Coordination Lab vertical completes a real World Substrate run;
- persistence/auth changes product authority; or
- evidence contradicts a current truth statement.

Replan rather than extend blindly if:

- live projection requires presentation to invent canonical facts;
- generated mechanics routinely require arbitrary model-written code;
- information and cognition cannot be separated without leaking observer truth;
- causal closure repair effort grows faster than useful world complexity;
- an external dependency requires surrendering Engine consequence authority; or
- a new feature does not purchase trustworthy evidence or immediate product throughput.

## Exact next action

**Build the live-projection vertical. Do not run another framework comparison or another toy-world experiment first.**

Use Repair Bay or another already-retained real run. Define the smallest read-only projection representation needed to drive the versioned prototype, then replace the prototype's synthetic timeline with canonical snapshot/event data. Preserve stable entity/event IDs and current scene semantics. Add one-way incremental delivery (SSE is enough) only after the retained-run projection is correct.

Acceptance is exact agreement between UI-visible state/event identity and the full retained run, with no renderer-specific canonical state and no invented information/causal links. If that vertical succeeds, the next slice is first-class information/conversation semantics; only after that should the Coordination Lab require richer process/institution/cognition features.
