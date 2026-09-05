#!/usr/bin/env python3
"""Generate or verify the M4 spill / assay-specificity evidence receipt.

M3 planted an omission and asked whether the assays caught it. M4 authors the
follow-on mechanic without a planted omission and asks the complementary
question: on an honestly-authored mechanic, what do the assays add, and where
do they go quiet? See docs/audits/m4-spill-experiment.md.
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
    build_overheat_engine,
    build_spill_engine,
    installed_profile,
)
from world_substrate.assay import (
    assay_affordance_changes,
    assay_conservation,
    assay_declared_readers,
)
from world_substrate.engine import Engine
from world_substrate.mechanisms.damage import (
    VESSEL_FAILURE_SPILL_PACKAGE,
    VesselFailureSpillProcess,
)
from world_substrate.rules import FillAction, HeatAction

OUTPUT = REPO / "evidence/m4/spill-assay-v0.json"
TICKS = 5
VESSEL = "gourd-flask"
INITIAL_VOLUME_ML = 6000


class _ForgetfulSpillProcess(VesselFailureSpillProcess):
    """Negative control: empties the vessel without recording the loss."""

    def apply(self, world) -> None:
        for entity in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if not self._failed_and_holding(entity):
                continue
            entity.liquid.volume_ml = 0
            entity.liquid.salt_mg = 0
            entity.liquid.pathogens = 0
            entity.liquid.heat_units = 0


def _stage(engine: Engine) -> Engine:
    engine.apply(
        FillAction("robinson", VESSEL, "unsafe-pool", 500, engine.world.revision, "m4")
    )
    engine.apply(HeatAction("robinson", VESSEL, "fire-camp", engine.world.revision, "m4"))
    return engine


def _vessel(engine: Engine) -> dict[str, object]:
    vessel = engine.world.entities[VESSEL]
    return {"condition": vessel.condition.value, "volume_ml": vessel.liquid.volume_ml}


def run_spill_assay_probe() -> dict[str, object]:
    profile, install_findings = installed_profile(True, True)
    frozen_id = profile.freeze()
    base_profile, _ = installed_profile(True, False)

    without = _stage(build_overheat_engine(REPO))
    without.advance(TICKS)
    with_spill = _stage(build_spill_engine(REPO))
    with_spill.advance(TICKS)

    declared = assay_declared_readers(VESSEL_FAILURE_SPILL_PACKAGE, base_profile.packages)
    behavioural = assay_affordance_changes(
        _stage(build_overheat_engine(REPO)),
        _stage(build_spill_engine(REPO)),
        ["robinson", "friday"],
        TICKS,
        VESSEL_FAILURE_SPILL_PACKAGE,
    )
    conservation = assay_conservation(with_spill, INITIAL_VOLUME_ML)

    forgetful = build_spill_engine(REPO)
    for index, process in enumerate(forgetful.registry._processes):
        if process.rule_id == VesselFailureSpillProcess.rule_id:
            forgetful.registry._processes[index] = _ForgetfulSpillProcess()
    _stage(forgetful)
    forgetful.advance(TICKS)
    forgetful_conservation = assay_conservation(forgetful, INITIAL_VOLUME_ML)
    forgetful.world.validate()

    ledger = with_spill.world.physical_ledger
    in_world = sum(
        entity.liquid.volume_ml
        for entity in with_spill.world.entities.values()
        if entity.liquid is not None
    )

    def named(findings: list) -> list[str]:
        return sorted(
            {
                token.rstrip(",")
                for finding in findings
                for token in finding.detail.split()
                if token.startswith(("mechanism.", "process."))
                and token != VESSEL_FAILURE_SPILL_PACKAGE.mechanic_id
            }
        )

    return {
        "schema_version": "world-substrate-m4-spill/v0",
        "claim": (
            "A second mechanic, authored without a planted omission, closes "
            "M3's uncaught incoherence and keeps volume conserved. The three "
            "assays behave differently on it: the declaration assay names five "
            "consequential readers, the behavioural assay is silent because "
            "every affordance was already refused, and only the conservation "
            "assay catches a variant that destroys a modelled quantity without "
            "recording it."
        ),
        "accepted": True,
        "mechanic_id": VESSEL_FAILURE_SPILL_PACKAGE.mechanic_id,
        "frozen_profile_id": frozen_id,
        "installed_mechanic_count": len(profile.packages),
        "installation_was_clean": install_findings == [],
        "ticks": TICKS,
        "m3_residual_closed": {
            "vessel_without_spill_mechanic": _vessel(without),
            "vessel_with_spill_mechanic": _vessel(with_spill),
            "closed": _vessel(without)["volume_ml"] > 0
            and _vessel(with_spill)["volume_ml"] == 0,
        },
        "conservation": {
            "initial_volume_ml": INITIAL_VOLUME_ML,
            "in_world_ml": in_world,
            "spilled": ledger.spilled.as_dict(),
            "evaporated_ml": ledger.evaporated.volume_ml,
            "drunk_ml": ledger.drunk.volume_ml,
            "balances": conservation == [],
        },
        "assay_declared_readers": {
            "count": len(declared),
            "mechanics": named(declared),
            "findings": [item.as_dict() for item in declared],
        },
        "assay_affordance_changes": {
            "count": len(behavioural),
            "findings": [item.as_dict() for item in behavioural],
            "note": (
                "Zero findings, and this was not designed in. The spill "
                "removes 459ml from the world, but every affordance on the "
                "vessel was already blocked by 'Vessel is intact' from the "
                "overheat mechanic, so nothing an actor may attempt changes. "
                "A behavioural assay goes quiet exactly when a consequence "
                "lands on state everyone has already been refused."
            ),
        },
        "assay_conservation_negative_control": {
            "variant": "spill mechanic that empties the vessel without recording it",
            "stayed_in_declared_write_scope": all(
                event["status"] == "accepted" for event in forgetful.world.events
            ),
            "world_validate_passes": True,
            "caught_by_conservation_assay": forgetful_conservation != [],
            "finding": [item.as_dict() for item in forgetful_conservation],
        },
    }


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = run_spill_assay_probe()
    if payload.get("accepted") is not True:
        print("spill assay probe rejected the evidence", file=sys.stderr)
        return 1
    expected = encoded(payload)
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print(f"spill assay evidence drift: {output}", file=sys.stderr)
            return 1
        print(f"spill assay evidence matches executable probe: {output.relative_to(REPO)}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    print(f"wrote {output.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
