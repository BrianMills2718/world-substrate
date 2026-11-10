# Trace read: wind chain under the old limit of 32 (J0, acceptance A7)

Run: World Builder `/run`, scripted policy, 1 round, `tests/knock_on_worlds.py` `wind_chain(40)`, made with the
code on origin/main `43663e9` before J0 (a separate local service on port 8892), so the run record has no
`reaction_limit` key: it ran under the old cap of 32. Saved by `agent:j0-evidence`. Run log line read whole.

Trace id: `world-builder-live/run/63c0b19249a045cbbb055bdbe864fd47`. Scripted, no model call: no llm_client
call under this id; cost 0.0 (measured, run log `cost_usd`).

## Findings

- Under the old cap the wind's knock-on (40 dominoes) was refused whole: `r1-e00002`, status `reaction_limit`,
  rule `wind-topples-the-first`, check "Knock-on effects settle within 32 reactions" failed (actual "more than 32"),
  `changes: []`, `hash_before == hash_after`. Nothing changed.
- With J0 the record carries no `reaction_limit`, so `recorded_reaction_limit` reads it as 32 and replay runs under
  32: the test `a-run-saved-under-the-old-limit-replays-under-it` replays this world's commands and gets the same
  refusal and the same hash.
- Before J0 the run page showed this refused world change as an ordinary change. J0's share marks it refused, and
  the page (run-page.png, opened as a shared run on the J0 service) reads "refused: knock-on effects did not settle
  within 32 steps (the limit this run ran under). Nothing changed."
- The refusal shows on the round's "By itself" sentence (the world's own rule), not on an actor's square, since Sam's
  pull was accepted.

## Round 1

Sam (`sam`) pulled the lever (`r1-e00001`, `pull-lever`, accepted; the lever is not linked to the row, so nothing followed
from it). Then the world's each-round rule fired: the wind tried to topple `w1` (`r1-e00002`), and the knock-on that
would follow (39 more falls) exceeded 32, so the engine refused the whole step and nothing changed. 2 engine events.
