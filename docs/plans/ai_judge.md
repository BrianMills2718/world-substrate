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
    engine's results; the judge rules only that coins can change hands, Rosa decides whether to sign, the gate
    opens for the signed release whoever holds it, a 100-link chain from the gate runs in one moment, and the
    same offer by another trader later is decided by the new rule with no judge call."
  forbidden_substitutes: "a judge prompt of our own outside Concordia's game master; a judge that writes outcomes
    or decides another person's choice; a ruling used without passing the World Builder rules check; a norm
    written as a declared law; hand-edited rules or runs; a chain shortened to fit a cap; a fixture run reported
    as live."
  boundaries: "world-substrate and its own deploy only; Concordia and Cybernetic Influence v3 read-only; each
    slice merges through ship after scripts/check_project.py exits 0 on the committed change; saved worlds
    still replay unchanged; owner allowance only for live runs."
  done_when: "Acceptance checks A1-A6 below pass, each judged from the full trace of the run it names."
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

**Status:** complete draft, pending Brian's review. Not adopted; nothing is built. Its planning package and review
page are built once the documentation cleanup (branch `docs/cleanup-2026-11-09`) has merged, because both read the
repository-wide package that the cleanup rewrites.

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

1. Vik offers Rosa 40 coins to sign without inspecting. No rule covers a bribe.
2. The engine works out what it can first: Vik does hold 40 coins; nothing physical blocks the hand-over.
3. The judge gets the attempt plus those results and blockers. It rules on the constraint only: coins can pass
   from one person to another here. That ruling becomes a rule, after the rules check.
4. Whether the bribe works is Rosa's choice. Her resident decides to accept or refuse.
5. If she signs, Vik holds a signed release. The gate (a mechanism) opens for the valid code however Vik got it.
   "Bribery is forbidden" is a norm: it was broken, and it has consequences only if an inspector notices and acts.
6. The gate opening sets off the 100-step chain. It runs to the end inside the same moment, each step citing the
   step that caused it.
7. Later, another trader offers a bribe. The new rule decides the hand-over; the judge is not called again.

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
4. **Exception: another person's choice is a decision, not a rule.** Whether a bribe works is decided by the
   person being bribed, not by the judge and not by a rule.
5. **Mid-run rulings: a setting, approved by default.** Source: Brian, 2026-11-09, "can we make this
   configurable? or is that more troubel than it is worth. if so i say yes". Each world gets a setting under
   Options on the Create page, "Judge rulings during a run":
   - **Approved by Create** (default): a ruling that passes the rules check is installed at once and decides
     later identical attempts in the same run.
   - **Wait for my approval**: the ruling settles only the attempt it was made for (a run cannot pause for a
     person), nothing is installed, a later identical attempt asks the judge again, and the run page lists the
     held ruling with an Approve button that installs it for later runs.

   Either way the run page lists every ruling. The setting travels with the world the way "Simulate as" does
   (`scripts/world_builder_service.py:1603`, saved at `:478` and `:645`). Agent's basis for calling it cheap: both
   settings use the same install step; "wait" skips it during the run and the Approve button calls it afterwards.
   Extra work over the default alone is one Options control, one saved field, one branch, one button and its
   endpoint, and a test per setting (guess: under a day of agent work).

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
archives, so these come from v3's code and docs):

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

## Current truth (read from code at main `0e66a98`, 2026-11-09)

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
| R2 | The judge's input holds the engine's propagation results and blockers for the attempt | Brian 2026-11-09 (Why) | A2 |
| R3 | The judge decides only attempts no rule covers and never overrides a blocker | Decided 2 | A3 |
| R4 | A ruling becomes a rule after the rules check and then decides the same attempt for everyone | Decided 3 | A4 |
| R5 | Another person's choice goes to that person, not to the judge or a rule | Decided 4 | A5 |
| R6 | Mechanism, credential holder and norm are separate; a credential can change hands; a norm can be broken | Decided (norms) | A6 |
| R7 | The judge is Concordia's game master, conditioned on our data; no judge prompt of our own | Decision 006 | A2 (trace) |
| R8 | Every run keeps its full trace, read before any slice is reported | workspace rule (Trace visibility) | A1-A6 |
| R9 | A world's setting chooses whether checked rulings install during the run (default) or wait for approval; the run page lists every ruling | Decided 5 | A4 |

All nine are required; none is deferred.

## Acceptance checks

Each is judged from the full trace of the run it names, not its outcome alone.

