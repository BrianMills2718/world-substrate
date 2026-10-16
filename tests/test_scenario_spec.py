"""ScenarioSpecV1, ported from Cybernetic Influence v3 (docs/plans/scenario_spec_adoption.md, check S1).

Input is the recorded Cybernetic Influence pencil draft (draft_49524bf20017, approved 2026-10-07), copied from the
VPS to spikes/any-scenario-2026-10/evidence/scenario-spec/pencil_draft.json; its people are invented.
"""
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPIKE = REPO / "spikes/any-scenario-2026-10"
sys.path.insert(0, str(SPIKE))

from pydantic import ValidationError  # noqa: E402
from scenario_spec import ScenarioSpecV1, from_donor_scenario  # noqa: E402

DRAFT = json.loads((SPIKE / "evidence/scenario-spec/pencil_draft.json").read_text())
DONOR = DRAFT["proposal"]["scenario"]


def _minimal(**over):
    spec = {
        "scenario_id": "concern_demo", "title": "Concern demo", "description": "A group raises a concern.",
        "people": [
            {"entity_id": "legal_group", "label": "Legal group", "position": "Legal advisers",
             "disposition": "Careful", "memories": ["Saw a data-sharing clause conflict."],
             "behavioral_profile": {"goals": ["Get the clause fixed before activation."]}},
            {"entity_id": "country_b", "label": "Country B", "position": "Member", "disposition": "Supportive",
             "memories": ["Voted for the pilot."], "behavioral_profile": {}},
        ],
        "information_items": [
            {"representation_id": "clause_conflict", "content": "Clause 4 conflicts with national law.",
             "apparent_source": "Legal group", "holder_id": "legal_group", "channel_id": "legal_channel",
             "recipient_ids": ["country_b"]},
        ],
        "behaviors": [{"request_id": "raise_concern", "subject_refs": ["legal_group", "clause_conflict"],
                       "behavior_description": "The legal group sends its concern.",
                       "desired_effects": ["Country B knows the concern."], "fidelity_need": "exact",
                       "causally_material": True}],
        "fidelity_assumptions": ["One concern."],
    }
    spec.update(over)
    return spec


class DonorDraftTests(unittest.TestCase):
    def test_recorded_pencil_draft_reads_with_people_and_profiles(self):
        spec = from_donor_scenario(DONOR)
        self.assertEqual([p.entity_id for p in spec.people], ["maya_chen", "elena_ruiz", "owen_brooks"])
        maya = spec.people[0]
        self.assertTrue(maya.behavioral_profile.goals and maya.behavioral_profile.decision_tendencies)
        self.assertEqual(len(spec.world_records), len(DONOR["world_records"]))

    def test_unported_donor_parts_are_listed_not_dropped(self):
        spec = from_donor_scenario(DONOR)
        self.assertIn("donor part not ported: resource_extension", spec.unsupported)
        self.assertTrue(any(u.startswith("behavior transport_pencils_request: subjects in unported parts")
                            for u in spec.unsupported))


class ContractTests(unittest.TestCase):
    def test_minimal_concern_scenario_is_valid(self):
        spec = ScenarioSpecV1.model_validate(_minimal())
        self.assertEqual(spec.information_items[0].recipient_ids, ["country_b"])

    def test_undeclared_recipient_is_refused(self):
        bad = _minimal()
        bad["information_items"][0]["recipient_ids"] = ["country_z"]
        with self.assertRaisesRegex(ValidationError, "undeclared recipients"):
            ScenarioSpecV1.model_validate(bad)

    def test_item_sent_to_its_own_holder_is_refused(self):
        bad = _minimal()
        bad["information_items"][0]["recipient_ids"] = ["legal_group"]
        with self.assertRaisesRegex(ValidationError, "sent to its own holder"):
            ScenarioSpecV1.model_validate(bad)

    def test_unknown_field_is_refused(self):
        bad = _minimal()
        bad["people"] = deepcopy(bad["people"])
        bad["people"][0]["mood"] = "tense"
        with self.assertRaises(ValidationError):
            ScenarioSpecV1.model_validate(bad)


