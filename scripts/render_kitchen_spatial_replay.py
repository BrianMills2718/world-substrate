#!/usr/bin/env python3
"""Render a retained kitchen trace as a graphical, spatial replay.

The kitchen geometry is an illustrative presentation layout, not canonical
world state. Actions, item preparation, ownership, order progress, reasoning,
contention, handoff, and terminal state come from the retained v3 trace.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from render_kitchen_service import action_label, load_trace, reconstruct_turns

REPO = Path(__file__).resolve().parents[1]
ITEM_ICONS = {"carrot": "🥕", "onion": "🧅", "potato": "🥔", "knife": "🔪"}


def _kind(item: str) -> str:
    return item.split("-", 1)[0]


def build_frames(trace: dict[str, Any]) -> list[dict[str, Any]]:
    actors = list(trace["actors"])
    turn_views = reconstruct_turns(trace)
    item_state: dict[str, dict[str, Any]] = {
        "carrot-1": {"prep": "raw", "plated_to": None},
        "potato-1": {"prep": "raw", "plated_to": None},
        "onion-1": {"prep": "raw", "plated_to": None},
        "onion-2": {"prep": "raw", "plated_to": None},
    }
    frames: list[dict[str, Any]] = []

    for raw, view in zip(trace["transcript"], turn_views, strict=True):
        for actor in [raw["committed_first"], *[a for a in actors if a != raw["committed_first"]]]:
            record = raw["actors"].get(actor) or {}
            action = record.get("did")
            if record.get("status") != "accepted" or not isinstance(action, dict):
                continue
            item = action.get("item")
            if not isinstance(item, str) or item == "knife":
                continue
            state = item_state.setdefault(item, {"prep": "raw", "plated_to": None})
            if action.get("kind") == "chop":
                state["prep"] = "chopped"
            elif action.get("kind") == "cook":
                state["prep"] = "cooked"
            elif action.get("kind") == "plate":
                state["prep"] = "plated"
                state["plated_to"] = action.get("order")

        actor_rows: dict[str, Any] = {}
        for actor in actors:
            record = raw["actors"].get(actor) or {}
            action = record.get("did") or record.get("wanted")
            actor_rows[actor] = {
                "status": record.get("status"),
                "action": action_label(action),
                "reasoning": record.get("said_on_retry") or record.get("said") or "",
                "retried": bool(record.get("retried")),
                "did": record.get("did"),
            }

        frames.append(
            {
                "turn": view.turn,
                "actors": actor_rows,
                "holdings": {a: list(view.holdings[a]) for a in actors},
                "knife_owner": view.knife_owner,
                "moments": list(view.moments),
                "progress": view.progress,
                "items": json.loads(json.dumps(item_state)),
            }
        )
    return frames


def render_html(trace: dict[str, Any]) -> str:
    frames = build_frames(trace)
    actors = list(trace["actors"])
    payload = json.dumps(frames, separators=(",", ":")).replace("</", "<\\/")
    model = str(trace.get("model") or "unknown")
    cost = float(trace.get("cost_usd") or 0)
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Kitchen spatial replay — two cooks, one knife</title>
<style>
:root{{--ink:#182126;--muted:#617079;--paper:#efe7d7;--wood:#a96f42;--wood2:#c58a55;--tile:#d8cdb9;--line:#47382c;--ama:#5f7fdb;--bo:#d96b5f;--good:#5da46d;--warn:#f0b448}}
*{{box-sizing:border-box}} body{{margin:0;background:#171b1d;color:var(--ink);font:15px/1.35 system-ui,-apple-system,sans-serif;overflow-x:hidden}}
.shell{{max-width:1240px;margin:auto;padding:18px}} .top{{color:white;display:flex;justify-content:space-between;align-items:end;gap:18px;margin-bottom:12px}}
h1{{font-size:clamp(24px,3vw,42px);margin:0;letter-spacing:-.03em}} .sub{{color:#b8c1c5;max-width:650px;margin:4px 0 0}} .badge{{font-size:12px;color:#dbe2e5}}
.stage{{position:relative;aspect-ratio:16/9;border:4px solid #090b0c;border-radius:18px;overflow:hidden;background:var(--tile);box-shadow:0 20px 60px #0008}}
.floor{{position:absolute;inset:0;background:linear-gradient(90deg,#0000 49%,#bcae9655 50%,#0000 51%),linear-gradient(#0000 49%,#bcae9655 50%,#0000 51%);background-size:64px 64px}}
.wall{{position:absolute;left:0;right:0;top:0;height:17%;background:#d8b988;border-bottom:5px solid #8d6846}}
.station{{position:absolute;background:var(--wood);border:4px solid var(--line);border-radius:10px;box-shadow:inset 0 0 0 5px #ffffff18,0 5px 0 #6f482c}}
#island{{left:31%;top:38%;width:38%;height:25%}} #pantry{{left:39%;top:17%;width:22%;height:12%;background:#b9875b}}
#burners{{left:33%;top:4%;width:34%;height:12%;background:#565b5d;border-color:#282c2e;display:flex;justify-content:space-around;align-items:center;padding:8px 14px}}
.burner{{width:70px;height:52px;border-radius:50%;background:#222;border:5px solid #777;position:relative}} .burner.hot::after{{content:'🔥';position:absolute;font-size:30px;left:15px;top:5px;filter:drop-shadow(0 2px 2px #000)}}
.order{{position:absolute;bottom:4%;width:22%;height:21%;background:#e9dfc9;border:4px solid #79634c;border-radius:14px;padding:8px;text-align:center}} #order-ama{{left:4%}} #order-bo{{right:4%}}
.order h3{{margin:0 0 4px;font-size:14px;text-transform:uppercase;letter-spacing:.08em}} .plate{{height:58px;border:4px solid #c8c4b8;background:#f8f6ee;border-radius:50%;margin:4px auto;width:110px;display:flex;justify-content:center;align-items:center;gap:2px;font-size:28px}} .needs{{font-size:11px;color:#6b6258}}
.actor{{position:absolute;width:92px;height:110px;transition:left .65s ease,top .65s ease;z-index:8;text-align:center}} .chef{{width:62px;height:62px;margin:auto;border-radius:50%;border:4px solid #24292c;background:white;display:flex;align-items:center;justify-content:center;font-size:34px;box-shadow:0 5px 0 #0003}} .actor.ama .chef{{outline:6px solid var(--ama)}} .actor.bo .chef{{outline:6px solid var(--bo)}} .name{{background:#16191be8;color:white;border-radius:9px;margin:6px auto 0;padding:3px 8px;width:max-content;font-weight:800;text-transform:capitalize}}
.thought{{position:absolute;z-index:12;width:min(310px,34vw);background:#fffffff2;border:3px solid #30383c;border-radius:14px;padding:9px 11px;box-shadow:0 8px 22px #0004;font-size:13px;transition:opacity .25s}} .thought strong{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#657078;margin-bottom:3px}} #thought-ama{{left:2%;top:18%}} #thought-bo{{right:2%;top:18%}}
.item{{position:absolute;z-index:7;font-size:34px;transition:left .6s ease,top .6s ease,transform .3s ease;filter:drop-shadow(0 4px 2px #0004)}} .item small{{position:absolute;left:50%;top:34px;transform:translateX(-50%);background:#fffddd;border:1px solid #695a44;border-radius:6px;padding:1px 4px;font-size:9px;white-space:nowrap}} .item.chopped{{transform:scale(.85) rotate(-8deg)}} .item.cooked{{filter:drop-shadow(0 4px 2px #0004) saturate(.65) brightness(.85)}}
.knife{{font-size:40px}}
.hud{{position:absolute;left:50%;top:18%;transform:translateX(-50%);z-index:20;background:#15191de8;color:white;border-radius:12px;padding:7px 12px;text-align:center;min-width:190px}} .turn{{font-size:22px;font-weight:900}} .moment{{display:inline-block;margin-top:4px;background:var(--warn);color:#251b0b;border-radius:999px;padding:2px 8px;font-size:10px;font-weight:900;text-transform:uppercase}} .terminal{{background:var(--good);color:white}}
.action{{position:absolute;left:50%;bottom:2%;transform:translateX(-50%);z-index:20;background:#111d;color:white;border-radius:999px;padding:8px 15px;font-size:12px;white-space:nowrap}}
.controls{{display:flex;gap:10px;align-items:center;margin-top:12px;color:white}} button{{background:#f1eadc;border:0;border-radius:10px;padding:9px 13px;font-weight:800;cursor:pointer}} .bar{{height:8px;background:#ffffff24;border-radius:99px;flex:1;overflow:hidden}} .bar>i{{display:block;height:100%;background:#f0b448;width:0;transition:width .25s}}
.note{{color:#aeb8bd;font-size:12px;margin-top:8px}} @media(max-width:800px){{.thought{{font-size:11px;width:38vw}} .actor{{transform:scale(.82);transform-origin:center}} .item{{font-size:28px}}}}
</style></head><body><div class='shell'>
<div class='top'><div><h1>Kitchen replay: two cooks, one knife</h1><p class='sub'>A graphical replay of the retained service. The kitchen geometry is illustrative; actions, ownership, preparation state, order progress, and reasoning come from the recorded trace.</p></div><div class='badge'>{model} · ${cost:.5f}</div></div>
<div class='stage' id='stage'><div class='floor'></div><div class='wall'></div>
<div class='station' id='burners'><div class='burner' id='burner-1'></div><div class='burner' id='burner-2'></div></div><div class='station' id='pantry'></div><div class='station' id='island'></div>
<div class='order' id='order-ama'><h3>Ama · stew</h3><div class='plate' id='plate-ama'></div><div class='needs' id='needs-ama'></div></div><div class='order' id='order-bo'><h3>Bo · hash</h3><div class='plate' id='plate-bo'></div><div class='needs' id='needs-bo'></div></div>
<div class='actor ama' id='actor-ama'><div class='chef'>👩‍🍳</div><div class='name'>Ama</div></div><div class='actor bo' id='actor-bo'><div class='chef'>👨‍🍳</div><div class='name'>Bo</div></div>
<div class='thought' id='thought-ama'></div><div class='thought' id='thought-bo'></div><div class='hud'><div class='turn' id='turn'></div><div id='moments'></div></div><div class='action' id='action'></div>
<div class='item knife' id='item-knife'>🔪</div><div class='item' id='item-carrot-1'>🥕<small>carrot</small></div><div class='item' id='item-potato-1'>🥔<small>potato</small></div><div class='item' id='item-onion-1'>🧅<small>onion 1</small></div><div class='item' id='item-onion-2'>🧅<small>onion 2</small></div>
</div>
<div class='controls'><button id='restart'>↺ Replay</button><button id='prev'>←</button><button id='toggle'>Pause</button><button id='next'>→</button><div class='bar'><i id='progressbar'></i></div></div><div class='note'>Autoplays every 2.3 seconds. The main event is t10 → t11: Bo releases the knife for Ama, then Ama takes it and finishes the service.</div></div>
<script>const FRAMES={payload}; const ACTORS={json.dumps(actors)};
const POS={{ama:{{home:[13,53],prep:[27,43],cook:[30,17],plate:[17,70]}},bo:{{home:[79,53],prep:[67,43],cook:[63,17],plate:[80,70]}}}};
const PANTRY={{'carrot-1':[43,23],'potato-1':[54,23],'onion-1':[47,23],'onion-2':[50,23]}}; let idx=0,timer=null,playing=true;
function iconFor(name){{return name.startsWith('carrot')?'🥕':name.startsWith('potato')?'🥔':name.startsWith('onion')?'🧅':'•'}}
function itemPos(item,f){{if(item==='knife'){{if(f.knife_owner){{const a=f.knife_owner,b=actorTarget(a,f.actors[a]);return [b[0]+(a==='ama'?4:-1),b[1]+6]}}return [49,48]}} const s=f.items[item]||{{}}; if(s.plated_to==='order-stew')return [14+(item.endsWith('2')?4:0),77]; if(s.plated_to==='order-hash')return [77+(item.endsWith('2')?4:0),77]; for(const a of ACTORS){{const held=f.holdings[a]||[];const n=held.indexOf(item);if(n>=0){{const b=actorTarget(a,f.actors[a]);const food=held.filter(x=>x!=='knife');const j=food.indexOf(item);return [b[0]+(a==='ama'?-6:7),b[1]+3+j*6]}}}} return PANTRY[item]||[49,24]}}
function actorTarget(actor,rec){{const did=rec.did||{{}};const k=did.kind||'';if(rec.status==='no_action')return POS[actor].home;if(k==='cook')return POS[actor].cook;if(k==='plate')return POS[actor].plate;if(k==='take'||k==='chop'||k==='put_down')return POS[actor].prep;return POS[actor].home}}
function setXY(el,p){{el.style.left=p[0]+'%';el.style.top=p[1]+'%'}}
function render(i){{idx=Math.max(0,Math.min(FRAMES.length-1,i));const f=FRAMES[idx];document.getElementById('turn').textContent='Turn '+f.turn+' / '+FRAMES.length;document.getElementById('progressbar').style.width=((idx+1)/FRAMES.length*100)+'%';
 for(const a of ACTORS){{const rec=f.actors[a];setXY(document.getElementById('actor-'+a),actorTarget(a,rec));const th=document.getElementById('thought-'+a);th.innerHTML='<strong>'+a+' · '+rec.action+'</strong>'+rec.reasoning;}}
 for(const item of ['knife','carrot-1','potato-1','onion-1','onion-2']){{const el=document.getElementById('item-'+item);setXY(el,itemPos(item,f));const s=f.items[item]||{{}};el.classList.toggle('chopped',s.prep==='chopped');el.classList.toggle('cooked',s.prep==='cooked');}}
 for(const a of ACTORS){{const p=f.progress[a]||{{}};document.getElementById('plate-'+a).innerHTML=(p.plated||[]).map(iconFor).join('');document.getElementById('needs-'+a).textContent=p.filled?'✓ order complete':'still needs: '+((p.still_wants||[]).join(', ')||'nothing');}}
 document.querySelectorAll('.burner').forEach(x=>x.classList.remove('hot'));for(const a of ACTORS){{const d=f.actors[a].did||{{}};if(d.kind==='cook'&&d.burner)document.getElementById(d.burner)?.classList.add('hot')}}
 const labels={{contention:'⚡ knife contention',handoff:'🤝 knife released for Ama',takeover:'🔪 Ama takes the knife',terminal:'✓ service complete'}};document.getElementById('moments').innerHTML=f.moments.map(m=>'<span class="moment '+(m==='terminal'?'terminal':'')+'">'+labels[m]+'</span>').join('');
 const acts=ACTORS.map(a=>a+': '+f.actors[a].action).join('  ·  ');document.getElementById('action').textContent=acts;}}
function schedule(){{clearInterval(timer);if(playing)timer=setInterval(()=>{{if(idx>=FRAMES.length-1){{playing=false;document.getElementById('toggle').textContent='Play';clearInterval(timer)}}else render(idx+1)}},2300)}}
document.getElementById('toggle').onclick=()=>{{playing=!playing;document.getElementById('toggle').textContent=playing?'Pause':'Play';schedule()}};document.getElementById('prev').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx-1)}};document.getElementById('next').onclick=()=>{{playing=false;document.getElementById('toggle').textContent='Play';schedule();render(idx+1)}};document.getElementById('restart').onclick=()=>{{playing=true;document.getElementById('toggle').textContent='Pause';render(0);schedule()}};
const q=new URLSearchParams(location.search);const start=Math.max(0,Math.min(FRAMES.length-1,(parseInt(q.get('turn')||'1',10)||1)-1));render(start);if(start>0){{playing=false;document.getElementById('toggle').textContent='Play'}}schedule();
</script></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    trace = load_trace(args.input)
    args.output.write_text(render_html(trace))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
