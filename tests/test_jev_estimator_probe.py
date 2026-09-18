from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "run_jev_estimator_probe.py"

spec = importlib.util.spec_from_file_location("run_jev_estimator_probe", SCRIPT)
probe = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(probe)


class JevEstimatorProbeTests(unittest.TestCase):
    def test_request_is_decisions_shape_and_pinned(self):
        case = probe.CASES[0]
        payload = probe.build_request(case)
        self.assertEqual(payload["model"], "openrouter/typesafe/jev-1.13")
        self.assertEqual(payload["state"], case["state"])
        self.assertEqual(
            set(payload["questions"]),
            {"failure_mode", "shutdown_required", "severity"},
        )
        self.assertEqual(payload["questions"]["failure_mode"]["type"], "choice")
        self.assertEqual(payload["questions"]["shutdown_required"]["type"], "noul")
        self.assertEqual(payload["questions"]["severity"]["type"], "score")

    def test_grade_uses_predeclared_labels_only(self):
        case = probe.CASES[0]
        response = {
            "answers": {
                "failure_mode": {
                    "choice": "shaft_misalignment",
                    "probabilities": {
                        "bearing_wear": 0.05,
                        "shaft_misalignment": 0.8,
                        "coolant_loss": 0.03,
                        "sensor_fault": 0.05,
                        "electrical_fault": 0.07,
                    },
                },
                "shutdown_required": {"noul": 0.81},
                "severity": {"score": 2.7},
            }
        }
        grade = probe.grade_case(case, response)
        self.assertTrue(grade["failure_mode_correct"])
        self.assertTrue(grade["shutdown_correct"])
        self.assertEqual(grade["predicted_failure_mode"], "shaft_misalignment")
        self.assertEqual(grade["severity"], 2.7)

    def test_grade_accepts_shared_client_noul_shape(self):
        case = probe.CASES[3]
        response = {"answers": {"failure_mode": {"choice": "sensor_fault", "probabilities": {"sensor_fault": .99}}, "shutdown_required": {"probability": .22}, "severity": {"score": 1.37}}}
        grade = probe.grade_case(case, response)
        self.assertFalse(grade["predicted_shutdown_required"])
        self.assertTrue(grade["shutdown_correct"])
        self.assertEqual(grade["shutdown_probability"], .22)

    def test_dry_run_never_requires_credentials(self):
        payload = probe.dry_run("openrouter/typesafe/jev-1.13", "sensor-01")
        self.assertEqual(payload["status"], "dry-run")
        self.assertEqual(payload["transport"], "llm_client.call_decisions")
        self.assertEqual(len(payload["requests"]), 1)
        self.assertEqual(payload["requests"][0]["case_id"], "sensor-01")


if __name__ == "__main__":
    unittest.main()
