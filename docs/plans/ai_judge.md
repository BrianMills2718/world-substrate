---
plan_id: "ai-judge"
dependencies: ["open-attempt"]
dependencies_reviewed: "2026-11-09"
planning_path: durable_solo
status: adopted
goal:
  outcome: "Worlds stay faithful as they grow too big for an AI to track: the engine works out every knock-on
    effect and blocker of an attempt, however long the chain, and an AI judge that sees those results decides
    only what no rule covers; its rulings become rules for everyone, and other people's choices stay theirs."
  canonical_example: "The port world in 'Canonical example' below: Vik's bribe offer reaches the judge with the
    facts and blockers the engine can compute without a rule; the judge proposes a rule that coins can
    change hands; the engine test-runs it on a copy of the world and shows the judge its net changes, every blocker and how far the chain ran; the
    judge confirms, the rule is installed, and Rosa chooses whether to accept the exact offer.
    Coins settle only under its consent and feasibility conditions. Signing remains separately constrained;
    the gate opens for a valid signed release whoever holds it, a 100-link chain from the gate runs in one moment, and the same offer by another trader
    later is decided by the new rule with no judge call."
  forbidden_substitutes: "a judge prompt of our own outside Concordia's game master; a judge that writes outcomes
    or decides another person's choice; a ruling used without passing the World Builder rules check; a norm
    written as a declared law; hand-edited rules or runs; a chain shortened to fit a cap; a fixture run reported
    as live."
  boundaries: "world-substrate and its own deploy only; Concordia and Cybernetic Influence v3 read-only; each
    slice merges through ship after scripts/check_project.py exits 0 on the committed change; saved worlds
    still replay unchanged; owner allowance only for live runs."
  done_when: "Acceptance checks A1-A8 below pass, each judged from the full trace of the run it names."
  do_not_gate_on: "Organisations and institutions beyond single norms; a real-world truth claim for any
    ruling."
  stop_after: 3
conflict_surfaces:
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/ai_judge.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/ai-judge/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/planning-package.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/ai-judge/review-page/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/decisions/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/attempt.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/consequences.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/concordia_residents.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/ai-judge/, access: write}
---
# Plan: an AI judge fed by automatic propagation

Planning package: docs/planning/ai-judge/planning-package.json

<!-- planning-compliance-checklist:v1 -->
## Compliance checklist

Written by `plan_checklist.py --write`, not by hand. `--check` re-runs the validator and fails
if any line below differs from what it says now. Unticked pending items are not passes.

Manifest: `docs/planning/ai-judge/planning-package.json`
Package revision: `05356af5ded4`
Verdict: compliant, 2 pending

- [x] part investigation: ok
- [x] part checks: ok
- [x] part open_questions: ok
- [x] part system_model: ok
- [x] part domain_model: ok
- [x] part diagrams: ok
- [x] part plan: ok
- [x] part acceptance: ok
- [x] part review_page: ok
- [x] part cold_review: ok
- [x] substance route follows from its path decision: ok
- [x] substance citations resolve: ok
- [x] substance domain model has a glossary: ok
- [x] substance project layer checks against the planning layer: ok
- [x] substance concepts point at their code: ok
- [x] substance plan names the concepts it relies on: ok
- [x] substance plan records the cost basis of each AI step: ok
- [x] substance plan compares its AI answer path with the plain version: ok
- [ ] substance plan shows what each stage adds over the plain version: failing
- [x] substance plan records Brian's stops on this work: ok
- [x] substance type-level model of executable rules: ok
- [x] substance cold review read this revision: ok
- [x] initiative initiative names its home: ok
- [x] tiers spectrum rungs 1-11 are cited: ok
- [x] tiers production rungs 12-14 are cited when it runs in production: ok
- [x] tiers thesaurus separates near-identical names (rung 4): ok
- [ ] system_map system map names every code unit: pending
- [ ] coverage goal coverage: pending
- [x] goal_provenance goal provenance: ok
- [x] freshness package is current: ok
<!-- /planning-compliance-checklist -->


