---
role: contract
status: implemented
reviewed_through: 2026-09-08
---

# CVS Situation IR structural import v0

`cvs-situation-import/v0` is a **bounded adapter** from the declared Situation IR used by `BrianMills2718/compositional-viable-systems` into `world-substrate-authoring-bundle/v0`.

It exists to exercise one real analytical-to-simulation seam. It is not a universal architecture IR, a CVS runtime dependency, or a license to infer simulation law from an architecture description.

## Implemented path

```text
CVS Situation IR
  role / pool / capability / action / protected-reserve rule / scenario
        |
        | scripts/import_cvs_situation.py
        v
world-substrate-authoring-bundle/v0
  represented entities + typed components + action signatures
        |
        v
ordinary World Substrate causal-authoring/review path
```

The adapter currently supports only the constructs exercised by the pinned two-depot sustainment fixture:

- entity kinds `role`, `pool`, `capability`, and `action`;
- action kind `transfer`;
- rule kind `protected_reserve`;
- one explicitly selected scenario at a time;
- explicit capability activation supplied by the caller.

Unknown relations, measures, entity kinds, action kinds, rule kinds, scenarios, references, or capability IDs fail visibly. Expand the adapter only when an authentic new consumer case needs another distinction.

## Identity

CVS source IDs such as `regional_hq` and `stock_a` are **not rewritten as if they were World Substrate canonical IDs**. World Substrate retains its local slug invariant (`regional-hq`, `stock-a`) and every imported entity carries:

```json
{
  "external_identity": {
    "system": "compositional-viable-systems",
    "identifier": "regional_hq"
  }
}
```

That explicit mapping is the seam. A downstream view may display either identifier, but identity equivalence must be traceable through the mapping rather than inferred from labels.

## Structural meaning retained

The projection preserves enough represented structure for a scenario model to be authored and reviewed:

- decider role and scenario/regime context;
- resource-pool supply, demand, unit, and protected-reserve quantity;
- capability identity, kind, cost, optional target/overridden rule, amount, and caller-selected enabled state;
- directional action-template identity, source, target, maximum amount, and required CVS capability IDs;
- protected-reserve rule identity, quantity, scope IDs, and waiver regimes;
- source evidence-reference IDs.

The two directional CVS transfer templates are represented as entities while the World Substrate action **signature** is deduplicated to one `transfer(source_ref, target_ref, amount)` kind. Direction-specific limits and requirements remain represented on the template entities for later mechanic review.

## Causal boundary

The adapter does **not** determine what transfer actually does, whether an actor may invoke it, how reserve waiver changes applicability, how demand is served, or what outcome is successful. Those are causal/modeling decisions.

A generated package therefore follows the normal World Substrate safety behavior: action-signature stubs refuse until mechanics are separately implemented or proposed through the constrained causal model, locally compiled, reviewed, explicitly approved, and installed.

CVS analysis can propose a structural intervention such as enabling observation, transfer authority, and reserve override. The adapter may represent those flags in a candidate world variant. That representation is a hypothesis/input to simulation, not proof that the intervention is correct or that its simulated result will occur in reality.

## Pinned integration evidence

The test fixture is copied verbatim from:

- repository: `BrianMills2718/compositional-viable-systems`;
- revision: `5cb9933f2551ca3e0e75590814f7e686f50d8edb`;
- path: `applications/sustainment/sustainment_situation_ir.json`;
- SHA-256: `e357e25db6c4c7979e1f235fba1fceeb61b36e1c1448816845973bca3a68894b`.

That donor fixture explicitly labels itself synthetic. Tests here therefore prove contract behavior and identity/structure preservation only; they do not establish real DoD facts or policy validity.
