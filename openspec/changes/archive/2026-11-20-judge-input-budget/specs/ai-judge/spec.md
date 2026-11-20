## MODIFIED Requirements

### Requirement: The judge is Concordia's game master, conditioned on the world and the consequence report

The judge SHALL be Concordia's `EventResolution` game master component, run on an entity built from Concordia's own
parts, with the attempt as the putative event. It SHALL be conditioned on the world (the description, kinds of
thing, installed rules and processes, declared laws, and every thing by id, label and kinds) and on the consequence
report: pass 1 before any rule exists, with the current values of the person trying and of each person and thing named,
and, when it reviews a proposed rule, pass 2. It SHALL read pass 1 grouped: each person's blocked bindings of one move
as one entry, with how many bindings are blocked, one example and each failed check once, by its label, with how many
bindings it stopped and at most three example values and what each requires, and no passing checks; the run record
keeps pass 1 in full. Our own part SHALL be limited to the resolution
steps, each a typed question asked of the document Concordia assembled, answered in the declaration language; every
model call SHALL go through `llm_client` under the run's trace id.

Source: the AI judge plan, `docs/plans/ai_judge.md` (R2, R7); Decision 006; Brian, 2026-11-09: "deliver the results of
that propagation to the judge along with blockers"; build approved 2026-11-10; reading pass 1 grouped inferred by agent
2026-11-19 from run `s4-waltzman-4` (world-substrate#473: 5 people x 80 blocked bindings, every check, made each judge
prompt about 285,000 tokens), under Brian, 2026-11-19: "anything that is high confidence or low signifcane"; the world
without current values and each failed check once: Brian, 2026-11-20: "ia pprove your recommendations" (the judge
reads only what concerns the attempt)

#### Scenario: The game master reads the whole world and pass 1 and resolves the putative event

- **WHEN** Vik offers Rosa 40 coins to sign the release for his uninspected crate and no installed rule covers the
  hand-over
- **THEN** the judge's first document holds the world, pass 1 (Vik's moves, Rosa's moves with "sign release"
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
- **THEN** the judge reads one entry for that move with its count, one example, and each failed check once with how
  many bindings it stopped and at most three example values, and no passing checks
- **AND** the run row keeps pass 1 in full, every binding with every check

## ADDED Requirements

### Requirement: The judge's input is bounded and its unchanging part comes first

The judge's input SHALL be bounded by the world's moves and checks, not by how many bindings they have: the judge's
first prompt for an attempt in the largest saved world SHALL stay under 20,000 input tokens, counted at 4.2 characters
a token (judge call 24925 on the VPS: prompt tokens over characters). Every judge call in a round SHALL start with the
same text: a system message that names no person and no step, then the document, which starts with the world; the
person trying and the step's instructions SHALL come in a last message, so the provider can read the leading part from
its cache.

Source: Brian, 2026-11-20: "ia pprove your recommendations" (decision 1: a requirement that the judge's input stays
under 20,000 tokens for the largest saved world, tested on the Waltzman run, and the prompt ordered so caching works);
2026-11-20: "i dont understand why we would be giving the judges 285,0000 tokens for these tiny simulations. this
obviosuly wont scale". Context: world-substrate#473; `docs/plans/ai_judge.md`, "Pass 1, measured 2026-11-19".

#### Scenario: The judge's input stays under 20,000 tokens for the largest saved world

- **WHEN** the judge rules on country-a's attempt in run `s4-waltzman-4` (5 people, 80 blocked bindings of
  `communicate` each), with pass 1 computed by today's code on that run's world
- **THEN** its first prompt is under 84,000 characters (20,000 tokens); the run recorded 1,190,699

#### Scenario: The same leading text starts every judge call in a round

- **WHEN** the judge proposes a rule for Vik's offer and then reviews its test run
- **THEN** both calls have the same system message, which does not name Vik, and both documents start with the same
  world text, which holds no current value
- **AND** "The person trying is vik." and the step's instructions come in each call's last message
