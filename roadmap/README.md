---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-08
---

# World Substrate living roadmap

**Authority:** [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md), and [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md).  
**Stage:** prototype substrate complete; deployed authoring/run alpha; integrated local Waltzman Coordination Lab demo first gate implemented; current phase is review, hardening, and authorized product-surface integration.
**Current frontier:** validate and land the integrated Waltzman demo as one canonical World Substrate vertical. The local implementation now covers read-only snapshot/event projection, asymmetric information, explicit hard-causal parents, scenario-driven cadence/duration, a represented coalition institution, a forked stabilization intervention, detachable Waltzman analysis, and bounded causal-adequacy reporting. Do not add generic breadth unless review of this demo exposes a concrete gap.
**Deployment boundary:** the existing World Builder and standalone visualization prototype are authorized/public. New publication surfaces, provider spend outside the bounded Builder service, or runtime-generated-law installation outside the reviewed path still require explicit human authority.

## Outcome and success criteria

### End goal

Build a **generatively authored, reviewable, persistent simulation platform for plausible worlds**. A user describes a bounded world conversationally; the system compiles represented structure and executable law; the user reviews the important assumptions and causal coverage; residents/processes inhabit the world; the world evolves under installed mechanics; and the user watches and interrogates the result through a dynamic visual surface.

The product thesis remains:

> **Generative worlds with executable laws.**
> Generative-World Builder on top; rigorous causal world engine underneath.

### Current deliverable — Waltzman Coordination Lab demo

The concrete prototype/deliverable for the current phase is the **Waltzman Coordination Lab demo**, inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*.

This is not merely a later target vertical after generic platform work. The current roadmap is organized around shipping this demo. Live projection, first-class information/conversation semantics, multi-timescale processes and activities, institutions, resident cognition, bounded causal-closure reporting, and intervention/fork workflows are enabling slices to be added only as the Waltzman scenario requires them.

The demo should make the product thesis visible end to end: a bounded coordination world runs under canonical executable mechanics; residents receive asymmetric represented information, communicate through represented channels, act under resource/process/institution constraints, and evolve over one canonical simulated timeline; the user watches and interrogates that world through the living client; and Waltzman trust/risk/readiness analysis attaches as detachable analysis rather than hidden universal world state.

Generality remains an architectural constraint and later validation target, but it is not the immediate deliverable. Avoid generic breadth work that does not directly purchase Waltzman-demo evidence, trustworthy causal semantics, or immediate product throughput.

Predictive behavioral validity is not a current promotion gate. The current objective is internally coherent, inspectable worlds under explicit assumptions, with the Waltzman demo serving as the demanding product proof.

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

### Waltzman demo acceptance criteria

The current phase succeeds when one coherent Waltzman Coordination Lab scenario demonstrates all of the following through the real World Substrate path:

1. **Real living world:** the graphical client is driven by canonical World Substrate snapshots/events rather than a synthetic timeline, with stable entity/event identity and no presentation-owned world truth.
2. **Represented information:** residents can receive different information through explicit source/recipient/channel/provenance/visibility semantics; delivery and observation are distinguishable from hard causal ancestry.
3. **Resident interaction:** residents can communicate and select bounded attempts through a cognition/policy seam while the Engine and installed mechanics retain consequence authority.
4. **Coordination constraints:** at least one consequential outcome depends on represented shared resources, process state, permissions/commitments, deadlines, or another institutional constraint rather than model narration alone.
5. **One simulated timeline:** the scenario can express the minimum independent cadences and duration-bearing activities required by the demo without making render time or cognition cadence canonical world time.
6. **Inspectable causality:** the user can select important events/outcomes and inspect mechanically supported ancestry, information lineage/context evidence, state changes, and refusals without collapsing those categories.
7. **Waltzman analysis is detachable:** trust/risk/readiness or related Waltzman measures can be enabled, disabled, or recomputed without altering canonical state/history or primitive effects.
8. **Intervention/fork proof:** the user can change at least one represented condition or intervention and compare a resulting branch/run without silently rewriting the original history.
9. **Bounded causal-adequacy report:** the authored scenario exposes consequential dependency assumptions, the mechanisms that enforce them, known unsupported relationships, and residual risk rather than claiming global completeness.
10. **Demo continuity:** the full scenario can be launched and understood as one product experience rather than a collection of disconnected repository assays or bespoke renderer paths.

