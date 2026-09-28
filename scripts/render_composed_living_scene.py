#!/usr/bin/env python3
"""Generic composed-world renderer for Living Scene v1 retained projections."""
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


def _asset_uri(asset: dict[str, Any], profile_dir: Path) -> str | None:
    if asset.get("kind") != "image":
        return None
    raw = asset.get("path")
    if not isinstance(raw, str) or not raw:
        raise ValueError("image asset requires path")
    path = (profile_dir / raw).resolve()
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _asset_html(asset: dict[str, Any], profile_dir: Path) -> str:
    kind = asset.get("kind")
    if kind in {"emoji", "text"}:
        return html.escape(str(asset.get("value") or ""))
    uri = _asset_uri(asset, profile_dir)
    if uri is not None:
        return f"<img alt='' draggable='false' src='{uri}'>"
    raise ValueError(f"unsupported asset kind {kind!r}")


def _label(visual_id: str, visual: dict[str, Any]) -> str:
    return html.escape(str(visual.get("label") or visual_id))


def _visual_markup(
    group: str,
    visual_id: str,
    visual: dict[str, Any],
    assets: dict[str, str],
) -> str:
    render = visual.get("render") or {}
    display = html.escape(str(render.get("display") or "world"), quote=True)
    accent = html.escape(str(render.get("accent") or "#7fc1b4"), quote=True)
    asset = assets.get(visual.get("asset"), html.escape(str(visual.get("glyph") or "◆")))
    label = _label(visual_id, visual)
    identity = html.escape(visual_id, quote=True)
    common = f"data-kind='{group}' data-id='{identity}' style='--accent:{accent}' aria-label='{label}' title='{label}'"
    if group == "actors":
        return (
            f"<button class='actor display-{display}' data-actor='{identity}' {common}>"
            f"<span class='actor-aura'></span><span class='actor-figure'>{asset}</span>"
            f"<span class='actor-name'>{label}</span><span class='actor-state'></span></button>"
        )
    class_name = {
        "entities": "entity-object",
        "activities": "activity-object",
        "institutions": "institution-object",
    }[group]
    data_name = {"entities": "entity", "activities": "activity", "institutions": "institution"}[group]
    if group == "entities":
        extra = "<span class='object-values'></span><span class='meter'><i></i></span>"
    elif group == "activities":
        extra = "<span class='activity-state object-state'></span>"
    else:
        extra = "<span class='institution-state object-state'></span><span class='institution-counts object-values'></span>"
    return (
        f"<button class='world-object {class_name} display-{display}' data-{data_name}='{identity}' {common}>"
        f"<span class='object-visual'>{asset}<span class='status-light'></span></span>"
        f"<span class='object-name'>{label}</span>{extra}</button>"
    )


