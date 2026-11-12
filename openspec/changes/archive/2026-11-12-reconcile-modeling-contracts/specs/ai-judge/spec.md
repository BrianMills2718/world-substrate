## MODIFIED Requirements

### Requirement: Another person's choice goes to that person

A ruling SHALL cover only whether the world allows the move, never what another person chooses. When an attempt needs
another person's choice (to accept, sell, sign or hand over), the judge SHALL name that person and the attempt SHALL
go to that person as their decision. A voluntary exchange SHALL require each party's agreement bound to the exact
live offer, parties and terms. A guarded giver-shaped conditional move or receiver-shaped settlement is permitted;
neither shape SHALL transfer goods without that agreement. Rule installation and owner approval SHALL NOT supply
actor agreement, revive an expired offer or reuse agreement for altered terms. Settlement SHALL also satisfy current
world constraints and consume the offer once; duplicate acceptance SHALL NOT repeat its effects.

Source: the AI judge plan, `docs/plans/ai_judge.md` (Decided 4, R5); Brian, 2026-11-09: "whether the bribe works seems
like should be a deicsion made by the person being bribed"; build approved 2026-11-10

#### Scenario: Another person's choice goes to that person

- **WHEN** Vik offers Rosa 40 coins to sign without inspecting, or the sawmill offers to pay the logger for its cedar
  logs
- **THEN** the ruling names Rosa (or the logger) as the one whose choice it is, the exact offer reaches that
  person, and no coin or log moves without that person's matching agreement; either guarded settlement shape
  applies current constraints, and an expired, changed or consumed offer cannot settle

Example clarification (2026-11-12): agreeing to the bribe does not satisfy the existing `inspected` check in pass 1. Rosa’s signing attempt remains blocked while that fact is false, and a signature-conditional exchange cannot settle. A scenario permitting signing without inspection must separately represent that executable capability and a breakable norm; the judge does not override the installed blocker. This clarifies the existing no-override requirement, not a new runtime behavior.

Source: 2026-11-12 normative reconciliation, inferred by agent from the Q96 exact-offer contract in docs/plans/ai_judge.md under Brian's approval to resolve design contracts. Required behavior; lifecycle implementation remains unbuilt.

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
- **THEN** the rule is installed after the rules check and the ruling is listed as installed and approved;
  each waiting voluntary exchange settles only if its own offer is still live, has matching actor agreement
  bound to the approved effects, and satisfies current constraints. Otherwise its pending or terminal
  disposition is recorded without transfer; approval alone supplies no actor agreement

#### Scenario: Rejecting refuses both waiting attempts and names the ruling

- **WHEN** the owner rejects the held ruling and the next round starts
- **THEN** each waiting attempt is refused naming the rejected ruling, the rule is never installed, and a later
  attempt of the same kind is refused the same way without a judge call

#### Scenario: The setting is saved with the world and defaults to approved by Create

- **WHEN** a world is built with no setting, with "wait", and with a value that is neither
- **THEN** the world saves "create", "wait", and is refused with an error, and a shared run records the setting

Source: 2026-11-12 normative reconciliation, inferred by agent from the Q96 exact-offer contract in docs/plans/ai_judge.md under Brian's approval to resolve design contracts. Required behavior; lifecycle implementation remains unbuilt.
