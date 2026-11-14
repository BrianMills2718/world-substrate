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
        _object(row, {"id", "label", "fields"}, {"actor_ids", "scope"})
        if "scope" in row and row["scope"] != "place":
            raise ActorInformationError("unsupported public entity scope")
        if not isinstance(row["id"], str) or row["id"] in known:
            raise ActorInformationError("invalid or duplicate public entity")
        paths(row["id"], row["fields"])
        if "actor_ids" in row:
            allowed = row["actor_ids"]
            if not isinstance(allowed, list) or any(not isinstance(a, str) or a not in declaration["actors"] for a in allowed) or len(allowed) != len(set(allowed)):
                raise ActorInformationError("invalid actor identity visibility")
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
        _object(form, {"kind", "description", "fields"}, {"unobserved_refs", "not_self"})
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
        for key in ("unobserved_refs", "not_self"):
            names = form.get(key, [])
            if not isinstance(names, list) or any(declared.get(n) != "entity_ref" for n in names):
                raise ActorInformationError(f"{key} must name entity_ref fields of the form")


def _declaration(bundle: dict[str, Any], actor: str) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_actor_information(bundle)
    if not has_actor_boundary(bundle):
        raise ActorInformationError("legacy bundle has no declared actor-information boundary")
    declaration = bundle["actor_information"]
    if actor not in declaration["actors"]:
        raise ActorInformationError("actor has no declared information profile")
    return declaration, declaration["actors"][actor]


def _place_of(engine: Any, entity_id: str) -> str | None:
    entity = engine.world.entities.get(entity_id)
    return entity.location.location_id if entity is not None and entity.location is not None else None


