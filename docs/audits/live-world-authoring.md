---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Live mechanics generation and fresh-run audit

## Question

Can the visual world-authoring surface move from represented structure to a
fresh, graphical simulation without either (a) downloading/scaffolding by hand
or (b) letting model prose become executable world law?

## Implemented vertical

The live path is now:

```text
authoring bundle
  -> bounded mechanics proposal
  -> local causal compiler
  -> compiler-derived authority review
  -> explicit human approval
  -> frozen mechanic profile
  -> fresh scripted or LLM-selected run
  -> retained v3 trace
  -> generic graphical replay
```

The authoring bundle remains structural. Causal mechanics live in a separate
`world-substrate-causal-model/v0` declaration. The model cannot submit source
code or its own read/write scope. The compiler derives authority and refuses
unsupported state paths, unconstrained selectors, type-incoherent checks,
component access unsupported by the participant selector, and engine-owned
causal metadata writes.

## Orchard acceptance fixture

`examples/world_authoring/orchard-v0.json` is paired with
`examples/world_authoring/orchard-causal-v0.json` for deterministic acceptance.
A worker may pick a represented ripe apple. The hand declaration checks the
fruit's stage, co-location, and shared-store ownership; the accepted action
transfers ownership and records a represented picked stage. Its terminal is
derived from all represented fruit reaching that stage.

A zero-spend scripted fresh run completed in one accepted action and rendered a
standalone graphical replay. The causal-to-presentation seam also derives a
visual take/attach projection from the explicit ownership effect, so the apple
visibly follows the worker without any `pick`-specific renderer branch.

## Real model probes

Two live Luna probes were run under explicit user authority and hard per-trace
caps.

**Mechanics proposal.** `openrouter/openai/gpt-5.6-luna` proposed the Orchard
`pick` mechanic. The first ordinary-text draft used an abbreviated state path;
the compiler refused it. One compiler-guided repair produced a valid declaration
with a conservative ownership-transfer effect and no invented terminal. The two
proposal calls on the successful trace cost **$0.00156146** total. The compiler
review derived the only material write as fruit ownership plus engine-owned cause
attribution.

**Live action selection.** With the reviewed Orchard fixture mechanic installed,
Luna selected from the engine's one offered action and chose `pick apple-1`,
reasoning that the apple was ripe and available. The action committed through
`Engine.submit`, the world terminal was reached in one turn, and observed model
cost was **$0.0001138**.

The generated-mechanics probe is intentionally not presented as proof of causal
completeness. Its conservative choice to omit an unrepresented completion state
is evidence that the system can leave questions unresolved rather than forcing a
demo-friendly law.

## Public service boundary

`scripts/world_builder_service.py` exposes the deployed same-origin API. It:

- binds to loopback only;
- accepts bounded JSON bodies;
- requires browser same-origin on public POSTs;
- rate-limits general and LLM requests;
- serializes LLM requests;
- imposes per-request mechanics/run caps and a **$0.50/day** World Builder LLM
  ceiling, reducing the final request cap to the exact remaining allowance;
- requires explicit mechanics approval before `/run`;
- compiles the causal model before any live policy call;
- returns the fresh trace and graphical replay rather than granting the browser
  direct mutation authority.

Scripted runs cost zero. LLM policies select only engine-minted action ids; the
installed mechanics remain the sole source of consequences.

## Remaining limitation

The action declaration language is intentionally narrower than arbitrary causal
programming. Complex continuous physics, stochastic models, list mutation,
multi-step processes, institutions, and interactions that cannot be expressed
as the current finite action language still need a reviewed extension or
hand-written mechanic. A model generation failure is therefore a request for
review/extension, not permission to execute arbitrary code.
