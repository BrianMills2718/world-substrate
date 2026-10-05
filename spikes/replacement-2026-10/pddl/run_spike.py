"""Replacement-first spike: can a PDDL toolchain host/ground World Substrate's governed-rules layer?

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 \
        --with unified-planning==1.3.0 --with up-enhsp==0.1.1 \
        --with up-pyperplan==1.1.0 --with up-fast-downward==0.5.2 \
        python spikes/replacement-2026-10/pddl/run_spike.py

Steps (all programmatic from the bundle + causal model; no hand-written PDDL):
 1. translate the constrained-handoff mechanics + initial state into a UP problem and
    write domain.pddl / problem.pddl;
 2. validate the reference trajectory World Substrate accepted (from a direct
    run_native_coordination() run) with UP's SequentialPlanValidator, and show the
    refused approval is rejected on the same failing precondition;
 3. plan to gate `ready` with an off-the-shelf planner and replay that plan through
    World Substrate's engine.discover/engine.submit;
 4. list what the translation could not express.
Exits nonzero if any step fails. Zero LLM/provider spend.
"""

from __future__ import annotations

import importlib.metadata as md
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

import unified_planning as up  # noqa: E402
from unified_planning.engines import PlanGenerationResultStatus, ValidationResultStatus  # noqa: E402
from unified_planning.io import PDDLReader, PDDLWriter  # noqa: E402
from unified_planning.model.walkers import StateEvaluator  # noqa: E402
from unified_planning.plans import ActionInstance, SequentialPlan  # noqa: E402
from unified_planning.shortcuts import (  # noqa: E402
    GE, GT, LE, LT, And, BoolType, Equals, Fluent, InstantaneousAction, IntType, Not,
    Object, OneshotPlanner, PlanValidator, Problem, SequentialSimulator, UserType,
    get_environment,
)

from scripts.run_authored_world import build_engine  # noqa: E402
from scripts.run_native_coordination import DEFAULT_CAUSAL, run_native_coordination  # noqa: E402
from scripts.scaffold_world import load_bundle  # noqa: E402

