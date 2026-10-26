"""The metamodel files in docs/model/ are current with scripts/build_metamodel.py and cite real code.

No model calls, no network: runs the builder's --check, which fails when a written file differs from
what the TYPES and LINKS tables produce or when a type's code citation names a missing file or line.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MetamodelTest(unittest.TestCase):
    def test_metamodel_files_are_current(self) -> None:
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_metamodel.py"), "--check"],
                                capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 problems", result.stdout)


if __name__ == "__main__":
    unittest.main()
