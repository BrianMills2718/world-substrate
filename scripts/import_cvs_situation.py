#!/usr/bin/env python3
"""Project a bounded CVS Situation IR into a World Substrate authoring bundle.

This adapter imports represented structure only. It does not infer, install, or
approve causal mechanics, and it fails visibly on CVS constructs it does not yet
know how to preserve.
"""
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable

SOURCE_SYSTEM = "compositional-viable-systems"
TARGET_SCHEMA = "world-substrate-authoring-bundle/v0"
SUPPORTED_ENTITY_KINDS = {"role", "pool", "capability", "action"}
SUPPORTED_ACTION_KINDS = {"transfer"}
SUPPORTED_RULE_KINDS = {"protected_reserve"}


class SituationImportError(ValueError):
    pass


def _as_dict(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SituationImportError(f"{label} must be an object")
    return value


def _as_list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise SituationImportError(f"{label} must be a list")
    return value


def _source_id(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SituationImportError(f"{label} must be a nonempty string")
    return value


def _slug(source_id: str) -> str:
    """Create a World Substrate-local ID while retaining source ID separately."""
    slug = re.sub(r"[^a-z0-9]+", "-", source_id.lower()).strip("-")
    if not slug or not slug[0].isalpha():
        slug = f"entity-{slug}" if slug else "entity"
    return slug


def _unique_local_ids(source_ids: Iterable[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    used: dict[str, str] = {}
    for source_id in source_ids:
        local = _slug(source_id)
        if local in used and used[local] != source_id:
            raise SituationImportError(
                f"source IDs {used[local]!r} and {source_id!r} collide at local ID {local!r}"
            )
        used[local] = source_id
        result[source_id] = local
    return result


def _evidence_ids(row: dict[str, Any]) -> list[str]:
    evidence = row.get("evidence", [])
    if not isinstance(evidence, list) or any(not isinstance(item, str) for item in evidence):
        raise SituationImportError("evidence references must be a list of strings")
    return list(evidence)


def _component_specs() -> list[dict[str, Any]]:
    return [
        {
            "name": "external_identity",
            "fields": [
                {"name": "system", "type": "string", "default": SOURCE_SYSTEM},
                {"name": "identifier", "type": "string", "default": "unknown"},
            ],
        },
        {
            "name": "evidence_refs",
            "fields": [
                {"name": "source_ids", "type": "string_list", "default": []},
            ],
        },
        {
            "name": "scenario_context",
            "fields": [
                {"name": "scenario_id", "type": "string", "default": "unknown"},
                {"name": "scenario_name", "type": "string", "default": "unknown"},
                {"name": "regime", "type": "string", "default": "unknown"},
                {"name": "is_decider", "type": "boolean", "default": False},
            ],
        },
        {
            "name": "inventory",
            "fields": [
                {"name": "available", "type": "integer", "default": 0},
                {"name": "demand", "type": "integer", "default": 0},
                {"name": "unit", "type": "string", "default": "units"},
                {"name": "protected_reserve", "type": "integer", "default": 0},
            ],
        },
        {
            "name": "capability",
            "fields": [
                {"name": "capability_kind", "type": "string", "default": "unknown"},
                {"name": "enabled", "type": "boolean", "default": False},
                {"name": "cost", "type": "number", "default": 0.0},
                {"name": "target_ref", "type": "entity_ref_or_null", "default": None},
                {"name": "overrides_ref", "type": "entity_ref_or_null", "default": None},
                {"name": "amount", "type": "integer", "default": 0},
            ],
        },
        {
            "name": "action_template",
            "fields": [
                {"name": "action_kind", "type": "string", "default": "unknown"},
                {"name": "source_ref", "type": "entity_ref", "default": "unknown"},
                {"name": "target_ref", "type": "entity_ref", "default": "unknown"},
                {"name": "max_amount", "type": "integer", "default": 0},
                {"name": "required_capability_ids", "type": "string_list", "default": []},
            ],
        },
        {
            "name": "rule_state",
            "fields": [
                {"name": "rule_kind", "type": "string", "default": "unknown"},
                {"name": "quantity", "type": "integer", "default": 0},
                {"name": "waived_in_regimes", "type": "string_list", "default": []},
                {"name": "applies_to_ids", "type": "string_list", "default": []},
            ],
        },
    ]


def convert_situation(
    value: object,
    *,
    scenario_id: str,
    enabled_capabilities: Iterable[str] = (),
    source_ref: str = "CVS Situation IR",
) -> dict[str, Any]:
    situation = _as_dict(value, "situation")
    situation_id = _source_id(situation.get("id"), "situation.id")
    situation_name = _source_id(situation.get("name"), "situation.name")
    metadata = _as_dict(situation.get("metadata", {}), "metadata")
    decider_id = _source_id(metadata.get("decider"), "metadata.decider")
    question = _source_id(metadata.get("question"), "metadata.question")

    if situation.get("relations") not in (None, []):
        raise SituationImportError("relations are not represented by cvs-situation-import/v0")
    if situation.get("measures") not in (None, []):
        raise SituationImportError("measures are not represented by cvs-situation-import/v0")

    source_entities = _as_list(situation.get("entities"), "entities")
    source_rules = _as_list(situation.get("rules", []), "rules")
    scenarios = _as_list(situation.get("scenarios"), "scenarios")
    scenario = next((row for row in scenarios if isinstance(row, dict) and row.get("id") == scenario_id), None)
    if scenario is None:
        raise SituationImportError(f"unknown scenario: {scenario_id}")
    scenario = _as_dict(scenario, "scenario")
    scenario_name = _source_id(scenario.get("name"), "scenario.name")
    state = _as_dict(scenario.get("state"), "scenario.state")
    supply = _as_dict(state.get("supply"), "scenario.state.supply")
    demand = _as_dict(state.get("demand"), "scenario.state.demand")
    regime = _source_id(state.get("regime"), "scenario.state.regime")

    rows: dict[str, dict[str, Any]] = {}
    for raw in source_entities:
        row = _as_dict(raw, "entity")
        source_entity_id = _source_id(row.get("id"), "entity.id")
        kind = _source_id(row.get("kind"), f"entity {source_entity_id}.kind")
        if kind not in SUPPORTED_ENTITY_KINDS:
            raise SituationImportError(f"unsupported entity kind {kind!r} at {source_entity_id}")
        if source_entity_id in rows:
            raise SituationImportError(f"duplicate entity id: {source_entity_id}")
        rows[source_entity_id] = row

    for raw in source_rules:
        rule = _as_dict(raw, "rule")
        source_rule_id = _source_id(rule.get("id"), "rule.id")
        kind = _source_id(rule.get("kind"), f"rule {source_rule_id}.kind")
        if kind not in SUPPORTED_RULE_KINDS:
            raise SituationImportError(f"unsupported rule kind {kind!r} at {source_rule_id}")
        if source_rule_id in rows:
            raise SituationImportError(f"duplicate source id: {source_rule_id}")
        rows[source_rule_id] = {**rule, "_is_rule": True}

    if decider_id not in rows or rows[decider_id].get("kind") != "role":
        raise SituationImportError("metadata.decider must name a declared role")

    local_ids = _unique_local_ids(rows)
    enabled = set(enabled_capabilities)
    capability_ids = {sid for sid, row in rows.items() if row.get("kind") == "capability"}
    unknown_enabled = enabled - capability_ids
    if unknown_enabled:
        raise SituationImportError(f"enabled capabilities are not declared: {sorted(unknown_enabled)}")

    reserve_by_pool: dict[str, int] = {}
    for sid, row in rows.items():
        if not row.get("_is_rule"):
            continue
        params = _as_dict(row.get("parameters", {}), f"rule {sid}.parameters")
        quantity = params.get("quantity", 0)
        if type(quantity) is not int or quantity < 0:
            raise SituationImportError(f"rule {sid}.quantity must be a nonnegative integer")
        applies_to = _as_list(row.get("applies_to", []), f"rule {sid}.applies_to")
        for pool_id in applies_to:
            if pool_id not in rows or rows[pool_id].get("kind") != "pool":
                raise SituationImportError(f"rule {sid} applies to unknown/non-pool {pool_id!r}")
            reserve_by_pool[pool_id] = max(reserve_by_pool.get(pool_id, 0), quantity)

    entities: list[dict[str, Any]] = []
    action_kinds: dict[str, str] = {}
    for sid, row in rows.items():
        local_id = local_ids[sid]
        label = row.get("name") or sid
        if not isinstance(label, str) or not label.strip():
            raise SituationImportError(f"{sid}.name must be nonempty")
        components: dict[str, Any] = {
            "external_identity": {"system": SOURCE_SYSTEM, "identifier": sid},
            "evidence_refs": {"source_ids": _evidence_ids(row)},
        }
        categories: list[str]

        if row.get("_is_rule"):
            params = _as_dict(row.get("parameters", {}), f"rule {sid}.parameters")
            waived = params.get("waived_in_regimes", [])
            if not isinstance(waived, list) or any(not isinstance(x, str) for x in waived):
                raise SituationImportError(f"rule {sid}.waived_in_regimes must be string list")
            applies_to = _as_list(row.get("applies_to", []), f"rule {sid}.applies_to")
            components["rule_state"] = {
                "rule_kind": row["kind"],
                "quantity": params.get("quantity", 0),
                "waived_in_regimes": list(waived),
                "applies_to_ids": list(applies_to),
            }
            categories = ["rule"]
        else:
            kind = row["kind"]
            attrs = _as_dict(row.get("attributes", {}), f"entity {sid}.attributes")
            if kind == "role":
                components["scenario_context"] = {
                    "scenario_id": scenario_id,
                    "scenario_name": scenario_name,
                    "regime": regime,
                    "is_decider": sid == decider_id,
                }
                categories = ["actor", "decision-role"]
            elif kind == "pool":
                available = supply.get(sid)
                requested = demand.get(sid)
                if type(available) is not int or type(requested) is not int:
                    raise SituationImportError(f"scenario {scenario_id} must give integer supply/demand for {sid}")
                unit = attrs.get("unit", "units")
                if not isinstance(unit, str) or not unit:
                    raise SituationImportError(f"pool {sid}.unit must be nonempty")
                components["inventory"] = {
                    "available": available,
                    "demand": requested,
                    "unit": unit,
                    "protected_reserve": reserve_by_pool.get(sid, 0),
                }
                categories = ["resource-pool"]
            elif kind == "capability":
                target = attrs.get("target")
                overrides = attrs.get("overrides")
                if target is not None and target not in local_ids:
                    raise SituationImportError(f"capability {sid} targets unknown source id {target!r}")
                if overrides is not None and overrides not in local_ids:
                    raise SituationImportError(f"capability {sid} overrides unknown source id {overrides!r}")
                amount = attrs.get("amount", 0)
                if type(amount) is not int:
                    raise SituationImportError(f"capability {sid}.amount must be integer when present")
                cost = attrs.get("cost", 0.0)
                if type(cost) not in (int, float):
                    raise SituationImportError(f"capability {sid}.cost must be numeric")
                cap_kind = attrs.get("capability_kind")
                if not isinstance(cap_kind, str) or not cap_kind:
                    raise SituationImportError(f"capability {sid}.capability_kind must be nonempty")
                components["capability"] = {
                    "capability_kind": cap_kind,
                    "enabled": sid in enabled,
                    "cost": float(cost),
                    "target_ref": local_ids[target] if target is not None else None,
                    "overrides_ref": local_ids[overrides] if overrides is not None else None,
                    "amount": amount,
                }
                categories = ["capability"]
            elif kind == "action":
                action_kind = attrs.get("action_kind")
                if action_kind not in SUPPORTED_ACTION_KINDS:
                    raise SituationImportError(f"unsupported action kind {action_kind!r} at {sid}")
                source = attrs.get("source")
                target = attrs.get("target")
                if source not in local_ids or target not in local_ids:
                    raise SituationImportError(f"action {sid} source/target must name declared entities")
                max_amount = attrs.get("max_amount")
                if type(max_amount) is not int or max_amount < 0:
                    raise SituationImportError(f"action {sid}.max_amount must be nonnegative integer")
                required = attrs.get("requires", [])
                if not isinstance(required, list) or any(item not in capability_ids for item in required):
                    raise SituationImportError(f"action {sid}.requires must name declared capabilities")
                components["action_template"] = {
                    "action_kind": action_kind,
                    "source_ref": local_ids[source],
                    "target_ref": local_ids[target],
                    "max_amount": max_amount,
                    "required_capability_ids": list(required),
                }
                action_kinds.setdefault(action_kind, sid)
                categories = ["action-template"]
            else:  # guarded above
                raise AssertionError(kind)

        entities.append(
            {
                "id": local_id,
                "label": label,
                "categories": categories,
                "components": components,
            }
        )

    actions: list[dict[str, Any]] = []
    for action_kind in sorted(action_kinds):
        if action_kind == "transfer":
            actions.append(
                {
                    "kind": "transfer",
                    "description": "Transfer an integer amount between represented resource pools. Signature only; mechanics remain separately reviewed.",
                    "fields": [
                        {"name": "source_ref", "type": "entity_ref"},
                        {"name": "target_ref", "type": "entity_ref"},
                        {"name": "amount", "type": "integer"},
                    ],
                }
            )

    synthetic = any(
        isinstance(ev, dict) and ev.get("status") == "synthetic"
        for ev in _as_list(situation.get("evidence", []), "evidence")
    )
    summary = (
        f"Structural projection of {situation_name}, scenario {scenario_id}, from {source_ref}. "
        f"Question: {question} Causal mechanics are not implied or installed."
    )
    if synthetic:
        summary = "SYNTHETIC INTEGRATION FIXTURE. " + summary

    return {
        "schema_version": TARGET_SCHEMA,
        "world": {
            "id": _slug(f"cvs-{situation_id}-{scenario_id}"),
            "label": f"{situation_name} — {scenario_name}",
            "summary": summary,
            "location": "analysis-space",
            "content_version": 1,
        },
        "components": _component_specs(),
        "entities": entities,
        "actions": actions,
        "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("situation", type=Path)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--enable-capability", action="append", default=[])
    parser.add_argument("--source-ref", default="CVS Situation IR")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    value = json.loads(args.situation.read_text())
    bundle = convert_situation(
        value,
        scenario_id=args.scenario,
        enabled_capabilities=args.enable_capability,
        source_ref=args.source_ref,
    )
    text = json.dumps(bundle, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
