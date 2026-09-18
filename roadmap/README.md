---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-18
---

# World Substrate living roadmap

**Authority:** [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md), [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md), and [Decision 005](../docs/decisions/005-native-waltzman-delivery.md).
**Stage:** prototype substrate complete; deployed authoring/run alpha; promoted donor-backed Waltzman demo retained; active phase is **native Waltzman convergence: description -> editable World Substrate draft -> approved mechanics -> native Engine run -> automatic living UI -> bounded inspection/comparison**.
**Current frontier:** establish the first configurable native coordination vertical and prove that two materially different coordination configurations run through the same World Substrate mechanics and automatic-view path. Preserve the promoted donor experience as regression/fallback while the native path is built; do not make donor hosting migration, conversational editing, bespoke assets, Jev optimization, or a repo merger part of this critical path.
**Deployment boundary:** the 2026-09-09 donor-backed promotion remains valid evidence and a fallback surface. The 2026-09-18 product decision now targets World Substrate as the native substrate for the next Waltzman release. Public cutover waits until the native description-to-view path meets Decision 005's stopping rule; the existing donor route must not be silently presented as a fresh native run if generation fails.

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

### Current showcase world — Waltzman Coordination Lab

The demo is a **World Substrate product demo**. **Waltzman Coordination Lab is the showcase/reference world used to demonstrate it**, inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*. Cybernetic Influence remains research lineage, not the product surface.

The demo makes the product thesis visible end to end: a bounded coordination world runs under canonical executable mechanics; residents receive asymmetric represented information, communicate through represented channels, act under resource/process/institution constraints, and evolve on one canonical simulated timeline; the user watches and interrogates that world through the living client; and Waltzman trust/risk/readiness analysis remains detachable analysis rather than hidden universal world state.

Waltzman remains a **reviewed reference world** for the living-view/causal semantics, but the stakeholder demo is no longer limited to replaying it. The promoted visitor-facing release accepts a natural-language situation and runs a fresh generated simulation through the bounded Cybernetic V3 donor path. Public presentation must keep that implementation boundary truthful rather than implying the current World Builder generated the donor run.

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

These criteria are now satisfied for the promoted stakeholder slice through the retained reference world plus the donor authoring/fresh-run path. Durable saved user worlds/runs, broad second-domain proof, generalized institution authoring, massive scale, persistent cognition, generic future-event scheduling, and predictive validity remain outside that completed promotion gate.

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
- The current `SemanticBinding` object is a World Substrate profile over pinned Linguistic Core meaning: it cites a reviewed LC sense and role identities, then adds World-Substrate-owned specialization, causal classification, bearer, mechanic identity, and interpretation limits. `unheat` remains deliberately unbound rather than minting an unsupported LC sense.
- Linguistic Core's fact-oriented design already targets typed n-ary facts, objectification, and richer role semantics. Future adoption of a more explicit predicate-local role-definition contract can strengthen World Substrate's semantic bindings without moving persistence, effects, scheduling, authority, or commit semantics into Linguistic Core.
- The constrained causal declaration/compiler path is deployed: model proposes data, local compiler derives authority, a human explicitly approves, then an ordinary frozen declaration profile runs through the Engine.
- `MechanicProfile.freeze()` gives the package/declaration set a stable ID; future durable generated-law provenance should additionally fingerprint the exact executable law plus compiler/interpreter version.
- Every live Builder diagnosis starts from complete request/response logs and retained causal traces; summaries/replay are orientation surfaces only.
- Repair Bay proved nontrivial generated law can compile and a bounded LLM policy can reach terminal without a heavier cognition framework.
- Warehouse Rush v0 exposed a real law/representation omission (`route` did not enforce physical dock); v1 represents `target_dock`. Draft PR #37 retains the experiment; its provider retry is deferred.
- The deployed World Builder is `https://brianmills.dev/world-builder/`.
- The promoted stakeholder surface is `https://brianmills.dev/waltzman/`, served through the Cybernetic V3 donor path with a temporary Mac origin pending approved shared Netcup VPS migration.
- The standalone visualization URL still serves the synthetic prototype. It is retained as a legacy/public design surface rather than the exact next product action.
- `evidence/renders/waltzman-demo-v0.html` remains a self-contained canonical reference client with embedded baseline/intervention projection bundles; it is regression/reference evidence, not the outreach endpoint.
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
- [Semantic–mechanical binding v0](../docs/contracts/semantic-mechanical-binding-v0.md): downstream profile over pinned Linguistic Core senses/roles; meaning and consequence authority remain separate.

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
| Waltzman reference-world demo | implemented local | coherent living coordination world with detachable analysis; retained as presentation/evidence fixture |
| Waltzman outreach authoring/run path | existing donor capability | Cybernetic V3 public V2 path supports prose -> editable configuration -> approval -> fresh run -> retained evidence |
| Waltzman outreach + living replay | implemented donor integration | Cybernetic V3 Plans 37–38 provide the first-two-minute funnel and read-only living replay over retained general-run summaries |
| Waltzman stakeholder demo | **promoted 2026-09-09** | `65eb465a` public donor build; separated Sol authoring/execution certification; approved fresh `general_world_v2` run `run_0e488a37157f`; desktop/mobile living replay verified |
| Shared Netcup VPS migration | **active** | move the donor backend off the temporary Mac origin without changing the promoted product contract; preserve the Mac as rollback |
| Provenance/authority/repro hardening | queued post-demo | exact law fingerprint, role-specific scopes, visible action-space overflow, appropriate CI/locking |
| Semantic binding alignment | later / when earned | consume richer LC role/relation representation without moving mechanics or effects into LC; close real vocabulary gaps rather than minting local `lc:` senses |
| Persistence / second-domain proof | later | durable user worlds/runs and proof beyond Waltzman |

