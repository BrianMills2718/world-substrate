from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.generate_causal_model import causal_model_schema
from scripts.scaffold_world import validate_bundle

REPO = Path(__file__).resolve().parents[1]


class CausalModelGenerationSchemaTests(unittest.TestCase):
    def test_schema_has_exactly_one_mechanic_per_action_signature(self):
        bundle = validate_bundle(json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text()))
        schema = causal_model_schema(bundle)
        mechanics = schema["properties"]["mechanics"]
        self.assertEqual(mechanics["minItems"], 1)
        self.assertEqual(mechanics["maxItems"], 1)
        row = mechanics["items"]["anyOf"][0]
        self.assertEqual(row["properties"]["action_kind"]["const"], "pick")
        self.assertEqual(row["properties"]["participants"]["required"], ["fruit"])

    def test_scalar_fields_become_finite_parameter_choice_arrays(self):
        bundle = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())
        bundle["actions"][0]["fields"].append({"name": "count", "type": "integer"})
        schema = causal_model_schema(validate_bundle(bundle))
        parameters = schema["properties"]["mechanics"]["items"]["anyOf"][0]["properties"]["parameters"]
        self.assertEqual(parameters["required"], ["count"])
        self.assertEqual(parameters["properties"]["count"]["items"]["type"], "integer")


if __name__ == "__main__":
    unittest.main()
