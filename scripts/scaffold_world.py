#!/usr/bin/env python3
"""Validate a world-authoring bundle and scaffold a safe code-first world package."""
from __future__ import annotations

import argparse
import json
import keyword
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "world-substrate-authoring-bundle/v0"
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
OWNER_RE = re.compile(r"^(?:actor|place|entity):[^:]+$|^unowned$")
FIELD_TYPES = {
    "string": "str", "integer": "int", "number": "float", "boolean": "bool",
    "string_list": "list[str]", "entity_ref": "str", "entity_ref_or_null": "str | None",
}
ACTION_TYPES = {"string": "str", "integer": "int", "number": "float", "boolean": "bool", "entity_ref": "str"}
RESERVED_ACTION_FIELDS = {"actor", "kind", "base_revision", "controller"}

class BundleError(ValueError):
    pass

def _identifier(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.isidentifier() or keyword.iskeyword(value):
        raise BundleError(f"{label} must be a Python identifier: {value!r}")
    return value

def _slug(value: object, label: str) -> str:
    if not isinstance(value, str) or not ID_RE.fullmatch(value):
        raise BundleError(f"{label} must match {ID_RE.pattern}: {value!r}")
    return value

def _type_ok(kind: str, value: object) -> bool:
    if kind in {"string", "entity_ref"}: return isinstance(value, str) and bool(value)
    if kind == "entity_ref_or_null": return value is None or (isinstance(value, str) and bool(value))
    if kind == "integer": return type(value) is int
    if kind == "number": return type(value) in (int, float)
    if kind == "boolean": return type(value) is bool
    if kind == "string_list": return isinstance(value, list) and all(isinstance(x, str) for x in value)
    return False

def validate_bundle(value: object) -> dict[str, Any]:
    if not isinstance(value, dict): raise BundleError("bundle must be a JSON object")
    if value.get("schema_version") != SCHEMA_VERSION: raise BundleError(f"schema_version must be {SCHEMA_VERSION}")
    world = value.get("world")
    if not isinstance(world, dict): raise BundleError("world must be an object")
    _slug(world.get("id"), "world.id")
    for key in ("label", "summary", "location"):
        if not isinstance(world.get(key), str) or not world[key].strip(): raise BundleError(f"world.{key} must be nonempty")
    if type(world.get("content_version", 1)) is not int or world.get("content_version", 1) < 1:
        raise BundleError("world.content_version must be a positive integer")

    components = value.get("components")
    if not isinstance(components, list): raise BundleError("components must be a list")
    component_map: dict[str, dict[str, Any]] = {}
    for comp in components:
        if not isinstance(comp, dict): raise BundleError("each component must be an object")
        name = _identifier(comp.get("name"), "component.name")
        if name in component_map: raise BundleError(f"duplicate component: {name}")
        fields = comp.get("fields")
        if not isinstance(fields, list) or not fields: raise BundleError(f"component {name} needs fields")
        seen: set[str] = set()
        for field in fields:
            if not isinstance(field, dict): raise BundleError(f"component {name} field must be an object")
            fname = _identifier(field.get("name"), f"component {name} field.name")
            if fname in seen: raise BundleError(f"duplicate field {name}.{fname}")
            seen.add(fname)
            kind = field.get("type")
            if kind not in FIELD_TYPES: raise BundleError(f"unsupported field type {kind!r} at {name}.{fname}")
            if "default" not in field or not _type_ok(kind, field.get("default")):
                raise BundleError(f"default for {name}.{fname} does not match {kind}")
        component_map[name] = comp

    entities = value.get("entities")
    if not isinstance(entities, list) or not entities: raise BundleError("entities must be a nonempty list")
    entity_ids: set[str] = set()
    for entity in entities:
        if not isinstance(entity, dict): raise BundleError("each entity must be an object")
        eid = _slug(entity.get("id"), "entity.id")
        if eid in entity_ids: raise BundleError(f"duplicate entity: {eid}")
        entity_ids.add(eid)
        if not isinstance(entity.get("label"), str) or not entity["label"].strip(): raise BundleError(f"entity {eid} label must be nonempty")
        cats = entity.get("categories")
        if not isinstance(cats, list) or not cats or any(not isinstance(x, str) or not x for x in cats):
            raise BundleError(f"entity {eid} categories must be nonempty strings")
        owner = entity.get("owner_ref")
        if owner is not None and (not isinstance(owner, str) or not OWNER_RE.fullmatch(owner)):
            raise BundleError(f"entity {eid} owner_ref is invalid: {owner!r}")
        comps = entity.get("components", {})
        if not isinstance(comps, dict): raise BundleError(f"entity {eid} components must be an object")
        for cname, fields in comps.items():
            if cname not in component_map: raise BundleError(f"entity {eid} uses undeclared component {cname}")
            if not isinstance(fields, dict): raise BundleError(f"entity {eid} component {cname} must be an object")
            declared = {f["name"]: f for f in component_map[cname]["fields"]}
            if set(fields) != set(declared): raise BundleError(f"entity {eid} component {cname} fields must be {sorted(declared)}")
            for fname, item in declared.items():
                if not _type_ok(item["type"], fields[fname]): raise BundleError(f"entity {eid} value {cname}.{fname} does not match {item['type']}")
    for entity in entities:
        for cname, fields in (entity.get("components") or {}).items():
            declared = {f["name"]: f for f in component_map[cname]["fields"]}
            for fname, item in declared.items():
                target = fields[fname]
                if item["type"] in {"entity_ref", "entity_ref_or_null"} and target is not None and target not in entity_ids:
                    raise BundleError(f"entity {entity['id']} reference {cname}.{fname} names unknown entity {target!r}")

    actions = value.get("actions")
    if not isinstance(actions, list): raise BundleError("actions must be a list")
    kinds: set[str] = set()
    for action in actions:
        if not isinstance(action, dict): raise BundleError("each action must be an object")
        kind = _slug(action.get("kind"), "action.kind")
        if kind in kinds: raise BundleError(f"duplicate action kind: {kind}")
        kinds.add(kind)
        if not isinstance(action.get("description"), str) or not action["description"].strip(): raise BundleError(f"action {kind} description must be nonempty")
        fields = action.get("fields", [])
        if not isinstance(fields, list): raise BundleError(f"action {kind} fields must be a list")
        seen = set()
        for field in fields:
            if not isinstance(field, dict): raise BundleError(f"action {kind} field must be an object")
            name = _identifier(field.get("name"), f"action {kind} field.name")
            if name in RESERVED_ACTION_FIELDS or name in seen: raise BundleError(f"reserved/duplicate action field: {name}")
            seen.add(name)
            if field.get("type") not in ACTION_TYPES: raise BundleError(f"unsupported action field type at {kind}.{name}")

    presentation = value.get("presentation", {})
    if not isinstance(presentation, dict): raise BundleError("presentation must be an object")
    assets = presentation.get("assets", {})
    if not isinstance(assets, dict): raise BundleError("presentation.assets must be an object")
    for asset_id, asset in assets.items():
        _identifier(asset_id, "asset id")
        if not isinstance(asset, dict) or asset.get("kind") not in {"emoji", "text"} or not isinstance(asset.get("value"), str):
            raise BundleError(f"asset {asset_id} must be emoji/text with string value")
    for key in ("category_assets", "station_roles"):
        if not isinstance(presentation.get(key, {}), dict): raise BundleError(f"presentation.{key} must be an object")
    for category, asset_id in presentation.get("category_assets", {}).items():
        if asset_id not in assets: raise BundleError(f"category {category} references unknown asset {asset_id}")
    for category, role in presentation.get("station_roles", {}).items():
        if role not in {"source", "workstation", "surface", "goal"}: raise BundleError(f"category {category} has unsupported station role {role}")
    return deepcopy(value)

def load_bundle(path: Path) -> dict[str, Any]:
    return validate_bundle(json.loads(path.read_text()))

def _class_name(name: str) -> str:
    return "".join(part.capitalize() for part in name.replace("-", "_").split("_"))

def _render_components(bundle: dict[str, Any]) -> str:
    lines = ['"""Typed components generated from authoring-v0.json."""', '', 'from __future__ import annotations', '', 'from dataclasses import dataclass, field', '', 'from world_substrate.model import register_component', '']
    for comp in bundle["components"]:
        cls = _class_name(comp["name"]) + "State"
        lines += ['@dataclass', f'class {cls}:']
        for item in comp["fields"]:
            annotation = FIELD_TYPES[item["type"]]
            if item["type"] == "string_list":
                lines.append(f'    {item["name"]}: {annotation} = field(default_factory=lambda: {item["default"]!r})')
            else:
                lines.append(f'    {item["name"]}: {annotation} = {item["default"]!r}')
        lines += ['', f'register_component({comp["name"]!r}, {cls})', '']
    return "\n".join(lines).rstrip() + "\n"

def _render_mechanics(bundle: dict[str, Any]) -> str:
    lines = ['"""Safe action-signature stubs generated from authoring-v0.json.', '', 'Signatures are not causal law. Every generated rule refuses until a developer', 'implements checks, declared read/write authority, effects, and tests.', '"""', 'from __future__ import annotations', '', 'from dataclasses import dataclass', 'from typing import Any', '', 'from world_substrate.model import World', 'from world_substrate.rules import Check, TypedAction', '']
    rule_names=[]
    for action in bundle["actions"]:
        kind=action["kind"]; cls=_class_name(kind)+"Action"; rule=_class_name(kind)+"Rule"; rule_names.append(rule)
        lines += ['@dataclass(frozen=True)', f'class {cls}:', '    actor_id: str']
        for field in action.get("fields", []): lines.append(f'    {field["name"]}: {ACTION_TYPES[field["type"]]}')
        lines += ['    base_revision: int', '    controller_id: str', f'    kind: str = {kind!r}', '', '    def as_dict(self) -> dict[str, object]:', '        return {', '            "actor": self.actor_id,', '            "kind": self.kind,']
        for field in action.get("fields", []): lines.append(f'            {field["name"]!r}: self.{field["name"]},')
        lines += ['            "base_revision": self.base_revision,', '            "controller": self.controller_id,', '        }', '', '    @classmethod', f'    def from_dict(cls, value: dict[str, Any]) -> "{cls}":', f'        if value.get("kind") != {kind!r}:', f'            raise ValueError("record is not a {kind} action")', '        actor = value.get("actor")', '        revision = value.get("base_revision")', '        controller = value.get("controller")', '        if not isinstance(actor, str) or not actor or type(revision) is not int or not isinstance(controller, str) or not controller:', '            raise ValueError("malformed action envelope")']
        for field in action.get("fields", []):
            n=field["name"]; t=field["type"]
            check = {'string':'isinstance(v, str) and bool(v)','entity_ref':'isinstance(v, str) and bool(v)','integer':'type(v) is int','number':'type(v) in (int, float)','boolean':'type(v) is bool'}[t]
            lines += [f'        {n} = value.get({n!r})', f'        v = {n}', f'        if not ({check}):', f'            raise ValueError("invalid action field: {n}")']
        args=['actor_id=actor']+[f'{f["name"]}={f["name"]}' for f in action.get("fields", [])]+['base_revision=revision','controller_id=controller']
        lines += [f'        return cls({", ".join(args)})', '', f'class {rule}:', f'    """TODO: implement causal law for `{kind}`; this stub always refuses."""', f'    rule_id = {(bundle["world"]["id"] + ".action." + kind)!r}', '    version = "1"', f'    action_kind = {kind!r}', '    read_paths: tuple[str, ...] = ()', '    write_paths: tuple[str, ...] = ()', '', f'    def action_from_dict(self, value: dict[str, Any]) -> {cls}:', f'        return {cls}.from_dict(value)', '', '    def discover(self, world: World, actor_id: str) -> list[TypedAction]:', '        return []', '', '    def checks(self, world: World, action: TypedAction) -> list[Check]:', '        return [Check("Mechanic implementation required", False)]', '', '    def apply(self, world: World, action: TypedAction, event_id: str) -> None:', f'        raise RuntimeError("{kind} mechanic is not implemented")', '']
    if rule_names:
        suffix=',' if len(rule_names)==1 else ''
        lines.append(f'STUB_RULE_TYPES = ({", ".join(rule_names)}{suffix})')
    else:
        lines.append('STUB_RULE_TYPES: tuple[type, ...] = ()')
    lines.append('')
    return "\n".join(lines)

def _render_model(bundle: dict[str, Any]) -> dict[str, Any]:
    world=bundle["world"]; entities=[]
    for entity in bundle["entities"]:
        row={"entity_id":entity["id"],"label":entity["label"],"category_ids":entity["categories"],"location":{"location_id":entity.get("location") or world["location"]}}
        if entity.get("portable") is not None: row["portable"]={"portable":bool(entity["portable"])}
        if entity.get("owner_ref") is not None: row["ownership"]={"owner_ref":entity["owner_ref"]}
        if entity.get("components"): row["components"]=deepcopy(entity["components"])
        entities.append(row)
    return {"schema_version":"world-substrate-reference-world/v0","world_id":f'{world["id"]}-v0',"content_id":f'world-substrate-{world["id"]}@{world.get("content_version",1)}',"source":{"repository":"world-substrate","authored_for":"world authoring starter kit","note":world["summary"]},"entities":entities}

def _render_probe(bundle: dict[str, Any], model_name: str) -> str:
    classes={c["name"]:_class_name(c["name"])+"State" for c in bundle["components"]}
    imports=", ".join(sorted(classes.values()))
    lines=['"""Load the scaffolded world through the shared substrate."""','from __future__ import annotations','','import json','from pathlib import Path','from typing import Any','','from world_substrate.engine import Engine','from world_substrate.model import Entity, LocationState, OwnershipState, PortableState, World','from world_substrate.rules import RuleRegistry','']
    if imports: lines.append(f'from .components import {imports}')
    lines += ['', f'CONTENT = {model_name!r}', f'_TYPES = {{{", ".join(repr(k)+": "+v for k,v in classes.items())}}}', '', 'def package_root() -> Path:', '    return Path(__file__).resolve().parent', '', 'def build_registry() -> RuleRegistry:', '    # Register only mechanics whose checks/effects/write scopes have been implemented and reviewed.', '    return RuleRegistry()', '', 'def build_engine() -> Engine:', '    content = json.loads((package_root() / CONTENT).read_text())', '    entities: dict[str, Entity] = {}', '    for row in content["entities"]:', '        components: dict[str, Any] = {name: _TYPES[name](**fields) for name, fields in (row.get("components") or {}).items()}', '        entity = Entity(', '            entity_id=row["entity_id"], label=row["label"], category_ids=tuple(row["category_ids"]),', '            location=LocationState(**row["location"]) if row.get("location") else None,', '            ownership=OwnershipState(**row["ownership"]) if row.get("ownership") else None,', '            portable=PortableState(**row["portable"]) if row.get("portable") else None,', '            source_pack_id=content["content_id"], source_entity_id=row["entity_id"], components=components,', '        )', '        entities[entity.entity_id] = entity', '    registry = build_registry()', '    world = World(world_id=content["world_id"], revision=0, tick=0, entities=entities, engine_id="world-substrate-core@1", content_id=content["content_id"], rule_versions=registry.versions())', '    world.validate()', '    return Engine(world, registry)', '']
    return "\n".join(lines)

def _render_terminal() -> str:
    return ('"""World-defined terminal predicate scaffold."""\nfrom __future__ import annotations\n\n'
            'from world_substrate.model import World\n\ndef world_complete(world: World) -> bool:\n'
            '    # TODO: derive completion from represented state; do not duplicate a completion flag.\n    return False\n')

def _render_presentation(bundle: dict[str, Any]) -> dict[str, Any]:
    p=bundle.get("presentation",{}); category={cat:{"asset":asset} for cat,asset in p.get("category_assets",{}).items()}; stations={cat:{"role":role} for cat,role in p.get("station_roles",{}).items()}
    return {"schema_version":"world-substrate-scene-catalog-extension/v0","world":bundle["world"]["id"],"assets":deepcopy(p.get("assets",{})),"category_entity_bindings":category,"category_station_bindings":stations,"note":"Review and merge only justified entries into the shared scene presentation catalog."}

def _render_readme(bundle: dict[str, Any], model_name: str) -> str:
    w=bundle["world"]
    return f'''# {w["label"]}\n\n{w["summary"]}\n\nGenerated by `scripts/scaffold_world.py` from `authoring-v0.json`.\n\n## Safe starting state\n\n- `{model_name}` contains represented initial world state.\n- `components.py` contains typed component declarations.\n- `mechanics.py` contains action signatures whose generated rules **always refuse**. A signature is not causal law.\n- `probe.py` loads and validates the initial world but registers no stub mechanics.\n- `terminal.py` deliberately returns `False` until completion can be derived from represented state.\n- `scene-catalog-extension-v0.json` is presentation input for review; it does not change world truth.\n\n## Implement next\n\n1. Implement each mechanic's checks, read/write scopes, effects, tests, and causal trace behavior.\n2. Register only reviewed mechanics in `probe.build_registry()`.\n3. Replace the terminal stub with a state-derived predicate.\n4. Retain a deterministic no-spend run before attempting model-driven policies.\n5. Merge only justified presentation declarations into the shared scene catalog, then bootstrap an Automatic replay.\n'''

def scaffold(bundle: dict[str, Any], output_root: Path) -> Path:
    bundle=validate_bundle(bundle); slug=bundle["world"]["id"]; target=output_root/slug.replace("-","_")
    if target.exists(): raise BundleError(f"target already exists: {target}")
    target.mkdir(parents=True); model_name=f"{slug}-v0.json"
    (target/'__init__.py').write_text('"""World package generated by the World Substrate authoring starter."""\n')
    (target/'authoring-v0.json').write_text(json.dumps(bundle,indent=2)+"\n")
    (target/model_name).write_text(json.dumps(_render_model(bundle),indent=2)+"\n")
    (target/'components.py').write_text(_render_components(bundle)); (target/'mechanics.py').write_text(_render_mechanics(bundle)); (target/'probe.py').write_text(_render_probe(bundle,model_name)); (target/'terminal.py').write_text(_render_terminal()); (target/'scene-catalog-extension-v0.json').write_text(json.dumps(_render_presentation(bundle),indent=2)+"\n"); (target/'README.md').write_text(_render_readme(bundle,model_name))
    return target

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('bundle',type=Path); ap.add_argument('--output-root',type=Path,default=Path('reference_worlds')); ap.add_argument('--check-only',action='store_true'); args=ap.parse_args(); bundle=load_bundle(args.bundle)
    if args.check_only: print(f"valid {SCHEMA_VERSION}: {bundle['world']['id']}"); return 0
    print(scaffold(bundle,args.output_root)); return 0
if __name__ == '__main__': raise SystemExit(main())
