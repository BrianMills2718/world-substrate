## Why

When a person tries something no installed rule covers, the AI judge (Concordia's game master) must rule on it from
what the engine already computes, not from its own guess at the consequences. Brian, 2026-11-09: "deliver the
results of that propagation to the judge". An attempt no rule covers commits no event, and knock-on effects start
only from a committed event, so that report comes in two passes (`docs/plans/ai_judge.md`, Canonical example;
ledger Q78). Slice J1 of the AI judge plan, approved for building by Brian on 2026-11-10 ("yes if ti si planned out
and you have no quesitons for me").

## What Changes

- New capability `ai-judge`, its first part: the consequence report (`scripts/consequence_report.py`).
- Pass 1: for an unmatched attempt, the moves (available and blocked, with every check and its values) of the
  person acting and of each person the attempt names, and the current values of the person acting and everything
  named. Each run records pass 1 with each unmatched attempt (`consequence.pass_one` on the attempt's round row).
- The attempt interpreter's reading lists what the attempt's words name (`names`, prompt version 1.3), and an
  unmatched reading keeps that list, filtered to the world; a reply recorded before `names` existed names only the
  person it asks.
- Pass 2: a proposed rule, written in the declaration language every World Builder rule uses, goes through the
  same rules check a build's rules go through, then is test-run on a copy of the world as it is now. It reports the
  net changes, the blockers, the chain's length and where it stopped, and keeps the full chain; the summary a judge
  reads drops the chain. A rule the check rejects is reported with the check's error and is not run.
- No judge yet (J2), and nothing is installed (J3).

## Impact

- Code: `scripts/consequence_report.py` (new), `src/world_substrate/attempt.py`, `prompts/attempt_interpreter.yaml`,
  `scripts/run_authored_world.py`.
- Tests: `tests/test_consequence_report.py`, `tests/judge_worlds.py` (new), `tests/test_open_attempt.py`.
- Docs: `docs/model/ODD.md`, `docs/model/METAMODEL.md`, `docs/model/world_substrate_model.toml`,
  `docs/architecture/arc42.md`, the AI judge planning package.
