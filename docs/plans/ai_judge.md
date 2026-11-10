---
plan_id: "ai-judge"
dependencies: ["open-attempt"]
dependencies_reviewed: "2026-11-09"
planning_path: durable_solo
status: draft
goal:
  outcome: "Worlds stay faithful as they grow too big for an AI to track: the engine works out every knock-on
    effect and blocker of an attempt, however long the chain, and an AI judge that sees those results decides
    only what no rule covers; its rulings become rules for everyone, and other people's choices stay theirs."
  canonical_example: "The port world in 'Canonical example' below: Vik's bribe offer reaches the judge with the
    facts and blockers the engine can compute without a rule; the judge proposes a rule that coins can
    change hands; the engine test-runs it on a copy of the world and shows the judge every knock-on effect; the
    judge confirms, the rule is installed, Rosa decides whether to sign and the coins move only if she does, the
    gate opens for the signed release
    whoever holds it, a 100-link chain from the gate runs in one moment, and the same offer by another trader
    later is decided by the new rule with no judge call."
  forbidden_substitutes: "a judge prompt of our own outside Concordia's game master; a judge that writes outcomes
    or decides another person's choice; a ruling used without passing the World Builder rules check; a norm
    written as a declared law; hand-edited rules or runs; a chain shortened to fit a cap; a fixture run reported
    as live."
  boundaries: "world-substrate and its own deploy only; Concordia and Cybernetic Influence v3 read-only; each
    slice merges through ship after scripts/check_project.py exits 0 on the committed change; saved worlds
    still replay unchanged; owner allowance only for live runs."
  done_when: "Acceptance checks A1-A7 below pass, each judged from the full trace of the run it names."
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