### Active slice — Netcup migration and post-demo authority hardening

The stakeholder demo is already promoted. The active slice is to preserve that product contract while removing the temporary Mac-origin dependency and then continue the bounded hardening queue.

The promoted regression target is:

```text
ordinary-language situation
      v
Cybernetic V3 public V2 authoring + coverage/review
      v
approved generated scenario/run
      v
Cybernetic V3 retained execution
      v
run summary / raw retained evidence
      v
World-Substrate-style living-view adapter
      v
residents + information + constraints + accepted/rejected changes
+ timeline + mechanic-declared ancestry + detachable Waltzman analysis
```

This remains an integration strategy, not a new product identity. **World Substrate is the product/demo surface.** Cybernetic V3 is a bounded implementation donor for mature authoring/execution capability. Do not expose two engines for the same run or imply that World Builder generated laws it did not generate.

#### Hosting migration sequence

1. **Preserve regression target:** retain donor commit `65eb465a48f8f1f996afd81f64105a99c982f070`, the approved fresh-run evidence, and current public behavior as the comparison target.
2. **Provision shared VPS:** deploy the existing donor backend on the approved shared Netcup VPS without reviving the closed Cloudflare Container path or changing the simulation/product contract.
3. **Certify before cutover:** verify health, route certification, retained-run access, browser network/console behavior, and rollback against the VPS origin.
4. **Cut over with rollback:** move the public route only after independent verification; retain the Mac origin until the VPS route is proven stable.
5. **Record outcome evidence:** refresh this roadmap and the derived wiki after the hosting result is retained; hosting changes must not be mistaken for a new simulator architecture.

#### Current hardening queue

After or independently of the hosting cutover where safe, continue small reversible changes:

1. fingerprint exact executable generated-law identity plus compiler/interpreter version for durable approval/run provenance;
2. bind action write-scope placeholders to exact action roles, not merely any named participant;
3. make authored affordance-space overflow explicit rather than silently truncating after the finite candidate cap;
4. add appropriate CI/project gates and exact dependency locking as external dependencies enter reproducible production paths; and
5. keep semantic closure honest: bind only reviewed Linguistic Core senses/roles, preserve `unheat` as unbound until an upstream reviewed sense exists, and treat future predicate-local role-definition support as semantic precision rather than consequence authority.

None of these requires reopening the product architecture.

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
| Semantic/mechanical binding | keep project-owned as a World Substrate profile over pinned Linguistic Core meaning |
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

### Semantic-profile rule

Linguistic Core contributes reusable meanings, role concepts, and semantic relationships. World Substrate may profile those meanings into local action/process bindings, but the profile owns only the bridge: specialization, causal classification, represented bearer, selected mechanic, and interpretation limits. A richer LC n-ary/role-definition contract may improve the semantic half of that bridge; it must not acquire World Substrate's persistence, effects, scheduling, write authority, or commit semantics.

### Approval / law provenance rule

A reviewer should ultimately be able to approve human-readable law and have that approval point to one exact executable law identity for the run. Current declaration-profile freezing is a partial implementation of this chain. Strengthen it before durable user-generated laws become long-lived/persisted; do not block the hand-authored Waltzman reference demo on it.

### Experiment-selection rule

- **Novel uncertainty:** experiment.
- **Commodity uncertainty:** research → reason → select.
- **Integration uncertainty:** prove the selected adapter conforms; do not run comparative framework tournaments.

## Evidence and review artifacts

Primary current artifacts:

