# Mechanic profile contract v0

**Status:** partially implemented — `src/world_substrate/profile.py` implements the package, the installer checks below, and profile freezing; `src/world_substrate/assay.py` implements step 5's interaction assays. The `semantic_bindings`, `emits`, `effects`, and `trace_contract` fields are declared and reviewed but not machine-validated.  
**Purpose:** define the reviewable unit that an offline mechanics agent may author and an installer may freeze for a simulation run

<!-- status-facts
declared_reader_assay_detects_an_overlap: true
-->

## Mechanic package

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

## Installation

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

## Agent-authored output

A mechanics agent may produce source code or a declarative package offline. Its output is never installed merely because it parses or passes isolated unit tests. Installation requires reviewable authority, effects, interaction evidence, and limitations. Runtime law revision is outside v0.