**Status:** adopted. Brian approved its direction on 2026-11-09 ("i approve", after Decided 5) and building it on
2026-11-10 ("yes if ti si planned out and you have no quesitons for me"). J0 built 2026-11-10 (no knock-on cap;
PR #362, live at `d89a446`; saved runs in `evidence/ai-judge/j0/`, live share links in
`evidence/ai-judge/j0/live-shares.json`); J1 and J2 built 2026-11-10 (J2: PR #367, live at `b8d26b5`); J3 built
2026-11-10 and live at `cab821d` on 2026-11-11 (a checked ruling becomes a rule, installed at once or held for the
owner's approval; saved live runs and share links in `evidence/ai-judge/j3/live-shares.json`; the live approve run
showed an installed coin rule letting a person take another's coins with no offer, open question Q96, to fix before
J5); J5 is next; J4's representation design is settled below; implementation remains deferred.

## Why

Brian, 2026-11-09: "an ai adjudicator doesnt really scale and that we need to facts to have implications and
blockers. like 50 things could propagate down a causal chain 100 links deep taht the llm would not be able to
understand so we need that causal chain to automaticlaly rpogate and to deliver the resutls of that propagation to
he ai judge along with blockers."

## Actor and result

**Actor:** a World Builder visitor (and Brian as owner) who describes a world and watches its people act.
**Result they can inspect:** the run page and run record show, for an attempt no rule covered, what the engine
worked out (every knock-on effect and blocker), what the judge ruled and the rule it became, and whose choice
decided the rest.

## Project outcome

Project outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top,
rigorous causal engine underneath; the World Builder is the visitor-facing surface). This plan serves that actor
directly. **Recurring job and pre-plan baseline (2026-11-09):** a visitor describes a world and watches its people act. Before J0–J3, an attempt
no rule covered changed nothing (except a request, which reached the person asked, #326), knock-on chains stopped at 32
reactions per moment, and a blocker was told only to the person who tried. The Status section records delivered slices and remaining gaps. **Inspectable result:** the port world's
run page and record (canonical example). **Stage and investment boundary:** prototype stage; six slices, each one
pull request; at most $3.00 of owner allowance per slice; no new service, engine or repository.

## Canonical example

The port. "A small port: Rosa, the customs officer, signs inspection releases. Vik, a trader, has 40 coins and a
crate he has not declared. The exit gate is a barcode scanner that opens for any valid release code. Beyond the
gate, a 100-step chain runs: the crate reaches the warehouse, the warehouse fills, the dispatcher sends a truck..."

1. Vik offers Rosa 40 coins to sign without inspecting. No installed rule covers handing coins to an officer.
2. **Pass 1, before any rule exists.** The engine computes only what needs no new rule, from a fixed selection:
   `engine.discover` (`src/world_substrate/engine.py:380-440`) for the person acting (Vik) and for each person
   the attempt names (Rosa), keeping each page's available and blocked moves with their checks, plus the current
   values of every entity the attempt names (Vik, Rosa, the crate). Here: Vik holds 40 coins; Rosa and Vik are
   both at the customs desk; and from Rosa's page, "sign release: blocked, inspected is false". Vik's own page
   could not show that blocker, because `discover` lists only the moves of the person asked. There is nothing to
   propagate yet, because propagation starts only from a committed event.
3. The judge gets the whole world, the attempt and pass 1. It proposes a ruling on the constraint only, written
   as a rule in the existing declaration language: "a person may hand coins they hold to a person at the same
   place", which applies to everyone in that situation. Vik's attempt is an exchange, coins for a signature, so
   it settles only on Rosa's choice (Decided 4).
4. **Pass 2, the test run.** The engine runs the World Builder rules check on the proposed rule and test-runs it
   on a copy of the world with the exchange settled. The copy's net changes, any blockers, the chain's length and where it
   stopped form the consequence report (the full chain stays in the run record and on the run page: a 5,000-step
   chain is about 500,000 tokens, Q74): coins move to Rosa, Vik's purse empties, and nothing else follows. The judge reads the
   report and confirms, revises the rule once, or withdraws it. If the language cannot express the ruling (the
   check rejects it, and the one revision is rejected too), the attempt is refused with "no rule could express
   this" and the run records a language gap.
5. Only now is the rule installed. Vik's offer goes to Rosa as her decision; no coins move yet.
6. Rosa’s resident decides whether to accept the offer. Acceptance alone does not satisfy the installed signing check: while `inspected` is false, that signing attempt remains blocked and the conditional exchange cannot settle. Coins move only after her own feasible signing action completes under the installed rules; agreement is necessary, not sufficient.
7. If she signs, Vik holds a signed release. The gate (a mechanism) opens for the valid code however Vik got it.
   "Bribery is forbidden" is a norm: it was broken, and it has consequences only if an inspector notices and acts.
8. The gate opening sets off the 100-step chain. It runs to the end inside the same moment, each step citing the
   step that caused it.
9. Later, another trader offers a bribe. The new rule decides the hand-over; the judge is not called again.

Design clarification, 2026-11-12: the existing `inspected` check is a hard blocker in this example. A world intended to permit signing without inspection must separately model that capability and the breakable inspection norm; the judge cannot bypass the existing check by relabeling it. The example’s gate-opening continuation is conditional on a feasible signing action, not guaranteed by accepting the bribe.

This two-pass order is how Brian's "deliver the results of that propagation to the judge" is met: the judge
sees the propagation of its own proposed rule (pass 2) before anything is installed, plus the blockers that
installed rules already name for the people involved (pass 1). Inferred by agent, 2026-11-09. Basis: an attempt no rule covers commits
no event, and `_settle` in `src/world_substrate/engine.py` propagates only from a committed event, so a report
of knock-on effects can exist only for a proposed rule run on a copy (the cold review of 2026-11-09, finding 1);
the pass 1 rows already exist as `engine.discover` pages (`engine.py:380-440`); each round today's runs call it
for every resident and record a few distinct blocked rows each as `blocked_by_rules`
(`scripts/run_authored_world.py:601-634`), not tied to any attempt, so J1 selects the pages of the person acting
and the people the attempt names, in full, and adds the named entities' values. Resolved as an agent question in the
ledger (Q78).

The same split covers Brian's password computer: the computer logs in whoever types Alice's password (mechanism);
Alice knows it, and Mallory can learn it by phishing (a fact that can change); only Alice should log in (a norm).

## Decided

Source: Brian, 2026-11-09, "yes i aprpove all those except for whether the bribe works seems like should be a
deicsion made by the person being bribed. that is not a rule as much as a decision. maybe we need to discuss the
difference between rules/constraints and ddecisions?"

1. **Goal.** The project goal gains scale: a simulation platform for plausible worlds "that stays faithful as
   worlds grow too big for an AI to track: the engine works out every knock-on effect and blocker, and an AI judge
   decides using those results."
2. **What the judge decides: gaps only.** The judge decides attempts that no rule covers. The rulebook keeps
   deciding everything it covers. The judge never overrides a blocker the engine found.
3. **Rulings become rules.** A judge ruling is written down as a new rule, passes the World Builder's existing
   rules check, applies to everyone from then on, and the engine propagates its effects.
   **How a one-off becomes general** (inferred by agent, 2026-11-09): every ruling is a rule in the existing
   declaration language (`action-mechanic/v0`, `src/world_substrate/action_authoring.py`), so it names a
   situation (who, what, which checks) rather than a person, and applies to everyone in that situation. If the
   judge cannot express a ruling in that language, the rules check rejects it, the attempt is refused with "no
   rule could express this", and the run records a language gap. Basis: reading the language (expression kinds
   at `action_authoring.py:893-927`) and checking 3 real rulings by hand (Plain baseline below): it expresses
   transfers guarded by checks, but has no arithmetic between two values (a price times a quantity) and no way
   to require another person's agreement, which is routed to that person instead (Decided 4). Resolved as an
   agent question in the ledger (Q79).
4. **Exception: another person's choice is a decision, not a rule.** Whether a bribe works is decided by the
   person being bribed, not by the judge and not by a rule.
5. **Mid-run rulings: a setting, approved by default.** Source: Brian, 2026-11-09, "can we make this
   configurable? or is that more troubel than it is worth. if so i say yes". Each world gets a setting under
   Options on the Create page, "Judge rulings during a run":
   - **Approved by Create** (default): a ruling that passes the rules check and the test run is installed at
     once, the attempt settles through it, and it decides later identical attempts in the same run.
   - **Wait for my approval**: the proposed rule is held, not installed, and the attempt waits as pending; it
     changes nothing while it waits. The run goes on for everyone else, and a later identical attempt joins the
     same pending ruling rather than calling the judge again. The run page lists the held ruling with Approve
     and Reject buttons. On Approve the rule installs and each pending attempt settles through it; on Reject each
     pending attempt is refused, naming the rejected ruling. Nothing settles without an installed rule.

   Wait mode, inferred by agent, 2026-11-09. Basis: the earlier wording let a ruling settle its own attempt with
   nothing installed, which is an outcome with no rule; that breaks the invariants that installed rules alone
   decide consequences and that the judge never writes outcomes (cold review of 2026-11-09, finding 2). Resolved
   as an agent question in the ledger (Q80).

   Either way the run page lists every ruling. The setting travels with the world the way "Simulate as" does
   (`scripts/world_builder_service.py:1603`, saved at `:478` and `:645`). Agent's basis for calling it cheap: both
   settings use the same install step; "wait" holds it during the run and the Approve button calls it.
   Extra work over the default alone is one Options control, one saved field, a pending state for an attempt,
   Approve and Reject buttons and their endpoint, and a test per setting (guess: about a day of agent work).

## Decided: constraints, decisions and norms

Source: Brian, 2026-11-09, closing the discussion with "i liek the ostrom stuff" after the refinement quoted below.

- **Constraint:** what the world makes possible or impossible. Nobody can break it. Examples: you cannot hand
  over coins you do not have; a truck with no fuel does not move. The engine owns these (checks, declared laws
  in `src/world_substrate/laws.py`, propagation).
