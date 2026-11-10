# Trace read

Run: "empty purse" (`tests/judge_worlds.py` `empty_purse()`: the port with the coin rule `hand-coins` already
installed, and a second trader, Ines, who holds no coins), 1 round, policy `resident`, owner allowance, posted by
`post_world.py empty-purse` to a local service on the J2 branch, 2026-11-10 18:26 UTC. Ines's brief tells her to bluff:
she holds no coins, and means to hand Rosa 10 from her purse anyway. One run-log line, `run-log.jsonl`; its one
llm_client trace id is `world-builder-live/run/174dd4921aec4efb800ae0660c46d8d0`. Measured cost: `cost_usd` 0.0010218,
matching the 6 `llm_calls` rows (3 interpreter, 3 resident, no judge call). `earlier-tries.jsonl` holds the six other
paid tries ($0.0073 for the five from 18:09 to 18:12, under the debt briefs of `post_world.py` at `31142e0`, and $0.0010 for
a repeat of this run, trace bac136e5, with the same result); in none did a trader without coins try to hand coins, so
the offer this run shows did not arise before the bluff brief.

I read the round, every person's belief, expectation and event, and the engine events. There is no judge call to
read: that absence is the finding. Interpreter and resident calls: read through their recorded outputs.

## Findings

- **A3 holds.** Ines's words ("I try to hand Rosa 10 coins at the customs desk") were read as `hand-coins` to Rosa,
  amount 10, which the installed rule covers. The engine refused it: `precondition_failed`, r1-e00001, `refused_because`
  "the giver holds that many coins" (Ines holds 0). Nothing changed. The attempt row has no `judge` and the run page
  prints "Decided by rule, judge not asked." for it. The refusal wording is the rule's own check label; the plan's
  "holds 0 coins" is a paraphrase, and the actual (0) sits in the engine event's check row, not in the label.
- **The brief carries the demonstration.** Without the bluff, residents never offered coins they lack (seven runs in this
  folder and `earlier-tries.jsonl`: Ines declared the crate, asked Rosa to sign, or searched her purse and was ruled "no rule needed"). This
  run is one honest sample of what a person who bluffs does, not a count of how often.
- **Rosa and Vik.** Rosa inspected the crate (r1-e00002) and did not sign; Vik waited as briefed.

## Round 1

- Ines (`ines`) tried `hand-coins` to Rosa, amount 10: refused by the installed rule, r1-e00001, "the giver holds that
  many coins"; judge not asked.
- Rosa (`rosa`) tried `inspect-crate` on the crate: accepted, r1-e00002.
- Vik (`vik`) waited as briefed (no event).
