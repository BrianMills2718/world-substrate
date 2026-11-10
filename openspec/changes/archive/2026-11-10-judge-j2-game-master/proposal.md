## Why

When a person tries something no installed rule covers, the AI judge must rule on it from what the engine computes,
as Concordia's own game master (Decision 006), and send another person's choice to that person (Decided 4).
Slice J2 of the AI judge plan (`docs/plans/ai_judge.md`), building on J1's consequence report; approved for building
by Brian on 2026-11-10 ("yes if ti si planned out and you have no quesitons for me").

## What Changes

- New `scripts/judge.py`: Concordia's `EventResolution` game master component, on an entity built from Concordia's
  stock parts, resolves each unmatched attempt as the putative event, conditioned on the whole world and the
  consequence report. Our part is the resolution steps (`prompts/judge_steps.yaml`), each a typed question.
- The judge proposes a rule in the World Builder's own declaration language, reads pass 2 (the rules check and a test
  run on a copy of the world) and confirms, revises once or withdraws; a rule the check rejects twice is a language gap.
- A ruling that needs another person's choice names them; the attempt goes to them as their decision.
- Each run rules on every unmatched attempt after the round's moves (`run_world(judge=True)`, on for the resident
  policy), records the ruling and keeps the full test run in the run log; the run page gets a judge panel.
- A ruling is recorded, not installed (J3).

## Impact

- Code: `scripts/judge.py`, `prompts/judge_steps.yaml`, `scripts/consequence_report.py` (grouped long test runs),
  `scripts/run_authored_world.py`, `scripts/world_builder_service.py`, `scripts/world_builder_home.html`.
- Tests: `tests/test_judge.py`, `tests/judge_worlds.py`.
- Evidence: `evidence/ai-judge/j2/` (port, blocked chain, long line, empty purse, sawmill), each with `TRACE_READ.md`.
