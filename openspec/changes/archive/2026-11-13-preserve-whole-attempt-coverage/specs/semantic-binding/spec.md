## ADDED Requirements

### Requirement: Whole attempt coverage

Fresh open-attempt interpretations MUST assess whether one identified operation represents the whole utterance, before binding even a wait. The existing interpreter call MUST return coverage status (`complete`, `requires_decomposition`, `partial`, or `ambiguous`), exact nonblank action substrings, and exact nonblank unrepresented substrings. Complete requires an identified operation and no unrepresented spans; incomplete requires unrepresented spans, and only ambiguous may have no identified action span. Missing or malformed fresh assessments MUST fail closed. Exact quote checks validate evidence shape, not semantic truth.

A concrete means MUST be bound rather than substituted with the goal it serves. Expressed stance, assent and withholding or revoking assent MUST remain distinct. Quoted speech, coordinated instruments, motives and expected consequences do not themselves add independent operations. An impossible single operation remains complete and is submitted to the installed mechanics.

An incomplete interpretation MUST preserve the original utterance and available coverage, execute no part, invoke no rule judge and deliver no request. The actor MUST receive a constant clarification without privileged model reasoning; analyst evidence retains the reading. A complete operation with no installed rule remains eligible for the existing unmatched-attempt judge/request path. Historical records without coverage MUST remain readable without inventing an assessment.

Source: inferred by agent from production5 (2026-11-13), Q36 and Brian's approval “i approve proceed” after the recommended compound-attempt follow-up; technical defaults implement the approved bounded correction.

#### Scenario: A concrete recording serves a goal

- **WHEN** someone says “withhold assent by recording a concern” and an installed kind represents recording concern
- **THEN** the interpreter binds that recording rather than revoking assent; the installed rule alone decides its effects

#### Scenario: Multiple independent operations have no installed composite

- **WHEN** someone tries to repair a condition and send a separate request, and no installed composite covers both
- **THEN** coverage requires decomposition, no part is executed, no judge is called and no request reaches another actor
- **AND** the original text and coverage remain inspectable and the actor receives safe clarification

#### Scenario: An installed composite covers the request

- **WHEN** one installed composite kind and its fields represent the complete request
- **THEN** it may bind as one operation and its installed mechanics decide atomically

#### Scenario: Content and consequences are not extra operations

- **WHEN** an attempt reports quoted content with several verbs, uses coordinated instruments, or expects knock-on consequences
- **THEN** these do not alone require decomposition; an impossible identified single operation still reaches the installed rule checks

#### Scenario: Fresh missing assessments and historical unassessed readings differ

- **WHEN** a fresh model response omits or malforms coverage
- **THEN** it is retained as an interpretation rejection with no action, judge or request effect
- **AND** an older recorded reading without coverage remains readable without claiming a newly assessed interpretation
