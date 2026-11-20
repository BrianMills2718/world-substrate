## MODIFIED Requirements

### Requirement: The judge is Concordia's game master, conditioned on the world and the consequence report

The judge SHALL be Concordia's `EventResolution` game master component, run on an entity built from Concordia's own
parts, with the attempt as the putative event. It SHALL be conditioned on the whole world (the description, kinds of
thing, installed rules and processes, declared laws and every current value) and on the consequence report: pass 1
before any rule exists, and, when it reviews a proposed rule, pass 2. It SHALL read pass 1 grouped: each person's
blocked bindings of one move as one entry, with how many bindings are blocked, one example and each failed check with
its value, what it requires and how many bindings it stopped, and no passing checks; the run record keeps pass 1 in
full. Our own part SHALL be limited to the resolution
steps, each a typed question asked of the document Concordia assembled, answered in the declaration language; every
model call SHALL go through `llm_client` under the run's trace id.

Source: the AI judge plan, `docs/plans/ai_judge.md` (R2, R7); Decision 006; Brian, 2026-11-09: "deliver the results of
that propagation to the judge along with blockers"; build approved 2026-11-10; reading pass 1 grouped inferred by agent
2026-11-19 from run `s4-waltzman-4` (world-substrate#473: 5 people x 80 blocked bindings, every check, made each judge
prompt about 285,000 tokens), under Brian, 2026-11-19: "anything that is high confidence or low signifcane"

#### Scenario: The game master reads the whole world and pass 1 and resolves the putative event

- **WHEN** Vik offers Rosa 40 coins to sign the release for his uninspected crate and no installed rule covers the
  hand-over
- **THEN** the judge's first document holds the whole world, pass 1 (Vik's moves, Rosa's moves with "sign release"
  blocked because "the crate is inspected" is false, and the values of Vik, Rosa and the crate) and "vik: I take the 40
  coins ... offer them to Rosa" as the putative event
- **AND** the judge's record says it came from the world's game master

#### Scenario: The review reads where a blocked chain stopped

- **WHEN** a proposed rule sets off a 40-step chain that reaches a truck with no fuel
- **THEN** the review step's document holds the test run's stopping point, "blocked at step 40" at "truck leaves" by
  "the truck has fuel" (actual 0), and the judge confirms, revises or withdraws with that blocker in what it read

#### Scenario: A long test run is read grouped

- **WHEN** a proposed rule's test run changes more than 40 fields (the long line changes 5,000)
- **THEN** the judge reads the net changes grouped by the same change on the same things, with their count, and no
  chain, and the run log keeps every step of the full test run

#### Scenario: Pass 1 is read grouped

- **WHEN** a person's blocked moves include many bindings of one move (in `s4-waltzman-4`, 80 bindings of
  `communicate` for each of 5 people, each with every check)
- **THEN** the judge reads one entry for that move with its count, one example, and each failed check with its value,
  what it requires and how many bindings it stopped, and no passing checks
- **AND** the run row keeps pass 1 in full, every binding with every check
