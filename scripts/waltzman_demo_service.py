#!/usr/bin/env python3
"""Tiny read-only HTTP/SSE host for the Waltzman living-world demo."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_waltzman_demo import render_html
from scripts.run_waltzman_demo import build_demo_runs
from world_substrate.projection import projection_sse_messages


class WaltzmanDemoHandler(BaseHTTPRequestHandler):
    runs = build_demo_runs()

    def _branch(self) -> str:
        query = parse_qs(urlparse(self.path).query)
        branch = query.get("branch", ["baseline"])[0]
        return branch if branch in self.runs else "baseline"

    def _send(self, body: bytes, content_type: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._send(render_html(self.runs).encode(), "text/html; charset=utf-8")
            return
        if path == "/api/branches":
            body = json.dumps(
                {
                    "branches": [
                        {"id": name, "fork": run["fork"], "event_count": len(run["events"])}
                        for name, run in self.runs.items()
                    ]
                },
                sort_keys=True,
            ).encode()
            self._send(body, "application/json")
            return
        if path == "/api/projection":
            body = json.dumps(self.runs[self._branch()], sort_keys=True).encode()
            self._send(body, "application/json")
            return
        if path == "/api/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "close")
            self.end_headers()
            for message in projection_sse_messages(self.runs[self._branch()]):
                self.wfile.write(message.encode())
                self.wfile.flush()
            return
        self._send(b"not found\n", "text/plain; charset=utf-8", 404)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), WaltzmanDemoHandler)
    print(f"Waltzman demo: http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
