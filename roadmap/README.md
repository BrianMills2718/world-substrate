---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-08
---

# World Substrate living roadmap

**Authority:** [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md), and [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md).  
**Stage:** prototype substrate complete; deployed authoring/run alpha; integrated Waltzman Coordination Lab first gate implemented/reviewed/landed; current phase is **public canonical demo publication**.
**Current frontier:** make the small truth-label cleanup, replace the existing standalone synthetic visualization with the already-implemented canonical Waltzman client at the same public URL, smoke-test it, and stop. Do not widen the framework to ship this demo.
**Deployment boundary:** the 2026-09-08 human product decision explicitly authorizes replacing the existing standalone synthetic visualization with the canonical Waltzman demo at `https://brianmills.dev/world-substrate-visualization/`. World Builder integration is not required for this demo. Other new publication surfaces, provider spend outside the bounded Builder service, or runtime-generated-law installation outside the reviewed path still require explicit human authority.

## Outcome and success criteria

### End goal

Build a **generatively authored, reviewable, persistent simulation platform for plausible worlds**. A user describes a bounded world conversationally; the system compiles represented structure and executable law; the user reviews important assumptions and causal coverage; residents/processes inhabit the world; the world evolves under installed mechanics; and the user watches and interrogates the result through a dynamic visual surface.

The product thesis remains:

> **Generative worlds with executable laws.**
> Generative-World Builder on top; rigorous causal world engine underneath.

### Causal product contract

A World Substrate causal claim explains why a transition occurred **inside the represented world under the installed mechanics that governed that run**.

That is not, by itself, a claim that those mechanics are scientifically or empirically true of the corresponding real-world system. Predictive validity, calibration, and real-world causal identification require separate evidence.

Current `causal_parent_event_ids` are **mechanic-declared hard causal ancestry** validated against retained history. They are not inferred merely from temporal order or prompt/context inclusion, but the runtime also does not yet derive them automatically from instrumented reads.

The current Waltzman adequacy surface is a **bounded dependency inventory**: declared consequential assumptions are mapped to represented state and installed enforcement surfaces, with residual risk. It is not counterfactual proof of necessity/sufficiency. Stronger automatic counterfactual/mutation verification is deferred unless later evidence makes it worth building.

### Current deliverable — Waltzman Coordination Lab demo

The concrete deliverable is the **Waltzman Coordination Lab demo**, inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*.

The demo makes the product thesis visible end to end: a bounded coordination world runs under canonical executable mechanics; residents receive asymmetric represented information, communicate through represented channels, act under resource/process/institution constraints, and evolve on one canonical simulated timeline; the user watches and interrogates that world through the living client; and Waltzman trust/risk/readiness analysis remains detachable analysis rather than hidden universal world state.

Waltzman is currently a **reviewed reference world**. The current World Builder does not yet conversationally generate all of its richer hand-written information/activity/institution mechanics. Public presentation must not imply otherwise.

Generality remains an architectural constraint and later validation target, not the immediate deliverable. Predictive behavioral validity is not a current promotion gate.

### Prototype phase — complete

The substrate phase has established:

1. persistent typed canonical state;
2. bounded actor observations and state-derived affordances;
3. scripted/human/LLM selection outside consequence authority;
4. semantic/mechanical separation;
5. reviewed/frozen declaration profiles;
6. atomic commit/refusal with write-scope enforcement;
7. retained causal evidence and full-log debugging; and
8. transfer to multiple materially different worlds.

### Waltzman demo acceptance criteria

The first public Waltzman demo succeeds when one coherent scenario demonstrates all of the following through the real World Substrate path:

