---
description: World Substrate owns only the governed-rules layer; minds and schedulers run on commodity runtimes.
---

# Decision 006: World Substrate is the governed-rules layer, hosted on commodity runtimes

Governs: RULE-DERIVED-AUTHORITY, src/world_substrate/action_authoring.py

**Status:** accepted
**Date:** 2026-10-05
**Decided by:** Brian (approved the recommended option in session, 2026-10-05: "i approve")
**Related:** [Decision 004](004-product-and-adoption-strategy.md), [Decision 005](005-native-waltzman-delivery.md), [roadmap replacement-first gate disposition](../../roadmap/README.md#replacement-first-gate-disposition-recorded-2026-10-05)

## Context

Brian's 2026-10-01 workspace rule presumes that building ourselves is bad when something off the shelf already does the job. The replacement-first gate (`spikes/replacement-2026-10/`) ran World Substrate's governed-rules layer on Concordia, Mesa and a PDDL toolchain. Each could host or check the layer, and none could replace it. Rewriting the rules inside Concordia or Mesa lost atomic commit/refusal, declared write scopes, recorded cause, compiler-checkable rules and replay. The PDDL tooling could not express information visibility, write scopes or causal records.

Brian was offered three options: keep a narrow rules layer, freeze, or keep building native. He approved the narrow rules layer.

## Decision

1. World Substrate's product is the **governed-rules layer**: rules as data -> compiler-derived authority -> explicit human approval -> atomic commit/refusal with recorded cause, plus the authoring/review path that produces those rules.
2. World Substrate adds **no engine, scheduler, renderer or resident-cognition capability of its own**. When a world first needs one:
   - LLM residents run on Concordia, with the Engine as sole consequence authority (spike: identical world state);
   - grids/networks, stochastic activation or parameter sweeps run on Mesa over the Engine;
   - formal validation and reachability checks use a PDDL export.
3. Existing native pieces (integer-tick Engine loop, Living Scene renderer, Automatic replay) stay and are maintained while they serve current worlds. They are not extended.
4. The public World Builder is kept and its generate/run backend is restored on the personal VPS. Restoring it is not new capability; it brings back what was already built.

This narrows Decision 005. Native convergence produced the coordination vertical (#75/#79/#80) and stops there. Decision 004's "own reality; borrow minds" stands.

## Wrong when

- The first LLM-resident run hosted on Concordia needs a game-master component that writes state outside `Engine.submit`, or more glue than the `CognitionAdapter` path.
- A Concordia, Mesa or other runtime release ships transactional state with write scopes and per-change history. Re-run the gate; adopting it may then remove the native Engine.
- The PDDL translator needs hand edits for a second world, or the PDDL validator and `engine.submit` disagree on any step of a recorded run.
- A concrete world needs a capability that none of the three can host without the Engine losing consequence authority. Then a bounded native extension is justified, and the gap must be named.
