## Why

Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C: one whole-system graph layer, shown alone for a world with no map such as Waltzman and, later, over the room map), after "on cybernetic v3 there was this large graph that represented eveyrthign in the system. and i am saying thatwhole thing as an overlay over the spatial structure". The World Builder's Network panel already draws such a graph, but for the Waltzman rebuild the whole-world view is 70 boxes and 411 links in a small tangle (checked live on share jyVbywXT8N8F, 2026-11-14) and the "this round" view shows 5 boxes.

## What Changes

- `scripts/world_graph.py` builds the graph (a port of the Network's `worldNetwork`) and what each round lit in it.
- `GET /share/<id>/graph` returns it for any shared run, with labels and statuses only (no message words).
- `viewer/smallville/graph.html`: three columns (who acts, moves the rules allow, things), every box always there, the chosen round's tries lit blue (allowed), orange (refused, with the reason) or grey (no move); links drawn only for the round or the clicked box.
