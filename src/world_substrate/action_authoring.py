"""Compile constrained authored action mechanics into ordinary ActionRules.

This is the action-side counterpart to :mod:`world_substrate.authoring`.  A
model or human may propose a JSON declaration, but the declaration language is
small, inspectable, and interpreted by this module.  It never executes authored
source code.

The compiler derives the rule's read/write paths from selectors, checks and
effects.  The resulting rule still crosses the ordinary Engine boundary, so
write-scope enforcement, atomic commit, causal events and mechanic-profile
installation apply exactly as they do to hand-written rules.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import Any

from .model import Entity, World, owner_ref
from .profile import MechanicPackage
from .rules import Check, TypedAction

CAUSAL_MODEL_SCHEMA_VERSION = "world-substrate-causal-model/v0"
ACTION_MECHANIC_SCHEMA_VERSION = "world-substrate-action-mechanic/v0"
PROCESS_SCHEMA_VERSION = "world-substrate-process-mechanic/v0"
MAX_PROCESSES = 6
MAX_DISCOVERED_ACTIONS = 256

OPS = {
    "eq": lambda a, b: a == b,
    "ne": lambda a, b: a != b,
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
    "contains": lambda a, b: b in a,
}
EFFECT_OPS = frozenset({"set", "add", "subtract"})


class ActionDeclarationError(ValueError):
    """An authored action mechanic is not interpretable as written."""


@dataclass(frozen=True)
class DeclaredAction:
    """Generic typed-action envelope after a declaration validates its shape."""

    record: dict[str, Any]
    kind: str
    base_revision: int

    def as_dict(self) -> dict[str, object]:
        return deepcopy(self.record)


@dataclass(frozen=True)
class DeclaredActionMechanic:
    mechanic_id: str
    version: str
    action_kind: str
    rationale: str
    actor_selector: dict[str, Any]
    participants: dict[str, dict[str, Any]]
    parameters: dict[str, tuple[Any, ...]]
    checks: tuple[dict[str, Any], ...]
    effects: tuple[dict[str, Any], ...]
    limits: tuple[str, ...]
    tests: tuple[str, ...]
    semantic_bindings: tuple[str, ...]
    action_signature: dict[str, Any]
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]

    def package(self) -> MechanicPackage:
        return MechanicPackage(
            mechanic_id=self.mechanic_id,
            version=self.version,
            causal_bearer="agent action (authored declaration)",
            representation="deterministic",
            reads=self.read_paths,
            writes=self.write_paths,
            effects=(self.rationale,),
            limits=self.limits,
            tests=self.tests,
            semantic_bindings=self.semantic_bindings,
            trace_contract="Ordinary action attempt with checks and state-path changes.",
        )

    @classmethod
    def from_dict(
        cls,
        value: dict[str, Any],
        *,
        bundle: dict[str, Any],
    ) -> "DeclaredActionMechanic":
        if not isinstance(value, dict):
            raise ActionDeclarationError("action mechanic must be an object")
        if value.get("schema_version", ACTION_MECHANIC_SCHEMA_VERSION) != ACTION_MECHANIC_SCHEMA_VERSION:
            raise ActionDeclarationError(
                f"schema_version must be {ACTION_MECHANIC_SCHEMA_VERSION}"
            )
        required = {
            "mechanic_id",
            "action_kind",
            "rationale",
            "actor_selector",
            "participants",
            "parameters",
            "checks",
            "effects",
            "limits",
            "tests",
        }
        missing = sorted(required - set(value))
        if missing:
            raise ActionDeclarationError(f"action mechanic is missing: {missing}")
        allowed = required | {"schema_version", "version", "semantic_bindings"}
        unknown = sorted(set(value) - allowed)
        if unknown:
            raise ActionDeclarationError(f"unknown action mechanic keys: {unknown}")

        mechanic_id = _nonempty(value["mechanic_id"], "mechanic_id")
        action_kind = _nonempty(value["action_kind"], "action_kind")
        rationale = _nonempty(value["rationale"], "rationale")
        signature = _action_signature(bundle, action_kind)
        field_types = {row["name"]: row["type"] for row in signature.get("fields", [])}
        entity_fields = {name for name, kind in field_types.items() if kind == "entity_ref"}
        scalar_fields = set(field_types) - entity_fields

        actor_selector = _selector(value["actor_selector"], bundle, "actor_selector")
        raw_participants = value["participants"]
        if not isinstance(raw_participants, dict):
            raise ActionDeclarationError("participants must be an object")
        if set(raw_participants) != entity_fields:
            raise ActionDeclarationError(
                f"participants must exactly name entity_ref fields {sorted(entity_fields)}"
            )
        participants = {
            name: _selector(raw_participants[name], bundle, f"participants.{name}")
            for name in sorted(raw_participants)
        }

        raw_parameters = value["parameters"]
        if not isinstance(raw_parameters, dict) or set(raw_parameters) != scalar_fields:
            raise ActionDeclarationError(
                f"parameters must exactly name scalar fields {sorted(scalar_fields)}"
            )
        parameters: dict[str, tuple[Any, ...]] = {}
        for name in sorted(raw_parameters):
            choices = raw_parameters[name]
            if not isinstance(choices, list) or not choices:
                raise ActionDeclarationError(f"parameters.{name} must be a nonempty list")
            kind = field_types[name]
            for choice in choices:
                if not _value_matches_authoring_type(kind, choice):
                    raise ActionDeclarationError(
                        f"parameters.{name} value {choice!r} does not match {kind}"
                    )
            parameters[name] = tuple(deepcopy(choices))

        selectors = {"actor": actor_selector, **participants}
        checks = _checks(value["checks"], bundle, signature, selectors)
        effects = _effects(value["effects"], bundle, signature, selectors)
        limits = _string_list(value["limits"], "limits", nonempty=True)
        tests = _string_list(value["tests"], "tests", nonempty=True)
        semantic_bindings = _string_list(
            value.get("semantic_bindings", []), "semantic_bindings", nonempty=False
        )
        read_paths = _derived_reads(actor_selector, participants, checks, effects)
        write_paths = _derived_writes(effects)
        return cls(
            mechanic_id=mechanic_id,
            version=str(value.get("version", "1")),
            action_kind=action_kind,
            rationale=rationale,
            actor_selector=actor_selector,
            participants=participants,
            parameters=parameters,
            checks=checks,
            effects=effects,
            limits=limits,
            tests=tests,
            semantic_bindings=semantic_bindings,
            action_signature=deepcopy(signature),
            read_paths=read_paths,
            write_paths=write_paths,
        )


@dataclass(frozen=True)
class DeclaredTerminal:
    """State-derived stop condition over a selected set of represented entities."""

    mode: str
    selector: dict[str, Any]
    checks: tuple[dict[str, Any], ...]

    @classmethod
    def from_dict(cls, value: object, *, bundle: dict[str, Any]) -> "DeclaredTerminal | None":
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ActionDeclarationError("terminal must be an object or null")
        mode = value.get("mode")
        if mode not in {"all", "any"}:
            raise ActionDeclarationError("terminal.mode must be all or any")
        selector = _selector(value.get("selector", {}), bundle, "terminal.selector")
        raw_checks = value.get("checks")
        if not isinstance(raw_checks, list) or not raw_checks:
            raise ActionDeclarationError("terminal.checks must be a nonempty list")
        checks: list[dict[str, Any]] = []
        for index, row in enumerate(raw_checks):
            if not isinstance(row, dict):
                raise ActionDeclarationError(f"terminal check {index} must be an object")
            path = _nonempty(row.get("path"), f"terminal.checks[{index}].path")
            target_type = _path_type(bundle, path)
            _require_selector_path(selector, path, f"terminal.checks[{index}]")
            op = row.get("op")
            if op not in OPS:
                raise ActionDeclarationError(f"terminal check {index} has unknown op {op!r}")
            if "value" not in row:
                raise ActionDeclarationError(f"terminal check {index} needs value")
            source_type = _literal_type(row["value"])
            _validate_comparison(target_type, op, source_type, f"terminal.checks[{index}]")
            checks.append({"path": path, "op": op, "value": deepcopy(row["value"])})
        return cls(mode=mode, selector=selector, checks=tuple(checks))

    def reached(self, world: World) -> bool:
        selected = [e for e in world.entities.values() if _selector_matches(e, self.selector)]
        if not selected:
            return False
        verdicts = [
            all(_compare(_entity_value(entity, c["path"]), c["op"], c["value"])
                for c in self.checks)
            for entity in selected
        ]
        return all(verdicts) if self.mode == "all" else any(verdicts)


@dataclass(frozen=True)
class DeclaredProcess:
    """Something the world does by itself every round, with no actor.

    It uses the same selector/check/effect language as actions, with a single
    participant named ``it``: every entity matching the selector whose checks
    hold has the effects applied, once per round. This is what lets a world
    keep going (plants dry out again, new orders arrive) instead of stopping
    once its actors have done everything once.
    """

    process_id: str
    version: str
    rationale: str
    selector: dict[str, Any]
    checks: tuple[dict[str, Any], ...]
    effects: tuple[dict[str, Any], ...]
    limits: tuple[str, ...]
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]

    def package(self) -> MechanicPackage:
        return MechanicPackage(
            mechanic_id=self.process_id,
            version=self.version,
            causal_bearer="autonomous process (authored declaration)",
            representation="deterministic",
            reads=self.read_paths,
            writes=self.write_paths,
            effects=(self.rationale,),
            limits=self.limits,
            tests=("applies once per round to every matching entity whose checks hold",),
            semantic_bindings=(),
            trace_contract="Process event per round with state-path changes on matching entities.",
        )

    @classmethod
    def from_dict(cls, value: object, *, bundle: dict[str, Any]) -> "DeclaredProcess":
        if not isinstance(value, dict):
            raise ActionDeclarationError("process must be an object")
        required = {"process_id", "rationale", "selector", "checks", "effects"}
        missing = sorted(required - set(value))
        if missing:
            raise ActionDeclarationError(f"process is missing: {missing}")
        unknown = sorted(set(value) - required - {"schema_version", "version", "limits"})
        if unknown:
            raise ActionDeclarationError(f"unknown process keys: {unknown}")
        process_id = _nonempty(value["process_id"], "process_id")
        selector = _selector(value["selector"], bundle, f"process {process_id} selector")
        signature: dict[str, Any] = {"fields": []}
        selectors = {"it": selector}
        # A process may run on every matching entity unconditionally.
        checks = _checks(value["checks"], bundle, signature, selectors) if value["checks"] else ()
        effects = _effects(value["effects"], bundle, signature, selectors)
        return cls(
            process_id=process_id,
            version=str(value.get("version", "1")),
            rationale=_nonempty(value["rationale"], f"process {process_id} rationale"),
            selector=selector,
            checks=checks,
            effects=effects,
            limits=_string_list(value.get("limits", []), "limits", nonempty=False),
            # _derived_reads names the selector's entity `<actor>`; a process's
            # only participant is `it`.
            read_paths=tuple(sorted(p.replace("<actor>", "<it>") for p in _derived_reads(selector, {}, checks, effects))),
            write_paths=_derived_writes(effects),
        )


class CompiledProcessMechanic:
    """A ProcessRule interpreted entirely from a validated declaration."""

    def __init__(self, declared: DeclaredProcess, order: int) -> None:
        self.declared = declared
        self.rule_id = declared.process_id
        self.version = declared.version
        self.order = order
        self.read_paths = declared.read_paths
        self.write_paths = declared.write_paths

    def _matching(self, world: World) -> list[str]:
        out = []
        for entity_id in sorted(world.entities):
            entity = world.entities[entity_id]
            if not _selector_matches(entity, self.declared.selector):
                continue
            participants = {"it": entity_id}
            ok = True
            for row in self.declared.checks:
                try:
                    left = _resolve_expr(row["left"], world, {}, participants, None)
                    right = _resolve_expr(row["right"], world, {}, participants, None)
                    ok = _compare(left, row["op"], right)
                except (KeyError, TypeError, ValueError, ActionDeclarationError):
                    ok = False
                if not ok:
                    break
            if ok:
                out.append(entity_id)
        return out

    def due(self, world: World) -> bool:
        return bool(self._matching(world))

    def apply_with_event_id(self, world: World, event_id: str | None) -> None:
        for entity_id in self._matching(world):
            participants = {"it": entity_id}
            entity = world.entities[entity_id]
            for effect in self.declared.effects:
                value = _resolve_expr(effect["value"], world, {}, participants, event_id)
                _assign_entity_value(entity, effect["path"], effect["op"], value)
            if event_id is not None:
                entity.last_cause_event_id = event_id

    def apply(self, world: World) -> None:
        self.apply_with_event_id(world, None)


@dataclass(frozen=True)
class CausalModel:
    mechanics: tuple[DeclaredActionMechanic, ...]
    terminal: DeclaredTerminal | None
    processes: tuple[DeclaredProcess, ...] = ()

    @classmethod
    def from_dict(cls, value: object, *, bundle: dict[str, Any]) -> "CausalModel":
        if not isinstance(value, dict):
            raise ActionDeclarationError("causal model must be a JSON object")
        if value.get("schema_version") != CAUSAL_MODEL_SCHEMA_VERSION:
            raise ActionDeclarationError(
                f"schema_version must be {CAUSAL_MODEL_SCHEMA_VERSION}"
            )
        raw = value.get("mechanics")
        if not isinstance(raw, list) or not raw:
            raise ActionDeclarationError("causal model mechanics must be a nonempty list")
        mechanics = tuple(
            DeclaredActionMechanic.from_dict(row, bundle=bundle) for row in raw
        )
        kinds = [m.action_kind for m in mechanics]
        if len(kinds) != len(set(kinds)):
            raise ActionDeclarationError("causal model has duplicate action kinds")
        expected_kinds = {
            row["kind"] for row in (bundle.get("actions") or [])
            if isinstance(row, dict) and isinstance(row.get("kind"), str)
        }
        if set(kinds) != expected_kinds:
            raise ActionDeclarationError(
                "causal model action kinds must exactly match the authoring bundle: "
                f"expected {sorted(expected_kinds)}, got {sorted(kinds)}"
            )
        terminal = DeclaredTerminal.from_dict(value.get("terminal"), bundle=bundle)
        raw_processes = value.get("processes") or []
        if not isinstance(raw_processes, list) or len(raw_processes) > MAX_PROCESSES:
            raise ActionDeclarationError(f"processes must be a list of at most {MAX_PROCESSES}")
        processes = tuple(DeclaredProcess.from_dict(row, bundle=bundle) for row in raw_processes)
        ids = [p.process_id for p in processes] + [m.mechanic_id for m in mechanics]
        if len(ids) != len(set(ids)):
            raise ActionDeclarationError("process and mechanic ids must be unique")
        return cls(mechanics=mechanics, terminal=terminal, processes=processes)

    def as_review(self) -> dict[str, Any]:
        """Authority-oriented summary suitable for a human review surface."""
        return {
            "schema_version": CAUSAL_MODEL_SCHEMA_VERSION,
            "mechanics": [
                {
                    "mechanic_id": m.mechanic_id,
                    "action_kind": m.action_kind,
                    "rationale": m.rationale,
                    "reads": list(m.read_paths),
                    "writes": list(m.write_paths),
                    "checks": deepcopy(list(m.checks)),
                    "effects": deepcopy(list(m.effects)),
                    "limits": list(m.limits),
                    "tests": list(m.tests),
                }
                for m in self.mechanics
            ],
            "processes": [
                {
                    "process_id": p.process_id,
                    "rationale": p.rationale,
                    "selector": deepcopy(p.selector),
                    "checks": deepcopy(list(p.checks)),
                    "effects": deepcopy(list(p.effects)),
                    "writes": list(p.write_paths),
                }
                for p in self.processes
            ],
            "terminal": None
            if self.terminal is None
            else {
                "mode": self.terminal.mode,
                "selector": deepcopy(self.terminal.selector),
                "checks": deepcopy(list(self.terminal.checks)),
            },
        }


class CompiledActionMechanic:
    """An ActionRule interpreted entirely from a validated declaration."""

    def __init__(self, declared: DeclaredActionMechanic) -> None:
        self.declared = declared
        self.rule_id = declared.mechanic_id
        self.version = declared.version
        self.action_kind = declared.action_kind
        self.read_paths = declared.read_paths
        self.write_paths = declared.write_paths
        self._field_types = {
            row["name"]: row["type"] for row in declared.action_signature.get("fields", [])
        }

    def action_from_dict(self, value: dict[str, Any]) -> DeclaredAction:
        if not isinstance(value, dict) or value.get("kind") != self.action_kind:
            raise ValueError(f"record is not a {self.action_kind} action")
        expected = {"actor", "kind", "base_revision", "controller", *self._field_types}
        if set(value) != expected:
            raise ValueError(
                f"{self.action_kind} action fields must be {sorted(expected)}"
            )
        actor = value.get("actor")
        controller = value.get("controller")
        revision = value.get("base_revision")
        if not isinstance(actor, str) or not actor:
            raise TypeError("actor must be a nonempty string")
        if not isinstance(controller, str) or not controller:
            raise TypeError("controller must be a nonempty string")
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        for name, kind in self._field_types.items():
            if not _value_matches_authoring_type(kind, value.get(name)):
                raise TypeError(f"{name} does not match {kind}")
        return DeclaredAction(deepcopy(value), self.action_kind, revision)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = world.entities.get(actor_id)
        if actor is None or not _selector_matches(actor, self.declared.actor_selector):
            return []
        participant_names = sorted(self.declared.participants)
        participant_choices: list[list[str]] = []
        for name in participant_names:
            selector = self.declared.participants[name]
            participant_choices.append(
                [
                    entity.entity_id
                    for entity in sorted(world.entities.values(), key=lambda e: e.entity_id)
                    if _selector_matches(entity, selector)
                ]
            )
        parameter_names = sorted(self.declared.parameters)
        parameter_choices = [list(self.declared.parameters[name]) for name in parameter_names]
        dimensions: list[list[Any]] = [*participant_choices, *parameter_choices]
        combinations = product(*dimensions) if dimensions else [()]
        actions: list[TypedAction] = []
        for values in combinations:
            row: dict[str, Any] = {
                "actor": actor_id,
                "kind": self.action_kind,
                "base_revision": world.revision,
                "controller": "unselected",
            }
            offset = 0
            for name in participant_names:
                row[name] = values[offset]
                offset += 1
            for name in parameter_names:
                row[name] = values[offset]
                offset += 1
            actions.append(DeclaredAction(row, self.action_kind, world.revision))
            if len(actions) >= MAX_DISCOVERED_ACTIONS:
                break
        return actions

    def effect_preview(self, world: World, action: TypedAction) -> list[str]:
        """Describe the concrete writes this installed mechanic would perform."""
        if not isinstance(action, DeclaredAction) or action.kind != self.action_kind:
            raise TypeError(f"{self.action_kind} declaration requires DeclaredAction")
        record = action.record
        participants = {"actor": str(record["actor"])}
        participants.update(
            {name: str(record[name]) for name in self.declared.participants}
        )
        rows: list[str] = []
        for effect in self.declared.effects:
            target_id = participants[effect["participant"]]
            expr = effect["value"]
            if "event_id" in expr:
                value: Any = "<event-id>"
            else:
                value = _resolve_expr(expr, world, record, participants, None)
            rows.append(
                f"{target_id}.{effect['path']} {effect['op']} {value!r}"
            )
        return rows

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, DeclaredAction) or action.kind != self.action_kind:
            raise TypeError(f"{self.action_kind} declaration requires DeclaredAction")
        record = action.record
        actor = world.entities.get(str(record.get("actor")))
        checks: list[Check] = [
            Check("Actor exists", actor is not None),
            Check(
                "Actor matches mechanic selector",
                actor is not None and _selector_matches(actor, self.declared.actor_selector),
            ),
        ]
        participants: dict[str, str] = {}
        for name, selector in self.declared.participants.items():
            entity_id = record.get(name)
            entity = world.entities.get(entity_id) if isinstance(entity_id, str) else None
            participants[name] = entity_id if isinstance(entity_id, str) else ""
            checks.append(Check(f"Participant {name} exists", entity is not None))
            checks.append(
                Check(
                    f"Participant {name} matches mechanic selector",
                    entity is not None and _selector_matches(entity, selector),
                )
            )
        participants["actor"] = str(record.get("actor") or "")
        for row in self.declared.checks:
            try:
                left = _resolve_expr(row["left"], world, record, participants, None)
                right = _resolve_expr(row["right"], world, record, participants, None)
                ok = _compare(left, row["op"], right)
            except (KeyError, TypeError, ValueError, ActionDeclarationError):
                left, right, ok = None, None, False
            checks.append(Check(row["label"], ok, left, right))
        return checks

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        if not isinstance(action, DeclaredAction) or action.kind != self.action_kind:
            raise TypeError(f"{self.action_kind} declaration requires DeclaredAction")
        record = action.record
        participants = {"actor": str(record["actor"])}
        participants.update(
            {name: str(record[name]) for name in self.declared.participants}
        )
        touched: set[str] = set()
        for effect in self.declared.effects:
            participant = effect["participant"]
            entity_id = participants[participant]
            entity = world.entities[entity_id]
            value = _resolve_expr(
                effect["value"], world, record, participants, event_id
            )
            _assign_entity_value(entity, effect["path"], effect["op"], value)
            touched.add(entity_id)
        for entity_id in touched:
            world.entities[entity_id].last_cause_event_id = event_id


# ---------------------------------------------------------------------------
# Validation helpers


def _nonempty(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ActionDeclarationError(f"{label} must be a nonempty string")
    return value


def _string_list(value: object, label: str, *, nonempty: bool) -> tuple[str, ...]:
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ActionDeclarationError(f"{label} must be a list of nonempty strings")
    if nonempty and not value:
        raise ActionDeclarationError(f"{label} must not be empty")
    return tuple(value)


def _action_signature(bundle: dict[str, Any], kind: str) -> dict[str, Any]:
    for row in bundle.get("actions") or []:
        if isinstance(row, dict) and row.get("kind") == kind:
            return row
    raise ActionDeclarationError(f"action_kind {kind!r} is absent from authoring bundle")


def _component_specs(bundle: dict[str, Any]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for comp in bundle.get("components") or []:
        if not isinstance(comp, dict) or not isinstance(comp.get("name"), str):
            continue
        out[comp["name"]] = {
            row["name"]: row["type"]
            for row in comp.get("fields") or []
            if isinstance(row, dict)
            and isinstance(row.get("name"), str)
            and isinstance(row.get("type"), str)
        }
    return out


def _selector(value: object, bundle: dict[str, Any], label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ActionDeclarationError(f"{label} must be an object")
    unknown = sorted(set(value) - {"categories", "components"})
    if unknown:
        raise ActionDeclarationError(f"{label} has unknown keys: {unknown}")
    categories = value.get("categories", [])
    components = value.get("components", [])
    if not isinstance(categories, list) or any(not isinstance(x, str) or not x for x in categories):
        raise ActionDeclarationError(f"{label}.categories must be strings")
    if not isinstance(components, list) or any(not isinstance(x, str) or not x for x in components):
        raise ActionDeclarationError(f"{label}.components must be strings")
    if not categories and not components:
        raise ActionDeclarationError(f"{label} must constrain at least one category or component")
    known = _component_specs(bundle)
    missing = sorted(set(components) - set(known))
    if missing:
        raise ActionDeclarationError(f"{label} names unknown components: {missing}")
    return {"categories": list(categories), "components": list(components)}


def _selector_matches(entity: Entity, selector: dict[str, Any]) -> bool:
    if any(category not in entity.category_ids for category in selector.get("categories", [])):
        return False
    if any(entity.component(name) is None for name in selector.get("components", [])):
        return False
    return True


def _require_selector_path(selector: dict[str, Any], path: str, label: str) -> None:
    parts = path.split(".")
    if len(parts) == 3 and parts[0] == "components" and parts[1] not in selector.get("components", []):
        raise ActionDeclarationError(
            f"{label} reads/writes {path}, but its participant selector does not require component {parts[1]!r}"
        )


def _path_type(bundle: dict[str, Any], path: str) -> str:
    if path == "location.location_id":
        return "string"
    if path == "ownership.owner_ref":
        return "string"
    if path == "portable.portable":
        return "boolean"
    if path == "last_cause_event_id":
        return "string"
    parts = path.split(".")
    if len(parts) == 3 and parts[0] == "components":
        component, field = parts[1], parts[2]
        specs = _component_specs(bundle)
        if component in specs and field in specs[component]:
            return specs[component][field]
    raise ActionDeclarationError(f"unsupported or unknown state path: {path}")


def _value_matches_authoring_type(kind: str, value: object) -> bool:
    if kind in {"string", "entity_ref"}:
        return isinstance(value, str) and bool(value)
    if kind == "integer":
        return type(value) is int
    if kind == "number":
        return type(value) in {int, float}
    if kind == "boolean":
        return type(value) is bool
    return False


def _expr(value: object, bundle: dict[str, Any], signature: dict[str, Any], selectors: dict[str, dict[str, Any]], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or len(value) != 1:
        raise ActionDeclarationError(f"{label} must be a one-key expression object")
    key, raw = next(iter(value.items()))
    field_types = {row["name"]: row["type"] for row in signature.get("fields", [])}
    participant_names = set(selectors)
    if key == "literal":
        return {"literal": deepcopy(raw)}
    if key == "action_field":
        if raw not in field_types:
            raise ActionDeclarationError(f"{label} names unknown action field {raw!r}")
        return {"action_field": raw}
    if key == "participant":
        if not isinstance(raw, dict) or set(raw) != {"name", "path"}:
            raise ActionDeclarationError(f"{label}.participant needs name and path")
        if raw["name"] not in participant_names:
            raise ActionDeclarationError(f"{label} names unknown participant {raw['name']!r}")
        path = _nonempty(raw["path"], f"{label}.participant.path")
        _path_type(bundle, path)
        _require_selector_path(selectors[raw["name"]], path, label)
        return {"participant": {"name": raw["name"], "path": path}}
    if key == "entity_id":
        if raw not in participant_names:
            raise ActionDeclarationError(f"{label}.entity_id names unknown participant {raw!r}")
        return {"entity_id": raw}
    if key == "owner_ref":
        if raw not in participant_names:
            raise ActionDeclarationError(f"{label}.owner_ref names unknown participant {raw!r}")
        return {"owner_ref": raw}
    if key == "event_id":
        if raw is not True:
            raise ActionDeclarationError(f"{label}.event_id must be true")
        return {"event_id": True}
    raise ActionDeclarationError(f"{label} has unknown expression kind {key!r}")


def _literal_type(value: object) -> str | None:
    if value is None:
        return "null"
    if type(value) is bool:
        return "boolean"
    if type(value) is int:
        return "integer"
    if type(value) is float:
        return "number"
    if isinstance(value, str):
        return "string"
    return None


def _expr_type(expr: dict[str, Any], bundle: dict[str, Any], signature: dict[str, Any]) -> str | None:
    if "literal" in expr:
        return _literal_type(expr["literal"])
    if "action_field" in expr:
        fields = {row["name"]: row["type"] for row in signature.get("fields", [])}
        return fields.get(expr["action_field"])
    if "participant" in expr:
        return _path_type(bundle, expr["participant"]["path"])
    if "entity_id" in expr:
        return "entity_ref"
    if "owner_ref" in expr or "event_id" in expr:
        return "string"
    return None


def _compatible(target: str, source: str | None) -> bool:
    if source is None:
        return False
    if target == source:
        return True
    if target == "number" and source == "integer":
        return True
    if target == "string" and source == "entity_ref":
        return True
    if target == "entity_ref_or_null" and source in {"entity_ref", "string", "null"}:
        return True
    if target == "entity_ref" and source == "string":
        return True
    return False


def _validate_comparison(left: str | None, op: str, right: str | None, label: str) -> None:
    if op in {"eq", "ne"}:
        if not (_compatible(left or "", right) or _compatible(right or "", left)):
            raise ActionDeclarationError(f"{label} compares incompatible types {left} and {right}")
        return
    if op in {"lt", "lte", "gt", "gte"}:
        if left not in {"integer", "number"} or right not in {"integer", "number"}:
            raise ActionDeclarationError(f"{label} {op} comparison requires numeric values")
        return
    if op == "contains":
        if not ((left == "string_list" and right == "string") or (left == "string" and right == "string")):
            raise ActionDeclarationError(f"{label} contains comparison requires string/list compatibility")


def _checks(value: object, bundle: dict[str, Any], signature: dict[str, Any], selectors: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, list) or not value:
        raise ActionDeclarationError("checks must be a nonempty list")
    out: list[dict[str, Any]] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict) or set(row) != {"label", "left", "op", "right"}:
            raise ActionDeclarationError(
                f"checks[{index}] must contain label, left, op, right"
            )
        label = _nonempty(row["label"], f"checks[{index}].label")
        op = row["op"]
        if op not in OPS:
            raise ActionDeclarationError(f"checks[{index}] has unknown op {op!r}")
        left = _expr(row["left"], bundle, signature, selectors, f"checks[{index}].left")
        right = _expr(row["right"], bundle, signature, selectors, f"checks[{index}].right")
        _validate_comparison(
            _expr_type(left, bundle, signature),
            op,
            _expr_type(right, bundle, signature),
            f"checks[{index}]",
        )
        out.append({"label": label, "left": left, "op": op, "right": right})
    return tuple(out)


def _effects(value: object, bundle: dict[str, Any], signature: dict[str, Any], selectors: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], ...]:
    if not isinstance(value, list) or not value:
        raise ActionDeclarationError("effects must be a nonempty list")
    names = set(selectors)
    out: list[dict[str, Any]] = []
    for index, row in enumerate(value):
        if not isinstance(row, dict) or set(row) != {"participant", "path", "op", "value"}:
            raise ActionDeclarationError(
                f"effects[{index}] must contain participant, path, op, value"
            )
        participant = row["participant"]
        if participant not in names:
            raise ActionDeclarationError(
                f"effects[{index}] names unknown participant {participant!r}"
            )
        path = _nonempty(row["path"], f"effects[{index}].path")
        target_type = _path_type(bundle, path)
        if path == "last_cause_event_id":
            raise ActionDeclarationError("last_cause_event_id is engine-owned and cannot be authored as an effect")
        _require_selector_path(selectors[participant], path, f"effects[{index}]")
        op = row["op"]
        if op not in EFFECT_OPS:
            raise ActionDeclarationError(f"effects[{index}] has unknown op {op!r}")
        expr = _expr(row["value"], bundle, signature, selectors, f"effects[{index}].value")
        source_type = _expr_type(expr, bundle, signature)
        if op == "set":
            if not _compatible(target_type, source_type):
                raise ActionDeclarationError(
                    f"effects[{index}] cannot set {target_type} from {source_type}"
                )
        elif target_type not in {"integer", "number"} or source_type not in {"integer", "number"}:
            raise ActionDeclarationError(
                f"effects[{index}] {op} requires numeric target and value"
            )
        out.append(
            {
                "participant": participant,
                "path": path,
                "op": op,
                "value": expr,
            }
        )
    return tuple(out)


def _derived_reads(actor_selector: dict[str, Any], participants: dict[str, dict[str, Any]], checks: tuple[dict[str, Any], ...], effects: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
    reads: set[str] = set()
    for name, selector in [("actor", actor_selector), *sorted(participants.items())]:
        if selector.get("categories"):
            reads.add(f"entities.<{name}>.category_ids")
        for component in selector.get("components", []):
            reads.add(f"entities.<{name}>.components.{component}")
    for row in checks:
        for side in (row["left"], row["right"]):
            if "participant" in side:
                ref = side["participant"]
                reads.add(f"entities.<{ref['name']}>.{ref['path']}")
    for row in effects:
        if row["op"] in {"add", "subtract"}:
            reads.add(f"entities.<{row['participant']}>.{row['path']}")
        expr = row["value"]
        if "participant" in expr:
            ref = expr["participant"]
            reads.add(f"entities.<{ref['name']}>.{ref['path']}")
    return tuple(sorted(reads))


def _derived_writes(effects: tuple[dict[str, Any], ...]) -> tuple[str, ...]:
    writes: set[str] = set()
    for row in effects:
        participant = row["participant"]
        writes.add(f"entities.<{participant}>.{row['path']}")
        writes.add(f"entities.<{participant}>.last_cause_event_id")
    return tuple(sorted(writes))


# ---------------------------------------------------------------------------
# Runtime helpers


def _entity_value(entity: Entity, path: str) -> Any:
    parts = path.split(".")
    if parts[0] == "components":
        current: Any = entity.component(parts[1])
        parts = parts[2:]
    else:
        current = getattr(entity, parts[0], None)
        parts = parts[1:]
    for part in parts:
        if current is None:
            return None
        current = getattr(current, part, None)
    return current


def _assign_entity_value(entity: Entity, path: str, op: str, value: Any) -> None:
    parts = path.split(".")
    if parts[0] == "components":
        holder: Any = entity.component(parts[1])
        parts = parts[2:]
    else:
        holder = getattr(entity, parts[0], None)
        parts = parts[1:]
    for part in parts[:-1]:
        holder = getattr(holder, part, None)
    if holder is None or not parts:
        raise ActionDeclarationError(
            f"effect path {path} is absent on entity {entity.entity_id}"
        )
    field = parts[-1]
    current = getattr(holder, field)
    if op == "set":
        setattr(holder, field, deepcopy(value))
    elif op == "add":
        setattr(holder, field, current + value)
    elif op == "subtract":
        setattr(holder, field, current - value)
    else:
        raise ActionDeclarationError(f"unknown effect op {op!r}")


def _resolve_expr(expr: dict[str, Any], world: World, action: dict[str, Any], participants: dict[str, str], event_id: str | None) -> Any:
    if "literal" in expr:
        return deepcopy(expr["literal"])
    if "action_field" in expr:
        return action[expr["action_field"]]
    if "participant" in expr:
        ref = expr["participant"]
        entity_id = participants[ref["name"]]
        return _entity_value(world.entities[entity_id], ref["path"])
    if "entity_id" in expr:
        return participants[expr["entity_id"]]
    if "owner_ref" in expr:
        entity_id = participants[expr["owner_ref"]]
        return owner_ref("actor", entity_id)
    if "event_id" in expr:
        if event_id is None:
            raise ActionDeclarationError("event_id is unavailable during checks")
        return event_id
    raise ActionDeclarationError("unresolvable expression")


def _compare(left: Any, op: str, right: Any) -> bool:
    try:
        return bool(OPS[op](left, right))
    except (TypeError, KeyError):
        return False
