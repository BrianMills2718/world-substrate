---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-07
---

# World Substrate living roadmap

**Authority:** user-approved direction in [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), and [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md)  
**Selected path:** durable solo; one writer; reversible branches; no deployment, publication, or model spend without explicit authority  
**Stage:** prototype complete; zero-review replay generation proven across Workshop, Castaway, and Kitchen
**Last outcome-bearing result:** Kitchen cleared the five-action zero-review breadth gate. Explicit `take`/`put_down`/`chop`/`cook`/`plate` presentation bindings resolve only trace-grounded fields; auto-layout supplies two actor homes, two burner/workstation scenes, two goal/order scenes, loose item homes and deterministic plated-item grids. The retained zero-review replay shows Bo's t10 release reasoning, Ama holding the knife at t11, and both orders complete at t17, with zero bootstrap TODOs. The polished flagship remains byte-for-byte unchanged. Functional zero-review generation is now established across all three real replay worlds in the repository.
**Superseded:** the flagship-world, viewer-surface, and first-impressive-behavior decisions are answered by the kitchen, the rendered reasoning-vs-world view, and scarce-resource coordination respectively; before that, the observation seam and authoring obligations were narrowed through M5–M7b.  
**Current strategy frontier:** human/product review of the automatic zero-review Kitchen default versus the polished flagship; no further replay-framework generalization without a new real-world failure or explicit product requirement; publication/deployment remains an explicit authority boundary

## Outcome and success criteria

### The end goal

**A sophisticated world-modelling system, with one instantiation good enough to
show off as the flagship.** Stated by Brian on 2026-09-04, in those terms.

Everything below it — the seven-bullet workflow and six numbered criteria — is
the *prototype phase*, and that phase is finished. Read the two as a sequence,
not as alternatives: the prototype asked "do these contracts hold?", and the
answer is yes. Phase two asks whether one world produces a robust, legible
behavior worth showing. The kitchen is the selected attempt; three fresh
replications have cleared the first robustness gate, so legibility is now the
immediate question.

A fresh agent should take three things from this section:

1. **"All six success criteria met" does not mean the project is done.** It
   means phase one is done.
2. **The flagship direction is no longer open.** The kitchen is the selected
   world; its rendered run is the selected viewer surface; the first behavior
   being tested is coordination over scarce shared resources between agents
   that cannot talk to each other.
3. **The first two reference worlds are deliberately small.** Castaway and the
   workshop were built to test whether the contracts work and transfer. The
   kitchen is the first world built to be watched rather than merely to prove a
   substrate property.

### What "sophisticated" and "show off" mean for the active experiment

The first choices have been made, reversibly:

- **World:** the kitchen, chosen from a measured weakness in the two-agent
  Castaway run rather than from domain taste.
- **Viewer surface:** a rendered trace showing each agent's stated reasoning
  beside the world state and causal outcome. Publication/deployment remains a
  separate authority boundary.
- **First impressive behavior:** two agents with no communication contending
  over one knife and zero-slack ingredients, yet partitioning resources,
  waiting, and handing over the bottleneck without being instructed to
  cooperate. Three fresh replications reproduced the handoff; the next gate is
  whether the evidence can explain itself to a viewer without project narration.

### The prototype phase, and its criteria (complete)

For a substrate developer and later a data-oriented world builder, change the recurring task of hand-coding isolated actions and narrating missing consequences into a reviewable workflow that:

- defines persistent typed world state;
- grounds intents in Linguistic Core senses and roles;
- binds causal primitives and processes to installed local mechanics;
- exposes state-derived affordances;
- validates and commits causally coupled effects once;
- makes attempts, refusals, assumptions, and consequences observable; and
- lets mechanics agents expand a world before a run through reviewable, frozen profiles.

The prototype succeeds when:

1. one reference world runs end to end through neutral substrate contracts;
2. the same semantic action interface can be exercised by scripted, human, or LLM policies without giving policy prose consequence authority;
3. ordinary composites and analytic patterns can be recognized without double-applying primitive effects;
4. one agent-authored adjacent mechanic is installed offline, frozen, and exercised with interaction evidence;
5. unsupported behavior and residual causal-closure risk remain visible; and
6. a second materially different world reuses the semantic, transition, and mechanic-profile contracts.

Exact replay, universal physics, predictive validity, complete linguistic coverage, and defining all mechanics up front are not success criteria.

## Canonical outcome probe

