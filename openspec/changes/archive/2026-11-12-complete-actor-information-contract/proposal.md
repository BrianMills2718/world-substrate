# Complete actor-information contract (documentation adoption only)

## Why

Brian's November 12 documentation goal requires a complete actor-information contract before implementation. The implemented v0 delivery seam filters represented messages but does not establish that briefs, summaries, recent events, restored memory, offered actions or UI hide inaccessible world state. The modeling guide now specifies the missing target and a single-concern example.

## What Changes

- Adopt target requirements for every actor-input ingress, provenance and temporal exposure.
- Preserve v0's documented behavior and limitations; add no runtime implementation claim.
- Keep the guide's concrete scenario as a design example, not a prescribed persuasion result.

## Impact

Only normative documentation changes. No simulator code, tests, runtime schema or paid run is introduced. These requirements remain unbuilt until implementation and direct evidence establish them. Archive completion means documentation adoption, not runtime delivery.

Source: Brian's explicit pre-implementation documentation goal, 2026-11-12, and agent-inferred contract in docs/model/modeling-choices.md, Complete actor-information contract.
