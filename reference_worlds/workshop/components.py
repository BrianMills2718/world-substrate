"""Workshop components, registered with the substrate's open component set.

Deliberately shares nothing with the Castaway components. There is no volume,
no temperature, no material, no heat source and no quantity of anything -- the
workshop is discrete. If the substrate is a substrate, that should be fine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from world_substrate.model import register_component


@dataclass
class WorkerState:
    """A person at a bench. No health, no hydration -- nothing can hurt them."""

    fatigue: int = 0
    skill: int = 1


@dataclass
class PartState:
    part_kind: str
    attached_to: str | None = None


@dataclass
class ToolState:
    tool_kind: str
    wear: int = 0
    wear_limit: int = 100


@dataclass
class AssemblyState:
    required_kinds: list[str] = field(default_factory=list)
    requires_tool: str = ""


register_component("worker", WorkerState)
register_component("part", PartState)
register_component("tool", ToolState)
register_component("assembly", AssemblyState)
