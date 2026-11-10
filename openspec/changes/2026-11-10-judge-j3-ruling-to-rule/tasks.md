## 1. Install

- [x] 1.1 `scripts/rulings.py`: install a checked rule into the running engine; the effective world (original rules plus installed rulings)
- [x] 1.2 `run_world`: install after the judge confirms (default), settle or route the attempt
- [x] 1.3 Held rulings: pending attempts, joining, Approve and Reject at the next round, language gaps

## 2. Service and page

- [x] 2.1 Setting `judge_rulings` saved with the world; `rulings` and `decisions` sealed run state
- [x] 2.2 Options control, ruling list with Approve and Reject, per-attempt status lines, capitalised judge panel

## 3. Tests, evidence

- [x] 3.1 `tests/test_judge_rulings.py`, service and page tests
- [x] 3.2 Saved runs under `evidence/ai-judge/j3/` with `TRACE_READ.md`; live share links
