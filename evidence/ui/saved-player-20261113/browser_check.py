"""Exercise the real saved-run player without any simulation/model writes.

Run with ``uv run --no-project --with playwright python <this-file>``.
Use --source PATH for a checkout's HTML over actual saved-record GETs, or --live.
The initial red receipt was recorded before the new player existed.
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from playwright.async_api import async_playwright, expect

ROOT = Path(__file__).resolve().parents[3]
CHROMIUM = Path.home() / ".cache/ms-playwright/chromium-1254/chrome-linux64/chrome"
BASE = "https://brianmills.dev/world-builder/"
PUMP = "T-e9dYLdIi61"
LEGACY = "PKVERt8chzt7"


class Run:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.out = args.output.resolve()
        self.out.mkdir(parents=True, exist_ok=True)
        self.checks: list[str] = []
        self.errors: list[str] = []
        self.failed_requests: list[str] = []
        self.blocked_writes: list[str] = []
        self.api_responses: list[dict[str, Any]] = []
        self.source = args.source.resolve()

    def passed(self, name: str) -> None:
        self.checks.append(name)

    async def route(self, route):
        request = route.request
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            self.blocked_writes.append(request.url)
            await route.abort()
            return
        if not self.args.live and request.is_navigation_request() and request.url.startswith(BASE + "?"):
            await route.fulfill(body=self.source.read_text(), content_type="text/html")
            return
        await route.continue_()

    async def select_round(self, page, number: int):
        options = await page.locator("#saved-round-select option").evaluate_all(
            "els => els.map(el => ({value:el.value,text:el.textContent,round:el.dataset.round}))"
        )
        # Known UI labels are checked here, never inferred as simulation meaning.
        matches = [x for x in options if x.get("round") == str(number) or x["text"].strip() in {str(number), f"Round {number}"} or x["text"].strip().startswith(f"Round {number} ")]
        assert len(matches) == 1, (number, options)
        await page.locator("#saved-round-select").select_option(matches[0]["value"])
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", str(number))

    async def select_event(self, page, event_id: str, historical: bool = False):
        scope = page if historical else page.locator("#saved-events")
        button = scope.locator(f'button[data-event-id="{event_id}"]').first
        await expect(button).to_be_attached()
        await button.evaluate("el => { for(let p=el.parentElement;p;p=p.parentElement) if(p.tagName==='DETAILS')p.open=true; }")
        await button.focus()
        await button.press("Enter")
        await expect(page.locator("#saved-event-detail")).to_have_attribute("data-event-id", event_id)

    async def state(self, page, path: str, value: Any):
        field = page.locator(f'#saved-world-state [data-state-path="{path}"]')
        await expect(field).to_have_count(1)
        expected = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        await expect(field).to_have_attribute("data-state-value", expected)
        assert await field.is_visible(), path

    async def actor_input(self, page, actor: str, number: int):
        panel = page.locator("#saved-actor-input")
        await expect(panel).to_have_attribute("data-actor", actor)
        await expect(panel).to_have_attribute("data-round", str(number))
        retained = json.loads((ROOT / "evidence/i0-i1/visible-run-20261113/share.json").read_text())
        expected = next(row for row in retained["actor_inputs"][actor] if row["round"] == number)
        raw = []
        for text in await panel.locator("pre").all_text_contents():
            try:
                raw.append(json.loads(text))
            except json.JSONDecodeError:
                continue
        matches = [row for row in raw if isinstance(row, dict) and row.get("round") == number and row.get("context", {}).get("actor_id") == actor]
        assert len(matches) == 1, (actor, number, "Exact retained actor input must remain available", raw)
        for key in ("messages", "context", "memory", "output"):
            assert matches[0].get(key) == expected.get(key), (actor, number, key)

    async def open_ancestor_details(self, locator):
        await locator.evaluate("el => { for(let p=el.parentElement;p;p=p.parentElement) if(p.tagName==='DETAILS')p.open=true; }")

    async def capture(self, page, name: str):
        await page.mouse.move(0, 0)
        await page.locator("body").screenshot(path=str(self.out / f"{name}.png"))
        (self.out / f"{name}.txt").write_text(await page.locator("body").inner_text())

    async def playback(self, page, width: int):
        await page.evaluate("""() => {
          const player = document.querySelector('#saved-player');
          window.__savedPlayerObservedRounds = [player.dataset.round];
          window.__savedPlayerRoundObserver = new MutationObserver(() => {
            const round = player.dataset.round;
            const observed = window.__savedPlayerObservedRounds;
            if (round !== observed[observed.length - 1]) observed.push(round);
          });
          window.__savedPlayerRoundObserver.observe(player, {attributes:true, attributeFilter:['data-round']});
        }""")
        await page.locator("#play-btn").click()
        await expect(page.locator("#play-btn")).to_have_text(re.compile("Pause"))
        # The recorded player uses a 2000ms interval. 3500ms permits one interval
        # plus scheduling margin, while detecting an accidental duplicate first round.
        await page.wait_for_function("window.__savedPlayerObservedRounds.length > 1", timeout=3500)
        rounds = await page.evaluate("window.__savedPlayerObservedRounds")
        assert rounds[:2] == ["1", "2"], rounds
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "2")
        await page.locator("#play-btn").click()
        await expect(page.locator("#play-btn")).to_have_text(re.compile("Play|Replay"))
        await page.wait_for_timeout(2300)
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "2")
        self.passed(f"{width}: Play advances once from round1 to round2 and Pause holds that round beyond the playback interval")

        await self.select_round(page, 6)
        await expect(page.locator("#play-btn")).to_have_text(re.compile("Replay|Watch again"))
        await page.locator("#play-btn").click()
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "1")
        await expect(page.locator("#play-btn")).to_have_text(re.compile("Pause"))
        await page.locator("#play-btn").click()
        await page.wait_for_timeout(2300)
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "1")
        self.passed(f"{width}: Replay from final round returns to round1 and can immediately be paused")
        await page.evaluate("window.__savedPlayerRoundObserver.disconnect()")

    async def pump(self, context, width: int):
        page = await context.new_page()
        page.set_default_timeout(self.args.timeout)
        page.on("pageerror", lambda error: self.errors.append(str(error)))
        page.on("requestfailed", lambda request: self.failed_requests.append(request.url) if "/cdn-cgi/rum" not in request.url else None)
        await page.goto(BASE + "?run=" + PUMP, wait_until="domcontentloaded")
        await expect(page.locator("#saved-player")).to_be_visible()
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "1")
        await expect(page.locator("#play-btn")).to_have_text(re.compile("Play|Replay"))
        options = await page.locator("#saved-round-select option").count()
        assert options == 6, options
        assert "prototype pump" in (await page.locator("#saved-scenario").inner_text()).lower()
        await page.wait_for_timeout(2300)
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "1")
        self.passed(f"{width}: saved scenario is visible, all six rounds seekable, initial round stays paused")
        await self.capture(page, f"{width}-initial")
        await self.playback(page, width)

        await self.select_event(page, "r1-e00002")
        detail = await page.locator("#saved-event-detail").inner_text()
        for text in ("not assenting", "record assent", "false", "true"):
            assert text in detail.lower(), (text, detail)
        await self.state(page, "entities.position-bo.components.actor_position.assent", True)
        await self.actor_input(page, "bo", 1)
        actor_text = await page.locator("#saved-actor-input").inner_text()
        assert "Turn 6" not in actor_text and "Input before round 6" not in actor_text
        assert "sensor channel C drifted 8" not in actor_text, "Bo received another actor's private detail"
        self.passed(f"{width}: Bo original words, interpreted assent, actual false-to-true consequence and own round1 input stay together")
        await self.capture(page, f"{width}-bo-round1")

        await self.select_round(page, 3)
        await self.select_event(page, "r3-e00001")
        await self.state(page, "entities.pump-activation.components.validation_decision.review", "completed")
        await self.actor_input(page, "ari", 3)
        self.passed(f"{width}: Ari validation event restores its own intermediate completed-review state and round3 input")
        await self.select_event(page, "r3-e00002")
        await self.state(page, "entities.pump-activation.components.validation_decision.hold", False)
        await self.state(page, "entities.pump-activation.components.validation_decision.validation", "passed")
        await self.state(page, "entities.pump-activation.components.validation_decision.review", "idle")
        child = await page.locator("#saved-event-detail").text_content()
        assert "r3-e00001" in child, child
        self.passed(f"{width}: immediate child has its own causal parent and hold/validation/review state")
        await self.capture(page, f"{width}-validation-child")

        await self.select_round(page, 6)
        await self.select_event(page, "r3-e00002", historical=True)
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "3")
        await expect(page.locator("#saved-world-state")).to_have_attribute("data-event-id", "r3-e00002")
        await self.state(page, "entities.pump-activation.components.validation_decision.review", "idle")
        self.passed(f"{width}: selecting historical child from round6 restores round3 child state rather than latest-round state")

        await page.locator("#saved-round-next").focus()
        await page.locator("#saved-round-next").press("Enter")
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "4")
        await page.locator("#saved-round-prev").focus()
        await page.locator("#saved-round-prev").press("Enter")
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "3")
        await page.locator("#saved-round-range").focus()
        await page.locator("#saved-round-range").press("ArrowRight")
        await expect(page.locator("#saved-player")).to_have_attribute("data-round", "4")
        self.passed(f"{width}: previous, next and range support keyboard round navigation")

        for selector in ("#saved-round-prev", "#saved-round-next", "#saved-round-select", "#saved-round-range"):
            control = page.locator(selector)
            box = await control.bounding_box()
            assert box and box["height"] >= 44 and box["width"] >= 44, (selector, box)
            await control.hover()
            await expect(page.locator("#tip-bubble")).to_be_visible(timeout=1000)
            assert (await page.locator("#tip-bubble").inner_text()).strip(), selector
            await page.mouse.move(0, 0)
        self.passed(f"{width}: main navigation controls have at least44px targets and styled hover tooltips")
        next_control = page.locator("#saved-round-next")
        await next_control.focus()
        await expect(page.locator("#tip-bubble")).to_be_visible(timeout=1000)
        if width <= 600:
            await next_control.scroll_into_view_if_needed()
            box = await next_control.bounding_box()
            session = await context.new_cdp_session(page)
            try:
                await session.send("Input.dispatchTouchEvent", {"type": "touchStart", "touchPoints": [{"x": box["x"] + box["width"] / 2, "y": box["y"] + box["height"] / 2}]})
                await expect(page.locator("#tip-toast")).to_be_visible(timeout=1200)
            finally:
                await session.send("Input.dispatchTouchEvent", {"type": "touchEnd", "touchPoints": []})
                await session.detach()
            self.passed(f"{width}: a real touch long-press exposes navigation help without requiring hover")
        self.passed(f"{width}: keyboard focus exposes the same styled navigation help")
        assert await page.locator("body").evaluate("el=>el.scrollWidth<=innerWidth"), "page overflows horizontally"
        for selector in ("#saved-events", "#saved-event-detail", "#saved-world-state", "#saved-actor-input"):
            assert await page.locator(selector).evaluate("el=>el.scrollWidth<=el.clientWidth"), selector
        self.passed(f"{width}: critical player regions wrap within desktop/phone viewport")

        await page.locator("#context-mode").select_option("actor")
        await expect(page.locator("#saved-player")).to_be_hidden()
        await expect(page.locator("#analyst-context")).to_be_hidden()
        await page.locator("#context-actor").select_option("bo")
        actor_body = await page.locator("#actor-context").inner_text()
        assert "sensor channel C drifted 8" not in actor_body
        assert "trace_id" not in actor_body and "provenance" not in actor_body
        self.passed(f"{width}: Actor-only mode hides analyst state/navigation and other actors' input/provenance")
        await page.locator("#context-mode").select_option("analyst")
        for selector in ("#replay", "#network", "#attempts"):
            locator = page.locator(selector)
            await expect(locator).to_be_attached()
            await self.open_ancestor_details(locator)
            if selector != "#replay":
                await expect(locator).to_be_visible()
        self.passed(f"{width}: preserved picture, network and refusal inspection remain reachable")
        await page.close()

    async def legacy(self, context, width: int):
        page = await context.new_page()
        page.set_default_timeout(self.args.timeout)
        page.on("pageerror", lambda error: self.errors.append(str(error)))
        await page.goto(BASE + "?run=" + LEGACY, wait_until="domcontentloaded")
        await expect(page.locator("#saved-player")).to_be_visible()
        await self.select_event(page, "r1-e00001")
        assert "training" in (await page.locator("#saved-event-detail").inner_text()).lower()
        unavailable = (await page.locator("#saved-actor-input").inner_text()).lower()
        assert any(term in unavailable for term in ("not recorded", "unavailable", "no authorized", "legacy")), unavailable
        self.passed(f"{width}: older airfield accepted event stays readable and absent authorized inputs are explicit")
        await self.select_event(page, "r1-e00002")
        unmatched = (await page.locator("#saved-event-detail").inner_text()).lower()
        assert "invite him" in unmatched and any(word in unmatched for word in ("unmatched", "no installed", "not match")), unmatched
        await self.select_event(page, "r1-e00004")
        refused = (await page.locator("#saved-event-detail").inner_text()).lower()
        assert any(word in refused for word in ("refused", "precondition", "check")), refused
        self.passed(f"{width}: historical unmatched and rule-refused events remain distinct")
        await page.close()

    async def main(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(executable_path=str(CHROMIUM), headless=True, args=["--no-sandbox"])
            try:
                for width in self.args.widths:
                    context = await browser.new_context(viewport={"width": width, "height": 1000 if width > 600 else 844}, has_touch=width <= 600)
                    await context.route("**/*", self.route)
                    await self.pump(context, width)
                    await self.legacy(context, width)
                    await context.close()
            finally:
                await browser.close()
        assert not self.errors, self.errors
        assert not self.failed_requests, self.failed_requests
        assert all("/cdn-cgi/rum" in url for url in self.blocked_writes), self.blocked_writes

    def receipt(self, failure: str | None):
        return {"schema": "saved-player-browser-check/v1", "mode": "live" if self.args.live else "local source over actual read-only saved GETs", "source_sha256": hashlib.sha256(self.source.read_bytes()).hexdigest(), "viewports": self.args.widths, "passed_checks": len(self.checks), "checks": self.checks, "page_errors": self.errors, "unexpected_failed_requests": self.failed_requests, "blocked_writes": self.blocked_writes, "no_model_calls": True, "failure": failure, "result": "fail" if failure else "pass"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "scripts/world_builder_home.html")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "browser-results")
    parser.add_argument("--widths", nargs="+", type=int, default=[1440, 390])
    parser.add_argument("--timeout", type=int, default=8000)
    args = parser.parse_args()
    run = Run(args)
    failure = None
    try:
        asyncio.run(run.main())
    except Exception as error:
        failure = f"{type(error).__name__}: {error}"
    receipt = run.receipt(failure)
    (run.out / "checks.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in receipt.items() if key not in {"checks", "blocked_writes"}}, ensure_ascii=False))
    return 1 if failure else 0


if __name__ == "__main__":
    sys.exit(main())
