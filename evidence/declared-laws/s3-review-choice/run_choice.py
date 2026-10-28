"""Q44: each candidate reviewer on the saved incident worlds (docs/plans/declared_laws.md, Evaluation design).

Same input per candidate (description, laws, rules), same findings schema; one call per world and model, run in
parallel. Writes results.jsonl here (findings, cost, error per call); the llm_client trace id per call is
`s3-review-choice/<world>/<model>`. Run from the repository root:
    uv run --no-project --python 3.12 --with-editable ~/code/llm_client python evidence/declared-laws/s3-review-choice/run_choice.py
"""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from scripts.review_rules import review_rules  # noqa: E402

HERE = Path(__file__).resolve().parent
PENCIL = json.loads((ROOT / "tests/fixtures/pencil13-kept.json").read_text())["description"]
WORLDS = ["pencil13-kept", "pencil2-live", "pencil4-live", "pencil9-live", "pencil-s2-kept", "pencil-s2-2-kept",
          "pencil-s2-3-kept"]
MODELS = ["openrouter/google/gemini-3.1-pro-preview", "openrouter/deepseek/deepseek-v4-flash",
          "openrouter/openai/gpt-6-luna"]  # the last is the rules writer's own model: the same-family control
EFFORT = {"openrouter/deepseek/deepseek-v4-flash": "high"}  # the only effort llm_client allows it


def one(world: str, model: str) -> dict:
    saved = json.loads((ROOT / f"tests/fixtures/{world}.json").read_text())
    # pencil2, pencil4 and pencil9 were built from the same one-line description (the live driver's pencil.txt).
    description = saved.get("description") or PENCIL
    row = {"world": world, "model": model, "trace_id": f"s3-review-choice/{world}/{model.split('/')[-1]}"}
    try:
        row["findings"], row["cost"] = review_rules(description, saved["bundle"], saved["causal_model"],
                                                    trace_id=row["trace_id"], max_budget=0.5, model=model,
                                                    reasoning_effort=EFFORT.get(model, "medium"))
    except Exception as exc:  # recorded, not hidden: a failed review is a result
        row["error"] = f"{type(exc).__name__}: {exc}"[:400]
    return row


if __name__ == "__main__":
    only = sys.argv[1:] or MODELS  # rerun some models, keeping the others' saved rows
    saved = HERE / "results.jsonl"
    kept = [json.loads(line) for line in saved.read_text().splitlines()] if saved.exists() else []
    with ThreadPoolExecutor(max_workers=8) as pool:
        fresh = list(pool.map(lambda wm: one(*wm), [(w, m) for w in WORLDS for m in only]))
    rows = [r for r in kept if r["model"] not in only] + fresh
    with saved.open("w") as out:
        for row in rows:
            out.write(json.dumps(row) + "\n")
    for row in rows:
        print(row["world"], row["model"].split("/")[-1], len(row.get("findings") or []), round(row.get("cost") or 0, 4),
              row.get("error", "")[:120])
    print("RESULT calls=%d errors=%d cost=%.4f" % (len(rows), sum(1 for r in rows if "error" in r),
                                                  sum(r.get("cost") or 0 for r in rows)))
