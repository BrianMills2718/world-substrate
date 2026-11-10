## Why

A judge ruling that is only recorded decides nothing: the next person to try the same thing is ruled on again, and
nothing in the world changes. Slice J3 of the AI judge plan (`docs/plans/ai_judge.md`, Decided 3 and 5) turns a
confirmed ruling into a rule the engine enforces for everyone, with a per-world setting that either installs it at
once (default) or holds it, with the attempts that wait on it, until the owner approves. Approved for building by Brian
on 2026-11-10 ("yes if ti si planned out and you have no quesitons for me").

## What Changes

- A confirmed ruling that passed the rules check and the test run is installed into the running engine
  (`scripts/rulings.py`, `run_world(judge_rulings="create")`, the default); the attempt then settles through the rule,
  or, when it needs another person's choice, reaches that person, whose page now offers the move. Later attempts the
  rule covers are decided by it with no judge call.
- The world's new setting "Judge rulings during a run" (Options on the Create page, saved with the world like
  "Simulate as"): "Approved by Create" (default) or "Wait for my approval". In wait mode the rule is held, nothing is
  installed, the attempt and every later attempt read as the held rule wait as pending, and the run page lists the
  ruling with Approve and Reject. Approve installs the rule and settles each waiting attempt; Reject refuses each,
  naming the ruling.
- A ruling the declaration language cannot express (rules check rejects it and its one revision) is refused with
  "no rule could express this" and listed as a language gap.
- The run page lists every ruling with its state; the installed rules travel with the run as sealed state, so the
  world's own rules (the shared run's fingerprint) are unchanged.
- The judge panel's first sentence is capitalised.

## Impact

- Code: `scripts/rulings.py` (new), `scripts/run_authored_world.py`, `scripts/world_builder_service.py`,
  `scripts/world_builder_home.html`, `scripts/judge.py` (wording only).
- Tests: `tests/test_judge_rulings.py` (new), `tests/test_world_builder_service.py`, `tests/test_world_builder_home.py`,
  `tests/judge_worlds.py`.
- Evidence: `evidence/ai-judge/j3/` (port with two traders: default, wait then approve, wait then reject; price times
  quantity), each with `TRACE_READ.md`; live share links after deploy.