- **Decision:** what a person chooses among the things the constraints leave possible. Examples: the trader
  offers 40 coins; the officer accepts or refuses, then signs or does not. People (Concordia residents) own
  these. An attempt that needs another person's choice goes to that person; today only plain requests do this
  (#326).
- **Norm (society's rule):** what people expect or forbid, which can be broken. Example: bribery is illegal.
  Detection and enforcement are separate mechanisms: a human may notice and decide to act, or an authored
  automatic monitor may respond. A breakable norm must not be written as a declared
  law: the engine refuses every step that breaks a declared law, so nobody could ever take a bribe.
- **The judge's job** is narrow: when the rulebook is silent, rule on constraints only (can coins change hands
  here? what actually opens the gate?), write the ruling as a rule, and route every choice to the person whose
  choice it is.

Brian's refinement, 2026-11-09: "there is a ddifference between as igned release clearing the cargo as a norm
and like some programmatic enry with abar code or whateve.r this was deiscussed pretty extneively in the form of
hte idea of a password managed comptuer where only 1 person was supped to use it with ehir password but if they
could be social engineered for exampel to get a password then someone else woul eb abel to sue it. i liek the
ostrom stuff". So authority splits three ways:

- **What the mechanism checks** (constraint): the computer logs in whoever types the right password; a barcode
  gate opens for whatever valid code it reads. A gate a guard opens combines the guard's decision with the gate mechanism; its opening is not implied by institutional permission alone.
- **Credential access and custody** (distinct facts in the world): Alice can recall a password; the trader holds a signed
  release. Disclosure, copying, forgery and phishing are distinct mechanisms, not capabilities implied by a credential label.
- **Who is supposed to use it** (norm): only Alice should log in; only signed cargo should pass. Breakable.

Writing "only Alice can log in" as a constraint would make social engineering impossible, which is wrong.

What the earlier Cybernetic Influence work (v3) already settled, to reuse rather than re-derive (searched
2026-11-09; the original chat discussion was not found in the chat archive, and v1 and v2 survive only as Drive
archives, so these come from v3's code and docs; paths below are in the `cybernetic_influence_v3`
repository):

- It kept four things apart: identity proof, normative permission, technical availability, and the physical
  outcome (`docs/archive/plans/005-physical-access-generalization.md:20-26`); "software enforcement differs from
  written permission" (`docs/archive/plans/011-purchase-payment-representation-boundary.md:52`).
- A credential was a protected verifier string, and whoever submitted the matching string was accepted
  (`src/cybernetic_influence/causal_core/fixtures.py:79-95,391-396`). Who holds the credential was not recorded.
- Social engineering and tailgating were explicitly out of scope (`src/cybernetic_influence/api.py:6716`), and
  "a claim of authority distinct from actual technical control" and "a norm or obligation distinct from personal
  preference" were listed as not represented
  (`docs/research/general-purpose-simulator-ontology-and-machinery.md:1071-1085`).

So this plan adds what v3 left out: who holds each credential, as a fact that can change (told, stolen, phished),
and norms as breakable declarations whose detection and enforcement are separate from technical prevention.

## Q76 design contract: possession, knowledge, verification and norms

**Status and source:** agent-inferred design, 2026-11-12, under Brian's approval to resolve the remaining
modeling contracts before implementation. This settles J4's representation choice; it does not claim J4 is
built. It applies Brian's password example above, the [modeling guide](../model/modeling-choices.md),
Decision 003's semantic/mechanical boundary and Decision 006's scope. No new cognition engine or scheduler.

**Represent distinct things, not a universal `authorized` flag.** A credential declaration identifies the
credential, its issuer/verifier, its validity/version and the mechanism accepting it. A person's modeled
access to its content is a separate actor-scoped information record; custody of a physical token is a
separate custody relation. Neither institutional permission nor an analyst's statement that someone is
"authorized" supplies either. These are proposed declaration fields, not claims about today's schema.

For the password fixture, use a symbolic credential value and an explicit equality verifier. Alice can have
access to the value; telling it creates a new recipient's information access without removing Alice's.
A physical key, by contrast, transfers custody only through its declared transfer mechanic. Copying a key,
forging a signature, guessing a password, or remotely using a token requires a separately represented
mechanism; the word "credential" does not grant those capabilities. A computer may check identity as an
additional technical condition, but the password-only fixture must not silently add it. A human guard's
choice belongs to the guard's policy; a reader device's predicate belongs to program mechanics.

**Submission and visibility.** An access attempt binds actor, target verifier and the presented symbolic
value/token. The verifier compares presented evidence with current valid state; it never infers agreement
from a norm. An actor may present a value already in that actor's available information, or make an explicitly
represented guess. Knowing the credential's public id is not possessing its secret value. The interpreter
must not fill in a hidden value from omniscient state. Protected credential information uses the existing
`InformationState`/`DeliveryState` visibility seam (`src/world_substrate/information.py`), not a freely visible
ordinary entity field: that module's generic visibility helper currently passes other entity types through.
All actor-facing prompt, candidate-action and rendering paths must respect the same boundary. A symbolic
model stores no real service secrets and does not claim to model cryptographic strength.

**Acquisition and change.** A disclosure decision is Alice's, using her own observations and policy. The
communication mechanism records what was transmitted and delivered. Delivery establishes modeled access to
content, not belief in the sender or willingness to use it. If memory loss, attention or mistaken recall
matters, its actor-policy/observation model must represent that distinction; the minimum fixture explicitly
assumes retained, accurately usable content after delivery. Revocation or rotation changes the verifier's
valid state, not other actors' historical memories. Old content can remain known and cease to work. Every
copy/delivery records its source lineage; it is not automatically a hard cause of a later login.

**Norm declaration and enforcement.** J4 represents a norm as data: id, applicable actor/role, modality
(must/must not/may), described action, applicability conditions, and any declared enforcement actor/process.
A violation predicate can record an event in the analyst trace without refusing the attempted action. This
is the local minimal representation of the existing five-part norm discussion, not a claim of complete
Institutional Grammar support. An observation mechanism separately determines who learns of the event.
A human enforcer then chooses its response; an explicitly modeled automatic monitor may trigger its own
programmed response. Neither a violation nor an omniscient audit row supplies a human with knowledge.
Mandatory prevention is a separate technical rule and must be described as such. An ambiguous norm can
remain contested information rather than acquiring a fabricated machine-decidable violation test.

**First-principles checks and tradeoff.** A correct-password login by Mallory succeeds under a password-only
verifier even if Alice alone is permitted; a revoked password fails although Alice remembers it; delivery
to Mallory does not reveal it to everyone; observing a breach does not compel a guard to sanction it. Each is
a counterexample to collapsing two representations. Symbolic credentials preserve these distinctions
without simulating cryptography. They cannot answer questions about password entropy, side channels or
physical key duplication unless those mechanisms are deliberately added. These limits are scenario choices,
not a reason to turn every person into a prescribed responder. J4/A6 still must demonstrate the contract,
including direct submissions and actor-view leakage checks; the design decision alone closes no runtime defect.

## Pre-plan baseline (read from code at origin/main `0dcbcd6`, 2026-11-09)

Historical baseline, not current status. J0 removed the cap for new runs; J1–J3 added consequence reports, the judge and sealed mid-run rulings. The Status section above is the current progress authority.

- **Propagation exists but is capped.** `timing: immediately` processes run in waves inside one commit
  ([Decision 009](../decisions/009-same-moment-knock-on-effects.md); `src/world_substrate/engine.py` `_settle`).
  Each (process, entity) pair fires at most once per moment, and each reaction cites its parent. A moment with
  more than `REACTION_LIMIT = 32` reactions is refused whole (`engine.py:1005`, `:1153`).
- **Blockers reach only the person who tried.** A refused attempt names its failed checks to that resident; no
  other component reads them.
- **There was no AI judge in the World Builder path.** Concordia's game master was kept off on purpose
  (`scripts/concordia_residents.py:6`); J2 (2026-11-10) turns on its `EventResolution` for unmatched attempts.
  This repository's own earlier version, in a spike and not in the World Builder, is in Prior art.
  An attempt the installed kinds do not fit goes in as unmatched and changes nothing
  (`scripts/run_authored_world.py:576-580`), except a request, which reaches the person asked (#326, `14afa48`).
- **An earlier "not yet".** The open-attempt plan's D2 (Brian, 2026-10-26) declined an AI game master inventing
  effects for uncovered attempts (`docs/plans/open_attempt.md`, Decisions). Brian's 2026-11-09 approval above
  replaces it with a narrower judge: rulings on constraints only, which become checked rules.
- **Approval comes before a run.** Pressing Create simulation is the approval (RULE-APPROVAL-BEFORE-RUN,
  `docs/model/ODD.md` 8.7); until J3 the World Builder installed no rule mid-run. The spike path did install
  rules mid-run (Prior art, Decision 007, ODD 8.19). Slice J3 (built 2026-11-10) changes this for the World Builder
  (Decided 5): under "Approved by Create" a checked ruling is installed as a rule of the running engine (the world's
  own rules and fingerprint stay as approved; installed rules are sealed run state), and under "Wait for my approval"
  nothing is installed until the owner presses Approve.

## Q96 design contract: a voluntary exchange requires a particular offer

**Status:** design decision inferred by agent, 2026-11-12, during Brian’s requested preimplementation audit. It implements the already-approved rule that other people’s choices stay theirs. No offer lifecycle described here is built yet; Q96’s observed implementation defect stays open until the contract is implemented and checked.

**Existing seams and chosen ownership.** `scripts/run_authored_world.py` currently routes requests through `reach`/resident observations and records pending attempts under `scripts/rulings.py`’s `Rulebook`. `scripts/world_builder_service.py` seals snapshots, approvals and rulings across one-round requests. A message in memory is not durable consent. Add a typed `offers` list to that same server-sealed run continuation, not to resident memory and not to the reusable rule definition. The run coordinator in `scripts/run_authored_world.py` owns offer lifecycle and routes decisions; `scripts/rulings.py` continues to own rule lifecycle. World effects remain one atomic Engine transition. The server’s continuation/share serializers and seal must carry `offers` with the snapshot and rulings; no new database, service or scheduler is needed for this bounded slice.

**Scope.** This contract covers voluntary two-party exchanges under existing or judge-proposed exchange rules, including receiver-shaped and giver-shaped rules. It is not a universal prohibition on taking others’ goods: theft, dropping a gift and automatic mechanical transfers are distinct explicitly authored mechanisms, not a bypass that relabels a voluntary exchange. Multi-party agreements, escrow and exchanges requiring several independently committed actions are outside this slice. If the existing rule language cannot express all agreed settlement effects and checks in one atomic transition, refuse with a language gap; never perform a partial bargain.

**Rule binding.** An exchange rule declares its voluntary-exchange role mapping: proposer/giver field, respondent field, transferred-resource fields, conditions and settlement effect scope. The compiler/checker verifies these names against the typed action and derived reads/writes; the reviewed mapping is retained with the exact rule fingerprint. Runtime guards use that mapping, not action-name keywords or the judge’s one-time `whose_choice` string. Receiver-shaped settlement can run only for the offer’s named respondent and giver; giver-shaped settlement is the proposer’s previously authorized conditional move released by the respondent’s matching acceptance. Neither shape supplies authority for substituted people or goods. A rule with ambiguous exchange roles is a language gap. Relabeling an exchange as theft to avoid these checks is a model-authoring defect, not an authorized automatic fallback.

**Record and identity.** Each offer records a run/branch-local `offer_id`, origin attempt/event id, proposer, intended respondent, typed immutable settlement parameters (participants, items, quantities and every condition), a canonical terms hash, creation round, expiry round, required rule kind and eventual exact rule fingerprint, lifecycle state, and terminal event/reason. The terms must say who supplies each resource and what the other party is asked to do. An ambiguous interpretation produces a recorded refusal or request for clarification, not a partly specified executable offer. After creation, changing price, quantity, party or condition creates a new offer id; neither a model nor delayed rule approval edits the existing terms.

**Creation and delivery.** A proposer’s authenticated actor attempt creates an `offered` record only after its typed terms and party identities validate. Creation reserves or moves no assets. It supplies the proposer’s conditional assent to those exact terms, not the respondent’s assent. The named respondent receives the terms and id as an observation at the existing end-of-round request-delivery seam; others receive no private offer contents. Repeating the same origin attempt is idempotent. Deliberately making another offer creates a distinct record, even when its terms match.

**Response and feasibility.** Only the named respondent’s own action can reject or accept an active offer, naming its id and terms hash. The interpreter resolves their words to that offer; no inferred consent from an earlier conversation, silence, owner approval or a general rule installation is accepted. Rejection is terminal. Acceptance triggers settlement only when the exact approved rule is installed and the offer is still valid. The coordinator checks the parties, terms, expiry and state, then submits the one bound settlement action to the Engine; the Engine rechecks current resources, location and all installed blockers. A failed feasibility check is recorded as terminal `failed` with no asset change; a new attempt requires a new offer. An accepted response awaiting rule approval is retained as `accepted_pending_rule`, with no effects, and the same checks run again when that rule becomes available.

**Expiry and withdrawal.** The bounded default is expiry after the respondent has had its next scheduled decision opportunity: an offer created in round r remains valid through the end of round r+1, then expires before r+2 decisions. In this round-based path that is an explicit approximation, not a general account of human agreements. Waiting for the owner to approve a rule does not extend it. The proposer may withdraw an unsettled offer through their own action; the respondent may withdraw an `accepted_pending_rule` response before settlement. Expiry/withdrawal is terminal and recorded. No automatic renewal or reassignment occurs. Outstanding offer decisions or scheduled expiry remain pending work for quiet-stop assessment; a budget or explicit round limit can still end a run, leaving the unfinished offers visible in its final record. A later authoring change may declare a different scenario-specific lifetime, but this first slice uses the stated default consistently.

**Delayed approval binding.** A held rule and an offer are different records. Rule approval may install a general capability, but cannot create an offer, supply either party’s consent, revive an expired offer, or settle arbitrary attempts merely because their action kind matches. Bind a pending offer to the fingerprint of the exact checked rule whose settlement parameters and effect scope were shown with its terms. A revised rule with different effects invalidates that binding; obtaining a new offer and response is required. If approval arrives while an offer is still open and unaccepted, route it to the respondent; do not settle it. If it arrives for `accepted_pending_rule`, revalidate every term and current check before settlement. Rejection of the required rule makes the pending offer terminal `rule_rejected`.

**Consumption, discovery and replay.** Every entry path to a voluntary exchange action uses the same offer guard: direct interpreted actions, discovered actions, newly installed rulings and resumed pending attempts. Discovery may expose only the named respondent’s currently valid offers for acceptance; direct submission still rechecks, so hiding a move is not the enforcement boundary. The exact terms supply the settlement fields; the resident cannot substitute another giver or amount. Prepare effects and the offer’s terminal state on the same local run-state copy: publish a sealed continuation only when the Engine has committed the whole settlement and the offer is marked `consumed` with that event id. On refusal publish no asset change and the terminal failure record. A crash before producing a continuation does not publish a partial result. Within a branch, consumed/terminal offers cannot settle again; replay of an old sealed snapshot is a replay/fork, not a second settlement in the current branch. Record creation, delivery, response, approval binding, refusal and consumption so replay uses those records without asking a model or inventing consent. Old saved runs without offers continue to replay under their recorded semantics; they are not evidence that the repaired contract holds.

**Why this settles the design question.** Consent is specific to parties and immutable terms; a reusable transfer rule contains neither. Therefore changing the judge prompt or rule actor alone cannot repair Q96. A sealed per-offer lifecycle makes both the giver- and receiver-shaped bypasses checkable while preserving the original profile, existing rule installation and atomic world-effects boundaries. Implementation evidence must exercise both shapes, delayed approval, altered terms, expiry, duplicate submission and infeasible settlement before Q96 is closed.

## Requirements

| Id | Requirement | Source | Check |
| --- | --- | --- | --- |
| R1 | A knock-on chain of any length runs to the end in one moment; loops still cannot repeat | Brian 2026-11-09 (Why) | A1 |
| R2 | The judge's input holds what the engine can compute without a rule (the moves and checks open to the person acting and each person the attempt names, and the named things' values), and, before anything is installed, the test-run report of its proposed rule | Brian 2026-11-09 (Why); two-pass order (Canonical example, inferred by agent) | A2 |
| R3 | The judge decides only attempts no rule covers; a covered attempt whose check fails is refused by the engine with no judge call | Decided 2 | A3 |
| R4 | A ruling becomes a rule after the rules check and test run and then decides the same attempt for everyone; a ruling the language cannot express is refused and recorded as a language gap | Decided 3 | A4 |
| R5 | Another person's choice goes to that person, not to the judge or a rule | Decided 4 | A5 |
| R6 | Mechanism, credential holder and norm are separate; a credential can change hands; a norm can be broken | Decided (norms) | A6 |
| R7 | The judge is Concordia's game master (`EventResolution`), conditioned on our data and configured only through its resolution steps (typed questions in the declaration language); no judge agent or component of our own (Q91) | Decision 006 | A2 (trace) |
| R8 | Every run keeps its full trace, read before any slice is reported | workspace rule (Trace visibility) | A1-A8 |
| R9 | A world's setting chooses whether checked rulings install during the run (default) or are held with the attempt pending until approved; the run page lists every ruling | Decided 5 | A4 |
| R10 | Each saved run records the reaction limit it ran under, and replay uses the recorded value, so runs saved before J0 replay unchanged | goal boundary "saved worlds still replay unchanged" (inferred by agent, Agent technical calls) | A7 |
| R11 | The person can write a stopping point in plain words ("stop once the team has agreed a budget"); after each round the judge assesses whether it has been reached, and the run stops when it has, as one more condition of the world's "When to stop a run" setting beside quiet rounds, a round limit and a spending limit (whichever fires first) | Brian 2026-11-10 (Stopping point) | A8 |

All eleven are required; none is deferred.

### Stopping point (Brian, 2026-11-10)

Brian, 2026-11-10: "i should be able to stop a world based on budget or number of rounds or a natural langue stopping
potin that the judge assesses once we build him". The round limit and the spending limit are built (`scripts/run_stop.py`,
`max_rounds` and `max_spend_usd`, OpenSpec requirement "A run stops at a round or spending limit"). The stopping point
in plain words waits for the judge (slice J5): the world's `run_stop` setting gains an optional `stop_when` text; after
each round the judge (Concordia's game master, R7) is given that text and the round's world state and answers reached
or not, with its reason; when reached, the run stops with `reason: stopping_point` and the judge's reason in the run
page's one line, through the same `limit_check` path, so whichever condition fires first still wins. Its cost counts
toward the run's spending limit like every other call of the run.

The question asked is "has this stopping point been reached?", handed to the game master as one more event to
resolve in its normal way, with the stopping text as the event and the world state as its context; it is a thin
framing of Concordia's resolution step, not a judge prompt of our own (R7). Cost (computed, guessed run length): one
call per round, 46 rounds (the Waltzman run of 2026-10-23, `evidence/waltzman-tasks-slice2/c1r24`) × (15,000 input
tokens × $0.10/M + 150 output tokens × $0.50/M, gpt-6-luna, no cached share) = about $0.07 per run. Trigger (normative correction, 2026-11-12): assess after every completed round as R11 requires. A fingerprint of mutable material fields is insufficient: a deadline, a delivered message or a pending offer can change whether the condition holds without such a field changing. A six-quiet-round backstop can miss the requested stopping point. Skip a repeated assessment only when all dependencies of that condition are known and unchanged; unrestricted natural-language conditions provide no such dependency proof, so the default is one assessment per completed round. Budget and round limits still apply before further work. This resolves the trigger by counterexample, without a comparative run.

A cheaper option for this check, a Jev chance question at about 1/50 of the cost, is recorded in [the estimate rules plan](estimate_rules.md) (Q86); the choice stays with J5.

## Acceptance checks

Each is judged on the run page, from the full trace of the run it names, not its outcome alone. The steps and
results below are in the run page's own words; the record files behind each are listed in
`docs/planning/ai-judge/acceptance-criteria.json` (field `evidence`).

- **A1 (J0):** the saved run "fifty chains" (50 chains of 100 steps set off in one moment) shows a summary line
  "5,000 steps run, 5,000 with a cause, no refusal"; any step opens to the step that caused it; in the saved run
  "loop", each rule fires once for each thing and the moment ends; in the saved run "truck without fuel", step 40
  shows "blocked: the truck has no fuel" in orange and no step follows it.
- **A2 (J1, J2):** on the saved run "port bribe" (`evidence/ai-judge/j2/port/`; its world is the whole
  description "A small port: Rosa, the customs officer, signs inspection releases. Vik, a trader, has 40 coins and a crate he has not declared.", with the fixture rules in `tests/judge_worlds.py` `port()`), Vik's offer opens to what the
  judge was given first: the facts (Vik holds 40 coins; Rosa and Vik are at the customs desk) and, under Rosa's
  moves, "sign release: blocked, inspected is false"; then the rule it proposed (a rule that lets coins change
  hands, written as Rosa's own move), the test-run report of that rule (coins move to Rosa, Vik's purse empties,
  nothing else follows), and its confirmation; the judge panel says the ruling came from the world's game master
  and everything above appears in what the judge read. In the saved run "blocked chain ruling", the test run shows
  "blocked at step 40: the truck has no fuel", and that blocker is in what the judge read before it answered. In
  the saved run "long line ruling", the proposed rule sets off 5,000 steps: the judge read the net changes
  (grouped, with their count), no blocker, chain length 5,000 and "settled", while the run page lists all 5,000
  steps (the net-change report, not the whole chain, is what the judge reads).
- **A3 (J2):** once the coin rule is installed, the saved run "empty purse" shows a trader with no coins offering
  coins (briefed to bluff; residents never did it unprompted): the offer is covered by that rule, is refused with
  "the giver holds that many coins" (the rule's own check), nothing changes, and its row says "Decided by rule,
  judge not asked".
- **A4 (J3):** with the default setting, the run page's ruling list shows the coin rule as "installed, passed the
  rules check and test run", and a second trader's later offer says "decided by rule, judge not asked". With
  "Wait for my approval", the ruling shows "held" and both offers show "pending: waiting for your approval" with
  nothing changed; after Approve each settles only if its own live Q96 offer has matching acceptance and remains feasible; after Reject both are refused, naming the
  rejected ruling. In the saved run "price times quantity", a ruling the language cannot express is refused with
  "no rule could express this" and listed as a language gap.
- **A5 (J2 routing; Q96 lifecycle not built):** Vik's exact offer leads to Rosa's own acceptance or refusal;
  acceptance of an unconditional payment does not imply a signature. If signing is an explicit settlement
  condition, the whole bargain must satisfy current constraints atomically or be refused. The Q96 lifecycle
  above and A5 in the acceptance record require both giver- and receiver-shaped rules to bind live offer terms,
  reject altered/stale/duplicate offers, recheck delayed approval and feasibility, and record terminal
  consumption/failure for replay. Earlier request routing is partial evidence, not a passing lifecycle contract.
- **A6 (J4):** in the saved run "password", Mallory phishes Alice's password, the computer logs Mallory in, the
  run page shows "norm broken: only Alice should log in", and a consequence follows only after someone who saw it
  acts. In the port, the gate opens because it read a valid code, not because of who holds it, and the cargo
  norm's breach is shown separately. Following Ostrom's grammar, each norm and rule reads as who it applies to;
  must, must not or may; what; when; and, for an enforced rule, what happens otherwise and who enforces it, so a
  norm with no "otherwise" reads differently from an enforced rule.
- **A7 (J0):** a run saved before J0 that stopped at the old limit replays on the run page exactly as saved,
  showing "refused: knock-on effects did not settle within 32 steps (the limit this run ran under)"; a new run
  of the same world has no such limit. The existing test of that refusal
  (`tests/test_open_attempt.py:466-501`) is kept, run against the recorded limit.
- **A8 (J5):** build a team world from the description "A small team of three, Ana, Ben and Cai, must agree a
  budget for the quarter; each can propose an amount and each can accept or counter" with Options, "Stop when" set to "stop once the team has agreed a budget"; run it.
  When the team agrees a budget, the run stops after that round and the run page says "Stopped at round N: the
  team has agreed a budget (the judge's reading of your stopping point)", with the judge's reason opening to what
  it read; in the rounds before, each round's panel shows "stopping point: not yet" with its reason. With a round
  limit of 3 as well and no agreement by then, the run stops at round 3 on the round limit instead.

## Slices, in order

Each slice is one pull request, merged through `ship` after `scripts/check_project.py` exits 0, and ends in a
traced run.

| Slice | Change | Epistemic state | Acceptance |
| --- | --- | --- | --- |
| J0 | Remove the 32-reaction cap; keep once-per-pair-per-moment; each saved run records the limit it ran under and replay uses it | fully specifiable now | A1, A7 |
| J1 | Consequence report: pass 1 (`engine.discover` for the person acting and each person the attempt names, plus the named entities' current values) and pass 2 (a proposed rule test-run on a copy of the world: its net changes, blockers, chain length and stopping point, with the full chain in the run record) | J1 is built and J2 retains report-delivery evidence; which named people and entities an attempt yields still depends on the interpreter. The complete acceptance demonstration and semantic benefit are not established merely by delivery | A2 (data) |
| J2 | Judge: turn on Concordia's `EventResolution` for unmatched attempts, given the whole world plus pass 1; it proposes a rule, reads the pass 2 report, then confirms, revises once or withdraws; choices go to the person | conditional on J1 | A2, A3, A5 |
| J3 | Ruling to rule: install the confirmed rule (or hold it with the attempt pending, per the world's setting); refuse with "no rule could express this" and record a language gap when the rules check rejects it | built 2026-11-10, live `cab821d` 2026-11-11 (`scripts/rulings.py`; `openspec/specs/ai-judge`; open defect Q96) | A4 |
| J4 | Credentials, actor-scoped access and breakable norms under the Q76 contract | representation design settled; declaration/compiler/visibility implementation unbuilt | A6 |
| J5 | Stopping point in plain words: `run_stop.stop_when`, assessed by the judge after each round, stopping with `reason: stopping_point` through the existing stop check | conditional on J2 | A8 |

J0 first because it is small, independent and delivers Brian's "100 links deep" alone. J4 remains a later
implementation slice: Q76 now settles its representation, while credential visibility and enforcement
integration still require their own implementation and acceptance work.

## Agent technical calls

- **Remove the 32-reaction cap** ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)): each
  process and entity pair already fires at most once per moment (`engine.py` `_settle` docstring), so a chain
  cannot loop without it, and Brian's example (50 chains, 100 links deep) needs 5,000. The bound becomes the
  number of (process, entity) pairs, which is finite. J0 amends Decision 009 in the same pull request.
- **Saved runs replay under the limit they ran with** (inferred by agent, 2026-11-09). Each run record gains the
  reaction limit it ran under; replay reads it (a record with none was made under 32), so a run once refused for
  "reaction_limit" replays as refused, while new runs use the new setting. Basis: the refusal status is written
  into the run's commands (`engine.py:1005`; checked by `tests/test_open_attempt.py:466-501`, which stays), so
  replaying old runs with no limit would change their outcome and break the boundary "saved worlds still replay
  unchanged" (cold review of 2026-11-09, finding 2). Resolved as an agent question in the ledger (Q81).
- **The judge is Concordia's own game master** (`concordia/components/game_master/event_resolution.py`,
  `EventResolution`), conditioned on a component that supplies the consequence report, not a judge of our own
  (Decision 006). Its output is a proposed rule in the existing declaration language, never an outcome. It
  works in two passes (Canonical example): it reads the whole world plus pass 1, proposes a rule, reads the
  pass 2 test-run report, and confirms, revises once or withdraws.
- **Norms are not declared laws.** J4 adds a separate breakable-norm declaration; `laws.py` keeps refusing only
  true impossibilities.

## System model

- Model: [docs/model/ODD.md](../model/ODD.md). Relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a refused attempt
  changes nothing), RULE-PROJECTION-FROM-CANONICAL-ONLY, RULE-DURABLE-RUN-RECORD. Changed:
  RULE-APPROVAL-BEFORE-RUN gains one exception for checked judge rulings when the world's setting allows it
  (J3, Decided 5); 8.20
  knock-on effects loses the reaction limit (J0). Adds: `consequence report` (J1), `judge ruling` (J2),
  `ruling-origin rule` (J3), `credential holder` fact and `norm` (J4).
- Scope: this repository's own model, linked from the documentation entry point. Not changed: actors, places,
  information reach, tasks, the budget ledger.
- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) gains the J1-J4 types, each mapped onto the
  scientific-hypergraph kernel; each slice updates ODD.md, `world_substrate_model.toml` and
  `tests/test_system_model.py` in the same pull request.