**Status:** complete draft; Brian approved its direction on 2026-11-09 ("i approve", after Decided 5). Not
adopted; nothing is built.

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
directly. **Recurring job and baseline:** a visitor describes a world and watches its people act. Today an attempt
no rule covers changes nothing (except a request, which reaches the person asked, #326), knock-on chains stop at 32
reactions per moment, and a blocker is told only to the person who tried. **Inspectable result:** the port world's
run page and record (canonical example). **Stage and investment boundary:** prototype stage; five slices, each one
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
   on a copy of the world with the exchange settled. The copy's full knock-on chain and any blockers form the
   consequence report: coins move to Rosa, Vik's purse empties, and nothing else follows. The judge reads the
   report and confirms, revises the rule once, or withdraws it. If the language cannot express the ruling (the
   check rejects it, and the one revision is rejected too), the attempt is refused with "no rule could express
   this" and the run records a language gap.
5. Only now is the rule installed. Vik's offer goes to Rosa as her decision; no coins move yet.
6. Rosa's resident decides. If she refuses, the offer lapses and nothing changes. If she accepts, she signs, and
   the coins move through the installed rule in the same moment: they move only because she chose to sign.
7. If she signs, Vik holds a signed release. The gate (a mechanism) opens for the valid code however Vik got it.
   "Bribery is forbidden" is a norm: it was broken, and it has consequences only if an inspector notices and acts.
8. The gate opening sets off the 100-step chain. It runs to the end inside the same moment, each step citing the
   step that caused it.
9. Later, another trader offers a bribe. The new rule decides the hand-over; the judge is not called again.

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
  It has consequences only when someone notices and decides to act. A norm must not be written as a declared
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
  gate opens for whatever valid code it reads. A gate a guard opens is not a mechanism: it opens when the guard
  decides to.
- **Who holds the credential** (a fact in the world): Alice knows the password; the trader holds a signed
  release. A credential can be told, overheard, copied, forged or phished.
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
and norms as breakable rules with consequences only when someone acts on them.

## Current truth (read from code at origin/main `0dcbcd6`, 2026-11-09)

- **Propagation exists but is capped.** `timing: immediately` processes run in waves inside one commit
  ([Decision 009](../decisions/009-same-moment-knock-on-effects.md); `src/world_substrate/engine.py` `_settle`).
  Each (process, entity) pair fires at most once per moment, and each reaction cites its parent. A moment with
  more than `REACTION_LIMIT = 32` reactions is refused whole (`engine.py:1005`, `:1153`).
- **Blockers reach only the person who tried.** A refused attempt names its failed checks to that resident; no
  other component reads them.
- **There is no AI judge.** Concordia's game master is kept off on purpose (`scripts/concordia_residents.py:6`).
  An attempt the installed kinds do not fit goes in as unmatched and changes nothing
  (`scripts/run_authored_world.py:576-580`), except a request, which reaches the person asked (#326, `14afa48`).
- **An earlier "not yet".** The open-attempt plan's D2 (Brian, 2026-10-26) declined an AI game master inventing
  effects for uncovered attempts (`docs/plans/open_attempt.md`, Decisions). Brian's 2026-11-09 approval above
  replaces it with a narrower judge: rulings on constraints only, which become checked rules.
- **Approval comes before a run.** Pressing Create simulation is the approval (RULE-APPROVAL-BEFORE-RUN,
  `docs/model/ODD.md` 8.7); no rule is installed mid-run today. Slice J3 changes this (Decided 5).

## Requirements

| Id | Requirement | Source | Check |
| --- | --- | --- | --- |
| R1 | A knock-on chain of any length runs to the end in one moment; loops still cannot repeat | Brian 2026-11-09 (Why) | A1 |
| R2 | The judge's input holds what the engine can compute without a rule (the moves and checks open to the person acting and each person the attempt names, and the named things' values), and, before anything is installed, the test-run report of its proposed rule | Brian 2026-11-09 (Why); two-pass order (Canonical example, inferred by agent) | A2 |
| R3 | The judge decides only attempts no rule covers; a covered attempt whose check fails is refused by the engine with no judge call | Decided 2 | A3 |
| R4 | A ruling becomes a rule after the rules check and test run and then decides the same attempt for everyone; a ruling the language cannot express is refused and recorded as a language gap | Decided 3 | A4 |
| R5 | Another person's choice goes to that person, not to the judge or a rule | Decided 4 | A5 |
| R6 | Mechanism, credential holder and norm are separate; a credential can change hands; a norm can be broken | Decided (norms) | A6 |
| R7 | The judge is Concordia's game master, conditioned on our data; no judge prompt of our own | Decision 006 | A2 (trace) |
| R8 | Every run keeps its full trace, read before any slice is reported | workspace rule (Trace visibility) | A1-A7 |
| R9 | A world's setting chooses whether checked rulings install during the run (default) or are held with the attempt pending until approved; the run page lists every ruling | Decided 5 | A4 |
| R10 | Each saved run records the reaction limit it ran under, and replay uses the recorded value, so runs saved before J0 replay unchanged | goal boundary "saved worlds still replay unchanged" (inferred by agent, Agent technical calls) | A7 |

All ten are required; none is deferred.

## Acceptance checks

Each is judged on the run page, from the full trace of the run it names, not its outcome alone. The steps and
results below are in the run page's own words; the record files behind each are listed in
`docs/planning/ai-judge/acceptance-criteria.json` (field `evidence`).

- **A1 (J0):** the saved run "fifty chains" (50 chains of 100 steps set off in one moment) shows a summary line
  "5,000 steps run, 5,000 with a cause, no refusal"; any step opens to the step that caused it; in the saved run
  "loop", each rule fires once for each thing and the moment ends; in the saved run "truck without fuel", step 40
  shows "blocked: the truck has no fuel" in orange and no step follows it.
- **A2 (J1, J2):** on the port run page, Vik's offer opens to what the judge was given first: the facts (Vik
  holds 40 coins; Rosa and Vik are at the customs desk) and, under Rosa's moves, "sign release: blocked,
  inspected is false"; then the rule it proposed, the test-run report of that rule (coins move to Rosa, Vik's
  purse empties, nothing else follows), and its confirmation; the judge panel says the ruling came from the world's game master and everything above
  appears in what the judge read. In the saved run "blocked chain ruling", the test run shows "blocked at step
  40: the truck has no fuel", and that blocker is in what the judge read before it answered.
