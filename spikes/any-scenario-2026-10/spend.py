#!/usr/bin/env python3
"""Total model spend for this plan: every llm_client call whose trace id starts with 'any-scenario'."""
import json
import sys
from pathlib import Path

# llm_client names its log folder after the working directory, so a run from a clone or worktree logs under
# another project name. Sum this plan's trace prefix across every project's call logs.
DATA = Path.home() / "projects/data"
LOGS = DATA / "world-substrate/world-substrate_llm_client_data"  # must exist: a missing home log reads as $0
# any-scenario-poc ($5 cap) ended at $3.93; linked-process-participants adds $3 on top (approved 2026-10-08).
CAP = 3.93 + 3.00


def plan_spend() -> tuple[int, float]:
    if not LOGS.is_dir():  # a missing log must not read as $0 spent: that would silently disable the cap
        raise SystemExit(f"spend log directory not found: {LOGS}")
    n, total = 0, 0.0
    for f in sorted(DATA.glob("*/*_llm_client_data/calls_*.jsonl")):
        try:
            lines = f.read_text(errors="replace").splitlines()
        except (FileNotFoundError, IsADirectoryError, PermissionError):
            continue  # another project's log moved or is a broken link; it holds none of this plan's calls
        for line in lines:
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
