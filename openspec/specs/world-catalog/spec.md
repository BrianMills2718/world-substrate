# world-catalog Specification

## Purpose
Keep created worlds privately accessible, preserve logical run identity and complete native continuation state, and support independent branches from completed saved rounds.

## Requirements

### Requirement: Durable private created-world library

Source: Brian’s 2026-11-13 world-library request; owner-only default inferred from existing authentication and the requirement not to publish other visitors’ unshared prompts.

The service SHALL persist successful owner-created world definitions before acknowledging their catalog save. Stable catalog identity SHALL be distinct from immutable simulation bundle identity and content fingerprint. Existing owner authentication SHALL protect catalog listing, world/run records, checkpoints and private scene requests. Public sharing SHALL remain explicit; guest/IP bookkeeping SHALL NOT establish ownership. Storage failure SHALL NOT be reported as a successful durable save.

#### Scenario: Owner-created worlds remain available after reload

- **WHEN** an authenticated owner creates a valid world and later reloads the starting page
- **THEN** the same saved world is available in Your worlds with its definition and runs
- **AND** unauthenticated requests cannot list or read that private catalog

#### Scenario: Persistence failure is visible

- **WHEN** saving a generated world or completed run checkpoint fails
- **THEN** the service reports failure rather than acknowledging durable progress
- **AND** existing stored history remains intact

### Requirement: Logical runs and completed checkpoints

Source: Brian’s 2026-11-13 play/replay/branch request and explicit saved-round-first answer; checkpoint completeness derived from the existing native continuation contract.

World definitions, logical runs, request segments, public shares and checkpoints SHALL retain distinct identities. A saved checkpoint SHALL bind the exact world/rules, final material snapshot, actor state/memory, reviewed rulings/approval and applicable continuation metadata. New catalog run segments SHALL identify their preceding checkpoint; stale continuation SHALL be rejected before native work in the deployed service process. Durable append SHALL validate ancestry. An explicit terminal response with zero new rounds SHALL preserve the current checkpoint and record finish metadata without fabricating progress.

#### Scenario: Continue restores a saved run

- **WHEN** the owner continues a catalog run from its latest complete checkpoint
- **THEN** the native runner receives that checkpoint’s exact state, memory and reviewed authority
- **AND** the completed segment is durably appended before success
- **AND** a stale competing checkpoint request does not append divergent history

#### Scenario: A completed world produces no fictitious checkpoint

- **WHEN** the native runner reports an explicit terminal outcome without a new round
- **THEN** the run records that terminal outcome and retains its previous checkpoint
- **AND** the UI does not claim that another round occurred

### Requirement: Independent saved-round branches

Source: Brian, 2026-11-13, selects saved-round branches first; natural-language interventions and starting-condition configuration are future features.

A branch SHALL begin from an existing complete round checkpoint under the same reviewed rules and preserved actor memories. It SHALL have independent logical run identity, exact parent/checkpoint provenance and the retained parent history prefix. Appending a child SHALL NOT mutate parent state/history or conflate equal local event IDs across runs. A material event projection alone SHALL NOT be accepted as a cognitive checkpoint. Legacy recovery SHALL use provable owner/build/record data only, without inventing parentage or missing state; unavailable continuation SHALL have an explicit reason.

#### Scenario: Branching preserves the parent

- **WHEN** the owner branches from a saved completed round and continues the child
- **THEN** the child starts with the checkpoint’s state and actor memory
- **AND** its new segment belongs to the child while the parent and prefix remain unchanged

#### Scenario: Incomplete historical recordings remain replayable

- **WHEN** a historical recording lacks a complete resumable checkpoint
- **THEN** it can be replayed with its retained evidence
- **AND** Continue and Branch are unavailable with a truthful explanation
