## ADDED Requirements

### Requirement: Preserve operation and referents

The interpreter MUST match the complete attempted operation, preserving its object, polarity and qualifications. Recording non-assent MUST NOT be represented as recording positive assent merely because both use a recording verb. Negation of an operation, uncertainty about its success, and negative content quoted within another operation MUST remain distinct. If no installed operation represents the meaning, the reading MUST remain unmatched rather than execute the opposite.

The speaker, an authority/credential they hold and their recorded position MUST remain distinct referents. A self-reference MUST supply the actor identity only when that field denotes the person; an object/role field MUST resolve to its own represented identity. Ambiguous referents MUST NOT be guessed.

For declared actor-information worlds, interpretation MUST retain the public example field bindings from the same visibility-filtered action forms supplied to the actor. An example is interpretive context, not a forced filler or proof of executability. Explicitly named different participants or objects MUST NOT be overwritten. Unseen form identities/descriptions and hidden canonical singleton/derived values MUST NOT enter the model input. Mechanical checks alone still decide feasibility; this contract does not claim semantic infallibility.

Source: inferred by agent from retained native calls23480/23481/23493 and Brian's 2026-11-13 approval of the recommended negation/authority correction.

#### Scenario: Non-assent is not assent

- **WHEN** an actor attempts to record a position of non-assent
- **THEN** interpretation preserves that polarity or remains unmatched; it does not select a positive-assent operation

#### Scenario: An actor uses a represented authority

- **WHEN** repair requires a separate authority object and the actor refers to their own role implicitly or explicitly
- **THEN** interpretation uses visible public referents rather than automatically binding every self-reference to the actor

#### Scenario: Public examples do not disclose private forms or force an action

- **WHEN** an action form references an entity absent from the actor's observation
- **THEN** its example and description do not enter interpretation
- **AND** visible examples cannot replace an explicitly named different argument or determine whether a move succeeds

#### Scenario: Private state does not change interpreter input

- **WHEN** only hidden canonical state or labels change
- **THEN** the actor-authorized interpreter input remains identical
