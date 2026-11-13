"""An interpretation gap has no partial rule, judge, or communication effect."""
from copy import deepcopy
from unittest.mock import Mock
import sys
from types import SimpleNamespace

import pytest

from scripts import run_authored_world as runner, concordia_residents, judge as judge_module, rulings
from world_substrate import attempt as attempts
from test_independent_rule_authority import world_and_rule

TEXT = 'I repair the condition and ask decider to record assent.'

class RecordedResidents:
    def __init__(self, actors, **kwargs):
        self.memory = deepcopy(kwargs.get('memory') or {a: [] for a in actors})
    def observe(self, actor, text):
        self.memory.setdefault(actor, []).append(text)
    def choose(self, actor, offered, context, **kwargs):
        return {'belief': 'My own evidence.', 'attempt': TEXT if actor == 'validator' else 'wait',
                'expected_effect': 'Explain my attempt.', 'work': 'none', 'reasoning': 'My own choice.'}
    def cost(self):
        return 0
    def memory_state(self):
        return self.memory

@pytest.mark.req('semantic-binding/whole-attempt-coverage')
@pytest.mark.parametrize('declared', [True, False])
@pytest.mark.parametrize('with_judge', [True, False])
@pytest.mark.parametrize('reader_failure', [True, False])
def test_rejected_compound_changes_nothing_and_cannot_reach_judge_or_recipient(monkeypatch, declared, with_judge, reader_failure):
    bundle, causal, _ = world_and_rule()
    if not declared:
        bundle.pop('actor_information')
    original = {e['id']: deepcopy(e.get('components', {})) for e in bundle['entities']}
    monkeypatch.setattr(concordia_residents, 'Residents', RecordedResidents)
    def read(engine, actor, text, *args, **kwargs):
        if actor != 'validator':
            return {'kind': 'wait', 'fields': {}}, 0
        return {'unmatched': True, 'nearest_kind': 'repair-condition',
                'why': 'HIDDEN analyst-only diagnostic.', 'interpretation_rejection': 'requires_decomposition',
                'coverage': {'status': 'requires_decomposition', 'action_spans': ['I repair the condition'],
                             'unrepresented_spans': ['ask decider to record assent']}}, 0
    if reader_failure:
        class ReadError(Exception):
            pass
        monkeypatch.setitem(sys.modules, 'llm_client', SimpleNamespace(LLMError=ReadError))
        monkeypatch.setattr(attempts, 'interpret', Mock(side_effect=ReadError('HIDDEN invalid schema: missing coverage')))
    else:
        monkeypatch.setattr(runner, '_read_attempt', read)
    # The receiving adapter must enforce rejection even if a future transport retains asks metadata.
    original_envelope = attempts.envelope
    def envelope(reading, **kwargs):
        value = original_envelope(reading, **kwargs)
        if reading.get('interpretation_rejection'):
            value['asks'] = 'decider'
        return value
    monkeypatch.setattr(attempts, 'envelope', envelope)
    judge_call = Mock(side_effect=AssertionError('interpretation rejection must never ask the judge'))
    monkeypatch.setattr(judge_module, 'judge', judge_call)
    trace, engine, _ = runner.run_world(bundle, causal, policy='resident', open_attempts=True,
        judge=with_judge, judge_rulings=rulings.CREATE, max_turns=1, model_name='recorded-policy')
    assert judge_call.call_count == 0
    assert {k: v.get('components', {}) for k,v in engine.world.material_dict()['entities'].items()} == original
    row = trace['transcript'][0]['actors']['validator']
    assert row['changes'] == [] and 'judge' not in row and 'request_delivery' not in row and 'asked' not in row
    assert row['interpretation_feedback'] == attempts.rejection_message(row['attempt']['reading'])
    assert 'No part' in row['interpretation_feedback']
    assert any(row['interpretation_feedback'] in text for text in trace['resident_memory']['validator'])
    assert not any('HIDDEN' in text for texts in trace['resident_memory'].values() for text in texts)
    assert not any('asked you' in text or TEXT in text for text in trace['resident_memory']['decider'])
    item = trace['summary']['unmatched_attempts'][0]
    assert item['attempt'] == TEXT
    assert item['interpretation_rejection'] == ('unread' if reader_failure else 'requires_decomposition')
    if not reader_failure:
        assert item['coverage'] == row['attempt']['reading']['coverage']
    assert engine.replay()['ok']
