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
import re
import sys
import threading
from concurrent.futures import wait as futures_wait
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

from scripts.attempts import attempt_findings, long_tasks, part_way_findings
from scripts.generate_causal_model import DEFAULT_MODEL, generate_causal_model
from scripts.generate_world_bundle import generate_world_bundle
from scripts.world_dialogue import clarify, surprise_description
from scripts.native_coordination_authoring import (
    DEFAULT_CAUSAL as NATIVE_COORDINATION_CAUSAL,
    generate_native_coordination_draft,
)
from scripts.native_coordination_comparison import with_approval_threshold
from scripts.people_world import about_people, prepare_people_world, unfinished_hedges, write_people_rules
from scripts.run_authored_world import MEMORY_ITEM_CHARS, MEMORY_ITEMS, actor_ids, build_engine, render_run, run_world
from scripts.run_native_coordination import run_native_coordination
from scripts.scaffold_world import BundleError, validate_bundle
from world_substrate.action_authoring import ActionDeclarationError, CausalModel

API_PREFIX = "/world-builder/api"
MAX_BODY_BYTES = 512_000
DRAFT_BUDGET = 0.08
MECHANICS_BUDGET = 0.12
RUN_BUDGET = 0.12
# Shared visitor allowance per day. Raised from $0.50 to $3 on 2026-10-15 (Brian approved, "yeah thats fine"):
# a people world costs up to PEOPLE_WORLD_BUDGET to build and its AI members choose every move.
DAILY_LLM_BUDGET = 3.00
# Owner override (Brian, 2026-10-05: "i always want to be able to put in a
# password to override the budget"). A request carrying the owner password in
# X-World-Builder-Owner skips the shared visitor allowance and per-visitor rate
# limits and spends from a separate owner ledger instead. Unset password: off.
OWNER_HEADER = "X-World-Builder-Owner"
# The owner's own test allowance; WORLD_BUILDER_OWNER_DAILY_BUDGET sets another for a server started with it (the
# override exists so the owner is never stopped by a budget an agent chose).
OWNER_DAILY_BUDGET = float(os.environ.get("WORLD_BUILDER_OWNER_DAILY_BUDGET") or 5.00)
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
# Description -> structure -> mechanics (+ dry-run-guided mechanics retries).
WORLD_BUDGET = 0.20
# Rules attempts for a world of things: the first draft plus rewrites, each told what the last test run showed,
# until a test run passes. #179, 2026-10-18 (pencil c4-run7/run8): one rewrite still left 5 of 7 moves never
# possible and was accepted anyway; a rules call costs about $0.005, so four fit WORLD_BUDGET easily.
RULES_ATTEMPTS = 4
# Ongoing worlds split RULES_ATTEMPTS across this many structures (#187).
STRUCTURE_ATTEMPTS = 2
# A people world (scripts/people_world.py): one stronger-model call for the people, goals and information, one for
# the rules, a small one for the attempts, at most one compiler- or test-run-guided rules retry. 2026-10-16 Waltzman
# (inc14b): the first rules cost $0.71 of $0.80, so the retry that would have fixed 9 of 10 stalled people never ran;
# $1.30 leaves room for it.
PEOPLE_WORLD_BUDGET = 1.30
# The small call that decides whether a description is a world of people or of things.
WORLD_KIND_BUDGET = 0.01
WORLD_DEFS = ("things", "people", "auto")
MAX_BRIEF_CHARS = 4000
# The model for the rules retries, set by WORLD_BUILDER_STRONG_MODEL (also scripts/people_world.py). History:
# 2026-10-05, the same six descriptions (scripts/measure_world_builder.py): gpt-5.6-luna finished 11/24 builds,
# gpt-5.6-sol 6/6, so the retry moved to sol. 2026-10-16, Brian: gpt-6-luna for everything for cost, sol only when
# sharing with Waltzman. 2026-10-23, the same six descriptions, four rounds, gpt-6-luna for every call: 23/24
# finished (the miss had correct rules; a 12-round test was too short for them), $0.0032 per build
# (evidence/luna-rules-2026-10-23). gpt-6-luna stays the default.
RULES_RETRY_MODEL = os.environ.get("WORLD_BUILDER_STRONG_MODEL") or "openrouter/openai/gpt-6-luna"
RULES_RETRY_JUSTIFICATION = (
    "World Builder rules retry: the first rules did not let the described world reach its finish line; "
    "the retry uses WORLD_BUILDER_STRONG_MODEL (gpt-6-luna measured 23/24 on 2026-10-23, against "
    "gpt-5.6-luna 11/24 and gpt-5.6-sol 6/6 on 2026-10-05)."
)
DRY_RUN_TURNS = 12
# Ongoing/open worlds must stay alive past the first visible run: live, an open
# village was busy for 12 rounds and then went quiet, so test twice as long.
DRY_RUN_TURNS_CONTINUING = 24
DRY_RUN_TURNS_LATE = 8
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
# One "What happened" readout reads every recorded event of a run (a 40-round, ten-person run is about 40k tokens).
READOUT_BUDGET = 0.10
# 2026-10-18 live Waltzman fYUjOhb2z1VC: one lock held for every whole build and round made the site run one AI job
# at a time, so round 1 waited ~100 s behind another visitor's build (C1: within 150 s). Ledger updates are atomic
# under _BUDGET_LOCK and every job reserves its whole cap first, so concurrent jobs cannot overspend.
AI_JOBS_AT_ONCE = int(os.environ.get("WORLD_BUILDER_AI_JOBS_AT_ONCE") or 4)
_AI_SLOTS = threading.BoundedSemaphore(AI_JOBS_AT_ONCE)
_BUDGET_LOCK = threading.RLock()


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
    with _BUDGET_LOCK:
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
    with _BUDGET_LOCK:
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


# Held for each duplicate build call still running when its build is settled (people_world.hedged), until its real
# cost is known; the visitor allowance therefore always covers it. A copy costs under $0.01 (2026-10-16 ledger).
LATE_HEDGE_RESERVE = 0.05
# A people build rewrites its rules after a weak test run only if it is this early: a rewrite takes 40-85 s and the
# first round must play within 150 s of pressing Create (goal best-of-all-worlds, C1).
PEOPLE_REWRITE_BY_S = float(os.environ.get("WORLD_BUILDER_REWRITE_BY_S") or 80)


def _settle_late_hedges(trace_id: str, charged: float) -> None:
    """Keep a reservation for this trace's still-running duplicate calls; charge their cost when they finish."""
    late = unfinished_hedges(trace_id)
    if not late:
        return
    reserve = LATE_HEDGE_RESERVE * len(late)
    with _BUDGET_LOCK:
        state = _load_budget_state()
        state["reserved_usd"] = float(state["reserved_usd"]) + reserve
        _write_budget_state(state)

    def settle() -> None:
        futures_wait(late, timeout=900)
        try:
            extra = max(0.0, _trace_cost(trace_id) - charged)
        except Exception:
            extra = reserve  # fail closed, like _settle_daily_budget
        _settle_daily_budget(reserve, extra)

    # copy_context: the owner/visitor ledger choice (_LEDGER) lives in a context variable a new thread would lose
    threading.Thread(target=contextvars.copy_context().run, args=(settle,), name="late-hedges", daemon=True).start()


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
MAX_PROGRESS_STEPS = 40
MAX_PROGRESS_ITEMS = 16
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
                "/generate-mechanics", "/compare-native-coordination", "/readout")
CLIENT_HEADER = "X-World-Builder-Client"
_REQUEST: contextvars.ContextVar[dict[str, Any] | None] = contextvars.ContextVar("world_builder_request", default=None)
_RUN_LOG_LOCK = threading.Lock()


def _run_log_dir() -> Path:
    return Path(os.environ.get("WORLD_BUILDER_RUN_LOG_DIR") or BUDGET_STATE_PATH.parent / "runs")


def _fingerprint(client: str) -> str:
    salt = (_owner_password() or "world-builder").encode()
    return hmac.new(salt, client.encode(), "sha256").hexdigest()[:12]


