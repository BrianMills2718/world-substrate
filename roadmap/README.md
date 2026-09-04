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
**Last outcome-bearing implementation:** repaired the under-declared M1 read scopes and the audit assay's false positives (M1 and M2 verticals remain promoted)  
**Current strategy frontier:** M5 installed institution

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
- M2 has one implemented, tested slice: `give` is bound to the pinned Linguistic Core sense `lc:give_transfer` (`src/world_substrate/semantic.py`), and a derived, read-only exchange classification recognizes reciprocal `give` pairs without performing a second transfer (`src/world_substrate/exchange.py`). Verified by `tests/test_give_exchange.py` and `scripts/run_give_exchange_probe.py --check`.
- The M2 M1-audit is complete: [docs/audits/m2-give-path-audit.md](../docs/audits/m2-give-path-audit.md). Findings: `owner` is bounded possession/control only, never legal title; no transition effect is committed before its enclosing action succeeds (verified structurally in both `Engine.apply` and `Engine.advance`); events cover 5 of Decision 002's 8 observability fields directly, with 2 real gaps (no observation payload, no bound semantic sense/roles attached to an event) and 1 partial gap (mechanic yes, authority/bearer no) — closing these is a `core-v0` schema change, left for a future slice; only 2 of 10 `give`/`take` checks are substrate-universal (existence, revision-currency), the rest are this world's goal-relative content; 6 of 7 M1 action kinds (`fill`/`heat`/`unheat`/`pour`/`drink`/`take`) still have no semantic binding. This closes M2's audit scope; M2 itself is not fully closed by an audit alone.
- Declared write scopes are now enforced, not merely recorded. `Engine.apply`
  compares each committed change against the rule's `write_paths` and returns
  the new `scope_violation` status without committing anything; a process that
  writes outside its scope raises `ScopeViolation` and `advance` restores the
  tick. Before this, the invariant stated in the root `CLAUDE.md`,
  [architecture](../docs/architecture.md), and
  [transition envelope v0](../docs/contracts/transition-envelope-v0.md) held
  only by the good behaviour of reviewed rules. Every registered M1 rule and
  process passes unchanged with the guard active; the negative controls are
  `tests/test_write_scope.py`. This is the enforcement that "declared
  enforcement coverage" depends on before M3 authoring.
- M3 is complete and was run adversarially. One adjacent mechanic
  (`process.material.overheat-damage`) was authored offline as a reviewable
  package with a deliberately omitted consequential dependency, installed with
  zero findings, frozen, and run. Three results hold and are reproducible via
  `python scripts/run_overheat_assay_probe.py --check`: installation alone
  surfaces nothing, because the missing part is missing from the thing being
  checked; two complementary interaction assays surface it, naming six of the
  seven affected action mechanics between them, and neither alone is
  sufficient; and one real incoherence — a destroyed vessel that still holds
  its liquid — is caught by neither, passes `World.validate()`, and leaves
  every check in the repository green. See
  [the experiment](../docs/audits/m3-overheat-authoring-experiment.md).
- Read scopes are declared but not enforced at runtime. Three promoted M1
  rules read a component their declaration omitted — `take`, `give`, and
  `process.thermal.vessels`, all reading `condition` — and **those three
  declarations are now repaired**. No behaviour changed, so rule versions were
  deliberately not bumped; evidence receipts were regenerated because
  `declared_read_paths` appears on every event, and the donor fixture carries
  no read paths, so donor parity is untouched.
  `tests/test_overheat_assay.py` guards against a new mechanic reintroducing an
  undeclared read. This originally went into the M3 and M4 audits as *seven*
  rules; four of those were false positives in the audit assay's own text
  matching, corrected in [the M3 audit's follow-up](../docs/audits/m3-overheat-authoring-experiment.md).
  Enforcing reads at runtime remains open and is harder than writes, because a
  read leaves no trace in state.
- M4 is complete. `process.material.vessel-failure-spill` was authored without
  a planted omission, closed M3's residual (a destroyed vessel now loses its
  contents), and keeps volume conserved against the ledger. It also gave
  `physical_ledger.spilled_ml` its first writer; that field and `overflow_ml`
  had been declared and written by nothing.
- The three assays behaved completely differently on it, and this is the
  substantive M4 result: the declaration assay named five readers (including
  `take`/`give`, which it could *not* see in M3, because they declare their
  liquid read but not their condition read); the behavioural assay found
  **nothing at all**, because every affordance on the vessel was already
  blocked by the overheat mechanic — a behavioural assay is blind behind an
  existing refusal; and only the conservation assay caught a control variant
  that destroys 459ml without recording it, which stays inside its declared
  write scope, commits cleanly, and passes `World.validate()`. No single basis
  and no pair of bases is sufficient. See
  [the M4 experiment](../docs/audits/m4-spill-experiment.md).
