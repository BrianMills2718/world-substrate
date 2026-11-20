# Tasks

Files touched: `scripts/world_builder_service.py`, `tests/test_world_builder_service.py`,
`docs/architecture/arc42.md`. No `lockstep.yaml` row changes: none of these files is a new governed file, and
`openspec/specs/world-builder-page/spec.md` already has its row (archiving only edits that file).

- [x] 1. Tests first, in `tests/test_world_builder_service.py` (same class as `test_async_run_completes`, line ~1245;
  use its `post`/`wait_for_job` helpers). Patch `service.WorldBuilderHandler._run` with a stub that waits on a
  `threading.Event` (for the running case) then calls `self._json(200, {"ok": True})`, counting calls; no model is called.
  Add five tests, each marked:
  - `@pytest.mark.req("world-builder-page/the-same-request-twice-while-the-run-is-going")`: post the same body twice
    before releasing the event; assert equal `job_id`, second has `deduplicated` true, call count 1 after release.
  - `@pytest.mark.req("world-builder-page/a-repeated-continued-round-after-it-finished")`: body with `continue_from`
    (any dict; the stub never validates), wait for done, post again; same `job_id`, count 1.
  - `@pytest.mark.req("world-builder-page/a-repeat-after-a-failed-job-starts-a-new-run")`: stub calls
    `self._error(422, "x")`; second post gives a new `job_id`, count 2.
  - `@pytest.mark.req("world-builder-page/a-finished-fresh-run-is-not-reused")`: fresh body, finished, repeat gives new id.
  - `@pytest.mark.req("world-builder-page/a-different-request-is-not-deduplicated")`: vary `turn_offset`, then
    `catalog_run_id`+`expected_checkpoint_id`, then owner vs visitor (use `_owner_env` and the owner-password header
    the existing owner tests send); distinct ids each time.
  Run them and confirm they fail (the second post starts a new job).
- [x] 2. In `scripts/world_builder_service.py`, next to `_prune_jobs`, add
  `_run_request_key(body, allowance, client) -> str` (`Implements: world-builder-page/a-repeated-run-request-gets-the-first-job-back`):
  SHA-256 hex of `json.dumps({k: v for k, v in body.items() if k != "async"}, sort_keys=True, separators=(",", ":"))`
  joined with `allowance` and `_fingerprint(client)`. Add `_is_continued_round(body) -> bool`:
  `"continue_from" in body or "catalog_run_id" in body or body.get("turn_offset", 0) not in (0, None)`
  (non-int `turn_offset` just counts as continued; `_run` validates it later).
- [x] 3. In `_start_job` (line ~1827), when `path == "/run"`: compute the key (allowance from
  `(_REQUEST.get() or {}).get("allowance")`, fall back to `"owner" if _is_owner() else "visitor"`); inside the
  existing `with _JOBS_LOCK:` block, after `_prune_jobs()`, scan `_JOBS` for a job with `key` equal and either
  `status == "running"` or (`status == "done"`, `http_status < 400`, `reusable` true). If found, release the lock,
  `self._json(HTTPStatus.ACCEPTED, {"ok": True, "status": "running", "job_id": found, "deduplicated": True})`
  and return before creating a job or thread. Otherwise store `key` and `reusable=_is_continued_round(body)` on the new
  job record. The scan and the insert stay in one lock hold so two simultaneous duplicates cannot both start.
  `/generate-world` gets no key. Re-run task 1's tests; all pass.
- [x] 4. Run the neighbours: `uv run pytest tests/test_world_builder_service.py -q` (all pass, same count as before
  plus five) and `python scripts/check_project.py`.
- [x] 5. `docs/architecture/arc42.md` line ~230/257 area: add one sentence to the Background jobs description that a
  repeated async `/run` from the same caller with the same body returns the running (or finished, for continued
  rounds) job instead of starting another. Run `python scripts/check_project.py` again.
- [x] 6. `openspec archive 2026-11-20-run-request-is-idempotent --yes`, then `make docs-specs` if the Makefile has it,
  `lockstep check`, commit.
