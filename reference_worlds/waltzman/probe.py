"""Build and execute the integrated Waltzman Coordination Lab demo."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Importing these modules registers the typed open components before snapshots
# are constructed or replayed.
from world_substrate.information import DeliveryState, InformationState
from world_substrate.engine import Engine
from world_substrate.mechanisms.time import ClockAdvanceProcess
from world_substrate.model import Entity, LocationState, World
from world_substrate.policy import apply_choice, resolve_choice
from world_substrate.rules import RuleRegistry

from .components import (
    ActivityState,
    CommitmentState,
    ConstraintState,
    InstitutionState,
    PackageState,
    ResidentState,
    ResourceState,
)
from .mechanics import (
    CoalitionDecisionProcess,
    CommunicateRule,
    DeliverPackageRule,
    MeetingCompletionProcess,
    ReassessCommitmentRule,
    ReserveConflictProcess,
    SafeguardGapProcess,
    StaffingShortfallProcess,
    StartMeetingRule,
    ValidationFailureProcess,
)

CONTENT = "reference_worlds/waltzman/coordination-lab-v0.json"
SCENE = "reference_worlds/waltzman/scene-v0.json"

_TYPES: dict[str, type[Any]] = {
    "resident": ResidentState,
    "resource": ResourceState,
    "constraint": ConstraintState,
    "commitment": CommitmentState,
    "institution": InstitutionState,
    "activity": ActivityState,
    "package": PackageState,
    "information": InformationState,
    "delivery": DeliveryState,
}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_content(root: Path | None = None) -> dict[str, Any]:
    root = root or repository_root()
    return json.loads((root / CONTENT).read_text())


def load_scene(root: Path | None = None) -> dict[str, Any]:
    root = root or repository_root()
    return json.loads((root / SCENE).read_text())


def build_registry() -> RuleRegistry:
    registry = RuleRegistry()
    registry.register_action(CommunicateRule())
    registry.register_action(ReassessCommitmentRule())
    registry.register_action(StartMeetingRule())
    registry.register_action(DeliverPackageRule())
    registry.register_process(ClockAdvanceProcess())
    registry.register_process(ValidationFailureProcess())
    registry.register_process(StaffingShortfallProcess())
    registry.register_process(ReserveConflictProcess())
    registry.register_process(SafeguardGapProcess())
    registry.register_process(MeetingCompletionProcess())
    registry.register_process(CoalitionDecisionProcess())
    return registry


def build_engine(root: Path | None = None) -> Engine:
    content = load_content(root)
    entities: dict[str, Entity] = {}
    for row in content["entities"]:
        components = {
            name: _TYPES[name](**fields)
            for name, fields in (row.get("components") or {}).items()
        }
        entity = Entity(
            entity_id=row["entity_id"],
            label=row["label"],
            category_ids=tuple(row["category_ids"]),
            location=LocationState(**row["location"]) if row.get("location") else None,
            source_pack_id=content["content_id"],
            source_entity_id=row["entity_id"],
            components=components,
        )
        entities[entity.entity_id] = entity
    registry = build_registry()
    world = World(
        world_id=content["world_id"],
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id=content["content_id"],
        rule_versions=registry.versions(),
    )
    return Engine(world, registry)


def _choose(engine: Engine, actor_id: str, kind: str, **participants: str) -> dict[str, Any]:
    """Select one Engine-minted affordance through the ordinary policy seam."""

    page = engine.discover(actor_id, kind=kind)
    matches = []
    for row in page["available"]:
        action = row["action"]
        if all(action.get(key) == value for key, value in participants.items()):
            matches.append(row)
    if len(matches) != 1:
        raise AssertionError(
            f"expected one {kind} affordance for {actor_id} {participants}, got {len(matches)}"
        )
    row = matches[0]
    choice = resolve_choice(page, row["action_id"], f"scripted Waltzman demo: choose {kind}")
    outcome = apply_choice(engine, choice, "waltzman-scripted")
    if outcome is None or outcome["status"] != "accepted":
        raise AssertionError(f"{kind} did not commit: {outcome}")
    return outcome["event"]


def _tick(engine: Engine, steps: int = 1) -> list[dict[str, Any]]:
    outcome = engine.advance(steps)
    return [event for event in outcome["events"] if event]


def run_baseline(root: Path | None = None) -> Engine:
    """Run the shared-information scenario to the blocked coalition gate."""

    engine = build_engine(root)

    _tick(engine)  # t1: validation failure -> private briefing to Mara
    _choose(engine, "mara", "reassess_commitment")
    _choose(
        engine,
        "mara",
        "communicate",
        information="msg-mara-validation",
        delivery="delivery-mara-ari",
    )

    _tick(engine)  # t2: staffing shortfall -> private briefing to Tomas
    _choose(engine, "tomas", "reassess_commitment")
    _choose(
        engine,
        "tomas",
        "communicate",
        information="msg-tomas-staff",
        delivery="delivery-tomas-selene",
    )

    _tick(engine)  # t3: reserve conflict -> private briefing to Nira
    _choose(engine, "nira", "reassess_commitment")
    _choose(
        engine,
        "nira",
        "communicate",
        information="msg-nira-reserve",
        delivery="delivery-nira-selene",
    )

    _tick(engine)  # t4: safeguard gap -> private briefing to Idris
    _choose(engine, "idris", "reassess_commitment")
    _choose(
        engine,
        "idris",
        "communicate",
        information="msg-idris-safeguard",
        delivery="delivery-idris-selene",
    )

    _choose(engine, "selene", "start_meeting", activity="coordination-meeting")
    _tick(engine, 2)  # t5-t6: duration completes; institution evaluates and blocks

    institution = engine.world.entities["coalition-hub"].component("institution")
    meeting = engine.world.entities["coordination-meeting"].component("activity")
    if institution is None or institution.status != "blocked":
        raise AssertionError("baseline coalition should be blocked")
    if meeting is None or meeting.status != "completed":
        raise AssertionError("coordination meeting should complete before decision")
    return engine


def run_intervention(baseline: Engine | None = None) -> Engine:
    """Fork the blocked run and apply the represented stabilization package."""

    baseline = baseline or run_baseline()
    engine = Engine.replay_commands(
        initial_snapshot=baseline.initial_snapshot(),
        commands=baseline.world.commands,
        registry=build_registry(),
    )
    if engine.world.events != baseline.world.events:
        raise AssertionError("intervention fork did not preserve the baseline history exactly")

    _choose(
        engine,
        "selene",
        "deliver_package",
        package="stabilization-package",
        validation="validation-capacity",
        staffing="clinical-staff",
        reserve="shared-reserve",
        safeguard="safeguard-record",
    )
    for actor_id in ("mara", "tomas", "nira", "idris"):
        _choose(engine, actor_id, "reassess_commitment")
    _tick(engine)  # t7: gate recomputes from represented commitments

    institution = engine.world.entities["coalition-hub"].component("institution")
    if institution is None or institution.status != "ready":
        raise AssertionError("intervention branch should restore coalition readiness")
    return engine


def event_annotations(engine: Engine) -> dict[str, dict[str, Any]]:
    """Downstream display labels keyed by canonical event id."""

    commands = {command["command_id"]: command for command in engine.world.commands}
    labels = {
        "system.clock.advance": "Canonical clock advances",
        "waltzman.process.validation-failure": "Alba validation capacity drops",
        "waltzman.process.staffing-shortfall": "Borin staffing shortfall arrives",
        "waltzman.process.reserve-conflict": "Shared reserve conflict appears",
        "waltzman.process.safeguard-gap": "Safeguard prerequisite becomes pending",
        "waltzman.activity.start-meeting": "Coordination meeting starts",
        "waltzman.process.meeting-completion": "Coordination meeting completes",
        "waltzman.institution.coalition-gate": "Coalition gate recomputes",
        "waltzman.intervention.deliver-package": "Stabilization package delivered",
        "waltzman.commitment.reassess": "Resident commitment reassessed",
        "waltzman.information.communicate": "Represented information delivered",
    }
    rows: dict[str, dict[str, Any]] = {}
    for event in engine.world.events:
        command = commands.get(event["cause"], {})
        action = command.get("action") if isinstance(command, dict) else None
        title = labels.get(event["rule_id"], event["rule_id"])
        detail = ""
        if isinstance(action, dict):
            if action.get("kind") == "communicate":
                info_id = action.get("information")
                info_entity = engine.world.entities.get(str(info_id))
                info = info_entity.component("information") if info_entity else None
                if info is not None:
                    detail = info.content
            elif action.get("kind") == "reassess_commitment":
                actor_id = action.get("actor")
                actor = engine.world.entities.get(str(actor_id))
                commitment = actor.component("commitment") if actor else None
                if actor is not None and commitment is not None:
                    detail = f"{actor.label}: {commitment.stance}"
            elif action.get("kind") == "start_meeting":
                detail = "Two-tick represented activity; completion rechecks current world time."
            elif action.get("kind") == "deliver_package":
                detail = "Restores represented validation, staffing, reserve, and safeguard prerequisites."
        if not detail:
            detail = title
        rows[event["event_id"]] = {
            "title": title,
            "detail": detail,
            "kind": (
                "information"
                if "information" in event["rule_id"] or "brief" in title.lower()
                else "institution"
                if "institution" in event["rule_id"]
                else "intervention"
                if "intervention" in event["rule_id"]
                else "world"
            ),
        }
    return rows


def blocked_event_id(engine: Engine) -> str:
    matches = [
        event["event_id"]
        for event in engine.world.events
        if event["rule_id"] == "waltzman.institution.coalition-gate"
    ]
    if not matches:
        raise AssertionError("no coalition gate event")
    return matches[-1]
