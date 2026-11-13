"""A retained production request flag is not evidence of delivered communication."""
import json
from pathlib import Path

from scripts import people_world


def recorded_inputs():
    compiler, pipeline = people_world._pipeline()
    from scenario_spec import ScenarioSpecV1
    root = Path(__file__).resolve().parents[1]
    calls = {row['id']: row for row in map(json.loads, (root / 'evidence/i0-i1/deployed-integration-3/llm-calls.jsonl').read_text().splitlines())}
    spec = ScenarioSpecV1.model_validate_json(calls[23414]['response'])
    bundle, compiled, coverage = compiler.compile_spec(spec)
    signatures = [a.model_dump() for a in pipeline.ActionSignatures.model_validate_json(calls[23416]['response']).actions]
    signatures = pipeline.record_fields(spec, signatures)
    bundle['actions'] += [{k: a[k] for k in ('kind', 'description', 'fields')} for a in signatures]
    cycle = compiler.add_work_cycle(spec, bundle, compiled, [a['kind'] for a in signatures])
    prepared = {'spec': spec, 'bundle': bundle, 'compiled': compiled, 'coverage': coverage,
                'sigs': signatures, 'work_cycle': cycle}
    generated = json.loads(calls[23425]['response'])
    return prepared, generated


def test_actual_generated_private_flags_do_not_masquerade_as_world_actions():
    prepared, generated = recorded_inputs()
    result = people_world.assemble_people_world(prepared, generated)
    kinds = {a['kind'] for a in result['bundle']['actions']}
    assert 'send-report' in kinds and 'request-review' in kinds
    assert not {'request-evidence', 'investigate-evidence', 'ignore-claim'} & kinds
    assert any('only isolated private work bookkeeping' in note for note in result['dropped_generated_rules'])


def test_a_flag_read_by_a_process_with_another_effect_is_preserved():
    prepared, generated = recorded_inputs()
    process = generated['processes'][0]
    process['selector']['components'].append('member')
    process['effects'].append({'participant': 'it', 'path': 'components.member.aware', 'op': 'set', 'value': {'literal': True}})
    result = people_world.assemble_people_world(prepared, generated)
    assert 'request-evidence' in {a['kind'] for a in result['bundle']['actions']}
    assert process['process_id'] in {p['process_id'] for p in result['causal_model']['processes']}


def test_a_flag_used_by_a_declared_terminal_is_preserved():
    prepared, generated = recorded_inputs()
    generated['terminal'] = {'label': 'A request was made', 'selector': {'categories': ['actor'], 'components': ['work']},
                             'mode': 'any', 'checks': [{'path': 'components.work.request_evidence_done', 'op': 'eq', 'value': True}]}
    result = people_world.assemble_people_world(prepared, generated)
    assert 'request-evidence' in {a['kind'] for a in result['bundle']['actions']}
    assert result['causal_model']['terminal'] == generated['terminal']
