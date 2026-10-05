from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_native_coordination import run_matrix

REPO = Path(__file__).resolve().parents[1]


class NativeCoordinationMatrixTests(unittest.TestCase):
    def test_matrix_runs_both_worlds_and_requires_one_mechanics_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "matrix"
            summary = run_matrix(
                output_root=output,
                run_id_prefix="test/native-coordination-matrix",
            )
            self.assertEqual(summary["status"], "passed")
            self.assertTrue(summary["all_worlds_passed"])
            self.assertTrue(summary["shared_mechanic_profile"]["passed"])
            self.assertTrue(summary["shared_mechanic_profile"]["profile_id"])
            self.assertEqual(
                set(summary["worlds"]),
                {"distributed-approval", "constrained-handoff"},
            )
            retained = json.loads((output / "matrix-summary.json").read_text())
            self.assertEqual(retained, summary)
            for world_id in summary["worlds"]:
                self.assertTrue((output / world_id / "summary.json").exists())
                self.assertTrue((output / world_id / "acceptance.json").exists())
                self.assertTrue((output / world_id / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
