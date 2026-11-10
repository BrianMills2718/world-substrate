# ai-judge Specification

## Purpose
The AI judge rules on attempts no installed rule covers, from what the engine computes rather than from its own guess: the consequence report (slice J1 of `docs/plans/ai_judge.md`) gives it, in two passes, what installed rules already say about the people involved and what a proposed rule would do when test-run on a copy of the world. The judge itself (Concordia's game master, J2) and installing its rulings (J3) are later slices.

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
