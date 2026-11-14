# World Builder product context

Source: Brian’s current world-workspace request and branching follow-up, 2026-11-13; accepted simulator decisions in [architecture](docs/architecture/arc42.md). This file records the product target for UI work. Architecture, OpenSpec and accepted decisions retain their narrower authority.

## Platform and stack

Web. Extend the existing HTML/CSS/JavaScript and Python service, existing SQLite persistence, native runner and composed Living Scene renderer. Catalog identity is application metadata outside immutable world bundles. No new simulator engine, scheduler, renderer or cognition system.

## Users, purpose and main journey

A person starts at a natural-language world-creation page. Created worlds remain in a durable library. Opening a world leads to its visual/spatial studio, runs and branches. The person can start or continue a run, replay its retained history, or create a new branch from a saved completed round.

The world itself is the primary display. Spatial/visual and causal inspection belong together; the event/state/actor inspector supports the world view. The saved-player slice is an inspection capability inside this larger product, not a replacement for the visual world or home/library workflow.

Waltzman influence/coordination is one application of a general-purpose simulator. Preserve actual represented place membership, object ownership and accepted movement. Screen geometry may be illustrative; it is not evidence of physical distance, collision or walking constraints unless those are represented by the world’s own rules.

## Current implementation scope

- Home retains one description box and Create simulation, with Your worlds below. Successful owner-created worlds are saved durably. The initial catalog is private under existing Owner access; public sharing remains explicit. Guest/IP bookkeeping is not an ownership credential.
- A world definition, logical run, request segment, public share and saved checkpoint have distinct IDs. Existing simulation content IDs are never rewritten to become catalog IDs.
- New run starts the world from its initial state. Continue resumes the current run from its complete saved checkpoint. Replay is read-only and makes no model calls. Branch copies a completed saved round’s material state, actor memory, reviewed rule/ruling identity and applicable continuation state into an independent child run with linked parent history.
- An event projection is not a resumable cognitive checkpoint. Branching is explicitly from the end of a saved round, with the checkpoint state previewed before creation. Parents remain unchanged.
- Recoverable owner logs/public recordings may be imported without inventing missing state, ownership or parentage. Replay-only older recordings show why Continue/Branch is unavailable.
- Original wording, interpretation, mechanical result, later settlements and reactions remain distinct. Actor inputs use actual retained person/round records and do not prove belief. Actor-only viewing hides privileged world/diagnostic content.

## Future features explicitly requested by Brian

Source: Brian’s branching answer, 2026-11-13: start with saved-round branches; document these as future features.

1. **Natural-language interventions at a fork.** For example, ask that Ari tell Bo about the failed sensor. A later design must translate an intervention through installed/reviewed mechanics and retain what was actually done, without rewriting parent history or directly assigning a human’s belief.
2. **Natural-language configuration of starting conditions.** Configure an existing world’s initial conditions through language as a separate reviewed variant, rather than silently editing a recorded run or its world rules. Initial state, agent information and rule/version identity must remain explicit.

Neither feature is implemented or advertised by the current saved-round branching UI. Natural-language creation can already describe a new world; that is distinct from configuring a reusable saved world’s starting conditions.

## Evidence and success

Reuse existing native Kitchen/Castaway/Workshop/Greenhouse examples and retained pump data. The polished [native Coordination Hall](https://brianmills.dev/waltzman/world-substrate) demonstrates existing composed visual capability. The [Replay Studio](https://brianmills.dev/world-builder/play/) is a static example set, not the created-world library.

Success is one continuous workflow: create → find world → open spatial/visual studio → play/replay → preview completed checkpoint → branch → observe independent continuation. Inspect the corresponding action, effects and supplied actor information without losing world/run/time context. Technical checks do not establish human comprehension or scientific model fidelity.

Inhabited facility (2026-11-13): the pump facility example shows rooms, doors, people and delivered reports end to end with place-scoped perception; it is still short of an illustrated Smallville-like place (see the roadmap review).