- Linguistic Core is the semantic interface for senses and roles, not an executable mechanics source.
- Consequences require a represented causal bearer and installed mechanic.
- Composite and analytic descriptions ordinarily remain derived.
- Observability is required. Exact replay and deterministic execution are not universal promotion gates.
- Mechanics-agent authoring begins offline. An installer validates and freezes the selected profile before the run.
- Runtime invention or revision of world laws is deferred.
- Donor repositories remain read-only idea, implementation, or failure-analysis sources unless a later consumer path explicitly adopts code.

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
- Local mechanics have independently enforced read/write scopes.
- One enclosing transition owns each causally coupled commit.
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
| M2: semantic/causal give vertical | complete | Linguistic Core binding for `give`; two independent gives derivable as exchange without duplicate effects | promoted: binding (`semantic.py`), authority (giver-only enforced in `GiveRule`), refusal (pre-existing `test_transfer.py::test_recipient_capacity_rejection_is_atomic`), reneging (`test_give_exchange.py`), and no-double-transfer trace cases all pass |
| M3: offline mechanics-authoring vertical | complete | `process.material.overheat-damage` authored as a package, installed with no findings, frozen as profile `d525940e065d8361`, and run | promoted: installation validated scope, effects, tests, limits; two interaction assays surfaced the package's omitted dependency and one residual survived both — [the experiment](../docs/audits/m3-overheat-authoring-experiment.md) |
| M4: causal-coherence assay | complete | three assays on three different bases, each with a stated blind spot, plus a negative control that only accounting catches | promoted: M3's residual closed by an honestly-authored mechanic; no single basis and no pair is sufficient — [the experiment](../docs/audits/m4-spill-experiment.md) |
| M5: installed institution | conditional | escrow-like bearer couples effects through one transition envelope | deliberate downstream failures produce no provisional commit |
| M6: non-agent process and second world | human_decision_required | autonomous process plus a materially different reference world | selected domain tests reuse rather than cosmetic variation |
| M7: scale and dynamical evaluation | deliberately_deferred | measurements or perturbation studies that can change a design decision | activate only when a real world exposes the need |

The later ordering is conditional. M3–M5 may be reordered after M2 evidence and selection of the first bounded authoring scenario. The hard dependency is that semantic binding, persistent effects, observability, local authority, and singular commit work before open-ended mechanics authoring.

### Active slice: M2 semantic/causal give vertical

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

**M1 audit included in the slice:** complete, [docs/audits/m2-give-path-audit.md](../docs/audits/m2-give-path-audit.md).

- document whether current `owner` means bounded operational possession/control rather than universal legal title; — done: possession/control only.
- identify any transition effects committed before the enclosing action succeeds; — done: none, structurally.
- map current events to the proposed observability fields; — done: 5 of 8 covered, 2 gaps, 1 partial gap.
- identify which current checks are goal-relative M1 invariants rather than universal substrate laws; and — done: 2 of 10 universal, rest goal-relative.
- record the gap between current action IDs and Linguistic Core sense/role bindings. — done: 1 of 7 action kinds bound (`give`).

**Failure boundary:** if the proposed semantic layer requires a new top-level ontology before donor coverage is inspected, stop and perform the coverage audit. If exchange requires a second state-writing transfer path, keep it derived and repair the classification. If local write scope or singular commit cannot be enforced without revising `core-v0`, propose a versioned transition contract rather than silently changing the implemented M1 contract.

## Enabling policy adapter

A genuine LLM policy consumer remains useful for checking the observation/action seam, but it is not the main research uncertainty. No provider call is authorized without an explicit model-execution decision and spend cap. A future adapter must select from or produce a valid semantic intent; it cannot author canonical effects.

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
| Give/derived exchange as active vertical | reversible planning choice | replan from M2 evidence |
| Later M3–M5 ordering | conditional | select from the first bounded authoring scenario |
| Second reference-world domain | human decision later | no domain selected |

## Evidence and review artifacts

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

M3 and M4 are both complete. Together they establish that installation never
validates completeness, that three assay bases each catch what the others miss,
and that each basis has a stateable blind spot.

The next actions, in the order their evidence justifies:

1. ~~Repair the under-declared M1 read scopes.~~ **Done.** Three rules
   repaired, the audit assay's own false positives fixed, and the ceiling M3
   identified is demonstrably lifted: the same declaration assay that could not
   see `take`/`give` now names both. Runtime *enforcement* of read scopes is
   still open.
2. Decide the ledger's shape for lost quantities. `evaporated` is a full liquid
   vector, `spilled_ml` is a bare integer, so spilled salt and pathogens leave
   the world unaccounted, and `overflow_ml` is still written by nothing.
3. Correct `mechanic-profile-v0.md` installer step 3, which read literally
   rejects the promoted M1 mechanics.
4. M5's installed institution is the next vertical: an escrow-like bearer that
   couples effects through one transition envelope.

Do not make a model call.