BUNDLE_PATH = REPO / "examples/native_coordination/constrained-handoff-v0.json"
get_environment().credits_stream = None
FAILURES: list[str] = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def pname(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", text).lower()


class Translator:
    """Bundle + causal model -> unified-planning Problem (lifted, numeric)."""

    def __init__(self, bundle: dict[str, Any], causal: dict[str, Any]) -> None:
        self.bundle, self.causal = bundle, causal
        self.untranslatable: list[str] = []
        self.ftype = {(c["name"], f["name"]): f["type"] for c in bundle["components"] for f in c["fields"]}
        self.Entity = UserType("entity")
        self.Symbol = UserType("symbol")
        self.problem = Problem(pname(bundle["world"]["id"]))
        # PDDL types: one subtype of `entity` per component. Without them ENHSP grounds
        # approve/finalize over 17^6 bindings and exhausts memory (observed: >4 GB, >2 min).
        self.ctype = {c["name"]: UserType(pname(c["name"]), self.Entity) for c in bundle["components"]}
        self.objects = {}
        for e in bundle["entities"]:
            comps = list(e.get("components", {}))
            if len(comps) != 1:
                raise NotImplementedError(f"entity {e['id']} has {len(comps)} components; single-type PDDL objects need 1")
            self.objects[e["id"]] = Object(pname(e["id"]), self.ctype[comps[0]])
        self.symbols: dict[str, Object] = {}
        self.fluents: dict[tuple[str, str], Fluent] = {}
        self.static_eq: dict[tuple, Fluent] = {}
        self.cat: dict[str, Fluent] = {}
        self.has: dict[str, Fluent] = {}
        self.labels: dict[str, list[tuple[str, Any]]] = {}  # action -> [(check label, precondition)]
        self.params: dict[str, list[str]] = {}  # action -> ws field names in UP parameter order
        self.written = {
            tuple(eff["path"].split(".")[1:3]) for m in causal["mechanics"] for eff in m["effects"]
        }
        self.referenced = self._referenced_fields()

    # --- vocabulary -------------------------------------------------------
    def _referenced_fields(self) -> set[tuple[str, str]]:
        refs: set[tuple[str, str]] = set()
        for m in self.causal["mechanics"]:
            for c in m["checks"]:
                for side in (c["left"], c["right"]):
                    if "participant" in side:
                        refs.add(tuple(side["participant"]["path"].split(".")[1:3]))
            for eff in m["effects"]:
                refs.add(tuple(eff["path"].split(".")[1:3]))
                if "participant" in eff["value"]:
                    refs.add(tuple(eff["value"]["participant"]["path"].split(".")[1:3]))
        for c in (self.causal.get("terminal") or {}).get("checks", []):
            refs.add(tuple(c["path"].split(".")[1:3]))
        return refs

    def sym(self, value: str) -> Object:
        if value not in self.symbols:
            self.symbols[value] = Object("s_" + pname(value), self.Symbol)
        return self.symbols[value]

    def fluent(self, comp: str, field: str) -> Fluent:
        key = (comp, field)
        if key not in self.fluents:
            kind = self.ftype[key]
            name = f"{pname(comp)}_{pname(field)}"
            if kind == "boolean":
                f = Fluent(name, BoolType(), e=self.Entity)
            elif kind in ("integer", "number"):
                f = Fluent(name, IntType(), e=self.Entity)
            elif kind == "entity_ref":
                f = Fluent(name, BoolType(), e=self.Entity, v=self.Entity)
            elif kind == "string":
                f = Fluent(name, BoolType(), e=self.Entity, v=self.Symbol)
            else:
                raise ValueError(f"unsupported field type {kind} for {key}")
            self.fluents[key] = f
        return self.fluents[key]

    def selector_pre(self, selector: dict[str, Any], term) -> list[tuple[str, Any]]:
        out = []
        for c in selector.get("categories", []):
            f = self.cat.setdefault(c, Fluent("cat_" + pname(c), BoolType(), e=self.Entity))
            out.append((f"selector category {c}", f(term)))
        for c in selector.get("components", []):
            f = self.has.setdefault(c, Fluent("has_" + pname(c), BoolType(), e=self.Entity))
            out.append((f"selector component {c}", f(term)))
        return out

    # --- expressions --------------------------------------------------------
    def _side(self, side: dict[str, Any], pmap: dict[str, Any]):
        if "participant" in side:
            ref = side["participant"]
            _, comp, field = ref["path"].split(".")
            return ("field", comp, field, pmap[ref["name"]])
        if "literal" in side:
            return ("literal", side["literal"])
        if "entity_id" in side:
            return ("entity", pmap[side["entity_id"]])
        raise NotImplementedError(f"expression kind {list(side)} has no PDDL translation")

    def check_expr(self, check: dict[str, Any], pmap: dict[str, Any], mechanic: str):
        left, right, op = self._side(check["left"], pmap), self._side(check["right"], pmap), check["op"]
        assert left[0] == "field", "checks are field-on-the-left in this bundle"
        _, comp, field, term = left
        kind = self.ftype[(comp, field)]
        f = self.fluent(comp, field)
        if kind in ("integer", "number"):
            lhs = f(term)
            rhs = right[1] if right[0] == "literal" else self.fluent(right[1], right[2])(right[3])
            expr = {"lt": LT, "lte": LE, "gt": GT, "gte": GE, "eq": Equals}[op](lhs, rhs) if op != "ne" else Not(Equals(lhs, rhs))
            return expr
        if kind == "boolean":
            assert right[0] == "literal"
            base = f(term) if right[1] is True else Not(f(term))
        elif kind == "entity_ref":
            assert right[0] == "entity", f"{mechanic}: entity_ref compared to {right[0]}"
            base = f(term, right[1])
        elif kind == "string" and right[0] == "literal":
            base = f(term, self.sym(right[1]))
        elif kind == "string" and right[0] == "field":
            # string field == string field: compiled to a static relation computed from the
            # initial state (sound only because neither field is written by any mechanic).
            rk = (right[1], right[2])
            if (comp, field) in self.written or rk in self.written:
                raise NotImplementedError("dynamic string-to-string equality needs existential quantification")
            key = (comp, field, *rk)
            if key not in self.static_eq:
                self.static_eq[key] = Fluent(
                    f"same_{pname(comp)}_{pname(field)}__{pname(rk[0])}_{pname(rk[1])}",
                    BoolType(), a=self.Entity, b=self.Entity,
                )
            base = self.static_eq[key](term, right[3])
            self.untranslatable.append(
                f"{mechanic}: check '{check['label']}' compares two string fields; translated as a precomputed "
                "static relation (not an existential over symbols, to keep the problem quantifier-free) "
                f"{self.static_eq[key].name} (breaks if a mechanic ever writes either field)"
            )
        else:
            raise NotImplementedError(f"{kind} vs {right[0]}")
        return base if op == "eq" else Not(base)

    # --- build ----------------------------------------------------------------
    def build(self) -> Problem:
        p = self.problem
        for m in self.causal["mechanics"]:
            kind = m["action_kind"]
            names = ["actor", *sorted(m["participants"])]
            sels = {"actor": m["actor_selector"], **m["participants"]}
            ptype = {n: self.ctype[sels[n]["components"][0]] if sels[n].get("components") else self.Entity for n in names}
            action = InstantaneousAction(pname(kind), **{pname(n): ptype[n] for n in names})
            pmap = {n: action.parameter(pname(n)) for n in names}
            self.params[action.name] = names
            labels: list[tuple[str, Any]] = []
            labels += [(f"actor {lab}", e) for lab, e in self.selector_pre(m["actor_selector"], pmap["actor"])]
            for n, sel in sorted(m["participants"].items()):
                labels += [(f"{n} {lab}", e) for lab, e in self.selector_pre(sel, pmap[n])]
            for c in m["checks"]:
                labels.append((c["label"], self.check_expr(c, pmap, m["mechanic_id"])))
            for _, e in labels:
                action.add_precondition(e)
            self.labels[action.name] = labels
            for eff in m["effects"]:
                _, comp, field = eff["path"].split(".")
                kind_t = self.ftype[(comp, field)]
                f = self.fluent(comp, field)
                term = pmap[eff["participant"]]
                val = eff["value"]
                if "literal" in val:
                    v = val["literal"]
                elif "participant" in val:
                    r = val["participant"]
                    _, rc, rf = r["path"].split(".")
                    v = self.fluent(rc, rf)(pmap[r["name"]])
                else:
                    raise NotImplementedError(f"{m['mechanic_id']}: effect value {list(val)} untranslatable")
                if eff["op"] == "add":
                    action.add_increase_effect(f(term), v)
                elif eff["op"] == "subtract":
                    action.add_decrease_effect(f(term), v)
                elif kind_t == "string":
                    for s in self._string_domain(comp, field):
                        action.add_effect(f(term, self.sym(s)), s == v)
                elif kind_t == "entity_ref":
                    raise NotImplementedError("set on entity_ref field")
                else:
                    action.add_effect(f(term), v)
            p.add_action(action)
        self._initial_state()
        self._goal()
        return p

    def _string_domain(self, comp: str, field: str) -> list[str]:
        vals = {e["components"][comp][field] for e in self.bundle["entities"] if comp in e.get("components", {})}
        for m in self.causal["mechanics"]:
            for c in m["checks"]:
                if c["left"].get("participant", {}).get("path") == f"components.{comp}.{field}" and "literal" in c["right"]:
                    vals.add(c["right"]["literal"])
            for eff in m["effects"]:
                if eff["path"] == f"components.{comp}.{field}" and "literal" in eff["value"]:
                    vals.add(eff["value"]["literal"])
        for c in (self.causal.get("terminal") or {}).get("checks", []):
            if c["path"] == f"components.{comp}.{field}":
                vals.add(c["value"])
        return sorted(vals)

    def _initial_state(self) -> None:
        p = self.problem
        p.add_objects(self.objects.values())
        dropped: set[tuple[str, str]] = set()
        for (comp, field) in list(self.referenced):
            self.fluent(comp, field)
        for f in [*self.fluents.values(), *self.cat.values(), *self.has.values(), *self.static_eq.values()]:
            default = 0 if f.type.is_int_type() else False
            p.add_fluent(f, default_initial_value=default)
        for e in self.bundle["entities"]:
            o = self.objects[e["id"]]
            for c in e.get("categories", []):
                if c in self.cat:
                    p.set_initial_value(self.cat[c](o), True)
            for comp, values in e.get("components", {}).items():
                if comp in self.has:
                    p.set_initial_value(self.has[comp](o), True)
                for field, value in values.items():
                    if (comp, field) not in self.referenced:
                        dropped.add((comp, field))
                        continue
                    f, kind = self.fluents[(comp, field)], self.ftype[(comp, field)]
                    if kind == "string":
                        p.set_initial_value(f(o, self.sym(value)), True)
                    elif kind == "entity_ref":
                        if value in self.objects:
                            p.set_initial_value(f(o, self.objects[value]), True)
                    else:
                        p.set_initial_value(f(o), value)
        p.add_objects(self.symbols.values())
        for (c1, f1, c2, f2), rel in self.static_eq.items():
            holders1 = [e for e in self.bundle["entities"] if c1 in e.get("components", {})]
            holders2 = [e for e in self.bundle["entities"] if c2 in e.get("components", {})]
            for a in holders1:
                for b in holders2:
                    if a["components"][c1][f1] == b["components"][c2][f2]:
                        p.set_initial_value(rel(self.objects[a["id"]], self.objects[b["id"]]), True)
        if dropped:
            self.untranslatable.append(
                "fields carried no PDDL fluent because no mechanic reads/writes them (meaning lost, e.g. "
                "information.content 'The shared handoff token is unavailable.'): "
                + ", ".join(f"{c}.{f}" for c, f in sorted(dropped))
            )

    def _goal(self) -> None:
        term = self.causal["terminal"]
        sel = term["selector"]
        matches = [
            e for e in self.bundle["entities"]
            if all(c in e.get("categories", []) for c in sel.get("categories", []))
            and all(c in e.get("components", {}) for c in sel.get("components", []))
        ]
        goals = []
        for e in matches:
            for c in term["checks"]:
                _, comp, field = c["path"].split(".")
                assert c["op"] == "eq" and self.ftype[(comp, field)] == "string"
                goals.append(self.fluents[(comp, field)](self.objects[e["id"]], self.sym(c["value"])))
        if term["mode"] != "all":
            raise NotImplementedError("terminal mode any")
        self.problem.add_goal(And(goals) if len(goals) > 1 else goals[0])
        self.untranslatable.append(
            f"terminal selector ({sel}) was grounded to a fixed entity list {[e['id'] for e in matches]} at "
            "translation time; PDDL has a fixed object set, so entities created during a run cannot exist in the plan"
        )

    # --- plan mapping ---------------------------------------------------------
    def to_up(self, ws_action: dict[str, Any]) -> ActionInstance:
        a = self.problem.action(pname(ws_action["kind"]))
        return ActionInstance(a, [self.problem.object(pname(ws_action[n])) for n in self.params[a.name]])

    def to_ws(self, ai: ActionInstance) -> dict[str, Any]:
        ids = {pname(k): k for k in self.objects}
        row = {"kind": next(m["action_kind"] for m in self.causal["mechanics"] if pname(m["action_kind"]) == ai.action.name)}
        for n, p in zip(self.params[ai.action.name], ai.actual_parameters):
            row[n] = ids[p.object().name]
        return row


def ws_submit(engine: Any, row: dict[str, Any]) -> dict[str, Any]:
    page = engine.discover(row["actor"], kind=row["kind"])
    matches = [
        r for r in [*page["available"], *page["blocked"]]
        if all(r["action"].get(k) == v for k, v in row.items())
    ]
    if len(matches) != 1:
        raise AssertionError(f"discover returned {len(matches)} matches for {row}")
    action = dict(matches[0]["action"], controller="pddl-spike")
    return engine.submit(action)


def failing_labels(tr: Translator, problem: Problem, prefix: list[ActionInstance], ai: ActionInstance) -> tuple[list[str], list[str]]:
    """Return (labels of the translated WS checks that are false, simulator's raw unsatisfied conditions)."""
    with SequentialSimulator(problem=problem) as sim:
        state = sim.get_initial_state()
        for step in prefix:
            state = sim.apply(state, step)
        unsat, _ = sim.get_unsatisfied_conditions(state, ai, full_check=True)
    evaluator = StateEvaluator(problem)
    sub = dict(zip(ai.action.parameters, ai.actual_parameters))
    subst = get_environment().substituter
    false = [lab for lab, e in tr.labels[ai.action.name]
             if not evaluator.evaluate(subst.substitute(e, sub), state).bool_constant_value()]
    return false, [str(u) for u in unsat]


def main() -> int:
    versions = {p: md.version(p) for p in ("unified-planning", "up-enhsp", "up-pyperplan", "up-fast-downward")}
    print("== package versions:", json.dumps(versions))

    bundle = load_bundle(BUNDLE_PATH)
    causal = json.loads(Path(DEFAULT_CAUSAL).read_text())

    # 1. translate + write PDDL
    tr = Translator(bundle, causal)
    problem = tr.build()
    writer = PDDLWriter(problem)
    writer.write_domain(str(OUT / "domain.pddl"))
    writer.write_problem(str(OUT / "problem.pddl"))
    reread = PDDLReader().parse_problem(str(OUT / "domain.pddl"), str(OUT / "problem.pddl"))
    print(f"== 1. translation: {len(problem.actions)} actions, {len(problem.fluents)} fluents, "
          f"{len(problem.all_objects)} objects; wrote domain.pddl/problem.pddl; re-parsed OK "
          f"({len(reread.actions)} actions); problem kind features: {sorted(problem.kind.features)}")

    # 2. reference trajectory from World Substrate itself
    ref = run_native_coordination(bundle, causal)
    attempts = []
    for t in ref["trace"]["transcript"]:
        for row in t["actors"].values():
            if row["did"]:
                attempts.append((row["did"], row["status"], row["refused_because"]))
    accepted = [a for a, s, _ in attempts if s == "accepted"]
    refused_idx = next(i for i, (_, s, _) in enumerate(attempts) if s != "accepted")
    refused_action, _, ws_reason = attempts[refused_idx]
    prefix = [a for a, s, _ in attempts[:refused_idx] if s == "accepted"]
    print(f"== 2. World Substrate reference: {len(accepted)} accepted, refused attempt #{refused_idx + 1} "
          f"{refused_action['actor']}:{refused_action['kind']} because {ws_reason}")

    ref_plan = SequentialPlan([tr.to_up(a) for a in accepted])
    with PlanValidator(problem_kind=problem.kind, plan_kind=ref_plan.kind, name="sequential_plan_validator") as v:
        res = v.validate(problem, ref_plan)
    print(f"   validator verdict, reference plan ({len(accepted)} steps): {res.status.name}")
    if res.status != ValidationResultStatus.VALID:
        fail(f"reference plan invalid: {res.reason} {res.log_messages}")
    # same plan against the PDDL re-read from disk (proves the written files carry the semantics)
    disk_plan = SequentialPlan([
        ActionInstance(reread.action(ai.action.name), [reread.object(p.object().name) for p in ai.actual_parameters])
        for ai in ref_plan.actions
    ])
    with PlanValidator(problem_kind=reread.kind, plan_kind=disk_plan.kind, name="sequential_plan_validator") as v:
        res_disk = v.validate(reread, disk_plan)
    print(f"   validator verdict, reference plan against re-read .pddl files: {res_disk.status.name}")
    if res_disk.status != ValidationResultStatus.VALID:
        fail("reference plan invalid against written PDDL")

    bad_plan = SequentialPlan([tr.to_up(a) for a in prefix] + [tr.to_up(refused_action)])
    with PlanValidator(problem_kind=problem.kind, plan_kind=bad_plan.kind, name="sequential_plan_validator") as v:
        bad = v.validate(problem, bad_plan)
    print(f"   validator verdict, refused-approval plan ({len(bad_plan.actions)} steps): {bad.status.name}; "
          f"inapplicable action: {bad.inapplicable_action}")
    pddl_reason, raw_unsat = failing_labels(tr, problem, bad_plan.actions[:-1], bad_plan.actions[-1])
    print(f"   simulator's unsatisfied precondition(s): {raw_unsat}")
    print(f"   failing PDDL precondition(s) mapped to WS check labels: {pddl_reason}")
    if len(raw_unsat) != len(pddl_reason):
        fail("simulator and label evaluation disagree on the number of failing preconditions")
    if bad.status != ValidationResultStatus.INVALID:
        fail("validator accepted the refused approval")
    if bad.inapplicable_action is None or str(bad.inapplicable_action) != str(bad_plan.actions[-1]):
        fail("validator did not stop at the refused approval")
    if sorted(pddl_reason) != sorted(ws_reason):
        fail(f"failing precondition mismatch: pddl={pddl_reason} ws={ws_reason}")
    else:
        print("   MATCH: PDDL validator and World Substrate refuse on the same precondition")

    # 3. plan with off-the-shelf planners
    for name in ("pyperplan", "fast-downward", "enhsp"):
        with OneshotPlanner(name=name) as planner:
            print(f"   planner {name} supports this problem kind: {planner.supports(problem.kind)}")
    with OneshotPlanner(name="enhsp") as planner:
        result = planner.solve(problem)
    plan = result.plan
    solved = result.status in (PlanGenerationResultStatus.SOLVED_SATISFICING, PlanGenerationResultStatus.SOLVED_OPTIMALLY)
    print(f"== 3. planner enhsp: status={result.status.name} plan length={len(plan.actions) if plan else None}")
    if not solved:
        fail("planner did not find a plan")
        return 1
    for i, ai in enumerate(plan.actions, 1):
        print(f"   {i}. {ai}")
    engine, causal_model, _ = build_engine(bundle, causal)
    statuses = []
    for ai in plan.actions:
        row = tr.to_ws(ai)
        outcome = ws_submit(engine, row)
        statuses.append(outcome["status"])
        if outcome["status"] != "accepted":
            fail(f"engine refused planner step {row}: {[c['label'] for c in outcome['event']['checks'] if not c['ok']]}")
    reached = causal_model.terminal.reached(engine.world)
    gate = next(e for e in engine.world.entities.values() if "gate" in e.category_ids)
    print(f"   engine replay: {statuses.count('accepted')}/{len(statuses)} accepted; terminal reached={reached}; "
          f"gate status={gate.component('gate').status}")
    if not reached:
        fail("engine replay of planner plan did not reach terminal")

    # 4. what PDDL could not express (translation-derived + structural observations from the engine)
    ev = engine.world.events[-1]
    structural = [
        "information delivery/visibility: 'communicate' becomes three boolean flips (info.active, delivery.status, "
        "recipient.aware); PDDL has no notion of who can observe what, so actor-scoped visibility "
        "(world_substrate.information) and asymmetric knowledge are absent; the planner is an omniscient single agent",
        f"write scopes: engine enforces declared writes per mechanic (e.g. last event wrote {ev['declared_write_paths']}); "
        "PDDL effects are the only writes by construction, so there is no separate scope to enforce or violate",
        f"causal-parent recording / event log: engine records event_id, checks, hash_before/after, cause per attempt "
        f"(fields {sorted(ev)}); a PDDL plan is a bare action sequence with no refusals, ids or ancestry",
        "refused attempts as first-class history: World Substrate commits a precondition_failed event; PDDL "
        "validation just declares the whole plan invalid at that step",
        "selectors: categories became static unary predicates (cat_*); PDDL types were derived one per component "
        "because multi-category entities (handoff-token is resource+prereq-a+restorable) do not fit a type tree, "
        "and without types ENHSP grounded approve/finalize over all 6-entity tuples and ran >2 min / >4 GB before being killed",
        "string-valued fields became (field entity symbol) predicates with explicit delete effects over a closed "
        "value domain; any value not seen in bundle/mechanics at translation time is unrepresentable",
        "atomic commit against base_revision / optimistic concurrency and multi-actor turn order: no PDDL analogue",
        "expression kinds owner_ref, action_field, event_id (in the language, unused here) have no translation",
        "agency: the planner chooses every actor (here finalize by bo; WS reference used dev); PDDL is one "
        "centralized omniscient planner, not per-resident policies with private knowledge",
    ]
    print("== 4. untranslatable / lossy features:")
    for item in [*tr.untranslatable, *structural]:
        print(f"   - {item}")

    print(f"== RESULT: {'PASS' if not FAILURES else 'FAIL'} ({len(FAILURES)} failures)")
    return 0 if not FAILURES else 1


if __name__ == "__main__":
    raise SystemExit(main())