- `https://brianmills.dev/world-builder/` — deployed authoring/run alpha;
- `https://brianmills.dev/waltzman/` — promoted stakeholder surface using the bounded Cybernetic V3 donor path;
- `https://brianmills.dev/world-substrate-visualization/` — legacy synthetic standalone surface; retained design evidence rather than active promotion target;
- `evidence/renders/waltzman-demo-v0.html` — self-contained canonical Waltzman reference client and regression fixture;
- `prototypes/living-world-overlay-v0.html` — retained synthetic design prototype;
- [Waltzman integrated demo audit](../docs/audits/waltzman-coordination-lab-v0.md) + `evidence/waltzman/`;
- [Information/delivery v0](../docs/contracts/information-delivery-v0.md) and [live projection v0](../docs/contracts/live-projection-v0.md);
- [Semantic–mechanical binding v0](../docs/contracts/semantic-mechanical-binding-v0.md);
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
| P0 | native authoring may not express Waltzman-class information/activity/institution constraints | prove two configurable native coordination worlds first; if generic generation is too narrow, use a reviewed reusable coordination-mechanics package rather than narrated consequences |
| P0 | the zero-review Automatic replay path and richer Waltzman Living Scene path may not compose directly | measure the smallest adapter/mapping from one actual native coordination run before redesigning either renderer |
| P1 | promoted donor-backed stakeholder demo still depends on a temporary Mac origin | keep it stable as regression/fallback; migrate only as an operational-continuity task, not as a blocker for the native World Substrate vertical |
| P1 | frozen profile does not yet fingerprint every executable determinant | add exact executable law + compiler/interpreter provenance |
| P1 | action placeholder write authority is participant-bounded rather than role-specific | bind placeholders to exact action fields |
| P1 | authored affordance discovery can hit a finite candidate cap | make overflow explicit/paged/refused rather than silent |
| P1 | repository production reproducibility needs stronger CI/locking | add as selected external dependencies become part of production manifests |
| P2 | generic live actions are not semantically closed against Linguistic Core | consume reviewed LC senses/roles when available; do not mint fake `lc:` senses locally; adopt richer role-definition support when it earns a real binding improvement |
| P2 | information v0 is intentionally narrow | extend only for demonstrated latency/corruption/audience needs |
| P2 | generic authoring cannot generate Waltzman's richer mechanics | use another concrete world to earn the smallest generic extension |
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
| Linguistic Core relation/role refinement moves causal mechanics upstream? | answered — no; LC may improve semantic relation/role representation while World Substrate retains persistence, effects, authority, scheduling, and commit semantics |
| Product face | answered — generative living worlds over causal engine |
| Causal claim boundary | answered — causal explanation is internal to installed represented-world mechanics; real-world validity is separate |
| Current prototype/deliverable | answered — Waltzman Coordination Lab demo |
| Integrated Waltzman first gate | answered — implemented/reviewed/landed |
| Public Waltzman demo | **answered — interactive natural-language generation + fresh run + living inspection; static replay alone is insufficient** |
| World Builder integration required for the fastest 2026-09-09 promotion? | answered — no; donor reuse was the fastest promotion path and remains valid historical evidence |
| Cybernetic V3 role going forward? | answered — donor, analysis/UX source, and temporary regression/fallback implementation lineage; not the required runtime for the native World Substrate product |
| Native World Substrate path for the next Waltzman release? | **answered 2026-09-18 — yes; World Substrate owns the draft/mechanics/Engine/history/UI path, with selected Cybernetic ideas promoted only when the Waltzman vertical needs them** |
| Waltzman richer mechanics generated by the current Builder today? | answered — no; this is the first active uncertainty to resolve with a configurable native coordination vertical |
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

- the first configurable native coordination vertical lands or exposes a mechanics/viewer gap;
- the native one-shot authoring flow first produces a fresh automatic-view run;
- the shared Netcup VPS migration completes or is materially blocked, if that migration is still operationally relevant;
- post-demo executable-law provenance/role-authority/affordance-overflow hardening lands;
- Linguistic Core publishes or adopts a relation/role contract that materially changes how World Substrate semantic bindings are represented;
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

**Establish the first configurable native coordination vertical and prove it renders automatically.**

Concretely:

1. preserve the promoted donor-backed `/waltzman/` experience and retained promotion evidence as regression/fallback; make no public-route change for this slice;
2. run two materially different coordination configurations through the same native World Substrate state/mechanics/Engine path so this is not merely renamed template content;
3. from those real runs, identify the smallest missing coordination-mechanics capability and the smallest adapter from retained history into the automatic generic UI;
4. retain a deterministic/no-spend native run and inspect actual failed/satisfied checks plus information visibility before adding prose generation on top; and
5. only after that native vertical is sound, connect one-shot natural-language drafting to the same versioned authoring artifact and approval path.

The acceptance target for the first vertical is narrower than the full product stopping rule: two different configurations execute natively, produce different consequential structure or parameters, and render through one generic automatic-view path without a hand-authored scene file.

Do **not** start with full conversational editing, bespoke generated art, a Cybernetic runtime port, generalized cognition/scheduling, Jev benchmarking, or a broad arbitrary-world benchmark. Let an observed Waltzman-blocking failure choose any extension.
