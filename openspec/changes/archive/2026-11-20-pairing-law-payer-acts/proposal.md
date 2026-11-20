# Proposal: in a generated trade, the one who pays is the one who starts it

Plan size: small

## Why

Issue #282 (live S1 pencil build, `evidence/declared-laws/s1-pencil/`): in buy-logs, buy-graphite, buy-leads and
buy-slats the seller started 19 of 25 accepted trades, moving the buyer's cash without the buyer choosing; in
buy-boxed-pencils the shop (the buyer) was refused "Actor matches mechanic selector" four times because the rules
writer's one actor selector named only the factory. Re-seen in `evidence/declared-laws/s2-pencil/TRACE_READ.md:56-58`.
A pairing law (`laws.py:78-97`) checks the amounts moved but says nothing about who may start the move, and the
interpreter prompt (v1.1, #319) makes seller-started `buy-` moves more common.

## What changes

Fix at the origin, with no engine change and no model call to test:

1. `scripts/scaffold_world.py`: new function `pairing_starter_problems(bundle)` returning one plain sentence per
   pairing law whose `pays.from` is not `"actor"` (the payer must be the one acting).
2. `scripts/generate_world_bundle.py`: after `validate_bundle` in the existing validator-repair loop, raise
   `BundleError` with those sentences, so the designer's next try is told and rewrites the move as the payer's move
   (a sale the seller starts becomes a `buy-...` move with the seller as an `entity_ref`). The designer's `laws`
   contract text says the same.
3. `scripts/generate_causal_model.py`: one `authority_rules` sentence: for a move named by a pairing law, the
   actor selector names the kind of entity that pays, and must not be narrowed to the one who is paid.

`validate_bundle` itself is NOT changed: saved worlds (`tests/fixtures/pencil-s3-kept.json` has seller-started
`sell-boxes` with `pays.from: customer`) must keep loading.

## Out of scope

- Enforcing it in the engine/`laws.py` at commit (would refuse saved worlds and old runs).
- Checking that the rules writer's selector really matches the payer's entities (needs the entity kinds; prompt only).
- The interpreter prompt (#319) and any paid replay; no live run.

## Owner decision assumed

Agreement is modelled as "the payer starts the move" (`pays.from == "actor"`), not as a two-step offer/accept move.
Reason: two-step trades need new engine capability, which AGENTS.md forbids. Undo: delete the call in
`generate_world_bundle.py`.

Source: issue #282 (Brian's issue; the fix is inferred by agent).
