# world-authoring-bundle Specification

## Purpose

The shared description of represented world structure (`world-substrate-authoring-bundle/v0`): entities, typed properties, starting relations, action signatures and presentation intent, with no executable consequence authority.

**World authoring bundle v0** (folded on 2026-11-09 from `docs/contracts/world-authoring-bundle-v0.md`, status `implemented`, reviewed through 2026-09-07, last commit `807053e`):

`world-substrate-authoring-bundle/v0` is the shared input between the implemented code-first
starter kit and the implemented local visual world builder (`evidence/renders/world-builder-v0.html`). It describes **represented world
structure and authoring intent**, not executable consequence authority.

## Requirements

### Requirement: What the bundle owns

A bundle may declare:

- world identity, label, summary, shared location, and content version;
- typed custom component schemas;
- initial entities, categories, built-in portability/ownership, and component values;
- action **signatures**: action kind, human description, and typed fields;
- presentation assets, category-to-asset bindings, and station roles.

The structural JSON Schema is retained at
`schemas/world-authoring-bundle-v0.schema.json`. `scripts/scaffold_world.py`
performs the stronger semantic checks that JSON Schema cannot express, including
component/value agreement and entity-reference resolution.

Source: inferred by agent (world authoring bundle v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded)

### Requirement: Causal boundary

An action signature is not a mechanic. The code-first starter still generates a
rule stub whose discovery is empty and whose checks always refuse. The live
World Builder may now ask a model to propose a **separate**
`world-substrate-causal-model/v0`, but that proposal is not part of this bundle
and does not execute directly.

The causal declaration is compiled under
[action mechanic declaration v0](../causal-model-authoring/spec.md): participants
and state paths are checked, read/write authority is derived locally rather than
accepted from the proposer, a mechanic profile is installed/frozen, and the UI
requires explicit approval before a fresh run. Hand-written mechanics remain the
escape hatch when the constrained declaration language is insufficient.

This preserves the project invariant that natural language, a form field, a
well-shaped action envelope, or raw model output cannot acquire consequence
authority merely by existing.

Source: inferred by agent (world authoring bundle v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded)

### Requirement: Generated package

Given a valid bundle, `scripts/scaffold_world.py` writes one Python package with:

- `authoring-v0.json` — the exact authoring input;
- `<world>-v0.json` — reference-world initial state;
- `components.py` — registered typed custom component dataclasses;
- `mechanics.py` — typed action envelopes plus refusing rule stubs;
- `probe.py` — initial-state loader using the shared substrate and an empty registry;
- `terminal.py` — a deliberately incomplete state-derived terminal stub;
- `scene-catalog-extension-v0.json` — presentation declarations for review;
- `README.md` — the remaining causal implementation checklist.

The command refuses to overwrite an existing world directory.

Source: inferred by agent (world authoring bundle v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded)

### Requirement: Supported v0 types

Component fields support `string`, `integer`, `number`, `boolean`,
`string_list`, `entity_ref`, and `entity_ref_or_null`. Action fields support the
same scalar set except lists and null references. Entity references are checked
against the bundle's entity set.

This is intentionally narrower than arbitrary Python. Expanding it should be
justified by a real authoring need rather than by schema completeness.

Source: inferred by agent (world authoring bundle v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded)

### Requirement: Declared resources and laws (current code)

A bundle may declare its own world's `resources` and `laws` (declared-laws plan, slice S1); `_validate_laws` in `scripts/scaffold_world.py:45-93` validates them, and a bundle without them is unchanged. A world that declares its places as entities must start everything in one of them; saved worlds that name places as plain words keep loading (`scaffold_world.py:151-161`).

Source: declared-laws plan, Brian, 2026-10-28: "yes" and "i approve" (`docs/plans/declared_laws.md`); code read on 2026-11-09
