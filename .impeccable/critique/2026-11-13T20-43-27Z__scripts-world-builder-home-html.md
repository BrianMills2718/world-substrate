---
target: World Builder saved-run viewer
total_score: 12
max_score: 32
na_heuristics: 5,9
p0_count: 0
p1_count: 5
target_identity: "file:/home/brian/code2/worktrees/ws-viewer-usability-review/scripts/world_builder_home.html"
target_fingerprint: "sha256:422acd911801664c7f8a3658fc41ed150c01f7aeb91cd3221e0e7cdf9190ff9a"
target_path: /home/brian/code2/worktrees/ws-viewer-usability-review/scripts/world_builder_home.html
timestamp: 2026-11-13T20-43-27Z
slug: scripts-world-builder-home-html
---
# World Builder saved-run viewer: usability and Astryx assessment

Source: Brian, 2026-11-13: “the ui is bascially unusuable”; request to assess the linked Reddit item. Review of deployed viewer f43846f, using retained recording T-e9dYLdIi61. Independent design and mechanical/browser assessments completed before synthesis. This is a diagnosis and proposed direction, not an adopted redesign or implementation claim.

The previous 78 local/77 live checks establish the bounded attempt inspector behavior. They do not establish that the whole run can be understood or investigated. This review finds that the primary viewing journey fails despite the controls working.

[Retained evidence](../../evidence/ui/usability-review-20261113/) contains the reports, screenshots, geometry and pinned primary-source receipt named below.

## Verdict and priorities

The interface groups implementation outputs into a long column: Picture, Network, causal receipts, refusal squares and actor-input JSON. It asks the reader to reconstruct the connection between them. The scene's overlapping labels obstruct the most prominent output. Proposed repair order:

1. Make the recording understandable before playback: scenario, people, initial situation, outcome of interest and truthful recorded-run status. Offer visible previous/next/direct round selection. Start a saved recording paused. Keep the existing one-box creation flow separate and preserve its approved behavior.
2. Use one selected round and event across the event list, before/after world state, rule/refusal/knock-on explanation and actor information. Opening a historical event must select its historical state. A selected attempt opens original words, interpreted fields and recorded result in context; the full trace and whole-world graph stay available as deeper inspection.
3. Compose a readable phone view explicitly. Show one useful region at a time with reachable round navigation and contextual details. Replace the overlapping generic stage in this nonspatial example; retain spatial representations where location explains the event. This exchanges ambient animation for readable inspection, while preserving the complete world model on demand.

Proposed critical task: open the recording; identify what situation is being simulated; select Bo's first attempt; explain the original words, interpretation and actual assent change; open Ari's round-3 validation consequence and see round-3 state; inspect the actor's supplied information for that choice without losing event context. No new model call or simulation is needed. Technical execution and Brian's understanding must be checked separately.

## What the browser shows

| Observation | Consequence for the task | Evidence |
| --- | --- | --- |
| A saved replay opens under the creation pitch and advances while the reader is orienting. No visible direct round selector; embedded step controls are hidden in driven mode. | Returning to a specific round requires replay timing. | desktop-before.png; design-assessment.txt; browser-assessment.txt |
| Thought cards, round badge, object labels and action caption overlap at desktop width. On phone, a 298×167.6px stage clips cards 205–220px tall. | The primary output is physically unreadable. | desktop-before.png; mobile-before.png; browser geometry JSON |
| The useful inspector is beneath Picture and a large graph, inside “Why things were refused”; Actor view replaces the world context with collapsed exact-input records. | Understanding an accepted action or what its actor received requires finding and remembering separate views. | actor-context-before.png; design-assessment.txt |
| Expanding round 3's causal receipt leaves the picture/network at round 6. | Historical evidence is presented beside a different current state; selecting history does not establish matching context. | historical-selection-before.png; design-assessment.txt |

These are interface observations. Predicted confusion is evaluator judgment. Brian's explicit unusability report is the human feedback; no comprehension success rate was measured.

