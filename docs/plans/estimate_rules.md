---
plan_id: "estimate-rules"
dependencies: ["open-attempt"]
dependencies_reviewed: "2026-11-10"
planning_path: durable_solo
status: draft
goal:
  outcome: "Some rules in a world can depend on a chance or an amount that Jev estimates during the run: the rule
    asks Jev a fixed, typed question about named facts of the world, the engine rolls against the answer, both
    are recorded on the event, the rule's effects and every knock-on effect follow as usual, and a replay reads
    the recorded estimate and roll and never calls Jev; other people's own choices stay with them."
  canonical_example: "The sawmill blade in 'Canonical example' below: each day a rule asks Jev for the chance the
    blade fails today given its days since maintenance and its load; the engine draws a number from the run's
    seed, the blade fails when the draw is under the chance, the run page shows the question, the facts Jev read,
    its answer, the draw and the outcome, the failure stops the saw and its knock-on effects follow, and a replay
    of the run shows the same days with no Jev call."
  forbidden_substitutes: "a probability treated as a fact (fails because Jev said 0.8); a threshold on Jev's
    answer instead of a draw; Jev or another model deciding what a person does; an estimate rule that reads the
    attempt's wording or a resident's reasoning; a silent default when Jev fails; a replay that calls Jev again;
    a second seed or recording scheme beside the skill roll's; a fixture run reported as live."
  boundaries: "world-substrate and its own deploy only; llm_client, Concordia and Mesa read-only; each slice
    merges through ship after scripts/check_project.py exits 0 on the committed change; saved worlds still replay
    unchanged; owner allowance only for live runs."
  done_when: "Acceptance checks A1-A7 below pass, each judged from the full trace of the run it names."
  do_not_gate_on: "Estimates for people's own choices; calibration of Jev against real-world failure rates;
    estimate rules proposed by the AI judge (E4) before the judge's J3 lands."
  stop_after: 2
conflict_surfaces:
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/estimate_rules.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/estimate-rules/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/estimate-rules/review-page/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/decisions/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/estimate.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/estimate-rules/, access: write}
---
# Plan: estimate rules (rules that propagate on a Jev estimate)

Planning package: docs/planning/estimate-rules/planning-package.json

**Status:** complete draft; Brian approved planning it on 2026-11-10 ("i approve"), in parallel with the AI judge
build. Not adopted; nothing is built.

## Why

Brian, 2026-11-10: "im not saying jsut the judge uses jev. i can see there being a way where we have certain types
of rules/contstatins that progagte base don jev". He then approved planning it now ("i approve").

Today every rule in a world is certain: if its checks pass, its effects happen. Real worlds have things that
happen by chance, where the chance depends on the facts: a blade that has not been serviced for two weeks is more
likely to break today than one serviced yesterday. Writing a fixed formula for every such chance is what a rules
writer cannot do well for a world described in one paragraph. Jev, a typed estimator, answers "how likely, given
these facts?" in about half a second for a few thousandths of a cent. An estimate rule lets a world use that
answer without letting Jev decide what is true.

## Actor and result

**Actor:** a World Builder visitor (and Brian as owner) who describes a world and watches it run.
**Result they can inspect:** the run page shows, for each chance event, the question the rule asked, the facts it
read with their values, Jev's answer, the roll, and what followed; replaying the run shows the same outcomes
with no Jev call.

## Project outcome

Project outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top,
rigorous causal engine underneath). **Recurring job and baseline:** a visitor describes a world and watches it
run. Today nothing in a world happens by chance: no rule uses randomness (`docs/plans/open_attempt.md:124`), and
the skill roll that would add the first one is designed but not built (open-attempt S3, Q33 open).
**Inspectable result:** the sawmill run page and record (canonical example). **Stage and investment boundary:**
prototype stage; the first slice is one pull request with one live run under $0.05 of owner allowance (computed
below); no new service, engine or repository.

## Canonical example

The sawmill. "A small sawmill: the saw cuts logs into boards while its blade is sound. The blade wears; the longer
since it was serviced and the harder it is worked, the more likely it breaks. Mara, the sawyer, can service it,
which takes the day. When the blade breaks, the saw stops, boards stop coming, and the buyer's order runs late. Logs come by cart
across a ford, which is too deep to cross after heavy rain."

1. The world has a blade with `days_since_service` (a number a process adds 1 to each day) and `load` (logs cut
   yesterday), and a saw that runs only while the blade is `sound`.
