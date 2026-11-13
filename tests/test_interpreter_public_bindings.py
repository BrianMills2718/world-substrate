"""Interpreter receives public referents, never private form identities or fillers."""
from copy import deepcopy
import sys
from types import ModuleType

import pytest

from scripts import run_authored_world as runner
from world_substrate import attempt
from world_substrate.model import Entity
from test_actor_information import fixture, Details

pytestmark = pytest.mark.req('semantic-binding/preserve-operation-and-referents')


def capture(monkeypatch, bundle, engine, actor='mara'):
    engine.actor_information_bundle = bundle
    monkeypatch.setitem(sys.modules, 'llm_client', ModuleType('llm_client'))
    calls = []
    def interpret(text, **kwargs):
        calls.append(deepcopy(kwargs))
        return {'kind': 'inspect', 'fields': {'target': 'mara'}, 'quoted_spans': {'target': 'myself'}}, 0
    monkeypatch.setattr(attempt, 'interpret', interpret)
    signatures = [{'kind': 'inspect', 'description': 'PRIVILEGED mechanic text', 'fields': [
        {'name': 'target', 'type': 'entity_ref', 'only': 'private-note',
         'from': {'participant': 'actor', 'path': 'details.secret'}}]}]
    original = deepcopy(signatures)
    reading, _ = runner._read_attempt(engine, actor, 'I inspect myself', signatures,
                                     model='fixture', trace_id='fixture', max_budget=1)
    assert signatures == original
    assert reading['fields'] == {'target': 'mara'}  # public examples cannot override an explicit reading
    return calls[0]


def test_visible_public_binding_survives_without_private_fillers(monkeypatch):
    bundle, engine = fixture()
    sent = capture(monkeypatch, bundle, engine)
    assert sent['signatures'][0]['known_bindings'] == [{'target': 'ari'}]
    assert sent['signatures'][0]['description'] == 'Request inspection.'
    assert sent['signatures'][0]['fields'] == [{'name': 'target', 'type': 'entity_ref'}]
    assert 'PRIVILEGED' not in str(sent)


def test_hidden_action_form_and_description_stay_out_of_interpreter(monkeypatch):
    bundle, engine = fixture()
    bundle['entities'].append({'id': 'private-note', 'label': 'SECRET', 'categories': ['record'],
                              'components': {'details': {'visible': 'known', 'secret': 'hidden'}}})
    engine.world.entities['private-note'] = Entity(entity_id='private-note', label='SECRET',
        category_ids=('record',), components={'details': Details()})
    bundle['actor_information']['public_entities'].append({'id': 'private-note', 'label': 'Known note',
                                                          'fields': [], 'actor_ids': ['ari']})
    bundle['actor_information']['public_actions'].append({'kind': 'inspect', 'description': 'PRIVATE FORM',
                                                         'fields': {'target': 'private-note'}})
    sent = capture(monkeypatch, bundle, engine)
    assert 'private-note' not in str(sent) and 'PRIVATE FORM' not in str(sent)
    authorized = capture(monkeypatch, bundle, engine, actor='ari')
    assert {'target': 'private-note'} in authorized['signatures'][0]['known_bindings']


def test_private_state_change_cannot_change_interpretation_input(monkeypatch):
    bundle, engine = fixture()
    first = capture(monkeypatch, bundle, engine)
    engine.world.entities['ari'].components['details'].secret = 'different hidden credential'
    engine.world.entities['ari'].label = 'NEW SECRET LABEL'
    bundle['actions'][0]['description'] = 'NEW SECRET DESCRIPTION'
    assert capture(monkeypatch, bundle, engine) == first
