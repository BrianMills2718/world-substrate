#!/usr/bin/env python3
"""Small same-origin API for World Builder mechanics generation and fresh runs."""
from __future__ import annotations

import argparse
import contextvars
import hashlib
import hmac
import json
import math
import os
import sys
import threading
import time
import uuid
from collections import defaultdict, deque
from datetime import date
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.generate_causal_model import DEFAULT_MODEL, generate_causal_model
from scripts.generate_world_bundle import generate_world_bundle
from scripts.world_dialogue import clarify, surprise_description
from scripts.native_coordination_authoring import (
    DEFAULT_CAUSAL as NATIVE_COORDINATION_CAUSAL,
    generate_native_coordination_draft,
)
from scripts.native_coordination_comparison import with_approval_threshold
from scripts.run_authored_world import actor_ids, build_engine, render_run, run_world
from scripts.run_native_coordination import run_native_coordination
from scripts.scaffold_world import BundleError, validate_bundle
from world_substrate.action_authoring import ActionDeclarationError, CausalModel

API_PREFIX = "/world-builder/api"
MAX_BODY_BYTES = 512_000
DRAFT_BUDGET = 0.08
MECHANICS_BUDGET = 0.12
RUN_BUDGET = 0.12
DAILY_LLM_BUDGET = 0.50
# Owner override (Brian, 2026-10-05: "i always want to be able to put in a
# password to override the budget"). A request carrying the owner password in
# X-World-Builder-Owner skips the shared visitor allowance and per-visitor rate
# limits and spends from a separate owner ledger instead. Unset password: off.
OWNER_HEADER = "X-World-Builder-Owner"
OWNER_DAILY_BUDGET = 5.00
_LEDGER: contextvars.ContextVar[str] = contextvars.ContextVar("world_builder_ledger", default="visitor")


def _owner_password() -> str | None:
    return os.environ.get("WORLD_BUILDER_OWNER_PASSWORD") or None


def _is_owner() -> bool:
    return _LEDGER.get() == "owner"


def _ledger_path() -> Path:
    if _is_owner():
        return BUDGET_STATE_PATH.with_name("llm-owner-budget-v1.json")
    return BUDGET_STATE_PATH


def _ledger_cap() -> float:
    return OWNER_DAILY_BUDGET if _is_owner() else DAILY_LLM_BUDGET
# Description -> structure -> mechanics (+ at most one dry-run-guided mechanics retry).
WORLD_BUDGET = 0.20
# Rules-step retry escalates to a stronger model. Measured 2026-10-05 on six
# descriptions: default model finished 11/24 builds, this model 6/6, at about
# $0.037 vs $0.003 per rules call, so it is used only when the cheap attempt
# does not reach its finish line.
RULES_RETRY_MODEL = "openrouter/openai/gpt-5.6-sol"
RULES_RETRY_JUSTIFICATION = (
    "World Builder rules retry: the default model's rules did not let the described world "
    "reach its finish line; the stronger model measured 6/6 vs 11/24 on the same descriptions."
)
DRY_RUN_TURNS = 12
# Ongoing/open worlds must stay alive past the first visible run: live, an open
# village was busy for 12 rounds and then went quiet, so test twice as long.
DRY_RUN_TURNS_CONTINUING = 24
WORLD_KINDS = ("task", "ongoing", "open")
# Live play continues a world one round at a time for as long as the viewer
# likes; the daily budget, not a round count, is the limit.
MAX_CONTINUED_TURNS = 100_000
MAX_RECENT_MOVES = 12
LLM_REQUESTS_PER_HOUR = 8
# Live play asks for AI moves one round at a time, so AI rounds get their own
# hourly allowance (the daily dollar budget still caps spend).
AI_RUN_REQUESTS_PER_HOUR = 360
# Live play with simple moves asks for one free round every ~1.5 s.
GENERAL_REQUESTS_PER_MINUTE = 60
ALLOWED_ORIGINS = {"https://brianmills.dev", "https://www.brianmills.dev"}
TRACE_ROOT = "world-builder-live"
BUDGET_STATE_PATH = Path.home() / ".local/state/world-builder/llm-budget-v1.json"
BUDGET_STATE_SCHEMA = "world-builder-llm-budget/v1"

_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
_LLM_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
# Dialogue turns are small and frequent; they get their own per-visitor
# allowance so a conversation does not use up the build allowance.
_DIALOGUE_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
_AI_RUN_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
DIALOGUE_REQUESTS_PER_HOUR = 30
DIALOGUE_BUDGET = 0.02
_LLM_LOCK = threading.Lock()


def _prune(queue: deque[float], window: float) -> None:
    cutoff = time.time() - window
    while queue and queue[0] < cutoff:
        queue.popleft()


def _rate_ok(client: str, *, llm: bool, dialogue: bool = False, ai_run: bool = False) -> bool:
    if _is_owner():
        return True
    if ai_run:
        queue, window, limit = _AI_RUN_REQUESTS[client], 3600.0, AI_RUN_REQUESTS_PER_HOUR
    elif dialogue:
        queue, window, limit = _DIALOGUE_REQUESTS[client], 3600.0, DIALOGUE_REQUESTS_PER_HOUR
    else:
        queue = _LLM_REQUESTS[client] if llm else _REQUESTS[client]
        window = 3600.0 if llm else 60.0
        limit = LLM_REQUESTS_PER_HOUR if llm else GENERAL_REQUESTS_PER_MINUTE
    _prune(queue, window)
    if len(queue) >= limit:
        return False
    queue.append(time.time())
    return True


