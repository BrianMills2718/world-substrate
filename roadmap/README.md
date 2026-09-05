---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-09-04
---

# World Substrate living roadmap

**Authority:** user-approved direction in [Decision 001](../docs/decisions/001-project-scope.md), [Decision 002](../docs/decisions/002-observability-and-replay.md), and [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md)  
**Selected path:** durable solo; one writer; reversible branches; no deployment, publication, or model spend without explicit authority  
**Stage:** prototype  
**Last outcome-bearing implementation:** cleared the Open obligations — six of seven closed outright, `unheat`'s binding handed to the upstream ontology, and read-scope enforcement designed and costed rather than implemented  
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
- Ownership references are checked: `owner_ref` must be `<kind>:<target>`, enforced in `World.validate()` and refused at construction by `model.owner_ref()`. This closes the one defect class M7 found that nothing in the repository could catch.
- Declared **write** scopes are enforced by the engine (`scope_violation`; negative controls in `tests/test_write_scope.py`). Declared **read** scopes are recorded on every event and are **not** enforced at runtime; the three rules that under-declared reads are repaired and `tests/test_overheat_assay.py` guards against regression.
- Three interaction assays exist on three different bases — declarations, differential behaviour, conserved-quantity accounting. Each has a stated blind spot; no single basis and no pair is sufficient. Evidence: [M3](../docs/audits/m3-overheat-authoring-experiment.md), [M4](../docs/audits/m4-spill-experiment.md).
- Installation validates internal consistency and never completeness. A residual class of omission survives every check the repository has; M4 records one that is live in the world today only because a second mechanic closed it.
- A policy has driven this world (criterion 2, met): an LLM chose 16 actions through the ordinary affordance seam for $0.005, beat a no-foresight baseline on health 60 to 4, and was corrected by a mechanic when its stated belief was wrong. See [the M5 audit](../docs/audits/m5-policy-consumer.md).
- A second, materially different world reuses the contracts (criterion 6, met). **All six prototype success criteria are now met.** The workshop world shares no content with Castaway and the split was clean in both directions: the transition kernel, causal events, exact replay, the profile installer, all three assays and the policy seam transferred with no edits at all, while *zero* Castaway mechanics were reusable — `take`/`give` compute carrying capacity from `liquid.volume_ml` and cannot move a bolt. Four couplings had to be broken: `Entity` was a closed component set, `observe()` required `ActorState`, write-scope binding used Castaway's action vocabulary, and `policy.present()` read health and hydration. Two of the four were written earlier in the same session in modules named for their general purpose. See [the M6 audit](../docs/audits/m6-second-world.md).
- The declaration language expresses one relation: a selected entity binds a second one it names through its own string field, and conditions and effects reach it by that name. This is the first time an authored mechanic can put a cause on one entity and its effect on another, and the first time an authored write-scope violation is possible rather than self-contradictory. See [the M7b audit](../docs/audits/m7b-relational-authoring.md).
- The write-scope guard no longer trusts the submitter, and the interaction assays are no longer bound to Castaway's vocabulary. Both were found by probing the workshop rather than reading the code — the same way M6 found its four couplings, in the same modules M6 certified as having transferred unchanged. `assay_undeclared_component_reads` could not produce a finding in the workshop world at all; `_subject` collapsed every workshop action to `?`; and `controller`, a free-form string the submitter chooses, bound a participant and widened a rule's write scope to any entity it named.
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
| M7b: relational authoring | complete | ten mechanics authored against a language that can express one relation, graded on criteria fixed beforehand and identical to M7's | promoted: 4/8 valid declarations used a relation and two produced cross-entity behaviour nothing in this project could previously express; the two inert clamps recurred anyway, so the language ceiling was real and not the main driver; zero scope violations, this time against machinery a relational write can actually load — [the audit](../docs/audits/m7b-relational-authoring.md) |
| M8: scale and dynamical evaluation | deliberately_deferred | measurements or perturbation studies that can change a design decision | activate only when a real world exposes the need |

Ordering after M4 was re-derived from the unmet success criteria rather than from this table's original sequence. Two of six criteria are unmet — a policy driving the world (2) and a second world (6) — and neither is a mechanics question, so both outrank further mechanics work including M5.

### Active slice: clear the Open obligations — complete

This section is the goal authority for the current run. The repository forbids
a second roadmap or a handoff document, so the goal lives here rather than in a
parallel file, and the Open obligations table below is its backlog of record.

**Mission.** Clear the obligations an accepted decision or contract already
requires, so the substrate's own stated invariants hold and the two seam
weaknesses M5 found in the observation are fixed. Both halves of the central
hypothesis are already answered; this is the work the project committed to and
has not done, not new scope.

