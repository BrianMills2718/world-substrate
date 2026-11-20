# Tasks

- [x] Test first: `InputBudgetTests` in `tests/test_judge.py`. On PR #478's head the leading-text test failed (the
      system message named the person); the budget test passed there (77,659 characters, under the 84,000 limit).
      This change brings the prompt to 44,067 characters and makes its leading part the same on every call.
- [x] `consequence_report.pass_one_reading`: failed checks by label, at most three examples
- [x] `judge.world_text`: things by id, label and kinds; no values, no revision
- [x] `prompts/judge_steps.yaml`: fixed system message; person and step last
- [x] Update the older judge and pass-1 tests to the new reading
