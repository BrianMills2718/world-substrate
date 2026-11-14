"""Retained worlds use composed scenes without executing the simulation."""
from copy import deepcopy
import json
from pathlib import Path
import pytest
import shutil
import subprocess

from scripts.world_scene_bridge import build_scene_inputs, render_world_scene
from world_substrate.living_scene import build_living_scene_frames, load_scene_contract

ROOT = Path(__file__).resolve().parents[1]


def test_initial_scene_is_self_contained_and_parent_driven(tmp_path):
    world = json.loads((ROOT / 'tests/fixtures/airfield-s1-live.json').read_text())
    before = deepcopy(world)
    result = render_world_scene(world, [], run_id='retained')
    assert world == before
    for marker in ('data:image/svg+xml;base64,', 'ws-scene-event', 'ws-scene-select', 'ws-scene-ready', 'const DRIVEN=true', "data-actor='sam'"):
        assert marker in result['html']
    assert 'schematic' in result['spatial_semantics'].lower()
    _, profile, _ = build_scene_inputs(world, [])
    path = tmp_path / 'scene.json'
    path.write_text(json.dumps(profile))
    assert load_scene_contract(path) == profile


def test_canonical_location_and_ownership_survive_projection():
    world = json.loads((ROOT / 'tests/fixtures/airfield-s1-live.json').read_text())
    world['bundle']['entities'].append({'id':'tool','label':'Tool','categories':['object'], 'location':'office', 'owner_ref':'actor:sam', 'components':{}})
    rounds = [{'turn':1,'actors':{'sam':{'event_id':'r1-e00001','status':'accepted','changes':[{'path':'entities.sam.location.location_id','before':'office','after':'hangar'}]}}}]
    projection, profile, _ = build_scene_inputs(world, rounds, run_id='retained')
    frames = build_living_scene_frames(projection, profile)
    assert frames[0]['views']['actors']['sam']['bindings']['location'] == 'office'
    assert frames[1]['views']['actors']['sam']['bindings']['location'] == 'hangar'
    assert frames[1]['views']['entities']['tool']['bindings']['owner'] == 'actor:sam'
    assert profile['actors']['sam']['render']['position_by_state']['office'] != profile['actors']['sam']['render']['position_by_state']['hangar']
    assert profile['entities']['tool']['render']['owner_binding'] == 'owner'


def test_retained_pump_exact_reaction_boundaries():
    saved = json.loads((ROOT / 'evidence/i0-i1/visible-run-20261113/share.json').read_text())
    before = deepcopy(saved)
    projection, profile, _ = build_scene_inputs(saved['world'], saved['rounds'])
    frames = build_living_scene_frames(projection, profile)
    assert saved == before
    by_id = {f['event']['event_id']:f for f in frames[1:]}
    ids = list(by_id)
    assert ids.index('r3-e00001') + 1 == ids.index('r3-e00002')
    binding = next(k for k,v in profile['entities']['pump-activation']['bindings'].items() if v == 'components.validation_decision.validation')
    assert by_id['r3-e00001']['views']['entities']['pump-activation']['bindings'][binding] == 'failed'
    assert by_id['r3-e00002']['views']['entities']['pump-activation']['bindings'][binding] == 'passed'


def test_nested_settlements_and_rulings_not_lost_or_duplicated():
    world = {'bundle':{'world':{'id':'example','label':'Example','location':'space'},'entities':[{'id':'a','label':'A','categories':['actor'],'components':{'status':{'value':0}}}]}}
    event = {'event_id':'r1-e00002','changes':[{'path':'entities.a.components.status.value','before':0,'after':2}]}
    rounds = [{'turn':1,'actors':{'a':{'event_id':'r1-e00001','changes':[]}},'settled':{'reactions':[event]},'ruling_events':[event]}]
    projection, profile, _ = build_scene_inputs(world, rounds)
    assert [e['event_id'] for e in projection['events']] == ['r1-e00001','r1-e00002']
    assert build_living_scene_frames(projection,profile)[-1]['views']['actors']['a']['bindings']['status_value'] == 2


