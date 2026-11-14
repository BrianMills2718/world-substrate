#!/usr/bin/env python3
"""Open the owner's map view of a saved run: fetch its run-log rows, export them with the world's own layout, serve the viewer.

Implements: scene-viewer/owner-run-viewer
Brian, 2026-11-14: "i approve c then b then a" (A). The viewer uses Smallville's art, which is for private use only, so it
is never served from the public site or the VPS: this command runs on the owner's machine, reads the run from the service
with the owner password (env WORLD_BUILDER_OWNER_PASSWORD, never printed) or from a run-log file, and serves
`viewer/smallville/` on localhost. Needs `scripts/setup_smallville_viewer.py` done once, and the Smallville clone's map data.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.export_smallville_replay import export_from_rows  # noqa: E402

SERVICE = "https://brianmills.dev/world-builder/api"
DEFAULT_CLONE = Path.home() / "code2/generative_agents"
MAZE = "environment/frontend_server/static_dirs/assets/the_ville/matrix"


def fetch_rows(service: str, password: str) -> list[dict[str, Any]]:
    request = urllib.request.Request(f"{service}/runs?full=1&limit=200", headers={"X-World-Builder-Owner": password})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read())["runs"]


def pick_run(rows: list[dict[str, Any]], world: str | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """The newest world's saved rounds in order, and its bundle (only the first round of a run carries it).

    `world` filters by world label or fingerprint; with none given the newest laid-out world is used."""
    ok = sorted((r for r in rows if r.get("path") == "/run" and r.get("status") == 200 and (r.get("result") or {}).get("transcript")),
                key=lambda r: r["ts"])
    if world:
        ok = [r for r in ok if world in (r["request"].get("world"), r["request"].get("world_fingerprint"))]
    for fingerprint in dict.fromkeys(r["request"].get("world_fingerprint") for r in reversed(ok)):
        chain = [r for r in ok if r["request"].get("world_fingerprint") == fingerprint]
        for row in chain:
            bundle = row["request"].get("bundle")
            if bundle and "layout" in bundle:
                return chain, bundle
    raise SystemExit("no saved run of a world that declares a layout" + (f" named {world!r}" if world else ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-log", type=Path, help="a run-log jsonl file instead of asking the service")
    ap.add_argument("--service", default=SERVICE)
    ap.add_argument("--world", help="world label or fingerprint (default: the newest world that declares a layout)")
    ap.add_argument("--clone", type=Path, default=DEFAULT_CLONE)
    ap.add_argument("--port", type=int, default=8780)
    ap.add_argument("--no-serve", action="store_true")
    args = ap.parse_args()
    viewer = ROOT / "viewer/smallville"
    if not (viewer / "assets").exists():
        raise SystemExit("run `python3 scripts/setup_smallville_viewer.py <clone>` first (copies the private art)")
    if args.run_log:
        rows = [json.loads(line) for line in args.run_log.read_text().splitlines() if line.strip()]
    else:
        password = os.environ.get("WORLD_BUILDER_OWNER_PASSWORD")
        if not password:
            raise SystemExit("set WORLD_BUILDER_OWNER_PASSWORD (it is in ~/.secrets/api_keys.env) or pass --run-log")
        rows = fetch_rows(args.service, password)
    chain, bundle = pick_run(rows, args.world)
    replay = export_from_rows(chain, bundle, args.clone / MAZE)
    (viewer / "replay-owner.json").write_text(json.dumps(replay))
    print(f"{bundle['world']['label']}: {len(chain)} saved rounds, {len(replay['steps'])} steps, map {replay['map']}")
    url = f"http://127.0.0.1:{args.port}/index.html?replay=owner"
    print(url)
    if not args.no_serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(viewer))
        http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
