# M1 freshwater review

**Result:** PASS — the scripted neutral freshwater journey and all three discriminating negative paths are accepted.

The detailed machine receipt is [freshwater-v0.json](freshwater-v0.json), and the complete command/event trace is [transfer-v0.json](transfer-v0.json).

## Positive journey

| Observation | Result |
| --- | --- |
| Commands replayed | 22 |
| Final tick | 15 |
| Clay-pot owner | `actor:friday` |
| Clay-pot contents | 728 ml, 0 pathogens, 20278 heat units at 27.85 C |
| Actor hydration | Robinson 60; Friday 35 |
| Heat / treatment ledger | 78000 added; 68552 lost; 400 pathogens killed |
| Vessel identity preserved | true |
| Donor semantic checkpoint matched | true |
| Exact replay matched | true |

## Negative journeys

| Case | Expected / observed | Material state | Replay |
| --- | --- | --- | --- |
| Overfill | `precondition_failed` / `precondition_failed` | atomic: true | exact: true |
| Valid pressure envelope without a rule | `unsupported_action` / `unsupported_action` | atomic: true | exact: true |
| Malformed fill envelope | `invalid_action` / `invalid_action` | atomic: true | exact: true |

## Claim boundary

This establishes one deterministic scripted physical reference vertical. It does not establish LLM policy competence, cross-domain reuse, scale, deployment, or real-world water-treatment validity.
