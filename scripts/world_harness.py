"""Write a people world's rules inside an agent harness (Decision 008).

Instead of one bare call for all the rules plus our own retry loop, Codex works in a scratch workspace that holds the
world (people, things, the actions without rules) and one command, `./check`. The check runs the same causal compiler
and scripted test run the World Builder uses, and prints exact problems: an action with no rule, a rule the compiler
rejects, people who cannot act, a world that goes in circles. Codex writes `rules.json`, runs the check, makes small
edits and repeats until the check passes or its time runs out.

    python -m scripts.world_harness prepare DESCRIPTION_FILE WORKSPACE   # people + actions (two bare calls, as before)
    python -m scripts.world_harness check WORKSPACE                      # what the agent runs
    python -m scripts.world_harness write WORKSPACE                      # run Codex until the check passes

Full trace: WORKSPACE/codex-events.jsonl is every Codex event (commands it ran with their output, its messages and
token use); WORKSPACE/checks.jsonl appends every check result. The Codex home is a clean folder beside the workspace,
so no operator rules, hooks or skills load.
"""
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from scripts.generate_causal_model import WORLD_KIND_RULES, _context, causal_model_schema
from scripts.people_world import PIPELINE, _pipeline, actions_to_write, assemble_people_world, rules_guidance
from scripts.run_authored_world import run_world

REPO = Path(__file__).resolve().parents[1]
DRY_RUN_TURNS = 24  # the same length as world_builder_service's DRY_RUN_TURNS_CONTINUING
HARNESS_MODEL = os.environ.get("WORLD_BUILDER_HARNESS_MODEL") or "openai/gpt-6-luna"  # an OpenRouter model id
HARNESS_EFFORT = os.environ.get("WORLD_BUILDER_HARNESS_EFFORT") or "medium"
# OpenRouter list prices per million tokens (2026-10-16) for reporting a run's cost from Codex's token counts.
PRICES = {"openai/gpt-6-luna": (0.10, 0.50), "openai/gpt-5.6-luna": (0.20, 1.20), "openai/gpt-5.6-sol": (4.0, 20.0)}

AGENTS_MD = """# Write the rules of this world

This folder holds a simulated world: people with goals, the things they work on, and the actions they can try.
Your job is `rules.json`: finish the one rule ("mechanic") already started there for each action, and add any
processes the world needs, so that `./check` passes. If the world has no record for the work an action does (a
review, a plan, a person's readiness), add one to `records.json` and give the action an `entity_ref` field naming it
in `actions.json`; `./check` then rebuilds `world.json` with the new record's entity, component and paths.

Files you edit: `rules.json`, `records.json` (the world's records: `record_id`, `kind`, `label`, `public_state` as
`[{"key", "value"}]`, `hidden_state`, `visible_to_actor_ids`; a field `x` becomes path `components.<record_id>.x` on
entity `<record_id with each _ turned into ->`), and `actions.json` (only to add or change fields; keep every action kind, and
name an entity field after the record it points to). The rest are read-only:
- `world.json`: the world, its components (with fields), entities, `initial_builtin_state`, `allowed_state_paths`
  (rebuilt by `./check` from `records.json`).
- `example_rule.json`: one finished, correct rule from this world, for the exact JSON shape.
- `compiled_rules.json`: rules that already exist (support, concerns, the decision, meetings, passing information).
  Your rules may read the components they own but never write them.
- `schema.json`: the full JSON Schema of `rules.json`, only if `./check` points you to a shape question.
- `prepared.json`, `spec.json`, `check`: what the check uses; you do not need to read them.

How to work:
1. Read this file, `actions.json`, `example_rule.json` and the parts of `world.json` you need. Do not read source
   code outside this folder; `./check` tells you exactly what is wrong.
2. Within your first few steps, write a complete first draft of every rule in `rules.json`. A rough draft that the
   check can test beats long planning.
3. Run `./check`. Fix exactly what it names with small edits, and run it again. Repeat until it prints
   `CHECK PASSED` (exit 0). Then stop.

Rule shape, in short: `actor_selector` and each participant are `{"categories": [...], "components": [...]}`
(list every component whose fields that participant's checks or effects use). Expressions are one of
`{"literal": v}`, `{"action_field": name}`, `{"participant": {"name": n, "path": p}}`, `{"entity_id": n}`,
`{"owner_ref": n}`, where `n` is `actor` or a participant name. Checks are `{"label", "left", "op", "right"}` with op
in eq, ne, lt, lte, gt, gte, contains; effects are `{"participant", "path", "op": set|add|subtract, "value"}`.
Every path is copied exactly from `allowed_state_paths`. `checks`, `effects`, `limits` and `tests` each need at least
one entry; `limits` and `tests` are short plain sentences. Processes (at most 6 of yours) are
`{"process_id", "rationale", "selector", "checks", "effects"}` acting on each matching entity `it`.

## What the rules must do

{guidance}

## Rules you must follow

{authority}
"""