- **A3 (J2):** once the coin rule is installed, the saved run "empty purse" shows a trader with no coins offering
  coins: the offer is covered by that rule, is refused with "blocked: holds 0 coins", nothing changes, and its
  panel says "decided by rule, judge not asked".
- **A4 (J3):** with the default setting, the run page's ruling list shows the coin rule as "installed, passed the
  rules check and test run", and a second trader's later offer says "decided by rule, judge not asked". With
  "Wait for my approval", the ruling shows "held" and both offers show "pending: waiting for your approval" with
  nothing changed; after Approve both settle through the rule; after Reject both are refused, naming the
  rejected ruling. In the saved run "price times quantity", a ruling the language cannot express is refused with
  "no rule could express this" and listed as a language gap.
- **A5 (J2):** Vik's offer leads to Rosa's own choice, accept or refuse, in her words; the ruling covers only
  whether coins can change hands, and the coins move only if she signs. In the saved run "sawmill", a ruling that
  would move another person's goods on the buyer's move alone goes to that person as an offer instead.
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

## Slices, in order

Each slice is one pull request, merged through `ship` after `scripts/check_project.py` exits 0, and ends in a
traced run.

| Slice | Change | Epistemic state | Acceptance |
| --- | --- | --- | --- |
| J0 | Remove the 32-reaction cap; keep once-per-pair-per-moment; each saved run records the limit it ran under and replay uses it | fully specifiable now | A1, A7 |
| J1 | Consequence report: pass 1 (`engine.discover` for the person acting and each person the attempt names, plus the named entities' current values) and pass 2 (a proposed rule test-run on a copy of the world: its net changes, blockers, chain length and stopping point, with the full chain in the run record) | specified by design: pass 1's selection is defined, but which named people and entities an attempt yields depends on the interpreter's reading, and no run has produced a pass 1 page yet | A2 (data) |
| J2 | Judge: turn on Concordia's `EventResolution` for unmatched attempts, given the whole world plus pass 1; it proposes a rule, reads the pass 2 report, then confirms, revises once or withdraws; choices go to the person | conditional on J1 | A2, A3, A5 |
| J3 | Ruling to rule: install the confirmed rule (or hold it with the attempt pending, per the world's setting); refuse with "no rule could express this" and record a language gap when the rules check rejects it | conditional on J2 | A4 |
| J4 | Credentials as facts and norms as breakable rules (Ostrom's grammar) | exploration required | A6 |

J0 first because it is small, independent and delivers Brian's "100 links deep" alone. J4 last because its
representation needs a short design step of its own (Uncertainties, U3).

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
original. Trace-review criteria: A1-A7, each `expected_outcome: pass`.

## Capability reuse

No catalogue entry fits, because `reuse_candidates.yml` and `capability_registry.yml` hold search, approval,
notification and document wrappers, none of which judge actions or run rules (searched 2026-11-09 for judge,
adjudication, game master, norm and institution: no hits). Reused, not catalogue entries: Concordia's
`EventResolution` (the judge), the World Builder rules check (`scripts/world_builder_service.py`), and `llm_client`
for every model call. No new cross-project capability.

## Prior art

- Concordia's game master components (`EventResolution`), already a dependency, kept off until now.
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
  instead of $0.54. Chosen: keep it, inferred by agent, 2026-11-09. Basis: the sawmill case (Plain baseline)
  shows the free checks pass a valid but wrong rule, and the review is the one existing step that reads a rule
  against the world's description; $0.49 per run is small next to a wrong rule installed for everyone. J2
  measures it on the saved sawmill case; if the review does not flag the single price there, J2 drops it. The
  plain version (one judge call per attempt) would save only the confirm call ($0.02 per run).

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
- **U3 (agent):** how to represent a breakable norm and a credential holder in the declaration language.
  Settled by prior art first (Ostrom's grammar, Institutional Grammar 2.0, v3); a design step opens J4.

## Needs Brian

None open. Mid-run rulings and approval was answered on 2026-11-09 (Decided 5).

## Not in this plan

Organisations and institutions beyond single norms; an AI judge writing outcomes; any claim that a ruling is true
of the real world.
