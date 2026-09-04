"""The M3 overheat world: the M1 substrate plus one adjacent mechanic.

Builds the same world twice -- once with the promoted M1 registry, once with
`OverheatDamageProcess` additionally installed -- so an assay can compare
behaviour with and without the authored mechanic.
"""

from __future__ import annotations

import json
from pathlib import Path

from world_substrate.engine import Engine
from world_substrate.mechanisms import (
    ClockAdvanceProcess,
    DrinkRule,
    FillRule,
    FireFuelProcess,
    GiveRule,
    HeatRule,
    HydrationDecayProcess,
    PourRule,
    TakeRule,
    ThermalProcess,
    UnheatRule,
)
from world_substrate.mechanisms.damage import (
    OVERHEAT_DAMAGE_PACKAGE,
    OverheatDamageProcess,
)
from world_substrate.model import (
    CarryingState,
    PhysicalLedger,
    PortableState,
    World,
)
from world_substrate.profile import MechanicProfile, retrofit_package
from world_substrate.rules import RuleRegistry

from .probe import _entities, repository_root

CONTENT_PATH = "reference_worlds/castaway/overheat-v0.json"

BEARERS = {
    "mechanism.liquid.fill": "actor action",
    "mechanism.liquid.pour": "actor action",
    "mechanism.liquid.drink": "actor action",
    "mechanism.ownership.take": "actor action",
    "mechanism.ownership.give": "actor action",
    "mechanism.thermal.heat": "actor action",
    "mechanism.thermal.unheat": "actor action",
    "system.clock.advance": "canonical time",
    "process.actor.hydration-decay": "autonomous process",
    "process.thermal.vessels": "autonomous process",
    "process.heat-source.fuel": "autonomous process",
}


def _base_registry() -> RuleRegistry:
    registry = RuleRegistry()
    for rule in (
        DrinkRule(),
        FillRule(),
        GiveRule(),
        HeatRule(),
        PourRule(),
        TakeRule(),
        UnheatRule(),
    ):
        registry.register_action(rule)
    for process in (
        ClockAdvanceProcess(),
        HydrationDecayProcess(),
        ThermalProcess(cool_empty_vessels=True),
        FireFuelProcess(),
    ):
        registry.register_process(process)
    return registry


def _world(registry: RuleRegistry, root: Path | None = None) -> World:
    root = root or repository_root()
    content = json.loads((root / CONTENT_PATH).read_text())
    world = World(
        world_id=content["world_id"],
        revision=0,
        tick=0,
        entities=_entities(content),
        engine_id="world-substrate-core@1",
        content_id=content["content_id"],
        rule_versions=registry.versions(),
        physical_ledger=PhysicalLedger(),
    )
    for actor_id in ("robinson", "friday"):
        world.entities[actor_id].carrying = CarryingState(capacity_weight=24)
    for vessel_id in ("gourd-flask", "clay-pot"):
        world.entities[vessel_id].portable = PortableState()
    return world


def build_baseline_engine(root: Path | None = None) -> Engine:
    """The world under the promoted M1 mechanics alone."""
    registry = _base_registry()
    return Engine(_world(registry, root), registry)


def build_overheat_engine(root: Path | None = None) -> Engine:
    """The same world with the authored overheat mechanic installed."""
    registry = _base_registry()
    registry.register_process(OverheatDamageProcess())
    return Engine(_world(registry, root), registry)


def installed_profile(with_overheat: bool) -> tuple[MechanicProfile, list]:
    """Install the M1 mechanics, then the authored mechanic through validation."""
    registry = _base_registry()
    profile = MechanicProfile()
    rules = [registry.action(kind) for kind in registry.action_kinds()]
    rules += list(registry.processes())
    for rule in rules:
        findings = profile.install(
            retrofit_package(rule, BEARERS.get(rule.rule_id, "unspecified")), rule
        )
        rejects = [item for item in findings if item.severity == "reject"]
        if rejects:
            raise AssertionError(f"retrofit rejected for {rule.rule_id}: {rejects}")
    if not with_overheat:
        return profile, []
    candidate = OverheatDamageProcess()
    install_findings = profile.install(OVERHEAT_DAMAGE_PACKAGE, candidate)
    return profile, install_findings