Durable saved user worlds/runs, broad second-domain proof, generalized institution schema breadth, massive scale, and predictive behavioral validity are not required for the first Waltzman demo unless the scenario itself proves they are necessary.

## Canonical outcome probe

M1 remains the neutral substrate baseline: persistent actors/vessels, finite resources, autonomous processes, atomic rejection, causal events, snapshots, and exact pinned replay. It proves the core seam; it is not the product destination.

Current product fixtures have narrower roles in service of the Waltzman deliverable:

- **Kitchen** — replicated watched-world behavior and polished/Automatic presentation.
- **Greenhouse** — post-renderer new-world portability and multi-entity effects.
- **Orchard** — live authoring acceptance fixture.
- **Repair Bay** — first nontrivial deployed authoring world and current live-projection stepping stone.
- **Warehouse Rush** — retained draft experiment showing scalar/physical semantic gaps and full-log-driven repair; not the active roadmap.
- **Waltzman Coordination Lab** — current integrated product deliverable and capability driver.

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
- The authorized public standalone visualization at `https://brianmills.dev/world-substrate-visualization/` remains the earlier synthetic prototype. Separately, the repository now has an integrated local Waltzman living client driven by `world-substrate-live-projection/v0` snapshot/event data; replacing the public surface is a deployment decision, not an implementation assumption.
- `world_substrate.information` now implements a bounded first-class information/delivery v0 with source, recipient, channel, visibility, delivery status, provenance linkage, and actor-local asymmetric visibility. Retained actor observations may surface `information_context` without turning it into hard causal ancestry.
- Rules/processes can now opt into explicit `causal_parent_event_ids`; parentage is mechanically declared rather than inferred from temporal order or prompt context.
- The Waltzman fixture has a represented two-tick meeting, tick-specific autonomous prerequisite changes, an installed coalition gate, and a forked stabilization intervention. These prove the scenario's required cadence/duration/institution seam without claiming a generic future-event scheduler.
- [Living-world projection research](../docs/research/living-world-projection-2026-09.md) defines the current visual semantics: one spatial world, dynamic core overlays, analytic plugins, and a strict distinction between information lineage and hard causal ancestry.
- Commodity procurement is settled by Decision 004: deck.gl 9.4.x for living projection; Pydantic AI 2.41.x behind `CognitionAdapter`; SimPy 4.1.2 for scheduling only; Cytoscape.js 3.34.x for expanded graph inspection.
- The selection doctrine is **novel uncertainty → experiment; commodity uncertainty → research/reason/select; integration uncertainty → conformance test**.
- The core time/process runtime remains the integer-tick `Engine.advance()` + `due(world)` baseline. The Waltzman first gate uses that canonical timeline for independent scheduled triggers and one represented duration-bearing activity; a generic future-event/SimPy scheduler remains unimplemented because this scenario does not require it.
- Persistent resident memory/planning, generic rich process/institution authoring, saved user worlds/runs, and conversational generation of the new Waltzman-specific richer mechanics remain unimplemented. The first integrated demo uses the existing bounded policy seam rather than adding cognition framework complexity it does not need.
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
- hardening/generic breadth must buy Waltzman-demo evidence, trustworthy causal semantics, or immediate product throughput.

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it establishes for the Waltzman demo |
| --- | --- | --- |
| M0–M7b substrate/generative mechanics | complete | persistent governed world + authoring/compiler/policy seams |
| Kitchen + generic replay | complete first gate | watched-world behavior + portable read-only visualization |
| Greenhouse/Orchard | complete first gate | new-world presentation + live generated-law authoring |
| Repair Bay | complete first gate | nontrivial deployed authoring and LLM inhabitant proof |
| Warehouse Rush | retained draft evidence | law/representation failure discovered and minimally repaired |
| Commodity procurement | **complete** | deck.gl / Pydantic AI / SimPy / Cytoscape defaults selected |
| Living-world visual prototype | **complete prototype** | desired interaction/overlay model is publicly inspectable |
| Waltzman slice 1 — live projection seam | **implemented local first gate** | canonical snapshot/event deltas reconstruct both branches exactly; JSON + SSE observer seam |
| Waltzman slice 2 — information/conversation | **implemented v0 first gate** | asymmetric represented source/recipient/channel/provenance/visibility + observation context |
| Waltzman slice 3 — timeline/process/activity | **implemented scenario first gate** | tick-specific processes + one represented two-tick meeting on canonical time; generic scheduler still later |
| Waltzman slice 4 — institutions | **implemented scenario first gate** | explicit commitments + represented coalition gate consume canonical state/events |
| Waltzman slice 5 — cognition adapter | **not required for first gate** | existing bounded policy seam is sufficient; persistent cognition remains later if earned |
| Waltzman slice 6 — causal adequacy + intervention | **implemented first bounded gate** | eight dependency mappings, residual risk, exact-history fork + represented stabilization intervention |
| Waltzman integrated demo | **implemented local first gate / current deliverable** | one coherent living coordination scenario with detachable Waltzman analysis and retained evidence |
| Persistence / second-domain proof | later | durable user worlds/runs and proof of generality beyond Waltzman |

