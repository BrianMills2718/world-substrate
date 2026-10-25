---
plan_id: "open-attempt"
dependencies: []
dependencies_reviewed: "2026-10-25"
planning_path: durable_solo
status: proposed
goal:
  outcome: "World Builder residents say in their own words what they physically try, instead of picking from a list; the world's rules decide what happens, knock-on effects run to the end inside the same moment, and a person's recorded skill (never how expert their words sound) decides how a risky attempt turns out."
  canonical_example: "A World Builder world generated from 'A small airfield office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown'. In one run Sam tries to walk through the wall and nothing happens, with the wall named as the cause; someone knocks the glass off the desk and in the same event chain it falls, breaks, the water spills and the person in the next room hears it; Sam tries to fly the helicopter and a recorded roll from Sam's piloting level 0 gives a crash or a rough landing, never a clean flight from good wording."
  forbidden_substitutes: "hand-edited specs, rules or runs; an interpreter that decides success; outcomes written by an LLM rather than by an installed rule; a roll whose dice come from the attempt's wording; a scripted move presented as an attempt; Waltzman-specific code paths; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run."
  boundaries: "world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change; existing saved worlds still replay unchanged; owner allowance only, visitor allowance stays $3/day; free replays of saved worlds before any paid run; publish-checker before anything new goes public."
  done_when: "Acceptance checks A1-A9 below pass, each judged from the full trace of the run it names."
  do_not_gate_on: "letting an AI game master invent effects for attempts no rule covers (Decision D2, deferred); organisations, the decider spectrum and thinking-as-effector (later designs); a clingo cross-check of the reaction rules; Brian's review of a run."
  stop_after: 3
conflict_surfaces:
  - {kind: repository_path, path: docs/plans/open_attempt.md, access: write}
  - {kind: repository_path, path: proposals/open-attempt/review-page/, access: write}
  - {kind: repository_path, path: docs/planning/open-attempt/, access: write}
  - {kind: repository_path, path: docs/planning/open-questions.json, access: write}
  - {kind: repository_path, path: scripts/concordia_residents.py, access: write}
  - {kind: repository_path, path: scripts/run_authored_world.py, access: write}
  - {kind: repository_path, path: prompts/, access: write}
  - {kind: repository_path, path: src/world_substrate/attempt.py, access: write}
  - {kind: repository_path, path: src/world_substrate/engine.py, access: write}
  - {kind: repository_path, path: src/world_substrate/action_authoring.py, access: write}
  - {kind: repository_path, path: src/world_substrate/rules.py, access: write}
  - {kind: repository_path, path: docs/model/, access: write}
  - {kind: repository_path, path: tests/, access: write}
  - {kind: repository_path, path: evidence/open-attempt/, access: write}
---
# Plan: open attempts, knock-on effects that run to the end, and skill rolls

Planning package: docs/planning/open-attempt/planning-package.json

Review page: [proposals/open-attempt/review-page/](../../proposals/open-attempt/review-page/index.html), live at
<https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/>.

Project outcome: [roadmap/README.md](../../roadmap/README.md) (generative living worlds on top, rigorous causal engine underneath; the World Builder is the visitor-facing surface).

## Why, in one example

