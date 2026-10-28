# Which model reviews the rules (Q44, declared-laws plan S3)

One run, 2026-10-28: `run_choice.py` sent the same request to three models: the description, the world's laws and the
compiled rules of each of seven saved incident worlds, and nothing else. All three used the same findings schema.
Results: `results.jsonl`, 21 calls, 0 errors, $0.4356 in total. Trace ids are `s3-review-choice/<world>/<model>`.
gpt-6-luna writes the rules, so it is here only as a same-family control. The plan forbids it as the reviewer.

I read every finding against the bug each world is known for (plan, incident table). "Yes" means a finding names that
bug; the finding is quoted in short. Nothing was scored by pattern matching.

| World | Known bug | gemini-3.1-pro-preview | deepseek-v4-flash | gpt-6-luna (control) |
| --- | --- | --- | --- | --- |
| pencil13-kept | buy-boxed-pencils pays nothing (L4) | **yes**: "buy-boxed-pencils … removes the boxed pencils … without any money being paid" (and the same for all 7 buy-* moves) | no: it names buy-boxed-pencils only for a hard-coded shop | no |
| pencil2-live | clay, paint, erasers and ferrules come from nowhere | yes: "no rule that allows anyone to … obtain clay" | yes | yes |
| pencil4-live | stock with nowhere to go (the supplier's clay and paint) | yes: "no rule to deliver clay, paint … from the supplier" | yes | yes |
| pencil4-live | ship-pencil-boxes needs a component no entity has | no (it names only a Pennsylvania-only restriction) | no | no |
| pencil9-live | a seller starts with none of what it sells | yes: "cut-cedar subtracts logs … instead of producing" them | yes | yes |
| pencil-s2-kept | buy-*-transfer moves goods and no cash | no | no | no ("the transfer effects are sensible") |
| pencil-s2-kept | trucks deliver into their own stock | yes: deliver-packed-boxes "lacks an effect to ever add them to the destination shop" | yes | yes |
| pencil-s2-2-kept | cedar-total does not name saw-slats | yes: "the cedar law does not name this move and would refuse it" | no | yes |
| pencil-s2-3-kept | no move takes goods from another holder | yes: "No rule transfers cedar logs from the logger … to the mill" (and four more) | no | yes |

Bugs named: gemini 7 of 9, deepseek 4 of 9, luna 6 of 9. Only gemini named the L4 bug: pencil13's unpaid purchase.
pencil-s2's "everyone starts with 1000 of everything" cannot be found here, because the reviewer is never shown
starting stock.

Gemini also made claims that are wrong or doubtful. On pencil13 it says mine-graphite "conjures" graphite; that may be
how the description reads, so I counted it neither way. On pencil2 it says sell-pencils pays from a field that "may be
zero"; luna said the same, and it is a real mismatch. Neither of the others had fewer false findings.

Cost: gemini $0.038–0.099 per call (median about $0.05); deepseek and luna about $0.002.

**Choice: `openrouter/google/gemini-3.1-pro-preview` at medium reasoning effort.** It is the only reviewer from another
family that named both the L4 bug and more than half of the bugs. That clears the plan's bar for review that is more
than advice. deepseek is 25 times cheaper but missed the unpaid purchase, which is the canonical example.

To keep the cost down, the build reviews only a try it would otherwise keep, plus each structure's last try. A try the
test run already faults gets that fault fixed first (scripts/world_builder_service.py).

What this means for S4: the review named the incidents behind `_unsourced_inputs` (pencil2), `_dead_end_stock`
(pencil4) and `_starved_holders` (pencil9). Those checks are candidates to retire. `_missing_components` (pencil4's
ship-pencil-boxes) stays, because no reviewer named that incident. Each retirement still needs its own S4 replay (L6).
