"""Workshop mechanics: pick up, attach, detach, and wear.

Written against the shared rule protocols without modifying them. None of the
Castaway mechanics were reusable here, and the reason is specific rather than
aesthetic: `mechanisms.ownership` computes carrying capacity from liquid volume
(`_vessel_weight` divides `liquid.volume_ml`), so `take` and `give` cannot move
a bolt. See docs/audits/m6-second-world.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from world_substrate.model import World, owner_ref, parse_owner_ref
from world_substrate.rules import Check, TypedAction, _require_nonempty_string


def _held_by(world: World, actor_id: str) -> list[str]:
    return sorted(
        entity.entity_id
        for entity in world.entities.values()
        if entity.ownership is not None
        and entity.ownership.owner_ref == owner_ref("actor", actor_id)
    )


@dataclass(frozen=True)
class PickUpAction:
    actor_id: str
    item_id: str
    base_revision: int
    controller_id: str
    kind: str = "pick_up"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "item": self.item_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PickUpAction:
        if value.get("kind") != "pick_up":
            raise ValueError("record is not a pick_up action")
        item = value["item"]
        if not isinstance(item, str) or not item:
            raise TypeError("item must be a nonempty string")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            item_id=item,
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class AttachAction:
    actor_id: str
    part_id: str
    assembly_id: str
    base_revision: int
    controller_id: str
    kind: str = "attach"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "part": self.part_id,
            "assembly": self.assembly_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> AttachAction:
        if value.get("kind") != "attach":
            raise ValueError("record is not an attach action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            part_id=_require_nonempty_string(value, "part"),
            assembly_id=_require_nonempty_string(value, "assembly"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


class PickUpRule:
    rule_id = "workshop.inventory.pick-up"
    version = "1"
    action_kind = "pick_up"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<actor>.components.worker",
        "entities.<item>.location",
        "entities.<item>.ownership",
        "entities.<item>.portable",
        "entities.<item>.components.part",
    )
    write_paths: tuple[str, ...] = (
        "entities.<item>.ownership.owner_ref",
        "entities.<item>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> PickUpAction:
        return PickUpAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.location is None:
            return []
        return [
            PickUpAction(actor_id, entity.entity_id, world.revision, "unselected")
            for entity in sorted(world.entities.values(), key=lambda i: i.entity_id)
            if entity.portable is not None
            and entity.ownership is not None
            and entity.location is not None
            and entity.location.location_id == actor.location.location_id
            and entity.ownership.owner_ref != owner_ref("actor", actor_id)
            and not (
                entity.component("part") and entity.component("part").attached_to
            )
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        assert isinstance(action, PickUpAction)
        actor = world.entities.get(action.actor_id)
        item = world.entities.get(action.item_id)
        checks = [
            Check("Worker exists", actor is not None and actor.location is not None),
            Check("Item exists", item is not None),
        ]
        if actor is None or item is None:
            return checks
        part = item.component("part")
        checks.extend(
            [
                Check("Item is portable", bool(item.portable and item.portable.portable)),
                Check(
                    "Item is here",
                    bool(
                        item.location
                        and actor.location
                        and item.location.location_id == actor.location.location_id
                    ),
                ),
                Check("Item is not already attached", not (part and part.attached_to)),
                Check(
                    "Item is not already held",
                    bool(
                        item.ownership
                        and item.ownership.owner_ref != owner_ref("actor", action.actor_id)
                    ),
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, PickUpAction)
        item = world.entities[action.item_id]
        assert item.ownership
        item.ownership.owner_ref = owner_ref("actor", action.actor_id)
        item.last_cause_event_id = event_id


class AttachRule:
    rule_id = "workshop.assembly.attach"
    version = "1"
    action_kind = "attach"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<actor>.components.worker",
        "entities.<part>.ownership",
        "entities.<part>.components.part",
        "entities.<assembly>.location",
        "entities.<assembly>.components.assembly",
        "entities.<tool>.ownership",
        "entities.<tool>.components.tool",
    )
    write_paths: tuple[str, ...] = (
        "entities.<part>.components.part.attached_to",
        "entities.<part>.ownership.owner_ref",
        "entities.<part>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> AttachAction:
        return AttachAction.from_dict(value)

    def _held_tool_kinds(self, world: World, actor_id: str) -> set[str]:
        return {
            world.entities[item].component("tool").tool_kind
            for item in _held_by(world, actor_id)
            if world.entities[item].component("tool") is not None
            and world.entities[item].component("tool").wear
            < world.entities[item].component("tool").wear_limit
        }

    def _filled_kinds(self, world: World, assembly_id: str) -> list[str]:
        return sorted(
            entity.component("part").part_kind
            for entity in world.entities.values()
            if entity.component("part")
            and entity.component("part").attached_to == assembly_id
        )

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.location is None:
            return []
        assemblies = [
            entity
            for entity in sorted(world.entities.values(), key=lambda i: i.entity_id)
            if entity.component("assembly")
            and entity.location
            and entity.location.location_id == actor.location.location_id
        ]
        held_parts = [
            world.entities[item]
            for item in _held_by(world, actor_id)
            if world.entities[item].component("part")
            and not world.entities[item].component("part").attached_to
        ]
        return [
            AttachAction(
                actor_id, part.entity_id, assembly.entity_id, world.revision, "unselected"
            )
            for assembly in assemblies
            for part in held_parts
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        assert isinstance(action, AttachAction)
        actor = world.entities.get(action.actor_id)
        part_entity = world.entities.get(action.part_id)
        assembly_entity = world.entities.get(action.assembly_id)
        checks = [
            Check("Worker exists", actor is not None and actor.location is not None),
            Check(
                "Part exists",
                part_entity is not None and part_entity.component("part") is not None,
            ),
            Check(
                "Assembly exists",
                assembly_entity is not None
                and assembly_entity.component("assembly") is not None,
            ),
        ]
        if actor is None or part_entity is None or assembly_entity is None:
            return checks
        part = part_entity.component("part")
        assembly = assembly_entity.component("assembly")
        if part is None or assembly is None:
            return checks
        filled = self._filled_kinds(world, action.assembly_id)
        checks.extend(
            [
                Check("Worker holds the part", bool(
                    part_entity.ownership
                    and part_entity.ownership.owner_ref == owner_ref("actor", action.actor_id)
                )),
                Check("Part is not already attached", part.attached_to is None),
                Check(
                    "Assembly is here",
                    bool(
                        assembly_entity.location
                        and actor.location
                        and assembly_entity.location.location_id
                        == actor.location.location_id
                    ),
                ),
                Check(
                    "Assembly needs this part kind",
                    part.part_kind in assembly.required_kinds,
                    part.part_kind,
                    list(assembly.required_kinds),
                ),
                Check(
                    "That slot is still open",
                    filled.count(part.part_kind)
                    < list(assembly.required_kinds).count(part.part_kind),
                    filled,
                    list(assembly.required_kinds),
                ),
                Check(
                    "Worker holds a usable required tool",
                    not assembly.requires_tool
                    or assembly.requires_tool
                    in self._held_tool_kinds(world, action.actor_id),
                    sorted(self._held_tool_kinds(world, action.actor_id)),
                    assembly.requires_tool,
                ),
            ]
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, AttachAction)
        part_entity = world.entities[action.part_id]
        part = part_entity.component("part")
        assert part is not None and part_entity.ownership is not None
        part.attached_to = action.assembly_id
        part_entity.ownership.owner_ref = owner_ref("assembly", action.assembly_id)
        part_entity.last_cause_event_id = event_id


class ToolWearProcess:
    rule_id = "workshop.process.tool-wear"
    version = "1"
    order = 20
    read_paths: tuple[str, ...] = (
        "entities.<tool>.components.tool",
        "entities.<tool>.ownership",
    )
    write_paths: tuple[str, ...] = ("entities.<tool>.components.tool.wear",)

    def _in_use(self, world: World, entity) -> bool:
        tool = entity.component("tool")
        return (
            tool is not None
            and entity.ownership is not None
            # Read the reference through the parser rather than matching its
            # prefix by hand. `startswith("actor:")` is the same convention-in-
            # a-string shape M7 found in `owner_ref` itself, and it silently
            # treats any future kind beginning "actor" as a holder.
            and parse_owner_ref(entity.ownership.owner_ref)[0] == "actor"
            and tool.wear < tool.wear_limit
        )

    def due(self, world: World) -> bool:
        return any(self._in_use(world, e) for e in world.entities.values())

    def apply(self, world: World) -> None:
        for entity in sorted(world.entities.values(), key=lambda i: i.entity_id):
            if self._in_use(world, entity):
                tool = entity.component("tool")
                tool.wear = min(tool.wear_limit, tool.wear + 7)


class FatigueProcess:
    rule_id = "workshop.process.fatigue"
    version = "1"
    order = 10
    read_paths: tuple[str, ...] = ("entities.<actor>.components.worker",)
    write_paths: tuple[str, ...] = ("entities.<actor>.components.worker.fatigue",)

    def due(self, world: World) -> bool:
        return any(e.component("worker") for e in world.entities.values())

    def apply(self, world: World) -> None:
        for entity in world.entities.values():
            worker = entity.component("worker")
            if worker is not None:
                worker.fatigue = min(100, worker.fatigue + 3)
