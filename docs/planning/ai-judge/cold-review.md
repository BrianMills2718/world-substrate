**Reviewed revision: 31142e0364fa837fbb4a5e4e4168f30eb1631bbb** (branch `feat/judge-j2`, plus the uncommitted changes you described, read in `/home/brian/code2/worktrees/ws-judge-j2`). I changed nothing in the checkout.

## Validator

`validate_planning_package.py --repo . docs/planning/ai-judge/planning-package.json` exits **1**. Groups:
- **Parts:** 6 of 10 ok, 3 failing, 1 pending (investigation, not due).
  - FAIL `open_questions`: "Q89: touches 'mid-run-rule', which is not a domain-model node".
  - FAIL `acceptance`: "A2, A3, A5: entrypoint must be a URL or planned". The part reports 3 not built, 5 built.
  - FAIL `cold_review`: verdict is still `revise` on the old review. This is expected until this review is recorded.
- **Substance:** ok on citations (250 file citations), concepts (65 implemented, 14 dashed), relies_on (28), cost basis (4 AI steps: 1 measured, 3 computed), plain baseline, Brian's stops (0 hold) and the typed-rules model (29 types). Three checks are pending, including "3 stages untested".
- **Coverage:** pending. 13 requirements, 12 covered, 1 about the planning process. A2 to A8 were edited, so they are re-judged tonight.
- **Freshness:** FAIL, expected. Six plan files changed since `a863097`.

## Previous findings

- **B3 (A2 promised the whole chain): fixed.**
  - A2's criterion now says "net changes, every blocker, the chain's length and where it stopped", and the plan matches at lines 105 and 460.
  - A "long line ruling" case was added.
  - `long-line/TRACE_READ.md` shows the judge read 5,001 net changes grouped into two rows, `chain_length` 5000, no blocker, and no chain. The run log holds all the steps.
- **B4 (port world not reproducible): fixed.**
  - The full port description is quoted in A2, A4 and A6, and the demonstration says plainly that a fresh build need not reproduce the strings.
  - A saved run, `port/`, now carries the strings.
  - A8's team world is described in full.
- **B5 (the repository's earlier mid-run game master was missing): fixed in substance.**
  - Q89 is open, cites Decision 007, and the plan now cites the spike at `ai_judge.md:426`.
  - I confirmed the 27 rules: 3 in `waltzman/run` and 24 in `waltzman-spec/run2/run`.
  - A new blocking finding below concerns Q89's graph node.
- **B6 (missing question on R7 versus Concordia's `EventResolution`): fixed.**
  - Q90 is resolved with a reading of the code, and says it is inferred and that Brian may read Decision 006 differently.
  - R7 is reworded at `ai_judge.md:261`.
  - The "no judge prompt of our own" tension is honestly stated.

## Saved runs against A2, A3, A5

The run logs and `TRACE_READ.md` files bear out what the entries say.
- **A2, port:** the judge read the sign-release blocker. Order was propose, rules check, test run (Rosa 0 to 40, Vik 40 to 0, no blocker), then confirm. Nothing was installed.
- **A2, blocked chain:** the judge's review input contained "the truck has fuel", with the chain stopped at step 40.
- **A2, long line:** as under B3 above.
- **A3, empty purse:** the engine refused with "the giver holds that many coins" and there is no judge call. The trace states plainly that residents did not do this unprompted and that it took a bluff brief.
- **A5, port:** Rosa chose to inspect instead of signing, and the coins did not move.
- **A5, sawmill:** the choice went to the logger, and the rule was rewritten as the logger's own move.

Costs match the run logs, for example $0.00302 for the port run.

## Findings

1. **blocking, acceptance, A2/A3/A5 `entrypoint` (`acceptance-criteria.json`).**
   - The entrypoint is the repo path `evidence/ai-judge/j2/` plus a sentence, not a URL. The validator fails on it.
   - There is no run page a non-expert can open for these runs. The steps say "open Vik's offer on the run page" and "open the judge panel", but the saved runs are JSONL folders.
   - A step also names `tests/judge_worlds.py` `port()`, which is code jargon.
   - Fix: serve the three runs as share links or run pages on the deployed builder, like A1's `?run=` URLs, and use those as `entrypoint`. Drop the code path from the steps.

2. **blocking, acceptance, `status_note` on A2/A3/A5.**
   - It says "Built in J2 (merged and live 2026-11-10)". At this revision J2 is a WIP commit on `feat/judge-j2`, which no other branch contains, and the runs were posted to "a local service on the J2 branch".
   - "Live" and "merged" are therefore unsupported, and so are the `entrypoint` words "every new resident run on the World Builder shows the judge panel".
   - Fix: merge and deploy, then record the live URLs. Until then mark A2, A3 and A5 as not built, or say "built on a branch, not deployed".

3. **blocking, open_questions, Q89 (`docs/planning/open-questions.json`).**
   - It touches `mid-run-rule`, which is not a domain node. The validator fails on it.
   - Fix: add the concept to `docs/model/domain.graph.json` and DOMAIN.md with its spike location (`spikes/any-scenario-2026-10/midrun.py`) marked as spike or theory-only, or touch an existing node.

4. **blocking, cold_review (`planning-package.json:374`).**
   - It still records `reviewed_revision` `a863097` with verdict `revise`. This review should be recorded as `31142e0364fa837fbb4a5e4e4168f30eb1631bbb` after findings 1 to 3 are fixed.

5. **non-blocking, A5.**
   - The saved runs show only the refuse branch: Rosa inspected, and the logger's offer was rerouted. The accept branch, where she signs and the coins move, is not shown anywhere.
   - The expected result "coins move only if she signs" is therefore shown only by the coins not moving.
   - A5's demonstration also leans on a JSON file for the sawmill ruling.

6. **non-blocking, A3.** The trace itself says the refusal rests on a bluff brief and one sample. The entry says so, which is acceptable. The expected text matches the rule's check label, not "holds 0 coins".

7. **non-blocking, `sawmill/TRACE_READ.md`.** The confirmed rule moved 3 logs for 1 coin against a world price of 10, and nothing flagged it. The trace marks this for J3, so it should be a ledger or plan item. I did not find one.

8. **non-blocking, port rule.** The judge's `accept-coin-offer` is Rosa's move, whereas the plan and the empty-purse world's hand-installed `hand-coins` rule are the payer's move. The trace notes the mismatch. A4's "second trader's later offer" step may therefore not reproduce through the judge's rule. This is for J3.

## Unsure

- Whether the validator's URL rule for `entrypoint` should accept a repo path for evidence-only runs. I treated it as binding, since the contract says a non-expert must be able to follow the demonstration.
- Whether Q90's reading ("steps are configuration, not our own prompt") is what Brian meant. The entry flags this itself.

Verdict: revise

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
