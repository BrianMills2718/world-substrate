# World Builder workspace design

Source: Brian’s 2026-11-13 request for a creation-first home, persistent worlds, play/replay/branching and an actual spatial view; confirmed saved-round-first branching. Product truth is in [PRODUCT.md](PRODUCT.md); required behavior is in OpenSpec. This supersedes the inspection-first composition of the initial saved-player slice while preserving its useful controls.

## Home

One natural-language description box and Create simulation remain the starting action. Your worlds appears beneath it, with readable names, run availability and direct open actions. Private library access uses existing Owner access; no public list of visitor prompts. Search and empty/auth/error states say what is actually available. Example replays are labelled examples, separate from created worlds.

## World studio

The main region is the composed visual world: people, places, objects and represented movement. Reuse native Living Scene projections, profiles/layout and project-owned assets, including the existing Coordination Hall lineage. The generic older role-grid picture remains an additional historical view, not the primary replacement for this scene.

Scene, timeline, selected action and inspector share world/run/event identity. Selecting an earlier event reconstructs that event’s represented state and updates the scene. Delayed scene/run responses must not replace a later selection. Screen coordinates derived for display are labelled schematic; actual location/ownership fields remain authoritative.

Time controls remain reachable. Run controls explicitly distinguish New run, Continue, Replay and Branch from this checkpoint. The run list records parent and fork checkpoint; branch prefixes are preserved. A selected mid-round event is not the same as the completed-round checkpoint: preview/select round end before enabling Branch. Old replay-only recordings explain missing continuation data.

The event inspector shows original words, interpretation and actual effects, including separate reactions and ruling settlements. Actor input remains exact-person/decision-round evidence, deeper than the scene and concise outcome. Actor-only projection hides full-world scenes and other privileged Analyst data. Exact trace, full graph, rules and existing inspection remain available.

## Visual and responsive system

Inherit World Builder’s neutral dark controls, readable type, blue/orange/grey status labels and styled contextual help. The scene can use its established project assets and background; never make meaning depend on colour alone. No React migration is required. On phones the scene remains usable above a compact event selector and contextual detail, with explicit layout/zoom/full-view affordances rather than overlapping speech panels.

## Acceptance and limits

Use actual retained native data for scene/projection checks and a controlled persistent HTTP catalog for creation/resume/branch integration. Verify no mutation on merely opening a world, durable save acknowledgement, stale checkpoint rejection, parent immutability, exact state/memory restoration, and clear inability to branch from an incomplete historical recording. New simulations are unnecessary for renderer/catalog mechanics; any native model call must follow the existing free-first and budget rules.

Natural-language interventions and starting-condition configuration are future features. There are no enabled controls implying those capabilities in this implementation.

Inhabited worlds: a place-scoped entity is perceived only from its place; delivered reports, global knowledge and memories are separate from what a person physically sees. The scene shows each person’s recorded place and each door’s recorded state; room layout stays illustrative (topology, not coordinates).
