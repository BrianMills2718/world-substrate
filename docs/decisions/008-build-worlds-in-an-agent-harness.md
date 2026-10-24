---
description: "World Builder builds worlds inside an agent harness (Codex on OpenRouter) that drafts, checks and edits, not bare one-shot LLM calls."
---

# Decision 008: Build worlds inside an agent harness, not with bare LLM calls

Governs: scripts/people_world.py, scripts/world_builder_service.py, spikes/any-scenario-2026-10

**Status:** accepted (implementation in progress)
**Date:** 2026-10-16
**Decided by:** Brian, in session 2026-10-16: "codex agents should be able to flexibly build and then lint/test and then do small etis and iterate untile ach step is done"; "this is rediculous that we arent using the actual harness and are using bare llm calls. no wodner we are having so much problems. please make sure tot odcuemnt this leanring"; billing: "yeah we can use openrotuer".
**Related:** [Decision 007](007-any-scenario-path.md), goal `docs/plans/best-of-all-worlds.goal.md`

## Context (observed)

Until this decision the people-world build was three one-shot structured calls (`call_llm_structured` /
`call_llm_json_schema`): people, then actions, then rules. Our own code wrapped them in a fixed two-attempt loop, a
merge with compiled rules, and a growing set of automatic repairs and guidance sentences. On 2026-10-16 alone the
Waltzman test runs inc15f–inc15l (records: `~/code/.scratch/waltzman-demo/STATE.md`) each failed in a new way, and each
fix added more of the same:

- one rule mismatched → the retry rewrote all 16 rules;
- a rule whose only effect wrote a compiled component was removed by the merge, leaving its action rule-less and
  failing the whole build (fix b769d0f);
- people went idle, duplicated compiled actions or toggled a text field; each answer was another sentence of guidance.

That is a home-made, weak agent harness. The checks we already have (the causal compiler and the scripted dry run)
are exactly a linter and a test suite, but the model never got to run them itself and fix only what failed.

## Decision

1. The build runs inside a real agent harness: Codex (`codex exec`, through llm_client's `agents_codex` wrapper where
   it fits), in a scratch workspace holding the world files and one check command.
2. The check command runs the existing compiler and dry run and prints exact, actionable problems (an action without a
   rule, people with nothing to do after round N, a decision that can never move). The agent drafts, runs the check,
   makes small edits, and repeats until the check passes or the build budget or time runs out.
3. Billing stays on the OpenRouter key with `openrouter/openai/gpt-6-luna` (Codex custom provider,
   `wire_api="responses"`); no new spend route. `WORLD_BUILDER_STRONG_MODEL` still switches to sol for a shared demo.
4. The harness runs with its own clean Codex home: no personal agent rules, hooks or skills.
5. Once the harness build beats the current path on the Waltzman text, the hand-written retry loop, the special-case
   repairs and most guidance sentences are removed.

## Evidence so far

- Smoke test 2026-10-16 (`~/code/.scratch/codex-harness/smoke/`): Codex 0.162.1 on OpenRouter gpt-6-luna ran a failing
  check, made the smallest edit, reran it, and stopped at exit 0; 77 s, ~30k tokens. It loaded the operator's personal
  rules and hooks, hence point 4.
- Not yet shown: a full Waltzman build through the harness, its time against the 150 s first-round target, or that it
  runs on the live server.

## Lesson

When a model must produce something a checker can verify, give the model the checker inside an agent harness. Bare
structured calls are for a single small classification or extraction with no check-and-fix loop.
