## ADDED Requirements

### Requirement: A repeated run request gets the first job back

When the same caller sends `POST /run` with `{"async": true}` and a body identical to one whose job is still running,
or whose job finished without error and continued a saved round, the service returns that first job's id and starts
no second run. A request whose earlier job failed, or whose earlier job was a finished fresh run, SHALL start a new job.
The caller and the body (without `async`) identify the request, so a different caller, a different snapshot, a
different `turn_offset` or a different saved-run checkpoint is a different request.

Where it is enforced: `scripts/world_builder_service.py` (`_run_request_key`, `_start_job`);
`tests/test_world_builder_service.py`.

Source: world-substrate#225 (owner's issue): "Make /run idempotent on the server, keyed per (session, turn_offset,
base revision), so a repeated request gets the first job_id back instead of starting a second paid run." Key
derivation and the failed-job and fresh-run exceptions: inferred by agent (the server has no session; reusing a
failed or fresh run would block a legitimate retry or restart).

#### Scenario: The same request twice while the run is going

- **WHEN** the same caller sends the same `/run` body with `async` true twice while the first job is running
- **THEN** both answers carry the same `job_id`, the second says `"deduplicated": true`, and the run function was called once

#### Scenario: A repeated continued round after it finished

- **WHEN** a continued round (body has `continue_from`) finished with status 200 and the same body is sent again
- **THEN** the first `job_id` is returned and the run function was called once

#### Scenario: A repeat after a failed job starts a new run

- **WHEN** the first job for a body ended with status 422 and the same body is sent again
- **THEN** a new `job_id` is returned and the run function was called twice

#### Scenario: A finished fresh run is not reused

- **WHEN** a fresh run (no `continue_from`, `turn_offset` 0) finished and the same body is sent again
- **THEN** a new `job_id` is returned

#### Scenario: A different request is not deduplicated

- **WHEN** two `/run` bodies differ in `turn_offset`, in `continue_from`, or in `expected_checkpoint_id`, or are sent by callers with different allowances
- **THEN** each starts its own job with its own `job_id`
