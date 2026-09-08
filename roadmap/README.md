---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-07
---

# World Substrate living roadmap

**Authority:** [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md), and [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md).  
**Stage:** prototype complete; deployed authoring/run alpha; next phase is product/semantic depth rather than more generic substrate breadth.  
**Current frontier:** prove the deployed Builder on a meaningfully less-trivial authored world, then close the semantic loop and evaluate off-the-shelf cognition/rendering only where the world exposes a real need.  
**Deployment boundary:** the current `brianmills.dev/world-builder/` deployment and its bounded LLM service were explicitly authorized. New deployment/publication or provider spend outside an already-approved bounded service remains an explicit human authority boundary.

## Outcome and success criteria

### End goal

Build **a sophisticated world-modeling system with one instantiation compelling enough to show**, while preserving a stronger causal contract than ordinary generative-agent demos.

The approved product thesis is now:

> **Generative-World Builder on top; rigorous causal world engine underneath.**

A person should be able to represent a world, define/ground the things that can happen, review generated causal law, run scripted or LLM residents, and watch the world evolve graphically. The world—not a narrator—owns what actually happened.

### Prototype phase — complete

The original prototype succeeds when it can:

1. represent persistent typed state;
2. expose bounded observations and state-derived affordances;
3. let scripted/human/LLM policies choose without consequence authority;
4. bind semantic intent separately from effects;
5. install/review mechanics under explicit local authority;
6. atomically commit or refuse causally coupled writes;
7. retain enough causal evidence to inspect failures and outcomes; and
8. transfer the substrate to a materially different world.

Those questions are answered. Exact replay remains an M1/debugging capability, not a universal project goal.

### Product-phase success criteria

The next phase succeeds when:

- a nontrivial world can be authored primarily through the product rather than bespoke repo surgery;
- newly authored actions carry reviewed semantic identity as well as causal law;
- generated mechanics are understandable enough for a human to approve/refuse with confidence;
- resident agents can maintain useful cognition without becoming world authority;
- graphical execution feels like a world rather than a trace viewer; and
- useful worlds/runs can persist without compromising causal provenance.

## Canonical outcome probe

M1 remains the canonical substrate probe: persistent actors/vessels, finite contaminated water, finite fuel, ownership/container/liquid/thermal/material state, actions and autonomous processes, atomic rejection, causal events, snapshots, and exact pinned replay.

M1 establishes the implemented `core-v0` seam. It does **not** establish universal physics, complete semantics, global causal closure, or a requirement that future worlds remain deterministic.

For current product behavior, the Kitchen/Greenhouse/Orchard evidence is more relevant than M1; M1 remains the substrate baseline rather than the active product experiment.

## Current truth

State, not milestone narrative:

- Canonical material truth lives in one `World`; policy text, UI, resident private cognition, and analysis are not alternate authorities.
- The engine enforces declared **write** scopes. Rule-facing discovery/check/progress/consequence/trigger hooks use detached state, and rules cannot write revision, commands, or causal history.
- Declared **read** scopes are recorded but not runtime-enforced; an optional recording/verification contract exists.
- Linguistic Core provides semantic senses/roles, not effects. Six of seven M1 action kinds are reviewed/bound; `unheat` remains upstream-unbound.
- Mechanic-profile installation checks declared surfaces but cannot prove causal completeness. Three complementary assay bases exist and all retain blind spots.
- Scripted, human-shaped, and LLM policy seams all remain outside consequence authority.
- Kitchen is the flagship watched world. Three same-model/prompt runs reproduced Bo completing at t9, releasing the knife for Ama at t10, Ama taking it at t11, and both orders completing at t17.
- One generic replay system now renders Kitchen, Castaway, Workshop, and Greenhouse. Automatic replay is the authoring baseline; Polished is optional art direction.
- Greenhouse proved the replay/authoring pipeline on a world created after the system existed, including a multi-entity `water` effect with no world-specific renderer branch.
- `world-substrate-authoring-bundle/v0` is the shared code-first/browser structural authoring format.
- `world-substrate-causal-model/v0` is the separate constrained causal companion. The model proposes JSON; the local compiler derives reads/writes and rejects unsupported paths/types/selectors before installation.
- The deployed World Builder can Generate Mechanics → show compiler review → require explicit approval → Run Scripted or Run with LLM → render the fresh trace graphically.
- The live LLM policy can select only engine-minted action IDs. Installed mechanics still determine consequences.
- The public service binds loopback behind Cloudflare, requires same-origin browser POSTs, rate-limits/serializes model calls, uses per-request caps, and enforces a persistent fail-closed `$0.50/day` reservation ledger.
- The product does not yet provide durable resident cognition, saved user worlds/runs, or identity-backed approval receipts.

## Applicable context

