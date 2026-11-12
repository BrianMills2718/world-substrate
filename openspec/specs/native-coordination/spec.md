# native-coordination Specification

## Purpose

The first native Waltzman coordination vertical: one-shot authoring from a description, a bounded change-one-condition comparison, and the diagnostic bundle every run is debugged from. Landed on main 2026-10-05 in #75, #79 and #80.

**Native coordination one-shot authoring v0** (folded on 2026-11-09 from `docs/contracts/native-coordination-authoring-v0.md`, status `proposed`, reviewed through 2026-09-19, last commit `bbaeaf4`):

This contract defines the bounded natural-language front door for the first
native Waltzman release. It does not define arbitrary-world generation or
conversational refinement.

**Native coordination comparison v0** (folded on 2026-11-09 from `docs/contracts/native-coordination-comparison-v0.md`, status `proposed`, reviewed through 2026-09-19, last commit `91878f4`):

This contract defines the first bounded "change one condition and compare"
interaction for native Waltzman delivery.

**Native coordination diagnostic bundle v0** (folded on 2026-11-09 from `docs/contracts/native-coordination-diagnostics-v0.md`, status `proposed`, reviewed through 2026-09-18, last commit `91878f4`):

The first native Waltzman coordination vertical is debugged from retained evidence rather than from UI summaries or model prose.

This contract is deliberately narrow. It applies to the deterministic structured coordination fixtures in `examples/native_coordination/` and does not define a general experiment framework.

## Requirements

### Requirement: Authoring: Product path

The v0 path is:

```text
one description
  -> versioned native-coordination draft
  -> deterministic World Substrate authoring bundle
  -> requirement / assumption / unsupported-intent review
  -> shared reviewed coordination mechanics
  -> explicit mechanics approval
  -> native World Substrate Engine execution
  -> automatic Living Scene
```

The original description is retained exactly in the draft artifact.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: One description becomes a native run

- **WHEN** a visitor gives one description to the one-shot path
- **THEN** it becomes a versioned native-coordination draft, then a deterministic authoring bundle, then a requirement, assumption and unsupported-intent review, then the shared reviewed coordination mechanics, then explicit mechanics approval, then native Engine execution and an automatic Living Scene
- **AND** the original description is retained exactly in the draft artifact

### Requirement: Authoring: Model authority

The model proposes configuration only:

- world label, summary, and location;
- 3-6 represented members and roles;
- one uniquely authorized member;
- exactly four represented prerequisites/resources;
- exactly one restorable prerequisite that begins below its requirement;
- direct represented reports with distinct recipients;
- an approval threshold;
- extracted requirement coverage;
- explicit assumptions; and
- explicit unsupported requests.

The model does **not** author executable law, Python, write scopes, or causal
effects in this path.

The executable family remains the reviewed shared native coordination model:

- `coordination.action.communicate`;
- `coordination.action.approve`;
- `coordination.action.intervene`; and
- `coordination.action.finalize`.

The deterministic draft compiler produces the ordinary
`world-substrate-authoring-bundle/v0` consumed by the existing compiler and
Engine.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: The model proposes configuration only

- **WHEN** the model proposes a world
- **THEN** it supplies the world label, summary and location, 3-6 members and roles, one uniquely authorized member, exactly four prerequisites, exactly one restorable prerequisite that begins below its requirement, direct reports with distinct recipients, an approval threshold, extracted requirement coverage, assumptions and unsupported requests
- **AND** the draft is refused for more than one authorized member, a second unhealthy resource, duplicate report recipients, fewer than two reports, a generated delivery id collision, or unknown model fields

#### Scenario: No model-written law

- **WHEN** the deterministic draft compiler builds the world
- **THEN** it produces an ordinary `world-substrate-authoring-bundle/v0`, and the model authors no executable law, Python, write scopes or causal effects
- **AND** the executable family is the shared reviewed model with exactly `coordination.action.communicate`, `.approve`, `.intervene` and `.finalize`

### Requirement: Authoring: Intent completeness boundary

The review distinguishes:

- extracted requirements and the represented surface assigned to each;
- inferred assumptions;
- explicitly unsupported requests; and
- compiler-derived executable mechanics.

Requirement coverage is review evidence, not proof that every material clause
in the description was extracted correctly. The UI must preserve the original
description so a user can compare it with the inferred structure.

