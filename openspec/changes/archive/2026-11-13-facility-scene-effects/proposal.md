## Why

The first inhabited-facility slice was judged short of Smallville: reports and refused moves were not visible in the replayed scene, and a resident run (2026-11-13, `evidence/ui/inhabited-facility-20261113/`) found the authored world not usable by an LLM person: people were seen from every room, `open-door` was never offered, and one retry path dropped its controller.

## What changes

- The replayed scene shows a delivered report as a visible message from the sender's room to the recipient's, and a refused move as a banner naming its reason; doors and the pump draw through the existing profile art.
- A declared public action form may list `unobserved_refs` (fields it names without perceiving them) and `not_self` (fields that must not be the actor).
- The facility declares people place-scoped.
- The stale-revision retry for boundary worlds resubmits with its controller.

Source: Brian's 2026-11-13 goal ("make the pump facility feel like an inhabited place a person can watch, replay and branch"); mechanism inferred by agent.
