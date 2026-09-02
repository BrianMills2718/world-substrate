---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-02
---

# World Substrate living roadmap

**Authority:** user-approved direction in [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), and [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md)  
**Selected path:** durable solo; one writer; reversible branches; no deployment, publication, or model spend without explicit authority  
**Stage:** prototype  
**Last outcome-bearing implementation:** promoted M1 freshwater vertical  
**Current strategy frontier:** semantic/mechanical integration and the first mechanics-authoring experiment

## Outcome and success criteria

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

- This repository owns the project goal, decisions, architecture, contracts, source dispositions, and roadmap.
- M1 is promoted at implementation revision `4c3303828b7c9b97e22a806caa404306f8616f7a`; its retained evidence remains authoritative for that claim.
- `core-v0` is an implemented M1 contract. The semantic binding, mechanic profile, and transition envelope v0 documents are proposed target contracts.
- Linguistic Core is the semantic interface for senses and roles, not an executable mechanics source.
- Consequences require a represented causal bearer and installed mechanic.
- Composite and analytic descriptions ordinarily remain derived.
- Observability is required. Exact replay and deterministic execution are not universal promotion gates.
- Mechanics-agent authoring begins offline. An installer validates and freezes the selected profile before the run.
- Runtime invention or revision of world laws is deferred.
- Donor repositories remain read-only idea, implementation, or failure-analysis sources unless a later consumer path explicitly adopts code.

## Architecture and capability invariants

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
- Local mechanics have independently enforced read/write scopes.
- One enclosing transition owns each causally coupled commit.
- Independent actions may commit independently.
- Resident cognition and post-run analysis are not canonical world authorities.
- Invariants and accounting are goal-relative to the selected representation.
- Passing declared-contract checks does not prove the author named every consequential dependency.

## Milestone horizon

| Milestone | State | Inspectable output | Promotion or replan trigger |
| --- | --- | --- | --- |
| M0: canonical foundation | complete | repository authorities, navigation, checks | established |
| M1: freshwater vertical | complete | neutral CLI trace, refusals, persistence, and M1 replay | promoted |
| M2: semantic/causal give vertical | active | Linguistic Core binding for `give`; two independent gives derivable as exchange without duplicate effects | binding, authority, refusal, reneging, and trace cases pass |
| M3: offline mechanics-authoring vertical | conditional | one adjacent mechanic authored as a reviewable package and frozen into a profile | installer validates local scope, effects, tests, limits, and interactions |
| M4: causal-coherence assay | conditional | declared-coverage report plus adversarial interaction findings | missing/overlapping dependencies become explicit risks, refusals, or repaired bindings |
| M5: installed institution | conditional | escrow-like bearer couples effects through one transition envelope | deliberate downstream failures produce no provisional commit |
| M6: non-agent process and second world | human_decision_required | autonomous process plus a materially different reference world | selected domain tests reuse rather than cosmetic variation |
| M7: scale and dynamical evaluation | deliberately_deferred | measurements or perturbation studies that can change a design decision | activate only when a real world exposes the need |

The later ordering is conditional. M3–M5 may be reordered after M2 evidence and selection of the first bounded authoring scenario. The hard dependency is that semantic binding, persistent effects, observability, local authority, and singular commit work before open-ended mechanics authoring.

## Active slice: M2 semantic/causal give vertical

**State:** `fully_specifiable_now`.

**Question:** Can one linguistic predicate be grounded in a primitive mechanic while a related higher-order predicate remains useful but non-causal?

**Visible result:**

- one reviewed Linguistic Core `give` sense and participant-role binding;
- canonical giver, object, and recipient references;
- an installed local transfer mechanic with explicit state-path scope;
- observable attempt, applicability, refusal, commit, and resulting possession state;
- two independently initiated gives recognizable as an exchange;
- a trace showing that one participant can decline or renege; and
- no second transfer caused by the derived exchange classification.

**M1 audit included in the slice:**

- document whether current `owner` means bounded operational possession/control rather than universal legal title;
- identify any transition effects committed before the enclosing action succeeds;
- map current events to the proposed observability fields;
- identify which current checks are goal-relative M1 invariants rather than universal substrate laws; and
- record the gap between current action IDs and Linguistic Core sense/role bindings.

**Failure boundary:** if the proposed semantic layer requires a new top-level ontology before donor coverage is inspected, stop and perform the coverage audit. If exchange requires a second state-writing transfer path, keep it derived and repair the classification. If local write scope or singular commit cannot be enforced without revising `core-v0`, propose a versioned transition contract rather than silently changing the implemented M1 contract.

## Enabling policy adapter

A genuine LLM policy consumer remains useful for checking the observation/action seam, but it is not the main research uncertainty. No provider call is authorized without an explicit model-execution decision and spend cap. A future adapter must select from or produce a valid semantic intent; it cannot author canonical effects.

## Authoring and causal-closure hypothesis

The central test is whether agent teams can add useful, coherent mechanics faster than interaction risk grows.

An agent-authored package must include semantic bindings, causal bearer, applicability, local authority, proposed effects, goal-relative invariants, dependencies, interaction cases, unsupported combinations, limits, and a trace contract. Passing isolated tests is insufficient.

The compiler or installer can establish declared enforcement coverage. Causal closure remains a fallible assay because an author may omit a dependency entirely. Mechanics agents should inspect neighboring semantic state, search for unbound consequential relations, generate counterexamples, and label residual risk.

## Evidence and claim boundaries

| Claim | Evidence | Limitation | Status |
| --- | --- | --- | --- |
| M1 freshwater behavior works | retained machine/human receipts, probes, tests, and replay | deterministic scripted vertical only | established |
| M1 exact replay works | fresh-process replay receipt | M1 property, not product requirement | established |
| Semantic binding works | M2 binding and trace evidence | no claim before implementation | target |
| Derived exchange avoids double application | M2 reciprocal/reneging cases | ordinary voluntary exchange only | target |
| Offline mechanics authoring works | M3 frozen package and interaction evidence | one bounded extension cannot prove scalability | conditional |
| Global causal closure is proven | none | not generally decidable from author declarations | rejected claim |
| Second-world reuse works | M6 evidence | domain not selected | deferred |

## Risks and needs resolution

- Linguistic breadth can hide mechanical sparsity.
- A new classification enum could accidentally replace rather than bind donor ontologies.
- A generic component model can become an untyped property bag.
- Broad LLM adjudication can bypass local causal authority.
- Individually valid mechanics can disagree about units, timing, identity, capability revocation, or overlapping effects.
- Declared dependencies can create false confidence when consequential state was never declared.
- Coarse organizational or social surrogates can double-count detailed lower-level mechanisms.
- Documentation can outrun implementation; proposed contracts must remain labeled.

## Human decisions

No decision is required to begin M2 documentation and local implementation. Model execution and spend, selection of the first agent-authored mechanic, selection of the second reference world, deployment, and publication remain explicit human boundaries.

## Refresh and reset triggers

Refresh this roadmap after an outcome-bearing slice, a material user correction, an accepted decision, a selected donor revision, or evidence that invalidates a contract. Replan after two consecutive non-vertical increments or when a later milestone no longer tests the central hypothesis.

## Exact next action

Audit the current M1 `give` path against the proposed semantic-binding and transition-envelope contracts. Produce the smallest versioned binding and trace that preserves the implemented transfer while making ordinary exchange a detachable derived view. Do not make a model call.
