# Source dispositions

This page prevents related projects from becoming competing authorities. Exact revisions and hashes are recorded in [the source manifest](../references/sources.json).

| Source | What it contributes | Disposition | Adoption proof required | Authority limit |
| --- | --- | --- | --- | --- |
| Castaway `world-systems` | Deterministic engine behavior, physical rules, discovery, persistence, replay, browser evidence, reviewed linguistic subset | **Extract** the freshwater vertical first | Same semantic trace and replay through World Substrate contracts, with donor behavior retained | The bounded fill-through-drink consumer path is adopted here; donor remains authority for whole-vessel transfer and the complete trace |
| Castaway `main` | Earlier survival world, needs/weather/fire/spoilage/regrowth, genuine agent trace | **Retain as historical reference** | None until a later mechanism selects it | Not current substrate architecture |
| Cybernetic Influence V3 | Conversational authoring, canonical-world component, semantic intents, transition contracts, patch validation, evidence projections, Concordia integration | **Reuse selectively** through named seams | A World Substrate consumer runs the reused seam without importing a second state/time authority | Its socio-technical product goal and LLM/coarse transition policy are not inherited |
| Linguistic Core in `onto-canon6` | Predicates, roles, entity types, hierarchy, source-native semantic provenance | **Pinned dependency** for vocabulary | Reproducible extraction, semantic review, source hashes | Vocabulary never creates mechanics; uncommitted donor changes are excluded |
| Dynamical Laboratory specification | Trajectories, perturbations, representations, recurrence, coarse-graining, experimental ladder | **Research input** | A later evaluation uses a named method and reports its limits | Not the runtime architecture or current implementation plan |
| Dwarf Fortress research report | Design lessons about categories, materials, reactions, shared objects, ongoing processes, persistence, scale | **Research input** | Claims used in design remain traceable to the preserved report and reviewed summary | Not executable code and not proof of a universal ontology |
| Shared `llm_client` | Authenticated model invocation, route/accounting evidence | **Runtime dependency** when policy integration begins | One traced consumer call through the canonical client | No provider client in the engine; current dirty worktree is not vendored |
| Project Meta documentation/context policies | Progressive disclosure, one-copy authority, root/subtree instruction surfaces, OKF-style navigation | **Governance dependency** | Repository navigation and structural checks | Does not define simulation behavior |

## Why this is not a monorepo import

The related repositories have independent goals and active histories. Bulk copying would create stale duplicates and ambiguous authority. This project owns the shared substrate contract and migrates capabilities only when an active slice has a consumer and an adoption test.

The bounded fill-through-drink consumer path is retained in
[first-fill](../evidence/m1/first-fill-v0.json) and
[boiling](../evidence/m1/boiling-v0.json),
[pour](../evidence/m1/pour-v0.json), and
[drink](../evidence/m1/drink-v0.json) evidence. Those receipts do not adopt
Castaway take/give behavior or the full scenario trace.

## Current-source cautions

- `castaway-world-systems` is a branch worktree of the original Castaway Git repository and has no configured remote.
- The inspected `onto-canon6` and shared `llm_client` worktrees contain unrelated uncommitted changes. Only their committed revision or an exact content-hashed artifact may be used.
- Cybernetic Influence V3's archived topological-world Slice 8 is historical evidence. Its current goal, roadmap, ADRs, plans, and `general_simulation` implementation are the relevant sources.
- Local paths are conveniences. Revisions and hashes, not machine paths, identify source content.
