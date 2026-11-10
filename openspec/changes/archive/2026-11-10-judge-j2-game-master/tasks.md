## 1. The judge

- [x] 1.1 `scripts/judge.py`: Concordia `EventResolution` on stock parts; world and consequence report as context
- [x] 1.2 Propose, pass 2, review, one revision, language gap; whose choice
- [x] 1.3 Long test runs read grouped (`consequence_report.summary`)

## 2. In a run

- [x] 2.1 `run_world(judge=True)`: rule on each unmatched attempt after the round's moves; record, do not install
- [x] 2.2 Service: judge on for the resident policy; full test runs in the run log, summaries on the page
- [x] 2.3 Run page judge panel (what it was given, ruling, rule, test run, answer; "decided by rule, judge not asked")

## 3. Tests, evidence

- [x] 3.1 `tests/test_judge.py` (17 tests, every model call faked)
- [x] 3.2 Saved runs under `evidence/ai-judge/j2/` with `TRACE_READ.md`: port, blocked chain, long line, empty purse, sawmill