def _world_fingerprint(bundle: Any, causal: Any) -> str | None:
    """Same world and rules -> same fingerprint, so a run can be matched to its build.

    Hashed as the browser hands the world back (`_canon`): c1r23's build held `1.0` where its rounds held `1`, so the
    share dropped the build and the readout read a people world as goods.
    """
    if not isinstance(bundle, dict) or not isinstance(causal, dict):
        return None
    canonical = json.dumps(_canon({"bundle": bundle, "causal_model": causal}), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def _canon(value: Any) -> Any:
    """JSON as the browser hands it back: whole floats become ints (JavaScript writes 2.0 as 2)."""
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, dict):
        return {k: _canon(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_canon(v) for v in value]
    return value


def _snapshot_seal(snapshot: Any, bundle: Any, causal: Any, approval: Any = None) -> str:
    """Issue #127 (G11): a keyed hash of the world state a round ended in, under these exact rules.

    The browser holds the state between live rounds; a continued round must bring back one this
    server sealed, so an edited state (or the same state under other rules) is refused.
    The first round's approval record is sealed with it (#122), so it cannot be swapped either.
    """
    key = (_owner_password() or "world-builder").encode()
    canonical = json.dumps(_canon({"snapshot": snapshot, "bundle": bundle, "causal_model": causal,
                                  "approval": approval}),
                           sort_keys=True, separators=(",", ":"))
    return hmac.new(key, canonical.encode(), "sha256").hexdigest()


def _approval_record(*, bundle: Any, causal: Any, trace: dict[str, Any]) -> dict[str, Any]:
    request = _REQUEST.get() or {}
    who = request.get("who") or "visitor"
    return {
        "approval_id": uuid.uuid4().hex[:12],
        "approved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "approved_by": f"visitor:{request.get('client')}" if who == "visitor" else who,
        "mechanic_profile_id": trace.get("mechanic_profile_id"),
        "world_fingerprint": _world_fingerprint(bundle, causal),
    }


def _request_summary(path: str, body: dict[str, Any]) -> dict[str, Any]:
    keep = ("description", "world_kind", "policy", "turns", "turn_offset", "approved", "execution_mode", "async")
    out = {k: body[k] for k in keep if k in body}
    if path == "/readout":
        out["run_trace_ids"] = body.get("run_trace_ids")
        out["build_trace_id"] = body.get("build_trace_id")
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
            # What a shared run shows beside its rounds (increment 5, best-of-all-worlds.goal.md).
            "world_def": value.get("world_def"),
            "world_kind": value.get("world_kind"),
            "people": value.get("people"),
            "briefs": value.get("briefs"),
        }
    if path == "/run":
        trace = value.get("trace") or {}
        return {
            "summary": value.get("summary"),
            "mover": trace.get("model"),
            # Concordia residents' memories after the round (policy resident), the state each person decided from.
            "resident_memory": trace.get("resident_memory"),
            # The frozen rules identity (MechanicProfile.freeze()): same id, same
            # installed law. Gap G7 (docs/model/VIEW_COVERAGE.md): it was dropped.
            "mechanic_profile_id": trace.get("mechanic_profile_id"),
            "transcript": trace.get("transcript"),
            # Where the world ended up, so the next live round (or a later replay) starts from it.
            "final_snapshot": trace.get("final_snapshot"),
            "approval": value.get("approval"),
        }
    if path == "/clarify":
        return {k: value.get(k) for k in ("reply", "questions", "description", "ready")}
    if path == "/readout":
        return {"readout": value.get("readout")}
    if path == "/surprise":
        return {k: value.get(k) for k in ("theme", "description")}
    # Gap G4: these logged only key names. Keep the full result; cost and trace id
    # are already on the line, and a replay page is rebuilt from its trace.
    if path == "/generate-mechanics":
        return _full_result(value)
    if path == "/generate-draft":
        return _full_result(value)
    if path == "/compare-native-coordination":
        return _full_result(value)
    return {"keys": sorted(value)[:20]}


def _full_result(value: dict[str, Any]) -> dict[str, Any]:
    on_line = {"ok", "cost_usd", "daily_cost_usd", "trace_id"}
    return {k: v for k, v in value.items() if k not in on_line and not k.endswith("html")}


def _new_trace_id(kind: str) -> str:
    """A fresh llm_client trace id, remembered on the current request so its run-log line names it even on failure."""
    trace_id = f"{TRACE_ROOT}/{kind}/{uuid.uuid4().hex}"
    request = _REQUEST.get()
    if request is not None:
        request.setdefault("trace_ids", []).append(trace_id)
    return trace_id


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
        # 2026-10-16: a build stopped by its budget logged trace_id None although llm_client had traced it.
        "trace_id": value.get("trace_id") or (request.get("trace_ids") or [None])[-1],
        "trace_ids": request.get("trace_ids") or [],
        "cost_usd": value.get("cost_usd"),
        "request": request["summary"],
        "result": _result_summary(request["path"], int(status), value),
    }
    if request.get("engine_events") is not None and status < 400:
        entry["result"]["engine_events"] = request["engine_events"]
    try:
        directory = _run_log_dir()
        directory.mkdir(parents=True, exist_ok=True)
        line = json.dumps(entry, separators=(",", ":"), default=str) + "\n"
        with _RUN_LOG_LOCK, open(directory / f"runs_{entry['ts'][:10]}.jsonl", "a") as handle:
            handle.write(line)
    except Exception as error:  # observability must never break the request
        print(f"world-builder-api: run log write failed: {type(error).__name__}: {error}", flush=True)


SHARE_SCHEMA = "world-builder-share/v1"
_TRACE_PATTERN = re.compile(rf"{re.escape(TRACE_ROOT)}/[a-z-]+/[0-9a-f]{{32}}")
MAX_SHARED_RUNS = 500  # rounds are fetched one request at a time, so one run id per round
SHARES_PER_CLIENT_PER_DAY = 30
SHARE_LOOKBACK_DAYS = 3
_SHARE_LOCK = threading.Lock()


def _share_db() -> Path:
    return Path(os.environ.get("WORLD_BUILDER_SHARE_DB") or _run_log_dir().parent / "shares.sqlite")


def _share_connect():
    import sqlite3
    path = _share_db()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS shares (id TEXT PRIMARY KEY, created TEXT NOT NULL, client TEXT NOT NULL, "
               "record BLOB NOT NULL)")
    return db


def _logged_entries(trace_ids: set[str]) -> dict[str, dict[str, Any]]:
    """The run-log entries (recent days) whose trace id is wanted, by trace id."""
    found: dict[str, dict[str, Any]] = {}
    for path in sorted(_run_log_dir().glob("runs_*.jsonl"), reverse=True)[:SHARE_LOOKBACK_DAYS]:
        with open(path) as handle:
            for line in handle:
                if not any(t in line for t in trace_ids - set(found)):
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("trace_id") in trace_ids and int(row.get("status") or 0) == 200:
                    found[row["trace_id"]] = row
        if len(found) == len(trace_ids):
            break
    return found


def _assemble_share(build_trace_id: str | None, run_trace_ids: list[str]) -> dict[str, Any]:
    """A finished run rebuilt from the server's own run log, never from what the page sends: every round is the
    recorded result of a /run this service answered, in order, on one world and one rule set."""
    wanted = set(run_trace_ids) | ({build_trace_id} if build_trace_id else set())
    rows = _logged_entries(wanted)
    missing = [t for t in run_trace_ids if t not in rows]
    if missing:
        raise ValueError(f"{len(missing)} of the {len(run_trace_ids)} rounds are not in this server's recent run log, "
                         "so this run cannot be shared")
    runs = sorted((rows[t] for t in run_trace_ids), key=lambda r: (r["result"].get("summary") or {}).get("first_turn") or 0)
    first = runs[0]
    if first["path"] != "/run" or first["request"].get("continued") or not isinstance(first["request"].get("bundle"), dict):
        raise ValueError("a shared run must start from round 1 of its world")
    fingerprint = first["request"].get("world_fingerprint")
    rounds: list[dict[str, Any]] = []
    last = 0
    for row in runs:
        if row["path"] != "/run" or row["request"].get("world_fingerprint") != fingerprint:
            raise ValueError("those rounds come from different worlds or rules")
        transcript = row["result"].get("transcript") or []
        if transcript and transcript[0].get("turn") != last + 1:
            raise ValueError("those rounds are not one unbroken run")
        rounds += transcript
        last = (row["result"].get("summary") or {}).get("last_turn") or last
    bundle, causal = first["request"]["bundle"], first["request"]["causal_model"]
    build = rows.get(build_trace_id) if build_trace_id else None
    # Recomputed from the logged world and rules, so rows logged before the fingerprint ignored 2.0 vs 2 still match.
    build_fingerprint = (_world_fingerprint((build["result"] or {}).get("bundle"), (build["result"] or {}).get("causal_model"))
                         if build is not None else None)
    if build is not None and (build["path"] != "/generate-world"
                              or build_fingerprint != _world_fingerprint(first["request"]["bundle"],
                                                                         first["request"].get("causal_model"))
                              or build.get("client") != first.get("client")):
        # The rules were edited after the build, it is another build, or another visitor's build (its description
        # and briefs are theirs): show the run without a build.
        build = None
    built = (build or {}).get("result") or {}
    return {
        "schema": SHARE_SCHEMA,
        "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "world": {
            "description": (build or {}).get("request", {}).get("description"),
            "world_def": built.get("world_def"),
            "world_kind": built.get("world_kind"),
            "people": built.get("people"),
            "briefs": built.get("briefs"),
            "dry_run": built.get("dry_run"),
            "bundle": bundle,
            "causal_model": causal,
            "review": CausalModel.from_dict(causal, bundle=validate_bundle(bundle)).as_review(),
            "trace_id": build_trace_id if build is not None else None,
        },
        "rounds": rounds,
        "runs": [{"trace_id": r["trace_id"], "mover": r["result"].get("mover"), "policy": r["request"].get("policy"),
                  "first_turn": (r["result"].get("summary") or {}).get("first_turn"),
                  "last_turn": (r["result"].get("summary") or {}).get("last_turn"), "cost_usd": r.get("cost_usd")}
                 for r in runs],
        "world_fingerprint": fingerprint,
    }


def _save_share(client: str, record: dict[str, Any]) -> str | None:
    """Store one shared run; None when this visitor already shared too many today."""
    import gzip
    import secrets
    with _SHARE_LOCK:
        db = _share_connect()
        try:
            today = time.strftime("%Y-%m-%d", time.gmtime())
            (count,) = db.execute("SELECT COUNT(*) FROM shares WHERE client = ? AND created >= ?",
                                  (client, today)).fetchone()
            if count >= SHARES_PER_CLIENT_PER_DAY and not _is_owner():
                return None
            share_id = secrets.token_urlsafe(9)
            db.execute("INSERT INTO shares VALUES (?, ?, ?, ?)", (share_id, record["created"], client,
                       gzip.compress(json.dumps(record, separators=(",", ":")).encode())))
            db.commit()
            return share_id
        finally:
            db.close()


