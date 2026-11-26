## ADDED Requirements

### Requirement: A world that will stall says so on the run page

When the quick test of a freshly built world went quiet, left groups unable to act, or got stuck on one move, the run page shows that warning in plain words before the person plays, and the build wait message gives an honest time.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 7).

#### Scenario: a-world-that-will-stall-says-so-on-the-run-page

- **WHEN** a build goes straight to the run and its quick test ended with nobody able to act
- **THEN** the run page shows the warning above the run controls
- **AND** the build wait message says it usually takes two to three minutes
- **AND** on a narrow screen the library list is capped in height so the map is not pushed off the first screen
