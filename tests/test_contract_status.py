"""A contract's stated status is checked against the code it describes.

`check_project.REQUIRED` asserted that contract files exist and are linked.
Nothing asserted that what they *say about themselves* is still true, which is
how semantic-mechanical-binding-v0.md spent several commits claiming one
binding of seven while six were implemented, and claiming no binding reached a
causal event after all of them did.

These tests exist because a status check that cannot go red is worth nothing.
Each one breaks a fact and asserts the check notices.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

_spec = importlib.util.spec_from_file_location(
    "check_project", REPO / "scripts/check_project.py"
)
check_project = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_project)


class TheStatusCheckIsWiredUp(unittest.TestCase):
    def test_it_passes_on_the_current_tree(self):
        self.assertEqual(check_project.check_contract_status(REPO), [])

    def test_at_least_one_contract_declares_facts(self):
        # An inert check is the failure this file exists to prevent, so the
        # check itself fails when nothing opts in.
        declared = {}
        for name in check_project.REQUIRED:
            if name.startswith("docs/contracts/"):
                declared.update(
                    check_project._parse_status_facts((REPO / name).read_text())
                )
        self.assertTrue(declared)

    def test_every_declared_fact_is_one_the_checker_computes(self):
        live = check_project._live_facts(REPO)
        for name in check_project.REQUIRED:
            if not name.startswith("docs/contracts/"):
                continue
            for key in check_project._parse_status_facts((REPO / name).read_text()):
                with self.subTest(contract=name, fact=key):
                    self.assertIn(key, live)


class FactsAreComputedFromBehaviourNotDeclarations(unittest.TestCase):
    """The facts must come from running the engine.

    A check that reads `SEMANTIC_BINDINGS` to confirm a claim about
    `SEMANTIC_BINDINGS` could not fail if the wiring that uses it broke.
    """

    def test_binding_on_events_is_read_off_a_committed_event(self):
        import world_substrate.engine as engine_module

        saved = engine_module.Engine._binding_of
        engine_module.Engine._binding_of = lambda self, action: None
        try:
            live = check_project._live_facts(REPO)
        finally:
            engine_module.Engine._binding_of = saved
        self.assertFalse(
            live["semantic_binding_on_events"],
            "the fact survived the binding being detached from events, so it "
            "is reading a declaration rather than a committed event",
        )

    def test_write_scope_enforcement_is_read_off_a_refusal(self):
        import world_substrate.engine as engine_module

        saved = engine_module._scope_violations
        engine_module._scope_violations = lambda *args, **kwargs: []
        try:
            live = check_project._live_facts(REPO)
        finally:
            engine_module._scope_violations = saved
        self.assertFalse(
            live["write_scopes_enforced"],
            "the fact survived the write-scope guard being disabled",
        )

    def test_a_removed_binding_moves_the_count(self):
        from world_substrate import semantic

        saved = dict(semantic.SEMANTIC_BINDINGS)
        semantic.SEMANTIC_BINDINGS.pop("pour")
        try:
            live = check_project._live_facts(REPO)
        finally:
            semantic.SEMANTIC_BINDINGS.clear()
            semantic.SEMANTIC_BINDINGS.update(saved)
        self.assertEqual(live["semantic_bindings_bound"], 5)
        self.assertIn("pour", live["unbound_action_kinds"])


class DriftIsReported(unittest.TestCase):
    def drift(self, key, wrong):
        """Run the comparison with one live fact deliberately wrong."""
        live = check_project._live_facts(REPO)
        live[key] = wrong
        saved = check_project._live_facts
        check_project._live_facts = lambda root: live
        try:
            return check_project.check_contract_status(REPO)
        finally:
            check_project._live_facts = saved

    def test_a_wrong_binding_count_is_reported(self):
        failures = self.drift("semantic_bindings_bound", 1)
        self.assertTrue(failures)
        self.assertTrue(any("semantic_bindings_bound" in f for f in failures))
        self.assertTrue(any("semantic-mechanical-binding" in f for f in failures))

    def test_a_wrong_boolean_is_reported(self):
        failures = self.drift("semantic_binding_on_events", False)
        self.assertTrue(any("semantic_binding_on_events" in f for f in failures))

    def test_a_wrong_list_is_reported(self):
        failures = self.drift("unbound_action_kinds", ["fill", "unheat"])
        self.assertTrue(any("unbound_action_kinds" in f for f in failures))

    def test_read_scope_enforcement_would_be_reported_if_it_shipped(self):
        # transition-envelope-v0.md says reads are unenforced. If that ever
        # becomes untrue and the contract is not updated, this is the failure.
        failures = self.drift("read_scopes_enforced", True)
        self.assertTrue(any("read_scopes_enforced" in f for f in failures))

    def test_an_unknown_fact_is_reported(self):
        text = "<!-- status-facts\nnot_a_real_fact: 1\n-->"
        self.assertEqual(
            check_project._parse_status_facts(text), {"not_a_real_fact": 1}
        )
        live = check_project._live_facts(REPO)
        self.assertNotIn("not_a_real_fact", live)


class TheParserHandlesTheDeclaredForms(unittest.TestCase):
    def test_ints_bools_and_lists(self):
        text = """<!-- status-facts
a_count: 6
a_flag: true
another_flag: false
a_list: [unheat, fill]
-->"""
        self.assertEqual(
            check_project._parse_status_facts(text),
            {
                "a_count": 6,
                "a_flag": True,
                "another_flag": False,
                "a_list": ["fill", "unheat"],
            },
        )

    def test_a_contract_with_no_block_declares_nothing(self):
        self.assertEqual(check_project._parse_status_facts("# just prose"), {})


if __name__ == "__main__":
    unittest.main()
