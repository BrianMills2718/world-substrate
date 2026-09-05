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
**Stage:** prototype complete; the project is not  
**Last outcome-bearing implementation:** cleared the Open obligations — six of seven closed outright, `unheat`'s binding handed to the upstream ontology, and read-scope enforcement designed and costed rather than implemented  
**Current strategy frontier:** the gap between a substrate that works and a world worth showing anyone

## Outcome and success criteria

### The end goal

**A sophisticated world-modelling system, with one instantiation good enough to
show off as the flagship.** Stated by Brian on 2026-09-04, in those terms.

This had never been written down. Everything below it — the seven-bullet
workflow, the six numbered criteria — is the *prototype phase*, and that phase
is finished. Read the two as a sequence, not as alternatives: the prototype
asked "do these contracts hold?", and the answer is yes. The project asks "is
there a world here anyone would want to look at?", and that has not been
attempted.

A fresh agent should take three things from this section:

1. **"All six success criteria met" does not mean the project is done.** It
   means phase one is done. The repository said otherwise until 2026-09-04 and
   a reader would reasonably have concluded the work was over.
2. **Nothing here has ever been shown to anyone.** There is no demo, no UI, no
   deployment, and no consumer: no repository outside this one imports
   `world_substrate`. Every run to date is a probe, a test, or a retained
   evidence file.
3. **The two reference worlds are deliberately small.** Castaway is six
   entities and seven action kinds; the workshop is seven entities and two.
   They were built to test whether the contracts transfer, and they do. Neither
   was built to be interesting, and neither is.

### What "sophisticated" and "show off" still need to mean

These are the open questions, and they are Brian's to answer rather than a
fresh agent's to assume. Do not start building a flagship against a guess.

- **Which world.** A third world built to be watched, or one of the two
  existing ones grown until it is worth watching? They share no content, so
  this is a real fork rather than a naming choice.
- **What a viewer sees.** The substrate has no surface. `policy.present()`
  renders a text block for a language model, and the probes print JSON. Showing
  this to a person needs something that does not exist yet, and the project has
  standing instructions not to deploy or publish without explicit authority.
- **What makes it impressive.** Candidates the existing evidence points at, in
  no order: many interacting mechanics rather than four; agents whose beliefs
  visibly diverge from the world and get corrected by it, which M5 produced by
  accident and is the most striking thing in the repository; mechanics authored
  live rather than offline, which is currently deferred by decision; or scale.
  These pull in different directions and at most one should be chosen first.

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

### Active slice: none — the next one needs a decision that has not been made

The Open obligations slice is complete; what it did is recorded in the
obligations table below and in the audits, and the goal document that drove it
is retired rather than kept as a second roadmap.

No slice is specified here, and specifying one would be guessing. The end goal
above names three open questions — which world, what a viewer sees, what makes
it impressive — and each leads somewhere different. Picking one before Brian
does would mean building a flagship against an assumption.

**What a fresh agent should do first, before proposing any slice.** In this
order, and none of it needs permission:

1. **Run the thing.** `python scripts/run_llm_policy.py --thirsty --turns 8`
   costs nothing and prints a real trace. Then read
   [the M5 audit](../docs/audits/m5-policy-consumer.md), which is the closest
   this project has to a story worth telling: a model boiled its water, then
   refilled the pot from the contaminated pool, drank it believing it was
   treated, and lost 40 health to a mechanic that did not care what it
   believed.
2. **Look at how small the worlds are.** `reference_worlds/castaway/freshwater-v0.json`
   and `reference_worlds/workshop/bench-v0.json` are the entire content of both
   worlds. Six and seven entities. This is the gap between the substrate and
   the goal, and it is visible in two files.
3. **Read the two audits that bound what is known**:
   [M6](../docs/audits/m6-second-world.md) established that the machinery
   transfers and *no* mechanic does — every world's content is written from
   nothing — and [M7b](../docs/audits/m7b-relational-authoring.md) measured how
   much a model can write for you, which is some, and less than hoped.
4. **Then ask Brian the three questions**, with a recommendation rather than a
   menu.

**What not to do.** Do not start hardening, refactoring, or adding contracts.
The prototype is over-verified relative to what it does: 175 tests and ten
pinned evidence probes for two worlds nobody has watched. More of that moves
nothing toward the goal.

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
| ~~Second reference-world domain~~ | answered: the workshop world (M6) | superseded by the flagship-world decision above |

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
| **Which world becomes the flagship** | No world has been chosen to be worth watching, and the two that exist share no content, so this is a fork rather than a naming choice | The only thing that unblocks any flagship work at all. Everything else waits on it |
| **What a viewer actually sees** | The substrate has no surface: `policy.present()` renders text for a model and the probes print JSON | Whether the next work is a world or an interface. Also crosses the deployment boundary below |
| **What "sophisticated" means here** | Named candidates pull in different directions: many interacting mechanics, agent belief visibly diverging from the world, live mechanic authoring (currently deferred by decision), or scale | Which of those the flagship is built around. At most one should be first |
| Deployment and publication | Explicit authority boundary | Showing the flagship to anyone. Not yet blocking, because there is nothing to show |

Selection of the first agent-authored mechanic is no longer a boundary: M3 and
M4 exercised two, and the remaining authoring questions are answerable without
a new selection.

The three flagship decisions are stated as questions rather than options on
purpose. A fresh agent should bring a recommendation to them, not a menu, and
should have run the world first — see the Active slice section.

## Refresh and reset triggers

Refresh this roadmap after an outcome-bearing slice, a material user correction, an accepted decision, a selected donor revision, or evidence that invalidates a contract. Replan after two consecutive non-vertical increments or when a later milestone no longer tests the central hypothesis.

## Exact next action

Nothing is in progress and the working tree is clean.

The next action is a decision, not an implementation: which of the three
questions under the end goal gets answered first. Until one is, any code
written here is a guess at a flagship nobody specified.

The cheapest thing that would inform that decision is the first step above —
run the world, read the M5 audit, look at how small the two content files are.
Half an hour, no spend, and it turns the goal from an adjective into a
comparison.

Model calls are authorized under a $2 cap and have cost **$0.085** to date
(`get_cost(task=...)`: $0.00675 for the M5 policy run, $0.07816 for authoring
across M7 and M7b, including pilots and one killed run). Read that figure from
the observability DB rather than adding up per-run numbers.
