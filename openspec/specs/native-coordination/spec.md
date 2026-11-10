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

### Requirement: Authoring: Provider spend

One-shot extraction shares the World Builder's existing server-side rate limit
and daily spend ledger. Draft generation has its own bounded per-request cap.

A provider failure after reservation fails closed and charges the reserved
amount under the existing budget-ledger semantics.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18 (native World Substrate convergence for the next Waltzman release), exact words not recorded

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

### Requirement: Comparison: Fresh execution

A comparison is a second fresh Engine run. It is not:

- an edit of baseline commands or events;
- a fork that rewrites retained history;
- a post-hoc change to a Living Scene frame; or
- an analytic prediction of what would have happened.

The request log contains the complete comparison bundle, making the changed
initial condition inspectable.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

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

### Requirement: Comparison: Limits

The v0 comparison surface does not yet support arbitrary state editing,
multi-variable experiments, probabilistic sweeps, sensitivity analysis,
automatic causal identification, or provider-generated intervention advice.

Those additions require separate contracts rather than extending this control
implicitly.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

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

### Requirement: Diagnostics: Acceptance authority

`examples/native_coordination/acceptance-v0.json` is the executable acceptance matrix for this slice.

Each world declares expected configuration facts such as participant count, approval threshold, information channels, the prerequisite that must block the first approval, the represented intervention resource, and the actor authorized to restore it.

The acceptance evaluator may compare those declared expectations to retained execution and presentation evidence. It must not mutate the world or substitute expected values for observed state.

A run is accepted only when all evaluated checks pass. A summary may say that acceptance passed; the individual retained checks remain the evidence.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

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

### Requirement: Diagnostics: Privacy and causal boundary

Direct/private represented information may appear in canonical evidence where actor-authorized observations legitimately contain it. The public Living Scene render receives no observer identity by default, so private message content must remain hidden there even when the represented transmission line itself is visible.

Information context and message delivery are not promoted into mechanic-declared causal ancestry.

Source: Decision 005, accepted 2026-09-18; the wiki records it as a human product decision of 2026-09-18, exact words not recorded

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