def _two_recipient_spec():
    spec = _minimal(scheduled_moments=[{"moment_id": "weekly_meeting", "tick": 2, "every_ticks": 3,
                                        "description": "Partnership meeting"}])
    spec["people"].append({"entity_id": "country_c", "label": "Country C", "position": "Member",
                           "disposition": "Cautious", "memories": ["Asked about data rules."],
                           "behavioral_profile": {}})
    spec["information_items"][0]["recipient_ids"] = ["country_b", "country_c"]
    spec["behaviors"].append({"request_id": "concern_slows_meeting", "subject_refs": ["clause_conflict", "weekly_meeting"],
                              "behavior_description": "Considering the concern uses meeting time.",
                              "desired_effects": ["The meeting runs longer."], "fidelity_need": "coarse",
                              "causally_material": True})
    spec["behaviors"].append({"request_id": "meeting_slows", "subject_refs": ["weekly_meeting"],
                              "behavior_description": "Concerns slow the meeting.",
                              "desired_effects": ["Less time for decisions."], "fidelity_need": "coarse",
                              "causally_material": True})
    return ScenarioSpecV1.model_validate(spec)


class CompilerTests(unittest.TestCase):  # S2
    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        from scaffold_world import validate_bundle
        from scripts.run_authored_world import build_engine
        self.bundle, self.causal, self.coverage = compile_spec(_two_recipient_spec())
        validate_bundle(self.bundle)
        self.engine, _, _ = build_engine(self.bundle, self.causal)

    def _status(self, eid):
        return self.engine.world.entities[eid].as_dict()["components"]["delivery"]["status"]

    def test_one_information_entity_and_pending_delivery_per_recipient(self):
        infos = [e for e in self.bundle["entities"] if "information" in e["categories"]]
        self.assertEqual(sorted(e["id"] for e in infos),
                         ["info-clause-conflict-to-country-b", "info-clause-conflict-to-country-c"])
        self.assertTrue(all(e["components"]["information"]["topic"] == "clause_conflict" for e in infos))
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-b"), "pending")

    def test_one_communicate_event_delivers_to_exactly_its_recipient(self):
        offered = [a["action"] for a in self.engine.discover("legal-group")["available"]]
        to_b = next(a for a in offered if a["recipient"] == "country-b")
        result = self.engine.submit(dict(to_b, controller="test"))
        self.assertEqual(result["status"], "accepted")
        changed = {c["path"] for c in result["event"]["changes"]}
        self.assertIn("entities.delivery-info-clause-conflict-to-country-b.components.delivery.status", changed)
        self.assertIn("entities.country-b.components.member.aware", changed)
        self.assertFalse([p for p in changed if "country-c" in p])
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-b"), "delivered")
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-c"), "pending")

    def test_only_the_holder_is_offered_communicate(self):
        self.assertEqual(self.engine.discover("country-b")["available"], [])

    def test_scheduled_moment_occurs_on_its_ticks(self):
        from world_substrate.mechanisms.time import ClockAdvanceProcess
        self.engine.registry.register_process(ClockAdvanceProcess())
        ticks = []
        for _ in range(9):
            if any(e["rule_id"] == "moment-occurs" for e in self.engine.advance(1)["events"]):
                ticks.append(self.engine.world.tick)
        self.assertEqual(ticks, [2, 5, 8])

    def test_a_moment_is_happening_only_in_the_round_after_it_occurs(self):
        # inc15a: every rule gated on "ticks_until == 0" never passed, because the tick that reaches 0 restarts it.
        from world_substrate.mechanisms.time import ClockAdvanceProcess
        self.engine.registry.register_process(ClockAdvanceProcess())
        on = []
        for _ in range(9):
            self.engine.advance(1)
            moment = self.engine.world.entities["weekly-meeting"].as_dict()["components"]["moment"]
            self.assertNotEqual(moment["ticks_until"], 0)  # what people see when they act
            if moment["happening_now"]:
                on.append(self.engine.world.tick)
        self.assertEqual(on, [2, 5, 8])

    def test_a_meeting_due_check_is_rewritten_to_one_that_can_pass(self):
        from spec_pipeline import fix_moment_due_checks
        ref = {"participant": {"name": "weekly_meeting", "path": "components.moment.ticks_until"}}
        causal = {"mechanics": [{"mechanic_id": "raise", "checks": [
            {"label": "the weekly meeting is due", "left": ref, "op": "eq", "right": {"literal": 0}},
            {"label": "the meeting is ahead", "left": ref, "op": "gt", "right": {"literal": 0}}]}]}
        fixed_causal, fixed = fix_moment_due_checks(causal)
        due, ahead = fixed_causal["mechanics"][0]["checks"]
        self.assertEqual(due["left"]["participant"]["path"], "components.moment.happening_now")
        self.assertEqual(due["right"], {"literal": True})
        self.assertEqual(ahead["left"]["participant"]["path"], "components.moment.ticks_until")  # untouched
        self.assertEqual(len(fixed), 1)

    def test_coverage_marks_delivery_exact_and_the_rest_for_the_generator(self):
        rows = {r["request_id"]: r["classification"] for r in self.coverage["rows"]}
        # mentioning an item does not make a behavior delivery: the concern slowing a meeting needs its own rules
        self.assertEqual(rows, {"raise_concern": "exact", "concern_slows_meeting": "to_generate",
                                "meeting_slows": "to_generate"})

    def test_communicate_rule_is_the_reviewed_one_unchanged(self):
        reviewed = json.loads((REPO / "examples/native_coordination/coordination-causal-v0.json").read_text())
        self.assertEqual(self.causal["mechanics"][0], reviewed["mechanics"][0])


