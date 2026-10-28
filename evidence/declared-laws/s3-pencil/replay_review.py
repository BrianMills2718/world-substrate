"""Replay the live build's review of try 2 (llm call 22202) with the current reviewer prompt.

The description, laws and rules are read back from the saved request, so the reviewer sees exactly what it saw
live; only the system prompt is today's. Writes replay.json next to this file. One paid call (about $0.10).
Run from the repository root:  LLM_CLIENT_PROJECT=world-substrate python evidence/declared-laws/s3-pencil/replay_review.py
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

CALL_ID = 22202


def saved_request() -> tuple[str, dict, dict]:
    for line in (HERE / "llm-calls.jsonl").read_text().splitlines():
        row = json.loads(line)
        if row["id"] == CALL_ID:
            user = json.loads(row["messages"])[1]["content"]
            break
    else:
        raise SystemExit(f"call {CALL_ID} not in llm-calls.jsonl")
    description = user.split("Description:\n", 1)[1].split("\n\nLaws (", 1)[0].strip()
    laws = json.loads(user.split("what may change their totals):\n", 1)[1].split("\n\nRules:\n", 1)[0])
    rules = json.loads(user.split("\n\nRules:\n", 1)[1])
    return description, laws, rules


def main() -> None:
    description, laws, rules = saved_request()
    trace_id = f"world-substrate/s3-pencil/replay-review/{uuid.uuid4().hex}"
    findings, cost = review_rules(description, laws, rules, trace_id=trace_id, max_budget=0.5)
    out = {"replayed_call": CALL_ID, "trace_id": trace_id, "cost_usd": cost, "findings": findings}
    (HERE / "replay.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
