# Airfield build after the build-quality fixes (2026-10-26)

One owner-allowance build of `evidence/open-attempt/s2-airfield/`'s description ("A small airfield office: a
brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam,
a trainee who has never flown.") against a local service on commit 0acf082, `world_kind: ongoing`. Build only, no
rounds were run, so this folder holds the build record (`airfield-build-record.json`, the /jobs result), not a
`run-log.jsonl`. Cost $0.0175, trace `world-builder-live/world/eaa759fdd3dc45db92c619967dc0832b`, run once.

What came out:

- Three rules attempts. 1: circling, never offered `conduct-training-flight`, `move`, `service-helicopter`.
  2: circling, never offered `conduct-training-flight`. 3: not circling, every move offered, nobody stalled.
  Attempt 3 was kept (`dry_run.never_offered: []`, `moves_at_end` fly, move, service).
- No kept effect is a no-op: the flight adds 1 to `person.flights` and burns fuel; the S2 run's world had
  `fly-training-lesson` adding 0 flights and `drink-water` setting a place to itself (#254).
- **No knock-on process was written in any of the three attempts** (`knock_on_processes: []` each time), even
  with the stronger prompt. The build record now says so ("nothing sets off a knock-on effect"). The world has
  nothing a move knocks over: the glass got `refill-water` only. A generated world sets off a chain only when
  its moves can push, drop or break something, which is the action designer's job
  (`scripts/generate_world_bundle.py`, owned by the model-more lane, #259), not the rules writer's.
