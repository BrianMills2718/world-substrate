# mechanic-installation Specification

## Purpose

The mechanic package an offline mechanics agent may author and the installer checks that admit and freeze it for one run.

**Mechanic profile contract v0** (folded on 2026-11-09 from `docs/contracts/mechanic-profile-v0.md`, given in its Status line, last commit `60b3f6b`):

**Status:** partially implemented — `src/world_substrate/profile.py` implements the package, the installer checks below, and profile freezing; `src/world_substrate/assay.py` implements step 5's interaction assays. The `semantic_bindings`, `emits`, `effects`, and `trace_contract` fields are declared and reviewed but not machine-validated.  
**Purpose:** define the reviewable unit that an offline mechanics agent may author and an installer may freeze for a simulation run

<!-- status-facts
declared_reader_assay_detects_an_overlap: true
-->

## Requirements

### Requirement: Mechanic package

Each mechanic declares:

| Field | Meaning |
| --- | --- |
| `mechanic_id`, `version` | Stable installed identity |
| `semantic_bindings` | Linguistic Core senses, roles, specializations, and causal class |
| `causal_bearer` | Agent action, process, disposition, institution, or exogenous injection |
| `requires` | State, components, relations, and conditions required for applicability |
| `optional_modifiers` | Recognized state that changes behavior when present |
| `forbids` | Explicit incompatible conditions, not a closed global component schema |
| `reads` | State paths the mechanic may inspect |
| `writes` | State paths the mechanic may propose changing |
| `emits` | Observations, events, or scheduled work it may emit |
| `effects` | Proposed transition operations; validation performs no canonical mutation |
| `invariants` | Goal-relative postconditions and accounting rules |
| `dependencies` | Mechanics and state surfaces believed consequential |
| `unsupported_interactions` | Known combinations that refuse, warn, or require refinement |
| `representation` | Deterministic, stochastic, empirical, scripted, external, model-mediated, or other declared form |
| `limits` | Preserved distinctions, omissions, assumptions, and invalid questions |
| `tests` | Positive, refusal, boundary, interference, and double-application cases |
| `trace_contract` | Required explanation when the mechanic applies, refuses, or fails |

Entities remain open to unrelated components. A mechanic has closed local authority: state outside its declared reads and writes may coexist but cannot be inspected or changed by that mechanic.

Source: inferred by agent (mechanic profile contract v0, applying Decision 003, accepted 2026-09-02; the decider is not recorded)

#### Scenario: A mechanic is declared as a package

- **WHEN** an offline mechanics agent authors a mechanic
- **THEN** the package declares its `mechanic_id` and `version`, semantic bindings, causal bearer, requires, optional modifiers, forbids, reads, writes, emits, effects, invariants, dependencies, unsupported interactions, representation, limits, tests and trace contract
- **AND** the installer's `validate_package` refuses a package with no `mechanic_id` or `version`, with an unknown `representation`, or with no declared tests

#### Scenario: Local authority is closed

- **WHEN** a mechanic runs
- **THEN** it can inspect and change only the state paths in its declared reads and writes
- **AND** state outside them may coexist on the same entities but is neither inspected nor changed by that mechanic

### Requirement: Installation

An installer must:

1. resolve semantic and mechanic identities;
2. validate all declared state paths and operations;
3. reject overlapping writes **between mechanics that can commit on the same
   occasion** without declared ordering, arbitration, or composition. Two
   independent actions writing one path is ordinary and is already serialised
   by the transition envelope; the rule bites for processes, which share one
   `advance()` and are ordered only by `order`. Read without that qualifier
   this step rejects the promoted M1 mechanics, since `fill` and `drink` both
   write `entities.<vessel>.liquid`;
4. check dependency references and declared enforcement coverage;
5. run the mechanic's tests plus selected interaction assays;
6. record limitations and unsupported interactions in the installed profile; and
7. freeze a profile identity before the run.

Passing installation does not prove global causal closure. It proves only that the declared contract is internally valid and that the selected assays passed.

Source: inferred by agent (mechanic profile contract v0, applying Decision 003, accepted 2026-09-02; the decider is not recorded)

#### Scenario: Installation checks run before the profile freezes

- **WHEN** a package is installed into a profile
- **THEN** the installer resolves its identities, validates its declared state paths, checks that its dependencies are installed, records limits and unsupported interactions, and refuses it with a `reject` finding if any check fails
- **AND** the caller runs the mechanic's tests and the selected interaction assays (`world_substrate.assay`) before freezing a profile identity for the run

#### Scenario: Two processes write one path

- **WHEN** two mechanics that commit on the same occasion (processes sharing one `advance()`) at the same `order` write overlapping paths, and neither names ordering, arbitration or composition
- **THEN** the second is rejected as `overlapping_write_without_arbitration`
- **AND** two independent actions that write one path are not rejected, because the transition envelope already serialises them

#### Scenario: Passing is not proof of closure

- **WHEN** a package passes installation
- **THEN** that proves only that its declared contract is internally valid and that the selected assays passed, not global causal closure

### Requirement: Agent-authored output

A mechanics agent may produce source code or a declarative package offline. Its output is never installed merely because it parses or passes isolated unit tests. Installation requires reviewable authority, effects, interaction evidence, and limitations. Runtime law revision is outside v0.

Source: inferred by agent (mechanic profile contract v0, applying Decision 003, accepted 2026-09-02; the decider is not recorded)

#### Scenario: Output that parses is not installed

- **WHEN** a mechanics agent produces source code or a declarative package offline, and it parses or passes isolated unit tests
- **THEN** it is not installed on that evidence alone; installation requires reviewable authority, effects, interaction evidence and limitations
- **AND** revising laws at runtime is outside v0