def _empty_budget_state() -> dict[str, Any]:
    return {
        "schema_version": BUDGET_STATE_SCHEMA,
        "date": date.today().isoformat(),
        "spent_usd": 0.0,
        "reserved_usd": 0.0,
    }


def _load_budget_state() -> dict[str, Any]:
    path = _ledger_path()
    if not path.exists():
        return _empty_budget_state()
    try:
        value = json.loads(path.read_text())
    except Exception as error:
        raise RuntimeError("World Builder budget ledger is unreadable; refusing LLM spend") from error
    if not isinstance(value, dict) or value.get("schema_version") != BUDGET_STATE_SCHEMA:
        raise RuntimeError("World Builder budget ledger has an unsupported schema; refusing LLM spend")
    if value.get("date") != date.today().isoformat():
        return _empty_budget_state()
    for key in ("spent_usd", "reserved_usd"):
        amount = value.get(key)
        if type(amount) not in (int, float) or not math.isfinite(float(amount)) or amount < 0:
            raise RuntimeError(f"World Builder budget ledger has invalid {key}; refusing LLM spend")
    return {
        "schema_version": BUDGET_STATE_SCHEMA,
        "date": value["date"],
        "spent_usd": float(value["spent_usd"]),
        "reserved_usd": float(value["reserved_usd"]),
    }


def _write_budget_state(state: dict[str, Any]) -> None:
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(state, sort_keys=True, separators=(",", ":")) + "\n")
    temp.replace(path)


def _daily_cost() -> float:
    state = _load_budget_state()
    return float(state["spent_usd"] + state["reserved_usd"])


def _reserve_daily_budget(requested_cap: float) -> float | None:
    state = _load_budget_state()
    committed = float(state["spent_usd"] + state["reserved_usd"])
    remaining = max(0.0, _ledger_cap() - committed)
    if remaining <= 0.0001:
        return None
    cap = min(float(requested_cap), remaining)
    state["reserved_usd"] = float(state["reserved_usd"] + cap)
    _write_budget_state(state)
    return cap


def _settle_daily_budget(reserved_cap: float, actual_cost: float | None) -> float:
    state = _load_budget_state()
    state["reserved_usd"] = max(0.0, float(state["reserved_usd"]) - float(reserved_cap))
    # If a call or accounting read fails after reservation, charge the whole
    # reservation. This intentionally fails closed until the next calendar day.
    charged = float(reserved_cap if actual_cost is None else max(0.0, actual_cost))
    state["spent_usd"] = float(state["spent_usd"] + charged)
    _write_budget_state(state)
    return float(state["spent_usd"] + state["reserved_usd"])


def _settle_failed_call(reserved_cap: float, trace_id: str) -> float:
    """Settle a reservation whose request failed after (possibly) spending.

    A generation that fails validation has usually completed paid calls whose
    cost is recorded; charging the whole reservation for it let two or three
    rejected descriptions exhaust the public daily budget. Charge the recorded
    cost when there is one. When nothing is recorded (the provider call itself
    failed, or the cost lookup did), stay fail-closed and charge the whole cap.
    """
    try:
        recorded = _trace_cost(trace_id)
    except Exception:
        recorded = 0.0
    return _settle_daily_budget(reserved_cap, recorded if recorded > 0 else None)


def _trace_cost(trace_id: str) -> float:
    from llm_client import get_cost

    return float(get_cost(trace_id=trace_id) or 0.0)


def _client_ip(handler: BaseHTTPRequestHandler) -> str:
    forwarded = handler.headers.get("CF-Connecting-IP") or handler.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return handler.client_address[0]


def _origin_allowed(handler: BaseHTTPRequestHandler) -> bool:
    origin = handler.headers.get("Origin")
    forwarded = handler.headers.get("CF-Connecting-IP") or handler.headers.get("X-Forwarded-For")
    # A Cloudflare-originated connection is locally sourced at the socket layer,
    # so absence of Origin must not be mistaken for a trusted localhost caller.
    if forwarded:
        return origin in ALLOWED_ORIGINS
    if origin in ALLOWED_ORIGINS:
        return True
    return handler.client_address[0] in {"127.0.0.1", "::1"} and origin in {None, "http://127.0.0.1", "http://localhost"}


def _strip_review(value: dict[str, Any]) -> dict[str, Any]:
    out = json.loads(json.dumps(value))
    out.pop("review", None)
    return out


def _requested_model(body: dict[str, Any]) -> str:
    """Public callers may only name the service's approved model.

    A free-form model id would let any visitor choose an arbitrary (and
    arbitrarily priced) route; the shared client also refuses non-default
    models without a justification, which surfaced as a 500.
    """
    requested = body.get("model")
    if requested in (None, "", DEFAULT_MODEL):
        return DEFAULT_MODEL
    raise ValueError(f"model must be {DEFAULT_MODEL} (or omitted)")


