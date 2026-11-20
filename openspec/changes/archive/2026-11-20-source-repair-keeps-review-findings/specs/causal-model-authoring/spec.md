## ADDED Requirements

### Requirement: A source repair also passes on the review's rule findings

When the independent rules review rejects a try's source judgment (actor inputs or current state) and the build
repairs the world definition, the one rewrite of the rules SHALL receive that same review's rule findings, put first
in its guidance, along with the repaired definition; the retained rejected try SHALL record those findings.

Source: Brian, 2026-11-20: "go" (fix issue #474 before a fresh Waltzman run); the mechanism is from the s4-waltzman-4
trace (review call 24906, issue #474), inferred by agent.

#### Scenario: A privacy repair also passes on the missing decision

- **GIVEN** a review that rejects a try's source judgment and also finds "Nothing lets the partnership decide by the
  deadline"
- **WHEN** the build repairs the world definition and writes the rules again
- **THEN** the rewrite's guidance names that finding and the description's words, and the rejected try's record
  holds the finding
