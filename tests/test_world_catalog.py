from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.world_catalog import WorldCatalog, CatalogConflict, CatalogUnavailable


WORLD = {"description": "Two people review a pump", "bundle": {
    "world": {"id": "content-id", "label": "Pump"}, "entities": [],
    "actor_information": {"version": 1}}, "causal_model": {"mechanics": []}}


def result(number):
    return {"ok": True, "summary": {"first_turn": number, "last_turn": number},
            "trace": {"summary": {"first_turn": number, "last_turn": number},
                      "transcript": [{"turn": number, "actors": {}}],
                      "final_snapshot": {"world": {"revision": number}},
                      "actor_inputs": {"ari": [{"round": number, "context": {"actor_id": "ari"}}]},
                      "actor_information_mode": "declared-v1", "rulings": []},
            "actor_state": {"resident_memory": {"ari": [str(number)]}, "recent": [],
                            "briefs": {}, "underway": [], "turn_offset": number},
            "approval": {"profile": "reviewed"}, "trace_id": f"trace-{number}"}


class WorldCatalogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "catalog.sqlite"
        self.catalog = WorldCatalog(self.path)
        self.world = self.catalog.save_world(WORLD, "fp", build_trace_id="build-1")

    def tearDown(self):
        self.tmp.cleanup()

    def test_world_survives_reopen_without_rewriting_content_identity(self):
        self.assertNotEqual(self.world["id"], "content-id")
        reopened = WorldCatalog(self.path).world(self.world["id"])
        self.assertEqual(reopened["world"]["definition"], WORLD)
        self.assertEqual(self.catalog.save_world(WORLD, "fp", build_trace_id="build-1")["id"], self.world["id"])
        self.assertEqual(len(self.catalog.worlds()), 1)

    def test_branch_preserves_parent_prefix_and_exact_actor_checkpoint(self):
        parent = self.catalog.create_run(self.world["id"])
        cp1 = self.catalog.append(parent["run"]["id"], None, {"turn_offset": 0}, result(1))
        cp2 = self.catalog.append(parent["run"]["id"], cp1["id"], {"turn_offset": 1}, result(2))
        before = self.catalog.run(self.world["id"], parent["run"]["id"])
        child = self.catalog.create_run(self.world["id"], parent_run_id=parent["run"]["id"], checkpoint_id=cp1["id"])
        self.assertEqual([x["turn"] for x in child["record"]["rounds"]], [1])
        self.assertEqual(self.catalog.resume(child["run"]["id"])["response"]["actor_state"], result(1)["actor_state"])
        self.catalog.append(child["run"]["id"], cp1["id"], {"turn_offset": 1}, result(2))
        self.assertEqual(self.catalog.run(self.world["id"], parent["run"]["id"]), before)
        self.assertNotEqual(child["run"]["id"], parent["run"]["id"])
        self.assertEqual(self.catalog.run(self.world["id"], parent["run"]["id"])["run"]["checkpoint_id"], cp2["id"])

    def test_stale_or_gapped_step_does_not_change_history(self):
        run = self.catalog.create_run(self.world["id"])["run"]["id"]
        cp = self.catalog.append(run, None, {"turn_offset": 0}, result(1))
        with self.assertRaises(CatalogConflict):
            self.catalog.append(run, None, {"turn_offset": 0}, result(1))
        with self.assertRaises(CatalogConflict):
            self.catalog.append(run, cp["id"], {"turn_offset": 1}, result(3))
        self.assertEqual(len(self.catalog.run(self.world["id"], run)["record"]["rounds"]), 1)

    def test_missing_actor_state_is_not_a_faithful_branch_checkpoint(self):
        run = self.catalog.create_run(self.world["id"])["run"]["id"]
        incomplete = result(1)
        incomplete.pop("actor_state")
        cp = self.catalog.append(run, None, {"turn_offset": 0}, incomplete)
        detail = self.catalog.run(self.world["id"], run)
        self.assertFalse(detail["run"]["can_continue"])
        self.assertFalse(detail["checkpoints"][0]["can_branch"])
        with self.assertRaises(CatalogUnavailable):
            self.catalog.create_run(self.world["id"], parent_run_id=run, checkpoint_id=cp["id"])

    def test_existing_shared_recording_is_explicitly_replay_only(self):
        record = {"world": WORLD, "rounds": [{"turn": 1, "actors": {}}], "actor_inputs": {}}
        recovered = self.catalog.import_share(self.world["id"], "share1", record)
        self.assertFalse(recovered["run"]["can_continue"])
        self.assertEqual(recovered["record"]["rounds"], record["rounds"])
        self.assertEqual(recovered["checkpoints"], [])
        with self.assertRaises(CatalogUnavailable):
            self.catalog.resume(recovered["run"]["id"])

    def test_returned_records_cannot_mutate_stored_world_or_checkpoint(self):
        definition = copy.deepcopy(WORLD)
        definition["description"] = "changed client copy"
        run = self.catalog.create_run(self.world["id"])["run"]["id"]
        response = result(1)
        self.catalog.append(run, None, {"turn_offset": 0}, response)
        response["actor_state"]["resident_memory"]["ari"].append("mutation")
        out = self.catalog.resume(run)
        out["response"]["actor_state"]["resident_memory"]["ari"].append("other mutation")
        self.assertEqual(self.catalog.resume(run)["response"]["actor_state"], result(1)["actor_state"])
        self.assertEqual(self.catalog.world(self.world["id"])["world"]["definition"], WORLD)

    def test_explicit_finished_response_preserves_checkpoint_and_disables_continue(self):
        rid = self.catalog.create_run(self.world['id'])['run']['id']
        cp = self.catalog.append(rid, None, {}, result(1))
        finished = {'ok': True, 'summary': {'last_turn': 1, 'terminal_reached': True}, 'trace': {'transcript': []}}
        saved = self.catalog.append(rid, cp['id'], {}, finished)
        self.assertEqual(saved['id'], cp['id'])
        detail = self.catalog.run_by_id(rid)
        self.assertEqual(len(detail['checkpoints']), 1)
        self.assertEqual(len(detail['record']['rounds']), 1)
        self.assertEqual(detail['run']['status'], 'finished')
        with self.assertRaises(CatalogUnavailable):
            self.catalog.resume(rid)

    def test_initial_recovery_is_atomic_and_idempotent(self):
        request = {'continued': False}
        first = self.catalog.import_initial_run(self.world['id'], 'old-1', request, result(1))
        again = self.catalog.import_initial_run(self.world['id'], 'old-1', request, result(1))
        self.assertEqual(first['run']['id'], again['run']['id'])
        with self.assertRaises(CatalogConflict):
            self.catalog.import_initial_run(self.world['id'], 'bad', request, result(2))
        self.assertEqual(len(self.catalog.world(self.world['id'])['runs']), 1)
