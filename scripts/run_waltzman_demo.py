#!/usr/bin/env python3
"""Execute, verify, retain, and render the Waltzman Coordination Lab demo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.waltzman.adequacy import build_adequacy_report
from reference_worlds.waltzman.analysis import analysis_series
from reference_worlds.waltzman.probe import (
    blocked_event_id,
    event_annotations,
    load_scene,
    run_baseline,
    run_intervention,
)
from scripts.render_waltzman_demo import render_html
from world_substrate.projection import build_live_projection


def build_demo_runs() -> dict[str, dict[str, Any]]:
    baseline = run_baseline()
    intervention = run_intervention(baseline)
    adequacy = build_adequacy_report(baseline.registry)
    scene = load_scene()
    fork_event = blocked_event_id(baseline)
    engines = {"baseline": baseline, "intervention": intervention}
    runs: dict[str, dict[str, Any]] = {}
    for branch, engine in engines.items():
        projection = build_live_projection(
            initial_snapshot=engine.initial_snapshot(),
            events=engine.world.events,
            scene=scene,
            branch_id=branch,
            annotations=event_annotations(engine),
            analysis=analysis_series(engine.initial_snapshot(), engine.world.events),
            adequacy=adequacy,
        )
        projection["verification"] = {
            "exact_replay": engine.replay(),
            "projection_matches_world": projection["projection_final"] == engine.world.material_dict(),
            "canonical_material_hash": engine.world.material_hash(),
        }
        projection["fork"] = (
            {"forked": False, "fork_event_id": fork_event, "shared_event_count": len(baseline.world.events)}
            if branch == "baseline"
            else {
                "forked": True,
                "from_branch": "baseline",
                "fork_event_id": fork_event,
                "shared_event_count": len(baseline.world.events),
            }
        )
        runs[branch] = projection
    return runs


def write_evidence(runs: dict[str, dict[str, Any]]) -> dict[str, str]:
    evidence = REPO / "evidence" / "waltzman"
    renders = REPO / "evidence" / "renders"
    evidence.mkdir(parents=True, exist_ok=True)
    renders.mkdir(parents=True, exist_ok=True)
    paths = {
        "baseline": evidence / "demo-baseline-v0.json",
        "intervention": evidence / "demo-intervention-v0.json",
        "adequacy": evidence / "causal-adequacy-v0.json",
        "html": renders / "waltzman-demo-v0.html",
    }
    paths["baseline"].write_text(json.dumps(runs["baseline"], indent=2) + "\n")
    paths["intervention"].write_text(json.dumps(runs["intervention"], indent=2) + "\n")
    paths["adequacy"].write_text(json.dumps(runs["baseline"]["adequacy"], indent=2) + "\n")
    paths["html"].write_text(render_html(runs))
    return {key: str(path.relative_to(REPO)) for key, path in paths.items()}


def summary(runs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "world-substrate-waltzman-demo-summary/v0",
        "world_id": runs["baseline"]["world_id"],
        "baseline": {
            "events": len(runs["baseline"]["events"]),
            "final_status": runs["baseline"]["projection_final"]["entities"]["coalition-hub"]["components"]["institution"]["status"],
            "replay_ok": runs["baseline"]["verification"]["exact_replay"]["ok"],
            "projection_match": runs["baseline"]["verification"]["projection_matches_world"],
        },
        "intervention": {
            "events": len(runs["intervention"]["events"]),
            "final_status": runs["intervention"]["projection_final"]["entities"]["coalition-hub"]["components"]["institution"]["status"],
            "replay_ok": runs["intervention"]["verification"]["exact_replay"]["ok"],
            "projection_match": runs["intervention"]["verification"]["projection_matches_world"],
        },
        "causal_adequacy": runs["baseline"]["adequacy"]["summary"],
        "fork_event_id": runs["baseline"]["fork"]["fork_event_id"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="execute and verify without writing retained evidence")
    args = parser.parse_args()
    runs = build_demo_runs()
    report = summary(runs)
    if not args.check:
        report["artifacts"] = write_evidence(runs)
    print(json.dumps(report, indent=2, sort_keys=True))
    if (
        report["baseline"]["final_status"] != "blocked"
        or report["intervention"]["final_status"] != "ready"
        or not report["baseline"]["replay_ok"]
        or not report["intervention"]["replay_ok"]
        or not report["baseline"]["projection_match"]
        or not report["intervention"]["projection_match"]
        or report["causal_adequacy"]["gaps"] != 0
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
