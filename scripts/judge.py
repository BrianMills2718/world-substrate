"""The judge: Concordia's game master rules on an attempt no installed rule covers (ai-judge plan, slice J2).

The judge is Concordia's own `EventResolution` game master component (gdm-concordia 2.4.0), on a game master entity
built from Concordia's stock parts (`EntityAgentWithLogging`, `SwitchAct`, `ListMemory`), not a judge of our own
(Decision 006). Two context components condition it: the whole world (description, things, installed rules,
processes and declared laws, and current values) and the consequence report (`scripts/consequence_report.py`). The
attempt is the putative event in the game master's memory. Our part is the thin resolution steps
(`event_resolution_steps`): each asks one typed question of the document Concordia assembled, so the answer is a
rule in the World Builder's own declaration language (`action-mechanic/v0`), never an outcome.

The order (docs/plans/ai_judge.md, Canonical example):

1. **Propose**, given the world and pass 1: whose choice the attempt needs beyond the person trying (Decided 4), the
   ruling on the constraint only, and the ruling written as one new move with the attempt as its test move.
2. **Pass 2**: the rule goes through the World Builder's rules check and is test-run on a copy of the world as it
   is now (`consequence_report.pass_two`); the judge reads `summary` (net changes, blockers, length, stop).
3. **Review**: confirm, revise once, or withdraw. A revision gets its own pass 2, then a last answer: confirm or
   withdraw. A ruling whose rules check rejects it and whose one revision is rejected too is a language gap.

Nothing is installed here: this module records the ruling; `scripts/rulings.py` (J3) installs it, or holds it for the
owner's approval, per the world's setting. The model
rules review is not run on judge rulings: J2 measured it on the saved sawmill case, where it did not flag the
single-price charge (evidence/ai-judge/j2/sawmill-review/review.json), so per the plan it is dropped.

Every model call goes through llm_client, on the interpreter's model and route.

Implements: ai-judge/the-judge-is-concordia-s-game-master-conditioned-on-the-world-and-the-consequence-report
Implements: ai-judge/the-judge-proposes-a-rule-reads-its-test-run-and-confirms-revises-once-or-withdraws
Implements: ai-judge/another-person-s-choice-goes-to-that-person
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Collection, Mapping, Sequence

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from concordia.agents import entity_agent_with_logging  # noqa: E402
from concordia.components.agent import action_spec_ignored, memory as memory_component  # noqa: E402
from concordia.components.game_master import event_resolution, next_acting, switch_act  # noqa: E402
from concordia.language_model import language_model  # noqa: E402
from concordia.typing import entity as entity_lib  # noqa: E402

from scripts import consequence_report  # noqa: E402

TASK = "world-substrate-judge"
PROMPT = REPO / "prompts/judge_steps.yaml"
BY = "the world's game master (Concordia's EventResolution)"
NO_RULE = "no rule could express this"
MAX_OUTPUT_TOKENS = 4000

_RULE_TEXT = ("The ruling as ONE new move in the world's declaration language: a JSON string holding "
              '{"action": {...}, "mechanic": {...}}, or "" when no constraint question remains.')
_MOVE_TEXT = ('A JSON string: the move\'s fields for this attempt (field name to value; entity ids for entity fields), '
              'plus "actor" when someone other than the person trying makes the move. "" when there is no rule.')

PROPOSE_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False,
    "required": ["facts", "blockers", "whose_choice", "ruling", "proposed_rule", "test_move", "reasoning"],
    "properties": {
        "facts": {"type": "array", "items": {"type": "string"},
                  "description": "The current values that bear on this attempt, each with the value read."},
        "blockers": {"type": "array", "items": {"type": "string"},
                     "description": "What the installed rules' checks or the values say would stop it."},
        "whose_choice": {"type": "string",
                         "description": "The entity id of the person whose decision the attempt needs, or 'none'."},
        "ruling": {"type": "string", "description": "What the world allows here, on the constraint only."},
        "proposed_rule": {"type": "string", "description": _RULE_TEXT},
        "test_move": {"type": "string", "description": _MOVE_TEXT},
        "reasoning": {"type": "string", "description": "One or two sentences on why."},
    },
}


def review_schema(choices: Sequence[str]) -> dict[str, Any]:
    return {
        "type": "object", "additionalProperties": False,
        "required": ["decision", "why", "revised_rule", "revised_test_move"],
        "properties": {
            "decision": {"type": "string", "enum": list(choices)},
            "why": {"type": "string", "description": "One or two sentences, citing the test run."},
            "revised_rule": {"type": "string", "description": "With revise: " + _RULE_TEXT + ' Otherwise "".'},
            "revised_test_move": {"type": "string", "description": "With revise: " + _MOVE_TEXT + ' Otherwise "".'},
        },
    }


class LlmClientModel(language_model.LanguageModel):
    """Concordia's language model interface over llm_client, so every call the game master makes is traced and
    priced under the run's trace id and budget. `sample_json` is the typed call our resolution steps make."""

    def __init__(self, model: str, *, trace_id: str, max_budget: float, task: str = TASK):
        self.model, self.trace_id, self.max_budget, self.task = model, trace_id, max_budget, task
        self.calls: list[dict[str, Any]] = []
        self.cost = 0.0

    def _note(self, kind: str, result: Any) -> None:
        cost = float(getattr(result, "cost", 0.0) or 0.0)
        self.cost += cost
        self.calls.append({"kind": kind, "model": self.model, "task": self.task, "trace_id": self.trace_id,
                           "cost_usd": cost})

    def sample_text(self, prompt: str, *, max_tokens: int = language_model.DEFAULT_MAX_TOKENS,
                    terminators: Collection[str] = language_model.DEFAULT_TERMINATORS,
                    temperature: float = language_model.DEFAULT_TEMPERATURE,
                    top_p: float = language_model.DEFAULT_TOP_P, top_k: int = language_model.DEFAULT_TOP_K,
                    timeout: float = language_model.DEFAULT_TIMEOUT_SECONDS, seed: int | None = None) -> str:
        from llm_client import call_llm

        result = call_llm(self.model, [{"role": "user", "content": prompt}], task=self.task, trace_id=self.trace_id,
                          max_budget=self.max_budget, max_tokens=min(int(max_tokens), MAX_OUTPUT_TOKENS))
        self._note("text", result)
        text = str(getattr(result, "content", "") or "")
        for stop in terminators:
            if stop and stop in text:
                text = text[: text.index(stop)]
        return text

    def sample_choice(self, prompt: str, responses: Sequence[str], *,
                      seed: int | None = None) -> tuple[int, str, Mapping[str, Any]]:
        schema = {"type": "object", "additionalProperties": False, "required": ["choice"],
                  "properties": {"choice": {"type": "string", "enum": list(responses)}}}
        value = self.sample_json([{"role": "user", "content": prompt}], schema, name="choice")
        index = list(responses).index(value["choice"])
        return index, responses[index], {}

    def sample_json(self, messages: list[dict[str, str]], schema: dict[str, Any], *, name: str) -> dict[str, Any]:
        from llm_client import call_llm_json_schema

        value, result = call_llm_json_schema(
            self.model, messages, schema, schema_name=f"world_substrate_judge_{name}", task=self.task,
            trace_id=self.trace_id, max_budget=self.max_budget, max_tokens=MAX_OUTPUT_TOKENS, reasoning_effort="low")
        self._note(name, result)
        return value if isinstance(value, dict) else {}