Unsupported requests must remain visible. The v0 path may visibly narrow them;
it must not silently convert them into narration or pretend they execute.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: The review separates what is known

- **WHEN** the review is shown
- **THEN** it distinguishes extracted requirements and the represented surface assigned to each, inferred assumptions, explicitly unsupported requests, and compiler-derived mechanics, and keeps the original description visible so a user can compare it with the inferred structure
- **AND** requirement coverage is review evidence, not proof that every material clause was extracted correctly

#### Scenario: An unsupported request

- **WHEN** the description asks for something unsupported (for example "Use probabilistic delivery delays.")
- **THEN** it stays visible with status `unsupported` and no implementing mechanic
- **AND** the path narrows it visibly and does not turn it into narration or pretend it executes

### Requirement: Authoring: Supported family

The first release intentionally supports one bounded coordination family:

- 3-6 members in one shared coordination space;
- exactly four prerequisites/resources;
- one unique intervention authority;
- one restorable prerequisite initially below requirement;
- at least two direct source-to-recipient represented information deliveries;
- unique report recipients sufficient to cover the approval threshold and one alternate threshold;
- member approval;
- represented prerequisite restoration; and
- gate finalization.

Arbitrary scheduling, probabilistic behavior, deception, hidden cognition,
custom institution semantics, generalized activities, and arbitrary generated
mechanics are outside this one-shot path unless separately represented and
reviewed by a later contract.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: Inside the supported family

- **WHEN** a description fits 3-6 members in one shared space, exactly four prerequisites, one unique intervention authority, one restorable prerequisite initially below requirement, at least two direct information deliveries with unique report recipients enough to cover the approval threshold and one alternate threshold, member approval, restoration and gate finalization
- **THEN** the one-shot path can represent it

#### Scenario: Outside the supported family

- **WHEN** a description needs arbitrary scheduling, probabilistic behavior, deception, hidden cognition, custom institution semantics, generalized activities or arbitrary generated mechanics
- **THEN** this one-shot path does not provide it unless a later contract represents and reviews it

### Requirement: Authoring: Approval and staleness

Generating a draft does not approve mechanics.

The Builder receives the exact shared causal model and compiler-derived review,
sets `mechanicsApproved=false`, and requires the ordinary explicit approval
before a run.

The generated bundle is editable. If it changes after draft/mechanics review,
the review is marked stale and mechanics approval is invalidated. The original
description, requirement review, and assumptions remain provenance for the
generated version rather than silently changing to describe later edits.

If a user replaces the shared mechanics through the generic mechanics
generator, execution returns to the generic authored-world path. It may not
continue to claim native-coordination execution.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: A draft is not an approval

- **WHEN** a draft is generated
- **THEN** the Builder receives the exact shared causal model and compiler-derived review, sets `mechanicsApproved=false`, and requires the ordinary explicit approval before a run

#### Scenario: Editing the generated world

- **WHEN** the generated bundle is changed after draft or mechanics review
- **THEN** the review is marked stale and mechanics approval is invalidated, while the original description, requirement review and assumptions remain provenance for the generated version
- **AND** if a user replaces the shared mechanics through the generic mechanics generator, execution returns to the generic authored-world path and no longer claims native-coordination execution

### Requirement: Authoring: Execution authority

A one-shot native draft uses explicit
`execution_mode="native_coordination"`.

The service accepts that mode only when:

1. the authoring bundle validates;
2. the causal model compiles against the bundle;
3. the supplied causal model exactly equals the reviewed shared coordination
   causal model;
4. mechanics approval is explicit; and
5. policy is the deterministic scripted native path.

The native runner remains the same Engine/Living Scene path proven by the
native coordination vertical. Provider spend for execution is zero.

Generic authored worlds keep `execution_mode="authored_world"` and the
existing scripted/LLM policy seam.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: The service accepts native execution

- **WHEN** a request uses `execution_mode="native_coordination"` with a bundle that validates, a causal model that compiles against it and exactly equals the reviewed shared coordination model, explicit mechanics approval, and the deterministic scripted policy
- **THEN** the service runs the native runner, the same Engine and Living Scene path, at zero provider spend

#### Scenario: The service refuses native execution