### Active slice — Waltzman integrated demo review and product integration

The first integrated local Waltzman gate is now implemented. The active work is to review and harden this one vertical rather than starting another capability expansion.

Implemented flow:

```text
canonical Waltzman World
      |
      +--> scheduled prerequisite changes + asymmetric information delivery
      |
      +--> bounded resident policy choices + represented communication/commitments
      |
      +--> duration-bearing meeting + installed coalition gate
      |
      +--> blocked baseline
      |
      +--> exact-history intervention fork -> restored prerequisites -> resident reassessment -> ready gate
      |
      v
initial snapshot + retained canonical event/deltas
      |
      v
read-only projection / JSON / SSE
      |
      v
living client + detachable Waltzman analysis + bounded adequacy report
```

Current acceptance evidence:

1. both baseline and intervention branches replay exactly through the Engine;
2. snapshot + retained deltas reconstruct each final material world and hash exactly;
3. information can be delivered asymmetrically and appears separately as observation/context evidence;
4. hard causal parents are explicitly declared by mechanics/processes and are not inferred from message history;
5. the represented two-tick meeting must complete before the coalition institution evaluates;
6. the baseline blocks at 2 support / 4 conditional, while the forked stabilization intervention reaches 6 / 0 and `ready`;
7. Waltzman trust/risk/readiness proxies are computed as detachable observer analysis and do not mutate the world;
8. the bounded adequacy report maps eight declared consequential dependencies to enforcement and retains explicit residual risk; and
9. the interactive client is data-driven by the same projection bundles exposed over the one-way SSE service.

Primary retained evidence is in `evidence/waltzman/`, `evidence/renders/waltzman-demo-v0.html`, and [the Waltzman audit](../docs/audits/waltzman-coordination-lab-v0.md).

The authorized public standalone visualization still shows the earlier synthetic prototype. Do not replace/deploy a public surface without the separate deployment authority already required by this repository. If public integration is authorized, use the implemented projection/SSE seam rather than reintroducing synthetic stage data.

Persistent Pydantic-AI cognition and a generic SimPy future-event scheduler are deliberately **not** blockers for this first gate: the accepted scenario proves resident selection through the existing policy seam and its required duration/cadence through canonical ticks. Add either dependency only when a reviewed scenario demonstrates a need that this implementation cannot meet.

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
| Resident cognition | Pydantic AI 2.41.x selected behind `CognitionAdapter`; integrate only when the Waltzman scenario earns it |
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

- **Novel uncertainty:** experiment. Primary example: bounded generative causal closure in the Waltzman scenario.
- **Commodity uncertainty:** research → reason → select. Renderer/model/harness/library selection normally lives here.
- **Integration uncertainty:** prove the adapter seam conforms; do not run a comparative architecture tournament.

## Evidence and review artifacts

Primary current artifacts:

- `https://brianmills.dev/world-builder/` — deployed authoring/run alpha;
- `https://brianmills.dev/world-substrate-visualization/` — deployed living-world interaction prototype;
- `prototypes/living-world-overlay-v0.html` — versioned source for that prototype;
- [Living-world projection research](../docs/research/living-world-projection-2026-09.md);
- [Technology procurement](../docs/research/technology-procurement-2026-09.md);
- [Waltzman integrated demo audit](../docs/audits/waltzman-coordination-lab-v0.md) + `evidence/waltzman/` + `evidence/renders/waltzman-demo-v0.html`;
- [Information/delivery v0](../docs/contracts/information-delivery-v0.md) and [live projection v0](../docs/contracts/live-projection-v0.md);
- [Repair Bay live proof](../docs/audits/repair-bay-live-preflight.md) + `evidence/repair-bay/live-experiment-v0-summary.json`;
- [Live authoring audit](../docs/audits/live-world-authoring.md);
- [Kitchen audit](../docs/audits/kitchen-contested-world.md) and retained renders;
- [Scene profile v0](../docs/contracts/scene-profile-v0.md);
- [World authoring bundle v0](../docs/contracts/world-authoring-bundle-v0.md); and
- [Action mechanic declaration v0](../docs/contracts/action-mechanic-declaration-v0.md).

