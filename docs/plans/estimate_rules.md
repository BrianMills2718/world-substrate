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
    answer instead of a draw for a declared stochastic event; a mechanics estimate taking over an actor's choice; an estimate rule that reads the
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

<!-- planning-compliance-checklist:v1 -->
## Compliance checklist

Written by `plan_checklist.py --write`, not by hand. `--check` re-runs the validator and fails
if any line below differs from what it says now. Unticked pending items are not passes.

Manifest: `docs/planning/estimate-rules/planning-package.json`
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
- [ ] substance plan records the cost basis of each AI step: failing
- [ ] substance plan compares its AI answer path with the plain version: failing
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
prototype stage; the first slice is one pull request with one live run of about $0.06 of owner allowance for two
people over 30 days, or $0.13 with Waltzman-sized prompts (both computed in LLM call boundary and cost); the run's
cap is $0.13 so it reaches day 30 either way; no new service, engine or repository.

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
Whether a view of the hand-over reaches the harbourmaster at the far end of the quay depends on declared
facts such as geometry, occlusion and light. E5 models this sensory availability, not whether he recognizes
bribery or believes anyone's intention. His interpretation and response (report it, ask for a share, ignore it)
belong to his policy; Rosa's acceptance belongs to hers. The Q84 contract below makes delivery, interpretation
and response separate. This mechanics-estimate path never takes over an actor's choice. A separately declared
actor policy may use Jev for attention or interpretation when adequate for the investigation. E5 is later
because a visibility gate must cover information delivery and every actor-facing narration path.

## Decided