PIPELINE1 = SPIKE / "evidence/waltzman-spec/pipeline1"  # pipeline run waltzman-spec-20261008T163904 (audit 2026-10-08)


def _decision_spec(**decision):
    spec = json.loads(_two_recipient_spec().model_dump_json())
    spec["scheduled_moments"].append({"moment_id": "deadline", "tick": 3, "description": "Decision deadline"})
    spec["decision"] = {"decision_id": "activate", "question": "Activate the system?",
                        "decider_ids": ["country_b", "country_c"], "supporters_at_start": ["country_b", "country_c"],
                        "support_needed": 2, "deadline_moment_id": "deadline", "max_postponements": 1,
                        "postpone_ticks": 2, **decision}
    return spec


class GroupDecisionTests(unittest.TestCase):
    """The compiled group decision: support moves both ways on a named concern and the deadline settles it.
    2026-10-16 Waltzman inc15c-e: generated rules left support only falling and the decision never ending."""

    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        from scaffold_world import validate_bundle
        from scripts.run_authored_world import build_engine
        from world_substrate.mechanisms.time import ClockAdvanceProcess
        self.compile, self.build = compile_spec, build_engine
        self.bundle, self.causal, _ = compile_spec(ScenarioSpecV1.model_validate(_decision_spec()))
        validate_bundle(self.bundle)
        self.engine, _, _ = build_engine(self.bundle, self.causal)
        self.engine.registry.register_process(ClockAdvanceProcess())

    def test_compiled_processes_leave_room_for_a_full_generated_set(self):
        # 2026-10-16 Waltzman inc15f: 3 moment + 3 deadline processes filled the engine's old bound of 6, so any
        # generated process made the build fail with "processes must be a list of at most 6".
        from world_substrate.action_authoring import MAX_PROCESSES
        from scripts.generate_causal_model import causal_model_schema
        generated_max = causal_model_schema(self.bundle)["properties"]["processes"]["maxItems"]
        self.assertLessEqual(len(self.causal["processes"]) + generated_max, MAX_PROCESSES)

    def test_the_rule_writer_is_asked_only_for_actions_no_compiled_rule_covers(self):
        # 2026-10-16 inc15h (luna): asked for every action, compiled ones included, it returned a mismatched list.
        from unittest.mock import patch
        from scripts import people_world
        bundle = dict(self.bundle, actions=self.bundle["actions"] + [
            {"kind": "inspect-site", "description": "Inspect a site.", "fields": []}])
        prepared = {"spec": ScenarioSpecV1.model_validate(_decision_spec()), "bundle": bundle, "compiled": self.causal,
                    "coverage": {"rows": []}, "sigs": []}
        seen = []

        def stop(b, **_):
            seen.extend(a["kind"] for a in b["actions"])
            raise RuntimeError("stop")
        with patch.object(people_world, "generate_causal_model", side_effect=stop), \
                self.assertRaisesRegex(RuntimeError, "stop"):
            people_world.write_people_rules(prepared, trace_id="t", max_budget=0.0, progress=lambda *a: None)
        self.assertEqual(seen, ["inspect-site"])

    def test_an_action_whose_rule_only_wrote_compiled_parts_leaves_the_world(self):
        # 2026-10-16 inc15j (luna): reconsider-settled-issue only set a concern's status; the merge removed its rule
        # and the build failed because the action had none.
        import copy
        from unittest.mock import patch
        from scripts import people_world
        bundle = dict(self.bundle, actions=self.bundle["actions"] + [
            {"kind": "inspect-site", "description": "Inspect a site.", "fields": []}])
        prepared = {"spec": ScenarioSpecV1.model_validate(_decision_spec()), "bundle": bundle, "compiled": self.causal,
                    "coverage": {"rows": []}, "sigs": []}
        writer = next(m for m in self.causal["mechanics"]
                      if any(e["path"].startswith("components.concern.") for e in m["effects"]))
        generated = {"mechanics": [dict(copy.deepcopy(writer), action_kind="inspect-site", mechanic_id="inspect-site",
                                        effects=[e for e in copy.deepcopy(writer["effects"])
                                                 if e["path"].startswith("components.concern.")])],
                     "processes": [], "terminal": None}
        with patch.object(people_world, "generate_causal_model", return_value=(generated, None)):
            world = people_world.write_people_rules(prepared, trace_id="t", max_budget=0.0, progress=lambda *a: None)
        self.assertNotIn("inspect-site", [a["kind"] for a in world["bundle"]["actions"]])
        self.assertTrue(any("inspect-site removed" in d for d in world["dropped_generated_rules"]))

    def _decision(self):
        return self.engine.world.entities["activate"].as_dict()["components"]["group_decision"]

    def _do(self, actor, kind, **fields):
        offered = [a["action"] for a in self.engine.discover(actor)["available"] if a["action"]["kind"] == kind]
        match = [a for a in offered if all(a.get(k) == v for k, v in fields.items())]
        self.assertTrue(match, f"{actor} is not offered {kind} {fields}; offered {offered}")
        result = self.engine.submit(dict(match[0], controller="test"))
        self.assertEqual(result["status"], "accepted", result)
        return result

    def _offered(self, actor, kind):
        return [a["action"] for a in self.engine.discover(actor)["available"] if a["action"]["kind"] == kind]

    def _remedy_runs(self, matter):
        """A started remedy is under way, not done: the concern resolves REMEDY_TICKS rounds later."""
        from compile_spec import REMEDY_TICKS
        self.assertEqual(self._offered("country-b", "restore-full-support"), [])
        self.engine.advance(REMEDY_TICKS)
        status = self.engine.world.entities[matter].as_dict()["components"]["concern"]["status"]
        self.assertEqual(status, "resolved")

    def _until_deadline(self):
        from compile_spec import MIN_DECISION_TICKS
        for _ in range(MIN_DECISION_TICKS + 2):
            events = self.engine.advance(1)["events"]
            ids = [e["rule_id"] for e in events]
            if any(i.startswith("decision-") for i in ids):
                return ids
        self.fail("the deadline never settled anything")

    def test_support_waits_on_a_received_concern_and_returns_once_it_is_resolved(self):
        matter = "info-clause-conflict-to-country-b"
        self.assertEqual(self._offered("country-b", "make-support-conditional"), [])  # nothing received yet
        self._do("legal-group", "communicate", recipient="country-b")
        self._do("country-b", "make-support-conditional", matter=matter)
        self.assertEqual((self._decision()["support"], self._decision()["conditional"]), (1, 1))
        self.assertEqual(self._offered("country-b", "restore-full-support"), [])  # concern still open
        self.assertEqual(self._offered("country-c", "resolve-concern"), [])  # only the holder resolves
        self._do("legal-group", "resolve-concern", matter=matter)
        self._remedy_runs(matter)
        self.assertEqual(self._offered("legal-group", "reopen-concern"), [])  # the one who fixed it does not undo it
        self._do("country-b", "restore-full-support", matter=matter)
        self.assertEqual((self._decision()["support"], self._decision()["conditional"]), (2, 0))
        self._do("country-b", "reopen-concern", matter=matter)  # and it can fall again
        self._do("country-b", "make-support-conditional", matter=matter)
        self.assertEqual(self._decision()["support"], 1)

    def test_the_person_a_concern_reached_can_resolve_it_on_their_own_side(self):
        matter = "info-clause-conflict-to-country-b"
        self._do("legal-group", "communicate", recipient="country-b")
        self._do("country-b", "make-support-conditional", matter=matter)
        self.assertEqual(self._offered("country-c", "resolve-own-concern"), [])  # not the one it reached
        self._do("country-b", "resolve-own-concern", matter=matter)
        self._remedy_runs(matter)
        self._do("country-b", "restore-full-support", matter=matter)
        self.assertEqual((self._decision()["support"], self._decision()["conditional"]), (2, 0))

    def test_short_support_postpones_at_the_deadline_then_enough_support_authorizes(self):
        matter = "info-clause-conflict-to-country-b"
        self._do("legal-group", "communicate", recipient="country-b")
        self._do("country-b", "make-support-conditional", matter=matter)
        self._do("legal-group", "resolve-concern", matter=matter)  # the remedy runs while the deadline nears
        self.assertIn("decision-postponed-at-deadline", self._until_deadline())
        self.assertEqual((self._decision()["status"], self._decision()["postponements"]), ("open", 1))
        self._do("country-b", "restore-full-support", matter=matter)
        self.assertIn("decision-authorized-at-deadline", self._until_deadline())
        self.assertEqual(self._decision()["status"], "authorized")
        self.assertEqual(self._offered("country-b", "make-support-conditional"), [])  # settled stays settled

    def test_concerns_delay_and_block_deployment_after_authorization(self):
        # 2026-10-16 Waltzman stance1: authorization ended the story in round 4; the texts say concerns "delay or
        # block deployment", so an authorized decision deploys over rounds that a reopened concern can stop.
        from compile_spec import DEPLOY_TICKS
        matter = "info-clause-conflict-to-country-b"
        self._do("legal-group", "communicate", recipient="country-b")
        self._do("country-b", "resolve-own-concern", matter=matter)
        self.assertIn("decision-authorized-at-deadline", self._until_deadline())
        self.assertEqual((self._decision()["status"], self._decision()["deploy_ticks_left"]), ("authorized", DEPLOY_TICKS))
        self._do("country-b", "reopen-concern", matter=matter)
        self._do("country-b", "make-support-conditional", matter=matter)
        ids = [e["rule_id"] for e in self.engine.advance(1)["events"]]
        self.assertIn("authorization-withdrawn", ids)  # full support fell below the threshold
        self.assertEqual(self._decision()["status"], "open")
        self._do("country-b", "resolve-own-concern", matter=matter)
        self.engine.advance(2)
        self._do("country-b", "restore-full-support", matter=matter)
        self.assertIn("decision-authorized-at-deadline", self._until_deadline())
        ids = []
        for _ in range(DEPLOY_TICKS + 1):
            ids += [e["rule_id"] for e in self.engine.advance(1)["events"]]
        self.assertIn("deployment-progresses", ids)
        self.assertIn("deployment-completes", ids)
        self.assertEqual(self._decision()["status"], "deployed")
        self.assertEqual(self._offered("country-b", "reopen-concern"), [])  # deployed stays deployed

    def test_short_support_with_no_postponements_left_rejects_at_the_deadline(self):
        self._do("legal-group", "communicate", recipient="country-b")
        self._do("country-b", "make-support-conditional", matter="info-clause-conflict-to-country-b")
        self._until_deadline()
        self.assertIn("decision-rejected-at-deadline", self._until_deadline())
        self.assertEqual(self._decision()["status"], "rejected")

    def test_generated_rules_cannot_write_the_decision(self):
        from spec_pipeline import merge_causal
        generated = {"mechanics": [{"mechanic_id": "x", "action_kind": "vote", "effects": [
            {"participant": "d", "path": "components.group_decision.status", "op": "set", "value": {"literal": "authorized"}}]}],
            "processes": []}
        merged, dropped = merge_causal(self.causal, generated)
        self.assertNotIn("vote", [m["action_kind"] for m in merged["mechanics"]])
        self.assertTrue(dropped)

    def test_a_decision_naming_undeclared_people_is_refused(self):
        with self.assertRaisesRegex(ValidationError, "undeclared people"):
            ScenarioSpecV1.model_validate(_decision_spec(decider_ids=["country_z"]))