- [Decision 001](../docs/decisions/001-project-scope.md): this repository is the canonical applied project and executable-consequence authority.
- [Decision 002](../docs/decisions/002-observability-and-replay.md): attempts/refusals/consequences must remain inspectable; exact replay is optional outside the bounded evidence case.
- [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md): semantic predicates do not imply effects; resident cognition/analysis remain separate causal layers.
- [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md): Generative-World Builder front end; custom causal kernel; off-the-shelf systems around it when they preserve authority.
- [Source dispositions](../docs/source-dispositions.md): neighboring repositories remain donors/dependencies only through explicit adoption paths.

## Constraints and authorities

```text
represented state
  -> semantic intent / action signature
  -> reviewed semantic binding
  -> installed/constrained mechanic
  -> checks + proposed effects
  -> one Engine commit or refusal
  -> canonical state + causal event
  -> detachable replay / analysis
```

Hard constraints:

- policy prose cannot mutate canonical state;
- a mechanic cannot enlarge its own write authority;
- model-generated source is not a live-law fallback;
- composition/analytics cannot duplicate primitive effects;
- presentation coordinates/assets are not world truth;
- cognition frameworks may choose actions but not adjudicate consequences;
- external frameworks become dependencies only after a bounded consumer proof; and
- future generic work must answer a concrete world/product failure.

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it established |
| --- | --- | --- |
| M0 foundation | complete | canonical repo/navigation/authority |
| M1 freshwater | complete | neutral persistent transition substrate + replay |
| M2 give/exchange | complete | semantic binding + derived composite without duplicate effects |
| M3 mechanic authoring | complete | offline reviewed mechanic/profile workflow |
| M4 coherence assays | complete | multiple causal-closure evidence bases |
| M5 policy consumer | complete | LLM choosing through ordinary affordances |
| M6 second world | complete | cross-domain substrate reuse |
| M7/M7b model authoring | complete | generated and relational mechanics under bounded authority |
| Kitchen flagship | complete first gate | replicated scarce-resource coordination + polished replay |
| Generic replay | complete first gate | one renderer/profile system across real worlds |
| Greenhouse new-world proof | complete | post-system authoring + zero-review Automatic replay |
| Code-first + visual authoring | complete first gate | one authoring bundle across CLI/browser |
| Live causal authoring | complete first gate | model proposal → compiler → approval → fresh run |
| Nontrivial product-world proof | **next** | product/DSL/review failure discovery |
| Semantic closure for generic authoring | queued after product-world evidence | reviewed Linguistic Core sense/role mapping for new actions |
| Resident cognition / live-world feel | conditional next | compare lightweight vs off-the-shelf agent runtime |
| Saved worlds/runs | conditional next | durable product state/auth after workflow earns persistence |

### Active slice: nontrivial live authoring proof

Use the deployed World Builder as the authoring surface, not a bespoke repo fixture.

The test world should be materially richer than Orchard and should include enough structure to stress the current system—for example 3–5 actors, multiple resources/locations/goals, several action kinds, shared or contested objects, and at least one process or relationship-dependent effect.

**Chosen world: Repair Bay.** A zero-spend local preflight now proves the current language can run four technicians, three contested tools, three broken machines, matched parts, five action kinds, multi-entity repair, stale-revision contention, and a tool handoff to terminal in five turns. It also exposed and fixed one concrete fresh-world presentation-binding collision. This is a solvability/preflight baseline, not yet the deployed generated-mechanics review result; see [Repair Bay preflight](../docs/audits/repair-bay-live-preflight.md).

For each generated mechanic, review:

- semantic intent and participant meaning;
- actor/participant selectors;
- derived reads/writes;
- preconditions/checks;
- effects;
- terminal condition;
- stated limits/tests; and
- whether the graphical projection remains faithful to canonical state.

Run a zero-spend Scripted baseline first, then an LLM-selected run only under the approved bounded service. Record the **first concrete point** where the language, review UI, observation, policy cognition, or renderer cannot express/communicate the intended world.

Do not expand the causal language or swap frameworks pre-emptively. The failure is the input to the next design decision.

## Decisions and assumptions

### Product/adoption strategy

Accepted in [Decision 004](../docs/decisions/004-product-and-adoption-strategy.md):

| Layer | Posture |
| --- | --- |
| Canonical state / identity | keep project-owned |
| Transition kernel / authority / traces | keep project-owned |
| Causal declaration/compiler | keep project-owned |
| Semantic-mechanical binding | keep project-owned with Linguistic Core |
| Scene semantics | keep project-owned |
| Browser rendering execution | evaluate Phaser rather than grow a bespoke game engine |
| Resident cognition | compare lightweight custom runtime with Concordia/LangGraph adapters |
| Multi-agent evaluation | add PettingZoo adapter when useful; never alternate world authority |
| Persistence/auth | use standard infrastructure |
| Rich discrete-event scheduling | evaluate SimPy only after a demonstrated need |

Assumption to test: the causal kernel is the differentiator; rendering, cognition orchestration, auth, and persistence are leverage surfaces rather than strategic reasons to build from scratch.

## Evidence and review artifacts

Primary current evidence:

