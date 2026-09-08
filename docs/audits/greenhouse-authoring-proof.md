---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Greenhouse fourth-world authoring proof

## Question

After the Automatic replay baseline and World Replay Studio existed, could a
**genuinely new world** be authored end to end — represented state, mechanics,
retained behavior, assets/presentation semantics, zero-review replay, and Studio
entry — without writing world-specific visualization code?

## World

Greenhouse was authored after the replay system and Studio were already fixed.
It contains:

- two gardeners, Nora and Leo;
- one shared watering can;
- one water tap;
- one represented garden bed;
- a dry fern and a dry tomato plant.

Its new causal behavior is `water`: the action names the gardener, watering can,
plant, and garden bed. A successful water commit changes both the can state and
the plant state, so the trace and write-scope boundary retain the full causal
relationship rather than simplifying the action for presentation.

## Retained run

`scripts/run_greenhouse_fixture.py` drives the ordinary engine for seven accepted
commits:

1. Nora takes the can.
2. Nora fills it at the tap.
3. Nora waters the fern.
4. Nora returns the empty can to the shared store.
5. Leo takes it.
6. Leo refills it.
7. Leo waters the tomato plant.

The terminal predicate is derived from represented plant state: every plant is
`watered`. The retained run costs zero, reaches that terminal, and passes exact
engine replay.

## Automatic replay result

The zero-review profile was generated from:

- `reference_worlds/greenhouse/bed-v0.json`;
- `evidence/greenhouse/first-service-v0.json`;
- `reference_worlds/scene-asset-catalog-v0.json`;
- deterministic auto-layout;
- **no Greenhouse scene review overlay**.

It has zero bootstrap TODOs. The shared catalog supplies gardener/can/plant
assets, state appearance, the garden-bed station role, and explicit presentation
semantics for `water`. World semantics do the useful placement work: the can
starts at the water-source anchor, and the two plants are laid out inside the
represented garden bed. The generic renderer/bootstrap source contains no
Greenhouse entity ids.

Real browser checks at turns 1, 3, 4, and 7 showed the shared-can lifecycle, the
plant state changes, the return-to-store handoff, and terminal watering legibly.
The Automatic replay was then added to the World Replay Studio as an
Automatic-only world; no fake Polished variant was created.

## Portability findings

Greenhouse exposed two shared presentation assumptions, both before merge.

**Field-neutral action labels.** Existing generic `take` / `put_down` catalog
rows hard-coded labels using an `item` field, while the substrate's generic
`TakeAction` correctly names its referent `vessel`. The shared declaration now
lets the bootstrapper's trace-inferred field name generate those labels. Kitchen
continues to infer `item`, while Greenhouse infers `vessel`.

**One action can change more than one visual entity.** The first Greenhouse
replay correctly showed a watered plant but left the watering can visually
`filled`, because `water` causally changes both the plant and can while scene
projection previously exposed only one primary `item_field` state update. The
trace/world state was already correct. `scene-profile/v0` now has a generic
`state_effects` declaration for additional explicit entity-state projections.
The shared `water` binding sets the primary plant to `watered` and the explicitly
named `vessel` back to `empty`. Domain-neutral tests reject a state effect whose
action field does not name a known visual entity.

Neither fix adds a Greenhouse branch. One corrected a shared catalog assumption;
the other added a generic declarative primitive because a real fourth world
proved the prior one-entity projection insufficient. Existing worlds do not opt
into `state_effects`, so their retained replay behavior remains unchanged.

## Boundary preserved

The Greenhouse mechanics own watering, ownership and plant state. The retained
trace owns what happened. The presentation catalog owns only appearance and
explicit action projection. Auto-layout owns illustrative coordinates. The
Studio only packages the resulting replay.

No model call, deployment, publication, or world-specific visualization code was
used.

## Meaning

The product sequence that motivated the Studio is now demonstrated end to end:

```text
new represented world
  -> real mechanics + terminal state
  -> retained no-spend run
  -> shared assets/presentation declarations
  -> zero-review Automatic replay
  -> World Replay Studio
```

The next useful step is no longer another generic replay proof. It is a product
choice about how a person should author or import a new world — for example a
form/schema workflow, a code-first starter kit, or another concrete domain. That
choice should be explicit before more framework code is added.