_CSS = r"""
:root{--shell:__SHELL__;--world:__WORLD__;--ink:#12202a;--good:#52b184;--warn:#dda04b;--danger:#d86f67;--cyan:#72d8e4}
*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--shell);font:14px/1.35 Inter,ui-sans-serif,system-ui,-apple-system,sans-serif;color:#f5f6f4}button,input{font:inherit}.shell{max-width:1440px;margin:auto;padding:10px}.stage{position:relative;aspect-ratio:__ASPECT__;min-height:620px;overflow:hidden;border-radius:22px;background:var(--world);box-shadow:0 24px 70px #0009;border:1px solid #ffffff18;isolation:isolate}.world-background{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-5;user-select:none}.scene-heading{position:absolute;left:18px;top:16px;z-index:32;pointer-events:none;text-shadow:0 2px 12px #0009}.scene-heading h1{font-size:clamp(18px,2vw,28px);margin:0;font-weight:850;letter-spacing:-.02em}.scene-heading p{margin:2px 0 0;color:#d7e0df;font-size:11px;max-width:540px}.zone{position:absolute;border:1px solid #d9ede838;border-radius:18px;background:#ffffff08;color:#d8e6e3;pointer-events:none}.zone>span{position:absolute;left:10px;top:8px;font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.1em}.hud{position:absolute;left:50%;top:14px;transform:translateX(-50%);z-index:34;background:#071016c9;border:1px solid #ffffff1f;backdrop-filter:blur(10px);border-radius:999px;padding:7px 12px;font-size:10px;color:#e8eeee;max-width:52%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.actor,.world-object{position:absolute;border:0;background:transparent;color:inherit;padding:0;cursor:pointer;transform:translate(-50%,-50%);transition:left .55s cubic-bezier(.2,.75,.25,1),top .55s cubic-bezier(.2,.75,.25,1),filter .2s,opacity .2s}.actor{z-index:16;width:82px;height:104px}.actor-figure{position:absolute;left:50%;top:42%;transform:translate(-50%,-50%);width:58px;height:76px;display:grid;place-items:center;filter:drop-shadow(0 8px 6px #0006);transition:transform .18s,filter .18s}.actor-figure img{max-width:100%;max-height:100%;display:block}.actor-aura{position:absolute;left:50%;top:42%;width:62px;height:62px;border-radius:50%;transform:translate(-50%,-50%);background:radial-gradient(circle,var(--accent)22 0 40%,transparent 70%);transition:.2s}.actor-name{position:absolute;left:50%;bottom:2px;transform:translateX(-50%);max-width:92px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;background:#0a151ccf;border:1px solid #ffffff18;border-radius:999px;padding:3px 7px;font-size:9px;font-weight:780;opacity:.88}.actor-state{display:none}.actor:hover .actor-figure,.actor:focus-visible .actor-figure,.actor.selected .actor-figure{transform:translate(-50%,-54%) scale(1.08)}.actor:focus-visible,.world-object:focus-visible{outline:none}.actor:focus-visible .actor-aura,.actor.selected .actor-aura{box-shadow:0 0 0 3px #fff9,0 0 22px var(--accent)}.actor.state-positive .actor-aura{background:radial-gradient(circle,#52b18455,transparent 70%)}.actor.state-warning .actor-aura{background:radial-gradient(circle,#dda04b66,transparent 70%)}.actor.state-danger .actor-aura{background:radial-gradient(circle,#d86f6766,transparent 70%)}.world-object{z-index:11;min-width:90px;text-align:center}.object-visual{position:relative;display:grid;place-items:center;width:78px;height:70px;margin:auto;filter:drop-shadow(0 8px 7px #0005);transition:.2s}.object-visual img{max-width:100%;max-height:100%;display:block}.object-name{display:block;margin:4px auto 0;max-width:140px;color:#f1f4ef;text-shadow:0 2px 7px #000;font-size:9px;font-weight:760;line-height:1.15}.object-values,.object-state{display:block;margin:2px auto 0;max-width:140px;color:#d4dcda;font-size:8px;line-height:1.15}.status-light{position:absolute;right:2px;top:2px;width:10px;height:10px;border-radius:50%;background:#83908f;border:2px solid #f5f5ee;box-shadow:0 0 8px #0007}.meter{display:block;height:4px;width:64px;margin:4px auto 0;border-radius:9px;background:#ffffff28;overflow:hidden}.meter i{display:block;height:100%;width:0;background:var(--good);border-radius:inherit}.world-object.unmet .meter i{background:var(--warn)}.world-object.state-positive .status-light{background:var(--good);box-shadow:0 0 10px var(--good)}.world-object.state-warning .status-light,.world-object.unmet .status-light{background:var(--warn);box-shadow:0 0 10px var(--warn)}.world-object.state-danger .status-light{background:var(--danger);box-shadow:0 0 12px var(--danger)}.world-object.selected .object-visual,.world-object:focus-visible .object-visual{filter:drop-shadow(0 8px 7px #0006) drop-shadow(0 0 10px var(--accent));transform:translateY(-3px)}.world-object.event-focus .object-visual{animation:pulse .85s ease-out 1}.display-card{background:#f7f7f4ee;color:var(--ink);border:1px solid #20303a42;border-radius:12px;padding:7px 9px;min-width:145px;box-shadow:0 7px 20px #0003}.display-card .object-name,.display-card .object-values,.display-card .object-state{color:var(--ink);text-shadow:none}.display-card .object-visual{width:50px;height:42px}.activity-object.active .object-visual{animation:activityGlow 1.4s ease-in-out infinite}.institution-object.blocked .object-visual{filter:drop-shadow(0 0 15px var(--danger))}.institution-object.ready .object-visual{filter:drop-shadow(0 0 15px var(--good))}.effect-lines{position:absolute;inset:0;width:100%;height:100%;z-index:22;pointer-events:none}.transmission-line{stroke:var(--cyan);stroke-width:2.4;stroke-dasharray:8 7;fill:none;filter:drop-shadow(0 0 5px #72d8e4aa);animation:dash .8s linear infinite}.message-bubble{position:absolute;z-index:27;transform:translate(-50%,0);max-width:210px;background:#08151bdd;color:#eef9f8;border:1px solid #78dae388;border-radius:10px;padding:6px 8px;box-shadow:0 8px 22px #0006;font-size:9px;backdrop-filter:blur(8px)}.message-bubble strong{display:block;font-size:9px}.message-bubble small{display:block;color:#93bdc1;margin:1px 0}.feedback{position:absolute;z-index:27;left:50%;bottom:76px;transform:translateX(-50%);max-width:70%;background:#0a151cdd;color:white;border:1px solid #ffffff28;border-radius:999px;padding:6px 10px;font-size:9px;box-shadow:0 6px 18px #0005}.feedback.accepted{border-color:#69d19b}.feedback.rejected,.feedback.refused,.feedback.blocked{border-color:#e18b66}.controls{position:absolute;z-index:35;left:50%;bottom:14px;transform:translateX(-50%);display:flex;align-items:center;gap:6px;width:min(720px,calc(100% - 28px));padding:7px 8px;background:#071016db;border:1px solid #ffffff20;border-radius:14px;backdrop-filter:blur(10px);box-shadow:0 8px 25px #0005}.controls button{width:34px;height:32px;border:0;border-radius:9px;background:#ffffff13;color:white;font-weight:850;cursor:pointer}.controls button:hover{background:#ffffff22}.scrub{flex:1;min-width:90px;accent-color:#77c7cf}.progress{height:4px;background:#ffffff18;border-radius:99px;width:100px;overflow:hidden}.progress i{display:block;height:100%;background:#77c7cf}.inspector{position:absolute;z-index:40;right:14px;top:64px;width:min(300px,calc(100% - 28px));max-height:calc(100% - 150px);overflow:auto;background:#0b151ce8;border:1px solid #ffffff22;border-radius:16px;box-shadow:0 20px 55px #0008;backdrop-filter:blur(14px);padding:13px;transform:translateX(calc(100% + 28px));opacity:0;pointer-events:none;transition:.2s}.inspector.open{transform:none;opacity:1;pointer-events:auto}.inspector-head{display:flex;align-items:flex-start;gap:8px}.inspector h2{margin:0;font-size:16px}.inspector-kind{color:#86a7aa;font-size:9px;text-transform:uppercase;letter-spacing:.12em}.inspector-close{margin-left:auto;border:0;background:#ffffff12;color:white;border-radius:8px;width:28px;height:28px;cursor:pointer}.inspector dl{display:grid;grid-template-columns:minmax(85px,.8fr) 1.2fr;gap:7px 10px;margin:12px 0 0;font-size:10px}.inspector dt{color:#91a3a5}.inspector dd{margin:0;color:#f1f4f1;overflow-wrap:anywhere}@keyframes dash{to{stroke-dashoffset:-15}}@keyframes pulse{0%{transform:scale(1)}45%{transform:scale(1.15)}100%{transform:scale(1)}}@keyframes activityGlow{0%,100%{filter:drop-shadow(0 0 7px #72d8e466)}50%{filter:drop-shadow(0 0 18px #72d8e4cc)}}
@media(max-width:760px){.shell{padding:0}.stage{border-radius:0;min-height:__MOBILE_MIN__px;aspect-ratio:auto;height:100vh;border:0}.scene-heading{left:12px;top:12px}.scene-heading h1{font-size:18px}.scene-heading p{display:none}.hud{top:48px;max-width:86%;font-size:9px}.actor{width:64px;height:84px}.actor-figure{width:46px;height:60px}.actor-aura{width:48px;height:48px}.actor-name{font-size:8px;max-width:72px}.world-object{min-width:72px}.object-visual{width:58px;height:52px}.object-name{font-size:8px;max-width:100px}.object-values,.object-state{font-size:7px;max-width:100px}.controls{bottom:8px;width:calc(100% - 16px);padding:6px}.controls button{width:32px;height:30px}.progress{display:none}.inspector{top:auto;right:8px;left:8px;bottom:50px;width:auto;max-height:46%;transform:translateY(calc(100% + 70px));border-radius:16px 16px 10px 10px}.inspector.open{transform:none}}
"""

