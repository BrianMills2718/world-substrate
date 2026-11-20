# Offer generated moves whose fields are text

Plan size: small

## Why

In the Waltzman rebuild on deploy dae881b (`evidence/declared-laws/s4-waltzman-5/`, issue #488) the build kept 10
rules, but none of its 9 generated moves (raise a concern, reopen a settled issue, make support conditional, ...) was
ever played in 31 rounds. Residents are listed only the moves declared as public forms, and a people build declared
forms only for its compiled moves; every generated move takes free-text fields, so it got none. Residents were never
told those moves existed, and the reader saw each one only by its kind name.

## What changes

- A public action form may leave its non-referent fields open (`open_fields`); the resident is asked to state them in
  its own words, and the reader fills them from the attempt.
- A people build declares one form per generated move: referent fields bound to the public entities the move's rule
  accepts, text fields open. A move with a referent no public entity fits gets no form.

## Impact

- `scripts/actor_information.py`, `scripts/people_world.py`; test `tests/test_generated_move_forms.py` on the saved
  s4w5 build (`tests/fixtures/waltzman-s4w5-build.json`).
- Residents' move lists grow by about one row per generated move.
