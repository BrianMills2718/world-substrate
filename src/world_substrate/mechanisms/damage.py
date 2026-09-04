"""Overheat damage: an adjacent mechanic authored offline for the M3 experiment.

Authored against docs/contracts/mechanic-profile-v0.md as a reviewable package
plus its executable rule. It is a content-adjacent extension, not a new
subsystem: every component it touches (`material.heat_limit_c`,
`material.overheat_damage_per_tick`, `thermal.temperature_c`,
`condition.value`) already existed in the M1 substrate. Before this mechanic,
`heat_limit_c` and `overheat_damage_per_tick` were declared, range-validated,
and read by nothing, and `condition.value` was read as a gate by several
mechanics and written by none -- no vessel in the world could ever be damaged.

The package below is the author's own declaration, preserved as written. It is
deliberately NOT corrected to match what the mechanic actually implies for the
rest of the world; the M3 experiment is whether installation and the
interaction assays surface what the author failed to declare. See
docs/audits/m3-overheat-authoring-experiment.md for the result.
"""

from __future__ import annotations

from ..model import World
from ..profile import MechanicPackage


class OverheatDamageProcess:
    """A vessel held above its material's heat limit degrades and fails."""

    rule_id = "process.material.overheat-damage"
    version = "1"
    order = 25
    read_paths: tuple[str, ...] = (
        "entities.<vessel>.thermal.temperature_c",
        "entities.<vessel>.material.heat_limit_c",
        "entities.<vessel>.material.overheat_damage_per_tick",
        "entities.<vessel>.condition.value",
    )
    write_paths: tuple[str, ...] = ("entities.<vessel>.condition.value",)

    def _overheating(self, entity) -> bool:
        return (
            entity.material is not None
            and entity.thermal is not None
            and entity.condition is not None
            and entity.condition.value > 0
            and entity.thermal.temperature_c > entity.material.heat_limit_c
        )

    def due(self, world: World) -> bool:
        return any(self._overheating(entity) for entity in world.entities.values())

    def apply(self, world: World) -> None:
        for entity in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if not self._overheating(entity):
                continue
            assert entity.condition and entity.material
            entity.condition.value = max(
                0, entity.condition.value - entity.material.overheat_damage_per_tick
            )


OVERHEAT_DAMAGE_PACKAGE = MechanicPackage(
    mechanic_id="process.material.overheat-damage",
    version="1",
    causal_bearer="autonomous process (material failure under sustained heat)",
    representation="deterministic",
    reads=OverheatDamageProcess.read_paths,
    writes=OverheatDamageProcess.write_paths,
    commit_occasion="tick",
    order=OverheatDamageProcess.order,
    requires=(
        "entities.<vessel>.material",
        "entities.<vessel>.thermal",
        "entities.<vessel>.condition",
    ),
    optional_modifiers=("entities.<vessel>.container.heat_source_id",),
    forbids=(),
    emits=("causal event per tick in which any vessel takes overheat damage",),
    effects=(
        (
            "condition.value -= material.overheat_damage_per_tick, floored at 0, "
            "for every vessel whose thermal.temperature_c exceeds "
            "material.heat_limit_c"
        ),
    ),
    invariants=(
        "condition.value stays within 0..100",
        "no vessel at or below its heat limit takes damage",
        "damage is monotonic: this mechanic never repairs",
    ),
    dependencies=("process.thermal.vessels",),
    unsupported_interactions=(),
    limits=(
        (
                "Failure is a single scalar. There is no cracking, leaking, partial "
            "failure, or material-specific failure mode."
        ),
        "Damage is not reversible and no repair mechanic exists.",
        (
            "Only vessel temperature is considered; ambient exposure, thermal "
            "shock, and rate of change are not represented."
        ),
    ),
    tests=(
        "tests/test_overheat_assay.py::test_vessel_over_its_heat_limit_degrades_and_fails",
        "tests/test_overheat_assay.py::test_vessel_within_its_heat_limit_is_undamaged",
        "tests/test_overheat_assay.py::test_damage_stops_at_zero_and_never_repairs",
    ),
    semantic_bindings=(),
    trace_contract=(
        "Each tick in which damage applies emits an event naming the vessel, "
        "its temperature, its heat limit, and the condition before and after."
    ),
)