class Text(action_spec_ignored.ActionSpecIgnored):
    """A context component holding fixed text (the world, or the consequence report)."""

    def __init__(self, label: str, text: str):
        super().__init__(label)
        self._text = text

    def _make_pre_act_value(self) -> str:
        return self._text

    def get_state(self) -> dict[str, Any]:
        return {"text": self._text}

    def set_state(self, state: Mapping[str, Any]) -> None:
        self._text = str(state.get("text", ""))


class Acting(next_acting.NextActing):
    """Concordia's next-acting component with the turn already decided: the person who tried."""

    def __init__(self, model: language_model.LanguageModel, actor: str, people: Sequence[str]):
        super().__init__(model, list(people) or [actor])
        self._currently_active_player = actor

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        return ""


_CONTRACT: list[str] = []


def contract() -> str:
    """The declaration language's contract for a mechanic: the World Builder rule writer's own response contract
    (`scripts/generate_causal_model.py`), shown for an example move with one person field and one amount field."""
    if not _CONTRACT:
        from scripts.generate_causal_model import _mechanic_schema

        example = {"kind": "example-move", "fields": [{"name": "recipient", "type": "entity_ref"},
                                                      {"name": "amount", "type": "integer"}]}
        _CONTRACT.append(json.dumps(_mechanic_schema(example), separators=(",", ":")))
    return _CONTRACT[0]