- **WHEN** the causal model differs from the reviewed shared model, or the policy is not scripted
- **THEN** the request is refused (for example "native_coordination execution requires the reviewed shared coordination mechanics")
- **AND** generic authored worlds keep `execution_mode="authored_world"` and the existing scripted and LLM policy seam

### Requirement: Authoring: Provider spend

One-shot extraction shares the World Builder's existing server-side rate limit
and daily spend ledger. Draft generation has its own bounded per-request cap.

A provider failure after reservation fails closed and charges the reserved
amount under the existing budget-ledger semantics.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: Extraction spend is limited and fails closed

- **WHEN** one-shot extraction runs
- **THEN** it shares the World Builder's server-side rate limit and daily spend ledger and has its own bounded per-request cap
- **AND** a provider failure after reservation fails closed and charges the reserved amount under the existing budget-ledger semantics

### Requirement: Authoring: Debugging evidence

The Builder log records the complete `/generate-draft` request and response,
including:

- retained draft;
- compiled authoring bundle;
- shared causal model;
- requirement/assumption review;
- model and cost;
- daily committed cost; and
- trace id.

The subsequent `/run` response retains the Engine trace and Living Scene HTML
through the existing log surface.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: The log keeps the whole draft exchange

- **WHEN** `/generate-draft` completes
- **THEN** the Builder log records the complete request and response, including the retained draft, compiled authoring bundle, shared causal model, requirement and assumption review, model and cost, daily committed cost and trace id
- **AND** the later `/run` response retains the Engine trace and Living Scene HTML through the existing log surface

### Requirement: Authoring: First verification

The focused static/runtime suite for this contract is:

```bash
python -m pytest \
  tests/test_native_coordination_authoring.py \
  tests/test_world_builder_service.py \
  tests/test_world_authoring_builder.py
```

This does not replace the native coordination Linux gate from
`native-coordination-diagnostics-v0.md`. Until that underlying gate is
executed, this stacked slice remains unverified end to end.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

#### Scenario: The focused suite

- **WHEN** `tests/test_native_coordination_authoring.py`, `tests/test_world_builder_service.py` and `tests/test_world_authoring_builder.py` are run with pytest
- **THEN** they are the focused static and runtime checks for this contract
- **AND** they do not replace the native coordination Linux gate, so until that gate is executed this stacked slice is unverified end to end

### Requirement: Comparison: Purpose

After a user has explicitly approved the shared native coordination mechanics
and completed one native run, the Builder may create one comparison run without
discarding or rewriting the original.

The v0 comparison changes exactly one supported initial condition:

```text
gate.required_approvals
```

No executable rule, information record, actor authorization, resource state,
event, command, or prior trace is edited in place.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A comparison after one approved run

- **WHEN** a user has approved the shared native mechanics and completed one native run, and asks for a comparison
- **THEN** the Builder creates one comparison run that changes exactly one supported initial condition, `gate.required_approvals`, without discarding or rewriting the original
- **AND** no executable rule, information record, actor authorization, resource state, event, command or prior trace is edited in place

### Requirement: Comparison: Baseline retention

When a fresh run succeeds, the Builder retains:

- the exact initial authoring bundle used for that run;
- the exact approved causal model;
- the execution mode;
- the returned trace;
- the returned Living Scene HTML; and
- the service trace id.

Starting a comparison does not clear those objects.

A comparison failure also leaves the baseline visible.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: The baseline survives

- **WHEN** a fresh run succeeds
- **THEN** the Builder retains the exact initial authoring bundle, the exact approved causal model, the execution mode, the returned trace, the returned Living Scene HTML and the service trace id
- **AND** starting a comparison does not clear them, and a comparison failure also leaves the baseline visible

### Requirement: Comparison: Supported intervention

The comparison request sends the retained baseline bundle and requested threshold to the service. The service clones and validates the baseline, applies the one supported mutation, recompiles the shared causal model against the resulting comparison bundle, and only then executes it.

It may replace only:

```text
entities.<gate>.components.gate.required_approvals
```

The new threshold must:

- be an integer;
- be at least 1;
- be no greater than the number of represented informed report recipients; and
- differ from the retained baseline threshold.

The service counts an informed recipient only through a represented delivery whose `recipient_id` names a represented member and whose `info_id` names represented information. The retained baseline threshold must itself be within that supported informed-recipient count; malformed or impossible baselines are refused before the comparison run.

The one-shot authoring family requires at least two distinct report recipients
so every generated first-release world has at least one alternate valid
threshold.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A valid new threshold

