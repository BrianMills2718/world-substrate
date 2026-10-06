#!/usr/bin/env python3
"""Measure natural-language world building against a running World Builder API.

Builds each description (for each requested world kind) through /generate-world
as a background job and reports, per build, whether its rules let anything
happen, whether a task world reaches its finish line, and whether an ongoing or
open world is still active at the end of the quick test. Spends real model
money: about $0.005-0.08 per build.

    uv run --no-project --python 3.12 python scripts/measure_world_builder.py \
        --base http://127.0.0.1:8899 --kinds task,ongoing,open

Prints one line per build and a RESULT line with counts; exits 1 if any build
request failed outright (HTTP error), 0 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

DESCRIPTIONS = [
    "One delivery driver has one van and must deliver three packages to two houses before the van runs out of fuel.",
    "Two gardeners share one watering can and must water four plants before noon.",
    "Two cooks share one knife and must finish three salad orders before closing.",
    "A librarian lends three books to two students; a student can only borrow a book that is on the shelf.",
    "A small bakery: the baker turns flour into dough, bakes dough into bread, and a customer buys bread until four loaves are sold.",
    "Three firefighters share one hose and must put out two small fires; the hose must be connected to the hydrant first.",
]
# Cloudflare rejects urllib's default user agent; the live site needs a browser-like one.
HEADERS = {"Content-Type": "application/json", "Origin": "https://brianmills.dev",
           "User-Agent": "Mozilla/5.0 world-builder-measurement"}
# Measurement spends from the owner allowance, never the shared visitor budget.
if os.environ.get("WORLD_BUILDER_OWNER_PASSWORD"):
    HEADERS["X-World-Builder-Owner"] = os.environ["WORLD_BUILDER_OWNER_PASSWORD"]


def _request(url: str, body: dict | None = None) -> tuple[int, dict]:
    req = urllib.request.Request(url, data=None if body is None else json.dumps(body).encode(),
                                 headers=HEADERS, method="GET" if body is None else "POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        raw = error.read()
        return error.code, json.loads(raw) if raw[:1] == b"{" else {"error": raw[:200].decode(errors="ignore")}


def build(base: str, description: str, kind: str) -> tuple[int, dict, float]:
    started = time.time()
    status, payload = _request(f"{base}/world-builder/api/generate-world",
                               {"description": description, "world_kind": kind, "async": True})
    if status == 202:
        job = payload["job_id"]
        while True:
            time.sleep(2)
            status, payload = _request(f"{base}/world-builder/api/jobs/{job}")
            if payload.get("status") != "running":
                break
    return status, payload, time.time() - started


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="http://127.0.0.1:8899")
    parser.add_argument("--kinds", default="task")
    parser.add_argument("--limit", type=int, default=len(DESCRIPTIONS))
    parser.add_argument("--save", help="write every response to this JSON file")
    args = parser.parse_args()
    kinds = [k.strip() for k in args.kinds.split(",") if k.strip()]
    rows, failures, saved = [], 0, []
    for kind in kinds:
        for i, description in enumerate(DESCRIPTIONS[: args.limit]):
            status, payload, seconds = build(args.base, description, kind)
            saved.append({"kind": kind, "description": description, "status": status, "payload": payload})
            if status != 200:
                failures += 1
                print(f"{kind:8} {i} HTTP {status} {seconds:5.0f}s {str(payload.get('error'))[:150]}", flush=True)
                continue
            dry = payload["dry_run"]
            ok_kind = dry.get("terminal_reached") if kind == "task" else dry.get("active_at_end")
            rows.append((kind, bool(dry["ok"]), bool(dry["ok"] and ok_kind)))
            print(f"{kind:8} {i} HTTP 200 {seconds:5.0f}s ${payload['cost_usd']:.4f} {payload['bundle']['world']['id']:22} "
                  f"runnable={dry['ok']} {'finished' if kind == 'task' else 'active_at_end'}={ok_kind} "
                  f"attempts={[a['ok'] for a in payload['dry_run_attempts']]}", flush=True)
    if args.save:
        with open(args.save, "w") as handle:
            json.dump(saved, handle, indent=1)
    for kind in kinds:
        mine = [r for r in rows if r[0] == kind]
        print(f"RESULT kind={kind} builds={len(mine)} runnable={sum(r[1] for r in mine)} "
              f"{'finished' if kind == 'task' else 'active_at_end'}={sum(r[2] for r in mine)}")
    print(f"RESULT http_failures={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
