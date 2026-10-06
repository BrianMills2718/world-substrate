"""The declared system model (docs/model/world_substrate_model.toml) matches the code.

No model calls, no network. The code is read with the Python parser and compared
with the model in both directions, so a new, renamed or removed event status,
command op, run-row status, record schema, API route or run-log path fails here
until docs/model/ is updated.

What is extracted, and from where:

- Engine event statuses: the literal ``status=`` given to ``Engine._event`` and
  the literal status argument given to ``Engine._reject`` in
  src/world_substrate/engine.py.
- Engine command ops: dict literals with an ``"op"`` key in the same file.
- Run-row statuses the run loop writes itself (not the Engine):
  dict literals with a literal ``"status"`` in scripts/run_authored_world.py.
- Record schemas: string literals of the form ``world-substrate-<name>/v<N>``
  (plus ``world-builder-<name>/v<N>``) in src/, scripts/ and reference_worlds/
  that are not just the right-hand side of a comparison.
- World Builder API routes: ``path == "/x"`` tests inside the request handler's
  ``do_GET``/``do_POST`` in scripts/world_builder_service.py.
- Run log: the ``LOGGED_PATHS`` tuple and the paths ``_result_summary`` keeps a
  specific summary for.

Line numbers in the model are documentation; the test enforces file and
function, so a drifted line is a documentation fix, not a failure.
"""

from __future__ import annotations

import ast
import re
import tomllib
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "docs" / "model" / "world_substrate_model.toml"
COVERAGE_PATH = ROOT / "docs" / "model" / "VIEW_COVERAGE.md"
ENGINE = ROOT / "src" / "world_substrate" / "engine.py"
RUN_LOOP = ROOT / "scripts" / "run_authored_world.py"
SERVICE = ROOT / "scripts" / "world_builder_service.py"
SCHEMA_ROOTS = ("src", "scripts", "reference_worlds")
SCHEMA_RE = re.compile(r"^world-(?:substrate|builder)-[a-z0-9-]+/v[0-9]+$")
COVERAGE_VALUES = {"shown", "partial", "hidden", "missing", "n/a"}


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _function_at(tree: ast.Module, line: int) -> str:
    """Innermost function containing ``line``; ``<module>`` when none does."""
    best: ast.AST | None = None
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = node.end_lineno or node.lineno
            if node.lineno <= line <= end:
                if best is None or (end - node.lineno) < ((best.end_lineno or best.lineno) - best.lineno):  # type: ignore[attr-defined]
                    best = node
    return best.name if best is not None else "<module>"  # type: ignore[attr-defined]


def _str(node: ast.AST | None) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _sites(found: dict[str, list[dict[str, Any]]], name: str, path: Path, tree: ast.Module, line: int) -> None:
    found.setdefault(name, []).append({"file": _rel(path), "function": _function_at(tree, line), "line": line})


def engine_event_statuses() -> dict[str, list[dict[str, Any]]]:
    tree = _parse(ENGINE)
    found: dict[str, list[dict[str, Any]]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr == "_event":
            for keyword in node.keywords:
                status = _str(keyword.value) if keyword.arg == "status" else None
                if status:
                    _sites(found, status, ENGINE, tree, node.lineno)
        elif node.func.attr == "_reject" and len(node.args) >= 4:
            status = _str(node.args[3])
            if status:
                _sites(found, status, ENGINE, tree, node.lineno)
    return found


def _dict_literal_values(path: Path, key: str) -> dict[str, list[dict[str, Any]]]:
    tree = _parse(path)
    found: dict[str, list[dict[str, Any]]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for k, v in zip(node.keys, node.values):
            if _str(k) == key and _str(v):
                _sites(found, _str(v), path, tree, v.lineno)  # type: ignore[arg-type]
    return found


def engine_command_ops() -> dict[str, list[dict[str, Any]]]:
    return _dict_literal_values(ENGINE, "op")


def run_row_statuses() -> dict[str, list[dict[str, Any]]]:
    return _dict_literal_values(RUN_LOOP, "status")


def record_schemas() -> dict[str, list[dict[str, Any]]]:
    found: dict[str, list[dict[str, Any]]] = {}
    for root in SCHEMA_ROOTS:
        for path in sorted((ROOT / root).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            tree = _parse(path)
            compared: set[int] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Compare):
                    for side in [node.left, *node.comparators]:
                        compared.add(id(side))
            for node in ast.walk(tree):
                value = _str(node)
                if value and SCHEMA_RE.match(value) and id(node) not in compared:
                    _sites(found, value, path, tree, node.lineno)  # type: ignore[attr-defined]
    return found


def api_routes() -> set[str]:
    tree = _parse(SERVICE)
    routes: set[str] = set()
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef) or fn.name not in {"do_GET", "do_POST"}:
            continue
        method = fn.name[3:]
        for node in ast.walk(fn):
            if isinstance(node, ast.Compare) and len(node.comparators) == 1 and isinstance(node.ops[0], ast.Eq):
                route = _str(node.comparators[0])
                if route and route.startswith("/"):
                    routes.add(f"{method} {route}")
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "startswith"
                and node.args
                and (_str(node.args[0]) or "").endswith("/")
            ):
                routes.add(f"{method} {_str(node.args[0])}*")
    return routes


