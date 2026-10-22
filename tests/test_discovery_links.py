"""Discovery joins participants on their id links before the 256-move cap.

Live run c1r18 (2026-10-22, evidence/waltzman-belief-and-traces/c1r18): `communicate` takes a delivery, an
information item and a recipient. 8 x 8 x 11 combinations passed the cap before any technical or logistics
delivery, so for 46 rounds neither group was ever offered its own message and both concerns stayed undelivered.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.run_authored_world import build_engine

# The world that run built, as its first /run request carried it.
WORLD = Path(__file__).resolve().parent / "fixtures/c1r18_waltzman_world.json"


class DiscoveryLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        request = json.loads(WORLD.read_text())
        cls.engine = build_engine(request["bundle"], request["causal_model"])[0]

    def offered(self, actor: str) -> set[str]:
        page = self.engine.discover(actor, kind="communicate")
        return {row["action"]["delivery"] for row in page["available"]}

    def test_every_group_is_offered_each_of_its_own_deliveries(self):
        for group, recipients in {
            "technical-group": ("country-one", "regional-health-network"),
            "logistics-group": ("country-three", "regional-health-network"),
            "legal-group": ("country-two", "partnership"),
            "community-group": ("country-four", "partnership"),
        }.items():
            topic = group.removesuffix("-group")
            self.assertEqual(
                self.offered(group), {f"delivery-info-{topic}-concern-to-{r}" for r in recipients}, group)

    def test_someone_with_nothing_to_send_still_sees_why(self):
        page = self.engine.discover("country-one", kind="communicate")
        self.assertEqual(page["available"], [])
        reasons = {row.get("reason", "") for row in page["blocked"]}
        self.assertTrue(any("information source" in r for r in reasons), reasons)


if __name__ == "__main__":
    unittest.main()
