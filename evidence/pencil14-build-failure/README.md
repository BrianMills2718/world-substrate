# pencil14: build failed before the run

A live World Builder build of the pencil description at `5d6a48e` (#278), 2026-10-28, driven in a browser as a
visitor. The rules writer passed its test run after two rewrites and a redesign, then the next rules failed to
install: the page received a 422 and showed "mechanic installer rejected shipment-arrival: malformed_path" at 286.9 s
(`driver.log` here, lines 16-17). Job `f0b6d1a3dc0a40848456e6fe2ce172c0`, trace
`world-builder-live/world/62e3ca0e18c64b75bae1b696f0f29f97` on the service. No world was built, so no round ran.

`malformed_path` is the installer's refusal of a field path it cannot read (`src/world_substrate/profile.py:157`);
it is a correct refusal of raw path authoring, not a bookkeeping law. Used as the baseline in
`docs/plans/declared_laws.md` (Project outcome, Incidents).