class RecordedPipelineRepairTests(unittest.TestCase):
    """Defects the audit found in that run, checked against its recorded files."""

    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        self.spec = ScenarioSpecV1.model_validate_json((PIPELINE1 / "scenario_spec.json").read_text())
        _, self.compiled, self.coverage = compile_spec(self.spec)
        self.recorded = json.loads((PIPELINE1 / "causal.json").read_text())
        self.model = json.loads((PIPELINE1 / "model.json").read_text())

    def test_generated_rules_may_not_write_moment_countdowns(self):
        from spec_pipeline import merge_causal
        generated = {**self.recorded,
                     "mechanics": [m for m in self.recorded["mechanics"] if m["action_kind"] != "communicate"],
                     "processes": [p for p in self.recorded["processes"]
                                   if p["process_id"] not in ("moment-passes", "moment-countdown", "moment-occurs")]}
        merged, dropped = merge_causal(self.compiled, generated)
        writers = [p["process_id"] for p in merged["processes"]
                   if any(e["path"].startswith("components.moment.") for e in p["effects"])]
        self.assertEqual(writers, ["moment-passes", "moment-countdown", "moment-occurs"])
        self.assertIn("generated process advance-scheduled-moments dropped: it writes what a compiled rule owns",
                      dropped)

    def test_actions_get_fields_for_their_behaviors_records(self):
        from spec_pipeline import record_fields
        sigs = {a["kind"]: [f["name"] for f in a["fields"]] for a in record_fields(self.spec,
                                                                                   self.model["action_signatures"])}
        self.assertIn("member_support", sigs["make-support-conditional"])
        self.assertIn("meeting_progress", sigs["reopen-settled-issue"])

    def test_generated_actions_never_declare_fields_the_engine_fills(self):
        # 2026-10-16: an action declared "actor" and the Waltzman build failed with "reserved/duplicate action field".
        import types
        from unittest.mock import patch
        import spec_pipeline
        bundle, _, coverage = spec_pipeline.compile_spec(self.spec)
        rows = [r for r in coverage["rows"] if r["classification"] == "to_generate"]
        self.assertTrue(rows)
        reply = spec_pipeline.ActionSignatures.model_validate({"actions": [{
            "kind": "address_concern", "description": "Address a raised concern", "for_behaviors": [rows[0]["request_id"]],
            "fields": [{"name": "actor", "type": "entity_ref"}, {"name": "concern", "type": "entity_ref"},
                       {"name": "concern", "type": "entity_ref"}, {"name": "base_revision", "type": "integer"}]}]})
        fake = types.SimpleNamespace(call_llm_structured=lambda *a, **k: (reply, None))
        with patch.dict(sys.modules, {"llm_client": fake}):
            sigs, _ = spec_pipeline.action_signatures(self.spec, bundle, coverage, model="m", trace_id="t")
        self.assertEqual([f["name"] for f in sigs[0]["fields"]], ["concern"])

    def test_coverage_counts_rules_that_change_records_not_names(self):
        from spec_pipeline import behavior_coverage
        cov = behavior_coverage(self.spec, self.model["action_signatures"], self.recorded, deepcopy(self.coverage))
        rows = {r["request_id"]: r for r in cov["rows"]}
        self.assertEqual(rows["raise_local_concerns"]["classification"], "exact")
        self.assertEqual(rows["make_support_conditional"]["classification"], "unsupported")  # was reported coarse
        self.assertIn("member_support", rows["make_support_conditional"]["why"])


