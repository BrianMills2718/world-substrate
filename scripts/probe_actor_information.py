#!/usr/bin/env python3
"""One local I0/I1 service demonstration; preparation is free, --execute spends.

Uses the real HTTP handler, normal owner ledger and model routes. No world is
hand-built and no policy reply is scripted. Run once after the free checks;
do not repeat to obtain a preferred social result. Inspect every retained
model/tool record and failure before writing TRACE_READ.md or making a claim.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
SOURCE = REPO / "evidence/i0-i1/source-input.json"


def save(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def run_job(request: Any, path: str, body: dict[str, Any], *, pause: Any = time.sleep, report: Any = print) -> dict[str, Any]:
    """Submit once, observe the same job, and accept either native or wrapped completion.

    A transport/observation timeout propagates; it never starts a replacement job.
    The native HTTP endpoint returns the completed payload directly. Retained
    job envelopes can also be inspected without mistaking them for that payload.
    """
    started = time.monotonic()
    value = request(path, {**body, "async": True})
    job_id = value.get("job_id")
    last_progress = None
    while job_id:
        if value.get("status") == "done":
            payload = value.get("payload")
            if not isinstance(payload, dict):
                raise RuntimeError("Completed job has no response payload")
            if value.get("http_status", 200) >= 400 or payload.get("ok") is False:
                raise RuntimeError(f"{path} failed: {payload.get('error')}")
            return payload
        if "trace" in value or "bundle" in value:
            return value
        pause(2)
        value = request("/jobs/" + job_id)
        progress = value.get("progress")
        if progress != last_progress:
            report(json.dumps({"step": path, "elapsed_s": round(time.monotonic() - started, 1), "progress": progress}))
            last_progress = progress
        if value.get("status") not in ("running", "done"):
            if value.get("ok") is False:
                raise RuntimeError(f"{path} failed: {value.get('error')}")
            return value
    return value


def inspect_generated_boundary(build: dict[str, Any]) -> dict[str, Any]:
    """Check the compiled procedure's structural identity before resident spend.

    This guard establishes the intended path, not scientific validity or a
    complete semantic review. The generated declarations remain evidence to read.
    """
    bundle, causal = build["bundle"], build["causal_model"]
    components = {name for entity in bundle["entities"] for name in entity["components"]}
    required = {"validation_decision", "actor_position", "technical_condition", "technical_role"}
    kinds = {rule["action_kind"] for rule in causal.get("mechanics", [])}
    expected_actions = {"record-assent", "withdraw-assent", "repair-condition", "complete-validation", "activate"}
    forbidden_processes = []
    for process in causal.get("processes", []):
        for effect in process.get("effects", []):
            path = effect.get("path", "")
            if (path.startswith("components.concern.") or path.startswith("components.group_decision.")
                    or path.startswith("components.technical_condition.") or path.endswith(".stance") or path.endswith(".support")):
                forbidden_processes.append(process.get("process_id"))
    checks = {"declared_actor_information": "actor_information" in bundle,
              "independent_components": required <= components, "no_legacy_group_decision": "group_decision" not in components,
              "explicit_repair_validation_and_assent": expected_actions <= kinds,
              "no_forced_stance_or_timer_repair": not forbidden_processes}
    return {"checks": checks, "passed": all(checks.values()), "missing_components": sorted(required - components),
            "missing_actions": sorted(expected_actions - kinds), "forbidden_processes": forbidden_processes,
            "limitation": "Read the complete generated declarations and traces before making behavioral claims."}


def public_trace_record(value: Any) -> Any:
    """Remove credential identifiers, including from encoded native snapshots."""
    if isinstance(value, dict):
        return {key: ("[credential identifier omitted]" if key == "openrouter_key_fingerprint" else public_trace_record(item)) for key, item in value.items()}
    if isinstance(value, list):
        return [public_trace_record(item) for item in value]
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return value
        if isinstance(parsed, (dict, list)):
            clean = public_trace_record(parsed)
            return json.dumps(clean, ensure_ascii=False) if clean != parsed else value
    return value


def export_traces(output: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Export exact native records, including failures, using recorded trace families.

    get_call_record restores replay snapshots. Native rows additionally retain
    usage, reasoning where exposed, retry and other fields the narrow API omits.
    No database or budget path is replaced by this probe.
    """
    import llm_client.io_log as io_log
    from llm_client.observability.replay import get_call_record
    from llm_client.observability.query import get_call_lifecycle, summarize_trace
    from llm_client.observability.structured_attempts import get_structured_attempt_histories
    from llm_client.observability.raw_artifacts import read_structured_raw_artifact

    roots = sorted({tid for row in rows for tid in [row.get("trace_id"), *(row.get("trace_ids") or [])] if tid})
    save(output / "trace-ids.json", roots)
    counts: dict[str, Any] = {"trace_roots": roots, "llm_calls": 0, "tool_calls": 0}
    database = sqlite3.connect(f"file:{io_log._db_path}?mode=ro", uri=True)
    database.row_factory = sqlite3.Row
    native_calls: dict[int, dict[str, Any]] = {}
    native_tools: dict[int, dict[str, Any]] = {}
    try:
        for table, target in (("llm_calls", native_calls), ("tool_calls", native_tools)):
            for root in roots:
                for row in database.execute(
                    f"SELECT * FROM {table} WHERE trace_id = ? OR (trace_id >= ? AND trace_id < ?) ORDER BY id",
                    (root, root + "/", root + "0"),
                ):
                    target[row["id"]] = dict(row)
        with (output / "llm-calls.jsonl").open("a") as handle:
            for call in native_calls.values():
                # Keep messages as the native JSON string for replay_build compatibility.
                call["restored_record"] = get_call_record(call["id"])
                handle.write(json.dumps(public_trace_record(call), ensure_ascii=False) + "\n")
        with (output / "tool-calls.jsonl").open("a") as handle:
            for call in native_tools.values():
                handle.write(json.dumps(public_trace_record(call), ensure_ascii=False) + "\n")
        trace_ids = sorted(set(roots) | {row["trace_id"] for row in [*native_calls.values(), *native_tools.values()]})
        save(output / "call-lifecycle.json", {tid: get_call_lifecycle(trace_id=tid) for tid in trace_ids})
        histories = {}
        for tid in trace_ids:
            histories[tid] = {}
            for call_id, events in get_structured_attempt_histories(tid).items():
                histories[tid][call_id] = []
                for event in events:
                    retained = event.model_dump(mode="json")
                    if event.raw_artifact_ref and event.raw_sha256:
                        retained["raw_content"] = read_structured_raw_artifact(
                            artifact_ref=event.raw_artifact_ref, logical_call_id=call_id,
                            attempt_ordinal=event.attempt_ordinal, expected_sha256=event.raw_sha256).decode("utf-8")
                    histories[tid][call_id].append(retained)
        save(output / "structured-attempts.json", histories)
        save(output / "trace-summaries.json", {root: summarize_trace(root, rooted=True) for root in roots})
        counts.update(llm_calls=len(native_calls), tool_calls=len(native_tools))
        return counts
    finally:
        database.close()


