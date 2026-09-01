---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-08-31
---

# World Substrate living roadmap

**Authority:** user-approved project direction in [Decision 001](../docs/decisions/001-project-scope.md)
**Selected path:** durable solo; one writer, reversible local work, no external effects
**Stage:** prototype
**Consumer:** a fresh authorized implementation agent needs the outcome, invariants, evidence frontier, active slice, and next action without a handoff
**Last outcome-bearing update:** M1 cooled-and-poured consumer path, in the revision containing this page

## Outcome and success criteria

For a substrate developer during M1, and a data-oriented world author after M3, change the recurring task of hand-coding isolated agent actions and narrating missing consequences into a reviewable workflow that defines typed world state, registers reusable deterministic actions/processes, generates current affordances, runs LLM or human choices, and retains exact causal evidence and replay.

The project succeeds at prototype stage when:

1. one reference world runs end to end through neutral substrate contracts;
2. the same world accepts LLM-selected actions without giving the model consequence authority;
3. a second materially different world reuses the core and adds mechanisms through explicit registered rules;
4. unsupported behavior and incomplete causal closure remain visible; and
5. retained commands reproduce canonical state and events exactly.

These criteria do not claim universal physics, unlimited affordances, real-world calibration, or predictive validity.

## Canonical outcome probe

**Starting state:** two actors, one persistent clay vessel, one separate metal cup, a finite pathogen-bearing fresh-water source, one finite-fuel fire, and registered ownership, container, liquid, heat, material, and process rules.

**Operation:** the scripted M1 controller selects discovered fill, heat, unheat, pour, drink, take, and give actions for one actor while the runner advances canonical time; heating, boiling, evaporation, cooling, hydration decay, and fuel consumption run as registered processes. M2 replaces the scripted selector with a genuine policy consumer without changing consequence authority.

**Inspectable result:** one trace shows finite water and fuel consumption; heat, pathogen, evaporation, and volume changes; the same vessel identity crossing systems and ownership; automatic processes; checks; before/after values; and an exact replay hash.

**Negative cases:** overfilling fails atomically; a valid typed pressure action envelope returns `unsupported_action` because pressure mechanics are absent, while a malformed envelope returns `invalid_action`.

**Evidence step-down:** human-readable trace -> causal events -> typed commands and state deltas -> pinned rule/content versions -> replay comparison.

## Current truth

- This repository now owns the project goal, architecture, core contract, source dispositions, and roadmap.
- The neutral runtime path now reaches the pinned cooled-and-poured checkpoint through registered fill, heat, unheat, and pour rules; clock, hydration, thermal, evaporation, pathogen-removal, cooling, and fire-fuel processes; state-derived discovery; causal events; semantic donor comparison; and exact replay.
- Castaway `world-systems` remains implementation authority for drinking, ownership transfer, and other freshwater mechanisms beyond the adopted pour prefix.
- Cybernetic Influence V3 has broader authoring and transition machinery, but its product and consequence-authority choices differ.
- Linguistic Core supplies reviewed vocabulary, not executable mechanics.
- No public deployment, paid model execution, second reference world, or scale target is authorized or required now.

## Applicable context

- **Approved:** [Decision 001](../docs/decisions/001-project-scope.md) selects one canonical repository and the deterministic-consequence boundary.
- **Working evidence:** the pinned Castaway vertical and Cybernetic Influence V3 capability seams in [source dispositions](../docs/source-dispositions.md).
- **Research input:** the Dwarf Fortress and Dynamical Laboratory syntheses inform design but do not authorize implementation claims.
- **Historical:** Castaway main and Cybernetic Influence's archived topology plan remain provenance, not current direction.

## Constraints and authorities

The user owns the outcome, deterministic-consequence boundary, public/external actions, spend, and later selection of a second reference world. This roadmap owns sequence and active local work. Architecture and contracts own their narrower boundaries. Donor repositories remain read-only.

### Architecture and capability invariants

```text
observed trace
  <- typed action + automatic processes
  <- canonical state + registered rules
  <- content + ontology bindings
  <- pinned donor definitions and implementation
```