# --- Background jobs -------------------------------------------------------
#
# Cloudflare closes a proxied request after 100 seconds, and a build with a
# stronger-model retry, or a run with AI-chosen moves, can take longer. Those
# endpoints accept {"async": true}: the request returns a job id at once and
# the page polls GET /jobs/<id>. The work and its result are identical to the
# synchronous path; only delivery changes.
JOB_TTL_SECONDS = 3600
MAX_JOBS = 200
_JOBS: dict[str, dict[str, Any]] = {}
_JOBS_LOCK = threading.Lock()
ASYNC_PATHS = ("/generate-world", "/run")


def _prune_jobs() -> None:
    cutoff = time.time() - JOB_TTL_SECONDS
    for job_id in [k for k, v in _JOBS.items() if v["created"] < cutoff]:
        del _JOBS[job_id]
    while len(_JOBS) > MAX_JOBS:
        del _JOBS[min(_JOBS, key=lambda k: _JOBS[k]["created"])]


# --- Run log ----------------------------------------------------------------
#
# Every build, run, dialogue turn and surprise leaves one durable JSONL record
# (one file per UTC day), so what happened in any visitor's world can be read
# after the fact: who (owner / agent / visitor, visitors only as a salted
# fingerprint), what they asked, the world and rules produced, the quick test,
# the run outcome, errors and cost. Read it with GET /runs (owner only) or
# scripts/world_builder_runs.py.
LOGGED_PATHS = ("/generate-world", "/run", "/clarify", "/surprise", "/generate-draft",
                "/generate-mechanics", "/compare-native-coordination")
CLIENT_HEADER = "X-World-Builder-Client"
_REQUEST: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar("world_builder_request", default=None)
_RUN_LOG_LOCK = threading.Lock()


def _run_log_dir() -> Path:
    return Path(os.environ.get("WORLD_BUILDER_RUN_LOG_DIR") or BUDGET_STATE_PATH.parent / "runs")


def _fingerprint(client: str) -> str:
    salt = (_owner_password() or "world-builder").encode()
    return hmac.new(salt, client.encode(), "sha256").hexdigest()[:12]


def _world_fingerprint(bundle: Any, causal: Any) -> str | None:
    """Same world and rules -> same fingerprint, so a run can be matched to its build."""
    if not isinstance(bundle, dict) or not isinstance(causal, dict):
        return None
    canonical = json.dumps({"bundle": bundle, "causal_model": causal}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def _request_summary(path: str, body: dict[str, Any]) -> dict[str, Any]:
    keep = ("description", "world_kind", "policy", "turns", "turn_offset", "approved", "execution_mode", "async")
    out = {k: body[k] for k in keep if k in body}
    if isinstance(body.get("messages"), list):
        out["messages"] = body["messages"][-6:]
    if path == "/run" and isinstance(body.get("bundle"), dict):
        out["world"] = (body["bundle"].get("world") or {}).get("label")
        out["continued"] = body.get("continue_from") is not None
        # The exact world and rules this run used (they can be edited after the
        # build), so any logged run can be matched to its build and re-run.
        out["world_fingerprint"] = _world_fingerprint(body["bundle"], body.get("causal_model"))
        if body.get("continue_from") is None:
            # A continued round's world is the previous round's final_snapshot
            # (logged there) under the same fingerprint, so live play does not
            # re-log the whole world every round.
            out["bundle"] = body["bundle"]
            out["causal_model"] = body.get("causal_model")
    return out


def _result_summary(path: str, status: int, value: dict[str, Any]) -> dict[str, Any]:
    if status >= 400 or value.get("ok") is False:
        return {"error": str(value.get("error"))[:500]}
    if path == "/generate-world":
        bundle = value.get("bundle") or {}
        review = value.get("review") or {}
        return {
            "world": (bundle.get("world") or {}).get("label"),
            "things": [e.get("label") for e in bundle.get("entities", [])],
            "rules": [m.get("action_kind") for m in review.get("mechanics", [])],
            "processes": [p.get("process_id") for p in review.get("processes", [])],
            "finish_line": review.get("terminal") is not None,
            "dry_run": value.get("dry_run"),
            "dry_run_attempts": value.get("dry_run_attempts"),
            "not_modeled": value.get("not_modeled"),
            # Full artifacts, so the exact world can be rebuilt and re-run later.
            "world_fingerprint": _world_fingerprint(bundle, value.get("causal_model")),
            "bundle": bundle,
            "causal_model": value.get("causal_model"),
        }
    if path == "/run":
        trace = value.get("trace") or {}
        return {
            "summary": value.get("summary"),
            "mover": trace.get("model"),
            "transcript": trace.get("transcript"),
            # Where the world ended up, so the next live round (or a later replay) starts from it.
            "final_snapshot": trace.get("final_snapshot"),
        }
    if path == "/clarify":
        return {k: value.get(k) for k in ("reply", "questions", "description", "ready")}
    if path == "/surprise":
        return {k: value.get(k) for k in ("theme", "description")}
    return {"keys": sorted(value)[:20]}


def _record_response(status: int, value: dict[str, Any]) -> None:
    request = _REQUEST.get()
    if request is None or request["path"] not in LOGGED_PATHS:
        return
    if status == HTTPStatus.ACCEPTED and value.get("job_id"):
        return  # the job's final result is recorded when it finishes
    entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "path": request["path"],
        "status": int(status),
        "who": request["who"],
        "allowance": request.get("allowance"),
        "client": request["client"],
        "job_id": request.get("job_id"),
        "trace_id": value.get("trace_id"),
        "cost_usd": value.get("cost_usd"),
        "request": request["summary"],
        "result": _result_summary(request["path"], int(status), value),
    }
    try:
        directory = _run_log_dir()
        directory.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry, separators=(",", ":"), default=str) + "\n"
        with _RUN_LOG_LOCK, open(directory / f"runs_{entry['ts'][:10]}.jsonl", "a") as handle:
            handle.write(line)
    except Exception as error:  # observability must never break the request
        print(f"world-builder-api: run log write failed: {type(error).__name__}: {error}", flush=True)


