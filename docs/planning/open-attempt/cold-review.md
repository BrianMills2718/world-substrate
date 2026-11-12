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

---

### Modeling-contract re-review — 2026-11-12

Scope: changes since `65ffed8` to the shared modeling contracts, question dispositions, acceptance criteria, review pages and AES mappings used by all five planning packages. This is a substantive review of those changes, not a fresh certification of every historical claim or runtime capability.

- **Q76 — resolved appropriately:** the selected contract separates credential knowledge, physical custody, current verifier validity and institutional permission. Disclosure belongs to the actor; verification belongs to the mechanism. Revocation does not erase memory, and detecting a norm violation does not supply an observer with knowledge or compel a human response. Symbolic credentials are explicitly an approximation.
- **Q83 — resolved appropriately:** dependency selection follows the modeled mechanism and interventions. The blade’s two varying inputs are justified only within explicit fixed assumptions and exclusions. Missing inputs, versioned context, cache identity and persistent/shared uncertainty have defined treatment. Model agreement is not presented as proof of sufficiency.
- **Q84 — finding fixed:** the original draft left exposure-time context ambiguous. The revised contract captures the projected content, geometry, light, observer position, source revision/time and model identity when the opportunity occurs. Retries preserve that snapshot; changed conditions require a separately authored opportunity; late results cannot overwrite a terminal disposition. Exposure-specific draw identity avoids accidentally sharing one draw across recipients. A5 and the review page reflect this correction.
- **Architecture challenge — coherent:** the influence, program and physical examples expose different representational requirements without proposing a speculative universal engine. Native expressibility, generated-language support, live integration and scientific adequacy remain distinct. Once-per-pair termination is correctly distinguished from numerical convergence.
- **AES mappings — appropriately bounded:** the inspected existing tests directly support their named information-delivery, write-scope and hook-authority scenarios. Scan roots include the actual owners. Annotation coverage is not presented as behavioral validation, and existing consent, visibility, durability and spending gaps remain explicit.

Verification: committed revision confirmed; working tree clean at inspection; `git diff --check` returned exit 0 before commit; ledger independently counted **96 questions: 43 open, 53 resolved**. Generated estimate and judge pages contain the revised contract dispositions and exposure-time qualification. No simulation or backend evaluation was performed for this review. The parent’s running full check and final package-validation receipts are separate verification obligations.

No remaining substantive finding or human scope decision was identified for these documentation contracts. J4, E1 and E5 remain unbuilt; the complete actor-input boundary still needs its owning design and implementation. These conceptual closures do not establish credential secrecy, perception accuracy, estimator calibration, scientific fidelity or complete AES conformance.

Scoped dispositions for the shared changes: repository **pass**; open-attempt **pass**; declared-laws **pass**; AI-judge **pass**; estimate-rules **pass**.

Reviewed revision: 05356af5ded4f719d5b4c3878bb7fc91ab6c5008

Verdict: pass
