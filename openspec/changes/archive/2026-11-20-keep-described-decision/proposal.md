# Ask again when a draft leaves out the decision its description asks for

Plan size: small

## Why

The Waltzman rebuild s4w6 (`evidence/declared-laws/s4-waltzman-6/`, issue #496) had no decision: two identical
scenario requests race and the first answer is kept, and the kept one (call 25412) was the only reply of four without
the activation decision. Every generated move then only recorded its own work, so nothing could be decided. The
named-groups check that should catch a bad draft had not run at all: it failed on every build with
`LLMConfigurationError: reasoning_effort is required`.

## What changes

- The draft check also says which shared decision the description asks for when the draft has none; the builder then
  asks again once, together with any missing groups, and notes it if the second draft still has no decision.
- The check call states its reasoning level (`low`), so it runs again.

## Impact

- `scripts/people_world.py` (`check_draft`; `check_named_groups` kept as a wrapper); tests in `tests/test_named_groups.py`.
- No extra call on a good draft; one more scenario request when the decision is missing.