TASK = ("Read AGENTS.md. Write a full first draft of rules.json quickly, then run ./check after every small edit and "
        "fix only what it reports. Stop when it prints CHECK PASSED.")


def _spec_class():
    if str(PIPELINE) not in sys.path:
        sys.path.insert(0, str(PIPELINE))
    from scenario_spec import ScenarioSpecV1
    return ScenarioSpecV1


def save_prepared(prepared: dict[str, Any], ws: Path, guidance: str = "") -> None:
    """Lay out the workspace for one rules build."""
    ws.mkdir(parents=True, exist_ok=True)
    keep = {k: prepared[k] for k in ("bundle", "compiled", "coverage", "sigs")}
    (ws / "prepared.json").write_text(json.dumps(keep, indent=1))
    (ws / "spec.json").write_text(prepared["spec"].model_dump_json(indent=1))
    to_write = actions_to_write(prepared)
    context = _context(to_write)
    world = {k: context[k] for k in ("world", "components", "entities", "initial_builtin_state", "allowed_state_paths")}
    (ws / "world.json").write_text(json.dumps(world, indent=1))
    if not (ws / "actions.json").exists():
        (ws / "actions.json").write_text(json.dumps(to_write["actions"], indent=1))
    if not (ws / "records.json").exists():
        (ws / "records.json").write_text(json.dumps(
            [r.model_dump() for r in prepared["spec"].world_records], indent=1))
    (ws / "schema.json").write_text(json.dumps(causal_model_schema(to_write), indent=1))
    (ws / "compiled_rules.json").write_text(json.dumps(prepared["compiled"], indent=1))
    example = next((m for m in prepared["compiled"]["mechanics"] if m["action_kind"] != "communicate"),
                   prepared["compiled"]["mechanics"][0])
    (ws / "example_rule.json").write_text(json.dumps(example, indent=1))
    authority = "\n".join(f"- {r}" for r in [*context["authority_rules"], WORLD_KIND_RULES["ongoing"]])
    (ws / "AGENTS.md").write_text(AGENTS_MD.replace("{guidance}", rules_guidance(prepared, guidance))
                                  .replace("{authority}", authority))
    if not (ws / "rules.json").exists():
        (ws / "rules.json").write_text(json.dumps(_skeleton(prepared["compiled"]["schema_version"], to_write), indent=1))
    if not (ws / ".git").exists():  # its own repository, so Codex loads no AGENTS.md from folders above
        subprocess.run(["git", "init", "-q", str(ws)], check=True)
    env = f"PYTHONDONTWRITEBYTECODE=1 PYTHONPATH={shlex.quote(str(REPO))}"
    # The check needs only pydantic; a `uv run` interpreter is temporary, so WORLD_HARNESS_PYTHON can name a lasting one.
    python = os.environ.get("WORLD_HARNESS_PYTHON") or sys.executable
    (ws / "check").write_text(
        f"#!/bin/sh\ncd {shlex.quote(str(REPO))} && {env} exec {shlex.quote(python)} -m scripts.world_harness "
        f"check {shlex.quote(str(ws.resolve()))}\n")
    (ws / "check").chmod(0o755)


def _skeleton(schema_version: str, to_write: dict[str, Any]) -> dict[str, Any]:
    """One started rule per action: the agent fills in selectors, checks and effects."""
    from world_substrate.action_authoring import ACTION_MECHANIC_SCHEMA_VERSION
    mechanics = []
    for action in to_write["actions"]:
        fields = action.get("fields") or []
        mechanics.append({
            "schema_version": ACTION_MECHANIC_SCHEMA_VERSION, "mechanic_id": f"generated.{action['kind']}",
            "version": "1", "action_kind": action["kind"], "rationale": "",
            "actor_selector": {"categories": [], "components": []},
            "participants": {f["name"]: {"categories": [], "components": []} for f in fields if f["type"] == "entity_ref"},
            "parameters": {f["name"]: [] for f in fields if f["type"] != "entity_ref"},
            "checks": [], "effects": [], "limits": [], "tests": [], "semantic_bindings": [],
        })
    return {"schema_version": schema_version, "mechanics": mechanics, "processes": [], "terminal": None}