def _load_share(share_id: str) -> dict[str, Any] | None:
    import gzip
    if not re.fullmatch(r"[A-Za-z0-9_-]{6,32}", share_id):
        return None
    db = _share_connect()
    try:
        row = db.execute("SELECT record FROM shares WHERE id = ?", (share_id,)).fetchone()
    finally:
        db.close()
    return json.loads(gzip.decompress(row[0])) if row else None


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

    def _progress(self, state: str, step: str, detail: str = "", items: list[str] | None = None) -> None:
        """Record one build step so the page can show it while the job runs."""
        with _JOBS_LOCK:
            job = _JOBS.get(self.job_id)
            if job is None:
                return
            steps = job.setdefault("progress", [])
            if len(steps) < MAX_PROGRESS_STEPS:
                steps.append({
                    "at_s": round(time.time() - job["created"], 1),
                    "state": state,
                    "step": step,
                    "detail": detail,
                    "items": [str(x)[:80] for x in (items or [])[:MAX_PROGRESS_ITEMS]],
                })


def _words(name: str) -> str:
    return str(name).replace("_", " ").replace("-", " ")


def _decision_settled(snapshot: Any) -> bool:
    """True when the world holds a group decision that is deployed or rejected (compile_spec's decision family)."""
    entities = ((snapshot or {}).get("world") or {}).get("entities") or {}
    return any(((e.get("components") or {}).get("group_decision") or {}).get("status") in ("deployed", "rejected")
               for e in entities.values() if isinstance(e, dict))


def _budget_message(error: Exception) -> str:
    """Plain words for an AI budget stop: this build's own allowance, or the service's monthly one."""
    if "monthly allowance" in str(error):
        # 2026-10-15: a local build hit llm_client's per-project monthly cap and reported it as "needed more AI work".
        return "The World Builder has used its AI allowance for this month, so it cannot build new worlds right now."
    return "This description needed more AI work than one build allows. Try a shorter or simpler description."


# llm_client errors with a plain meaning for a visitor, by class name (llm_client is imported lazily). 2026-10-16: the
# shared OpenRouter account ran out of credit and the page said "internal world-builder error".
_PROVIDER_FAILURES = {
    "LLMQuotaExhaustedError": (HTTPStatus.SERVICE_UNAVAILABLE,
                               "The AI service behind the World Builder has run out of credit, so it cannot build "
                               "worlds or choose AI moves right now. Simple moves still work."),
    "LLMRateLimitError": (HTTPStatus.SERVICE_UNAVAILABLE,
                          "The AI service behind the World Builder is busy. Try again in a minute."),
    "LLMTransientError": (HTTPStatus.SERVICE_UNAVAILABLE,
                          "The AI service behind the World Builder did not answer. Try again in a minute."),
    "LLMAuthError": (HTTPStatus.SERVICE_UNAVAILABLE,
                     "The World Builder cannot reach its AI service right now (its access was refused)."),
}


def _provider_failure(error: BaseException) -> tuple[HTTPStatus, str] | None:
    """A plain status and message for an AI-provider failure anywhere in the error's cause chain, else None."""
    seen: set[int] = set()
    current: BaseException | None = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        name = type(current).__name__
        if name == "LLMBudgetExceededError":
            return HTTPStatus.UNPROCESSABLE_ENTITY, _budget_message(current)
        if name in _PROVIDER_FAILURES:
            return _PROVIDER_FAILURES[name]
        current = current.__cause__ or current.__context__
    return None


def _dry_run_sentence(row: dict[str, Any], world_kind: str) -> str:
    """One plain sentence about a quick test run, for the build progress list."""
    if not row.get("ok"):
        return "nobody could act from the starting state"
    moves = row.get("accepted_actions", 0)
    rounds = row.get("turns", 0)
    head = f"{moves} move{'s' if moves != 1 else ''} in {rounds} round{'s' if rounds != 1 else ''}"
    if world_kind == "task":
        return head + ("; reached the finish line" if row.get("terminal_reached") else "; did not reach the finish line")
    never = row.get("never_offered") or []
    tasks = row.get("long_tasks")
    fail = sorted({_words(t["action"]) for t in tasks or [] if t["can_fail_part_way"]
                   and t.get("started_by", "person") == "person"})
    world = sorted({_words(t["action"]) for t in tasks or [] if t.get("started_by") == "world"})
    return (head + ("; still busy at the end" if row.get("active_at_end") else "; went quiet by the end")
            + (f"; never possible: {', '.join(_words(k) for k in never)}" if never else "")
            + ("" if tasks is None else f"; can fail part-way: {', '.join(fail)}" if fail
               else "; no task a person starts can fail part-way" if tasks else "; no task takes several rounds")
            + (f"; followed as the world's own tasks: {', '.join(world)}" if world else "")
            + ("; a move refuses up front on what its own task uses up" if row.get("attempt_findings") else "")
            + ("" if row.get("knock_on_processes") is None
               else f"; knock-on effects: {', '.join(_words(k) for k in row['knock_on_processes'])}"
               if row["knock_on_processes"] else "; nothing sets off a knock-on effect"))


def _idle_guidance(dry: dict[str, Any], idle: list[str], turns: int) -> str:
    """Tell the rules model which actors stopped acting in the dry run, and why (latest reasons first)."""
    reasons: dict[str, list[str]] = {}
    for turn in reversed(dry.get("transcript") or []):
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
        f" In the {turns}-round test these actors stopped being able to do anything (or never could): {detail}. Every actor role must be able "
        "to act regularly: make sure some actor's action brings what each one's action needs to where it is "
        "checked (for example, if a carrier must hold goods before delivering, give another actor an action "
        "that loads goods onto the carrier, or let the carrier pick them up itself). A process may renew raw "
        "materials at their source or bring new demand, but never supply what an action makes or move goods between places."
    )


def _unsourced_inputs(bundle: dict[str, Any], causal: dict[str, Any]) -> list[str]:
    """Fields some move uses up that nothing ever makes or renews and that everyone starts with none of.

    2026-10-26 pencil build (share NZD33sh3iX29): assembling a pencil needed clay, paint, erasers and ferrules,
    no actor or process produced any of them and every stock started at 0, so no pencil and no sale could ever
    happen. Read from the effect structure: moving a field from one holder to another is not a source.
    """
    used: set[str] = set()
    made: set[str] = set()
    for mechanic in causal.get("mechanics") or []:
        effects = mechanic.get("effects") or []
        taken = {e.get("path") for e in effects if e.get("op") == "subtract"}
        used |= taken
        made |= {e.get("path") for e in effects if e.get("op") in ("add", "set") and e.get("path") not in taken}
    for process in causal.get("processes") or []:
        made |= {e.get("path") for e in process.get("effects") or [] if e.get("op") in ("add", "set")}

    def held(path: str) -> bool:
        parts = path.split(".")
        if len(parts) != 3 or parts[0] != "components":
            return True
        values = [((entity.get("components") or {}).get(parts[1]) or {}).get(parts[2]) for entity in bundle.get("entities") or []]
        return any(isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0 for v in values)

    return sorted({path.rsplit(".", 1)[-1] for path in used - made if path and not held(path)})


def _conjuring_processes(causal: dict[str, Any]) -> list[str]:
    """'process adds field (made by action)' for each process that creates a good some action makes from others.

    2026-10-20 c4-run14 (trace world-builder-live/world/41373883...): restock-production-inputs added boards,
    graphite and pencils to every inventory each round, so every worker looked busy while nothing flowed.
    An action makes a field when it adds to it while using up a different field; a process may still renew
    gathered raw materials or demand. A process collides only when its selector could reach the entity
    the making action adds to (shared category, or either side names none).
    """
    def field(path: str) -> str:
        return path.split(".", 1)[1] if path.startswith("components.") else path

    made: dict[str, list[tuple[str, set[str]]]] = {}
    for mechanic in causal.get("mechanics") or []:
        roles = {**(mechanic.get("participants") or {}), "actor": mechanic.get("actor_selector") or {}}
        effects = mechanic.get("effects") or []
        used = {field(e["path"]) for e in effects if e.get("op") == "subtract"}
        for effect in effects:
            target = field(effect["path"])
            if effect.get("op") != "add" or target in used or not used - {target}:
                continue
            categories = set((roles.get(effect.get("participant")) or {}).get("categories") or [])
            made.setdefault(target, []).append((mechanic.get("action_kind", "?"), categories))
    found: list[str] = []
    for process in causal.get("processes") or []:
        reach = set((process.get("selector") or {}).get("categories") or [])
        for effect in process.get("effects") or []:
            if effect.get("op") != "add" or effect.get("participant") != "it":
                continue
            target = field(effect["path"])
            for kind, categories in made.get(target, []):
                if not reach or not categories or reach & categories:
                    found.append(f"{process.get('process_id', '?')} adds {target} (made by {kind})")
                    break
    return found


def _retry_label(first_model: str) -> str:
    """The progress line for a rules retry: it claims a stronger model only when the retry uses a different one
    (#255: with WORLD_BUILDER_STRONG_MODEL unset the retry ran on the same model as the first try)."""
    return "Rewriting the rules with a stronger model" if RULES_RETRY_MODEL != first_model else "Rewriting the rules"


