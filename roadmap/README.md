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
**Last outcome-bearing implementation:** M7 measured whether an agent can author a mechanic it was not handed  
**Current strategy frontier:** none selected — the prototype's stated success criteria are all met

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

State, not history. Milestone narratives live in the milestone table and their
audits; findings live in the audit that produced them.

- This repository owns the project goal, decisions, architecture, contracts, source dispositions, and roadmap.
- M1 through M4 are complete and promoted. M1 is pinned at implementation revision `4c3303828b7c9b97e22a806caa404306f8616f7a`; its retained evidence remains authoritative for that claim.
- Contract status is mixed: `core-v0` is implemented; [mechanic profile](../docs/contracts/mechanic-profile-v0.md) and [transition envelope](../docs/contracts/transition-envelope-v0.md) are partially implemented; [semantic binding](../docs/contracts/semantic-mechanical-binding-v0.md) has one binding of seven. Each contract states its own status.
- Declared **write** scopes are enforced by the engine (`scope_violation`; negative controls in `tests/test_write_scope.py`). Declared **read** scopes are recorded on every event and are **not** enforced at runtime; the three rules that under-declared reads are repaired and `tests/test_overheat_assay.py` guards against regression.
- Three interaction assays exist on three different bases — declarations, differential behaviour, conserved-quantity accounting. Each has a stated blind spot; no single basis and no pair is sufficient. Evidence: [M3](../docs/audits/m3-overheat-authoring-experiment.md), [M4](../docs/audits/m4-spill-experiment.md).
- Installation validates internal consistency and never completeness. A residual class of omission survives every check the repository has; M4 records one that is live in the world today only because a second mechanic closed it.
- A policy has driven this world (criterion 2, met): an LLM chose 16 actions through the ordinary affordance seam for $0.005, beat a no-foresight baseline on health 60 to 4, and was corrected by a mechanic when its stated belief was wrong. See [the M5 audit](../docs/audits/m5-policy-consumer.md).
- A second, materially different world reuses the contracts (criterion 6, met). **All six prototype success criteria are now met.** The workshop world shares no content with Castaway and the split was clean in both directions: the transition kernel, causal events, exact replay, the profile installer, all three assays and the policy seam transferred with no edits at all, while *zero* Castaway mechanics were reusable — `take`/`give` compute carrying capacity from `liquid.volume_ml` and cannot move a bolt. Four couplings had to be broken: `Entity` was a closed component set, `observe()` required `ActorState`, write-scope binding used Castaway's action vocabulary, and `policy.present()` read health and hydration. Two of the four were written earlier in the same session in modules named for their general purpose. See [the M6 audit](../docs/audits/m6-second-world.md).
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
| M5: policy consumer | complete | an LLM selecting from `discover()` over 16 turns, compared against a no-foresight baseline on the same world | promoted: seam holds (no policy output is ever parsed into an action), the world corrected the model's wrong belief mechanically, and two observation-seam weaknesses surfaced that a scripted controller cannot expose — [the audit](../docs/audits/m5-policy-consumer.md) |
| M5b: installed institution | deprioritized | escrow-like bearer couples effects through one transition envelope | Revisit only when a world needs an institution. Atomic commit-or-refuse has existed and been tested since M1, so escrow largely re-exercises machinery rather than testing an open question |
| M6: second reference world | complete | a workshop world — worker, bench, discrete parts, tool, assembly — sharing no content with Castaway | promoted: the transition kernel, events, replay, profile installer, all three assays and the policy seam transferred with no edits; four substrate/content couplings were found and fixed; zero Castaway mechanics were reusable — [the audit](../docs/audits/m6-second-world.md) |
| M7: authoring rate | complete | ten mechanics authored by a model that was told neither which mechanic to write nor what the checks look for, graded against criteria fixed beforehand | promoted: 9/10 installed, 0 scope violations, 5/10 added real behaviour, 2/10 were inert, and 2/10 violated an undeclared world convention that nothing can check — [the audit](../docs/audits/m7-authoring-rate.md) |
| M8: scale and dynamical evaluation | deliberately_deferred | measurements or perturbation studies that can change a design decision | activate only when a real world exposes the need |

Ordering after M4 was re-derived from the unmet success criteria rather than from this table's original sequence. Two of six criteria are unmet — a policy driving the world (2) and a second world (6) — and neither is a mechanics question, so both outrank further mechanics work including M5.

### Active slice: none until a domain or a spend cap is chosen

M2's give/exchange slice is complete and promoted; its detail lives in the
milestone table and [its audit](../docs/audits/m2-give-path-audit.md).

Both candidate next slices are gated on a human decision (see Human decisions
below), so no slice is specified here. Specifying one before the domain or the
spend cap is chosen would be planning ahead of the decision that determines its
shape.

## Open obligations

Work an accepted decision or contract already requires, which no milestone
currently owns. Listed here so it is schedulable rather than resident only in
the audit that found it.

