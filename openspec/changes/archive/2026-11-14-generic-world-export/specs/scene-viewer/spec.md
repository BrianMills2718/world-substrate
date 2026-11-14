## ADDED Requirements

### Requirement: Any world's actions and doors show

Source: inferred by agent, from the first live Builder-made world (clinic, 2026-11-14) failing to export.

The replay exporter SHALL show every action kind of any world, not only the pump facility's, and SHALL draw a door open from the first step someone walks through it when the world has no action that opens it.

#### Scenario: A clinic world exports

- **GIVEN** a shared run of a Builder-made world whose actions include check-in, unlock-lab-door and examine
- **WHEN** its room-map replay is requested
- **THEN** each action appears in words, and the door two people walk through is open from that round
