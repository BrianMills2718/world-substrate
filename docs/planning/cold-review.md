# Cold review: repo planning package (AI judge J3 live evidence), 2026-11-11

Reviewer: planning-compliance reviewer (subagent), two passes. No file was edited and no paid call was made.

- Pass 1 read 993f2178b34460f0c318b28522f021139c058014 (J3 merged and its live evidence): verdict revise, 2 blocking
  findings and 4 notes. (1) A4's status note named only the approve run's defect, not the default run's giver rule
  moving coins into Rosa's purse without her choosing, which the package's own trace read records; "built" overstated
  it. (2) Q94 treated the giver shape as the good outcome while Q96 shows it is defective. Notes: Q96's try count
  (5 tries, not 6), Q96's replay not tied to a decision, two stale J2 lines in `openspec/specs/ai-judge/spec.md`
  ("not installed") and the missing `withdrawn` state, and the domain model putting a ruling's origin on the rule.
  The cost ($0.0328 over 19 run-log lines), run counts and Q96's round 4 fact (r4-e00001) reproduced.
- Pass 2 read 7160bda9d8ec8b74d5599b17de91ba105377daba (the fixes): all six resolved, nothing new wrong. Validator in
  the worktree: exit 0, "Verdict: compliant". Verdict: pass.

Reviewed revision: 7160bda9d8ec8b74d5599b17de91ba105377daba

## Earlier review: repo planning package (round 3), 2026-11-10

Reviewer: planning-compliance reviewer, given the round-2 report (verdict revise, at 0c09c1d).
Reviewed revision: 32860542557cf2698a05669b4b29b5041a7e1818
(Confirmed with `git rev-parse HEAD` in `/home/brian/code2/worktrees/ws-estimate-plan`. The tree was clean. No file was edited.)

Scope: the repository package. In the estimate-rules diff I judged only what it changes here: Q63, Q82 to Q88, the domain concepts and the review page data. The estimate-rules plan and its own package are out of scope.

## Validator

I ran `validate_planning_package.py --repo . docs/planning/planning-package.json`. It exited 1.

- Parts: 9 of 10 ok, 0 failing, 1 pending (`investigation`).
- Substance: 6 of 12 ok, 0 failing, 6 pending. The pending ones are checks required only of a new or full_method repository.
- Citations: 245 file citations and 23 other sources resolved.
- Domain model: 64 implemented, 15 dashed; the plan names 18 concepts.
- Metamodel: 29 types, all mapped onto `scientific-hypergraph@7b0638fe0aef`.
- Coverage: 6 of 7 requirements covered; the seventh is about the planning process.
- The only FAIL is freshness: "reviewed at c99cbc704c5a, 19 plan files changed since". Recording this report fixes it. Nothing else fails.

## Previous findings (round 2)

1. **Checks did not reproduce: fixed.** I reran the recorded commands read-only at 3286054. A diff from 4b5bda9 to HEAD touched only check records, the Q77 text, the manifest, page data and `questions_src.py`, so the counts carry over.

| Check | Recorded | Reran |
| --- | --- | --- |
| Project check (`check_project.py`, with the recorded `uv` command) | 891 passed, 2 skipped, exit 0 | 891 passed, 2 skipped, 222 subtests, exit 0 |
| Trace reads | 38 runs, 0 problems | 38 runs, 0 problems |
| Repository format (`repo_format.py`) | compliant 1 of 1, exit 0 | compliant 1 of 1, exit 0 |
| Wiki and Markdown cap (`md_file_cap.py --ref HEAD`) | exit 1, 162 files, 28 unreachable (10 not linked, 18 deep), 16 durable | same, exit 1 |
| Durable documents (`durable_docs_check.py --arc42`) | 16 findings, exit 1 | 16 findings (8 arc42 and goal, 8 STALE), exit 1 |

   Both failing checks carry `tracked_by: Q77`. `checks.txt` matches the manifest.
2. **Q15 answered but open: fixed.** It is now `resolved` with evidence: `repo_format.py` reports compliant 1 of 1, and the cited files exist. The `tracked_by: Q15` on the repository-format row is gone.
3. **Q77 stale counts: fixed.** Q77 now gives 28 unreachable documents, 16 findings and the eight STALE rule names. All of these match my reruns. The J0 trace reads are linked from `docs/catalog.md:192-198`, all five. Q77 says honestly that they remain more than two links deep.
4. **Estimate-rules cold review pending (note): out of scope.** It is reviewed separately.
5. **Weak code anchors for `contention` and `test-run` (note): not fixed here. I accept deferring it.**

