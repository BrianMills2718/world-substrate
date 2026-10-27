# Vanishing goods and unanswered demand (2026-10-26)

Two live owner builds on the deployed service at `809984e` (#263 knock-on targets, #264 unsourced inputs).
Each folder file is the public share JSON plus the driver log. I read every round of both shares (who tried
what, status, world events), not just the counts.

## Pencil, share `4VmgkXIVWn4p` (12 rounds)

- #264 worked: the factory started with paint, erasers and ferrules, so `make-pencils` was accepted in
  rounds 4, 6 and 9. `sell-pencils` charges the shop's price once for one pencil, and both sides' cash moves.
- No sale happened. `pack-pencils` subtracted one pencil and one box and added nothing, although its rationale
  says it "records one packed pencil". The pencil maker packed each pencil right after making it (rounds 5, 7
  and 11), so `deliver-pencils` never found one and the truck failed every delivery.
- Cause: the world had no field for packed pencils, so the rules writer could not make anything.

## Cafe, share `eFmPomcnsyQq` (8 rounds)

- #263 worked as far as rules go: the world writer gave the objects `on`, `upright` and `broken` fields and a
  laptop in category `fragile`; the rules writer wrote `fallen-fragile-breaks` with timing immediately, plus
  `knock-over` and `drop-object`.
- No knock-on fired in the run: nobody chose to knock anything over (the customer only drank coffee).
  `tests/test_build_quality.py::test_live_cafe_knock_over_breaks_a_fragile_thing_at_once` replays this world
  locally (free) and knocking the laptop over breaks it in the same moment.
- `orders_waiting` rose from 2 to 10: `serve-order` named only the customer, so (in its own words) "the
  waiting-order count and tray are unavailable as participants".

## Change

- `_vanishing_moves`: a move that uses up two or more different things and adds or sets nothing.
- `_unanswered_demand`: a field a process adds to each round that no move ever lowers.
- Either one keeps an attempt from scoring 3 and tells the next attempt and the redesign what to fix.
- On the 7 saved worlds before these (airfield, Waltzman, cafe1, firefighting, garden, pencil c4-run17,
  pencil2), neither check names anything; on these two live worlds each one names exactly the failure above.
- The world writer is told that a step that makes something needs a field for it, and a move that answers a
  waiting need needs a field naming where that need is counted.