Conceptual clarification (2026-11-12): the draw defaults below apply when an estimate represents
modeled event variability. Answer confidence about an existing fact is not automatically an event
probability. The ford example must distinguish persistent passability from per-crossing variation;
repeated attempts alone cannot resample a persistent condition. See the
[modeling guide](../model/modeling-choices.md#probability-is-a-modeling-decision).
This qualifies inferred defaults; it does not claim implementation or calibration.


Source for direction: Brian, 2026-11-10 (Why). The design points below are the agent's calls, inferred by agent
on 2026-11-10 from the reading and prior art named with each; they stand as working defaults.

1. **An estimate is an input, never a fact.** Jev's answer is recorded evidence that a rule turns into an outcome
   through a declared mechanism: a draw for stochastic events, a persistent realization for a latent condition,
   or an explicit classification/policy rule for those separate roles. It never writes world state by itself. This is
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
     ford after its persistent depth/passability check permits an attempt. Jev estimates this cart's chance
     of completing the crossing, conditional on the declared conditions; on "otherwise" the attempt is
     refused, "blocked: the cart could not get across the ford (chance 0.7, roll 0.81)", nothing changes,
     and the sawmill gets no logs from that attempt. The estimate and draw are recorded on the refusal.
     A fresh draw represents per-crossing variability, not a new ford condition. Another cart may succeed
     only while the persistent passability check permits crossing. A deep-water blocker cannot be bypassed
     by a favorable draw. Independence between permitted attempts is an explicit fixture approximation;
     shared causes must be retained whenever the investigation depends on them.

   **Ruled out: a check on the probability itself** ("the blade fails if Jev's chance is over 0.5"). That turns
   a probability into a truth claim, the retired note's second anti-pattern ("P(fire)=0.81 -> fire=true"), and
   makes the world fail every day above the threshold and never below it.
3. **What an estimate rule declares.** Inside an ordinary process or move (`action-mechanic/v0`,
   `src/world_substrate/action_authoring.py:62` and `:246`), one `estimate` block:
   - `question`: fixed text, written when the world is built; it never contains run-time wording.
   - Fixed model context: the Q83 meaning, units, time interval, applicability and fixed assumptions, included
     in the versioned question/model identity. This is proposed authoring metadata, not an implemented schema field.
   - `reads`: every varying input Jev is shown, as declared paths (the E1 blade's `days_since_service` and `load`).
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
   (resolved model version, estimator/prompt version, question, fixed model context, answer type and options, input values): if the world's rule was edited after the run, so its
   question or reads no longer match the record, the replay stops with "no recorded estimate for this event"
   instead of reusing an answer to a different question.
6. **Caching: one call per distinct complete input per run.** The cache key is (resolved model version, estimator/prompt version, question, answer type and its
   options, the fixed model context, the canonical values of the declared reads). Because a rule declares everything Jev may read, the
   same key means the same question, so the answer is reused for the rest of the run and recorded as "cached,
   first asked at event N". A fresh stochastic event draws its own number; a duplicate exposure or a query about the same persistent
   condition reuses its recorded realization. Distinct daily events with the same declared conditions can
   share an estimated distribution without asserting independence when a modeled shared cause applies.
7. **When Jev fails: retry once, then the rule's declared fallback.** Measured: 1,330 of 20,001 recorded Jev
   calls failed (6.6%: 745 provider errors raised as RuntimeError, 585 network errors; failed calls averaged
   9.4 s), read from `~/projects/data/llm_observability.db` on 2026-11-10, split by the error type each call
   records. `call_decisions` does not retry. One
   retry is the smallest step that keeps a 30-day run from being refused or falling back about twice a run.
   The proposed per-try ceiling is 5 s; enforcing it remains an E1 integration obligation because the deployed timeout policy does not honor ordinary per-call timeout arguments. Measured in the same database: successful
   calls averaged 0.43 s (median 0.26 s, 99th percentile 2.8 s; 61 of 18,671 took over 5 s), provider errors
   came back in 0.89 s on average, and the 585 network errors waited 20.2 s on average before failing. If enforced, a 5 s
   ceiling would cut that wait and turn about 0.3% of those historical successful calls into a retry.
   Both the failed call and the fallback are recorded on the event, and the run page shows "estimate
   unavailable: used the rule's fallback 0.1" in orange.

## Q83 design contract: declare the modeled dependency boundary

**Status and source:** agent-inferred design, 2026-11-12, under Brian's approval to resolve the remaining
modeling contracts. This settles the dependency-selection procedure and the E1 fixture's approximation,
not whether Jev estimates real failure rates adequately. It applies the [modeling guide](../model/modeling-choices.md)
and the existing declared-read/write boundary in `src/world_substrate/action_authoring.py` and `engine.py`.

Before choosing fields, the author states: the quantity or event being estimated; its entity/population and
simulated time interval; the causal mechanism; allowed interventions; fixed assumptions; varying state;
shared causes and persistent latent state; and excluded conclusions. These declarations are part of the
reviewed rule/model identity. `reads` contains every varying input actually supplied to the estimator,
including any declared time, history summary or latent-state reference it needs. Fixed assumptions belong in
its versioned fixed context. Units, category meanings and time intervals accompany the values; a bare number
such as `load: 2` is not enough to define the question. The estimator receives only this context and these
values. Missing or incompatible inputs take the declared unavailable/fallback path; missing is never zero.

**E1 choice.** Keep two varying inputs, elapsed service age and load, for the illustrative blade fixture.
Explicitly stipulate a homogeneous blade/material class, a fixed operating interval per question, an
unchanging environment, and servicing that resets the modeled service age. Under that simplified model,
those two inputs define the intended conditional question; no claim is made that they are sufficient for a
real blade. The fixture can investigate consequences of its assumed failure mechanism and interventions on
load/servicing. It cannot investigate fatigue history, manufacturing defects, material changes or temperature
without adding the corresponding state or changing the model. An actual authoring brief that requires those
distinctions must expand the dependency declaration or reject the approximation, not silently use two fields.
The shape of the age effect is a declared wear assumption, not a universal law of equipment failure.

**Closure by argument, not model agreement.** For each proposed intervention, trace what variable changes,
which mechanism consumes it, and what outcome can change. If two situations that the question requires us
to distinguish have identical estimator inputs and model identity, this representation cannot distinguish
them. That counterexample requires adding a dependency, retaining latent state, or narrowing the question.
More-context answers do not prove missing causality; agreement does not prove sufficiency. A structural
checker can enforce complete declared inputs, units/schema and scopes; it cannot prove all relevant causes
were declared. Authoring must record that residual risk explicitly.

**Reuse and resource tradeoff.** Reuse the estimated distribution only for identical complete declared input
and model identity. A persistent condition keeps its own realization and lifetime; a new query is not a new
physical event. Shared causes remain shared when multiple recipients/events depend on them. Cached estimates
save calls but do not imply independent samples, unchanged real-world conditions or correctness. Narrow
inputs make costs predictable and prevent unrelated private text from entering mechanics; the price is an
explicit applicability boundary. Add information because its mechanism/intervention requires it, not merely
because the context window can fit it. E1 still must show correct enforcement and record/replay, and any
claimed backend sensitivity or calibration needs its own evidence (Q82).

## Q84 design contract: deliver evidence without deciding belief

**Status and source:** agent-inferred design, 2026-11-12; E5 remains unbuilt. Reuse the canonical information
and delivery types (`src/world_substrate/information.py`) and the existing resident observation seam
(`scripts/concordia_residents.py::Residents.observe` and `scripts/run_authored_world.py`'s end-of-round
request delivery). The [information-delivery specification](../../openspec/specs/information-delivery/spec.md)
explicitly says probabilistic delivery is not generic v0 behavior. This is its planned extension, not a claim
that today's request messages already pass through this gate.

**Choose the layer.** Distinguish a world event, a signal/representation emitted about it, its availability
at a recipient, the actor's noticing/interpretation, and the actor's response. E5's minimum port fixture
estimates sensory availability: whether a view of the hand-over reaches the harbourmaster under declared
geometry, light and occlusion. Delivery means "this evidence was made available", not "the harbourmaster
believes a bribe occurred". A separate attention policy may filter or interpret available input if the
investigation needs that distinction; it belongs to the actor model. The E5 fixture explicitly abstracts
that extra stage and must label its trace `view delivered`, not claim measured human noticing.

**Proposed declaration and identity.** A delivery rule names source event/item, content projection, eligible
recipient rule, channel, opportunity time/window, and a typed estimator with Q83 dependencies and fallback.
The content projection states what the channel can convey; seeing a hand-over is not knowing the parties'
private intention. Each actual exposure opportunity has a durable id bound to source event, recipient,
channel, occurrence and rule version. Retrying a request, refreshing the UI or re-querying the same exposure
uses its existing result. At the authored opportunity time, capture the content projection and all declared varying inputs (including observer position, geometry, light and occlusion), their source revision and simulated timestamp, and the fixed context/rule/model identities in that opportunity record. A delayed estimator or resumed request consumes this captured context; it must not read later light or a moved observer to decide visibility of the earlier event. If the scenario samples across a time window, its channel rule must define the sampling times or aggregation of that window explicitly. Changed conditions create a new opportunity only when that authored rule emits one. Retries preserve the same captured input and identity; a terminal fallback/disposition rejects a late duplicate backend result rather than rewriting prior visibility. E5 keys the recorded random realization by that exposure id, not only the common source event id; two recipients must not accidentally share a random draw. Correlated noise, where modeled, names a shared latent/group realization explicitly. A later observation opportunity is distinct only when the authored channel process
makes one; repeated attempts cannot manufacture visibility by repeated rolls. Common fog, blackout or
observer position is represented state shared by affected opportunities, not independent noise by default.

**Execution and persistence.** The source transition first commits. At the existing observation boundary,
authoritative delivery mechanics consume its retained event/item and declared context, obtain/record the
estimate and any permitted draw, and atomically commit the delivery disposition. They do not roll back the
source action merely because nobody saw it. No resident receives the candidate text before the delivery
commit. On continuation, retained pending opportunity ids are resumed idempotently; an already committed
disposition cannot be sampled or delivered again. An unavailable estimator follows the declared failure
behavior for this delivery transition (not a rollback of the earlier source event) and records that result; it does not
silently deliver. A failed source transition creates no success-event signal, although the scenario may
separately emit a signal about the attempted/refused action. No new scheduler or cognition engine is needed.

Use direct recipient-specific information/delivery rows, retaining v0 `pending`/`delivered` semantics;
record a suppressed or unavailable opportunity's disposition in the retained delivery evidence rather than
making the information public. Public active information bypasses recipient checks in v0 and therefore
cannot represent a probabilistically private sighting. Every actor-facing route, including the live
run-loop narration, candidate actions and UI projection, must consume the same committed visibility result;
one unrestricted narration would defeat the gate. The analyst trace may show non-delivery and hidden event
truth, but the actor must not learn a concealed event from a `you missed X` message or a visible negative row.

**Interpretation, response and checks.** After committed delivery, the actor's own policy receives the
projected evidence through `observe`; its memory, personality and current beliefs determine what it makes of
it and what it attempts. It may misinterpret, distrust or ignore it. Content can be inaccurate or deceptive
only through an explicitly modeled source/channel mechanism; delivery does not certify truth. Replay uses
the recorded opportunities, estimates, dispositions and delivered content, without new calls or fresh draws.
Required counterexamples for E5/A5: failed delivery leaves no actor-view leak; duplicate exposure cannot
redraw; two recipients can receive different evidence; a shared occlusion affects both as declared; delivered
hand-over evidence neither proves bribery nor forces reporting. These are implementation obligations. The
layering decision is settled by the information/cognition distinction; adequacy of a particular perception
model remains a scenario-specific question.

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
- **Q63** is conceptually resolved by this plan's estimate contract (2026-11-12); its implementation remains unbuilt.

## Requirements

| Id | Requirement | Source | Check |
| --- | --- | --- | --- |
| R1 | A rule can make an outcome depend on a chance Jev estimates from declared facts, drawn against the run's seed, and its effects and knock-on effects follow as for any rule | Brian 2026-11-10 (Why) | A1 |
| R10 | A constraint can depend on such a chance: a move whose estimate comes out "otherwise" is refused whole with the estimate named as its blocker, and the refusal is recorded with the estimate and the draw | Brian 2026-11-10 (Why: "rules/contstatins") | A7 |
| R2 | Each estimate event records the question, the inputs and their values, the answer, the model version returned, the trace id, the cost, whether it was cached, and the draw; the run page shows them | Q63 contract; workspace rule (Trace visibility) | A1 |
| R3 | A replay reproduces every estimate outcome from the record and never calls Jev; a missing record stops the replay visibly | Q63 contract; goal boundary "saved worlds still replay unchanged" | A2 |
| R4 | Every estimate rule declares a fallback; when Jev fails twice the rule's fallback applies (or the moment is refused) and the run page says so | arc42 section 8 (`docs/architecture/arc42.md:292`) | A3 |
| R5 | A mechanics estimate reads only its declared varying inputs and fixed model context; it never reads the attempt's wording or a resident's private reasoning, and never takes over that resident's choice | judge plan Decided 4; skill roll rule (`docs/plans/open_attempt.md:194`) | A1, A5 |
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
  fields it reads, its fallback and its outcomes in plain words; the run shows oven-failure rows as in A1. The
  saved draft "bakery oven, fallback removed" (that build's oven rule with its fallback deleted, kept with the
  run as A2 keeps its damaged copy) is run through the rules check and shown rejected with "estimate rule needs
  a fallback", so a broken check cannot hide behind a writer that happened to include one.
- **A5 (E1, E5):** in the sawmill run, Jev's recorded input contains the two declared varying fields plus the
  Q83 fixed model context, with no undeclared runtime state or private actor reasoning. In the port run (E5), whether a view of the hand-over reached the harbourmaster appears as "view delivered (chance 0.4,
  roll 0.17)". Q84's no-leak, duplicate-exposure, recipient and shared-cause checks apply. His interpretation
  and subsequent move appear separately; the mechanics estimate supplies neither belief nor decision.
- **A7 (E1):** in the saved run "sawmill blade", the log cart's crossing on a wet day shows "blocked: the cart
  could not get across the ford (chance 0.7, roll 0.81)" in orange; the move changed nothing, no logs reach the
  sawmill from that attempt,
  and opening the refusal shows the per-crossing question, its declared conditions and the draw. The ford
  must already be passable; a deep-water blocker is never bypassed by a roll. A dry day's permitted crossing
  shows the chance, the roll and "crossed".
- **A6 (E3):** in a world with a pick and an amount (the blade's failure mode; repair takes 1, 2 or 4 days), the
  run page shows "failure mode: chipped tooth (Jev: chipped 0.6, cracked 0.3, bent 0.1; roll 0.41)" and "repair
  takes 2 days (Jev: 1 day 0.2, 2 days 0.5, 4 days 0.3; roll 0.55)", and the repair's counter uses 2.

## Slices, in order

Each slice is one pull request, merged through `ship` after `scripts/check_project.py` exits 0, and ends in a
traced run.

| Slice | Change | Epistemic state | Acceptance |
| --- | --- | --- | --- |
| E1 | Chance roll only, on a `timing: each_round` process (the blade, a rule) and on one move (the ford crossing, a constraint): the `estimate` block in the language and its checks, the run seed (if S3 has not built it), the injected estimator (live and recorded), the per-run cache, the record on the event, replay, the run page rows; a hand-written sawmill fixture world; one live 30-day run; the plain-version comparison | fully specifiable now | A1, A2, A3, A5 (sawmill part), A7 |
| E2 | The rules writer declares estimate rules from a description, through the World Builder; the rules check enforces fallback, stakes and declared reads; the free test run uses the stand-in estimator (Q87) | conditional on E1 | A4 |
| E3 | Picks and amounts, when a described world needs one | conditional on E1 | A6 |
| E4 | Judge-proposed estimate rules: the judge's ruling may contain an `estimate` block, checked and test-run like any ruling | conditional on E2 and the judge plan's J3 | (judge plan A4, with an estimate rule) |
| E5 | Recipient-specific sensory availability under the Q84 delivery contract; interpretation stays with actor policy | design contract settled; delivery integration and evidence unbuilt | A5 (port part) |

E1 first because one rule kind on one world with a traced live run is the thinnest path through language,
engine, record, replay and page. E2 before E3 because a visitor's own worlds matter more than more kinds. E4
needs nothing new if E2's rules check is the one judge rulings pass (the judge plan's Decided 3). E5 last because
its Q84 design changes recipient-specific information availability and must cover both canonical delivery
and the live narration path; a field-write example alone does not demonstrate that boundary.

## Agent technical calls

**Resource-limit qualification (2026-11-12):** the five-second-per-attempt ceiling below is a proposed enforcement requirement, not an observed current limit. The deployed service sets `LLM_CLIENT_TIMEOUT_POLICY=ban` (arc42 section 7), so per-call timeout arguments do not establish that ceiling. All latency bounds relying on it are conditional calculations. E1 must establish the supported cancellation/budget mechanism or revise those bounds before claiming bounded wall time; no timeout-policy change is made in this design review.

- **Draw, not argmax and not threshold** (Decided 2). Prior art agrees: models are poor at sampling from a
  probability they state ("Do LLMs Play Dice?", COLING 2025, aclanthology.org/2025.coling-main.360), so the model
  states the probability and the engine draws.
- **The draw is rule semantics, not a scheduler.** Decision 006 sends "stochastic activation or parameter sweeps"
  to Mesa (`docs/decisions/006-governed-rules-layer-scope.md:25`): that is who acts when. An estimate rule's draw
  decides a rule's outcome inside one commit, exactly as the skill roll's dice do, which the open-attempt plan
  already put in the engine. No scheduler, cognition or engine is added. Q27 set the precedent that whether new
  engine control flow is the capability Decision 006 forbids is Brian's call; he allowed the same-moment fixpoint
  as rule semantics (Decision 009). Why the estimate stays inside that ruling without a new one is recorded as
  Q89 (resolved, inferred by agent).
- **Where the estimate is asked.** Inside the commit, after the rule's ordinary checks pass and before its
  effects, so a refused move never asks Jev. If Jev fails and the rule says `refuse`, the whole moment is refused
  (RULE-ATOMIC-COMMIT-OR-REFUSAL).
- **Content kept.** Live calls use `content_persistence="full"` (the default is `metadata_only`): the inputs are
  world fields, not private evidence, and the trace must show them.
- **Latency, not cost, is the constraint.** Measured in `llm_observability.db` (2026-11-10): successful Jev
  calls averaged 0.43 s, but 6.6% of calls failed, provider errors after 0.89 s and network errors after 20.2 s
  on average. With the 5 s timeout and one retry (Decided 7), the expected time per estimate is 0.933 x 0.43 s +
  0.037 x (0.89 + 0.43) s + 0.029 x (5 + 0.43) s = about 0.61 s (computed from those shares), so about 18 s for a
  30-day sawmill run, and a proposed 10 s request-time allowance before fallback, conditional on an actually enforced deadline. The current `LLM_CLIENT_TIMEOUT_POLICY=ban` does not establish that bound; two five-second arguments alone cannot guarantee it. Without the timeout it would be
  about 1.05 s per estimate, about 32 s per run. A world with many estimate rules could ask thousands of times;
  E1 asks sequentially and measures, and parallel asking within a moment is added only if a run shows it is
  needed (Q85).
- **The moment waits for the estimate.** The estimate is asked inside the commit, so the moment, including a
  knock-on chain computed in the same moment (Decision 009), waits for it: the worked-out estimate above is about 0.6 s under its assumptions; no enforced maximum is established by the current timeout policy.
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
- **The free test run never calls Jev** (Q87). The World Builder test-runs each draft's rules with simple
  scripted moves for a fixed number of rounds (`run_world(..., policy="scripted")`,
  `scripts/world_builder_service.py:1845` and `:2215`), and that score is a gate only because it is free and
  gives the same result every time. In it the estimator is a stand-in that never calls Jev: for each rule it
  answers 1 and 0 in turn (for a pick or an amount, each option in turn), so every outcome branch of every
  estimate rule runs, and each answer is recorded as "stand-in estimate (test run)". Calling Jev there would
  make the gate paid and different on each try; using the rule's fallback would test one branch only, or refuse
  every moment when the fallback is `refuse`. The stand-in says nothing about how often a branch fires in a real
  run: the test run checks that the rules work, not how likely their outcomes are.
- **Spend is counted in the existing ledger.** A live run's Jev calls carry the run's own trace id, so the cost
  the World Builder already settles into its daily ledger from that trace includes them (`_trace_cost`,
  `scripts/world_builder_service.py:297`; `_reserve_daily_budget` and `_settle_daily_budget`, :225-238): about
  $0.00084 for the illustrative 30-query blade component before retries; crossing-context estimates and other calls are additional (LLM call boundary and cost). The ledger code is unchanged.

## System model

- Model: [docs/model/ODD.md](../model/ODD.md). Relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL, RULE-DURABLE-RUN-RECORD,
  RULE-PROJECTION-FROM-CANONICAL-ONLY, and 8.20 knock-on effects (Decision 009). Changed: a world package with an
  estimate rule is `model-mediated`. Adds: `estimate rule` (E1), `recorded estimate` (E1), `recorded draw` (E1,
  shared with the skill roll), `estimator` (E1). Domain nodes for these are added now as "In documents only".
- Scope: this repository's own model. Not changed: actors, places, information reach (until E5), tasks. The
  budget ledger's code is unchanged, but a live run's settled cost now includes its Jev calls (Agent technical
  calls).
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
- **Blade estimates in E1 (worked-out scenario estimate, not a run bound):** 30 daily opportunities with one uncached blade query each would cost 30 × $0.0000279 = $0.00084 before retries. The observed 6.6% failure share gives an illustrative retry addition, not a guarantee. E1 also includes A7 crossing estimates: add one call per uncached crossing context and any retry. Total requests are blade cache misses + crossing cache misses + retries; specify those counts for the chosen fixture before running.
- **The rest of the live E1 run (existing calls, computed):** A1 needs Mara's own move and reason, so the run
  also calls the Concordia residents, the attempt interpreter and the readout. Per person per day, the saved
  airfield run (`evidence/open-attempt/s2-airfield/llm-calls.jsonl`: one person, 9 rounds, 36 resident and 12
  interpreter calls, gpt-6-luna) made 4 resident calls (1,256 input and 124 output tokens each) and 1.33
  interpreter calls (993 and 68). At $0.10/M input and $0.50/M output (registry price above) that is
  4 x $0.000188 + 1.33 x $0.000133 = $0.00093 per person per day. Two people over 30 days: 240 resident calls,
  $0.045, and 80 interpreter calls, $0.011; one readout call (1,523 and 309 tokens) adds $0.0003. With Jev, about
  $0.057, so about $0.06 per run. With Waltzman-sized prompts (`evidence/declared-laws/s4-waltzman-3/llm-calls.jsonl`:
  residents 2,761 and 223 tokens, $0.000388 per call; interpreter 3,231 and 242, $0.000444) the same run is
  $0.0021 per person per day, about $0.13 before additional crossing estimates and workload variation. The E1 cap of $0.13 is a spending limit, not assurance of 30 completed days. Larger prompts, additional activations or retries can stop the run earlier; account for the full fixture workload before execution and report an early budget stop as incomplete evidence.
- **Plain-version comparison (E1, once):** 10 cases x 4 variants (below). Jev with the declared reads:
  10 x $0.0000279 = $0.00028 (measured per-call figure). Jev with the whole world: guess, up to 10 times the
  tokens, so up to 10 x $0.000279 = $0.0028. The two Jev variants: up to $0.0031. The gpt-6-luna variant:
  10 x (800 input x $0.10/M + 100 output x $0.50/M) = $0.0013 (computed; price from
  `~/code/llm_client/llm_client/data/default_model_registry.json`). Variant (d), declared bands: one rules-writer
  call, $0.0021 (measured median, next bullet), and no Jev call. Up to $0.0065 in all, under $0.01.
- **Rules writer (E2, existing call):** measured `llm-cost estimate --task world-substrate-mechanic-authoring`
  (2026-11-10): 68 calls, median $0.0021 per call (11,551 input and 1,574 output tokens, 0% cached). Estimate
  rules add a few lines to its output; no new call.
- **Cheapest design that still does the job.** Two designs cost nothing per run.
  - A rule-writer formula (p = min(1, 0.03 x days)). The language has no arithmetic between two values (judge
    plan Decided 3), so a formula would need a language change of its own.
  - Declared bands: the rule's ordinary checks choose among literal chances the rules writer writes. For the
    sawmill: under 5 days since service 0.05, 5 to 9 days 0.2, 10 or more 0.4, each drawn against the same run
    seed. Bands need no arithmetic, no estimator and no Jev call, and a literal chance is exactly the path a
    rule's `{use: value}` fallback already takes (Decided 7), so E1 gets them with no new code.

  Against bands: every number is the rules writer's guess, fixed when the world is built; the facts count only at
  the band edges; and the numbers multiply with the facts a chance depends on (3 facts in 3 bands each is 27
  chances to write and check). Brian also asked for rules that propagate based on Jev. That is an argument about
  fit, not proof that Jev's chances are better, so E1 measures it: variant (d) of the comparison (Plain baseline)
  has the rules writer write the sawmill's bands from its description. Agreement within 0.1 on at least
  8 of the 10 cases is a diagnostic for those inputs only. It establishes neither interchangeability nor
  correctness. Before preferring bands, E2 must justify their applicability, dependencies, thresholds and
  responses to the investigation's interventions. Disagreement or a flat Jev response motivates inspection;
  neither establishes which method is adequate. Nothing here checks Jev against real failure rates.
  Jev costs under a tenth
  of a cent per run and needs no language arithmetic. Chosen: Jev with the per-run cache, with declared bands as
  the cheaper rival measured in E1.

**Where estimate rules could serve the judge's stopping point (not taken over).** The judge plan's J5 asks the
judge, after every completed round, whether a plain-words stopping point has been reached, at about $0.0016 per call
(15,000 input and 150 output tokens of gpt-6-luna, the judge plan's figure). A Jev `NoulQuestion` over the same
state would cost about $0.00003 (measured per-call figure above, for a smaller input; a whole-state input costs
more), about 1/50. It would answer a probability, which J5 would need to turn into stop or not, and Jev has not
been shown to read a world's state well. That choice belongs to J5 and its plan; this plan only records the
option (Q86).

## Plain baseline (conditional diagnostic for E1)

**Decision rule (2026-11-12):** the Q83 contract settles the dependency boundary by argument. Do not run the
comparison below merely to complete a checklist. It is a retained diagnostic option only if a named backend
or omitted-dependency decision survives the declared-mechanism and intervention review. Record that decision
and the result that would change it before running; model agreement cannot establish causal adequacy.

The answer path is Jev's estimate. The plain version, by the workspace rule, is the same model given the whole
source and the question: Jev given the whole world state rather than the declared inputs and fixed context.
If the diagnostic is warranted, the retained candidate set uses days
0, 3, 6, 9 and 12 with and without recent servicing (10 cases), side by side: (a) Jev with the declared reads,
(b) Jev with the whole world, (c) gpt-6-luna with the declared reads asked for a probability, and (d) declared
bands, literal chances the rules writer writes from the sawmill's description with no Jev call (Cheapest design).
Read side by side: does the chance rise with days since service, do (a) and (b) differ, does (c) agree, and do
the bands (d) agree with (a) on these inputs (Q88). Agreement is diagnostic; applicability and
intervention analysis must justify replacement. Variant (b) is kept as
the plain-version record the workspace rule asks for, not as a design candidate: argument already rules out Jev
reading the whole world in a rule, because the cache key would be the whole world (so unrelated world changes invalidate reuse), and
the world can hold what A5 forbids an estimate to read. Differences in (b) motivate inspecting dependencies
and omitted mechanisms; they do not prove that (b) is better or that (a) reads too little. Add declared reads
only when causal and intervention analysis justifies them, preserving the declared-read boundary (Q83).
No Jev call was made for planning.

**Conditional probe, not run:** if backend sensitivity remains a named decision after the dependency review, ten Jev calls for days 1 to 10 at load 14 could inspect monotonicity on those inputs. Worked-out cost is ten times the historical per-call figure, about $0.0003 for that input size. This does not establish calibration or adequacy, is not a mandatory E1 checklist step, and requires the diagnostic justification above before execution.

## Irreversible actions and spend

Nothing irreversible: each slice is a pull request (revert with git), and the World Builder deploy is redeployable
from the previous commit. No deletion of saved worlds or run records, no outreach, no change to other repositories.
Spend: owner allowance only; at most $0.13 per E1 run (expected about $0.06 for two people over 30 days;
computed in LLM call boundary and cost) and $0.50 per slice, enforced by the run's `max_budget`.

## Uncertainties

Review correction, 2026-11-12: the earlier cold review and coverage records are historical. Their
small-case interchangeability conclusion is superseded by the applicability requirements below; the ford
example now samples crossing variability conditional on persistent passability, never passability itself.

- **U1 (agent, Q82):** does Jev's chance rise with the facts it reads (days since service), or is it flat or
  coarse? The probe's chance answers were coarse (0.6, 0.55). The ten-call probe is conditional on a named backend-sensitivity decision remaining after dependency analysis; it inspects only those cases and cannot establish calibration or adequacy.
- **U2 (agent, Q83 design resolved 2026-11-12):** the dependency contract above selects two varying fields only
  within the stated E1 homogeneous-blade approximation. Other investigations must declare their own dependencies
  and interventions. Enforcement, backend adequacy and any real-world sufficiency claim remain unproved.
- **U3 (agent, Q33, existing):** where the run seed lives, shared with the skill roll. Settled by argument in
  whichever of S3 and E1 lands first: drawn at run start and kept in the run record.
- **U4 (agent, Q84 design resolved 2026-11-12):** the delivery contract above uses committed recipient-specific
  exposure records before actor observation, with no belief update or choice imposed. E5 still must implement
  the shared gate across narration and projection and demonstrate the listed negative cases.
- **U5 (agent, Q85):** latency for worlds with many estimates (about 0.61 s expected per estimate, computed in
  Agent technical calls); a measured E1 run characterizes only its own workload. A larger supported workload needs a declared envelope, dependency depth, concurrency, tail latency and saturation evidence. Establish enforceable deadlines separately; parallel calls help only independent work.
- **U6 (agent, Q86):** whether J5's stopping point should use Jev; belongs to the judge plan.
- **U7 (agent, Q88):** whether declared bands written by the rules writer give the same chances as Jev on the
  10 cases. E1 variant (d) is diagnostic, not a replacement decision. E2 may prefer bands only after
  applicability, dependency and intervention analysis supports that approximation; matching cases or flat
  Jev outputs alone do not establish interchangeability or correctness.

## Needs Brian

None open. Which kinds of things a chance may decide is settled by his own split of constraints, decisions and
norms (the judge plan): a chance decides what the world does, never what a person chooses. Whether a draw and a
Jev call inside the commit count as the engine capability Decision 006 forbids was argued by the agent, not
asked again, because Decision 009 already allows rule semantics inside the commit and Brian asked for this
feature; the argument is Q89 (resolved, inferred by agent), and he can reopen it.

## Not in this plan

Estimates of people's choices; calibration against real-world failure data; free-number estimates (Jev has none);
parameter sweeps over many runs (Mesa's job, Decision 006); using Jev for the judge's stopping point (J5's call);
carrying a probability through a chain of rules, as a probabilistic logic network such as ProbLog does. An estimate is used according to its declared semantics: a latent condition persists, an event may draw once per declared identity, and a classification follows its assessment policy. Knock-on effects consume that recorded result. Shared causes require explicit dependence; frequencies across chains are not generally products of independent chances. No generic probabilistic-logic machinery is adopted.

## Complete actor-information dependency (documentation design, 2026-11-12)

Source: Brian's November 12 documentation goal; design application inferred by agent. The [modeling guide](../model/modeling-choices.md) owns the complete actor-information contract and single-concern example. Credential secrecy (J4) and uncertain delivery (E5) depend on that contract across observation, brief, summary, memory, events, offered actions, refusals and actor-facing UI. Item-level message filtering alone is insufficient. These slices must retain the actual authorized context in restricted evidence and demonstrate that an undelivered fact cannot enter through another surface. Analyst access is separate. This dependency is proposed required behavior, not an assertion that current read scopes or projections enforce it. Implementation remains on hold under the documentation goal.
