# Transition envelope contract v0

**Status:** proposed  
**Purpose:** give one enclosing action or process sole authority to commit a causally coupled state transition

## Pipeline

```text
actor/process observation
  -> semantic sense and role binding
  -> local mechanic selection
  -> applicability and authorization
  -> proposed effects
  -> resource and invariant validation
  -> one commit or refusal
  -> causal trace
```

## Requirements

- An attempt identifies its causal bearer and current world revision or snapshot identity.
- Semantic binding and mechanic selection occur before effect proposal.
- The selected mechanic can read and propose writes only within independently enforced state-path scope.
- Applicability rules, permissions, contracts, pricing rules, and institutions may inspect state and propose effects. They may not commit effects belonging to an enclosing transition that can still fail.
- The coordinator validates all causally coupled effects before committing any of them.
- A refusal leaves canonical state unchanged, except for separately modeled causal events whose occurrence is independent of the refused transition.
- Successful commit records the accepted operations, relevant checks, commit order, and resulting persistent state identity.
- Derived interpretations may observe the committed history but cannot reapply its effects.

This is not a requirement for universal ACID transactions. Independent actions may commit independently. The singular boundary applies when several effects belong to one claimed causal transition.

## Examples

Two voluntary gives are independent transitions. Robin may give a spear and Friday may renege on giving coconuts. A derived `exchange` view can recognize the reciprocal history but cannot transfer either asset again.

An installed escrow release is one institutionally coupled transition. Asset release, payment, and escrow-state changes either pass validation and commit together or refuse together.

A pressure check may propose vessel damage, capability revocation, fluid release, and relation handoff as one coupled transition when the selected mechanics profile defines them as consequences of the same rupture.