def _recent_runs(limit: int) -> list[dict[str, Any]]:
    directory = _run_log_dir()
    rows: list[dict[str, Any]] = []
    for path in sorted(directory.glob("runs_*.jsonl"), reverse=True):
        for line in reversed(path.read_text().splitlines()):
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if len(rows) >= limit:
                return rows
    return rows


class _JobResponder:
    """Stands in for the HTTP handler inside a job: captures the one response."""

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id

    def _json(self, status: int, value: dict[str, Any]) -> None:
        with _JOBS_LOCK:
            job = _JOBS.get(self.job_id)
            if job is not None:
                job.update(status="done", http_status=int(status), payload=value)
        _record_response(status, value)

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"ok": False, "error": message})


def _idle_guidance(dry: dict[str, Any], idle: list[str], turns: int) -> str:
    """Tell the rules model which actors never acted in the dry run, and why."""
    reasons: dict[str, list[str]] = {}
    for turn in dry.get("transcript") or []:
        for actor in idle:
            for blocked in (turn["actors"].get(actor) or {}).get("blocked_by_rules") or []:
                values = "; ".join(
                    f"{f.get('check')}: was {f.get('actual')!r}, needed {f.get('required')!r}"
                    for f in blocked.get("failed") or []
                )
                line = f"{blocked['action'].get('kind', '?')}: {values or blocked.get('reason', '')}"
                if line not in reasons.setdefault(actor, []) and len(reasons[actor]) < 3:
                    reasons[actor].append(line)
    detail = "; ".join(
        f"{actor} (refused: {', '.join(reasons.get(actor) or ['it was never offered an action'])})" for actor in idle
    )
    return (
        f" In {turns} rounds these actors never managed a single action: {detail}. Every actor role must be able "
        "to act regularly: make sure some other actor's action or a process produces what each one's action "
        "needs (for example, if a carrier must hold goods before delivering, give another actor an action "
        "that loads goods onto the carrier, or let the carrier pick them up itself)."
    )


def _initial_refusals(bundle: dict[str, Any], causal: dict[str, Any], limit: int = 6) -> list[str]:
    """Distinct 'action: failed checks' lines for every actor in the starting state."""
    engine, model, _ = build_engine(bundle, causal)
    seen: list[str] = []
    for actor in actor_ids(engine, model):
        for row in engine.discover(actor)["blocked"]:
            line = f"{row['action'].get('kind')}: {row.get('reason', '')}"
            if line not in seen:
                seen.append(line)
    return seen[:limit]


