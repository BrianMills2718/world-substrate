"""Build the kitchen world through the shared substrate."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from world_substrate.engine import Engine
from world_substrate.model import (
    Entity,
    LocationState,
    OwnershipState,
    PortableState,
    World,
)
from world_substrate.rules import RuleRegistry

from .components import BurnerState, CookState, IngredientState, OrderState, ToolState
from .mechanics import (
    BurnerFreeProcess,
    ChopRule,
    CookRule,
    PlateRule,
    PutDownRule,
    TakeRule,
)

CONTENT = "reference_worlds/kitchen/service-v0.json"
_TYPES = {
    "cook": CookState,
    "order": OrderState,
    "ingredient": IngredientState,
    "kitchen_tool": ToolState,
    "burner": BurnerState,
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_registry() -> RuleRegistry:
    registry = RuleRegistry()
    registry.register_action(TakeRule())
    registry.register_action(ChopRule())
    registry.register_action(CookRule())
    registry.register_action(PlateRule())
    registry.register_action(PutDownRule())
    registry.register_process(BurnerFreeProcess())
    return registry


def build_engine(root: Path | None = None) -> Engine:
    root = root or repository_root()
    content = json.loads((root / CONTENT).read_text())
    entities: dict[str, Entity] = {}
    for row in content["entities"]:
        components: dict[str, Any] = {
            name: _TYPES[name](**fields)
            for name, fields in (row.get("components") or {}).items()
        }
        entity = Entity(
            entity_id=row["entity_id"],
            label=row["label"],
            category_ids=tuple(row["category_ids"]),
            location=LocationState(**row["location"]) if row.get("location") else None,
            ownership=(
                OwnershipState(**row["ownership"]) if row.get("ownership") else None
            ),
            portable=PortableState(**row["portable"]) if row.get("portable") else None,
            source_pack_id=content["content_id"],
            source_entity_id=row["entity_id"],
            components=components,
        )
        entities[entity.entity_id] = entity
    registry = build_registry()
    world = World(
        world_id=content["world_id"],
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id=content["content_id"],
        rule_versions=registry.versions(),
    )
    return Engine(world, registry)
