"""Registered action and process contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Protocol

from .model import World


@dataclass(frozen=True)
class Check:
    label: str
    ok: bool
    actual: object | None = None
    required: object | None = None

    def as_dict(self) -> dict[str, object | None]:
        return asdict(self)


@dataclass(frozen=True)
class FillAction:
    actor_id: str
    vessel_id: str
    source_id: str
    volume_ml: int
    base_revision: int
    controller_id: str
    kind: str = "fill"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "source": self.source_id,
            "volume_ml": self.volume_ml,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> FillAction:
        if value.get("kind") != "fill":
            raise ValueError("record is not a fill action")
        return cls(
            actor_id=str(value["actor"]),
            vessel_id=str(value["vessel"]),
            source_id=str(value["source"]),
            volume_ml=int(value["volume_ml"]),
            base_revision=int(value["base_revision"]),
            controller_id=str(value["controller"]),
        )


@dataclass(frozen=True)
class HeatAction:
    actor_id: str
    vessel_id: str
    target_id: str
    base_revision: int
    controller_id: str
    kind: str = "heat"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "target": self.target_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> HeatAction:
        if value.get("kind") != "heat":
            raise ValueError("record is not a heat action")
        return cls(
            actor_id=str(value["actor"]),
            vessel_id=str(value["vessel"]),
            target_id=str(value["target"]),
            base_revision=int(value["base_revision"]),
            controller_id=str(value["controller"]),
        )


@dataclass(frozen=True)
class UnheatAction:
    actor_id: str
    vessel_id: str
    base_revision: int
    controller_id: str
    kind: str = "unheat"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> UnheatAction:
        if value.get("kind") != "unheat":
            raise ValueError("record is not an unheat action")
        return cls(
            actor_id=str(value["actor"]),
            vessel_id=str(value["vessel"]),
            base_revision=int(value["base_revision"]),
            controller_id=str(value["controller"]),
        )


@dataclass(frozen=True)
class PourAction:
    actor_id: str
    vessel_id: str
    destination_id: str
    volume_ml: int
    base_revision: int
    controller_id: str
    kind: str = "pour"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "destination": self.destination_id,
            "volume_ml": self.volume_ml,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> PourAction:
        if value.get("kind") != "pour":
            raise ValueError("record is not a pour action")
        return cls(
            actor_id=str(value["actor"]),
            vessel_id=str(value["vessel"]),
            destination_id=str(value["destination"]),
            volume_ml=int(value["volume_ml"]),
            base_revision=int(value["base_revision"]),
            controller_id=str(value["controller"]),
        )


@dataclass(frozen=True)
class DrinkAction:
    actor_id: str
    vessel_id: str
    volume_ml: int
    base_revision: int
    controller_id: str
    kind: str = "drink"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "volume_ml": self.volume_ml,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> DrinkAction:
        if value.get("kind") != "drink":
            raise ValueError("record is not a drink action")
        return cls(
            actor_id=str(value["actor"]),
            vessel_id=str(value["vessel"]),
            volume_ml=int(value["volume_ml"]),
            base_revision=int(value["base_revision"]),
            controller_id=str(value["controller"]),
        )


class TypedAction(Protocol):
    @property
    def kind(self) -> str: ...

    @property
    def base_revision(self) -> int: ...

    def as_dict(self) -> dict[str, object]: ...


class ActionRule(Protocol):
    rule_id: str
    version: str
    action_kind: str
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]

    def discover(self, world: World, actor_id: str) -> list[TypedAction]: ...

    def action_from_dict(self, value: dict[str, Any]) -> TypedAction: ...

    def checks(self, world: World, action: TypedAction) -> list[Check]: ...

    def apply(self, world: World, action: TypedAction, event_id: str) -> None: ...


class ProcessRule(Protocol):
    rule_id: str
    version: str
    order: int
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]

    def due(self, world: World) -> bool: ...

    def apply(self, world: World) -> None: ...


class RuleRegistry:
    """The sole lookup surface for executable action and process rules."""

    def __init__(self) -> None:
        self._actions: dict[str, ActionRule] = {}
        self._processes: list[ProcessRule] = []

    def register_action(self, rule: ActionRule) -> None:
        if rule.action_kind in self._actions:
            raise ValueError(f"duplicate action rule: {rule.action_kind}")
        self._actions[rule.action_kind] = rule

    def register_process(self, rule: ProcessRule) -> None:
        if any(existing.rule_id == rule.rule_id for existing in self._processes):
            raise ValueError(f"duplicate process rule: {rule.rule_id}")
        self._processes.append(rule)
        self._processes.sort(key=lambda item: (item.order, item.rule_id))

    def action(self, kind: str) -> ActionRule | None:
        return self._actions.get(kind)

    def action_kinds(self) -> tuple[str, ...]:
        return tuple(sorted(self._actions))

    def processes(self) -> tuple[ProcessRule, ...]:
        return tuple(self._processes)

    def versions(self) -> dict[str, str]:
        rules = list(self._actions.values()) + self._processes
        return {rule.rule_id: rule.version for rule in rules}