def test_authored_labels_cannot_escape_script_or_markup():
    label = '</script><script>globalThis.injected=true</script><img src=x onerror=alert(1)>__PROFILE____AUTOPLAY__'
    world = {'bundle':{'world':{'id':'hostile','label':label},'entities':[{'id':'a','label':label,'categories':['actor'],'components':{}}]}}
    result = render_world_scene(world, [])
    assert label not in result['html']
    assert result['html'].count('</script>') == 1
    assert '\\u003c/script>' in result['html']
    assert '__PROFILE____AUTOPLAY__' in result['html']


def test_settlement_under_native_actor_judge_is_retained():
    world = {'bundle':{'world':{'id':'example'},'entities':[{'id':'a','categories':['actor'],'components':{}}]}}
    rounds = [{'turn':1,'actors':{'a':{'event_id':'r1-e00001','status':'unsupported_action','changes':[], 'judge':{'disposition':{'settled':{'event_id':'r1-e00002','status':'accepted','changes':[]}}}}}}]
    projection, _, _ = build_scene_inputs(world, rounds)
    assert [e['event_id'] for e in projection['events']] == ['r1-e00001','r1-e00002']


def test_missing_original_world_is_explicit():
    with pytest.raises(ValueError, match='Original authored world entities are unavailable'):
        render_world_scene({}, [])


def test_conflicting_duplicate_event_is_not_silently_reconstructed():
    world = {'bundle':{'world':{'id':'example'},'entities':[{'id':'a','categories':['actor'],'components':{}}]}}
    rounds = [{'turn':1,'actors':{'a':{'event_id':'r1-e00001','changes':[]}},'reactions':[{'event_id':'r1-e00001','changes':[{'path':'tick','after':1}]}]}]
    with pytest.raises(ValueError, match='Conflicting retained changes'):
        build_scene_inputs(world, rounds)


def test_rendered_actor_moves_but_ownership_does_not_move_remote_object():
    from scripts.render_composed_living_scene import _JS
    from world_substrate.living_scene_layout import ACTOR_POSITIONS_JS
    node = shutil.which('node')
    if node is None:
        pytest.skip('node is unavailable')
    world = json.loads((ROOT / 'tests/fixtures/airfield-s1-live.json').read_text())
    world['bundle']['entities'].append({'id':'tool','label':'Tool','categories':['object'], 'location':'office', 'owner_ref':'actor:sam','components':{}})
    rounds = [{'turn':1,'actors':{'sam':{'event_id':'r1-e00001','status':'accepted','changes':[{'path':'entities.sam.location.location_id','before':'office','after':'hangar'}]}}}]
    projection, profile, _ = build_scene_inputs(world, rounds)
    frames = build_living_scene_frames(projection, profile)
    functions = ('mobile', 'bind', 'homePoint', 'anchorPoint', 'statePosition', 'anchorFor', 'actorPositions')
    source = '\n'.join(line for line in _JS.splitlines() if any(line.startswith('function '+name+'(') for name in functions))
    script = 'const [FRAMES,PROFILE]=JSON.parse(require("fs").readFileSync(0,"utf8"));let idx=0;const window={matchMedia:()=>({matches:false})};\n'
    script += ACTOR_POSITIONS_JS + source + '\nconst before=actorPositions(FRAMES[0]);idx=1;const after=actorPositions(FRAMES[1]);console.log(JSON.stringify({before,after,tool:statePosition(PROFILE.entities.tool,FRAMES[1].views.entities.tool)}));'
    result = subprocess.run([node,'-e',script],input=json.dumps([frames,profile]),capture_output=True,text=True,check=True)
    positions = json.loads(result.stdout)
    assert positions['before']['sam'][0] < 50 < positions['after']['sam'][0]
    assert positions['tool'][0] < 50


def test_native_actor_selector_identifies_worker_without_actor_category():
    world = {'bundle': json.loads((ROOT / 'examples/world_authoring/orchard-v0.json').read_text()),
             'causal_model': json.loads((ROOT / 'examples/world_authoring/orchard-causal-v0.json').read_text())}
    _, profile, _ = build_scene_inputs(world, [])
    assert 'ava' in profile['actors']
    assert 'ava' not in profile['entities']
    assert profile['actors']['ava']['asset'].startswith('portrait-')
    assert profile['actors']['ava']['mobile_home'][1] < profile['entities']['apple-1']['mobile_home'][1]
