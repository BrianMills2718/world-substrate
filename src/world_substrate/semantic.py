"""Semantic-mechanical bindings per docs/contracts/semantic-mechanical-binding-v0.md.

A binding explains what an attempt means; it never mutates state itself. Every
binding here cites the pinned Linguistic Core extraction recorded in
references/sources.json (`linguistic_core`, via the `castaway_world_systems`
artifact) rather than inventing a sense or role.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticBinding:
    binding_id: str
    sense_id: str
    roles: dict[str, str]
    causal_class: str
    interpretation_limits: tuple[str, ...]
    causal_bearer: str | None = None
    mechanic_id: str | None = None
    specialization: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "binding_id": self.binding_id,
            "sense_id": self.sense_id,
            "roles": dict(self.roles),
            "specialization": self.specialization,
            "causal_class": self.causal_class,
            "causal_bearer": self.causal_bearer,
            "mechanic_id": self.mechanic_id,
            "interpretation_limits": list(self.interpretation_limits),
        }


GIVE_BINDING = SemanticBinding(
    binding_id="binding.give.v0",
    # Pinned Linguistic Core 0.3.0 sense, reused verbatim from the reviewed
    # Castaway extraction rather than re-derived: castaway-world/worktrees/
    # world-systems/content/linguistic-core-subset.json, action_bindings.give,
    # at revision da5ccb46fa536505bbc0235a4157c648c8bb4bcb (content sha256
    # c3a5559166d6bf1a11531fd763da52dafbefd44a6cde245ffa05bd6b85a81d9f, see
    # references/sources.json -> linguistic_core).
    sense_id="lc:give_transfer",
    roles={
        "giver": "lc.role.donor",
        "transferred_object": "lc.role.theme",
        "recipient": "lc.role.recipient",
    },
    causal_class="primitive_intentional_action",
    causal_bearer="giver",
    mechanic_id="mechanism.ownership.give",
    interpretation_limits=(
        "Sense and roles are semantic description only; the installed "
        "mechanism.ownership.give mechanic alone validates arguments and "
        "computes every effect (carried over from the donor extraction's own "
        "review note).",
        "This binding does not license an 'exchange' primitive: a reciprocal "
        "pair of independent give bindings may later be classified by "
        "world_substrate.exchange as a derived view. That classification "
        "performs no transfer and has no binding of its own.",
    ),
)

SEMANTIC_BINDINGS: dict[str, SemanticBinding] = {
    "give": GIVE_BINDING,
}
