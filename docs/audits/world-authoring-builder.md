---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Visual/schema world authoring builder

## Product decision

The user selected both authoring paths: code-first starter and visual/schema
builder. The starter landed first so the builder could target an existing,
tested authoring contract rather than create a second representation. The later
product correction was equally explicit: ordinary use should not require a
bundle download just to run a world.

## Surface

`evidence/renders/world-builder-v0.html` edits
`world-substrate-authoring-bundle/v0` through eight sections:

1. world identity and location;
2. typed custom components;
3. represented entities and component values;
4. action signatures;
5. causal mechanics generation/review/approval;
6. presentation assets/bindings/roles;
7. fresh scripted or LLM-selected run with an in-page graphical replay;
8. optional review/export for the code-first handoff.

The structural form remains a standalone HTML artifact. Live mechanics and fresh
runs use the same-origin World Builder API when the artifact is served at
`brianmills.dev/world-builder/`; opening the file directly still supports
structural authoring and export without a server.

## Shared validation

`scripts/world_builder_core.js` is a pure validation core usable from Node or the
browser. Tests run the Orchard bundle and invalid mutations through both the
JavaScript core and `scripts/scaffold_world.py`; their valid/invalid result
agrees for unresolved entity references, invalid presentation asset bindings,
reserved action fields, and bad typed defaults.

The generated HTML embeds the exact Orchard starter bundle and regenerates
byte-for-byte from `scripts/render_world_builder.py`.

## Causal boundary

Action rows remain **signatures only**. Causal mechanics are a separate
`world-substrate-causal-model/v0` proposal. The browser may request a bounded LLM
proposal and show the compiler-derived reads/writes, checks, effects, limits,
tests and terminal, but it cannot install raw prose or Python.

A generated declaration must pass the local causal compiler and installer, and
the user must press **Approve mechanics for run**. Editing the represented world
after generation marks the mechanics stale and revokes approval. Fresh policy
selection then chooses only from actions the engine actually offers.

See [action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md)
and the [live authoring audit](live-world-authoring.md).

## Visual checks

Real Chrome renders were inspected at a 1600×1100 viewport for the original
World/Action Signatures surface and again for the new Causal Mechanics and Run
sections. The compiler-governance warning, optional mechanic guidance, disabled
pre-approval Run control, JSON preview, and optional export affordances are
legible at laptop scale.

A generated fresh Orchard replay was also rendered in Chrome. The first smoke
found that in-memory bootstrapped profiles skipped the actor carry defaults used
by the file loader; the generic fresh-run path now normalizes those defaults.
The final frame places Ava at the tree with the picked apple visibly carried,
derived from the mechanic's ownership effect rather than the word `pick`.

## Current boundary

The browser can now stay in one product flow from represented structure through
reviewed mechanics to a fresh graphical run. The next useful gate is human use:
try a world whose causal intent is less trivial than Orchard and judge whether
the generated review is understandable and whether the constrained declaration
language is expressive enough. A concrete failure should drive the next
language/UI extension; arbitrary code generation should not.
