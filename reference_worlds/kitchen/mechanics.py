"""Kitchen mechanics: take, chop, cook, plate, and a burner that frees itself.

Each stage needs a different contested resource, which is the point. Chopping
needs the one knife. Cooking needs one of two burners. Plating needs an
ingredient nobody else has already used, and there is no spare of anything.

Written against the shared rule protocols without modifying them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from world_substrate.model import World, owner_ref, parse_owner_ref
from world_substrate.rules import Check, TypedAction, _require_nonempty_string


def _holder(entity) -> str | None:
    """The actor holding this thing, if an actor holds it."""
    if entity.ownership is None:
        return None
    kind, target = parse_owner_ref(entity.ownership.owner_ref)
    return target if kind == "actor" else None


def _held_by(world: World, actor_id: str) -> list[str]:
    return sorted(
        e.entity_id for e in world.entities.values() if _holder(e) == actor_id
    )


def _order_of(world: World, actor_id: str):
    cook = world.entities[actor_id].component("cook")
    return world.entities.get(cook.order_id) if cook else None


def _outstanding(world: World, actor_id: str) -> list[str]:
    """What this cook's order still needs, after what they have plated."""
    cook = world.entities[actor_id].component("cook")
    order = _order_of(world, actor_id)
    if cook is None or order is None:
        return []
    wants = list(order.components["order"].wants)
    for done in cook.plated:
        if done in wants:
            wants.remove(done)
    return wants


def _action(kind: str, **fields):
    return {"kind": kind, **fields}


