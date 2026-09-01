"""Authentic first-fill probe against the pinned Castaway checkpoint."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar

from world_substrate.engine import Engine
from world_substrate.mechanisms import (
    ClockAdvanceProcess,
    FillRule,
    FireFuelProcess,
    HeatRule,
    HydrationDecayProcess,
    ThermalProcess,
    UnheatRule,
)
from world_substrate.model import (
    ActorState,
    ConditionState,
    ContainerState,
    Entity,
    HeatSourceState,
    LiquidState,
    LocationState,
    MaterialState,
    OwnershipState,
    PhysicalLedger,
    ThermalState,
    World,
)
from world_substrate.rules import FillAction, HeatAction, RuleRegistry, UnheatAction

T = TypeVar("T")


def _component(component_type: type[T], value: dict[str, Any] | None) -> T | None:
    if value is None:
        return None
    return component_type(**value)  # type: ignore[call-arg]


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _entities(content: dict[str, Any]) -> dict[str, Entity]:
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
            material=_component(MaterialState, row.get("material")),
            heat_source=_component(HeatSourceState, row.get("heat_source")),
            source_pack_id=content["content_id"],
            source_entity_id=row["entity_id"],
        )
        entities[entity.entity_id] = entity
    return entities


def build_first_fill_engine(root: Path | None = None) -> Engine:
    root = root or repository_root()
    content = json.loads(
        (root / "reference_worlds/castaway/freshwater-fill-v0.json").read_text()
    )
    entities = _entities(content)

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


def build_freshwater_engine(root: Path | None = None) -> Engine:
    root = root or repository_root()
    content = json.loads(
        (root / "reference_worlds/castaway/freshwater-v0.json").read_text()
    )
    entities = _entities(content)
    registry = RuleRegistry()
    registry.register_action(FillRule())
    registry.register_action(HeatRule())
    registry.register_action(UnheatRule())
    registry.register_process(ClockAdvanceProcess())
    registry.register_process(HydrationDecayProcess())
    registry.register_process(ThermalProcess(**content["thermal_rules"]))
    registry.register_process(FireFuelProcess())
    initial = LiquidState()
    for entity in entities.values():
        if entity.liquid is not None:
            for key in initial.as_dict():
                setattr(initial, key, getattr(initial, key) + getattr(entity.liquid, key))
    world = World(
        world_id=content["world_id"],
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id=content["content_id"],
        rule_versions=registry.versions(),
        physical_ledger=PhysicalLedger(initial=initial),
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


def _without_donor_event_ids(projection: dict[str, Any]) -> dict[str, Any]:
    result = json.loads(json.dumps(projection))
    for vessel in result["vessels"].values():
        vessel.pop("last_cause", None)
    return result


def run_boiling_probe(root: Path | None = None) -> dict[str, Any]:
    root = root or repository_root()
    fixture = json.loads(
        (root / "tests/fixtures/castaway/freshwater-v0.json").read_text()
    )
    expected_checkpoint = fixture["expected"]["checkpoints"][2]
    expected_projection = _without_donor_event_ids(
        {
            "tick": expected_checkpoint["tick"],
            "actors": expected_checkpoint["actors"],
            "vessels": expected_checkpoint["vessels"],
        }
    )
    expected_ledger = {
        "evaporated": expected_checkpoint["totals"]["evaporated"],
        "pathogens_killed": expected_checkpoint["totals"]["pathogens_killed"],
        "heat_added": expected_checkpoint["totals"]["heat_added"],
        "heat_lost": expected_checkpoint["totals"]["heat_lost"],
        "latent_heat_used": expected_checkpoint["totals"]["latent_heat_used"],
        "drunk": expected_checkpoint["totals"]["drunk"],
    }

    engine = build_freshwater_engine(root)
    fill_page = engine.discover("robinson", kind="fill")
    fill_row = next(
        row
        for row in fill_page["available"]
        if row["action"]["vessel"] == "clay-pot"
        and row["action"]["source"] == "unsafe-pool"
        and row["action"]["volume_ml"] == 1000
    )
    fill = FillAction.from_dict(
        {**fill_row["action"], "controller": "verification_script"}
    )
    fill_result = engine.apply(fill)
    engine.advance()

    heat_page = engine.discover("robinson", kind="heat")
    heat_row = next(
        row
        for row in heat_page["available"]
        if row["action"]["vessel"] == "clay-pot"
        and row["action"]["target"] == "fire-camp"
    )
    heat = HeatAction.from_dict(
        {**heat_row["action"], "controller": "verification_script"}
    )
    heat_result = engine.apply(heat)
    engine.advance(5)

    actual_projection = _without_donor_event_ids(_checkpoint_projection(engine))
    assert engine.world.physical_ledger is not None
    actual_ledger = engine.world.physical_ledger.semantic_deltas()
    fire = engine.world.entities["fire-camp"]
    assert fire.heat_source is not None
    fuel_at_checkpoint = fire.heat_source.fuel

    unheat_page = engine.discover("robinson", kind="unheat")
    unheat_row = next(
        row
        for row in unheat_page["available"]
        if row["action"]["vessel"] == "clay-pot"
    )
    unheat = UnheatAction.from_dict(
        {**unheat_row["action"], "controller": "verification_script"}
    )
    unheat_result = engine.apply(unheat)
    replay = engine.replay()

    return {
        "schema_version": "world-substrate-evidence/boiling-v0",
        "claim": "The neutral substrate executed registered fill, heat, and unheat actions; applied deterministic fuel, heating, boiling, pathogen-removal, and evaporation processes; matched the pinned boiling checkpoint's semantic projection; and replayed exactly.",
        "limitations": [
            "This is the boiling prefix of M1, not the complete freshwater vertical.",
            "The comparison omits donor event IDs and raw state hashes because the neutral event and state schemas intentionally differ.",
            "The reference data contains only entities required by the M1 scenario.",
            "This does not establish cooling, pour, drink, ownership transfer, LLM policy behavior, or cross-domain generality.",
        ],
        "source": {
            "fixture_id": fixture["fixture_id"],
            "donor_revision": fixture["source"]["revision"],
            "donor_checkpoint_hash": expected_checkpoint["state_hash"],
        },
        "execution": {
            "fill_status": fill_result["status"],
            "heat_status": heat_result["status"],
            "unheat_status": unheat_result["status"],
            "fuel_at_checkpoint": fuel_at_checkpoint,
            "events": engine.world.events,
            "final_material_hash": engine.world.material_hash(),
        },
        "checkpoint_comparison": {
            "matched": actual_projection == expected_projection,
            "expected": expected_projection,
            "actual": actual_projection,
        },
        "ledger_comparison": {
            "matched": actual_ledger == expected_ledger,
            "expected": expected_ledger,
            "actual": actual_ledger,
        },
        "replay": replay,
        "accepted": bool(
            fill_result["status"] == "accepted"
            and heat_result["status"] == "accepted"
            and unheat_result["status"] == "accepted"
            and fuel_at_checkpoint == 18
            and actual_projection == expected_projection
            and actual_ledger == expected_ledger
            and replay["ok"]
        ),
    }
