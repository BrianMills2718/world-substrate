---
role: audit
status: active
reviewed_through: 2026-09-09
---

# Living Scene information and outcome feedback gate

## Question

Can a living scene visibly show represented information delivery and action
outcomes while preserving canonical visibility, evidence, and causal boundaries?

## Implementation

The Living Scene logical-frame layer now resolves two exact declared presentation
operations:

- `information.transmit` resolves an explicit delivery entity or a delivery among
  entities changed by the retained canonical event; and
- `action.feedback` exposes only the retained event status plus failed check labels.

The generic renderer draws source-to-recipient transmission lines and a message
bubble, then clears and reconstructs those effects on every frame. It renders
action feedback as a scene-level status cue. No model call creates explanatory
copy.

## Privacy boundary

The prior logical frame included the full retained event object. Waltzman events
can contain actor-scoped observations, so that shape was too broad for a public
scene payload. The frame now retains only presentation-safe event metadata. Raw
observations, state changes, and information-context content remain in retained
evidence, not the public living-scene JSON.

Direct/private information content is omitted unless the requested observer is
the represented source/authorized delivered recipient under the existing
information visibility rules. Public information remains visible after activation.
The source/recipient/channel transmission fact can still be presented without
exposing hidden content.

## Causal boundary

Information transmission and information context are not causal ancestry. Tests
verify that a delivered message can be presented while no
`causal_parent_event_ids` are created. Existing parent ids, when present in the
retained event, remain separate metadata.

## Domain-neutral evidence

The retained information fixture uses two neutral actors, one direct/private
message, one delivery, and a synthetic rejected action. Browser evidence is:

- `evidence/renders/living-scene-information-v1.html`;
- `evidence/renders/living-scene-information-v1-message.png`; and
- `evidence/renders/living-scene-information-v1-rejected.png`.

The message screenshot is rendered for the authorized recipient. Its payload
contains literal `<b>` text to prove message content is assigned with DOM
`textContent`, not injected as markup. The rejected-action screenshot displays
the retained failed-check label without relying on an event log.

## Boundary

This gate does not establish Waltzman composition or M1 product acceptance. It
only proves reusable information/outcome primitives for downstream profile work.
