# Physical moves, hand-offs and cash (2026-10-27)

Why: the live pencil build `pencil1` (share `Y-OQRAo16ekn`, 6 AI rounds) stalled: every specialist had a make
step but none could pass its output on, so the mill asked the logger for logs and the lead works asked the miner
for graphite for six rounds and matched no action; only the shop and customer held cash. The #260 airfield build
wrote no same-moment knock-on process because no action could knock, drop or spill anything.

Change: `scripts/generate_world_bundle.py` SIZE_RULES now ask for (1) an action moving each actor's output to the
actor that needs it, with starting cash for buyers; (2) cash whenever selling, buying, paying or prices are implied;
(3) at least one physical move that can upset loose objects, plus fields for where things rest and their state.

Samples after the change (bundle step, then the rules writer on the cafe bundles):

| File | Trace id | Result |
| --- | --- | --- |
| description-bundle-1.json (pencil) | see its log | hand-off moves for every stage; cash on all 8 businesses |
| description-bundle-2.json (pencil) | see its log | carry moves for logs, slats, leads, boxes; no carry-graphite (gap the build's test run flags); cash on all 7 |
| cafe-bundle-1.json | see its log | `knock-stack`; fields upright, on, wet |
| cafe-bundle-2.json | see its log | `drop-cups`; fields upright, on, wet |
| cafe-rules-1.json | model-more/rules/ca3c155b5c62482bb4d62a37c6331606 | no `timing: immediately` process |
| cafe-rules-2.json | model-more/rules/51890883ce30486986083a8e58b352f5 | one `timing: immediately` process: dropped cups wet the floor |

Before the change, the same two descriptions (one sample each) gave a pencil world with no cash and a cafe with
state fields but no move that could upset anything. Reproduce: `uv run --no-project --python 3.12 --with pydantic
--with-editable ~/code2/llm_client python evidence/physical-moves/run_bundle.py . out.json cafe.txt`, then
`run_rules.py . out.json rules.json` (add `--with gdm-concordia==2.4.0`).
