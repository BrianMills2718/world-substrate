"""The independent rules review (docs/plans/declared_laws.md, piece 3, slice S3, check L4).

The reviewer's request holds only the description, the laws and the compiled rules, on another model family than the
rules writer, and its reply is a findings list, never a pass mark. The live call is checked in
evidence/declared-laws/s3-review-choice/ and evidence/declared-laws/s3-pencil/; here llm_client is faked.
"""
from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts import review_rules as reviewer  # noqa: E402
from scripts.generate_causal_model import DEFAULT_MODEL  # noqa: E402

PENCIL13 = json.loads((REPO / "tests/fixtures/pencil13-kept.json").read_text())


class ReviewTests(unittest.TestCase):
    def test_findings_on_unknown_rules_or_with_no_problem_are_dropped(self):
        ids = ["buy-boxes", "sell-pencil"]
        reply = {"findings": [
            {"rule_id": "buy-boxes", "description_words": "buys boxes", "problem": "No money moves."},
            {"rule_id": "made-up", "description_words": "", "problem": "Not a rule."},
            {"rule_id": "missing", "description_words": "glue", "problem": "Nothing supplies glue."},
            {"rule_id": "sell-pencil", "description_words": "", "problem": "  "},
        ]}
        self.assertEqual([f["rule_id"] for f in reviewer.read_findings(reply, ids)], ["buy-boxes", "missing"])
        with self.assertRaises(ValueError):
            reviewer.read_findings({"verdict": "pass"}, ids)

    def test_the_request_holds_only_description_laws_rules_and_starting_values_on_another_family(self):
        sent = {}

        def fake_call(model, messages, schema, **kwargs):
            sent.update(model=model, messages=messages, schema=schema, **kwargs)
            return {"findings": [{"rule_id": "buy-boxed-pencils", "description_words": "ship them to shops",
                                  "problem": "The purchase moves the boxes and no money."}]}, types.SimpleNamespace(cost=0.05)

        fake = types.ModuleType("llm_client")
        fake.call_llm_json_schema = fake_call
        fake.render_prompt = lambda path, **values: [{"role": "user", "content": json.dumps(values)}]
        bundle = {**PENCIL13["bundle"], "resources": [{"resource_id": "cash"}], "laws": [{"law_id": "sale"}]}
        with patch.dict(sys.modules, {"llm_client": fake}):
            found, cost = reviewer.review_rules(PENCIL13["description"], bundle, PENCIL13["causal_model"],
                                                trace_id="t", max_budget=0.5)
        self.assertEqual(found[0]["rule_id"], "buy-boxed-pencils")
        self.assertEqual(cost, 0.05)
        values = json.loads(sent["messages"][0]["content"])
        self.assertEqual(sorted(values), ["description", "laws", "rules", "start"])
        self.assertEqual(sorted(json.loads(values["laws"])), ["laws", "resources"])
        self.assertEqual(sorted(json.loads(values["rules"])), ["mechanics", "processes"])
        self.assertNotIn("entities", values["laws"] + values["rules"])
        start = json.loads(values["start"])
        self.assertEqual(sorted(start), sorted(e["id"] for e in PENCIL13["bundle"]["entities"]))
        self.assertNotEqual(sent["model"].split("/")[1], DEFAULT_MODEL.split("/")[1])
        self.assertIn("buy-boxed-pencils", sent["schema"]["properties"]["findings"]["items"]["properties"]["rule_id"]["enum"])


if __name__ == "__main__":
    unittest.main()


class ReviewUseTests(unittest.TestCase):
    def test_an_unreviewed_try_never_outranks_a_reviewed_one_at_the_same_score(self):
        # Pencil XlX1z5lyl8QT: try 1 (score 2, not reviewed) was kept over try 2 (score 2, reviewed, 6 findings).
        from scripts import world_builder_service as service

        unreviewed = {"ok": True}
        reviewed = {"ok": True, "review_findings": [{"rule_id": "missing"}] * 6}
        clean = {"ok": True, "review_findings": []}
        self.assertGreater(service._attempt_rank(2, reviewed), service._attempt_rank(2, unreviewed))
        self.assertGreater(service._attempt_rank(2, clean), service._attempt_rank(2, reviewed))
        self.assertGreater(service._attempt_rank(3, unreviewed), service._attempt_rank(2, clean))

    def test_the_prompt_says_laws_bind_only_the_goods_they_name_and_transfers_keep_totals(self):
        # Pencil XlX1z5lyl8QT: five of six findings on try 2 said goods no law names, or transfers no law lists,
        # would be refused; the engine refuses neither (src/world_substrate/laws.py).
        system = reviewer.PROMPT.read_text()
        self.assertIn("a law constrains only the resource it names", system)
        self.assertIn("keeps the total", system)
