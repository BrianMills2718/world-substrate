"""An authoring sub-bundle must not retain forms for omitted compiled actions."""
import json
import sys
from pathlib import Path
from scripts.people_world import actions_to_write
from scripts.scaffold_world import validate_bundle

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'spikes/any-scenario-2026-10'))
from scenario_spec import ScenarioSpecV1
from compile_spec import compile_spec


def test_recorded_independent_build_has_valid_generated_rule_input():
    calls = [json.loads(line) for line in (ROOT / 'evidence/i0-i1/local-integration-1/llm-calls.jsonl').read_text().splitlines()]
    spec = ScenarioSpecV1.model_validate_json(calls[0]['response'])
    bundle, compiled, _ = compile_spec(spec)
    # This is the exact successful structured response from the failed build;
    # the independent compiled mechanics are omitted only for rule authoring.
    validate_bundle(actions_to_write({'bundle': bundle, 'compiled': compiled}))


def test_replay_records_old_missing_privacy_verdict_as_stopped_without_approval(tmp_path):
    from types import ModuleType
    from unittest.mock import patch
    from scripts import replay_build, world_builder_service
    from scripts.review_rules import ActorInputPrivacyError
    (tmp_path / 'run-log.jsonl').write_text(json.dumps({'path': '/generate-world', 'request': {}}) + '\n')
    (tmp_path / 'llm-calls.jsonl').write_text('')
    with patch.object(replay_build, 'recorded_llm_client', return_value=ModuleType('llm_client')), \
            patch.object(world_builder_service.WorldBuilderHandler, '_generate_world',
                         side_effect=ActorInputPrivacyError('actor-input review is missing or malformed')):
        result = replay_build.replay(tmp_path)
    assert result['kept'] is None
    assert result['stopped'] == 'ActorInputPrivacyError: actor-input review is missing or malformed'
