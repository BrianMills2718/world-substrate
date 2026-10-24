# Goal: a person who loses a race is told who took it, and nobody's round runs twice

Planning package: docs/planning/planning-package.json

Follows [waltzman-tasks-slice2.goal.md](waltzman-tasks-slice2.goal.md), which is done. Chosen from the planning
package's open questions: Q2 (losers of a race are not told) and Q6 (one round run twice), both in the substrate's run
loop, so they affect every world on every run. Q13 asks Brian whether this comes before the roadmap's hardening queue;
the recommendation and default are this goal. Not adopted until Brian answers Q13 or starts it.
Profile: continuous-light.

## Roadmap

| # | Goal | Depends on | Why here | Status |
| --- | --- | --- | --- | --- |
| 1 | best-of-all-worlds.goal.md | – | the live World Builder | done |
| 2 | waltzman-belief-and-traces.goal.md | 1 | enforced trace reads; #128 design and first slice | done |
| 3 | waltzman-tasks-slice2.goal.md | 2 | tasks that can fail part-way | done |
| 4 | this goal | 3 | the run loop wastes most people's turns whenever one thing is contested, in any world | open |

## The problem, in one example

Seven people in the Waltzman world each want to settle the one agenda item in round 14. The first succeeds. Each of
the other six is told only "your choice was no longer allowed after earlier moves this round; choose again"
(`scripts/run_authored_world.py:544-545`) and asked once more; with nothing useful left most wait, and their rows read
`nothing_left` (`:570-572`). None is told who settled it or what changed, so none can reason about the loss. A world
with one fire and five firefighters does the same. The "What happened" readout then quotes each loser's first words
next to the move its retry made (`scripts/run_readout.py:93`). Separately, the page once sent one
round's `/run` twice and the server ran and billed both (#225).

## Canonical example

On a free replay of a saved world (the c1r24 Waltzman world, and the truck world), when several people pick the same
one-of-a-kind move in a round, each loser's retry prompt and row say who took it and what it changed, and the
readout quotes the retry's own words. A second `/run` for the same round is refused without spending.

## Done when

- **F1. A loser is told who took it.** A row whose move lost a race records who took the thing and the event id, and
  the loser's retry prompt contains both. Tested on free replays of two saved worlds with no AI calls (stand-in
  residents).
- **F2. The readout quotes the words behind the move that ran.** For a retried move the readout quotes
  `said_on_retry`, as the scene replay already does (Q10). Tested as F1.
- **F3. No round runs twice.** The service refuses a second `/run` for the same session, round and base revision with
  no AI spend, and the page shows the first result. Test sends the same round twice.
- **F4. One live owner-allowance canonical run** at the deployed commit, read in full (`run-log.jsonl` and a
  `TRACE_READ.md` that `scripts/check_trace_reads.py` passes), reporting every lost race and what each loser did next.

Judge each criterion from the full trace of the run it names (llm_client trace ids, Engine event ids, run log), not
from a reported status.

## Boundaries

world-substrate and its own deploy only. Merge after `scripts/check_project.py` exits 0; deploy and confirm the live
commit through the health endpoint; publish-checker before anything new goes public. Owner allowance only; visitor
allowance stays $3/day. Free replays before the one paid run. No Waltzman-specific code paths. Never restart WSL.

## Forbidden substitutes

Hand-edited runs; scripted moves presented as AI; a fix that only changes the Waltzman agenda; rerunning until a
behaviour appears.

## Stop rules

Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence; report it and what
would unblock it. Revalidate after three increments or about four hours.

## Do not gate on

Brian's review; agenda content (Q3); the notice wording (Q4).

## Progress

- 2026-10-24: goal written from the planning package (Q2, Q6, Q10).
- 2026-10-24: Q2 and F2 corrected after the cold review: losers are already asked to choose again; what is missing is
  who took it.
