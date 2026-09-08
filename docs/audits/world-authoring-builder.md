---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Visual/schema world authoring builder

## Product decision

The user selected both authoring paths: code-first starter and visual/schema
builder. The starter landed first so the builder could target an existing,
tested authoring contract rather than create a second representation.

## Surface

`evidence/renders/world-builder-v0.html` is a standalone local browser artifact.
It embeds the Orchard example and edits `world-substrate-authoring-bundle/v0`
through six sections:

1. world identity and location;
2. typed custom components;
3. represented entities and component values;
4. action signatures;
5. presentation assets/bindings/roles;
6. review and export.

It supports importing bundle JSON, live validation, JSON preview, bundle download,
copying JSON, and copying the code-first scaffold command. It has no external
runtime dependency or server requirement.

## Shared validation

`scripts/world_builder_core.js` is a pure validation core usable from Node or the
browser. Tests run the Orchard bundle and several invalid mutations through both
the JavaScript core and `scripts/scaffold_world.py`; their valid/invalid result
agrees for unresolved entity references, invalid presentation asset bindings,
reserved action fields, and bad typed defaults.

The generated HTML embeds the exact Orchard starter bundle and regenerates
byte-for-byte from `scripts/render_world_builder.py`.

## Authority boundary

The builder does not expose causal effect editing. An action row describes only
an intent signature. The UI states that explicitly, and the exported bundle
still causes the code-first starter to generate an unregistered, always-refusing
rule stub.

This is a product constraint rather than a missing feature to silently work
around. A future causal-mechanic editor would need an explicit authority design
and should reuse the existing reviewable mechanic declarations where possible.

## Visual check

Real Chrome renders were inspected for the World and Action Signatures sections
at a 1600×1100 viewport. The causal-boundary warning, live valid-bundle state,
JSON preview, and export affordances are legible as a local product surface.

## Next boundary

The two requested authoring surfaces now exist over one contract. The next useful
gate is human use of the builder → exported bundle → starter scaffold handoff.
Do not add hidden causal authoring to the browser merely to make the flow appear
more complete.
