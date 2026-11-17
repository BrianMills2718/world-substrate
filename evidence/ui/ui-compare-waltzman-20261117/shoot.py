import json, sys, asyncio
from playwright.async_api import async_playwright
S = sys.argv[1]
CHROME = "/home/brian/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome"
PAGES = {
  "wb_home": "https://brianmills.dev/world-builder/",
  "wb_run": "https://brianmills.dev/world-builder/?run=FQHXnP_TLKPi",
  "donor": "https://brianmills.dev/waltzman/",
  "hall_v2": "https://brianmills.dev/waltzman/world-substrate",
  "demo_v0": "https://brianmills.dev/world-substrate-visualization/",
  "native": "https://brianmills.dev/world-substrate-runs/waltzman-native/",
  "play": "https://brianmills.dev/world-builder/play/",
  "build": "https://brianmills.dev/world-builder/build/",
  "living_v1": "file:///home/brian/code2/world-substrate/evidence/renders/waltzman-living-v1.html",
}
ALLOWED_POST = ("/live-replay",)
async def guard(route):
    r = route.request
    if r.method != "GET" and not any(r.url.split("?")[0].endswith(p) for p in ALLOWED_POST):
        print("BLOCKED", r.method, r.url, flush=True); await route.abort(); return
    await route.continue_()
async def main():
    only = sys.argv[2:] or list(PAGES)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME)
        log = {}
        for name in only:
            url = PAGES[name]
            for w, h in ((1280, 800), (390, 844)):
                ctx = await b.new_context(viewport={"width": w, "height": h})
                pg = await ctx.new_page(); await pg.route("**/*", guard)
                errs = []
                pg.on("console", lambda m, errs=errs: errs.append(m.text[:200]) if m.type == "error" else None)
                pg.on("pageerror", lambda e, errs=errs: errs.append("PAGEERROR " + str(e)[:200]))
                await pg.goto(url, wait_until="load", timeout=60000)
                await pg.wait_for_timeout(9000 if name.startswith("wb_run") else 3000)
                await pg.screenshot(path=f"{S}/shots/{name}-{w}.png")
                await pg.screenshot(path=f"{S}/shots/{name}-{w}-full.png", full_page=True)
                dims = await pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight]")
                log[f"{name}-{w}"] = {"errors": errs, "scroll": dims}
                await ctx.close()
        print(json.dumps(log, indent=1))
        await b.close()
asyncio.run(main())
