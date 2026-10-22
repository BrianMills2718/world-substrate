from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_trace_reads import check_run

ROWS = [
    {"path": "/generate-world", "trace_id": "live/people/aaa", "trace_ids": ["live/people/aaa"], "result": {}},
    {"path": "/run", "trace_id": "live/run/bbb", "trace_ids": ["live/run/bbb"], "result": {"transcript": [
        {"turn": 1, "actors": {
            "country-a": {"status": "accepted", "event_id": "r1-e00001"},
            "legal-group": {"status": "refused", "wanted": {"kind": "x"}, "event_id": "r1-e00002"},
            "idle": {"status": "no_action"}}},
        {"turn": 2, "actors": {"country-a": {"status": "accepted", "event_id": "r2-e00001"}}},
    ]}},
]
GOOD = """# Trace read

## Findings

Country A acted every round; the legal group was refused once.

## Round 1

country-a put the matter on the agenda (r1-e00001); legal-group was refused (r1-e00002).
Build trace live/people/aaa: ten briefs, each with private information.

## Round 2

country-a settled it (r2-e00001). Trace live/run/bbb: one resident call per person.
"""


class TraceReadCheckTests(unittest.TestCase):
    def folder(self, read: str | None) -> Path:
        path = Path(tempfile.mkdtemp())
        (path / "run-log.jsonl").write_text("".join(json.dumps(r) + "\n" for r in ROWS))
        if read is not None:
            (path / "TRACE_READ.md").write_text(read)
        return path

    def test_a_complete_read_passes(self):
        self.assertEqual(check_run(self.folder(GOOD)), [])

    def test_a_run_with_no_read_fails(self):
        self.assertIn("no TRACE_READ.md", check_run(self.folder(None))[0])

    def test_a_count_summary_that_skips_rounds_people_and_traces_fails(self):
        # 2026-10-22: the "analysis" was a counting script's output naming 1 of 111 trace ids.
        problems = check_run(self.folder("# Trace read\n\n## Findings\n\n237 moves, 181 accepted.\n"))
        text = "\n".join(problems)
        self.assertIn("trace id never named: live/run/bbb", text)
        self.assertIn("no '## Round 1' section", text)
        self.assertIn("no '## Round 2' section", text)

    def test_each_round_must_name_everyone_who_tried_and_cite_an_event(self):
        read = GOOD.replace("legal-group was refused (r1-e00002)", "one refusal").replace("(r2-e00001)", "")
        text = "\n".join(check_run(self.folder(read)))
        self.assertIn("Round 1 does not mention legal-group", text)
        self.assertIn("Round 2 cites none of its event ids", text)
        self.assertNotIn("idle", text)  # someone who did not try a move need not be named

    def test_findings_must_not_be_empty(self):
        read = GOOD.replace("Country A acted every round; the legal group was refused once.", "")
        self.assertIn("'## Findings' is missing or empty", "\n".join(check_run(self.folder(read))))


if __name__ == "__main__":
    unittest.main()
