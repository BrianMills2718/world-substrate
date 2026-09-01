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
class CarryingState:
    capacity_weight: int
    liquid_ml_per_weight: int = 250


@dataclass
class PortableState:
    portable: bool = True


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
class MaterialState:
    material_id: str
    heat_limit_c: int
    heat_transfer_percent: int
    overheat_damage_per_tick: int
    open_top: bool = True


@dataclass
class HeatSourceState:
    fuel: int
    heat_units_per_tick: int
    heat_slots: int


@dataclass
class PhysicalLedger:
    initial: LiquidState = field(default_factory=LiquidState)
    added: LiquidState = field(default_factory=LiquidState)
    drunk: LiquidState = field(default_factory=LiquidState)
    evaporated: LiquidState = field(default_factory=LiquidState)
    pathogens_killed: int = 0
    heat_added: int = 0
    heat_lost: int = 0
    latent_heat_used: int = 0
    spilled_ml: int = 0
    overflow_ml: int = 0

    def semantic_deltas(self) -> dict[str, object]:
        return {
            "evaporated": self.evaporated.as_dict(),
            "pathogens_killed": self.pathogens_killed,
            "heat_added": self.heat_added,
            "heat_lost": self.heat_lost,
            "latent_heat_used": self.latent_heat_used,
            "drunk": self.drunk.as_dict(),
        }


@dataclass
class Entity:
    entity_id: str
    label: str
    category_ids: tuple[str, ...]
    actor: ActorState | None = None
    carrying: CarryingState | None = None
    portable: PortableState | None = None
    location: LocationState | None = None
    ownership: OwnershipState | None = None
    condition: ConditionState | None = None
    container: ContainerState | None = None
    liquid: LiquidState | None = None
    thermal: ThermalState | None = None
    material: MaterialState | None = None
    heat_source: HeatSourceState | None = None
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
            "carrying",
            "portable",
            "location",
            "ownership",
            "condition",
            "container",
            "liquid",
            "thermal",
            "material",
            "heat_source",
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
    physical_ledger: PhysicalLedger | None = None
    commands: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def material_dict(self) -> dict[str, Any]:
        result = {
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
        if self.physical_ledger is not None:
            result["physical_ledger"] = asdict(self.physical_ledger)
        return result

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
            if entity.carrying is not None:
                if entity.carrying.capacity_weight < 0:
                    raise ValueError(f"carrying capacity is negative: {entity_id}")
                if entity.carrying.liquid_ml_per_weight <= 0:
                    raise ValueError(f"liquid carrying divisor is invalid: {entity_id}")
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
            if entity.material is not None:
                if not 0 <= entity.material.heat_transfer_percent <= 100:
                    raise ValueError(f"invalid heat transfer percent: {entity_id}")
                if entity.material.heat_limit_c <= 0:
                    raise ValueError(f"invalid heat limit: {entity_id}")
            if entity.heat_source is not None:
                if entity.heat_source.fuel < 0:
                    raise ValueError(f"heat source fuel is negative: {entity_id}")
                if entity.heat_source.heat_units_per_tick <= 0:
                    raise ValueError(f"heat source power must be positive: {entity_id}")
                if entity.heat_source.heat_slots <= 0:
                    raise ValueError(f"heat source slots must be positive: {entity_id}")
        if self.physical_ledger is not None:
            values = asdict(self.physical_ledger)
            for key, value in values.items():
                if isinstance(value, dict):
                    if any(type(item) is not int or item < 0 for item in value.values()):
                        raise ValueError(f"physical ledger {key} must be nonnegative")
                elif type(value) is not int or value < 0:
                    raise ValueError(f"physical ledger {key} must be nonnegative")


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
