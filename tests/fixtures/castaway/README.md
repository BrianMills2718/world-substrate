# Castaway donor fixtures

`freshwater-v0.json` is a compact expected-behavior fixture derived from the pinned Castaway `world-systems` revision. It contains the exact recorded command sequence, selected state checkpoints, conservation/process totals, and replay result needed by the first neutral extraction.

It is scripted evidence with zero model calls. It proves donor behavior, not World Substrate implementation or LLM competence.

When the sibling donor repository is available, regenerate or verify it with:

```sh
python scripts/extract_castaway_fixture.py
python scripts/extract_castaway_fixture.py --check
```

The extractor reads the files from the manifest's pinned Git revision and
verifies the receipt hash before writing stable JSON. The donor's current
checkout may advance without invalidating the pin. The repository's default
`python scripts/check_project.py` remains self-contained; use
`python scripts/check_project.py --with-donors` for the optional source audit.
