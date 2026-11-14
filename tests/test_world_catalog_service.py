"""Catalog boundary integration uses native scripted worlds; no provider calls."""
from __future__ import annotations

import json
import copy
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import scripts.world_builder_service as service

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / 'examples/world_authoring/orchard-v0.json').read_text())
# Three fruit make continuation observable without replacing the real runner.
for number in (2, 3):
    fruit = copy.deepcopy(BUNDLE['entities'][-1])
    fruit['id'] = f'apple-{number}'
    BUNDLE['entities'].append(fruit)
CAUSAL = json.loads((REPO / 'examples/world_authoring/orchard-causal-v0.json').read_text())
WORLD = {'ok': True, 'bundle': BUNDLE, 'causal_model': CAUSAL, 'description': 'An orchard'}


class CatalogServiceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(service.os.environ, {
            'WORLD_BUILDER_OWNER_PASSWORD': 'test-owner',
            'WORLD_BUILDER_RUN_LOG_DIR': self.tmp.name + '/runs',
            'WORLD_BUILDER_SHARE_DB': self.tmp.name + '/shares.sqlite',
            'WORLD_BUILDER_CATALOG_DB': self.tmp.name + '/catalog.sqlite'})
        self.env.start()
        service._REQUESTS.clear()
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), service.WorldBuilderHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f'http://127.0.0.1:{self.server.server_port}/world-builder/api'
        self.world = service._catalog().save_world(WORLD, service._world_fingerprint(BUNDLE, CAUSAL))

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.env.stop()
        self.tmp.cleanup()

    def request(self, path, body=None, owner=True):
        headers = {'Content-Type': 'application/json'}
        if owner:
            headers[service.OWNER_HEADER] = 'test-owner'
        req = urllib.request.Request(self.base + path, headers=headers,
            data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)

    def new_run(self):
        status, result = self.request('/worlds/' + self.world['id'] + '/runs', {})
        self.assertEqual(status, 200, result)
        return result['run']['id']

    def step(self, rid, checkpoint=None, **extra):
        return self.request('/run', {'catalog_run_id': rid, 'expected_checkpoint_id': checkpoint,
                                    'approved': True, 'policy': 'scripted', 'turns': 1, **extra})

    def test_catalog_readout_uses_durable_prefix_and_only_shares_matching_checkpoint(self):
        rid = self.new_run()
        status, first = self.step(rid)
        self.assertEqual(status, 200, first)
        detail = service._catalog().run_by_id(rid)
        def fake_dialogue(handler, client, kind, call, **kwargs):
            payload, _ = call('readout-test', 0)
            handler._json(200, {'ok': True, **payload, 'trace_id': service.TRACE_ROOT + '/readout/' + 'a' * 32})
        def fake_read(rounds, **kwargs):
            self.assertEqual(rounds, detail['record']['rounds'])
            return {'title': 'Durable orchard'}, None
        from scripts import run_readout
        with patch.object(service.WorldBuilderHandler, '_dialogue_call', fake_dialogue), patch.object(run_readout, 'read_run', fake_read):
            status, result = self.request('/readout', {'catalog_run_id': rid})
        self.assertEqual(status, 200, result)
        readout_id = result['trace_id']
        status, shared = self.request('/share', {'catalog_run_id': rid, 'readout_trace_id': readout_id})
        self.assertEqual(status, 200, shared)
        self.assertEqual(self.request('/share/' + shared['share_id'], owner=False)[1]['readout'], result['readout'])
        status, second = self.step(rid, first['checkpoint_id'])
        self.assertEqual(status, 200, second)
        status, shared = self.request('/share', {'catalog_run_id': rid, 'readout_trace_id': readout_id})
        self.assertEqual(status, 200, shared)
        self.assertNotIn('readout', self.request('/share/' + shared['share_id'], owner=False)[1])

    def test_private_catalog_requires_owner_for_reads_creates_and_runs(self):
        self.assertEqual(self.request('/worlds', owner=False)[0], 403)
        self.assertEqual(self.request('/worlds/' + self.world['id'] + '/runs', {}, owner=False)[0], 403)
        self.assertEqual(self.request('/run', {'catalog_run_id': 'x', 'expected_checkpoint_id': None}, owner=False)[0], 403)
        status, detail = self.request('/worlds/' + self.world['id'])
        self.assertEqual(status, 200)
        self.assertEqual({k: detail['world']['definition'][k] for k in WORLD}, WORLD)

    def test_real_native_round_continue_branch_and_durable_prefix(self):
        rid = self.new_run()
        status, first = self.step(rid, bundle={'malicious': True})
        self.assertEqual(status, 200, first)
        self.assertEqual(first['summary']['last_turn'], 1)
        cid = first['checkpoint_id']
        status, branch = self.request('/worlds/' + self.world['id'] + '/runs',
                                    {'parent_run_id': rid, 'checkpoint_id': cid})
        self.assertEqual(status, 200, branch)
        self.assertEqual(len(branch['record']['rounds']), 1)
        status, second = self.step(branch['run']['id'], cid)
        self.assertEqual(status, 200, second)
        self.assertEqual(second['summary']['last_turn'], 2)
        original = service._catalog().run(self.world['id'], rid)
        child = service._catalog().run(self.world['id'], branch['run']['id'])
        self.assertEqual(len(original['record']['rounds']), 1)
        self.assertEqual(len(child['record']['rounds']), 2)
        self.assertEqual([r['trace_id'] for r in child['record']['runs']], [first['trace_id'], second['trace_id']])
        self.assertEqual(self.request('/share', {'catalog_run_id': branch['run']['id']})[0], 200)

    def test_duplicate_step_rejected_before_native_work(self):
        rid = self.new_run()
        status, first = self.step(rid)
        self.assertEqual(status, 200, first)
        with patch.object(service.WorldBuilderHandler, '_run_native', side_effect=AssertionError('must not run')):
            status, stale = self.step(rid)
        self.assertEqual(status, 409, stale)
        self.assertEqual(len(service._catalog().run(self.world['id'], rid)['record']['rounds']), 1)

    def test_generation_save_hook_owner_only_and_fail_closed(self):
        service._REQUEST.set({'path': '/generate-world', 'summary': {'description': 'Built orchard'}})
        token = service._LEDGER.set('owner')
        try:
            status, payload = service._catalog_response(200, {**WORLD, 'trace_id': 'build-test'})
            self.assertEqual(status, 200)
            self.assertEqual(service._catalog().world(payload['catalog_world_id'])['world']['description'], 'Built orchard')
            with patch.object(service, '_catalog', side_effect=OSError('disk unavailable')):
                self.assertEqual(service._catalog_response(200, WORLD)[0], 500)
        finally:
            service._LEDGER.reset(token)
        token = service._LEDGER.set('visitor')
        try:
            self.assertNotIn('catalog_world_id', service._catalog_response(200, WORLD)[1])
        finally:
            service._LEDGER.reset(token)
            service._REQUEST.set(None)

    def test_checkpoint_failure_never_returns_success(self):
        rid = self.new_run()
        with patch.object(service.WorldCatalog, 'append', side_effect=OSError('disk unavailable')):
            status, result = self.step(rid)
        self.assertEqual(status, 500, result)
        self.assertEqual(service._catalog().run(self.world['id'], rid)['record']['rounds'], [])

    def test_async_native_round_persists_before_job_success(self):
        import time
        rid = self.new_run()
        status, started = self.step(rid, **{'async': True})
        self.assertEqual(status, 202, started)
        for _ in range(100):
            status, result = self.request('/jobs/' + started['job_id'])
            if result.get('status') != 'running':
                break
            time.sleep(.02)
        self.assertEqual(status, 200, result)
        self.assertIn('checkpoint_id', result)
        self.assertEqual(len(service._catalog().run(self.world['id'], rid)['record']['rounds']), 1)

    def test_native_finished_world_returns_success_without_fake_checkpoint(self):
        finished_world = copy.deepcopy(WORLD)
        finished_world['bundle']['entities'] = finished_world['bundle']['entities'][:3]
        world = service._catalog().save_world(finished_world, 'finished')
        run = service._catalog().create_run(world['id'])['run']['id']
        status, result = self.step(run)
        self.assertEqual(status, 200, result)
        checkpoint = result['checkpoint_id']
        status, result = self.step(run, checkpoint)
        self.assertEqual(status, 200, result)
        self.assertEqual(result['checkpoint_id'], checkpoint)
        detail = service._catalog().run_by_id(run)
        self.assertEqual(len(detail['checkpoints']), 1)
        self.assertEqual(len(detail['record']['rounds']), 1)
        self.assertEqual(detail['run']['status'], 'finished')
        with patch.object(service.WorldBuilderHandler, '_run_native', side_effect=AssertionError('must not run')):
            self.assertEqual(self.step(run, checkpoint)[0], 422)

    def test_stopped_checkpoint_cannot_offer_a_branch_that_cannot_advance(self):
        definition = copy.deepcopy(WORLD)
        definition['run_stop'] = {'mode': 'every_round', 'max_rounds': 1}
        wid = service._catalog().save_world(definition, 'round-limited')['id']
        rid = service._catalog().create_run(wid)['run']['id']
        status, first = self.step(rid)
        self.assertEqual(status, 200, first)
        detail = service._catalog().run_by_id(rid)
        self.assertFalse(detail['run']['can_continue'])
        self.assertFalse(detail['checkpoints'][0]['can_branch'])
        self.assertIn('earlier checkpoint', detail['checkpoints'][0]['reason'])
        self.assertEqual(self.request('/worlds/' + wid + '/runs', {'parent_run_id': rid, 'checkpoint_id': first['checkpoint_id']})[0], 422)

    def test_request_round_cap_does_not_exhaust_logical_run(self):
        definition = copy.deepcopy(WORLD)
        definition['run_stop'] = {'mode': 'every_round'}
        wid = service._catalog().save_world(definition, 'every-round')['id']
        rid = service._catalog().create_run(wid)['run']['id']
        status, first = self.step(rid)
        self.assertEqual(status, 200, first)
        self.assertEqual(first['summary']['stopped']['reason'], 'round_cap')
        detail = service._catalog().run_by_id(rid)
        self.assertTrue(detail['run']['can_continue'])
        self.assertTrue(detail['checkpoints'][0]['can_branch'])
        status, second = self.step(rid, first['checkpoint_id'])
        self.assertEqual(status, 200, second)
        self.assertEqual(second['summary']['last_turn'], 2)

    def test_historical_missing_display_review_is_derived_without_rewriting_definition(self):
        wid = self.world['id']
        status, detail = self.request('/worlds/' + wid)
        self.assertEqual(status, 200, detail)
        self.assertTrue(detail['world']['definition']['review']['mechanics'])
        self.assertEqual(detail['world']['definition']['review_origin'], 'compiler-derived-from-retained-rules')
        status, run = self.request('/worlds/' + wid + '/runs', {})
        self.assertEqual(status, 200, run)
        self.assertTrue(run['record']['world']['review']['mechanics'])
        self.assertEqual(service._catalog().world(wid)['world']['definition'], WORLD)
        status, first = self.step(run['run']['id'])
        self.assertEqual(status, 200, first)
        status, share = self.request('/share', {'catalog_run_id': run['run']['id']})
        self.assertEqual(status, 200, share)
        self.assertTrue(self.request('/share/' + share['share_id'], owner=False)[1]['world']['review']['mechanics'])

    def test_recovery_closes_share_reader_before_writing_the_same_database(self):
        # Production defaults catalog and shares to the same SQLite file.
        with patch.dict(service.os.environ, {'WORLD_BUILDER_CATALOG_DB': self.tmp.name + '/shares.sqlite'}):
            world = service._catalog().save_world(WORLD, service._world_fingerprint(BUNDLE, CAUSAL))
            record = {'schema': 'world-builder-share/v1', 'created': '2026-11-14T00:00:00Z', 'world': WORLD, 'rounds': [], 'actor_inputs': {}}
            service._save_share('synthetic-client', record)
            status, result = self.request('/worlds/import-logs', {})
            self.assertEqual(status, 200, result)
            self.assertEqual(result['public_recordings_matched'], 1)
            self.assertEqual(len(service._catalog().world(world['id'])['runs']), 1)

    def test_backfill_is_owner_only_and_does_not_import_guest_builds(self):
        logdir = Path(self.tmp.name) / 'runs'
        logdir.mkdir(exist_ok=True)
        owner = {'status': 200, 'who': 'owner', 'path': '/generate-world', 'trace_id': 'owned-build',
                 'request': {'description': 'Owner world'}, 'result': WORLD}
        agent = {**owner, 'who': 'agent:script', 'allowance': 'owner', 'trace_id': 'owner-agent-build'}
        guest = {**owner, 'who': 'visitor', 'trace_id': 'guest-build', 'request': {'description': 'Guest private prompt'}}
        (logdir / 'runs_2026-11-13.jsonl').write_text('\n'.join(json.dumps(row) for row in [owner, agent, guest]))
        self.assertEqual(self.request('/worlds/import-logs', {}, owner=False)[0], 403)
        first = self.request('/worlds/import-logs', {})
        second = self.request('/worlds/import-logs', {})
        self.assertEqual(first[0], 200, first)
        self.assertEqual(second[0], 200, second)
        self.assertEqual(len(service._catalog().worlds()), 3)
        self.assertEqual(first[1]['owner_builds_found'], 2)
        self.assertNotIn('Guest private prompt', json.dumps(second))

    def test_declared_branch_restores_exact_cognition_and_ignores_client_replacements(self):
        definition = copy.deepcopy(WORLD)
        bundle = definition['bundle']
        bundle['actor_information'] = {'version': 1, 'public_summary': 'Orchard', 'public_entities': [
            {'id': e['id'], 'label': e['label'], 'fields': []} for e in bundle['entities']],
            'actors': {'ava': {'brief': 'My own profile', 'initial_knowledge': [], 'observable_fields': []}}}
        world = service._catalog().save_world(definition, 'declared')
        rid = service._catalog().create_run(world['id'])['run']['id']
        status, first = self.step(rid)
        self.assertEqual(status, 200, first)
        checkpoint = first['checkpoint_id']
        child = service._catalog().create_run(world['id'], parent_run_id=rid, checkpoint_id=checkpoint)
        native = service.WorldBuilderHandler._run_native
        bodies = []

        def inspect(handler, client, body):
            bodies.append(copy.deepcopy(body))
            return native(handler, client, body)

        with patch.object(service.WorldBuilderHandler, '_run_native', inspect):
            status, second = self.step(child['run']['id'], checkpoint,
                actor_state={'briefs': {'ava': 'injected'}}, resident_memory={'ava': ['injected']},
                rulings=[{'injected': True}], turn_offset=90, continue_from={'injected': True})
        self.assertEqual(status, 200, second)
        self.assertEqual(bodies[0]['actor_state'], first['actor_state'])
        self.assertEqual(bodies[0]['continue_from'], first['trace']['final_snapshot'])
        self.assertEqual(bodies[0]['turn_offset'], 1)
        self.assertNotIn('resident_memory', bodies[0])
        self.assertEqual(second['actor_state']['briefs'], {'ava': 'My own profile'})
