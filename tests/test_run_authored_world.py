from __future__ import annotations

import importlib.util
import json
import sys
import types
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.bootstrap_scene_profile import _entity_binding
from scripts.run_authored_world import _llm_choice, _scripted_choice, bookkeeping_fields, _runtime_catalog, build_engine, render_run, run_world
from scripts.scaffold_world import load_bundle
from world_substrate.action_authoring import ActionDeclarationError

REPO = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO / "examples/world_authoring/orchard-v0.json"
CAUSAL_PATH = REPO / "examples/world_authoring/orchard-causal-v0.json"
REPAIR_BUNDLE_PATH = REPO / "examples/world_authoring/repair-bay-v0.json"
REPAIR_CAUSAL_PATH = REPO / "examples/world_authoring/repair-bay-causal-v0.json"


class AuthoredWorldRunTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(BUNDLE_PATH)
        self.causal = json.loads(CAUSAL_PATH.read_text())

    def test_scripted_run_uses_compiled_mechanics_and_reaches_terminal(self):
        trace, engine, model = run_world(
            self.bundle, self.causal, policy="scripted", max_turns=5
        )
        self.assertEqual(trace["model"], "scripted-least-recent")
        self.assertEqual(trace["cost_usd"], 0.0)
        self.assertEqual(trace["summary"]["turns"], 1)
        self.assertTrue(trace["summary"]["terminal_reached"])
        self.assertEqual(engine.world.entities["apple-1"].ownership.owner_ref, "actor:ava")
        self.assertEqual(engine.world.entities["apple-1"].component("fruit").stage, "picked")
        self.assertTrue(model.terminal and model.terminal.reached(engine.world))

    def test_scripted_choice_takes_the_move_done_least_recently(self):
        page = {"available": [{"action": {"kind": "cut-logs"}}, {"action": {"kind": "load-logs"}}]}
        self.assertEqual(_scripted_choice(page)[0]["kind"], "cut-logs")
        self.assertEqual(_scripted_choice(page, {"cut-logs": 3})[0]["kind"], "load-logs")
        self.assertEqual(_scripted_choice(page, {"cut-logs": 3, "load-logs": 4})[0]["kind"], "cut-logs")
        self.assertIsNone(_scripted_choice({"available": []})[0])

    def test_scripted_run_keeps_every_step_of_a_generated_chain_working(self):
        # c4-run17 (live, 2026-10-21): taking the first allowed move kept the timber crew cutting and never
        # loading, so the sawmill worker and pencil maker never acted in 26 rounds.
        fixture = json.loads((REPO / "tests/fixtures/pencil-c4-run17.json").read_text())
        trace, _, _ = run_world(fixture["bundle"], fixture["causal_model"], policy="scripted", max_turns=26)
        self.assertEqual(trace["summary"]["idle_actors"], [])
        self.assertEqual(trace["summary"]["never_offered"], {})
        done = {row["did"]["kind"] for t in trace["transcript"] for row in t["actors"].values()
                if row.get("status") == "accepted" and row.get("did")}
        self.assertTrue({"load-logs", "assemble-pencils", "deliver-pencils", "sell-pencils"} <= done, done)

    def test_a_move_made_on_a_same_round_retry_is_not_reported_never_offered(self):
        # 2026-10-23 luna measurement R1.5: the hose was connected first in round 1, the other two firefighters
        # retried and put out both fires that round, yet the summary said extinguish-fire was never possible.
        fixture = json.loads((REPO / "tests/fixtures/firefighting-luna-r1.json").read_text())
        trace, _, _ = run_world(fixture["bundle"], fixture["causal_model"], policy="scripted", max_turns=12)
        done = [row["did"]["kind"] for t in trace["transcript"] for row in t["actors"].values()
                if row.get("status") == "accepted" and row.get("did")]
        self.assertEqual(done.count("extinguish-fire"), 2)
        self.assertTrue(trace["summary"]["terminal_reached"])
        self.assertEqual(trace["summary"]["never_offered"], {})

    def test_run_records_distinct_rule_refusals_with_their_failed_checks(self):
        bundle = load_bundle(REPAIR_BUNDLE_PATH)
        causal = json.loads(REPAIR_CAUSAL_PATH.read_text())
        trace, _, _ = run_world(bundle, causal, policy="scripted", max_turns=5)
        rows = [row for turn in trace["transcript"] for row in turn["actors"].values()]
        self.assertTrue(all("blocked_by_rules" in row for row in rows))
        refusals = [b for row in rows for b in row["blocked_by_rules"]]
        self.assertTrue(refusals, "Repair Bay should show at least one refused action")
        for row in rows:
            keys = [(b["action"]["kind"], b["reason"]) for b in row["blocked_by_rules"]]
            self.assertEqual(len(keys), len(set(keys)))
            self.assertLessEqual(len(keys), 3)
        self.assertTrue(all(b["reason"] for b in refusals))

    def test_world_builder_replay_labels_rounds_not_turn_of_total(self):
        trace, _, model = run_world(self.bundle, self.causal, policy="scripted", max_turns=1)
        html = render_run(self.bundle, trace, model)
        self.assertIn("'Round '+f.turn", html)
        self.assertNotIn("'Turn '+f.turn+' / '", html)

    def test_moves_that_change_nothing_are_never_chosen(self):
        # 2026-10-06: two cooks "recorded" an already-waiting order every round
        # and the world was reported busy. A move whose only effect leaves state
        # as it was must not be offered or counted.
        causal = json.loads(json.dumps(self.causal))
        causal["mechanics"][0]["effects"] = [
            {"participant": "fruit", "path": "components.fruit.stage", "op": "set", "value": {"literal": "ripe"}},
        ]
        with self.assertRaisesRegex(ValueError, "no actions"):
            run_world(self.bundle, causal, policy="scripted", max_turns=3)
        # The same world with a real effect still acts, and the move is marked as a change.
        trace, _, _ = run_world(self.bundle, self.causal, policy="scripted", max_turns=1)
        rows = [r for t in trace["transcript"] for r in t["actors"].values() if r["status"] == "accepted"]
        self.assertTrue(rows and all(r["changed"] for r in rows))

    def test_busy_but_stuck_world_reports_stalled_people_and_its_one_remaining_move(self):
        # Ongoing orchard: the only move left is picking the fruit that regrows.
        causal = json.loads(json.dumps(self.causal)); causal["terminal"] = None
        causal["processes"] = [{
            "process_id": "regrow", "rationale": "Picked fruit grows back.",
            "selector": {"categories": ["fruit"], "components": ["fruit"]},
            "checks": [{"label": "the fruit has been picked",
                        "left": {"participant": {"name": "it", "path": "components.fruit.stage"}},
                        "op": "eq", "right": {"literal": "picked"}}],
            "effects": [{"participant": "it", "path": "components.fruit.stage", "op": "set", "value": {"literal": "ripe"}},
                        {"participant": "it", "path": "ownership.owner_ref", "op": "set", "value": {"literal": "place:orchard"}}],
        }]
        trace, _, _ = run_world(self.bundle, causal, policy="scripted", max_turns=6)
        self.assertEqual(trace["summary"]["moves_at_end"], ["pick"])
        self.assertEqual(trace["summary"]["stalled_actors"], [])

    def test_world_where_only_processes_run_is_not_active(self):
        # The 2026-10-06 pencil world: drains ran every round but no actor could
        # ever act, and it was reported as still alive.
        causal = json.loads(json.dumps(self.causal))
        causal["terminal"] = None
        for mechanic in causal["mechanics"]:
            mechanic["checks"].append({"label": "never possible",
                                       "left": {"literal": 1}, "op": "eq", "right": {"literal": 2}})
        def flip(pid, a, b):
            return {"process_id": pid, "rationale": "Fruit changes by itself.",
                    "selector": {"categories": ["fruit"], "components": ["fruit"]},
                    "checks": [{"label": f"the fruit is {a}",
                                "left": {"participant": {"name": "it", "path": "components.fruit.stage"}},
                                "op": "eq", "right": {"literal": a}}],
                    "effects": [{"participant": "it", "path": "components.fruit.stage", "op": "set",
                                 "value": {"literal": b}}]}
        causal["processes"] = [flip("wilt", "ripe", "wilted"), flip("recover", "wilted", "ripe")]
        trace, _, _ = run_world(self.bundle, causal, policy="scripted", max_turns=6)
        self.assertEqual(trace["summary"]["accepted_actions"], 0)
        self.assertTrue(all(t["world_changes"] for t in trace["transcript"]))
        self.assertFalse(trace["summary"]["active_at_end"])

    def test_processes_keep_an_ongoing_world_going_and_runs_continue(self):
        causal = json.loads(json.dumps(self.causal))
        causal["terminal"] = None
        causal["processes"] = [{
            "process_id": "regrow", "rationale": "Picked fruit grows back.",
            "selector": {"categories": ["fruit"], "components": ["fruit"]},
            "checks": [{"label": "the fruit has been picked",
                        "left": {"participant": {"name": "it", "path": "components.fruit.stage"}},
                        "op": "eq", "right": {"literal": "picked"}}],
            "effects": [{"participant": "it", "path": "components.fruit.stage", "op": "set", "value": {"literal": "ripe"}},
                        {"participant": "it", "path": "ownership.owner_ref", "op": "set", "value": {"literal": "place:orchard"}}],
        }]
        first, _, model = run_world(self.bundle, causal, policy="scripted", max_turns=4)
        self.assertEqual(len(model.processes), 1)
        self.assertEqual(first["summary"]["accepted_actions"], 4)
        self.assertEqual(first["summary"]["world_changes"], 4)
        self.assertEqual([t["world_changes"] for t in first["transcript"]], [["regrow"]] * 4)
        self.assertTrue(first["summary"]["active_at_end"])
        second, engine, _ = run_world(
            self.bundle, causal, policy="scripted", max_turns=4,
            start_snapshot=first["final_snapshot"], turn_offset=first["summary"]["last_turn"],
        )
        self.assertEqual([t["turn"] for t in second["transcript"]], [5, 6, 7, 8])
        self.assertEqual(engine.world.revision, 16)
        # A snapshot from a different rule set is refused.
        other = json.loads(json.dumps(first["final_snapshot"]))
        other["world"]["rule_versions"] = {"someone.else": "1"}
        with self.assertRaises(ValueError):
            run_world(self.bundle, causal, policy="scripted", max_turns=2, start_snapshot=other)

    def test_compiled_profile_is_frozen_before_run(self):
        engine, _, profile_id = build_engine(self.bundle, self.causal)
        self.assertTrue(profile_id)
        self.assertEqual(engine.world.rule_versions, {"orchard.action.pick": "1"})

    def test_rendered_fresh_run_is_graphical_and_self_contained(self):
        trace, _, compiled = run_world(self.bundle, self.causal, policy="scripted", max_turns=5)
        html = render_run(self.bundle, trace, compiled)
        self.assertIn("Scene replay", html)
        self.assertIn("Apple", html)
        self.assertIn("Ava", html)
        self.assertIn("document.getElementById(\'turn\')", html)

    def test_run_keeps_every_engine_event_in_full(self):
        # Issue #123 (G1): builder runs kept no engine event records (hashes, checks, read/write paths).
        trace, _, _ = run_world(self.bundle, self.causal, policy="scripted", max_turns=3)
        events = trace["engine_events"]
        self.assertTrue(events)
        for event in events:
            for key in ("event_id", "rule_id", "status", "checks", "declared_read_paths",
                        "declared_write_paths", "changes", "hash_before", "hash_after", "observation"):
                self.assertIn(key, event)
            self.assertRegex(event["event_id"], r"^r\d+-e\d+$")
        cited = {row["event_id"] for t in trace["transcript"] for row in t["actors"].values() if row.get("event_id")}
        cited |= {e["event_id"] for t in trace["transcript"] for e in t.get("world_events", [])}
        self.assertTrue(cited)
        self.assertLessEqual(cited, {e["event_id"] for e in events})
        # A continued run restarts the engine's own ids; the run-wide ids stay unique.
        again, _, _ = run_world(self.bundle, self.causal, policy="scripted", max_turns=2,
                                start_snapshot=trace["final_snapshot"], turn_offset=trace["summary"]["last_turn"])
        self.assertFalse({e["event_id"] for e in events} & {e["event_id"] for e in again["engine_events"]})

    def test_round_picture_shows_by_itself_changes_apart_from_actions(self):
        # Issue #126 (G8): the picture carried no trace of process-made changes.
        trace, _, compiled = run_world(self.bundle, self.causal, policy="scripted", max_turns=2)
        # A run with no process changes keeps the picture as it was.
        self.assertNotIn("byitself", render_run(self.bundle, trace, compiled))
        trace["transcript"][0]["world_changes"] = ["orchard.process.regrow_apples"]
        html = render_run(self.bundle, trace, compiled)
        frames = json.loads(html.split("const FRAMES=", 1)[1].split(";const PROFILE=", 1)[0])
        self.assertEqual(frames[0]["world_changes"], ["orchard.process.regrow_apples"])
        self.assertIn("id='byitself'", html)
        self.assertIn("'By itself: '", html)

    def test_fresh_world_entity_id_does_not_inherit_reference_world_asset_binding(self):
        bundle = json.loads(json.dumps(self.bundle))
        bundle["entities"][0]["id"] = "bo"
        bundle["entities"][0]["label"] = "New-world Bo"
        trace, _, compiled = run_world(bundle, self.causal, policy="scripted", max_turns=5)
        html = render_run(bundle, trace, compiled)
        self.assertIn("New-world Bo", html)
        self.assertIn("Scene replay", html)

    def test_unreviewable_mechanic_never_reaches_runtime(self):
        causal = json.loads(json.dumps(self.causal))
        causal["mechanics"][0]["effects"][0]["path"] = "components.fruit.nonexistent"
        with self.assertRaises(ActionDeclarationError):
            run_world(self.bundle, causal, policy="scripted", max_turns=5)

    def test_live_runner_caps_turns_and_policy_modes(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 30"):
            run_world(self.bundle, self.causal, max_turns=31)
        with self.assertRaisesRegex(ValueError, "scripted, llm or resident"):
            run_world(self.bundle, self.causal, policy="random")


class NeverOfferedNamesTheRealGapTests(unittest.TestCase):
    """The test run's "never possible" note names the gap a rewrite must fix, not a step it already has."""

    def _never(self, fixture: str) -> dict[str, str]:
        saved = json.loads((REPO / "tests/fixtures" / fixture).read_text())
        trace, _, _ = run_world(saved["bundle"], saved["causal_model"], policy="scripted", max_turns=24)
        return trace["summary"]["never_offered"]

    def test_a_raiser_a_law_always_refused_is_named_with_the_law(self):
        # Saved pencil s3: the carrier's price was 0, so every purchase broke the purchase law and boxes never arrived.
        why = self._never("pencil-s3-kept.json")["sell-boxes"]
        self.assertIn("every buy-boxes broke law boxes-purchase", why)
        self.assertIn("lost 0", why)

    def test_a_role_no_one_fits_names_the_missing_part(self):
        # Saved pencil4: ship-pencil-boxes wanted a shop with a shipment part; the note used to be empty.
        self.assertEqual(self._never("pencil4-live.json")["ship-pencil-boxes"],
                         "no one fits its to (closest, pencil-shop, lacks a shipment part)")

    def test_the_comparison_is_named(self):
        # Saved pencil13: mining was allowed only while the miner held less than it asked for.
        self.assertIn("was 20, needed below 1", self._never("pencil13-kept.json")["mine-graphite"])


class RepairBayLiveProofTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(REPAIR_BUNDLE_PATH)
        self.causal = json.loads(REPAIR_CAUSAL_PATH.read_text())

    def test_scripted_baseline_reaches_terminal_through_contention_and_retries(self):
        initial, _, _ = build_engine(self.bundle, self.causal)
        self.assertEqual([initial.discover(a)["total"] for a in ("ava", "bo", "cam", "dee")], [48] * 4)

        trace, engine, model = run_world(
            self.bundle, self.causal, policy="scripted", max_turns=12
        )
        self.assertEqual(
            trace["summary"],
            {
                # 2026-10-21: the least-recent scripted mover brings dee in (no idle worker) for one more round.
                "turns": 6, "terminal_reached": True, "accepted_actions": 11,
                "world_changes": 0, "active_at_end": True, "idle_actors": [],
                "stalled_actors": ["ava", "bo"], "moves_at_end": ["diagnose", "handoff-tool", "repair"],
                "never_offered": {}, "first_turn": 1, "last_turn": 6,
            },
        )
        accepted_kinds = [
            row["did"]["kind"]
            for turn in trace["transcript"]
            for row in turn["actors"].values()
            if row.get("did") and row.get("status") == "accepted"
        ]
        self.assertEqual(accepted_kinds.count("claim-tool"), 3)
        self.assertEqual(accepted_kinds.count("diagnose"), 3)
        self.assertEqual(accepted_kinds.count("repair"), 3)
        self.assertEqual(accepted_kinds.count("handoff-tool"), 2)
        self.assertEqual(
            sum(bool(row.get("retried")) for turn in trace["transcript"] for row in turn["actors"].values()),
            6,
        )
        self.assertEqual(
            sum(row.get("status") == "nothing_left" for turn in trace["transcript"] for row in turn["actors"].values()),
            1,
        )
        for machine_id in ("pump-1", "generator-1", "conveyor-1"):
            self.assertEqual(engine.world.entities[machine_id].component("machine").status, "working")
        self.assertEqual(engine.world.entities["scanner-1"].ownership.owner_ref, "actor:bo")
        self.assertTrue(model.terminal and model.terminal.reached(engine.world))


    def test_a_flag_only_the_move_itself_reads_is_not_an_effect(self):
        # deploy10, 2026-10-16: "discuss concern at meeting" only set its own
        # once-per-meeting flag, yet members chose it in 88% of later rounds.
        rule = lambda mid, kind, reads, writes: types.SimpleNamespace(
            mechanic_id=mid, action_kind=kind, read_paths=reads, write_paths=writes)
        model = types.SimpleNamespace(
            mechanics=[
                rule("discuss", "discuss", ("entities.<actor>.components.work.discuss_done", "entities.<actor>.components.work"),
                     ("entities.<actor>.components.work.discuss_done",)),
                rule("vote", "vote", ("entities.<actor>.components.work.voted",),
                     ("entities.<actor>.components.work.voted", "entities.<actor>.components.member.note")),
            ],
            processes=[types.SimpleNamespace(process_id="tally", read_paths=("entities.<it>.components.work.voted",),
                                             write_paths=()),
                       types.SimpleNamespace(process_id="new-meeting", read_paths=(),
                                             write_paths=("entities.<it>.components.work.discuss_done",))],
            terminal=None,
        )
        found = bookkeeping_fields(model)
        self.assertEqual(found["discuss"], {"components.work.discuss_done"})
        # Read by another rule, or by nothing at all: still a real effect.
        self.assertEqual(found["vote"], set())
        # With no reset the flag changes once and stays changed: a real effect.
        model.processes.pop()
        self.assertEqual(bookkeeping_fields(model)["discuss"], set())

    def test_a_one_way_change_only_its_own_move_reads_stays_on_offer(self):
        # s4c café, 2026-10-29: stacking a chair and mopping the floor were dropped as
        # "bookkeeping", leaving the barista only "knock over".
        kept = json.loads((REPO / "tests/fixtures/cafe-s4-kept.json").read_text())
        _, model, _ = build_engine(kept["bundle"], kept["causal_model"])
        found = bookkeeping_fields(model)
        for kind in ("stack-chair", "mop-floor", "carry-tray"):
            self.assertEqual(found.get(kind, set()), set(), kind)
        trace, _, _ = run_world(kept["bundle"], kept["causal_model"], max_turns=24, trace_id="test/cafe")
        done = {(row.get("did") or {}).get("kind") for turn in trace["transcript"]
                for row in turn["actors"].values() if row.get("changed")}
        self.assertTrue({"stack-chair", "mop-floor"} <= done, done)

    def test_a_move_still_allowed_after_a_stale_revision_is_not_asked_again(self):
        # Every accepted move bumps the revision, so most AI choices in a round are stale by the time they
        # are submitted. A move the rules still allow is retaken at the new revision; only a move that is no
        # longer allowed costs a second AI call (2026-10-16: 183 one-at-a-time re-asks in 40 rounds).
        calls = []

        def fake_choice(engine, actor, page, **_):
            calls.append(actor)
            rows = page["available"]
            return (dict(rows[-1]["action"]) if rows else None), "fake", 0.0

        with patch("scripts.run_authored_world._llm_choice", side_effect=fake_choice):
            trace, _, _ = run_world(self.bundle, self.causal, policy="llm", max_turns=4, trace_id="test/stale")
        rows = [row for turn in trace["transcript"] for row in turn["actors"].values()]
        asked_first = sum(len(turn["actors"]) for turn in trace["transcript"])
        retaken = [row for row in rows if row.get("retried") and not row["lost_what_it_wanted"] and row["status"] == "accepted"]
        asked_again = [row for row in rows if row.get("retried") and (row["lost_what_it_wanted"] or row["status"] == "nothing_left")]
        self.assertTrue(retaken)
        self.assertEqual(len(calls), asked_first + len(asked_again))

    def test_policy_view_shows_installed_authored_effects(self):
        from world_substrate.policy import present

        engine, _, _ = build_engine(self.bundle, self.causal)
        page = engine.discover("ava")
        context = present(engine, "ava", page)
        claim = next(row for row in context["actions"] if "claim-tool" in row["description"])
        self.assertIn("effects:", claim["description"])
        self.assertIn("ownership.owner_ref set 'actor:ava'", claim["description"])
        self.assertIn("hands_free set False", claim["description"])

    def test_live_policy_caps_structured_output_tokens(self):
        engine, _, _ = build_engine(self.bundle, self.causal)
        page = engine.discover("ava")
        captured = {}
        fake = types.ModuleType("llm_client")

        def render_prompt(*args, **kwargs):
            return [{"role": "user", "content": "fixture"}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            captured.update(kwargs)
            action_id = schema["properties"]["action_id"]["enum"][0]
            result = types.SimpleNamespace(cost=0.001)
            return {"action_id": action_id, "reasoning": "choose offered action"}, result

        fake.render_prompt = render_prompt
        fake.call_llm_json_schema = call_llm_json_schema
        with patch.dict(sys.modules, {"llm_client": fake}):
            action, reasoning, cost = _llm_choice(
                engine,
                "ava",
                page,
                world_summary=self.bundle["world"]["summary"],
                model="fixture-model",
                trace_id="fixture-trace",
                max_budget=0.01,
                recent=[],
            )

        self.assertIsNotNone(action)
        self.assertEqual(reasoning, "choose offered action")
        self.assertEqual(cost, 0.001)
        self.assertEqual(captured["max_tokens"], 512)

    def test_concordia_residents_name_belief_and_expected_effect_and_remember_between_rounds(self):
        prompts = []
        fake = types.ModuleType("llm_client")

        def render_prompt(path, **kwargs):
            prompts.append((Path(path).name, kwargs))
            return [{"role": "user", "content": "fixture"}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            self.assertEqual(kwargs["task"], "world-builder-concordia-resident")
            self.assertEqual(schema["required"], ["belief", "action_id", "expected_effect", "work", "reasoning"])
            action_id = schema["properties"]["action_id"]["enum"][0]
            return ({"belief": "The apple is ripe and nobody holds it.", "action_id": action_id,
                     "expected_effect": "I will hold the apple.", "work": "none", "reasoning": "it is my goal"},
                    types.SimpleNamespace(cost=0.001))

        fake.render_prompt = render_prompt
        fake.call_llm_json_schema = call_llm_json_schema
        bundle, causal = load_bundle(BUNDLE_PATH), json.loads(CAUSAL_PATH.read_text())
        # Import Concordia outside patch.dict: leaving it drops modules first imported inside (numpy cannot reload).
        import scripts.concordia_residents  # noqa: F401
        with patch.dict(sys.modules, {"llm_client": fake}):
            first, _, _ = run_world(bundle, causal, policy="resident", model_name="fixture-model",
                                    max_turns=1, trace_id="fixture-trace", briefs={"ava": "Ava wants the apple."})
            row = first["transcript"][0]["actors"]["ava"]
            self.assertEqual(row["belief"], "The apple is ripe and nobody holds it.")
            self.assertEqual(row["expects"], "I will hold the apple.")
            self.assertEqual(first["model"], "llm-resident (Concordia) fixture-model")
            memory = first["resident_memory"]["ava"]
            self.assertTrue(any("you believed: The apple is ripe" in note for note in memory), memory)
            self.assertEqual(prompts[0][0], "concordia_resident_policy.yaml")
            self.assertIn("Ava wants the apple.", [kwargs["brief"] for _, kwargs in prompts])
            # Live play asks one round per request: the next request restores each resident's memory, and the
            # resident reads its own earlier belief and move (repair bay keeps going after round 1).
            bay, bay_causal = load_bundle(REPAIR_BUNDLE_PATH), json.loads(REPAIR_CAUSAL_PATH.read_text())
            one, _, _ = run_world(bay, bay_causal, policy="resident", model_name="fixture-model", max_turns=1)
            prompts.clear()
            two, _, _ = run_world(bay, bay_causal, policy="resident", model_name="fixture-model", max_turns=1,
                                  start_snapshot=one["final_snapshot"], turn_offset=1,
                                  resident_memory=one["resident_memory"])
        self.assertEqual(two["transcript"][0]["turn"], 2)
        # Someone whose choice was taken first and had nothing left still shows the belief behind the choice.
        rows = [row for t in one["transcript"] + two["transcript"] for row in t["actors"].values() if row["wanted"]]
        self.assertIn("nothing_left", [row["status"] for row in rows])
        self.assertTrue(all(row["belief"] and row["expects"] for row in rows), rows)
        self.assertTrue(prompts)
        for _, kwargs in prompts:
            self.assertIn("Round 1: you believed: The apple is ripe", kwargs["memory"])
        for actor, notes in one["resident_memory"].items():
            self.assertEqual(two["resident_memory"][actor][: len(notes)], notes)

    @unittest.skipUnless(importlib.util.find_spec("llm_client"), "llm_client renders the prompt")

    def test_concordia_resident_prompt_renders_memory_and_asks_for_belief(self):
        from llm_client import render_prompt

        from world_substrate.policy import present

        engine, _, _ = build_engine(load_bundle(BUNDLE_PATH), json.loads(CAUSAL_PATH.read_text()))
        context = present(engine, "ava", engine.discover("ava"))
        messages = render_prompt(REPO / "prompts/concordia_resident_policy.yaml", **context, recent=[],
                                 world_summary="orchard", brief="", memory="Round 1: you believed: x")
        text = "\n".join(m["content"] for m in messages)
        self.assertIn("Your memory (what you saw and did, newest last):\nRound 1: you believed: x", text)
        self.assertIn("say what you expect it to change", text)

    def test_summary_names_a_declared_move_nobody_was_ever_offered(self):
        # #166: the pencil wholesaler's only move needed stock no rule ever brought to it.
        causal = json.loads(json.dumps(self.causal))
        mechanic = next(m for m in causal["mechanics"] if m["action_kind"] == "repair")
        mechanic["checks"] = list(mechanic.get("checks") or []) + [
            {"label": "Machine is in an impossible state", "left": {"participant": {"name": "machine", "path": "components.machine.status"}},
             "op": "eq", "right": {"literal": "no-such-status"}}]
        trace, _, _ = run_world(self.bundle, causal, policy="scripted", max_turns=5)
        self.assertIn("repair", trace["summary"]["never_offered"])
        why = trace["summary"]["never_offered"]["repair"]
        self.assertIn("Machine is in an impossible state: was", why)
        self.assertNotIn("is the", why.split(";")[0].lower())  # the closest refusal, not another actor's role check

    def test_a_never_possible_move_names_what_raises_the_state_it_needs(self):
        # 2026-10-18 live pencil ML-LqyMAzAYo: slats were only ever added to the miller's own stock.
        from scripts.run_authored_world import _never_why
        causal = {"mechanics": [
            {"action_kind": "mill-slats", "checks": [], "effects": [
                {"participant": "actor", "path": "components.stock.slats", "op": "add", "value": {"literal": 1}}]},
            {"action_kind": "assemble", "checks": [
                {"label": "enough slats", "left": {"participant": {"name": "actor", "path": "components.stock.slats"}},
                 "op": "gte", "right": {"literal": 1}}], "effects": []}]}
        why = _never_why("assemble", [{"label": "enough slats", "actual": 0, "required": 1}], causal)
        self.assertIn("stock.slats is raised only by mill-slats (on its actor)", why)
        self.assertIn("no action ever brings stock.slats to this actor", why)

    def test_repair_bay_fresh_replay_is_graphical(self):
        trace, _, compiled = run_world(self.bundle, self.causal, policy="scripted", max_turns=12)
        html = render_run(self.bundle, trace, compiled)
        self.assertIn("Scene replay", html)
        self.assertIn("Coolant Pump", html)
        self.assertIn("Diagnostic Scanner", html)
        self.assertIn("Parts Conveyor", html)


if __name__ == "__main__":
    unittest.main()


class ResidentViewTests(unittest.TestCase):
    def test_other_peoples_work_records_are_not_shown(self):
        # 2026-10-18 live Waltzman 1nEGWZzSwHFA: nine other people's done-flags were 30% of a resident prompt.
        from scripts import run_authored_world as raw
        page = {"observation": {"entities": {
            "ana": {"label": "Ana", "components": {"member": {"role": "x"}, "work": {"a_done": True}}},
            "ben": {"label": "Ben", "components": {"member": {"role": "y"}, "work": {"a_done": False}}}}}}
        seen = {}
        with patch.object(raw, "present", lambda engine, actor, p: seen.update(p) or {}):
            raw._view(None, "ana", page)
        entities = seen["observation"]["entities"]
        self.assertIn("work", entities["ana"]["components"])
        self.assertEqual(set(entities["ben"]["components"]), {"member"})
        self.assertIn("work", page["observation"]["entities"]["ben"]["components"])  # the engine's page is untouched


class ResidentViewTests(unittest.TestCase):
    """pencil8 (evidence/pencil8-trace-audit/): what the factory was shown after round 4."""

    def _engine(self):
        from scripts.run_authored_world import _view, _without_no_ops, live_fields
        world = json.loads((Path(__file__).parent / "fixtures" / "pencil8-live.json").read_text())
        for entity in world["bundle"]["entities"]:
            if entity["id"] in world["after_round_4"]:
                entity["components"] = world["after_round_4"][entity["id"]]
        engine, model, _ = build_engine(world["bundle"], world["causal_model"])
        page = _without_no_ops(engine, engine.discover("factory"), bookkeeping=bookkeeping_fields(model))
        return _view(engine, "factory", page), _view(engine, "factory", page, live_fields(model))

    def test_zeros_no_rule_touches_are_hidden(self):
        old, new = self._engine()
        for stray in ("leads 0", "slats 0", "rounds_left 0"):
            self.assertIn(stray, old["actor_state"])
            self.assertNotIn(stray, new["actor_state"])
        self.assertIn("pencils 0", new["actor_state"])  # assembly writes it, so it stays
        self.assertIn("packed_pencils 10", new["actor_state"])

    def test_own_fields_are_shown_under_their_component(self):
        # pencil12 oRfOptv0O3f3: the shop read its price "packed_pencils 20" as stock it held
        from scripts.run_authored_world import _view, _without_no_ops, live_fields
        world = json.loads((Path(__file__).parent / "fixtures" / "pencil12-live.json").read_text())
        engine, model, _ = build_engine(world["bundle"], world["causal_model"])
        page = _without_no_ops(engine, engine.discover("shop"), bookkeeping=bookkeeping_fields(model))
        state = _view(engine, "shop", page, live_fields(model))["actor_state"]
        parts = dict(part.split(": ", 1) for part in state.split("; "))
        self.assertEqual(parts["business"], "cash 1000")
        self.assertIn("packed_pencils 20", parts["prices"])
        self.assertNotIn("packed_pencils", parts["stocks"])

    def test_offered_move_shows_what_it_draws_on_out_of_sight(self):
        _, new = self._engine()
        assemble = [a["description"] for a in new["actions"] if a["description"].startswith("assemble-pencils")]
        self.assertTrue(assemble)
        self.assertIn("[now, out of sight: mill stock.slats is 15; lead-maker stock.leads is 11]", assemble[0])