| Capability | Canonical owner or seam | Dependency | Current evidence | State |
| --- | --- | --- | --- | --- |
| Project direction | this roadmap | Decision 001 | repository documents | established |
| Canonical-state/rule contract | [core contract](../docs/contracts/core-v0.md) | Castaway behavior donor | first-fill, boiling, and pour tests/evidence | partially implemented |
| Physical reference vertical | shared core + Castaway reference data | Castaway `world-systems` | [first-fill](../evidence/m1/first-fill-v0.json), [boiling](../evidence/m1/boiling-v0.json), and [pour](../evidence/m1/pour-v0.json) evidence plus donor tests/traces | pour prefix adopted; remainder donor-only |
| Policy selection | future policy adapter | shared `llm_client` | donor real run | not adopted here |
| Authoring/causal closure | future compiler | CI V3 patterns | donor implementation/research | not adopted here |
| Ontology bindings | content adapter | Linguistic Core | pinned Castaway subset | donor-only |
| Experiment/evaluation | future evaluation package | Dynamical Laboratory methods | research specification | deferred |

## Vertical slices and current work

### Milestone horizon

| Milestone | Planning state | Inspectable output | Promotion or replan trigger |
| --- | --- | --- | --- |
| M0: canonical project foundation (enabling) | fully_specifiable_now | one repository with goal, wiki, architecture, contract, sources, roadmap, and checks | complete; checks pass, but this is enabling rather than stakeholder-outcome evidence |
| M1: neutral freshwater vertical | fully_specifiable_now | local CLI trace and exact replay through neutral contracts | promote after positive and negative cases match donor behavior |
| M2: genuine policy consumer | conditional | one traced shared-`llm_client` actor choosing from the same affordances | begin after M1 freezes the observation/action seam and model-call authority is confirmed |
| M3: authoring and causal-closure review | conditional | data-defined variation compiles with exact/descriptive/unsupported coverage | begin after M1 reveals the minimum stable rule/content contract |
| M4: second reference world | human_decision_required | materially different world reusing the core | select domain after M1/M3 show which mechanism family best tests generality |
| M5: scale frontier | exploration_required | repeatable candidate/context/storage measurements at a selected target | activate when a real reference world exceeds current linear/simple designs |
| M6: dynamical evaluation | deliberately_deferred | perturbation and trajectory analysis over retained worlds | activate when it can change a mechanism or representation decision |

### Active slice: M1 neutral freshwater vertical

**Visible result:** from this repository, one command creates the canonical freshwater starting state, executes the recorded action sequence, writes a human-readable and machine-readable causal trace, and verifies exact replay.

**Donor inputs:**

- `../castaway-world-systems/src/castaway/models.py`;
- `engine.py`, `physical.py`, `discovery.py`, and `storage.py`;
- relevant world/content definitions;
- freshwater, saltwater, overfill, process, ownership, and replay checks;
- curated donor evidence for expected behavior.

**Target boundaries:**

- `src/world_substrate/`: neutral state, rule registry, engine, discovery, event, and replay seams;
- `src/world_substrate/mechanisms/`: reusable container, liquid, heat, material, ownership, and process rules;
- `reference_worlds/castaway/`: Castaway content and the freshwater scenario;
- `tests/`: contract, interaction, rejection, and replay evidence;
- `artifacts/`: ignored generated runs, with only compact curated evidence retained later.

**Implementation constraints:**

- no Castaway-specific object name in shared rule dispatch;
- no model import in state, rules, processes, or replay;
- ontology IDs remain provenance/bindings, not dispatch authority;
- integer or otherwise exact extensive quantities for conservation;
- one state/time authority and atomic commit;
- unsupported pressure remains explicit;
- maintained architecture views use implemented identifiers and interfaces once
  those exist, identify their source revision and status, and never substitute
  diagram coherence for trace or replay evidence;
- donor repositories remain unmodified.

**Focused checks and authentic observation:**

1. run the donor freshwater case and capture its expected final state/event ledger;
2. run the equivalent World Substrate case;
3. compare conserved quantities, process timing, vessel identity, final state, and replay;
4. run saltwater retention, overfill rejection, and unsupported-pressure counterexamples;
5. inspect the produced trace directly; and
6. trace each exercised rule ID through its operation, positive or negative
   check, retained observation, and donor mapping.

