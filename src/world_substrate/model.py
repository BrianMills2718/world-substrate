"""Typed canonical state records for the first neutral vertical."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any

# --- Ownership references ---------------------------------------------------
#
# `owner_ref` encodes a kind and a target: "actor:robinson", "place:camp",
# "assembly:frame-a". Until M7 that convention lived only in the eighteen
# f-strings that built it, so every layer treated it as a bare string: the type
# system, the engine's write-scope guard, World.validate() and the mechanic
# installer all accepted "" as a valid owner. Two of nine mechanics authored by
# a model in the M7 experiment set exactly that, destroying the attachment
# provenance AttachRule establishes, and nothing caught it.
#
# The wire format is unchanged -- the same prefixed string, so every pinned
# receipt still matches byte for byte. What changed is that the shape is now
# enforced, and code asks for a reference instead of formatting one by hand.

OWNER_REF_PATTERN = re.compile(r"^[a-z][a-z0-9_]*:[A-Za-z0-9._\-]+$")

# Held by nobody. Making `owner_ref` a checked reference correctly refused the
# empty string, and left an author with no way to say what two of ten M7b
# proposals meant: a tool worn past its limit should leave the worker's hands.
# The refusal made a missing capability visible without supplying one (M7b
# finding).
#
# A reserved literal rather than a `<kind>:<target>` form, because there is no
# target -- and because every consumer compares against a reference it built
# itself, so "unowned" matches none of them by construction and no consumer
# needed changing. It is also expressible by the declaration language, which
# can set a string on a field and nothing more.
UNOWNED = "unowned"


def is_owned(reference: str) -> bool:
    """Whether an ownership reference names an owner at all."""
    return reference != UNOWNED


def owner_ref(kind: str, target: str) -> str:
    """Build an ownership reference, refusing a malformed one at the source."""
    reference = f"{kind}:{target}"
    if not OWNER_REF_PATTERN.match(reference):
        raise ValueError(f"invalid ownership reference: {reference!r}")
    return reference


def parse_owner_ref(reference: str) -> tuple[str, str]:
    """Split an ownership reference into (kind, target).

    Unowned parses as ``("unowned", "")``: it is a valid reference that names
    no owner, which is different from a malformed one.
    """
    if reference == UNOWNED:
        return UNOWNED, ""
    if not OWNER_REF_PATTERN.match(reference):
        raise ValueError(f"invalid ownership reference: {reference!r}")
    kind, _, target = reference.partition(":")
    return kind, target


SNAPSHOT_SCHEMA_VERSION = "world-substrate-snapshot/v1"


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


# --- Open typed components -------------------------------------------------
#
# The eleven component fields above were extracted from Castaway and are the
# freshwater world's content, not substrate law. A materially different world
# needs its own components, and before M6 there was no way to add one: Entity
# rejected unknown fields and silently dropped ad-hoc attributes.
#
# This registry keeps components typed while opening the set. A world pack
# registers its dataclasses at import time and refers to them by name. Nothing
# about the original eleven changes, and an entity with no registered
# components serialises byte-identically to before, so pinned M1 evidence and
# donor parity are untouched.

COMPONENT_TYPES: dict[str, type] = {}


def register_component(name: str, component_type: type) -> None:
    """Register a typed component a world pack may attach to its entities."""
    if not name or not name.replace("_", "").isalnum():
        raise ValueError(f"component name must be alphanumeric: {name!r}")
    existing = COMPONENT_TYPES.get(name)
    if existing is not None and existing is not component_type:
        raise ValueError(f"component {name!r} is already registered to {existing}")
    if name in _BUILTIN_COMPONENT_NAMES:
        raise ValueError(f"{name!r} is a built-in component field")
    COMPONENT_TYPES[name] = component_type


# The eleven Castaway-derived components, by name. Kept as one mapping rather
# than a name set plus a parallel dict inside `Entity.from_dict`, because the
# authoring path needs to resolve a declared path to the dataclass that owns
# the field -- and a second copy of this list is exactly how a checker ends up
# blind to a component nobody remembered to add to it.
BUILTIN_COMPONENT_TYPES: dict[str, type] = {
    "actor": ActorState,
    "carrying": CarryingState,
    "portable": PortableState,
    "location": LocationState,
    "ownership": OwnershipState,
    "condition": ConditionState,
    "container": ContainerState,
    "liquid": LiquidState,
    "thermal": ThermalState,
    "material": MaterialState,
    "heat_source": HeatSourceState,
}

_BUILTIN_COMPONENT_NAMES = frozenset(BUILTIN_COMPONENT_TYPES)


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
    components: dict[str, Any] = field(default_factory=dict)

    def component(self, name: str) -> Any:
        """Return a registered component, or None."""
        return self.components.get(name)

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
        # Omitted entirely when empty, so a world that registers no components
        # serialises exactly as it did before this existed.
        if self.components:
            result["components"] = {
                name: asdict(self.components[name])
                for name in sorted(self.components)
            }
        return result

    @classmethod
    def from_dict(cls, value: object) -> Entity:
        if not isinstance(value, dict):
            raise TypeError("snapshot entity must be an object")
        entity_id = value.get("entity_id")
        label = value.get("label")
        category_ids = value.get("category_ids")
        if not isinstance(entity_id, str) or not entity_id:
            raise ValueError("snapshot entity_id must be a nonempty string")
        if not isinstance(label, str) or not label:
            raise ValueError("snapshot entity label must be a nonempty string")
        if not isinstance(category_ids, list) or any(
            not isinstance(item, str) or not item for item in category_ids
        ):
            raise ValueError("snapshot category_ids must be nonempty strings")

        component_types: dict[str, type[Any]] = dict(BUILTIN_COMPONENT_TYPES)
        components: dict[str, Any] = {}
        for name, component_type in component_types.items():
            record = value.get(name)
            if record is None:
                components[name] = None
                continue
            if not isinstance(record, dict):
                raise TypeError(f"snapshot {name} component must be an object")
            try:
                components[name] = component_type(**record)
            except TypeError as error:
                raise ValueError(f"invalid snapshot {name} component: {error}") from error

        optional_identities: dict[str, str | None] = {}
        for name in ("source_pack_id", "source_entity_id", "last_cause_event_id"):
            item = value.get(name)
            if item is not None and (not isinstance(item, str) or not item):
                raise ValueError(f"snapshot {name} must be a nonempty string or null")
            optional_identities[name] = item
        registered: dict[str, Any] = {}
        record = value.get("components")
        if record is not None:
            if not isinstance(record, dict):
                raise TypeError("snapshot components must be an object")
            for name, fields in sorted(record.items()):
                component_type = COMPONENT_TYPES.get(name)
                if component_type is None:
                    raise ValueError(f"unregistered component: {name!r}")
                if not isinstance(fields, dict):
                    raise TypeError(f"snapshot component {name} must be an object")
                try:
                    registered[name] = component_type(**fields)
                except TypeError as error:
                    raise ValueError(f"invalid snapshot component {name}: {error}") from error

        allowed = {
            "entity_id",
            "label",
            "category_ids",
            "components",
            *component_types,
            *optional_identities,
        }
        unknown = sorted(set(value) - allowed)
        if unknown:
            raise ValueError(f"unknown snapshot entity fields: {unknown}")
        return cls(
            entity_id=entity_id,
            label=label,
            category_ids=tuple(category_ids),
            actor=components["actor"],
            carrying=components["carrying"],
            portable=components["portable"],
            location=components["location"],
            ownership=components["ownership"],
            condition=components["condition"],
            container=components["container"],
            liquid=components["liquid"],
            thermal=components["thermal"],
            material=components["material"],
            heat_source=components["heat_source"],
            source_pack_id=optional_identities["source_pack_id"],
            source_entity_id=optional_identities["source_entity_id"],
            last_cause_event_id=optional_identities["last_cause_event_id"],
            components=registered,
        )


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

    def snapshot(self) -> dict[str, Any]:
        """Return a versioned JSON-serializable canonical-state snapshot."""
        return {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "world": deepcopy(self.material_dict()),
        }

    @classmethod
    def from_snapshot(cls, snapshot: object) -> World:
        """Load canonical state from a versioned snapshot without command history."""
        if not isinstance(snapshot, dict):
            raise TypeError("snapshot must be an object")
        if set(snapshot) != {"schema_version", "world"}:
            raise ValueError("snapshot must contain only schema_version and world")
        if snapshot.get("schema_version") != SNAPSHOT_SCHEMA_VERSION:
            raise ValueError("unsupported snapshot schema_version")
        value = snapshot.get("world")
        if not isinstance(value, dict):
            raise TypeError("snapshot world must be an object")
        required = {
            "world_id",
            "revision",
            "tick",
            "entities",
            "engine_id",
            "content_id",
            "rule_versions",
        }
        optional = {"physical_ledger"}
        missing = sorted(required - set(value))
        unknown = sorted(set(value) - required - optional)
        if missing:
            raise ValueError(f"snapshot world is missing fields: {missing}")
        if unknown:
            raise ValueError(f"unknown snapshot world fields: {unknown}")
        for field_name in ("world_id", "engine_id", "content_id"):
            item = value[field_name]
            if not isinstance(item, str) or not item:
                raise ValueError(f"snapshot {field_name} must be a nonempty string")
        for field_name in ("revision", "tick"):
            if type(value[field_name]) is not int:
                raise ValueError(f"snapshot {field_name} must be an integer")
        entities_record = value["entities"]
        if not isinstance(entities_record, dict):
            raise TypeError("snapshot entities must be an object")
        entities = {
            entity_id: Entity.from_dict(record)
            for entity_id, record in entities_record.items()
        }
        versions = value["rule_versions"]
        if not isinstance(versions, dict) or any(
            not isinstance(rule_id, str)
            or not rule_id
            or not isinstance(version, str)
            or not version
            for rule_id, version in versions.items()
        ):
            raise ValueError("snapshot rule_versions must map strings to strings")

        ledger_record = value.get("physical_ledger")
        ledger = None
        if ledger_record is not None:
            if not isinstance(ledger_record, dict):
                raise ValueError("snapshot physical_ledger must be an object")
            ledger_values = deepcopy(ledger_record)
            for name in ("initial", "added", "drunk", "evaporated"):
                item = ledger_values.get(name)
                if not isinstance(item, dict):
                    raise TypeError(
                        f"snapshot physical_ledger.{name} must be an object"
                    )
                try:
                    ledger_values[name] = LiquidState(**item)
                except TypeError as error:
                    raise ValueError(
                        f"invalid snapshot physical_ledger.{name}: {error}"
                    ) from error
            try:
                ledger = PhysicalLedger(**ledger_values)
            except TypeError as error:
                raise ValueError(f"invalid snapshot physical_ledger: {error}") from error

        world = cls(
            world_id=value["world_id"],
            revision=value["revision"],
            tick=value["tick"],
            entities=entities,
            engine_id=value["engine_id"],
            content_id=value["content_id"],
            rule_versions=dict(versions),
            physical_ledger=ledger,
        )
        world.validate()
        return world

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
            if entity.ownership is not None and not (
                entity.ownership.owner_ref == UNOWNED
                or OWNER_REF_PATTERN.match(entity.ownership.owner_ref)
            ):
                raise ValueError(
                    f"invalid ownership reference on {entity_id}: "
                    f"{entity.ownership.owner_ref!r}"
                )
            # An identifier the substrate resolves against must actually name
            # something. `owner_ref` got this check when M7 found a mechanic
            # blanking it; the other identifier fields did not, and they fail
            # far more quietly. An emptied `location_id` keeps validating,
            # keeps round-tripping through a snapshot, and removes the entity
            # from every observation -- nothing shares a location with it any
            # more, so no policy can see or act on it and nothing reports why.
            for holder, field_name in (
                (entity.location, "location_id"),
                (entity.container, "definition_id"),
                (entity.container, "heat_source_id"),
                (entity.material, "material_id"),
            ):
                if holder is None:
                    continue
                value = getattr(holder, field_name)
                if value is None:
                    continue
                if not isinstance(value, str) or not value:
                    raise ValueError(
                        f"{field_name} on {entity_id} must be a nonempty "
                        f"string: {value!r}"
                    )
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