- **WHEN** a comparison request sends the retained baseline bundle and a threshold that is an integer, at least 1, no greater than the number of informed report recipients, and different from the baseline's
- **THEN** the service clones and validates the baseline, replaces only `entities.<gate>.components.gate.required_approvals`, recompiles the shared causal model against the new bundle, and only then executes it (a baseline of 2 changed to 1 gives a second fresh run)

#### Scenario: An invalid threshold or baseline

- **WHEN** the threshold equals the baseline, exceeds the informed recipient count or is not an integer, or the baseline threshold is itself above that count
- **THEN** the comparison is refused before the run
- **AND** a recipient counts as informed only through a delivery whose `recipient_id` names a represented member and whose `info_id` names represented information, so a delivery to a non-member or of a non-information entity does not count

### Requirement: Comparison: Mechanics authority

The comparison reuses the exact causal model retained with the approved
baseline.

It does not call mechanics generation and does not create new executable law.

The service still applies the ordinary native-coordination run boundary:

- the modified authoring bundle must validate;
- the causal model must compile against it;
- the causal model must exactly equal the reviewed shared coordination model;
- execution mode is `native_coordination`; and
- policy is deterministic scripted execution.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: The comparison reuses the approved law

- **WHEN** a comparison runs
- **THEN** it reuses the exact causal model retained with the approved baseline, does not call mechanics generation and creates no new executable law
- **AND** the ordinary native run boundary still applies: the modified bundle validates, the causal model compiles against it and equals the reviewed shared model, the mode is `native_coordination`, and the policy is deterministic scripted execution

### Requirement: Comparison: Fresh execution

A comparison is a second fresh Engine run. It is not:

- an edit of baseline commands or events;
- a fork that rewrites retained history;
- a post-hoc change to a Living Scene frame; or
- an analytic prediction of what would have happened.

The request log contains the complete comparison bundle, making the changed
initial condition inspectable.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A second run, not an edit

- **WHEN** a comparison runs
- **THEN** it is a second fresh Engine run, with the same mechanic profile id and zero provider spend, that differs in turns, accepted actions and final projection from the baseline
- **AND** it is not an edit of baseline commands or events, a fork that rewrites retained history, a post-hoc change to a Living Scene frame, or an analytic prediction

#### Scenario: The changed condition is inspectable

- **WHEN** the comparison request is logged
- **THEN** the request log contains the complete comparison bundle

### Requirement: Comparison: Presentation

The Builder keeps the baseline Living Scene visible and adds:

- baseline threshold and result summary;
- comparison threshold and result summary; and
- the comparison Living Scene.

The two traces remain separately inspectable in Full logs.

The UI may state the represented difference in outcomes. It may not claim that
the threshold is a real-world cause beyond the installed mechanics governing
these two represented runs.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: Two runs side by side

- **WHEN** a comparison finishes
- **THEN** the Builder keeps the baseline Living Scene visible and adds the baseline threshold and result summary, the comparison threshold and result summary, and the comparison Living Scene, with the two traces separately inspectable in Full logs
- **AND** the UI may state the represented difference in outcomes, but may not claim the threshold is a real-world cause beyond the installed mechanics of these two represented runs

### Requirement: Comparison: Limits

The v0 comparison surface does not yet support arbitrary state editing,
multi-variable experiments, probabilistic sweeps, sensitivity analysis,
automatic causal identification, or provider-generated intervention advice.

Those additions require separate contracts rather than extending this control
implicitly.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A comparison beyond one threshold

- **WHEN** someone wants arbitrary state editing, multi-variable experiments, probabilistic sweeps, sensitivity analysis, automatic causal identification or provider-generated intervention advice
- **THEN** the v0 comparison does not support it, and each needs its own contract rather than extending this control implicitly

### Requirement: Comparison: Verification

Focused verification:

```bash
python -m pytest \\
  tests/test_native_coordination_comparison.py \\
  tests/test_world_builder_service.py \\
  tests/test_world_authoring_builder.py
```

The comparison also depends on the native coordination runner and therefore
inherits the Linux verification gate from
`native-coordination-diagnostics-v0.md`.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: The focused comparison suite