- `tools/planning/domain_src.py:29` (`contention`) still anchors to `scripts/run_authored_world.py:740`, which is the scripted-choice line in the blocked-row loop.
- `tools/planning/domain_src.py:35` (`test-run`) still anchors to `scripts/world_builder_service.py:1797`, which is a comment in the retry handler.
- Both anchors resolve, so the validator passes. Pull request #363 (`origin/feat/judge-j0-live`) exists and re-anchors these lines, so editing them here would only create a conflict.
- It stays a note. It must be closed when #363 merges.

6. **Estimate-rules plan citations (note):** out of scope.
7. **Page names the old reviewed revision (note):** the builder run after this review is recorded will fix that.

## Review of the whole package

- **Open questions:**
  - Q63 quotes Brian and cites lines that say what it claims.
  - Q82 and Q83 each name a decision their result would change. The probe's coarse answers do not settle them, and no argument or counterexample in the repository does. The tests are justified.
  - Q85 and Q86 are labelled as not blocking E1 or the plan.
  - Q87's evidence is an argument from construction (the stand-in estimator keeps the free run free). Its citations were not each opened at the line level.
  - Q88 names a decision: whether E2's instructions prefer declared bands.
  - I found no answered question marked open among Q63 and Q82 to Q88.
- **Domain concepts and page data:** the validator resolves citations and the concept count (64 implemented and 15 dashed, with 79 concepts and 134 relations). The estimate-rules concepts are marked theory or dashed.
- **Q77 remains a real open problem and is correctly open.** The 28 unreachable files and 16 durable findings fail on origin/main too, and the question names the fix route. This is not a finding against this package.

## Findings

