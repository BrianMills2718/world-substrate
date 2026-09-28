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
    role_definition_ids: dict[str, str] | None = None

    def __post_init__(self) -> None:
        if self.role_definition_ids is None:
            return
        if set(self.role_definition_ids) != set(self.roles):
            raise ValueError("semantic binding role_definition_ids must match roles exactly")
        if any(not value.startswith("lc.roledef.") for value in self.role_definition_ids.values()):
            raise ValueError("semantic binding role_definition_ids must use lc.roledef.* ids")

    def as_dict(self) -> dict[str, object]:
        value: dict[str, object] = {
            "binding_id": self.binding_id,
            "sense_id": self.sense_id,
            "roles": dict(self.roles),
            "specialization": self.specialization,
            "causal_class": self.causal_class,
            "causal_bearer": self.causal_bearer,
            "mechanic_id": self.mechanic_id,
            "interpretation_limits": list(self.interpretation_limits),
        }
        return value


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
    role_definition_ids={
        "giver": "lc.roledef.give_transfer.giver",
        "transferred_object": "lc.roledef.give_transfer.transferred_object",
        "recipient": "lc.roledef.give_transfer.recipient",
    },
    causal_class="primitive_intentional_action",
    causal_bearer="giver",
    mechanic_id="mechanism.ownership.give",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed "
            "mechanism.ownership.give mechanic alone validates arguments and "
            "computes every effect (carried over from the donor extraction's own "
            "review note)."
        ),
        (
            "This binding does not license an 'exchange' primitive: a reciprocal "
            "pair of independent give bindings may later be classified by "
            "world_substrate.exchange as a derived view. That classification "
            "performs no transfer and has no binding of its own."
        ),
    ),
)

# --- The remaining M1 action kinds -----------------------------------------
#
# Decision 003 requires every action kind to carry a sense. Only `give` was
# bound, so six of seven accepted action events recorded `semantic_binding:
# null`.
#
# Every predicate and role id below is read from the same pinned extraction as
# GIVE_BINDING -- `predicates[*].id` and `roles[*].id` of the artifact at
# content sha256 c3a5559166d6bf1a11531fd763da52dafbefd44a6cde245ffa05bd6b85a81d9f.
# Choosing which of its eighteen predicates a world action means is the binding
# act and is recorded here; inventing a sense that is not in the source is not,
# and `unheat` is left unbound below for exactly that reason.

DRINK_BINDING = SemanticBinding(
    binding_id="binding.drink.v0",
    sense_id="lc:drink_ingest_liquids",
    roles={
        "actor": "lc.role.ingestor",
        "consumed_liquid": "lc.role.ingestibles",
        "vessel": "lc.role.container",
    },
    causal_class="primitive_intentional_action",
    causal_bearer="actor",
    mechanic_id="mechanism.liquid.drink",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed mechanic "
            "alone validates arguments and computes every effect (the pinned "
            "extraction states this as the binding's own authority note)."
        ),
        (
            "The sense says nothing about what the liquid does to the drinker. "
            "Pathogen harm is computed by the mechanic and is not implied here."
        ),
    ),
)

HEAT_BINDING = SemanticBinding(
    binding_id="binding.heat.v0",
    sense_id="lc:boil_apply_heat_water",
    roles={"actor": "lc.role.cook", "vessel": "lc.role.food"},
    causal_class="primitive_intentional_action",
    causal_bearer="actor",
    mechanic_id="mechanism.thermal.heat",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed mechanic "
            "alone validates arguments and computes every effect (the pinned "
            "extraction states this as the binding's own authority note)."
        ),
        (
            "The predicate is 'apply heat to water'; placing a vessel on a heat "
            "source is the application, not the boiling. Whether the contents ever "
            "reach temperature, and whether that treats them, is owned by "
            "process.thermal.vessels."
        ),
        (
            "The pinned subset types lc.role.food as a LiquidMixture, so this "
            "binding does not extend to heating a vessel that holds no liquid."
        ),
    ),
)

FILL_BINDING = SemanticBinding(
    binding_id="binding.fill.v0",
    sense_id="lc:collect_acquire",
    roles={
        "actor": "lc.role.agent",
        "acquired_liquid": "lc.role.individuals",
        "source": "lc.role.source",
    },
    specialization="acquisition into a carried container",
    causal_class="primitive_intentional_action",
    causal_bearer="actor",
    mechanic_id="mechanism.liquid.fill",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed mechanic "
            "alone validates arguments and computes every effect (the pinned "
            "extraction states this as the binding's own authority note)."
        ),
        (
            "Shares lc:collect_acquire with `take` and is distinguished only by "
            "its specialization. The subset has no predicate for filling a "
            "container specifically, so this is the nearest recorded sense rather "
            "than an exact one."
        ),
        (
            "The sense carries no notion of what is acquired alongside the volume; "
            "salt and pathogens travel with it because the mechanic says so."
        ),
    ),
)

TAKE_BINDING = SemanticBinding(
    binding_id="binding.take.v0",
    sense_id="lc:collect_acquire",
    roles={"actor": "lc.role.agent", "taken_object": "lc.role.individuals"},
    specialization="acquisition of a portable object into carrying",
    causal_class="primitive_intentional_action",
    causal_bearer="actor",
    mechanic_id="mechanism.ownership.take",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed mechanic "
            "alone validates arguments and computes every effect (the pinned "
            "extraction states this as the binding's own authority note)."
        ),
        (
            "Shares lc:collect_acquire with `fill`. The source role is left "
            "unbound because taking an object names no source in this world."
        ),
        (
            "Acquisition here is a change of ownership reference, not a claim "
            "about rights; the world models no rights system."
        ),
    ),
)

POUR_BINDING = SemanticBinding(
    binding_id="binding.pour.v0",
    sense_id="lc:move_change_location",
    roles={
        "actor": "lc.role.self_mover",
        "moved_liquid": "lc.role.theme",
        "destination": "lc.role.goal",
    },
    specialization="relocation of a liquid between containers",
    causal_class="primitive_intentional_action",
    causal_bearer="actor",
    mechanic_id="mechanism.liquid.pour",
    interpretation_limits=(
        (
            "Sense and roles are semantic description only; the installed mechanic "
            "alone validates arguments and computes every effect (the pinned "
            "extraction states this as the binding's own authority note)."
        ),
        (
            "lc:move_change_location is a general relocation sense and its "
            "self_mover role expects the agent to be what moves. Here the agent "
            "moves a liquid, so the binding is a specialization rather than a "
            "direct reading of the predicate."
        ),
        (
            "Mixing is not implied by relocation. What happens when two liquids "
            "meet is computed by mechanism.liquid.pour."
        ),
    ),
)

# `unheat` is deliberately absent.
#
# The pinned extraction has eighteen predicates and none of them is the removal
# of a vessel from a heat source: the nearest, lc:boil_apply_heat_water, is the
# application of heat and reversing it is not a sense it carries. Binding it to
# a predicate that does not mean it, or minting `lc:unheat_*`, would put an
# invented sense in a module whose whole contract is that it cites a pinned
# source. So this obligation is closed for six of seven action kinds and stays
# open for the seventh, against the upstream ontology rather than against this
# file.

SEMANTIC_BINDINGS: dict[str, SemanticBinding] = {
    "give": GIVE_BINDING,
    "drink": DRINK_BINDING,
    "heat": HEAT_BINDING,
    "fill": FILL_BINDING,
    "take": TAKE_BINDING,
    "pour": POUR_BINDING,
}

UNBOUND_ACTION_KINDS: frozenset[str] = frozenset({"unheat"})
