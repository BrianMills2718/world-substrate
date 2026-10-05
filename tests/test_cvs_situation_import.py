from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


adapter = _load_module("import_cvs_situation", REPO / "scripts/import_cvs_situation.py")
scaffold = _load_module("scaffold_world_for_cvs", REPO / "scripts/scaffold_world.py")
FIXTURE = REPO / "tests/fixtures/cvs/sustainment_situation_ir.json"
PROVENANCE = REPO / "tests/fixtures/cvs/sustainment_situation_ir.provenance.json"


class CvsSituationImportTests(unittest.TestCase):
    def load(self):
        return json.loads(FIXTURE.read_text())

    def bundle(self, enabled=()):
        return adapter.convert_situation(
            self.load(),
            scenario_id="sc_1",
            enabled_capabilities=enabled,
            source_ref="compositional-viable-systems@5cb9933:applications/sustainment/sustainment_situation_ir.json",
        )

    def by_external_id(self, bundle):
        return {
            row["components"]["external_identity"]["identifier"]: row
            for row in bundle["entities"]
        }

    def test_fixture_pins_exact_donor_provenance(self):
        provenance = json.loads(PROVENANCE.read_text())
        self.assertEqual(provenance["source_revision"], "5cb9933f2551ca3e0e75590814f7e686f50d8edb")
        import hashlib
        self.assertEqual(hashlib.sha256(FIXTURE.read_bytes()).hexdigest(), provenance["sha256"])

    def test_projection_validates_as_authoring_bundle_and_preserves_external_identity(self):
        bundle = scaffold.validate_bundle(self.bundle())
        rows = self.by_external_id(bundle)
        self.assertEqual(rows["regional_hq"]["id"], "regional-hq")
        self.assertEqual(rows["stock_a"]["id"], "stock-a")
        self.assertNotIn("regional_hq", {row["id"] for row in bundle["entities"]})
        self.assertTrue(bundle["world"]["summary"].startswith("SYNTHETIC INTEGRATION FIXTURE."))

    def test_selected_scenario_becomes_initial_inventory_state(self):
        rows = self.by_external_id(self.bundle())
        self.assertEqual(
            rows["stock_a"]["components"]["inventory"],
            {"available": 4, "demand": 1, "unit": "units", "protected_reserve": 1},
        )
        self.assertEqual(
            rows["stock_b"]["components"]["inventory"],
            {"available": 1, "demand": 3, "unit": "units", "protected_reserve": 1},
        )
        context = rows["regional_hq"]["components"]["scenario_context"]
        self.assertEqual(context["scenario_id"], "sc_1")
        self.assertEqual(context["regime"], "local_priority")
        self.assertTrue(context["is_decider"])

    def test_capability_activation_is_explicit_structural_variant(self):
        wanted = {
            "cap_observe_distribution",
            "cap_transfer_authority",
            "cap_override_reserve",
        }
        baseline = self.by_external_id(self.bundle())
        target = self.by_external_id(self.bundle(wanted))
        for cap_id in wanted:
            self.assertFalse(baseline[cap_id]["components"]["capability"]["enabled"])
            self.assertTrue(target[cap_id]["components"]["capability"]["enabled"])
        self.assertFalse(target["cap_extra_a_1"]["components"]["capability"]["enabled"])

    def test_action_templates_keep_directional_source_identity_but_signature_is_deduplicated(self):
        bundle = self.bundle()
        rows = self.by_external_id(bundle)
        self.assertEqual([action["kind"] for action in bundle["actions"]], ["transfer"])
        a_to_b = rows["act_move_a_to_b"]["components"]["action_template"]
        self.assertEqual(a_to_b["source_ref"], "stock-a")
        self.assertEqual(a_to_b["target_ref"], "stock-b")
        self.assertEqual(
            a_to_b["required_capability_ids"],
            ["cap_observe_distribution", "cap_transfer_authority"],
        )

    def test_projection_scaffolds_only_refusing_mechanics(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = scaffold.scaffold(self.bundle(), Path(tmp))
            mechanics = (package / "mechanics.py").read_text()
            self.assertIn("always refuse", mechanics)
            self.assertIn("TransferRule", mechanics)

    def test_unknown_semantics_fail_loudly(self):
        value = self.load()
        value["relations"] = [{"kind": "unsupported"}]
        with self.assertRaisesRegex(adapter.SituationImportError, "relations are not represented"):
            adapter.convert_situation(value, scenario_id="sc_1")
        with self.assertRaisesRegex(adapter.SituationImportError, "unknown scenario"):
            adapter.convert_situation(self.load(), scenario_id="missing")
        with self.assertRaisesRegex(adapter.SituationImportError, "enabled capabilities are not declared"):
            adapter.convert_situation(self.load(), scenario_id="sc_1", enabled_capabilities=["invented"])


if __name__ == "__main__":
    unittest.main()
