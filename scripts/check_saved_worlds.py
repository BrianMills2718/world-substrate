"""Free check over every saved world and recorded build, before a paid build and after a rules-engine change.

1. Each saved world in tests/fixtures (a bundle and causal_model) runs a 24-round scripted test. A world whose
   every move was offered at least once is "whole"; one listed in saved_worlds_whole.json that stops being whole
   fails the check, so a fix that breaks a working world shows here, for free.
2. With --builds, each recorded build under evidence/ (run-log.jsonl + llm-calls.jsonl) is replayed with today's
   code and its own recorded replies (scripts/replay_build.py --follow-record), and the kept world's
   never-offered moves are printed. A forced reply answered a question today's code worded differently, so those
   rows show which recorded draft today's code would keep, not what a new build would write.

Usage: check_saved_worlds.py [--builds] [--update]   (--update rewrites the whole list from this run)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]
WHOLE = REPO / "tests/fixtures/saved_worlds_whole.json"
TURNS = 24


def saved_worlds() -> list[tuple[str, dict, dict]]:
    out = []
    for path in sorted((REPO / "tests/fixtures").glob("*.json")):
        try:
            value = json.loads(path.read_text())
        except ValueError:
            continue
        if isinstance(value, dict) and isinstance(value.get("bundle"), dict) and isinstance(value.get("causal_model"), dict):
            out.append((path.name, value["bundle"], value["causal_model"]))
    return out


def never_offered(bundle: dict, causal: dict) -> dict[str, str]:
    from scripts.run_authored_world import run_world

    dry, _, _ = run_world(bundle, causal, policy="scripted", max_turns=TURNS)
    return dry["summary"]["never_offered"]


def main() -> int:
    args = set(sys.argv[1:])
    expected = set(json.loads(WHOLE.read_text())["whole"]) if WHOLE.exists() else set()
    whole, broken, errors = [], [], []
    for name, bundle, causal in saved_worlds():
        try:
            missing = never_offered(bundle, causal)
        except Exception as error:  # a saved world that no longer compiles is a finding, not a crash
            errors.append(name)
            print(f"ERROR  {name}: {type(error).__name__}: {str(error)[:160]}")
            continue
        (broken if missing else whole).append(name)
        print(f"{'whole ' if not missing else 'broken'} {name}" + (f": never offered {sorted(missing)}" if missing else ""))
    lost = sorted(expected - set(whole))
    if "--update" in args:
        WHOLE.write_text(json.dumps({"note": "saved worlds whose every move is offered in a 24-round scripted test; "
                                     "scripts/check_saved_worlds.py fails if one stops being whole", "whole": sorted(whole)},
                                    indent=1) + "\n")
        lost = []
    if "--builds" in args:
        import scripts.replay_build as replay_build

        for folder in sorted({p.parent for p in (REPO / "evidence").rglob("llm-calls.jsonl")}):
            if not (folder / "run-log.jsonl").exists():
                continue
            rows = (folder / "run-log.jsonl").read_text()
            if '"/generate-world"' not in rows:
                continue
            out = replay_build.replay(folder, follow_record=True)
            forced = sum(1 for a in out["asked"] if a.get("forced"))
            kept = out["kept"] or {}
            missing = (kept.get("dry_run") or {}).get("never_offered")
            state = out["stopped"] or ("whole" if kept.get("causal_model") and not missing else f"never offered {sorted(missing or [])}")
            print(f"build  {folder.relative_to(REPO)}: {state} ({forced} forced replies)")
    print(f"RESULT saved={len(whole) + len(broken) + len(errors)} whole={len(whole)} broken={len(broken)} "
          f"errors={len(errors)} lost={len(lost)}" + (f" ({', '.join(lost)})" if lost else ""))
    return 1 if lost or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
