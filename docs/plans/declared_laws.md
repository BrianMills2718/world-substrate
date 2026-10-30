---
plan_id: "declared-laws"
dependencies: []
dependencies_reviewed: "2026-10-28"
planning_path: reset
planning_path_ref: docs/plans/declared_laws/path-decision.json
method_conformance_receipt: docs/plans/declared_laws/conformance-receipt.json
status: adopted
goal:
  outcome: "A World Builder world stops depending on a growing list of hand-written checks for past bugs: the AI that designs a world also declares that world's own laws (which goods can only appear or vanish through which moves, and what a move such as a purchase must move each way); the engine refuses any move or knock-on effect that breaks a declared law and names the law; and a separate AI review, not the rules writer, reads the written rules against the description and the laws and lists concrete mismatches for the rules writer to fix."
  canonical_example: "Paste the pencil description (~/code/.scratch/open-attempt-s2/pencil.txt, the one behind pencil2-pencil14) into https://brianmills.dev/world-builder/ and press Create simulation. The build record lists the world's declared laws in plain words (for example 'pencils are made only by the factory's make move' and 'buying boxed pencils moves boxes to the shop and cash to the factory'); a move whose rules would make pencils from nothing or take boxes without paying is refused in the test run with that law named, and the rules writer is told so; the review lists any rule that contradicts the description (pencil13's buy-boxed-pencils, which paid nothing) by name; and the world that is kept runs with no law refusals from its own rules."
  forbidden_substitutes: "a fixed list of built-in move types that every world must use (Brian 2026-10-28: it 'destorys the whol e potin'); laws or rules written by hand for the pencil world; pencil-specific or Waltzman-specific code paths; a review by the same call or context that wrote the rules; a review that returns a pass mark instead of findings; retiring a heuristic check without showing that the saved world of each incident it caught is refused by a law or named by the review; laptop runs presented as live; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run."
  boundaries: "world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change, then deploys and the live commit is confirmed through the health endpoint; saved worlds without laws replay unchanged; owner allowance only, visitor allowance stays $3/day, no new spend route without Brian's yes; free replays of saved worlds before any paid run; publish-checker before anything new goes public; never restart WSL."
  done_when: "Acceptance checks L1-L8 below pass, each judged from the full trace of the run it names."
  do_not_gate_on: "a static build-time proof of laws (Q46: deferred); laws of shapes other than totals and pairings (Q43); the AI game master for unmatched attempts (Decision D2 of the open-attempt plan); the open-attempt plan's S3 skill rolls; Brian's review of a run."
  stop_after: 3
conflict_surfaces:
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/declared_laws.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/declared_laws/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/declared-laws/review-page/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/planning-package/review-page/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/laws.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/review_rules.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/declared-laws/, access: write}
  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: wiki/catalog.md, access: write}
---
# Plan: worlds declare their own laws, the engine enforces them, and an independent review reads the rules

Planning package: docs/planning/declared-laws/planning-package.json

This is the plan's own package. The repository's package (`docs/planning/planning-package.json`, page
`proposals/planning-package/review-page/`) covers the whole repository; its plan part now points at this plan,
and both share the checks, open-questions ledger, models and diagrams rebuilt by `tools/planning/` (Q41).

Review page: [proposals/declared-laws/review-page/](../../proposals/declared-laws/review-page/index.html), live at
<https://hive.brianmills.dev/plans/world-substrate/main/proposals/declared-laws/review-page/>.

## Actor and result

**Actor:** a World Builder visitor (and Brian as owner) who pastes a description and watches the generated world
run. **Result they can inspect:** the build record lists the world's declared laws in plain words, every move the
laws refused (with the law named), and the independent review's findings; the run page shows a world whose goods
come from somewhere and go somewhere. **Stable example:** the pencil description in the front matter.

## Project outcome

