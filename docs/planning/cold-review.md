# Cold review of the planning package

Reviewer: the `company-planning:planning-compliance-reviewer` subagent, a fresh read with no session context. This is an
agent review, not Brian's approval.

| Round | Commit | Verdict | What it found |
| --- | --- | --- | --- |
| 1 | a895f7f | revise | The project-check command could not be reproduced as recorded. Q2 claimed losers are never asked to choose again (they are, `run_authored_world.py:544-556`). Q10 cited a comment. Q5, Q7 and Q11 were answerable now. Q1 and Q8 had wrong cites. ODD 11.1 had the models wrong. The domain model lacked policy, Linguistic Core senses, frozen profile, write scope, causal trace, world kind and the World Builder. The page loaded libraries from a CDN. |
| 2 | 3673408 | revise | Q2 still claimed losers are never told who took the thing; the retry prompt shows the round's earlier moves (c1r24 call 18016). The same false sentence was in ODD 11.3, DOMAIN and the next goal. Q3 proposed a free replay that cannot show AI behaviour. The manifest command carried a note. The page caption was stale. The domain map was unreadable at its starting zoom. |
| 3 | 0ef2c35 | **pass** | No premise errors. Minor: the goal's round-14 counts, Q1 not saying no observed world needed repair, no scene-replay concept, two weak code anchors, Q12's "6 rounds" uncited. All five were fixed after the pass. The context diagram's label overlap (mermaid C4) was left as is. |

Round 3 checks, reproduced by the reviewer against the sources:

- Q2: call 18016's prompt ends with "your choice was no longer allowed after earlier moves this round; choose again".
  It also carries "What just happened: - community-group: decision.action.settle-agenda-matter"
  (`run_authored_world.py:547`). Neither the prompt nor the row names the refused move or the blocking event.
- Q3: the round-40 quote is at `c1r24/TRACE_READ.md:110` and `:602`. It names both hypotheses and ties the paid run
  to a decision.
- Q5: call 18032 shows `status deployed, support 5` together with `approved False, authorized False`. This matches
  `compile_spec.py:33-34` and `:626`.
- Q11: calls 17868, 17870 and 17876-17878 carry no concern items.
- Q1: start times of 85, 101 and 111 s against the 80 s cut-off (`world_builder_service.py:263`).
- Q9: #217. Q10: `run_authored_world.py:584`, `:599-600`, `run_readout.py:93`, `render_scene_replay.py:398`.
- Q13 and Q14: the cited roadmap lines and Decision 008:48.
- The plan follows from Q6, Q10 and Q2. Its F1-F3 are testable on free replays, with one paid run for F4.
- The page shows all eight parts. Its checks table matches the manifest.

The project check was reproduced by round 2 with the recorded command: 710 tests, OK (skipped=2), exit 0. It was
rerun at 0ef2c35 with the same result.

Lesson from rounds 1 and 2: a "people are never told X" premise is checked against an actual saved prompt, not only
against the code path that adds one line to it.