def _attempt_rank(score: int, row: dict[str, Any]) -> tuple[int, bool, int, int, int, bool]:
    """Order rules attempts: by score, then ties go to a test run that did not go in circles, then to fewer moves
    never offered, then to fewer people who stopped acting (#253: an airfield build kept the one test run that
    circled and never offered `move`, because it had one stalled person fewer), and last to one whose rules have a
    knock-on process."""
    idle = set(row.get("idle_actors") or []) | set(row.get("stalled_actors") or [])
    # A move no world entity can ever take part in loses first (2026-10-27 pencil iMrL2U84cLCS kept the attempt
    # whose shipping could never happen over one where every move ran).
    return (score, not row.get("circling"), -len(row.get("missing_components") or []),
            -len(row.get("never_offered") or []), -len(idle),
            bool(row.get("knock_on_processes")))


def _state_flips(causal: dict[str, Any]) -> list[str]:
    """Action kinds that set a thing's yes/no field to a fixed value (tip over, break, switch off): the changes a
    knock-on process could follow. Read from the effect structure, not from names."""
    return sorted({
        m.get("action_kind", "")
        for m in causal.get("mechanics") or []
        for e in m.get("effects") or []
        if e.get("op") == "set" and isinstance((e.get("value") or {}).get("literal"), bool)
    })


def _knock_on_processes(causal: dict[str, Any]) -> list[str]:
    """Ids of the processes that run at once as a knock-on of another change (timing immediately, Decision 009).

    The build record names them, or says there are none, so a world in which nothing can set off a chain is visible
    instead of looking like slice 2 failed (2026-10-26 airfield: six rules answers, none wrote one).
    """
    return [p.get("process_id", "") for p in causal.get("processes") or [] if p.get("timing") == "immediately"]


def _missing_components(bundle: dict[str, Any], causal: dict[str, Any]) -> list[str]:
    """'kind needs component' for each move whose actor or participant must have a component no entity has.

    2026-10-27 pencil build (share iMrL2U84cLCS): ship-pencil-boxes required the shop to have a `shipment`
    component that no entity had, so no box could ever ship; the attempt still won the tie-break.
    """
    held = {name for entity in bundle.get("entities") or [] for name in (entity.get("components") or {})}
    found: set[str] = set()
    for mechanic in causal.get("mechanics") or []:
        selectors = [mechanic.get("actor_selector") or {}, *(mechanic.get("participants") or {}).values()]
        for selector in selectors:
            for name in (selector or {}).get("components") or []:
                if name not in held:
                    found.add(f"{mechanic.get('action_kind', '?')} needs {name}")
    return sorted(found)


def _dead_end_stock(bundle: dict[str, Any], causal: dict[str, Any]) -> list[str]:
    """'good piles up at entity (move)' where a move makes or supplies a good that some step uses up, at an entity no
    move or process ever takes it from.

    2026-10-27 pencil build (share iMrL2U84cLCS): the materials supplier added clay, paint, erasers, ferrules and
    boxes to its own stock every few rounds and nothing carried them on, so the factory ran down its starting stock.
    Read from selectors against the world's entities, because every business keeps goods in the same component.
    Hand-overs (a move that takes and gives the same good) and tallies nothing ever uses up are not named.
    """
    entities = bundle.get("entities") or []
    mechanics = causal.get("mechanics") or []

    def fits(selector: Any, entity: dict[str, Any]) -> bool:
        selector = selector or {}
        return (set(selector.get("categories") or []) <= set(entity.get("categories") or [])
                and set(selector.get("components") or []) <= set(entity.get("components") or {}))

    def role(mechanic: dict[str, Any], name: Any) -> Any:
        return mechanic.get("actor_selector") if name == "actor" else (mechanic.get("participants") or {}).get(name)

    takers = [(e.get("path"), role(m, e.get("participant")))
              for m in mechanics for e in m.get("effects") or [] if e.get("op") == "subtract"]
    takers += [(e.get("path"), p.get("selector")) for p in causal.get("processes") or []
               for e in p.get("effects") or [] if e.get("op") == "subtract" and e.get("participant") == "it"]
    used = {str(path).rsplit(".", 1)[-1] for path, _ in takers}
    found: set[str] = set()
    for mechanic in mechanics:
        effects = mechanic.get("effects") or []
        handed = {str(e.get("path")).rsplit(".", 1)[-1] for e in effects if e.get("op") == "subtract"}
        for effect in effects:
            path = str(effect.get("path") or "")
            good = path.rsplit(".", 1)[-1]
            if effect.get("op") != "add" or not path.startswith("components.") or good in handed or good not in used:
                continue
            for entity in entities:
                if fits(role(mechanic, effect.get("participant")), entity) and not any(
                        taken == path and fits(selector, entity) for taken, selector in takers):
                    found.add(f"{good} piles up at {entity.get('id', '?')} ({mechanic.get('action_kind', '?')})")
    return sorted(found)


def _starved_holders(bundle: dict[str, Any], causal: dict[str, Any]) -> list[str]:
    """'move needs good at holder, which starts with none and nothing ever gives it any', read per holder.

    2026-10-28 pencil build (share q2sG4d_J7279, evidence/pencil9-trace-audit/): sell-pencils took a box from the
    shop's own stock, the shop started with no boxes, and the only move that added boxes added them at the factory;
    the delivery put them "in transit" and nothing ever landed them. The shop never sold in 17 rounds. _unsourced_inputs
    missed it because it asks whether anyone holds or makes boxes, and the factory did.
    """
    entities = bundle.get("entities") or []
    mechanics = causal.get("mechanics") or []

    def fits(selector: Any, entity: dict[str, Any]) -> bool:
        selector = selector or {}
        return (set(selector.get("categories") or []) <= set(entity.get("categories") or [])
                and set(selector.get("components") or []) <= set(entity.get("components") or {}))

    def role(rule: dict[str, Any], name: Any) -> Any:
        if name == "actor":
            return rule.get("actor_selector")
        if name == "it":
            return rule.get("selector")
        return (rule.get("participants") or {}).get(name)

    rules = [*mechanics, *(causal.get("processes") or [])]
    givers = [(e.get("path"), role(r, e.get("participant"))) for r in rules
              for e in r.get("effects") or [] if e.get("op") in ("add", "set")]
    needs = [(m, e.get("path"), role(m, e.get("participant")))
             for m in mechanics for e in m.get("effects") or [] if e.get("op") == "subtract"]
    found: set[str] = set()
    for mechanic, path, selector in needs:
        parts = str(path or "").split(".")
        if len(parts) != 3 or parts[0] != "components" or selector is None:
            continue
        # The move is possible while any holder it may use has or can get the good; a broad role (carry boxes from
        # anyone with stock) is not starved because most holders have none.
        candidates = [entity for entity in entities if fits(selector, entity)]
        starved = []
        for entity in candidates:
            start = ((entity.get("components") or {}).get(parts[1]) or {}).get(parts[2], 0)
            if (isinstance(start, (int, float)) and not isinstance(start, bool) and start <= 0
                    and not any(given == path and fits(sel, entity) for given, sel in givers)):
                starved.append(str(entity.get("id", "?")))
        if candidates and len(starved) == len(candidates):
            found.add(f"{mechanic.get('action_kind', '?')} needs {parts[2]} at {' or '.join(starved)}, which starts "
                      "with none and nothing ever gives it any")
    return sorted(found)


def _never_together(bundle: dict[str, Any], causal: dict[str, Any]) -> list[str]:
    """'kind needs a and b in one place: a in x, b in y' for each move that requires two roles to share a place no
    pair of their entities ever shares, in a world where no move or process changes where anything is.

    2026-10-27 pencil build (share czt5uoGw5t3L): buy-leads and buy-slats required the factory in Pennsylvania to be
    with the lead-maker in Sri Lanka and the sawmill in Oregon, and nothing moved anyone, so the factory waited from
    round 6 to round 17 and no pencil was made. The dry run listed both as never offered without saying why.
    """
    mechanics = causal.get("mechanics") or []
    moved = [e for m in [*mechanics, *(causal.get("processes") or [])] for e in m.get("effects") or []
             if e.get("path") == "location.location_id"]
    if moved:
        return []
    entities = bundle.get("entities") or []

    def fits(selector: Any, entity: dict[str, Any]) -> bool:
        selector = selector or {}
        return (set(selector.get("categories") or []) <= set(entity.get("categories") or [])
                and set(selector.get("components") or []) <= set(entity.get("components") or {}))

    def where(entity: dict[str, Any]) -> Any:
        # The engine puts a place with no location at itself (cafe1: the barista "is at the cafe").
        return entity.get("location") or (entity.get("id") if "place" in (entity.get("categories") or []) else None)

    found: set[str] = set()
    for mechanic in mechanics:
        roles = {"actor": mechanic.get("actor_selector"), **(mechanic.get("participants") or {})}
        for check in mechanic.get("checks") or []:
            sides = [(check.get(side) or {}).get("participant") or {} for side in ("left", "right")]
            if check.get("op") != "eq" or any(side.get("path") != "location.location_id" for side in sides):
                continue
            first, second = (side.get("name") for side in sides)
            if first not in roles or second not in roles or first == second:
                continue
            pairs = [(a, b) for a in entities if fits(roles[first], a) for b in entities
                     if fits(roles[second], b) and b is not a]
            if pairs and not any(where(a) == where(b) for a, b in pairs):
                a, b = pairs[0]
                found.add(f"{mechanic.get('action_kind', '?')} needs {first} and {second} in one place: "
                          f"{a.get('id', '?')} is in {where(a)}, {b.get('id', '?')} in {where(b)}")
    return sorted(found)


