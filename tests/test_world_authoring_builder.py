from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXAMPLE = REPO / "examples/world_authoring/orchard-v0.json"
HTML = REPO / "evidence/renders/world-builder-v0.html"
CORE = REPO / "scripts/world_builder_core.js"
APP = REPO / "scripts/world_builder_app.js"

spec = importlib.util.spec_from_file_location("render_world_builder", REPO / "scripts/render_world_builder.py")
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)

starter_spec = importlib.util.spec_from_file_location("scaffold_world", REPO / "scripts/scaffold_world.py")
starter = importlib.util.module_from_spec(starter_spec)
starter_spec.loader.exec_module(starter)


class WorldAuthoringBuilderTests(unittest.TestCase):
    def test_builder_regenerates_exactly_as_standalone_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "builder.html"
            output.write_text(renderer.render())
            self.assertEqual(output.read_text(), HTML.read_text())
        source = HTML.read_text()
        self.assertNotIn("<script src=", source.lower())
        self.assertNotIn("<link rel=", source.lower())

    def test_builder_embeds_the_same_orchard_bundle_as_starter(self):
        source = HTML.read_text()
        match = re.search(r"window\.INITIAL_BUNDLE=(.*?);</script><script>", source, re.S)
        self.assertIsNotNone(match)
        embedded = json.loads(match.group(1))
        self.assertEqual(embedded, json.loads(EXAMPLE.read_text()))
        self.assertEqual(starter.validate_bundle(embedded)["world"]["id"], "orchard")

    def test_browser_core_and_python_validator_agree_on_key_cases(self):
        cases = []
        valid = json.loads(EXAMPLE.read_text())
        cases.append(valid)
        bad_ref = json.loads(json.dumps(valid)); bad_ref["entities"][2]["components"]["fruit"]["tree_id"] = "missing"; cases.append(bad_ref)
        bad_asset = json.loads(json.dumps(valid)); bad_asset["presentation"]["category_assets"]["fruit"] = "missing"; cases.append(bad_asset)
        bad_action = json.loads(json.dumps(valid)); bad_action["actions"][0]["fields"][0]["name"] = "actor"; cases.append(bad_action)
        bad_default = json.loads(json.dumps(valid)); bad_default["components"][0]["fields"][0]["default"] = "ten"; cases.append(bad_default)
        python_results = []
        for case in cases:
            try:
                starter.validate_bundle(case); python_results.append(True)
            except starter.BundleError:
                python_results.append(False)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cases.json"; path.write_text(json.dumps(cases))
            js = (
                "const fs=require('fs'); const core=require(process.argv[1]); "
                "const cases=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); "
                "process.stdout.write(JSON.stringify(cases.map(x=>core.validateBundle(x).ok)));"
            )
            result = subprocess.run(["node", "-e", js, str(CORE), str(path)], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), python_results)

    def test_builder_surface_makes_causal_boundary_explicit(self):
        source = APP.read_text()
        self.assertIn("Signatures describe intent shape only", source)
        self.assertIn("LLM proposes; compiler governs", source)
        self.assertIn("Signatures still are not causal law", source)
        self.assertNotIn("write_paths", source)
        self.assertIn("/generate-draft", source)
        self.assertIn("/generate-mechanics", source)
        self.assertIn("/run", source)
        self.assertIn("Generate bounded coordination draft", source)
        self.assertIn("Explicitly not simulated", source)
        self.assertIn("coverage_limit", source)
        self.assertIn("Extracted requirements → represented surfaces", source)
        self.assertIn("Approve mechanics for run", source)
        html_source = HTML.read_text()
        for label in ("World", "Components", "Entities", "Action signatures", "Causal mechanics", "Presentation", "Run", "Full logs", "Review & export"):
            self.assertIn(label, html_source)

    def test_live_flow_keeps_mechanics_separate_from_bundle_export(self):
        source = APP.read_text()
        self.assertIn("let causalModel = null", source)
        self.assertIn("draftArtifact", source)
        self.assertIn("draftReview", source)
        self.assertIn("draftSource", source)
        self.assertIn("mechanicsSource", source)
        self.assertIn("mechanicsApproved", source)
        self.assertIn("causalModel=payload.causal_model", source)
        self.assertIn("causalReview=payload.review?.mechanics||null", source)
        self.assertIn('executionMode="native_coordination"', source)
        self.assertIn('execution_mode:executionMode', source)
        self.assertIn("Native coordination · deterministic Engine path · Living Scene · $0 provider spend", source)
        self.assertIn("causal_model:causalModel", source)
        self.assertIn("approved:true", source)
        self.assertIn("iframe", source)

    def test_live_flow_exposes_complete_debug_logs(self):
        source = APP.read_text()
        self.assertIn("liveLog = []", source)
        self.assertIn('recordLiveLog("request"', source)
        self.assertIn('recordLiveLog("response"', source)
        self.assertIn("await response.text()", source)
        self.assertIn("Full logs", source)
        self.assertIn("Copy complete raw logs", source)
        self.assertIn("Full engine traces", source)
        self.assertIn('["/generate-draft","One-shot draft"]', source)
        self.assertIn("trace_id:payload.trace_id", source)
        self.assertIn("replay_html hidden on-screen", source)
        self.assertIn("exact replay HTML", source)
        self.assertIn("filteredLiveLog", source)
        self.assertIn("Search logs", source)
        self.assertIn("Errors only", source)
        self.assertIn("Copy filtered logs", source)
        self.assertIn('data-section="logs"', HTML.read_text())

    def test_core_rejects_unknown_entity_reference(self):
        js = (
            "const core=require(process.argv[1]); const fs=require('fs'); "
            "const x=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); "
            "x.entities[2].components.fruit.tree_id='missing'; "
            "const r=core.validateBundle(x); if(r.ok || !r.errors.some(e=>e.includes('unknown entity'))) process.exit(2);"
        )
        subprocess.run(["node", "-e", js, str(CORE), str(EXAMPLE)], check=True)


if __name__ == "__main__":
    unittest.main()
