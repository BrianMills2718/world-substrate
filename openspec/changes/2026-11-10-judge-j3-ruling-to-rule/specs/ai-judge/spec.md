## ADDED Requirements

### Requirement: A checked ruling is installed as a rule during the run

When the world's setting is "Approved by Create" (the default), a ruling the judge confirmed that passed the rules
check and the test run SHALL be installed into the running engine before the round ends, as a rule that applies to
everyone in the situation it names. Installing SHALL go through the same rules check a build's rules go through, and
the world's own rules and fingerprint SHALL stay as the visitor approved them: installed rules are run state, listed
with their origin. The attempt SHALL settle through the installed rule when it needs no one else's choice, and SHALL
reach the person whose choice it is otherwise, whose page then offers the rule's move. The judge SHALL NOT write an
outcome: only the engine, under the installed rule, commits or refuses.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 3 and 5, Canonical example steps 5 and 6); Brian,
2026-11-09: "can we make this configurable? or is that more troubel than it is worth. if so i say yes"; build approved
2026-11-10

#### Scenario: A confirmed ruling is installed after the rules check and the test run

- **WHEN** the judge confirms the coin rule for Vik's offer to Rosa and the world's setting is the default
- **THEN** the rule is a registered action of the running engine, the ruling's state is "installed" with its rules
  check and test run, and the world's own bundle and rules are unchanged

#### Scenario: A ruling that needs no one else's choice settles the attempt through the rule

- **WHEN** the judge confirms a rule for an attempt that needs no one else's choice and the rule is installed
- **THEN** the engine submits the attempt as the rule's move and commits or refuses it by the rule's own checks, and
  the attempt's row says which rule settled it and what changed

#### Scenario: A ruling that needs another person's choice reaches that person under the rule

- **WHEN** the judge confirms a rule for an offer to Rosa and names Rosa as the person whose choice it is
- **THEN** nothing moves, Rosa is asked, and her page offers the installed rule's move, which she may choose

#### Scenario: A later attempt the rule covers is decided by the rule and the judge is not asked

- **WHEN** another trader later tries the same kind of hand-over after the rule is installed
- **THEN** the interpreter reads it as the installed rule's move, the engine decides it by the rule's own checks, and
  the judge is not called

### Requirement: The world's setting can hold a ruling until the owner approves it

When the world's setting is "Wait for my approval", a confirmed ruling that passed the rules check and the test run
SHALL be held: nothing is installed, the attempt waits as pending and changes nothing, the run goes on for everyone
else, and a later attempt the held rule would cover SHALL join the same pending ruling without a judge call. The run
page SHALL list the held ruling with Approve and Reject. Approving SHALL install the rule through the rules check at
the start of the next round and settle each waiting attempt through it; rejecting SHALL refuse each waiting attempt,
naming the ruling, and a later attempt the rejected rule would cover SHALL be refused the same way. Nothing settles
without an installed rule.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 5, Wait mode; ledger Q80); Brian, 2026-11-09: "can we
make this configurable? or is that more troubel than it is worth. if so i say yes"; build approved 2026-11-10

#### Scenario: A held ruling changes nothing and its attempt waits

- **WHEN** the judge confirms the coin rule for Vik's offer under "Wait for my approval"
- **THEN** the ruling is "held", the rule is not a registered action, the world's state is unchanged, the attempt's
  row says "pending: waiting for your approval" and Rosa is not yet asked

#### Scenario: A later identical attempt joins the held ruling

- **WHEN** a second trader tries the same kind of hand-over while the ruling is held
- **THEN** the attempt is read as the held rule's kind and joins the pending ruling, the judge is not called, and
  its row says "pending: waiting for your approval"

#### Scenario: Approving installs the rule and settles both waiting attempts

- **WHEN** the owner approves the held ruling and the next round starts
- **THEN** the rule is installed after the rules check, each waiting attempt settles through it (it reaches the
  person whose choice it is, or the engine commits it), and the ruling is listed as installed and approved

#### Scenario: Rejecting refuses both waiting attempts and names the ruling

- **WHEN** the owner rejects the held ruling and the next round starts
- **THEN** each waiting attempt is refused naming the rejected ruling, the rule is never installed, and a later
  attempt of the same kind is refused the same way without a judge call

#### Scenario: The setting is saved with the world and defaults to approved by Create

- **WHEN** a world is built with no setting, with "wait", and with a value that is neither
- **THEN** the world saves "create", "wait", and is refused with an error, and a shared run records the setting

### Requirement: A ruling the language cannot express is refused and listed as a language gap

A ruling whose rule the rules check rejects, and whose one revision is rejected too, SHALL be refused: nothing is
installed, the attempt is refused with "no rule could express this", and the run lists the ruling as a language gap
with the rules check's error.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 3, ledger Q79); build approved 2026-11-10

#### Scenario: A language gap is refused and listed

- **WHEN** the judge's rule and its one revision are both rejected by the rules check
- **THEN** the attempt's row says "no rule could express this", the ruling list shows it as a language gap with the
  check's error, nothing is installed and the world is unchanged

### Requirement: Installed rulings travel with the run

The rulings of a run (installed, held, rejected and language gaps) SHALL be sealed run state: each round's response
carries them, the next round sends them back under the same seal as the world's state, and a list the server did not
seal SHALL be refused. A round SHALL list every ruling with its state, and the owner's Approve or Reject SHALL reach
the server with the next round's request.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 5); "saved worlds still replay unchanged" (goal
boundaries); inferred by agent, 2026-11-10: the World Builder keeps no run state on the server, so installed rules
ride in the sealed run state beside the snapshot

#### Scenario: A continued round keeps the installed rule

- **WHEN** a round installs a rule and the next round is requested with the sealed state
- **THEN** the next round's engine has the rule, and a list or decision the server did not seal is refused

#### Scenario: The Create page offers the setting and the run page lists every ruling

- **WHEN** a visitor opens Options on the Create page and a run holds or has installed a ruling
- **THEN** "Judge rulings during a run" offers "Approved by Create" (selected) and "Wait for my approval", and the run
  page lists each ruling with its state and Approve and Reject for a held one
