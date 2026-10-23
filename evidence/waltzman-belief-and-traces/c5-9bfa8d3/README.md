# C5 at 9bfa8d3 (2026-10-23)

Failures say so plainly. No AI call was made in any of these.

- **Forced rules rejection** (live site): the page's build answer was the saved c4-run20 world (mocked in the
  browser), and every `/run` it sent had one rule rewritten to change a part the world does not have. The live
  server answered 422 and the page said: "Paused: These rules were refused before anything ran, so nothing
  changed: one rule does not fit this world (...). Build the world again or start from an example." No
  "internal world-builder error" text. `c5-rules-9bfa8d3.json`, `c5-rules-rejection-9bfa8d3.png`.
- **Forced budget stop, visitor**: the live page with its API calls routed to a test container `wb-c5-budget`
  from the live image `world-builder:9bfa8d3ac61a`, visitor ledger seeded at $3.00 spent for 2026-10-23, no
  OpenRouter key. The page shows "Today's AI budget is used up; it resets at midnight UTC." with Create
  disabled and no build request sent (only GET health). `c5-budget-visitor-allowance-used-9bfa8d3.*`.
- **Forced budget stop, owner**: same container, owner allowance $0.0001. The build request was accepted
  (202), its job answered 429, and the page says "Your owner AI allowance for today is used up; it resets at
  midnight UTC. You can still watch an example run." No internal error text.
  `c5-budget-owner-allowance-0.0001-9bfa8d3.*`.

The container was removed and the tunnel closed after the check.
