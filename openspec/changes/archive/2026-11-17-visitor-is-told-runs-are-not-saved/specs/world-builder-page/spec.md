## ADDED Requirements

### Requirement: A visitor is told runs are not saved
When no owner password is set in the browser, the describe stage shows beside Run that the world and its runs will not be saved, with a button that opens owner access; the notice is hidden once owner access is on.

Source: Brian, 2026-11-17: "also it doesnt seem to save runs"

#### Scenario: a-visitor-is-told-runs-are-not-saved
- **WHEN** a person without owner access opens the page
- **THEN** the notice and its Turn on owner access button show next to Run
- **AND** after owner access is entered the notice is hidden
