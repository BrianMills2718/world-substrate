"""Derived, read-only exchange classification over committed give events.

Per docs/decisions/003-semantic-mechanical-boundary.md and
docs/contracts/transition-envelope-v0.md: "Two voluntary gives are independent
transitions... A derived exchange view can recognize the reciprocal history but
cannot transfer either asset again." find_exchanges is a pure analytic pass
over already-committed world.events/world.commands. It never touches World
state, registers no rule, and has no write_paths -- it cannot commit anything.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

GIVE_RULE_ID = "mechanism.ownership.give"


@dataclass(frozen=True)
class DerivedExchange:
    """A reciprocal pair of independently committed give events."""

    actor_a: str
    actor_b: str
    event_id_a: str
    event_id_b: str
    vessel_a: str
    vessel_b: str

    def as_dict(self) -> dict[str, object]:
        return {
            "classification": "exchange",
            "binding": "derived; no binding_id of its own (semantic-mechanical-binding-v0.md)",
            "actor_a": self.actor_a,
            "actor_b": self.actor_b,
            "event_id_a": self.event_id_a,
            "event_id_b": self.event_id_b,
            "vessel_a": self.vessel_a,
            "vessel_b": self.vessel_b,
        }


def _accepted_gives(
    events: list[dict[str, Any]], commands: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    commands_by_id = {command["command_id"]: command for command in commands}
    gives = []
    for event in events:
        if event.get("rule_id") != GIVE_RULE_ID or event.get("status") != "accepted":
            continue
        command = commands_by_id.get(event["cause"])
        if command is None or command.get("op") != "action":
            continue
        action = command["action"]
        if action.get("kind") != "give":
            continue
        gives.append(
            {
                "event_id": event["event_id"],
                "giver": action["actor"],
                "recipient": action["target"],
                "vessel": action["vessel"],
            }
        )
    return gives


def find_exchanges(
    events: list[dict[str, Any]], commands: list[dict[str, Any]]
) -> list[DerivedExchange]:
    """Classify reciprocal give pairs as a derived exchange view.

    Read-only over already-committed events/commands. Each accepted give
    participates in at most one derived exchange, paired in commit order with
    the first unmatched reciprocal give from the other party.
    """

    gives = _accepted_gives(events, commands)
    unmatched: list[dict[str, Any]] = []
    exchanges: list[DerivedExchange] = []
    for give in gives:
        reciprocal = next(
            (
                candidate
                for candidate in unmatched
                if candidate["giver"] == give["recipient"]
                and candidate["recipient"] == give["giver"]
            ),
            None,
        )
        if reciprocal is not None:
            unmatched.remove(reciprocal)
            exchanges.append(
                DerivedExchange(
                    actor_a=reciprocal["giver"],
                    actor_b=give["giver"],
                    event_id_a=reciprocal["event_id"],
                    event_id_b=give["event_id"],
                    vessel_a=reciprocal["vessel"],
                    vessel_b=give["vessel"],
                )
            )
        else:
            unmatched.append(give)
    return exchanges
