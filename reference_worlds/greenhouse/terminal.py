"""Derived completion predicate for the Greenhouse world."""

from __future__ import annotations

from world_substrate.model import World


def garden_complete(world: World) -> bool:
    plants = [
        entity.component("plant")
        for entity in world.entities.values()
        if entity.component("plant") is not None
    ]
    return bool(plants) and all(plant.stage == "watered" for plant in plants)
