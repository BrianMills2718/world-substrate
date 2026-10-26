# Q28: does the S2 glass chain reuse the library's damage and spill processes?

**Answer: no. The rules writer writes its own declared processes; the library stays reference-only.**

Reading (2026-10-26):

- `OverheatDamageProcess` and `VesselFailureSpillProcess` (`src/world_substrate/mechanisms/damage.py:25`, `:116`)
  read the built-in entity slots `entity.condition`, `entity.container`, `entity.liquid` and `entity.thermal`,
  and the spill writes `world.physical_ledger`.
- `build_engine` (`scripts/run_authored_world.py:55-106`) builds every entity of a generated world with only its
  bundle components (generated dataclasses in `entity.components`) plus location, ownership and portable. It never
  sets those built-in slots or a physical ledger, and registers only the compiled mechanics and declared processes.
  So a generated glass cannot carry what the library reads, whatever the bundle names its components.
- Neither library process has `timing`, `due_bindings` or `apply_to`, so neither could run as a knock-on effect.

Free probe (no model call; `probe.out`, run from the repo root): the S2 glass fixture
(`tests/test_open_attempt.py` `GLASS_BUNDLE`, the shape a generated world has) after the push has run its whole
chain. Both library processes report `due` False on the broken glass, `ReactsImmediately` False, the glass has
only its `glass` component, and the world has no physical ledger.

Consequence: the glass chain in S2 is the rules writer's own `timing: "immediately"` processes
(`scripts/generate_causal_model.py`, rule added in S2). Sharing physics between generated and reference worlds would
need the generated path to build those built-in slots; nothing in this plan needs that.