1. **note, `tools/planning/domain_src.py:29` and `:35` (and the manifest's implemented map):** the anchors for `contention` and `test-run` are still weak. They are deferred to #363 by agreement. Re-anchor by symbol when #363 merges.
2. **note, `docs/planning/estimate-rules/cold-review.md`:** the estimate-rules package must be reviewed before its adoption.
3. **note, `proposals/planning-package/review-page/data.js`:** it names the previous reviewed revision until the builder reruns.
4. **note, repository `README`/package fields:** several package fields (`investigation`, plan cost basis, plain baseline, stage effects, stops, spectrum) are absent. The validator treats them as not required of this repository (first commit 2026-08-31, `full_method` not set). That could change if the repository is later judged new or full_method.

No blocking findings.

## Judgments I was unsure about

- I did not render the review page in a browser, so draw quality and link resolution are unchecked beyond the files existing and the validator's checks.
- I did not re-read the acceptance `asked_by` quotes. The stored coverage (6 of 7) came through the validator and was not independently re-derived this round.
- I did not verify each OpenSpec scenario against code.
- I opened the `contention` and `test-run` anchors but did not re-open every domain citation. The validator confirmed that cited files and lines exist.
- I judged the estimate-rules questions only for being open, real and not answered in the repository.

Verdict: pass

## Earlier reviews of this package

The reviews below came before 2026-11-10. They are kept as they were, oldest first.

## Earlier review: round 9, 2026-10-26

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

## 2026-11-04 re-review, repo planning package

Reviewer: `company-planning:planning-compliance-reviewer` subagent, delta since f83c6d8, three rounds.
Reviewed revision: f824249cf6738faad501bfd07b99e2ee5a54ed78
Verdict: pass

- **Round 1, revise:** Q50 had no recommendation or default; Q45 denied a live people-world build; the plan showed S3 and Q44 as open and left out Q48 and Q49; nothing covered whether an asked person acts on a request (Q52 added).
- **Round 2, revise:** the Q45 fix cut its sentence mid-word; Q51 wrongly said #316's probes used `?share=` (only the issue body misprints it); Q50 conflicted with the plan's done_when and do_not_gate_on; the review page named the wrong plan.
- **Round 3, pass:** all fixed. Project check 859 passed, 2 skipped, exit 0; trace reads 31 runs, 0 problems.
- **Notes kept:** the 2026-11-01 build has no evidence folder yet (follow-up); Q45 cites `people_world.py:298` for the law call only, not the review wiring; `asks` is not yet a domain concept.

## 2026-11-06 re-review, repo planning package (freshness refresh)

Reviewer: `company-planning:planning-compliance-reviewer` agent (run headless with `claude -p --agent`), delta f824249..935d17e and this branch, two rounds.
Reviewed revision: c99cbc704c5a8f2876c464b313373d343108cf1e
Verdict: pass

- **Round 1, revise (reviewed efa3d0d):** (1) the 2026-11-04 Waltzman rebuild kept rules its own review flagged (max_postponements 0) and the ledger, trace read and Q50 did not say so: Q55 added, Q45 and Q50 qualified, the trace read's finding 3 corrected, the plan's S3 noted; (2) many code citations had been moved by a fixed line offset and landed on unrelated or blank lines: domain, ledger, ODD and plan citations re-anchored by symbol. Notes: builds of one description differ (folded into Q50); Q54 can be settled by reading; Q1's anchor (now :266); the served page updates on merge.
- **Round 2, pass (report below).** Its note 1 (ODD P4 and 8.7 compile anchors) is fixed by re-anchoring to `world_builder_service.py:2480-2482`; note 2 is fixed by recording this review.

I found nothing that needs to block this round. The package checks out at subject revision c99cbc7. The validator fails only on the cold-review record, which still points at f824249, and recording this review fixes that.

**The previous report could not be read.** The file holds only a stdin warning and no report text, and the repository's `cold-review.md` has no entry for the efa3d0d review. So I worked out the two earlier findings from the fix commit, which describes them as "the cold review's two findings":

- **Finding 1, the 2026-11-04 Waltzman rebuild (s4-waltzman-3) kept rules its own review flagged: fixed.** The new Q55, the trace read, Q45, Q50 and step S3 of `docs/plans/declared_laws.md` now all say it.
  - I checked the record itself. Review call 23042 says `max_postponements` starts at 0, "so the decision can never be delayed". Row 1 of `run-log.jsonl` shows that finding and one try with no rewrite.
  - The code matches: the 80-second limit (`PEOPLE_REWRITE_BY_S`) is at `world_builder_service.py:266`, the check at `:2254`, and the $1.30 budget at `:94`.
  - Q50 now says the shared run can be judged only once Q55 is answered, or with that caveat stated next to it.
- **Finding 2, code citations pointing at shifted line numbers: fixed.** I opened 20 of the re-anchored lines. Each lands on the function or line it names, for example `_world_fingerprint` at `:384`, `_approval_record` at `:421`, `_assemble_share` at `:603`, `build_engine` at `:71`, `said_on_retry` at `:815-816` and `?run=` at `world_builder_home.html:1272`.

**Validator:** exit 1.

- Parts: 9 of 10 ok, 0 failing, 1 pending.
- Substance checks: 5 of 8 ok, 1 failing, 2 pending; 157 file citations resolve.
- Initiative and spectrum checks: 0 of 4 ok, 4 pending (not required until 2026-11-12).
- Coverage: 6 of Brian's 7 requirements covered. The uncovered one is "company planning compliant", which is about the planning process rather than the product.
- Freshness: ok, 0 commits since c99cbc7.
- The one failure is the expected one: the cold review read f824249.

**Rerun checks:** both match `checks.txt`.

- Trace reads (`check_trace_reads.py --root evidence`): 33 runs, 0 problems, exit 0.
- Markdown cap (`md_file_cap.py --repo . --ref HEAD`): 174 files, 0 unreachable, exit 0.

**Review page:** I rendered it headless. It loads with no script errors and shows c99cbc7. Q55 appears on the Open questions and Next plan tabs, and acceptance criteria A1 to A7 are on the Next plan tab. The diagrams are drawn on the page, not linked. The repository is owned by `BrianMills2718`, so the hive.brianmills.dev address is allowed.

### Notes (not blocking)

1. **Q55, `docs/planning/open-questions.json` (Q55 `resolves_with`):** it calls the time limit "the likely cause", but the code settles it. In the loop at `world_builder_service.py:2251-2256`, every other way out is ruled out:
   - the "good enough" exit needs no review findings, and this try had two;
   - the "second try" exit needs `attempt == 1`, and this was the first try (`attempt` counts from 0, `:2117`);
   - the "budget" exit needs a cost near $1.15, and this build cost $0.14.

   That leaves only the 80-second check. The comment near `:2226-2229` also shows that reviewing a try that will be kept anyway is deliberate. Fix: state the cause as settled and leave only "should a flagged world be kept" open.
2. **Q2 prose:** it still cites `refused_because` at `:622-627`. That field is now at `run_authored_world.py:800`. Q2 is resolved, so nothing a reader concludes changes.
3. **`docs/planning/checks.txt`:** the project check is recorded at efa3d0d (862 tests), not c99cbc7. The commits since changed only planning tools, docs and evidence, not runtime code. The file says so honestly, but it would be cleaner to rerun it at c99cbc7 or name that difference.
4. **`docs/model/open-questions.graph.json:163`:** the Q55 text ends with a double period ("path..").

### What I was unsure about

- I inferred the earlier findings from commit messages because their text was lost. If that report had other findings, I have not checked them here.
- I did not rerun the full project check, render the served copy of the page, or recheck acceptance router records and model mappings that did not change in this diff.

Reviewed revision: c99cbc704c5a8f2876c464b313373d343108cf1e

Verdict: pass

---

### Normative reconciliation re-review — 2026-11-12

Scope: repository package and open-attempt, declared-laws, AI-judge and estimate-rules packages, reviewed together against their shared model and question ledger. This verdict concerns documentation reconciliation. It does **not** certify all implementation slices, predictive validity, complete runtime traceability or full AES conformance.

Previous findings:

- **Fixed — shared checks:** trace-read records now reproduce: `python3 scripts/check_trace_reads.py --root evidence` returned **47 runs, 0 problems, exit 0**.
- **Fixed — method scope:** all five manifests declare `full_method`; investigation, route and semantic-spectrum records distinguish current capabilities from planned contracts.
- **Fixed — open-attempt ownership:** its plan correctly identifies declared-laws as the repository package’s current plan.
- **Fixed — open-attempt acceptance:** A1–A9 now have explicit demonstrations, expected results and failure examples. The novice crash probability follows from the declared dice distribution: **75% versus 12.5%**, not a guaranteed outcome or an empirical aviation claim.
- **Fixed — AI-judge evidence:** historical baseline results and J2/J3 evidence are distinguished. The additional model reviewer is deferred from the minimum required design; existing advisory behavior is not presented as demonstrated semantic protection.
- **Fixed — Q96 design:** the offer contract specifies immutable terms, parties, acceptance, expiry, withdrawal, approval binding and atomic settlement/consumption. The domain model marks the offer as planned; A5 covers the associated failures. The implementation defect correctly remains open.
- **Fixed — stopping:** J5 requires assessment after every completed round; unchanged material fields do not establish that a natural-language condition remains false.
- **Fixed — review pages:** the rebuilt pages remove the identified obsolete reaction-cap, signature/consent, universal-sampling, Q63-status and whole-run-cost claims.

The conceptual guide is coherent with Brian’s direction: heterogeneous models selected by process; actor-owned interpretation and choice; constraints distinguished from norms; explicit uncertainty lifetimes; and resource tradeoffs subordinate to preserving the investigation’s required distinctions. The three conceptual closures, Q63/Q73/Q75, are justified. The **46 remaining open questions** include implementation defects, evidence obligations and explicitly deferred later-slice design work; they must not be reported as universally resolved.

Validator reruns used installed Company Planning `0.2.0+codex.20261112213000` with `--offline-coverage`:

| Package | Parts | Substance | Exit before recording this review |
|---|---|---|---|
| Repository | 10 OK | 10 OK, 2 pending | 1: stale review |
| Open-attempt | 10 OK | 10 OK, 2 pending | 1: stale review |
| Declared-laws | 10 OK | 10 OK, 2 pending | 1: stale review |
| AI-judge | 9 OK, 1 failure | 11 OK, 1 pending | 1: old `revise` and stale review |
| Estimate-rules | 10 OK | 9 OK, 1 failure, 3 pending | 1: old report verdict format and stale review |

All five have four passing initiative/tier checks and a pending system-map requirement dated November 17. Review metadata and the final validator receipts must be updated after recording this review; these pre-update results are not passing compliance receipts.

Remaining limits: baseline/stage-effect evidence and estimate workload guesses remain explicitly pending. Q96 implementation, later-slice design gates, storage failure behavior, aggregate budget verification, legacy documentation findings and broader AES trace coverage remain open. I inspected source files and rebuilt page content, but did not independently repeat the parent’s browser verification or exhaustively reverify every historical quotation and live acceptance demonstration. No additional blocking finding remains **within this documentation-reconciliation scope**.

Scoped dispositions: repository **pass**; open-attempt **pass**; declared-laws **pass**; AI-judge **pass**; estimate-rules **pass**.

Reviewed revision: 0d2a8752ee5625c7e55dd1e1bedb87ab77c7ef73

Verdict: pass
