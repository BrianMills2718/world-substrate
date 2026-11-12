"""Declared actor inputs, independent of privileged discovery and presentation.

Implements: information-delivery/complete-actor-input-boundary
Legacy bundles deliberately have no implicit declaration. Callers may retain a
historical adapter, but must not describe its inputs as authorized v1 inputs.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any

from world_substrate.information import entity_visible_to_actor


class ActorInformationError(ValueError):
    pass


def has_actor_boundary(bundle: dict[str, Any]) -> bool:
    return "actor_information" in bundle


def _object(value: Any, required: set[str], optional: set[str] = frozenset()) -> None:
    if not isinstance(value, dict) or not required <= value.keys() or value.keys() - required - optional:
        raise ActorInformationError("invalid actor_information declaration shape")


def _text(value: Any) -> None:
    if not isinstance(value, str):
        raise ActorInformationError("actor_information text must be a string")


def validate_actor_information(bundle: dict[str, Any]) -> None:
    """Reject malformed declarations without including privileged values in errors."""
    if not has_actor_boundary(bundle):
        return
    declaration = bundle["actor_information"]
    _object(declaration, {"version", "public_summary", "public_entities", "actors"}, {"public_actions"})
    if type(declaration["version"]) is not int or declaration["version"] != 1:
        raise ActorInformationError("unsupported actor_information version")
    _text(declaration["public_summary"])
    entities = {row["id"]: row for row in bundle["entities"]}
    components = {row["name"]: {f["name"]: f for f in row["fields"]} for row in bundle["components"]}

    def paths(entity: str, values: Any) -> None:
        if not isinstance(entity, str) or entity not in entities or not isinstance(values, list) or any(not isinstance(p, str) for p in values):
            raise ActorInformationError("invalid actor_information field references")
        if len(set(values)) != len(values):
            raise ActorInformationError("duplicate actor_information field references")
        for path in values:
            parts = path.split(".")
            if len(parts) != 2 or parts[0] not in entities[entity].get("components", {}) or parts[1] not in components.get(parts[0], {}):
                raise ActorInformationError("unknown actor_information field reference")

    public = declaration["public_entities"]
    if not isinstance(public, list):
        raise ActorInformationError("public_entities must be a list")
    known: set[str] = set()
    for row in public:
        _object(row, {"id", "label", "fields"})
        if not isinstance(row["id"], str) or row["id"] in known:
            raise ActorInformationError("invalid or duplicate public entity")
        paths(row["id"], row["fields"])
        _text(row["label"])
        known.add(row["id"])
    if not isinstance(declaration["actors"], dict):
        raise ActorInformationError("actors must be an object")
    for actor, profile in declaration["actors"].items():
        if actor not in known:
            raise ActorInformationError("actor must have a declared public identity")
        _object(profile, {"brief", "initial_knowledge", "observable_fields"})
        _text(profile["brief"])
        if not isinstance(profile["initial_knowledge"], list) or not isinstance(profile["observable_fields"], list):
            raise ActorInformationError("actor knowledge and observations must be lists")
        ids: set[str] = set()
        for item in profile["initial_knowledge"]:
            _object(item, {"id", "text", "source"})
            for value in item.values():
                _text(value)
            if not item["id"] or item["id"] in ids or not item["source"]:
                raise ActorInformationError("knowledge needs unique identity and source")
            ids.add(item["id"])
        seen: set[str] = set()
        for row in profile["observable_fields"]:
            _object(row, {"entity", "paths"})
            if not isinstance(row["entity"], str) or row["entity"] not in known or row["entity"] in seen:
                raise ActorInformationError("observation requires unique declared public identity")
            paths(row["entity"], row["paths"])
            seen.add(row["entity"])
    actions = {row["kind"]: row for row in bundle["actions"]}
    forms = declaration.get("public_actions", [])
    if not isinstance(forms, list):
        raise ActorInformationError("public_actions must be a list")
    for form in forms:
        _object(form, {"kind", "description", "fields"})
        _text(form["description"])
        if not isinstance(form["kind"], str) or form["kind"] not in actions or not isinstance(form["fields"], dict):
            raise ActorInformationError("invalid public action form")
        declared = {f["name"]: f["type"] for f in actions[form["kind"]]["fields"]}
        if form["fields"].keys() != declared.keys():
            raise ActorInformationError("public action form must bind its declared fields")
        for name, value in form["fields"].items():
            kind = declared[name]
            valid = ((kind in {"string", "entity_ref"} and isinstance(value, str)) or
                     (kind == "integer" and type(value) is int) or
                     (kind == "number" and type(value) in {int, float}) or
                     (kind == "boolean" and type(value) is bool))
            if not valid or (kind == "entity_ref" and value not in known):
                raise ActorInformationError("invalid public action field")


def _declaration(bundle: dict[str, Any], actor: str) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_actor_information(bundle)
    if not has_actor_boundary(bundle):
        raise ActorInformationError("legacy bundle has no declared actor-information boundary")
    declaration = bundle["actor_information"]
    if actor not in declaration["actors"]:
        raise ActorInformationError("actor has no declared information profile")
    return declaration, declaration["actors"][actor]


def actor_observation(engine: Any, bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    """Project only explicit authorized paths; never infer a field from its name."""
    declaration, profile = _declaration(bundle, actor)
    extra = {row["entity"]: row["paths"] for row in profile["observable_fields"]}
    entities = {}
    for row in declaration["public_entities"]:
        entity = engine.world.entities.get(row["id"])
        if entity is None or not entity_visible_to_actor(engine.world, actor, entity):
            continue
        projected = {"entity_id": row["id"], "label": row["label"], "components": {}}
        for path in sorted(set(row["fields"]) | set(extra.get(row["id"], []))):
            component, field = path.split(".")
            value = getattr(entity.component(component), field, None)
            projected["components"].setdefault(component, {})[field] = deepcopy(value)
        entities[row["id"]] = projected
    return {"actor_id": actor, "entities": entities}


def actor_page(engine: Any, bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    """Known action forms are attempts, independent of hidden executability."""
    declaration, _ = _declaration(bundle, actor)
    observation = actor_observation(engine, bundle, actor)
    available = []
    for form in declaration.get("public_actions", []):
        # A represented message's identity is not available before delivery.
        refs = {f["name"] for a in bundle["actions"] if a["kind"] == form["kind"] for f in a["fields"] if f["type"] == "entity_ref"}
        if any(form["fields"][name] not in observation["entities"] for name in refs):
            continue
        identity = {"actor": actor, "kind": form["kind"], **form["fields"]}
        digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:20]
        available.append({"action_id": "known-" + digest,
                          "action": {**identity, "base_revision": engine.world.revision},
                          "description": form["description"], "checks": [], "effects": [], "consequences": [],
                          "executability": "unknown"})
    return {"observation": observation, "available": available, "blocked": [], "progress": [], "total": len(available)}


def actor_context(engine: Any, bundle: dict[str, Any], actor: str, round_no: int | None = None) -> dict[str, Any]:
    """Prompt data from declared inputs only; provenance belongs to analyst records."""
    declaration, profile = _declaration(bundle, actor)
    page = actor_page(engine, bundle, actor)
    def render(record: dict[str, Any]) -> str:
        return "; ".join(f"{component}.{field}: {json.dumps(value, ensure_ascii=False)}"
                         for component, fields in sorted(record["components"].items()) for field, value in sorted(fields.items()))
    entities = page["observation"]["entities"]
    knowledge = "\n".join(item["text"] for item in profile["initial_knowledge"])
    return {"tick": round_no if round_no is not None else engine.world.tick, "actor_id": actor,
            "actor_state": render(entities.get(actor, {"components": {}})) or "nothing observed",
            "visible": "\n".join(f"{row['label']} ({eid}): {render(row)}" for eid, row in sorted(entities.items()) if eid != actor),
            "progress": "", "actions": [{"number": i, "action_id": row["action_id"], "description": row["description"] + " (" + ", ".join(
                f"{name}={entities[value]['label']} ({value})" if isinstance(value, str) and value in entities
                else f"{name}={json.dumps(value, ensure_ascii=False)}"
                for name, value in sorted(row["action"].items()) if name not in {"actor", "kind", "base_revision", "controller"}) + ") [executability unknown]"} for i, row in enumerate(page["available"], 1)],
            "world_summary": declaration["public_summary"], "brief": profile["brief"] + ("\n" + knowledge if knowledge else ""), "recent": []}


def actor_input_provenance(bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    declaration, profile = _declaration(bundle, actor)
    return {"mode": "declared-v1", "summary": "actor_information.public_summary",
            "brief": f"actor_information.actors.{actor}.brief", "initial_knowledge": deepcopy(profile["initial_knowledge"]),
            "public_entities": deepcopy(declaration["public_entities"]), "observable_fields": deepcopy(profile["observable_fields"])}
