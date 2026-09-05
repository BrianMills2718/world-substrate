"""Registered action and process contracts."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any, Protocol, runtime_checkable

from .model import World


def _require_nonempty_string(value: dict[str, Any], field: str) -> str:
    item = value[field]
    if not isinstance(item, str) or not item:
        raise TypeError(f"{field} must be a nonempty string")
    return item


def _require_integer(value: dict[str, Any], field: str) -> int:
    item = value[field]
    if type(item) is not int:
        raise TypeError(f"{field} must be an integer")
    return item


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
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            source_id=_require_nonempty_string(value, "source"),
            volume_ml=_require_integer(value, "volume_ml"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
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
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            target_id=_require_nonempty_string(value, "target"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
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
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
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
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            destination_id=_require_nonempty_string(value, "destination"),
            volume_ml=_require_integer(value, "volume_ml"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
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
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            volume_ml=_require_integer(value, "volume_ml"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class TakeAction:
    actor_id: str
    vessel_id: str
    base_revision: int
    controller_id: str
    kind: str = "take"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> TakeAction:
        if value.get("kind") != "take":
            raise ValueError("record is not a take action")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class GiveAction:
    actor_id: str
    vessel_id: str
    target_actor_id: str
    base_revision: int
    controller_id: str
    kind: str = "give"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "vessel": self.vessel_id,
            "target": self.target_actor_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> GiveAction:
        if value.get("kind") != "give":
            raise ValueError("record is not a give action")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            vessel_id=_require_nonempty_string(value, "vessel"),
            target_actor_id=_require_nonempty_string(value, "target"),
            base_revision=_require_integer(value, "base_revision"),
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class UnsupportedAction:
    """A structurally valid action envelope with no registered rule."""

    record: dict[str, Any]
    kind: str
    base_revision: int

    def as_dict(self) -> dict[str, object]:
        return deepcopy(self.record)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> UnsupportedAction:
        return cls(
            record=deepcopy(value),
            kind=_require_nonempty_string(value, "kind"),
            base_revision=_require_integer(value, "base_revision"),
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


# --- Optional capabilities a rule may declare --------------------------------
#
# `progress` and `consequences` were reached through `getattr` and appeared in
# no protocol, so a world author reading `ActionRule` or `ProcessRule` had no
# way to discover that either existed. They cannot be ordinary protocol members
# -- a protocol member is required, and most rules correctly have neither -- so
# they are separate opt-in protocols. The engine tests for them structurally,
# which is the same check `getattr` was doing, said out loud and typed.


@runtime_checkable
class DeclaresConsequences(Protocol):
    """An action rule that can say what taking it would destroy.

    A `Check` says whether an action is permitted. This says what a permitted
    action throws away that the actor already has, so an affordance list can
    distinguish `fill` on an empty vessel from `fill` on one holding water the
    actor spent fuel and several turns treating (M5 finding).

    Return an empty list when this particular attempt destroys nothing.
    """

    def consequences(self, world: World, action: TypedAction) -> list[str]: ...


@runtime_checkable
class ReportsProgress(Protocol):
    """A process that accumulates toward a threshold and can report how far.

    The count is usually already in the observation; the threshold is not, and
    a count without its threshold is unreadable -- `boiling_ticks: 1` says
    nothing unless two is known to be the target (M5 finding).

    Return one row per entity currently in flight, each with `entity_id`,
    `label`, `current` and `required`. Return an empty list when nothing is in
    flight; the substrate cannot infer which of a world's fields are counters,
    which is why this is declared rather than derived.
    """

    def progress(self, world: World) -> list[dict[str, Any]]: ...


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
