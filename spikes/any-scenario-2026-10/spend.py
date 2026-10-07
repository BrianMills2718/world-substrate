#!/usr/bin/env python3
"""Total model spend for this plan: every llm_client call whose trace id starts with 'any-scenario'."""
import json
import sys
from pathlib import Path

LOGS = Path.home() / "projects/data/world-substrate/world-substrate_llm_client_data"
CAP = 5.00


def plan_spend() -> tuple[int, float]:
    n, total = 0, 0.0
    for f in sorted(LOGS.glob("calls_*.jsonl")):
        for line in f.open():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("trace_id") or "").startswith("any-scenario"):
                n += 1
                total += float(row.get("cost") or 0.0)
    return n, total


if __name__ == "__main__":
    n, total = plan_spend()
    print(f"plan spend: calls={n} cost=${total:.4f} cap=${CAP:.2f} remaining=${CAP - total:.4f}")
    sys.exit(1 if total > CAP else 0)
