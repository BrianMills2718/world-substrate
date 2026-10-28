"""A world's own declared laws, checked at every commit (declared-laws plan, S2).

The world designer declares what the world keeps count of (``resources``: which integer or number fields hold an
amount of it) and what must stay true about those amounts (``laws``), in the world's own terms
(docs/plans/declared_laws.md). Nothing here knows what money or pencils are: a total law says a resource's world
total changes only through the steps it lists, and a pairing law says one move always hands one thing over in
return for another. The engine calls ``law_breaches`` on the state before and after a step and refuses the step
whole when it returns anything.
"""

from __future__ import annotations

from typing import Any

Holdings = dict[str, float]


def _holdings(state: dict[str, Any], kept_in: list[tuple[str, str]]) -> Holdings:
    """How much of one resource each entity holds in ``state`` (a ``World.material_dict()``)."""
    result: Holdings = {}
    for entity_id, entity in (state.get("entities") or {}).items():
        components = entity.get("components") or {}
        amount = 0.0
        for component, field in kept_in:
            value = (components.get(component) or {}).get(field)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                amount += value
        result[entity_id] = amount
    return result


def _amount(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def law_breaches(
    laws: list[dict[str, Any]],
    resources: list[dict[str, Any]],
    before: dict[str, Any],
    after: dict[str, Any],
    step_id: str,
    action: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """The declared laws a step breaks, each ``{law_id, says, found}``; empty when it keeps them all.

    ``step_id`` is the move's action kind, or ``process:<process id>`` for something the world does by itself.
    ``action`` is the move's typed action (its ``actor`` and entity_ref fields), needed for pairing laws.
    """
    if not laws:
        return []
    kept = {
        row["resource_id"]: [(k["component"], k["field"]) for k in row.get("kept_in") or []]
        for row in resources
    }
    cache: dict[str, tuple[Holdings, Holdings]] = {}

    def held(resource: str) -> tuple[Holdings, Holdings]:
        if resource not in cache:
            fields = kept.get(resource) or []
            cache[resource] = (_holdings(before, fields), _holdings(after, fields))
        return cache[resource]

    breaches: list[dict[str, str]] = []
    for law in laws:
        if "move" not in law:
            old, new = held(law["resource"])
            change = sum(new.values()) - sum(old.values())
            if change and step_id not in (law.get("may_change_by") or []):
                breaches.append({
                    "law_id": law["law_id"],
                    "says": law["says"],
                    "found": (
                        f"{step_id} changed the world's total {law['resource']} by {_amount(change)}; "
                        f"only {', '.join(law.get('may_change_by') or []) or 'nothing'} may change it"
                    ),
                })
            continue
        if step_id != law["move"] or action is None:
            continue
        problems = []
        for side in ("gives", "pays"):
            leg = law[side]
            giver, receiver = (
                action.get("actor") if leg[end] == "actor" else action.get(leg[end]) for end in ("from", "to")
            )
            old, new = held(leg["resource"])
            lost = old.get(giver, 0.0) - new.get(giver, 0.0)
            gained = new.get(receiver, 0.0) - old.get(receiver, 0.0)
            if not (lost > 0 and gained == lost):
                problems.append(
                    f"{side} {leg['resource']} from {giver} to {receiver}: "
                    f"{giver} lost {_amount(lost)}, {receiver} gained {_amount(gained)}"
                )
        if problems:
            breaches.append({"law_id": law["law_id"], "says": law["says"], "found": "; ".join(problems)})
    return breaches