M1 remains the first implementation probe: two actors, persistent vessels, a finite pathogen-bearing freshwater source, a finite-fuel fire, and registered ownership, container, liquid, heat, material, and process rules.

The promoted trace exercises fill, heat, unheat, pour, drink, take, and give; advances canonical time; exposes finite water and fuel use, heat and pathogen changes, cross-system vessel identity, automatic processes, atomic rejection, and an exact replay hash.

That probe establishes the implemented `core-v0` seam. It does not establish:

- a general semantic compiler;
- a complete rights model;
- agent-authored mechanics;
- cross-domain reuse;
- global causal closure; or
- a requirement that future worlds replay exactly.

## Current truth

State, not history. Milestone narratives live in the milestone table and their
audits; findings live in the audit that produced them.

- This repository owns the project goal, decisions, architecture, contracts, source dispositions, and roadmap.
- M1 through M4 are complete and promoted. M1 is pinned at implementation revision `4c3303828b7c9b97e22a806caa404306f8616f7a`; its retained evidence remains authoritative for that claim.
- Contract status is mixed: `core-v0` is implemented; [mechanic profile](../docs/contracts/mechanic-profile-v0.md) and [transition envelope](../docs/contracts/transition-envelope-v0.md) are partially implemented; [semantic binding](../docs/contracts/semantic-mechanical-binding-v0.md) has six bindings of seven, with `unheat` unbound because the pinned extraction has no sense for it. Each contract states its own status.
- Ownership references are checked: `owner_ref` must be `<kind>:<target>`, enforced in `World.validate()` and refused at construction by `model.owner_ref()`.
- Declared **write** scopes are enforced by the engine (`scope_violation`; negative controls in `tests/test_write_scope.py`). Rule-facing discovery, checks, progress, consequences and triggers are isolated from canonical state, and engine-owned revision/history cannot be proposed by mechanics. Declared **read** scopes remain recorded and unenforced at runtime.
- Three interaction assays exist on three different bases — declarations, differential behaviour, conserved-quantity accounting. Each has a stated blind spot; no single basis and no pair is sufficient. Evidence: [M3](../docs/audits/m3-overheat-authoring-experiment.md), [M4](../docs/audits/m4-spill-experiment.md).
- Installation validates internal consistency and never completeness. A residual class of omission survives every check the repository has.
- **The kitchen has a terminal state without duplicating state.** `reference_worlds/kitchen/terminal.py` derives completion from the existing `order.filled` fields, and `run_contested_world.py` stops before another policy decision once every order is filled. New contested-run outputs use schema v3 and record whether the terminal was reached. The retained `full-service-v0` evidence remains a historical v2 run: its thirteen trailing turns are the observation that motivated this fix, not current runner behavior.
- **The complete service now replicates.** Three fresh post-terminal-state runs under the same model and prompt all filled Bo's order at t9, had Bo deliberately release the knife for Ama at t10, had Ama take it at t11, and reached world completion at t17. Actual contention was 1 in every run; stale retries varied 4/3/2 and zero attempts were refused after retry. The three service runs cost $0.028785. See [the kitchen audit](../docs/audits/kitchen-contested-world.md) and `evidence/kitchen/full-service-replication-v1-summary.json`.
- **The kitchen became watchable only after the policy could distinguish its actions.** `describe_action` originally rendered only Castaway participant vocabulary, collapsing several kitchen choices to the same word. Fixing that moved the run from blind churn toward purposeful waiting and completion; the audit records the sequence.
- **The kitchen was built against a measurement rather than a domain preference.** Under the same scripted policy it produces materially more contention than Castaway and does not inherit Castaway's long process waits.
- **The observation seam is a measured design variable.** Across the M5 comparison, exposing progress, destroyed value and mechanic warnings materially changed policy outcomes without changing the mechanics. The re-run then regenerated the same failure shape at the next hidden threshold, leaving the broader threshold-observation obligation open.
- A policy has driven this world (criterion 2, met): an LLM chose actions only through the ordinary affordance seam and never received consequence authority.
- A second, materially different world reuses the contracts (criterion 6, met). **All six prototype success criteria are met.** The workshop shares no content with Castaway; substrate contracts transferred while Castaway mechanics did not.
- The declaration language expresses one relation between entities, making cross-entity authored behavior and meaningful authored write-scope violations possible.
- Doctrine, unchanged: Linguistic Core supplies senses and roles, not effects; consequences require a represented causal bearer and an installed mechanic; composites stay derived; observability is required while exact replay is not a universal gate; mechanics authoring is offline and runtime law revision is deferred; donor repositories stay read-only unless a consumer path explicitly adopts code.