def _vanishing_moves(causal: dict[str, Any]) -> list[str]:
    """Action kinds that use up two or more different things and make or change nothing: what they use disappears.

    2026-10-26 pencil build (share 4VmgkXIVWn4p): pack-pencils took one pencil and one box and added nothing, though
    its rationale said it recorded a packed pencil, so every pencil the maker packed was gone and none ever reached
    the shop. Using up one thing alone (drinking a coffee) is ordinary consumption and is not named.
    """
    found: list[str] = []
    for mechanic in causal.get("mechanics") or []:
        effects = mechanic.get("effects") or []
        taken = {e.get("path") for e in effects if e.get("op") == "subtract"}
        if len(taken) >= 2 and not any(e.get("op") in ("add", "set") for e in effects):
            found.append(mechanic.get("action_kind", "?"))
    return sorted(found)


def _unanswered_demand(causal: dict[str, Any]) -> list[str]:
    """Fields a process adds to every round that no move ever lowers, so they only grow.

    2026-10-26 cafe build (share eFmPomcnsyQq): orders_waiting rose by one each round and serve-order never took
    one off, because its action named only the customer ("the waiting-order count ... unavailable as participants").
    """
    grows = {e.get("path") for p in causal.get("processes") or [] if p.get("timing") == "each_round"
             for e in p.get("effects") or [] if e.get("op") == "add"}
    lowered = {e.get("path") for m in causal.get("mechanics") or [] for e in m.get("effects") or []
               if e.get("op") in ("subtract", "set")}
    return sorted(path.rsplit(".", 1)[-1] for path in grows - lowered if path)


def _second_source_processes(causal: dict[str, Any]) -> list[str]:
    """'process adds field (already added from nothing by action)': a raw good with two sources.

    2026-10-21 c4-run20 (trace world-builder-live/world/5c2f3bc4490f4319b01f0f8983922265): mine-graphite added
    graphite from nothing and graphite-renews added it again to the same stock, so 29 piles sat unused at the
    mine. Recorded on the build result only: goods still flow, and the same shape appears in most saved pencil
    worlds, so it does not lower the score or ask for a rewrite.
    """
    def field(path: str) -> str:
        return path.split(".", 1)[1] if path.startswith("components.") else path

    gathered: dict[str, list[tuple[str, set[str]]]] = {}
    for mechanic in causal.get("mechanics") or []:
        roles = {**(mechanic.get("participants") or {}), "actor": mechanic.get("actor_selector") or {}}
        effects = mechanic.get("effects") or []
        if any(e.get("op") == "subtract" for e in effects):
            continue
        for effect in effects:
            if effect.get("op") == "add":
                categories = set((roles.get(effect.get("participant")) or {}).get("categories") or [])
                gathered.setdefault(field(effect["path"]), []).append((mechanic.get("action_kind", "?"), categories))
    found: list[str] = []
    for process in causal.get("processes") or []:
        reach = set((process.get("selector") or {}).get("categories") or [])
        for effect in process.get("effects") or []:
            if effect.get("op") != "add" or effect.get("participant") != "it":
                continue
            target = field(effect["path"])
            for kind, categories in gathered.get(target, []):
                if not reach or not categories or reach & categories:
                    found.append(f"{process.get('process_id', '?')} adds {target} (already added from nothing by {kind})")
                    break
    return found


def _moving_processes(causal: dict[str, Any]) -> list[str]:
    """'process moves field from it to participant' for each process that carries goods between entities.

    2026-10-20 c4-run16 (trace world-builder-live/world/cde24f8929724605bee600215b12e326): move-logs-to-sawmill and
    four more processes passed every good down the chain each round, so the carrier sat idle and deliver-pencils
    was never possible. Moving goods is an actor's work; a process may only change what it acts on.
    """
    def field(path: str) -> str:
        return path.split(".", 1)[1] if path.startswith("components.") else path

    found: list[str] = []
    for process in causal.get("processes") or []:
        effects = process.get("effects") or []
        taken = {field(e["path"]) for e in effects if e.get("op") == "subtract" and e.get("participant") == "it"}
        for effect in effects:
            target = field(effect["path"])
            if effect.get("op") == "add" and effect.get("participant") not in (None, "it") and target in taken:
                found.append(f"{process.get('process_id', '?')} moves {target} to {effect['participant']}")
                break
    return found


def _initial_refusals(bundle: dict[str, Any], causal: dict[str, Any], limit: int = 6) -> list[str]:
    """Distinct 'action: failed checks' lines for every actor in the starting state."""
    engine, model, _ = build_engine(bundle, causal)
    seen: list[str] = []
    try:
        actors = actor_ids(engine, model)
    except ValueError as error:
        # 2026-10-19 live pencil build (trace world-builder-live/world/3bac7221d2834482a14af883b9ff5e47): the dry run
        # failed with this same error, and raising it again here ended the build instead of guiding the next rewrite.
        return [f"{error}: each mechanic's actor_selector must name categories and components that some entity in "
                "the world actually has"]
    for actor in actors:
        for row in engine.discover(actor)["blocked"]:
            line = f"{row['action'].get('kind')}: {row.get('reason', '')}"
            if line not in seen:
                seen.append(line)
    return seen[:limit]