def load_prepared(ws: Path) -> dict[str, Any]:
    prepared = json.loads((ws / "prepared.json").read_text())
    prepared["spec"] = _spec_class().model_validate_json((ws / "spec.json").read_text())
    return prepared


def _refusals(dry: dict[str, Any], actors: list[str]) -> dict[str, list[str]]:
    """Latest distinct refusal reasons per actor in the test run (same reading as the service's idle guidance)."""
    reasons: dict[str, list[str]] = {}
    for turn in reversed(dry.get("transcript") or []):
        for actor in actors:
            for blocked in (turn["actors"].get(actor) or {}).get("blocked_by_rules") or []:
                values = "; ".join(f"{f.get('check')}: was {f.get('actual')!r}, needed {f.get('required')!r}"
                                   for f in blocked.get("failed") or [])
                line = f"{blocked['action'].get('kind', '?')}: {values or blocked.get('reason', '')}"
                if line not in reasons.setdefault(actor, []) and len(reasons[actor]) < 3:
                    reasons[actor].append(line)
    return reasons


def check(ws: Path) -> tuple[bool, list[str], dict[str, Any] | None]:
    """Compile and test-run the workspace's rules. Returns (passed, problems, built world or None)."""
    from world_substrate.action_authoring import CausalModel

    try:
        prepared = rebuild(ws)
    except Exception as error:
        return False, [f"records.json or actions.json is not usable: {type(error).__name__}: {error}"[:1500]], None
    try:
        generated = json.loads((ws / "rules.json").read_text())
    except (OSError, json.JSONDecodeError) as error:
        return False, [f"rules.json is not valid JSON: {error}"], None
    to_write = actions_to_write(prepared)
    wanted = [a["kind"] for a in to_write["actions"]]
    have = [m.get("action_kind") for m in generated.get("mechanics") or [] if isinstance(m, dict)]
    problems = [f"no rule for action {k}" for k in wanted if k not in have]
    problems += [f"rule for {k}, which is not an action in actions.json (remove it)" for k in have if k not in wanted]
    problems += [f"more than one rule for action {k}" for k in sorted({k for k in have if have.count(k) > 1})]
    if problems:
        return False, problems, None
    # Compile each rule on its own first, so every broken rule is named at once, not only the first.
    by_kind = {a["kind"]: a for a in to_write["actions"]}
    for m in generated.get("mechanics") or []:
        one = {**generated, "mechanics": [m], "processes": [], "terminal": None}
        try:
            CausalModel.from_dict(one, bundle={**to_write, "actions": [by_kind[m["action_kind"]]]})
        except Exception as error:
            problems.append(f"rule for {m['action_kind']}: {type(error).__name__}: {error}")
    if problems:
        return False, problems, None
    try:
        CausalModel.from_dict(generated, bundle=to_write)
    except Exception as error:  # the compiler's message is the exact problem
        return False, [f"the causal compiler rejected rules.json: {type(error).__name__}: {error}"], None
    try:
        built = assemble_people_world(prepared, generated)
    except Exception as error:
        return False, [f"the rules do not fit with the compiled rules: {type(error).__name__}: {error}"], None
    removed = [d for d in built["dropped_generated_rules"] if "dropped" in d or "removed" in d]
    problems += [f"{d} (write only components you own; the compiled rules already do this)" for d in removed]
    problems += _dead_writes(built["causal_model"], {m["action_kind"] for m in generated.get("mechanics") or []})
    try:
        dry, _, _ = run_world(built["bundle"], built["causal_model"], policy="scripted", max_turns=DRY_RUN_TURNS)
    except ValueError as error:
        return False, problems + [f"a test run failed from the starting state: {error}"], built
    summary = dry["summary"]
    mechanics = len(built["causal_model"]["mechanics"])
    if mechanics >= 3 and len(summary.get("moves_at_end") or []) <= 1:
        problems.append(
            f"in a {DRY_RUN_TURNS}-round test with simple moves, only {', '.join(summary.get('moves_at_end') or ['nothing'])} "
            "still happened in the last third: the world went in circles. Add the missing reverse rules and limits so "
            "different moves stay possible.")
    stuck = sorted(set(summary.get("idle_actors") or []) | set(summary.get("stalled_actors") or []))
    reasons = _refusals(dry, stuck)
    for actor in stuck:
        never = actor in (summary.get("idle_actors") or [])
        problems.append(
            f"{actor} {'never changed anything' if never else 'stopped changing anything in the last third'} in the "
            f"{DRY_RUN_TURNS}-round test; refused: {'; '.join(reasons.get(actor) or ['no action was offered to them'])}. "
            "Make sure some action or process gives them something real to do again.")
    built["dry_run"] = summary
    return not problems, problems, built


