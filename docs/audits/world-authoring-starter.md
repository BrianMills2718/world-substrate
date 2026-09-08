---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Code-first world authoring starter

## Decision

The product direction is both a code-first starter and a visual/schema builder,
with the starter first so both surfaces share one authoring contract.

## Implemented seam

`world-substrate-authoring-bundle/v0` is the common input. The starter validates
world metadata, custom component schemas, entity/component values, entity
references, action signatures, and presentation declarations. A valid bundle is
scaffolded into a reference-world package with initial state, typed components,
a probe, terminal stub, presentation extension, and typed action envelopes.

The critical boundary is deliberate: generated action **rules always refuse**
and are not registered by the generated probe. A form or action signature cannot
become causal law merely because it is well shaped. Checks, read/write authority,
effects, tests, registration, and a state-derived terminal still require causal
implementation/review.

## Fixture

`examples/world_authoring/orchard-v0.json` exercises:

- two custom components;
- a cross-entity `entity_ref`;
- actor/station/portable entities;
- one action signature;
- presentation assets and a station role.

Tests verify semantic validation, unresolved-reference refusal, generated Python
compilation, initial world loading through the shared engine, action-envelope
round trip, always-refusing rule stubs, overwrite refusal, and presentation-only
catalog output.

## Next

The local visual/schema builder should edit and export this exact bundle. It may
make world structure easier to author, but it must preserve the same causal
boundary rather than adding hidden effects in JavaScript.
