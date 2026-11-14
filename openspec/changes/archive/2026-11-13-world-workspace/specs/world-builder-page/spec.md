## ADDED Requirements

### Requirement: Creation-first world workspace

Source: Brian’s 2026-11-13 request for natural-language creation as the starting page, created worlds, run lifecycle and an actual spatial/visual view; follow-up saved-round-first scope.

The starting page SHALL retain natural-language creation and provide the owner’s durable world library. Opening a world SHALL be read-only and show its initial visual state and available runs without silently creating a run. The studio SHALL provide distinct New run, Continue, Replay and completed-checkpoint Branch actions. Branching SHALL require a visible round-end checkpoint preview rather than silently branching from a different state than the selected mid-round event.

The existing native composed scene SHALL be the primary world presentation, synchronized to world/run/event selection. It SHALL preserve represented place membership, ownership and accepted movement; illustrative screen geometry SHALL NOT claim unmodelled physical constraints. Existing causal, event, actor-input, exact-trace and older visual inspection SHALL remain available as supporting views. Actor-only mode SHALL hide privileged full-world scenes and other Analyst content. A stale asynchronous response SHALL NOT replace the current world/run selection.

#### Scenario: Create and reopen a visual world

- **WHEN** the owner creates a world from the home description box and later opens it from Your worlds
- **THEN** the world’s visual scene and runs are available in the same workspace
- **AND** merely opening it makes no model call and creates no run

#### Scenario: Replay and live continuation are distinct

- **WHEN** the owner selects Replay or Continue for a saved run
- **THEN** Replay reads retained data without a model call
- **AND** Continue explicitly executes the native saved checkpoint under the existing budget and approval controls
- **AND** Pause preserves any completed server checkpoint even when its response arrives after the pause

#### Scenario: Branch uses the shown completed checkpoint

- **GIVEN** a mid-round event is selected
- **WHEN** the owner previews that round’s complete saved checkpoint
- **THEN** the scene and inspector show the checkpoint state before Branch is enabled
- **AND** the resulting branch identifies its parent and fork point

#### Scenario: The visual world remains primary on desktop and phone

- **WHEN** a created world or public recording is opened at desktop or phone width
- **THEN** its native visual/spatial scene is available ahead of the supporting inspector
- **AND** time, event and run controls remain readable and operable without clipped essential labels
- **AND** causal and actor-input inspection retain the same selected context
