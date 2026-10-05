"""Variant 1 (compose): Mesa owns model/agent loop, activation and data collection;
the World Substrate Engine is the sole consequence authority."""
from __future__ import annotations

from typing import Any

import mesa

from scripts.run_authored_world import build_engine
from scripts.run_native_coordination import (
    _authorized_member, _entity_with_category, _members, _report_plan, _required_approvals,
)

CONTROLLER = "mesa-spike"


def scripted_plan(bundle: dict[str, Any]) -> list[tuple[str, str, dict[str, str], str]]:
    """Same choices as run_native_coordination(), as (actor, kind, fields, expected)."""
    gate = _entity_with_category(bundle, "gate")
    prereqs = {f"prereq_{x}": _entity_with_category(bundle, f"prereq-{x}") for x in "abcd"}
    authorized = _authorized_member(bundle)
    reports = _report_plan(bundle)
    plan = [(src, "communicate", {"information": info, "delivery": dl, "recipient": rc}, "accepted")
            for src, info, dl, rc in reports]
    voters = [rc for *_, rc in reports]
    plan.append((voters[0], "approve", {"gate": gate, **prereqs}, "precondition_failed"))
    plan.append((authorized, "intervene", {"resource": _entity_with_category(bundle, "restorable")}, "accepted"))
    plan += [(v, "approve", {"gate": gate, **prereqs}, "accepted") for v in voters[: _required_approvals(bundle)]]
    plan.append((authorized, "finalize", {"gate": gate, **prereqs}, "accepted"))
    return plan


class MemberAgent(mesa.Agent):
    """A Mesa agent that can only discover and submit through the Engine."""

    def __init__(self, model: "HandoffModel", actor_id: str):
        super().__init__(model)
        self.actor_id = actor_id
        self.intents: dict[int, tuple[str, dict[str, str], str]] = {}
        self.last_status: str | None = None

    def step(self) -> None:
        intent = self.intents.get(self.model.steps)
        if intent is None:
            self.last_status = None
            return
        kind, fields, expected = intent
        page = self.model.engine.discover(self.actor_id, kind=kind)
        rows = [r for r in [*page["available"], *page["blocked"]]
                if all(r["action"].get(k) == v for k, v in fields.items())]
        if len(rows) != 1:
            raise AssertionError(f"{self.actor_id} {kind}: {len(rows)} matching actions")
        action = dict(rows[0]["action"], controller=CONTROLLER)
        outcome = self.model.engine.submit(action)
        if outcome["status"] != expected:
            raise AssertionError(f"{self.actor_id} {kind}: {outcome['status']} != {expected}")
        self.last_status = outcome["status"]
        self.model.outcomes.append((self.actor_id, kind, outcome))


class HandoffModel(mesa.Model):
    def __init__(self, bundle: dict[str, Any], causal_value: dict[str, Any], rng: int = 7):
        super().__init__(rng=rng)
        self.engine, self.causal_model, self.profile_id = build_engine(bundle, causal_value)
        self.gate_id = _entity_with_category(bundle, "gate")
        self.outcomes: list[tuple[str, str, dict[str, Any]]] = []
        by_actor = {a: MemberAgent(self, a) for a in _members(bundle)}
        for index, (actor, kind, fields, expected) in enumerate(scripted_plan(bundle), start=1):
            by_actor[actor].intents[index] = (kind, fields, expected)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "gate_status": lambda m: m._gate()["status"],
                "approval_count": lambda m: m._gate()["approval_count"],
                "event_count": lambda m: len(m.engine.world.events),
                "revision": lambda m: m.engine.world.revision,
            },
            agent_reporters={"actor": "actor_id", "last_status": "last_status"},
        )

    def _gate(self) -> dict[str, Any]:
        return self.engine.world.material_dict()["entities"][self.gate_id]["components"]["gate"]

    def terminal(self) -> bool:
        return self.causal_model.terminal.reached(self.engine.world)

    def step(self) -> None:
        self.agents.do("step")  # Mesa activation; deterministic insertion order
        self.datacollector.collect(self)
