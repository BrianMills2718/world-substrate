---
role: living-feedback-log
status: active
reviewed_through: 2026-10-05
---

# World Builder visual and usability feedback

Living record of critiques of World Builder pages. Owner critiques become rules here; rules that apply beyond this project are promoted to Representation Router heuristics (named in the right-hand column).

## Rules

| Rule | Source (exact words, date) | Where it is enforced | Router heuristic |
| --- | --- | --- | --- |
| The Builder opens on a landing page with a short tutorial, not the form editor. | Brian, 2026-10-05: "it should open on a landing page with a tutorial." | `scripts/world_builder_home.html` (published as `/world-builder/`); `tests/test_world_builder_home.py` | `describe-first-creation-surface` (representation-router #65) |
| Building is done through natural language; the form editor is an advanced route. | Brian, 2026-10-05: "the build thing i would have no idea how to do. building should be done through natural language" | `/generate-world`; landing page links `build/` as "Advanced editor" | `describe-first-creation-surface` |
| A failed build says what went wrong and what to try. | Cold first-visit review, 2026-10-05 | `plainError` in the landing page | existing: `every-label-explains-itself` |
| Parts of a description the simulator cannot represent are listed, not dropped silently. | Cold first-visit review, 2026-10-05 ("before noon" disappeared) | `not_modeled` from `scripts/generate_world_bundle.py` | none (project-specific) |
| A run shows what the rules refused and why, grouped one square per person per round. | Cold first-visit review, 2026-10-05 (headline promised refusals; none visible); 39 squares judged noisy | `blocked_by_rules` in `scripts/run_authored_world.py`; landing page strip | existing: `density-budget`, `every-mark-opens-its-subject` |
| Rule checks read as plain English with the things' names, never jargon. | Cold first-visit review, 2026-10-05 ("ownership context", "Actor is available") | label rule in `scripts/generate_causal_model.py` | existing: `every-label-explains-itself` |
| Every secondary page links back to the landing page. | Cold first-visit review, 2026-10-05 | home links in Play and the advanced editor | existing: `navigation-holds-only-live-views` |
| Never red against green; allowed is solid blue, refused is orange dashed with a word. | Brian's standing preference (red-green colorblind) | landing page palette; `tests/test_world_builder_home.py` | existing |

## Log

- 2026-10-05: Brian asked for a landing page with a tutorial and natural-language building. Built and deployed (world-substrate #92, machine-coordination #84). A cold first-visit review found five problems; fixed in #93–#95 and machine-coordination #85.
