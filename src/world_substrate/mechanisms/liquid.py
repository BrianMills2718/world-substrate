"""Exact extensive-liquid transfer rules."""

from __future__ import annotations

from typing import Any

from ..model import Entity, LiquidState, World, owner_ref
from ..rules import Check, DrinkAction, FillAction, PourAction, TypedAction

LIQUID_FIELDS = ("volume_ml", "salt_mg", "pathogens", "heat_units")


def _accessible(world: World, actor: Entity, vessel: Entity) -> bool:
    if actor.location is None or vessel.ownership is None:
        return False
    return vessel.ownership.owner_ref in {
        owner_ref("actor", actor.entity_id),
        owner_ref("place", actor.location.location_id),
    }


def _split(source: LiquidState, volume_ml: int) -> LiquidState:
    original_volume = source.volume_ml
    if not 0 < volume_ml <= original_volume:
        raise ValueError("split volume is outside source contents")
    portion = {
        field: getattr(source, field) * volume_ml // original_volume
        for field in LIQUID_FIELDS
    }
    for field in LIQUID_FIELDS:
        setattr(source, field, getattr(source, field) - portion[field])
    return LiquidState(**portion)


def _mix(destination: LiquidState, portion: LiquidState) -> None:
    for field in LIQUID_FIELDS:
        setattr(
            destination, field, getattr(destination, field) + getattr(portion, field)
        )


class FillRule:
    rule_id = "mechanism.liquid.fill"
    version = "1"
    action_kind = "fill"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.condition",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
        "entities.<source>.location",
        "entities.<source>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.liquid",
        "entities.<vessel>.thermal",
        "entities.<vessel>.last_cause_event_id",
        "entities.<source>.liquid",
    )

    def action_from_dict(self, value: dict[str, Any]) -> FillAction:
        return FillAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        vessels = [
            entity
            for entity in world.entities.values()
            if entity.container is not None
            and entity.liquid is not None
            and _accessible(world, actor, entity)
        ]
        sources = [
            entity
            for entity in world.entities.values()
            if "liquid_source" in entity.category_ids
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
            and entity.liquid is not None
        ]
        actions: list[TypedAction] = []
        for vessel in sorted(vessels, key=lambda item: item.entity_id):
            assert vessel.container is not None and vessel.liquid is not None
            room = vessel.container.capacity_ml - vessel.liquid.volume_ml
            if room <= 0:
                continue
            for source in sorted(sources, key=lambda item: item.entity_id):
                assert source.liquid is not None
                maximum = min(room, source.liquid.volume_ml)
                for amount in sorted({min(maximum, 250), min(maximum, 1000)}):
                    if amount > 0:
                        actions.append(
                            FillAction(
                                actor_id=actor_id,
                                vessel_id=vessel.entity_id,
                                source_id=source.entity_id,
                                volume_ml=amount,
                                base_revision=world.revision,
                                controller_id="unselected",
                            )
                        )
        return actions

    def consequences(self, world: World, action: TypedAction) -> list[str]:
        """What filling this vessel would throw away.

        Filling a treated vessel from a pathogen-bearing source re-contaminates
        everything already in it. The mixing rule is correct and the affordance
        said nothing: `fill` looked identical whether the vessel was empty or
        held water the actor had just spent fuel and several turns boiling. The
        M5 policy filled its own treated pot and drank it, losing 40 health.
        """
        if not isinstance(action, FillAction):
            return []
        vessel = world.entities.get(action.vessel_id)
        source = world.entities.get(action.source_id)
        if vessel is None or source is None:
            return []
        if vessel.liquid is None or source.liquid is None:
            return []
        if vessel.liquid.volume_ml <= 0 or vessel.liquid.pathogens:
            return []
        if not source.liquid.pathogens:
            return []
        return [
            (
                f"re-contaminates the {vessel.liquid.volume_ml}ml of treated "
                f"water already in {action.vessel_id}"
            )
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, FillAction):
            raise TypeError("fill rule requires FillAction")
        actor = world.entities.get(action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        source = world.entities.get(action.source_id)
        checks = [
            Check("Actor exists", actor is not None and actor.actor is not None),
            Check("Vessel exists", vessel is not None and vessel.container is not None),
            Check(
                "Source exists",
                source is not None and "liquid_source" in source.category_ids
                if source
                else False,
            ),
            Check(
                "Positive bounded liquid volume",
                type(action.volume_ml) is int and 1 <= action.volume_ml <= 10_000,
                action.volume_ml,
                "1..10000 ml",
            ),
        ]
        if actor is None or vessel is None or source is None:
            return checks
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Vessel is local or carried", _accessible(world, actor, vessel)),
                Check(
                    "Vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                    vessel.condition.value if vessel.condition else None,
                    ">0",
                ),
                Check(
                    "Local liquid source",
                    bool(
                        actor.location
                        and source.location
                        and source.location.location_id == actor.location.location_id
                    ),
                ),
            ]
        )
        if source.liquid is not None:
            checks.append(
                Check(
                    "Source has volume",
                    source.liquid.volume_ml >= action.volume_ml,
                    source.liquid.volume_ml,
                    action.volume_ml,
                )
            )
        else:
            checks.append(Check("Source has liquid state", False))
        if vessel.container is not None and vessel.liquid is not None:
            checks.append(
                Check(
                    "Vessel has room",
                    vessel.liquid.volume_ml + action.volume_ml
                    <= vessel.container.capacity_ml,
                    vessel.container.capacity_ml - vessel.liquid.volume_ml,
                    action.volume_ml,
                )
            )
        else:
            checks.append(Check("Vessel has container and liquid state", False))
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, FillAction):
            raise TypeError("fill rule requires FillAction")
        vessel = world.entities[action.vessel_id]
        source = world.entities[action.source_id]
        assert vessel.liquid is not None and source.liquid is not None
        portion = _split(source.liquid, action.volume_ml)
        _mix(vessel.liquid, portion)
        if vessel.container is not None:
            vessel.container.boiling_ticks = 0
        if vessel.thermal is not None and vessel.liquid.volume_ml:
            vessel.thermal.temperature_c = round(
                vessel.liquid.heat_units / vessel.liquid.volume_ml, 2
            )
        vessel.last_cause_event_id = event_id