Project outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top,
rigorous causal engine underneath). **External job the World Builder serves:** the visitor (an analyst such as Rand
Waltzman exploring an influence scenario, a teacher, a planner of a small supply chain) is thinking through how a real
situation could play out: who would do what, what would run out, what a change would set off. **Their baseline without
it:** a tabletop exercise or wargame with people playing the parts, a written scenario, or a spreadsheet or
stock-and-flow model they build by hand; each is slow to set up, and a spreadsheet keeps the books but does not let
people try things freely. **How the World Builder helps:** it turns their plain description into a running world in
minutes, in which people try moves freely and the books are kept, so they can watch the situation unfold and rerun it.
This plan serves that job by making the books right (money and goods neither appear nor vanish except as the world's own
laws allow), which a reader needs before trusting what the run shows. **Recurring job and baseline:** a visitor describes a world and watches it run.
Baseline from pencil2 to pencil14 (2026-10-27/28): each live build found one more way the rules writer got the
bookkeeping wrong (goods from nothing, stock with nowhere to go, a purchase that pays nothing, a move that changes
nothing, a malformed field path), and each was fixed by one more hand-written check in
`scripts/world_builder_service.py:840-1220`, some of which then raised false alarms. pencil14 at `5d6a48e` failed
outright (422 after about 287 s, job `f0b6d1a3dc0a40848456e6fe2ce172c0`: "mechanic installer rejected
shipment-arrival: malformed_path"; driver log in `evidence/pencil14-build-failure/`). **Inspectable result of this plan:** the canonical example above, live.

## Outcome step

Outcome probe: `roadmap/README.md#canonical-outcome-probe`
Observed: `evidence/pencil13-trace-audit/TRACE_READ.md`
Step: step 2 of the probe, "The builder generates the world (places, things, people, the moves they may attempt) and its rules."
Class: vertical

pencil13 is the last live pencil run read round by round: 5 sales moved cash, goods were conserved along factory,
truck, shop and customer, and the shop's buy-boxed-pencils move paid the factory nothing, which no check caught.
Each slice changes the build and the run end to end and ends in a live traced run.

## Why, in one example

The rules writer is a capable model: it knows that buying pencils means paying for them. But it writes every move as
raw field changes ("add 10 to shop.boxes, subtract 10 from factory.boxes"), and nothing compares those changes with
what it knows. So a purchase that forgets the payment installs and runs (pencil13). Our answer so far was a new
check per mistake, each guessing at meaning from the rules' shape. Brian, 2026-10-28: "my guess is that you hjave been
fixing symptoms not root problems". Fixed move types (transfer, exchange, transform) would stop the mistakes by
stopping the flexibility; Brian rejected that ("seems to me liek it destorys the whol e potin of what we are doing").
This plan keeps the moves free and asks the model to state, once, what must hold in this world, then holds the
rules to it.

## Incidents this plan must catch

One row per build check that guesses at meaning, with the incident its docstring names (`scripts/world_builder_service.py`)
and the saved world that shows it, plus the incident no check caught. This is the proof set L6 and S4 use: a check
retires only when its incident's saved world is refused by a law or named by the review.

| Incident | Saved world | Shape | Caught today by | After this plan |
| --- | --- | --- | --- | --- |
| A purchase that pays nothing (buy-boxed-pencils) | pencil13 `3SogfsdEGx9M`, `tests/fixtures/pencil13-kept.json` | pairing | nothing | pairing law refuses it; the review names it |
| A process restocks goods an action makes (restock-production-inputs) | c4-run14, `evidence/best-of-all-worlds/final-1a5498f/c4-run14.log`, trace `world-builder-live/world/41373883...` | total | `_conjuring_processes` (`:867`) | total law: the good may change only by its making move |
| A move uses up goods and makes nothing (pack-pencils) | `4VmgkXIVWn4p`, `evidence/vanishing-goods/pencil3-share.json` | total | `_vanishing_moves` (`:1114`) | total law: pencils may leave only by being used |
| A raw good with two sources (mine-graphite and graphite-renews) | c4-run20, trace `world-builder-live/world/5c2f3bc4...` | total, only if the designer names one source | `_second_source_processes` (`:1143`), report only | total law when declared; otherwise not a mistake |
| Inputs nobody makes (clay, paint, erasers, ferrules) | pencil2 `NZD33sh3iX29`, `tests/fixtures/pencil2-live.json` | reachability, not a law | `_unsourced_inputs` (`:840`) | the test run's "never possible" report and the review |
| A move needs a component no entity has (ship-pencil-boxes) | pencil4 `iMrL2U84cLCS`, `tests/fixtures/pencil4-live.json` | structure, not a law | `_missing_components` (`:943`) | stays: a structural fact read from the bundle |
| Stock with nowhere to go (the supplier's clay and paint) | pencil4 `iMrL2U84cLCS` | reachability, not a law (Q43) | `_dead_end_stock` (`:960`) | a test-run report of stock that only grew, and the review |
| The customer flagged as a dead end though it uses pencils | pencil12, pencil13 | false alarm | `_dead_end_stock` (patched in #275, #277) | goes with the guess |
| A seller starts with none of what it sells and nothing gives it any | pencil9 `q2sG4d_J7279`, `tests/fixtures/pencil9-live.json` | reachability, not a law | `_starved_holders` (`:1023`) | the test run's "never possible" report and the review |
| Demand that only grows (orders_waiting) | cafe `eFmPomcnsyQq`, `evidence/vanishing-goods/cafe2-share.json` | reachability, not a law | `_unanswered_demand` (`:1130`) | a test-run report of a field that only grew, and the review |
| Processes carry goods that actors should carry | c4-run16, trace `world-builder-live/world/cde24f89...` | role, not a law | `_moving_processes` (`:1178`) | the review |
| Malformed field path | pencil14, `evidence/pencil14-build-failure/README.md` | not a law | installer, already refused | unchanged |

Laws catch the bookkeeping rows (four). The reachability rows are about what can never happen or what piles up: no
law refuses them because every total is unchanged, so they move to reports of what the test run saw, which stay, and
to the review.

## Current truth (read from code 2026-10-28, main `5d6a48e`)

| Have | Where |
| --- | --- |
| A move's candidate state is checked for writes outside its declared scope and refused whole | `Engine.apply`, `src/world_substrate/engine.py:686-720` |
| Knock-on effects settle in waves inside the same commit | `_settle`, `engine.py:896`; Decision 009 |
| Effects are rows `{participant, path, op: set|add|subtract, value}` | `EFFECT_OPS`, `src/world_substrate/action_authoring.py:42`; rows read at `:1052`, applied at `:1109` |
| A process (tick or knock-on) that writes outside its scope raises `ScopeViolation` and the state is restored (`engine.py:1005-1015`). A moment is refused only for `reaction_limit`, `_settle` returning `None`: in `Engine.apply` through `_reject` with the move's rule id (`engine.py:760-781`), in `Engine.advance` through `_refuse_round` with the process's rule id, which ends the advance (`engine.py:858-866`, `:871-895`) | `src/world_substrate/engine.py` |
| A world-specific conservation check exists for one reference world only, "not a substrate law" | `assay_conservation`, `src/world_substrate/assay.py:269` |
| A read-only derived view pairs two give events into one exchange | `src/world_substrate/exchange.py:68` |
| About fourteen build checks guess meaning from rule shape or report the test run | `scripts/world_builder_service.py:840-1220`, used at `:1700-1760` |
| The rules writer revises only the moves it changes | `merge_revision`, `scripts/generate_causal_model.py` (#278) |
| Nothing declares a law, and nothing reviews the rules against the description | absent |

## The three pieces

### Piece 1. The world declares its laws (copy: Petri-net place invariants; Concordia's stock-and-flow ledger)

The world designer's output gains `resources` and `laws`, each with a plain sentence for the page. A **resource** is
declared once with every place it is kept, because the same thing can sit under different names on different
entities (pencil13: the customer pays from `customer.cash` into the shop's `business.cash`; Q47):
`{resource_id, says, kept_in: [{component, field}, ...]}`. A resource's amount on an entity is the sum of the fields
it is kept in there. Laws come in two shapes and name resources, never raw fields:

- **total**: `{law_id, says, resource: <resource id>, may_change_by: [move or process ids]}`. The resource's amount
  summed over every entity may change only in a step made by a listed move or process (the factory's `make-pencils`,
  the customer's `use-pencil`); every other step must leave it unchanged. This is a P-invariant with named exempt
  transitions, and it covers both "nothing from nothing" and "nothing vanishes".
- **pairing**: `{law_id, says, move: <move id>, gives: {resource, from, to}, pays: {resource, from, to}}`, where
  `from` and `to` are the move's participant roles. Every step of that move that moves `gives` from one to the other
  must also move `pays` the other way, both non-zero. "A purchase moves goods one way and payment the other."

Laws do not cover stock with nowhere to go: piling up leaves every total unchanged, so it is a reachability question
(Q43), left to the test-run report and the review. A law can itself be wrong for the world; the review reads the
laws against the description too (Q48).

Laws name the world's own fields and moves. There is no fixed list of goods or moves; the designer writes the
laws
for whatever the description holds. A world with no `laws` behaves exactly as today. The rules writer sees the laws as
input and is told every move must keep them.

### Piece 2. The engine enforces declared laws (extends the existing scope check)

`src/world_substrate/laws.py` holds one pure function, `law_breaches(laws, before, after, step_id)`, called at every
commit point. Two cases, because moves and processes are refused differently today:

- **A move** (`Engine.apply`, right after the write-scope check at `engine.py:686-720`): a breach refuses the whole
  step with status `law_breach` and a failed check that quotes the law's `says` sentence, exactly as a scope
  violation of a move does today: nothing changes, the refusal event is recorded.
- **A process** (a tick in `Engine.advance`, or a knock-on wave in `_settle`): today a scope breach here raises
  `ScopeViolation` and the state is restored with no event (`engine.py:1005-1015`), because a process is
  engine-trusted. A law breach is different: it is a mistake in model-written rules, so it must be recorded, not a
  crash. `_apply_process` runs the law check after its scope check and reports a breach (the process id and the law)
  instead of committing. `_settle` then stops and returns a refusal record, `{status, process_id, law_id, says}`, in
  place of today's bare `None` (which becomes the same record with status `reaction_limit`). The two callers refuse
  the whole moment as they refuse `reaction_limit` today:
  - **in `Engine.apply`** (a move's knock-on effects): the world is restored and `_reject` records the move refused
    with status `law_breach`; the event carries the move's rule id, and its failed check quotes the law's sentence
    and names the process that broke it;
  - **in `Engine.advance`** (a tick process, or the knock-on effects of one): `_refuse_round` gains `status` and
    `check` arguments; the tick is undone and one event with status `law_breach` carries the process's rule id and
    the law. As with `reaction_limit` today, the advance returns there: later steps of a multi-step advance do not
    run, and the next round starts from the restored state. Because the build's scripted test run runs the rules, a breach there is
a build finding sent to the rules writer by name (Q46). This is the existing invariant "Mechanics propose; one
enclosing transition validates and commits or refuses" (AGENTS.md), with the world's own laws added to what the
enclosing transition validates; it adds no loop, clock or scheduler (Decision 006).

### Piece 3. An independent review reads the rules (copy: LLM+P and Guan et al. 2023 validator feedback)

`scripts/review_rules.py`: one typed `llm_client` call, a different model family from the rules writer, with a fresh
context holding only the description, the laws and the compiled rules. It returns findings, each
`{rule_id, description_words, problem}`, never a pass mark (Q44). Findings go to the rules writer's existing revision
step (`merge_revision`), and the build record lists them. Laws catch bookkeeping; the review catches meaning a law
cannot state (a move that changes nothing, a rule that contradicts the description).

## Requirements

| Id | Requirement (source) | Fails when | Control | Status |
| --- | --- | --- | --- | --- |
| R1 | Moves stay free; no fixed move types (Brian 2026-10-28) | a law shape forces a move into a template | laws constrain totals and pairings only; L1 | Built and run live (S1: #280, `evidence/declared-laws/s1-pencil/`) |
| R2 | The world's own laws are written by the AI that designs it (Brian 2026-10-28 design 1) | laws are hand-written or pencil-specific | L1 on the live pencil build and S5's other descriptions | Built (S1); S5 planned |
| R3 | The engine enforces declared laws generically and names the law (design 2) | a breach commits, or a refusal names no law | L2, L3 | Built (S2: `src/world_substrate/laws.py`, `tests/test_laws.py`); L3 live half runs on the deployed build |
| R4 | A separate review checks rules against description and laws (design 3) | the reviewer is the writer, or returns a verdict | L4 | Built (S3); live check `evidence/declared-laws/s3-pencil/`: L4 held, L5 failed (an unreviewed try was kept; rank and reviewer prompt fixed; the reviewer now sees starting values and preview law refusals reach the build record, #293); second build `evidence/declared-laws/s3-pencil-2/`: no review ran because the last try of each structure failed to compile (fixed: the best unreviewed try is now reviewed), and its replay names the starved shop; third build `evidence/declared-laws/s3-pencil-3/`: both reviews ran and named the missing arrival, the redesign wrote it, and the compiler refused it because the destination field may be empty (fixed: `ref:` links accept `entity_ref_or_null`; the free replay then delivers and sells); fourth build `evidence/declared-laws/s3-pencil-4/`: both reviews ran, the redesign added the moves the first review asked for, and the whole chain ran live to a sale, but the dry run had said eight moves were never offered because discovery stopped at 256 moves before reaching the right buyer (fixed: discovery narrows participants by their own checks first; the free replay offers every move and sells 7); the same build kept a try in which pencils could never be sold over one that ran every move, because an ongoing world counted as alive only with a world process (fixed: alive is what the test run saw, still active at the end; the recorded build replayed with today's code keeps a try that offers every move) |
| R5 | Validation stops growing one check per bug | a heuristic retires without proof, or a new one is added | L6 | Planned (S4) |
| R6 | Saved worlds replay unchanged (AGENTS.md invariants) | a world with no laws behaves differently | L7 | Planned in every slice |
| R7 | Every run is readable in full (core rules) | a law refusal or review call is missing from the trace | L8 | Planned in every slice |

## Acceptance checks

| Id | Check | Run and what its trace must show |
| --- | --- | --- |
| L1 | The designer declares laws in the world's own terms | `evidence/declared-laws/s1-pencil/`: the build record's `laws` names the pencil world's own resources and moves, each with a `says` sentence; no law was hand-edited (the bundle's laws equal the model reply in the trace) |
| L2 | A step that breaks a total or a pairing is refused whole, law named | `tests/test_laws.py`: the pencil13 fixture's buy-boxed-pencils with a pairing law gives status `law_breach`, world unchanged, failed check quotes the law; a make move outside `may_change_by` is refused the same way; a move whose knock-on wave breaks a law is refused through `_reject` (status `law_breach`, the move's rule id, a failed check naming the process and quoting the law); a tick process that breaks a law is refused through `_refuse_round` (status `law_breach`, the process's rule id, the law quoted) and the advance stops there; a write-scope breach by a process still raises `ScopeViolation` |
| L3 | A test-run breach reaches the rules writer by name | `evidence/declared-laws/s2-pencil/`: if the test run refused a step, the next rules call's request quotes the law; if none was refused, the TRACE_READ says so and L2 carries the claim |
| L4 | The review is independent and returns findings | `evidence/declared-laws/s3-pencil/`: the review call's model differs from the rules writer's, its request holds only description, laws and rules, and its reply is a findings list; run on `tests/fixtures/pencil13-kept.json` it names buy-boxed-pencils |
| L5 | The canonical example runs live | `evidence/declared-laws/s3-pencil/` (or S5): the kept world's run shows sales moving cash both ways, no law refusals from its own rules, and the build record lists laws and findings |
| L6 | Each retired heuristic is covered | `evidence/declared-laws/s4-retire/README.md`: per retired check, every incident it caught (table above) is refused by a law or named by the review on its saved world; checks that report the test run stay |
| L7 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with the open-attempt plan's A8 replay tests named passing |
| L8 | Every run is fully traced | each `evidence/declared-laws/<run>/` has `run-log.jsonl` and a `TRACE_READ.md` that passes `scripts/check_trace_reads.py`, read by the implementing agent before reporting |

## What Brian judges on the working page

L1-L8 are the agent's checks. What a person opens and sees to decide it works is in
`docs/planning/declared-laws/acceptance-criteria.json`, each with steps on the World Builder, the expected result
and a broken case that looks different:

| Id | Criterion | Broken case to tell it apart |
| --- | --- | --- |
| A1 | The build record shows the world's own laws in plain words | no laws, or laws naming things the world lacks |
| A2 | A move that breaks a law is refused and the page names the law | pencil13's buy-boxed-pencils shows as done with no payment |
| A3 | The review names where rules miss the description, quoting it | empty, "looks good", or findings with no quoted words |
| A4 | The pencil world runs with every sale paying | goods move and cash does not; or the build fails (pencil14) |
| A5 | Moves stay free, in each world's own terms, with no fixed move kinds | every move labelled transfer, exchange or transform |
| A6 | Four very different descriptions (pencil, airfield, kitchen, the long Waltzman scenario) each build a world that keeps its own laws | pencil laws reworded, a committed step that breaks a law, or only pencils work |
| A7 | Mistakes are caught by laws and the review, not a growing list of hand-written checks | a new mistake fixed by adding another guess check |

## Success and disproof

**What L1-L8 are:** the agent's acceptance checks for R1-R7, one row each in the table above. Each is a direct check
of the claimed property, not a stand-in for it: L1 reads the laws themselves in the build record and compares them
with the designer's reply; L2 and L3 read the refusal events and the rules writer's next request; L4 reads the review
call's model, request and findings; L5 reads the kept world's own run, sale by sale; L6 replays each incident's saved
world and reads whether a law or a finding names it; L7 replays law-free saved worlds; L8 reads each run's trace
files. A test count, a merged pull request or a status line alone satisfies none of them.

**Success:** L1-L8 pass, each judged from the full trace of the run it names. **Disproof:** any of these in a named
run's trace: a law that names a field or move the world does not have; a committed step whose before and after break a
declared law; a refusal without the law's sentence; a review call sharing the rules writer's model or conversation; a
retired check with an incident neither a law nor the review catches; a law-free saved world whose replay differs.
Trace review: the implementing agent reads every law refusal, every review finding and a sample of at least five
ordinary steps per run, and writes `TRACE_READ.md`; each of L1-L8 is expected `pass`. Where each trace lives:
L1, L3, L4, L5 and L6 in `evidence/declared-laws/<run>/run-log.jsonl` (with `TRACE_READ.md` beside it) plus the
`llm_client` trace ids it records; L2 and L7 in the `scripts/check_project.py` output for the slice's merge commit,
saved as `evidence/declared-laws/<slice>/check_project.txt`, with the named tests' assertions read; L8 is the reading
of those files itself. An acceptance criterion that names only an outcome ("tests pass", "pull request merged", "the
status reads ok") fails this rule; every row names what its trace must show. Exemption: a criterion with no run (a
pure document edit, such as this adoption commit) says so and why in its slice's `TRACE_READ.md`; no criterion
L1-L8 is exempt.

## When a run fails or surprises us

This procedure is separate from the anticipated failure modes in Requirements and Uncertainties: those are designed
for in advance, while this is what to do when a real run fails or surprises us in a way nobody planned. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,
intermediate stages (laws, rules, review findings, test-run refusals) and the output (build record, page) before
choosing a fix; cite where it diverged; classify it evidence absent (never retrieved), evidence returned but unused or contradicted, invalid
expectation, or unresolved. An unresolved cause permits investigation, not a repair. A repair is verified by a new traced run whose
`TRACE_READ.md` links the original; the original stays. A new symptom is first asked "which law or review finding
should have caught this?" and fixed there; a new heuristic check is the last resort and is recorded as a question.
Never rerun until a behavior appears and report only that run. Review completeness never changes the run verdict.

## Slices, in order

| Slice | What lands | State | Checks |
| --- | --- | --- | --- |
| S1 | `resources` and `laws` in the world design contract (`scripts/generate_world_bundle.py`) and its validator; laws passed to the rules writer; build record and page list them | fully_specifiable_now | L1, L7, L8; one live pencil build |
| S2 | `law_breaches` in `src/world_substrate/laws.py`, called in `Engine.apply` after the scope check and in `_apply_process` (ticks and knock-on waves); `_settle` returns a refusal record; `_reject` and `_refuse_round` record `law_breach`; status `law_breach`; test-run breaches become build findings | fully_specifiable_now | L2, L3, L7; free replays of saved worlds first |
| S3 | `scripts/review_rules.py` and its findings into the rules writer's revision step | conditional (Q44: model choice) | L4, L5, L8 |
| S4 | retire the heuristics Q45 names, one by one, each with its incident proof | conditional (Q45, needs S2 and S3) | L6, L7 |
| S5 | live builds of four varied descriptions in parallel (pencil, airfield, a kitchen, the Waltzman scenario) | conditional (needs S1-S3) | L1, L5, L8 per run; read for Q43 counterexamples |

Each slice is its own pull request and leaves a working World Builder.

## Decisions

- **D1 (Brian, 2026-10-28, "yes lets make it companhy plannign complaint"):** the three-part design (laws declared
  by the designer, enforced by the engine, an independent review) replaces fixed move types.
- **D2 (made, technical):** law checking sits beside the write-scope check inside the existing commit, not in a new
  engine stage (Q46; Decision 006).
- **D3 (made, technical):** two law shapes, total and pairing (Q43). Anything else stays an ordinary rule the review reads.
- **D4 (made, technical):** borrow the semantics of Concordia's `stock_flow_ledger.py` (holders, an outside boundary,
  `is_conserved`) but do not adopt it: its fixed operation set is the fixed-move-types design Brian rejected.

## System model

- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a law breach changes
  nothing), RULE-DERIVED-AUTHORITY. Adds: `world-law` (the bundle's `laws`), `law-check` (status `law_breach`),
  `rules-review` (the build record's `review_findings`). Each is a node in
  [docs/model/domain.graph.json](../model/domain.graph.json) marked "in documents only" until its slice builds it.
- Scope: this repository's own model, linked from `docs/wiki/README.md`; the scientific-hypergraph mapping is unchanged.
- Each slice updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request;
  the drift test must fail on a renamed field before it passes. Views: `owner_run_log` and `home` must show the laws,
  each law refusal with its sentence, and the review findings; each slice adds its row to `docs/model/VIEW_COVERAGE.md`.
- The trace must show, per element: the bundle's `laws` as the designer's reply; each `law_breach` event with the law
  id and before/after; each review call's trace id, model and findings.

## Trace visibility

- Each run's `run-log.jsonl` records the inputs (description, bundle hash), every build step with its time, each model
  call (designer, rules writer, reviewer, residents) with request messages, typed result and `llm_client` trace id,
  every engine event with before/after and failed checks (including `law_breach`), and the output (build record, page
  JSON). Kept for ordinary runs, not only failures; this adoption commit alone is document-only and runs nothing.
- The model's reasoning, where the model exposes it: each call's reasoning text (OpenRouter `reasoning` field, and
  the residents' `reasoning` field in `scripts/run_authored_world.py:368`) is kept in the run log with the call, not
  dropped; a model that exposes none is recorded as such.
- How to open one: `jq . evidence/declared-laws/<run>/run-log.jsonl`; model calls in the VPS `llm_calls` table by
  trace id. Who reads and when: the implementing agent reads every run's trace before reporting its slice: every law
  refusal and review finding in full, and at least five ordinary steps per run across rounds and actors.

## Capability reuse

No catalogue entry fits, because `reuse_candidates.yml` and `capability_registry.yml` hold approvals, notifications,
scheduling, document-to-text and search wrappers, none of which check rules or conservation. Model calls go through
the shared `llm_client` (listed in `~/code2/workspace/docs/capabilities.md`). No new cross-project capability is added;
the law check's and the review's first and only consumer is the World Builder build.

## Prior art and ownership

Prior-art review 2026-10-28 (summarised in Decisions D3-D4): Petri-net place invariants (laws as weighted sums with
exempt transitions); Concordia contrib `stock_flow_ledger.py` (Apache-2.0, semantics borrowed); LLM+P and Guan et al.
2023, AutoToS, WorldCoder (a model writes a world model, a validator feeds corrections back); Huang et al. 2023
(arXiv 2310.01798), SCORE (2404.17140) and Wataoka et al. 2024 (2410.21819): self-review without outside feedback is
weak and self-preferring, hence D2 of Piece 3. Overall disposition: **compose**, with a small law language of our own.
Per candidate:

| Candidate | Disposition | What we take |
| --- | --- | --- |
| Petri-net place invariants | compose (idea only) | a law is a weighted sum that only named moves may change |
| Concordia contrib `stock_flow_ledger.py` | bounded exception (semantics borrowed, code not adopted) | holders, an outside boundary, `is_conserved`; its fixed operation set is the fixed-move-types design Brian rejected (D4) |
| LLM+P, Guan et al. 2023, AutoToS, WorldCoder | compose (method) | a model writes the world model and an outside validator feeds named corrections back to it (Pieces 2 and 3) |
| Huang et al. 2023, SCORE, Wataoka et al. 2024 | reuse (finding) | the reviewer must be a different model and context from the writer (Piece 3) |
Owner: World Substrate's rules layer. Parallel-implementation check: one commit path; `grep -n "def apply"
src/world_substrate/engine.py` stays one hit and `law_breaches` has one caller per commit site.

## LLM call boundary

Build call graph: world designer (existing; output gains `laws`) -> rules writer (existing; laws added to its input,
test-run law refusals and review findings added to its revision input) -> reviewer (new, one call per build attempt,
after compile, before the test run's verdict) -> no further model call. Laws and review findings have no authority to
change state: laws only refuse, and findings only reach the rules writer. Rules writer and designer stay on the World
Builder's model; the reviewer uses a different family through `llm_client` (Q44). Structured result boundaries:
the **world designer** returns the world bundle JSON defined by `_contract()` (`scripts/generate_world_bundle.py:93`),
parsed with `safe_json_loads` and accepted only by `validate_bundle` (`scripts/scaffold_world.py:45`); S1 adds
`resources` and `laws` to both, and a reply that fails validation goes back for repair, up to `MAX_REPAIRS`. The
**rules writer** returns the causal model JSON whose schema `causal_model_schema(bundle)`
(`scripts/generate_causal_model.py:330`) builds from the bundle, then `tidy_proposal` and the installer check it; a
revision is merged by `merge_revision`. The **reviewer** (new, S3) returns `{"findings": [{"rule_id": str,
"description_words": str, "problem": str}]}` through `llm_client`'s typed structured call, with `rule_id` checked
against the compiled rules' ids; any other shape is recorded as a failed review. Failure: a failed or malformed
review call is recorded with its error and the build continues without findings, visibly. Tracing: each build's calls
share its trace id, as today.

Provider: OpenRouter through `llm_client`; designer and rules writer on the World Builder's `DEFAULT_MODEL`
(`scripts/run_authored_world.py:37`), the reviewer on a model of another family chosen in S3 (Q44). Spend authority:
Brian's owner allowance, given for this plan by his 2026-10-28 "yes" and his added OpenRouter credit; the visitor
allowance stays $3/day. Promotion condition: laws and review findings count as working only after an authentic live
build on the deployed service (owner allowance, through the real page) whose `run-log.jsonl` and `TRACE_READ.md` show
them; fixture and replay results support a slice but are never reported as live.

## Evaluation design

One measurement (Q44), for one decision. **Decision it changes:** S4, whether each guessing check retires. If the review
and the laws together catch every incident a check caught, that check goes; if not, it stays and the miss becomes an
open question. **Why argument cannot settle it:** whether a different model, given the description and the rules,
notices a payment missing from a purchase is a fact about that model on these worlds; the prior art says self-review
is weak but says nothing about this reviewer on these rules. **Parity:** every candidate reviewer gets the same input
(description, laws, compiled rules of each saved incident world, no other context) and the same findings schema, and
is scored only on whether it names the incident's rule; the heuristics it is compared with run on the same saved
worlds. **Cost:** about seven saved worlds, one review call each, a few cents and minutes on free replays; a wrong
retirement would let the next pencil-style bug run unnoticed, which has already cost several paid builds and days.
Why measuring is cheaper than choosing now and correcting later: retiring a check is reversible in code, but a wrong
retirement is found only when a live build ships a broken world to a visitor, after paid builds and a trace read
(pencil2-pencil14 took about $2 and two days to surface their bugs); the replay costs cents and minutes and runs before
any retirement. **Under each result:** a reviewer that names an incident's rule lets that check retire in S4; one that
misses it keeps the check and opens a question; if no candidate names more than half, S3's review stays advisory and
S4 retires only checks a law covers.

## Irreversible actions and spend

Who authorizes spend: Brian alone. He authorized this plan's owner-allowance builds on 2026-10-28 ("yes lets make it
companhy plannign complaint", with the OpenRouter credit he added: "there is more money"); any spend past the caps
below, or any new spend route, needs his yes first. Nothing irreversible: merges are pull requests and deploys redeploy from the previous commit. No deletion of saved
worlds or run records, no outreach, no change to other repositories. Spend: owner allowance only, after free replays;
about $0.15 per live pencil build, at most $1.00 per slice and $3.00 across the plan before reporting; S5's four builds
are about $0.60. The visitor allowance stays $3/day.

## Uncertainties

- Q43 (agent, resolved by reading): two law shapes cover every logged incident; S5 is read for a counterexample.
- Q44 (agent, open): which model reviews, and whether the review earns its cost; settled by the review run on the
  saved incident worlds before S4.
- Q45 (agent, open): which heuristic checks retire; settled per check in S4.
- Q46 (agent, resolved by argument): run-time refusal first; a static proof is optional.
- Wrong or missing laws: a designer that declares too few laws catches less, never more wrongly; a designer that
  declares a wrong law makes the test run refuse a legitimate move, which shows as a law refusal in the build record
  and goes to the rules writer and the review. L1 and S5's reads check both.

## Activation facts

Recorded in [activation-facts.json](declared_laws/activation-facts.json): shared mechanism yes (the engine and
the build serve every world), one empirical comparison (Q44, see Evaluation design), LLM central yes, spend yes (owner
allowance), deploys yes (see Deployment). Route: [path-decision.json](declared_laws/path-decision.json), reset: this re-plans the World Builder's
validation after the one-check-per-bug approach hit an implementation obstacle (pencil2-pencil14), with no single
identified fix. One writer still runs the slices in order. The plan copies
established methods but claims conformance to none, so `claims_external_standard` is false.

## Deployment

Each slice deploys once, after its pull request merges (squash) on `main`. Targets and commands:

| Target | Deploy command | Live check that the new version serves | Rollback |
| --- | --- | --- | --- |
| World Builder API on the personal VPS (container `world-builder`, `/srv/apps/world-builder`) and the pages Worker `world-builder-pages` (home, play, build) | `scripts/deploy_world_builder.sh <merged commit>`: runs the local gate unless that tree already passed, then personal-vps `apps/world-builder/deploy.sh` for the API and `deploy/cloudflare/world-builder/build.sh` plus Wrangler for the pages | `curl https://brianmills.dev/world-builder/api/health` reports `build_commit` equal to the merged commit (the script waits for it and exits 3 otherwise); the home page served at <https://brianmills.dev/world-builder/> contains the slice's new text (S1: "Laws this world keeps") | API: `ssh personal-vps 'docker tag world-builder:<previous short sha> world-builder:current && cd /srv/apps/world-builder && docker-compose up -d'` (the last 3 image tags are kept); pages: rerun `scripts/deploy_world_builder.sh <previous commit>` |

No deploy runs while a live run is in progress on the service.

## Durable documents

Durable documents: system_model#ENT-RUN-RECORD, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, plans

These roles are declared in the repository's `durable_documents` block (`.agentic/repo.yaml:3-11`): `system_model`
is `{prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`, where ENT-RUN-RECORD, PROC-TRANSITION and
PROC-PROCESS-TICK are ids (`docs/model/trace.yaml:22, 28, 31`), and `plans` is `docs/plans/`.

S1 changes ENT-RUN-RECORD (the build record gains `laws`); S2 changes PROC-TRANSITION and PROC-PROCESS-TICK (law
checks in each commit and wave); S3 changes ENT-RUN-RECORD (`review_findings`). At completion of each slice,
`python3 ~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan
docs/plans/declared_laws.md --range <adoption revision>..HEAD` must exit 0.

## Authority and non-goals

**Authority:** Brian's "yes lets make it companhy plannign complaint" on 2026-10-28 to this design; one agent writes;
world-substrate and its own deploy only.

**Non-goals:** fixed move types; laws of shapes other than totals and pairings; a static proof of laws; changes to
the open-attempt plan's S3 skill rolls; any change to Cybernetic Influence v3 or Concordia.
