## ADDED Requirements

### Requirement: The Simple view discloses progressively
The Simple view SHALL show only what a newcomer needs first: the world in a short clamped description with a Read more control, the outcome, the map, and one collapsed card per round with a one-line headline. Opening a round SHALL show its sentences as short bullets, only the round shown on the map SHALL be open, and choosing a round SHALL move the map and the numbers to it. The list of every world and branch and the run controls SHALL be folded away in the Simple view and remain in the Advanced view.

#### Scenario: simple-view-discloses-progressively
- **WHEN** a person opens a saved run
- **THEN** the list of worlds and branches is not shown, the rounds are collapsed cards with headlines, and only the shown round is open
