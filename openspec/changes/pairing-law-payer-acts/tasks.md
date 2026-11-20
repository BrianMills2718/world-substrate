# Tasks

- [ ] Tests first, in `tests/test_declared_laws.py` (fail before the change; reuse its `SHOP` bundle and `broken()` helper):
  - `@pytest.mark.req("world-authoring-bundle/a-seller-started-sale-is-refused")`: `SHOP`'s `sell-pencil` law has
    `pays.from: customer`, so `pairing_starter_problems(validate_bundle(SHOP))` returns one sentence naming `a-sale-is-paid`.
  - `@pytest.mark.req("world-authoring-bundle/a-buyer-started-purchase-is-accepted")`: a copy with the law's
    `gives`/`pays` ends swapped to the actor paying returns `[]`.
  - `@pytest.mark.req("world-authoring-bundle/saved-worlds-still-load")`: `validate_bundle` on `pencil-s3-kept.json`'s bundle does not raise.
  - `@pytest.mark.req("world-authoring-bundle/a-seller-started-sale-is-refused")`: a `generate_world_bundle` call
    with `call_llm` patched to return the seller-started bundle first and the fixed one second is retried once and
    returns the fixed one (look at how other tests patch `call_llm` there; no real call).
  - `@pytest.mark.req("causal-model-authoring/the-rules-writer-is-told-who-acts-in-a-trade")`: `_context(validate_bundle(SHOP))["authority_rules"]` has an entry containing "actor selector" and "pays".
- [ ] `scripts/scaffold_world.py`: add `pairing_starter_problems(bundle) -> list[str]`; do not call it from `validate_bundle`.
- [ ] `scripts/generate_world_bundle.py`: after `validate_bundle(parsed)` raise `BundleError("; ".join(problems))` when
  non-empty (the existing except/repair loop reports it); add to the `laws` contract text: "in a pairing law the one
  who pays is `actor`; a sale the seller starts is written as the buyer's `buy-...` move".
- [ ] `scripts/generate_causal_model.py`: add the `authority_rules` sentence next to the #259 price rule.
- [ ] Check: `uv run pytest tests/test_declared_laws.py tests/test_laws.py tests/test_people_laws.py -q`, then
  `python scripts/check_project.py`; `openspec validate pairing-law-payer-acts --strict`. No lockstep.yaml change:
  only ungoverned `scripts/` and `tests/` files change; archiving updates existing spec rows.
- [ ] Archive: `openspec archive pairing-law-payer-acts --yes`; replace any placeholder Purpose; commit `(Fixes #282)`.