def actor_observation(engine: Any, bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    """Project only explicit authorized paths; never infer a field from its name.

    A public row with `scope: "place"` is perceived only from the place it stands in (or is), so physical perception
    follows where the actor is. Rows without a scope stay known everywhere (identities, the map, delivered
    reports); that is a declaration, not a distance model. Memory and initial knowledge are separate inputs."""
    declaration, profile = _declaration(bundle, actor)
    extra = {row["entity"]: row["paths"] for row in profile["observable_fields"]}
    entities = {}
    here_id = _place_of(engine, actor)
    placed = any(row.get("scope") == "place" for row in declaration["public_entities"])
    here: list[str] = []
    for row in declaration["public_entities"]:
        if "actor_ids" in row and actor not in row["actor_ids"]:
            continue
        entity = engine.world.entities.get(row["id"])
        if entity is None or not entity_visible_to_actor(engine.world, actor, entity):
            continue
        in_place = here_id is not None and (row["id"] == here_id or _place_of(engine, row["id"]) == here_id)
        if in_place and row["id"] != actor and row["id"] != here_id and "place" not in entity.category_ids:
            here.append(row["id"])
        if row.get("scope") == "place" and row["id"] != actor and not in_place:
            continue
        projected = {"entity_id": row["id"], "label": row["label"], "components": {}}
        for path in sorted(set(row["fields"]) | set(extra.get(row["id"], []))):
            component, field = path.split(".")
            value = getattr(entity.component(component), field, None)
            projected["components"].setdefault(component, {})[field] = deepcopy(value)
        entities[row["id"]] = projected
    observation: dict[str, Any] = {"actor_id": actor, "entities": entities}
    if placed and actor in entities:
        observation["messages"] = _delivered_messages(entities[actor])
    if placed and here_id is not None:
        observation["place"] = {"place_id": here_id, "label": declared_label(declaration, here_id, engine)}
        observation["here"] = sorted(here)
    return observation


def _delivered_messages(own: dict[str, Any]) -> list[dict[str, str]]:
    """Reports delivered to this actor, from the actor's own declared report log (any room, no line of sight)."""
    rows = []
    for raw in own["components"].get("report_log", {}).get("entries", []) or []:
        try:
            item = json.loads(raw)
            rows.append({"from": str(item["source_id"]), "content": str(item["content"])})
        except (TypeError, ValueError, KeyError):
            rows.append({"from": "unknown", "content": str(raw)})
    return rows


def declared_label(declaration: dict[str, Any], entity_id: str, engine: Any) -> str:
    for row in declaration["public_entities"]:
        if row["id"] == entity_id:
            return row["label"]
    entity = engine.world.entities.get(entity_id)
    return entity.label if entity is not None else entity_id


def actor_page(engine: Any, bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    """Known action forms are attempts, independent of hidden executability."""
    declaration, _ = _declaration(bundle, actor)
    observation = actor_observation(engine, bundle, actor)
    available = []
    for form in declaration.get("public_actions", []):
        # A represented message's identity is not available before delivery.
        refs = {f["name"] for a in bundle["actions"] if a["kind"] == form["kind"] for f in a["fields"] if f["type"] == "entity_ref"}
        # `unobserved_refs`: fields the actor names without perceiving them (the far side of a door it stands at);
        # `not_self`: fields that must not be the actor (telling yourself something).
        if any(form["fields"][name] not in observation["entities"] for name in refs - set(form.get("unobserved_refs", []))):
            continue
        if any(form["fields"][name] == actor for name in form.get("not_self", [])):
            continue
        identity = {"actor": actor, "kind": form["kind"], **form["fields"]}
        digest = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:20]
        available.append({"action_id": "known-" + digest,
                          "action": {**identity, "base_revision": engine.world.revision},
                          "description": form["description"], "checks": [], "effects": [], "consequences": [],
                          "executability": "unknown"})
    return {"observation": observation, "available": available, "blocked": [], "progress": [], "total": len(available)}


def actor_context(engine: Any, bundle: dict[str, Any], actor: str, round_no: int | None = None,
                  memories: list[str] | None = None) -> dict[str, Any]:
    """Prompt data from declared inputs only; provenance belongs to analyst records.

    Four inputs stay distinct: the current observation (`place`, `actor_state`, `visible`, which include reports
    delivered to this actor), global knowledge (`world_summary` and the `brief`'s knowledge), retained `memories`
    when the caller supplies them, and the declared actions."""
    declaration, profile = _declaration(bundle, actor)
    page = actor_page(engine, bundle, actor)
    def render(record: dict[str, Any]) -> str:
        return "; ".join(f"{component}.{field}: {json.dumps(value, ensure_ascii=False)}"
                         for component, fields in sorted(record["components"].items()) for field, value in sorted(fields.items()))
    entities = page["observation"]["entities"]
    knowledge = "\n".join(item["text"] for item in profile["initial_knowledge"])
    observation = page["observation"]
    place = observation.get("place")
    here = [entities[e]["label"] for e in observation.get("here", []) if e in entities]
    state = render(entities.get(actor, {"components": {}})) or "nothing observed"
    context = {"tick": round_no if round_no is not None else engine.world.tick, "actor_id": actor,
            "actor_state": (f"You are in the {place['label']}. " if place else "") + state,
            "visible": "\n".join(([f"In this place with you: {', '.join(here) or 'no one else'}."] if place else []) +
                                 [f"Delivered to you from {m['from']}: {m['content']}" for m in observation.get("messages", [])] +
                                 [f"{row['label']} ({eid}): {render(row)}" for eid, row in sorted(entities.items()) if eid != actor]),
            "progress": "", "actions": [{"number": i, "action_id": row["action_id"], "description": row["description"] + " (" + ", ".join(
                f"{name}={entities[value]['label'] if value in entities else declared_label(declaration, value, engine)} ({value})"
                if isinstance(value, str) and (value in entities or any(r["id"] == value for r in declaration["public_entities"]))
                else f"{name}={json.dumps(value, ensure_ascii=False)}"
                for name, value in sorted(row["action"].items()) if name not in {"actor", "kind", "base_revision", "controller"}) + ") [executability unknown]"} for i, row in enumerate(page["available"], 1)],
            "world_summary": declaration["public_summary"], "brief": profile["brief"] + ("\n" + knowledge if knowledge else ""), "recent": []}
    if memories is not None:
        context["memories"] = list(memories)
    return context


def actor_input_provenance(bundle: dict[str, Any], actor: str) -> dict[str, Any]:
    declaration, profile = _declaration(bundle, actor)
    return {"mode": "declared-v1", "summary": "actor_information.public_summary",
            "brief": f"actor_information.actors.{actor}.brief", "initial_knowledge": deepcopy(profile["initial_knowledge"]),
            "public_entities": deepcopy(declaration["public_entities"]), "observable_fields": deepcopy(profile["observable_fields"])}
