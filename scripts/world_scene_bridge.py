"""Read-only adapter from authored worlds/retained rounds to the existing scene.

The screen arrangement is presentation, never a source of simulated distance,
motion, collision, ownership, or causal state. No model or engine is executed.
"""
from __future__ import annotations

from copy import deepcopy
import math
from pathlib import Path
import re
from typing import Any

from scripts.render_composed_living_scene import render_html
from world_substrate.living_scene import LIVING_SCENE_SCHEMA_VERSION
from world_substrate.action_authoring import _selector_matches
from world_substrate.model import Entity

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'reference_worlds/waltzman/assets-v2'
PORTRAITS = ('resident-ari.svg', 'resident-mara.svg', 'resident-idris.svg',
             'resident-nira.svg', 'resident-selene.svg', 'resident-tomas.svg')
SEMANTICS = ('Schematic world view: place membership and ownership follow retained canonical state. '
             'Screen positions, portrait art, spacing and transitions are illustrative; '
             'they do not establish physical distance, speed or collisions.')


def _retained_events(rounds: list) -> tuple[list[dict], dict[str, Any], list[str]]:
    events, event_rounds, limitations = [], {}, []
    seen: dict[str, list] = {}
    for index, row in enumerate(rounds):
        turn = row.get('turn', index + 1)
        found: list[dict] = []

        def visit(value: Any) -> None:
            if isinstance(value, list):
                for item in value:
                    visit(item)
            elif isinstance(value, dict):
                if isinstance(value.get('changes'), list) and (value.get('event_id') or value.get('status') or value.get('rule_id')):
                    found.append(value)
                # Only recorded event containers, never cognition/attempt text.
                for key in ('world_events', 'actors', 'reactions', 'ruling_events', 'settled', 'events', 'ruling', 'judge', 'disposition'):
                    child = value.get(key)
                    if key == 'actors' and isinstance(child, dict):
                        for actor in child.values():
                            visit(actor)
                    else:
                        visit(child)

        visit(row)
        # Native IDs explicitly encode commit order; transcript actor maps do not.
        def order(item: tuple[int, dict]) -> tuple[int, int, int]:
            n, event = item
            match = re.fullmatch(r'(?:r(\d+)-)?e(\d+)', str(event.get('event_id', '')))
            return (int(match[1] or turn), int(match[2]), n) if match else (int(turn), 10**9, n)

        for n, event in sorted(enumerate(found), key=order):
            event_id = event.get('event_id') or f'round-{turn}-event-{n}'
            if event_id in seen:
                if seen[event_id] != event['changes']:
                    raise ValueError(f'Conflicting retained changes for event {event_id}')
                continue
            seen[event_id] = event['changes']
            if not event.get('event_id'):
                limitations.append('Some legacy events have presentation IDs; their exact native commit order was not retained.')
            clean = {key: deepcopy(event[key]) for key in ('rule_id', 'rule_version', 'status', 'tick', 'world_revision', 'causal_bearer', 'causal_parent_event_ids', 'changes') if key in event}
            clean['event_id'] = event_id
            events.append(clean)
            event_rounds[event_id] = turn
    return events, event_rounds, list(dict.fromkeys(limitations))


