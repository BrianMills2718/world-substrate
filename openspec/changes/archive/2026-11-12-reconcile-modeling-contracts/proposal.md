## Why

The adopted Q96 plan allows either guarded giver-shaped or receiver-shaped exchange settlement, while the canonical AI-judge spec requires receiver-shaped rules and suggests owner approval settles every pending attempt. That representation constraint does not guarantee consent and contradicts the selected contract.

## What Changes

Reconcile the normative exchange requirements with actor-owned assent to exact live terms and current feasibility. Preserve both valid rule shapes; neither installation nor owner approval supplies assent. This change adopts specification wording only. Q96 implementation and A5 demonstrations remain unbuilt; archiving this document does not claim otherwise.

## Capabilities

### Modified Capabilities
- `ai-judge`: actor choice and conditional settlement after owner approval.

## Impact

Existing desired behavior and scenario IDs remain; required safeguards are clarified from docs/plans/ai_judge.md. No runtime changes. Source: Brian's 2026-11-12 approval of resolving modeling contracts before implementation; technical reconciliation inferred by agent from the selected Q96 design and original actor-choice direction.