class PourRule:
    rule_id = "mechanism.liquid.pour"
    version = "1"
    action_kind = "pour"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.condition",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
        "entities.<destination>.ownership",
        "entities.<destination>.condition",
        "entities.<destination>.container",
        "entities.<destination>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.liquid",
        "entities.<vessel>.thermal",
        "entities.<vessel>.last_cause_event_id",
        "entities.<destination>.liquid",
        "entities.<destination>.thermal",
        "entities.<destination>.container.boiling_ticks",
        "entities.<destination>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> PourAction:
        return PourAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        vessels = sorted(
            (
                entity
                for entity in world.entities.values()
                if entity.container is not None
                and entity.liquid is not None
                and _accessible(world, actor, entity)
            ),
            key=lambda item: item.entity_id,
        )
        actions: list[TypedAction] = []
        for vessel in vessels:
            assert vessel.liquid is not None
            for destination in vessels:
                if destination.entity_id == vessel.entity_id:
                    continue
                assert destination.container and destination.liquid
                maximum = min(
                    vessel.liquid.volume_ml,
                    destination.container.capacity_ml
                    - destination.liquid.volume_ml,
                )
                for amount in sorted({min(maximum, 250), min(maximum, 1000)}):
                    if amount > 0:
                        actions.append(
                            PourAction(
                                actor_id=actor_id,
                                vessel_id=vessel.entity_id,
                                destination_id=destination.entity_id,
                                volume_ml=amount,
                                base_revision=world.revision,
                                controller_id="unselected",
                            )
                        )
        return actions

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, PourAction):
            raise TypeError("pour rule requires PourAction")
        actor = world.entities.get(action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        destination = world.entities.get(action.destination_id)
        checks = [
            Check("Actor exists", actor is not None and actor.actor is not None),
            Check(
                "Source vessel exists",
                vessel is not None and vessel.container is not None,
            ),
            Check(
                "Destination vessel exists",
                destination is not None and destination.container is not None,
            ),
            Check(
                "Positive bounded liquid volume",
                type(action.volume_ml) is int and 1 <= action.volume_ml <= 10_000,
                action.volume_ml,
                "1..10000 ml",
            ),
        ]
        if actor is None or vessel is None or destination is None:
            return checks
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Source vessel is accessible", _accessible(world, actor, vessel)),
                Check(
                    "Destination vessel is accessible",
                    _accessible(world, actor, destination),
                ),
                Check(
                    "Different destination vessel",
                    vessel.entity_id != destination.entity_id,
                ),
                Check(
                    "Source vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                ),
                Check(
                    "Destination vessel is intact",
                    bool(destination.condition and destination.condition.value > 0),
                ),
                Check(
                    "Source vessel is removed from heat",
                    bool(vessel.container and vessel.container.heat_source_id is None),
                ),
                Check(
                    "Destination vessel is removed from heat",
                    bool(
                        destination.container
                        and destination.container.heat_source_id is None
                    ),
                ),
                Check(
                    "Source contains requested volume",
                    bool(
                        vessel.liquid
                        and vessel.liquid.volume_ml >= action.volume_ml
                    ),
                    vessel.liquid.volume_ml if vessel.liquid else None,
                    action.volume_ml,
                ),
                Check(
                    "Destination has room",
                    bool(
                        destination.container
                        and destination.liquid
                        and destination.liquid.volume_ml + action.volume_ml
                        <= destination.container.capacity_ml
                    ),
                    (
                        destination.container.capacity_ml
                        - destination.liquid.volume_ml
                        if destination.container and destination.liquid
                        else None
                    ),
                    action.volume_ml,
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, PourAction):
            raise TypeError("pour rule requires PourAction")
        vessel = world.entities[action.vessel_id]
        destination = world.entities[action.destination_id]
        assert vessel.liquid and destination.liquid and destination.container
        portion = _split(vessel.liquid, action.volume_ml)
        _mix(destination.liquid, portion)
        destination.container.boiling_ticks = 0
        for entity in (vessel, destination):
            if entity.thermal is not None and entity.liquid and entity.liquid.volume_ml:
                entity.thermal.temperature_c = round(
                    entity.liquid.heat_units / entity.liquid.volume_ml, 2
                )
            entity.last_cause_event_id = event_id


class DrinkRule:
    """Consume an exact liquid portion; hazards warn but remain possible."""

    rule_id = "mechanism.liquid.drink"
    version = "1"
    action_kind = "drink"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.actor",
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.condition",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<actor>.actor.health",
        "entities.<actor>.actor.hydration",
        "entities.<actor>.actor.alive",
        "entities.<vessel>.liquid",
        "entities.<vessel>.last_cause_event_id",
        "physical_ledger.drunk",
    )

    safe_drinking_temperature_c = 45
    safe_salt_mg_per_litre = 1_000
    hydration_per_250ml = 25
    pathogen_harm_per_250ml = 12
    salt_harm_per_250ml = 4
    salt_hydration_loss_per_250ml = 35
    hot_harm_per_250ml = 10

    def action_from_dict(self, value: dict[str, Any]) -> DrinkAction:
        return DrinkAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        actions: list[TypedAction] = []
        for vessel in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if (
                vessel.container is None
                or vessel.liquid is None
                or not _accessible(world, actor, vessel)
            ):
                continue
            for amount in sorted(
                {
                    min(vessel.liquid.volume_ml, 250),
                    min(vessel.liquid.volume_ml, 1_000),
                }
            ):
                if amount > 0:
                    actions.append(
                        DrinkAction(
                            actor_id=actor_id,
                            vessel_id=vessel.entity_id,
                            volume_ml=amount,
                            base_revision=world.revision,
                            controller_id="unselected",
                        )
                    )
        return actions

    def _warnings(self, liquid: LiquidState) -> list[str]:
        warnings: list[str] = []
        if liquid.pathogens:
            warnings.append("Contains pathogens")
        if (
            liquid.volume_ml
            and liquid.salt_mg * 1_000
            > self.safe_salt_mg_per_litre * liquid.volume_ml
        ):
            warnings.append("Salty: boiling will not remove salt")
        if (
            liquid.volume_ml
            and liquid.heat_units
            > self.safe_drinking_temperature_c * liquid.volume_ml
        ):
            warnings.append("Too hot to drink safely")
        return warnings

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, DrinkAction):
            raise TypeError("drink rule requires DrinkAction")
        actor = world.entities.get(action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        checks = [
            Check("Actor exists", actor is not None and actor.actor is not None),
            Check(
                "Vessel exists",
                vessel is not None and vessel.container is not None,
            ),
            Check(
                "Positive bounded liquid volume",
                type(action.volume_ml) is int and 1 <= action.volume_ml <= 10_000,
                action.volume_ml,
                "1..10000 ml",
            ),
        ]
        if actor is None or vessel is None:
            return checks
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Vessel is local or carried", _accessible(world, actor, vessel)),
                Check(
                    "Vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                ),
                Check(
                    "Vessel is removed from heat",
                    bool(vessel.container and vessel.container.heat_source_id is None),
                ),
                Check(
                    "Vessel contains requested volume",
                    bool(
                        vessel.liquid
                        and vessel.liquid.volume_ml >= action.volume_ml
                    ),
                    vessel.liquid.volume_ml if vessel.liquid else None,
                    action.volume_ml,
                ),
            ]
        )
        if vessel.liquid and vessel.liquid.volume_ml >= action.volume_ml:
            preview = LiquidState(
                **{
                    field: getattr(vessel.liquid, field)
                    * action.volume_ml
                    // vessel.liquid.volume_ml
                    for field in LIQUID_FIELDS
                }
            )
            checks.extend(
                Check(
                    f"Warning: {warning}",
                    True,
                    warning,
                    "The action remains possible and causes rule-defined harm",
                )
                for warning in self._warnings(preview)
            )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, DrinkAction):
            raise TypeError("drink rule requires DrinkAction")
        actor = world.entities[action.actor_id]
        vessel = world.entities[action.vessel_id]
        assert actor.actor and vessel.liquid and world.physical_ledger
        portion = _split(vessel.liquid, action.volume_ml)
        warnings = self._warnings(portion)
        _mix(world.physical_ledger.drunk, portion)
        portions = (action.volume_ml + 249) // 250
        hydration = action.volume_ml * self.hydration_per_250ml // 250
        harm = 0
        if "Contains pathogens" in warnings:
            harm += portions * self.pathogen_harm_per_250ml
        if "Salty: boiling will not remove salt" in warnings:
            harm += portions * self.salt_harm_per_250ml
            hydration -= portions * self.salt_hydration_loss_per_250ml
        if "Too hot to drink safely" in warnings:
            harm += portions * self.hot_harm_per_250ml
        actor.actor.hydration = min(100, max(0, actor.actor.hydration + hydration))
        actor.actor.health = max(0, actor.actor.health - harm)
        actor.actor.alive = actor.actor.health > 0
        vessel.last_cause_event_id = event_id
