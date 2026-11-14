#!/usr/bin/env python3
"""Build the two public demo replays on the generated map from retained evidence runs (no Smallville files, no spend).

Implements: scene-viewer/public-generated-map

`replay-public.json`: the scripted pump run (3 rounds). `replay-resident.json`: the AI-residents run (15 rounds), report words
withheld as for any visitor. Both carry the world's rules for the overlay.
"""
from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/ui/inhabited-facility-20261113"
OUT = ROOT / "viewer/smallville"


def public_bundle(bundle: dict) -> dict:
    from scripts.scene_layout import public_layout
    return {**bundle, "layout": public_layout(bundle["layout"])}


def main() -> int:
    import sys
    sys.path.insert(0, str(ROOT))
    sys.path.insert(0, str(ROOT / "src"))
    from scripts.export_smallville_replay import export_from_rows, withhold_words
    from scripts.open_scene_viewer import pick_run
    from scripts.scaffold_world import validate_bundle
    base = json.loads((ROOT / "examples/world_authoring/pump-facility-v0.json").read_text())
    causal = json.loads((ROOT / "examples/world_authoring/pump-facility-causal-v0.json").read_text())
    for name, log, hide in (("public", "scripted-run-log.jsonl", False), ("resident", "run-log.jsonl", True)):
        rows = [json.loads(line) for line in (EVIDENCE / log).read_text().splitlines() if line.strip()]
        if "bundle" in rows[0]["request"]:  # a resident run: pick its rounds; the saved run predates layouts
            rows[0]["request"]["bundle"] = {**rows[0]["request"]["bundle"], "layout": base["layout"]}
            chain, bundle = pick_run(rows, None)
        else:  # the scripted run's log keeps no bundle; it is the example world
            chain, bundle = rows, base
        replay = export_from_rows(chain, validate_bundle(public_bundle(bundle)), Path("/nonexistent"), causal=causal)
        if hide:
            withhold_words(replay)
        (OUT / f"replay-{name}.json").write_text(json.dumps(replay, separators=(",", ":")))
        print(name, len(chain), "rows,", replay["meta"]["step"], "steps,", len(replay["rounds"]), "rounds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
