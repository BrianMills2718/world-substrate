"""Canonical transition authority with causal events and exact replay."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from .model import World, differences
from .rules import (
    Check,
    DeclaresCausalParents,
    DeclaresConsequences,
    DeclaresProcessCausalParents,
    DescribesEffects,
    ProcessRule,
    ReceivesProcessEventId,
    ReportsProgress,
    RuleRegistry,
    TypedAction,
    UnsupportedAction,
)
from .information import entity_visible_to_actor, observation_information_context
from .semantic import SEMANTIC_BINDINGS

ENGINE_OWNED_PATHS: frozenset[str] = frozenset({"revision"})
# Entity references are found by asking the world, not by guessing at key
# names. The first version of this listed Castaway's action vocabulary
# ("vessel", "source", "target", ...), which silently rejected legitimate
# writes in any world whose actions name their participants differently -- the
# workshop world's `item`, `part` and `assembly` keys bound to nothing, so a
# correctly declared write looked out of scope (M6 finding).


class ScopeViolation(RuntimeError):
    """A registered rule exceeded its authority over the world."""


class CausalParentViolation(RuntimeError):
    """A rule declared hard ancestry outside retained canonical history."""


def _validate_causal_parent_ids(
    parent_ids: list[str],
    events: list[dict[str, Any]],
    rule_id: str,
) -> list[str]:
    """Require hard parents to be stable IDs already present in history."""

    if any(not isinstance(parent_id, str) or not parent_id for parent_id in parent_ids):
        raise CausalParentViolation(
            f"rule {rule_id} declared a causal parent that is not a nonempty event id"
        )
    known_ids = {event.get("event_id") for event in events}
    unknown = sorted(set(parent_ids) - known_ids)
    if unknown:
        raise CausalParentViolation(
            f"rule {rule_id} declared causal parents outside retained history: {unknown}"
        )
    return sorted(set(parent_ids))


# The engine's own envelope metadata. `kind` names the action and `controller`
# names whoever submitted it; neither is a world participant, and both are
# free-form strings the submitter chooses. Counting them as participants let an
# untrusted envelope widen a rule's write scope to any entity it cared to name:
# the same defective rule was refused with `controller="script"` and accepted
# with `controller="wrench-1"`. Excluding the engine's four reserved fields is
# not the hand-listed Castaway vocabulary M6 removed -- every other key is
# world-specific participant naming and still counts, whatever it is called.
_ENVELOPE_METADATA: frozenset[str] = frozenset({"kind", "controller", "base_revision"})


def _action_entity_refs(
    record: dict[str, Any], known_ids: frozenset[str]
) -> frozenset[str]:
    """Entity identifiers the attempt itself names as participants."""
    return frozenset(
        value
        for key, value in record.items()
        if key not in _ENVELOPE_METADATA
        and isinstance(value, str)
        and value in known_ids
    )


def _path_permitted(
    changed_path: str,
    declared_paths: tuple[str, ...],
    bound_refs: frozenset[str] | None,
) -> bool:
    """Whether one changed leaf path falls under a declared write path.

    A declared path is a prefix: declaring ``entities.<vessel>.liquid``
    permits ``entities.<vessel>.liquid.volume_ml``. A ``<name>`` segment
    matches exactly one path segment. When ``bound_refs`` is supplied -- an
    action names its participants -- a placeholder may only bind to an entity
    the attempt itself referenced, so a rule cannot reach a third party
    through a correctly shaped path. Processes are universally quantified over
    the entities they apply to and pass ``None``.
    """

    changed = changed_path.split(".")
    for declared_path in declared_paths:
        declared = declared_path.split(".")
        if len(declared) > len(changed):
            continue
        for declared_segment, changed_segment in zip(declared, changed):
            if declared_segment.startswith("<") and declared_segment.endswith(">"):
                if bound_refs is not None and changed_segment not in bound_refs:
                    break
            elif declared_segment != changed_segment:
                break
        else:
            return True
    return False


def _scope_violations(
    changes: list[dict[str, Any]],
    declared_paths: tuple[str, ...],
    bound_refs: frozenset[str] | None,
) -> list[str]:
    """Changed paths the rule never declared, in deterministic order."""
    return sorted(
        {
            change["path"]
            for change in changes
            if change["path"] not in ENGINE_OWNED_PATHS
            and not _path_permitted(change["path"], declared_paths, bound_refs)
        }
    )


def _rule_world(world: World) -> World:
    """Detached material state for rule code, with engine-owned history hidden.

    Rules need the same typed world shape they already consume, but commands and
    events are coordinator-owned history rather than mechanic state. Replacing
    those lists in the deepcopy memo avoids both exposing committed event
    objects and paying to copy a history the rule has no authority to mutate.
    """
    return deepcopy(world, {id(world.commands): [], id(world.events): []})


def _rule_mutations(before: dict[str, Any], world: World) -> list[str]:
    """Any mutation made by a hook that is required to be read-only."""
    paths = {change["path"] for change in differences(before, world.material_dict())}
    if world.commands:
        paths.add("commands")
    if world.events:
        paths.add("events")
    return sorted(paths)


def _engine_owned_mutations(before: dict[str, Any], world: World) -> list[str]:
    """Writes a rule may never propose, even inside its declared state scope."""
    paths = {
        change["path"]
        for change in differences(before, world.material_dict())
        if change["path"] in ENGINE_OWNED_PATHS
    }
    if world.commands:
        paths.add("commands")
    if world.events:
        paths.add("events")
    return sorted(paths)


def _identifier(prefix: str, count: int) -> str:
    return f"{prefix}{count:05d}"


def _action_id(action: TypedAction) -> str:
    encoded = json.dumps(
        action.as_dict(), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()[:12]


def _world_component_types(world: World) -> dict[str, type]:
    """Component classes actually carried by one world, keyed by component name."""
    result: dict[str, type] = {}
    for entity in world.entities.values():
        for name, component in entity.components.items():
            component_type = type(component)
            existing = result.get(name)
            if existing is not None and existing is not component_type:
                raise ValueError(
                    f"world carries multiple component classes for {name!r}: "
                    f"{existing} and {component_type}"
                )
            result[name] = component_type
    return result


class Engine:
    def _bearer_of(self, action: TypedAction) -> dict[str, Any]:
        record = action.as_dict()
        actor = record.get("actor")
        return {
            "kind": "actor",
            "id": actor if isinstance(actor, str) else None,
            "controller": record.get("controller"),
        }

    def _binding_of(self, action: TypedAction) -> dict[str, Any] | None:
        binding = SEMANTIC_BINDINGS.get(action.kind)
        return binding.as_dict() if binding is not None else None

    def _observation_of(self, action: TypedAction) -> dict[str, Any] | None:
        """What the actor could see when it chose, or None if it cannot see."""
        actor = action.as_dict().get("actor")
        if not isinstance(actor, str):
            return None
        entity = self.world.entities.get(actor)
        if entity is None or entity.location is None:
            return None
        return self.observe(actor)

    def __init__(self, world: World, registry: RuleRegistry):
        world.validate()
        if world.rule_versions != registry.versions():
            raise ValueError("world rule versions do not match the executable registry")
        self.world = world
        self.registry = registry
        self._component_types = _world_component_types(world)
        self._initial_snapshot = world.snapshot()

    def initial_snapshot(self) -> dict[str, Any]:
        """Return the versioned initial state required for independent replay."""
        return deepcopy(self._initial_snapshot)

    def observe(self, actor_id: str) -> dict[str, Any]:
        actor = self.world.entities.get(actor_id)
        # An observer needs a place to observe from. It does not need to be a
        # Castaway survivor: requiring ActorState here made health/hydration a
        # precondition of being able to see anything, which is freshwater
        # content sitting in the substrate's observation path (M6 finding).
        if actor is None or actor.location is None:
            raise ValueError("unknown actor")
        local = {}
        for entity_id, entity in self.world.entities.items():
            entity_location = entity.location.location_id if entity.location else None
            if (
                (entity_id == actor_id or entity_location == actor.location.location_id)
                and entity_visible_to_actor(self.world, actor_id, entity)
            ):
                projected = entity.as_dict()
                if entity.actor is not None and entity_id != actor_id:
                    projected["actor"] = {
                        "health": entity.actor.health,
                        "alive": entity.actor.alive,
                    }
                local[entity_id] = projected
        return {
            "world_id": self.world.world_id,
            "revision": self.world.revision,
            "tick": self.world.tick,
            "actor_id": actor_id,
            "entities": local,
        }

    def _readonly_call(
        self,
        world: World,
        before: dict[str, Any],
        rule_id: str,
        hook: str,
        call: Any,
    ) -> Any:
        result = call()
        mutations = _rule_mutations(before, world)
        if mutations:
            raise ScopeViolation(
                f"{rule_id}.{hook} mutated a read-only rule view: {mutations}"
            )
        return result

    def _consequences(
        self,
        rule: Any,
        action: TypedAction,
        world: World,
        before: dict[str, Any],
    ) -> list[str]:
        if not isinstance(rule, DeclaresConsequences):
            return []
        return list(
            self._readonly_call(
                world,
                before,
                rule.rule_id,
                "consequences",
                lambda: rule.consequences(world, action),
            )
        )

    def _effect_preview(
        self,
        rule: Any,
        action: TypedAction,
        world: World,
        before: dict[str, Any],
    ) -> list[str]:
        if not isinstance(rule, DescribesEffects):
            return []
        return list(
            self._readonly_call(
                world,
                before,
                rule.rule_id,
                "effect_preview",
                lambda: rule.effect_preview(world, action),
            )
        )

    def _progress(
        self, world: World, before: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """In-flight process progress, for policies that must not act early.

        A policy could always read `container.boiling_ticks` -- it is in the
        observation like every other field. What it could not read was the
        threshold: `boiling_ticks: 1` means nothing without knowing two
        consecutive ticks are needed, so the M5 run pulled the pot off the fire
        early and oscillated heat/unheat for seven turns. A process that
        accumulates toward a threshold declares it here and the affordance page
        carries current-against-required.

        Declared, not inferred: the substrate cannot know which of a world's
        fields are counters toward something.
        """
        rows: list[dict[str, Any]] = []
        for process in self.registry.processes():
            if not isinstance(process, ReportsProgress):
                continue
            progress = self._readonly_call(
                world,
                before,
                process.rule_id,
                "progress",
                lambda process=process: process.progress(world),
            )
            for row in progress:
                rows.append({"rule_id": process.rule_id, **row})
        return sorted(rows, key=lambda row: (row["entity_id"], row["rule_id"]))

    def discover(self, actor_id: str, kind: str | None = None) -> dict[str, Any]:
        # One detached view is enough for the whole affordance page. Every hook
        # is checked immediately after it returns; if it mutates the view we
        # fail before any subsequent hook can consume the altered state.
        world = _rule_world(self.world)
        before = world.material_dict()
        actions: list[TypedAction] = []
        for action_kind in self.registry.action_kinds():
            if kind is None or action_kind == kind:
                rule = self.registry.action(action_kind)
                assert rule is not None
                discovered = self._readonly_call(
                    world,
                    before,
                    rule.rule_id,
                    "discover",
                    lambda rule=rule: rule.discover(world, actor_id),
                )
                actions.extend(discovered)
        available = []
        blocked = []
        for action in actions:
            rule = self.registry.action(action.kind)
            assert rule is not None
            checks = self._readonly_call(
                world,
                before,
                rule.rule_id,
                "checks",
                lambda rule=rule, action=action: rule.checks(world, action),
            )
            row = {
                "action_id": _action_id(action),
                "action": action.as_dict(),
                "checks": [check.as_dict() for check in checks],
                # What taking this action would destroy. A check says whether
                # an action is permitted; nothing said whether a permitted
                # action throws away something the actor already has. `fill`
                # was presented identically whether or not it re-contaminated a
                # treated vessel, and the M5 policy filled its own boiled pot
                # and then drank it (M5 finding).
                "consequences": self._consequences(rule, action, world, before),
                "effects": self._effect_preview(rule, action, world, before),
            }
            if all(check.ok for check in checks):
                available.append(row)
            else:
                row["reason"] = "; ".join(
                    check.label for check in checks if not check.ok
                )
                blocked.append(row)
        return {
            "observation": self.observe(actor_id),
            "available": available,
            "blocked": blocked,
            "progress": self._progress(world, before),
            "total": len(available) + len(blocked),
        }

    def submit(self, value: object) -> dict[str, Any]:
        """Validate an untrusted action envelope before entering typed rules."""
        errors: list[str] = []
        if not isinstance(value, dict):
            errors.append("action envelope must be an object")
            return self._reject_invalid(value, errors)
        if any(not isinstance(key, str) for key in value):
            errors.append("action envelope keys must be strings")
        for field in ("actor", "kind", "controller"):
            if not isinstance(value.get(field), str) or not value[field]:
                errors.append(f"{field} must be a nonempty string")
        if type(value.get("base_revision")) is not int:
            errors.append("base_revision must be an integer")
        if errors:
            return self._reject_invalid(value, errors)

        kind = str(value["kind"])
        rule = self.registry.action(kind)
        if rule is None:
            return self.apply(UnsupportedAction.from_dict(value))
        try:
            action = rule.action_from_dict(value)
        except (KeyError, TypeError, ValueError) as error:
            return self._reject_invalid(value, [f"invalid {kind} payload: {error}"])
        return self.apply(action)

    def _claimed_bearer(self, value: object) -> dict[str, Any] | None:
        """Who an untrusted envelope claims is acting, if it says at all.

        Marked `claimed_actor` rather than `actor` because nothing here has
        been validated -- the envelope is malformed by definition at this
        point, and the named actor may not exist. Recording it anyway matters
        because every untrusted policy submission arrives through this path,
        so these are exactly the events an inspector needs attributed.
        """
        if not isinstance(value, dict):
            return None
        actor = value.get("actor")
        controller = value.get("controller")
        if not isinstance(actor, str) or not actor:
            return None
        return {
            "kind": "claimed_actor",
            "id": actor,
            "controller": controller if isinstance(controller, str) else None,
        }

    def _observation_for_actor(self, actor_id: str | None) -> dict[str, Any] | None:
        if not isinstance(actor_id, str):
            return None
        entity = self.world.entities.get(actor_id)
        if entity is None or entity.location is None:
            return None
        return self.observe(actor_id)

    def _reject_invalid(self, value: object, errors: list[str]) -> dict[str, Any]:
        command_id = _identifier("c", len(self.world.commands) + 1)
        event_id = _identifier("e", len(self.world.events) + 1)
        before = self.world.material_dict()
        bearer = self._claimed_bearer(value)
        checks = [
            Check(
                "Valid action envelope",
                False,
                errors,
                "registered typed action or structurally valid unsupported action",
            )
        ]
        event = self._event(
            event_id=event_id,
            rule_id="system.action-envelope",
            rule_version="1",
            cause=command_id,
            status="invalid_action",
            checks=checks,
            before=before,
            after=before,
            read_paths=(),
            write_paths=(),
            bearer=bearer,
            binding=None,
            observation=self._observation_for_actor(
                bearer["id"] if bearer else None
            ),
        )
        self.world.commands.append(
            {
                "command_id": command_id,
                "op": "invalid_action",
                "record": deepcopy(value),
                "status": "invalid_action",
            }
        )
        self.world.events.append(event)
        return {"status": "invalid_action", "event": event}

    def _event(
        self,
        *,
        event_id: str,
        rule_id: str,
        rule_version: str,
        cause: str,
        status: str,
        checks: list[Check],
        before: dict[str, Any],
        after: dict[str, Any],
        read_paths: tuple[str, ...],
        write_paths: tuple[str, ...],
        bearer: dict[str, Any] | None = None,
        binding: dict[str, Any] | None = None,
        observation: dict[str, Any] | None = None,
        causal_parent_event_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        # Decision 002 requires eight things be inspectable per transition.
        # bearer, binding and observation are the three that were computed
        # elsewhere in this engine and never attached, so an inspector reading
        # world.events could not tell who acted, what their attempt meant, or
        # what they had been shown. Emitted explicitly as null rather than
        # omitted, so "there was no observer" is distinguishable from "not
        # recorded" -- a process has no observation and says so.
        event = {
            "event_id": event_id,
            "causal_bearer": bearer,
            "semantic_binding": binding,
            "observation": observation,
            "tick": after["tick"],
            "world_revision": after["revision"],
            "rule_id": rule_id,
            "rule_version": rule_version,
            "cause": cause,
            "status": status,
            "checks": [check.as_dict() for check in checks],
            "declared_read_paths": list(read_paths),
            "declared_write_paths": list(write_paths),
            "changes": differences(before, after),
            "hash_before": _material_hash(before),
            "hash_after": _material_hash(after),
        }
        # Keep existing event wire output byte-compatible for rules that do not
        # opt into hard ancestry. Information present in the observation is
        # separately summarized as context evidence only when it exists.
        if causal_parent_event_ids is not None:
            event["causal_parent_event_ids"] = sorted(set(causal_parent_event_ids))
        information_context = observation_information_context(observation)
        if information_context:
            event["information_context"] = information_context
        return event

    def apply(self, action: TypedAction) -> dict[str, Any]:
        rule = self.registry.action(action.kind)
        command_id = _identifier("c", len(self.world.commands) + 1)
        event_id = _identifier("e", len(self.world.events) + 1)
        before = self.world.material_dict()
        # Captured before anything mutates: this is what the actor could see
        # at the moment it chose, which is the field Decision 002 asks for.
        observation = self._observation_of(action)
        revision_check = Check(
            "Base revision is current",
            action.base_revision == self.world.revision,
            action.base_revision,
            self.world.revision,
        )
        if rule is None:
            checks = [
                revision_check,
                Check("Registered action rule", False, action.kind),
            ]
            return self._reject(
                action,
                command_id,
                event_id,
                "unsupported_action",
                checks,
                before,
                observation,
            )

        # Checks execute against the same detached candidate the rule may later
        # propose effects on. This adds no second world clone to the accepted
        # path while still making any check-time mutation observable and safe to
        # discard.
        candidate = _rule_world(self.world)
        checks = [revision_check] + rule.checks(candidate, action)
        check_mutations = _rule_mutations(before, candidate)
        if check_mutations:
            return self._reject(
                action,
                command_id,
                event_id,
                "scope_violation",
                checks
                + [
                    Check(
                        "Rule checks are read-only",
                        False,
                        check_mutations,
                        [],
                    )
                ],
                before,
                observation,
            )
        if not revision_check.ok:
            return self._reject(
                action, command_id, event_id, "stale_revision", checks, before, observation
            )
        if not all(check.ok for check in checks):
            return self._reject(
                action,
                command_id,
                event_id,
                "precondition_failed",
                checks,
                before,
                observation,
            )

        causal_parents = (
            list(
                self._readonly_call(
                    candidate,
                    before,
                    rule.rule_id,
                    "causal_parents",
                    lambda: rule.causal_parents(candidate, action),
                )
            )
            if isinstance(rule, DeclaresCausalParents)
            else None
        )
        if causal_parents is not None:
            causal_parents = _validate_causal_parent_ids(
                causal_parents, self.world.events, rule.rule_id
            )
        rule.apply(candidate, action, event_id)
        authority_violations = _engine_owned_mutations(before, candidate)
        if authority_violations:
            return self._reject(
                action,
                command_id,
                event_id,
                "scope_violation",
                checks
                + [
                    Check(
                        "Rules cannot write engine-owned state or history",
                        False,
                        authority_violations,
                        [],
                    )
                ],
                before,
                observation,
            )

        # Revision belongs to the enclosing coordinator. It is incremented only
        # after the rule's proposal has been checked for engine-owned writes.
        candidate.revision += 1
        candidate.validate()
        after = candidate.material_dict()
        violations = _scope_violations(
            differences(before, after),
            rule.write_paths,
            _action_entity_refs(action.as_dict(), frozenset(self.world.entities)),
        )
        if violations:
            # The rule is defective, not the attempt. Discard the candidate so
            # nothing commits, and record which undeclared paths it reached.
            return self._reject(
                action,
                command_id,
                event_id,
                "scope_violation",
                checks
                + [
                    Check(
                        "Committed writes stay in declared scope",
                        False,
                        violations,
                        list(rule.write_paths),
                    )
                ],
                before,
                observation,
            )
        event = self._event(
            event_id=event_id,
            rule_id=rule.rule_id,
            rule_version=rule.version,
            cause=command_id,
            status="accepted",
            checks=checks,
            before=before,
            after=after,
            read_paths=rule.read_paths,
            write_paths=rule.write_paths,
            bearer=self._bearer_of(action),
            binding=self._binding_of(action),
            observation=observation,
            causal_parent_event_ids=causal_parents,
        )
        candidate.commands = list(self.world.commands)
        candidate.events = list(self.world.events)
        candidate.commands.append(
            {
                "command_id": command_id,
                "op": "action",
                "action": action.as_dict(),
                "status": "accepted",
            }
        )
        candidate.events.append(event)
        self.world = candidate
        return {"status": "accepted", "event": event}

    def _reject(
        self,
        action: TypedAction,
        command_id: str,
        event_id: str,
        status: str,
        checks: list[Check],
        before: dict[str, Any],
        observation: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        rule = self.registry.action(action.kind)
        event = self._event(
            event_id=event_id,
            rule_id=rule.rule_id if rule else f"unsupported.{action.kind}",
            rule_version=rule.version if rule else "0",
            cause=command_id,
            status=status,
            checks=checks,
            before=before,
            after=before,
            read_paths=rule.read_paths if rule else (),
            write_paths=rule.write_paths if rule else (),
            bearer=self._bearer_of(action),
            binding=self._binding_of(action),
            observation=observation,
        )
        self.world.commands.append(
            {
                "command_id": command_id,
                "op": "action",
                "action": action.as_dict(),
                "status": status,
            }
        )
        self.world.events.append(event)
        return {"status": status, "event": event}

    def advance(self, steps: int = 1) -> dict[str, Any]:
        if type(steps) is not int or steps < 1:
            raise ValueError("steps must be a positive integer")
        produced: list[dict[str, Any]] = []
        for _ in range(steps):
            saved = self.world.clone()
            command_id = _identifier("c", len(self.world.commands) + 1)
            try:
                self.world.commands.append(
                    {
                        "command_id": command_id,
                        "op": "advance",
                        "steps": 1,
                        "status": "accepted",
                    }
                )
                for process in self.registry.processes():
                    # Build the process candidate before checking its trigger.
                    # A due() hook that writes can only corrupt this detached
                    # view, and a due process reuses the same candidate for its
                    # effect proposal rather than paying for another clone.
                    candidate = _rule_world(self.world)
                    before = candidate.material_dict()
                    due = self._readonly_call(
                        candidate,
                        before,
                        process.rule_id,
                        "due",
                        lambda process=process: process.due(candidate),
                    )
                    if due:
                        produced.append(
                            self._apply_process(process, command_id, candidate, before)
                        )
            except Exception:
                self.world = saved
                raise
        return {"status": "accepted", "events": produced}

    def _apply_process(
        self,
        process: ProcessRule,
        command_id: str,
        candidate: World,
        before: dict[str, Any],
    ) -> dict[str, Any]:
        event_id = _identifier("e", len(self.world.events) + 1)
        causal_parents = (
            list(
                self._readonly_call(
                    candidate,
                    before,
                    process.rule_id,
                    "causal_parents",
                    lambda: process.causal_parents(candidate),
                )
            )
            if isinstance(process, DeclaresProcessCausalParents)
            else None
        )
        if causal_parents is not None:
            causal_parents = _validate_causal_parent_ids(
                causal_parents, self.world.events, process.rule_id
            )
        if isinstance(process, ReceivesProcessEventId):
            process.apply_with_event_id(candidate, event_id)
        else:
            process.apply(candidate)
        authority_violations = _engine_owned_mutations(before, candidate)
        if authority_violations:
            raise ScopeViolation(
                f"process {process.rule_id} wrote engine-owned state or history: "
                f"{authority_violations}"
            )
        if candidate.material_dict() == before:
            return {}
        candidate.revision += 1
        candidate.validate()
        after = candidate.material_dict()
        violations = _scope_violations(
            differences(before, after), process.write_paths, None
        )
        if violations:
            # A process is the world's own law: there is no attempt to refuse,
            # so a defective one stops the tick loudly. Engine.advance restores
            # the pre-tick state before this propagates.
            raise ScopeViolation(
                f"process {process.rule_id} wrote outside its declared scope: "
                f"{violations} (declared {list(process.write_paths)})"
            )
        event = self._event(
            event_id=event_id,
            rule_id=process.rule_id,
            rule_version=process.version,
            cause=command_id,
            status="accepted",
            checks=[],
            before=before,
            after=after,
            read_paths=process.read_paths,
            write_paths=process.write_paths,
            bearer={"kind": "process", "id": process.rule_id, "controller": None},
            binding=None,
            observation=None,
            causal_parent_event_ids=causal_parents,
        )
        candidate.commands = list(self.world.commands)
        candidate.events = list(self.world.events)
        candidate.events.append(event)
        self.world = candidate
        return event

    @classmethod
    def replay_commands(
        cls,
        *,
        initial_snapshot: object,
        commands: object,
        registry: RuleRegistry,
        component_types: dict[str, type] | None = None,
    ) -> Engine:
        """Rebuild an engine using only a loaded snapshot, commands, and registry."""
        if not isinstance(commands, list):
            raise TypeError("replay commands must be an array")
        replayed = cls(
            World.from_snapshot(initial_snapshot, component_types=component_types),
            registry,
        )
        for index, command in enumerate(commands, start=1):
            if not isinstance(command, dict):
                raise TypeError(f"replay command {index} must be an object")
            op = command.get("op")
            if op == "action":
                result = replayed.submit(command.get("action"))
            elif op == "invalid_action":
                result = replayed.submit(command.get("record"))
            elif op == "advance":
                steps = command.get("steps")
                if type(steps) is not int:
                    raise TypeError(f"replay command {index} steps must be an integer")
                result = replayed.advance(steps)
            else:
                raise ValueError(f"unknown recorded command op: {op}")
            if result["status"] != command.get("status"):
                raise ValueError(
                    f"replay command {index} status differs: "
                    f"expected {command.get('status')}, got {result['status']}"
                )
        return replayed

    def replay(self) -> dict[str, Any]:
        recorded = deepcopy(self.world.commands)
        replayed = self.replay_commands(
            initial_snapshot=self.initial_snapshot(),
            commands=recorded,
            registry=self.registry,
            component_types=self._component_types,
        )
        expected = self.world.material_hash()
        actual = replayed.world.material_hash()
        event_match = self.world.events == replayed.world.events
        return {
            "ok": expected == actual and event_match,
            "steps": len(recorded),
            "expected": expected,
            "actual": actual,
            "event_match": event_match,
        }


def _material_hash(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()
