"""ScenarioSpecV1: the describe-any-scenario world definition (plan scenario-spec-adoption, check S1).

Ported, not imported (Decision 005), from Cybernetic Influence v3 at revision 1c1c207:
  src/cybernetic_influence/general_simulation/contracts_v2.py      ScenarioSpecV2, ComponentRequestV2
  src/cybernetic_influence/general_simulation/authoring_models.py  GeneralPersonDraft, GeneralBehavioralProfileDraft,
                                                                   GeneralWorldRecordProposalV1, StateEntryV1,
                                                                   InformationRepresentationProposalV1,
                                                                   ScheduledMomentProposalV1
Field names follow the donor. Two additions, both needed so a person can decide whether to pass information on:
an information item names its `holder_id` (who holds it at the start) and its `channel_id` (the route it travels).
Ticks replace the donor's minutes. Spatial, resource, transport and relationship parts are not ported; a scenario
that needs them lists them in `unsupported`.
"""
from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

_ID = r"^[a-z][a-z0-9_]*$"
Statement = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Scalar = None | bool | int | float | str  # donor: authoring_models.Scalar


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


class BehavioralProfile(_Strict):
    """Scenario-relevant descriptions of one person, not behavioral commands (donor: GeneralBehavioralProfileDraft)."""
    values: list[Statement] = Field(default_factory=list)
    goals: list[Statement] = Field(default_factory=list)
    beliefs: list[Statement] = Field(default_factory=list)
    decision_tendencies: list[Statement] = Field(default_factory=list)
    social_perceptions: list[Statement] = Field(default_factory=list)
    current_state: list[Statement] = Field(default_factory=list)
    capabilities: list[Statement] = Field(default_factory=list)
    limitations: list[Statement] = Field(default_factory=list)


class Person(_Strict):
    """donor: GeneralPersonDraft"""
    entity_id: str = Field(pattern=_ID)
    label: str = Field(min_length=1)
    position: str = Field(min_length=1)
    disposition: str = Field(min_length=1)
    memories: list[Statement] = Field(min_length=1)
    behavioral_profile: BehavioralProfile


class StateEntry(_Strict):
    """donor: StateEntryV1"""
    key: str = Field(pattern=_ID)
    value: Scalar | list[Scalar]


class WorldRecord(_Strict):
    """donor: GeneralWorldRecordProposalV1"""
    record_id: str = Field(pattern=_ID)
    kind: str = Field(min_length=1)
    label: str = Field(min_length=1)
    public_state: list[StateEntry]
    hidden_state: list[StateEntry]
    visible_to_actor_ids: list[str]


class InformationItem(_Strict):
    """donor: InformationRepresentationProposalV1, plus holder_id and channel_id."""
    representation_id: str = Field(pattern=_ID)
    content: str = Field(min_length=1)
    apparent_source: str = Field(min_length=1)
    holder_id: str = Field(pattern=_ID, description="The person who holds the item at the start and may send it.")
    channel_id: str = Field(pattern=_ID, description="The route the item travels (for example a group's own channel).")
    recipient_ids: list[str] = Field(min_length=1)
    hidden_provenance: list[StateEntry] = Field(default_factory=list)


class ScheduledMoment(_Strict):
    """donor: ScheduledMomentProposalV1 (in the donor it lives in RunSpecV2); `minute` becomes `tick`."""
    moment_id: str = Field(pattern=_ID)
    tick: int = Field(ge=0)
    every_ticks: int | None = Field(default=None, ge=1, description="Repeat interval, for regular meetings.")
    description: str = Field(min_length=1)
    participant_ids: list[str] = Field(default_factory=list)


class Behavior(_Strict):
    """A behavior the world must be able to produce (donor: ComponentRequestV2, without transition contracts)."""
    request_id: str = Field(pattern=_ID)
    subject_refs: list[str] = Field(min_length=1)
    behavior_description: str = Field(min_length=1)
    desired_effects: list[str] = Field(min_length=1)
    fidelity_need: Literal["exact", "bounded", "coarse", "descriptive"]
    causally_material: bool