1. **Real living world:** the graphical client is driven by canonical World Substrate snapshots/events rather than a synthetic timeline, with stable entity/event identity and no presentation-owned world truth.
2. **Represented information:** residents receive different information through explicit source/recipient/channel/provenance/visibility semantics; delivery and observation remain distinct from hard causal ancestry.
3. **Resident interaction:** residents communicate and select bounded attempts through the policy seam while the Engine and installed mechanics retain consequence authority.
4. **Coordination constraints:** consequential outcomes depend on represented resources/process/institution state rather than model narration alone.
5. **One simulated timeline:** the scenario expresses its required trigger ticks and duration-bearing meeting without making render time or cognition cadence canonical world time.
6. **Inspectable causality:** the user can inspect mechanic-declared hard parentage, information/context evidence, state changes, and refusals without collapsing those categories.
7. **Waltzman analysis is detachable:** trust/risk/readiness proxies can be recomputed/hidden without altering canonical state/history.
8. **Intervention/fork proof:** the user can compare the blocked baseline with a represented exact-history intervention branch without rewriting the original history.
9. **Bounded dependency report:** the scenario exposes consequential dependency assumptions, their represented/enforcement mappings, known unsupported relationships, and residual risk without claiming counterfactual proof or global completeness.
10. **Demo continuity:** the full scenario is understandable as one public product experience rather than disconnected repository assays.

Durable saved user worlds/runs, broad second-domain proof, generalized institution authoring, massive scale, persistent cognition, generic future-event scheduling, and predictive validity are **not** required for the first public Waltzman demo.

## Canonical outcome probe

M1 remains the neutral substrate baseline: persistent actors/vessels, finite resources, autonomous processes, atomic rejection, causal events, snapshots, and exact pinned replay. It proves the core seam; it is not the product destination.

Current product fixtures have narrower roles:

- **Kitchen** — replicated watched-world behavior and polished/Automatic presentation.
- **Greenhouse** — post-renderer new-world portability and multi-entity effects.
- **Orchard** — live authoring acceptance fixture.
- **Repair Bay** — first nontrivial deployed authoring world.
- **Warehouse Rush** — retained draft evidence of a real generated-law/representation omission and minimal repair; not active roadmap work.
- **Waltzman Coordination Lab** — current integrated product deliverable and public demo.

## Current truth

State, not milestone narrative:

- One `World` owns canonical material truth. Policy prose, UI animation state, resident private cognition, and analysis are not alternate authorities.
- Engine write scopes are enforced. Declared read scopes are retained but not runtime-enforced.
- Current action write-scope placeholder binding is participant-bounded but not yet role-specific.
- Linguistic Core supplies semantic senses/roles, not effects. Generic live authoring can still compile actions before semantic closure is complete.
- The constrained causal declaration/compiler path is deployed: model proposes data, local compiler derives authority, a human explicitly approves, then an ordinary frozen declaration profile runs through the Engine.
- `MechanicProfile.freeze()` gives the package/declaration set a stable ID; future durable generated-law provenance should additionally fingerprint the exact executable law plus compiler/interpreter version.
- Every live Builder diagnosis starts from complete request/response logs and retained causal traces; summaries/replay are orientation surfaces only.
- Repair Bay proved nontrivial generated law can compile and a bounded LLM policy can reach terminal without a heavier cognition framework.
- Warehouse Rush v0 exposed a real law/representation omission (`route` did not enforce physical dock); v1 represents `target_dock`. Draft PR #37 retains the experiment; its provider retry is deferred.
- The deployed World Builder is `https://brianmills.dev/world-builder/`.
- The standalone visualization URL still serves the synthetic prototype, but replacement with the canonical Waltzman client is now explicitly authorized and is the exact next product action.
- `evidence/renders/waltzman-demo-v0.html` is already a self-contained canonical client with embedded baseline/intervention projection bundles. The public first demo therefore does not require a continuously running simulation backend.
- `scripts/waltzman_demo_service.py` additionally exposes the same projection over JSON/SSE and remains an optional observer/live seam.
- `world_substrate.information` implements bounded first-class information/delivery v0 with source, recipient, channel, visibility, delivery status, provenance linkage, and actor-local asymmetric visibility.
- Rules/processes can opt into `causal_parent_event_ids`; these are mechanic-declared and history-validated, not inferred from message history or prompt context.
- The Waltzman fixture has a represented two-tick meeting, tick-specific autonomous prerequisite changes, an installed coalition gate, and a forked stabilization intervention.
- The Waltzman bounded dependency report maps eight declared consequential assumptions to represented/enforcement surfaces and retains explicit residual risk; automatic counterfactual/mutation proof is not implemented or required for the demo.
- The core time/process runtime remains integer-tick `Engine.advance()` + `due(world)`. Generic SimPy future-event scheduling is not implemented because the current scenario does not require it.
- Persistent resident memory/planning, generic rich process/institution authoring, saved user worlds/runs, and conversational generation of Waltzman's richer mechanics remain later work.
- Open PR #43 (CVS sustainment seam) is a separate integration track and does not define this roadmap.