def build_scene_inputs(world: dict, rounds: list, *, run_id: str | None = None) -> tuple[dict, dict, list[str]]:
    """Build inspectable v1 profile + projection using the authored initial values."""
    bundle = world.get('bundle', world)
    spec = bundle.get('world') or {}
    rows = bundle.get('entities')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Original authored world entities are unavailable for this retained run')
    if not isinstance(spec.get('id'), str):
        raise ValueError('Original authored world identity is unavailable')
    events, event_rounds, limitations = _retained_events(rounds)
    # Same authored-to-material field mapping used by run_authored_world.build_engine,
    # without compiling laws, creating controllers, or executing an engine.
    defaults = {c['name']:{f['name']:deepcopy(f['default']) for f in c.get('fields',[]) if 'default' in f} for c in bundle.get('components',[])}
    entities = {}
    for row in rows:
        entity = {'entity_id': row['id'], 'label': row.get('label', row['id']),
                  'category_ids': deepcopy(row.get('categories', [])),
                  'components': {name:{**deepcopy(defaults.get(name,{})),**deepcopy(values)} for name,values in (row.get('components') or {}).items()}}
        location = row.get('location') or spec.get('location')
        if location:
            entity['location'] = {'location_id': location}
        if row.get('owner_ref') is not None:
            entity['ownership'] = {'owner_ref': row['owner_ref']}
        if row.get('portable') is not None:
            entity['portable'] = {'portable': bool(row['portable'])}
        entities[row['id']] = entity
    world_id = spec['id'] + '-live'
    projection = {'schema_version':'world-substrate-live-projection/v0',
                  'branch_id':run_id or 'retained', 'world_id':world_id,
                  'initial_snapshot':{'schema_version':'world-substrate-snapshot/v1',
                                      'world':{'world_id':world_id, 'revision':0, 'tick':0, 'entities':entities}},
                  'events':events}
    places = [row for row in rows if 'place' in row.get('categories', [])]
    profile = {'schema_version':LIVING_SCENE_SCHEMA_VERSION, 'scene_id':spec['id']+'-composed',
               'world':world_id, 'title':spec.get('label',spec['id']), 'subtitle':'Recorded world · layout and artwork are illustrative.',
               'scene':{'background':'#263840','shell_background':'#101b24', 'mobile_min_height':max(720, len(rows)*48)},
               'assets':{'object':{'kind':'image','path':'package.svg'}},
               'zones':{}, 'actors':{}, 'entities':{}, 'activities':{}, 'institutions':{},
               'event_visuals':{}, 'state_styles':{},
               'presentation':{'event_rounds':event_rounds, 'spatial_semantics':SEMANTICS}}
    anchors = {}
    columns = min(3, max(1,len(places)))
    lines = max(1, math.ceil(len(places)/columns))
    for i, row in enumerate(places):
        x, y, w, h = 3+(i%columns)*94/columns, 17+(i//columns)*76/lines, 91/columns, 72/lines
        point = [x+w/2, y+h/2]
        profile['zones'][row['id']] = {'label':row.get('label',row['id']), 'rect':[x,y,w,h], 'anchor':point, 'mobile_rect':[3,17+i*76/max(1,len(places)),94,72/max(1,len(places))], 'mobile_anchor':[50,17+(i+.5)*76/max(1,len(places))]}
        anchors[row['id']] = point
    # The runner selects agents by mechanics, not by a mandatory category name.
    # A generated orchard worker is an actor even when its category is 'worker'.
    selectors = [m['actor_selector'] for m in (world.get('causal_model') or {}).get('mechanics', []) if isinstance(m.get('actor_selector'), dict)]
    actors = [r for r in rows if 'actor' in r.get('categories', []) or any(
        _selector_matches(Entity(entity_id=r['id'], label=r.get('label',r['id']), category_ids=tuple(r.get('categories',[])), components=entities[r['id']]['components']), selector) for selector in selectors)]
    objects = [r for r in rows if r not in actors and r not in places]
    profile['scene']['mobile_min_height'] = max(720, (math.ceil(len(objects)/3)+math.ceil(len(actors)/3)+2)*110)
    if not places:
        profile['zones']['schematic'] = {'label':'Schematic world', 'rect':[3,16,94,78], 'anchor':[50,50]}
        limitations.append('This world has no authored place entities; the view is a schematic arrangement of its actors and state-bearing entities.')
    # Spread each location's inhabitants within its illustrative region. Offsets
    # are stable per entity, not inferred physical coordinates.
    if places:
        max_rows = max(1,math.ceil((len(actors)+len(objects))/3))
        profile['scene']['mobile_min_height'] = max(profile['scene']['mobile_min_height'], math.ceil(len(places)*max_rows*110/.76))
    for actor_index, row in enumerate(actors+objects):
        is_actor = row in actors
        group = 'actors' if is_actor else 'entities'
        entity_id = row['id']
        group_rows = actors if is_actor else objects
        local = group_rows.index(row)
        cols = min(5, max(1,len(group_rows)))
        nrows = max(1,math.ceil(len(group_rows)/cols))
        home = [(50 if cols==1 else 12+(local%cols)*76/(cols-1)), (28 if is_actor else (58 if actors else 28))+(local//cols)*((20 if is_actor else (28 if actors else 56))/max(1,nrows-1))]
        mobile_cols = min(3,max(1,len(group_rows)))
        mobile_rows = max(1,math.ceil(len(group_rows)/mobile_cols))
        mobile_home = [(50 if mobile_cols==1 else 17+(local%mobile_cols)*66/(mobile_cols-1)), (23 if is_actor else (48 if actors else 23))+(local//mobile_cols)*((18 if is_actor else (38 if actors else 63))/max(1,mobile_rows-1))]
        mobile_positions = {}
        if places:
            loc = row.get('location') or spec.get('location') or ''
            rank = actor_index
            slots = max(1,math.ceil((len(actors)+len(objects))/3))
            positions = {key:[zone['anchor'][0]+(rank%3-1)*min(14,28/columns),zone['rect'][1]+14+(rank//3)*(zone['rect'][3]-24)/max(1,slots-1)] for key,zone in profile['zones'].items()}
            mobile_positions = {key:[zone['mobile_anchor'][0]+(rank%3-1)*25, zone['mobile_rect'][1]+9+(rank//3)*(zone['mobile_rect'][3]-15)/max(1,slots-1)] for key,zone in profile['zones'].items()}
            home = positions.get(loc, home)
            mobile_home = mobile_positions.get(loc,mobile_home)
        else:
            positions = {}
        bindings = {'location':'location.location_id', 'owner':'ownership.owner_ref'}
        for name, component in entities[entity_id]['components'].items():
            # Information content and logs have their own visibility-aware views.
            if name in {'information', 'report_log'}:
                continue
            for field, value in component.items():
                if value is None or isinstance(value,(str,int,float,bool)):
                    bindings[name+'_'+field] = f'components.{name}.{field}'
        render = {'position_state_binding':'location', 'position_by_state':positions, 'mobile_position_by_state':mobile_positions,
                  'owner_binding':'owner', 'accent':'#8ac5eb'}
        for field in ('status', 'state', 'validation', 'value', 'ready', 'hold'):
            candidates = [key for key,path in bindings.items() if path.startswith('components.') and path.endswith('.'+field)]
            if candidates:
                render['state_binding'] = candidates[0]
                break
        for field in ('current', 'required', 'unit'):
            candidates = [key for key,path in bindings.items() if path.endswith('.'+field)]
            if candidates:
                render[field+'_binding'] = candidates[0]
        asset = 'object'
        art_by_component = {'validation_decision':'validation.svg','condition':'safeguard.svg','technical_condition':'safeguard.svg','resource':'reserve.svg','authority':'staff.svg','position':'coalition.svg','decision_position':'coalition.svg','boundary':'safeguard.svg'}
        for name in entities[entity_id]['components']:
            if name in art_by_component:
                asset = name+'-art'
                profile['assets'][asset] = {'kind':'image','path':art_by_component[name]}
                break
        if is_actor:
            asset = 'portrait-'+str(actor_index%len(PORTRAITS))
            profile['assets'][asset] = {'kind':'image','path':PORTRAITS[actor_index%len(PORTRAITS)]}
        profile[group][entity_id] = {'entity':entity_id, 'label':row.get('label',entity_id),
                                      'asset':asset, 'home':home, 'mobile_home':mobile_home, 'bindings':bindings, 'render':render}
    limitations.append('Generic reusable artwork does not claim to depict an entity’s actual appearance. Select an entity to inspect its retained state.')
    return projection, profile, limitations


def render_world_scene(world: dict, rounds: list, *, run_id: str | None = None, driven: bool = True) -> dict:
    projection, profile, limitations = build_scene_inputs(world, rounds, run_id=run_id)
    return {'html':render_html(projection,profile,ART,driven=driven),
            'spatial_semantics':SEMANTICS, 'limitations':limitations}
