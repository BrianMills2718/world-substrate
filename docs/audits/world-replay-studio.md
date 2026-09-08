---
role: audit
status: active
reviewed_through: 2026-09-07
---

# World Replay Studio product surface

## Question

Can the retained graphical replay system become a usable local product surface
without introducing a server, changing simulation truth, or turning polished
scene choices into mandatory world-authoring work?

## Implementation

`evidence/renders/world-replay-studio-v0.html` is one standalone browser file.
It packages the existing replay documents byte-for-byte and provides a product
shell around them:

- Kitchen, Castaway, and Workshop world navigation;
- Automatic vs Polished variant switching;
- existing replay playback/step controls inside the embedded document;
- an "open replay alone" action;
- retained trace/profile metadata as a secondary disclosure;
- optional `?world=<id>&variant=<id>` initial selection.

`scripts/render_replay_studio.py` is domain-neutral. The declarative
`evidence/replay-studio-v0.json` manifest says which retained replay variants
belong to a world. Actor/action/turn/model/bootstrap metadata is read from the
retained zero-review profile and trace instead of copied into product code.

The six embedded replay documents are base64-packaged only for standalone
portability. Tests decode each one and compare it byte-for-byte with the retained
artifact.

## Product boundary

The **Automatic** variant is the authoring baseline: world model + retained
trace + explicit shared presentation catalog + deterministic auto-layout. A
per-world review overlay is not required for a functional replay.

The **Polished** variant is optional product presentation. It may improve scene
composition, emphasis, copy, or art direction, but it does not own causal truth
and is not required to create a new world.

The Studio itself has no simulation authority. It does not run mechanics, alter
traces, infer new relationships, or write canonical state. It only packages and
navigates retained replay artifacts.

## Verification

Focused tests cover manifest validation, retained metadata, byte-exact replay
embedding, deterministic single-file regeneration, and domain isolation in the
Studio renderer. Real Chrome renders were inspected for polished Kitchen and
automatic Kitchen/Castaway/Workshop at a laptop-scale viewport.

## Next product proof

Do not add more generic replay machinery just because the Studio exists. The
next useful test is the user workflow on a fourth genuinely new world: author the
world model/mechanics/relationships/assets, retain a no-spend run, and obtain a
watchable Automatic replay without writing visualization code. Only a concrete
failure in that flow should reopen generic replay architecture.

Deployment and publication remain separate authority boundaries.
