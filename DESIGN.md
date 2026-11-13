# World Builder saved-player design

Source: Brian’s 2026-11-13 approval of the [viewer recommendations](docs/VISUAL_FEEDBACK.md). Product truth is in [PRODUCT.md](PRODUCT.md); required behavior is in [world-builder-page](openspec/specs/world-builder-page/spec.md). This design extends the existing World Builder identity and applies to saved recordings.

## Surface and visual authority

Mode: operate/read. Preserve the World Builder name, existing neutral dark surfaces, readable sans-serif text, blue/orange/grey status distinctions and styled contextual tooltips. Use words as well as status styling. This is a workflow replacement inside the existing visual system, not a new brand.

## Composition

Lead with the retained scenario description and truthful recorded-run status. The player starts paused. Visible previous/next, round choice and scrub controls make time deliberate.

The working area contains a chronological event list, readable world state and contextual event detail. A desktop layout keeps the event list and explanation together; narrow screens stack readable regions and keep navigation reachable. Use explicit width budgets and a contextual inspector, following the pinned Astryx scaffold/structure/side-panel/responsive references in the [source receipt](evidence/ui/usability-review-20261113/astryx-sources.json).

Select one round and event. Event detail shows original words, interpreted fields and recorded result; reaction children and installed-rule settlements retain separate identities. The primary world state and network are reconstructed through that selected event. The retained scene picture has round granularity and is labelled as the whole selected round, inside advanced inspection.

Actor information stays attached to the selected actor and exact decision round. Present available structured input fields plainly; keep exact input and provenance available deeper. Do not infer missing information, summarize with another model, or equate supplied input with belief. Actor-only mode preserves the existing privacy projection and hides Analyst content.

## Preservation and acceptance

Keep Picture, Network, causal history, the original attempt inspector, exact actor inputs, rules, readout, download and existing creation/live actions reachable. Historical missing data is visibly unavailable. New controls support keyboard focus and styled hover/focus/phone help; use phone-sized targets.

Acceptance is the retained-data task in PRODUCT.md at desktop and phone widths, including direct historical selection from round 6 back to Ari’s round-3 reaction. The world state must become that event’s state; later actions in the same round must not overwrite it. No new simulation, engine, cognition capability or framework migration is part of this slice.