_JS = r"""
const FRAMES=__FRAMES__;const PROFILE=__PROFILE__;let idx=0,playing=true,timer=null,selection=null;
function xy(el,p){if(!el||!p)return;el.style.left=p[0]+'%';el.style.top=p[1]+'%'}
function mobile(){return window.matchMedia('(max-width:760px)').matches}
function bind(view,name){return view?.bindings?.[name]}
function homePoint(cfg){return mobile()&&cfg.mobile_home?cfg.mobile_home:cfg.home}
function anchorPoint(cfg){return mobile()&&cfg.mobile_anchor?cfg.mobile_anchor:cfg.anchor}
function stateToken(state){return PROFILE.state_styles?.[state]||'neutral'}
function statePosition(cfg,view){const r=cfg.render||{},key=r.position_state_binding,state=key?bind(view,key):null,map=mobile()?(r.mobile_position_by_state||r.position_by_state):r.position_by_state;if(map&&state!=null&&Array.isArray(map[state]))return map[state];return homePoint(cfg)}
function anchorFor(op,f){if(Array.isArray(op.anchor))return op.anchor;if(op.zone)return PROFILE.zones?.[op.zone]?.anchor||null;if(op.entity){const cfg=PROFILE.entities?.[op.entity]||{};return statePosition(cfg,f.views.entities?.[op.entity])}return null}
function actorPositions(f){const out={};for(const [id,cfg] of Object.entries(PROFILE.actors))out[id]=homePoint(cfg)||[50,50];for(const [aid,av] of Object.entries(PROFILE.activities)){const row=f.views.activities?.[aid],status=bind(row,av.render?.status_binding||'status');if(status==='active'&&Array.isArray(av.participants)&&anchorPoint(av)){const a=anchorPoint(av),r=mobile()?(av.render?.mobile_gather_radius||av.render?.gather_radius||11):(av.render?.gather_radius||11);av.participants.forEach((actor,n)=>{const angle=(Math.PI*2*n/Math.max(av.participants.length,1))-Math.PI/2;out[actor]=[a[0]+Math.cos(angle)*r,a[1]+Math.sin(angle)*r]})}}for(let boundary=0;boundary<=idx;boundary++){const bf=FRAMES[boundary];for(const op of bf?.event_visual?.operations||[]){if(op.op==='actor.move_to'&&op.actor&&out[op.actor]){const p=anchorFor(op,bf);if(p)out[op.actor]=p}}}return out}
function displayName(id,f){for(const group of ['actors','entities','activities','institutions']){const view=f.views[group]?.[id],cfg=PROFILE[group]?.[id];if(view||cfg)return bind(view,'label')||cfg?.label||id}return id}
function effectPoint(id,positions,f){if(positions[id])return positions[id];if(PROFILE.entities?.[id])return statePosition(PROFILE.entities[id],f.views.entities?.[id]);if(PROFILE.activities?.[id])return anchorPoint(PROFILE.activities[id]);if(PROFILE.institutions?.[id])return anchorPoint(PROFILE.institutions[id]);return null}
function setStateClasses(el,state,unmet=false){for(const token of ['positive','warning','danger','neutral','muted'])el.classList.toggle('state-'+token,stateToken(state)===token);el.classList.toggle('unmet',!!unmet)}
function renderEffects(f,positions){const svg=document.getElementById('effectLines'),messages=document.getElementById('messageLayer'),feedback=document.getElementById('feedback');svg.innerHTML='';messages.innerHTML='';feedback.hidden=true;feedback.className='feedback';document.querySelectorAll('.event-focus').forEach(el=>el.classList.remove('event-focus'));for(const op of f.event_visual?.operations||[]){if(op.entity)document.querySelector('[data-id="'+CSS.escape(op.entity)+'"]')?.classList.add('event-focus')}for(const effect of f.presentation_effects||[]){if(effect.kind==='information_transmission'){const a=effectPoint(effect.source_id,positions,f),b=effectPoint(effect.recipient_id,positions,f);if(a&&b){const line=document.createElementNS('http://www.w3.org/2000/svg','line');for(const [k,v] of Object.entries({x1:a[0]+'%',y1:a[1]+'%',x2:b[0]+'%',y2:b[1]+'%',class:'transmission-line'}))line.setAttribute(k,v);svg.appendChild(line)}if(b){const bubble=document.createElement('div');bubble.className='message-bubble';bubble.style.left=b[0]+'%';bubble.style.top=Math.min(84,b[1]+6)+'%';const head=document.createElement('strong'),channel=document.createElement('small'),body=document.createElement('div');head.textContent=displayName(effect.source_id,f)+' → '+displayName(effect.recipient_id,f);channel.textContent=effect.channel_id||'message';body.textContent=effect.content_visible&&effect.content?effect.content:'message delivered';bubble.append(head,channel,body);messages.appendChild(bubble)}}else if(effect.kind==='action_feedback'){feedback.hidden=false;feedback.className='feedback '+effect.status;const reasons=(effect.reasons||[]).join(' · ');feedback.textContent=(effect.label||effect.status)+(reasons?' — '+reasons:'')}}}
function prettyKey(key){return key.replaceAll('_',' ').replace(/\\b\\w/g,c=>c.toUpperCase())}
function formatValue(value){if(value===null||value===undefined||value==='')return '—';if(Array.isArray(value))return value.join(', ');if(typeof value==='object')return JSON.stringify(value);return String(value)}
function appendInspectorRow(body,key,value){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=key;dd.textContent=formatValue(value);body.append(dt,dd)}
function representedDeliveries(actorId){const rows=[];for(let n=0;n<=idx;n++){for(const effect of FRAMES[n]?.presentation_effects||[]){if(effect.kind==='information_transmission'&&effect.recipient_id===actorId)rows.push(effect)}}return rows}
function showInspector(group,id){selection={group,id};document.querySelectorAll('.selected').forEach(el=>el.classList.remove('selected'));document.querySelector('[data-kind="'+group+'"][data-id="'+CSS.escape(id)+'"]')?.classList.add('selected');const f=FRAMES[idx],view=f.views[group]?.[id],cfg=PROFILE[group]?.[id]||{},bindings=view?.bindings||{};document.getElementById('inspectorKind').textContent=group.slice(0,-1);document.getElementById('inspectorTitle').textContent=bindings.label||cfg.label||id;const body=document.getElementById('inspectorBody');body.innerHTML='';const order=cfg.render?.inspector_fields||Object.keys(bindings).filter(k=>k!=='label');for(const key of order){if(!(key in bindings)||key==='label')continue;appendInspectorRow(body,prettyKey(key),bindings[key])}if(group==='actors'){const deliveries=representedDeliveries(id);appendInspectorRow(body,'Represented deliveries',deliveries.length);if(deliveries.length){const latest=deliveries[deliveries.length-1];appendInspectorRow(body,'Latest from',displayName(latest.source_id,f));if(latest.topic)appendInspectorRow(body,'Latest topic',latest.topic);appendInspectorRow(body,'Message detail',latest.content_visible&&latest.content?latest.content:'Private in this public view')}}document.getElementById('inspector').classList.add('open')}
function closeInspector(){selection=null;document.getElementById('inspector').classList.remove('open');document.querySelectorAll('.selected').forEach(el=>el.classList.remove('selected'))}
function render(i){idx=Math.max(0,Math.min(FRAMES.length-1,i));const f=FRAMES[idx],positions=actorPositions(f);for(const [id,v] of Object.entries(f.views.actors)){const el=document.querySelector('[data-actor="'+CSS.escape(id)+'"]'),cfg=PROFILE.actors[id],state=bind(v,cfg.render?.state_binding||Object.keys(v.bindings||{})[0]);xy(el,positions[id]);el.querySelector('.actor-name').textContent=bind(v,'label')||cfg.label||id;setStateClasses(el,state)}for(const [id,v] of Object.entries(f.views.entities)){const el=document.querySelector('[data-entity="'+CSS.escape(id)+'"]'),cfg=PROFILE.entities[id],r=cfg.render||{},current=bind(v,r.current_binding||'current'),required=bind(v,r.required_binding||'required'),unit=bind(v,r.unit_binding||'unit'),state=bind(v,r.state_binding||'state');xy(el,statePosition(cfg,v));el.querySelector('.object-name').textContent=bind(v,'label')||cfg.label||id;let text='';if(current!==undefined&&current!==null)text+=String(current)+(unit?' '+unit:'');if(required!==undefined&&required!==null)text+=(text?' / ':'')+'need '+required+(unit?' '+unit:'');if(state!==undefined&&state!==null)text+=(text?' · ':'')+state;el.querySelector('.object-values').textContent=text;const ratio=(typeof current==='number'&&typeof required==='number'&&required>0)?Math.max(0,Math.min(1,current/required)):null;setStateClasses(el,state,ratio!==null&&ratio<1);el.querySelector('.meter').style.display=ratio===null?'none':'';if(ratio!==null)el.querySelector('.meter i').style.width=(ratio*100)+'%';if(r.visible_binding)el.style.opacity=bind(v,r.visible_binding)?'1':'0'}for(const [id,v] of Object.entries(f.views.activities)){const el=document.querySelector('[data-activity="'+CSS.escape(id)+'"]'),cfg=PROFILE.activities[id],state=bind(v,cfg.render?.status_binding||'status');xy(el,anchorPoint(cfg));el.querySelector('.object-name').textContent=bind(v,'label')||cfg.label||id;el.querySelector('.activity-state').textContent=state??'';el.classList.toggle('active',state==='active');setStateClasses(el,state)}for(const [id,v] of Object.entries(f.views.institutions)){const el=document.querySelector('[data-institution="'+CSS.escape(id)+'"]'),cfg=PROFILE.institutions[id],r=cfg.render||{},state=bind(v,r.status_binding||'status'),support=bind(v,r.support_binding||'support'),required=bind(v,r.required_binding||'required'),conditional=bind(v,r.conditional_binding||'conditional');xy(el,anchorPoint(cfg));el.querySelector('.object-name').textContent=bind(v,'label')||cfg.label||id;el.querySelector('.institution-state').textContent=state??'';el.querySelector('.institution-counts').textContent=(support!==undefined&&support!==null)?('support '+support+(required!==undefined&&required!==null?' / '+required:'')+(conditional!==undefined&&conditional!==null?' · conditional '+conditional:'')):'';el.classList.toggle('blocked',state==='blocked');el.classList.toggle('ready',state==='ready');setStateClasses(el,state)}renderEffects(f,positions);const ev=f.event,vis=f.event_visual;document.getElementById('hud').textContent='tick '+f.tick+' · '+(ev?(vis?.label||ev.rule_id||ev.event_id):'initial state');document.getElementById('bar').style.width=((idx+1)/FRAMES.length*100)+'%';document.getElementById('scrub').value=idx;if(selection)showInspector(selection.group,selection.id)}
function schedule(){clearInterval(timer);if(playing)timer=setInterval(()=>{if(idx>=FRAMES.length-1){playing=false;document.getElementById('toggle').textContent='Play';clearInterval(timer)}else render(idx+1)},__AUTOPLAY__)}
document.querySelectorAll('[data-kind][data-id]').forEach(el=>{el.onclick=()=>showInspector(el.dataset.kind,el.dataset.id);el.onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();showInspector(el.dataset.kind,el.dataset.id)}}});document.getElementById('inspectorClose').onclick=closeInspector;document.getElementById('toggle').onclick=()=>{playing=!playing;document.getElementById('toggle').textContent=playing?'Pause':'Play';schedule()};document.getElementById('prev').onclick=()=>{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx-1)};document.getElementById('next').onclick=()=>{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx+1)};document.getElementById('restart').onclick=()=>{playing=true;document.getElementById('toggle').textContent='Pause';closeInspector();render(0);schedule()};document.getElementById('scrub').oninput=e=>{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(parseInt(e.target.value,10)||0)};const q=new URLSearchParams(location.search),start=Math.max(0,Math.min(FRAMES.length-1,parseInt(q.get('frame')||'0',10)||0));render(start);if(start>0){playing=false;document.getElementById('toggle').textContent='Play'}schedule();window.addEventListener('resize',()=>render(idx));
"""