## Applicable context

- [Decision 001](../docs/decisions/001-project-scope.md): this repository is canonical executable-consequence authority.
- [Decision 002](../docs/decisions/002-observability-and-replay.md): important attempts/refusals/consequences remain inspectable; exact replay is not universal.
- [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md): semantic predicates do not imply effects; cognition and analysis remain distinct layers.
- [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md): own causal reality; borrow commodity cognition/rendering/scheduling/graph infrastructure.
- [Architecture](../docs/architecture.md): causal claims are internal to the represented world/model; real-world validity requires separate evidence.
- [Living-world projection](../docs/research/living-world-projection-2026-09.md): current visualization/overlay semantics and public integration path.
- [Technology procurement](../docs/research/technology-procurement-2026-09.md): selected external defaults and conformance boundaries.
- [Competitive landscape](../docs/research/competitive-landscape-2026-09.md): adjacent systems and the "own reality; borrow minds" positioning.
- [Source dispositions](../docs/source-dispositions.md): neighboring repositories are donors/evidence unless explicitly adopted.

## Constraints and authorities

```text
conversational authoring
  -> represented state + dependency intent
  -> reviewed semantic/action structure
  -> constrained/generated mechanics
  -> local compiler + approval + frozen declaration profile
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
- information delivery/context must not automatically become hard causal parentage;
- causal claims about the represented world must not be marketed as automatic real-world causal truth;
- the current adequacy inventory must not be marketed as counterfactual proof;
- commodity selection is not a reason for local framework bake-offs; and
- generic breadth must buy real product/evidence value rather than exist for completeness.

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it establishes |
| --- | --- | --- |
| M0–M7b substrate/generative mechanics | complete | persistent governed world + authoring/compiler/policy seams |
| Kitchen + generic replay | complete first gate | watched-world behavior + portable read-only visualization |
| Greenhouse/Orchard | complete first gate | new-world presentation + live generated-law authoring |
| Repair Bay | complete first gate | nontrivial deployed authoring and LLM inhabitant proof |
| Warehouse Rush | retained draft evidence | law/representation failure discovered and minimally repaired |
| Commodity procurement | complete | deck.gl / Pydantic AI / SimPy / Cytoscape defaults selected |
| Living-world visual prototype | complete prototype | desired interaction/overlay model established |
| Waltzman live projection | implemented local first gate | canonical snapshot/event deltas reconstruct both branches; static HTML + JSON/SSE |
| Waltzman information/conversation | implemented v0 first gate | asymmetric source/recipient/channel/provenance/visibility + context evidence |
| Waltzman timeline/activity | implemented scenario first gate | tick-specific processes + represented two-tick meeting |
| Waltzman institution/intervention | implemented scenario first gate | explicit commitments + coalition gate + exact-history stabilization fork |
| Waltzman bounded dependency report | implemented v0 | eight declared dependency mappings + residual risk; no global/counterfactual proof |
| Waltzman integrated demo | implemented local / publication next | coherent living coordination reference world with detachable analysis |
| Public canonical Waltzman demo | **active** | replace synthetic standalone surface with real canonical client |
| Provenance/authority/repro hardening | next after demo | exact law fingerprint, role-specific scopes, visible action-space overflow, appropriate CI/locking |
| Persistence / second-domain proof | later | durable user worlds/runs and proof beyond Waltzman |

### Active slice — public canonical Waltzman demo

The product-surface decision is answered. The current slice is **publication**, not another architecture decision.

Use the existing canonical path:

```text
canonical Waltzman World
      |
      +--> scheduled prerequisite changes + asymmetric information delivery
      +--> bounded resident choices + represented communication/commitments
      +--> duration-bearing meeting + installed coalition gate
      +--> blocked baseline
      +--> exact-history intervention fork -> restored prerequisites -> reassessment -> ready gate
      v