A scripted chooser is sufficient for M1 because the uncertainty is consequence composition. It is explicitly labeled and does not establish the LLM-policy criterion.

**Failure and reset boundary:** if the neutral seam requires named Castaway branches, duplicates state/time authority, or cannot reproduce the donor trace without weakening evidence, stop widening the abstraction and revise [the core contract](../docs/contracts/core-v0.md). The donor remains intact and authoritative.

## Later work

M2 through M6 remain conditional. Do not prebuild generalized authoring, a UI, a plugin system, economics, organizational simulation, continuous terrain, or Concordia integration before M1 evidence identifies a real seam.

## Decisions and assumptions

| Choice | Disposition | Reason | Boundary |
| --- | --- | --- | --- |
| One new canonical repository | human_set | approved consolidation goal | project authority |
| LLM/humans choose; rules determine effects | human_set | central project thesis | consequence authority |
| Castaway is the first reference donor | human_set | approved source role | first vertical |
| Repository name `world-substrate` | agent_decided_reversible | clear neutral identity | filesystem/project name |
| Python-first extraction | agent_decided_reversible | donors and dependencies are Python; minimizes migration risk | M1 implementation |
| No bulk source imports | agent_decided_reversible | prevents duplicate authority and premature coupling | source management |
| Deterministic-only M1 | agent_decided_reversible | tests the accepted hard boundary first | transition rules |
| Seeded stochastic rules | human_required_later | unnecessary for M1 | future core |
| Second reference-world domain | human_required_later | evidence should inform the choice | M4 |

## Evidence and review artifacts

| Claim | Evidence | Limitation | Status |
| --- | --- | --- | --- |
| Related sources are classified and revision-bound | [source manifest](../references/sources.json) | local paths are machine-specific | established |
| Project navigation is progressively disclosed | structural checker and Project Meta navigation validator | structure does not prove semantic truth | passed at this revision |
| Castaway behavior exists | donor tests and evidence at pinned revision | not yet adopted here | external evidence |
| Freshwater behavior is characterized locally | [pinned fixture](../tests/fixtures/castaway/freshwater-v0.json) and extractor `--check` | expected donor behavior only | established |
| Neutral fill-through-pour path works | [first-fill](../evidence/m1/first-fill-v0.json), [boiling](../evidence/m1/boiling-v0.json), and [pour](../evidence/m1/pour-v0.json) evidence, executable probes, and focused tests | drinking and ownership transfer remain donor-only | established |
| Full neutral freshwater core works | complete M1 trace, checks, and replay | pour-prefix evidence covers only a bounded subset | open |
| LLM policy works through neutral seam | M2 provider trace | no claim from scripted M1 | conditional |

## Risks and needs resolution

- A premature generic component model could become an untyped property bag; M1 must keep explicit components and rule contracts.
- Copying donor implementations without a consumer-path proof would create parallel authorities.
- One physical vertical cannot prove cross-domain generality; that claim remains blocked until M4.
- Typed causal-closure checks cannot prove the author remembered every consequential dependency.
- Whether maintained architecture views should be generated from contracts and
  code or maintained manually remains open until M1 reveals stable identifiers
  and interfaces.
- A UML, SysML, or KerML toolchain is deferred unless observed cross-view
  inconsistency justifies its added authority and maintenance cost.
- Documentation can outrun implementation; the exact next action remains an executable trace, not another planning layer.

## Human decisions

None required for M0 or M1. Seeded randomness, the second reference world, paid model calls, deployment, and publication remain later human boundaries.

## Refresh and reset triggers

Refresh this roadmap after a committed outcome-bearing slice, a material user correction, a donor revision change selected for adoption, or evidence that invalidates the core contract. Replan rather than accumulate infrastructure after two consecutive non-vertical increments or when the user-visible outcome is no longer clear.

## Exact next action

Implement the registered drink action and rule-defined hydration/harm accounting
needed to reach and compare the pinned post-drink checkpoint. Preserve exact
consumption ledgers and cooling. Do not add take, give, policy calls, or UI in
that slice.
