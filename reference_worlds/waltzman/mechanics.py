"""Executable laws for the Waltzman Coordination Lab demo.

The rules deliberately separate represented information delivery, explicit
commitments, shared constraints, institutional recomputation, and analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from world_substrate.information import DELIVERED_STATUSES
from world_substrate.model import World
from world_substrate.rules import Check, TypedAction, _require_nonempty_string


def _resident(world: World, actor_id: str):
    actor = world.entities.get(actor_id)
    if actor is None or actor.component("resident") is None or actor.location is None:
        return None
    return actor


def _expected_stance(world: World, actor_id: str) -> str | None:
    actor = _resident(world, actor_id)
    if actor is None:
        return None
    commitment = actor.component("commitment")
    if commitment is None:
        return None
    constraint = world.entities.get(commitment.constraint_id)
    if constraint is None:
        return None
    resource = constraint.component("resource")
    if resource is not None:
        return "support" if resource.current >= resource.required else "conditional"
    state = constraint.component("constraint")
    if state is not None:
        return "support" if state.status == state.required_status else "conditional"
    return None


def _last_event(world: World, entity_id: str) -> str | None:
    entity = world.entities.get(entity_id)
    return entity.last_cause_event_id if entity is not None else None


def _actor_received(world: World, actor_id: str, info_id: str) -> bool:
    return any(
        delivery.info_id == info_id
        and delivery.recipient_id == actor_id
        and delivery.status in DELIVERED_STATUSES
        for entity in world.entities.values()
        if (delivery := entity.component("delivery")) is not None
    )


@dataclass(frozen=True)
class CommunicateAction:
    actor_id: str
    information_id: str
    delivery_id: str
    base_revision: int
    controller_id: str
    kind: str = "communicate"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "information": self.information_id,
            "delivery": self.delivery_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> CommunicateAction:
        if value.get("kind") != "communicate":
            raise ValueError("record is not a communicate action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            information_id=_require_nonempty_string(value, "information"),
            delivery_id=_require_nonempty_string(value, "delivery"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class ReassessCommitmentAction:
    actor_id: str
    base_revision: int
    controller_id: str
    kind: str = "reassess_commitment"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> ReassessCommitmentAction:
        if value.get("kind") != "reassess_commitment":
            raise ValueError("record is not a reassess_commitment action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class StartMeetingAction:
    actor_id: str
    activity_id: str
    base_revision: int
    controller_id: str
    kind: str = "start_meeting"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "activity": self.activity_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> StartMeetingAction:
        if value.get("kind") != "start_meeting":
            raise ValueError("record is not a start_meeting action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            activity_id=_require_nonempty_string(value, "activity"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


@dataclass(frozen=True)
class DeliverPackageAction:
    actor_id: str
    package_id: str
    validation_id: str
    staffing_id: str
    reserve_id: str
    safeguard_id: str
    base_revision: int
    controller_id: str
    kind: str = "deliver_package"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "package": self.package_id,
            "validation": self.validation_id,
            "staffing": self.staffing_id,
            "reserve": self.reserve_id,
            "safeguard": self.safeguard_id,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> DeliverPackageAction:
        if value.get("kind") != "deliver_package":
            raise ValueError("record is not a deliver_package action")
        revision = value["base_revision"]
        if type(revision) is not int:
            raise TypeError("base_revision must be an integer")
        return cls(
            actor_id=_require_nonempty_string(value, "actor"),
            package_id=_require_nonempty_string(value, "package"),
            validation_id=_require_nonempty_string(value, "validation"),
            staffing_id=_require_nonempty_string(value, "staffing"),
            reserve_id=_require_nonempty_string(value, "reserve"),
            safeguard_id=_require_nonempty_string(value, "safeguard"),
            base_revision=revision,
            controller_id=_require_nonempty_string(value, "controller"),
        )


class CommunicateRule:
    rule_id = "waltzman.information.communicate"
    version = "1"
    action_kind = "communicate"
    read_paths = (
        "entities.<actor>.components.resident",
        "entities.<information>.components.information",
        "entities.<delivery>.components.delivery",
    )
    write_paths = (
        "entities.<information>.components.information.active",
        "entities.<information>.last_cause_event_id",
        "entities.<delivery>.components.delivery.status",
        "entities.<delivery>.components.delivery.delivered_tick",
        "entities.<delivery>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> CommunicateAction:
        return CommunicateAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        if _resident(world, actor_id) is None:
            return []
        rows: list[TypedAction] = []
        for info_entity in sorted(world.entities.values(), key=lambda row: row.entity_id):
            info = info_entity.component("information")
            if info is None or info.source_id != actor_id or info.active:
                continue
            for delivery_entity in sorted(world.entities.values(), key=lambda row: row.entity_id):
                delivery = delivery_entity.component("delivery")
                if (
                    delivery is not None
                    and delivery.info_id == info_entity.entity_id
                    and delivery.status == "pending"
                ):
                    action = CommunicateAction(
                        actor_id,
                        info_entity.entity_id,
                        delivery_entity.entity_id,
                        world.revision,
                        "unselected",
                    )
                    if all(check.ok for check in self.checks(world, action)):
                        rows.append(action)
        return rows

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, CommunicateAction):
            raise TypeError("communicate rule requires CommunicateAction")
        actor = _resident(world, action.actor_id)
        info_entity = world.entities.get(action.information_id)
        delivery_entity = world.entities.get(action.delivery_id)
        info = info_entity.component("information") if info_entity else None
        delivery = delivery_entity.component("delivery") if delivery_entity else None
        checks = [
            Check("Resident exists", actor is not None),
            Check("Information representation exists", info is not None),
            Check("Delivery representation exists", delivery is not None),
        ]
        if info is None or delivery is None:
            return checks
        checks.extend(
            [
                Check("Resident is represented source", info.source_id == action.actor_id),
                Check("Information is not already active", not info.active),
                Check("Delivery names information", delivery.info_id == action.information_id),
                Check("Channel agrees", delivery.channel_id == info.channel_id),
                Check("Delivery is pending", delivery.status == "pending"),
            ]
        )
        if info.derived_from_info_id:
            checks.append(
                Check(
                    "Resident received represented source information",
                    _actor_received(world, action.actor_id, info.derived_from_info_id),
                )
            )
        return checks

    def causal_parents(self, world: World, action: TypedAction) -> list[str]:
        assert isinstance(action, CommunicateAction)
        info_entity = world.entities[action.information_id]
        info = info_entity.component("information")
        assert info is not None
        if not info.derived_from_info_id:
            return []
        parent = _last_event(world, info.derived_from_info_id)
        return [parent] if parent else []

    def effect_preview(self, world: World, action: TypedAction) -> list[str]:
        assert isinstance(action, CommunicateAction)
        delivery = world.entities[action.delivery_id].component("delivery")
        assert delivery is not None
        return [f"deliver represented information to {delivery.recipient_id}"]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, CommunicateAction)
        info_entity = world.entities[action.information_id]
        delivery_entity = world.entities[action.delivery_id]
        info = info_entity.component("information")
        delivery = delivery_entity.component("delivery")
        assert info is not None and delivery is not None
        info.active = True
        delivery.status = "delivered"
        delivery.delivered_tick = world.tick
        info_entity.last_cause_event_id = event_id
        delivery_entity.last_cause_event_id = event_id


class ReassessCommitmentRule:
    rule_id = "waltzman.commitment.reassess"
    version = "1"
    action_kind = "reassess_commitment"
    read_paths = (
        "entities.<actor>.components.resident",
        "entities.<actor>.components.commitment",
        "entities.<constraint>.components.resource",
        "entities.<constraint>.components.constraint",
    )
    write_paths = (
        "entities.<actor>.components.commitment.stance",
        "entities.<actor>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> ReassessCommitmentAction:
        return ReassessCommitmentAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _resident(world, actor_id)
        if actor is None:
            return []
        commitment = actor.component("commitment")
        expected = _expected_stance(world, actor_id)
        if commitment is None or expected is None or commitment.stance == expected:
            return []
        return [ReassessCommitmentAction(actor_id, world.revision, "unselected")]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, ReassessCommitmentAction):
            raise TypeError("commitment rule requires ReassessCommitmentAction")
        actor = _resident(world, action.actor_id)
        commitment = actor.component("commitment") if actor else None
        constraint = world.entities.get(commitment.constraint_id) if commitment else None
        expected = _expected_stance(world, action.actor_id)
        return [
            Check("Resident exists", actor is not None),
            Check("Explicit commitment exists", commitment is not None),
            Check("Commitment constraint exists", constraint is not None),
            Check("Constraint yields a stance", expected is not None),
        ]

    def causal_parents(self, world: World, action: TypedAction) -> list[str]:
        assert isinstance(action, ReassessCommitmentAction)
        actor = world.entities[action.actor_id]
        commitment = actor.component("commitment")
        assert commitment is not None
        parent = _last_event(world, commitment.constraint_id)
        return [parent] if parent else []

    def effect_preview(self, world: World, action: TypedAction) -> list[str]:
        assert isinstance(action, ReassessCommitmentAction)
        expected = _expected_stance(world, action.actor_id)
        return [f"explicit commitment becomes {expected}"] if expected else []

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, ReassessCommitmentAction)
        actor = world.entities[action.actor_id]
        commitment = actor.component("commitment")
        expected = _expected_stance(world, action.actor_id)
        assert commitment is not None and expected is not None
        commitment.stance = expected
        actor.last_cause_event_id = event_id


class StartMeetingRule:
    rule_id = "waltzman.activity.start-meeting"
    version = "1"
    action_kind = "start_meeting"
    read_paths = (
        "entities.<actor>.components.resident",
        "entities.<activity>.components.activity",
    )
    write_paths = (
        "entities.<activity>.components.activity.status",
        "entities.<activity>.components.activity.started_tick",
        "entities.<activity>.components.activity.end_tick",
        "entities.<activity>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> StartMeetingAction:
        return StartMeetingAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _resident(world, actor_id)
        if actor is None or actor.component("resident").role != "regional coordinator":
            return []
        return [
            StartMeetingAction(actor_id, entity.entity_id, world.revision, "unselected")
            for entity in world.entities.values()
            if (activity := entity.component("activity")) is not None
            and activity.kind == "coordination-meeting"
            and activity.status == "pending"
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, StartMeetingAction):
            raise TypeError("start meeting rule requires StartMeetingAction")
        actor = _resident(world, action.actor_id)
        activity_entity = world.entities.get(action.activity_id)
        activity = activity_entity.component("activity") if activity_entity else None
        return [
            Check("Coordinator exists", bool(actor and actor.component("resident").role == "regional coordinator")),
            Check("Meeting exists", bool(activity and activity.kind == "coordination-meeting")),
            Check("Meeting is pending", bool(activity and activity.status == "pending")),
        ]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, StartMeetingAction)
        entity = world.entities[action.activity_id]
        activity = entity.component("activity")
        assert activity is not None
        activity.status = "active"
        activity.started_tick = world.tick
        activity.end_tick = world.tick + activity.duration_ticks
        entity.last_cause_event_id = event_id


class DeliverPackageRule:
    rule_id = "waltzman.intervention.deliver-package"
    version = "1"
    action_kind = "deliver_package"
    read_paths = (
        "entities.<actor>.components.resident",
        "entities.<package>.components.package",
        "entities.<validation>.components.resource",
        "entities.<staffing>.components.resource",
        "entities.<reserve>.components.resource",
        "entities.<safeguard>.components.constraint",
        "entities.coalition-hub.components.institution.status",
    )
    write_paths = (
        "entities.<package>.components.package.status",
        "entities.<package>.last_cause_event_id",
        "entities.<validation>.components.resource.current",
        "entities.<validation>.last_cause_event_id",
        "entities.<staffing>.components.resource.current",
        "entities.<staffing>.last_cause_event_id",
        "entities.<reserve>.components.resource.current",
        "entities.<reserve>.last_cause_event_id",
        "entities.<safeguard>.components.constraint.status",
        "entities.<safeguard>.last_cause_event_id",
    )

    def action_from_dict(self, value: dict[str, Any]) -> DeliverPackageAction:
        return DeliverPackageAction.from_dict(value)

    def discover(self, world: World, actor_id: str) -> list[TypedAction]:
        actor = _resident(world, actor_id)
        institution = world.entities["coalition-hub"].component("institution")
        package = world.entities["stabilization-package"].component("package")
        if (
            actor is None
            or actor.component("resident").role != "regional coordinator"
            or institution is None
            or institution.status != "blocked"
            or package is None
            or package.status != "available"
        ):
            return []
        return [
            DeliverPackageAction(
                actor_id,
                "stabilization-package",
                "validation-capacity",
                "clinical-staff",
                "shared-reserve",
                "safeguard-record",
                world.revision,
                "unselected",
            )
        ]

    def checks(self, world: World, action: TypedAction) -> list[Check]:
        if not isinstance(action, DeliverPackageAction):
            raise TypeError("deliver package rule requires DeliverPackageAction")
        actor = _resident(world, action.actor_id)
        package = world.entities.get(action.package_id)
        validation = world.entities.get(action.validation_id)
        staffing = world.entities.get(action.staffing_id)
        reserve = world.entities.get(action.reserve_id)
        safeguard = world.entities.get(action.safeguard_id)
        institution = world.entities["coalition-hub"].component("institution")
        return [
            Check("Coordinator exists", bool(actor and actor.component("resident").role == "regional coordinator")),
            Check("Package is available", bool(package and package.component("package") and package.component("package").status == "available")),
            Check("Validation resource exists", bool(validation and validation.component("resource"))),
            Check("Staffing resource exists", bool(staffing and staffing.component("resource"))),
            Check("Reserve resource exists", bool(reserve and reserve.component("resource"))),
            Check("Safeguard constraint exists", bool(safeguard and safeguard.component("constraint"))),
            Check("Coalition is blocked", bool(institution and institution.status == "blocked")),
        ]

    def causal_parents(self, world: World, action: TypedAction) -> list[str]:
        parent = _last_event(world, "coalition-hub")
        return [parent] if parent else []

    def effect_preview(self, world: World, action: TypedAction) -> list[str]:
        return ["restore validation, staffing, reserve, and safeguard prerequisites"]

    def apply(self, world: World, action: TypedAction, event_id: str) -> None:
        assert isinstance(action, DeliverPackageAction)
        package_entity = world.entities[action.package_id]
        package = package_entity.component("package")
        validation = world.entities[action.validation_id].component("resource")
        staffing = world.entities[action.staffing_id].component("resource")
        reserve = world.entities[action.reserve_id].component("resource")
        safeguard = world.entities[action.safeguard_id].component("constraint")
        assert package is not None and validation is not None and staffing is not None and reserve is not None and safeguard is not None
        package.status = "delivered"
        validation.current = max(validation.current, validation.required + 1)
        staffing.current = max(staffing.current, staffing.required)
        reserve.current = max(reserve.current, reserve.required + 10)
        safeguard.status = safeguard.required_status
        for entity_id in (
            action.package_id,
            action.validation_id,
            action.staffing_id,
            action.reserve_id,
            action.safeguard_id,
        ):
            world.entities[entity_id].last_cause_event_id = event_id


class _ScheduledBriefingProcess:
    version = "1"
    read_paths: tuple[str, ...]
    write_paths: tuple[str, ...]
    order: int
    trigger_tick: int
    target_entity_id: str
    info_id: str
    delivery_id: str

    def due(self, world: World) -> bool:
        info = world.entities[self.info_id].component("information")
        return bool(world.tick == self.trigger_tick and info is not None and not info.active)

    def apply(self, world: World) -> None:
        raise AssertionError("event-aware process hook should be used")

    def apply_with_event_id(self, world: World, event_id: str) -> None:
        self._change_target(world)
        info_entity = world.entities[self.info_id]
        delivery_entity = world.entities[self.delivery_id]
        info = info_entity.component("information")
        delivery = delivery_entity.component("delivery")
        assert info is not None and delivery is not None
        info.active = True
        delivery.status = "delivered"
        delivery.delivered_tick = world.tick
        for entity_id in (self.target_entity_id, self.info_id, self.delivery_id):
            world.entities[entity_id].last_cause_event_id = event_id

    def _change_target(self, world: World) -> None:
        raise NotImplementedError


class ValidationFailureProcess(_ScheduledBriefingProcess):
    rule_id = "waltzman.process.validation-failure"
    order = 10
    trigger_tick = 1
    target_entity_id = "validation-capacity"
    info_id = "brief-validation"
    delivery_id = "delivery-validation-mara"
    read_paths = (
        "tick",
        "entities.validation-capacity.components.resource",
        "entities.brief-validation.components.information.active",
    )
    write_paths = (
        "entities.validation-capacity.components.resource.current",
        "entities.validation-capacity.last_cause_event_id",
        "entities.brief-validation.components.information.active",
        "entities.brief-validation.last_cause_event_id",
        "entities.delivery-validation-mara.components.delivery",
        "entities.delivery-validation-mara.last_cause_event_id",
    )

    def _change_target(self, world: World) -> None:
        world.entities[self.target_entity_id].component("resource").current = 2


class StaffingShortfallProcess(_ScheduledBriefingProcess):
    rule_id = "waltzman.process.staffing-shortfall"
    order = 20
    trigger_tick = 2
    target_entity_id = "clinical-staff"
    info_id = "brief-staff"
    delivery_id = "delivery-staff-tomas"
    read_paths = (
        "tick",
        "entities.clinical-staff.components.resource",
        "entities.brief-staff.components.information.active",
    )
    write_paths = (
        "entities.clinical-staff.components.resource.current",
        "entities.clinical-staff.last_cause_event_id",
        "entities.brief-staff.components.information.active",
        "entities.brief-staff.last_cause_event_id",
        "entities.delivery-staff-tomas.components.delivery",
        "entities.delivery-staff-tomas.last_cause_event_id",
    )

    def _change_target(self, world: World) -> None:
        world.entities[self.target_entity_id].component("resource").current = 18


class ReserveConflictProcess(_ScheduledBriefingProcess):
    rule_id = "waltzman.process.reserve-conflict"
    order = 30
    trigger_tick = 3
    target_entity_id = "shared-reserve"
    info_id = "brief-reserve"
    delivery_id = "delivery-reserve-nira"
    read_paths = (
        "tick",
        "entities.shared-reserve.components.resource",
        "entities.brief-reserve.components.information.active",
    )
    write_paths = (
        "entities.shared-reserve.components.resource.current",
        "entities.shared-reserve.last_cause_event_id",
        "entities.brief-reserve.components.information.active",
        "entities.brief-reserve.last_cause_event_id",
        "entities.delivery-reserve-nira.components.delivery",
        "entities.delivery-reserve-nira.last_cause_event_id",
    )

    def _change_target(self, world: World) -> None:
        world.entities[self.target_entity_id].component("resource").current = 61


class SafeguardGapProcess(_ScheduledBriefingProcess):
    rule_id = "waltzman.process.safeguard-gap"
    order = 40
    trigger_tick = 4
    target_entity_id = "safeguard-record"
    info_id = "brief-safeguard"
    delivery_id = "delivery-safeguard-idris"
    read_paths = (
        "tick",
        "entities.safeguard-record.components.constraint",
        "entities.brief-safeguard.components.information.active",
    )
    write_paths = (
        "entities.safeguard-record.components.constraint.status",
        "entities.safeguard-record.last_cause_event_id",
        "entities.brief-safeguard.components.information.active",
        "entities.brief-safeguard.last_cause_event_id",
        "entities.delivery-safeguard-idris.components.delivery",
        "entities.delivery-safeguard-idris.last_cause_event_id",
    )

    def _change_target(self, world: World) -> None:
        world.entities[self.target_entity_id].component("constraint").status = "pending"


class MeetingCompletionProcess:
    rule_id = "waltzman.process.meeting-completion"
    version = "1"
    order = 50
    read_paths = ("tick", "entities.coordination-meeting.components.activity")
    write_paths = (
        "entities.coordination-meeting.components.activity.status",
        "entities.coordination-meeting.last_cause_event_id",
    )

    def due(self, world: World) -> bool:
        activity = world.entities["coordination-meeting"].component("activity")
        return bool(
            activity
            and activity.status == "active"
            and activity.end_tick is not None
            and world.tick >= activity.end_tick
        )

    def causal_parents(self, world: World) -> list[str]:
        parent = _last_event(world, "coordination-meeting")
        return [parent] if parent else []

    def apply(self, world: World) -> None:
        raise AssertionError("event-aware process hook should be used")

    def apply_with_event_id(self, world: World, event_id: str) -> None:
        entity = world.entities["coordination-meeting"]
        activity = entity.component("activity")
        assert activity is not None
        activity.status = "completed"
        entity.last_cause_event_id = event_id


class CoalitionDecisionProcess:
    rule_id = "waltzman.institution.coalition-gate"
    version = "1"
    order = 60
    read_paths = (
        "tick",
        "entities.<resident>.components.commitment.stance",
        "entities.coordination-meeting.components.activity.status",
        "entities.coalition-hub.components.institution",
    )
    write_paths = (
        "entities.coalition-hub.components.institution.status",
        "entities.coalition-hub.components.institution.support_count",
        "entities.coalition-hub.components.institution.conditional_count",
        "entities.coalition-hub.components.institution.last_evaluated_tick",
        "entities.coalition-hub.last_cause_event_id",
    )

    def due(self, world: World) -> bool:
        activity = world.entities["coordination-meeting"].component("activity")
        institution = world.entities["coalition-hub"].component("institution")
        return bool(
            activity
            and activity.status == "completed"
            and institution
            and institution.last_evaluated_tick < world.tick
        )

    def causal_parents(self, world: World) -> list[str]:
        parents = []
        meeting_parent = _last_event(world, "coordination-meeting")
        if meeting_parent:
            parents.append(meeting_parent)
        for entity in world.entities.values():
            if entity.component("commitment") is not None and entity.last_cause_event_id:
                parents.append(entity.last_cause_event_id)
        return parents

    def apply(self, world: World) -> None:
        raise AssertionError("event-aware process hook should be used")

    def apply_with_event_id(self, world: World, event_id: str) -> None:
        institution_entity = world.entities["coalition-hub"]
        institution = institution_entity.component("institution")
        assert institution is not None
        stances = [
            entity.component("commitment").stance
            for entity in world.entities.values()
            if entity.component("commitment") is not None
        ]
        support = sum(stance == "support" for stance in stances)
        conditional = sum(stance == "conditional" for stance in stances)
        institution.support_count = support
        institution.conditional_count = conditional
        institution.status = (
            "ready"
            if support >= institution.required_support and conditional == 0
            else "blocked"
        )
        institution.last_evaluated_tick = world.tick
        institution_entity.last_cause_event_id = event_id