initial snapshot + retained canonical event/deltas
      v
world-substrate-live-projection/v0
      v
self-contained Waltzman client
      v
https://brianmills.dev/world-substrate-visualization/
```

#### Before-demo implementation sequence

1. **Truth-label cleanup:** change the public-facing adequacy language from “proved/enforced” style wording to “declared dependencies mapped to installed enforcement surfaces,” and label parent edges as mechanic-declared hard causal parents where needed.
2. **Regenerate/verify:** regenerate `evidence/renders/waltzman-demo-v0.html` from the canonical baseline/intervention bundles and pass the existing Waltzman checks.
3. **Publish:** replace the existing standalone synthetic page at the already-authorized public visualization URL with the canonical static Waltzman artifact. Retain `prototypes/living-world-overlay-v0.html` as design evidence.
4. **Smoke-test:** verify load, baseline/intervention switching, play/pause/step/scrub, information/causal/constraint/Waltzman overlays, and absence of synthetic stage data.
5. **Stop the slice:** do not add Builder integration, Pydantic AI, SimPy, persistence, or a new graph inspector to complete this demo.

The JSON/SSE service may remain available for local/observer integration, but running it publicly is not required for the first standalone demo because the generated HTML already embeds the canonical projection data.

#### Immediately after demo

Harden the broader product in small independent changes:

1. fingerprint exact executable generated-law identity plus compiler/interpreter version for durable approval/run provenance;
2. bind action write-scope placeholders to exact action roles, not merely any named participant;
3. make authored affordance-space overflow explicit rather than silently truncating after the finite candidate cap; and
4. add appropriate CI/project gates and exact dependency locking as external dependencies enter reproducible production paths.

These are clear engineering tasks. None requires reopening the product architecture.

#### Deliberately deferred

- automatic counterfactual/mutation causal-adequacy verification;
- always-on read-scope enforcement;
- persistent resident cognition;
- generic SimPy future-event scheduling;
- conversational generation of Waltzman's richer institution/activity/information mechanics;
- saved user worlds/auth; and
- massive/distributed scale.

Promote one only when a concrete product/evidence need earns it.

## Decisions and assumptions

### Product/adoption strategy

| Layer | Current posture |
| --- | --- |
| Canonical state / identity | keep project-owned |
| Transition kernel / authority / trace semantics | keep project-owned |
| Causal declaration/compiler | keep project-owned |
| Semantic/mechanical binding | keep project-owned with Linguistic Core |
| Dependency inventory / bounded adequacy | project-owned; current v0 is mapping + residual risk, not counterfactual proof |
| Scene/projection semantics | keep project-owned; renderer stays downstream |
| Living browser rendering | deck.gl 9.4.x selected; MapLibre optional for real geography |
| Resident cognition | Pydantic AI selected behind `CognitionAdapter`; integrate only when earned |
| Simulated scheduling | SimPy selected for event/time scheduling only; integrate only when earned |
| Activity duration | project-owned semantic/causal contract when earned; completion rechecks current world |
| Expanded graph inspection | Cytoscape.js selected when needed |
| Multi-agent evaluation | PettingZoo later if useful; never alternate world authority |
| Persistence/auth | standard commodity infrastructure later |

### Information / causality rule

Do not collapse these relationships:

- **world interaction** — e.g. Mara speaks to Ari;
- **information lineage** — representation, source, recipient, channel, delivery/observation;
- **cognition context/evidence** — information the resident harness was shown;
- **mechanic-declared hard causal ancestry** — parent dependencies explicitly named by installed transitions and validated against history; and
- **analytic interpretation** — post-run/observer inference.

Temporal precedence or prompt inclusion is never sufficient to label an information event a hard cause of a resident decision.

### Adequacy rule

Current bounded adequacy answers:

> Which consequential assumptions did we explicitly inventory, where are they represented, which installed rule surfaces are intended to enforce them, and what known residual risk remains?

It does **not** yet answer:

> Have we automatically proven each dependency necessary and sufficient by counterfactual intervention?

The latter is a deferred research option.

### Approval / law provenance rule

A reviewer should ultimately be able to approve human-readable law and have that approval point to one exact executable law identity for the run. Current declaration-profile freezing is a partial implementation of this chain. Strengthen it before durable user-generated laws become long-lived/persisted; do not block the hand-authored Waltzman public demo on it.

### Experiment-selection rule

- **Novel uncertainty:** experiment.
- **Commodity uncertainty:** research → reason → select.
- **Integration uncertainty:** prove the selected adapter conforms; do not run comparative framework tournaments.

## Evidence and review artifacts

Primary current artifacts:

- `https://brianmills.dev/world-builder/` — deployed authoring/run alpha;
- `https://brianmills.dev/world-substrate-visualization/` — current synthetic standalone surface; selected for canonical Waltzman replacement;
- `evidence/renders/waltzman-demo-v0.html` — self-contained canonical Waltzman client selected for publication;
- `prototypes/living-world-overlay-v0.html` — retained synthetic design prototype;
- [Waltzman integrated demo audit](../docs/audits/waltzman-coordination-lab-v0.md) + `evidence/waltzman/`;
- [Information/delivery v0](../docs/contracts/information-delivery-v0.md) and [live projection v0](../docs/contracts/live-projection-v0.md);
- [Living-world projection research](../docs/research/living-world-projection-2026-09.md);
- [Technology procurement](../docs/research/technology-procurement-2026-09.md);
- [Repair Bay live proof](../docs/audits/repair-bay-live-preflight.md) + retained traces;
- [Live authoring audit](../docs/audits/live-world-authoring.md);
- [Kitchen audit](../docs/audits/kitchen-contested-world.md) and retained renders;
- [Scene profile v0](../docs/contracts/scene-profile-v0.md);
- [World authoring bundle v0](../docs/contracts/world-authoring-bundle-v0.md); and
- [Action mechanic declaration v0](../docs/contracts/action-mechanic-declaration-v0.md).

