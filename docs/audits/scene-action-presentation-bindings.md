---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Explicit action-presentation bindings

## Question

Can the remaining structural `action_visuals` review be supplied by explicit,
reusable presentation declarations instead of per-world boilerplate—without
letting the bootstrapper guess effects from action names?

## Method

The shared scene asset/presentation catalog gained `action_visual_bindings`.
Each binding is opt-in and names its presentation projection explicitly. The
Workshop bindings declare:

- `pick_up`: take presentation ownership, clear prior station placement, and
  move the actor toward the visual entity named by the inferred item field;
- `attach`: release presentation ownership, set visual state to `attached`, and
  place the item at the station named by the inferred station field.

Bindings may reference `$item_field` and `$station_field`. Those placeholders
are resolved only from action-field structure the bootstrapper already proved
against visual entity/station ids. `complete: true` suppresses the action review
TODO only when every placeholder resolves.

A new generic renderer projection, `actor_target.entity_field`, moves an actor
toward the current visual home/station of an explicitly named entity. It is
presentation-only and contains no Workshop ids.

Negative controls rename an action to a lexical lookalike and verify that no
binding is inferred; a binding with an unresolved placeholder also remains a
TODO.

## Presentation-leak finding

The first combined run exposed a subtle bug: auto-layout initially let a later
`attach` target move loose parts to the frame in the opening scene. The generic
hint rule was tightened so an entity's starting presentation follows only its
**first** relevant action. Later actions cannot leak future placement backward.

## Result

Workshop no longer needs per-world `action_visuals` or `reviewed_actions` in its
polished review overlay. The compiled profile records `attach` and `pick_up` as
explicit catalog-declared bindings.

The polished Workshop review overlay is now **908 compact JSON bytes** against a
**2,645-byte profile core**, a **34.3% manual-review fraction**. The remaining
review is presentation copy/theme, actor accent, a synthetic “parts & tools”
visual grouping, and no causal/mechanical facts.

More importantly, Workshop now also has a retained **zero-review** artifact:

- `evidence/workshop/scene-profile-zero-review-v0.json`
- `evidence/renders/workshop-zero-review-v0.html`

That profile is generated from the world model + real-engine trace + shared
catalog using `--auto-layout`, with **no review overlay**. It has zero bootstrap
TODOs. Auto-layout notices that three explicitly projected items converge on
`frame-a` and proposes a deterministic grid item layout, so the final two legs
and seat remain spatially distinct. The default visual style is intentionally
plain, but the replay is functional and legible.

## Boundary preserved

The catalog binding is presentation authority only. It cannot make an action
valid, mutate the world, alter an event, or introduce a relationship. Unknown
or unresolved action projection stays review-required. No model calls,
deployment, or publication were used.

## Meaning

For Workshop, the functional replay path is now:

```text
world model + retained trace + explicit shared presentation catalog
                         + deterministic auto-layout
                                      |
                                      v
                          complete graphical replay
```

A review overlay is optional polish rather than a prerequisite for generation.
The next useful portability test is to obtain the same zero-review result on a
second real world, preferably Castaway, using explicit bindings for its
materially different `fill`/`drink` actions.
