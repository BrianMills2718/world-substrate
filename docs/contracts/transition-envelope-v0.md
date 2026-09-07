# Transition envelope contract v0

**Status:** partially implemented. Singular commit, atomic refusal, and causal trace are implemented in `Engine.apply`/`Engine.advance`. Independently enforced **write** scope is implemented (`scope_violation`). Rule-facing discovery, applicability, consequence, progress, and trigger hooks run against detached state and are enforced as read-only; effect application also receives detached state, while `revision`, commands, and events remain coordinator-owned. Independently enforced **read** scope is not implemented: declared reads are recorded on every event and unchecked. Institutional coupling of several bearers' effects into one transition is unimplemented and untested.  
**Purpose:** give one enclosing action or process sole authority to commit a causally coupled state transition

<!-- status-facts
write_scopes_enforced: true
read_scopes_enforced: false
-->

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
- Discovery, applicability checks, declared consequences, process progress, and process triggers are read-only. The coordinator invokes them against detached world state and treats a mutation as an authority violation rather than allowing it to reach canonical state.
- Effect application receives detached world state. Mechanics may propose only material changes within their declared authority; they do not own the world revision or causal history.
- `revision`, command records, and causal events are coordinator-owned. Rule code cannot advance the revision, append or rewrite history, or use a rejected candidate to modify already-committed history.
- Applicability rules, permissions, contracts, pricing rules, and institutions may inspect state and propose effects. They may not commit effects belonging to an enclosing transition that can still fail.
- The coordinator validates all causally coupled effects before committing any of them, then attaches the accepted command/event history itself.
- A refusal leaves canonical state unchanged, except for separately modeled causal events whose occurrence is independent of the refused transition.
- Successful commit records the accepted operations, relevant checks, commit order, and resulting persistent state identity.
- Derived interpretations may observe the committed history but cannot reapply its effects.

This is not a requirement for universal ACID transactions. Independent actions may commit independently. The singular boundary applies when several effects belong to one claimed causal transition.

## Examples

Two voluntary gives are independent transitions. Robin may give a spear and Friday may renege on giving coconuts. A derived `exchange` view can recognize the reciprocal history but cannot transfer either asset again.

An installed escrow release is one institutionally coupled transition. Asset release, payment, and escrow-state changes either pass validation and commit together or refuse together.

A pressure check may propose vessel damage, capability revocation, fluid release, and relation handoff as one coupled transition when the selected mechanics profile defines them as consequences of the same rupture.