class WorldBuilderHandler(BaseHTTPRequestHandler):
    server_version = "WorldBuilderService/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("world-builder-api: " + (fmt % args) + "\n")

    def _json(self, status: int, value: dict[str, Any]) -> None:
        _record_response(status, value)
        data = json.dumps(value, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.end_headers()
        self.wfile.write(data)

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"ok": False, "error": message})

    def _path(self) -> str:
        path = self.path.split("?", 1)[0]
        if path.startswith(API_PREFIX):
            path = path[len(API_PREFIX) :]
        return path or "/"

    def _owner_check(self) -> bool | None:
        """True: owner ledger selected. False: no owner password sent.
        None: a password was sent and it is wrong (caller must refuse)."""
        _LEDGER.set("visitor")
        supplied = self.headers.get(OWNER_HEADER)
        if not supplied:
            return False
        expected = _owner_password()
        if not expected or not hmac.compare_digest(supplied.encode(), expected.encode()):
            return None
        _LEDGER.set("owner")
        return True

    def do_GET(self) -> None:
        if self._path() == "/health":
            owner = self._owner_check()
            payload = {
                "ok": True,
                "service": "world-builder",
                "build_commit": os.environ.get("WORLD_SUBSTRATE_BUILD_COMMIT"),
                "owner": bool(owner),
            }
            if owner is None:
                payload["owner_error"] = "That owner password is not right."
            if owner:
                payload["owner_daily_budget_usd"] = OWNER_DAILY_BUDGET
                payload["owner_daily_committed_usd"] = _daily_cost()
            _LEDGER.set("visitor")
            payload["llm_daily_budget_usd"] = DAILY_LLM_BUDGET
            payload["llm_daily_committed_usd"] = _daily_cost()
            self._json(HTTPStatus.OK, payload)
            return
        path = self._path()
        if path == "/runs" or path.startswith("/runs?"):
            if self._owner_check() is not True:
                self._error(HTTPStatus.FORBIDDEN, "the run log needs the owner password")
                return
            from urllib.parse import parse_qs, urlparse
            query = parse_qs(urlparse(self.path).query)
            limit = max(1, min(200, int((query.get("limit") or ["20"])[0])))
            rows = _recent_runs(limit)
            if (query.get("full") or ["0"])[0] != "1":
                for row in rows:
                    result = row.get("result") or {}
                    request = row.get("request") or {}
                    for heavy in ("bundle", "causal_model", "transcript", "dry_run_attempts", "final_snapshot"):
                        result.pop(heavy, None)
                    for heavy in ("bundle", "causal_model", "continue_from"):
                        request.pop(heavy, None)
            self._json(HTTPStatus.OK, {"ok": True, "runs": rows})
            return
        if path.startswith("/jobs/"):
            job_id = path[len("/jobs/"):]
            with _JOBS_LOCK:
                job = _JOBS.get(job_id)
                snapshot = None if job is None else dict(job)
            if snapshot is None:
                self._error(HTTPStatus.NOT_FOUND, "unknown or expired job")
            elif snapshot["status"] == "running":
                self._json(HTTPStatus.OK, {"ok": True, "status": "running", "job_id": job_id})
            else:
                self._json(snapshot["http_status"], snapshot["payload"])
            return
        self._error(HTTPStatus.NOT_FOUND, "not found")

    def _start_job(self, client: str, path: str, body: dict[str, Any]) -> None:
        job_id = uuid.uuid4().hex
        with _JOBS_LOCK:
            _prune_jobs()
            _JOBS[job_id] = {"status": "running", "created": time.time()}
        responder = _JobResponder(job_id)
        # The handler methods only use _json/_error/_llm_budget on self, so a
        # job runs the exact same code with the responder standing in.
        responder._llm_budget = WorldBuilderHandler._llm_budget.__get__(responder)
        target = {"/generate-world": WorldBuilderHandler._generate_world, "/run": WorldBuilderHandler._run}[path]

        ledger = _LEDGER.get()
        request = dict(_REQUEST.get() or {}, job_id=job_id) if _REQUEST.get() else None

        def work() -> None:
            _LEDGER.set(ledger)
            _REQUEST.set(request)
            try:
                target(responder, client, body)
            except (BundleError, ActionDeclarationError, ValueError, TypeError) as error:
                responder._error(HTTPStatus.UNPROCESSABLE_ENTITY, str(error)[:500])
            except Exception as error:  # pragma: no cover - final job boundary
                print(f"world-builder-api: job {job_id} error: {type(error).__name__}: {str(error)[:300]}", flush=True)
                responder._error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal world-builder error")
            with _JOBS_LOCK:
                job = _JOBS.get(job_id)
                if job is not None and job["status"] == "running":
                    job.update(status="done", http_status=500, payload={"ok": False, "error": "job ended without a result"})

        threading.Thread(target=work, daemon=True).start()
        self._json(HTTPStatus.ACCEPTED, {"ok": True, "status": "running", "job_id": job_id})

    def do_POST(self) -> None:
        client = _client_ip(self)
        if not _origin_allowed(self):
            self._error(HTTPStatus.FORBIDDEN, "same-origin browser request required")
            return
        if self._owner_check() is None:
            self._error(HTTPStatus.FORBIDDEN, "That owner password is not right.")
            return
        if not _rate_ok(client, llm=False):
            self._error(HTTPStatus.TOO_MANY_REQUESTS, "request rate limit reached")
            return
        length = self.headers.get("Content-Length")
        if length is None or not length.isdigit():
            self._error(HTTPStatus.LENGTH_REQUIRED, "Content-Length required")
            return
        size = int(length)
        if size > MAX_BODY_BYTES:
            self._error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "request body too large")
            return
        try:
            body = json.loads(self.rfile.read(size))
        except Exception:
            self._error(HTTPStatus.BAD_REQUEST, "request body must be JSON")
            return
        if not isinstance(body, dict):
            self._error(HTTPStatus.BAD_REQUEST, "request body must be an object")
            return

        path = self._path()
        agent = (self.headers.get(CLIENT_HEADER) or "").strip()[:40]
        _REQUEST.set({
            "path": path,
            # Who acted, separately from whose allowance paid: a test agent using the
            # owner password must not look like the owner's own run.
            "who": f"agent:{agent}" if agent else ("owner" if _is_owner() else "visitor"),
            "allowance": "owner" if _is_owner() else "visitor",
            "client": _fingerprint(client),
            "summary": _request_summary(path, body),
        })
        if body.get("async") is True and path in ASYNC_PATHS:
            self._start_job(client, path, body)
            return
        try:
            if path == "/generate-draft":
                self._generate_draft(client, body)
                return
            if path == "/clarify":
                self._clarify(client, body)
                return
            if path == "/surprise":
                self._surprise(client, body)
                return
            if path == "/generate-world":
                self._generate_world(client, body)
                return
            if path == "/generate-mechanics":
                self._generate(client, body)
                return
            if path == "/compare-native-coordination":
                self._compare_native_coordination(client, body)
                return
            if path == "/run":
                self._run(client, body)
                return
            self._error(HTTPStatus.NOT_FOUND, "not found")
        except (BundleError, ActionDeclarationError, ValueError, TypeError) as error:
            self._error(HTTPStatus.UNPROCESSABLE_ENTITY, str(error)[:500])
        except Exception as error:  # pragma: no cover - final process boundary
            self.log_message("internal error: %s: %s", type(error).__name__, str(error)[:300])
            self._error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal world-builder error")

    def _llm_budget(self, client: str, requested_cap: float, *, dialogue: bool = False, ai_run: bool = False) -> float | None:
        if not _rate_ok(client, llm=True, dialogue=dialogue, ai_run=ai_run):
            self._error(HTTPStatus.TOO_MANY_REQUESTS, "LLM rate limit reached")
            return None
        cap = _reserve_daily_budget(requested_cap)
        if cap is None:
            spent = _daily_cost()
            self._error(
                HTTPStatus.TOO_MANY_REQUESTS,
                f"daily World Builder LLM budget reached (${spent:.3f}/${_ledger_cap():.2f})",
            )
            return None
        return cap

    def _dialogue_call(self, client: str, kind: str, call: Any) -> None:
        """Run one budgeted dialogue-sized model call and return its payload."""
        trace_id = f"{TRACE_ROOT}/{kind}/{uuid.uuid4().hex}"
        with _LLM_LOCK:
            budget = self._llm_budget(client, DIALOGUE_BUDGET, dialogue=True)
            if budget is None:
                return
            try:
                payload, _ = call(trace_id, budget)
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_failed_call(budget, trace_id)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
        self._json(
            HTTPStatus.OK,
            {"ok": True, **payload, "cost_usd": trace_cost, "daily_cost_usd": daily_cost, "trace_id": trace_id},
        )

    def _clarify(self, client: str, body: dict[str, Any]) -> None:
        model = _requested_model(body)
        messages = body.get("messages")
        # Validate before reserving any budget.
        from scripts.world_dialogue import _kind, _validate_turns
        _validate_turns(messages)
        _kind(body.get("world_kind"))
        self._dialogue_call(
            client, "clarify",
            lambda trace_id, budget: clarify(
                messages, model=model, trace_id=trace_id, max_budget=budget, world_kind=body.get("world_kind") or "task",
            ),
        )

    def _surprise(self, client: str, body: dict[str, Any]) -> None:
        model = _requested_model(body)
        from scripts.world_dialogue import _kind
        _kind(body.get("world_kind"))
        self._dialogue_call(
            client, "surprise",
            lambda trace_id, budget: surprise_description(
                model=model, trace_id=trace_id, max_budget=budget, world_kind=body.get("world_kind") or "task",
            ),
        )

    def _generate_world(self, client: str, body: dict[str, Any]) -> None:
        """Plain-English description -> reviewed structure + compiled mechanics.

        Nothing here runs a world for real. A deterministic, zero-cost dry run
        checks that the proposed mechanics let anything happen at all; if not,
        mechanics are regenerated once with that failure as guidance. The
        visitor still has to approve the mechanics before /run will execute.
        """
        description = body.get("description")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a nonempty string")
        model = _requested_model(body)
        world_kind = body.get("world_kind") or "task"
        if world_kind not in WORLD_KINDS:
            raise ValueError(f"world_kind must be one of {list(WORLD_KINDS)}")
        trace_id = f"{TRACE_ROOT}/world/{uuid.uuid4().hex}"
        with _LLM_LOCK:
            budget = self._llm_budget(client, WORLD_BUDGET)
            if budget is None:
                return
            try:
                bundle, not_modeled, _ = generate_world_bundle(
                    description, model=model, trace_id=trace_id, max_budget=budget, world_kind=world_kind,
                )
                guidance = ""
                attempts: list[dict[str, Any]] = []
                # Keep the best attempt: reaching the finish line beats merely
                # allowing actions, which beats allowing nothing.
                best: tuple[tuple[int, int], dict[str, Any], CausalModel, dict[str, Any]] | None = None
                for attempt in range(2):
                    try:
                        generated, _ = generate_causal_model(
                            bundle,
                            model=model if attempt == 0 else RULES_RETRY_MODEL,
                            trace_id=trace_id,
                            max_budget=budget,
                            guidance=guidance,
                            model_justification=None if attempt == 0 else RULES_RETRY_JUSTIFICATION,
                            world_kind=world_kind,
                        )
                        candidate = _strip_review(generated)
                        candidate_compiled = CausalModel.from_dict(candidate, bundle=bundle)
                    except (ActionDeclarationError, ValueError, TypeError, KeyError) as error:
                        # A rule set the compiler rejects is the cheapest failure to
                        # recover from: hand it to the stronger retry instead of
                        # ending the whole request.
                        attempts.append({"ok": False, "error": f"rules rejected by the compiler: {error}"[:300]})
                        if attempt == 1 or _trace_cost(trace_id) >= budget - 0.01:
                            if best is None:
                                raise
                            break
                        guidance = (
                            "Your previous proposal was rejected by the local causal compiler: "
                            f"{type(error).__name__}: {error}. Return a corrected proposal."
                        )
                        continue
                    try:
                        dry_turns = DRY_RUN_TURNS if world_kind == "task" else DRY_RUN_TURNS_CONTINUING
                        dry, _, _ = run_world(
                            bundle, candidate, policy="scripted", max_turns=dry_turns,
                            trace_id=f"{trace_id}/dry-run-{attempt}",
                        )
                        result_row = {"ok": True, **dry["summary"]}
                        if world_kind != "task":
                            # Ongoing/open worlds succeed by staying alive, not by finishing.
                            alive = (
                                candidate_compiled.terminal is None
                                and bool(candidate_compiled.processes)
                                and dry["summary"]["active_at_end"]
                            )
                            idle = list(dry["summary"].get("idle_actors") or [])
                            # Best: alive with every actor taking part; then alive; then not.
                            score = (3 if not idle else 2) if alive else 1
                            guidance = "" if alive else (
                                f"This is an {world_kind} world. A deterministic dry run of your previous mechanics "
                                f"gave: terminal {'present' if candidate_compiled.terminal else 'null'}, "
                                f"{len(candidate_compiled.processes)} processes, active in the last rounds: "
                                f"{dry['summary']['active_at_end']} (over {dry_turns} rounds). Set terminal to null and add "
                                "processes so state keeps changing and the actors keep having useful actions in every "
                                "round indefinitely: needs and resources must keep cycling (for example hunger rises, "
                                "eating lowers it, food regrows), never just run down to a stop."
                            )
                            if idle:
                                guidance += _idle_guidance(dry, idle, dry_turns)
                            finishes = None
                        else:
                            finishes = candidate_compiled.terminal is not None and dry["summary"]["terminal_reached"]
                            score = 2 if finishes else 1
                        if finishes is None:
                            pass
                        elif finishes:
                            guidance = ""
                        elif candidate_compiled.terminal is None:
                            guidance = (
                                "Your previous mechanics had terminal: null. The description has a goal; propose a "
                                "terminal condition derived from represented state (e.g. every order's stage is "
                                "served), and make the effects move state toward it."
                            )
                        else:
                            guidance = (
                                f"A deterministic dry run of your previous mechanics allowed "
                                f"{dry['summary']['accepted_actions']} actions over {DRY_RUN_TURNS} rounds but never "
                                "reached the terminal condition. Make the effects move represented state toward "
                                "the terminal condition (and keep checks from allowing the same useless action forever)."
                            )
                    except ValueError as error:
                        result_row = {"ok": False, "error": str(error)[:300]}
                        score = 0
                        refusals = _initial_refusals(bundle, candidate)
                        guidance = (
                            "A deterministic dry run of your previous mechanics from the initial state "
                            f"failed: {error}. In the starting state every action was refused because these "
                            "checks were false: " + "; ".join(refusals) + ". Remove or correct checks that "
                            "contradict the initial state (see initial_builtin_state and entity component "
                            "values) so at least one actor can act, keeping effects consistent with the "
                            "action descriptions."
                        )
                    attempts.append(result_row)
                    # Ties go to the attempt with fewer actors who never acted.
                    rank = (score, -len(result_row.get("idle_actors") or []))
                    if best is None or rank > best[0]:
                        best = (rank, candidate, candidate_compiled, result_row)
                    if score >= (2 if world_kind == "task" else 3) or attempt == 1 or _trace_cost(trace_id) >= budget - 0.01:
                        break
                assert best is not None
                _, causal, compiled, best_row = best
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_failed_call(budget, trace_id)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "description": description,
                "world_kind": world_kind,
                "not_modeled": not_modeled,
                "bundle": bundle,
                "causal_model": causal,
                "review": compiled.as_review(),
                "dry_run": best_row,
                "dry_run_attempts": attempts,
                "cost_usd": trace_cost,
                "daily_cost_usd": daily_cost,
                "trace_id": trace_id,
            },
        )

    def _generate_draft(self, client: str, body: dict[str, Any]) -> None:
        description = body.get("description")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("description must be a nonempty string")
        if len(description) > 8000:
            raise ValueError("description must be at most 8000 characters")
        model = _requested_model(body)
        trace_id = f"{TRACE_ROOT}/draft/{uuid.uuid4().hex}"
        with _LLM_LOCK:
            budget = self._llm_budget(client, DRAFT_BUDGET)
            if budget is None:
                return
            try:
                draft, bundle, review, result = generate_native_coordination_draft(
                    description,
                    model=model,
                    trace_id=trace_id,
                    max_budget=budget,
                )
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_failed_call(budget, trace_id)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "draft": draft,
                "bundle": bundle,
                "causal_model": json.loads(NATIVE_COORDINATION_CAUSAL.read_text()),
                "review": review,
                "model": getattr(result, "model", model),
                "cost_usd": trace_cost,
                "daily_cost_usd": daily_cost,
                "trace_id": trace_id,
            },
        )

    def _generate(self, client: str, body: dict[str, Any]) -> None:
        bundle = validate_bundle(body.get("bundle"))
        model = _requested_model(body)
        trace_id = f"{TRACE_ROOT}/mechanics/{uuid.uuid4().hex}"
        guidance = body.get("guidance") or ""
        if not isinstance(guidance, str):
            raise ValueError("guidance must be a string")
        # Serialize public LLM calls so two concurrent requests cannot both see
        # the same remaining daily budget and oversubscribe it.
        with _LLM_LOCK:
            budget = self._llm_budget(client, MECHANICS_BUDGET)
            if budget is None:
                return
            try:
                generated, result = generate_causal_model(
                    bundle,
                    model=model,
                    trace_id=trace_id,
                    max_budget=budget,
                    guidance=guidance[:4000],
                )
                causal = _strip_review(generated)
                compiled = CausalModel.from_dict(causal, bundle=bundle)
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_failed_call(budget, trace_id)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "causal_model": causal,
                "review": compiled.as_review(),
                "model": getattr(result, "model", model),
                "cost_usd": trace_cost,
                "daily_cost_usd": daily_cost,
                "trace_id": trace_id,
            },
        )

    def _compare_native_coordination(self, client: str, body: dict[str, Any]) -> None:
        if body.get("approved") is not True:
            self._error(
                HTTPStatus.CONFLICT,
                "mechanics must be explicitly approved before a comparison",
            )
            return
        baseline = validate_bundle(body.get("baseline_bundle"))
        causal = body.get("causal_model")
        if not isinstance(causal, dict):
            raise ValueError("causal_model must be an object")
        CausalModel.from_dict(causal, bundle=baseline)
        shared_causal = json.loads(NATIVE_COORDINATION_CAUSAL.read_text())
        if causal != shared_causal:
            raise ValueError(
                "native coordination comparison requires the reviewed shared coordination mechanics"
            )
        required = body.get("required_approvals")
        comparison_bundle, change = with_approval_threshold(baseline, required)
        CausalModel.from_dict(causal, bundle=comparison_bundle)
        trace_id = f"{TRACE_ROOT}/comparison/{uuid.uuid4().hex}"
        native = run_native_coordination(comparison_bundle, causal)
        trace = native["trace"]
        compiled = native["causal_model"]
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "summary": trace["summary"],
                "trace": trace,
                "causal_review": compiled.as_review(),
                "replay_html": native["html"],
                "comparison_bundle": comparison_bundle,
                "change": change,
                "cost_usd": 0.0,
                "daily_cost_usd": None,
                "execution_mode": "native_coordination_comparison",
                "trace_id": trace_id,
            },
        )

    def _run(self, client: str, body: dict[str, Any]) -> None:
        if body.get("approved") is not True:
            self._error(HTTPStatus.CONFLICT, "mechanics must be explicitly approved before a run")
            return
        bundle = validate_bundle(body.get("bundle"))
        causal = body.get("causal_model")
        if not isinstance(causal, dict):
            raise ValueError("causal_model must be an object")
        # Compile before any policy/model call. This is the install authority gate.
        CausalModel.from_dict(causal, bundle=bundle)
        execution_mode = str(body.get("execution_mode") or "authored_world")
        if execution_mode not in {"authored_world", "native_coordination"}:
            raise ValueError("execution_mode must be authored_world or native_coordination")
        policy = str(body.get("policy") or "scripted")
        turns = body.get("turns", 12)
        if type(turns) is not int:
            raise ValueError("turns must be an integer")
        continue_from = body.get("continue_from")
        if continue_from is not None and not isinstance(continue_from, dict):
            raise ValueError("continue_from must be a snapshot object")
        turn_offset = body.get("turn_offset", 0)
        if type(turn_offset) is not int or not 0 <= turn_offset <= MAX_CONTINUED_TURNS:
            raise ValueError(f"turn_offset must be an integer between 0 and {MAX_CONTINUED_TURNS}")
        # The last few moves before this round, so AI characters remember what
        # just happened when live play continues one round at a time.
        recent = body.get("recent") or []
        if (
            not isinstance(recent, list) or len(recent) > MAX_RECENT_MOVES
            or not all(isinstance(m, dict) and set(m) == {"actor", "action"}
                       and all(isinstance(v, str) and 0 < len(v) <= 80 for v in m.values()) for m in recent)
        ):
            raise ValueError(f"recent must be up to {MAX_RECENT_MOVES} {{actor, action}} moves")
        model = _requested_model(body)
        trace_id = f"{TRACE_ROOT}/run/{uuid.uuid4().hex}"
        if execution_mode == "native_coordination":
            shared_causal = json.loads(NATIVE_COORDINATION_CAUSAL.read_text())
            if causal != shared_causal:
                raise ValueError(
                    "native_coordination execution requires the reviewed shared coordination mechanics"
                )
            if policy != "scripted":
                raise ValueError("native_coordination execution is deterministic scripted-only in v0")
            native = run_native_coordination(bundle, causal)
            trace = native["trace"]
            compiled = native["causal_model"]
            replay = native["html"]
            daily_cost = None
        elif policy == "llm":
            with _LLM_LOCK:
                budget = self._llm_budget(client, RUN_BUDGET, ai_run=True)
                if budget is None:
                    return
                try:
                    trace, _, compiled = run_world(
                        bundle, causal, policy=policy, model_name=model,
                        max_turns=turns, max_budget=budget, trace_id=trace_id,
                        start_snapshot=continue_from, turn_offset=turn_offset, prior_recent=recent,
                    )
                    trace_cost = _trace_cost(trace_id)
                except Exception:
                    _settle_failed_call(budget, trace_id)
                    raise
                daily_cost = _settle_daily_budget(budget, trace_cost)
                trace["cost_usd"] = trace_cost
        else:
            trace, _, compiled = run_world(
                bundle, causal, policy=policy, model_name=model,
                max_turns=turns, max_budget=RUN_BUDGET, trace_id=trace_id,
                start_snapshot=continue_from, turn_offset=turn_offset, prior_recent=recent,
            )
            daily_cost = None
        if execution_mode == "authored_world":
            replay = render_run(bundle, trace, compiled)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "summary": trace["summary"],
                "trace": trace,
                "causal_review": compiled.as_review(),
                "replay_html": replay,
                "cost_usd": trace.get("cost_usd", 0.0),
                "daily_cost_usd": daily_cost,
                "execution_mode": execution_mode,
                "trace_id": trace_id,
            },
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8813)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), WorldBuilderHandler)
    print(f"World Builder API listening on http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