- **WHEN** `tests/test_native_coordination_comparison.py`, `tests/test_world_builder_service.py` and `tests/test_world_authoring_builder.py` are run with pytest
- **THEN** they are the focused verification for this contract
- **AND** the comparison depends on the native coordination runner and so inherits the Linux verification gate from the diagnostics contract

### Requirement: Diagnostics: Acceptance authority

`examples/native_coordination/acceptance-v0.json` is the executable acceptance matrix for this slice.

Each world declares expected configuration facts such as participant count, approval threshold, information channels, the prerequisite that must block the first approval, the represented intervention resource, and the actor authorized to restore it.

The acceptance evaluator may compare those declared expectations to retained execution and presentation evidence. It must not mutate the world or substitute expected values for observed state.

A run is accepted only when all evaluated checks pass. A summary may say that acceptance passed; the individual retained checks remain the evidence.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A run is accepted on its checks

- **WHEN** the acceptance evaluator compares the declared expectations in `examples/native_coordination/acceptance-v0.json` (participant count, approval threshold, information channels, the prerequisite that must block the first approval, the intervention resource, the actor authorized to restore it) to retained execution and presentation evidence
- **THEN** the run is accepted only when all evaluated checks pass, and the individual retained checks remain the evidence
- **AND** the evaluator does not mutate the world or substitute expected values for observed state

### Requirement: Diagnostics: Diagnostic run identity

Every diagnostic run has one explicit `run_id`.

The run id joins:

- exact structured world input;
- exact causal-model input;
- compiler-derived mechanics review;
- canonical initial snapshot;
- canonical commands and events;
- contested-run trace;
- live projection;
- Living Scene profile and deterministic frames;
- rendered HTML;
- acceptance results; and
- the artifact hash manifest.

A deterministic local run has provider spend `0`. Future provider-backed authoring may add provider trace ids, but provider identity never replaces the World Substrate diagnostic run id.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: One run id joins the evidence

- **WHEN** a diagnostic run is made
- **THEN** its one explicit `run_id` joins the exact structured world input, causal-model input, compiler-derived mechanics review, initial snapshot, commands and events, contested-run trace, live projection, Living Scene profile and frames, rendered HTML, acceptance results and artifact hash manifest
- **AND** a deterministic local run has provider spend 0, and a provider trace id never replaces the diagnostic run id

### Requirement: Diagnostics: Required artifacts

A complete successful diagnostic directory contains:

```text
summary.json
input-bundle.json
causal-model.json
acceptance-matrix.json
mechanics-review.json
initial-snapshot.json
commands.json
events.json
trace.json
projection.json
living-profile.json
living-frames.json
render.html
acceptance.json
manifest.json
```

`summary.json` is an index, not the source of truth. It records run/world identity, current diagnostic stage, pass/fail state, failure category when present, mechanic profile id, provider spend, terminal state, event count, and projection final hash.

`acceptance-matrix.json` is the exact machine-readable promise set used for this run.

`mechanics-review.json` is compiler-derived authority review. It exposes the installed declarations' derived reads/writes, checks, effects, limits, tests, and terminal predicate.

`commands.json` and `events.json` are canonical Engine history. Rejected or failed attempts remain present. Actor observations and information context stay attached to their retained events according to the Engine contract.

Acceptance also requires exact `Engine.replay()` agreement: replayed commands must reproduce the same final material hash and the same retained event sequence. Replay is checked from Engine-owned history; presentation artifacts never participate in that proof.

`projection.json` is read-only canonical projection evidence. `living-profile.json`, `living-frames.json`, and `render.html` are downstream presentation evidence only.

For action feedback, Living Scene may project each retained check's public rule label and boolean verdict so a visitor can inspect both satisfied and failed checks. It must not copy retained `actual`/`expected` operands into the public presentation payload; those remain evidence-layer data because they may contain actor-scoped or otherwise non-public values.

`acceptance.json` records each acceptance assertion independently, with a stable id, category, pass/fail value, and observed/expected values when useful.

`manifest.json` records SHA-256 for every other retained artifact in the directory. It is generated last and does not hash itself.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A successful diagnostic directory

- **WHEN** a diagnostic run succeeds
- **THEN** its directory contains `summary.json`, `input-bundle.json`, `causal-model.json`, `acceptance-matrix.json`, `mechanics-review.json`, `initial-snapshot.json`, `commands.json`, `events.json`, `trace.json`, `projection.json`, `living-profile.json`, `living-frames.json`, `render.html`, `acceptance.json` and `manifest.json`
- **AND** `manifest.json` records the SHA-256 of every other artifact, is generated last, and does not hash itself

