"""Pass 2 of the consequence report on this run's world as it stood at Vik's offer (round 2, revision 2): the coin
rule a judge would propose (tests/judge_worlds.py coin_rule) test-run with Vik handing Rosa 40 coins. The world is
rebuilt by submitting round 1's two accepted moves from run-log.jsonl in order; nothing calls a model.

  uv run --no-project --python 3.12 --with pydantic --with pyyaml --with gdm-concordia==2.4.0 \
      python evidence/ai-judge/j1/port/pass_two.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts import consequence_report as report  # noqa: E402
from scripts.run_authored_world import build_engine  # noqa: E402
from tests.judge_worlds import coin_rule  # noqa: E402

row = json.loads((HERE / "run-log.jsonl").read_text().splitlines()[0])
bundle, rules = row["request"]["bundle"], row["request"]["causal_model"]
engine, _, _ = build_engine(bundle, rules, reaction_limit=None)
for actor in ("rosa", "vik"):  # round 1 in the order it committed (Rosa's inspection first, then Vik's declaration)
    did = row["result"]["transcript"][0]["actors"][actor]["did"]
    out = engine.submit({**did, "base_revision": engine.world.revision})
    assert out["status"] == "accepted", out["status"]
offer = row["result"]["transcript"][1]["actors"]["vik"]
assert offer["did"]["kind"] == "unmatched-attempt" and engine.world.revision == offer["did"]["base_revision"]
two = report.pass_two(bundle, rules, engine, coin_rule(),
                      {"actor": "vik", "kind": "hand-coins", "to": "rosa", "amount": 40})
out = {"attempt": offer["did"]["attempt"], "names": offer["did"].get("names"), "rule": coin_rule(),
       "report": two, "what_the_judge_reads": report.summary(two)}
(HERE / "pass-two.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps(report.summary(two)["test_run"], indent=1))