Draft/open work that is useful but not roadmap authority:

- PR #37 — Warehouse Rush experiment; retained evidence and provider retry deliberately deferred behind the public demo.
- PR #43 — bounded CVS sustainment integration from a separate track; rebase/review before any merge decision.

## Risks and needs resolution

| Priority | Risk / open need | Current stance |
| --- | --- | --- |
| P0 | public standalone visualization is still synthetic | replacement with canonical Waltzman static client is authorized; execute now |
| P0 | public wording could overstate adequacy/parentage | small truth-label cleanup before publication; no new causal machinery |
| P1 | frozen profile does not yet fingerprint every executable determinant | add exact executable law + compiler/interpreter provenance after demo |
| P1 | action placeholder write authority is participant-bounded rather than role-specific | bind placeholders to exact action fields after demo |
| P1 | authored affordance discovery can hit a finite candidate cap | make overflow explicit/paged/refused rather than silent after demo |
| P1 | repository production reproducibility needs stronger CI/locking | add as selected external dependencies become part of production manifests |
| P2 | information v0 is intentionally narrow | extend only for demonstrated latency/corruption/audience needs |
| P2 | generic authoring cannot generate Waltzman's richer mechanics | use another concrete world to earn the smallest generic extension |
| P2 | generic live actions are not semantically closed against Linguistic Core | close when it blocks real authoring/review |
| P2 | no durable resident cognition | Pydantic AI selected; integrate only when needed |
| P2 | no saved user worlds/run history | later, after workflow earns persistence |
| P2 | mechanic/process exceptions are not first-class failure events | fix when it materially affects evidence trust/debugging |
| P3 | read scopes not runtime-enforced | optional verification design exists; not current blocker |
| P3 | automatic counterfactual adequacy proof not implemented | explicitly deferred idea |
| P3 | distributed/massive scale not demonstrated | defer until measured pressure |
| upstream | `unheat` lacks suitable pinned Linguistic Core sense | donor-owned semantic gap |