Draft/open work that is useful but not roadmap authority:

- PR #37 — Warehouse Rush experiment; retained evidence, v1 retry pending, currently deferred behind integrated Waltzman-demo review.
- PR #43 — bounded CVS sustainment integration from a separate track; rebase/review before merge.

## Risks and needs resolution

| Priority | Risk / open need | Current stance |
| --- | --- | --- |
| P1 | authorized public visualization is still the synthetic prototype | local canonical projection/SSE is implemented; public replacement requires deployment authority |
| P1 | information v0 is intentionally narrow | first-class source/recipient/channel/visibility/delivery/provenance is implemented; extend only for demonstrated latency/corruption/audience needs |
| P1 | causal ancestry can be overstated if observation/context is treated as hard cause | implemented separate `information_context` and opt-in `causal_parent_event_ids`; keep this separation in every new mechanic/UI |
| P1 | generated world may name consequential dependencies that no mechanic enforces | first Waltzman bounded report maps eight dependencies with zero in-scope gaps; generative closure/repair remains the research frontier |
| P2 | integer-tick loop may become inefficient for richer independent schedules | first Waltzman gate proves tick-specific triggers + represented duration; add SimPy only when a later scenario earns a future-event queue |
| P2 | generic authoring cannot yet generate the richer Waltzman information/activity/institution mechanics | keep the hand-authored accepted fixture as evidence; extend authoring only after demo review identifies the smallest useful language addition |
| P2 | generic live actions are not semantically closed against Linguistic Core | retain as explicit gap; close when it blocks Waltzman authoring/review |
| P2 | no durable resident cognition | Pydantic AI selected; integrate when the Waltzman scenario requires persistent minds |
| P2 | no saved user worlds/run history | not required for first Waltzman demo unless intervention/fork UX proves persistence necessary; otherwise later |
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
| Current prototype/deliverable | answered — Waltzman Coordination Lab demo |
| Role of Repair Bay/live projection | answered — Repair Bay was a stepping stone; canonical Waltzman projection is now implemented locally |
| Integrated Waltzman first gate | answered — implemented locally; current work is review/landing and authorized product integration |
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

- review of the integrated Waltzman first gate accepts it or materially revises an acceptance criterion;
- the canonical Waltzman projection replaces or integrates with an authorized public product surface;
- conversational authoring first produces the richer information/activity/institution mechanics used by the demo;
- a new causal-closure counterexample exposes an in-scope enforcement gap or repairs one;
- a scenario earns Pydantic AI resident cognition or a SimPy-backed future-event queue;
- persistence/auth changes product authority; or
- evidence contradicts a current truth statement.

Replan rather than extend blindly if:

- live projection requires presentation to invent canonical facts;
- generated mechanics routinely require arbitrary model-written code;
- information and cognition cannot be separated without leaking observer truth;
- causal closure repair effort grows faster than useful world complexity;
- an external dependency requires surrendering Engine consequence authority; or
- a new feature does not purchase Waltzman-demo evidence, trustworthy causal semantics, or immediate product throughput.

## Exact next action

**Review and land the integrated Waltzman demo first gate; do not start another generic framework/capability expansion.**

Run `python scripts/run_waltzman_demo.py --check`, inspect the retained baseline/intervention traces, causal-adequacy report, and `evidence/renders/waltzman-demo-v0.html`, then use the existing full repository check. Resolve any review finding against the Waltzman acceptance criteria rather than broadening schemas preemptively.

After this implementation is accepted, the next product decision is whether/where to publish it: replace or integrate with the already-authorized standalone visualization and/or World Builder using the implemented read-only projection/SSE seam. That is a deployment/publication authority decision. If deployment is not yet authorized, keep the verified local demo as the current deliverable and move only on concrete findings from review.
