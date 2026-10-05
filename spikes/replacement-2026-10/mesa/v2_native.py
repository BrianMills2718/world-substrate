"""Variant 2 (replace): constrained-handoff rules hand-written in Mesa, no Engine."""
from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

import mesa

from scripts.run_native_coordination import (
    _authorized_member, _entity_with_category, _members, _report_plan, _required_approvals,
)


class Refused(Exception):
    def __init__(self, failed: list[str]):
        super().__init__(", ".join(failed))
        self.failed = failed


class NativeMember(mesa.Agent):
    def __init__(self, model: "NativeHandoffModel", actor_id: str):
        super().__init__(model)
        self.actor_id = actor_id
        self.intents: dict[int, tuple[str, dict[str, str]]] = {}
        self.last_status: str | None = None

    # --- rules, as Python code -------------------------------------------
    def _c(self, eid: str, comp: str) -> dict[str, Any]:
        return self.model.state[eid][comp]

    def _require(self, checks: list[tuple[str, bool]]) -> None:
        failed = [label for label, ok in checks if not ok]
        if failed:
            raise Refused(failed)

    def communicate(self, information: str, delivery: str, recipient: str) -> None:
        info, dl = self._c(information, "information"), self._c(delivery, "delivery")
        self._require([
            ("Actor is the represented information source", info["source_id"] == self.actor_id),
            ("Delivery names the represented information", dl["info_id"] == information),
            ("Delivery names the represented recipient", dl["recipient_id"] == recipient),
            ("Delivery channel agrees with information channel", dl["channel_id"] == info["channel_id"]),
            ("Information is not active yet", info["active"] is False),
            ("Delivery is pending", dl["status"] == "pending"),
        ])
        info["active"] = True
        dl["status"] = "delivered"
        self._c(recipient, "member")["aware"] = True

    def _healthy(self, prereqs: dict[str, str]) -> list[tuple[str, bool]]:
        return [(f"Prerequisite {k[-1].upper()} is healthy",
                 self._c(v, "resource")["current"] >= self._c(v, "resource")["required"])
                for k, v in sorted(prereqs.items())]

    def approve(self, gate: str, **prereqs: str) -> None:
        me, g = self._c(self.actor_id, "member"), self._c(gate, "gate")
        self._require([
            ("Member received represented coordination information", me["aware"] is True),
            ("Member has not already approved", me["approved"] is False),
            ("Gate remains blocked", g["status"] == "blocked"),
            ("Approval threshold has not already been met", g["approval_count"] < g["required_approvals"]),
            *self._healthy(prereqs),
        ])
        me["approved"] = True
        g["approval_count"] += 1

    def intervene(self, resource: str) -> None:
        r = self._c(resource, "resource")
        self._require([
            ("Member holds represented intervention authorization", self._c(self.actor_id, "member")["authorized"] is True),
            ("Restorable resource is below requirement", r["current"] < r["required"]),
        ])
        r["current"] = r["required"]

    def finalize(self, gate: str, **prereqs: str) -> None:
        g = self._c(gate, "gate")
        self._require([
            ("Gate remains blocked", g["status"] == "blocked"),
            ("Approval threshold is met", g["approval_count"] >= g["required_approvals"]),
            *self._healthy(prereqs),
        ])
        g["status"] = "ready"

    # --- Mesa activation ---------------------------------------------------
    def step(self) -> None:
        intent = self.intents.get(self.model.steps)
        if intent is None:
            self.last_status = None
            return
        kind, fields = intent
        try:
            getattr(self, kind)(**fields)
            self.last_status = "accepted"
            self.model.outcomes.append((self.actor_id, kind, "accepted", []))
        except Refused as refusal:
            self.last_status = "precondition_failed"
            self.model.outcomes.append((self.actor_id, kind, "precondition_failed", refusal.failed))


class NativeHandoffModel(mesa.Model):
    def __init__(self, bundle: dict[str, Any], rng: int = 7):
        super().__init__(rng=rng)
        self.state = {e["id"]: deepcopy(e.get("components") or {}) for e in bundle["entities"]}
        self.gate_id = _entity_with_category(bundle, "gate")
        self.outcomes: list[tuple[str, str, str, list[str]]] = []
        self.by_actor = {a: NativeMember(self, a) for a in _members(bundle)}
        gate = self.gate_id
        prereqs = {f"prereq_{x}": _entity_with_category(bundle, f"prereq-{x}") for x in "abcd"}
        authorized = _authorized_member(bundle)
        reports = _report_plan(bundle)
        plan = [(s, "communicate", {"information": i, "delivery": d, "recipient": r}) for s, i, d, r in reports]
        voters = [r for *_, r in reports]
        plan.append((voters[0], "approve", {"gate": gate, **prereqs}))
        plan.append((authorized, "intervene", {"resource": _entity_with_category(bundle, "restorable")}))
        plan += [(v, "approve", {"gate": gate, **prereqs}) for v in voters[: _required_approvals(bundle)]]
        plan.append((authorized, "finalize", {"gate": gate, **prereqs}))
        for index, (actor, kind, fields) in enumerate(plan, start=1):
            self.by_actor[actor].intents[index] = (kind, fields)
        self.plan_length = len(plan)
        self.datacollector = mesa.DataCollector(
            model_reporters={"gate_status": lambda m: m.state[m.gate_id]["gate"]["status"],
                             "approval_count": lambda m: m.state[m.gate_id]["gate"]["approval_count"]})

    def state_hash(self) -> str:
        return hashlib.sha256(json.dumps(self.state, sort_keys=True).encode()).hexdigest()

    def step(self) -> None:
        self.agents.do("step")
        self.datacollector.collect(self)