#### Scenario: Replay and presentation evidence

- **WHEN** acceptance is evaluated
- **THEN** `Engine.replay()` from Engine-owned history must reproduce the same final material hash and the same event sequence, and presentation artifacts never take part in that proof
- **AND** rejected or failed attempts remain in `commands.json` and `events.json`, and Living Scene may show each check's public label and pass or fail verdict but does not copy retained `actual` or `expected` operands into the public payload

### Requirement: Diagnostics: Failure categories

The v0 diagnostic taxonomy is intentionally small:

- `input` — structured bundle or acceptance expectation is invalid;
- `compiler` — causal declaration cannot compile/install under current authority rules;
- `mechanic_check` — installed checks allow or block the wrong represented attempt;
- `authority` — an installed rule crosses Engine/write-scope authority;
- `engine` — deterministic execution or terminal behavior is otherwise wrong;
- `information_visibility` — source/recipient/outsider authorization is wrong;
- `projection` — retained projection does not match canonical history/state;
- `renderer` — Living Scene profile/frame/render construction fails or omits required generic presentation;
- `acceptance` — execution completed but one or more declared product promises fail;
- `environment` — required execution infrastructure fails before the product path can be exercised.

Do not use a broad category to hide a more specific observed failure.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A failure gets the most specific category

- **WHEN** a diagnostic run fails
- **THEN** its category is one of `input`, `compiler`, `mechanic_check`, `authority`, `engine`, `information_visibility`, `projection`, `renderer`, `acceptance` or `environment`
- **AND** a broad category is not used to hide a more specific observed failure

### Requirement: Diagnostics: Stage discipline

The diagnostic command records its current stage before entering a major boundary:

```text
input
  -> compiler
  -> engine
  -> projection
  -> renderer
  -> acceptance
  -> complete
```

If an exception escapes, `summary.json` must still be written with the last entered stage, mapped failure category, exception type, and message. Successful artifacts already written before the failure are retained.

This is observability, not recovery authority. A diagnostic writer cannot edit canonical history to make a failed run pass.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: An exception escapes mid-run

- **WHEN** an exception escapes while the run is in a stage (input, compiler, engine, projection, renderer, acceptance)
- **THEN** `summary.json` is still written with the last entered stage, the mapped failure category, the exception type and message, and artifacts already written are retained (a broken compiler effect gives stage and category `compiler`, error type `ActionDeclarationError`)
- **AND** the diagnostic writer cannot edit canonical history to make a failed run pass

### Requirement: Diagnostics: Matrix command

`scripts/check_native_coordination.py` is the first-slice acceptance entry point. It runs every world declared in the acceptance matrix into its own diagnostic directory, writes `matrix-summary.json`, and requires every world to pass while reporting one identical frozen mechanic-profile id.

The matrix command therefore checks the milestone claim that materially different configurations use one reusable mechanics family; that claim is not inferred from similar source files.

Canonical Linux verification command:

```bash
python scripts/check_native_coordination.py \
  --output-root /tmp/world-substrate-native-coordination
python -m pytest \
  tests/test_native_coordination.py \
  tests/test_native_coordination_matrix.py \
  tests/test_runtime_component_replay.py
python scripts/check_project.py
```

The first command is expected to leave complete diagnostic evidence whether the matrix passes or a product boundary fails. The final two commands remain required before the implementation PR is ready to merge.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: The acceptance matrix runs

- **WHEN** `scripts/check_native_coordination.py` runs
- **THEN** it runs every world in the acceptance matrix into its own diagnostic directory, writes `matrix-summary.json`, and requires every world to pass while reporting one identical frozen mechanic-profile id
- **AND** that identical id is the check that materially different configurations use one reusable mechanics family, not an inference from similar source files

### Requirement: Diagnostics: Privacy and causal boundary

Direct/private represented information may appear in canonical evidence where actor-authorized observations legitimately contain it. The public Living Scene render receives no observer identity by default, so private message content must remain hidden there even when the represented transmission line itself is visible.

Information context and message delivery are not promoted into mechanic-declared causal ancestry.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: Private content stays out of the public render

