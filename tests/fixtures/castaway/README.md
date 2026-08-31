# Castaway donor fixtures

`freshwater-v0.json` is a compact expected-behavior fixture derived from the pinned Castaway `world-systems` revision. It contains the exact recorded command sequence, selected state checkpoints, conservation/process totals, and replay result needed by the first neutral extraction.

It is scripted evidence with zero model calls. It proves donor behavior, not World Substrate implementation or LLM competence.

Regenerate or verify it with:

```sh
python scripts/extract_castaway_fixture.py
python scripts/extract_castaway_fixture.py --check
```

The extractor verifies donor revision and receipt hash before writing stable JSON.
