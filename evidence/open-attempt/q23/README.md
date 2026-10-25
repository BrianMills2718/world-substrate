# Q23: do generated moves check walls? (2026-10-25)

Description used (the plan's canonical example): "A small airfield office: a brick wall between the office and
the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown."
Model `openrouter/openai/gpt-6-luna`, run with `python -m scripts.generate_world_bundle` then
`python -m scripts.generate_causal_model` (llm_client traces `open-attempt-q23-*`). Total spend under $0.01.

Before the fix (`bundle.json`, `rules.json`): every entity stood at the one world location, there was no move
action, and the wall's `barrier` component was read by no rule. "Sam and the helicopter are in the same place"
was always true.

After the fix (`after-fix/`): places are entities, each thing starts in one, `move` names `to` and `way`, and the
wall carries `passable: false`. Three rule drafts, one per prompt change:

- `rules.json`: move checks the wall, but `fly` never checks Sam is in the hangar.
- `rules2.json`: `fly` fixed; move asks the destination to equal both sides of the wall at once (never passes).
- `rules3.json`: both right. `probe.txt` submits the attempts straight to the engine (a rules probe, not a run):
  walking through the wall fails "the way is passable"; flying from the office fails "the aircraft is where the
  trainee is". With the wall made passable in memory (control), Sam walks to the hangar and flies.

Known limit: checks have no "or", so a way works from its first place to its second only.
