#!/usr/bin/env python3
"""Run the complete deterministic native-coordination acceptance matrix."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.run_native_coordination import (
    DEFAULT_ACCEPTANCE,
    DEFAULT_CAUSAL,
    load_acceptance,
    run_diagnostic,
)
from scripts.scaffold_world import load_bundle

MATRIX_SUMMARY_SCHEMA = "world-substrate-native-coordination-matrix-summary/v0"


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    )


def run_matrix(
    *,
    output_root: Path,
    acceptance_path: Path = DEFAULT_ACCEPTANCE,
    causal_path: Path = DEFAULT_CAUSAL,
    run_id_prefix: str = "native-coordination-matrix",
) -> dict[str, Any]:
    acceptance = load_acceptance(acceptance_path)
    causal_value = json.loads(causal_path.read_text())
    output_root.mkdir(parents=True, exist_ok=True)

    worlds: dict[str, Any] = {}
    profile_ids: dict[str, str | None] = {}
    for world_id, row in sorted(acceptance["worlds"].items()):
        bundle_ref = row.get("bundle")
        if not isinstance(bundle_ref, str) or not bundle_ref:
            raise ValueError(f"acceptance world {world_id!r} must name bundle")
        bundle = load_bundle(REPO / bundle_ref)
        if bundle["world"]["id"] != world_id:
            raise ValueError(
                f"acceptance world {world_id!r} points to bundle "
                f"{bundle['world']['id']!r}"
            )
        summary = run_diagnostic(
            bundle,
            causal_value,
            acceptance=acceptance,
            output_dir=output_root / world_id,
            run_id=f"{run_id_prefix}/{world_id}",
        )
        worlds[world_id] = summary
        profile_ids[world_id] = summary.get("mechanic_profile_id")

    nonempty_profiles = {
        value for value in profile_ids.values()
        if isinstance(value, str) and value
    }
    shared_profile = (
        len(nonempty_profiles) == 1
        and len(nonempty_profiles) == len(set(profile_ids.values()))
        and all(profile_ids.values())
    )
    # The expression above deliberately requires every world to report a
    # concrete profile id; a failed world cannot pass the shared-mechanics gate
    # merely because the other world has one valid id.
    shared_profile = bool(
        len(nonempty_profiles) == 1
        and all(isinstance(value, str) and value for value in profile_ids.values())
    )
    all_worlds_passed = all(
        summary.get("status") == "passed" for summary in worlds.values()
    )
    result = {
        "schema_version": MATRIX_SUMMARY_SCHEMA,
        "status": "passed" if all_worlds_passed and shared_profile else "failed",
        "worlds": worlds,
        "shared_mechanic_profile": {
            "passed": shared_profile,
            "profile_ids": profile_ids,
            "profile_id": next(iter(nonempty_profiles)) if shared_profile else None,
        },
        "all_worlds_passed": all_worlds_passed,
    }
    _write_json(output_root / "matrix-summary.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--acceptance", type=Path, default=DEFAULT_ACCEPTANCE)
    parser.add_argument("--causal-model", type=Path, default=DEFAULT_CAUSAL)
    parser.add_argument("--run-id-prefix", default="native-coordination-matrix")
    args = parser.parse_args()
    summary = run_matrix(
        output_root=args.output_root,
        acceptance_path=args.acceptance,
        causal_path=args.causal_model,
        run_id_prefix=args.run_id_prefix,
    )
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["status"] == "passed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