def execute(source: dict[str, Any], output: Path) -> int:
    # Importing the service is deferred until explicit execution. Existing
    # llm_client credential loading and all normal spend gates remain in force.
    import scripts.world_builder_service as service

    output.mkdir(parents=True, exist_ok=False)
    save(output / "source-input.json", source)
    revision = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    changed = subprocess.run(["git", "-C", str(REPO), "status", "--short"], check=True, capture_output=True, text=True).stdout
    save(output / "revision.json", {"scope": source["claim_scope"], "revision": revision,
                                  "working_tree": changed, "started_utc": datetime.now(timezone.utc).isoformat()})
    old_password = os.environ.get("WORLD_BUILDER_OWNER_PASSWORD")
    old_logs = os.environ.get("WORLD_BUILDER_RUN_LOG_DIR")
    old_project = os.environ.get("LLM_CLIENT_PROJECT")
    raw_keys = ("LLM_CLIENT_STRUCTURED_RAW_ARTIFACTS", "LLM_CLIENT_STRUCTURED_RAW_ARTIFACT_ROOT")
    old_raw = {key: os.environ.get(key) for key in raw_keys}
    password = secrets.token_urlsafe(32)  # Never written, printed, or included in a request record.
    os.environ["WORLD_BUILDER_OWNER_PASSWORD"] = password
    daily = output / "service-daily"
    os.environ["WORLD_BUILDER_RUN_LOG_DIR"] = str(daily)
    os.environ.setdefault("LLM_CLIENT_PROJECT", "world-substrate")
    # A new per-run raw store preserves failed structured responses without
    # invoking retention cleanup on anybody else's existing artifact store.
    os.environ[raw_keys[0]] = "on"
    os.environ[raw_keys[1]] = str(output / "structured-raw")
    server = ThreadingHTTPServer(("127.0.0.1", 0), service.WorldBuilderHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_address[1]}{service.API_PREFIX}"
    protocol = output / f"protocol-{datetime.now(timezone.utc):%Y-%m-%d}.jsonl"
    start = time.monotonic()
    result: dict[str, Any] = {"status": "running", "scope": source["claim_scope"], "owner_daily_cap_usd": service.OWNER_DAILY_BUDGET}

    def request(path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        began = time.monotonic()
        req = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(),
            headers={"Content-Type": "application/json", service.OWNER_HEADER: password,
                     service.CLIENT_HEADER: "agent:i0-i1-local-probe"})
        status, raw = None, None
        try:
            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    status, raw = response.status, response.read().decode()
            except urllib.error.HTTPError as error:
                status, raw = error.code, error.read().decode()
            value = json.loads(raw)
            if status >= 400 or value.get("ok") is False:
                raise RuntimeError(f"{path} returned HTTP {status}: {value.get('error')}")
            return value
        finally:
            with protocol.open("a") as handle:
                handle.write(json.dumps({"path": path, "request": body, "status": status,
                    "response_raw": raw, "elapsed_s": round(time.monotonic() - began, 3)}) + "\n")

    exit_status = 1
    try:
        print(json.dumps({"step": "build", "scope": source["claim_scope"], "owner_daily_cap_usd": service.OWNER_DAILY_BUDGET}), flush=True)
        build = run_job(request, "/generate-world", {"description": source["description"], **source["build"]}, report=lambda line: print(line, flush=True))
        save(output / "build.json", build)
        inspection = inspect_generated_boundary(build)
        save(output / "build-path-inspection.json", inspection)
        if not inspection["passed"]:
            raise RuntimeError("Generated build did not select the independent actor/validation procedure; no rounds submitted. Read build-path-inspection.json.")
        previous = None
        for round_no in range(1, source["run"]["rounds"] + 1):
            body = {"bundle": build["bundle"], "causal_model": build["causal_model"], "approved": True,
                    "policy": source["run"]["policy"], "turns": source["run"]["turns_per_request"]}
            for key in ("run_stop", "judge_rulings"):
                if build.get(key):
                    body[key] = build[key]
            if previous:
                body.update(continue_from=previous["trace"]["final_snapshot"], continue_seal=previous["snapshot_seal"],
                            approval=previous["approval"], actor_state=previous["actor_state"],
                            turn_offset=previous["summary"]["last_turn"])
                if previous["trace"].get("rulings"):
                    body["rulings"] = previous["trace"]["rulings"]
            print(json.dumps({"step": "resident round", "round": round_no, "elapsed_s": round(time.monotonic() - start, 1)}), flush=True)
            previous = run_job(request, "/run", body, report=lambda line: print(line, flush=True))
            save(output / f"round-{round_no}.json", previous)
        result["status"] = "recorded; requires full trace inspection"
        exit_status = 0
    except Exception as error:
        result.update(status="failed; do not rerun for a preferred outcome", error_type=type(error).__name__, error=str(error))
        (output / "failure.txt").write_text(traceback.format_exc())
    finally:
        server.shutdown()
        server.server_close()
        rows = []
        for path in sorted(daily.glob("*.jsonl")):
            rows.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
        with (output / "run-log.jsonl").open("a") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        try:
            result["traces"] = export_traces(output, rows)
        except Exception as error:
            result["trace_export_error"] = f"{type(error).__name__}: {error}"
            (output / "trace-export-failure.txt").write_text(traceback.format_exc())
            exit_status = 1
        result.update(elapsed_s=round(time.monotonic() - start, 3), exit_status=exit_status)
        save(output / "result.json", result)
        for key, previous_value in (("WORLD_BUILDER_OWNER_PASSWORD", old_password),
                                    ("WORLD_BUILDER_RUN_LOG_DIR", old_logs), ("LLM_CLIENT_PROJECT", old_project), *old_raw.items()):
            if previous_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = previous_value
    print(json.dumps({"output": str(output), **result}), flush=True)
    return exit_status


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--execute", action="store_true", help="Make the authorized paid build and resident calls once.")
    args = parser.parse_args()
    source = json.loads(args.source.read_text())
    if not args.execute:
        print(json.dumps({"status": "prepared; no model calls", "source": str(args.source), "scope": source["claim_scope"],
                          "rounds": source["run"]["rounds"], "execution_requires": "--execute after free checks and authorization"}, indent=2))
        return 0
    output = args.output or REPO / "evidence/i0-i1" / ("local-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    return execute(source, output.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
