"""Typed canonical state records for the first neutral vertical."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ActorState:
    health: int
    hydration: int
    alive: bool = True


@dataclass
class LocationState:
    location_id: str


@dataclass
class OwnershipState:
    owner_ref: str


@dataclass
class ConditionState:
    value: int


@dataclass
class ContainerState:
    definition_id: str
    capacity_ml: int
    empty_weight: int
    boiling_ticks: int = 0
    heat_source_id: str | None = None


@dataclass
class LiquidState:
    volume_ml: int = 0
    salt_mg: int = 0
    pathogens: int = 0
    heat_units: int = 0

    def as_dict(self) -> dict[str, int]:
        return asdict(self)


@dataclass
class ThermalState:
    temperature_c: int | float


@dataclass
class Entity:
    entity_id: str
    label: str
    category_ids: tuple[str, ...]
    actor: ActorState | None = None
    location: LocationState | None = None
    ownership: OwnershipState | None = None
    condition: ConditionState | None = None
    container: ContainerState | None = None
    liquid: LiquidState | None = None
    thermal: ThermalState | None = None
    source_pack_id: str | None = None
    source_entity_id: str | None = None
    last_cause_event_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "entity_id": self.entity_id,
            "label": self.label,
            "category_ids": list(self.category_ids),
        }
        for name in (
            "actor",
            "location",
            "ownership",
            "condition",
            "container",
            "liquid",
            "thermal",
        ):
            value = getattr(self, name)
            if value is not None:
                result[name] = asdict(value)
        if self.source_pack_id is not None:
            result["source_pack_id"] = self.source_pack_id
        if self.source_entity_id is not None:
            result["source_entity_id"] = self.source_entity_id
        if self.last_cause_event_id is not None:
            result["last_cause_event_id"] = self.last_cause_event_id
        return result


@dataclass
class World:
    world_id: str
    revision: int
    tick: int
    entities: dict[str, Entity]
    engine_id: str
    content_id: str
    rule_versions: dict[str, str]
    commands: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def material_dict(self) -> dict[str, Any]:
        return {
            "world_id": self.world_id,
            "revision": self.revision,
            "tick": self.tick,
            "entities": {
                key: self.entities[key].as_dict() for key in sorted(self.entities)
            },
            "engine_id": self.engine_id,
            "content_id": self.content_id,
            "rule_versions": dict(sorted(self.rule_versions.items())),
        }

    def material_hash(self) -> str:
        encoded = json.dumps(
            self.material_dict(), sort_keys=True, separators=(",", ":")
        ).encode()
        return hashlib.sha256(encoded).hexdigest()

    def clone(self) -> World:
        return deepcopy(self)

    def validate(self) -> None:
        if self.revision < 0 or self.tick < 0:
            raise ValueError("revision and tick must be nonnegative")
        for entity_id, entity in self.entities.items():
            if entity_id != entity.entity_id:
                raise ValueError(f"entity key does not match identity: {entity_id}")
            if entity.actor is not None:
                if not 0 <= entity.actor.health <= 100:
                    raise ValueError(f"health out of range: {entity_id}")
                if not 0 <= entity.actor.hydration <= 100:
                    raise ValueError(f"hydration out of range: {entity_id}")
                if entity.actor.alive != (entity.actor.health > 0):
                    raise ValueError(f"alive flag disagrees with health: {entity_id}")
            if entity.condition is not None and not 0 <= entity.condition.value <= 100:
                raise ValueError(f"condition out of range: {entity_id}")
            if entity.liquid is not None:
                values = entity.liquid.as_dict()
                if any(
                    type(value) is not int or value < 0 for value in values.values()
                ):
                    raise ValueError(
                        f"liquid fields must be nonnegative integers: {entity_id}"
                    )
                if entity.liquid.volume_ml == 0 and entity.liquid.heat_units != 0:
                    raise ValueError(f"empty liquid cannot retain heat: {entity_id}")
            if entity.container is not None:
                if entity.container.capacity_ml <= 0:
                    raise ValueError(
                        f"container capacity must be positive: {entity_id}"
                    )
                if entity.liquid is None:
                    raise ValueError(f"container lacks liquid state: {entity_id}")
                if entity.liquid.volume_ml > entity.container.capacity_ml:
                    raise ValueError(f"container exceeds capacity: {entity_id}")


def differences(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    """Return deterministic leaf-level changes between two material projections."""
    if isinstance(before, dict) and isinstance(after, dict):
        result: list[dict[str, Any]] = []
        for key in sorted(before.keys() | after.keys()):
            child = f"{path}.{key}".strip(".")
            result.extend(differences(before.get(key), after.get(key), child))
        return result
    if before == after:
        return []
    return [{"path": path, "before": deepcopy(before), "after": deepcopy(after)}]