## Applicable context

- [Decision 001](../docs/decisions/001-project-scope.md) establishes the canonical project and executable-consequence boundary.
- [Decision 002](../docs/decisions/002-observability-and-replay.md) makes observability required and exact replay optional outside M1.
- [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md) establishes Linguistic Core binding, causal bearers, derived composites, and offline mechanics authoring.
- Castaway remains the adopted M1 implementation donor; other classified repositories remain idea, theory, contract, or failure-analysis donors.
- The proposed contracts describe the target seam and do not claim implementation.

## Constraints and authorities

```text
observable attempt or trigger
  <- resident policy or autonomous bearer
  -> Linguistic Core sense and role binding
  -> installed local mechanic
  -> proposed effects + checks
  -> one canonical commit or refusal
  -> persistent state + causal trace
  -> detachable analysis
```

- One canonical persistent state owns material world truth.
- Natural language and policy models cannot directly mutate it.
- Local mechanics have enforced write authority; declared read scopes are recorded and may be verified separately.
- One enclosing transition owns each causally coupled commit, including revision and causal-history attachment.
- Independent actions may commit independently.
- Resident cognition and post-run analysis are not canonical world authorities.
- Invariants and accounting are goal-relative to the selected representation.
- Passing declared-contract checks does not prove the author named every consequential dependency.

## Vertical slices and current work

### Milestone horizon

| Milestone | State | Inspectable output | Promotion or replan trigger |
| --- | --- | --- | --- |
| M0: canonical foundation | complete | repository authorities, navigation, checks | established |
| M1: freshwater vertical | complete | neutral CLI trace, refusals, persistence, and M1 replay | promoted |
| M2: semantic/causal give vertical | complete | Linguistic Core binding for `give`; two independent gives derivable as exchange without duplicate effects | promoted |
| M3: offline mechanics-authoring vertical | complete | authored mechanic package, frozen profile, and interaction evidence | promoted |
| M4: causal-coherence assay | complete | three assays on different bases plus negative control | promoted |
| M5: policy consumer | complete | LLM selecting only from `discover()` against a mechanical baseline | promoted |
| M5b: installed institution | deprioritized | escrow-like bearer couples effects through one transition envelope | revisit only when a world needs an institution |
| M6: second reference world | complete | materially different workshop world reusing substrate contracts | promoted |
| M7: authoring rate | complete | model-authored mechanics graded against fixed criteria | promoted |
| M7b: relational authoring | complete | authored mechanics using one cross-entity relation | promoted |
| M8: scale and dynamical evaluation | deliberately_deferred | measurements or perturbation studies that can change a design decision | activate only when a real world exposes the need |

### Active slice: generate replay scenes from declarations, not bespoke code

**Complete for the current real replay worlds.** Workshop, Castaway, and Kitchen
all retain functional profiles/replays generated from world model + retained
trace + explicit shared presentation catalog + deterministic auto-layout with no
per-world review overlay.

The three proofs exercise materially different structure:

- Workshop: `pick_up`/`attach`, assembly relation, multi-item station placement;
- Castaway: `fill`/`drink`, source activation, vessel state, initial actor ownership;
- Kitchen: five action kinds, two actors, two goal stations, two workstations,
  staged ingredients, shared knife ownership, and the replicated t10→t11 handoff.

Kitchen's default is intentionally plain, but at t10 Bo's recorded reasoning says
he releases the knife so Ama can use it; t11 shows Ama holding it; t17 shows both
orders complete. `kitchen-spatial-replay-v1.html` remains the polished flagship
and regenerates byte-for-byte unchanged.

**Engineering conclusion.** The requested architecture now exists: represented
world + retained behavior + explicit reusable assets/presentation semantics can
produce a graphical replay without a bespoke renderer or per-world review file.
Optional scene reviews remain valuable for product quality, not correctness or
basic generation.

**What a fresh agent should do first.** All cost nothing:

1. Compare `kitchen-zero-review-v0.html` with `kitchen-spatial-replay-v1.html`.
2. Read the Workshop, Castaway, and Kitchen zero-review audits before changing the scene contract.
3. Only reopen generic replay architecture when a new real world or explicit product requirement exposes a concrete gap.

**What not to do.** Do not add more generic projection/layout primitives merely
for completeness. Do not collapse polished presentation into inferred world
truth. Deployment/publication remains separately controlled.

## Open obligations

