from __future__ import annotations

import json
import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch
from pathlib import Path

from scripts.generate_causal_model import MAX_MECHANICS_OUTPUT_TOKENS, causal_model_schema, generate_causal_model
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

    def test_context_states_builtin_initial_values_exactly_as_the_engine_builds_them(self):
        from scripts.generate_causal_model import _context
        from scripts.run_authored_world import build_engine

        bundle = validate_bundle(json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text()))
        causal = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
        stated = _context(bundle)["initial_builtin_state"]
        engine, _, _ = build_engine(bundle, causal)
        for entity_id, entity in engine.world.entities.items():
            actual = {
                "location.location_id": entity.location.location_id if entity.location else None,
                "ownership.owner_ref": entity.ownership.owner_ref if entity.ownership else None,
                "portable.portable": entity.portable.portable if entity.portable else None,
            }
            self.assertEqual(stated[entity_id], actual, entity_id)

    def test_generation_caps_provider_output_tokens(self):
        bundle = validate_bundle(json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text()))
        causal = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
        fake = SimpleNamespace(content=json.dumps(causal), cost=0.0, model="fake-model")
        call = MagicMock(return_value=fake)
        fake_module = ModuleType("llm_client")
        fake_module.call_llm = call
        fake_module.safe_json_loads = json.loads
        with patch.dict(sys.modules, {"llm_client": fake_module}):
            generated, result = generate_causal_model(bundle, model="fake-model", trace_id="test-output-cap")
        self.assertEqual(generated["schema_version"], "world-substrate-causal-model/v0")
        self.assertIs(result, fake)
        self.assertEqual(MAX_MECHANICS_OUTPUT_TOKENS, 8192)
        self.assertEqual(call.call_args.kwargs["max_tokens"], MAX_MECHANICS_OUTPUT_TOKENS)


if __name__ == "__main__":
    unittest.main()
