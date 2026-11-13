"""Personal stance and nonbinding assent do not confer activation authority."""
import json
from pathlib import Path

import pytest

from test_independent_rule_authority import world_and_rule
from scripts import consequence_report
from scripts.run_authored_world import build_engine


def submit(engine, actor, kind, **fields):
    return engine.submit({'actor': actor, 'controller': 'test', 'kind': kind,
                          'base_revision': engine.world.revision, **fields})


@pytest.mark.req('native-coordination/independent-generated-concern-procedure')
def test_technical_person_can_state_a_position_without_becoming_a_required_decider():
    bundle, causal, _ = world_and_rule()
    engine, _, _ = build_engine(bundle, causal)
    assert submit(engine, 'validator', 'state-concerned', position='position-validator')['status'] == 'accepted'
    assert submit(engine, 'validator', 'record-assent', position='position-validator', decision='activation')['status'] == 'accepted'
    assert engine.world.entities['position-validator'].component('actor_position').assent is True
    assert engine.world.entities['activation'].component('validation_decision').assents == 0
    assert submit(engine, 'validator', 'repair-condition', authority='technical-role-validator', condition='condition-activation')['status'] == 'accepted'
    assert submit(engine, 'validator', 'complete-validation', authority='technical-role-validator', decision='activation')['status'] == 'accepted'
    assert submit(engine, 'decider', 'activate', decision='activation')['status'] == 'precondition_failed'
    assert submit(engine, 'decider', 'record-assent', position='position-decider', decision='activation')['status'] == 'accepted'
    assert engine.world.entities['activation'].component('validation_decision').assents == 1
    assert submit(engine, 'decider', 'activate', decision='activation')['status'] == 'accepted'


@pytest.mark.req('native-coordination/proposed-rules-cannot-replace-actor-owned-assent')
def test_raw_candidate_cannot_give_one_person_multiple_required_assent_units():
    bundle, causal, _ = world_and_rule()
    position = next(e for e in bundle['entities'] if e['id'] == 'position-validator')
    position['components']['actor_position']['assent_weight'] = 2
    assert not consequence_report.rules_check(bundle, causal)[0]['ok']


def test_retained_independent_world_keeps_its_original_position_contract():
    root = Path(__file__).resolve().parents[1]
    retained = json.loads((root / 'evidence/i0-i1/deployed-integration-4/build.json').read_text())
    engine, _, _ = build_engine(retained['bundle'], retained['causal_model'])
    assert 'position-ari' not in engine.world.entities
    assert submit(engine, 'bo', 'state-concerned', position='position-bo')['status'] == 'accepted'