class VesselFailureSpillProcess:
    """A vessel that has failed cannot hold its contents.

    Authored as the M4 follow-on to the incoherence M3 left open: a destroyed
    vessel that still holds liquid. Written without a planted omission -- the
    package below declares the causal story the author actually reasoned to,
    and the interaction assays are left to find consequential readers the
    author did not think of. That is the division of labour the assays exist
    for; see docs/audits/m4-spill-experiment.md for what they found.
    """

    rule_id = "process.material.vessel-failure-spill"
    version = "1"
    order = 26
    read_paths: tuple[str, ...] = (
        "entities.<vessel>.condition.value",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.liquid",
        "physical_ledger.spilled_ml",
        "physical_ledger.heat_lost",
    )

    def _failed_and_holding(self, entity) -> bool:
        return (
            entity.condition is not None
            and entity.condition.value == 0
            and entity.container is not None
            and entity.liquid is not None
            and entity.liquid.volume_ml > 0
        )

    def due(self, world: World) -> bool:
        return any(
            self._failed_and_holding(entity) for entity in world.entities.values()
        )

    def apply(self, world: World) -> None:
        if world.physical_ledger is None:
            raise ValueError("vessel failure spill requires a physical ledger")
        for entity in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if not self._failed_and_holding(entity):
                continue
            assert entity.liquid is not None
            world.physical_ledger.spilled_ml += entity.liquid.volume_ml
            world.physical_ledger.heat_lost += entity.liquid.heat_units
            entity.liquid.volume_ml = 0
            entity.liquid.salt_mg = 0
            entity.liquid.pathogens = 0
            entity.liquid.heat_units = 0


VESSEL_FAILURE_SPILL_PACKAGE = MechanicPackage(
    mechanic_id="process.material.vessel-failure-spill",
    version="1",
    causal_bearer="autonomous process (a failed container cannot retain contents)",
    representation="deterministic",
    reads=VesselFailureSpillProcess.read_paths,
    writes=VesselFailureSpillProcess.write_paths,
    commit_occasion="tick",
    order=VesselFailureSpillProcess.order,
    requires=(
        "entities.<vessel>.container",
        "entities.<vessel>.condition",
        "entities.<vessel>.liquid",
        "physical_ledger",
    ),
    optional_modifiers=(),
    forbids=(),
    emits=("causal event per tick in which any failed vessel loses its contents",),
    effects=(
        (
            "for every vessel at condition 0 still holding liquid: add its "
            "volume to physical_ledger.spilled_ml and its heat to "
            "physical_ledger.heat_lost, then zero every liquid field"
        ),
    ),
    invariants=(
        "a vessel at condition 0 never holds liquid after this process runs",
        (
            "volume is conserved against the ledger: initial + added equals "
            "in-world + drunk + evaporated + spilled"
        ),
        "an intact vessel is never emptied by this mechanic",
    ),
    dependencies=(
        "process.material.overheat-damage",
        "process.thermal.vessels",
    ),
    unsupported_interactions=(),
    limits=(
        (
            "The ledger records spilled volume and heat but has no field for "
            "spilled salt or pathogens, so those quantities leave the world "
            "unaccounted. physical_ledger.evaporated is a full LiquidState "
            "while spilled_ml is a bare integer; this asymmetry is in the "
            "existing ledger, not introduced here."
        ),
        (
            "Contents are destroyed rather than transferred anywhere. There "
            "is no ground, puddle, or location that receives them."
        ),
        "Failure is instantaneous and total; there is no slow leak.",
        (
            "physical_ledger.overflow_ml remains unwritten by any mechanic; "
            "this mechanic does not model overfilling."
        ),
    ),
    tests=(
        "tests/test_spill.py::test_failed_vessel_loses_its_contents",
        "tests/test_spill.py::test_intact_vessel_keeps_its_contents",
        "tests/test_spill.py::test_volume_is_conserved_against_the_ledger",
    ),
    semantic_bindings=(),
    trace_contract=(
        "Each tick in which a spill occurs emits an event naming the vessel, "
        "the volume and heat lost, and the ledger totals before and after."
    ),
)
