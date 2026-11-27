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
import mimetypes
import urllib.error
import urllib.request
from pathlib import Path

PAGE = Path(__file__).resolve().parent / "world_builder_home.html"
GRAPH_VIEWER = Path(__file__).resolve().parent / "vendor/graph-viewer.js"

ROOT = PAGE.parent.parent
ROOM = ROOT / "viewer/smallville"
ASSETS = {
    "/world-builder": PAGE,
    "/world-builder/graph-viewer.js": GRAPH_VIEWER,
    "/world-builder/room-map": ROOM / "index.html",
    "/world-builder/play": ROOT / "evidence/renders/world-replay-studio-v0.html",
    "/world-builder/build": ROOT / "evidence/renders/world-builder-v0.html",
}
for filename in ("world_builder_retained.js", "world_builder_retained.json"):
    ASSETS[f"/world-builder/{filename}"] = PAGE.parent / filename
for filename in ("index.html", "graph.html", "viewer.js", "replay-public.json", "replay-resident.json",
                 "assets-cc0/tinydungeon.png", "assets-cc0/TinyDungeon-License.txt"):
    ASSETS[f"/world-builder/room-map/{filename}"] = ROOM / filename


def handler(api: str) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        def _proxy(self) -> None:
            size = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(size) if size else None
            headers = {"Content-Type": self.headers.get("Content-Type", "application/json")}
            # Pass through who is asking, so owner mode and agent labelling work against any API.
            for name in ("User-Agent", "X-World-Builder-Owner", "X-World-Builder-Client"):
                if self.headers.get(name):
                    headers[name] = self.headers[name]
            if api.startswith("https://"):
                # The public API accepts only same-origin browser requests (and Cloudflare
                # refuses urllib's default agent), so speak as a page on that origin.
                headers.update({"Origin": api, "Referer": api + "/world-builder/", "Sec-Fetch-Site": "same-origin"})
                headers.setdefault("User-Agent", "Mozilla/5.0 (world-builder dev proxy)")
            req = urllib.request.Request(api + self.path, data=body, method=self.command, headers=headers)
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
            path = self.path.split("?", 1)[0]
            asset = ASSETS.get(path.rstrip("/"))
            if asset and asset.is_file():
                data = asset.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", mimetypes.guess_type(asset.name)[0] or "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
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
