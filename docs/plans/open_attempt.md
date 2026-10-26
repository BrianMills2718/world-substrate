---
plan_id: "open-attempt"
dependencies: []
dependencies_reviewed: "2026-10-25"
planning_path: durable_solo
planning_path_ref: docs/plans/open_attempt/path-decision.json
method_conformance_receipt: docs/plans/open_attempt/conformance-receipt.json
status: adopted
goal:
  outcome: "World Builder residents say in their own words what they physically try, instead of picking from a list; the world's rules decide what happens, knock-on effects run to the end inside the same moment, and a person's recorded skill (never how expert their words sound) decides how a risky attempt turns out."
  canonical_example: "A World Builder world generated from 'A small airfield office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown'. In one run Sam tries to walk through the wall and nothing happens, with the wall named as the cause; someone knocks the glass off the desk and in the same event chain it falls, breaks, the water spills and the person in the next room hears it; Sam tries to fly the helicopter and a recorded roll from Sam's piloting level 0 gives a crash or a rough landing, never a clean flight from good wording."
  forbidden_substitutes: "hand-edited specs, rules or runs; an interpreter that decides success; outcomes written by an LLM rather than by an installed rule; a roll whose dice come from the attempt's wording; a scripted move presented as an attempt; Waltzman-specific code paths; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run."
  boundaries: "world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change; existing saved worlds still replay unchanged; owner allowance only, visitor allowance stays $3/day; free replays of saved worlds before any paid run; publish-checker before anything new goes public."
  done_when: "Acceptance checks A1-A9 below pass, each judged from the full trace of the run it names."
  do_not_gate_on: "letting an AI game master invent effects for attempts no rule covers (Decision D2: not yet, Brian 2026-10-26); organisations, the decider spectrum and thinking-as-effector (later designs); a clingo cross-check of the reaction rules; Brian's review of a run."
  stop_after: 3
conflict_surfaces:
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/open-attempt/review-page/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-attempt/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/concordia_residents.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/attempt.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/open-attempt/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open-attempt.goal.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.verdicts.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/planning-package.json, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_readout.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/index.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/architecture/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: Makefile, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: lefthook.yml, access: write}
---
# Plan: open attempts, knock-on effects that run to the end, and skill rolls

Planning package: docs/planning/open-attempt/planning-package.json

This is the plan's own package. The repository's package (`docs/planning/planning-package.json`, repo-wide page
`proposals/planning-package/review-page/`) covers the whole repository and its plan part points at this same plan;
both share the checks, open-questions ledger, models and diagrams, are rebuilt by `tools/planning/` and are validated
at the same subject revision (open question Q41).

Review page: [proposals/open-attempt/review-page/](../../proposals/open-attempt/review-page/index.html), live at
<https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/>.

## Actor and result

**Actor:** a World Builder visitor (and Brian as owner) who pastes a scenario and watches the
generated people act. **Result they can inspect:** the run page and its build record show each
person's own-words attempt, what the rules made of it, and why it worked, failed or did nothing.
**Stable example:** the airfield office in the front matter's `canonical_example`: Sam walks into
the wall and is refused with the wall named; the glass chain runs in one moment; Sam's untrained
flight rolls two dice keep-lower.

## Project outcome

