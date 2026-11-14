## ADDED Requirements

### Requirement: World graph
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C, one whole-system graph layer).
A shared run SHALL be viewable as one graph of everything in its world (who acts, the moves its rules allow, the things and places, the changes it makes by itself) with the chosen round lit, whether or not the world has a layout.

#### Scenario: Waltzman graph carries every box and the round's tries
- **WHEN** the graph of the Waltzman share is built
- **THEN** it has 70 boxes (10 who act, 17 moves, 17 things, 26 by-itself changes), 411 links, and each round lists every actor's try with allowed, refused or no-move

#### Scenario: A refusal keeps its reason and no words
- **WHEN** a round has a refused try
- **THEN** the graph names its reasons and carries no message words