def run_log_paths() -> tuple[set[str], set[str]]:
    """(paths logged at all, paths whose result keeps a specific summary)."""
    tree = _parse(SERVICE)
    logged: set[str] = set()
    summarised: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "LOGGED_PATHS" for t in node.targets):
            assert isinstance(node.value, ast.Tuple)
            logged = {_str(e) for e in node.value.elts}  # type: ignore[misc]
        if isinstance(node, ast.FunctionDef) and node.name == "_result_summary":
            for inner in ast.walk(node):
                if (
                    isinstance(inner, ast.If)
                    and isinstance(inner.test, ast.Compare)
                    and isinstance(inner.test.left, ast.Name)
                    and inner.test.left.id == "path"
                ):
                    route = _str(inner.test.comparators[0])
                    if route:
                        summarised.add(route)
    return logged, summarised


def load_model() -> dict[str, Any]:
    with MODEL_PATH.open("rb") as handle:
        return tomllib.load(handle)


class SystemModelMatchesCode(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.model = load_model()
        assert cls.model.get("schema") == "world-substrate-system-model/v1"

    def _compare(self, kind: str, declared_rows: list[dict[str, Any]], in_code: dict[str, list[dict[str, Any]]]) -> None:
        # code_name: the literal in code, when the model renames it to keep names
        # unique across tables (the command op "invalid_action" vs the event status).
        declared = {row.get("code_name", row["name"]): row for row in declared_rows}
        self.assertEqual(len(declared), len(declared_rows), f"duplicate {kind} names in the model")
        self.assertEqual(sorted(set(in_code) - set(declared)), [], f"{kind} written in code but not declared in the model")
        self.assertEqual(sorted(set(declared) - set(in_code)), [], f"{kind} declared in the model but no longer written in code")
        for name, row in declared.items():
            want = {(w["file"], w["function"]) for w in row["writers"]}
            got = {(w["file"], w["function"]) for w in in_code[name]}
            self.assertEqual(want, got, f"{kind} {name!r}: declared writers differ from code {sorted(got)}")

    def test_engine_event_statuses(self) -> None:
        self._compare("engine event status", self.model["engine_events"], engine_event_statuses())

    def test_engine_command_ops(self) -> None:
        self._compare("engine command op", self.model["engine_commands"], engine_command_ops())

    def test_run_row_statuses(self) -> None:
        self._compare("run-row status", self.model["run_row_statuses"], run_row_statuses())

    def test_record_schemas(self) -> None:
        self._compare("record schema", self.model["records"], record_schemas())

    def test_api_routes(self) -> None:
        declared = {route for process in self.model["processes"] for route in process.get("routes", [])}
        self.assertEqual(sorted(api_routes() - declared), [], "API routes in code but not in any model process")
        self.assertEqual(sorted(declared - api_routes()), [], "API routes in the model but not in code")

    def test_run_log_paths(self) -> None:
        logged, summarised = run_log_paths()
        run_log = self.model["run_log"]
        self.assertEqual(set(run_log["logged_paths"]), logged)
        self.assertEqual(set(run_log["summarised_paths"]), summarised)

    def test_model_is_internally_consistent(self) -> None:
        processes = {p["name"]: p for p in self.model["processes"]}
        self.assertEqual(len(processes), len(self.model["processes"]), "duplicate process names")
        entities = {e["name"] for e in self.model["entities"]}
        written = {
            row["name"]
            for table in ("engine_events", "engine_commands", "run_row_statuses", "records")
            for row in self.model[table]
        }
        for process in processes.values():
            for name in process.get("writes", []):
                self.assertIn(name, written, f"process {process['name']} writes undeclared {name!r}")
            for name in process.get("changes", []):
                self.assertIn(name, entities, f"process {process['name']} changes undeclared entity {name!r}")
        for table in ("engine_events", "engine_commands", "run_row_statuses", "records"):
            for row in self.model[table]:
                for process in row.get("written_by", []):
                    self.assertIn(process, processes, f"{row['name']} names unknown process {process}")
                    self.assertIn(row["name"], processes[process].get("writes", []), f"{process} does not list {row['name']}")

    def test_view_coverage_names_only_declared_elements(self) -> None:
        views = {v["name"] for v in self.model["views"]}
        names = (
            {e["name"] for e in self.model["entities"]}
            | {p["name"] for p in self.model["processes"]}
            | {
                row["name"]
                for table in ("engine_events", "engine_commands", "run_row_statuses", "records")
                for row in self.model[table]
            }
        )
        for row in self.model["coverage"]:
            self.assertIn(row["element"], names, f"coverage row names undeclared element {row['element']!r}")
            self.assertEqual(set(row["views"]), views, f"coverage row {row['element']!r} must give every view")
            for view, value in row["views"].items():
                self.assertIn(value, COVERAGE_VALUES, f"{row['element']} / {view}: {value!r}")
        text = COVERAGE_PATH.read_text(encoding="utf-8")
        for gap in self.model["gaps"]:
            self.assertIn(gap["id"], text, f"gap {gap['id']} is not described in VIEW_COVERAGE.md")
            self.assertIn(gap.get("status"), {"open", "fixed"}, f"gap {gap['id']} needs status open or fixed")
            section = text.split(f"### {gap['id']}.", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
            self.assertEqual("**Fixed " in section, gap["status"] == "fixed",
                             f"gap {gap['id']}: model status and VIEW_COVERAGE.md disagree")


if __name__ == "__main__":
    unittest.main()