Work an accepted decision or contract already requires, which no milestone
currently owns. Listed here so it is schedulable rather than resident only in
the audit that found it.

| Obligation | Required by | State |
| --- | --- | --- |
| ~~Attach the causal bearer's observation to its event~~ | Decision 002 | **closed.** Captured before mutation and attached as `observation`; `null` for a process |
| ~~Attach the bound Linguistic Core sense and roles to its event~~ | Decision 002 | **closed.** Attached as `semantic_binding` where a reviewed binding exists |
| ~~Name the authority/causal bearer on an event~~ | Decision 002 | **closed.** Attached as `causal_bearer` |
| Bind the remaining M1 action kinds to Linguistic Core senses | Decision 003 | **six of seven closed.** `unheat` remains upstream-owned because the pinned extraction has no matching sense |
| ~~Decide the ledger's shape for lost quantities~~ | M4 finding | **closed.** `spilled` is a full `LiquidState` and conservation checks can cover represented quantities |
| ~~Decide whether `World.clone()` should deep-copy the event log~~ | performance review | **closed.** Ordinary world clones share append-only committed event objects for performance; rule-facing execution now receives detached state without engine history, so mechanics cannot rely on or mutate that optimization boundary |
| Enforce declared read scopes at runtime | roadmap invariant | **designed, not implemented** — [read-scope enforcement v0](../docs/contracts/read-scope-enforcement-v0.md) specifies an optional recording verification pass rather than always-on overhead |
| ~~Surface process progress in the observation~~ | M5 finding | **closed.** Processes may declare current-against-required progress |
| ~~Signal that an action destroys existing value~~ | M5 finding | **closed.** Actions may declare consequences surfaced per affordance |
| ~~Make `owner_ref` a typed reference~~ | M7 finding | **closed.** Reference shape is validated and construction goes through `model.owner_ref()` |
| ~~Refuse authored writes a field's type forbids~~ | M7 generalisation | **closed.** Declaration paths and literal types are checked against component dataclasses |
| ~~Give the world a way to say "unowned"~~ | M7b finding | **closed.** Reserved `unowned` literal |
| Surface progress toward *leaving* a threshold, not only toward reaching one | M5 re-run finding | **open.** Cooling toward a safe-drinking threshold remains the concrete case |

**All eight Decision 002 observability fields are covered on every event class.**
Malformed envelopes record a `claimed_actor` bearer rather than pretending an
unvalidated identity is authoritative.

## Authoring and causal-closure hypothesis

The central test is whether agent teams can add useful, coherent mechanics faster than interaction risk grows.

An agent-authored package must include semantic bindings, causal bearer, applicability, local authority, proposed effects, goal-relative invariants, dependencies, interaction cases, unsupported combinations, limits, and a trace contract. Passing isolated tests is insufficient.

The compiler or installer can establish declared enforcement coverage. Causal closure remains a fallible assay because an author may omit a dependency entirely. Mechanics agents should inspect neighboring semantic state, search for unbound consequential relations, generate counterexamples, and label residual risk.

## Decisions and assumptions

| Choice | Disposition | Boundary |
| --- | --- | --- |
| Observability over universal replay | human-set in Decision 002 | product evidence |
| Linguistic Core as semantic interface | human-set in Decision 003 | semantics, not effects |
| Offline pre-run mechanics authoring | human-set direction | runtime law changes deferred |
| Kitchen as first flagship world | answered 2026-09-04 | reversible product direction |
| Rendered reasoning beside world truth as viewer surface | answered | publication/deployment remains separate |
| Scarce-resource coordination as first impressive behavior | answered | 3/3 fresh replications cleared the first robustness gate; viewer legibility is current |
| Second reference-world domain | answered: workshop (M6) | complete |

## Evidence and review artifacts