- The trace must show, per element: the consequence report attached to the attempt's event; the judge's
  Concordia call with its component text and `llm_client` trace id; the rule's origin (ruling id, round) and its
  rules-check record; the credential's holder before and after; each norm breach and the act that followed.

## Trace visibility

- Each run's `run-log.jsonl` records the inputs (scenario text, bundle hash, seed), every round and attempt, each
  model call (resident, interpreter, judge, rules review) with its messages, typed result and `llm_client` trace
  id, the model's reasoning where returned, every engine event with its parent and blockers, and the output.
  Kept for every run, not only failures.
- How to open one: `evidence/ai-judge/<run>/run-log.jsonl` (`jq . <file>`), its `TRACE_READ.md`, and
  `python -m llm_client traces --trace-id <id>` for a call. All of a run's calls share one trace id
  (`world-builder-live-run-<uuid4 hex>`).
- Who reads: the implementing agent reads every judge call, every ruling and every refusal in full, and at least
  five ordinary attempts per run across rounds and actors, before reporting a slice.

## When a run fails or surprises us

Keep the run and its trace id; read its full inputs, prompts, tool calls and output before choosing a fix; cite
where it diverged; classify the cause as evidence absent, evidence unused or contradicted, invalid expectation, or
unresolved. An unresolved cause permits investigation, not a fix. Verify a fix with a new traced run and keep the
original. Trace-review criteria: A1-A8, each `expected_outcome: pass`.

