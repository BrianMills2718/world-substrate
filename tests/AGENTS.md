# Verification boundary

The root `AGENTS.md` applies.

- Derived donor fixtures are immutable expected behavior and must retain revision/hash provenance.
- Regenerate Castaway fixtures only through `scripts/extract_castaway_fixture.py`; never edit expected values by hand.
- Distinguish donor parity, neutral-core correctness, policy behavior, and cross-domain generality.
- Test rule contracts, sources/sinks, timing, atomic rejection, processes, observations, persistence, and replay.
- A scripted fixture does not establish LLM behavior.
- Free before paid: before any paid live World Builder run, replay the saved worlds in `tests/fixtures/` that the change could affect, with scripted moves and no AI call, and check the property the run is meant to show. Save each newly built world that a live run judges as a fixture ([lessons](../docs/wiki/lessons.md) 1).
- Prove only what a change could break: a change gets live runs for the behavior it adds and the criteria its code paths touch, plus one fully read live run of the canonical example; saved-run replays are the regression guard, not a full rerun of every past criterion ([lessons](../docs/wiki/lessons.md) 6).
