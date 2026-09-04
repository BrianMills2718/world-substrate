"""Compile a declared mechanic into a registrable process rule.

docs/contracts/mechanic-profile-v0.md permits an offline mechanics agent to
produce "declarative mechanics or executable source". This module implements
the declarative half, deliberately: a declaration is inspectable before it runs,
and nothing here executes author-supplied code. The compiled rule is an
ordinary `ProcessRule`, so an authored mechanic gets exactly the same treatment
as a hand-written one -- the engine's write-scope guard, the causal trace, the
installer, and the interaction assays all apply without knowing it was authored.

The declaration language is small on purpose. It can express selection over
entities by component and field comparison, and numeric or string effects on
declared state paths. That is enough for the workshop's plausible mechanics and
narrow enough to interpret deterministically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import World
from .profile import MechanicPackage

OPS = {
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
}
EFFECT_OPS = {"set", "add", "subtract"}


class DeclarationError(ValueError):
    """A declared mechanic is not interpretable as written."""


def _resolve(entity: Any, path: str) -> Any:
    """Read a dotted path relative to an entity, or raise."""
    parts = path.split(".")
    if parts[0] == "components":
        if len(parts) < 3:
            raise DeclarationError(f"component path too short: {path}")
        current: Any = entity.components.get(parts[1])
        parts = parts[2:]
    else:
        current = getattr(entity, parts[0], None)
        parts = parts[1:]
    for part in parts:
        if current is None:
            return None
        current = getattr(current, part, None)
    return current


def _assign(entity: Any, path: str, op: str, value: Any) -> None:
    parts = path.split(".")
    if parts[0] == "components":
        holder: Any = entity.components.get(parts[1])
        parts = parts[2:]
    else:
        holder = getattr(entity, parts[0], None)
        parts = parts[1:]
    if not parts:
        raise DeclarationError(f"effect path must name a field, not a component: {path}")
    for part in parts[:-1]:
        holder = getattr(holder, part, None)
    if holder is None:
        return
    field = parts[-1]
    current = getattr(holder, field, None)
    if op == "set":
        setattr(holder, field, value)
        return
    if not isinstance(current, int) or not isinstance(value, int):
        raise DeclarationError(f"{op} needs integers at {path}")
    setattr(holder, field, current + value if op == "add" else current - value)


@dataclass(frozen=True)
class DeclaredMechanic:
    """An authored process mechanic, declared rather than coded."""

    mechanic_id: str
    version: str
    rationale: str
    order: int
    selector: dict[str, Any]
    effects: tuple[dict[str, Any], ...]
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    unsupported_interactions: tuple[str, ...] = ()
    invariants: tuple[str, ...] = ()
    limits: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> DeclaredMechanic:
        required = {
            "mechanic_id",
            "rationale",
            "selector",
            "effects",
            "reads",
            "writes",
        }
        missing = sorted(required - set(value))
        if missing:
            raise DeclarationError(f"declaration is missing: {missing}")
        selector = value["selector"]
        if not isinstance(selector, dict) or "has_component" not in selector:
            raise DeclarationError("selector must name has_component")
        effects = value["effects"]
        if not isinstance(effects, list) or not effects:
            raise DeclarationError("effects must be a nonempty list")
        for effect in effects:
            if not isinstance(effect, dict):
                raise DeclarationError("each effect must be an object")
            if effect.get("op") not in EFFECT_OPS:
                raise DeclarationError(f"unknown effect op: {effect.get('op')!r}")
            path = effect.get("path")
            if not isinstance(path, str) or not path:
                raise DeclarationError("each effect needs a path")
            # A component path must reach a field: components.<name>.<field>.
            # Writing a whole component is not expressible in this language,
            # and must be refused when declared rather than crash when applied.
            segments = path.split(".")
            if segments[0] == "components" and len(segments) < 3:
                raise DeclarationError(
                    f"effect path must name a field, not a component: {path}"
                )
            if segments[0] != "components" and len(segments) < 2:
                raise DeclarationError(f"effect path must name a field: {path}")
        for clause in selector.get("where", []) or []:
            if clause.get("op") not in OPS:
                raise DeclarationError(f"unknown comparison: {clause.get('op')!r}")
        return cls(
            mechanic_id=str(value["mechanic_id"]),
            version=str(value.get("version", "1")),
            rationale=str(value["rationale"]),
            order=int(value.get("order", 50)),
            selector=selector,
            effects=tuple(effects),
            reads=tuple(value["reads"]),
            writes=tuple(value["writes"]),
            dependencies=tuple(value.get("dependencies") or ()),
            unsupported_interactions=tuple(value.get("unsupported_interactions") or ()),
            invariants=tuple(value.get("invariants") or ()),
            limits=tuple(value.get("limits") or ()),
        )

    def package(self) -> MechanicPackage:
        return MechanicPackage(
            mechanic_id=self.mechanic_id,
            version=self.version,
            causal_bearer="autonomous process (authored offline)",
            representation="deterministic",
            reads=self.reads,
            writes=self.writes,
            commit_occasion="tick",
            order=self.order,
            effects=(self.rationale,),
            invariants=self.invariants,
            dependencies=self.dependencies,
            unsupported_interactions=self.unsupported_interactions,
            limits=self.limits or ("Authored offline; limits not declared.",),
            tests=("scripts/run_authoring_experiment.py",),
            trace_contract="Ordinary causal event per tick in which it applies.",
        )


class CompiledMechanic:
    """A `ProcessRule` built from a declaration. Author code never runs."""

    def __init__(self, declared: DeclaredMechanic) -> None:
        self._declared = declared
        self.rule_id = declared.mechanic_id
        self.version = declared.version
        self.order = declared.order
        self.read_paths = declared.reads
        self.write_paths = declared.writes

    def _matches(self, entity: Any) -> bool:
        selector = self._declared.selector
        if entity.components.get(selector["has_component"]) is None:
            return False
        for clause in selector.get("where", []) or []:
            actual = _resolve(entity, clause["path"])
            if actual is None:
                return False
            try:
                if not OPS[clause["op"]](actual, clause["value"]):
                    return False
            except TypeError:
                return False
        return True

    def due(self, world: World) -> bool:
        return any(self._matches(entity) for entity in world.entities.values())

    def apply(self, world: World) -> None:
        for entity in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if not self._matches(entity):
                continue
            for effect in self._declared.effects:
                _assign(entity, effect["path"], effect["op"], effect.get("value"))


MECHANIC_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "mechanic_id",
        "rationale",
        "order",
        "selector",
        "effects",
        "reads",
        "writes",
        "dependencies",
        "invariants",
        "limits",
    ],
    "properties": {
        "mechanic_id": {
            "type": "string",
            "description": "Stable dotted id, e.g. workshop.process.something.",
        },
        "rationale": {
            "type": "string",
            "description": "One or two sentences: what this mechanic is and why the world needs it.",
        },
        "order": {
            "type": "integer",
            "description": "Process ordering within a tick. Existing: fatigue 10, tool wear 20.",
        },
        "selector": {
            "type": "object",
            "additionalProperties": False,
            "required": ["has_component", "where"],
            "properties": {
                "has_component": {
                    "type": "string",
                    "description": "Entities must have this component to be affected.",
                },
                "where": {
                    "type": "array",
                    "description": "Further conditions, all of which must hold.",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["path", "op", "value"],
                        "properties": {
                            "path": {"type": "string", "description": "Entity-relative dotted path, e.g. components.tool.wear."},
                            "op": {"type": "string", "enum": sorted(OPS)},
                            "value": {"type": ["integer", "string", "boolean"]},
                        },
                    },
                },
            },
        },
        "effects": {
            "type": "array",
            "description": "What changes on each affected entity.",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["path", "op", "value"],
                "properties": {
                    "path": {"type": "string", "description": "Entity-relative dotted path to change."},
                    "op": {"type": "string", "enum": sorted(EFFECT_OPS)},
                    "value": {"type": ["integer", "string", "boolean"]},
                },
            },
        },
        "reads": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Every state path this mechanic inspects, as entities.<x>.<path>.",
        },
        "writes": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Every state path this mechanic changes, as entities.<x>.<path>. Writing anything not declared here is refused.",
        },
        "dependencies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Installed mechanic ids whose behaviour this one depends on or affects.",
        },
        "invariants": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Goal-relative postconditions that should hold after this applies.",
        },
        "limits": {
            "type": "array",
            "items": {"type": "string"},
            "description": "What this deliberately does not model.",
        },
    },
}