2. Each day a process declares an estimate: "Given the blade's days since service and yesterday's load, what is
   the chance it fails today?" It reads exactly those two fields. Its answer type is a chance (Jev's
   `NoulQuestion`, which returns a probability between 0 and 1).
3. Day 9: the engine asks Jev with `{days_since_service: 9, load: 14}`. Jev answers 0.31. The engine draws a
   number between 0 and 1 from the run's seed and this event (`hash(run_seed, event_id, rule_id)`): 0.22. Since
   0.22 is under 0.31, the blade fails. The event records the question, both inputs and their values, the answer
   0.31, the model version Jev returned (`typesafe/jev-1.13-20260917` in the existing probe), the call's trace
   id and cost, and the draw 0.22.
4. The rule's "if it happens" effect sets the blade to `broken`. The usual same-moment knock-on effects follow
   ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)): the saw stops, no boards are made that day,
   and the order's due-date check now fails, each step citing the step that caused it.
5. Mara decides, as a resident, whether to service the blade the next day. That is her choice; no estimate is
   asked about it. Servicing sets `days_since_service` to 0 and the blade back to `sound`.
6. Day 10 (if not serviced) asks again with the new values; the answer may be higher. The same inputs asked
   again in the same run reuse the recorded answer (Caching, below).
7. A replay of the saved run reads each recorded estimate and draw and produces the same days, without calling
   Jev. If a recorded estimate is missing, the replay stops with "no recorded estimate for this event" rather
   than asking Jev.

