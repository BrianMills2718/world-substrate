"""First-class information representation and actor-visible delivery semantics.

Information is canonical only when a world chooses to represent it. Delivery is
separate from private cognition and from hard mechanical causal ancestry: an
actor may receive a representation without that representation automatically
becoming the cause of every later action.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import Entity, World, register_component

DELIVERED_STATUSES = frozenset({"delivered", "observed"})
INFORMATION_VISIBILITIES = frozenset({"direct", "public"})


@dataclass
class InformationState:
    """A represented information item in canonical world state."""

    content: str
    source_id: str
    channel_id: str
    visibility: str = "direct"
    topic: str = ""
    derived_from_info_id: str | None = None
    active: bool = False


@dataclass
class DeliveryState:
    """Delivery lineage for one information item and one recipient."""

    info_id: str
    recipient_id: str
    channel_id: str
    status: str = "pending"
    delivered_tick: int | None = None


register_component("information", InformationState)
register_component("delivery", DeliveryState)


def _delivery_rows(world: World, info_id: str) -> list[Entity]:
    return [
        entity
        for entity in world.entities.values()
        if (delivery := entity.component("delivery")) is not None
        and delivery.info_id == info_id
    ]


def information_visible_to_actor(world: World, actor_id: str, entity: Entity) -> bool:
    """Whether an information entity belongs in an actor-authorized observation."""

    info = entity.component("information")
    if info is None:
        raise ValueError("entity has no information component")
    if info.visibility not in INFORMATION_VISIBILITIES:
        return False
    # A represented source may inspect its own draft/unsent item. Recipients do
    # not see it until delivery makes the representation active.
    if info.source_id == actor_id:
        return True
    if not info.active:
        return False
    if info.visibility == "public":
        return True
    return any(
        delivery.recipient_id == actor_id and delivery.status in DELIVERED_STATUSES
        for row in _delivery_rows(world, entity.entity_id)
        if (delivery := row.component("delivery")) is not None
    )


def delivery_visible_to_actor(world: World, actor_id: str, entity: Entity) -> bool:
    """Delivery records are visible to their recipient and represented source."""

    delivery = entity.component("delivery")
    if delivery is None:
        raise ValueError("entity has no delivery component")
    if delivery.recipient_id == actor_id and delivery.status in DELIVERED_STATUSES:
        return True
    info_entity = world.entities.get(delivery.info_id)
    if info_entity is None:
        return False
    info = info_entity.component("information")
    return bool(info is not None and info.source_id == actor_id)


def entity_visible_to_actor(world: World, actor_id: str, entity: Entity) -> bool:
    """Apply only information-specific visibility; other entities pass through."""

    if entity.component("information") is not None:
        return information_visible_to_actor(world, actor_id, entity)
    if entity.component("delivery") is not None:
        return delivery_visible_to_actor(world, actor_id, entity)
    return True


def information_visible_in_material_world(
    material_world: dict[str, Any], actor_id: str, info_id: str
) -> bool:
    """Apply canonical information-delivery visibility to a material projection.

    This is the dict/projection counterpart of :func:`information_visible_to_actor`.
    It exists so read-only clients can enforce the same represented visibility
    boundary without reconstructing a mutable ``World`` instance.
    """

    entities = material_world.get("entities")
    if not isinstance(entities, dict):
        return False
    entity = entities.get(info_id)
    if not isinstance(entity, dict):
        return False
    components = entity.get("components")
    if not isinstance(components, dict):
        return False
    info = components.get("information")
    if not isinstance(info, dict):
        return False
    visibility = info.get("visibility")
    if visibility not in INFORMATION_VISIBILITIES:
        return False
    if info.get("source_id") == actor_id:
        return True
    if info.get("active") is not True:
        return False
    if visibility == "public":
        return True
    for row in entities.values():
        if not isinstance(row, dict):
            continue
        row_components = row.get("components")
        delivery = row_components.get("delivery") if isinstance(row_components, dict) else None
        if (
            isinstance(delivery, dict)
            and delivery.get("info_id") == info_id
            and delivery.get("recipient_id") == actor_id
            and delivery.get("status") in DELIVERED_STATUSES
        ):
            return True
    return False


def observation_information_context(observation: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Summarize represented information present in a retained actor observation.

    This is cognition *context evidence*, not a causal attribution.
    """

    if not observation:
        return []
    rows: list[dict[str, Any]] = []
    entities = observation.get("entities")
    if not isinstance(entities, dict):
        return rows
    for entity_id, record in sorted(entities.items()):
        if not isinstance(record, dict):
            continue
        components = record.get("components")
        if not isinstance(components, dict):
            continue
        info = components.get("information")
        if isinstance(info, dict) and info.get("active") is True:
            rows.append(
                {
                    "info_id": entity_id,
                    "source_id": info.get("source_id"),
                    "channel_id": info.get("channel_id"),
                    "topic": info.get("topic"),
                    "content": info.get("content"),
                }
            )
    return rows
