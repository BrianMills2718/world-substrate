"""Kitchen components: a third world, contested on purpose.

Castaway tested whether a world runs at all; the workshop tested whether the
contracts transfer. This one is built against a requirement the two-agent run
produced: six of ten turns there were both agents correctly waiting, because
that world has one pot, one cup and one fire and nothing to compete over.

So: two cooks with *different* orders, one knife, two burners, and exactly
enough ingredients that wasting one loses a dish. Every stage is a single
action, so nobody waits several turns for a process to finish.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from world_substrate.model import register_component


@dataclass
class CookState:
    """A cook, and the order they are trying to fill.

    `order_id` is what makes the two agents asymmetric: they want different
    dishes, so they are not simply racing for the same next action.
    """

    order_id: str
    plated: list[str] = field(default_factory=list)


@dataclass
class OrderState:
    """A dish, and the prepared ingredients it still needs."""

    wants: list[str] = field(default_factory=list)
    filled: bool = False


@dataclass
class IngredientState:
    """One ingredient, and how far through prep it is.

    Stages are raw -> chopped -> cooked. Each is one action, and each needs a
    different contested resource: chopping needs the knife, cooking needs a
    burner.
    """

    kind: str
    stage: str = "raw"
    spoiled: bool = False


@dataclass
class ToolState:
    """The knife. One of them, and both cooks need it repeatedly."""

    tool_kind: str


@dataclass
class BurnerState:
    """One hob. Two exist, so contention is frequent without being total."""

    occupied_by: str = ""


register_component("cook", CookState)
register_component("order", OrderState)
register_component("ingredient", IngredientState)
register_component("kitchen_tool", ToolState)
register_component("burner", BurnerState)