**A people-side example: the harbourmaster.** In the port world, Vik slips coins to Rosa at the customs desk.
Whether the harbourmaster, standing at the far end of the quay, *notices* is a chance that depends on facts
(distance, how busy the quay is, whether it is dark): an estimate rule can decide whether an observation of the
hand-over reaches him, which is information delivery, not anyone's choice. What he does once he knows (report
it, ask for a share, ignore it) is his own decision, made by his resident. Whether Rosa takes the coins is hers
(the judge plan's Decided 4). So an estimate never stands in for what a person chooses; it can stand in only for
what the world does to them (a blade breaks, a sound carries, a sighting happens). This example is a later slice
(E5), because information delivery is a different effect from a field write.

## Decided

Source for direction: Brian, 2026-11-10 (Why). The design points below are the agent's calls, inferred by agent
on 2026-11-10 from the reading and prior art named with each; they stand as working defaults.

1. **An estimate is an input, never a fact.** Jev's answer is recorded evidence that a rule turns into an outcome
   through a declared draw; it never becomes world state by itself and never decides an outcome alone. This is
   the contract Q63 already stated ("a recorded, non-authoritative input, like the skill roll's recorded dice")
   and the retired Jev note's first rule, "borrow estimators; own reality" (`git show
   0dcbcd6^:docs/research/jev-world-modeling-exploration-2026-09.md`).
2. **Which rule kinds may use an estimate.** Three, matching Jev's three typed answers exactly
   (`~/code/llm_client/llm_client/decisions.py`; guide `~/code/llm_client/docs/guides/typed-decisions.md`):
   - **Chance roll** (`NoulQuestion` -> probability p): the engine draws u in [0, 1); if u < p the rule's "if it
     happens" effects apply, otherwise its "otherwise" effects (may be empty). The sawmill blade.
   - **Pick among declared options** (`ChoiceQuestion` -> a probability per option): the engine draws one option
     by those probabilities and applies that option's effects. Example: which of three failure modes the broken
     blade shows. Not Jev's top choice: taking the most likely option every time turns a 60/40 chance into a
     certainty.
   - **An amount** (`ScoreQuestion` over declared, ordered buckets, each with a declared value -> a probability
     per bucket): the engine draws a bucket and writes its declared value. Example: repair takes 1, 2 or 4 days.
     Jev returns no free number (no such question type exists), so an amount is always one of the rule's own
     declared values.

   **Rules and constraints** (Brian's "rules/contstatins"). In the judge plan's terms a constraint is what the
   world makes possible or impossible, and a rule is what follows. An estimate can serve either:
   - **On a process (a rule the world runs):** the sawmill blade above; the outcome's effects and knock-on effects
     follow.
   - **On a move (a constraint on what a person can do):** the move's "otherwise" result may be `block`, which
     refuses the attempt whole and names the estimate as its blocker. Example: the log cart tries to cross the
     ford; Jev estimates the chance the ford is passable from the last three days' rain; on "otherwise" the
     attempt is refused, "blocked: the ford is too deep today (chance 0.7, roll 0.81)", nothing changes, and the
     sawmill gets no logs that day. The estimate and the draw are recorded on the refused event, as every
     refusal is recorded today.

   **Ruled out: a check on the probability itself** ("the blade fails if Jev's chance is over 0.5"). That turns
   a probability into a truth claim, the retired note's second anti-pattern ("P(fire)=0.81 -> fire=true"), and
   makes the world fail every day above the threshold and never below it.
3. **What an estimate rule declares.** Inside an ordinary process or move (`action-mechanic/v0`,
   `src/world_substrate/action_authoring.py:62` and `:246`), one `estimate` block:
   - `question`: fixed text, written when the world is built; it never contains run-time wording.
   - `reads`: the world fields Jev is shown, as declared paths (the blade's `days_since_service` and `load`).
     Nothing else reaches Jev: not the attempt's wording, not a resident's reasoning, not the rest of the world.
     This copies the skill roll's rule, "only the skill path is read; the attempt's wording never reaches the
     roll" (`docs/plans/open_attempt.md:194`).
   - `answer`: `chance`, `pick` with its options, or `amount` with its ordered buckets and their values.
   - `model`: the model id (`openrouter/typesafe/jev-1.13`).
   - `if_unavailable`: required. Either `refuse` (the moment is refused whole and names "estimate unavailable",
     like any refusal today) or `{use: <value>}`, a declared fallback answer. There is no default: a rule that
     omits it fails the rules check. This follows arc42 section 8: a missing authority refuses visibly unless the
     world profile defines the fallback; a silent permissive default is forbidden
     (`docs/architecture/arc42.md:292`).
   - `outcomes`: the effects for each result ("if it happens" and "otherwise"; or one list per option).
     No estimate without stakes: a chance roll whose "if it happens" list is empty fails the rules check, as the
     skill roll forbids a roll with no `fail` effects (`docs/plans/open_attempt.md:188`).

   The rule's derived reads include the estimate's `reads`; its derived writes include every outcome's effects,
   so write scopes and the rules check see them as for any other rule. The rule's fingerprint covers the whole
   block. A world package with any estimate rule is marked `model-mediated`, a representation the profile
   already lists (`src/world_substrate/profile.py:22`).
4. **One seed and one recording scheme, shared with the skill roll.** The draw is `hash(run_seed, event_id,
   rule_id)` mapped to [0, 1), the same seed the skill roll's dice use (`docs/plans/open_attempt.md:192`; Q33).
   Whichever of open-attempt S3 and this plan's E1 lands first builds the run seed; the other reuses it. Ruled
   out: a second seed or a separate log of draws.
5. **Replay never calls Jev.** The engine takes an estimator as an argument. In a live run it is
   `llm_client.call_decisions`; in a replay it is a reader of the recorded estimates that raises "no recorded
   estimate" for anything missing, the pattern `scripts/replay_build.py` already uses for model calls
   (`recorded_llm_client`, `Unrecorded`, lines 23-49). Replay resubmits recorded commands as today
   (`Engine.replay_commands`, `src/world_substrate/engine.py:1182`), so the recorded estimate and draw give the
   same status for each command. The recorded reader matches an estimate by event and by the cache key below
   (model, question, answer type and options, input values): if the world's rule was edited after the run, so its
   question or reads no longer match the record, the replay stops with "no recorded estimate for this event"
   instead of reusing an answer to a different question.
6. **Caching: one call per distinct question per run.** The cache key is (model, question, answer type and its
   options, the canonical values of the declared reads). Because a rule declares everything Jev may read, the
   same key means the same question, so the answer is reused for the rest of the run and recorded as "cached,
   first asked at event N". The draw is not cached: each event draws its own number, so day 9 and a later day
   with the same values share a chance but not an outcome.
7. **When Jev fails: retry once, then the rule's declared fallback.** Measured: 1,330 of 20,001 recorded Jev
   calls failed (6.6%: 745 provider errors raised as RuntimeError, 585 network errors; failed calls averaged
   9.4 s), read from `~/projects/data/llm_observability.db` on 2026-11-10. `call_decisions` does not retry. One
   retry is the smallest step that keeps a 30-day run from being refused or falling back about twice a run.
   Each try has a 5 s timeout (`call_decisions` defaults to 30 s). Measured in the same database: successful
   calls averaged 0.43 s (median 0.26 s, 99th percentile 2.8 s; 61 of 18,671 took over 5 s), provider errors
   came back in 0.89 s on average, and the 585 network errors waited 20.2 s on average before failing. A 5 s
   timeout cuts that wait to 5 s and turns about 0.3% of successful calls into a retry.
   Both the failed call and the fallback are recorded on the event, and the run page shows "estimate
   unavailable: used the rule's fallback 0.1" in orange.

## Current truth (read from code at origin/main `d89a446`, 2026-11-10)

- **Nothing in a world happens by chance.** No rule uses randomness (`docs/plans/open_attempt.md:124`). The skill
  roll (open-attempt S3) is design only: seed, dice and replay reading the dice (`docs/plans/open_attempt.md:182-197`);
  Q33 (where the run seed lives) is open. The domain model marks skill roll and run seed "Theory".
- **Replay is by recorded commands.** `Engine.replay_commands` (`src/world_substrate/engine.py:1182-1222`)
  resubmits each recorded command (`action`, `invalid_action` or `advance`) and checks its recorded status. A
  rule that consulted anything outside the world would need its answer recorded to replay.
- **Recorded model replies already replay.** `scripts/replay_build.py:23-49` answers each model call from the
  recorded reply for the same prompt and raises `Unrecorded` otherwise, never calling a model.
- **The rule language has no estimate.** Expressions are literal, action field, participant, entity id, owner
  reference and event id (`src/world_substrate/action_authoring.py:925-958`); every compiled package says
  `representation="deterministic"` (`:84`, `:278`), while the profile already allows `stochastic` and
  `model-mediated` (`src/world_substrate/profile.py:22`).
- **Jev is reachable and cheap, not used by any world.** `scripts/run_jev_estimator_probe.py` asked 5 typed
  maintenance cases through `call_decisions`; all 5 failure modes were right, about 645 input and 100 output
  tokens and $0.000027 per call, about 300 ms each, model returned `typesafe/jev-1.13-20260917`
  (`evidence/jev/maintenance-estimator-probe-v0.json`, trace `world-substrate/jev/probe-eb6d836e64`). Its
  `NoulQuestion` answers were coarse (0.6, 0.55) and its choice probabilities were 0 or 1. Decision 005 keeps Jev
  "available infrastructure for bounded intermediate estimates but ... not on the critical path"
  (`docs/decisions/005-native-waltzman-delivery.md:86`).
- **Q63** (open, deferred) states the contract this plan adopts and was waiting for "one described world [that]
  needs an estimate no mechanic computes". Brian's 2026-11-10 words reopen it; this plan answers it.

## Requirements

| Id | Requirement | Source | Check |
| --- | --- | --- | --- |
| R1 | A rule can make an outcome depend on a chance Jev estimates from declared facts, drawn against the run's seed, and its effects and knock-on effects follow as for any rule | Brian 2026-11-10 (Why) | A1 |
| R10 | A constraint can depend on such a chance: a move whose estimate comes out "otherwise" is refused whole with the estimate named as its blocker, and the refusal is recorded with the estimate and the draw | Brian 2026-11-10 (Why: "rules/contstatins") | A7 |
| R2 | Each estimate event records the question, the inputs and their values, the answer, the model version returned, the trace id, the cost, whether it was cached, and the draw; the run page shows them | Q63 contract; workspace rule (Trace visibility) | A1 |
| R3 | A replay reproduces every estimate outcome from the record and never calls Jev; a missing record stops the replay visibly | Q63 contract; goal boundary "saved worlds still replay unchanged" | A2 |
| R4 | Every estimate rule declares a fallback; when Jev fails twice the rule's fallback applies (or the moment is refused) and the run page says so | arc42 section 8 (`docs/architecture/arc42.md:292`) | A3 |
| R5 | An estimate reads only its declared fields; it never reads the attempt's wording or a resident's reasoning, and never decides a person's choice | judge plan Decided 4; skill roll rule (`docs/plans/open_attempt.md:194`) | A1, A5 |
| R6 | The same question with the same inputs is asked once per run | agent (Decided 6); cost | A1 |
| R7 | The World Builder's rules writer can declare estimate rules from a world description, and the rules check rejects one with no fallback or no stakes | Brian 2026-11-10 (Why: "types of rules/contstatins") | A4 |
| R8 | Picks among declared options and amounts from declared buckets work the same way as chance rolls | Decided 2 | A6 |
| R9 | Every run keeps its full trace, read before any slice is reported | workspace rule (Trace visibility) | A1-A7 |

All ten are required. R8 is built when a world needs it (E3); the rest by E2.

## Acceptance checks

Each is judged on the run page, from the full trace of the run it names. The record files behind each are listed
in `docs/planning/estimate-rules/acceptance-criteria.json` (field `evidence`).

- **A1 (E1):** the saved run "sawmill blade" (30 days, live Jev) shows, on each day the blade could fail, a row
  "chance the blade fails today: 0.31 (Jev, from days since service 9, load 14); roll 0.22; failed". Opening it
  shows the question, the two fields with their values, the model version and trace id. On a day it failed, the
  saw-stopped and late-order steps follow, each citing the failure. A later day with the same inputs says "same
  question as day N, answer reused". Mara's servicing appears as her own move with her reason, with no estimate
  attached.
- **A2 (E1):** "Replay" on that run shows the same 30 days and outcomes and the line "replayed from the record:
  0 Jev calls". The saved run "sawmill blade, estimate removed" (one estimate deleted from the record) stops at
  that day with "no recorded estimate for this event".
- **A3 (E1):** the saved run "sawmill blade, Jev down" (estimator forced to fail) shows on each day "estimate
  unavailable after 2 tries: used the rule's fallback 0.1" in orange, and the run continues; the same world with
  `if_unavailable: refuse` shows the day's moment refused with "estimate unavailable" and nothing changed.
- **A4 (E2):** on the World Builder, describe "a bakery whose oven sometimes fails, more often the longer since
  it was cleaned" and press Create simulation. "See how it works" shows the oven rule with its question, the
  fields it reads, its fallback and its outcomes in plain words; the run shows oven-failure rows as in A1. A
  rules writer draft with no fallback is shown rejected by the rules check with "estimate rule needs a fallback".
- **A5 (E1, E5):** in the sawmill run, Jev's recorded input for every estimate contains only the two declared
  fields. In the port run (E5), whether the harbourmaster noticed the hand-over appears as "noticed (chance 0.4,
  roll 0.17)", and what he did after appears as his own move with his reason, with no estimate attached.
- **A7 (E1):** in the saved run "sawmill blade", the log cart's crossing on a wet day shows "blocked: the ford is
  too deep today (chance 0.7, roll 0.81)" in orange; the move changed nothing, no logs reach the sawmill that day,
  and opening the refusal shows the question, the rain it read and the draw. A dry day's crossing shows the
  chance, the roll and "crossed".
- **A6 (E3):** in a world with a pick and an amount (the blade's failure mode; repair takes 1, 2 or 4 days), the
  run page shows "failure mode: chipped tooth (Jev: chipped 0.6, cracked 0.3, bent 0.1; roll 0.41)" and "repair
  takes 2 days (Jev: 1 day 0.2, 2 days 0.5, 4 days 0.3; roll 0.55)", and the repair's counter uses 2.

## Slices, in order

Each slice is one pull request, merged through `ship` after `scripts/check_project.py` exits 0, and ends in a
traced run.

| Slice | Change | Epistemic state | Acceptance |
| --- | --- | --- | --- |
| E1 | Chance roll only, on a `timing: each_round` process (the blade, a rule) and on one move (the ford crossing, a constraint): the `estimate` block in the language and its checks, the run seed (if S3 has not built it), the injected estimator (live and recorded), the per-run cache, the record on the event, replay, the run page rows; a hand-written sawmill fixture world; one live 30-day run; the plain-version comparison | fully specifiable now | A1, A2, A3, A5 (sawmill part), A7 |
| E2 | The rules writer declares estimate rules from a description, through the World Builder; the rules check enforces fallback, stakes and declared reads | conditional on E1 | A4 |
| E3 | Picks and amounts, when a described world needs one | conditional on E1 | A6 |
| E4 | Judge-proposed estimate rules: the judge's ruling may contain an `estimate` block, checked and test-run like any ruling | conditional on E2 and the judge plan's J3 | (judge plan A4, with an estimate rule) |
| E5 | Noticing: an estimate that decides whether an observation reaches a person (information delivery) | exploration required | A5 (port part) |

E1 first because one rule kind on one world with a traced live run is the thinnest path through language,
engine, record, replay and page. E2 before E3 because a visitor's own worlds matter more than more kinds. E4
needs nothing new if E2's rules check is the one judge rulings pass (the judge plan's Decided 3). E5 last because
it changes what a person learns, not a field, and needs its own short design step (U4).

## Agent technical calls

- **Draw, not argmax and not threshold** (Decided 2). Prior art agrees: models are poor at sampling from a
  probability they state ("Do LLMs Play Dice?", COLING 2025, aclanthology.org/2025.coling-main.360), so the model
  states the probability and the engine draws.
- **The draw is rule semantics, not a scheduler.** Decision 006 sends "stochastic activation or parameter sweeps"
  to Mesa (`docs/decisions/006-governed-rules-layer-scope.md:25`): that is who acts when. An estimate rule's draw
  decides a rule's outcome inside one commit, exactly as the skill roll's dice do, which the open-attempt plan
  already put in the engine. No scheduler, cognition or engine is added.
- **Where the estimate is asked.** Inside the commit, after the rule's ordinary checks pass and before its
  effects, so a refused move never asks Jev. If Jev fails and the rule says `refuse`, the whole moment is refused
  (RULE-ATOMIC-COMMIT-OR-REFUSAL).
- **Content kept.** Live calls use `content_persistence="full"` (the default is `metadata_only`): the inputs are
  world fields, not private evidence, and the trace must show them.
- **Latency, not cost, is the constraint.** Measured in `llm_observability.db` (2026-11-10): successful Jev
  calls averaged 0.43 s, but 6.6% of calls failed, provider errors after 0.89 s and network errors after 20.2 s
  on average. With the 5 s timeout and one retry (Decided 7), the expected time per estimate is 0.933 x 0.43 s +
  0.037 x (0.89 + 0.43) s + 0.029 x (5 + 0.43) s = about 0.61 s (computed from those shares), so about 18 s for a
  30-day sawmill run, and at most 10 s for any one estimate before its fallback. Without the timeout it would be
  about 1.05 s per estimate, about 32 s per run. A world with many estimate rules could ask thousands of times;
  E1 asks sequentially and measures, and parallel asking within a moment is added only if a run shows it is
  needed (Q85).
- **The moment waits for the estimate.** The estimate is asked inside the commit, so the moment, including a
  knock-on chain computed in the same moment (Decision 009), waits for it: about 0.6 s expected, 10 s at most.
  Each run has its own Engine and one canonical world (`docs/model/ODD.md`, section 3), so the wait holds only
  that run, and the fixpoint itself is unchanged: an estimate rule in a knock-on chain is one more rule whose
  effects are known once its draw is made.
- **What leaves the machine.** Jev is reached through `llm_client` and OpenRouter, the same route by which the
  World Builder already sends a visitor's whole description and world to gpt-6-luna for building and judging
  (ODD section 3: LLM providers, reached only through `llm_client`). An estimate sends less: the fixed question
  and the declared field values (the blade's days since service and load). `content_persistence="full"` keeps
  them in the workspace's own observability database, not with a third party.
- **Model version.** A rule names the model alias `openrouter/typesafe/jev-1.13`; each estimate records the dated
  version the provider returned (today `typesafe/jev-1.13-20260917`). A replay never calls Jev, so a later
  version cannot change a saved run; a version change during or between live runs shows on the run page as a
  different version string. No pin beyond the alias is needed until a run shows a version change mattered.

## System model

- Model: [docs/model/ODD.md](../model/ODD.md). Relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL, RULE-DURABLE-RUN-RECORD,
  RULE-PROJECTION-FROM-CANONICAL-ONLY, and 8.20 knock-on effects (Decision 009). Changed: a world package with an
  estimate rule is `model-mediated`. Adds: `estimate rule` (E1), `recorded estimate` (E1), `recorded draw` (E1,
  shared with the skill roll), `estimator` (E1). Domain nodes for these are added now as "In documents only".
- Scope: this repository's own model. Not changed: actors, places, information reach (until E5), tasks, the
  budget ledger.
- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) gains the estimate block as part of a rule (check ->
  estimate -> outcome effects); each slice updates ODD.md, `world_substrate_model.toml` and
  `tests/test_system_model.py` in the same pull request.
- The trace must show, per estimate: the rule and event, the question, the declared reads with values, the
  answer, the model version, the trace id and cost, cached or not, the draw and the outcome chosen.

## Trace visibility

- Each run's `run-log.jsonl` records the inputs (scenario text, bundle hash, run seed), every round and event,
  every estimate as above, each other model call with its messages, typed result and `llm_client` trace id, and
  the output. Kept for every run, not only failures.
- How to open one: `evidence/estimate-rules/<run>/run-log.jsonl` (`jq . <file>`), its `TRACE_READ.md`, and
  `python -m llm_client traces --trace-id <id>` for a Jev call. All of a run's calls share one trace id.
- Who reads: the implementing agent reads every estimate row of the E1 run, every fallback and refusal, and the
  replay's record, before reporting a slice.

## When a run fails or surprises us

Keep the run and its trace id; read its full inputs, the estimates and draws and the output before choosing a
fix; cite where it diverged; classify the cause as evidence absent, evidence unused or contradicted, invalid
expectation, or unresolved. An unresolved cause permits investigation, not a fix. Verify a fix with a new traced
run and keep the original. Trace-review criteria: A1-A7, each `expected_outcome: pass`.

## Capability reuse

Searched 2026-11-10: `~/code2/workspace/docs/capabilities.md`, `reuse_candidates.yml` and
`capability_registry.yml` for estimate, probability, random and seed: no entry fits. Reused: `llm_client`'s
`call_decisions` and its three question types (the estimator), `llm_client` observability (trace, cost),
`scripts/replay_build.py`'s recorded-reply pattern (replay), the skill roll's seed design (draw), the existing
rules check and same-moment propagation. No new cross-project capability.

## Prior art

Searched 2026-11-10 (reading, two web searches, and the installed Concordia 2.4.0):

- **Concordia** (already a dependency). `contrib/components/game_master/spaceship_system.py:125` uses a fixed
  failure probability with an unseeded `random.random()` and records neither: the counterexample this plan
  avoids. `event_resolution.py:1188` picks among plausible events with `random.choice` and the game master writes
  the outcome in prose. Nothing records an estimate and a draw. Not reused for this.
- **Mesa.** Seeded `model.random` makes a run reproducible by re-running, but keeps no record of each draw
  (`spikes/replacement-2026-10/mesa/run_spike.py:203-208`); re-running would call Jev again. Not reused.
- **Probabilistic programming (ProbLog, Pyro, PyMC).** ProbLog's annotated disjunctions
  (`0.6::chipped; 0.3::cracked; 0.1::bent :- broken.`) are exactly the "pick among options" kind, and its
  sampling makes one choice per grounding per sampled world; but these tools infer probabilities over many
  worlds, while a run needs one recorded world. The rule shape is borrowed; no library is adopted.
- **Tabletop oracles and rolls.** Mythic Game Master Emulator's fate chart and Ironsworn's "ask the oracle" ask
  a yes/no question, set its odds from the situation, and roll: the chance-roll kind with a person setting the
  odds. Blades in the Dark and GURPS rolls are already the skill roll's sources.
- **LLM probabilities in agent-based models.** "On the limits of agency in agent-based models" (arxiv
  2409.10568) asks a model for action distributions per archetype and samples decisions from them; this plan
  does the same for the world's chances but keeps people's decisions with their residents. A UNU report on
  accountable simulation recommends recording seeds and caching model responses for exact replay, which
  Decided 4-6 do.

## LLM call boundary and cost

Call graph per estimate: rule checks pass (code) -> cache lookup (code) -> Jev `call_decisions` with the declared
reads (new, only on a cache miss) -> draw (code) -> outcome effects and knock-on effects (existing).

- **Jev per call (measured):** `llm-cost estimate --task feedback-collector.triage --model jev` (2026-11-10):
  14,222 calls, $0.3963 in all, $0.0000279 per call, median 656 input and 78 output tokens. The probe's 5 calls
  measured $0.000027 each. The registry has no Jev price; cost is provider-reported.
- **Sawmill run (E1):** at most 30 calls (one per day; fewer with the cache), 30 x $0.0000279 = $0.00084; the
  retry on 6.6% of calls adds about $0.00006.
- **Plain-version comparison (E1, once):** 10 cases x 3 variants (below). Jev with the declared reads:
  10 x $0.0000279 = $0.00028 (measured per-call figure). Jev with the whole world: guess, up to 10 times the
  tokens, so up to 10 x $0.000279 = $0.0028. The two Jev variants: up to $0.0031. The gpt-6-luna variant:
  10 x (800 input x $0.10/M + 100 output x $0.50/M) = $0.0013 (computed; price from
  `~/code/llm_client/llm_client/data/default_model_registry.json`). Up to $0.0044 in all, under $0.01.
- **Rules writer (E2, existing call):** measured `llm-cost estimate --task world-substrate-mechanic-authoring`
  (2026-11-10): 68 calls, median $0.0021 per call (11,551 input and 1,574 output tokens, 0% cached). Estimate
  rules add a few lines to its output; no new call.
- **Cheapest design that still does the job.** A rule-writer formula (p = min(1, 0.03 x days)) costs nothing per
  run, and it is the cheaper alternative to Jev; but the language has no arithmetic between two values (judge plan
  Decided 3), so a formula would need a language change of its own, and the curve would be the rules writer's
  guess, fixed when the world is built. Jev costs under a tenth of a cent per run and
  needs no language arithmetic. Chosen: Jev, with the per-run cache; the E1 comparison records whether a plain
  answer differs.

**Where estimate rules could serve the judge's stopping point (not taken over).** The judge plan's J5 asks the
judge, after a changed round, whether a plain-words stopping point has been reached, at about $0.0016 per call
(15,000 input and 150 output tokens of gpt-6-luna, the judge plan's figure). A Jev `NoulQuestion` over the same
state would cost about $0.00003 (measured per-call figure above, for a smaller input; a whole-state input costs
more), about 1/50. It would answer a probability, which J5 would need to turn into stop or not, and Jev has not
been shown to read a world's state well. That choice belongs to J5 and its plan; this plan only records the
option (Q86).

## Plain baseline (planned for E1)

The answer path is Jev's estimate. The plain version, by the workspace rule, is the same model given the whole
source and the question: Jev given the whole world state rather than the two declared fields. E1 runs, for days
0, 3, 6, 9 and 12 with and without recent servicing (10 cases), side by side: (a) Jev with the declared reads,
(b) Jev with the whole world, (c) gpt-6-luna with the declared reads asked for a probability. Read side by side:
does the chance rise with days since service, do (a) and (b) differ, and does (c) agree. Variant (b) is kept as
the plain-version record the workspace rule asks for, not as a design candidate: argument already rules out Jev
reading the whole world in a rule, because the cache key would be the whole world (so nothing is reused), and
the world can hold what A5 forbids an estimate to read. What (b) can change is the declared reads: if (b) tracks
the facts better than (a), the rule is reading too little, and the fix is to declare more reads (and, from E2,
a rules-check warning), never to read the whole world (Q83). No Jev call was made for planning.

**Probe proposed, not run:** 10 Jev calls, one for each of days 1 to 10 since service at load 14 (about
$0.0003, measured per-call figure), would settle U1 (whether Jev's chance rises with days since service). It is
E1's first step, before the live run, and cheap enough that it is not run now.

## Irreversible actions and spend

Nothing irreversible: each slice is a pull request (revert with git), and the World Builder deploy is redeployable
from the previous commit. No deletion of saved worlds or run records, no outreach, no change to other repositories.
Spend: owner allowance only; at most $0.05 per E1 run and $0.50 per slice, enforced by the run's `max_budget`.

## Uncertainties

- **U1 (agent, Q82):** does Jev's chance rise with the facts it reads (days since service), or is it flat or
  coarse? The probe's chance answers were coarse (0.6, 0.55). Settled by E1's first step (the 10-call probe).
- **U2 (agent, Q83):** whether a rule's declared reads leave out facts Jev needs. Declared reads (not the whole
  world) are settled by argument (Plain baseline); the E1 side-by-side comparison shows whether the sawmill's
  two reads are enough.
- **U3 (agent, Q33, existing):** where the run seed lives, shared with the skill roll. Settled by argument in
  whichever of S3 and E1 lands first: drawn at run start and kept in the run record.
- **U4 (agent, Q84):** how a chance decides whether an observation reaches a person (E5): an estimate on the
  delivery of an information item rather than a field write. Settled by a short design step opening E5.
- **U5 (agent, Q85):** latency for worlds with many estimates (about 0.61 s expected per estimate, computed in
  Agent technical calls); settled by E1's measured run and, if needed, a parallel ask within a moment.
- **U6 (agent, Q86):** whether J5's stopping point should use Jev; belongs to the judge plan.

## Needs Brian

None open. Which kinds of things a chance may decide is settled by his own split of constraints, decisions and
norms (the judge plan): a chance decides what the world does, never what a person chooses.

## Not in this plan

Estimates of people's choices; calibration against real-world failure data; free-number estimates (Jev has none);
parameter sweeps over many runs (Mesa's job, Decision 006); using Jev for the judge's stopping point (J5's call).
