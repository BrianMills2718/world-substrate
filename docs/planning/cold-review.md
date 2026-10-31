# Cold review, repo planning package, round 9

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-26, given the round-8 report.
Reviewed revision: f8dc6daa76de3c84e195d1027cdde126d7de354c (round 9; superseded by the 2026-10-28 re-review below)
Verdict: pass

Scope: the delta since d305058 (`git diff d305058 76a6acd`, 15 files). Round 8 (at d305058) was a pass; its findings were notes.

- **Validator:** `validate_planning_package.py --repo . docs/planning/planning-package.json` reported 4 of 5 substance checks ok; the one failure was `cold_review.reviewed_revision` still at d305058, expected until this review is recorded. Freshness ok ("built from f8dc6daa76de, 0 commits of work since").
- **Counts:** `docs/planning/open-questions.json` has 42 questions, 16 open and 26 resolved, as at d305058. Its only change is the Q42 evidence wording, which now names the 3 calls with no finish reason (round-8 note fixed).
- **Manifest delta:** `tests_run` 718 to 728, `subject_revision` f8dc6da, `knock-on-now` anchored at `engine.py:884`, where `_settle` starts.
- **Docs:** `roadmap/README.md` and `docs/wiki/README.md` say S2 is built with the live generated run owed, matching code and plan. ODD 8.20 and `docs/model/trace.yaml` name both the renamed limit test and the new once-per-moment test.
- **Rerun:** `tests/test_open_attempt.py` 12 passed, exit 0.
- **Regression:** none found.

Findings:

- note, `docs/planning/checks.txt`: the round-8 note asked it to name `scripts/build_metamodel.py`. Moot now: the project check in it was rerun at the subject revision itself (728 tests, exit 0), so no later-commit disclosure is needed.
- note, `docs/planning/planning-package.json`: set `cold_review.reviewed_revision` to this revision (done when this report was saved).

Unsure about: nothing material. The reviewer did not run `check_project.py` (as instructed); the 728-test count comes from `checks.txt`.

Verdict: pass


## Re-review, 2026-10-28 (declared-laws round 3)

Reviewer: `company-planning:planning-compliance-reviewer` subagent, reviewing all three packages together. Reviewed revision: 3e376db030b31925f7a3b9f8c6d8806e06e17b9a. The full report is in `docs/planning/declared-laws/cold-review.md`.

- **Delta:** the declared-laws plan adds the acceptance part, the `world-design` and `resource` concepts, and questions Q43 to Q48. Counts are 48 questions, 19 of them open; 156 md files; 801 tests. The only validator failure was the old `reviewed_revision`.
- **Regression:** none found.

Verdict: pass


## Re-review, 2026-10-30 (people-world laws, rounds 4 and 5)

Reviewer: `company-planning:planning-compliance-reviewer` subagent, reviewing the package rebuilt at f83c6d8 (people worlds declare laws and get the review, 66e4b3b). Reviewed revision: f83c6d8a1589dfb8ec8d129c0e0a0e3e3fb9df82.

Round 4 returned revise with six blocking findings, all fixed in 0948968:

1. A missing question about laws the designer leaves out (5 of 9 pencil builds declared no payment law): added as Q49. It blocks S4, A1 and A4, and is settled by argument: the review catches an unpaid sale, so the pairing checks stay until the review catches pencil-s2-kept.
2. Q48 was half answered already: narrowed to laws that allow too much, with the too-narrow half's evidence cited.
3. `rules-review` was marked theory: it is now Substrate at `scripts/review_rules.py:92`.
4. The people-world law path (`declare_people_laws`, `keep_compiled_laws`) was missing from ODD 8.21 and the system model: added.
5. A stale review-page paragraph ("S1 starts next", Q44 open): updated.
6. The A1 and A5 steps could not be followed at the entrypoint: the shared-link steps and the cafe link were added.

Round 5 checked those fixes: validator 9 of 9 parts ok, 139 citations resolved, the package fresh, coverage 6 of 7 requirements (the seventh is about the planning process). Its notes are applied in the commit that records this review: Q49 cites the table rows (lines 13 and 18), Q48 says what keeps it open, and the page's A1 and A5 rows show the shared-link steps.

Carried notes, not blocking:
- The open-attempt package is out of date.
- A1 and A5 use a plain list, not the router's linked table (recorded in A1).
- "about $2 and two days" (`declared_laws.md:388`) has no source.
- Keeping run-log reasoning text is still a slice requirement.

Verdict: pass
