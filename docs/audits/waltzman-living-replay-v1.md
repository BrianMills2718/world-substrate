# Waltzman Living Replay v1 integration evidence

Status: implemented for Company Planning #221.

## Result

`evidence/renders/waltzman-living-v1.html` is the retained flagship branch player. It wraps the generic Living Scene renderer and exposes Baseline / Intervention branch selection plus play, pause, previous, next, and arbitrary canonical-boundary scrub controls. Branch selection swaps retained histories; it never modifies baseline state to manufacture the intervention.

## Exact retained inputs and manifest

`evidence/waltzman/living-replay-manifest-v1.json` pins SHA-256 hashes for the Waltzman Living Scene profile and both retained projection bundles. It records 21 baseline events / 22 frames, 28 intervention events / 29 frames, an exact 21-event common prefix, zero provider spend, and deterministic frame hashes for the initial, meeting-active, blocked, intervention-applied, and ready checkpoints.

The key retained event identities are `e00017` meeting active, `e00021` baseline blocked, `e00022` stabilization applied, and `e00028` recovered ready. Direct reconstruction of every event boundary is compared to sequential frame construction by `scripts/build_waltzman_living_replay.py --check`.

## Browser evidence

The following screenshots are generated from the flagship branch-player HTML itself:

- `evidence/renders/waltzman-living-v1-meeting-desktop.png`
- `evidence/renders/waltzman-living-v1-blocked-desktop.png`
- `evidence/renders/waltzman-living-v1-intervention-desktop.png`
- `evidence/renders/waltzman-living-v1-ready-desktop.png`
- `evidence/renders/waltzman-living-v1-blocked-mobile.png`
- `evidence/renders/waltzman-living-v1-ready-mobile.png`

Desktop evidence uses 1440×1100. Mobile evidence uses 390×900. Mobile geometry comes from generic presentation-only profile overrides; it does not alter world locations or mechanics.

## Legacy boundary

`scripts/render_waltzman_demo.py` remains only as legacy analytical comparison evidence. The Living Scene v1 profile plus generic renderer/branch player are the primary living-world implementation. No graph, Waltzman analysis metric, provider call, or simulation rerun is required to render the retained flagship replay.
