# Reference worlds

Reference worlds prove that the shared substrate supports real end-to-end behavior. They supply content and scenario parameters, not private engines.

## Castaway

**State:** post-drink prefix implemented; whole-vessel transfer remains donor-only.

**Donor:** `../castaway-world-systems` at the pinned revision in `references/sources.json`.

**First vertical:** one persistent clay pot, supported by a separate drinking cup, participates in ownership, carrying, finite liquid transfer, shared finite heating, boiling, evaporation, cooling, damage, pouring, drinking, and transfer between actors.

The registered fill-through-drink consumer path now runs and replays through
the neutral core without Castaway-specific dispatch. Its retained
[first-fill](../evidence/m1/first-fill-v0.json) and
[boiling](../evidence/m1/boiling-v0.json),
[pour](../evidence/m1/pour-v0.json), and
[drink](../evidence/m1/drink-v0.json) evidence match selected semantic donor
checkpoint fields without requiring donor-specific event IDs or state hashes.
The reference world as a whole becomes adopted only when the remaining vertical
runs through the same neutral contracts.

## Later reference worlds

An economic or socio-technical world will be selected after the first vertical. It must reuse the same canonical state, rule, process, affordance, observation, event, and replay seams while adding at least one genuinely new mechanism family.

No later reference world is active yet.