- **A1 (J0):** a fixture world with a 100-step chain and 50 chains in one moment (5,000 reactions) finishes in
  one commit; every reaction event cites its parent; a fixture with a loop still fires each pair once. Run:
  `tests/test_knock_on_unbounded.py`, output saved under `evidence/ai-judge/j0/`.
- **A2 (J1, J2):** in the port run, the judge's call input (its Concordia component text, in the `llm_client`
  trace) contains the engine's results and blockers for Vik's offer, and no prompt outside Concordia's game master
  produced the ruling.
- **A3 (J2):** a fixture attempt that hits an engine blocker (Vik offers coins he does not have) is refused by
  the engine with the blocker named; the judge is not called.
- **A4 (J3):** with the default setting, the ruling appears as a new rule that passed the rules check (review
  record and scripted test in the run record), and a later identical offer by another trader is decided by that
  rule with no judge call. With "Wait for my approval", the same run installs nothing, the later offer calls the
  judge again, the run page lists the held ruling, and after Approve a new run decides that offer by rule.
- **A5 (J2):** Rosa's own resident call decides accept or refuse; the judge's ruling covers only the hand-over.
- **A6 (J4):** in the password fixture, Mallory phishes Alice's password, the computer logs Mallory in, the norm
  breach is recorded, and a consequence follows only after an observer acts on it.

## Slices, in order

Each slice is one pull request, merged through `ship` after `scripts/check_project.py` exits 0, and ends in a
traced run.

| Slice | Change | Epistemic state | Acceptance |
| --- | --- | --- | --- |
| J0 | Remove the 32-reaction cap; keep once-per-pair-per-moment | fully specifiable now | A1 |
| J1 | Consequence report: every reaction and blocker of an attempt, as one record the judge and page can read | fully specifiable now | A2 (data) |
| J2 | Judge: turn on Concordia's `EventResolution` for unmatched attempts, conditioned on the consequence report; route choices to the person | conditional on J1 | A2, A3, A5 |
| J3 | Ruling to rule: the ruling goes through the World Builder rules check, is installed (or held, per the world's setting), applies to everyone | conditional on J2 | A4 |
| J4 | Credentials as facts and norms as breakable rules (Ostrom's grammar) | exploration required | A6 |

J0 first because it is small, independent and delivers Brian's "100 links deep" alone. J4 last because its
representation needs a short design step of its own (Uncertainties, U3).

## Agent technical calls

- **Remove the 32-reaction cap** ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)): each
  process and entity pair already fires at most once per moment (`engine.py` `_settle` docstring), so a chain
  cannot loop without it, and Brian's example (50 chains, 100 links deep) needs 5,000. The bound becomes the
  number of (process, entity) pairs, which is finite. J0 amends Decision 009 in the same pull request.
- **The judge is Concordia's own game master** (`concordia/components/game_master/event_resolution.py`,
  `EventResolution`), conditioned on a component that supplies the consequence report, not a judge of our own
  (Decision 006). Its output is a proposed rule in the existing declaration language, never an outcome.
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
original. Trace-review criteria: A1-A6, each `expected_outcome: pass`.

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

Call graph per round: resident (existing) -> attempt interpreter (existing) -> engine (code) -> judge (new, only
for an unmatched attempt, after the engine's report) -> rules review (existing, only when a ruling is proposed).
Same model and route as the interpreter (`openrouter/openai/gpt-6-luna`, `scripts/run_authored_world.py:38`).

Cost basis, worked out from measured history (`llm-cost cost --group-by task --days 30`, 2026-11-09):

- Interpreter: 115 calls, $0.0285, 205.3K tokens, so about 1,800 tokens and $0.00025 per call
  (about $0.14 per million tokens).
- Judge call: guess of 20,000 input tokens for a large report, times $0.14 per million, is about $0.003 per call.
- Rules review: 24 calls, $0.699, so about $0.029 per ruling.
- Per ruling about $0.032. With a guess of 10 uncovered attempts per run, about $0.32 per run, falling as
  rulings become rules.

## Irreversible actions and spend

Nothing irreversible: each slice is a pull request (revert with git), and the World Builder deploy is redeployable
from the previous commit. No deletion of saved worlds or run records, no outreach, no change to other repositories.
Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 per slice, enforced by the
run's `max_budget`.

## Uncertainties

- **U1 (agent):** can a consequence report for the largest saved world (786 links) fit the judge's context?
  Settled by working out its token count from the saved world before J1 (an argument, no run needed).
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
