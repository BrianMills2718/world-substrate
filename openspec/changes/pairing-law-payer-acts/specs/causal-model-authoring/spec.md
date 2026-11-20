## ADDED Requirements

### Requirement: A trade's actor selector names the payer

The rules writer's context SHALL tell it that, for a move named by a pairing law, the actor selector names the kind
of entity that pays and is not narrowed to the one who is paid.

Source: issue #282 (buy-boxed-pencils refused the shop four times); inferred by agent.

#### Scenario: The rules writer is told who acts in a trade

- **GIVEN** a bundle with a pairing law
- **WHEN** the rules writer's context is built
- **THEN** an `authority_rules` entry says the actor selector of a pairing law's move names the payer