Project outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top, rigorous causal engine underneath; the World Builder is the visitor-facing surface). This plan serves that actor directly: the roadmap's "user describing a world" is the
World Builder visitor of the Actor section. **Recurring job and baseline:** a visitor describes a world and
watches its people act; before S1 each person could only pick from moves the rules already allowed, so
impossible attempts (the wall) never appeared. S1 (merged at `fe8c492`, #239) lets residents say attempts in
their own words, and its live run (`evidence/open-attempt/s1-airfield/`, #247) shows residents acting every round; the
wall refusal and the untrained flight have not yet been seen in a live run, and knock-on chains (S2) and untrained
failures (S3) still never appear. **Inspectable result this plan
delivers:** the run page and build record of the airfield world showing the wall refusal, the glass chain
and the rolled crash. **Stage and investment boundary:** prototype stage; three slices, each one pull
request and at most $3.00 of owner allowance; no new service, engine or repository.

## Outcome step

Outcome probe: `roadmap/README.md#canonical-outcome-probe`
Observed: `evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md`
Step: step 3 of the probe, "the residents act in the generated world each round, and the installed rules decide each effect"
Class: vertical

The observed proof is the c1r24 run: the last live run of the whole probe before this plan, the canonical
Waltzman example driven through the real page (generate, 45 rounds, readout, share link `FQHXnP_TLKPi`, every
round read). It shows step 3 working with residents picking from a move list, which is what this plan changes.
S1's first live run of step 3 with free-form attempts is `evidence/open-attempt/s1-airfield/TRACE_READ.md`;
it does not replace c1r24 as the probe's observed proof, because the knock-on and skill cases (A2, A3) were
not exercised there and S1 is built, not done.

Each slice changes that step end to end (generator, resident, engine, page) and ends in a live traced run.

## Why, in one example

Before S1 a World Builder resident was handed a list of moves the rules already allowed and picked one
(the menu reply's `action_id` is that list plus `wait`, still so for the menu schema at
`scripts/concordia_residents.py:96`). So nobody ever walked into a wall: the wall never appeared as a
choice. S1 replaced that with an own-words `attempt` (built; see the slice table). Brian, 2026-10-24: a
person should be able to "attempt to walk through a wall but these should not be successful", and
someone who "dont know how" to fly a helicopter "should probably crash it". The survey
([flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md),
Brian's "yes" on 2026-10-25 to this design) found three pieces missing from World Substrate and
named the established method to copy for each. This plan designs those three, in the order they
depend on each other.

## Current truth (read from code before S1, 2026-10-25, main 63caf4c; S1 rows added after it merged at fe8c492)

| Have | Where |
| --- | --- |
| The rules list what a person can do now (an affordance page) | `Engine.discover`, `src/world_substrate/engine.py:352` |
| A move whose checks fail is refused with the failed check recorded, no partial change | `Engine.apply` / `_reject`, `engine.py:582`, `:749` |
| A move of a kind no rule knows is recorded as unsupported, nothing changes | `Engine.submit`, `engine.py:452`; `UnsupportedAction`, `rules.py:288` |
| Meaning (sense and roles) is kept apart from mechanics | `SemanticBinding`, `src/world_substrate/semantic.py:15`; Decision 003 |
| Things the world does by itself run once per round, each citing its causes | `Engine.advance`, `engine.py:786`; `DeclaredProcess`, `action_authoring.py:245` |
| Who hears or sees what is limited by the world | `world_substrate.information` |
| No randomness anywhere in rules | no `random`/`seed` in `engine.py` or `action_authoring.py` |
| S1: a resident answers `attempt` in its own words instead of an offered `action_id` | `OPEN_SCHEMA`, `scripts/concordia_residents.py:45` |
| S1: one typed call reads the attempt into one action kind and its fields, with no outcome field | `interpret`, `src/world_substrate/attempt.py:149`; `read_interpretation`, `:81` |
| S1: an unmatched attempt changes nothing and is listed in the build record | `UNMATCHED_KIND`, `attempt.py:25`; `unmatched_attempts`, `scripts/run_authored_world.py:800` |
| S1 (Q23): generated worlds have places, ways with a passable flag, and a move that checks the way | `scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`; `evidence/open-attempt/q23/README.md` |
| After S1 (#242, `87b4aa2`): the World Builder page sends open-attempt residents whenever AI chooses the moves | `scripts/world_builder_home.html` on main; `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md` on main |

Decision 006 limits World Substrate to the governed-rules layer. Pieces 1 and 3 are rules-layer pieces:
one turns words into a typed move, one adds a recorded roll to a rule. Piece 2 runs rules to a fixpoint
inside one commit, which changes `engine.py`. Brian ruled on 2026-10-26 (open question Q27, [Decision
009](../decisions/009-same-moment-knock-on-effects.md)) that this is rule semantics, not the engine capability
AGENTS.md and Decision 006 forbid: it adds no new loop, clock or scheduler and is bounded at 32 reactions
inside the existing commit.

## The three pieces

### Piece 1. Open attempt (copy: Inform 7 "try" plus Voyager-style attempts sent to an engine)

1. **Decide.** The resident's reply keeps `belief`, `expected_effect`, `work` and `reasoning`, and
   replaces `action_id` with `attempt`: one sentence of what they physically do, with their body,
   voice or hands ("walk east through the wall into the hangar"). The affordance page is still shown,
   as "things you know you can do here", but it no longer limits the answer.
2. **Interpret.** One typed light-model call (`llm_client`, the World Builder's current model, low
   effort) reads the attempt and the world's action kinds with their fields, and returns `{kind, fields,
   nearest_kind, why}`, where `fields` is a list of rows `{field, value, quoted_span}` (the words in the attempt
   behind each value) and `kind` may also be `wait`. `read_interpretation` (`src/world_substrate/attempt.py:81-148`)
   checks the rows against the world and turns a reading that does not fit (unknown kind or entity, missing field,
   quoted words not in the attempt) into `{unmatched: true, nearest_kind, why}`. Its schema has **no success field**:
   it says what is being tried, never whether it works. A `wait` reading of an attempt with real words is listed
   like an unmatched one (F9, Q39).
   The result is recorded as the command, so replay never calls the model again.
3. **Check.** The matched move goes through `Engine.submit` unchanged. The wall case is an ordinary
   refusal: the generated `move` rule's "the way between is open" check fails (S1's canonical world must show the rules writer gave `move` that check; if it did not, that gap is fixed in the rules writer, never by hand-editing the world), and the event names the wall.
4. **Unmatched fallback (v1).** An attempt that matches no kind is recorded through the existing
   unsupported path: nothing in the world changes, the person sees "you try to …; nothing comes of
   it", and the build record lists every unmatched attempt so the rules writer can add a rule in the
   next build. Letting an AI game master invent an effect is Decision D2: not yet (Brian, 2026-10-26).
5. **Who notices.** Unchanged: `world_substrate.information` decides who perceives the result.
   Shouting to someone overseas succeeds as speech and reaches only those in hearing range.

### Piece 2. Knock-on effects that run to the end (copy: C+ / Event Calculus ramification)

A process may declare `timing: "immediately"` (default stays `"each_round"`, so every existing world is
unchanged). After a move or round event commits its candidate state, the engine runs every immediate
process whose `due()` holds on the new state, then again on the state that produces, until none is
due. Rules:

- each (process, entity) pair fires at most once per moment, so a reaction cannot feed itself;
- at most 32 reactions per moment; going over refuses the whole moment visibly and changes nothing
  (the existing "no partial mutation" invariant);
- every reaction event cites its parent event as a hard causal parent, so the chain is readable;
- order inside one wave is the registry's fixed order, recorded in the events.

Glass: `push glass` moves it off the desk → `falls` (unsupported object above floor) → `breaks`
(fragile and fell) → `spills` (container broke while holding water) and, also from `breaks`, a `crash sound` event. Five events in
one moment: fall cites push, break cites fall, and spill and sound both cite break. The person next
door then learns of the sound through `information`; that is an observation, not a sixth event.

### Piece 3. Skill rolls (copy: Blades in the Dark action roll, GURPS defaults, progress clocks)

An action mechanic may declare `roll: {skill: <actor path>, position: controlled|risky|desperate,
outcomes: {full: [effects], partial: [effects], fail: [effects]}}`.

- Hard gates first: the ordinary checks (holds the key, knows the number, is in the cockpit) run
  before any roll. No roll without stakes: a mechanic with no `fail` effects may not declare a roll.
- Dice: as many six-sided dice as the recorded skill level; level 0 rolls two and keeps the lower
  (GURPS-style default for the untrained). Highest die 6 = full, 4-5 = partial, 1-3 = fail.
  Position picks which outcome list the rules writer gave for "partial" and "fail".
- The dice come from a seeded generator (`seed = hash(run_seed, event_id)`), and the values are
  recorded in the event, so a replay reproduces them and a reader can check them.
- Only the skill path is read. The attempt's wording never reaches the roll.
- Long tasks: a roll's outcome effects may write the counter field a process already reads (the world field behind `Engine._progress`, `engine.py:321`, which only reports it), so a partial result moves a task's counter less than a full one, like a Blades progress clock.

Helicopter: Sam (piloting 0) is in the cockpit (gate passes), rolls two dice, keeps the lower; on
1-3 the `fail` effects crash the helicopter, damaging it and injuring Sam, and Piece 2 carries on
(fuel leaks, alarm sounds, the ground crew hears it).

## Requirements

What Brian asked, plus what the plan's own claims imply; each row names its check in the acceptance table below. Status per check: S1 is built (merged `fe8c492`, #239): A1 (`tests/test_open_attempt.py`) and A8 (`scripts/check_project.py`) were checked in its pull request, and the owner-allowance airfield run with residents (`evidence/open-attempt/s1-airfield/`, 2026-10-26, merged in #247)
judged A4 and A9 passing (its TRACE_READ.md passes `scripts/check_trace_reads.py` and samples ordinary attempts, which is R1's trace check) and left A2 and A3 planned and not yet run: the live run never reached the helicopter or the wall, so both run next on the saved airfield world `tests/fixtures/airfield-s1-live.json` (see the S1 live result below); S2 is built: A6 and the A5 fixture chain pass in `tests/test_open_attempt.py`, and A5 on a generated world is the S2 owner run after deploy; A7 planned in S3; A8 planned in every slice
(run on each merge commit); A9 planned in S1 (open-attempt part) and completed in S3 (full chain). None is
deferred. The claimed property is the requirement itself (an impossible attempt is refused with its cause,
a chain finishes, skill sets the dice), never a count of passing tests.


| Id | Requirement (source) | Fails when | Control | Status |
| --- | --- | --- | --- | --- |
| R1 | Residents can try anything their body can do (Brian 2026-10-24) | The interpreter quietly maps "fly the helicopter" to a safe move | `quoted_span` per role; A2 negative fixture; TRACE_READ samples ordinary attempts | Passing in part: the S1 live run TRACE_READ samples ordinary attempts and passes; A2 planned and not yet run (fixture run next) |
| R2 | The world, not the interpreter, decides what happens (Decision 003; AGENTS.md "installed mechanics alone") | The interpreter refuses or judges success | No success field in its schema (A1); refusals only come from rule checks | Passing: A1 in #239 |
| R3 | Impossible attempts fail with a cause (Brian 2026-10-24) | A wall attempt is dropped instead of recorded | A3: refused event names the failed check | Planned and not yet run: A3 on the saved airfield world next |
| R4 | Knock-on effects run on their own to the end (Brian 2026-10-24) | A chain stops after one step, or loops | A5, A6: once-per-pair rule, cap of 32, whole moment refused on overflow | Passing in part (S2 built): A6 and the A5 fixture chain pass in `tests/test_open_attempt.py::KnockOnEffectTests`; A5 on a generated world planned as the S2 owner run after deploy |
| R5 | Skill decides risky outcomes, not wording (Brian 2026-10-24: LLM knowledge must not leak) | Dice depend on the attempt text, or outcomes are written by the model | A7: same attempt, skill 0 versus 3, different dice pools; dice only from seed | Planned and not yet run (S3) |
| R6 | Saved worlds and replays keep working (AGENTS.md invariants) | Replay calls the model or rerolls | A8: every retained replay test unchanged; rolls and interpretations replay from records | Passing at the S1 merge (A8); S2 at its merge commit (see the S2 row); planned for S3 |
| R7 | Every run is readable in full (core rules) | An interpretation or roll is missing from the trace | A9: run-log.jsonl has each interpreter call's trace id, each roll's dice; TRACE_READ.md passes | Passing for S1 (A9 on the live run); full chain planned in S3 |

## Acceptance checks

| Id | Check | Run and what its trace must show |
| --- | --- | --- |
| A1 | Interpreter schema has no success or outcome field | `pytest tests/test_open_attempt.py::test_schema_has_no_outcome` output |
| A2 | "Fly the helicopter to the coast" never binds to `move` | fixture run on the generated airfield world; the command records `kind: pilot`, `quoted_span` "fly the helicopter" |
| A3 | Walking through the wall is refused, wall named | the canonical run's event for Sam's wall attempt: `status: refused`, failed check names the wall entity. Q23 (generated worlds have walls) resolved: `evidence/open-attempt/q23/README.md` |
| A4 | An unmatched attempt changes nothing and is listed | the canonical run's build record `unmatched_attempts` list, and the event's before/after equal |
| A5 | The glass chain completes in one moment | canonical run: one moment with push, fall, break, spill and sound events; fall cites push, break cites fall, spill and sound cite break. Judged separately: the neighbour's observation for that moment includes the sound |
| A6 | A self-feeding reaction is refused whole | `tests/test_open_attempt.py` loop fixture: status refused, world unchanged, cap reason recorded |
| A7 | Skill, not wording, sets the dice | fixture: identical attempt text, piloting 0 and 3; events show 2-keep-lower versus 3 dice, seed recorded |
| A8 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with these replay tests named passing in the quoted output: `test_action_envelopes` (unsupported and malformed envelopes replay), `test_first_fill.test_fill_tick_and_replay_match_exactly`, `test_greenhouse_zero_review.test_replay_regenerates_exactly_through_generic_renderer`, `test_castaway_zero_review.test_zero_review_replay_regenerates_exactly` |
| A9 | The canonical run is fully traced | `evidence/open-attempt/<run>/run-log.jsonl` plus `TRACE_READ.md` passing `scripts/check_trace_reads.py`; read by the implementing agent before reporting |

## Success and disproof

The plan claims three properties: (1) residents state any physical attempt and only installed rules
decide its effect (R1-R3, checked by A1-A4); (2) knock-on effects run to the end inside one moment or the
moment is refused whole (R4, A5-A6); (3) recorded skill, not wording, decides risky outcomes (R5, A7);
with replay unchanged (R6, A8) and every run fully readable (R7, A9).

**Success:** A1-A9 pass, each judged from the full trace of the run it names. **Disproof:** any one
of these in the canonical run's trace: an interpreter output carrying a success or outcome; a wall
attempt that changes the world or is refused without naming the wall; a pilot attempt by a level-0
person that ends in a clean flight; dice whose seed is not `hash(run_seed, event_id)`; a replay that
calls a model. Trace review: the implementing agent reads every refused, unmatched and rolled attempt
and a sample of ordinary ones in the named run's `run-log.jsonl` and writes `TRACE_READ.md`; each criterion
A1-A9 is expected `pass`. Runs are named in order: `evidence/open-attempt/s1-replay/` (free replay of a
saved world), `evidence/open-attempt/s1-airfield/` (first owner-allowance run, judged for A2-A4 and A9),
`evidence/open-attempt/s2-airfield/` (A5), `evidence/open-attempt/s3-airfield/` (A7 and the full A9);
A1, A6 and A8 are judged from the named pytest and `check_project.py` output saved beside each run.

## When a run fails or surprises us

This is separate from the anticipated failure modes in the Requirements table: it covers what we did not
foresee. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,
intermediate stages (interpretation, checks, reactions, rolls) and the final output (build record, page)
before choosing a fix; cite where it diverged; classify it evidence absent, unused or
contradicted, invalid expectation, or unresolved. An unresolved cause permits investigation, not a
repair. A repair is verified by a new traced run whose `TRACE_READ.md` links the original run and the divergence it
fixes; the original stays. Never rerun until a behavior
appears and report only that run. Review completeness never changes the run verdict: a run's pass or fail
comes from its trace against A1-A9, and an incomplete review leaves the claim unreported, not passed.

## Slices, in order

| Slice | What lands | State | Checks |
| --- | --- | --- | --- |
| S1 | Close Q23 (rules writer makes places, ways and the wall check), then open attempt: resident `attempt` field, interpreter, unmatched fallback, build-record list | built, not done: merged `fe8c492` (#239); page fix `87b4aa2` (#242); live run `evidence/open-attempt/s1-airfield/` (#247): A4 and A9 pass, A2 and A3 not exercised; the run page does not yet show own-words attempts (Q26) | A1, A8 at merge; free replay `evidence/open-attempt/s1-replay/replay.txt` exit 0; A4, A9 on the owner-allowance run; still owed: A2 and A3 on the saved world `tests/fixtures/airfield-s1-live.json`, and Q26 |
| S2 | `timing: immediately` processes run to a fixpoint inside one moment | built, not done: engine `_settle` (Decision 009), rules writer `timing`, transcript `reactions`, round picture and state panel show each knock-on effect with its cause; Q28 resolved (no reuse of the library damage processes, `evidence/open-attempt/q28/README.md`); still owed: A5 on a generated world, the S2 owner run after deploy | A6 and the A5 fixture chain in `tests/test_open_attempt.py::KnockOnEffectTests`; A8 at merge; model drift test `tests/test_system_model.py::test_knock_on_effects` |
| S3 | `roll` on action mechanics, seeded and recorded; rules writer prompt can declare it; the compiler adds the roll's skill path to derived reads and every outcome's effects to derived writes (Q40) | fully_specifiable_now | A7, A8, a test that a roll outside its derived scope is refused, then the full canonical run for A9 |
| S4 | AI game master for unmatched attempts | deliberately_deferred (D2 answered "not yet" by Brian 2026-10-26) | none; reopened only by a new decision |

**Kinds the canonical airfield world must contain** (generated, never hand-written): `move` between
places with a check that the way between is open (the wall), `push` an object, `pilot` a craft to a
place, and `speak`. Before S1, generated worlds were economy-style (`make-leads`, `shape-slats`) and
nothing in the rules writer asked for places, ways between them or blocking. That was open question
**Q23**, S1's first step, resolved 2026-10-25 by a generic fix to the bundle contract and rules writer
(`scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`): the regenerated airfield
world refuses the walk through the wall with "the way is passable" failed
(`evidence/open-attempt/q23/after-fix/probe.txt`). Known limit, open question **Q25**: a way works from its
first place to its second only.

**S1 live result** (`evidence/open-attempt/s1-airfield/TRACE_READ.md`, owner allowance, deployed `87b4aa2`, 9 rounds,
65 model calls, $0.0319): residents moved every round; A4 passes live (15 refused or unmatched attempts each changed
nothing and every unmatched one is listed with the interpreter's nearest move); A2 and A3 were not exercised, because
the build left the helicopter unreachable: everyone but the mechanic starts in the office, the brick wall is the only
way to the hangar and is not passable, the builder's own test runs said the practice flight was never possible and the
build was accepted anyway (#244, Q30). Two smaller defects were filed: a refusal reason reads as a fact ("you are the
dispatcher") rather than a requirement (#245, Q31), and the readout chose the goods-flow lens for a training world (#246, Q32).
S1 is therefore built but not done. Next: A2 as a fixture run of "fly the helicopter to the coast" and A3 as an
interpreted attempt at the wall, both on the saved world `tests/fixtures/airfield-s1-live.json` (free, no new build),
then Q26 (the run page shows each attempt in its owner's words).

Each slice is its own pull request and leaves a working World Builder. S1 alone already lets a
resident walk into the wall. The rules writer (`scripts/generate_causal_model.py`, its process and mechanic schemas) learns `timing` in S2 and
`roll` in S3; until then generated worlds simply do not use them.

## Decisions

- **D1 (made, technical):** the interpreter is one typed light-model call per attempt, not a parser
  and not the resident's own model. Reason: words to (kind, roles) is meaning, which our rules say
  is never read with regex; a separate call keeps the resident from steering its own interpretation.
  Cost: one extra small call per attempt, measured in S1's first run against the visitor $3/day cap.
- **D2 (Brian's call, decided 2026-10-26: not yet):** for attempts no rule covers, should an AI game master be allowed
  to invent a rough effect, marked "coarse" in the record? Recommendation: not now. v1 says "nothing
  comes of it" and lists the attempt for the rules writer. If not answered, v1 stays. Prior art in this
  repository: the offline any-scenario spike already lets its game master write a rule mid-run for each unlisted
  attempt, installed if it passes the layer-1 checks, else recorded as a one-off ruling (`docs/model/ODD.md:194`,
  8.19 at `:266`); Decision 007 accepted that for the spike with review after the run, but no person approves (G14)
  and the spike stays offline (Q17). S4 would differ: it is on the live World Builder, where approval before a run
  still holds (Decision 006); it makes one coarse effect for one attempt, not a general rule; and the record marks it
  coarse. If allowed, it reuses the spike's check gate rather than a new path.
- **D3 (made, technical):** reactions are a `timing` field on the existing process declaration, not a
  new rule type, so they reuse its selector, checks, effects, linked participants and write scopes.

## System model

- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a refused attempt changes nothing), RULE-PROJECTION-FROM-CANONICAL-ONLY (the page shows only recorded events). Adds: `attempt interpretation` (adds), `unmatched_attempts` (adds), `timing` (adds), `roll` (adds).
- Scope: the system model is this repository's own (world-substrate only, linked from the documentation entry point
  `docs/wiki/README.md`), not a shared model. The one shared artefact it touches is the
  scientific-hypergraph kernel, which it reads at a pinned revision and never changes; the mapping
  onto it lives here (`docs/model/metamodel-mapping.json`).
- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) (built by `scripts/build_metamodel.py`) holds the
  world's own types this plan relies on (action kind, role, check, effect, process, affordance, decider,
  attempt, attempt reading, unmatched attempt, event, observation) and the two it plans (same-moment
  knock-on, skill roll), each mapped onto the scientific-hypergraph kernel at `7b0638f`. Its reuse-gate
  table records the formalisms checked before minting them (bounded-design typed-relational reference,
  rule 1); AlgebraicPetri and TypeDB were open question Q24, resolved by argument as compose. S2 and S3 flip their type to built in that
  table in the same pull request.
- Not changed, and why: actors, places, information reach (`world_substrate.information`), tasks and
  the budget ledger keep their current model elements; this plan only changes how a move is chosen,
  how reactions run and how a mechanic resolves, so their definitions stand. RULE-BUDGET-FAILS-CLOSED,
  RULE-FROZEN-PROFILE and RULE-DERIVED-AUTHORITY are relied on unchanged.
- Views: [docs/model/VIEW_COVERAGE.md](../model/VIEW_COVERAGE.md) records which view shows each element; each slice adds its rows there. Per element:
  - `attempt interpretation` (`AttemptReading`): `owner_run_log` shows it (`GET /runs?full=1` keeps the
    transcript, `scripts/world_builder_service.py:1011`); `home` does not yet, gap G17, now open question Q26 (S1 is not done until it closes).
  - `unmatched_attempts`: `owner_run_log` shows it in the run summary (`GET /runs` keeps `summary`,
    written at `scripts/run_authored_world.py:800`); `home` does not yet, gap G17.
  - `timing` and the reaction wave (S2): `round_replay` and `scenario_state_panel` must show each
    reaction event with its parent; S2 adds the row.
  - `roll` (S3): `scenario_state_panel` must show each roll's seed and dice; S3 adds the row.
- The trace must show, per element: the command's `interpretation` record with the interpreter's trace id; the build record's `unmatched_attempts`; reaction events citing their parent; each roll's seed and dice.
- S1 adds an `attempt interpretation` record
  (command field) and the `unmatched_attempts` build-record list; S2 adds the `timing` process field and
  the reaction-wave events; S3 adds the `roll` mechanic field and the event's `roll` record. Each slice
  updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request,
  and the drift test must fail on a renamed field before it passes.
## Trace visibility

- Each run's `run-log.jsonl` records: the inputs (scenario text, world bundle hash, run seed); every step
  (round, actor, attempt text); each model call (resident, interpreter, rules writer) with its prompt
  messages, arguments, typed result and `llm_client` trace id; the model's reasoning where it returns it
  (the resident's `reasoning` field); every engine event with before/after, failed checks, reaction parent
  and dice; and the output (build record, page JSON). Kept for ordinary runs, not only failures. No slice is a pure document edit, so no slice
claims the no-run exemption; this adoption commit alone is document-only and runs nothing.
- How to open one: `evidence/open-attempt/<run>/run-log.jsonl` is one JSON object per line (`jq . <file>`);
  the live run's page links its share id, and `llm_client` trace ids open in its trace store
  (`python -m llm_client traces --trace-id <id>`). Who reads and when: the implementing agent reads every run's
  trace before reporting that slice, including the free replay and fixture runs; every failure or surprise
  in full, and at least five ordinary attempts per run chosen across rounds and actors. This plan has no runs
  other than World Builder runs and the test suite, whose output is saved beside each run.
- World Builder runs keep `run-log.jsonl` (every request, interpreter and resident call with
  `llm_client` trace ids, every event with dice) beside the run; `TRACE_READ.md` per round. The
  implementing agent reads every refused, unmatched and rolled attempt in the canonical run and a sample
  of ordinary ones before reporting.
## Capability reuse

No catalogue entry fits, because `reuse_candidates.yml` and
  `capability_registry.yml` hold approvals, notifications, scheduling, document-to-text and search
  wrappers, none of which interpret actions or run rules. Model calls go through the workspace's shared
`llm_client` (listed in `~/code2/workspace/docs/capabilities.md`, not a catalogue entry). No new
cross-project capability is added; the interpreter's first and only consumer is the World Builder run loop.

## Prior art and ownership

Disposition per piece, from [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md): open attempt **extends** the existing unsupported-action path and `Engine.submit` (copying Inform 7 "try" and Voyager-style attempts); knock-on effects **extend** `DeclaredProcess` (copying C+/Event Calculus ramification); skill rolls **extend** `DeclaredActionMechanic` (copying Blades in the Dark and GURPS defaults). Owner: World Substrate's rules layer (Decision 006). Parallel-implementation check: no second command path, engine or scheduler; every attempt still enters through `Engine.submit`, and `grep -n "def submit" src/world_substrate/engine.py` stays one hit.

## LLM call boundary

Call graph per round: resident call (one per actor, existing) -> attempt interpreter call (one per attempt,
new, after the resident's reply, before `Engine.submit`) -> no further model call; rules, reactions and
rolls are code. The rules writer's calls (existing, at build time) change only in prompt and schema.
Provider: OpenRouter, model `openrouter/openai/gpt-6-luna` (the World Builder's `DEFAULT_MODEL`,
`scripts/run_authored_world.py:37`). Spend authority: Brian's owner allowance, granted for this plan on
2026-10-25. An interpretation becomes authoritative only as a recorded command after an authentic live
run; fixtures may use recorded interpretations but are never reported as live.

Existing resident call (unchanged boundary except the field): typed reply `{belief, attempt, expected_effect,
work, reasoning}`; `attempt` replaces `action_id`; it has no success field either; the reply is recorded in
`run-log.jsonl` with its trace id and is never re-read by rules or replay; a failed or malformed reply records
the actor as waiting, as today.

One new call: the attempt interpreter, through `llm_client`, typed output (`kind`, which may be `wait`; `fields` rows of `field`, `value` and `quoted_span`; `nearest_kind`; `why`), checked into a reading or `unmatched` by `read_interpretation`, no success field. Its output is recorded as the command and never re-read by rules or replay; it has no authority to change state, and promotion of its output to authority is refused by construction (only `Engine.submit` writes). Failure: a malformed or failed call records the attempt as unmatched with the error, never a guessed move.

Tracing: each run gets one trace id, `world-builder-live-run-<uuid4 hex>` (`scripts/run_authored_world.py:385`), passed to every resident call (`scripts/concordia_residents.py:101`) and every interpreter call (`src/world_substrate/attempt.py:158`), so all of a run's model calls share it; `llm_client` stores each call under that id in its `llm_calls` table (`~/projects/data/llm_observability.db`) with its task name, model, request messages, response, token counts, cost, latency, error and timestamp. The run's `run-log.jsonl` repeats the trace id beside each recorded reply and interpretation, so a run row links to its calls (Trace visibility, above).

## Irreversible actions and spend

Nothing irreversible is planned: merges are pull requests (revert with git) and deploys of World Builder's
own service are redeployable from the previous commit. Boundary: no deletion of saved worlds or run
records, no outreach, no change to other repositories. If a step would be irreversible, it stops and goes
to Brian first (core rules: "Ask first only for irreversible actions"); authorization for everything in
this plan is Brian's 2026-10-25 "yes". Containment: the deploy is checked through the health endpoint's
build commit and rolled back to the prior commit if it fails. Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 across S1
(stop and report if a run would exceed it, enforced by the run's `max_budget`); the visitor allowance
stays $3/day.

## Uncertainties

The material uncertainties, listed in full as of 2026-10-26: each below could change a slice's scope or an acceptance check's verdict, and none changes whether this plan is adopted. Q24 (whether Petri nets or TypeDB could carry the metamodel's types) was not material to this plan and is resolved by argument (compose).

- Q23 (agent, resolved 2026-10-25): the rules writer now gives `move` a way-open check (`evidence/open-attempt/q23/README.md`).
- Q25 (agent, resolved by argument 2026-10-26): ways are two-way unless the description declares them one-way; the build is F6 below. Until it lands, each run's `TRACE_READ.md` names any resident stuck behind a way it already used, so it is not read as a refusal by the world.
- Q26 (agent, open): the run page does not show an attempt in its owner's words or that it matched nothing (G17); S1 is not done until it does.
- Q27 (resolved by Brian 2026-10-26, "i approve"; Decision 009): S2's same-moment fixpoint in `engine.py` is rule semantics, not the engine capability AGENTS.md and Decision 006 forbid, within its bounds (inside the existing commit, 32-reaction cap, `timing: immediately` only).
- Q28 (agent, resolved 2026-10-26): S2's glass chain does not reuse the hand-written spill and damage processes (`src/world_substrate/mechanisms/damage.py:116`): they read built-in entity slots a generated world never has and cannot run immediately, so the rules writer writes its own (`evidence/open-attempt/q28/README.md`, reading plus one free probe).
- Q30 (#244, agent, open): a build is accepted although its own test runs say a task is never possible; blocks A2 and A3 on a newly built world, not on the saved fixture.
- Q31 (#245) and Q32 (#246) (agent, open): a refusal reason reads as a fact rather than a requirement, and the readout picked the goods-flow lens for a training world; neither changes an acceptance check's verdict, both change what a reader of the S1 run sees.
- Q33 (agent, open in part): S3's seeded roll is settled by argument for where `run_seed` lives (drawn once per run, recorded in the run record, dice recorded per roll event, so replay never rolls and saved worlds without rolls replay unchanged; the 'no randomness' row becomes 'no unrecorded randomness'); open is whether the rules writer gives a generated person a skill field from the description (Sam's piloting 0), checked by a free probe before S3. A7 and A9 depend on it.
- Q34 (agent, open): read scopes are recorded, not enforced; compiled rules derive their reads from their own checks, so only hand-written rules could leave F1's `blocked_by_event` or a Piece 2 parent link incomplete. Settled by a test-time read check before F1 relies on reads of hand-written rules.
- Q22 / D2 (Brian, resolved 2026-10-26): no AI game master yet; "nothing comes of it" stays.
- Q36 (agent, open): how an interpreter misreading (a legal but wrong move) is caught; quoted spans, A2's negative fixture and a listed set of readings off their nearest kind, settled before A2 is judged. Injected visitor text cannot add a kind, entity or outcome (Q35, resolved).
- Q37 (#241, agent, open): the builder added doorways around the wall and listed them as left out; A3 is judged on the saved fixture, whose wall is the only way.
- Q38 (agent, open): #128 closes once A3 shows a refused wall attempt chosen from belief.
- Q39 (agent, resolved by argument): a wait reading of an attempt with words is a silent no-op today; F9 lists it.
- Q40 (agent, resolved by argument): S3's rolls sit in the causal model, so approval and the fingerprint cover them; the run seed is a run input; the compiler derives the roll's reads and writes (S3 row).
- Interpreter cost per attempt (Q29, resolved 2026-10-26 from S1's live run): the 20 interpreter calls added 11.6% to
  the run's other calls (about 24% at the 30-round cap), under the 30% that would require batching, so S1 keeps one
  call per attempt.

## Fixes settled by argument

Open questions that an argument already answers; each is small, agent-owned, built alongside the slices in its own
pull request, and checked on a free replay of a saved world before any paid run.

| Id | Question | Fix | Check |
| --- | --- | --- | --- |
| F1 | Q2 | The refused row names the earlier event this round that changed what its failed checks read (`blocked_by_event`) | free replay of the saved airfield and c1r24 worlds: every refused row after a lost race names an accepted event id of that round |
| F2 | Q6 | `/run` refuses a second request for the same session, round and base revision | a test that sends the same round twice: one run, one charge |
| F3 | Q8 | A field a check reads that the build's spec names as used up, claimed or changed by a task, and that no rule writes, is a test-run finding; a fixed fact (the airfield wall's `components.boundary.passable`, read at `tests/fixtures/airfield-s1-live.json:392`, written by no rule) is not | the saved #218 build lists its resource; the airfield fixture's wall is not listed |
| F4 | Q10 | The readout quotes `said_on_retry` when present, as the scene replay does | free replay of a saved menu-path run |
| F5 | Q15 | Adopt the `~/code2` repository format (indexes over the existing documents) | the repo-format check reports compliant |
| F6 | Q25 | Ways are two-way unless the description declares them one-way | regenerate the airfield world and probe both directions |
| F7 | Q4 | A remedy's work answer says yes or no to the concern's question plus what was set, and the finished-task notice quotes it | a test that a remedy without that answer is refused and the notice quotes it; the next owner-allowance people-world run's TRACE_READ.md reads its notices |
| F8 | Q9 | Task worlds' scripted test run lasts 24 rounds, like ongoing worlds, instead of 12 | the saved build fixtures score the same or better, and the garden world (#217) finishes inside the test run |
| F9 | Q39 | An attempt with words that the interpreter read as `wait` is listed in the run summary as `read_as_wait` with the interpreter's why, beside `unmatched_attempts` | a test with a recorded wait reading of "fly the helicopter": the summary lists it; a literal "wait" is not listed |

## Activation facts

Recorded in [activation-facts.json](open_attempt/activation-facts.json): shared mechanism yes (engine and generator are shared by every world), no empirical comparison, LLM central yes, spend yes (owner allowance). Route: [path-decision.json](open_attempt/path-decision.json), durable_solo. The plan copies established methods (Inform 7, Event Calculus, Blades in the Dark,
GURPS) but claims conformance to none of them, so `claims_external_standard` is false.

## Durable documents

Durable documents: system_model#ENT-ACTION-ENVELOPE, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, system_model#ENT-RUN-RECORD, plans

S1 changes ENT-ACTION-ENVELOPE (the command gains its interpretation) and ENT-RUN-RECORD (the build
record gains `unmatched_attempts`); S2 changes PROC-PROCESS-TICK and PROC-TRANSITION (reaction waves);
S3 changes PROC-TRANSITION (rolls). Each ID is in `docs/model/trace.yaml` today. The roles are declared
in `.agentic/repo.yaml` lines 3-8: `system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`
and `plans: docs/plans/`. At completion of each slice, `python3
~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan
docs/plans/open_attempt.md --range <adoption revision>..HEAD` must exit 0.

## Authority and non-goals

**Authority:** Brian's "yes" on 2026-10-25 to adopt this plan and start S1; one agent writes; world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only.

**Non-goals:** Organisations as agents, the code/fast-model/LLM decider spectrum, thinking as an effector, moving off
Concordia 2.4.0, a clingo cross-check, and any change to Cybernetic Influence v3. Each comes after this.
