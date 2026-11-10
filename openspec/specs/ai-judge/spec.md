# ai-judge Specification

## Purpose
The AI judge rules on attempts no installed rule covers, from what the engine computes rather than from its own guess: the consequence report (slice J1 of `docs/plans/ai_judge.md`) gives it, in two passes, what installed rules already say about the people involved and what a proposed rule would do when test-run on a copy of the world. The judge itself (slice J2) is Concordia's game master: it proposes a rule for the attempt, reads its test run and confirms, revises once or withdraws, and sends another person's choice to that person. Installing its rulings (J3) is a later slice.

## Requirements

### Requirement: Pass 1 reports what installed rules compute for the people an attempt involves

For an attempt no installed rule covers, the consequence report's pass 1 SHALL list the moves of the person acting
and of each person the attempt names, as `Engine.discover` gives them (each available and blocked move with every
check, its value and what it requires), and the current values of the person acting and of every person and thing
the attempt names. A person's moves appear only on that person's own page. The names come from the attempt
interpreter's reading, which lists every person or thing in the world the attempt's words name; each run records
pass 1 with each unmatched attempt.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Canonical example; ledger Q78, inferred by agent 2026-11-09);
Brian, 2026-11-09: "deliver the results of that propagation to the judge"; build approved 2026-11-10

#### Scenario: Pass 1 lists the moves of the person acting and each person named

- **WHEN** Vik, a trader with 40 coins at the customs desk, offers Rosa, the customs officer, 40 coins to sign the
  release for his uninspected crate, and no rule covers handing coins
- **THEN** pass 1 lists Vik's moves and Rosa's moves, and Rosa's page shows "sign release" blocked by "the crate is
  inspected" (false), which never appears on Vik's page
- **AND** it gives the current values of Vik (40 coins, at the customs desk), Rosa and the crate

#### Scenario: An unmatched reading names who and what the attempt names

- **WHEN** the interpreter reads an attempt no rule covers and lists the people and things its words name
- **THEN** the unmatched reading keeps those names that are in the world, leaving out the person acting, with the
  person it asks first
- **AND** a reply recorded before the reading listed names names only the person it asks

#### Scenario: A run records pass 1 with each unmatched attempt

- **WHEN** a run's resident makes an attempt no installed rule covers
- **THEN** the attempt's round row carries `consequence.pass_one` with the moves and values above, and the run's
  list of unmatched attempts gives the names and the attempt's event

### Requirement: Pass 2 test-runs a proposed rule on a copy of the world

A proposed rule SHALL be test-run on a copy of the world as it is at the attempt, with the attempt submitted as the
rule's typed move. The report SHALL give the net changes, the blockers, the length of the knock-on chain and where it
stopped (settled, blocked after a given step with the failed check and its value, or refused), and SHALL keep the
full chain for the run record; the summary a judge reads leaves the full chain out. The real world, its bundle and
its rules SHALL be left unchanged.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Canonical example, "LLM call boundary and cost"); build approved
by Brian 2026-11-10

#### Scenario: The coin rule moves the coins and nothing else follows

- **WHEN** the rule "a person may hand coins they hold to a person at the same place" is test-run with Vik handing
  Rosa 40 coins
- **THEN** the net changes are Rosa's coins 0 to 40 and Vik's coins 40 to 0, with no blocker and a chain of length 0

#### Scenario: A test run that sets off a blocked chain says where it stopped

- **WHEN** a proposed rule that trips the lever of the truck-without-fuel world is test-run
- **THEN** the report gives a chain of 40 steps, stopped as blocked after step 40 at "truck leaves" by "the truck has
  fuel" (actual 0), and the blocker is in the summary a judge reads while the full chain stays in the report

#### Scenario: A move the proposed rule refuses is reported with its failed checks

- **WHEN** the coin rule is test-run with Vik handing Rosa 50 coins while he holds 40
- **THEN** the test run is refused (`precondition_failed`) with no net changes, and its stopping point and blocker
  name the failed check "the giver holds that many coins"

#### Scenario: The test run leaves the real world unchanged

- **WHEN** a proposed rule is test-run
- **THEN** the real world's state, revision, bundle and rules are the same afterwards, and the report names the
  revision it ran from

### Requirement: A proposed rule goes through the World Builder's rules check

Before any test run, a proposed rule SHALL be added to copies of the world's bundle and rules and put through the
same rules check a World Builder build goes through (bundle validation, the causal compiler, the mechanic
installer). A rule the check rejects SHALL be reported with the check's error and SHALL NOT be test-run.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Canonical example; RULE-APPROVAL-BEFORE-RUN); build approved by
Brian 2026-11-10

#### Scenario: A rule the check rejects is reported and not run

