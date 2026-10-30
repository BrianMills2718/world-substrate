"""Replay a saved World Builder build with today's code and the build's own recorded model replies. No model call.

Each call the build makes is answered with the recorded reply to the identical prompt, so today's ranking, test
runs and guidance decide what is kept. When today's code asks something the build never asked (its guidance
changed, or it revised a different try), the replay stops there and says so: past that point only a paid build can
answer. With --follow-record it goes on instead, handing out the oldest unused recorded reply of the same task: that
answers "given the same drafts, which would today's code keep?", and each such answer is counted as forced.
Usage: replay_build.py [--follow-record] <evidence folder with run-log.jsonl and llm-calls.jsonl>
"""
from __future__ import annotations

import collections
import json
import sys
import types
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]


class Unrecorded(RuntimeError):
    """Today's code asked a question the saved build never asked."""


def _key(messages: Any) -> str:
    return json.dumps([{"role": m.get("role"), "content": m.get("content")} for m in messages], sort_keys=True)


def recorded_llm_client(calls: list[dict[str, Any]], asked: list[dict[str, Any]],
                        follow_record: bool = False) -> types.ModuleType:
    """A stand-in llm_client whose calls return the recorded replies, matched by prompt, oldest first."""
    import llm_client as real

    ordered = sorted(calls, key=lambda c: c["id"])
    keys = {call["id"]: _key(json.loads(call["messages"])) for call in ordered}
    used: set[int] = set()

    def answer(messages: Any, task: str | None) -> dict[str, Any]:
        mine = _key(messages)
        call = next((c for c in ordered if c["id"] not in used and keys[c["id"]] == mine), None)
        forced = False
        if call is None and follow_record:
            call = next((c for c in ordered if c["id"] not in used and c.get("task") == task), None)
            forced = call is not None
        if call is None:
            asked.append({"task": task, "recorded": None, "forced": False})
            raise Unrecorded(f"no recorded reply for this {task or 'model'} call")
        used.add(call["id"])
        asked.append({"task": task, "recorded": call["id"], "forced": forced})
        return call

    def call_llm(model: str, messages: Any, **kwargs: Any) -> Any:
        call = answer(messages, kwargs.get("task"))
        return types.SimpleNamespace(content=call["response"], cost=0.0, model=call["model"], finish_reason="stop")

    def call_llm_json_schema(model: str, messages: Any, schema: Any, **kwargs: Any) -> Any:
        call = answer(messages, kwargs.get("task"))
        return json.loads(call["response"]), types.SimpleNamespace(cost=0.0, model=call["model"])

    stub = types.ModuleType("llm_client")
    stub.__dict__.update({k: v for k, v in vars(real).items() if not k.startswith("__")})
    stub.call_llm, stub.call_llm_json_schema = call_llm, call_llm_json_schema
    stub.get_cost = lambda **kwargs: 0.0
    return stub


def replay(folder: Path, follow_record: bool = False) -> dict[str, Any]:
    """{"kept": the build's reply payload or None, "stopped": why it stopped early or None, "asked": calls}."""
    rows = [json.loads(line) for line in (folder / "run-log.jsonl").read_text().splitlines()]
    build = next(r for r in rows if r["path"] == "/generate-world")
    calls = [json.loads(line) for line in (folder / "llm-calls.jsonl").read_text().splitlines()]
    asked: list[dict[str, Any]] = []
    stub = recorded_llm_client(calls, asked, follow_record)
    import scripts.world_builder_service as service
    out: dict[str, Any] = {"kept": None, "stopped": None, "asked": asked}

    class Replay(service.WorldBuilderHandler):
        def __init__(self) -> None:  # no socket
            pass

        def _progress(self, state: str, step: str, detail: str = "", items: list[str] | None = None) -> None:
            pass

        def _llm_budget(self, client: str, requested_cap: float, **kwargs: Any) -> float:
            return requested_cap

        def _json(self, status: int, value: dict[str, Any]) -> None:
            out["kept"] = value

        def _error(self, status: int, message: str) -> None:
            out["stopped"] = message

    real, side_by_side = sys.modules.get("llm_client"), service.RULES_SIDE_BY_SIDE
    sys.modules["llm_client"] = stub
    service.RULES_SIDE_BY_SIDE = False  # the recorded replies are handed out in order
    try:
        Replay()._generate_world("replay", build["request"])
    except Unrecorded as error:
        out["stopped"] = str(error)
    finally:
        service.RULES_SIDE_BY_SIDE = side_by_side
        if real is None:
            sys.modules.pop("llm_client", None)
        else:
            sys.modules["llm_client"] = real
    return out


def main() -> int:
    args = sys.argv[1:]
    follow = "--follow-record" in args
    folder = Path(next(a for a in args if not a.startswith("--")))
    out = replay(folder, follow)
    recorded = sum(1 for a in out["asked"] if a["recorded"])
    forced = sum(1 for a in out["asked"] if a.get("forced"))
    print(f"replay {folder}: answered {recorded} calls from the record, {forced} of them forced")
    if out["stopped"]:
        print("stopped:", out["stopped"])
    kept = out["kept"] or {}
    for i, row in enumerate(kept.get("dry_run_attempts") or []):
        print(f"  try {i}: score {row.get('score')} never_offered {sorted(row.get('never_offered') or [])} "
              f"review_findings {len(row['review_findings']) if 'review_findings' in row else '-'}")
    if kept.get("causal_model"):
        print("kept never_offered:", sorted((kept.get("dry_run") or {}).get("never_offered") or []))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
