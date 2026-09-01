"""Registered whole-vessel ownership and carrying rules."""

from __future__ import annotations

from typing import Any

from ..model import Entity, World
from ..rules import Check, GiveAction, TakeAction, TypedAction


def _vessel_weight(vessel: Entity, carrier: Entity) -> int:
    if vessel.container is None or vessel.liquid is None or carrier.carrying is None:
        raise ValueError("vessel weight requires container, liquid, and carrying state")
    divisor = carrier.carrying.liquid_ml_per_weight
    liquid_weight = (vessel.liquid.volume_ml + divisor - 1) // divisor
    return vessel.container.empty_weight + liquid_weight


def _carried_weight(world: World, actor: Entity) -> int:
    return sum(
        _vessel_weight(entity, actor)
        for entity in world.entities.values()
        if entity.ownership is not None
        and entity.ownership.owner_ref == f"actor:{actor.entity_id}"
        and entity.container is not None
        and entity.liquid is not None
        and entity.portable is not None
        and entity.portable.portable
    )


class TakeRule:
    rule_id = "mechanism.ownership.take"
    version = "1"
    action_kind = "take"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.actor",
        "entities.<actor>.carrying",
        "entities.<actor>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.portable",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.ownership.owner_ref",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> TakeAction:
        return TakeAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if (
            actor is None
            or actor.actor is None
            or actor.carrying is None
            or actor.location is None
        ):
            return []
        return [
            TakeAction(
                actor_id=actor_id,
                vessel_id=vessel.entity_id,
                base_revision=world.revision,
                controller_id="unselected",
            )
            for vessel in sorted(world.entities.values(), key=lambda item: item.entity_id)
            if vessel.container is not None
            and vessel.portable is not None
            and vessel.ownership is not None
            and vessel.ownership.owner_ref == f"place:{actor.location.location_id}"
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, TakeAction):
            raise TypeError("take rule requires TakeAction")
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
        checks.extend(
            [
                Check("Actor is alive", bool(actor.actor and actor.actor.alive)),
                Check("Actor has carrying state", actor.carrying is not None),
                Check(
                    "Portable vessel",
                    bool(vessel.portable and vessel.portable.portable),
                ),
                Check(
                    "Vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                ),
                Check(
                    "Vessel is removed from heat",
                    bool(vessel.container and vessel.container.heat_source_id is None),
                ),
                Check(
                    "Vessel is in local shared store",
                    bool(
                        actor.location
                        and vessel.ownership
                        and vessel.ownership.owner_ref
                        == f"place:{actor.location.location_id}"
                    ),
                ),
            ]
        )
        if actor.carrying and vessel.container and vessel.liquid:
            load = _carried_weight(world, actor)
            weight = _vessel_weight(vessel, actor)
            checks.append(
                Check(
                    "Carrying capacity including vessel",
                    load + weight <= actor.carrying.capacity_weight,
                    load + weight,
                    actor.carrying.capacity_weight,
                )
            )
        else:
            checks.append(Check("Carrying capacity can be evaluated", False))
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, TakeAction):
            raise TypeError("take rule requires TakeAction")
        vessel = world.entities[action.vessel_id]
        assert vessel.ownership
        vessel.ownership.owner_ref = f"actor:{action.actor_id}"
        vessel.last_cause_event_id = event_id


class GiveRule:
    rule_id = "mechanism.ownership.give"
    version = "1"
    action_kind = "give"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.actor",
        "entities.<actor>.location",
        "entities.<recipient>.actor",
        "entities.<recipient>.carrying",
        "entities.<recipient>.location",
        "entities.<vessel>.ownership",
        "entities.<vessel>.portable",
        "entities.<vessel>.container",
        "entities.<vessel>.liquid",
    )
    write_paths: tuple[str, ...] = (
        "entities.<vessel>.ownership.owner_ref",
        "entities.<vessel>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> GiveAction:
        return GiveAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            return []
        vessels = [
            entity
            for entity in sorted(world.entities.values(), key=lambda item: item.entity_id)
            if entity.container is not None
            and entity.portable is not None
            and entity.ownership is not None
            and entity.ownership.owner_ref == f"actor:{actor_id}"
        ]
        recipients = [
            entity
            for entity in sorted(world.entities.values(), key=lambda item: item.entity_id)
            if entity.entity_id != actor_id
            and entity.actor is not None
            and entity.actor.alive
            and entity.carrying is not None
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
        ]
        return [
            GiveAction(
                actor_id=actor_id,
                vessel_id=vessel.entity_id,
                target_actor_id=recipient.entity_id,
                base_revision=world.revision,
                controller_id="unselected",
            )
            for vessel in vessels
            for recipient in recipients
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, GiveAction):
            raise TypeError("give rule requires GiveAction")
        actor = world.entities.get(action.actor_id)
        recipient = world.entities.get(action.target_actor_id)
        vessel = world.entities.get(action.vessel_id)
        checks = [
            Check("Giver exists", actor is not None and actor.actor is not None),
            Check(
                "Recipient exists",
                recipient is not None and recipient.actor is not None,
            ),
            Check(
                "Vessel exists",
                vessel is not None and vessel.container is not None,
            ),
        ]
        if actor is None or recipient is None or vessel is None:
            return checks
        checks.extend(
            [
                Check("Giver is alive", bool(actor.actor and actor.actor.alive)),
                Check(
                    "Living distinct recipient here",
                    bool(
                        actor.location
                        and recipient.actor
                        and recipient.actor.alive
                        and recipient.entity_id != actor.entity_id
                        and recipient.location
                        and recipient.location.location_id
                        == actor.location.location_id
                    ),
                ),
                Check(
                    "Vessel is carried by giver",
                    bool(
                        vessel.ownership
                        and vessel.ownership.owner_ref == f"actor:{actor.entity_id}"
                    ),
                ),
                Check(
                    "Portable vessel",
                    bool(vessel.portable and vessel.portable.portable),
                ),
                Check(
                    "Vessel is intact",
                    bool(vessel.condition and vessel.condition.value > 0),
                ),
                Check(
                    "Vessel is removed from heat",
                    bool(vessel.container and vessel.container.heat_source_id is None),
                ),
                Check("Recipient has carrying state", recipient.carrying is not None),
            ]
        )
        if recipient.carrying and vessel.container and vessel.liquid:
            load = _carried_weight(world, recipient)
            weight = _vessel_weight(vessel, recipient)
            checks.append(
                Check(
                    "Recipient capacity including vessel",
                    load + weight <= recipient.carrying.capacity_weight,
                    load + weight,
                    recipient.carrying.capacity_weight,
                )
            )
        else:
            checks.append(Check("Recipient capacity can be evaluated", False))
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, GiveAction):
            raise TypeError("give rule requires GiveAction")
        vessel = world.entities[action.vessel_id]
        assert vessel.ownership
        vessel.ownership.owner_ref = f"actor:{action.target_actor_id}"
        vessel.last_cause_event_id = event_id
