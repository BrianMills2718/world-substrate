# A repeated /run request gets the first job back

## Why

`POST /run` with `{"async": true}` always starts a new background job and a new paid run
(`scripts/world_builder_service.py` `_start_job`, called from `do_POST` for `ASYNC_PATHS`). Nothing looks for a job
already started for the same request. If the same round's request reaches the server twice (a browser or proxy
retry after a timeout, a double click, an agent resending), the server pays for two runs, and for a continued round
the two runs write the same round twice. Open since 2026-11-09 (world-substrate#225; the page's `apiJob` has no retry
today, so the risk is from proxies, other clients and future retries, not a page bug).

Source: world-substrate#225 (owner's issue): "Make /run idempotent on the server, keyed per (session, turn_offset,
base revision), so a repeated request gets the first job_id back instead of starting a second paid run."

## What changes

- `_start_job` (path `/run` only) computes a **request key**: SHA-256 of the canonical JSON (sorted keys, compact
  separators) of the request body without its `async` field, together with the caller's allowance
  (`owner`/`visitor`) and `_fingerprint(client)`. The body already holds everything the issue names: the
  sealed snapshot being continued (`continue_from`, `continue_seal`; the base revision), `turn_offset`, and for saved
  catalog runs `catalog_run_id` and `expected_checkpoint_id`. There is no server session, so the key is the
  caller plus the exact request, not an invented session id.
- If a job with the same key exists and is **running**, or is **finished without error (HTTP status below 400) and
  was a continued round** (body has `continue_from` or `catalog_run_id`, or `turn_offset` above 0), the server
  returns `202 {"ok": true, "status": "running", "job_id": <first id>, "deduplicated": true}` and starts nothing, so
  nothing is spent and no ledger allowance is reserved.
- Otherwise it starts a job as today and remembers the key on the job record. A failed job (status 400 or above)
  is never reused, so a retry after a failure still runs. A finished fresh run (no snapshot, `turn_offset` 0) is
  not reused either, so "Start over" with the same world still starts a new run.
- Jobs are already pruned after `JOB_TTL_SECONDS` (3600) and at `MAX_JOBS` (200); the key lives and dies with the job.
- `/generate-world` is unchanged.

## Out of scope

- A page-side idempotency key or retry in `apiJob` (`scripts/world_builder_home.html`).
- Reusing results across server restarts: `_JOBS` is in memory, and a restart ends running jobs anyway.
- Deduplicating `/generate-world`, or the synchronous (non-async) `/run`.
- Any model call: the change and its tests are free (scripted runs, patched models).

## Owner decision assumed

1. Key = caller + exact body, not a (session, turn_offset, base revision) triple: the server has no sessions, and the
   body's snapshot and seal are the base revision. Undo: replace `_run_request_key` with another derivation.
2. A finished fresh run (turn_offset 0, no snapshot) is not reused; only a running one is. Reason: reusing it would
   make "Start over" with unchanged rules return an old result. Undo: drop the "continued" condition.
3. A duplicate reports `"deduplicated": true` and is not logged as a second run-log line.