- [Kitchen audit](../docs/audits/kitchen-contested-world.md) + `evidence/kitchen/full-service-replication-v1-summary.json`;
- `evidence/renders/kitchen-spatial-replay-v1.html` and `kitchen-zero-review-v0.html`;
- [Greenhouse authoring proof](../docs/audits/greenhouse-authoring-proof.md) + `evidence/renders/greenhouse-zero-review-v0.html`;
- [Scene profile contract](../docs/contracts/scene-profile-v0.md) and replay/bootstrap audits;
- [World authoring bundle](../docs/contracts/world-authoring-bundle-v0.md) + starter/builder audits;
- [Action mechanic declaration](../docs/contracts/action-mechanic-declaration-v0.md);
- [Live authoring audit](../docs/audits/live-world-authoring.md); and
- deployed `https://brianmills.dev/world-builder/`.

Older M1–M7b evidence remains authoritative for the narrower claims it established; it should not be copied into the active product narrative unless needed to explain a current boundary.

Cost records are evidence-scope specific. Do not fabricate a single lifetime total by adding figures from observability stores that do not cover the same period.

## Risks and needs resolution

| Priority | Risk / open need | Current stance |
| --- | --- | --- |
| P1 | generic live actions can compile without reviewed Linguistic Core binding | close after nontrivial-world test clarifies authoring UX |
| P1 | mechanic/process implementation exceptions are rollback-safe but not yet explicit causal failure events | stabilization target |
| P1 | current public approval is a client assertion after review, not an identity-bound server receipt | decide before consequential/persistent worlds |
| P1 | Builder is public/same-origin but not user-authenticated | decide whether product is public demo vs private authoring surface |
| P2 | causal language is intentionally narrow | extend only from observed expressiveness failures |
| P2 | no persistent resident memory/planning/reflection | evaluate after nontrivial world needs it |
| P2 | no saved user worlds/run history | add after authoring loop proves persistence value |
| P2 | root deployment uses pinned source but a shared mutable Python dependency environment | make deployment more hermetic before broader reliance |
| P2 | permanent required CI is absent | stabilization target |
| P3 | declared read scopes not runtime-enforced | optional measured verification, not current blocker |
| P3 | global component registration remains process/import coupled | defer until a real isolation failure |
| upstream | `unheat` lacks suitable pinned Linguistic Core sense | donor-owned semantic gap |

## Human decisions

| Decision | Status |
| --- | --- |
| Canonical project is World Substrate | answered — Decision 001 |
| Observability required; exact replay not universal | answered — Decision 002 |
| Semantics do not imply effects | answered — Decision 003 |
| Flagship world | answered — Kitchen |
| First watched behavior | answered — scarce shared-resource coordination |
| Replay product baseline | answered — Automatic; Polished optional |
| Authoring surfaces | answered — code-first starter + browser Builder over one bundle |
| Live causal generation | answered — constrained declaration + local compiler + explicit approval |
| Product face | answered — Generative-World Builder over causal engine |
| Off-the-shelf posture | answered — keep causal kernel custom; evaluate commodity layers via adapters/spikes |
| Current World Builder deployment/model service | explicitly authorized and live |
| Public demo vs authenticated private authoring | **open** |
| First nontrivial product-test world/domain | **answered — Repair Bay** |

## Refresh and reset triggers

Refresh this roadmap when any of these happens:

- a nontrivial live-authored world exposes the first causal-language/review failure;
- a generic authored action gains required semantic binding;
- an off-the-shelf cognition/rendering/interoperability spike is accepted/rejected;
- saved-world persistence or authentication becomes implemented;
- the public deployment/security/spend boundary changes;
- a new reference world exposes substrate coupling; or
- evidence contradicts a current truth statement above.

Replan rather than extend blindly if:

- generated mechanics routinely require arbitrary code;
- human reviewers cannot understand/meaningfully approve the generated law;
- agent behavior needs private cognition that the current policy seam cannot support;
- the renderer prevents world legibility despite correct scene semantics; or
- off-the-shelf integration would require surrendering canonical consequence authority.

## Exact next action

**Human-test Repair Bay through the deployed World Builder.** Import `examples/world_authoring/repair-bay-v0.json`, generate constrained mechanics with optional guidance, inspect the compiler-derived authority and effects against the retained hand-reviewed baseline, approve only what matches the intended law, run Scripted first, then compare an LLM-selected run under the existing bounded service.

Retain the first concrete failure or ambiguity. Classify it as one of: semantic grounding, causal-language expressiveness, review comprehensibility, affordance/observation, resident cognition, graphical presentation, persistence/product UX, or deployment/security. That classification—not framework availability—determines the next implementation slice.

After that evidence, the expected sequence is: close semantic binding for generic actions; add explicit mechanic-error events/permanent CI/auth as warranted; run a bounded cognition-framework comparison; then consider Phaser/persistence work. Do **not** add arbitrary model-written code or generalize the renderer/DSL without a demonstrated need.