## Human decisions

| Decision | Status |
| --- | --- |
| Canonical project is World Substrate | answered — Decision 001 |
| Observability required; exact replay not universal | answered — Decision 002 |
| Semantics do not imply effects | answered — Decision 003 |
| Product face | answered — generative living worlds over causal engine |
| Causal claim boundary | answered — causal explanation is internal to installed represented-world mechanics; real-world validity is separate |
| Current prototype/deliverable | answered — Waltzman Coordination Lab demo |
| Integrated Waltzman first gate | answered — implemented/reviewed/landed |
| Public standalone demo | **answered — replace synthetic surface with canonical Waltzman client at existing URL** |
| World Builder integration required for first public demo? | answered — no |
| Waltzman richer mechanics generated by current Builder? | answered — no; present Waltzman as reviewed reference world |
| Adequacy needs full counterfactual machinery before demo? | answered — no; current mapped dependency inventory + residual risk is sufficient, stronger verification deferred |
| Exact executable-law fingerprint required before Waltzman demo? | answered — no; important post-demo hardening for durable generated-law provenance |
| Waltzman constructs in universal core state? | answered — no; Waltzman analytics detachable |
| Behavioral predictive validity current goal? | answered — no |
| Commodity selection method | answered — research/reason/select, not local bake-offs |
| Living renderer | answered — deck.gl 9.4.x |
| Resident cognition harness | answered — Pydantic AI behind adapter when earned |
| Scheduler | answered — SimPy for scheduling only when earned |
| Time model direction | answered — one canonical timeline; independent mechanism cadences |
| Graph inspector | answered — Cytoscape.js when needed |

## Refresh and reset triggers

Refresh this roadmap when:

- the canonical Waltzman client replaces the public synthetic standalone surface;
- post-demo executable-law provenance/role-authority/affordance-overflow hardening lands;
- conversational authoring first produces richer information/activity/institution mechanics;
- a new dependency-inventory counterexample exposes an in-scope gap;
- a scenario earns resident cognition or a future-event queue;
- persistence/auth changes product authority; or
- evidence contradicts a current truth statement.

Replan rather than extend blindly if:

- live projection requires presentation to invent canonical facts;
- generated mechanics routinely require arbitrary model-written code;
- information and cognition cannot be separated without leaking observer truth;
- causal-adequacy work grows faster than useful world complexity;
- an external dependency requires surrendering Engine consequence authority; or
- a new feature is proposed only for completeness rather than a concrete product/evidence need.

## Exact next action

**Publish the canonical Waltzman demo at the existing standalone visualization URL.**

Concretely:

1. make the small public truth-label cleanup for adequacy and mechanic-declared causal parentage;
2. regenerate and verify `evidence/renders/waltzman-demo-v0.html` from the canonical projection bundles;
3. replace the existing synthetic standalone page at `https://brianmills.dev/world-substrate-visualization/` with that static canonical artifact;
4. smoke-test the public experience; and
5. stop the demo slice.

Do **not** add World Builder integration, Pydantic AI, SimPy, persistence, counterfactual causal machinery, or generic framework breadth to ship this demo. After publication, begin the independent provenance/authority/reproducibility hardening tasks listed above.