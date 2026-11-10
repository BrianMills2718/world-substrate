# Trace read

Run: "Long line" (`tests/judge_worlds.py` `long_line()`: 50 lines of 4 crates through 25 stages, so a press of the
start button sets off 5,000 process steps), 2 rounds, policy `resident`, owner allowance, posted by `post_world.py
long-line` to a local service on the J2 branch, 2026-11-10 18:12 UTC. One run-log line, `run-log.jsonl` (2.0 MB because
it holds the full 5,000-step chain in `result.judge_test_runs`); its one llm_client trace id is
`world-builder-live/run/527519ff93a846d69ec2c77d25d603b7`. Measured cost: `cost_usd` 0.01529601, matching the 6
`llm_calls` rows (2 interpreter, 2 resident, 2 judge). `earlier-tries.jsonl` holds the first try (trace e7063c8a,
$0.0205), which hallucinated a limit and revised a no-op before confirming; the prompt was corrected after it.

I read both rounds, the pass 1 record, the judge record, the run's `judge_test_runs` and both judge calls (llm_calls
ids 9675765 propose, 9675766 review) in full: the documents are 124,850 and 129,177 characters, about 46,000 and 48,000
tokens each, of which the world is about 123,000 characters.

## Findings

- **B3's long-chain case holds.** The proposed `press-button` rule passed the rules check and its test run settled with
  `chain_length: 5000`, no blocker, `stopping_point` kind `settled` after step 5000. The review call (9675766) was
  given 5,001 net changes as two grouped rows (the button's `pressed`, 1 change; and one row naming 200 crate-stage things
and their fields, 5,000 changes) with `net_change_count` 5001, and no chain; the run log holds every step. The judge's `why` says "settled
  with no blockers after 5,000 process steps". So the judge read the net changes and the blockers, and the page and run
  log hold the steps.
- **Cost of a long chain is the world, not the report.** Each judge call is about 47,000 input tokens ($0.0047) because
  the whole world is read; the report adds about 4,300 characters. The run cost $0.0153, 62 percent of it the judge.
- **The first round shows the problem the judge was built for.** Sam dusted the button (the only installed move, r1-
  e00001) and then said he would press it: no move presses it, so the judge was asked.

## Round 1

- Sam (`sam`) tried `dust-button` on the button: accepted, r1-e00001.

## Round 2

- Sam (`sam`) tried "I press the start button.": no rule covers it, recorded `unsupported_action`, r2-e00002; pass 1
  recorded; the judge ruled: confirmed `press-button`, 5,000 steps settled, `whose_choice` none.
