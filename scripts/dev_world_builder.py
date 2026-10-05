#!/usr/bin/env python3
"""Serve the World Builder landing page locally against a local API.

Starts nothing else: run `scripts/world_builder_service.py --port 8899` first
(with OPENROUTER_API_KEY and llm_client available), then

    python3 scripts/dev_world_builder.py --port 8898

and open http://127.0.0.1:8898/world-builder/ . The page is read from
scripts/world_builder_home.html on every request, so edits show on reload;
/world-builder/api/* is forwarded to the API unchanged.
"""
from __future__ import annotations

import argparse
import http.server
import urllib.error
import urllib.request
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "world_builder_home.html"


def handler(api: str) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        def _proxy(self) -> None:
            size = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(size) if size else None
            req = urllib.request.Request(api + self.path, data=body, method=self.command,
                                         headers={"Content-Type": self.headers.get("Content-Type", "application/json")})
            try:
                with urllib.request.urlopen(req, timeout=900) as response:
                    code, data = response.status, response.read()
            except urllib.error.HTTPError as error:
                code, data = error.code, error.read()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:  # noqa: N802
            if self.path.startswith("/world-builder/api"):
                return self._proxy()
            if self.path.rstrip("/") == "/world-builder":
                data = PAGE.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(data)
                return
            self.send_response(404)
            self.end_headers()

        def do_POST(self) -> None:  # noqa: N802
            self._proxy()

        def log_message(self, *args: object) -> None:
            pass

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--port", type=int, default=8898)
    parser.add_argument("--api", default="http://127.0.0.1:8899")
    args = parser.parse_args()
    print(f"World Builder page on http://127.0.0.1:{args.port}/world-builder/ (API {args.api})", flush=True)
    http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler(args.api)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
