"""Typed components required by the Waltzman Coordination Lab demo."""

from __future__ import annotations

from dataclasses import dataclass

from world_substrate.model import register_component


@dataclass
class ResidentState:
    role: str
    organization: str


@dataclass
class ResourceState:
    current: int
    required: int
    unit: str


@dataclass
class ConstraintState:
    status: str
    required_status: str = "clear"


@dataclass
class CommitmentState:
    stance: str
    constraint_id: str


@dataclass
class InstitutionState:
    status: str
    support_count: int
    conditional_count: int
    required_support: int
    last_evaluated_tick: int = -1


@dataclass
class ActivityState:
    kind: str
    status: str = "pending"
    duration_ticks: int = 2
    started_tick: int | None = None
    end_tick: int | None = None


@dataclass
class PackageState:
    status: str = "available"


register_component("resident", ResidentState)
register_component("resource", ResourceState)
register_component("constraint", ConstraintState)
register_component("commitment", CommitmentState)
register_component("institution", InstitutionState)
register_component("activity", ActivityState)
register_component("package", PackageState)