def rebuild(ws: Path) -> dict[str, Any]:
    """The prepared world with the agent's records and action fields: recompile the spec, keep its action kinds."""
    compile_spec, _ = _pipeline()
    prepared = load_prepared(ws)
    spec = prepared["spec"]
    if (ws / "records.json").exists():
        data = json.loads(spec.model_dump_json())
        data["world_records"] = json.loads((ws / "records.json").read_text())
        spec = type(spec).model_validate(data)
    bundle, compiled, coverage = compile_spec.compile_spec(spec)
    original = {a["kind"] for a in actions_to_write(prepared)["actions"]}
    actions = json.loads((ws / "actions.json").read_text()) if (ws / "actions.json").exists() else [
        a for a in prepared["bundle"]["actions"] if a["kind"] in original]
    kinds = [a.get("kind") for a in actions]
    if set(kinds) != original or len(kinds) != len(original):
        raise ValueError(f"actions.json must keep exactly these action kinds: {sorted(original)}; it has {kinds}")
    compiled_kinds = {a["kind"] for a in bundle["actions"]}
    bundle["actions"] = bundle["actions"] + [{k: a[k] for k in ("kind", "description", "fields")} for a in actions
                                             if a["kind"] not in compiled_kinds]
    fields = {a["kind"]: a["fields"] for a in actions}
    sigs = [{**sig, "fields": fields.get(sig["kind"], sig.get("fields"))} for sig in prepared["sigs"]]
    out = {"spec": spec, "bundle": bundle, "compiled": compiled, "coverage": coverage, "sigs": sigs}
    context = _context(actions_to_write(out))
    world = {k: context[k] for k in ("world", "components", "entities", "initial_builtin_state", "allowed_state_paths")}
    (ws / "world.json").write_text(json.dumps(world, indent=1))
    return out


def _paths(exprs: list[Any]) -> set[str]:
    out = set()
    for e in exprs:
        ref = e.get("participant") if isinstance(e, dict) else None
        if isinstance(ref, dict) and isinstance(ref.get("path"), str):
            out.add(ref["path"])
    return out


def _dead_writes(causal: dict[str, Any], generated_kinds: set[str]) -> list[str]:
    """A generated action's change that no other rule ever reads changes nothing in the world (2026-10-16 inc15k and
    the first harness run: every action set one shared text field that only a reset process looked at). A process
    that only resets the field does not count as a reader."""
    rules = [("action", m["action_kind"], m) for m in causal["mechanics"]] + [
        ("process", p["process_id"], p) for p in causal.get("processes") or []]
    reads: dict[str, set[str]] = {}
    for kind_, name, rule in rules:
        written = {e["path"] for e in rule.get("effects") or []}
        for c in rule.get("checks") or []:
            for path in _paths([c.get("left"), c.get("right")]):
                # An action that checks a field counts as using it (a next step waiting on this one), even if it
                # also writes it; a process that writes the field it checks is only resetting it.
                if kind_ == "action" or path not in written:
                    reads.setdefault(path, set()).add(name)
    problems = []
    for kind_, name, rule in rules:
        if kind_ != "action" or name not in generated_kinds:
            continue
        for path in sorted({e["path"] for e in rule.get("effects") or []}):
            if not (reads.get(path, set()) - {name}):
                problems.append(f"rule for {name} changes {path}, but no other rule ever checks it, so the change "
                                "makes no difference to anyone. Change a record that another person's action, a "
                                "process or the decision depends on, or make another rule depend on this one.")
    return problems


def _log_check(ws: Path, passed: bool, problems: list[str]) -> None:
    with (ws / "checks.jsonl").open("a") as f:
        f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "passed": passed, "problems": problems}) + "\n")


def codex_home(ws: Path) -> Path:
    """A clean Codex home: only the OpenRouter provider, no rules, hooks or skills."""
    home = ws.parent / f"{ws.name}-codex-home"
    home.mkdir(parents=True, exist_ok=True)
    (home / "config.toml").write_text(
        'model_provider = "openrouter"\n'
        '[model_providers.openrouter]\nname = "OpenRouter"\nbase_url = "https://openrouter.ai/api/v1"\n'
        'env_key = "OPENROUTER_API_KEY"\nwire_api = "responses"\n')
    return home


