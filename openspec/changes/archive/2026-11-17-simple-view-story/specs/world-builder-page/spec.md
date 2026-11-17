## ADDED Requirements

### Requirement: The run page opens in a plain Simple view
The run page SHALL open a saved run in a Simple view that says what the world is, shows the outcome bar and support chart, and tells what happened in plain sentences round by round. The detailed screen SHALL remain available, unchanged, as the Advanced view behind a switch, and the choice SHALL be remembered per browser. The account SHALL be written once per saved checkpoint, from the server's own record of the run, by an AI step whose every sentence cites events of that round; a sentence without a supporting event SHALL be dropped and counted, and a round or slice that could not be written SHALL be named.

#### Scenario: simple-view-story
- **WHEN** a person reopens a saved run
- **THEN** the page shows the plain per-round account by default, the detailed screen is one switch away, and opening the same run again makes no AI call
