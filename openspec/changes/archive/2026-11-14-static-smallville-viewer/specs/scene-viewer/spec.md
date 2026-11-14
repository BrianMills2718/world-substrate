## ADDED Requirements

### Requirement: Static replay viewer

Source: Brian's 2026-11-14 choice of option A; mechanism inferred by agent.

The viewer SHALL play an exported replay from static files with no server. It SHALL draw each door closed or open from the replay's door changes, show a refused attempt with its reason and a delivered report as readable text from the sender, place people sharing a room on different tiles, and fit the facility to the viewport at desktop and 390px widths. The map art SHALL NOT be committed; a setup script copies it from a local clone.

#### Scenario: Refusal at a closed door, then the door opens

- **GIVEN** an exported run in which a person is refused at a closed door and later opens it
- **WHEN** the viewer shows the refused step and then the later step
- **THEN** the door is drawn closed with the refusal reason shown, and later drawn open

#### Scenario: A report shows its words

- **WHEN** the viewer shows the step where one person reports to another
- **THEN** the sender's words appear as text above the sender and in the people panel
