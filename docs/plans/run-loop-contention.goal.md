# Goal: no round runs or bills twice, and a run's record says why each move was refused

Planning package: docs/planning/planning-package.json

Follows [waltzman-tasks-slice2.goal.md](waltzman-tasks-slice2.goal.md), which is done. Chosen from the planning
package's open questions: Q6 (one round run twice), Q10 (the readout quotes the wrong words after a retry) and Q2 (a
refusal is not linked to its cause). All three are in the substrate's run loop or readout, so they affect every world
on every run. Q13 asks Brian whether this comes before the roadmap's hardening queue; the recommendation and default
are this goal. Not adopted until Brian answers Q13 or starts it.
**Execution profile:** continuous-light

## Roadmap

| # | Goal | Depends on | Why here | Status |
| --- | --- | --- | --- | --- |
| 1 | best-of-all-worlds.goal.md | – | the live World Builder | done |
| 2 | waltzman-belief-and-traces.goal.md | 1 | enforced trace reads; #128 design and first slice | done |
| 3 | waltzman-tasks-slice2.goal.md | 2 | tasks that can fail part-way | done |
| 4 | this goal | 3 | double-billed rounds and records that misattribute words or refusals, in any world | open |

## The problem, in one example

The page once sent one round's `/run` twice and the server ran and billed both (#225). Separately, in round 14 of
the Waltzman run the community group settles the one agenda item and seven others had wanted it too (c1r24
TRACE_READ.md:307). Each loser is told "your choice was no longer allowed after earlier moves this round; choose again"
(`scripts/run_authored_world.py:544-545`) and shown the round's moves so far, so it can see that the community group
settled (for example country-one, c1r24 call 18016). But the prompt does not name which of its moves was refused, and the row does not record
which event blocked it, so a reader of the run cannot say why without re-deriving the order. Then the "What happened"
readout quotes each retried person's first words next to the move its retry made (`scripts/run_readout.py:93`).

## Canonical example

A second `/run` for the same round is refused without spending and the page shows the first result. On a free replay
of a saved world (the c1r24 Waltzman world, and the truck world), when several people pick the same one-of-a-kind move
in a round, each refused row names its refused move and the blocking event id, the retry prompt names both, and the
readout quotes the retry's own words.

## Done when

- **F1. No round runs twice.** The service refuses a second `/run` for the same session, round and base revision with
  no AI spend, and the page shows the first result. Test sends the same round twice.
- **F2. The readout quotes the words behind the move that ran.** For a retried move the readout quotes
  `said_on_retry`, as the scene replay already does (Q10). Tested on free replays of two saved worlds with no AI calls
  (stand-in residents).
- **F3. A refusal names its cause.** A row whose pick was refused after an earlier move records the refused move and
  the blocking event id, and the retry prompt names both (Q2). Tested as F2.
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
- 2026-10-24: Q2 corrected twice after cold reviews: losers are already asked to choose again and shown the round's
  moves (call 18016); what is missing is the link from a refusal to the move that caused it. Criteria reordered.
