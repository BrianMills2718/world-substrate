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
| Offer "I'm feeling lucky" (one click to a surprise world, built and run) and a dialogue where the AI helps flesh out and clarify the idea. | Brian, 2026-10-05: "there should be an \"im feeling lucky\" option as well as a dialogue option where the ai helps flesh out and clarify" | `/surprise`, `/clarify` (`scripts/world_dialogue.py`); landing page buttons | `describe-first-creation-surface` (extend) |
| Worlds are continuous, not only tasks: offer a task world, an open world, and the in-between (ongoing work); open and ongoing worlds keep going. | Brian, 2026-10-05: "it is stopping in the world i built at least in 4 turns and my conception is that this is like continuous worlds we should be building. i guess that should be one of the choices. like a do a task world. or an open world and i dont know what is in between" | kind choice on the landing page; `processes` in the rule language; Keep going via `continue_from` | none yet (project-specific) |
| The owner can always override the budget with a password. | Brian, 2026-10-05: "i always want to be able to put in a password to override the budget" | `X-World-Builder-Owner` + `WORLD_BUILDER_OWNER_PASSWORD`; separate owner ledger ($5/day); Owner access link on the landing page | none (project-specific) |
| Every control always has a tooltip, and choices that look alike say plainly how they differ. | Brian, 2026-10-06: "we should always have tool tips. i dont know the difference between build my world, and describe my world" | `title` on every button, link, text box, choice card and runtime chip; long press shows it on phones; visible one-line meanings under Build it now / Talk it through first / Surprise me; `test_every_control_has_a_tooltip` | existing, was broken here: `every-label-explains-itself` |
| Every secondary page links back to the landing page. | Cold first-visit review, 2026-10-05 | home links in Play and the advanced editor | existing: `navigation-holds-only-live-views` |
| Never red against green; allowed is solid blue, refused is orange dashed with a word. | Brian's standing preference (red-green colorblind) | landing page palette; `tests/test_world_builder_home.py` | existing |

## Log

- 2026-10-05: Brian asked for a landing page with a tutorial and natural-language building. Built and deployed (world-substrate #92, machine-coordination #84). A cold first-visit review found five problems; fixed in #93–#95 and machine-coordination #85.
- 2026-10-05: Brian asked for an "I'm feeling lucky" option and a clarifying dialogue. Built (this PR). He also asked for continuous worlds: "my conception is that this is like continuous worlds we should be building ... a do a task world. or an open world and i dont know what is in between". Next increment.
- 2026-10-06: Brian could not tell "Build my world" from "Help me describe it" and asked for tooltips everywhere. The router heuristic `every-label-explains-itself` already required this and the page broke it. Renamed to Build it now / Talk it through first / Surprise me with visible one-line meanings; tooltips on every control, enforced by a test.
- 2026-10-06: Brian still did not see tooltips ("i still dont see the tool tips i have asked for multiple times and should be a policy default for any ui"). Native `title` tooltips appear only after a long still hover and never on phones, so they did not count. Replaced with a styled bubble shown within 150 ms of hover or keyboard focus for every control, ⓘ buttons beside the three start buttons (tap on phones), long press anywhere; `scripts/e2e/world_builder_e2e.mjs tooltips` hovers every visible control in a real browser and fails if any shows no bubble. A page-script syntax test was added after a name collision broke every handler on the page during this change.
- 2026-10-06: Brian still could not tell "Build it now" from "Surprise me". The names did not say who writes the story, and an empty box silently built the grey example text, which looked like a surprise too. Renamed Build what I wrote / Help me write it / Make one up for me, with lines saying "you write the story" vs "the AI writes the story (the box is ignored)"; Build what I wrote is disabled until the box has text.