Today a World Builder resident is handed a list of moves the rules already allow and picks one
(`scripts/concordia_residents.py:81` sets the reply's `action_id` to that list plus `wait`). So
nobody ever walks into a wall: the wall simply never appears as a choice. Brian, 2026-10-24: a
person should be able to "attempt to walk through a wall but these should not be successful", and
someone who "dont know how" to fly a helicopter "should probably crash it". The survey
([flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md),
Brian's "yes" on 2026-10-25 to this design) found three pieces missing from World Substrate and
named the established method to copy for each. This plan designs those three, in the order they
depend on each other.

## Current truth (read from code, 2026-10-25, main 63caf4c)

| Have | Where |
| --- | --- |
| The rules list what a person can do now (an affordance page) | `Engine.discover`, `src/world_substrate/engine.py:352` |
| A move whose checks fail is refused with the failed check recorded, no partial change | `Engine.apply` / `_reject`, `engine.py:582`, `:749` |
| A move of a kind no rule knows is recorded as unsupported, nothing changes | `Engine.submit`, `engine.py:452`; `UnsupportedAction`, `rules.py:288` |
| Meaning (sense and roles) is kept apart from mechanics | `SemanticBinding`, `src/world_substrate/semantic.py:15`; Decision 003 |
| Things the world does by itself run once per round, each citing its causes | `Engine.advance`, `engine.py:786`; `DeclaredProcess`, `action_authoring.py:245` |
| Who hears or sees what is limited by the world | `world_substrate.information` |
| No randomness anywhere in rules | no `random`/`seed` in `engine.py` or `action_authoring.py` |

Decision 006 limits World Substrate to the governed-rules layer. All three pieces below are rules-layer
pieces: one turns words into a typed move, one runs rules to a fixpoint inside one commit, one adds a
recorded roll to a rule. None adds an engine, scheduler, renderer or cognition of our own.

## The three pieces

### Piece 1. Open attempt (copy: Inform 7 "try" plus Voyager-style attempts sent to an engine)

1. **Decide.** The resident's reply keeps `belief`, `expected_effect`, `work` and `reasoning`, and
   replaces `action_id` with `attempt`: one sentence of what they physically do, with their body,
   voice or hands ("walk east through the wall into the hangar"). The affordance page is still shown,
   as "things you know you can do here", but it no longer limits the answer.
2. **Interpret.** One typed light-model call (`llm_client`, the World Builder's current model, low
   effort) reads the attempt and the world's action kinds with their roles, and returns either
   `{kind, roles: {role: entity_id}, quoted_span per role}` or `{unmatched: true, nearest_kind,
   why}`. Its schema has **no success field**: it says what is being tried, never whether it works.
   The result is recorded as the command, so replay never calls the model again.
3. **Check.** The matched move goes through `Engine.submit` unchanged. The wall case is an ordinary
   refusal: the generated `move` rule's "the way between is open" check fails (S1's canonical world must show the rules writer gave `move` that check; if it did not, that gap is fixed in the rules writer, never by hand-editing the world), and the event names the wall.
4. **Unmatched fallback (v1).** An attempt that matches no kind is recorded through the existing
   unsupported path: nothing in the world changes, the person sees "you try to …; nothing comes of
   it", and the build record lists every unmatched attempt so the rules writer can add a rule in the
   next build. Letting an AI game master invent an effect is Decision D2, deferred.
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

## Requirements, failure modes and controls

| Id | Requirement (source) | Fails when | Control |
| --- | --- | --- | --- |
| R1 | Residents can try anything their body can do (Brian 2026-10-24) | The interpreter quietly maps "fly the helicopter" to a safe move | `quoted_span` per role; A2 negative fixture; TRACE_READ samples ordinary attempts |
| R2 | The world, not the interpreter, decides what happens (Decision 003; AGENTS.md "installed mechanics alone") | The interpreter refuses or judges success | No success field in its schema (A1); refusals only come from rule checks |
| R3 | Impossible attempts fail with a cause (Brian 2026-10-24) | A wall attempt is dropped instead of recorded | A3: refused event names the failed check |
| R4 | Knock-on effects run on their own to the end (Brian 2026-10-24) | A chain stops after one step, or loops | A5, A6: once-per-pair rule, cap of 32, whole moment refused on overflow |
| R5 | Skill decides risky outcomes, not wording (Brian 2026-10-24: LLM knowledge must not leak) | Dice depend on the attempt text, or outcomes are written by the model | A7: same attempt, skill 0 versus 3, different dice pools; dice only from seed |
| R6 | Saved worlds and replays keep working (AGENTS.md invariants) | Replay calls the model or rerolls | A8: every retained replay test unchanged; rolls and interpretations replay from records |
| R7 | Every run is readable in full (core rules) | An interpretation or roll is missing from the trace | A9: run-log.jsonl has each interpreter call's trace id, each roll's dice; TRACE_READ.md passes |

## Acceptance checks

| Id | Check | Run and what its trace must show |
| --- | --- | --- |
| A1 | Interpreter schema has no success or outcome field | `pytest tests/test_open_attempt.py::test_schema_has_no_outcome` output |
| A2 | "Fly the helicopter to the coast" never binds to `move` | fixture run on the generated airfield world; the command records `kind: pilot`, `quoted_span` "fly the helicopter" |
| A3 | Walking through the wall is refused, wall named | the canonical run's event for Sam's wall attempt: `status: refused`, failed check names the wall entity. Depends on Q23 (below) |
| A4 | An unmatched attempt changes nothing and is listed | the canonical run's build record `unmatched_attempts` list, and the event's before/after equal |
| A5 | The glass chain completes in one moment | canonical run: one moment with push, fall, break, spill and sound events; fall cites push, break cites fall, spill and sound cite break. Judged separately: the neighbour's observation for that moment includes the sound |
| A6 | A self-feeding reaction is refused whole | `tests/test_open_attempt.py` loop fixture: status refused, world unchanged, cap reason recorded |
| A7 | Skill, not wording, sets the dice | fixture: identical attempt text, piloting 0 and 3; events show 2-keep-lower versus 3 dice, seed recorded |
| A8 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with these replay tests named passing in the quoted output: `test_action_envelopes` (unsupported and malformed envelopes replay), `test_first_fill.test_fill_tick_and_replay_match_exactly`, `test_greenhouse_zero_review.test_replay_regenerates_exactly_through_generic_renderer`, `test_castaway_zero_review.test_zero_review_replay_regenerates_exactly` |
| A9 | The canonical run is fully traced | `evidence/open-attempt/<run>/run-log.jsonl` plus `TRACE_READ.md` passing `scripts/check_trace_reads.py`; read by the implementing agent before reporting |

## Slices, in order

| Slice | What lands | State | Checks |
| --- | --- | --- | --- |
| S1 | Close Q23 (rules writer makes places, ways and the wall check), then open attempt: resident `attempt` field, interpreter, unmatched fallback, build-record list | conditional (on Q23's first step) | A1-A4, A8, A9 (on a free replay first, then one owner-allowance run) |
| S2 | `timing: immediately` processes run to a fixpoint inside one moment | fully_specifiable_now | A5, A6, A8 |
| S3 | `roll` on action mechanics, seeded and recorded; rules writer prompt can declare it | fully_specifiable_now | A7, A8, then the full canonical run for A9 |
| S4 | AI game master for unmatched attempts | human_decision_required (D2) | none until decided |

**Kinds the canonical airfield world must contain** (generated, never hand-written): `move` between
places with a check that the way between is open (the wall), `push` an object, `pilot` a craft to a
place, and `speak`. Today's generated worlds are economy-style (`make-leads`, `shape-slats`) and
nothing in `scripts/generate_causal_model.py` asks for places, ways between them or blocking. That is
open question **Q23**, and it is the first step of S1: generate the airfield world, read its
mechanics, and if `move` lacks a passability check, change the rules writer's prompt and schema so
it writes one (never hand-edit the world). A3 cannot pass until Q23 is closed.

Each slice is its own pull request and leaves a working World Builder. S1 alone already lets a
resident walk into the wall. The rules writer (`scripts/generate_causal_model.py`, its process and mechanic schemas) learns `timing` in S2 and
`roll` in S3; until then generated worlds simply do not use them.

## Decisions

- **D1 (made, technical):** the interpreter is one typed light-model call per attempt, not a parser
  and not the resident's own model. Reason: words to (kind, roles) is meaning, which our rules say
  is never read with regex; a separate call keeps the resident from steering its own interpretation.
  Cost: one extra small call per attempt, measured in S1's first run against the visitor $3/day cap.
- **D2 (Brian's call, deferred):** for attempts no rule covers, should an AI game master be allowed
  to invent a rough effect, marked "coarse" in the record? Recommendation: not now. v1 says "nothing
  comes of it" and lists the attempt for the rules writer. If not answered, v1 stays.
- **D3 (made, technical):** reactions are a `timing` field on the existing process declaration, not a
  new rule type, so they reuse its selector, checks, effects, linked participants and write scopes.

## Model, traces and reuse

- **System model:** [docs/model/ODD.md](../model/ODD.md). S1 adds an `attempt interpretation` record
  (command field) and the `unmatched_attempts` build-record list; S2 adds the `timing` process field and
  the reaction-wave events; S3 adds the `roll` mechanic field and the event's `roll` record. Each slice
  updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request,
  and the drift test must fail on a renamed field before it passes.
- **Traces:** World Builder runs keep `run-log.jsonl` (every request, interpreter and resident call with
  `llm_client` trace ids, every event with dice) beside the run; `TRACE_READ.md` per round. The
  implementing agent reads every refused, unmatched and rolled attempt in the canonical run and a sample
  of ordinary ones before reporting.
- **Capability reuse:** No catalogue entry fits, because `reuse_candidates.yml` and
  `capability_registry.yml` hold approvals, notifications, scheduling, document-to-text and search
  wrappers, none of which interpret actions or run rules. Model calls reuse the shared `llm_client`.

## Non-goals

Organisations as agents, the code/fast-model/LLM decider spectrum, thinking as an effector, moving off
Concordia 2.4.0, a clingo cross-check, and any change to Cybernetic Influence v3. Each comes after this.
