# World Builder checks that cost real model money

Kept in git so they survive WSL restarts (session scratch folders under `/tmp` do not).

| Tool | What it checks | Run |
| --- | --- | --- |
| `world_builder_e2e.mjs` | The landing page as a visitor uses it: `tooltips` (free), `task`, `ongoing`, `open`, `pencil` (build, approve, watch it play live; continuing worlds are paused, checked to stay still, resumed; `E2E_AI=1` also switches to AI moves mid-play), `lucky` (empty box, Surprise me), `dialogue` (the Not sure what to write? link) | `npm install && npx playwright install chromium && node world_builder_e2e.mjs https://brianmills.dev task open` |
| `stuck_world_e2e.mjs` | A saved world that gets stuck (`fixtures/toy-workshop-stuck.json`, served instead of building, so free): review warns it goes in circles, live note names who is stuck, picture shows, play pauses itself at 100 rounds and resumes | `node stuck_world_e2e.mjs http://127.0.0.1:8898` (about 3 minutes; needs a running API) |
| `../measure_world_builder.py` | How often generated worlds are runnable and finish (task) or stay active (ongoing/open) | `uv run --no-project --python 3.12 python scripts/measure_world_builder.py --base http://127.0.0.1:8899 --kinds task,open` (add `--description "..."` to build your own text instead of the built-in set) |
| `../world_builder_runs.py` | Who built and ran what on the live site (owner only) | `WORLD_BUILDER_OWNER_PASSWORD=... python3 scripts/world_builder_runs.py --limit 20` |
| `../dev_world_builder.py` | Serves the landing page against a local API for these checks | `python3 scripts/dev_world_builder.py` after starting `scripts/world_builder_service.py --port 8899` |

Set `WORLD_BUILDER_OWNER_PASSWORD` (from `~/.secrets/api_keys.env`) so runs spend the owner allowance, never the public visitor budget. Each run prints per-step lines and a `RESULT` line with counts, and exits nonzero on failure. The public service has a $0.50/day model budget shared by all visitors; prefer a local service for repeated measurement. Put throwaway outputs in `~/code/.scratch/world-builder/` (on disk, 7-day retention), not in git and not in `/tmp`.