- **WHEN** the public Living Scene is rendered, with no observer identity by default
- **THEN** private message content stays hidden even when the represented transmission line itself is visible
- **AND** information context and message delivery are not promoted into mechanic-declared causal ancestry

### Requirement: Diagnostics: Hashing and reproducibility

A diagnostic output directory is one immutable run identity. The runner refuses a nonempty target rather than deleting, resetting, or mixing prior evidence. Reruns use a fresh directory.

JSON artifacts are written deterministically with sorted keys and a terminal newline. The manifest hashes exact bytes on disk.

The deterministic coordination runner should therefore allow a later investigator to answer, from one directory:

1. what world was supplied;
2. what law was installed;
3. what each attempted transition checked;
4. what the acting participant could observe;
5. what committed or refused;
6. what canonical state resulted;
7. what the projection and UI received; and
8. which acceptance promise failed, if any.

The contract does not require a provider call, database, server, or bespoke per-world scene file.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

#### Scenario: A directory is one immutable run

- **WHEN** a diagnostic runner is pointed at a nonempty output directory
- **THEN** it refuses (a `FileExistsError`) rather than deleting, resetting or mixing prior evidence, leaving existing files untouched, and reruns use a fresh directory

#### Scenario: Artifacts are deterministic

- **WHEN** JSON artifacts are written
- **THEN** they have sorted keys and a terminal newline, and the manifest hashes the exact bytes on disk
- **AND** an investigator can answer from one directory what world was supplied, what law was installed, what each attempt checked, what the actor could observe, what committed or refused, what state resulted, what the projection and UI received, and which acceptance promise failed

### Requirement: Independent generated concern procedure

Fresh generated coordination worlds using the independent validation procedure SHALL represent actual technical condition, sourced claim, recipient exposure, actor-owned interpretation, expressed personal stance, recorded assent and institutional hold separately. Installed mechanics SHALL determine technical and institutional consequences; residents SHALL choose their own responses. A declared effective authorized intervention may change a condition, but elapsed review time or a report SHALL NOT establish successful repair. Historical scripted decision specifications SHALL retain their recorded semantics.

Source: Brian's implementation goal, 2026-11-12, attachment 4c960cc4-dfc1-41c9-9c30-71b9e2b7d4ca/pasted-text-1.txt; docs/model/modeling-choices.md, end-to-end single-concern scenario contract.

#### Scenario: Claims and delivery do not decide technical condition or assent

- **WHEN** an actor delivers a report, including an inaccurate report, to a declared recipient
- **THEN** delivery changes available evidence without changing the actual technical condition, personal stance, recorded assent or technical hold
- **AND** recipients may disagree, ignore the report, request investigation or retain support

#### Scenario: Passing revalidation clears only the technical hold

- **WHEN** an authorized review tests a failing condition
- **THEN** the recorded validation fails and the institutional technical hold remains active
- **WHEN** an authorized effective intervention repairs that condition and authorized revalidation passes
- **THEN** passing revalidation clears the technical hold without changing any actor's recorded assent or personal stance
- **AND** activation remains blocked until every required actor independently records assent

#### Scenario: Generated authoring preserves independent choice

- **WHEN** a fresh collective activation scenario is authored through the actual scenario-spec and people-world assembly path
- **THEN** the independent procedure compiles without forced conditional-support or timer-remedy rules
- **AND** actor profiles and memory remain distinct from actual technical truth and claims preserve common source lineage
- **AND** the procedure exposes actor-authorized initial knowledge and safe public context through the declared actor-information contract

#### Scenario: Static action forms do not reveal technical condition

- **WHEN** two generated worlds differ only in the inaccessible actual technical condition
- **THEN** their declared public institutional action forms are identical and include the actor-owned assent and authorized validation operations
- **AND** communication forms are supplied only to actors authorized to know the represented item
- **AND** installed mechanics validate authority and consequences when an actor attempts a form

#### Scenario: Proposed rules cannot replace actor-owned assent

- **WHEN** the judge proposes a rule that would write the independent procedure's technical condition, hold, stance, authority or assent state
- **THEN** preview, installation and restored-rule reconstruction reject that proposed rule without mutating the world
- **AND** raw candidate validation accepts exact compiled procedural writers while rejecting additional or altered writers, including a writer with a copied compiled rule identifier
- **AND** proposals for unrelated state remain eligible for ordinary rules checks