## Capability reuse

No catalogue entry fits, because `reuse_candidates.yml` and `capability_registry.yml` hold search, approval,
notification and document wrappers, none of which judge actions or run rules (searched 2026-11-09 for judge,
adjudication, game master, norm and institution: no hits). Reused, not catalogue entries: Concordia's
`EventResolution` (the judge), the World Builder rules check (`scripts/world_builder_service.py`), and `llm_client`
for every model call. No new cross-project capability.

## Prior art

- Concordia's game master components (`EventResolution`), already a dependency, kept off until now.
- This repository's own earlier game master that writes rules mid-run: `spikes/any-scenario-2026-10/midrun.py`
  (Decision 007, Brian 2026-10-07: "The game master should be able to write new rules mid-run, not just make
  one-off rulings"; ODD 8.19). For an attempt no rule covers, its own rule writer proposes a general rule, the
  layer-1 checks run on the whole model, a pass installs it into the running engine's registry and a fail is a
  one-off ruling; no person approves. Its runs recorded 27 rules (`rules_written_mid_run`: 3 in
  `spikes/any-scenario-2026-10/evidence/waltzman/run/summary.json`, 24 in `.../waltzman-spec/run2/run/summary.json`)
  and about $0.10 per attempt (the comment in `midrun.py`). It was a spike, not in the World Builder. J2 does not reuse its
  rule writer (R7: the judge is Concordia's component, conditioned on pass 1 and pass 2, which the spike lacks);
  J3 read its install step and keep-or-drop record (Q90, 2026-11-10): the spike's `_install` registers a compiled action in
  the running registry, the step J3 reuses (`Rulebook.install`, after the World Builder's rules check on the world as it is
  now); its rule writer and its keep-or-drop check are not reused. Of the 27 rule-writing attempts in the two saved
  runs, 6 were installed (all in `waltzman-spec/run2`) and 21 ended as a plain ruling with nothing installed.
- Crawford and Ostrom (1995), "A Grammar of Institutions": a rule is Attributes, Deontic, aIm, Conditions, Or
  else. Its split between a norm (no "or else") and a rule (an "or else" someone enforces) matches the
  constraint, decision and norm split above. J4 starts from it and from Institutional Grammar 2.0 (Frantz and
  Siddiki) before designing anything.
- Cybernetic Influence v3's separation of identity proof, permission, availability and outcome (above).

## LLM call boundary and cost

Call graph per round: resident (existing) -> attempt interpreter (existing) -> engine pass 1 (code) -> judge
proposes a rule (new, only for an unmatched attempt) -> rules check and engine pass 2 test run (existing code
plus the existing rules review) -> judge confirms, revises once or withdraws (new). Same model and route as the
interpreter (`openrouter/openai/gpt-6-luna`, `scripts/run_authored_world.py:38`).

Prices: gpt-6-luna is $0.10 per million input tokens and $0.50 per million output tokens (above 272k input
tokens, $0.20 and $0.75), from `~/code/llm_client/llm_client/data/default_model_registry.json`
(`forecast_pricing`, source openrouter, checked 2026-11-05).

What the judge reads, measured from saved worlds (2026-11-09):

- **The whole world.** The largest saved world, `evidence/waltzman-tasks-slice2/c1r21`, is 34,863 characters of
  bundle, 79,457 of rules and at most 29,110 of state, 143,430 characters in all. At the measured 3.40
  characters per token (the three plain-baseline calls below), that is about 42,200 tokens.
- **The full chain.** One chain step (an event and its parent) averages 340 characters (2,081 steps measured
  across the saved runs; median 271, 90th percentile 563). Brian's 5,000-step example is then about 1.7 million
  characters, about 500,000 tokens: larger than the judge should read, and above the long-context price step.
  So the pass 2 report gives the judge the net changes, the blockers and the chain's length and stopping point;
  the full chain stays in the run record and on the run page. The net change is at most the size of the state
  (29,110 characters, about 8,600 tokens). The most steps in one round of any saved run today is 24.
- **Worst case per judge call:** about 42,200 + 8,600 + 2,000 (attempt, pass 1 and instructions) = 53,000 input
  tokens and about 1,300 output tokens, so 53,000 x $0.10/M + 1,300 x $0.50/M = about $0.006.

Cost per run:

- **Interpreter (measured):** `llm-cost estimate`, 114 calls, $0.0281, median 1,651 input and 160 output tokens
  per call, about $0.00025 per call. The saved airfield run (`evidence/open-attempt/s1-airfield`) read 36
  attempts in 9 rounds, so about $0.009 per run of that size.
- **Judge (computed):** a typical call is 15,000 input tokens (the three plain-baseline calls measured 9,938 to
  17,922) and 1,300 output tokens (measured 1,184 to 1,396). Two calls per unmatched attempt (propose, then
  confirm) and 10 unmatched attempts per run (the airfield run had 10 of 36): 20 x (15,000 x $0.10/M + 1,300 x
  $0.50/M) = $0.043 per run, falling as rulings become rules.
- **Rules review (computed):** tokens measured by `llm-cost estimate --task world-substrate-rules-review` (24
  calls on earlier review models, median 9,407 input and 2,856 output tokens, no cached share; $0.699 in all, mean
  $0.029). The current review model, `openrouter/google/gemini-4-argon` (`scripts/review_rules.py:18`), has no
  input and output price in the registry, only its `cost` field of $4.00 per million tokens, a 3:1 blend of input
  and output (`~/code/llm_client/docs/guides/model-selection.md`), used here for both. One review per ruling, 10
  per run: 10 x (9,407 + 2,856) x $4.00/M = about $0.49 per run. (The earlier models' measured mean gives $0.29.)
- **Total:** about $0.54 per run with 10 rulings; the rules review is most of it.
- **Cheapest design that still does the job.** Decided 3 requires a ruling to pass "the World Builder's
  existing rules check". The model review is not a pass mark: it returns findings only, and a build goes on
  without it when it fails (`scripts/review_rules.py:1-7`). So Decided 3 does not require it; the required part
  is the free declaration check and test run. Dropping the review for judge rulings costs about $0.05 per run
  instead of $0.54 (worked historical workload estimate above, not a new-run forecast).
  **Revised design decision, 2026-11-12 (agent inference):** the extra model reviewer is optional;
  defer it from the minimum required judge path. The sawmill counterexample proves that syntactic checks
  do not establish semantic correctness, but does not prove that another model fixes the error. Require
  the declaration checker, scripted test and trace inspection; do not claim they establish real-world
  validity or all intended semantics. Retain semantic-review findings as advisory where the existing
  runtime already produces them. Changing that runtime is a later implementation slice. Reintroducing
  a mandatory reviewer requires a named failure it corrects that the simpler artifact-checking path
  cannot handle. No comparative run is needed to settle the present design default.
  The judge's test-report confirmation is also unvalidated for semantic benefit; existing behavior is
  documented, not certified as necessary by its presence.

## Plain baseline (run 2026-11-09)

The plain version: the same model, given the whole world (description, bundle, rules and current state) and the
attempt in one call, asked for a ruling written as a rule. Three real attempts that no rule matched, taken from
saved runs:

| Case | Saved attempt | Plain ruling | Rules check |
| --- | --- | --- | --- |
| Sawmill buys logs | `evidence/declared-laws/s2-pencil-2/run-log.jsonl`, line 5: the sawmill offers to pay the logger for 3 cedar logs | buy logs at a price, logger's choice | accepted, but charges the price once rather than per log (the language has no multiplication) |
| Shop offers $1,000 | `evidence/pencil7-trace-audit/run-log.jsonl`, line 14: the shop offers the pencil factory $1,000 for pencils | an offer only, factory's choice; no effects | rejected: "participants must exactly name entity_ref fields" |
| Waiter picks up tray | `evidence/declared-laws/s4-cafe/run-log.jsonl`, line 12: the waiter picks up the tray | allowed: a general move for a waiter to pick up an empty tray from a surface (the tray is on the counter) | rejected: a field named "from" is not an identifier |

Calls: 3, trace id `world-substrate/ai-judge-plain-baseline/b75fd5f42b9742078c798df205243c73`, $0.0061 and 45.3K
tokens (`llm-cost`, task `world-substrate-ai-judge-plain-baseline`; worked out before calling as at most $0.02,
under the $2 stop). Inputs, outputs and the check verdicts: `evidence/ai-judge/plain-baseline/`.

- **Right:** every current value it cited was correct; it named whose choice each attempt needs (the logger, the
  pencil factory, nobody); in the cafe it ruled the pickup allowed and named the blocker the engine's own checks
  name (the carry move needs the tray held by the waiter, and it is on the counter); and it noticed a real gap in
  the sawmill world (the saw-slats move cannot saw logs the sawmill itself holds).
- **Wrong:** 2 of 3 rules were rejected by the rules check (the cafe rule only for its field name "from"). The
  one accepted rule, the sawmill's, was wrong twice: it charges the price once rather than per log, and it moves
  the logger's logs on the sawmill's move alone, although the plain ruling itself said the sale is the logger's
  choice. That second fault is a failure against Decided 4: another person's choice must go to that person, not
  into a rule. The shop rule changed nothing.
- **The test run on the accepted rule (2026-11-09, no model call):** the existing scripted test run
  (`run_world(policy="scripted")`, as `scripts/world_builder_service.py:1797` calls it), 12 rounds of the
  sawmill world with the rule added, tried only 1-log purchases (the rule offers quantity 1 alone) and flagged
  nothing on it. A 3-log attempt submitted directly was accepted: 3 logs moved for 10 coins, where 3 x 10 = 30
  was due. Neither the declaration check nor the test run catches the single-price charge; they catch malformed
  rules only. Evidence: `evidence/ai-judge/plain-baseline/sawmill-test-run.json` (script `sawmill_test_run.py`
  beside it).
- **What this says about the stages:** pass 2's declaration check is shown to stop malformed rules (2 of 3
  rejected, `rules-check.json`), so without it two unusable rules would be installed. That pass 2 stops a wrong
  but valid rule is untested: the test run missed the sawmill price, and whether the judge, reading the 3-log
  report, would revise it is untested until J2, as is whether the one revision fixes rejected rules. Pass 1
  added nothing the plain version lacked at these world sizes (it read the facts correctly from the whole
  world), so the judge starts from the plain input, the whole world, and pass 1 is added because it costs no
  call and names the blockers installed rules already find for the people involved; its value is untested.

## Irreversible actions and spend

Nothing irreversible: each slice is a pull request (revert with git), and the World Builder deploy is redeployable
from the previous commit. No deletion of saved worlds or run records, no outreach, no change to other repositories.
Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 per slice, enforced by the
run's `max_budget`.

## Uncertainties

- **U1 (agent, resolved 2026-11-09 by measurement):** does a consequence report for the largest saved world fit
  the judge's context? The world itself does (about 42,200 tokens); a 5,000-step chain does not (about 500,000
  tokens), so the judge gets net changes, blockers and the chain's length and stopping point (LLM call boundary
  and cost).
