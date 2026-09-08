# CVS sustainment integration world

This is a bounded World Substrate consumer path for the synthetic two-depot Situation IR in `BrianMills2718/compositional-viable-systems`.

It is intentionally split into two authorities:

1. `scripts/import_cvs_situation.py` projects represented CVS structure into `world-substrate-authoring-bundle/v0`.
2. `simulate.py` installs one reviewed transfer mechanic and executes **an externally selected action** through the ordinary World Substrate Engine.

World Substrate does not repeat CVS repair search. CVS answers which structural capability set is sufficient/cheapest within its model; this reference world asks what a supplied transfer does under the installed scenario mechanics.

The v0 model implements transfer consequences plus reserve/override outcome evaluation. It deliberately does not model policy action selection, actor observation restrictions, or capacity-capability effects. Those omissions are returned in every simulation result rather than silently approximated.

Example from repository root:

```bash
PYTHONPATH=src:. python -m reference_worlds.cvs_sustainment.simulate \
  tests/fixtures/cvs/sustainment_situation_ir.json \
  --scenario sc_1 \
  --enable-capability cap_observe_distribution \
  --enable-capability cap_transfer_authority \
  --enable-capability cap_override_reserve \
  --source stock_a --target stock_b --amount 2
```

The fixture is synthetic. This proves an integration and causal-execution seam, not a real DoD conclusion.