class ScenarioSpecV1(_Strict):
    scenario_spec_version: Literal[1] = 1
    scenario_id: str = Field(pattern=_ID)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    people: list[Person] = Field(min_length=1)
    world_records: list[WorldRecord] = Field(default_factory=list)
    information_items: list[InformationItem] = Field(default_factory=list)
    scheduled_moments: list[ScheduledMoment] = Field(default_factory=list)
    behaviors: list[Behavior] = Field(min_length=1)
    fidelity_assumptions: list[Statement] = Field(min_length=1)
    unsupported: list[Statement] = Field(default_factory=list,
                                         description="Parts of the scenario this schema cannot represent, said plainly.")
    unresolved_questions: list[Statement] = Field(default_factory=list)

    @model_validator(mode="after")
    def unique_ids_and_references(self) -> "ScenarioSpecV1":
        groups = {
            "people": [p.entity_id for p in self.people],
            "world records": [r.record_id for r in self.world_records],
            "information items": [i.representation_id for i in self.information_items],
            "scheduled moments": [m.moment_id for m in self.scheduled_moments],
            "behaviors": [b.request_id for b in self.behaviors],
        }
        for label, ids in groups.items():
            if len(ids) != len(set(ids)):
                raise ValueError(f"duplicate {label} ids")
        all_ids = [i for ids in groups.values() for i in ids]
        if len(all_ids) != len(set(all_ids)):
            raise ValueError("an id is used by two different kinds of thing")
        people = set(groups["people"])
        for r in self.world_records:
            if missing := set(r.visible_to_actor_ids) - people:
                raise ValueError(f"world record {r.record_id} is visible to undeclared people {sorted(missing)}")
        for i in self.information_items:
            if i.holder_id not in people:
                raise ValueError(f"information item {i.representation_id} is held by undeclared person {i.holder_id}")
            if missing := set(i.recipient_ids) - people:
                raise ValueError(f"information item {i.representation_id} names undeclared recipients {sorted(missing)}")
            if i.holder_id in i.recipient_ids:
                raise ValueError(f"information item {i.representation_id} is sent to its own holder")
        for m in self.scheduled_moments:
            if missing := set(m.participant_ids) - people:
                raise ValueError(f"scheduled moment {m.moment_id} names undeclared participants {sorted(missing)}")
        known = set(all_ids)
        for b in self.behaviors:
            if missing := set(b.subject_refs) - known:
                raise ValueError(f"behavior {b.request_id} names undeclared subjects {sorted(missing)}")
        return self


def from_donor_scenario(scenario: dict[str, Any]) -> ScenarioSpecV1:
    """Read a Cybernetic Influence ScenarioSpecV2 (an approved authoring draft's `proposal.scenario`) as ScenarioSpecV1.

    Donor information representations name recipients but no holder; they are read as held by the first person
    named as their apparent source when that is a person, and are otherwise left out and listed in `unsupported`.
    Donor parts with no counterpart here are listed in `unsupported`, never dropped silently.
    """
    people = scenario["people"]
    person_ids = {p["entity_id"] for p in people}
    unsupported: list[str] = []
    items = []
    for rep in (scenario.get("information_extension") or {}).get("representations", []):
        holder = rep["apparent_source"] if rep["apparent_source"] in person_ids else None
        if holder is None:
            unsupported.append(f"information item {rep['representation_id']}: its source is not a person")
            continue
        items.append({**rep, "holder_id": holder, "channel_id": f"{holder}_channel",
                      "recipient_ids": [r for r in rep["recipient_ids"] if r != holder] or rep["recipient_ids"]})
    for part in ("active_systems", "spatial_extension", "resource_extension", "relationship_extension",
                 "sensing_rules", "resource_transformations", "resource_transports"):
        if scenario.get(part):
            unsupported.append(f"donor part not ported: {part}")
    known = person_ids | {r["record_id"] for r in scenario.get("world_records", [])} | {
        i["representation_id"] for i in items}
    behaviors = []
    for r in scenario["component_requests"]:
        if dropped := [s for s in r["subject_refs"] if s not in known]:
            unsupported.append(f"behavior {r['request_id']}: subjects in unported parts {sorted(dropped)}")
        subjects = [s for s in r["subject_refs"] if s in known]
        if not subjects:
            continue
        behaviors.append({**{k: r[k] for k in ("request_id", "behavior_description", "desired_effects",
                                                "fidelity_need", "causally_material")}, "subject_refs": subjects})
    return ScenarioSpecV1.model_validate({
        "scenario_id": scenario["scenario_id"], "title": scenario["title"], "description": scenario["description"],
        "people": people, "world_records": scenario.get("world_records", []), "information_items": items,
        "behaviors": behaviors, "fidelity_assumptions": scenario["fidelity_assumptions"], "unsupported": unsupported,
    })
