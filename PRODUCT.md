# World Builder product context

Source: Brian’s approved simulator vision and the accepted decisions in [architecture](docs/architecture/arc42.md); saved-player recommendation in [visual feedback](docs/VISUAL_FEEDBACK.md), approved 2026-11-13: “yes do that”. This file summarizes product use for UI work; architecture, OpenSpec and accepted decisions retain their authority.

## Platform and stack

Web. The existing World Builder uses HTML, CSS and JavaScript with a Python service. The saved-player slice extends that stack, applying selected Astryx layout guidance without adopting its React components. This is an agent implementation choice under the approved scope.

## Users and purpose

Brian and simulation users describe a bounded world, watch people and processes act, and investigate what changed, why, and which information an actor received. Waltzman influence/coordination scenarios are one application of a general-purpose simulator, not the UI’s only domain.

The recurring viewing task is to choose a time and event, inspect its actual effects and causal context, and inspect the relevant actor’s supplied information without losing the selected event. Watching and investigating use the same recording.

## Capabilities and constraints

- Preserve the approved creation flow: one description box and Create simulation; existing live execution remains available.
- A saved recording is read-only evidence. Playback and seeking make no model calls and never alter stored state or resident memory.
- Original wording, interpretation, installed-rule result, later settlement and immediate reactions remain distinct. Preserve visible errors in historical recordings.
- Supplied actor input is evidence of what was supplied, not proof of belief. Actor-only viewing uses declared retained inputs; full-world state and diagnostics belong to Analyst view.
- General semantic accuracy and scientific fidelity are separate from UI correctness. [Modeling choices](docs/model/modeling-choices.md) defines those boundaries.

## Evidence and success

Use retained pump recording `T-e9dYLdIi61` and historical airfield recording `PKVERt8chzt7`, with no fresh simulation. The approved [usability assessment](.impeccable/critique/2026-11-13T20-43-27Z__scripts-world-builder-home-html.md) and its evidence identify the failures.

Success is a readable desktop and phone player with direct temporal control and coherent event context. Demonstrate Bo’s original negative words versus recorded positive assent, then Ari’s parent/child validation steps with their corresponding historical state and actor input. Human comprehension remains Brian’s judgment; passing technical assertions alone do not establish it.
