"""Where each actor stands in a Living Scene frame: one rule for every renderer.

Both living-scene renderers (``scripts/render_living_scene.py`` and
``scripts/render_composed_living_scene.py``) embed ``ACTOR_POSITIONS_JS`` and call
``wsActorPositions`` instead of keeping their own copy. Before 2026-10-06 each had
its own copy and they disagreed (system model gap G10): one applied only the
current frame's ``actor.move_to``, so an actor jumped back home on the next frame;
the other replayed every earlier move but let it override an active activity's
gathering ring.

The rule, applied for frame ``i``:

1. start every actor at its home point;
2. replay ``actor.move_to`` from every earlier frame (an actor stays where it last went);
3. gather the participants of every activity active in frame ``i`` on a ring
   around the activity (radius ``render.gather_radius``, default 11);
4. apply frame ``i``'s own ``actor.move_to`` (the move happening now wins);
5. spread actors that share an identical point on a ring around it, in actor-id
   order (issue #106), radius from the profile's ``render.gather_radius`` or 11.
   A single actor keeps the exact point.

Presentation only: nothing here reads or changes canonical state.
"""

from __future__ import annotations

ACTOR_POSITIONS_JS = r"""
function wsRing(c,ids,r,out){ids.forEach((a,n)=>{const angle=(Math.PI*2*n/Math.max(ids.length,1))-Math.PI/2;out[a]=[c[0]+Math.cos(angle)*r,c[1]+Math.sin(angle)*r]})}
function wsActorPositions(frames,i,profile,h){const out={};for(const [id,cfg] of Object.entries(profile.actors||{}))out[id]=h.home(cfg)||[50,50];const moves=fr=>{for(const op of fr?.event_visual?.operations||[]){if(op.op==='actor.move_to'&&op.actor&&out[op.actor]){const p=h.anchorFor(op,fr);if(p)out[op.actor]=[p[0],p[1]]}}};for(let b=0;b<i;b++)moves(frames[b]);const f=frames[i];for(const [aid,av] of Object.entries(profile.activities||{})){const row=f?.views?.activities?.[aid],status=row?.bindings?.[av.render?.status_binding||'status'],a=h.anchor(av);if(status==='active'&&Array.isArray(av.participants)&&a)wsRing(a,av.participants,h.radius(av.render||{}),out)}moves(f);const groups={};for(const id of Object.keys(out).sort()){const p=out[id],key=p[0].toFixed(3)+','+p[1].toFixed(3);(groups[key]=groups[key]||{p,ids:[]}).ids.push(id)}for(const g of Object.values(groups)){if(g.ids.length>1)wsRing(g.p,g.ids,h.radius(profile.render||{}),out)}return out}
function wsOccupied(positions,p){if(!p)return false;return Object.values(positions).some(q=>Math.abs(q[0]-p[0])<0.5&&Math.abs(q[1]-p[1])<0.5)}
"""
