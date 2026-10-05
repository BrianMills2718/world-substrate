#!/usr/bin/env python3
"""Small same-origin API for World Builder mechanics generation and fresh runs."""
from __future__ import annotations

import argparse
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
from scripts.native_coordination_authoring import (
    DEFAULT_CAUSAL as NATIVE_COORDINATION_CAUSAL,
    generate_native_coordination_draft,
)
from scripts.native_coordination_comparison import with_approval_threshold
from scripts.run_authored_world import render_run, run_world
from scripts.run_native_coordination import run_native_coordination
from scripts.scaffold_world import BundleError, validate_bundle
from world_substrate.action_authoring import ActionDeclarationError, CausalModel

API_PREFIX = "/world-builder/api"
MAX_BODY_BYTES = 512_000
DRAFT_BUDGET = 0.08
MECHANICS_BUDGET = 0.12
RUN_BUDGET = 0.12
DAILY_LLM_BUDGET = 0.50
# Description -> structure -> mechanics (+ at most one dry-run-guided mechanics retry).
WORLD_BUDGET = 0.20
DRY_RUN_TURNS = 12
LLM_REQUESTS_PER_HOUR = 8
GENERAL_REQUESTS_PER_MINUTE = 30
ALLOWED_ORIGINS = {"https://brianmills.dev", "https://www.brianmills.dev"}
TRACE_ROOT = "world-builder-live"
BUDGET_STATE_PATH = Path.home() / ".local/state/world-builder/llm-budget-v1.json"
BUDGET_STATE_SCHEMA = "world-builder-llm-budget/v1"

_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
_LLM_REQUESTS: dict[str, deque[float]] = defaultdict(deque)
_LLM_LOCK = threading.Lock()


def _prune(queue: deque[float], window: float) -> None:
    cutoff = time.time() - window
    while queue and queue[0] < cutoff:
        queue.popleft()


def _rate_ok(client: str, *, llm: bool) -> bool:
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
    if not BUDGET_STATE_PATH.exists():
        return _empty_budget_state()
    try:
        value = json.loads(BUDGET_STATE_PATH.read_text())
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
    BUDGET_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp = BUDGET_STATE_PATH.with_name(BUDGET_STATE_PATH.name + ".tmp")
    temp.write_text(json.dumps(state, sort_keys=True, separators=(",", ":")) + "\n")
    temp.replace(BUDGET_STATE_PATH)


def _daily_cost() -> float:
    state = _load_budget_state()
    return float(state["spent_usd"] + state["reserved_usd"])


def _reserve_daily_budget(requested_cap: float) -> float | None:
    state = _load_budget_state()
    committed = float(state["spent_usd"] + state["reserved_usd"])
    remaining = max(0.0, DAILY_LLM_BUDGET - committed)
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


class WorldBuilderHandler(BaseHTTPRequestHandler):
    server_version = "WorldBuilderService/0.1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write("world-builder-api: " + (fmt % args) + "\n")

    def _json(self, status: int, value: dict[str, Any]) -> None:
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

    def do_GET(self) -> None:
        if self._path() == "/health":
            self._json(
                HTTPStatus.OK,
                {
                    "ok": True,
                    "service": "world-builder",
                    "build_commit": os.environ.get("WORLD_SUBSTRATE_BUILD_COMMIT"),
                    "llm_daily_budget_usd": DAILY_LLM_BUDGET,
                    "llm_daily_committed_usd": _daily_cost(),
                },
            )
            return
        self._error(HTTPStatus.NOT_FOUND, "not found")

    def do_POST(self) -> None:
        client = _client_ip(self)
        if not _origin_allowed(self):
            self._error(HTTPStatus.FORBIDDEN, "same-origin browser request required")
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
        try:
            if path == "/generate-draft":
                self._generate_draft(client, body)
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

    def _llm_budget(self, client: str, requested_cap: float) -> float | None:
        if not _rate_ok(client, llm=True):
            self._error(HTTPStatus.TOO_MANY_REQUESTS, "LLM rate limit reached")
            return None
        cap = _reserve_daily_budget(requested_cap)
        if cap is None:
            spent = _daily_cost()
            self._error(
                HTTPStatus.TOO_MANY_REQUESTS,
                f"daily World Builder LLM budget reached (${spent:.3f}/${DAILY_LLM_BUDGET:.2f})",
            )
            return None
        return cap

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
        model = str(body.get("model") or DEFAULT_MODEL)
        trace_id = f"{TRACE_ROOT}/world/{uuid.uuid4().hex}"
        with _LLM_LOCK:
            budget = self._llm_budget(client, WORLD_BUDGET)
            if budget is None:
                return
            try:
                bundle, not_modeled, _ = generate_world_bundle(
                    description, model=model, trace_id=trace_id, max_budget=budget,
                )
                guidance = ""
                attempts: list[dict[str, Any]] = []
                for attempt in range(2):
                    generated, _ = generate_causal_model(
                        bundle, model=model, trace_id=trace_id, max_budget=budget, guidance=guidance,
                    )
                    causal = _strip_review(generated)
                    compiled = CausalModel.from_dict(causal, bundle=bundle)
                    try:
                        dry, _, _ = run_world(
                            bundle, causal, policy="scripted", max_turns=DRY_RUN_TURNS,
                            trace_id=f"{trace_id}/dry-run-{attempt}",
                        )
                        attempts.append({"ok": True, **dry["summary"]})
                        break
                    except ValueError as error:
                        attempts.append({"ok": False, "error": str(error)[:300]})
                        if attempt == 1 or _trace_cost(trace_id) >= budget - 0.01:
                            break
                        guidance = (
                            "A deterministic dry run of your previous mechanics from the initial state "
                            f"failed: {error}. Make every action's checks satisfiable from the represented "
                            "initial state for at least one actor, and keep effects consistent with the "
                            "action descriptions."
                        )
                trace_cost = _trace_cost(trace_id)
            except Exception:
                _settle_daily_budget(budget, None)
                raise
            daily_cost = _settle_daily_budget(budget, trace_cost)
        self._json(
            HTTPStatus.OK,
            {
                "ok": True,
                "description": description,
                "not_modeled": not_modeled,
                "bundle": bundle,
                "causal_model": causal,
                "review": compiled.as_review(),
                "dry_run": attempts[-1],
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
        model = str(body.get("model") or DEFAULT_MODEL)
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
                _settle_daily_budget(budget, None)
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
        model = str(body.get("model") or DEFAULT_MODEL)
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
                _settle_daily_budget(budget, None)
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
        model = str(body.get("model") or DEFAULT_MODEL)
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
                budget = self._llm_budget(client, RUN_BUDGET)
                if budget is None:
                    return
                try:
                    trace, _, compiled = run_world(
                        bundle, causal, policy=policy, model_name=model,
                        max_turns=turns, max_budget=budget, trace_id=trace_id,
                    )
                    trace_cost = _trace_cost(trace_id)
                except Exception:
                    _settle_daily_budget(budget, None)
                    raise
                daily_cost = _settle_daily_budget(budget, trace_cost)
                trace["cost_usd"] = trace_cost
        else:
            trace, _, compiled = run_world(
                bundle, causal, policy=policy, model_name=model,
                max_turns=turns, max_budget=RUN_BUDGET, trace_id=trace_id,
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