class Step:
    """One resolution step: a typed question asked of the document EventResolution assembled (the components'
    text and the putative event). The answer goes back into the document and becomes the event statement."""

    def __init__(self, model: LlmClientModel, name: str, schema: dict[str, Any], **words: Any):
        self.model, self.name, self.schema, self.words = model, name, schema, words
        self.answer: dict[str, Any] | None = None
        self.document_chars = 0

    def __call__(self, document: Any, premise: str, active_player_name: str) -> str:
        from llm_client import render_prompt

        text = document.view().text()
        self.document_chars = len(text)
        messages = render_prompt(PROMPT, step=self.name, document=text, actor=active_player_name,
                                 contract=contract(), **self.words)
        self.answer = self.model.sample_json(messages, self.schema, name=self.name)
        statement = json.dumps(self.answer, ensure_ascii=False)
        document.statement(statement)
        return statement


def world_text(bundle: dict[str, Any], causal_value: dict[str, Any], engine: Any) -> str:
    """The whole world, as the plain version read it: description, kinds of thing and moves, rules, and every thing
    with its current values. The things are given once, as they are now (the bundle's starting copy of them is left
    out), in compact JSON: the long line (5,000 knock-on steps) is 305,042 characters indented with both copies and
    about 123,000 this way."""
    shown = {k: v for k, v in bundle.items() if k not in {"presentation", "entities"}}

    def compact(value: Any) -> str:
        return json.dumps(value, separators=(",", ":"), ensure_ascii=False, default=str)

    return "\n\n".join([
        "Description: " + str((bundle.get("world") or {}).get("summary") or ""),
        "Kinds of thing, moves and declared laws (authoring bundle, without its things):\n" + compact(shown),
        "Installed rules and processes:\n" + compact(causal_value),
        f"Every thing and its current values (revision {engine.world.revision}):\n"
        + compact(engine.world.material_dict()["entities"]),
    ])


def resolve(model: LlmClientModel, step: Step, *, actor: str, attempt: str, people: Sequence[str],
            world: str, consequence: str) -> dict[str, Any]:
    """One game master turn: Concordia's EventResolution resolves the putative event with `step` as its one
    resolution step. Returns the step's typed answer."""
    resolution = event_resolution.EventResolution(
        model=model, event_resolution_steps=[step], components=["world", "consequence"])
    gm = entity_agent_with_logging.EntityAgentWithLogging(
        agent_name="game master",
        act_component=switch_act.SwitchAct(model=model, entity_names=list(people) or [actor]),
        context_components={
            "world": Text("The world", world),
            "consequence": Text("What the engine worked out (the consequence report)", consequence),
            memory_component.DEFAULT_MEMORY_COMPONENT_KEY: memory_component.ListMemory(
                memory_bank=[f"{event_resolution.PUTATIVE_EVENT_TAG} {actor}: {attempt}"]),
            next_acting.DEFAULT_NEXT_ACTING_COMPONENT_KEY: Acting(model, actor, people),
            event_resolution.DEFAULT_RESOLUTION_COMPONENT_KEY: resolution,
        },
    )
    gm.act(entity_lib.ActionSpec(call_to_action="Resolve the putative event.",
                                 output_type=entity_lib.OutputType.RESOLVE))
    if step.answer is None:
        raise RuntimeError("the game master's resolution step gave no answer")
    return step.answer


def _parse(text: Any) -> tuple[dict[str, Any] | None, str | None]:
    """A JSON object from a judge answer field, or (None, why not)."""
    if not str(text or "").strip():
        return None, None
    try:
        value = json.loads(text)
    except (TypeError, ValueError) as error:
        return None, f"not JSON: {error}"
    return (value, None) if isinstance(value, dict) else (None, "not a JSON object")


def _test(bundle: dict[str, Any], causal_value: dict[str, Any], engine: Any, actor: str,
          rule_text: Any, move_text: Any) -> dict[str, Any]:
    """Pass 2 for one proposed rule and test move: the full report (with the chain) and the summary the judge
    reads. A rule that is not even a JSON object is a rejection by the rules check, like any malformed rule."""
    rule, rule_error = _parse(rule_text)
    if rule is None:
        report = {"rules_check": {"ok": False, "error": rule_error or "no rule given"}, "test_run": None}
        return {"rule": None, "move": None, "report": report, "summary": report}
    fields, _ = _parse(move_text)
    fields = dict(fields or {})
    kind = str((rule.get("action") or {}).get("kind") or (rule.get("mechanic") or {}).get("action_kind") or "")
    move = {"actor": str(fields.pop("actor", actor) or actor), "kind": kind, **fields}
    report = consequence_report.pass_two(bundle, causal_value, engine, rule, move)
    return {"rule": rule, "move": move, "report": report, "summary": consequence_report.summary(report)}