**Outcome.** All five increments ran. Six obligations closed, one
(`unheat`'s sense) is closed as far as this repository can take it and belongs
to the upstream ontology, and one (read-scope enforcement) is designed and
costed rather than implemented, which is what it asked for. Two of the
acceptance checks needed honest restatement rather than quiet weakening: C4 is
six of seven action kinds with the seventh named, and C5's salt path is real
but unexercised because the freshwater world models no salt, so the
demonstration uses pathogens, which it does move. The canonical example holds:
at tick 4 a `discover("robinson")` page reports
`clay-pot: boiling to kill pathogens 1/2`, and once treated every `fill` on
that pot is marked as re-contaminating the 978ml it already holds while fills
on the empty cup stay silent.

**Execution profile:** continuous-light

One writer, reversible branches, no deployment, publication, or destructive
state. Model spend is not required by any increment and stays inside the
standing $2 cap if used.

**Stage and investment boundary:** prototype hardening. Expect one to two
sessions. Verification is the cheapest focused check that can invalidate the
changed behaviour, not a broad audit.

**Canonical example.** In the freshwater world, with a pot part-way through
boiling and holding treated water, one `discover("robinson")` page shows both:
the pot's boiling progress toward the two consecutive ticks treatment needs,
and a `fill` affordance explicitly marked as destroying the treatment it
already has. A policy reading that page can tell boiling is partway done and
that refilling would undo it. Those are exactly the two things the M5 policy
could not see, and it oscillated heat/unheat for seven turns and then drank
re-contaminated water.

**Forbidden substitutes.** None of these satisfies the example:

- a field added to canonical state but absent from `observe()` / `discover()`;
- a test asserting a constant rather than driving the engine to the state;
- a hand-edited evidence file, or regenerating a pinned probe's evidence
  without first showing field by field that the diff is the intended schema
  change and nothing else;
- a design document standing in for any increment that is implementable;
- documentation of an obligation as closed without the behaviour changing.

**Repository / working scope:** `/home/brian/code/world-substrate`, in a
claimed worktree under `worktrees/`. Root and subtree `CLAUDE.md` apply.

#### Boundaries

- In scope: the open rows of the Open obligations table.
- Out of scope: new milestones, a third reference world, deployment,
  publication, runtime law revision, and donor-repository changes.
- Writes allowed: this repository only.
- Read-only: donor repositories, and the donor fixtures under
  `tests/fixtures/`.
- Pinned evidence under `evidence/` may be **rebound** to a new revision when a
  deliberate schema change moves it, and may never be regenerated to make a
  failure go away. As written first, this said evidence could not be rewritten
  at all, which is not the rule the project actually follows — it rebound its
  receipts for the Decision 002 observability fields and again for envelope
  attribution. The distinction that matters is evidence, not intent: before
  regenerating, diff fresh against pinned field by field and show every changed
  leaf belongs to the schema being changed. This was done twice here, for the
  semantic bindings and for the ledger's shape, and both diffs are recorded in
  their commit messages.
- Requiring authorization: any model call beyond the standing cap, and any
  push to a repository other than this one.

#### Increments

Each changes a named field or behaviour rather than describing one.

1. **Observation seam** — surface process progress, and mark an affordance that
   destroys the value of a vessel's current contents. Both M5 findings; both
   change `observe()` / `discover()` output.
2. **Unowned** — give the world a way to say a thing is held by nobody, so the
   intent behind M7b's `worn-tool-drop` is expressible rather than only
   refused.
3. **Semantic bindings** — bind the remaining six of seven M1 action kinds, so
   `semantic_binding` is non-null on every accepted action event.
4. **The two decisions** — the ledger's shape for lost quantities, and whether
   `World.clone()` deep-copies the event log. Both are reversible technical
   calls; make them, implement them, and record the rejected alternative.
5. **Read-scope enforcement design** — the one obligation that is genuinely not
   designed. The deliverable is a named mechanism with its cost and its blind
   spot, not an implementation.

#### Acceptance checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| C1 | Boiling progress is observable | a test drives a pot to mid-boil and asserts the progress appears in `discover()` |
| C2 | A treatment-destroying `fill` is marked as such | a test drives a treated vessel and asserts the affordance carries the flag |
| C3 | Unowned is expressible | M7b's `worn-tool-drop` declaration, read from its evidence file, installs, fires, and leaves the tool held by nobody |
| C4 | Every accepted action event is semantically bound | a test asserts no accepted action event has a null `semantic_binding` |
| C5 | Lost quantities are accounted | spilled salt and pathogens balance, and `overflow_ml` is either written or gone |
| C6 | The clone decision is implemented | a measured before/after on the same trace length, reported as numbers |
| C7 | Read-scope enforcement is designed | a document naming the mechanism, its runtime cost, and what it still cannot see |
| C8 | Nothing regressed | full suite passes, all ten pinned probes byte-identical, `check_project.py` passes, ruff at its pre-existing baseline of 3 |

#### Stops

- **No progress:** two consecutive increments that change no target field or
  behaviour trigger strategic revalidation rather than a third.
- **Finite loop:** at most three attempts on the same reproduced blocker. If
  they produce no new evidence and no safe next action, record the blocker,
  its owner, and the exact resume event, and move to the next increment.
- **Revalidation:** after three increments, roughly four hours, or twice the
  stage estimate, compare outcome progress against enabling and process work
  and report whether to retain, replace, or clear this goal. Strategic
  misalignment is returned as such, never relabelled a technical blocker.

#### Non-gating next actions

These do not gate completion: any decision Brian may take on the project's
future beyond these obligations, publication or deployment of anything here,
and further authoring experiments.

## Open obligations

Work an accepted decision or contract already requires, which no milestone
currently owns. Listed here so it is schedulable rather than resident only in
the audit that found it.

| Obligation | Required by | State |
| --- | --- | --- |
| ~~Attach the causal bearer's observation to its event~~ | Decision 002, field 1 of 8 | **closed.** Captured before mutation and attached as `observation`; `null` for a process |
| ~~Attach the bound Linguistic Core sense and roles to its event~~ | Decision 002, field 3 of 8 | **closed.** Attached as `semantic_binding`; `null` for the six unbound action kinds |
| ~~Name the authority/causal bearer on an event~~ | Decision 002, field 4 of 8 | **closed.** Attached as `causal_bearer`, distinguishing an actor from a process |
| Bind the remaining M1 action kinds to Linguistic Core senses | [Decision 003](../docs/decisions/003-semantic-mechanical-boundary.md) | **six of seven closed.** `drink`, `heat`, `fill`, `take` and `pour` join `give`, every predicate and role id read from the same pinned extraction. `unheat` stays open and not in this repository: none of the extraction's eighteen predicates is the removal of a vessel from a heat source, and the nearest is the application of heat, which is not that sense reversed. Binding it to a predicate that does not mean it, or minting one, would put an invented sense in a module whose whole contract is that it cites a pinned source. Owned by the upstream ontology |
| ~~Decide the ledger's shape for lost quantities~~ | M4 finding | **closed.** `spilled` is a full `LiquidState` like `evaporated`, so a failed vessel's salt and pathogens are recorded rather than zeroed and forgotten. `overflow_ml` is removed rather than populated: nothing wrote or read it, and a ledger field no mechanic maintains is a false guarantee. `assay_conservation` checks volume always and any other quantity the caller states an initial total for — deriving those from `physical_ledger.initial` was rejected because no mechanic maintains it and it is all zeros in every world here, so every new check would have passed for the wrong reason |
| ~~Decide whether `World.clone()` should deep-copy the event log~~ | review of `3b89847` | **closed: it shares them.** Measured here at 34/173/732ms for 10/20/40 actions, now 207ms at forty. The objection was that this trades isolation for an unenforced convention, so the convention is not what it rests on: the only operations on `world.events` anywhere are appends and reads, and `tests/test_event_log_sharing.py` fingerprints every event as it appears and re-checks the whole log after every transition in both worlds, including refusals and malformed envelopes, and proves it can go red |
| Enforce declared read scopes at runtime | this roadmap's own invariant | **designed, not implemented** — [the contract](../docs/contracts/read-scope-enforcement-v0.md). A recording proxy at the rule boundary, measured at 10.9x on `checks()` (8.5us to 92us per call), so it belongs in a verification pass and not the run loop. Four blind spots are stated; the weakest point is that `as_dict()` reads a whole component at once, so bulk projections either hide reads or force rules to declare reads they do not conceptually perform |
| ~~Surface process progress in the observation~~ | M5 finding | **closed, and the obligation misstated the defect.** `boiling_ticks` was always in `observe()`; what was missing is the threshold, since the count means nothing without knowing two consecutive ticks are needed, and `present()` never rendered it. A process that accumulates toward a threshold now declares `progress` and the affordance page carries current-against-required |
| ~~Signal that an action destroys the value of existing contents~~ | M5 finding | **closed.** An action rule may declare `consequences`, and `discover()` carries them per affordance. Filling a treated vessel is marked as re-contaminating what it already holds; filling an empty or already-untreated one is silent |
| ~~Make `owner_ref` a typed reference~~ | M7 finding | **closed.** `owner_ref` is validated as `<kind>:<target>` in `World.validate()`, and the eighteen call sites that hand-built the convention now go through `model.owner_ref()`, which refuses a malformed reference at the source. `tests/test_owner_ref.py` replays the exact declaration from M7's evidence file and asserts it is now refused with the attachment provenance intact. The wire format is unchanged, so all ten probes remain byte-identical |

| ~~Refuse authored writes a field's type forbids~~ | generalisation of the M7 finding | **closed.** `owner_ref` was one instance of a wider class: `set` put any JSON scalar into any field and `World.validate()` covered only a hand-picked subset, so `worker.fatigue := "tired"` and `location.location_id := ""` both committed — the second silently removing four of seven entities from every observation while `validate()` and snapshot round-trip both passed. Effect and selector paths are now resolved against the owning dataclass at declaration time and the literal value type-checked there; `World.validate()` refuses an emptied `location_id`, `definition_id`, `heat_source_id` or `material_id`. `tests/test_authored_write_types.py` replays all seven observed corruptions. All ten probes remain byte-identical |

| ~~Give the world a way to say "unowned"~~ | M7b finding | **closed.** A reserved `unowned` literal, which costs nothing at the consumers because every one of them compares against a reference it built itself. `tests/test_unowned.py` reads the `worn-tool-drop` declaration a model actually wrote out of M7b evidence, shows it is still refused as written, and shows that changing the one value the model could not express makes it install, fire, and leave the tool held by nobody |

**All eight Decision 002 observability fields are covered, on every event class.**
The three rows above were closed together as one `core-v0` schema change. This
was the only requirement the project set for itself and did not meet. A
malformed envelope records its bearer as `claimed_actor` rather than `actor`,
since nothing in it has been validated — that path matters because every
untrusted policy submission arrives through it.

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
| A policy can drive this world | [M5 audit](../docs/audits/m5-policy-consumer.md); `evidence/m5/llm-policy-v0.json` | one model, one prompt, one world, 16 turns; the refusal path was never exercised by the model | **met** (criterion 2) |
| Global causal closure is proven | none | not generally decidable from author declarations | rejected claim |
| Second-world reuse works | [M6 audit](../docs/audits/m6-second-world.md); `tests/test_workshop_world.py` | one second world, chosen by the substrate's own author to be maximally different; zero Castaway mechanics transferred | **met** (criterion 6) |

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
| ~~Which second reference world~~ | **Answered: the workshop world, built and promoted in M6** | Criterion 6 met. The reuse test was real rather than cosmetic — zero Castaway mechanics transferred and four substrate/content couplings had to be broken |
| Deployment and publication | Explicit authority boundary | Nothing currently waiting on it |

Selection of the first agent-authored mechanic is no longer a boundary: M3 and
M4 exercised two, and the remaining authoring questions are answerable without
a new selection.

## Refresh and reset triggers

Refresh this roadmap after an outcome-bearing slice, a material user correction, an accepted decision, a selected donor revision, or evidence that invalidates a contract. Replan after two consecutive non-vertical increments or when a later milestone no longer tests the central hypothesis.

## Exact next action

Nothing is in progress. The prototype's six success criteria remain met, and
the central hypothesis has now been tested against a language that can express
more than a clamp. The answer to "does usefulness outrun risk" is unchanged in
direction and better grounded: usefulness rose (two cross-entity mechanics that
were previously inexpressible), risk did not (zero scope violations, against
machinery that a relational write can genuinely load), and the dominant cost is
still a steady supply of plausible-looking proposals that are redundant or
inert.

The open obligations table is the remaining work. The largest are enforcing
declared read scopes, the ledger's shape for lost quantities, and giving the
world a vocabulary for unowned.

Two follow-ons remain from M7, both small and needing no permission:

1. Give the assays a triviality check. Nothing today distinguishes a mechanic
   that fires and changes the world from one that installs cleanly, declares its
   scope correctly, and guards a condition existing rules make unreachable. Two
   of nine authored mechanics were the latter, and only running them revealed
   it.
2. The rest of the Open obligations table — the three uncovered Decision 002
   observability fields are the largest single item and are one `core-v0` schema
   change rather than six separate ones.

Beyond those, the prototype has answered both halves of its central hypothesis
and all six success criteria. Continuing is a scope choice rather than a next
step.

Model calls are authorized under a $2 cap and have cost **$0.085** to date
(`get_cost(task=...)`: $0.00675 for the M5 policy run, $0.07816 for authoring
across M7 and M7b, including pilots and one killed run). Read that figure from the
observability DB rather than adding up per-run numbers -- a previous version of
this line said $0.04 because it counted only the final M7 trace.