| Obligation | Required by | State |
| --- | --- | --- |
| Attach the causal bearer's observation to its event | [Decision 002](../docs/decisions/002-observability-and-replay.md), field 1 of 8 | open — `engine.observe()` exists but is never attached; a `core-v0` schema change |
| Attach the bound Linguistic Core sense and roles to its event | Decision 002, field 3 of 8 | open — `SEMANTIC_BINDINGS` exists but is never attached; same schema change |
| Name the authority/causal bearer on an event | Decision 002, field 4 of 8 | partial — `rule_id` gives the mechanic, nothing gives the bearer |
| Bind the remaining 6 of 7 M1 action kinds to Linguistic Core senses | [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md) | open — only `give` is bound |
| Decide the ledger's shape for lost quantities | M4 finding | open — `spilled_ml` is a bare integer while `evaporated` is a full liquid vector, so spilled salt and pathogens leave the world unaccounted; `overflow_ml` is written by nothing |
| Enforce declared read scopes at runtime | this roadmap's own invariant | open, and harder than writes — a read leaves no trace in state. Declarations are repaired and guarded by test; enforcement is not designed |
| Surface process progress in the observation | M5 finding | open — `container.boiling_ticks` exists in state and is not observable, so a policy cannot tell that boiling is partway done. The M5 run oscillated heat/unheat for seven turns because of this |
| Signal that an action destroys the value of existing contents | M5 finding | open — `fill` is presented identically whether or not it re-contaminates a treated vessel. The M5 policy did exactly that and then drank it |
| Make `owner_ref` a typed reference instead of a bare string | M7 finding | open — the world encodes ownership as `actor:`/`place:`/`assembly:` prefixes, but the convention is declared nowhere, so `''` is a valid value to the type system, the scope guard, `World.validate()` and the installer alike. Two of nine authored mechanics set it to `''` and destroyed attachment provenance; nothing caught it |

Five of eight Decision 002 observability fields are covered today. The three
rows above are the gap, and closing the first two is one `core-v0` schema
change rather than six separate ones.

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
| Semantic binding works | `semantic.py` binding plus `tests/test_give_exchange.py` | one sense of seven action kinds; no binding is attached to an event | established, narrowly |
| Derived exchange avoids double application | M2 reciprocal/reneging cases | ordinary voluntary exchange only, and the classifier matches any reciprocal pair regardless of interval or object | established, with a known over-match |
| Declared write scopes are enforced | `tests/test_write_scope.py` negative controls | writes only; reads are recorded and unenforced | established |
| Offline mechanics authoring works | M3 and M4 frozen packages, three assays, negative control | two mechanics, one world, and the same person authored both the mechanics and the assays judging them | established for the risk half; the *rate* half is untested |
| Interaction assays surface omitted dependencies | M3 and M4 findings | each basis has a stated blind spot; no basis and no pair is sufficient, and a residual survives all three | established, with the residual demonstrated |
| A policy can drive this world | none | never attempted; every run is a scripted controller | unmet success criterion 2 |
| Global causal closure is proven | none | not generally decidable from author declarations | rejected claim |
| Second-world reuse works | none | domain not selected; M2 audit measured 2 of 10 checks as substrate-universal | unmet success criterion 6 |

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

Boundaries only Brian can clear. Each names what changes if it is answered.

| Decision | Why it is blocked | What it unblocks |
| --- | --- | --- |
| ~~Model execution and a spend cap~~ | **Answered 2026-09-04: $2 cap granted** | Spent $0.005 of it. Criterion 2 met; see the M5 audit. Further runs stay under the same cap |
| **Which second reference world** | No domain selected | Success criterion 6, and the only test of whether "substrate" is real. The M2 audit measured the warning sign: 2 of 10 `give`/`take` checks are substrate-universal, the other 8 are Castaway content. A domain sharing little with Castaway — discrete objects, no liquids, no heat — makes the reuse test real rather than cosmetic |
| Deployment and publication | Explicit authority boundary | Nothing currently waiting on it |

Selection of the first agent-authored mechanic is no longer a boundary: M3 and
M4 exercised two, and the remaining authoring questions are answerable without
a new selection.

## Refresh and reset triggers

Refresh this roadmap after an outcome-bearing slice, a material user correction, an accepted decision, a selected donor revision, or evidence that invalidates a contract. Replan after two consecutive non-vertical increments or when a later milestone no longer tests the central hypothesis.

## Exact next action

Nothing is in progress. M7 answered the half of the central hypothesis that had
never been tested: a model asked for a mechanic the world needs, told neither
which one nor what the checks look for, produced nine installable mechanics for
$0.015 with zero scope violations. Risk did not outrun usefulness — but five of
ten added real behaviour, two were inert, and two violated a convention the
world never declared.

That reframes what is worth doing next. The bottleneck is not agents writing
dangerous mechanics; it is a steady supply of plausible-looking ones that are
redundant, inert, or quietly wrong, and review effort that scales with the
number of proposals rather than their quality.

The concrete follow-ons, in the order the evidence justifies:

1. Make `owner_ref` a typed reference. It is the one defect class M7 found that
   nothing in the repository can currently catch, and it is cheap.
2. Give the assays a triviality check. Nothing today distinguishes a mechanic
   that fires and changes the world from one that installs cleanly and is
   unreachable; two of nine were the latter and were graded only because the
   experiment ran them.
3. The rest of the Open obligations table.

Model calls are authorized under a $2 cap and have cost $0.04 to date.
