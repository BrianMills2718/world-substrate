## MODIFIED Requirements

### Requirement: Rule checks read as plain English

Rule checks read as plain English with the things' names, never jargon. A check's label states the requirement
("only the dispatcher can request training"), never a claim about the person trying ("you are the dispatcher"), because
a refusal shows the label as the unmet need.

Where it is enforced: label rule in `scripts/generate_causal_model.py`.

Router heuristic: existing: `every-label-explains-itself`.

Source: Cold first-visit review, 2026-10-05 ("ownership context", "Actor is available"); requirement wording inferred
by agent from world-substrate#245.

#### Scenario: A rule check is shown

- **WHEN** the page shows a rule check
- **THEN** it reads as plain English with the things' names
- **AND** it uses no internal jargon such as "ownership context"

#### Scenario: A refusal names the unmet requirement

- **WHEN** a move is refused because a role check failed
- **THEN** the reason reads as the requirement ("only the dispatcher can request training")
- **AND** it does not read as a statement about the person trying ("you are the dispatcher")
