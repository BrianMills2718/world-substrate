#!/usr/bin/env python3
"""List recent World Builder builds and runs from the live run log (owner only).

    WORLD_BUILDER_OWNER_PASSWORD=... python3 scripts/world_builder_runs.py [--limit 20] [--who owner|visitor|agent] [--full]

Reads GET /world-builder/api/runs on the live site (or --base). Each line: time, who
(owner / visitor fingerprint / agent:e2e), what was asked, and what came out. --full
prints whole JSON records (world, rules, transcript) for the matching rows.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="https://brianmills.dev")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--who", choices=["owner", "visitor", "agent"])
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    password = os.environ.get("WORLD_BUILDER_OWNER_PASSWORD")
    if not password:
        print("set WORLD_BUILDER_OWNER_PASSWORD (it is in ~/.secrets/api_keys.env)", file=sys.stderr)
        return 2
    url = f"{args.base}/world-builder/api/runs?limit={args.limit}" + ("&full=1" if args.full else "")
    request = urllib.request.Request(url, headers={"X-World-Builder-Owner": password, "User-Agent": "Mozilla/5.0 world-builder-runs"})
    with urllib.request.urlopen(request, timeout=30) as response:
        rows = json.loads(response.read())["runs"]
    shown = 0
    for row in rows:
        who = row["who"] if row["who"] != "visitor" else f"visitor:{row['client']}"
        if args.who and not row["who"].startswith(args.who):
            continue
        shown += 1
        if args.full:
            print(json.dumps(row, indent=1))
            continue
        req, res = row.get("request") or {}, row.get("result") or {}
        asked = req.get("description") or (f"run {req.get('world')} turns={req.get('turns')} from={req.get('turn_offset', 0)}" if row["path"] == "/run" else "")
        if "error" in res:
            outcome = "ERROR " + res["error"]
        elif row["path"] == "/generate-world":
            dry = res.get("dry_run") or {}
            outcome = f"{res.get('world')} rules={res.get('rules')} by-itself={res.get('processes')} quick-test ok={dry.get('ok')} finished={dry.get('terminal_reached')} active={dry.get('active_at_end')}"
        elif row["path"] == "/run":
            s = res.get("summary") or {}
            outcome = f"rounds {s.get('first_turn')}-{s.get('last_turn')} allowed={s.get('accepted_actions')} world-changes={s.get('world_changes')} finished={s.get('terminal_reached')} active={s.get('active_at_end')} rules-id={res.get('mechanic_profile_id') or '-'}"
        else:
            outcome = (res.get("description") or res.get("reply") or "")[:120]
        print(f"{row['ts']}  {who:22} {row['path']:16} {row['status']}  ${(row.get('cost_usd') or 0):.4f}  {asked[:70]!r} -> {outcome}")
    print(f"RESULT shown={shown} fetched={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
