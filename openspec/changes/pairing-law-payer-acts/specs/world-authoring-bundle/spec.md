## ADDED Requirements

### Requirement: A newly designed pairing law has the payer start the move

A world proposal from the designer SHALL be refused, and the designer told why, when a pairing law's `pays.from` is
anything other than `actor`: whoever pays is the one making the move, so nobody's money moves without their choosing.
Validating a saved bundle (`validate_bundle`) SHALL NOT apply this rule.

Source: issue #282 (S1 pencil build); the mechanism is inferred by agent.

#### Scenario: A seller-started sale is refused

- **GIVEN** a proposal whose pairing law for `sell-pencil` pays money from `customer` to `actor`
- **WHEN** the designer's proposal is checked
- **THEN** a `BundleError` names the law and says the payer must be the actor, and the designer is asked again

#### Scenario: A buyer-started purchase is accepted

- **GIVEN** a pairing law for `buy-logs` that pays money from `actor` to `seller`
- **WHEN** the designer's proposal is checked
- **THEN** it is accepted

#### Scenario: Saved worlds still load

- **GIVEN** the saved world `tests/fixtures/pencil-s3-kept.json`, whose `sell-boxes` law pays from `customer`
- **WHEN** it is validated with `validate_bundle`
- **THEN** it validates
