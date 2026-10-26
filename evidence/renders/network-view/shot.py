"""Render the World Builder Network view against a saved shared run (no AI, no server API)."""
import json, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

wt = Path(sys.argv[1]); share = json.loads(Path(sys.argv[2]).read_text()); out = Path(sys.argv[3])
srv = subprocess.Popen([sys.executable, str(wt / "scripts/dev_world_builder.py"), "--port", "8897", "--api", "http://127.0.0.1:9"])
time.sleep(1.5)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=str(Path.home() / ".cache/ms-playwright/chromium-1247/chrome-linux64/chrome"))
        pg = b.new_page(viewport={"width": 1280, "height": 1000})
        logs = []
        pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}"))
        pg.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
        def api(route):
            url = route.request.url
            if url.endswith("/health"):
                return route.fulfill(json={"ok": True, "llm_daily_budget_usd": 1, "llm_daily_committed_usd": 0})
            if "/share/" in url:
                return route.fulfill(json=share)
            return route.fulfill(status=404, json={"error": "not in this test"})
        pg.route("**/world-builder/api/**", api)
        pg.goto("http://127.0.0.1:8897/world-builder/?run=test")
        pg.wait_for_selector("#net-graph .react-flow", timeout=30000)
        pg.wait_for_timeout(int(sys.argv[4]) if len(sys.argv) > 4 else 6000)
        pg.locator("#network").scroll_into_view_if_needed()
        pg.locator("#network").screenshot(path=str(out))
        print("caption:", pg.locator("#net-caption").inner_text())
        print("outcome:", pg.locator("#outcome").inner_text())
        nodes = pg.locator("#net-graph .react-flow__node").count()
        print("nodes drawn:", nodes)
        first = pg.locator("#net-graph .react-flow__node", has_text=sys.argv[5] if len(sys.argv) > 5 else "").first
        first.click(); pg.wait_for_timeout(400)
        print("detail:", pg.locator("#net-detail").inner_text())
        print("\n".join(logs[-10:]))
        b.close()
finally:
    srv.terminate()
