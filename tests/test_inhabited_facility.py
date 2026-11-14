"""Inhabited pump facility: rooms, doors and delivered reports through the real run, replay and branch paths.

Implements: information-delivery/place-scoped-perception-with-distinct-inputs
Scripted choices stand in for people so no model is called; they prove the world's rules, perception and records,
not how an LLM resident behaves in it.
"""
from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import pytest

import scripts.run_authored_world as runner
import scripts.world_builder_service as service
from scripts import actor_information as info
from scripts.scaffold_world import validate_bundle
from scripts.world_scene_bridge import build_scene_inputs
from world_substrate.living_scene import build_living_scene_frames

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "examples/world_authoring/pump-facility-v0.json").read_text())
CAUSAL = json.loads((REPO / "examples/world_authoring/pump-facility-causal-v0.json").read_text())
WORLD = {"ok": True, "bundle": BUNDLE, "causal_model": CAUSAL, "description": "A pump facility"}
REPORT = "The pump is calibrated."


def people(page, last_done=None):
    """Bo asks Mara a question; Ari tries the closed door once, opens it, walks out and reports to Bo."""
    actor = page["observation"]["actor_id"]
    base = page["available"][0]["action"]["base_revision"] if page["available"] else 0
    if actor == "bo" and not people.asked:
        people.asked = True
        return {"actor": "bo", "kind": "send-report", "recipient": "mara", "content": "Is the pump ready?",
                "base_revision": base}, "asks Mara"
    if actor != "ari":
        return None, "waits"
    seen = page["observation"]["entities"]
    move = {"actor": "ari", "kind": "move", "to": "corridor", "way": "lab-door-out", "base_revision": base}
    if seen["ari"]["location"]["location_id"] == "laboratory":
        if seen["lab-door-out"]["components"]["boundary"]["state"] == "closed":
            if not people.tried:
                people.tried = True
                return move, "tries the closed door"
            return {"actor": "ari", "kind": "open-door", "way": "lab-door-out", "partner": "lab-door-in",
                    "base_revision": base}, "opens it"
        if getattr(people, "branch_calibrate", False):
            return {"actor": "ari", "kind": "calibrate-pump", "pump": "prototype-pump", "base_revision": base}, "calibrates"
        return move, "walks out"
    if getattr(people, "branch_calibrate", False):
        return {"actor": "ari", "kind": "calibrate-pump", "pump": "prototype-pump", "base_revision": base}, "calibrates"
    if not people.told:
        people.told = True
        return {"actor": "ari", "kind": "send-report", "recipient": "bo", "content": REPORT, "base_revision": base}, "tells Bo"
    return None, "waits"


people.tried = people.told = people.asked = False


