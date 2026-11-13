## ADDED Requirements

### Requirement: Saved recording player

Source: Brian, 2026-11-13, “yes do that”, approving the usability recommendations in docs/VISUAL_FEEDBACK.md; event-level reconstruction detail inferred from retained round-3 counterexample under that approval.

A saved run SHALL open paused with its retained scenario description and visible previous/next, direct round and scrub controls. Playback SHALL advance every retained event in recorded order within a round before advancing to the next round; reaching the final round alone SHALL NOT skip its remaining events or mark them finished. One selected event SHALL coordinate the readable event list, recorded attempt/result detail and primary world state/network. Selecting historical evidence SHALL select its historical event and reconstruct represented state through that event from retained initial entities and ordered changes, without applying later events. Reaction children and installed-rule settlements SHALL retain their own event identity. A whole-round retained picture SHALL remain available with its coarser temporal scope explicit.

Actor input SHALL be matched to the selected person and exact decision round using declared retained records only. Missing data SHALL remain visibly unavailable. Supplied input SHALL NOT be presented as proof of belief. Actor-only mode SHALL hide Analyst world state, attempts, causal diagnostics and other people’s inputs. Saved playback and inspection SHALL NOT invoke a model or mutate stored records or resident memory.

The player SHALL be readable and operable on desktop and phone, with keyboard and styled contextual help. Existing Picture, Network, causal history, exact trace/input, rules and other advanced actions SHALL remain reachable. The approved creation and live-execution paths SHALL retain their behavior.

#### Scenario: Inspect a recorded attempt without replay timing

- **GIVEN** the retained six-round pump recording
- **WHEN** the visitor opens it and selects Bo’s first-round attempt
- **THEN** playback begins paused and every retained round is directly selectable
- **AND** the visitor sees Bo’s original negative-assent words, positive-assent interpretation and actual false-to-true recorded change together
- **AND** seeking and inspection make no model calls or recording changes

#### Scenario: Earlier event selection restores the corresponding historical state

- **GIVEN** round 6 is selected in the pump recording
- **WHEN** the visitor selects Ari’s round-3 parent and then its validation reaction
- **THEN** the parent shows review completed and the child separately shows review idle, validation passed and hold false
- **AND** a later same-round review request does not overwrite either event’s selected state
- **AND** actor input uses the selected person’s exact pre-choice round-3 record, with missing child-policy input left unavailable

#### Scenario: Historical records and Actor privacy remain explicit

- **GIVEN** a declared-input recording or a historical unrestricted recording
- **WHEN** the visitor uses Actor-only viewing or opens a missing input
- **THEN** Actor mode hides Analyst world/event evidence and other people’s inputs
- **AND** unavailable historical actor input is labelled unavailable without reconstruction from canonical world state
- **AND** existing advanced inspection remains reachable in Analyst view

#### Scenario: The same inspection task works on a phone

- **WHEN** the visitor selects rounds and events at desktop and phone widths using pointer or keyboard
- **THEN** required text is readable without overlapping scene labels or page overflow
- **AND** temporal controls and contextual help remain usable

#### Scenario: Playback preserves every event

- **GIVEN** the first event of a saved recording is selected
- **WHEN** the visitor presses Play and then Pause
- **THEN** playback advances through the round’s actor attempts and automatic consequences in retained event order, without skipping to the next round’s first event
- **AND** Pause holds the selected event and its world state
- **AND** replaying from the last event returns to the recording’s first event without a model call