def _report_text(pass_one: dict[str, Any], test: dict[str, Any] | None = None, label: str = "") -> str:
    parts = ["Pass 1, before any rule exists (the moves and checks open to the person trying and to each person "
             "named, and the named things' current values):\n" + json.dumps(pass_one, indent=1, default=str)]
    if test is not None:
        parts.append(f"Pass 2, the test run of {label or 'your proposed rule'} (rules check, then the rule run on a "
                     "copy of the world as it is now; nothing is installed):\n"
                     + json.dumps({"move": test["move"], **test["summary"]}, indent=1, default=str))
    return "\n\n".join(parts)


def judge(bundle: dict[str, Any], causal_value: dict[str, Any], engine: Any, *, actor: str, attempt: str,
          pass_one: dict[str, Any], people: Sequence[str], model: str, trace_id: str,
          max_budget: float) -> dict[str, Any]:
    """Rule on one unmatched attempt. `engine` is the world as it was when the attempt was tried (the caller passes
    a copy when the real world moves on); it is only read. Returns the ruling record for the run."""
    llm = LlmClientModel(model, trace_id=trace_id, max_budget=max_budget)
    world = world_text(bundle, causal_value, engine)
    steps: list[dict[str, Any]] = []

    def ask(name: str, schema: dict[str, Any], consequence: str, **words: Any) -> dict[str, Any]:
        step = Step(llm, name, schema, **words)
        answer = resolve(llm, step, actor=actor, attempt=attempt, people=people, world=world, consequence=consequence)
        steps.append({"step": name, "answer": answer, "document_chars": step.document_chars,
                      "consequence": consequence})
        return answer

    proposed = ask("propose", PROPOSE_SCHEMA, _report_text(pass_one))
    whose = str(proposed.get("whose_choice") or "none")
    record: dict[str, Any] = {
        "by": BY, "model": model, "trace_id": trace_id,
        "whose_choice": whose if whose in people and whose != actor else None,
        "ruling": proposed.get("ruling") or "", "reasoning": proposed.get("reasoning") or "",
        "facts": list(proposed.get("facts") or []), "blockers": list(proposed.get("blockers") or []),
        "world_chars": len(world), "world_revision": engine.world.revision,
    }
    if not str(proposed.get("proposed_rule") or "").strip():
        record.update(outcome="no_rule", rule=None, tests=[])
        return _finish(record, steps, llm)
    first = _test(bundle, causal_value, engine, actor, proposed.get("proposed_rule"), proposed.get("test_move"))
    tests = [first]
    review = ask("review", review_schema(["confirm", "revise", "withdraw"]), _report_text(pass_one, first))
    decision = review.get("decision")
    final, why = first, review.get("why") or ""
    if decision == "revise":
        second = _test(bundle, causal_value, engine, actor, review.get("revised_rule"), review.get("revised_test_move"))
        tests.append(second)
        final = second
        if second["report"]["rules_check"]["ok"]:
            last = ask("final", review_schema(["confirm", "withdraw"]),
                       _report_text(pass_one, second, "your revised rule"), revised=True)
            decision, why = last.get("decision"), last.get("why") or why
        else:
            decision = "language_gap" if not first["report"]["rules_check"]["ok"] else "withdraw"
            why = (f"{NO_RULE}: the rules check rejected the rule and its one revision "
                   f"({second['report']['rules_check'].get('error')})") if decision == "language_gap" else (
                "the revision failed the rules check: " + str(second["report"]["rules_check"].get("error")))
    elif decision == "confirm" and not first["report"]["rules_check"]["ok"]:
        decision, why = "withdraw", "a rule the rules check rejected cannot be confirmed: " + str(
            first["report"]["rules_check"].get("error"))
    outcome = {"confirm": "confirmed", "withdraw": "withdrawn", "language_gap": "language_gap"}.get(str(decision),
                                                                                                   "withdrawn")
    record.update(outcome=outcome, why=why, revised=len(tests) > 1,
                  rule=final["rule"] if outcome == "confirmed" else None,
                  move=final["move"] if outcome == "confirmed" else None,
                  tests=[{"rule": t["rule"], "move": t["move"], **t["report"]} for t in tests])
    return _finish(record, steps, llm)


def _finish(record: dict[str, Any], steps: list[dict[str, Any]], llm: LlmClientModel) -> dict[str, Any]:
    record["steps"] = steps
    record["calls"] = llm.calls
    record["cost_usd"] = llm.cost
    return record


def frozen(engine: Any) -> Any:
    """A read-only copy of the world as it is now, under the same installed rules, for a judge run later in the
    round (the real world moves on with the moves after the attempt)."""
    from world_substrate.engine import Engine

    return Engine(deepcopy(engine.world), engine.registry, reaction_limit=None)


__all__ = ["BY", "LlmClientModel", "NO_RULE", "TASK", "frozen", "judge", "resolve", "world_text"]
