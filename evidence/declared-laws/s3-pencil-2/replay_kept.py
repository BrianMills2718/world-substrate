"""Review the kept try of pencil build 2 (tests/fixtures/pencil-s3p2-kept.json), which was never reviewed live
(defect G: the last try of each structure failed to compile, so the review gate never fired). Its shop is
starved: delivery gives boxed pencils, selling needs pencils. Writes replay_kept.json next to this file. One paid
call (about $0.10). Run from the repository root:
  LLM_CLIENT_PROJECT=world-substrate python evidence/declared-laws/s3-pencil-2/replay_kept.py
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

FIXTURE = REPO / "tests" / "fixtures" / "pencil-s3p2-kept.json"


def main() -> None:
    kept = json.loads(FIXTURE.read_text())
    trace_id = f"world-substrate/s3-pencil-2/replay-kept/{uuid.uuid4().hex}"
    findings, cost = review_rules(kept["description"], kept["bundle"], kept["causal_model"],
                                  trace_id=trace_id, max_budget=0.5)
    out = {"reviewed": "tests/fixtures/pencil-s3p2-kept.json", "trace_id": trace_id, "cost_usd": cost,
           "findings": findings}
    (HERE / "replay_kept.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
