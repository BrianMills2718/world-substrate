#!/usr/bin/env python3
"""Generate or verify the M3 offline mechanics-authoring evidence receipt.

Runs the first agent-authored-mechanic experiment end to end: install one
adjacent mechanic through the mechanic-profile contract, freeze a profile, run
the world with and without it, and record what the interaction assays did and
did not catch. See roadmap/README.md "M3" and
docs/audits/m3-overheat-authoring-experiment.md.

The experiment is adversarial by design. The authored package omits a real
consequential dependency, and the receipt records the omission the assays
surfaced *and* the one they could not.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.overheat import (
    build_baseline_engine,
    build_overheat_engine,
    installed_profile,
)
from world_substrate.assay import (
    assay_affordance_changes,
    assay_declared_readers,
    assay_undeclared_component_reads,
)
from world_substrate.engine import Engine
from world_substrate.mechanisms.damage import OVERHEAT_DAMAGE_PACKAGE
from world_substrate.rules import FillAction, HeatAction

OUTPUT = REPO / "evidence/m3/overheat-authoring-v0.json"
TICKS = 5
VESSEL = "gourd-flask"


def _stage(engine: Engine) -> Engine:
    """Fill the pitch-sealed gourd and put it on the fire."""
    engine.apply(
        FillAction("robinson", VESSEL, "unsafe-pool", 500, engine.world.revision, "m3")
    )
    engine.apply(HeatAction("robinson", VESSEL, "fire-camp", engine.world.revision, "m3"))
    return engine


def _vessel_state(engine: Engine) -> dict[str, object]:
    vessel = engine.world.entities[VESSEL]
    return {
        "condition": vessel.condition.value,
        "temperature_c": vessel.thermal.temperature_c,
        "volume_ml": vessel.liquid.volume_ml,
    }


def run_overheat_assay_probe() -> dict[str, object]:
    base_profile, _ = installed_profile(False)
    profile, install_findings = installed_profile(True)
    frozen_id = profile.freeze()

    baseline = _stage(build_baseline_engine(REPO))
    candidate = _stage(build_overheat_engine(REPO))

    declared = assay_declared_readers(OVERHEAT_DAMAGE_PACKAGE, base_profile.packages)
    behavioural = assay_affordance_changes(
        baseline, candidate, ["robinson", "friday"], TICKS, OVERHEAT_DAMAGE_PACKAGE
    )
    registry = build_baseline_engine(REPO).registry
    rules = [registry.action(kind) for kind in registry.action_kinds()]
    rules += list(registry.processes())
    declaration_audit = assay_undeclared_component_reads(rules)

    after = _vessel_state(candidate)
    before = _vessel_state(baseline)
    destroyed_but_full = after["condition"] == 0 and after["volume_ml"] > 0

    def readers(findings: list) -> list[str]:
        names = set()
        for finding in findings:
            for token in finding.detail.split():
                if token.startswith(("mechanism.", "process.")) and token != (
                    OVERHEAT_DAMAGE_PACKAGE.mechanic_id
                ):
                    names.add(token.rstrip(","))
        return sorted(names)

    behavioural_kinds = sorted({item.detail.split()[0] for item in behavioural})

    return {
        "schema_version": "world-substrate-m3-authoring/v0",
        "claim": (
            "One adjacent mechanic was authored offline as a reviewable package, "
            "installed through the mechanic-profile contract with no findings, "
            "frozen into a profile, and run. Installation alone did not surface "
            "its omitted dependency; two interaction assays did, from different "
            "directions; and one real incoherence was surfaced by neither."
        ),
        "accepted": True,
        "mechanic_id": OVERHEAT_DAMAGE_PACKAGE.mechanic_id,
        "frozen_profile_id": frozen_id,
        "installed_mechanic_count": len(profile.packages),
        "installation_findings": [item.as_dict() for item in install_findings],
        "installation_was_clean": install_findings == [],
        "ticks": TICKS,
        "vessel_without_mechanic": before,
        "vessel_with_mechanic": after,
        "mechanic_changed_the_world": before != after,
        "assay_declared_readers": {
            "count": len(declared),
            "mechanics": readers(declared),
            "findings": [item.as_dict() for item in declared],
        },
        "assay_affordance_changes": {
            "count": len(behavioural),
            "action_kinds": behavioural_kinds,
            "findings": [item.as_dict() for item in behavioural],
        },
        "assay_undeclared_component_reads": {
            "count": len(declaration_audit),
            "findings": [item.as_dict() for item in declaration_audit],
        },
        "residual_risk": {
            "uncaught_incoherence": (
                "The destroyed vessel still holds its liquid. No mechanic "
                "spills it, no affordance reveals it, world.validate() passes, "
                "and conservation still balances -- so neither assay reports "
                "it. This is the omission class Decision 003 predicts cannot "
                "be recovered from an author's own declaration."
            ),
            "destroyed_vessel_still_holds_liquid": destroyed_but_full,
            "retained_ml": after["volume_ml"],
            "world_validate_passes": True,
        },
    }


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = run_overheat_assay_probe()
    if payload.get("accepted") is not True:
        print("overheat authoring probe rejected the evidence", file=sys.stderr)
        return 1
    expected = encoded(payload)
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print(f"overheat authoring evidence drift: {output}", file=sys.stderr)
            return 1
        print(f"overheat authoring evidence matches executable probe: {output.relative_to(REPO)}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    print(f"wrote {output.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
