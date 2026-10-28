"""Review the kept try of the live pencil build (tests/fixtures/pencil-s3-kept.json) with the reviewer that now
sees the world's starting values (#293 E). That try was never reviewed live; its carrier starts with a price of 0,
so the purchase law refuses every purchase. Writes replay_start.json next to this file. One paid call (about $0.15).
Run from the repository root:  LLM_CLIENT_PROJECT=world-substrate python evidence/declared-laws/s3-pencil/replay_start.py
"""
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.review_rules import review_rules  # noqa: E402

FIXTURE = REPO / "tests" / "fixtures" / "pencil-s3-kept.json"


def main() -> None:
    kept = json.loads(FIXTURE.read_text())
    trace_id = f"world-substrate/s3-pencil/replay-start/{uuid.uuid4().hex}"
    findings, cost = review_rules(kept["description"], kept["bundle"], kept["causal_model"],
                                  trace_id=trace_id, max_budget=0.5)
    out = {"reviewed": "tests/fixtures/pencil-s3-kept.json", "trace_id": trace_id, "cost_usd": cost,
           "findings": findings}
    (HERE / "replay_start.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
