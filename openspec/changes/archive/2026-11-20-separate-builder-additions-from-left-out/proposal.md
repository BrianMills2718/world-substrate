# Separate what the builder added from what was left out

Fixes BrianMills2718/world-substrate#241.

## Why

The world designer returns one list, `not_modeled`, and the page and build progress show every item under
"Left out of the simulation". When the designer adds something the description does not have to make the world run
(evidence: `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md` finding 3, a doorway added "to give the actors a
passable route around the brick wall"), that addition lands in `not_modeled`, so the page tells the visitor the
opposite of what happened: the doorway is in the world, not left out.

## What changes

- `scripts/generate_world_bundle.py`: the contract gains an optional top-level `added_to_run` (list of short plain
  strings: things the designer added that the description does not state, so the world can run). `not_modeled`'s
  contract text says it is only for parts of the description that could not be represented, and never for anything
  that was added. The redesign message tells the model to return the full `added_to_run` list, keeping earlier
  items that still hold. The field is popped from the model's JSON like `not_modeled` (never stored in the bundle,
  validated as a list of strings, repaired through the existing repair loop). Returned to callers through a new
  optional keyword `added_out: list[str] | None = None`, which the function fills in place; the 3-tuple return and
  every existing caller and test double stay unchanged.
- `scripts/world_builder_service.py`: pass `added_out`, carry the list next to `not_modeled` through the best-try
  tuples, return `"added_to_run"` in the `/generate-world` response and in the world summary (next to
  `not_modeled`, line ~535), and emit a build-progress note "Added to make it run" beside "Left out of the simulation".
- `scripts/world_builder_home.html`: a second disclosure "Added to make it run (k thing(s))" under the existing
  "Left out" one; "Left out" shows only `not_modeled`.
- Spec deltas in `world-builder-page` and `world-authoring-bundle`.

## Out of scope

- The people-world path (`scripts/people_world.py`): its list comes from `spec.unsupported`, which has no
  additions; the response omits `added_to_run` and the page treats missing as empty.
- Reclassifying already-saved worlds or recorded builds (they keep `not_modeled` only; no regex over prose).
- Any judgement of whether an addition was a good idea (the invented instructor, TRACE_READ finding 4).
- Paid or live model calls: all tests use fake LLM replies.

## Owner decision assumed

- Field name `added_to_run`, heading "Added to make it run" (taken from the issue's own suggested wording).
- Additions are listed for transparency only; they do not block a build or need approval (pressing Run is the
  approval, Brian 2026-10-15).

Source: requirement inferred by agent from world-substrate#241 and the 2026-10-26 trace read.
