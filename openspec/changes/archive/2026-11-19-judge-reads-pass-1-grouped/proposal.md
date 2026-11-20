## Why

The Waltzman run on 2026-11-19 (`s4-waltzman-4`, world-substrate#473) cost 23 times a round of `s4-waltzman-3`
because each judge prompt was about 285,000 tokens (1,197,727 characters, call 24925). 1,161,410 characters of it
were pass 1, written with indentation: for the person acting and the four people named, every blocked binding of
`communicate` (80 each, one per information, delivery and recipient) with every check, most of them passing. The
judge rules on one person's one attempt; it needs which moves are blocked and by what, not 400 copies of passing
checks.

## What Changes

- `consequence_report.pass_one_reading` gives pass 1 as the judge reads it: a person's blocked bindings of one move
  as one entry (count, first binding as an example, each failed check with its value, what it requires and how many
  bindings it stopped); open moves without their checks, which all pass; the same values. `pass_one` is unchanged.
- The judge reads that reading, in compact JSON. The run row keeps `consequence.pass_one` in full.
- Measured on call 24925's pass 1: 1,161,410 characters before, 40,865 after; the whole prompt 1,197,727 to 77,182
  characters (about 18,400 tokens, worked out at the call's measured 0.238 tokens per character).
