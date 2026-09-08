"""Execute a CVS sustainment scenario under explicit World Substrate mechanics.

The CVS engine selects/justifies structural interventions. This module does not
repeat that optimization. It receives one scenario, an explicit capability set,
and at most one externally selected transfer, then executes the consequences
through the ordinary World Substrate transition authority.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from world_substrate.engine import Engine
from world_substrate.model import Entity, World, register_component
from world_substrate.rules import Check, RuleRegistry

REPO = Path(__file__).resolve().parents[2]
IMPORTER_PATH = REPO / "scripts/import_cvs_situation.py"


def _load_importer():
    spec = importlib.util.spec_from_file_location("cvs_situation_import_for_simulation", IMPORTER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


importer = _load_importer()


@dataclass
class ExternalIdentityState:
    system: str
    identifier: str


@dataclass
class EvidenceRefsState:
    source_ids: list[str]


@dataclass
class ScenarioContextState:
    scenario_id: str
    scenario_name: str
    regime: str
    is_decider: bool


@dataclass
class InventoryState:
    available: int
    demand: int
    unit: str
    protected_reserve: int


@dataclass
class CapabilityState:
    capability_kind: str
    enabled: bool
    cost: float
    target_ref: str | None
    overrides_ref: str | None
    amount: int


@dataclass
class ActionTemplateState:
    action_kind: str
    source_ref: str
    target_ref: str
    max_amount: int
    required_capability_ids: list[str]


@dataclass
class RuleState:
    rule_kind: str
    quantity: int
    waived_in_regimes: list[str]
    applies_to_ids: list[str]


_COMPONENT_TYPES = {
    "external_identity": ExternalIdentityState,
    "evidence_refs": EvidenceRefsState,
    "scenario_context": ScenarioContextState,
    "inventory": InventoryState,
    "capability": CapabilityState,
    "action_template": ActionTemplateState,
    "rule_state": RuleState,
}
for _name, _type in _COMPONENT_TYPES.items():
    register_component(_name, _type)


@dataclass(frozen=True)
class TransferAction:
    actor_id: str
    source_ref: str
    target_ref: str
    amount: int
    base_revision: int
    controller_id: str
    kind: str = "transfer"

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "source_ref": self.source_ref,
            "target_ref": self.target_ref,
            "amount": self.amount,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TransferAction":
        if value.get("kind") != "transfer":
            raise ValueError("record is not a transfer action")
        actor = value.get("actor")
        source = value.get("source_ref")
        target = value.get("target_ref")
        amount = value.get("amount")
        revision = value.get("base_revision")
        controller = value.get("controller")
        if not all(isinstance(item, str) and item for item in (actor, source, target, controller)):
            raise ValueError("actor/source_ref/target_ref/controller must be nonempty strings")
        if type(amount) is not int or type(revision) is not int:
            raise ValueError("amount/base_revision must be integers")
        return cls(actor, source, target, amount, revision, controller)


def _external_map(world: World) -> dict[str, Entity]:
    result: dict[str, Entity] = {}
    for entity in world.entities.values():
        identity = entity.component("external_identity")
        if identity is not None:
            result[identity.identifier] = entity
    return result


def _enabled_capability(world: World, source_capability_id: str) -> bool:
    entity = _external_map(world).get(source_capability_id)
    if entity is None:
        return False
    capability = entity.component("capability")
    return bool(capability and capability.enabled)


class SustainmentTransferRule:
    """Reviewed mechanic profile for the bounded two-depot transfer seam."""

    rule_id = "cvs-sustainment.transfer"
    version = "1"
    action_kind = "transfer"
    read_paths = (
        "entities.<source_ref>.components.inventory",
        "entities.<target_ref>.components.inventory",
        "entities.<actor>.components.scenario_context",
    )
    write_paths = (
        "entities.<source_ref>.components.inventory.available",
        "entities.<target_ref>.components.inventory.available",
    )

    def discover(self, world: World, actor_id: str) -> list[TransferAction]:
        # Policy/action selection is intentionally outside this simulation profile.
        # CVS or an analyst supplies the concrete action being evaluated.
        return []

    def action_from_dict(self, value: dict[str, Any]) -> TransferAction:
        return TransferAction.from_dict(value)

    def _matching_template(self, world: World, action: TransferAction) -> ActionTemplateState | None:
        for entity in world.entities.values():
            template = entity.component("action_template")
            if (
                template is not None
                and template.action_kind == action.kind
                and template.source_ref == action.source_ref
                and template.target_ref == action.target_ref
            ):
                return template
        return None

    def checks(self, world: World, action: TransferAction) -> list[Check]:
        actor = world.entities.get(action.actor_id)
        source = world.entities.get(action.source_ref)
        target = world.entities.get(action.target_ref)
        context = actor.component("scenario_context") if actor else None
        source_inventory = source.component("inventory") if source else None
        target_inventory = target.component("inventory") if target else None
        template = self._matching_template(world, action)
        required = template.required_capability_ids if template else []
        missing = [cap for cap in required if not _enabled_capability(world, cap)]
        return [
            Check("Actor is the represented scenario decider", bool(context and context.is_decider)),
            Check("Source is a represented inventory pool", source_inventory is not None),
            Check("Target is a represented inventory pool", target_inventory is not None),
            Check("Transfer direction is declared by the imported action template", template is not None),
            Check(
                "Transfer amount is positive and within the imported template limit",
                bool(template and 0 < action.amount <= template.max_amount),
                action.amount,
                template.max_amount if template else None,
            ),
            Check("Required structural capabilities are enabled", not missing, missing, []),
            Check(
                "Source has enough represented stock for the transfer",
                bool(source_inventory and source_inventory.available >= action.amount),
                source_inventory.available if source_inventory else None,
                action.amount,
            ),
        ]

    def effect_preview(self, world: World, action: TransferAction) -> list[str]:
        return [
            f"decrease {action.source_ref} inventory by {action.amount}",
            f"increase {action.target_ref} inventory by {action.amount}",
        ]

    def apply(self, world: World, action: TransferAction, event_id: str) -> None:
        source = world.entities[action.source_ref].component("inventory")
        target = world.entities[action.target_ref].component("inventory")
        assert source is not None and target is not None
        source.available -= action.amount
        target.available += action.amount


def _build_world(bundle: dict[str, Any]) -> World:
    entities: dict[str, Entity] = {}
    for row in bundle["entities"]:
        components = {
            name: _COMPONENT_TYPES[name](**fields)
            for name, fields in row.get("components", {}).items()
        }
        identity = components.get("external_identity")
        entities[row["id"]] = Entity(
            entity_id=row["id"],
            label=row["label"],
            category_ids=tuple(row["categories"]),
            source_pack_id="cvs-situation-import/v0",
            source_entity_id=identity.identifier if identity else row["id"],
            components=components,
        )
    registry = RuleRegistry()
    registry.register_action(SustainmentTransferRule())
    world = World(
        world_id=bundle["world"]["id"],
        revision=0,
        tick=0,
        entities=entities,
        engine_id="world-substrate-core@1",
        content_id="{}@{}".format(bundle["world"]["id"], bundle["world"].get("content_version", 1)),
        rule_versions=registry.versions(),
    )
    world.validate()
    return world


def _inventory_view(world: World) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for source_id, entity in _external_map(world).items():
        inventory = entity.component("inventory")
        if inventory is not None:
            result[source_id] = {
                "local_entity_id": entity.entity_id,
                "available": inventory.available,
                "demand": inventory.demand,
                "unit": inventory.unit,
                "protected_reserve": inventory.protected_reserve,
            }
    return result


def _scenario_context(world: World) -> ScenarioContextState:
    for entity in world.entities.values():
        context = entity.component("scenario_context")
        if context is not None and context.is_decider:
            return context
    raise ValueError("world has no scenario decider context")


def evaluate_outcome(world: World) -> dict[str, Any]:
    context = _scenario_context(world)
    external = _external_map(world)
    override_targets = {
        cap.overrides_ref
        for entity in world.entities.values()
        if (cap := entity.component("capability")) is not None
        and cap.enabled
        and cap.capability_kind == "rule_override"
        and cap.overrides_ref is not None
    }
    enabled_capacity = [
        identity.identifier
        for entity in world.entities.values()
        if (cap := entity.component("capability")) is not None
        and cap.enabled
        and cap.capability_kind == "capacity"
        and (identity := entity.component("external_identity")) is not None
    ]
    if enabled_capacity:
        raise ValueError(
            "cvs-sustainment-simulation/v0 does not yet implement enabled capacity capability effects: "
            + ", ".join(sorted(enabled_capacity))
        )

    shortfalls: dict[str, int] = {}
    usable_by_pool: dict[str, int] = {}
    withheld_by_pool: dict[str, int] = {}
    for source_id, entity in external.items():
        inventory = entity.component("inventory")
        if inventory is None:
            continue
        withheld = 0
        for rule_entity in world.entities.values():
            rule = rule_entity.component("rule_state")
            rule_identity = rule_entity.component("external_identity")
            if rule is None or rule_identity is None or source_id not in rule.applies_to_ids:
                continue
            if context.regime in rule.waived_in_regimes:
                continue
            if rule_entity.entity_id in override_targets:
                continue
            withheld += rule.quantity
        usable = max(0, inventory.available - withheld)
        usable_by_pool[source_id] = usable
        withheld_by_pool[source_id] = withheld
        if usable < inventory.demand:
            shortfalls[source_id] = inventory.demand - usable
    return {
        "viable": not shortfalls,
        "shortfalls": shortfalls,
        "total_shortfall": sum(shortfalls.values()),
        "usable_by_pool": usable_by_pool,
        "withheld_by_pool": withheld_by_pool,
        "regime": context.regime,
    }


def run_scenario(
    situation: object,
    *,
    scenario_id: str,
    enabled_capabilities: Iterable[str] = (),
    action: dict[str, Any] | None = None,
    source_ref: str = "CVS Situation IR",
) -> dict[str, Any]:
    enabled = tuple(sorted(set(enabled_capabilities)))
    bundle = importer.convert_situation(
        situation,
        scenario_id=scenario_id,
        enabled_capabilities=enabled,
        source_ref=source_ref,
    )
    world = _build_world(bundle)
    engine = Engine(world, _registry())
    initial = _inventory_view(engine.world)
    action_result = None
    if action is not None:
        external = _external_map(engine.world)
        decider = next(
            entity for entity in engine.world.entities.values()
            if (ctx := entity.component("scenario_context")) is not None and ctx.is_decider
        )
        source_source_id = action.get("source")
        target_source_id = action.get("target")
        if source_source_id not in external or target_source_id not in external:
            raise ValueError("action source/target must name imported CVS source IDs")
        amount = action.get("amount")
        if type(amount) is not int:
            raise ValueError("action amount must be an integer")
        transfer = TransferAction(
            actor_id=decider.entity_id,
            source_ref=external[source_source_id].entity_id,
            target_ref=external[target_source_id].entity_id,
            amount=amount,
            base_revision=engine.world.revision,
            controller_id="cvs-sustainment-simulation/v0",
        )
        action_result = engine.apply(transfer)
    outcome = evaluate_outcome(engine.world)
    return {
        "schema_version": "world-substrate-cvs-sustainment-simulation/v0",
        "scenario_id": scenario_id,
        "enabled_capabilities": list(enabled),
        "input_action": action,
        "action_result": action_result,
        "initial_inventory": initial,
        "final_inventory": _inventory_view(engine.world),
        "outcome": outcome,
        "causal_trace": list(engine.world.events),
        "model_boundary": {
            "structural_input": "cvs-situation-import/v0",
            "mechanic_profile": "cvs-sustainment.transfer@1",
            "action_selection": "external; not optimized by World Substrate",
            "observation_model": "not implemented in this execution-only profile",
            "capacity_capability_effects": "explicitly unsupported in v0",
            "truth_status": "scenario/model result; not real-world truth",
        },
    }


def _registry() -> RuleRegistry:
    registry = RuleRegistry()
    registry.register_action(SustainmentTransferRule())
    return registry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("situation", type=Path)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--enable-capability", action="append", default=[])
    parser.add_argument("--source")
    parser.add_argument("--target")
    parser.add_argument("--amount", type=int)
    parser.add_argument("--source-ref", default="CVS Situation IR")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if any(item is not None for item in (args.source, args.target, args.amount)) and not all(
        item is not None for item in (args.source, args.target, args.amount)
    ):
        parser.error("--source, --target, and --amount must be supplied together")
    action = None
    if args.source is not None:
        action = {"source": args.source, "target": args.target, "amount": args.amount}
    result = run_scenario(
        json.loads(args.situation.read_text()),
        scenario_id=args.scenario,
        enabled_capabilities=args.enable_capability,
        action=action,
        source_ref=args.source_ref,
    )
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
