from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scaffold_world", REPO / "scripts/scaffold_world.py")
scaffold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scaffold)
EXAMPLE = REPO / "examples/world_authoring/orchard-v0.json"


class WorldAuthoringStarterTests(unittest.TestCase):
    def load(self):
        return json.loads(EXAMPLE.read_text())

    def test_example_validates_and_has_structural_schema(self):
        value = scaffold.validate_bundle(self.load())
        self.assertEqual(value["world"]["id"], "orchard")
        schema = json.loads((REPO / "schemas/world-authoring-bundle-v0.schema.json").read_text())
        self.assertEqual(schema["$id"], scaffold.SCHEMA_VERSION)

    def test_entity_reference_must_resolve(self):
        value = self.load()
        value["entities"][2]["components"]["fruit"]["tree_id"] = "missing-tree"
        with self.assertRaisesRegex(scaffold.BundleError, "unknown entity"):
            scaffold.validate_bundle(value)

    def test_action_signature_is_not_causal_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = scaffold.scaffold(self.load(), root)
            env = {"PYTHONPATH": f"{REPO / 'src'}:{root}"}
            code = (
                "from orchard.probe import build_engine; "
                "from orchard.mechanics import PickAction, PickRule; "
                "e=build_engine(); a=PickAction('ava','apple-1',0,'test'); "
                "assert e.discover('ava')['total']==0; "
                "assert PickRule().checks(e.world,a)[0].ok is False; "
                "assert PickAction.from_dict(a.as_dict())==a"
            )
            subprocess.run([sys.executable, "-c", code], env=env, check=True)
            self.assertIn("always refuse", (package / "mechanics.py").read_text())

    def test_scaffold_compiles_and_preserves_authoring_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = scaffold.scaffold(self.load(), root)
            self.assertEqual(json.loads((package / "authoring-v0.json").read_text()), self.load())
            subprocess.run([sys.executable, "-m", "py_compile", *map(str, package.glob("*.py"))], check=True)
            model = json.loads((package / "orchard-v0.json").read_text())
            self.assertEqual(model["world_id"], "orchard-v0")
            self.assertEqual([e["entity_id"] for e in model["entities"]], ["ava", "tree-1", "apple-1"])

    def test_scaffold_refuses_existing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scaffold.scaffold(self.load(), root)
            with self.assertRaisesRegex(scaffold.BundleError, "already exists"):
                scaffold.scaffold(self.load(), root)

    def test_presentation_extension_does_not_claim_world_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            package = scaffold.scaffold(self.load(), Path(tmp))
            presentation = json.loads((package / "scene-catalog-extension-v0.json").read_text())
            self.assertEqual(presentation["category_entity_bindings"]["fruit"], {"asset": "fruit"})
            self.assertEqual(presentation["category_station_bindings"]["tree"], {"role": "source"})
            self.assertIn("Review", presentation["note"])


if __name__ == "__main__":
    unittest.main()