class WorldBuilderHandler(BaseHTTPRequestHandler):
    server_version = "WorldBuilderService/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("world-builder-api: " + (fmt % args) + "\n")

    def _progress(self, state: str, step: str, detail: str = "", items: list[str] | None = None) -> None:
        """Build steps are only visible to background jobs, which the page polls."""

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
        if path.startswith("/share/"):
            record = _load_share(path[len("/share/"):])
            if record is None:
                self._error(HTTPStatus.NOT_FOUND, "That shared run does not exist (check the link).")
                return
            self._json(HTTPStatus.OK, {"ok": True, **record})
            return
        if path.startswith("/jobs/"):
            job_id = path[len("/jobs/"):]
            with _JOBS_LOCK:
                job = _JOBS.get(job_id)
                snapshot = None if job is None else dict(job)
            if snapshot is None:
                self._error(HTTPStatus.NOT_FOUND, "unknown or expired job")
            elif snapshot["status"] == "running":
                self._json(HTTPStatus.OK, {
                    "ok": True, "status": "running", "job_id": job_id,
                    "elapsed_s": round(time.time() - snapshot["created"], 1),
                    "progress": [dict(step) for step in snapshot.get("progress", [])],
                })
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
        for name in ("_llm_budget", "_world_def", "_generate_people_world"):
            setattr(responder, name, getattr(WorldBuilderHandler, name).__get__(responder))
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
            except Exception as error:  # final job boundary
                print(f"world-builder-api: job {job_id} error: {type(error).__name__}: {str(error)[:300]}", flush=True)
                plain = _provider_failure(error)
                responder._error(*(plain or (HTTPStatus.INTERNAL_SERVER_ERROR, "internal world-builder error")))
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
            if path == "/share":
                self._share(client, body)
                return
            if path == "/readout":
                self._readout(client, body)
                return
            self._error(HTTPStatus.NOT_FOUND, "not found")
        except (BundleError, ActionDeclarationError, ValueError, TypeError) as error:
            self._error(HTTPStatus.UNPROCESSABLE_ENTITY, str(error)[:500])
        except Exception as error:  # final process boundary
            self.log_message("internal error: %s: %s", type(error).__name__, str(error)[:300])
            plain = _provider_failure(error)
            self._error(*(plain or (HTTPStatus.INTERNAL_SERVER_ERROR, "internal world-builder error")))

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

    def _dialogue_call(self, client: str, kind: str, call: Any, *, budget: float = DIALOGUE_BUDGET) -> None:
        """Run one budgeted dialogue-sized model call and return its payload."""
        trace_id = _new_trace_id(kind)
        cap = budget
        with _AI_SLOTS:
            budget = self._llm_budget(client, cap, dialogue=True)
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
        world_def = body.get("world_def") or "things"
        if world_def not in WORLD_DEFS:
            raise ValueError(f"world_def must be one of {list(WORLD_DEFS)}")
        if world_def == "auto":
            world_def = self._world_def(client, description)
            if world_def is None:
                return
        if world_def == "people":
            self._generate_people_world(client, description)
            return
        world_kind = body.get("world_kind") or "task"
        if world_kind not in WORLD_KINDS:
            raise ValueError(f"world_kind must be one of {list(WORLD_KINDS)}")
        if world_kind == "open":
            world_kind = "ongoing"  # older name for the same kind
        trace_id = _new_trace_id("world")
        with _AI_SLOTS:
            budget = self._llm_budget(client, WORLD_BUDGET)
            if budget is None:
                return
            try:
                self._progress("doing", "Reading your description")
                bundle, not_modeled, _ = generate_world_bundle(
                    description, model=model, trace_id=trace_id, max_budget=budget, world_kind=world_kind,
                )
                attempts: list[dict[str, Any]] = []
                # Keep the best attempt: reaching the finish line beats merely
                # allowing actions, which beats allowing nothing.
                best: tuple[tuple[int, int, int], dict[str, Any], CausalModel, dict[str, Any], dict[str, Any], list[str]] | None = None
                # An ongoing world whose best rules still leave a step impossible or an actor idle gets its structure
                # redesigned once from that evidence: rule rewrites cannot add a missing action or field (#187).
                structures = STRUCTURE_ATTEMPTS if world_kind != "task" else 1
                rules_per_structure = max(1, RULES_ATTEMPTS // structures)
                rules_attempt = 0
                out_of_budget = False
                redesign_feedback = ""

                def guidance_from_error(error: Exception) -> str:
                    return f"The rules for it could not be compiled: {type(error).__name__}: {error}"[:600]

                for structure_attempt in range(structures):
                    structure_feedback = ""
                    if structure_attempt:
                        self._progress("doing", "Redesigning what each one can do",
                                       "the test run showed steps that could never happen")
                        try:
                            bundle, not_modeled, _ = generate_world_bundle(
                                description, model=model, trace_id=trace_id, max_budget=budget, world_kind=world_kind,
                                feedback=redesign_feedback, previous=bundle,
                            )
                        except Exception as error:
                            # The first design's rules still stand; a failed redesign must not end the build.
                            if best is None or not (isinstance(error, ValueError)
                                                    or type(error).__name__ == "LLMBudgetExceededError"):
                                raise
                            self._progress("note", "Could not redesign it", "keeping the earlier rules")
                            break
                    entities = bundle.get("entities") or []
                    action_kinds = [a.get("kind") for a in bundle.get("actions") or [] if a.get("kind")]
                    self._progress(
                        "done", "Found what exists in your world",
                        f"{len(entities)} thing{'s' if len(entities) != 1 else ''}, "
                        f"{len(action_kinds)} kind{'s' if len(action_kinds) != 1 else ''} of action",
                        [e.get("label") or e.get("id") for e in entities],
                    )
                    if not_modeled:
                        self._progress("note", "Left out of the simulation", "", [str(x).rstrip(". ") for x in not_modeled])
                    guidance = ""
                    structure_best: tuple[tuple[int, int, int], str] | None = None
                    for try_index in range(rules_per_structure):
                        attempt = rules_attempt
                        rules_attempt += 1
                        last_try = try_index == rules_per_structure - 1
                        if try_index == 0:
                            self._progress("doing", "Writing the rules")
                        else:
                            self._progress("doing", _retry_label(model), "the last rules did not pass the test run")
                        try:
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
                            except Exception as error:
                                # Matched by name: llm_client is imported lazily, only where calls are made.
                                if type(error).__name__ != "LLMBudgetExceededError":
                                    raise
                                # A retry that runs out of this build's AI budget must not throw away
                                # an earlier attempt that works (2026-10-15: a pencil network lost its
                                # first rules this way and showed "internal world-builder error").
                                if best is None:
                                    raise ValueError(
                                        "This description needed more AI work than one build allows. "
                                        "Try a shorter or simpler description."
                                    ) from None
                                self._progress("note", "Out of AI budget for this build", "keeping the earlier rules")
                                out_of_budget = True
                                break
                            candidate = _strip_review(generated)
                            candidate_compiled = CausalModel.from_dict(candidate, bundle=bundle)
                        except (ActionDeclarationError, ValueError, TypeError, KeyError) as error:
                            # A rule set the compiler rejects is the cheapest failure to
                            # recover from: hand it to the stronger retry instead of
                            # ending the whole request.
                            attempts.append({"ok": False, "error": f"rules rejected by the compiler: {error}"[:300]})
                            self._progress("note", "Those rules did not fit together", str(error)[:160])
                            spent = _trace_cost(trace_id) >= budget - 0.01
                            if last_try or spent:
                                out_of_budget = out_of_budget or spent
                                if best is None and (spent or structure_attempt == structures - 1):
                                    raise
                                structure_feedback = structure_feedback or guidance_from_error(error)
                                break
                            guidance = (
                                "Your previous proposal was rejected by the local causal compiler: "
                                f"{type(error).__name__}: {error}. Return a corrected proposal."
                            )
                            continue
                        review = candidate_compiled.as_review()
                        self._progress(
                            "done",
                            f"Wrote {len(review['mechanics'])} rule{'s' if len(review['mechanics']) != 1 else ''}"
                            + (f" and {len(review['processes'])} thing{'s' if len(review['processes']) != 1 else ''} that happen by themselves"
                               if review.get("processes") else ""),
                            "with a finish line" if candidate_compiled.terminal is not None else "no finish line",
                            [_words(m["action_kind"]) for m in review["mechanics"]] + [_words(p["process_id"]) for p in review.get("processes") or []],
                        )
                        self._progress("doing", "Test-running the rules with simple moves")
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
                                summary = dry["summary"]
                                idle = sorted(set(summary.get("idle_actors") or []) | set(summary.get("stalled_actors") or []))
                                # Going in circles: one kind of move is all that still happens
                                # although the rules offer several.
                                circling = len(candidate_compiled.mechanics) >= 3 and len(summary.get("moves_at_end") or []) <= 1
                                # A declared move nobody was ever offered (#166, pencil: the wholesaler's only move).
                                never = summary.get("never_offered") or {}
                                # Best: alive with every actor still taking part, every move possible at some point and the
                                # work moving; then alive; then not.
                                conjuring_found = _conjuring_processes(candidate)
                                unsourced = _unsourced_inputs(bundle, candidate)
                                moving_found = _moving_processes(candidate)
                                # A move flips a thing's state but nothing ever follows from it at once (2026-10-26
                                # cafe build dI4j2qUYPBBZ: tip-stack set upright false and no knock-on was written).
                                # Advice on a retry and a tie-break only: watering a plant flips a field too, and
                                # nothing need follow from it, so this never fails an attempt by itself.
                                unfollowed = [] if _knock_on_processes(candidate) else _state_flips(candidate)
                                vanishing = _vanishing_moves(candidate)
                                missing_parts = _missing_components(bundle, candidate)
                                dead_ends = _dead_end_stock(bundle, candidate)
                                apart = _never_together(bundle, candidate)
                                starved = _starved_holders(bundle, candidate)
                                unanswered = _unanswered_demand(candidate)
                                score = (3 if not idle and not circling and not never and not conjuring_found
                                         and not moving_found and not vanishing and not unanswered and not dead_ends and not apart and not starved else 2) if alive else 1
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
                                if circling:
                                    guidance += (
                                        f" By the end of the {dry_turns}-round test the only move still happening was "
                                        f"{', '.join(summary.get('moves_at_end') or ['nothing'])}: the work stopped progressing. "
                                        "Make sure everything that can be taken or held can also be released or used up "
                                        "(for example a rule to put a shared tool back), and that each step's output is "
                                        "what the next step's checks need."
                                    )
                                if never:
                                    guidance += (
                                        f" In the {dry_turns}-round test these moves were never possible for anyone: "
                                        + "; ".join(f"{kind} ({why or 'nothing it applies to ever existed, or no actor ever held what it needs'})"
                                                    for kind, why in never.items())
                                        + ". For each, make sure some other action produces what its checks need (for "
                                        "example, if goods must be at the next stop before they can move on, give someone an "
                                        "action that brings them there)."
                                    )
                                if conjuring_found:
                                    guidance += (
                                        " These processes create goods that an action is meant to make, so nothing has "
                                        "to flow through the chain: " + "; ".join(conjuring_found) + ". Remove those effects; "
                                        "processes may only renew raw materials at their source and bring new demand."
                                    )
                                if unsourced:
                                    guidance += (
                                        " Nothing in the world ever makes or brings in these, and everyone starts with "
                                        "none, so every step that uses them is impossible: " + ", ".join(unsourced) + ". "
                                        "Give each one a source: an actor whose action makes or supplies it, or a "
                                        "process that renews it at the place it comes from."
                                    )
                                result_row["unsourced_inputs"] = unsourced
                                result_row["stalled_actors"] = summary.get("stalled_actors") or []
                                result_row["never_offered"] = sorted(never)
                                result_row["circling"] = circling
                                if moving_found:
                                    guidance += (
                                        " These processes carry goods from one place to another by themselves, so the "
                                        "people meant to move them have nothing to do: " + "; ".join(moving_found) + ". "
                                        "Remove those effects and let an actor's action do the moving."
                                    )
                                if unfollowed:
                                    guidance += (
                                        " These moves flip a thing's state, but no process has timing immediately, so "
                                        "nothing ever follows from them: " + ", ".join(unfollowed) + ". Write what follows "
                                        "at once wherever the represented state can hold it (a full container that tips "
                                        "spills; a spill wets what it rests on; a fragile thing that falls breaks), each as "
                                        "a process with timing immediately. If nothing physically follows, leave it."
                                    )
                                if vanishing:
                                    guidance += (
                                        " These moves use up several things and make nothing, so what they use simply "
                                        "disappears: " + ", ".join(vanishing) + ". If the move turns them into something "
                                        "(a packed box, a meal, a finished part), add one to the field that holds what it "
                                        "makes, and let the next step's checks use that field."
                                    )
                                if unanswered:
                                    guidance += (
                                        " These grow every round and no move ever lowers them: " + ", ".join(unanswered)
                                        + ". Let the move that answers them (serving an order, treating a patient) take "
                                        "one off; if that move cannot reach the thing that holds them, it needs a participant "
                                        "naming it."
                                    )
                                if missing_parts:
                                    guidance += (
                                        " These moves require something no entity in the world has, so they can never "
                                        "happen: " + "; ".join(missing_parts) + ". Use components the entities have, or "
                                        "give the entities that component."
                                    )
                                if dead_ends:
                                    guidance += (
                                        " These goods are made or supplied but no move ever takes them from where they "
                                        "pile up, so the step that needs them never gets them: " + "; ".join(dead_ends)
                                        + ". Give someone a move that carries each one to the place that uses it."
                                    )
                                if apart:
                                    guidance += (
                                        " These moves require two parties to be in one place, but they are always "
                                        "apart and nothing moves anyone, so the moves can never happen: "
                                        + "; ".join(apart) + ". A trade between places is an order sent from afar: drop "
                                        "the same-place check, and let the goods arrive by a delivery that counts down "
                                        "rounds."
                                    )
                                if starved:
                                    guidance += (
                                        " These moves use up a good where it never arrives, so they can never happen: "
                                        + "; ".join(starved) + ". Give the holder a source: the step that makes or carries "
                                        "the good must add it there (a delivery that counts down must add the goods to "
                                        "the receiver when it ends)."
                                    )
                                result_row["starved_holders"] = starved
                                result_row["dead_end_stock"] = dead_ends
                                result_row["never_together"] = apart
                                result_row["missing_components"] = missing_parts
                                result_row["vanishing_moves"] = vanishing
                                result_row["unanswered_demand"] = unanswered
                                result_row["unfollowed_moves"] = unfollowed
                                result_row["conjuring_processes"] = conjuring_found
                                result_row["moving_processes"] = moving_found
                                result_row["second_source_processes"] = _second_source_processes(candidate)
                                result_row["knock_on_processes"] = _knock_on_processes(candidate)
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
                                "checks were false: " + "; ".join(refusals) + ". Correct checks that "
                                "contradict the initial state by mistake (see initial_builtin_state and entity "
                                "component values) so at least one actor can act, keeping effects consistent with "
                                "the action descriptions. Keep a check that stops what the description says cannot "
                                "happen (a closed wall cannot be walked through); people may still try it, and the "
                                "check is what refuses them. Make sure the ordinary things the description lets "
                                "people do have actions someone can take from the start."
                            )
                        # Why an attempt was kept must be readable from the build record: pencil czt5uoGw5t3L kept
                        # attempt 4 over attempt 3, whose test run assembled pencils, and nothing recorded either score.
                        result_row["score"] = score
                        result_row["processes"] = len(candidate_compiled.processes)
                        attempts.append(result_row)
                        self._progress("done", "Test run: " + _dry_run_sentence(result_row, world_kind))
                        rank = _attempt_rank(score, result_row)
                        if best is None or rank > best[0]:
                            best = (rank, candidate, candidate_compiled, result_row, bundle, not_modeled)
                        if structure_best is None or rank > structure_best[0]:
                            structure_best = (rank, guidance)
                        out_of_budget = out_of_budget or _trace_cost(trace_id) >= budget - 0.01
                        if score >= (2 if world_kind == "task" else 3) or last_try or out_of_budget:
                            break
                    if structure_best is not None:
                        structure_feedback = structure_best[1]
                    if best is not None and best[0][0] >= (2 if world_kind == "task" else 3):
                        break
                    if out_of_budget or not structure_feedback:
                        break
                    redesign_feedback = structure_feedback
                assert best is not None
                _, causal, compiled, best_row, bundle, not_modeled = best
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

    def _world_def(self, client: str, description: str) -> str | None:
        """People or things? One small call, charged like any other; None means an error was already sent."""
        trace_id = _new_trace_id("kind")
        with _AI_SLOTS:
            budget = self._llm_budget(client, WORLD_KIND_BUDGET)
            if budget is None:
                return None
            self._progress("doing", "Deciding whether this is a world of people or of things")
            try:
                people, why = about_people(description, trace_id=trace_id, max_budget=budget)
            except Exception:
                _settle_failed_call(budget, trace_id)
                raise
            _settle_daily_budget(budget, _trace_cost(trace_id))
        self._progress("done", "A world of people, each with their own goals" if people else "A world of things and steps", why)
        return "people" if people else "things"

    def _generate_people_world(self, client: str, description: str) -> None:
        """Description -> people with goals, beliefs and information -> exact rules (scripts/people_world.py).

        Always an ongoing world. AI members choose the moves, each reading their own brief; a scripted dry run
        checks that someone can act from the starting state.
        """
        trace_id = _new_trace_id("people")
        started = time.monotonic()
        with _AI_SLOTS:
            budget = self._llm_budget(client, PEOPLE_WORLD_BUDGET)
            if budget is None:
                return
            try:
                try:
                    prepared = prepare_people_world(description, trace_id=trace_id, max_budget=budget,
                                                    progress=self._progress)
                except Exception as error:
                    if type(error).__name__ == "LLMBudgetExceededError":  # llm_client is imported lazily
                        raise ValueError(_budget_message(error)) from None
                    raise
                guidance, attempts = "", []
                best: tuple[int, dict[str, Any], dict[str, Any]] | None = None
                for attempt in range(2):
                    try:
                        built = write_people_rules(prepared, trace_id=trace_id, max_budget=budget,
                                                   progress=self._progress, guidance=guidance)
                    except Exception as error:
                        if type(error).__name__ == "LLMBudgetExceededError":  # llm_client is imported lazily
                            if best is not None:
                                self._progress("note", "Out of AI budget for this build", "keeping the earlier rules")
                                break
                            raise ValueError(_budget_message(error)) from None
                        if "response truncated" in str(error):
                            # The rules ran past the answer-length cap (inc15b): ask once for fewer, broader rules,
                            # and if that fails too, say so plainly instead of "internal error".
                            attempts.append({"ok": False, "error": "the rules were too long and were cut off"})
                            self._progress("note", "The rules came out too long and were cut off", "asking for fewer, broader rules")
                            if attempt == 1 or _trace_cost(trace_id) >= budget - 0.05:
                                if best is not None:
                                    break
                                raise ValueError("The AI's rules for this description came out too long and were cut "
                                                 "off. Try a shorter description, or press Create simulation again.") from None
                            guidance = (" Your previous answer was too long and was cut off. Write fewer rules: one "
                                        "rule may serve several people through its actor selector, and keep each "
                                        "rationale and limit to one short sentence.")
                            continue
                        if not isinstance(error, (ActionDeclarationError, BundleError, ValueError, TypeError, KeyError)):
                            raise
                        attempts.append({"ok": False, "error": f"rules rejected by the compiler: {error}"[:300]})
                        self._progress("note", "Those rules did not fit together", str(error)[:160])
                        if attempt == 1 or _trace_cost(trace_id) >= budget - 0.05:
                            if best is not None:
                                break
                            raise
                        guidance = (
                            "Your previous proposal was rejected by the local causal compiler: "
                            f"{type(error).__name__}: {error}. Return a corrected proposal."
                        )
                        continue
                    review = CausalModel.from_dict(built["causal_model"], bundle=built["bundle"]).as_review()
                    self._progress(
                        "done", f"Wrote {len(review['mechanics'])} rules and {len(review.get('processes') or [])} things "
                        "that happen by themselves", "",
                        [_words(m["action_kind"]) for m in review["mechanics"]] + [_words(p["process_id"]) for p in review.get("processes") or []],
                    )
                    self._progress("doing", "Test-running the rules with simple moves")
                    try:
                        # Past the rewrite cut-off the test can no longer change the rules, only report on
                        # them, so a short test is enough (the 24-round one took 16 s on the server).
                        dry_turns = (DRY_RUN_TURNS_CONTINUING if time.monotonic() - started <= PEOPLE_REWRITE_BY_S
                                     else DRY_RUN_TURNS_LATE)
                        dry, _, _ = run_world(built["bundle"], built["causal_model"], policy="scripted",
                                              max_turns=dry_turns, trace_id=f"{trace_id}/dry-run-{attempt}")
                        summary = dry["summary"]
                        dry_row = {"ok": True, **summary}
                        # Going in circles: one kind of move is all that still happens although the rules offer
                        # several (2026-10-15 Waltzman: everyone raised the same concern from round 4 on).
                        circling = len(review["mechanics"]) >= 3 and len(summary.get("moves_at_end") or []) <= 1
                        stalled = summary.get("stalled_actors") or []
                        if _decision_settled(dry.get("final_snapshot")):
                            # 2026-10-16 Waltzman deploy1: once the decision was deployed the countries had nothing
                            # left to decide and went quiet in the test's last third; that is the story ending, not
                            # people stuck, and the 64 s rewrite it triggered pushed the build past 150 s.
                            stalled = []
                        idle = sorted(set(summary.get("idle_actors") or []) | set(stalled))
                        dry_row.update(circling=circling, stalled_actors=stalled)
                        score = 1 + (not circling) + (not idle) + bool(summary.get("active_at_end"))
                        guidance = ""
                        if circling:
                            guidance += (
                                f" A {dry_turns}-round test of your previous rules ended with only "
                                f"{', '.join(summary.get('moves_at_end') or ['nothing'])} still happening: people "
                                "repeated one action and nothing else could happen. Add the missing reverse rules and "
                                "limits so the decision can still move."
                            )
                        if idle:
                            guidance += _idle_guidance(dry, idle, dry_turns)
                    except ValueError as error:
                        dry_row, score = {"ok": False, "error": str(error)[:300]}, 0
                        guidance = (
                            f"A test run of your previous rules failed from the starting state: {error}. Make sure "
                            "people can act from the starting state."
                        )
                    # Tasks that take several rounds (#128): a start must not refuse up front on what its own task
                    # uses up; that outcome plays out over rounds. A finding goes into the one rules retry.
                    tasks = long_tasks(built["causal_model"], built["bundle"])
                    dry_row["long_tasks"] = [{"action": t["action"], "started_by": t["started_by"],
                                              "can_fail_part_way": t["can_fail_part_way"]} for t in tasks]
                    # A world where every task people start can only finish (#128 slice 2, E1): the finding goes
                    # into the rules retry, and the build record says so if it is kept anyway.
                    part_way = part_way_findings(built["causal_model"])
                    if part_way:
                        dry_row["part_way_findings"] = [g["finding"] for g in part_way]
                        score -= 1
                        guidance += " " + " ".join(g["finding"] for g in part_way)
                    gates = attempt_findings(built["bundle"], built["causal_model"])
                    if gates:
                        dry_row["attempt_findings"] = [g["finding"] for g in gates]
                        score -= 1
                        guidance += " " + " ".join(g["finding"] for g in gates)
                    dry_row["knock_on_processes"] = _knock_on_processes(built["causal_model"])
                    attempts.append(dry_row)
                    sentence = _dry_run_sentence(dry_row, "ongoing")
                    if dry_row.get("circling"):
                        sentence += "; went in circles"
                    self._progress("done", "Test run: " + sentence)
                    if best is None or score > best[0]:
                        best = (score, built, dry_row)
                    if score >= 4 or attempt == 1 or _trace_cost(trace_id) >= budget - 0.15:
                        break
                    if time.monotonic() - started > PEOPLE_REWRITE_BY_S:
                        self._progress("note", "Kept these rules", "a rewrite would make the wait too long")
                        break
                    self._progress("doing", "Rewriting the rules so the world keeps moving",
                                   "the test run went in circles" if dry_row.get("circling")
                                   else "some people could not act" if dry_row.get("stalled_actors") or dry_row.get("idle_actors")
                                   else "a move refused up front on what its own task uses up" if dry_row.get("attempt_findings")
                                   else "the test run went quiet")
                assert best is not None
                _, built, dry_row = best
                bundle, causal = built["bundle"], built["causal_model"]
                review = CausalModel.from_dict(causal, bundle=bundle).as_review()
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_failed_call(budget, trace_id)
                try:
                    charged = _trace_cost(trace_id)
                except Exception:
                    charged = 0.0  # the late copies are then charged in full
                _settle_late_hedges(trace_id, charged)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
            _settle_late_hedges(trace_id, trace_cost)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "description": description,
                "world_def": "people",
                "world_kind": "ongoing",
                "not_modeled": built["not_modeled"],
                "bundle": bundle,
                "causal_model": causal,
                "review": review,
                "briefs": built["briefs"],
                "people": built["people"],
                "coverage": built["coverage"],
                "dropped_generated_rules": built["dropped_generated_rules"],
                "dry_run": dry_row,
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
        trace_id = _new_trace_id("draft")
        with _AI_SLOTS:
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
        trace_id = _new_trace_id("mechanics")
        guidance = body.get("guidance") or ""
        if not isinstance(guidance, str):
            raise ValueError("guidance must be a string")
        # Serialize public LLM calls so two concurrent requests cannot both see
        # the same remaining daily budget and oversubscribe it.
        with _AI_SLOTS:
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
        trace_id = _new_trace_id("comparison")
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
                "approval": _approval_record(bundle=comparison_bundle, causal=causal, trace=trace),
                "trace_id": trace_id,
            },
        )

    @staticmethod
    def _run_ids(body: dict[str, Any]) -> tuple[list[str], str | None]:
        runs = body.get("run_trace_ids")
        build = body.get("build_trace_id")
        if (not isinstance(runs, list) or not 0 < len(runs) <= MAX_SHARED_RUNS or len(set(runs)) != len(runs)
                or not all(isinstance(t, str) and _TRACE_PATTERN.fullmatch(t) for t in runs)):
            raise ValueError(f"run_trace_ids must list 1 to {MAX_SHARED_RUNS} distinct run ids from this service")
        if build is not None and not (isinstance(build, str) and _TRACE_PATTERN.fullmatch(build)):
            raise ValueError("build_trace_id must be a build id from this service")
        return runs, build

    def _readout(self, client: str, body: dict[str, Any]) -> None:
        """The "What happened" readout of a finished run, read from this server's own run log (one light AI call)."""
        runs, build = self._run_ids(body)
        record = _assemble_share(build, runs)
        from scripts.run_readout import read_run
        model = _requested_model(body)

        def call(trace_id: str, budget: float) -> tuple[dict[str, Any], Any]:
            people = record["world"].get("people")
            # #190: a things world has no people to coordinate, so it is read for how goods flowed.
            readout, result = read_run(record["rounds"], people=people, model=model, trace_id=trace_id,
                                       max_budget=budget, lens_id="coordination" if people else "flow")
            return {"readout": readout}, result

        self._dialogue_call(client, "readout", call, budget=READOUT_BUDGET)

    def _share(self, client: str, body: dict[str, Any]) -> None:
        """Save a finished run for a link. No AI call: the rounds come from this server's own run log."""
        runs, build = self._run_ids(body)
        readout_id = body.get("readout_trace_id")
        if readout_id is not None and not (isinstance(readout_id, str) and _TRACE_PATTERN.fullmatch(readout_id)):
            raise ValueError("readout_trace_id must be a readout id from this service")
        record = _assemble_share(build, runs)
        if readout_id:
            # The readout travels with the link only when this server made it for exactly these rounds.
            logged = _logged_entries({readout_id}).get(readout_id)
            if (logged and logged["path"] == "/readout"
                    and logged["request"].get("run_trace_ids") == runs and logged.get("client") == _fingerprint(client)):
                record["readout"] = (logged.get("result") or {}).get("readout")
                record["readout_trace_id"] = readout_id
        share_id = _save_share(_fingerprint(client), record)
        if share_id is None:
            self._error(HTTPStatus.TOO_MANY_REQUESTS, "You have shared a lot of runs today; try again tomorrow.")
            return
        self._json(HTTPStatus.OK, {"ok": True, "share_id": share_id, "rounds": len(record["rounds"])})

    def _run(self, client: str, body: dict[str, Any]) -> None:
        if body.get("approved") is not True:
            self._error(HTTPStatus.CONFLICT, "mechanics must be explicitly approved before a run")
            return
        bundle = validate_bundle(body.get("bundle"))
        causal = body.get("causal_model")
        if not isinstance(causal, dict):
            raise ValueError("causal_model must be an object")
        # Compile before any policy/model call. This is the install authority gate.
        try:
            CausalModel.from_dict(causal, bundle=bundle)
        except ActionDeclarationError as error:
            # 2026-10-16: a rejected rule reached the page as the gate's raw "unsupported or unknown state path: ...".
            raise ValueError(f"These rules were refused before anything ran, so nothing changed: one rule does not "
                             f"fit this world (the rule check said: {str(error)[:200]}). Build the world again "
                             f"or start from an example.") from None
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
        if continue_from is not None:
            seal = body.get("continue_seal")
            if not isinstance(seal, str) or not hmac.compare_digest(
                    seal.encode(), _snapshot_seal(continue_from, body.get("bundle"), causal,
                                                  body.get("approval")).encode()):
                raise ValueError("This world cannot carry on: the state sent back does not match the last round "
                                 "this server ran under these rules. Press Start over.")
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
        # People worlds: each person's brief from their own profile, read by the AI choosing that person's moves.
        briefs = body.get("briefs") or {}
        if (
            not isinstance(briefs, dict) or len(briefs) > 24
            or not all(isinstance(k, str) and 0 < len(k) <= 80 and isinstance(v, str) and len(v) <= MAX_BRIEF_CHARS
                       for k, v in briefs.items())
        ):
            raise ValueError(f"briefs must map up to 24 actor ids to text of at most {MAX_BRIEF_CHARS} characters")
        # Concordia residents' memories from the previous round (trace.resident_memory), so each person remembers.
        resident_memory = body.get("resident_memory") or {}
        if (
            not isinstance(resident_memory, dict) or len(resident_memory) > 24
            or not all(isinstance(k, str) and 0 < len(k) <= 80 and isinstance(v, list) and len(v) <= MEMORY_ITEMS
                       and all(isinstance(x, str) and len(x) <= MEMORY_ITEM_CHARS for x in v)
                       for k, v in resident_memory.items())
        ):
            raise ValueError(f"resident_memory must map up to 24 actor ids to up to {MEMORY_ITEMS} notes of at most "
                             f"{MEMORY_ITEM_CHARS} characters")
        # Tasks still under way from the previous round (trace.underway, #128). They are only records of who
        # started what; run_world keeps one only while the sealed world state still shows it under way.
        underway = body.get("underway") if continue_from is not None else None
        model = _requested_model(body)
        trace_id = _new_trace_id("run")
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
        elif policy in {"llm", "resident"}:
            with _AI_SLOTS:
                budget = self._llm_budget(client, RUN_BUDGET, ai_run=True)
                if budget is None:
                    return
                try:
                    trace, _, compiled = run_world(
                        bundle, causal, policy=policy, model_name=model,
                        max_turns=turns, max_budget=budget, trace_id=trace_id,
                        start_snapshot=continue_from, turn_offset=turn_offset, prior_recent=recent,
                        briefs=briefs, resident_memory=resident_memory, underway=underway,
                        # Residents say what they try in their own words (docs/plans/open_attempt.md).
                        open_attempts=policy == "resident",
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
                start_snapshot=continue_from, turn_offset=turn_offset, prior_recent=recent, underway=underway,
            )
            daily_cost = None
        if execution_mode == "authored_world":
            replay = render_run(bundle, trace, compiled)
        # Issue #122 (G6): who approved which frozen rules, when. Made on the first round;
        # continued rounds carry it back under the seal checked above.
        approval = body.get("approval") if continue_from is not None else _approval_record(bundle=body.get("bundle"),
                                                                                           causal=causal, trace=trace)
        # Every engine event in full goes to the run log only; the page never reads them (#123, G1).
        engine_events = trace.pop("engine_events", None)
        request = _REQUEST.get()
        if request is not None and engine_events is not None:
            request["engine_events"] = engine_events
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "summary": trace["summary"],
                "trace": trace,
                "causal_review": compiled.as_review(),
                "replay_html": replay,
                # The next continued round must send this back with final_snapshot (#127).
                "snapshot_seal": _snapshot_seal(trace.get("final_snapshot"), body.get("bundle"), causal, approval),
                "approval": approval,
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
