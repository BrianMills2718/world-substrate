---
role: contract
status: proposed
reviewed_through: 2026-09-18
---

# Native coordination diagnostic bundle v0

The first native Waltzman coordination vertical is debugged from retained evidence rather than from UI summaries or model prose.

This contract is deliberately narrow. It applies to the deterministic structured coordination fixtures in `examples/native_coordination/` and does not define a general experiment framework.

## Acceptance authority

`examples/native_coordination/acceptance-v0.json` is the executable acceptance matrix for this slice.

Each world declares expected configuration facts such as participant count, approval threshold, information channels, the prerequisite that must block the first approval, the represented intervention resource, and the actor authorized to restore it.

The acceptance evaluator may compare those declared expectations to retained execution and presentation evidence. It must not mutate the world or substitute expected values for observed state.

A run is accepted only when all evaluated checks pass. A summary may say that acceptance passed; the individual retained checks remain the evidence.

## Diagnostic run identity

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

## Required artifacts

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

<<<<<<< HEAD
For action feedback, Living Scene may project each retained check's public rule label and boolean verdict so a visitor can inspect both satisfied and failed checks. It must not copy retained `actual`/`expected` operands into the public presentation payload; those remain evidence-layer data because they may contain actor-scoped or otherwise non-public values.

=======
>>>>>>> origin/main
`acceptance.json` records each acceptance assertion independently, with a stable id, category, pass/fail value, and observed/expected values when useful.

`manifest.json` records SHA-256 for every other retained artifact in the directory. It is generated last and does not hash itself.

## Failure categories

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

## Stage discipline

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

## Matrix command

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

## Privacy and causal boundary

Direct/private represented information may appear in canonical evidence where actor-authorized observations legitimately contain it. The public Living Scene render receives no observer identity by default, so private message content must remain hidden there even when the represented transmission line itself is visible.

Information context and message delivery are not promoted into mechanic-declared causal ancestry.

## Hashing and reproducibility

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