def render_html(
    bundle: dict[str, Any],
    profile: dict[str, Any],
    profile_dir: Path,
    *,
    observer_actor_id: str | None = None,
) -> str:
    if profile.get("schema_version") != LIVING_SCENE_SCHEMA_VERSION:
        raise ValueError("composed renderer requires world-substrate-living-scene/v1")
    frames = build_living_scene_frames(bundle, profile, observer_actor_id=observer_actor_id)
    assets = {key: _asset_html(value, profile_dir) for key, value in profile["assets"].items()}
    profile_payload = deepcopy(profile)
    profile_payload["resolved_assets"] = assets
    payload = json.dumps(frames, separators=(",", ":")).replace("</", "<\\\\/")
    profile_json = json.dumps(profile_payload, separators=(",", ":")).replace("</", "<\\\\/")
    scene = profile.get("scene") or {}
    background_asset = scene.get("background_asset")
    background_uri = None
    if isinstance(background_asset, str) and background_asset in profile["assets"]:
        background_uri = _asset_uri(profile["assets"][background_asset], profile_dir)
    background_html = f"<img class='world-background' alt='' src='{background_uri}'>" if background_uri else ""
    zones = []
    for zone_id, zone in profile["zones"].items():
        if (zone.get("presentation") or {}).get("visible") is False:
            continue
        x, y, w, h = zone["rect"]
        zones.append(f"<div class='zone' data-zone='{html.escape(zone_id, quote=True)}' style='left:{x}%;top:{y}%;width:{w}%;height:{h}%;'><span>{_label(zone_id, zone)}</span></div>")
    groups = {
        name: "".join(_visual_markup(name, i, v, assets) for i, v in profile[name].items())
        for name in ("actors", "entities", "activities", "institutions")
    }
    title = html.escape(str(profile.get("title") or profile["scene_id"]))
    subtitle = html.escape(str(profile.get("subtitle") or ""))
    css = (_CSS
        .replace("__SHELL__", html.escape(str(scene.get("shell_background") or "#0b1217"), quote=True))
        .replace("__WORLD__", html.escape(str(scene.get("background") or "#18242a"), quote=True))
        .replace("__ASPECT__", html.escape(str(scene.get("aspect_ratio") or "16 / 9"), quote=True))
        .replace("__MOBILE_MIN__", str(max(560, int(scene.get("mobile_min_height") or 720)))))
    js = (_JS.replace("__FRAMES__", payload).replace("__PROFILE__", profile_json)
        .replace("__AUTOPLAY__", str(max(250, int(scene.get("autoplay_ms") or 1600)))))
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>{css}</style></head><body><main class='shell'><section class='stage' id='stage'>{background_html}<div class='scene-heading'><h1>{title}</h1><p>{subtitle}</p></div>{''.join(zones)}<div id='hud' class='hud'></div><svg id='effectLines' class='effect-lines'></svg><div id='messageLayer'></div><div id='feedback' class='feedback' hidden></div>{groups['entities']}{groups['activities']}{groups['institutions']}{groups['actors']}<aside id='inspector' class='inspector' aria-live='polite'><div class='inspector-head'><div><div id='inspectorKind' class='inspector-kind'></div><h2 id='inspectorTitle'></h2></div><button id='inspectorClose' class='inspector-close' aria-label='Close inspector'>×</button></div><dl id='inspectorBody'></dl></aside><div class='controls'><button id='restart' aria-label='Restart'>↺</button><button id='prev' aria-label='Previous event'>←</button><button id='toggle'>Pause</button><button id='next' aria-label='Next event'>→</button><input id='scrub' class='scrub' type='range' min='0' max='{len(frames)-1}' value='0' aria-label='canonical event boundary'><div class='progress'><i id='bar'></i></div></div></section></main><script>{js}</script></body></html>"""


def render_file(projection_path: Path, profile_path: Path, output_path: Path, *, observer_actor_id: str | None = None) -> None:
    profile = load_scene_contract(profile_path)
    bundle = load_live_projection_bundle(projection_path)
    output_path.write_text(render_html(bundle, profile, profile_path.parent, observer_actor_id=observer_actor_id))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projection", type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--observer", default=None)
    args = parser.parse_args()
    render_file(args.projection, args.profile, args.output, observer_actor_id=args.observer)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
