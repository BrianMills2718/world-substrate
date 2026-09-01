"""Canonical transition authority with causal events and exact replay."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from .model import World, differences
from .rules import Check, ProcessRule, RuleRegistry, TypedAction


def _identifier(prefix: str, count: int) -> str:
    return f"{prefix}{count:05d}"


def _action_id(action: TypedAction) -> str:
    encoded = json.dumps(
        action.as_dict(), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()[:12]


class Engine:
    def __init__(self, world: World, registry: RuleRegistry):
        world.validate()
        if world.rule_versions != registry.versions():
            raise ValueError("world rule versions do not match the executable registry")
        self.world = world
        self.registry = registry
        self.initial_world = world.clone()
        self.initial_world.commands = []
        self.initial_world.events = []

    def observe(self, actor_id: str) -> dict[str, Any]:
        actor = self.world.entities.get(actor_id)
        if actor is None or actor.actor is None or actor.location is None:
            raise ValueError("unknown actor")
        local = {}
        for entity_id, entity in self.world.entities.items():
            entity_location = entity.location.location_id if entity.location else None
            if entity_id == actor_id or entity_location == actor.location.location_id:
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

    def discover(self, actor_id: str, kind: str | None = None) -> dict[str, Any]:
        actions: list[TypedAction] = []
        for action_kind in self.registry.action_kinds():
            if kind is None or action_kind == kind:
                rule = self.registry.action(action_kind)
                assert rule is not None
                actions.extend(rule.discover(self.world, actor_id))
        available = []
        blocked = []
        for action in actions:
            rule = self.registry.action(action.kind)
            assert rule is not None
            checks = rule.checks(self.world, action)
            row = {
                "action_id": _action_id(action),
                "action": action.as_dict(),
                "checks": [check.as_dict() for check in checks],
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
            "total": len(available) + len(blocked),
        }

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
    ) -> dict[str, Any]:
        return {
            "event_id": event_id,
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

    def apply(self, action: TypedAction) -> dict[str, Any]:
        rule = self.registry.action(action.kind)
        command_id = _identifier("c", len(self.world.commands) + 1)
        event_id = _identifier("e", len(self.world.events) + 1)
        before = self.world.material_dict()
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
                action, command_id, event_id, "unsupported_action", checks, before
            )
        checks = [revision_check] + rule.checks(self.world, action)
        if not revision_check.ok:
            return self._reject(
                action, command_id, event_id, "stale_revision", checks, before
            )
        if not all(check.ok for check in checks):
            return self._reject(
                action, command_id, event_id, "precondition_failed", checks, before
            )

        candidate = self.world.clone()
        rule.apply(candidate, action, event_id)
        candidate.revision += 1
        candidate.validate()
        after = candidate.material_dict()
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
        )
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
                    if process.due(self.world):
                        produced.append(self._apply_process(process, command_id))
            except Exception:
                self.world = saved
                raise
        return {"status": "accepted", "events": produced}

    def _apply_process(self, process: ProcessRule, command_id: str) -> dict[str, Any]:
        before = self.world.material_dict()
        candidate = self.world.clone()
        process.apply(candidate)
        if candidate.material_dict() == before:
            return {}
        candidate.revision += 1
        candidate.validate()
        after = candidate.material_dict()
        event_id = _identifier("e", len(self.world.events) + 1)
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
        )
        candidate.events.append(event)
        self.world = candidate
        return event

    def replay(self) -> dict[str, Any]:
        recorded = deepcopy(self.world.commands)
        replayed = Engine(self.initial_world.clone(), self.registry)
        for command in recorded:
            if command["op"] == "action":
                action_record = command["action"]
                rule = self.registry.action(str(action_record["kind"]))
                if rule is None:
                    raise ValueError(
                        f"recorded action rule is unavailable: {action_record['kind']}"
                    )
                replayed.apply(rule.action_from_dict(action_record))
            else:
                replayed.advance(int(command["steps"]))
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
