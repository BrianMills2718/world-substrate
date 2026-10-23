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
offered their own key move, the chain reaches the customer). Pay for a live run only after those pass.

## 2. Read the run itself, not a summary of it

**What happened.** Counting scripts reported passes that a read of the run showed were false: a pencil run
passed "by the letter only" because the shop could never sell, and a readout credited AI members with
making support conditional when only a rule had done it (#194).

**Instead.** Enforced: a run reported as evidence needs `run-log.jsonl` and a `TRACE_READ.md` with a section
for every round. `scripts/check_trace_reads.py` refuses it otherwise.

## 3. Write pass criteria about the real outcome, not a count

**What happened.** "Runs at least 20 rounds without narrowing to one move" let pencil worlds pass where
pencils could never reach a customer (`docs/plans/best-of-all-worlds.goal.md`, C4 history).

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
