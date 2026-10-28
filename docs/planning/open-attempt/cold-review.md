# Cold review, open-attempt plan package, round 9

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-26.
Reviewed revision: f8dc6daa76de3c84e195d1027cdde126d7de354c (read at HEAD 76a6acd)
Verdict: pass

This replaces the round-7 report. It checks the delta since d305058 and the round-8 blocking finding.

## Round 8 (at d305058): revise

Blocking finding: A6 (`docs/plans/open_attempt.md:229`), R4 (`:215`) and the page's risk row said a self-feeding reaction is refused, but the code stops it quietly by the once-per-(process, entity) rule, and the only test (`test_a_self_feeding_reaction_is_refused_whole`) used a ring of 40 glasses, a long chain ending in `reaction_limit`. Nothing asserted the once-per-pair rule on its own. Notes: Q42 should mention the calls with no finish reason; `checks.txt` should name `scripts/build_metamodel.py`.

## Round 9: the blocking finding is fixed

- **New test:** `tests/test_open_attempt.py::KnockOnEffectTests::test_a_reaction_that_keeps_itself_due_fires_once_per_moment` adds a process `settles-on-floor` whose check (`on_desk == False`) stays true after it fires. It asserts the push is accepted, the rule fires exactly once, height is 0, and replay is ok.
- **It fails without the rule.** On a copy made with `git archive` (worktree untouched), replacing the filter at `engine.py:917` (`bindings = [b … not in fired]`) with `pass` makes the new test fail with `'reaction_limit' != 'accepted'`. The ring-of-40 test still passes under that mutant, as it should, since it tests the 32 cap. Each rule now has its own test.
- **Rename:** the old test is now `test_a_chain_past_the_reaction_limit_is_refused_whole`, still tagged A6.
- **Wording:** A6 (`:229`) says a reaction that stays due fires once per moment and a chain of more than 32 is refused whole, naming both tests; R4 (`:215`) says "A6 (once per pair, and the 32 limit)"; the page risk row says "once per thing per moment (tested), at most 32 in all"; ODD 8.20 and `docs/model/trace.yaml` list both tests. All match `_settle` (`engine.py:884`, the fired set, `REACTION_LIMIT` returning None).
- **Rerun:** `tests/test_open_attempt.py` 12 passed, exit 0.

Round-8 notes: Q42 now names the 3 calls with no finish reason (fixed). The `checks.txt` note is moot: its project check was rerun at the subject revision (728 tests, exit 0).

## Delta review

- **Validator:** 4 of 5 substance checks ok; the one failure was `cold_review.reviewed_revision` still at b2216ee, expected until this report is recorded. Freshness ok.
- **Manifest delta:** `tests_run` 728; `knock-on-now` anchored at `engine.py:884`.
- **Review page:** S2 shown as built in the legend, stage 7 ("built in S2"), the slice row and the glossary; the row still says "not done" because the live generated airfield run is owed, which is honest. The question header says 16 open and 26 resolved, matching `open-questions.json`. Q28 left the open table. The glass example is labelled as what the tests run.
- **Regression:** none found.

Unsure about: only that the mutation was done on a copy rather than the worktree; the edit hit exactly one line and the failure was the expected one.

Verdict: pass


## Re-review, 2026-10-28 (declared-laws round 3)

Reviewer: `company-planning:planning-compliance-reviewer` subagent, reviewing all three packages together. Reviewed revision: 3e376db030b31925f7a3b9f8c6d8806e06e17b9a. The full report is in `docs/planning/declared-laws/cold-review.md`.

- **Delta:** the declared-laws plan adds the acceptance part, the `world-design` and `resource` concepts, and questions Q43 to Q48. Counts are 48 questions, 19 of them open; 156 md files; 801 tests. The only validator failure was the old `reviewed_revision`.
- **Regression:** none found.

Verdict: pass