@dataclass(frozen=True)
class TakeAction:
    actor_id: str
    item_id: str
    base_revision: int
    controller_id: str
    kind: str = "take"

    def as_dict(self) -> dict[str, object]:
        return {"actor": self.actor_id, "kind": self.kind, "item": self.item_id,
                "base_revision": self.base_revision, "controller": self.controller_id}

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> TakeAction:
        if value.get("kind") != "take":
            raise ValueError("record is not a take action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            item_id=_require_nonempty_string(value, "item"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


class TakeRule:
    """Pick up the knife or an ingredient. The knife is the bottleneck."""

    rule_id = "kitchen.action.take"
    version = "1"
    action_kind = "take"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<item>.ownership.owner_ref",
        "entities.<item>.portable",
    )
    write_paths: tuple[str, ...] = ("entities.<item>.ownership.owner_ref",)

    def action_from_dict(self, value): return TakeAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or actor.component("cook") is None:
            return []
        return [
            TakeAction(actor_id, e.entity_id, world.revision, "unselected")
            for e in sorted(world.entities.values(), key=lambda x: x.entity_id)
            if e.portable is not None and _holder(e) != actor_id
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        actor = world.entities.get(action.actor_id)
        item = world.entities.get(action.item_id)
        checks = [
            Check("Cook exists", actor is not None and actor.component("cook") is not None),
            Check("Item exists and is portable",
                  item is not None and item.portable is not None),
        ]
        if actor is None or item is None:
            return checks
        held_by = _holder(item)
        checks.append(
            Check("Nobody else is holding it", held_by is None or held_by == action.actor_id,
                  held_by, "unheld")
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        item = world.entities[action.item_id]
        item.ownership.owner_ref = owner_ref("actor", action.actor_id)


@dataclass(frozen=True)
class PrepAction:
    actor_id: str
    item_id: str
    base_revision: int
    controller_id: str
    kind: str = "chop"
    station_id: str = ""
    order_id: str = ""

    def as_dict(self) -> dict[str, object]:
        record = {"actor": self.actor_id, "kind": self.kind, "item": self.item_id,
                  "base_revision": self.base_revision, "controller": self.controller_id}
        if self.station_id:
            record["burner"] = self.station_id
        if self.order_id:
            record["order"] = self.order_id
        return record


class ChopRule:
    """Raw to chopped. Needs the knife, and the knife is singular."""

    rule_id = "kitchen.action.chop"
    version = "1"
    action_kind = "chop"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.location",
        "entities.<item>.components.ingredient",
        "entities.<item>.ownership.owner_ref",
    )
    write_paths: tuple[str, ...] = ("entities.<item>.components.ingredient.stage",)

    def action_from_dict(self, value):
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        if value.get("kind") != "chop":
            raise ValueError("record is not a chop action")
        return PrepAction(
            _require_nonempty_string(value, "actor"),
            _require_nonempty_string(value, "item"),
            revision,
            _require_nonempty_string(value, "controller"),
        )

    def _knife(self, world: World):
        for e in world.entities.values():
            tool = e.component("kitchen_tool")
            if tool is not None and tool.tool_kind == "knife":
                return e
        return None

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        if world.entities.get(actor_id) is None:
            return []
        return [
            PrepAction(actor_id, e.entity_id, world.revision, "unselected")
            for e in sorted(world.entities.values(), key=lambda x: x.entity_id)
            if (i := e.component("ingredient")) is not None
            and i.stage == "raw" and not i.spoiled
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        item = world.entities.get(action.item_id)
        knife = self._knife(world)
        ingredient = item.component("ingredient") if item else None
        checks = [
            Check("Ingredient exists", ingredient is not None),
            Check("A knife exists", knife is not None),
        ]
        if ingredient is None or knife is None:
            return checks
        checks.extend([
            Check("You are holding the knife", _holder(knife) == action.actor_id,
                  _holder(knife), action.actor_id),
            Check("You are holding the ingredient", _holder(item) == action.actor_id,
                  _holder(item), action.actor_id),
            Check("It is still raw", ingredient.stage == "raw", ingredient.stage, "raw"),
            Check("It is not spoiled", not ingredient.spoiled),
        ])
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        world.entities[action.item_id].components["ingredient"].stage = "chopped"


class CookRule:
    """Chopped to cooked. Needs a free burner; there are two."""

    rule_id = "kitchen.action.cook"
    version = "1"
    action_kind = "cook"
    read_paths: tuple[str, ...] = (
        "entities.<item>.components.ingredient",
        "entities.<item>.ownership.owner_ref",
        "entities.<burner>.components.burner.occupied_by",
    )
    write_paths: tuple[str, ...] = (
        "entities.<item>.components.ingredient.stage",
        "entities.<burner>.components.burner.occupied_by",
    )

    def action_from_dict(self, value):
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        if value.get("kind") != "cook":
            raise ValueError("record is not a cook action")
        return PrepAction(
            _require_nonempty_string(value, "actor"),
            _require_nonempty_string(value, "item"),
            revision,
            _require_nonempty_string(value, "controller"),
            kind="cook",
            station_id=_require_nonempty_string(value, "burner"),
        )

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        free = [
            e.entity_id for e in sorted(world.entities.values(), key=lambda x: x.entity_id)
            if (b := e.component("burner")) is not None and not b.occupied_by
        ]
        ready = [
            e.entity_id for e in sorted(world.entities.values(), key=lambda x: x.entity_id)
            if (i := e.component("ingredient")) is not None
            and i.stage == "chopped" and not i.spoiled and _holder(e) == actor_id
        ]
        return [
            PrepAction(actor_id, item, world.revision, "unselected",
                       kind="cook", station_id=burner)
            for item in ready for burner in free[:1]
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        item = world.entities.get(action.item_id)
        burner = world.entities.get(action.station_id)
        ingredient = item.component("ingredient") if item else None
        hob = burner.component("burner") if burner else None
        checks = [
            Check("Ingredient exists", ingredient is not None),
            Check("Burner exists", hob is not None),
        ]
        if ingredient is None or hob is None:
            return checks
        checks.extend([
            Check("You are holding the ingredient", _holder(item) == action.actor_id,
                  _holder(item), action.actor_id),
            Check("It is chopped", ingredient.stage == "chopped", ingredient.stage, "chopped"),
            Check("The burner is free", not hob.occupied_by, hob.occupied_by, "free"),
        ])
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        world.entities[action.item_id].components["ingredient"].stage = "cooked"
        world.entities[action.station_id].components["burner"].occupied_by = action.actor_id


class PlateRule:
    """Put a cooked ingredient toward your own order. Only yours."""

    rule_id = "kitchen.action.plate"
    version = "1"
    action_kind = "plate"
    read_paths: tuple[str, ...] = (
        "entities.<actor>.components.cook",
        "entities.<item>.components.ingredient",
        "entities.<item>.ownership.owner_ref",
        "entities.<order>.components.order",
    )
    write_paths: tuple[str, ...] = (
        "entities.<actor>.components.cook.plated",
        "entities.<order>.components.order.filled",
        "entities.<item>.components.ingredient.stage",
    )

    def action_from_dict(self, value):
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        if value.get("kind") != "plate":
            raise ValueError("record is not a plate action")
        return PrepAction(
            _require_nonempty_string(value, "actor"),
            _require_nonempty_string(value, "item"),
            revision,
            _require_nonempty_string(value, "controller"),
            kind="plate",
            order_id=_require_nonempty_string(value, "order"),
        )

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        if world.entities.get(actor_id) is None:
            return []
        cook = world.entities[actor_id].component("cook")
        if cook is None:
            return []
        return [
            PrepAction(actor_id, e.entity_id, world.revision, "unselected",
                       kind="plate", order_id=cook.order_id)
            for e in sorted(world.entities.values(), key=lambda x: x.entity_id)
            if (i := e.component("ingredient")) is not None
            and i.stage == "cooked" and _holder(e) == actor_id
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        actor = world.entities.get(action.actor_id)
        item = world.entities.get(action.item_id)
        cook = actor.component("cook") if actor else None
        ingredient = item.component("ingredient") if item else None
        checks = [
            Check("Cook exists", cook is not None),
            Check("Ingredient exists", ingredient is not None),
        ]
        if cook is None or ingredient is None:
            return checks
        wants = _outstanding(world, action.actor_id)
        checks.extend([
            Check("It is your own order", action.order_id == cook.order_id,
                  action.order_id, cook.order_id),
            Check("You are holding it", _holder(item) == action.actor_id),
            Check("It is cooked", ingredient.stage == "cooked", ingredient.stage, "cooked"),
            Check("Your order still wants this", ingredient.kind in wants,
                  ingredient.kind, wants),
        ])
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        actor = world.entities[action.actor_id]
        item = world.entities[action.item_id]
        cook = actor.components["cook"]
        cook.plated = [*cook.plated, item.components["ingredient"].kind]
        item.components["ingredient"].stage = "plated"
        order = world.entities[action.order_id]
        if not _outstanding(world, action.actor_id):
            order.components["order"].filled = True


class PutDownRule:
    """Release something back to the kitchen so the other cook can take it.

    Found by running the world rather than by designing it: with take but no
    release, the first distribution of the knife and the ingredients is
    permanent. Ama held ingredients, Bo held the knife, and after five turns
    both had *zero* available actions -- each blocked on "nobody else is
    holding it" for what the other had. A deadlock neither agent could exit.

    This is deliberately not automatic. An agent has to decide to give up the
    knife, which is what makes the cooperation in this world a choice rather
    than a property of the rules.
    """

    rule_id = "kitchen.action.put_down"
    version = "1"
    action_kind = "put_down"
    read_paths: tuple[str, ...] = ("entities.<item>.ownership.owner_ref",)
    write_paths: tuple[str, ...] = ("entities.<item>.ownership.owner_ref",)

    def action_from_dict(self, value):
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        if value.get("kind") != "put_down":
            raise ValueError("record is not a put_down action")
        return PrepAction(
            _require_nonempty_string(value, "actor"),
            _require_nonempty_string(value, "item"),
            revision,
            _require_nonempty_string(value, "controller"),
            kind="put_down",
        )

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        return [
            PrepAction(actor_id, item, world.revision, "unselected", kind="put_down")
            for item in _held_by(world, actor_id)
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        item = world.entities.get(action.item_id)
        checks = [Check("Item exists", item is not None)]
        if item is None:
            return checks
        checks.append(
            Check("You are holding it", _holder(item) == action.actor_id,
                  _holder(item), action.actor_id)
        )
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        world.entities[action.item_id].ownership.owner_ref = owner_ref(
            "place", "kitchen"
        )


class BurnerFreeProcess:
    """A burner is busy for the tick it was used, then free again.

    Short on purpose. The two-agent run in Castaway spent six of ten turns with
    both agents waiting for a slow process, and that is the thing this world is
    built not to do.
    """

    rule_id = "kitchen.process.burner-free"
    version = "1"
    order = 10
    read_paths: tuple[str, ...] = ("entities.<burner>.components.burner.occupied_by",)
    write_paths: tuple[str, ...] = ("entities.<burner>.components.burner.occupied_by",)

    def due(self, world: World) -> bool:
        return any(
            (b := e.component("burner")) is not None and b.occupied_by
            for e in world.entities.values()
        )

    def apply(self, world: World) -> None:
        for e in sorted(world.entities.values(), key=lambda x: x.entity_id):
            burner = e.component("burner")
            if burner is not None and burner.occupied_by:
                burner.occupied_by = ""
