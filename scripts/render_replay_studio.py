#!/usr/bin/env python3
"""Render a standalone browser studio around retained graphical replays.

The Studio does not simulate or reinterpret a world. It packages existing replay
HTML documents, enriches their navigation with retained profile/trace metadata,
and lets a viewer compare an automatic baseline with optional polished variants.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

SCHEMA = "world-substrate-replay-studio/v0"


def _load_json(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _within(root: Path, path: Path) -> Path:
    resolved_root = root.resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError(f"studio resource escapes manifest directory: {path}") from exc
    return resolved


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = _load_json(path, "replay studio manifest")
    if manifest.get("schema_version") != SCHEMA:
        raise ValueError(f"replay studio manifest must use {SCHEMA}")
    worlds = manifest.get("worlds")
    if not isinstance(worlds, list) or not worlds:
        raise ValueError("replay studio manifest must contain worlds")
    ids: set[str] = set()
    for world in worlds:
        if not isinstance(world, dict):
            raise ValueError("each studio world must be an object")
        world_id = world.get("id")
        if not isinstance(world_id, str) or not world_id or world_id in ids:
            raise ValueError("studio world ids must be unique nonempty strings")
        ids.add(world_id)
        variants = world.get("variants")
        if not isinstance(variants, list) or not variants:
            raise ValueError(f"studio world {world_id!r} must contain variants")
        variant_ids: set[str] = set()
        for variant in variants:
            if not isinstance(variant, dict):
                raise ValueError(f"studio world {world_id!r} has invalid variant")
            variant_id = variant.get("id")
            replay = variant.get("replay")
            if not isinstance(variant_id, str) or not variant_id or variant_id in variant_ids:
                raise ValueError(f"studio world {world_id!r} variant ids must be unique")
            if not isinstance(replay, str) or not replay:
                raise ValueError(f"studio world {world_id!r} variant {variant_id!r} needs replay")
            variant_ids.add(variant_id)
        if world.get("default_variant") not in variant_ids:
            raise ValueError(f"studio world {world_id!r} has unknown default_variant")
        for key in ("trace", "profile"):
            if not isinstance(world.get(key), str) or not world[key]:
                raise ValueError(f"studio world {world_id!r} needs {key}")
    default_world = manifest.get("default_world")
    if default_world not in ids:
        raise ValueError("default_world must name a declared world")
    return manifest


def build_bundle(manifest_path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    manifest = deepcopy(load_manifest(manifest_path))
    root = manifest_path.parent
    documents: dict[str, str] = {}
    for world in manifest["worlds"]:
        trace_path = _within(root, root / world["trace"])
        profile_path = _within(root, root / world["profile"])
        trace = _load_json(trace_path, f"{world['id']} trace")
        profile = _load_json(profile_path, f"{world['id']} profile")
        if trace.get("world") != world["id"] or profile.get("world") != world["id"]:
            raise ValueError(f"studio world {world['id']!r} resource world mismatch")
        transcript = trace.get("transcript") or []
        actors = list(profile.get("actors") or {})
        action_kinds = list(profile.get("action_visuals") or {})
        bootstrap = profile.get("bootstrap") or {}
        world["metadata"] = {
            "actors": actors,
            "actor_count": len(actors),
            "entity_count": len(profile.get("entities") or {}),
            "station_count": len(profile.get("stations") or {}),
            "action_kinds": action_kinds,
            "turns": len(transcript),
            "model": trace.get("model") or "unknown",
            "cost_usd": float(trace.get("cost_usd") or 0),
            "bootstrap_todos": len(bootstrap.get("todos") or []),
            "declared_bindings": list(bootstrap.get("declared_action_bindings") or []),
            "world_model": profile.get("world_model"),
        }
        for variant in world["variants"]:
            replay_path = _within(root, root / variant["replay"])
            replay = replay_path.read_text()
            if "<html" not in replay.lower():
                raise ValueError(f"studio replay is not HTML: {variant['replay']}")
            key = f"{world['id']}:{variant['id']}"
            documents[key] = base64.b64encode(replay.encode("utf-8")).decode("ascii")
            variant["document_key"] = key
    return manifest, documents


def render_html(manifest: dict[str, Any], documents: dict[str, str]) -> str:
    title = html.escape(str(manifest.get("title") or "World Replay Studio"))
    subtitle = html.escape(str(manifest.get("subtitle") or ""))
    manifest_json = json.dumps(manifest, separators=(",", ":")).replace("</", "<\\/")
    documents_json = json.dumps(documents, separators=(",", ":")).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title>
<style>
:root{{--bg:#0e1114;--panel:#151a1e;--panel2:#1c2328;--line:#2b343a;--text:#edf2f4;--muted:#9ba8af;--warm:#e8b85b;--good:#78c18b}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:var(--bg);color:var(--text);font:14px/1.4 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
body{{min-height:100vh}}button{{font:inherit}}.app{{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}}
.sidebar{{border-right:1px solid var(--line);background:#11161a;padding:22px 16px;position:sticky;top:0;height:100vh;overflow:auto}}
.brand{{padding:0 8px 18px}}.brand h1{{font-size:21px;letter-spacing:-.03em;margin:0 0 5px}}.brand p{{color:var(--muted);margin:0;font-size:12px}}
.world-list{{display:grid;gap:8px}}.world-card{{width:100%;text-align:left;border:1px solid transparent;border-radius:12px;background:transparent;color:var(--text);padding:12px;cursor:pointer}}
.world-card:hover{{background:#ffffff08}}.world-card.active{{background:var(--panel2);border-color:#3a464e}}.world-name{{display:block;font-weight:800;font-size:15px;margin-bottom:3px}}.world-summary{{display:block;color:var(--muted);font-size:11px;line-height:1.35}}
.sidebar-foot{{margin:22px 8px 0;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:11px}}
.main{{min-width:0;padding:22px 26px 34px}}.topbar{{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;margin-bottom:14px}}.title h2{{margin:0 0 4px;font-size:25px;letter-spacing:-.025em}}.title p{{margin:0;color:var(--muted);max-width:720px}}
.variant-tabs{{display:flex;gap:7px;flex-wrap:wrap;justify-content:flex-end}}.variant{{border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:999px;padding:7px 11px;cursor:pointer}}.variant.active{{background:#f1eadc;color:#171b1d;border-color:#f1eadc}}
.variant small{{opacity:.62;margin-left:5px}}.stage-shell{{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#080a0c;box-shadow:0 18px 60px #0007}}iframe{{display:block;width:100%;height:min(76vh,850px);min-height:600px;border:0;background:#101417}}
.stage-foot{{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:10px 12px;border-top:1px solid var(--line);background:var(--panel)}}.variant-copy{{color:var(--muted);font-size:12px;max-width:820px}}.open-button{{white-space:nowrap;border:1px solid #56636b;background:transparent;color:var(--text);border-radius:9px;padding:7px 10px;cursor:pointer}}
.meta{{margin-top:14px;border:1px solid var(--line);border-radius:12px;background:var(--panel);overflow:hidden}}.meta summary{{cursor:pointer;padding:11px 13px;font-weight:750}}.meta-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border-top:1px solid var(--line)}}.metric{{background:var(--panel);padding:11px 13px;min-width:0}}.metric b{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:3px}}.metric span,.metric code{{word-break:break-word}}.good{{color:var(--good)}}
@media(max-width:900px){{.app{{grid-template-columns:1fr}}.sidebar{{height:auto;position:static;border-right:0;border-bottom:1px solid var(--line)}}.world-list{{grid-template-columns:repeat(3,minmax(0,1fr))}}.main{{padding:18px 14px 28px}}.topbar{{display:block}}.variant-tabs{{justify-content:flex-start;margin-top:12px}}iframe{{min-height:520px;height:70vh}}.meta-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
@media(max-width:600px){{.world-list{{grid-template-columns:1fr}}.meta-grid{{grid-template-columns:1fr}}iframe{{min-height:430px;height:66vh}}}}
</style>
</head>
<body>
<div class='app'>
<aside class='sidebar'>
  <div class='brand'><h1>{title}</h1><p>{subtitle}</p></div>
  <div class='world-list' id='world-list'></div>
  <div class='sidebar-foot'>Automatic is the declaration-driven authoring baseline. Polished variants are optional presentation layers over retained behavior.</div>
</aside>
<main class='main'>
  <div class='topbar'>
    <div class='title'><h2 id='world-title'></h2><p id='world-summary'></p></div>
    <div class='variant-tabs' id='variant-tabs'></div>
  </div>
  <section class='stage-shell'>
    <iframe id='replay-frame' sandbox='allow-scripts' title='World replay'></iframe>
    <div class='stage-foot'><div class='variant-copy' id='variant-copy'></div><button class='open-button' id='open-button'>Open replay alone ↗</button></div>
  </section>
  <details class='meta'><summary>Replay provenance & metadata</summary><div class='meta-grid' id='meta-grid'></div></details>
</main>
</div>
<script>
const MANIFEST={manifest_json};
const DOCUMENTS={documents_json};
let worldId=MANIFEST.default_world;
let variantId=null;
const byId=id=>document.getElementById(id);
function decodeDocument(key){{const binary=atob(DOCUMENTS[key]);const bytes=Uint8Array.from(binary,c=>c.charCodeAt(0));return new TextDecoder().decode(bytes)}}
function currentWorld(){{return MANIFEST.worlds.find(w=>w.id===worldId)}}
function currentVariant(){{const w=currentWorld();return w.variants.find(v=>v.id===variantId)}}
function metric(label,value,cls=''){{return `<div class="metric"><b>${{label}}</b><span class="${{cls}}">${{value}}</span></div>`}}
function renderSidebar(){{byId('world-list').innerHTML=MANIFEST.worlds.map(w=>`<button class="world-card ${{w.id===worldId?'active':''}}" data-world="${{w.id}}"><span class="world-name">${{w.label}}</span><span class="world-summary">${{w.summary}}</span></button>`).join('');document.querySelectorAll('[data-world]').forEach(el=>el.onclick=()=>selectWorld(el.dataset.world))}}
function renderTabs(){{const w=currentWorld();byId('variant-tabs').innerHTML=w.variants.map(v=>`<button class="variant ${{v.id===variantId?'active':''}}" data-variant="${{v.id}}">${{v.label}} <small>${{v.kind||''}}</small></button>`).join('');document.querySelectorAll('[data-variant]').forEach(el=>el.onclick=()=>{{variantId=el.dataset.variant;render()}})}}
function renderMetadata(){{const w=currentWorld(),m=w.metadata;const bindings=(m.declared_bindings||[]).join(', ')||'none';const actions=(m.action_kinds||[]).join(', ')||'none';byId('meta-grid').innerHTML=[metric('Actors',m.actors.join(', ')),metric('Turns',m.turns),metric('Action families',actions),metric('World visuals',`${{m.entity_count}} entities · ${{m.station_count}} stations`),metric('Model',m.model),metric('Retained cost',`$${{Number(m.cost_usd).toFixed(5)}}`),metric('Bootstrap TODOs',m.bootstrap_todos,m.bootstrap_todos===0?'good':''),metric('Declared bindings',bindings)].join('')}}
function render(){{const w=currentWorld(),v=currentVariant();renderSidebar();renderTabs();byId('world-title').textContent=w.label;byId('world-summary').textContent=w.summary;byId('variant-copy').textContent=v.description||'';byId('replay-frame').srcdoc=decodeDocument(v.document_key);renderMetadata()}}
function selectWorld(id){{worldId=id;variantId=currentWorld().default_variant;render()}}
byId('open-button').onclick=()=>{{const v=currentVariant();const blob=new Blob([decodeDocument(v.document_key)],{{type:'text/html;charset=utf-8'}});const url=URL.createObjectURL(blob);window.open(url,'_blank','noopener');setTimeout(()=>URL.revokeObjectURL(url),60000)}};
const params=new URLSearchParams(location.search);
const requestedWorld=params.get('world');if(requestedWorld&&MANIFEST.worlds.some(w=>w.id===requestedWorld))worldId=requestedWorld;
const requestedVariant=params.get('variant'),initialWorld=currentWorld();variantId=requestedVariant&&initialWorld.variants.some(v=>v.id===requestedVariant)?requestedVariant:initialWorld.default_variant;render();
</script>
</body>
</html>"""


def render_file(manifest_path: Path, output_path: Path) -> None:
    manifest, documents = build_bundle(manifest_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(manifest, documents))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    render_file(args.manifest, args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
