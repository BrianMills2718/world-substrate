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

- Kitchen, Castaway, Workshop, and Greenhouse world navigation;
- Automatic vs Polished variant switching;
- existing replay playback/step controls inside the embedded document;
- an "open replay alone" action;
- retained trace/profile metadata as a secondary disclosure;
- optional `?world=<id>&variant=<id>` initial selection.

`scripts/render_replay_studio.py` is domain-neutral. The declarative
`evidence/replay-studio-v0.json` manifest says which retained replay variants
belong to a world. Actor/action/turn/model/bootstrap metadata is read from the
retained zero-review profile and trace instead of copied into product code.

The seven embedded replay documents are base64-packaged only for standalone
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
automatic Kitchen/Castaway/Workshop at a laptop-scale viewport; Greenhouse was later inspected both standalone and inside the Studio.

## Fourth-world product proof

The next proof was completed with Greenhouse after this Studio existed. It added
real `take` / `fill` / `water` / `put_down` mechanics, a represented garden bed,
a shared watering-can handoff, a retained zero-spend engine run, and a
zero-review Automatic replay. No world-specific visualization code was added.
The Studio now includes Greenhouse as an Automatic-only world; no Polished
variant is fabricated where none has been authored.

See [the Greenhouse authoring proof](greenhouse-authoring-proof.md).

## Current boundary

The baseline product workflow is demonstrated. Further replay/Studio framework
work should wait for an explicit world-authoring product choice or a concrete
failure from a real user/domain. Deployment and publication remain separate
authority boundaries.
