# Goal: Waltzman, attempts from belief, and read traces

Follows [best-of-all-worlds.goal.md](best-of-all-worlds.goal.md), which is done (C1–C6 passed at b7d1dc5,
evidence merged in #198). Brian approved this work on 2026-10-22 ("yes" to steps 1–4 and to the
trace-read check). Profile: continuous-light.

## Mission

1. **Read every run, enforced.** A run reported as evidence is a folder with its server run-log lines
   (`run-log.jsonl`) and a `TRACE_READ.md`; `scripts/check_trace_reads.py` (inside `check_project.py`)
   fails a run whose read-through misses a round, a person who tried a move, an event id per round, an
   llm_client trace id, or findings. Brian, 2026-10-16: agents read the full trace before saying a run works.
2. **The Waltzman example still holds live** after the 2026-10-21/22 changes (seal, approval record,
   engine events, full logs).
3. **Design "attempt from belief" (#128):** people choose from what they believe they can do; an attempt can
   take several rounds and fail or succeed part-way from then-current state (the truck runs out of gas, or
   the driver refuels); they learn the outcome only from what they observe. Prior art to read first: this
   repo's scenario pipeline (Decision 007: attempts with belief and expected effect, the game master's
   mid-run rulings), Concordia's game-master pattern, Cybernetic Influence v3 ADR-013 (capability /
   permission / attempt / adjudication / realised outcome).
4. **Scenario replay shows what #128 needs:** the check that refused a move (G15), each attempt in full and
   the game master's rulings, with `continue` distinct from `no_action` (G16), and the whole built world (G12).
5. **First slice of #128**, only after Brian approves the design: one multi-round activity in the World
   Builder that can fail part-way, behind the existing rules approval.

## Canonical example

Paste Rand Waltzman's scenario into https://brianmills.dev/world-builder/ as a visitor and press Create
simulation: C1–C6 of best-of-all-worlds.goal.md pass again at the new commit. After the #128 slice, a person
in that world starts a multi-round task believing it will work, and a later round shows it failing (or
succeeding) because of state that changed in between, which that person learns from their own observation.

## Done when

- **D1.** The trace-read check is merged, and `scripts/check_project.py` exits 0 on main.
- **D2.** One live run of the canonical example on the owner allowance passes C1–C6 at a named commit, saved
  as `evidence/waltzman-belief-and-traces/<run>/` with `run-log.jsonl` and a `TRACE_READ.md` that the check
  passes, and every round actually read (each person's belief, move and result).
- **D3.** A clickable #128 design page, served from committed git, shows the attempt lifecycle, what the
  person believes versus what is true, where failure is discovered, and which prior art is adopted.
- **D4.** G15, G16 and G12 are marked fixed in `docs/model/`, with tests, and a rendered scenario replay of
  a saved run shows each (screenshot).
- **D5.** If Brian approves D3: the first #128 slice is merged and live, and one live run shows a part-way
  failure or success, read in full (D2's format). Without his approval, stopping after D1–D4 with the design
  link reported is a correct finish.

## Boundaries

- world-substrate and its own deploy only; Cybernetic Influence v3 is read-only.
- Merge after `scripts/check_project.py` exits 0 on the committed change, then deploy and confirm the live
  commit. Publish-checker before anything new goes public.
- AI spend: the owner allowance only; the visitor allowance stays $3/day; no new spend route without
  Brian's yes. No reruns to fish for a behaviour: report every run.
- No outreach to Waltzman. Never restart WSL; the scheduled 2026-10-23 02:00 rebuild takes it down for
  about 6–7 hours. Have work merged by 01:30, then resume after it.
- Respect the storage guard. Do not route around it.

## Stop rules

Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence. A stop at a
boundary (new spend route, outreach, Brian's design approval, a storage-guard block) is a correct finish
when reported with the request made. Revalidate after three increments or about four hours.

## Do not gate on

Brian's review of anything except D5's design approval; Waltzman; llm_client#283; Simudyne; the WSL rebuild.

## Progress

- 2026-10-22: trace-read check built and committed (`feat/trace-read-check`); merged with this document.
- 2026-10-22: D4 merged (#209), D3 merged and live (#210,
  https://brianmills.dev/world-builder/design/attempt-from-belief/). D5 waits for Brian's approval of D3.
- 2026-10-22: D2 live run c1r18 (936153d) read in full: fails C1 item 3 (technical and logistics groups were
  never offered their own message; the 256-move discovery cap cut them off). Fixed in #211 (4b48f22, live);
  evidence in `evidence/waltzman-belief-and-traces/c1r18/`. Rerun c1r19 at 4b48f22.
- 2026-10-22: D2 done. Live run c1r19 (4b48f22, share `SvqRPn-_hgxL`) read in full, all 46 rounds: passes C1
  items 1-7 (all four groups delivered in round 1; readout 51/51; replay with 0 AI calls). Evidence in
  `evidence/waltzman-belief-and-traces/c1r19/`. Open problems seen while reading are listed there (seeded
  recipient memory, retry changes the move but keeps the first `said`, logistics/Country Three reopen loop,
  confusing state labels). D1-D4 done; D5 waits for Brian's approval of the D3 design.
- 2026-10-23: C4 and C5 rerun at 9bfa8d3 so the whole C1-C6 table is evidenced on the new code. C4: pencil
  run c4-run21 (share `NVZGnhM87Yj1`), built as things, 29 rounds, 8 distinct moves every round from round 6,
  real chain, read in full (`evidence/waltzman-belief-and-traces/c4-run21/`). C5: forced rules rejection and
  forced visitor and owner budget stops each show a plain message (`.../c5-9bfa8d3/`). D4's rendered replay
  screenshot is `spikes/any-scenario-2026-10/evidence/waltzman/run/frame-round2-attempts.png` (#209).
- 2026-10-23: Brian approved D3 ("yes"). First #128 slice built (`scripts/attempts.py`): a move that sets a
  field a world process watches starts a task; the run follows it across one-round requests (the page sends
  open tasks back as `underway`), the person who started it is told each round what they expected beside what
  they now see, and the page lists tasks under way, stopped part-way and finished. Free replays: truck on an
  empty tank stops part-way, with fuel finishes; in the saved Waltzman world all 51 remedies finished because
  generated rules could never write `concern`, so a generated process may now stop a remedy part-way (status
  back to open) and the rules guidance asks for one when the description names something a remedy needs.
  The build check flags a start that refuses up front on a stock its own task uses up. Full check: 692 tests OK.
