#!/usr/bin/env python3
"""Render a Living Scene v1 profile over retained canonical live projections."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import (
    LIVING_SCENE_SCHEMA_VERSION,
    build_living_scene_frames,
    load_live_projection_bundle,
    load_scene_contract,
)


def _asset_html(asset: dict[str, Any], profile_dir: Path) -> str:
    kind = asset.get("kind")
    if kind in {"emoji", "text"}:
        return html.escape(str(asset.get("value") or ""))
    if kind == "image":
        path_value = asset.get("path")
        if not isinstance(path_value, str) or not path_value:
            raise ValueError("image asset requires path")
        path = (profile_dir / path_value).resolve()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"<img alt='' src='data:{mime};base64,{data}'>"
    raise ValueError(f"unsupported asset kind {kind!r}")


def _label(visual_id: str, visual: dict[str, Any]) -> str:
    return html.escape(str(visual.get("label") or visual_id))


def render_html(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    profile_dir: Path,
    *,
    observer_actor_id: str | None = None,
) -> str:
    if profile.get("schema_version") != LIVING_SCENE_SCHEMA_VERSION:
        raise ValueError("living renderer requires world-substrate-living-scene/v1")
    frames = build_living_scene_frames(
        bundle, profile, observer_actor_id=observer_actor_id
    )
    assets = {key: _asset_html(value, profile_dir) for key, value in profile["assets"].items()}
    payload = json.dumps(frames, separators=(",", ":")).replace("</", "<\\/")
    profile_payload = deepcopy(profile)
    profile_payload["resolved_assets"] = assets
    profile_json = json.dumps(profile_payload, separators=(",", ":")).replace("</", "<\\/")

    zones_html = []
    for zone_id, zone in profile["zones"].items():
        x, y, w, h = zone["rect"]
        zones_html.append(
            f"<div class='zone' data-zone='{html.escape(zone_id, quote=True)}' "
            f"style='left:{x}%;top:{y}%;width:{w}%;height:{h}%;'>"
            f"<span>{_label(zone_id, zone)}</span></div>"
        )

    actors_html = []
    for actor_id, actor in profile["actors"].items():
        asset = assets.get(actor.get("asset"), html.escape(str(actor.get("glyph") or "●")))
        actors_html.append(
            f"<div class='actor' data-actor='{html.escape(actor_id, quote=True)}'>"
            f"<div class='actor-glyph'>{asset}</div><strong>{_label(actor_id, actor)}</strong>"
            "<small class='actor-state'></small></div>"
        )

    entities_html = []
    for entity_id, entity in profile["entities"].items():
        asset = assets.get(entity.get("asset"), html.escape(str(entity.get("glyph") or "◆")))
        entities_html.append(
            f"<div class='entity-card' data-entity='{html.escape(entity_id, quote=True)}'>"
            f"<div class='entity-glyph'>{asset}</div><div><strong>{_label(entity_id, entity)}</strong>"
            "<div class='entity-values'></div><div class='meter'><i></i></div></div></div>"
        )

    activities_html = []
    for activity_id, activity in profile["activities"].items():
        activities_html.append(
            f"<div class='activity-card' data-activity='{html.escape(activity_id, quote=True)}'>"
            f"<strong>{_label(activity_id, activity)}</strong><span class='activity-state'></span></div>"
        )

    institutions_html = []
    for institution_id, institution in profile["institutions"].items():
        institutions_html.append(
            f"<div class='institution-card' data-institution='{html.escape(institution_id, quote=True)}'>"
            f"<strong>{_label(institution_id, institution)}</strong>"
            "<span class='institution-state'></span><small class='institution-counts'></small></div>"
        )

    scene = profile.get("scene") or {}
    title = html.escape(str(profile.get("title") or profile["scene_id"]))
    subtitle = html.escape(str(profile.get("subtitle") or ""))
    background = html.escape(str(scene.get("background") or "#d9e1e8"), quote=True)
    shell_background = html.escape(str(scene.get("shell_background") or "#111820"), quote=True)
    aspect = html.escape(str(scene.get("aspect_ratio") or "16 / 9"), quote=True)
    autoplay_ms = max(250, int(scene.get("autoplay_ms") or 1600))
    mobile_min_height = max(520, int(scene.get("mobile_min_height") or 700))

    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title}</title><style>
:root{{--bg:{shell_background};--world:{background};--ink:#17202a;--muted:#667685;--panel:#f7f8f8;--line:#22313f2c;--good:#287a52;--warn:#b16a16}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);font:15px/1.35 system-ui,-apple-system,sans-serif;color:white}}.shell{{max-width:1280px;margin:auto;padding:18px}}h1{{margin:0;font-size:clamp(24px,3vw,40px)}}.sub{{color:#b8c4ce;margin:4px 0 14px}}.stage{{position:relative;aspect-ratio:{aspect};min-height:520px;border-radius:18px;overflow:hidden;background:var(--world);border:4px solid #080b0e;box-shadow:0 24px 70px #0008}}.zone{{position:absolute;border:2px dashed #30485c66;border-radius:18px;background:#ffffff22;color:#273746}}.zone>span{{position:absolute;left:10px;top:8px;font-size:11px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}}.actor{{position:absolute;z-index:8;transform:translate(-50%,-50%);text-align:center;transition:left .55s ease,top .55s ease;width:110px}}.actor-glyph{{font-size:42px;filter:drop-shadow(0 4px 3px #0005)}}.actor strong{{display:block;background:#101820dd;border-radius:8px;padding:3px 7px;font-size:11px}}.actor small{{display:block;color:#d9e2e8;font-size:10px;margin-top:2px}}.actor.state-positive .actor-glyph{{filter:drop-shadow(0 0 8px #3fa770)}}.actor.state-warning .actor-glyph{{filter:drop-shadow(0 0 8px #d58a2c)}}.actor.state-danger .actor-glyph{{filter:drop-shadow(0 0 8px #d55b56)}}.entity-card{{position:absolute;z-index:6;transform:translate(-50%,-50%);display:flex;gap:8px;align-items:center;min-width:150px;max-width:210px;background:#fffffff0;color:var(--ink);border:1px solid #24374655;border-radius:12px;padding:8px 10px;box-shadow:0 7px 20px #0003;transition:opacity .2s,transform .2s}}.entity-glyph{{font-size:28px}}.entity-card strong{{font-size:11px}}.entity-values{{font-size:10px;color:var(--muted)}}.meter{{height:5px;background:#24374618;border-radius:99px;overflow:hidden;margin-top:4px}}.meter i{{display:block;height:100%;background:var(--good);width:0}}.entity-card.unmet .meter i{{background:var(--warn)}}.entity-card.state-positive{{outline:2px solid #4ea978}}.entity-card.state-warning{{outline:2px solid #d58a2c}}.entity-card.state-danger{{outline:2px solid #d55b56}}.activity-card,.institution-card{{position:absolute;z-index:7;transform:translate(-50%,-50%);background:#182838ed;color:white;border:1px solid #ffffff33;border-radius:12px;padding:9px 12px;min-width:150px;text-align:center;box-shadow:0 7px 20px #0004}}.activity-card span,.institution-card span,.institution-card small{{display:block;font-size:10px;color:#c9d5dd;margin-top:3px}}.activity-card.active{{outline:3px solid #62b7ff99}}.institution-card.blocked{{outline:3px solid #e18b6699}}.institution-card.ready{{outline:3px solid #69d19b99}}.hud{{position:absolute;left:50%;top:14px;transform:translateX(-50%);z-index:20;background:#0d151ddd;color:white;border-radius:999px;padding:7px 12px;font-size:11px;max-width:80%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.effect-lines{{position:absolute;inset:0;width:100%;height:100%;z-index:10;pointer-events:none}}.transmission-line{{stroke:#237f9c;stroke-width:2.5;stroke-dasharray:7 6;fill:none}}.message-bubble{{position:absolute;z-index:15;transform:translate(-50%,0);max-width:260px;background:#f7fbfd;color:#17202a;border:2px solid #4c8da2;border-radius:12px;padding:7px 9px;box-shadow:0 7px 18px #0003;font-size:10px}}.message-bubble strong{{display:block;font-size:10px}}.message-bubble small{{color:#657985}}.feedback{{position:absolute;z-index:16;left:50%;bottom:16px;transform:translateX(-50%);max-width:80%;background:#15202bdd;color:white;border:2px solid #75808a;border-radius:999px;padding:7px 12px;font-size:10px;box-shadow:0 6px 18px #0004}}.feedback.accepted{{border-color:#69d19b}}.feedback.rejected,.feedback.refused,.feedback.blocked{{border-color:#e18b66}}.controls{{display:flex;gap:8px;align-items:center;margin-top:10px}}button{{border:0;border-radius:9px;padding:9px 12px;font-weight:800;cursor:pointer}}.scrub{{flex:1;min-width:120px}}.progress{{height:7px;background:#ffffff20;border-radius:99px;width:min(220px,25%);overflow:hidden}}.progress i{{display:block;height:100%;background:#73a8d3}}@media(max-width:760px){{.shell{{padding:8px}}.stage{{min-height:600px;aspect-ratio:auto}}.actor{{width:82px}}.actor-glyph{{font-size:34px}}.entity-card{{min-width:0;width:132px;max-width:132px;padding:6px;transform:translate(-50%,-50%) scale(.82)}}.entity-glyph{{font-size:22px}}.entity-card strong{{font-size:10px}}.entity-values{{font-size:9px}}.activity-card,.institution-card{{min-width:0;width:176px;padding:7px;transform:translate(-50%,-50%) scale(.9)}}.stage{{min-height:{mobile_min_height}px}}}}
</style></head><body><main class='shell'><h1>{title}</h1><p class='sub'>{subtitle}</p><section class='stage' id='stage'>{''.join(zones_html)}<div id='hud' class='hud'></div><svg id='effectLines' class='effect-lines'></svg><div id='messageLayer'></div><div id='feedback' class='feedback' hidden></div>{''.join(entities_html)}{''.join(activities_html)}{''.join(institutions_html)}{''.join(actors_html)}</section><div class='controls'><button id='restart'>↺</button><button id='prev'>←</button><button id='toggle'>Pause</button><button id='next'>→</button><input id='scrub' class='scrub' type='range' min='0' max='{len(frames)-1}' value='0' aria-label='canonical event boundary'><div class='progress'><i id='bar'></i></div></div></main>
<script>const FRAMES={payload};const PROFILE={profile_json};let idx=0,playing=true,timer=null;
function xy(el,p){{if(!p)return;el.style.left=p[0]+'%';el.style.top=p[1]+'%'}}
function mobile(){{return window.matchMedia('(max-width:760px)').matches}}
function homePoint(cfg){{return mobile()&&cfg.mobile_home?cfg.mobile_home:cfg.home}}
function anchorPoint(cfg){{return mobile()&&cfg.mobile_anchor?cfg.mobile_anchor:cfg.anchor}}
function layoutZones(){{for(const [id,cfg] of Object.entries(PROFILE.zones||{{}})){{const el=document.querySelector('[data-zone="'+id+'"]'),r=mobile()&&cfg.mobile_rect?cfg.mobile_rect:cfg.rect;if(el&&r){{el.style.left=r[0]+'%';el.style.top=r[1]+'%';el.style.width=r[2]+'%';el.style.height=r[3]+'%'}}}}}}
function bind(view,name){{return view?.bindings?.[name]}}
function anchorFor(op){{if(Array.isArray(op.anchor))return op.anchor;if(op.zone)return PROFILE.zones?.[op.zone]?.anchor||null;if(op.entity)return homePoint(PROFILE.entities?.[op.entity]||{{}})||null;return null}}
function actorPositions(f){{const out={{}};for(const [id,v] of Object.entries(PROFILE.actors))out[id]=homePoint(v)||[50,50];for(const [aid,av] of Object.entries(PROFILE.activities)){{const row=f.views.activities?.[aid],status=bind(row,av.render?.status_binding||'status');if(status==='active'&&Array.isArray(av.participants)&&av.anchor){{av.participants.forEach((actor,n)=>{{const count=av.participants.length,angle=(Math.PI*2*n/Math.max(count,1))-Math.PI/2,r=13;out[actor]=[av.anchor[0]+Math.cos(angle)*r,av.anchor[1]+Math.sin(angle)*r]}})}}}}for(const op of f.event_visual?.operations||[]){{if(op.op==='actor.move_to'&&op.actor&&out[op.actor]){{const p=anchorFor(op);if(p)out[op.actor]=p}}}}return out}}
function effectPoint(id,positions){{if(positions[id])return positions[id];if(PROFILE.entities?.[id]){{const p=homePoint(PROFILE.entities[id]);if(p)return p}}if(PROFILE.activities?.[id]){{const p=anchorPoint(PROFILE.activities[id]);if(p)return p}}if(PROFILE.institutions?.[id]){{const p=anchorPoint(PROFILE.institutions[id]);if(p)return p}}return null}}
function renderEffects(f,positions){{const svg=document.getElementById('effectLines'),messages=document.getElementById('messageLayer'),feedback=document.getElementById('feedback');svg.innerHTML='';messages.innerHTML='';feedback.hidden=true;feedback.className='feedback';for(const effect of f.presentation_effects||[]){{if(effect.kind==='information_transmission'){{const a=effectPoint(effect.source_id,positions),b=effectPoint(effect.recipient_id,positions);if(a&&b){{const line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',a[0]+'%');line.setAttribute('y1',a[1]+'%');line.setAttribute('x2',b[0]+'%');line.setAttribute('y2',b[1]+'%');line.setAttribute('class','transmission-line');svg.appendChild(line)}}if(b){{const bubble=document.createElement('div');bubble.className='message-bubble';bubble.style.left=b[0]+'%';bubble.style.top=Math.min(88,b[1]+8)+'%';const detail=effect.content_visible&&effect.content?effect.content:'message delivered',head=document.createElement('strong'),channel=document.createElement('small'),body=document.createElement('div');head.textContent=effect.source_id+' → '+effect.recipient_id;channel.textContent=effect.channel_id||'channel';body.textContent=detail;bubble.append(head,channel,body);messages.appendChild(bubble)}}}}else if(effect.kind==='action_feedback'){{feedback.hidden=false;feedback.className='feedback '+effect.status;const checks=effect.checks||[],failed=checks.filter(x=>x.ok===false).map(x=>x.label),passed=checks.filter(x=>x.ok===true).map(x=>x.label),legacy=(effect.reasons||[]);const parts=[];if(failed.length)parts.push('failed: '+failed.join(' · '));else if(legacy.length)parts.push('failed: '+legacy.join(' · '));if(passed.length)parts.push('passed: '+passed.join(' · '));feedback.textContent=(effect.label||effect.status)+(parts.length?' — '+parts.join(' | '):'')}}}}}}
function render(i){{idx=Math.max(0,Math.min(FRAMES.length-1,i));const f=FRAMES[idx],positions=actorPositions(f);layoutZones();for(const [id,v] of Object.entries(f.views.actors)){{const el=document.querySelector('[data-actor="'+id+'"]');xy(el,positions[id]);const cfg=PROFILE.actors[id],key=cfg.render?.state_binding||Object.keys(v.bindings||{{}})[0],state=key?bind(v,key):'';el.querySelector('strong').textContent=bind(v,'label')||cfg.label||id;el.querySelector('.actor-state').textContent=state??'';for(const token of ['positive','warning','danger','neutral','muted'])el.classList.toggle('state-'+token,PROFILE.state_styles?.[state]===token)}}
for(const [id,v] of Object.entries(f.views.entities)){{const el=document.querySelector('[data-entity="'+id+'"]'),cfg=PROFILE.entities[id],r=cfg.render||{{}};xy(el,homePoint(cfg));el.querySelector('strong').textContent=bind(v,'label')||cfg.label||id;const current=bind(v,r.current_binding||'current'),required=bind(v,r.required_binding||'required'),unit=bind(v,r.unit_binding||'unit'),state=bind(v,r.state_binding||'state');for(const token of ['positive','warning','danger','neutral','muted'])el.classList.toggle('state-'+token,PROFILE.state_styles?.[state]===token);let text='';if(current!==undefined&&current!==null)text+=String(current)+(unit?' '+unit:'');if(required!==undefined&&required!==null)text+=(text?' / ':'')+'need '+required+(unit?' '+unit:'');if(state!==undefined&&state!==null)text+=(text?' · ':'')+state;el.querySelector('.entity-values').textContent=text;const ratio=(typeof current==='number'&&typeof required==='number'&&required>0)?Math.max(0,Math.min(1,current/required)):null;el.classList.toggle('unmet',ratio!==null&&ratio<1);el.querySelector('.meter').style.display=ratio===null?'none':'';if(ratio!==null)el.querySelector('.meter i').style.width=(ratio*100)+'%';const visibleKey=r.visible_binding;if(visibleKey)el.style.opacity=bind(v,visibleKey)?'1':'0'}}
for(const [id,v] of Object.entries(f.views.activities)){{const el=document.querySelector('[data-activity="'+id+'"]'),cfg=PROFILE.activities[id],key=cfg.render?.status_binding||'status',state=bind(v,key);xy(el,anchorPoint(cfg));el.querySelector('strong').textContent=bind(v,'label')||cfg.label||id;el.querySelector('.activity-state').textContent=state??'';el.classList.toggle('active',state==='active')}}
for(const [id,v] of Object.entries(f.views.institutions)){{const el=document.querySelector('[data-institution="'+id+'"]'),cfg=PROFILE.institutions[id],r=cfg.render||{{}},state=bind(v,r.status_binding||'status'),support=bind(v,r.support_binding||'support'),required=bind(v,r.required_binding||'required'),conditional=bind(v,r.conditional_binding||'conditional');xy(el,anchorPoint(cfg));el.querySelector('strong').textContent=bind(v,'label')||cfg.label||id;el.querySelector('.institution-state').textContent=state??'';el.querySelector('.institution-counts').textContent=(support!==undefined&&support!==null)?('support '+support+(required!==undefined&&required!==null?' / '+required:'')+(conditional!==undefined&&conditional!==null?' · conditional '+conditional:'')):'';el.classList.toggle('blocked',state==='blocked');el.classList.toggle('ready',state==='ready')}}
renderEffects(f,positions);const ev=f.event,vis=f.event_visual;document.getElementById('hud').textContent='tick '+f.tick+' · rev '+f.revision+(ev?' · '+(vis?.label||ev.rule_id||ev.event_id):' · initial state');document.getElementById('bar').style.width=((idx+1)/FRAMES.length*100)+'%';document.getElementById('scrub').value=idx}}
function schedule(){{clearInterval(timer);if(playing)timer=setInterval(()=>{{if(idx>=FRAMES.length-1){{playing=false;document.getElementById('toggle').textContent='Play';clearInterval(timer)}}else render(idx+1)}},{autoplay_ms})}}document.getElementById('toggle').onclick=()=>{{playing=!playing;document.getElementById('toggle').textContent=playing?'Pause':'Play';schedule()}};document.getElementById('prev').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx-1)}};document.getElementById('next').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx+1)}};document.getElementById('restart').onclick=()=>{{playing=true;document.getElementById('toggle').textContent='Pause';render(0);schedule()}};document.getElementById('scrub').oninput=e=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(parseInt(e.target.value,10)||0)}};const q=new URLSearchParams(location.search),start=Math.max(0,Math.min(FRAMES.length-1,parseInt(q.get('frame')||'0',10)||0));render(start);if(start>0){{playing=false;document.getElementById('toggle').textContent='Play'}}schedule();window.addEventListener('resize',()=>render(idx));
</script></body></html>"""


def render_file(
    projection_path: Path,
    profile_path: Path,
    output_path: Path,
    *,
    observer_actor_id: str | None = None,
) -> None:
    profile = load_scene_contract(profile_path)
    bundle = load_live_projection_bundle(projection_path)
    output_path.write_text(
        render_html(bundle, profile, profile_path.parent, observer_actor_id=observer_actor_id)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projection", type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--observer", default=None)
    args = parser.parse_args()
    render_file(
        args.projection, args.profile, args.output, observer_actor_id=args.observer
    )
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