| Claim | Evidence | Limitation | Status |
| --- | --- | --- | --- |
| M1 freshwater behavior works | retained machine/human receipts, probes, tests, and replay | deterministic scripted vertical only | established |
| M1 exact replay works | fresh-process replay receipt | M1 property, not product requirement | established |
| Semantic binding works | `semantic.py` plus binding/event tests | `unheat` remains unbound upstream | established, narrow |
| Derived exchange avoids double application | M2 reciprocal/reneging cases | ordinary voluntary exchange only | established |
| Declared write scopes are enforced | write-scope and rule-authority negative controls | reads remain separately declared and unenforced | established |
| Offline mechanics authoring works | M3/M4 packages and assays | bounded experiments | established |
| Interaction assays surface omitted dependencies | M3/M4 findings | every basis has blind spots | established with residual risk |
| A policy can drive the world | M5 audit and retained trace | one model/prompt/world slice | met |
| Global causal closure is proven | none | not generally decidable from author declarations | rejected claim |
| Second-world reuse works | M6 audit and workshop tests | one materially different second world | met |
| Kitchen service and knife handoff repeat under the fixed configuration | three fresh v3 traces plus retained `full-service-v0` | same model, prompt and world; execution-layer caveat documented in audit | **replicated 3/3 fresh runs** |
| Kitchen runner ends at represented completion | `terminal.py`, terminal tests, scripted runner smoke test | terminal condition is world-specific by design | established |
| Generic scene renderer projects retained traces into 2D world replays | `scripts/render_scene_replay.py`, `scene-profile-v0.md`, Kitchen + Castaway + Workshop profiles, lab tests | v0 is 2D and v3-envelope-oriented | **established on three real worlds; multi-item station layout closed generically** |
| Scene-profile bootstrapper reduces review-only authoring | bootstrapper + shared presentation catalog + Workshop/Castaway/Kitchen zero-review audits | zero-review defaults are plain; optional polish remains | **zero-review functional on all three real replay worlds; Workshop polish 34.3%** |
| Graphical flagship replay shows a retained terminal service as a world | generic renderer + kitchen scene profile + spatial replay tests + `evidence/renders/kitchen-spatial-replay-v1.html` | spatial geometry is illustrative; one replicated trace; no external human review yet | established technically, human review pending |
| Trace-oriented flagship timeline explains the same service | `scripts/render_kitchen_service.py`, renderer tests, `evidence/renders/kitchen-flagship-v1.html` | static read-only view of one replicated trace | established technically |

## Risks and needs resolution

- The kitchen handoff repeated in 3/3 fresh same-model/prompt runs, but robustness across models, prompts, or changed world conditions is still unknown.
- The flagship viewer has passed renderer tests and local visual inspection, but no external human has yet established that it is self-explanatory without project context.
- Linguistic breadth can hide mechanical sparsity.
- A generic component model can become an untyped property bag.
- Broad LLM adjudication can bypass local causal authority.
- Individually valid mechanics can disagree about units, timing, identity, capability revocation, or overlapping effects.
- Declared dependencies can create false confidence when consequential state was never declared.
- Coarse organizational or social surrogates can double-count detailed lower-level mechanisms.
- Documentation can outrun implementation; proposed contracts must remain labeled.

## Human decisions

Boundaries only Brian can clear. Answered choices remain here for traceability rather than being re-presented as blockers.

| Decision | State | What it means now |
| --- | --- | --- |
| Model execution and a spend cap | **answered 2026-09-04: $2 cap granted** | replication is complete; scene-profile portability work needs no model spend |
| Which second reference world | **answered: workshop, promoted in M6** | reuse criterion met |
| Which world becomes the flagship | **answered: kitchen** | current work stays on the kitchen unless evidence replans it |
| What a viewer actually sees | **answered: zero-review defaults exist for Workshop/Castaway/Kitchen; polished Kitchen remains the flagship** | productization/publication is now a human boundary, not a renderer gap |
| What "sophisticated" means first | **answered: scarce-resource coordination without communication** | behavior replicated and viewer built; human review is current |
| Deployment and publication | **open authority boundary** | do not publish or deploy without explicit permission |

## Refresh and reset triggers

Refresh this roadmap after an outcome-bearing slice, a material user correction, an accepted decision, a selected donor revision, or evidence that invalidates a contract. Replan after two consecutive non-vertical increments or when a later milestone no longer tests the central hypothesis.

## Exact next action

**Human-review the automatically generated Kitchen default beside the polished
flagship.** Compare `evidence/renders/kitchen-zero-review-v0.html` with
`evidence/renders/kitchen-spatial-replay-v1.html` and decide whether the
zero-review generation path is accepted as the authoring baseline and whether a
specific product surface/refinement should be authorized next. Do not add more
generic replay machinery without a new real-world failure or an explicit
presentation requirement.

Publishing or deploying either artifact still requires explicit authority. No
additional model call is needed for this review.

The historical pre-replication roadmap recorded **$0.123** of model spend. The
current single-copy observability DB no longer contains that older task history;
it records **$0.029571** for the compatibility probe and three-run replication
session. Keep those figures separate rather than replacing the historical
lifetime number with a falsely lower current-DB total or manually inventing a
new lifetime total.
