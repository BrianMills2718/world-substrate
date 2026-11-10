# Lessons: what would have made this faster

Written 2026-10-23 after the World Builder reached a full C1–C6 pass (#213, #214). Each lesson says what
happened, the evidence, and what to do instead. Lessons 1 and 6 are also standing rules in
`tests/AGENTS.md`, which the root `AGENTS.md` points to.

## 1. Test against saved worlds for free before paying for a live run

**What happened.** Several bugs were found only by a full paid live run and a full read of it. The latest:
in run c1r18 the technical and logistics groups were never offered their own message, because move
discovery stopped at its 256-move cap before reaching them. The fix was proven by replaying the saved world
offline, with no AI call (`tests/test_discovery_links.py` on `tests/fixtures/c1r18_waltzman_world.json`, #211).
The scripted-mover bug (#193) was also confirmed by no-spend replays of saved pencil worlds.

**Instead.** Every world a live run builds becomes a saved fixture. Before any paid run, replay the saved
worlds the change could affect, with scripted moves, and check the property you care about (every person
offered their own key move, the chain reaches the customer). Pay for a live run only after those pass. Two scripts do this: `scripts/check_saved_worlds.py` replays every
saved world in `tests/fixtures/` and fails if one listed as whole stops being whole (`--update` rewrites the
list), and `scripts/replay_build.py [--follow-record] <evidence folder>` reruns a recorded build with today's code
and its own recorded model replies, so it shows which try today's code would keep.

## 2. Read the run itself, not a summary of it

**What happened.** Counting scripts reported passes that a read of the run showed were false: a pencil run
passed "by the letter only" because the shop could never sell, and a readout credited AI members with
making support conditional when only a rule had done it (#194).

**Instead.** Enforced: a run reported as evidence needs `run-log.jsonl` and a `TRACE_READ.md` with a section
for every round. `scripts/check_trace_reads.py` refuses it otherwise.

## 3. Write pass criteria about the real outcome, not a count

**What happened.** "Runs at least 20 rounds without narrowing to one move" let pencil worlds pass where
pencils could never reach a customer (retired goal, `git show e332eb7:docs/plans/best-of-all-worlds.goal.md`, C4 history).

**Instead.** Each criterion names the outcome a person would check ("a pencil is sold to a customer", "each
group's concern reaches its named country"), and a count is only supporting evidence.

## 4. Adopt the established framework on day one

**What happened.** The live AI people first ran as direct model calls with hand-written briefs. Concordia
(an existing framework for AI agents in simulations) was shown to fit on 2026-10-05 (#89), but it began
playing the people only on 2026-10-16 (#168), after the direct calls' gaps had shown up in runs.

**Instead.** Prior art first. Once a spike shows an established tool fits, move to it before building
further on the home-made version.

## 5. Build worlds the way a developer works, not in one shot

**What happened.** One-shot model calls with hand-written retries produced fragile rules.

**Instead.** Documented in [Decision 008](../decisions/008-build-worlds-in-an-agent-harness.md): an agent
drafts, runs its own checks, makes small edits and iterates.

## 6. Prove only what a change could break

**What happened.** Each goal reran the whole C1–C6 set live: a Waltzman run, two pencil runs and the
failure checks, each needing a full read. Since October 1, roughly half the commits were evidence, goal or
check work rather than new ability.

**Instead.** Keep a fixed set of saved runs and replay them for free as the regression guard. A change
gets live runs only for the behavior it adds or the criteria its code paths touch, plus one fully read live
run of the canonical example.

## 7. Label scripted moves and never let them pass as behavior

**What happened.** A scripted mover that always took the first allowed move made worlds look stuck (two
workers never acted). The worlds were fine; the mover was wrong (#193).

**Instead.** Every run says whether its moves are scripted or AI. When a run looks stuck, check the mover
before the rules.

## Earlier lessons carried from the retired milestone audits

Added 2026-11-09 when the milestone audits were retired. Each names the audit's former path and the
last commit that holds it (`git show <commit>:<path>` restores it).

## 8. Installation checks consistency, never completeness

**What happened.** Across two authored mechanics, each check caught something the other two missed:
watching behaviour caught `take` in M3 where declarations could not; declarations caught five readers in
M4 where behaviour saw nothing; only the conservation ledger caught a destroyed quantity. A mechanic that
writes less than it declared is invisible to the scope guard by design (`docs/audits/m3-overheat-authoring-experiment.md`
at `d14d7b3`, `docs/audits/m4-spill-experiment.md` at `60b3f6b`).

**Instead.** State each check's blind spot next to its result: declarations inherit their inputs'
omissions, behaviour is blind behind an existing refusal, and accounting covers only quantities the ledger
models. The under-writing gap is open question Q56.

## 9. A check you just built is an untested claim

**What happened.** M3's new assay reported seven undeclared reads; four were false positives from its own
substring matching, and the wrong count reached the M4 audit, the roadmap and two commit messages before
anyone read a flagged line (`docs/audits/m3-overheat-authoring-experiment.md` at `d14d7b3`, "Corrections").

**Instead.** Read a sample of a new instrument's flagged lines before reporting its count.

## 10. What the observation shows decides the score

**What happened.** The same world, model and 16 turns scored final health 60, 80 and 100 as the policy's
move list gained process progress and then the rules' own warnings; the mechanics never changed
(`docs/audits/m5-policy-consumer.md` at `cb3e507`). Warehouse Rush showed the same thing: showing each
offered move's installed effects as an authoritative preview changed what the model chose
(`docs/audits/warehouse-rush-preflight.md` at `eed5651`).

**Instead.** When a resident behaves badly, first check what it was shown before changing rules or models.

## 11. Model-written rules fail by being inert or breaking an unwritten convention, not by being dangerous

**What happened.** Of ten M7 proposals none was harmful, two were no-ops and two set `owner_ref` to an
empty string, which broke a convention the world never declared and passed every check. With a richer
language (M7b) the model proposed the same no-ops and the same empty owner at the same rate; this time a
typed-reference invariant refused them (`docs/audits/m7-authoring-rate.md` at `b97665a`,
`docs/audits/m7b-relational-authoring.md` at `38c9cec`).

**Instead.** Declare world conventions as checkable invariants; review effort scales with the number of
proposals, not their quality. The language ceiling was real but was not the main cause.

## 12. Suspect the harness before the world

**What happened.** In Kitchen, a fixed `for actor in actors` order meant one cook always committed first,
so the other's every move was stale (14 of 14) although the plan was really taken only once; and a
hard-coded Castaway vocabulary rendered five different kitchen moves as the bare word "take", so the
agents were choosing between identical labels (`docs/audits/kitchen-contested-world.md` at `f57ef42`).

**Instead.** Alternate commit order, measure "was the plan still on offer" rather than "was it stale",
and test that distinct action ids get distinct descriptions. Lesson 7 is the same pattern.

## 13. Represent what matters causally; a neutral name is not generality

**What happened.** Warehouse Rush v0's transport law used the semantic `route` and never the physical
dock; v1 added `cargo.target_dock` and the law enforced it (`docs/audits/warehouse-rush-preflight.md` at
`eed5651`). The second world (M6) found four couplings to freshwater content sitting in modules named for
their general purpose (`docs/audits/m6-second-world.md` at `5d26e7c`).

**Instead.** Prove generality with a second, different world, and represent the distinction a law must
check rather than leaving it in a label.