- **U2 (agent):** how does the judge tell a constraint question from another person's choice? Settled by
  argument in J2's design: an attempt whose effect needs another resident's act is routed to that resident (the
  #326 path, generalised); the judge sees only what remains.
- **U4 (agent, resolved 2026-11-10 by reading Concordia 2.4.0, Q91):** do configured thinking steps break R7's "no
  judge prompt of our own"? `EventResolution(model, event_resolution_steps, components)` takes steps as its documented
  configuration (`concordia/components/game_master/event_resolution.py`, `EventResolution.__init__`) and conditions on named components; J2
  supplies two components (the world and the consequence report) and steps that each ask one typed question. Read
  as: no judge agent or component of ours; the question text is configuration. Brian may read Decision 006
  differently; if so, the steps are the part to remove.
- **U5 (agent, resolved 2026-11-10, Q90):** what the spike's 27 mid-run rules show, and whether J3 reuses its install step.
  Read free from `rules_written_mid_run` in the two `summary.json` files and `midrun.py`: 6 installed, 21 dropped; J3 reuses
  the install step only. Not done: running the 27 rules through today's rules check as a free replay (they are written
  for the spike's worlds, not these).
- **U3 (agent, Q76 design resolved 2026-11-12):** the Q76 contract above separates verifier state, actor access,
  physical custody, normative permission, observation and enforcement. J4/A6 retain implementation and adequacy
  obligations; symbolic credentials do not certify cryptographic or human-behavior fidelity.

## Needs Brian

None open. Mid-run rulings and approval was answered on 2026-11-09 (Decided 5).

## Not in this plan

Organisations and institutions beyond single norms; an AI judge writing outcomes; any claim that a ruling is true
of the real world.

## Complete actor-information dependency (documentation design, 2026-11-12)

Source: Brian's November 12 documentation goal; design application inferred by agent. The [modeling guide](../model/modeling-choices.md) owns the complete actor-information contract and single-concern example. Credential secrecy (J4) and uncertain delivery (E5) depend on that contract across observation, brief, summary, memory, events, offered actions, refusals and actor-facing UI. Item-level message filtering alone is insufficient. These slices must retain the actual authorized context in restricted evidence and demonstrate that an undelivered fact cannot enter through another surface. Analyst access is separate. This dependency is proposed required behavior, not an assertion that current read scopes or projections enforce it. Implementation remains on hold under the documentation goal.
