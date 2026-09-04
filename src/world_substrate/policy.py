"""Policy adapters: choose an action, never author an effect.

Per the roadmap's enabling-policy boundary and
docs/decisions/001-project-scope.md, a policy — scripted, human, or LLM —
selects from actions the world has already determined are possible. It cannot
describe, invent, or cause a consequence. Installed mechanics alone compute
what a choice does.

The seam that makes this true is `resolve_choice`: whatever a policy returns is
matched against the `action_id` values the engine itself produced for the
current revision. Anything else is refused and recorded. No policy output is
ever parsed into an action, so no prose can become an effect even if the model
returns something that looks like one.

Nothing here imports a provider SDK. The LLM adapter goes through the approved
shared `llm_client` and its required task/trace/budget contract.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol

from .engine import Engine

WAIT = "wait"


@dataclass(frozen=True)
class Choice:
    """A resolved selection: either a discovered action, a wait, or a refusal."""

    kind: str  # "action" | "wait" | "refused"
    action_id: str | None = None
    action: dict[str, Any] | None = None
    reasoning: str = ""
    refusal_reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "action_id": self.action_id,
            "action": self.action,
            "reasoning": self.reasoning,
            "refusal_reason": self.refusal_reason,
        }


class Policy(Protocol):
    """Returns an action_id string. It never returns an action."""

    name: str

    def select(self, page: dict[str, Any], context: dict[str, Any]) -> tuple[str, str]:
        """Return (action_id, reasoning). `action_id` may be anything at all."""
        ...


def resolve_choice(page: dict[str, Any], action_id: str, reasoning: str) -> Choice:
    """Match a policy's answer against what the world actually offered.

    This is the whole consequence boundary. `page` is the engine's own
    `discover()` output at the current revision, and its `action_id` values are
    engine-computed hashes of engine-generated actions. A policy that returns
    anything not in that set gets a refusal, not an effect.
    """
    if action_id == WAIT:
        return Choice(kind="wait", reasoning=reasoning)
    for row in page["available"]:
        if row["action_id"] == action_id:
            return Choice(
                kind="action",
                action_id=action_id,
                action=dict(row["action"]),
                reasoning=reasoning,
            )
    blocked = {row["action_id"] for row in page["blocked"]}
    if action_id in blocked:
        return Choice(
            kind="refused",
            action_id=action_id,
            reasoning=reasoning,
            refusal_reason="names an action the world currently blocks",
        )
    return Choice(
        kind="refused",
        action_id=action_id,
        reasoning=reasoning,
        refusal_reason="names no action the world offered at this revision",
    )


def apply_choice(
    engine: Engine, choice: Choice, controller: str
) -> dict[str, Any] | None:
    """Commit a resolved choice through the untrusted-envelope path.

    Deliberately `Engine.submit`, not `Engine.apply`: submit is the entry point
    that validates an envelope's shape and types before any typed rule sees it,
    so a policy-originated action crosses exactly the same boundary as any
    other untrusted input rather than a privileged one.
    """
    if choice.kind != "action" or choice.action is None:
        return None
    return engine.submit({**choice.action, "controller": controller})


def describe_action(action: dict[str, Any]) -> str:
    """A short natural description of a discovered action, for presentation only."""
    kind = action.get("kind", "?")
    parts = [
        f"{key} {action[key]}"
        for key in ("vessel", "source", "destination", "target", "volume_ml")
        if key in action
    ]
    return f"{kind}: " + ", ".join(str(part) for part in parts) if parts else str(kind)


def present(engine: Engine, actor_id: str, page: dict[str, Any]) -> dict[str, Any]:
    """A compact, lossy view of the observation for a policy to read.

    Presentation only. Shrinking what a policy sees cannot grant it authority;
    the action list is still the engine's, and every id is still checked.
    """
    actor = engine.world.entities[actor_id]
    observation = page["observation"]
    # Describe whatever the actor actually has. The first version of this read
    # actor.health and actor.hydration directly, which put Castaway content in
    # the shared policy module and crashed on any world whose actors are not
    # survivors (M6 finding).
    self_bits: list[str] = []
    if actor.actor is not None:
        self_bits.append(f"health {actor.actor.health}")
        self_bits.append(f"hydration {actor.actor.hydration}")
    for name in sorted(actor.components):
        component = actor.components[name]
        self_bits.extend(
            f"{field} {value}"
            for field, value in sorted(vars(component).items())
            if isinstance(value, (int, str))
        )
    visible = []
    for entity_id, record in sorted(observation["entities"].items()):
        if entity_id == actor_id:
            continue
        bits = []
        if record.get("liquid"):
            liquid = record["liquid"]
            if liquid["volume_ml"]:
                bits.append(f"{liquid['volume_ml']}ml")
                if liquid["pathogens"]:
                    bits.append("untreated")
                else:
                    bits.append("treated")
            else:
                bits.append("empty")
        if record.get("thermal"):
            bits.append(f"{record['thermal']['temperature_c']}C")
        if record.get("container", {}).get("heat_source_id"):
            bits.append("on the fire")
        if record.get("heat_source"):
            bits.append(f"fuel {record['heat_source']['fuel']}")
        if record.get("ownership"):
            bits.append(f"held by {record['ownership']['owner_ref']}")
        for name, fields in sorted((record.get("components") or {}).items()):
            rendered = ", ".join(
                f"{key} {value}"
                for key, value in sorted(fields.items())
                if value is not None and value != ""
            )
            if rendered:
                bits.append(f"{name}: {rendered}")
        visible.append(f"{record['label']} ({entity_id}): " + ", ".join(bits))
    return {
        "tick": engine.world.tick,
        "actor_id": actor_id,
        "actor_state": ", ".join(self_bits) or "nothing notable",
        "visible": "\n".join(visible),
        "actions": [
            {
                "number": index,
                "action_id": row["action_id"],
                "description": describe_action(row["action"]),
            }
            for index, row in enumerate(page["available"], start=1)
        ],
    }


CHOICE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["action_id", "reasoning"],
    "properties": {
        "action_id": {
            "type": "string",
            "description": (
                "The action_id of the single action you choose, copied exactly "
                "from the brackets in the list, or 'wait' to do nothing."
            ),
        },
        "reasoning": {
            "type": "string",
            "description": "One sentence on why, in plain language.",
        },
    },
}


class ScriptedPolicy:
    """A fixed sequence of action_ids. Used to test the seam without spend."""

    def __init__(self, answers: list[str], name: str = "scripted") -> None:
        self.name = name
        self._answers = list(answers)

    def select(self, page: dict[str, Any], context: dict[str, Any]) -> tuple[str, str]:
        if not self._answers:
            return WAIT, "script exhausted"
        return self._answers.pop(0), "scripted"


class ThirstyPolicy:
    """Drinks whenever it can, otherwise fills. A baseline with no foresight.

    Not a strawman for its own sake: it is the behaviour a policy exhibits when
    it reads the affordance list and optimises the obvious immediate need. The
    world, not the prompt, is what punishes it -- untreated water carries
    pathogens and DrinkRule turns those into health loss.
    """

    name = "thirsty-baseline"

    def select(self, page: dict[str, Any], context: dict[str, Any]) -> tuple[str, str]:
        rows = page["available"]
        for row in rows:
            if row["action"]["kind"] == "drink":
                return row["action_id"], "thirsty: drink whatever is to hand"
        for row in rows:
            if row["action"]["kind"] == "fill":
                return row["action_id"], "nothing to drink: fill something"
        return (rows[0]["action_id"], "take the first thing offered") if rows else (WAIT, "nothing offered")


class LlmPolicy:
    """An LLM chooses one already-offered action through the shared client."""

    def __init__(
        self,
        *,
        model: str,
        trace_id: str,
        max_budget: float,
        template: str = "prompts/castaway_policy.yaml",
        name: str = "llm",
        reasoning_effort: str = "low",
    ) -> None:
        self.name = name
        self.model = model
        self.trace_id = trace_id
        self.max_budget = max_budget
        self.template = template
        # The shared client forbids provider defaults here and requires an
        # explicit choice. Selecting one item from an enumerated menu is not a
        # reasoning-heavy task, and this run is under a hard spend cap.
        self.reasoning_effort = reasoning_effort
        self.calls: list[dict[str, Any]] = []

    def select(self, page: dict[str, Any], context: dict[str, Any]) -> tuple[str, str]:
        from llm_client import call_llm_json_schema, render_prompt

        offered = [row["action_id"] for row in page["available"]]
        schema = json.loads(json.dumps(CHOICE_SCHEMA))
        # Constrain what the model can even say. The seam does not depend on
        # this working -- resolve_choice checks regardless -- but there is no
        # reason to invite an invalid answer we would only refuse.
        schema["properties"]["action_id"]["enum"] = offered + [WAIT]

        messages = render_prompt(self.template, **context)
        value, result = call_llm_json_schema(
            self.model,
            messages,
            schema,
            schema_name="world_substrate_policy_choice",
            task="world-substrate-castaway-policy",
            trace_id=self.trace_id,
            max_budget=self.max_budget,
            reasoning_effort=self.reasoning_effort,
        )
        self.calls.append(
            {
                "tick": context.get("tick"),
                "cost_usd": getattr(result, "cost", None),
                "model": getattr(result, "model", self.model),
                "offered": len(offered),
            }
        )
        if not isinstance(value, dict):
            return "", "model returned a non-object"
        return str(value.get("action_id", "")), str(value.get("reasoning", ""))
