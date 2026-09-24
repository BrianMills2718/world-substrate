# Verification boundary

The root `AGENTS.md` applies.

- Derived donor fixtures are immutable expected behavior and must retain revision/hash provenance.
- Regenerate Castaway fixtures only through `scripts/extract_castaway_fixture.py`; never edit expected values by hand.
- Distinguish donor parity, neutral-core correctness, policy behavior, and cross-domain generality.
- Test rule contracts, sources/sinks, timing, atomic rejection, processes, observations, persistence, and replay.
- A scripted fixture does not establish LLM behavior.
