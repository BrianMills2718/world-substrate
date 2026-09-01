"""Registered vessel heating, boiling, evaporation, and fire-fuel rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..model import Entity, LiquidState, World
from ..rules import Check, HeatAction, TypedAction, UnheatAction


def _accessible(actor: Entity, vessel: Entity) -> bool:
    if actor.location is None or vessel.ownership is None:
        return False
    return vessel.ownership.owner_ref in {
        f"actor:{actor.entity_id}",
        f"place:{actor.location.location_id}",
    }


def _sync_temperature(vessel: Entity) -> None:
    if vessel.liquid is None or vessel.thermal is None:
        return
    if vessel.liquid.volume_ml:
        vessel.thermal.temperature_c = round(
            vessel.liquid.heat_units / vessel.liquid.volume_ml, 2
        )


class HeatRule:
    rule_id = "mechanism.thermal.heat"
    version = "1"
    action_kind = "heat"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.condition",
        "entities.<vessel>.container",
        "entities.<vessel>.material",
        "entities.<target>.location",
        "entities.<target>.condition",
        "entities.<target>.heat_source",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.ownership",
        "entities.<vessel>.container.heat_source_id",
        "entities.<vessel>.container.boiling_ticks",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> HeatAction:
        return HeatAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        vessels = sorted(
            (
                entity
                for entity in world.entities.values()
                if entity.container is not None
                and entity.material is not None
                and _accessible(actor, entity)
            ),
            key=lambda item: item.entity_id,
        )
        sources = sorted(
            (
                entity
                for entity in world.entities.values()
                if entity.heat_source is not None
                and entity.location is not None
                and entity.location.location_id == actor.location.location_id
            ),
            key=lambda item: item.entity_id,
        )
        return [
            HeatAction(
                actor_id=actor_id,
                vessel_id=vessel.entity_id,
                target_id=source.entity_id,
                base_revision=world.revision,
                controller_id="unselected",
            )
            for vessel in vessels
            for source in sources
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, HeatAction):
            raise TypeError("heat rule requires HeatAction")
        actor = world.entities.get(action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        source = world.entities.get(action.target_id)
        checks = [
            Check("Actor exists", actor is not None and actor.actor is not None),
            Check(
                "Vessel exists",
                vessel is not None and vessel.container is not None,
            ),
            Check(
                "Heat source exists",
                source is not None and source.heat_source is not None,
            ),
        ]
        if actor is None or vessel is None or source is None:
            return checks
        attached = sum(
            bool(
                entity.container
                and entity.container.heat_source_id == source.entity_id
            )
            for entity in world.entities.values()
        )
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Vessel is local or carried", _accessible(actor, vessel)),
                Check(
                    "Vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                ),
                Check(
                    "Vessel is removed from heat",
                    bool(vessel.container and vessel.container.heat_source_id is None),
                ),
                Check(
                    "Vessel has explicit material mechanics",
                    vessel.material is not None,
                ),
                Check(
                    "Local intact fueled heat source",
                    bool(
                        actor.location
                        and source.location
                        and source.location.location_id
                        == actor.location.location_id
                        and source.condition
                        and source.condition.value > 0
                        and source.heat_source
                        and source.heat_source.fuel > 0
                    ),
                ),
                Check(
                    "Free heat slot",
                    bool(source.heat_source and attached < source.heat_source.heat_slots),
                    attached,
                    source.heat_source.heat_slots if source.heat_source else None,
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, HeatAction):
            raise TypeError("heat rule requires HeatAction")
        actor = world.entities[action.actor_id]
        vessel = world.entities[action.vessel_id]
        assert actor.location and vessel.container and vessel.ownership
        vessel.ownership.owner_ref = f"place:{actor.location.location_id}"
        vessel.container.heat_source_id = action.target_id
        vessel.container.boiling_ticks = 0
        vessel.last_cause_event_id = event_id


class UnheatRule:
    rule_id = "mechanism.thermal.unheat"
    version = "1"
    action_kind = "unheat"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.condition",
        "entities.<vessel>.container.heat_source_id",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.container.heat_source_id",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> UnheatAction:
        return UnheatAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        return [
            UnheatAction(
                actor_id=actor_id,
                vessel_id=entity.entity_id,
                base_revision=world.revision,
                controller_id="unselected",
            )
            for entity in sorted(world.entities.values(), key=lambda item: item.entity_id)
            if entity.container is not None and _accessible(actor, entity)
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, UnheatAction):
            raise TypeError("unheat rule requires UnheatAction")
        actor = world.entities.get(action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        checks = [
            Check("Actor exists", actor is not None and actor.actor is not None),
            Check(
                "Vessel exists",
                vessel is not None and vessel.container is not None,
            ),
        ]
        if actor is None or vessel is None:
            return checks
        source = (
            world.entities.get(vessel.container.heat_source_id)
            if vessel.container and vessel.container.heat_source_id
            else None
        )
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Vessel is local or carried", _accessible(actor, vessel)),
                Check(
                    "Vessel is on a local heat source",
                    bool(
                        actor.location
                        and source
                        and source.location
                        and source.location.location_id
                        == actor.location.location_id
                    ),
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, UnheatAction):
            raise TypeError("unheat rule requires UnheatAction")
        vessel = world.entities[action.vessel_id]
        assert vessel.container
        vessel.container.heat_source_id = None
        vessel.last_cause_event_id = event_id


@dataclass
class ThermalProcess:
    ambient_temperature_c: int = 22
    boiling_temperature_c: int = 100
    boiling_ticks_to_kill_pathogens: int = 2
    boiling_evaporation_ml_per_tick: int = 25
    evaporation_heat_units_per_ml: int = 1000

    rule_id = "process.thermal.vessels"
    version = "1"
    order = 20
    read_paths: tuple[str, ...] = (
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
        "entities.<vessel>.material",
        "entities.<source>.heat_source",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.container.boiling_ticks",
        "entities.<vessel>.liquid",
        "entities.<vessel>.thermal",
        "physical_ledger",
    )

    def due(self, world: World) -> bool:
        return any(
            entity.container
            and entity.container.heat_source_id
            and entity.condition
            and entity.condition.value > 0
            for entity in world.entities.values()
        )

    def apply(self, world: World) -> None:
        if world.physical_ledger is None:
            raise ValueError("thermal process requires a physical ledger")
        allocations: dict[str, int] = {}
        for source in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if (
                source.heat_source is None
                or source.condition is None
                or source.condition.value <= 0
                or source.heat_source.fuel <= 0
            ):
                continue
            attached = sorted(
                entity.entity_id
                for entity in world.entities.values()
                if entity.container
                and entity.container.heat_source_id == source.entity_id
                and entity.condition
                and entity.condition.value > 0
            )
            if not attached:
                continue
            share, remainder = divmod(
                source.heat_source.heat_units_per_tick, len(attached)
            )
            for index, entity_id in enumerate(attached):
                allocations[entity_id] = share + (index < remainder)

        for vessel_id in sorted(allocations):
            vessel = world.entities[vessel_id]
            assert vessel.container and vessel.liquid and vessel.material
            gain = (
                allocations[vessel_id]
                * vessel.material.heat_transfer_percent
                // 100
            )
            if vessel.liquid.volume_ml:
                maximum = (
                    vessel.liquid.volume_ml * self.boiling_temperature_c
                )
                warming = max(
                    0, min(gain, maximum - vessel.liquid.heat_units)
                )
                vessel.liquid.heat_units += warming
                world.physical_ledger.heat_added += warming
                _sync_temperature(vessel)
                if vessel.liquid.heat_units >= maximum:
                    vessel.container.boiling_ticks += 1
                    if (
                        vessel.container.boiling_ticks
                        >= self.boiling_ticks_to_kill_pathogens
                        and vessel.liquid.pathogens
                    ):
                        world.physical_ledger.pathogens_killed += (
                            vessel.liquid.pathogens
                        )
                        vessel.liquid.pathogens = 0
                    if vessel.material.open_top:
                        amount = min(
                            self.boiling_evaporation_ml_per_tick,
                            vessel.liquid.volume_ml,
                            (gain - warming)
                            // self.evaporation_heat_units_per_ml,
                        )
                        self._evaporate(world, vessel.liquid, amount)
                else:
                    vessel.container.boiling_ticks = 0
            elif vessel.thermal is not None:
                heat_capacity = max(1, vessel.container.empty_weight * 250)
                vessel.thermal.temperature_c = min(
                    180,
                    vessel.thermal.temperature_c
                    + min(30, gain // heat_capacity),
                )
            _sync_temperature(vessel)

    def _evaporate(self, world: World, liquid: LiquidState, amount: int) -> None:
        if amount <= 0:
            return
        heat = liquid.heat_units * amount // liquid.volume_ml
        liquid.volume_ml -= amount
        liquid.heat_units -= heat
        ledger = world.physical_ledger
        assert ledger is not None
        ledger.evaporated.volume_ml += amount
        ledger.evaporated.heat_units += heat
        ledger.latent_heat_used += amount * self.evaporation_heat_units_per_ml


class FireFuelProcess:
    rule_id = "process.heat-source.fuel"
    version = "1"
    order = 30
    read_paths: tuple[str, ...] = ("entities.<source>.heat_source.fuel",)
    write_paths: tuple[str, ...] = ("entities.<source>.heat_source.fuel",)

    def due(self, world: World) -> bool:
        return any(
            entity.heat_source is not None and entity.heat_source.fuel > 0
            for entity in world.entities.values()
        )

    def apply(self, world: World) -> None:
        for entity in world.entities.values():
            if entity.heat_source is not None and entity.heat_source.fuel > 0:
                entity.heat_source.fuel -= 1
