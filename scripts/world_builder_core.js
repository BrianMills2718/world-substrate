(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.WorldBuilderCore = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";
  const SCHEMA_VERSION = "world-substrate-authoring-bundle/v0";
  const ID_RE = /^[a-z][a-z0-9-]*$/;
  const IDENT_RE = /^[A-Za-z_][A-Za-z0-9_]*$/;
  const OWNER_RE = /^(?:(?:actor|place|entity):[^:]+|unowned)$/;
  const FIELD_TYPES = new Set(["string", "integer", "number", "boolean", "string_list", "entity_ref", "entity_ref_or_null"]);
  const ACTION_TYPES = new Set(["string", "integer", "number", "boolean", "entity_ref"]);
  const RESERVED_ACTION_FIELDS = new Set(["actor", "kind", "base_revision", "controller"]);

  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function fail(errors, message) { errors.push(message); }
  function typeOk(kind, value) {
    if (kind === "string" || kind === "entity_ref") return typeof value === "string" && value.length > 0;
    if (kind === "entity_ref_or_null") return value === null || (typeof value === "string" && value.length > 0);
    if (kind === "integer") return Number.isInteger(value);
    if (kind === "number") return typeof value === "number" && Number.isFinite(value);
    if (kind === "boolean") return typeof value === "boolean";
    if (kind === "string_list") return Array.isArray(value) && value.every(x => typeof x === "string");
    return false;
  }
  function validateBundle(value) {
    const errors = [];
    if (!value || typeof value !== "object" || Array.isArray(value)) return {ok:false, errors:["bundle must be a JSON object"]};
    if (value.schema_version !== SCHEMA_VERSION) fail(errors, `schema_version must be ${SCHEMA_VERSION}`);
    const world = value.world;
    if (!world || typeof world !== "object" || Array.isArray(world)) fail(errors, "world must be an object");
    else {
      if (!ID_RE.test(world.id || "")) fail(errors, "world.id must be a lowercase slug");
      for (const key of ["label", "summary", "location"]) if (typeof world[key] !== "string" || !world[key].trim()) fail(errors, `world.${key} must be nonempty`);
      if (world.content_version !== undefined && (!Number.isInteger(world.content_version) || world.content_version < 1)) fail(errors, "world.content_version must be a positive integer");
    }
    const componentMap = new Map();
    if (!Array.isArray(value.components)) fail(errors, "components must be a list");
    else value.components.forEach((comp, ci) => {
      if (!comp || typeof comp !== "object") return fail(errors, `component ${ci} must be an object`);
      if (!IDENT_RE.test(comp.name || "")) fail(errors, `component ${ci} name must be an identifier`);
      if (componentMap.has(comp.name)) fail(errors, `duplicate component: ${comp.name}`); else componentMap.set(comp.name, comp);
      if (!Array.isArray(comp.fields) || !comp.fields.length) fail(errors, `component ${comp.name || ci} needs fields`);
      else {
        const seen = new Set();
        comp.fields.forEach(field => {
          if (!field || typeof field !== "object") return fail(errors, `component ${comp.name} field must be an object`);
          if (!IDENT_RE.test(field.name || "")) fail(errors, `component ${comp.name} field name must be an identifier`);
          if (seen.has(field.name)) fail(errors, `duplicate field ${comp.name}.${field.name}`); seen.add(field.name);
          if (!FIELD_TYPES.has(field.type)) fail(errors, `unsupported field type at ${comp.name}.${field.name}`);
          else if (!("default" in field) || !typeOk(field.type, field.default)) fail(errors, `default for ${comp.name}.${field.name} does not match ${field.type}`);
        });
      }
    });
    const entityIds = new Set();
    if (!Array.isArray(value.entities) || !value.entities.length) fail(errors, "entities must be a nonempty list");
    else value.entities.forEach((entity, ei) => {
      if (!entity || typeof entity !== "object") return fail(errors, `entity ${ei} must be an object`);
      if (!ID_RE.test(entity.id || "")) fail(errors, `entity ${ei} id must be a lowercase slug`);
      if (entityIds.has(entity.id)) fail(errors, `duplicate entity: ${entity.id}`); entityIds.add(entity.id);
      if (typeof entity.label !== "string" || !entity.label.trim()) fail(errors, `entity ${entity.id || ei} label must be nonempty`);
      if (!Array.isArray(entity.categories) || !entity.categories.length || entity.categories.some(x => typeof x !== "string" || !x)) fail(errors, `entity ${entity.id || ei} categories must be nonempty strings`);
      if (entity.owner_ref !== undefined && (!OWNER_RE.test(entity.owner_ref || ""))) fail(errors, `entity ${entity.id || ei} owner_ref is invalid`);
      const comps = entity.components || {};
      if (!comps || typeof comps !== "object" || Array.isArray(comps)) fail(errors, `entity ${entity.id || ei} components must be an object`);
      else Object.entries(comps).forEach(([name, fields]) => {
        const comp = componentMap.get(name);
        if (!comp) return fail(errors, `entity ${entity.id} uses undeclared component ${name}`);
        if (!fields || typeof fields !== "object" || Array.isArray(fields)) return fail(errors, `entity ${entity.id} component ${name} must be an object`);
        const declared = new Map(comp.fields.map(f => [f.name, f]));
        const actual = Object.keys(fields).sort().join("|"); const expected = [...declared.keys()].sort().join("|");
        if (actual !== expected) fail(errors, `entity ${entity.id} component ${name} fields must match its declaration`);
        for (const [fname, spec] of declared) if (fname in fields && !typeOk(spec.type, fields[fname])) fail(errors, `entity ${entity.id} value ${name}.${fname} does not match ${spec.type}`);
      });
    });
    if (Array.isArray(value.entities)) value.entities.forEach(entity => Object.entries(entity.components || {}).forEach(([name, fields]) => {
      const comp = componentMap.get(name); if (!comp) return;
      comp.fields.forEach(spec => {
        const target = fields[spec.name];
        if ((spec.type === "entity_ref" || spec.type === "entity_ref_or_null") && target !== null && target !== undefined && !entityIds.has(target)) fail(errors, `entity ${entity.id} reference ${name}.${spec.name} names unknown entity ${JSON.stringify(target)}`);
      });
    }));
    const kinds = new Set();
    if (!Array.isArray(value.actions)) fail(errors, "actions must be a list");
    else value.actions.forEach((action, ai) => {
      if (!action || typeof action !== "object") return fail(errors, `action ${ai} must be an object`);
      if (!ID_RE.test(action.kind || "")) fail(errors, `action ${ai} kind must be a lowercase slug`);
      if (kinds.has(action.kind)) fail(errors, `duplicate action kind: ${action.kind}`); kinds.add(action.kind);
      if (typeof action.description !== "string" || !action.description.trim()) fail(errors, `action ${action.kind || ai} description must be nonempty`);
      if (!Array.isArray(action.fields)) fail(errors, `action ${action.kind || ai} fields must be a list`);
      else {
        const seen = new Set();
        action.fields.forEach(field => {
          if (!field || typeof field !== "object") return fail(errors, `action ${action.kind} field must be an object`);
          if (!IDENT_RE.test(field.name || "")) fail(errors, `action ${action.kind} field name must be an identifier`);
          if (RESERVED_ACTION_FIELDS.has(field.name) || seen.has(field.name)) fail(errors, `reserved/duplicate action field: ${field.name}`); seen.add(field.name);
          if (!ACTION_TYPES.has(field.type)) fail(errors, `unsupported action field type at ${action.kind}.${field.name}`);
        });
      }
    });
    const p = value.presentation || {};
    if (!p || typeof p !== "object" || Array.isArray(p)) fail(errors, "presentation must be an object");
    else {
      const assets = p.assets || {};
      if (!assets || typeof assets !== "object" || Array.isArray(assets)) fail(errors, "presentation.assets must be an object");
      else Object.entries(assets).forEach(([id, asset]) => {
        if (!IDENT_RE.test(id)) fail(errors, `asset id must be an identifier: ${id}`);
        if (!asset || typeof asset !== "object" || !["emoji","text"].includes(asset.kind) || typeof asset.value !== "string") fail(errors, `asset ${id} must be emoji/text with string value`);
      });
      for (const key of ["category_assets","station_roles"]) if (!p[key] || typeof p[key] !== "object" || Array.isArray(p[key])) fail(errors, `presentation.${key} must be an object`);
      Object.entries(p.category_assets || {}).forEach(([cat, id]) => { if (!(id in assets)) fail(errors, `category ${cat} references unknown asset ${id}`); });
      Object.entries(p.station_roles || {}).forEach(([cat, role]) => { if (!["source","workstation","surface","goal"].includes(role)) fail(errors, `category ${cat} has unsupported station role ${role}`); });
    }
    return {ok: errors.length === 0, errors};
  }
  function defaultForType(kind) {
    if (kind === "integer" || kind === "number") return 0;
    if (kind === "boolean") return false;
    if (kind === "string_list") return [];
    if (kind === "entity_ref_or_null") return null;
    return "value";
  }
  return {SCHEMA_VERSION, FIELD_TYPES:[...FIELD_TYPES], ACTION_TYPES:[...ACTION_TYPES], validateBundle, defaultForType, clone};
});
