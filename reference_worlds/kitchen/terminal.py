"""Terminal condition for a kitchen service.

A service is complete when every order entity says it is filled. This is
derived from the order state the plating mechanic already owns rather than a
second completion flag that could drift out of sync.
"""

from __future__ import annotations

from world_substrate.model import World


def service_complete(world: World) -> bool:
    """Whether the kitchen has filled every represented order."""
    orders = [
        entity.component("order")
        for entity in world.entities.values()
        if entity.component("order") is not None
    ]
    return bool(orders) and all(order.filled for order in orders)
