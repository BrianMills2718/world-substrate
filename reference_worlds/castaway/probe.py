"""Authentic first-fill probe against the pinned Castaway checkpoint."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar

from world_substrate.engine import Engine
from world_substrate.mechanisms import (
    ClockAdvanceProcess,
    FillRule,
    HydrationDecayProcess,
)
from world_substrate.model import (
    ActorState,
    ConditionState,
    ContainerState,
    Entity,
    LiquidState,
    LocationState,
    OwnershipState,
    ThermalState,
    World,
)
from world_substrate.rules import FillAction, RuleRegistry

T = TypeVar("T")


def _component(component_type: type[T], value: dict[str, Any] | None) -> T | None:
    if value is None:
        return None
    return component_type(**value)  # type: ignore[call-arg]


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_first_fill_engine(root: Path | None = None) -> Engine:
    root = root or repository_root()
    content = json.loads(
        (root / "reference_worlds/castaway/freshwater-fill-v0.json").read_text()
    )
    entities: dict[str, Entity] = {}
    for row in content["entities"]:
        entity = Entity(
            entity_id=row["entity_id"],
            label=row["label"],
            category_ids=tuple(row["category_ids"]),
            actor=_component(ActorState, row.get("actor")),
            location=_component(LocationState, row.get("location")),
            ownership=_component(OwnershipState, row.get("ownership")),
            condition=_component(ConditionState, row.get("condition")),
            container=_component(ContainerState, row.get("container")),
            liquid=_component(LiquidState, row.get("liquid")),
            thermal=_component(ThermalState, row.get("thermal")),
            source_pack_id=content["content_id"],
            source_entity_id=row["entity_id"],
        )
        entities[entity.entity_id] = entity

    registry = RuleRegistry()
    registry.register_action(FillRule())
    registry.register_process(ClockAdvanceProcess())
    registry.register_process(HydrationDecayProcess())
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


def _liquid_totals(engine: Engine) -> dict[str, int]:
    totals = {"volume_ml": 0, "salt_mg": 0, "pathogens": 0, "heat_units": 0}
    for entity in engine.world.entities.values():
        if entity.liquid is not None:
            for key in totals:
                totals[key] += getattr(entity.liquid, key)
    return totals


def _checkpoint_projection(engine: Engine) -> dict[str, Any]:
    actors = {}
    for actor_id in ("friday", "robinson"):
        entity = engine.world.entities[actor_id]
        assert entity.actor is not None and entity.location is not None
        actors[actor_id] = {
            "health": entity.actor.health,
            "location": entity.location.location_id,
            "thirst": entity.actor.hydration,
        }
    vessels = {}
    for vessel_id in ("clay-pot", "cup-robinson"):
        entity = engine.world.entities[vessel_id]
        assert entity.container and entity.condition and entity.liquid
        assert entity.ownership and entity.thermal
        vessels[vessel_id] = {
            "boiling_ticks": entity.container.boiling_ticks,
            "capacity_ml": entity.container.capacity_ml,
            "condition": entity.condition.value,
            "definition": entity.container.definition_id,
            "empty_weight": entity.container.empty_weight,
            "id": entity.entity_id,
            "label": entity.label,
            "last_cause": entity.last_cause_event_id,
            "liquid": entity.liquid.as_dict(),
            "on_fire": entity.container.heat_source_id,
            "owner": entity.ownership.owner_ref,
            "temperature_c": entity.thermal.temperature_c,
        }
    return {"tick": engine.world.tick, "actors": actors, "vessels": vessels}


def run_first_fill_probe(root: Path | None = None) -> dict[str, Any]:
    root = root or repository_root()
    fixture = json.loads(
        (root / "tests/fixtures/castaway/freshwater-v0.json").read_text()
    )
    expected_checkpoint = fixture["expected"]["checkpoints"][1]
    expected_projection = {
        "tick": expected_checkpoint["tick"],
        "actors": expected_checkpoint["actors"],
        "vessels": expected_checkpoint["vessels"],
    }

    engine = build_first_fill_engine(root)
    before_totals = _liquid_totals(engine)
    page = engine.discover("robinson", kind="fill")
    selected_row = next(
        row
        for row in page["available"]
        if row["action"]["vessel"] == "clay-pot"
        and row["action"]["source"] == "unsafe-pool"
        and row["action"]["volume_ml"] == 1000
    )
    selected = FillAction.from_dict(
        {**selected_row["action"], "controller": "verification_script"}
    )
    result = engine.apply(selected)
    after_fill_totals = _liquid_totals(engine)
    engine.advance()
    actual_projection = _checkpoint_projection(engine)
    replay = engine.replay()

    return {
        "schema_version": "world-substrate-evidence/first-fill-v0",
        "claim": "The neutral substrate discovered and executed one registered fill action, conserved modeled liquid quantities, matched the selected pinned donor checkpoint fields after one tick, and replayed exactly.",
        "limitations": [
            "This is a scripted first-fill slice, not the complete freshwater vertical.",
            "The reference data contains only the entities needed for this checkpoint comparison, not the donor's complete workshop world.",
            "The neutral state hash is not compared with the donor hash because the schemas differ.",
            "This does not establish LLM policy behavior or cross-domain generality.",
        ],
        "source": {
            "fixture_id": fixture["fixture_id"],
            "donor_revision": fixture["source"]["revision"],
            "donor_checkpoint_hash": expected_checkpoint["state_hash"],
        },
        "discovery": {
            "actor_id": "robinson",
            "available_fill_count": page["total"],
            "selected_action_id": selected_row["action_id"],
            "selected_action": selected.as_dict(),
        },
        "execution": {
            "status": result["status"],
            "events": engine.world.events,
            "final_material_hash": engine.world.material_hash(),
        },
        "conservation": {
            "before": before_totals,
            "after_fill": after_fill_totals,
            "matched": before_totals == after_fill_totals,
        },
        "checkpoint_comparison": {
            "matched": actual_projection == expected_projection,
            "expected": expected_projection,
            "actual": actual_projection,
        },
        "replay": replay,
        "accepted": bool(
            result["status"] == "accepted"
            and before_totals == after_fill_totals
            and actual_projection == expected_projection
            and replay["ok"]
        ),
    }
