"""Concordia residents for live play (Decision 006: host resident loops on Concordia, add no cognition of our own).

Each person in a people world is a Concordia EntityAgentWithLogging. Its context component is the person's own
memory (what they observed and what they did, newest last); its acting component makes one typed llm_client call
that names an offered action, the person's current belief and the effect they expect. The Engine stays the only
authority: a resident only picks among the actions the installed rules offer, and the game master stays off
(an unlisted intent is not offered, so it cannot be chosen).

Live play runs one round per request, so a resident's memory travels with the run: `memory_state()` returns it and
`Residents(memory=...)` restores it, bounded by MEMORY_ITEMS and MEMORY_ITEM_CHARS.

Ported from the October 8 resident loop, spikes/any-scenario-2026-10/run_scenario.py (ObservationLog,
LLMAttemptAct), with the World Builder's offered-action menu in place of the spike's index menu.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from concordia.agents import entity_agent_with_logging
from concordia.typing import entity as entity_lib
from concordia.typing import entity_component

from scripts.run_authored_world import MEMORY_ITEM_CHARS, MEMORY_ITEMS, WAIT

REPO = Path(__file__).resolve().parents[1]

RESIDENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["belief", "action_id", "expected_effect", "work", "reasoning"],
    "properties": {
        "belief": {"type": "string", "description": "What you believe about your situation right now, in one or two sentences."},
        "action_id": {"type": "string", "description": "The action_id you choose, copied exactly from the brackets, or 'wait'."},
        "expected_effect": {"type": "string", "description": "What you expect this to change, in one sentence."},
        "work": {"type": "string", "description": "If the action starts work that takes several rounds, what that work will concretely decide, do or produce (for a concern: your answer to its question, or that it leaves the question open), since you and the others it concerns are shown these words when it finishes. Otherwise 'none'."},
        "reasoning": {"type": "string", "description": "One sentence on why, from your own goals and what you know."},
    },
}

# Open attempts (docs/plans/open_attempt.md): the person says in their own words what they physically try, in place of
# an offered action_id. src/world_substrate/attempt.py reads the words into one typed move; the rules decide its effect.
OPEN_SCHEMA: dict[str, Any] = json.loads(json.dumps(RESIDENT_SCHEMA))
OPEN_SCHEMA["required"] = ["belief", "attempt", "expected_effect", "work", "reasoning"]
del OPEN_SCHEMA["properties"]["action_id"]
OPEN_SCHEMA["properties"]["attempt"] = {
    "type": "string",
    "description": "What you physically try to do this turn, in your own words, naming the people, things and places "
                   "involved; or 'wait'.",
}


def _clip(text: str) -> str:
    return text if len(text) <= MEMORY_ITEM_CHARS else text[: MEMORY_ITEM_CHARS - 3] + "..."


class ResidentMemory(entity_component.ContextComponent):
    """This person's own observations and moves, newest last (the spike's ObservationLog)."""

    def __init__(self, items: list[str] | None = None):
        super().__init__()
        self._items = [_clip(str(x)) for x in (items or [])][-MEMORY_ITEMS:]

    def pre_observe(self, observation: str) -> str:
        self._items = (self._items + [_clip(observation)])[-MEMORY_ITEMS:]
        return ""

    def pre_act(self, action_spec: entity_lib.ActionSpec) -> str:
        return "\n---\n".join(self._items)

    def get_state(self) -> dict[str, Any]:
        return {"items": list(self._items)}

    def set_state(self, state: dict[str, Any]) -> None:
        self._items = list(state.get("items", []))[-MEMORY_ITEMS:]


class ResidentAct(entity_component.ActingComponent):
    """One typed llm_client call returning belief, offered action and expected effect (the spike's LLMAttemptAct)."""

    def __init__(self, actor: str, *, model: str, trace_id: str, max_budget: float, open_attempts: bool = False):
        super().__init__()
        self._actor, self._model, self._trace, self._budget = actor, model, trace_id, max_budget
        self._open = open_attempts
        self.request: dict[str, Any] = {}
        self.cost = 0.0

    def get_action_attempt(self, context: Any, action_spec: entity_lib.ActionSpec) -> str:
        from llm_client import call_llm_json_schema, render_prompt

        if self._open:
            schema, prompt = json.loads(json.dumps(OPEN_SCHEMA)), "prompts/concordia_resident_open_attempt.yaml"
        else:
            schema, prompt = json.loads(json.dumps(RESIDENT_SCHEMA)), "prompts/concordia_resident_policy.yaml"
            schema["properties"]["action_id"]["enum"] = list(self.request["offered"]) + [WAIT]
        memory = "\n".join(str(v) for v in context.values() if v)
        messages = render_prompt(REPO / prompt, **self.request["context"], memory=memory)
        value, result = call_llm_json_schema(
            self._model, messages, schema, schema_name="world_substrate_concordia_resident",
            task="world-builder-concordia-resident", trace_id=self._trace, max_budget=self._budget,
            max_tokens=640, reasoning_effort="low",
        )
        self.cost += float(getattr(result, "cost", 0.0) or 0.0)
        return json.dumps(value if isinstance(value, dict) else {})

    def get_state(self) -> dict[str, Any]:
        return {}

    def set_state(self, state: dict[str, Any]) -> None:
        pass


class Residents:
    """The Concordia agents for one live request, one per person."""

    def __init__(self, actors: list[str], *, model: str, trace_id: str, max_budget: float,
                 memory: dict[str, list[str]] | None = None, open_attempts: bool = False):
        self.open_attempts = open_attempts
        self.acts = {a: ResidentAct(a, model=model, trace_id=trace_id, max_budget=max_budget,
                                    open_attempts=open_attempts) for a in actors}
        self.memory = {a: ResidentMemory((memory or {}).get(a)) for a in actors}
        self.agents = {
            a: entity_agent_with_logging.EntityAgentWithLogging(
                agent_name=a, act_component=self.acts[a], context_components={"memory": self.memory[a]})
            for a in actors
        }

    def observe(self, actor: str, text: str) -> None:
        self.agents[actor].observe(text)

    def choose(self, actor: str, offered: list[str], context: dict[str, Any]) -> dict[str, Any]:
        """The resident's attempt: belief, action_id (an offered id or wait), expected_effect, work, reasoning.

        With open attempts it is `attempt` (their own words) in place of action_id, asked even when nothing is offered.
        """
        if self.open_attempts:
            self.acts[actor].request = {"offered": offered, "context": context}
            spec = entity_lib.ActionSpec(call_to_action="Say what you try.", output_type=entity_lib.OutputType.FREE)
            value = json.loads(self.agents[actor].act(spec) or "{}")
            return {k: (str(value[k]) if value.get(k) is not None else None) for k in OPEN_SCHEMA["required"]}
        if not offered:
            return {"belief": None, "action_id": WAIT, "expected_effect": None, "work": None,
                    "reasoning": "wait: no offered action"}
        self.acts[actor].request = {"offered": offered, "context": context}
        spec = entity_lib.ActionSpec(call_to_action="Choose one offered action.", output_type=entity_lib.OutputType.FREE)
        value = json.loads(self.agents[actor].act(spec) or "{}")
        return {k: (str(value[k]) if value.get(k) is not None else None) for k in RESIDENT_SCHEMA["required"]}

    def cost(self) -> float:
        return sum(act.cost for act in self.acts.values())

    def memory_state(self) -> dict[str, list[str]]:
        return {a: m.get_state()["items"] for a, m in self.memory.items()}