- **WHEN** a proposed rule names a field the declaration language does not accept ("from")
- **THEN** the report's rules check is not ok and gives the check's error, and there is no test run

### Requirement: The judge is Concordia's game master, conditioned on the world and the consequence report

The judge SHALL be Concordia's `EventResolution` game master component, run on an entity built from Concordia's own
parts, with the attempt as the putative event. It SHALL be conditioned on the whole world (the description, kinds of
thing, installed rules and processes, declared laws and every current value) and on the consequence report: pass 1
before any rule exists, and, when it reviews a proposed rule, pass 2. Our own part SHALL be limited to the resolution
steps, each a typed question asked of the document Concordia assembled, answered in the declaration language; every
model call SHALL go through `llm_client` under the run's trace id.

Source: the AI judge plan, `docs/plans/ai_judge.md` (R2, R7); Decision 006; Brian, 2026-11-09: "deliver the results of
that propagation to the judge along with blockers"; build approved 2026-11-10

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

### Requirement: The judge proposes a rule, reads its test run and confirms, revises once or withdraws

For an attempt that moves or changes something no installed rule covers, the judge SHALL propose one new move in the
World Builder's declaration language, with the attempt as its test move. The rule SHALL go through the rules check
and be test-run on a copy of the world as it is now; the judge SHALL read that report and confirm the rule, revise it
once, or withdraw it. A revision SHALL get its own rules check and test run and then a last answer, confirm or
withdraw. A rule the check rejects, and whose one revision is rejected too, SHALL be refused as "no rule could
express this" and recorded as a language gap. A confirmed ruling SHALL carry its rule, its move and its test runs.
Nothing is installed at this stage.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Canonical example steps 3 and 4, R4, slice J2); Brian, 2026-11-09:
"yes i aprpove all those"; build approved 2026-11-10

#### Scenario: A confirmed ruling carries its rule and its test run

- **WHEN** the judge confirms the rule it proposed for Vik's offer
- **THEN** the ruling's outcome is confirmed, and it carries the rule, the move that was test-run (Rosa accepting 40
  coins from Vik) and the test run (Rosa's coins 0 to 40, Vik's 40 to 0, no blocker, chain length 0)

#### Scenario: A ruling is revised at most once

- **WHEN** the judge answers "revise" to the report of its first rule
- **THEN** the revised rule is checked and test-run once, the judge gives a last answer of confirm or withdraw, and no
  second revision is made

#### Scenario: A rule the language cannot express is a language gap

- **WHEN** the rules check rejects the proposed rule and rejects its one revision too
- **THEN** the outcome is "language gap" with the words "no rule could express this", and no rule is confirmed

### Requirement: Another person's choice goes to that person

A ruling SHALL cover only whether the world allows the move, never what another person chooses. When an attempt needs
another person's choice (to accept, sell, sign or hand over), the judge SHALL name that person, the rule SHALL be
written as that person's own move, and the attempt SHALL go to that person as their decision. The person trying SHALL
never be named as the one whose choice it is.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 4, R5); Brian, 2026-11-09: "whether the bribe works seems
like should be a deicsion made by the person being bribed"; build approved 2026-11-10

#### Scenario: Another person's choice goes to that person

- **WHEN** Vik offers Rosa 40 coins to sign without inspecting, or the sawmill offers to pay the logger for its cedar
  logs
- **THEN** the ruling names Rosa (or the logger) as the one whose choice it is, its rule is her (or the logger's) own
  move, the words reach her as her decision, and no coin or log moves on the offerer's move alone

### Requirement: The judge rules on attempts no installed rule covers, and only those

In a run with open attempts, the judge SHALL rule on each attempt no installed rule covers, after everyone's move in
the round, each reading the world as it was when that attempt was tried. An attempt an installed rule covers SHALL be
decided by that rule, refused with the failed check named when one fails, and SHALL NOT reach the judge. A failed
judge call SHALL be recorded and the run SHALL go on. A ruling SHALL be recorded in the run, not installed.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 2, R3, slice J2); Brian, 2026-11-09: "yes i aprpove all
those"; build approved 2026-11-10

#### Scenario: The judge rules on each unmatched attempt in a run

- **WHEN** a resident's attempt matches no installed rule
- **THEN** the attempt's round row carries the judge's ruling and the run's cost counts the judge's calls, and no rule
  is installed

#### Scenario: An attempt an installed rule covers never reaches the judge

- **WHEN** Ines, holding no coins, tries to hand Rosa 10 coins and the installed coin rule covers handing coins
- **THEN** the engine refuses it with "the giver holds that many coins", nothing changes, no judge call is made, and the
  run page says "Decided by rule, judge not asked."
