## ADDED Requirements

### Requirement: Rules overlay

Source: Brian, 2026-11-14: "i approve" (overlay of the world's rules on the map; computer only); tag colours and click-through inferred by agent.

When a replay carries the world's rules, the viewer SHALL offer a switch that shows each rule on the map and marks, for the step shown, the rule each person's attempt met as allowed or refused with the failed check named in words as well as colour. A replay made from a shared run SHALL carry the rules of that run's world; rule text is the world's own definition and carries no report words.

#### Scenario: A refusal shows the rule that caused it

- **GIVEN** a saved run in which a person tries to walk through a closed door
- **WHEN** the replay is exported with the world's causal model
- **THEN** that step records the move rule, refused, with "the door must be open", on that door
- **AND** the later step where the door opens records the open-door rule as allowed