def write_rules(ws: Path, *, model: str = HARNESS_MODEL, effort: str = HARNESS_EFFORT, timeout_s: int = 420,
                on_event=None) -> dict[str, Any]:
    """Run Codex in the workspace until ./check passes or time runs out. Returns the outcome with token use."""
    env = {**os.environ, "CODEX_HOME": str(codex_home(ws))}
    if not env.get("OPENROUTER_API_KEY"):
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    common = ["--json", "--skip-git-repo-check", "-m", model, "-c", f"model_reasoning_effort={effort}",
              "-c", 'sandbox_mode="workspace-write"']
    started = time.monotonic()
    usage = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0}
    timed_out, thread_id, turns, exit_code = False, None, 0, None
    prompt = TASK
    # Codex may end its turn before ./check passes (2026-10-16 h6, low effort: it reported the failure and stopped
    # after 79 s). Resume the same session with the check's output until it passes or the time runs out.
    while not timed_out:
        turns += 1
        cmd = (["codex", "exec", *common, prompt] if thread_id is None
               else ["codex", "exec", "resume", *common, thread_id, prompt])
        with (ws / "codex-events.jsonl").open("a") as log:
            proc = subprocess.Popen(cmd, env=env, cwd=ws, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                    text=True, stdin=subprocess.DEVNULL)
            assert proc.stdout is not None
            for line in proc.stdout:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    event = {"type": "text", "text": line.rstrip("\n")}
                log.write(json.dumps({"t": round(time.monotonic() - started, 1), "turn": turns, **event}) + "\n")
                log.flush()
                if event.get("type") == "thread.started":
                    thread_id = thread_id or event.get("thread_id")
                if event.get("type") == "turn.completed":
                    for k in usage:
                        usage[k] += int((event.get("usage") or {}).get(k) or 0)
                if on_event:
                    on_event(event)
                if time.monotonic() - started > timeout_s:
                    timed_out = True
                    proc.kill()
                    break
            exit_code = proc.wait()
        passed, problems, _ = check(ws)
        if passed or thread_id is None or time.monotonic() - started > timeout_s - 20:
            break
        prompt = ("./check still fails with these problems:\n" + "\n".join(f"- {p}" for p in problems[:20])
                  + "\nKeep going: fix them with small edits and run ./check again until it prints CHECK PASSED.")
    passed, problems, built = check(ws)
    _log_check(ws, passed, problems)
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    cost = ((usage["input_tokens"] - usage["cached_input_tokens"]) * price_in
            + usage["cached_input_tokens"] * price_in * 0.25 + usage["output_tokens"] * price_out) / 1e6
    return {"passed": passed, "problems": problems, "built": built, "seconds": round(time.monotonic() - started, 1),
            "timed_out": timed_out, "exit_code": exit_code, "turns": turns, "usage": usage, "cost_usd_estimate": round(cost, 4),
            "model": model, "effort": effort}


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "check":
        ws = Path(argv[1])
        passed, problems, _ = check(ws)
        _log_check(ws, passed, problems)
        for p in problems:
            print("PROBLEM:", p)
        print("CHECK PASSED" if passed else f"CHECK FAILED: {len(problems)} problem(s)")
        return 0 if passed else 1
    if len(argv) >= 3 and argv[0] == "prepare":
        from scripts.people_world import prepare_people_world
        description = Path(argv[1]).read_text()
        trace_id = f"world-harness/{Path(argv[2]).name}"
        prepared = prepare_people_world(description, trace_id=trace_id, max_budget=0.5,
                                        progress=lambda *a: print(*a[:2], flush=True))
        save_prepared(prepared, Path(argv[2]))
        print("workspace ready:", argv[2], "trace", trace_id)
        return 0
    if len(argv) >= 2 and argv[0] == "write":
        ws = Path(argv[1])
        save_prepared(load_prepared(ws), ws)  # refresh AGENTS.md and ./check
        out = write_rules(ws, on_event=lambda e: print(json.dumps(e)[:300], flush=True))
        built = out.pop("built")
        if built is not None:
            (ws / "built.json").write_text(json.dumps({k: v for k, v in built.items() if k != "coverage"}, indent=1))
        print(json.dumps(out, indent=1))
        return 0 if out["passed"] else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