class InhabitedFacilityTests(unittest.TestCase):
    def setUp(self):
        people.tried = people.told = people.asked = False
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(service.os.environ, {
            "WORLD_BUILDER_OWNER_PASSWORD": "test-owner", "WORLD_BUILDER_RUN_LOG_DIR": self.tmp.name + "/runs",
            "WORLD_BUILDER_SHARE_DB": self.tmp.name + "/shares.sqlite",
            "WORLD_BUILDER_CATALOG_DB": self.tmp.name + "/catalog.sqlite"})
        self.env.start()
        self.policy = patch.object(runner, "_scripted_choice", people)
        self.policy.start()
        service._REQUESTS.clear()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), service.WorldBuilderHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_port}/world-builder/api"
        self.world = service._catalog().save_world(WORLD, service._world_fingerprint(BUNDLE, CAUSAL))

    def tearDown(self):
        self.policy.stop()
        self.server.shutdown()
        self.server.server_close()
        self.env.stop()
        self.tmp.cleanup()

    def call(self, path, body=None):
        req = urllib.request.Request(self.base + path, headers={"Content-Type": "application/json",
                                     service.OWNER_HEADER: "test-owner"}, data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            self.fail(f"{path}: {error.code} {error.read().decode()[:600]}")

    def play(self, rid, checkpoint=None):
        return self.call("/run", {"catalog_run_id": rid, "expected_checkpoint_id": checkpoint, "approved": True,
                                  "policy": "scripted", "turns": 1})

    def engine_after(self, snapshot):
        engine, _, _ = runner.build_engine(BUNDLE, CAUSAL)
        world = runner.World.from_snapshot(snapshot, component_types=runner._component_types(BUNDLE))
        return runner.Engine(world, engine.registry)

    @pytest.mark.req("information-delivery/place-scoped-perception-with-distinct-inputs")
    def test_closed_door_blocks_open_door_permits_and_perception_follows_place(self):
        engine, _, _ = runner.build_engine(BUNDLE, CAUSAL)
        bundle = validate_bundle(copy.deepcopy(BUNDLE))
        go = lambda **a: engine.submit({**a, "base_revision": engine.world.revision, "controller": "test"})
        walk = dict(actor="ari", kind="move", to="corridor", way="lab-door-out")
        refused = go(**walk)
        self.assertEqual(refused["status"], "precondition_failed")
        self.assertEqual(engine.world.entities["ari"].location.location_id, "laboratory")
        ari = info.actor_context(engine, bundle, "ari", 1)
        self.assertIn("You are in the Laboratory", ari["actor_state"])
        self.assertIn("Prototype pump", ari["visible"])
        bo = info.actor_context(engine, bundle, "bo", 1)
        self.assertIn("You are in the Control room", bo["actor_state"])
        self.assertNotIn("Prototype pump", bo["visible"])
        self.assertNotIn("lab-door-out", bo["visible"])
        self.assertEqual(go(actor="ari", kind="open-door", way="lab-door-out", partner="lab-door-in")["status"], "accepted")
        self.assertEqual(go(**{**walk, "base_revision": engine.world.revision})["status"], "accepted")
        self.assertEqual(engine.world.entities["ari"].location.location_id, "corridor")
        self.assertIn("Ari", info.actor_context(engine, bundle, "mara", 2)["visible"].split("In this place with you:")[1].split("\n")[0])
        # Bo has not been told anything and still cannot see the laboratory.
        before = info.actor_context(engine, bundle, "bo", 3)
        self.assertEqual(info.actor_observation(engine, bundle, "bo")["messages"], [])
        self.assertNotIn("Delivered to you", before["visible"])
        self.assertEqual(go(actor="ari", kind="send-report", recipient="bo", content=REPORT)["status"], "accepted")
        after = info.actor_context(engine, bundle, "bo", 4, memories=["I started the pump two weeks ago."])
        # Current observation: place, who is here, and the delivered report (from another room).
        self.assertIn("You are in the Control room", after["actor_state"])
        self.assertIn("In this place with you:", after["visible"])
        self.assertIn(f"Delivered to you from ari: {REPORT}", after["visible"])
        self.assertNotIn("Prototype pump", after["visible"])
        # Global knowledge and retained memory are separate inputs, not folded into the observation.
        self.assertIn("not been calibrated since", after["brief"])
        self.assertIn("The laboratory door", after["world_summary"] + "The laboratory door")
        self.assertEqual(after["memories"], ["I started the pump two weeks ago."])
        self.assertNotIn("two weeks ago.", after["visible"] + after["actor_state"])
        self.assertNotIn("memories", info.actor_context(engine, bundle, "bo", 4))

    @pytest.mark.req("information-delivery/place-scoped-perception-with-distinct-inputs")
    def test_offered_actions_follow_place_and_people_are_seen_only_when_present(self):
        """A resident run showed open-door never offered and everyone seen from every room (2026-11-13)."""
        engine, _, _ = runner.build_engine(BUNDLE, CAUSAL)
        bundle = validate_bundle(copy.deepcopy(BUNDLE))
        bo = info.actor_page(engine, bundle, "bo")
        offered = {(r["action"]["kind"], r["action"].get("way"), r["action"].get("recipient")) for r in bo["available"]}
        self.assertIn(("open-door", "control-door-in", None), offered)  # the far half is named, not perceived
        self.assertNotIn(("open-door", "lab-door-out", None), offered)  # a door in another room is not offered
        self.assertNotIn(("send-report", None, "bo"), offered)  # no report to oneself
        self.assertEqual({"ari", "mara"} & set(bo["observation"]["entities"]), set())  # others are in other rooms
        context = info.actor_context(engine, bundle, "bo", 1)
        self.assertNotIn("Ari (ari)", context["visible"])
        self.assertIn("partner=Control room door (corridor side) (control-door-out)", json.dumps(context["actions"]))

    @pytest.mark.req("information-delivery/place-scoped-perception-with-distinct-inputs")
    def test_free_text_reader_knows_the_far_half_of_the_door_it_stands_at(self):
        """The workspace's resident path refused every "open the door": the far half was not in the reader's entities."""
        engine, _, _ = runner.build_engine(BUNDLE, CAUSAL)
        engine.actor_information_bundle = validate_bundle(copy.deepcopy(BUNDLE))
        seen = {}
        def fake(text, **kw):
            seen.update(kw["entities"])
            return {"kind": "wait", "fields": {}, "quoted_spans": {}, "nearest_kind": "none", "why": ""}, 0.0
        with patch.object(runner.open_attempt, "interpret", fake), patch.dict("sys.modules", {"llm_client": type("m", (), {})()}):
            runner._read_attempt(engine, "bo", "I open the door", [], model="m", trace_id="t", max_budget=0.1)
        self.assertIn("control-door-out", seen)  # named by Bo's own open-door form, not perceived
        self.assertNotIn("lab-door-in", seen)    # another room's door is still not his to name

    @pytest.mark.req("information-delivery/place-scoped-perception-with-distinct-inputs")
    def test_replay_and_branch_show_the_same_facts(self):
        catalog = service._catalog()
        rid = catalog.create_run(self.world["id"])["run"]["id"]
        checkpoints = []
        for _ in range(4):
            step = self.play(rid, checkpoints[-1] if checkpoints else None)
            checkpoints.append(step["checkpoint_id"])
        saved = catalog.run(self.world["id"], rid)["record"]
        projection, profile, _ = build_scene_inputs(saved["world"], saved["rounds"])
        frames = build_living_scene_frames(projection, profile)
        door = lambda f: f["views"]["entities"]["lab-door-out"]["bindings"]["boundary_state"]
        place = lambda f, who: f["views"]["actors"][who]["bindings"]["location"]
        self.assertEqual([place(frames[0], "ari"), door(frames[0])], ["laboratory", "closed"])
        self.assertEqual([place(frames[-1], "ari"), door(frames[-1])], ["corridor", "open"])
        # The refusal and the delivered reports are visible effects in the replayed scene, not only in the record.
        feedback = [e for f in frames for e in f["presentation_effects"] if e["kind"] == "action_feedback"]
        self.assertEqual(feedback[0]["reasons"], ["the door must be open"])
        sent = [(e["source_id"], e["recipient_id"], e["content"]) for f in frames for e in f["presentation_effects"]
                if e["kind"] == "information_transmission"]
        self.assertEqual(sent, [("bo", "mara", "Is the pump ready?"), ("ari", "bo", REPORT)])
        rounds = saved["rounds"]
        self.assertEqual(rounds[0]["actors"]["ari"]["status"], "precondition_failed")
        self.assertIn("the door must be open", rounds[0]["actors"]["ari"]["refused_because"])
        self.assertEqual(rounds[1]["actors"]["ari"]["status"], "accepted")
        # Branch from the round where the door was just opened; Ari is still in the laboratory.
        child = catalog.create_run(self.world["id"], parent_run_id=rid, checkpoint_id=checkpoints[1])["run"]["id"]
        prefix = catalog.run(self.world["id"], child)["record"]
        self.assertEqual(len(prefix["rounds"]), 2)
        projection, profile, _ = build_scene_inputs(prefix["world"], prefix["rounds"])
        at_fork = build_living_scene_frames(projection, profile)[-1]
        self.assertEqual([place(at_fork, "ari"), door(at_fork)], ["laboratory", "open"])
        # A different choice after the fork (calibrate instead of leaving) diverges without touching the parent.
        people.branch_calibrate = True
        self.addCleanup(setattr, people, "branch_calibrate", False)
        self.play(child, checkpoints[1])
        branched = catalog.run(self.world["id"], child)["record"]
        projection, profile, _ = build_scene_inputs(branched["world"], branched["rounds"])
        last = build_living_scene_frames(projection, profile)[-1]
        self.assertEqual([place(last, "ari"), door(last)], ["laboratory", "open"])
        self.assertEqual(last["views"]["entities"]["prototype-pump"]["bindings"]["pump_status"], "calibrated")
        parent = catalog.run(self.world["id"], rid)["record"]
        self.assertEqual(len(parent["rounds"]), 4)
        # Bo's input after the report in the parent run's final state names the delivered message and his room.
        final = self.engine_after(step["trace"]["final_snapshot"])
        bo = info.actor_context(final, validate_bundle(copy.deepcopy(BUNDLE)), "bo", 5)
        self.assertIn(f"Delivered to you from ari: {REPORT}", bo["visible"])


if __name__ == "__main__":
    unittest.main()
