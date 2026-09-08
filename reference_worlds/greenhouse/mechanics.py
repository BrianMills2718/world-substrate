"""Greenhouse mechanics: take, put down, fill, and water."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from world_substrate.model import World, owner_ref
from world_substrate.rules import (
    Check,
    FillAction,
    TakeAction,
    TypedAction,
    _require_nonempty_string,
)


def _gardener(world: World, actor_id: str):
    actor = world.entities.get(actor_id)
    if actor is None or "gardener" not in actor.category_ids or actor.location is None:
        return None
    return actor


def _held_can_ids(world: World, actor_id: str) -> list[str]:
    return sorted(
        entity.entity_id
        for entity in world.entities.values()
        if entity.component("watering_can") is not None
        and entity.ownership is not None
        and entity.ownership.owner_ref == owner_ref("actor", actor_id)
    )


@dataclass(frozen=True)
class PutDownAction:
    actor_id: str
    vessel_id: str
    base_revision: int
    controller_id: str
    kind: str = "put_down"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PutDownAction:
        if value.get("kind") != "put_down":
            raise ValueError("record is not a put_down action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class WaterAction:
    actor_id: str
    vessel_id: str
    plant_id: str
    bed_id: str
    base_revision: int
    controller_id: str
    kind: str = "water"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "plant": self.plant_id,
            "bed": self.bed_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> WaterAction:
        if value.get("kind") != "water":
            raise ValueError("record is not a water action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            plant_id=_require_nonempty_string(value, "plant"),
            bed_id=_require_nonempty_string(value, "bed"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


class TakeCanRule:
    rule_id = "greenhouse.inventory.take"
    version = "1"
    action_kind = "take"
    read_paths = (
        "entities.<actor>.location",
        "entities.<vessel>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.portable",
        "entities.<vessel>.components.watering_can",
    )
    write_paths = (
        "entities.<vessel>.ownership.owner_ref",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> TakeAction:
        return TakeAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _gardener(world, actor_id)
        if actor is None:
            return []
        return [
            TakeAction(actor_id, entity.entity_id, world.revision, "unselected")
            for entity in sorted(world.entities.values(), key=lambda row: row.entity_id)
            if entity.component("watering_can") is not None
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
            and entity.portable is not None
            and entity.portable.portable
            and entity.ownership is not None
            and entity.ownership.owner_ref == owner_ref("place", actor.location.location_id)
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, TakeAction):
            raise TypeError("greenhouse take rule requires TakeAction")
        actor = _gardener(world, action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        checks = [
            Check("Gardener exists", actor is not None),
            Check("Watering can exists", vessel is not None and vessel.component("watering_can") is not None),
        ]
        if actor is None or vessel is None:
            return checks
        checks.extend(
            [
                Check("Watering can is portable", bool(vessel.portable and vessel.portable.portable)),
                Check(
                    "Watering can is here",
                    bool(vessel.location and vessel.location.location_id == actor.location.location_id),
                ),
                Check(
                    "Watering can is in the shared store",
                    bool(vessel.ownership and vessel.ownership.owner_ref == owner_ref("place", actor.location.location_id)),
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, TakeAction)
        vessel = world.entities[action.vessel_id]
        assert vessel.ownership is not None
        vessel.ownership.owner_ref = owner_ref("actor", action.actor_id)
        vessel.last_cause_event_id = event_id


class PutDownCanRule:
    rule_id = "greenhouse.inventory.put-down"
    version = "1"
    action_kind = "put_down"
    read_paths = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.components.watering_can",
    )
    write_paths = (
        "entities.<vessel>.ownership.owner_ref",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> PutDownAction:
        return PutDownAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _gardener(world, actor_id)
        if actor is None:
            return []
        return [
            PutDownAction(actor_id, vessel_id, world.revision, "unselected")
            for vessel_id in _held_can_ids(world, actor_id)
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, PutDownAction):
            raise TypeError("greenhouse put-down rule requires PutDownAction")
        actor = _gardener(world, action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        return [
            Check("Gardener exists", actor is not None),
            Check("Watering can exists", vessel is not None and vessel.component("watering_can") is not None),
            Check(
                "Gardener holds the watering can",
                bool(vessel and vessel.ownership and vessel.ownership.owner_ref == owner_ref("actor", action.actor_id)),
            ),
        ]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, PutDownAction)
        actor = world.entities[action.actor_id]
        vessel = world.entities[action.vessel_id]
        assert actor.location is not None and vessel.ownership is not None
        vessel.ownership.owner_ref = owner_ref("place", actor.location.location_id)
        vessel.last_cause_event_id = event_id


class FillCanRule:
    rule_id = "greenhouse.water.fill-can"
    version = "1"
    action_kind = "fill"
    read_paths = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.components.watering_can",
        "entities.<source>.location",
    )
    write_paths = (
        "entities.<vessel>.components.watering_can.state",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> FillAction:
        return FillAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _gardener(world, actor_id)
        if actor is None:
            return []
        cans = [
            world.entities[vessel_id]
            for vessel_id in _held_can_ids(world, actor_id)
            if world.entities[vessel_id].component("watering_can").state == "empty"
        ]
        sources = [
            entity
            for entity in sorted(world.entities.values(), key=lambda row: row.entity_id)
            if "liquid_source" in entity.category_ids
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
        ]
        return [
            FillAction(actor_id, can.entity_id, source.entity_id, 1, world.revision, "unselected")
            for can in cans
            for source in sources
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, FillAction):
            raise TypeError("greenhouse fill rule requires FillAction")
        actor = _gardener(world, action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        source = world.entities.get(action.source_id)
        can = vessel.component("watering_can") if vessel else None
        return [
            Check("Gardener exists", actor is not None),
            Check("Watering can exists", can is not None),
            Check(
                "Gardener holds the watering can",
                bool(vessel and vessel.ownership and vessel.ownership.owner_ref == owner_ref("actor", action.actor_id)),
            ),
            Check("Watering can is empty", bool(can and can.state == "empty")),
            Check("Requested fill is one can", action.volume_ml == 1, action.volume_ml, 1),
            Check(
                "Water source is here",
                bool(
                    actor
                    and source
                    and "liquid_source" in source.category_ids
                    and source.location
                    and source.location.location_id == actor.location.location_id
                ),
            ),
        ]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, FillAction)
        vessel = world.entities[action.vessel_id]
        can = vessel.component("watering_can")
        assert can is not None
        can.state = "filled"
        vessel.last_cause_event_id = event_id


class WaterPlantRule:
    rule_id = "greenhouse.plant.water"
    version = "1"
    action_kind = "water"
    read_paths = (
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.components.watering_can",
        "entities.<plant>.location",
        "entities.<plant>.components.plant",
        "entities.<bed>.location",
    )
    write_paths = (
        "entities.<vessel>.components.watering_can.state",
        "entities.<vessel>.last_cause_event_id",
        "entities.<plant>.components.plant.stage",
        "entities.<plant>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> WaterAction:
        return WaterAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _gardener(world, actor_id)
        if actor is None:
            return []
        cans = [
            world.entities[vessel_id]
            for vessel_id in _held_can_ids(world, actor_id)
            if world.entities[vessel_id].component("watering_can").state == "filled"
        ]
        plants = [
            entity
            for entity in sorted(world.entities.values(), key=lambda row: row.entity_id)
            if entity.component("plant") is not None
            and entity.component("plant").stage == "dry"
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
        ]
        return [
            WaterAction(actor_id, can.entity_id, plant.entity_id, plant.component("plant").bed_id, world.revision, "unselected")
            for can in cans
            for plant in plants
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, WaterAction):
            raise TypeError("greenhouse water rule requires WaterAction")
        actor = _gardener(world, action.actor_id)
        vessel = world.entities.get(action.vessel_id)
        plant_entity = world.entities.get(action.plant_id)
        bed = world.entities.get(action.bed_id)
        can = vessel.component("watering_can") if vessel else None
        plant = plant_entity.component("plant") if plant_entity else None
        return [
            Check("Gardener exists", actor is not None),
            Check("Watering can exists", can is not None),
            Check("Plant exists", plant is not None),
            Check("Garden bed exists", bed is not None and "garden_bed" in bed.category_ids),
            Check(
                "Gardener holds the watering can",
                bool(vessel and vessel.ownership and vessel.ownership.owner_ref == owner_ref("actor", action.actor_id)),
            ),
            Check("Watering can is filled", bool(can and can.state == "filled")),
            Check("Plant is dry", bool(plant and plant.stage == "dry")),
            Check("Plant belongs to the named bed", bool(plant and plant.bed_id == action.bed_id)),
            Check(
                "Plant and bed are here",
                bool(
                    actor
                    and plant_entity
                    and plant_entity.location
                    and bed
                    and bed.location
                    and plant_entity.location.location_id == actor.location.location_id
                    and bed.location.location_id == actor.location.location_id
                ),
            ),
        ]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, WaterAction)
        vessel = world.entities[action.vessel_id]
        plant_entity = world.entities[action.plant_id]
        can = vessel.component("watering_can")
        plant = plant_entity.component("plant")
        assert can is not None and plant is not None
        can.state = "empty"
        plant.stage = "watered"
        vessel.last_cause_event_id = event_id
        plant_entity.last_cause_event_id = event_id