## Does the linked library help?

The matching video names Meta Astryx. The official repository verifies a Beta React 19+ design system with components, templates, CLI/MCP documentation and one packaged skill. The “100-file skill library” description is not a verified count of independent skills. Reddit did not expose its outbound video URL to the available reader; attribution to the matching video is an inference, while the official Astryx source is directly verified.

Read-only primary-source receipt: astryx-sources.json, revision96ea82334e9eb26eb217145421cfa3dc037f3efb. No dependency or skill was installed.

- [Scaffold](https://github.com/meta/astryx/blob/96ea82334e9eb26eb217145421cfa3dc037f3efb/packages/cli/assets/docs/tree/scaffold.doc.mjs): define the page's regions and width budget before assembling components.
- [Structure](https://github.com/meta/astryx/blob/96ea82334e9eb26eb217145421cfa3dc037f3efb/packages/cli/assets/docs/tree/structure.doc.mjs): one lead/action per region and coherent row collections.
- [Side panels](https://github.com/meta/astryx/blob/96ea82334e9eb26eb217145421cfa3dc037f3efb/packages/cli/assets/docs/tree/side-panels.doc.mjs): selection opens relevant detail while preserving list context.
- [Responsive composition](https://github.com/meta/astryx/blob/96ea82334e9eb26eb217145421cfa3dc037f3efb/packages/cli/assets/docs/tree/responsive.doc.mjs): explicitly adapt which regions are visible at narrow widths.

Recommendation: compose this structural guidance with the existing UX comprehension, representation-router and UI workflows. Astryx components are a candidate for a bounded viewer rebuild, with a React 19 migration as the concrete tradeoff for the vanilla outer viewer. Selected patterns can be applied without that migration. Choose components after a reviewable layout uses the actual retained data and preserves all current inspection capabilities. More skill files alone do not settle the interaction design.

## Design judgment

Design specificity: simulation-specific content, but no coherent primary inspection journey. Preserve honest replay status, actual before/after values, exact actor inputs and focused subsets of the full world graph.

| Nielsen heuristic | Expert rating, 4 best |
| --- | --- |
| Status visibility | 2 |
| Match to familiar language | 2 |
| Control and freedom | 1 |
| Consistency | 2 |
| Error prevention | N/A: read-only path |
| Recognition over recall | 1 |
| Flexibility and efficiency | 1 |
| Minimalist design | 1 |
| Error recovery | N/A: not exercised |
| Help | 2 |
| Total | 12/32; expert judgment only |

First-time readers lack scenario orientation; repeat investigators cannot directly seek a round; mobile readers encounter clipped content. Working-memory load is high because event, state and actor-input contexts are separated. The predicted emotional journey is curiosity, confusion during motion, effort to pause, and frustration while reconnecting evidence; it is not a measured participant trajectory. Duplicate “More” labels and native selectors are secondary to these failures.

## Mechanical evidence and limits

Detector: one execution, exit2, three findings. Two are false positives in this replay context: hidden-stage headings and purposeful held-state stripes. A border/shadow advisory is minor. Browser screenshots and measured geometry establish the serious findings; a detector score does not establish usability.

Fresh desktop 1440×1000 and phone 390×844 captures; only recorded GETs, no paid calls or new runs. No JS page errors; analytics POSTs deliberately blocked. Two overlay preflights succeeded, but both detector injections were blocked by Chromium local-network/CORS policy. No user-visible overlay was produced; temporary server stopped, exit0. Keyboard/screen-reader conformance, broader run shapes and human comprehension remain unverified.

Router recommendations and honest dispositions are retained with the evidence. Timeline was selected for direct temporal access, local state transition for action/effect and master-detail for actor input. Unrelated chat/training defaults were marked inapplicable. The ratings and checklist counts are diagnostic accounting, not release thresholds or new acceptance requirements.

Questions skipped: the current request can be assessed from existing intent, the rendered recording and primary sources; no missing human preference blocks this recommendation.
