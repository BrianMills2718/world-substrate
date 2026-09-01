"""Registered time and actor-maintenance processes for the first probe."""

from __future__ import annotations

from ..model import World


class ClockAdvanceProcess:
    rule_id = "system.clock.advance"
    version = "1"
    order = 0
    read_paths: tuple[str, ...] = ("tick",)
    write_paths: tuple[str, ...] = ("tick",)

    def due(self, world: World) -> bool:
        return True

    def apply(self, world: World) -> None:
        world.tick += 1


class HydrationDecayProcess:
    rule_id = "process.actor.hydration-decay"
    version = "1"
    order = 10
    read_paths: tuple[str, ...] = ("entities.<actor>.actor.hydration",)
    write_paths: tuple[str, ...] = ("entities.<actor>.actor.hydration",)

    def due(self, world: World) -> bool:
        return True

    def apply(self, world: World) -> None:
        for entity in world.entities.values():
            if entity.actor is not None and entity.actor.alive:
                entity.actor.hydration = max(0, entity.actor.hydration - 1)