RUN2 = SPIKE / "evidence/waltzman-spec/run2"  # pipeline run waltzman-spec-20261008T174927, agent run run-20261008T184545


def _run2_events():
    import gzip
    with gzip.open(RUN2 / "run/events.jsonl.gz", "rt") as fh:
        return [json.loads(line) for line in fh if line.strip()]


class RecordedWaltzmanRunTests(unittest.TestCase):  # S5/S6: claims in the Assessment, against the recorded run
    def setUp(self):
        self.events = _run2_events()
        self.attempts = [json.loads(x) for x in (RUN2 / "run/attempts.jsonl").read_text().splitlines() if x.strip()]

    def _changes(self, event_id):
        e = next(e for e in self.events if e["event_id"] == event_id)
        return {c["path"]: (c["before"], c["after"]) for c in e["changes"]}

    def test_each_group_delivers_its_concern_to_exactly_one_country(self):
        sends = [e for e in self.events if e["rule_id"] == "coordination.action.communicate"]
        self.assertEqual(len(sends), 4)
        for e in sends:
            aware = [p for p in self._changes(e["event_id"]) if p.endswith(".components.member.aware")]
            self.assertEqual(len(aware), 1, e["event_id"])
        self.assertEqual(self._changes("e00006")["entities.delivery-info-legal-concern-to-country-two.components.delivery.status"],
                         ("pending", "delivered"))

    def test_country_two_makes_support_conditional_citing_the_concern_only_it_received(self):
        a = next(x for x in self.attempts if (x.get("performed") or {}).get("event_id") == "e00015")
        self.assertEqual(a["actor"], "country-two")
        self.assertTrue(any("to country_two" in c for c in a["cited_observations"]))
        self.assertEqual(self._changes("e00015")["entities.member-support.components.member_support.conditional_support_count"],
                         (1, 2))

    def test_reopened_issue_sets_progress_back(self):
        ch = self._changes("e00025")
        self.assertEqual(ch["entities.meeting-progress.components.meeting_progress.progress_percent"], (60, 50))
        self.assertEqual(ch["entities.meeting-progress.components.meeting_progress.settled_issues_reopened"], (0, 1))

    def test_every_agent_was_briefed_with_its_own_profile(self):
        briefed = {x["actor"] for x in self.attempts if x.get("brief")}
        self.assertEqual(briefed, {x["actor"] for x in self.attempts})
        legal = next(x for x in self.attempts if x["actor"] == "legal-group")
        self.assertIn("Legal", legal["brief"])

    def test_the_recorded_block_used_the_weekly_meeting_as_its_deadline(self):
        e = next(e for e in self.events if e["event_id"] == "e00047")
        check = next(c for c in e["checks"] if c["label"] == "the decision deadline has occurred")
        self.assertEqual(check["actual"], 5)  # occurrences of the weekly meeting; the deadline had occurred 0 times

    def test_pinned_slots_refuse_the_meeting_as_the_deadline(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        from scripts.run_authored_world import build_engine
        from spec_pipeline import pin_named_slots
        spec = ScenarioSpecV1.model_validate_json((RUN2 / "scenario_spec.json").read_text())
        bundle, _, _ = compile_spec(spec)
        recorded = json.loads((RUN2 / "run/bundle_after_run.json").read_text())
        bundle["actions"] = recorded["actions"]
        bundle["components"] = recorded["components"]
        for entity in bundle["entities"]:  # the recorded run predates the moment's happening_now field
            entity["components"].get("moment", {}).pop("happening_now", None)
        causal, pinned = pin_named_slots(spec, json.loads((RUN2 / "run/causal_after_run.json").read_text()))
        self.assertIn("block-at-deadline-for-missing-support.activation_decision_deadline -> activation-decision-deadline",
                      pinned)
        engine, _, _ = build_engine(bundle, causal)
        page = engine.discover("partnership", kind="block-deployment")
        slots = {r["action"]["activation_decision_deadline"] for r in page["available"] + page["blocked"]}
        self.assertEqual(slots, {"activation-decision-deadline"})


if __name__ == "__main__":
    unittest.main(verbosity=2)


class WorkCycleTests(unittest.TestCase):
    """compile_spec.add_work_cycle: routine work recurs (2026-10-16 Waltzman deploy4 went still after round 5)."""

    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]

    def _engine(self, spec):
        from compile_spec import add_work_cycle, compile_spec
        from scripts.run_authored_world import build_engine
        bundle, causal, _ = compile_spec(spec)
        bundle["actions"].append({"kind": "file-report", "description": "File a routine report.", "fields": []})
        cycle = add_work_cycle(spec, bundle, causal, ["file-report"])
        flag = "components.work.file_report_done"
        causal["mechanics"].append({
            "schema_version": "world-substrate-action-mechanic/v0", "mechanic_id": "file-report", "version": "1",
            "action_kind": "file-report", "rationale": "Once per cycle.",
            "actor_selector": {"categories": ["member"], "components": ["work"]}, "participants": {}, "parameters": {},
            "checks": [{"label": "not filed this cycle", "left": {"participant": {"name": "actor", "path": flag}},
                        "op": "eq", "right": {"literal": False}}],
            "effects": [{"participant": "actor", "path": flag, "op": "set", "value": {"literal": True}}],
            "limits": ["test"], "tests": ["test"], "semantic_bindings": ["test"]})
        engine, _, _ = build_engine(bundle, causal)
        return engine, cycle

    def _offered(self, engine):
        return [a["action"] for a in engine.discover("legal-group")["available"] if a["action"]["kind"] == "file-report"]

    def _report_again_after_cycle(self, engine):
        self.assertEqual(engine.submit(dict(self._offered(engine)[0], controller="test"))["status"], "accepted")
        self.assertEqual(self._offered(engine), [])
        for _ in range(8):
            if any(e["rule_id"] == "work-cycle-restarts" for e in engine.advance(1)["events"]):
                break
        else:
            self.fail("the work cycle never restarted")
        self.assertEqual(len(self._offered(engine)), 1)

    def test_the_scenarios_repeating_meeting_clears_done_work(self):
        engine, cycle = self._engine(_two_recipient_spec())
        self.assertEqual(cycle["cycle_id"], "weekly-meeting")
        self.assertEqual(cycle["flags"], {"file-report": "file_report_done"})
        self._report_again_after_cycle(engine)

    def test_without_a_repeating_moment_a_work_cycle_is_added(self):
        engine, cycle = self._engine(ScenarioSpecV1.model_validate(_minimal()))
        self.assertEqual(cycle["cycle_id"], "work-cycle")
        self._report_again_after_cycle(engine)

    def test_a_meeting_every_round_is_too_short_to_be_the_work_cycle(self):
        spec = _two_recipient_spec().model_copy(deep=True)
        spec.scheduled_moments[0].every_ticks = 1
        _, cycle = self._engine(spec)
        self.assertEqual(cycle["cycle_id"], "work-cycle")

    def test_a_rule_without_the_limit_gets_it(self):
        from compile_spec import limit_to_work_cycle
        rule = {"action_kind": "file-report", "checks": [], "effects": []}
        cycle = {"flags": {"file-report": "file_report_done"}}
        limited = limit_to_work_cycle([rule], cycle)[0]
        path = "components.work.file_report_done"
        self.assertEqual([c["left"]["participant"]["path"] for c in limited["checks"]], [path])
        self.assertEqual([(e["path"], e["value"]) for e in limited["effects"]], [(path, {"literal": True})])
        self.assertEqual(limit_to_work_cycle([limited], cycle)[0], limited)  # already limited: unchanged
        self.assertEqual(rule["checks"], [])  # the writer's rule is not edited in place
