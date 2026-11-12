---
description: Cold review of the declared-laws planning package, round 3 (pass).
---

# Cold review: declared-laws planning package, round 3

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-28, given the round-1 and round-2 reports.
Reviewed revision: 3e376db030b31925f7a3b9f8c6d8806e06e17b9a (HEAD of plan/declared-laws; subject_revision 9e63749, and only package files, review pages and checks.txt changed since)
Verdict: pass

Rounds 1 and 2 returned revise; their findings are all fixed (history in git for this file and `~/code/.scratch/declared-laws/NOTES.md`).

## Round-2 fixes

- **B1, refusal paths (fixed).** Piece 2, L2 and S2 (`docs/plans/declared_laws.md:157-176, 208, 256`) describe both refusal paths, and they match the code. On the move path, `Engine.apply` calls `_settle` and a refusal goes through `_reject` (`engine.py:762-781`). On the tick path, `Engine.advance` uses `_refuse_round` (`engine.py:864, 871-895`). `_settle` returns `None` today (`engine.py:896`); the plan changes that to a refusal record. A process scope breach still raises `ScopeViolation` (`engine.py:1005-1015`).
- **B2, incident attributions (fixed).** The incident table (`declared_laws.md:98-110`) agrees with the check functions in `scripts/world_builder_service.py`. Every line cite matches: `_unsourced_inputs` :840, `_conjuring_processes` :867, `_missing_components` :943, `_dead_end_stock` :960, `_starved_holders` :1023, `_vanishing_moves` :1114, `_unanswered_demand` :1130, `_second_source_processes` :1143, `_moving_processes` :1178. The saved worlds exist. Q43 and Q45 are consistent with the table. The observation checks are rightly left out.
- **B3, domain concepts (fixed).** `world-design` (implemented, `scripts/generate_world_bundle.py:53`) and `resource` (theory) are in the graph. The edges run correctly: e92 and e93 are "declares" from world-design, e96 runs world-law to gen-rules, and e103 runs rules-review to build. `relies_on` lists 18 concepts.
- **Earlier notes (fixed).** A2 demonstrates the knock-on case and names the model as the laws' author. A7 names its view, a composite-linked-view. Q48 names the decision it changes. The page links `acceptance-criteria.json`. Goal coverage counts 6 of 7 requirements covered, and the seventh is the planning-process requirement.

## Checks rerun

- Validator, `docs/planning/declared-laws/planning-package.json`: exit 1. 8 of 9 parts ok; substance 4 of 6 ok. The only failures are the cold-review verdict and `reviewed_revision`, both filled from this report.
- Validator, `docs/planning/planning-package.json` and `docs/planning/open-attempt/planning-package.json`: exit 1. The only failure in each is the old `reviewed_revision` f8dc6dad. For open-attempt, acceptance is WAIT until 2026-11-08, with 127 citations and 59 implemented concepts, all resolved.
- `md_file_cap.py --repo . --ref HEAD`: exit 0, 156 of 180 files, 0 orphans.
- `scripts/check_trace_reads.py`: exit 0, 20 runs, 0 problems.

## Findings

- **note:** set `reviewed_revision` to 3e376db0 and the verdict to pass in all three manifests (done when this report was saved).
- **note:** the domain map's `knock-on-now` cites `engine.py:884`, which now falls inside `_refuse_round`. `_settle` is at `:896`. The cite still resolves, but it should be re-pointed when S1 edits `engine.py`.
- **note:** the `_settle` refusal record and the new `_refuse_round` arguments are design, not code yet. The plan says so, and the graph marks `world-law` and `law-check` as theory.

Unsure about: the reviewer did not render the page; it read the HTML. It sampled the saved-world paths and did not open every pencil fixture.

Per package, once the fields are filled: declared-laws pass; repository pass; open-attempt pass.

Verdict: pass

## Round 4, 2026-10-28: delta after adoption

Reviewer: `company-planning:planning-compliance-reviewer` subagent. Reviewed revision: 4ff4c274a7a97508fc004c24f2cce6bdae412136. Scope: `git diff 3e376db 4ff4c27`, the adoption through the company-planning gate.

- **Validator:** all three manifests exit 0.
- **Cites:** every new cite matches the code: `_contract` :93, `MAX_REPAIRS` :215, `validate_bundle` :45, `causal_model_schema` :330, `reasoning` :368, `.agentic/repo.yaml:3-11` and `trace.yaml:22, 28, 31`.
- **Route:** reset agrees with the path-decision facts. The receipt hashes match the files on disk, and it records 25 items passed.

Findings, all notes:

- `docs/plans/declared_laws.md:406` still says "see Measurement". The section is now "Evaluation design", so the pointer needs updating at the next plan edit, which re-adopts the plan.
- Keeping the model's reasoning text in the run log is a requirement on the slices, not current behaviour. The plan states it as a requirement.
- "about $2 and two days" for pencil2-pencil14 was not checked against a cited file, and no decision rests on it.

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
