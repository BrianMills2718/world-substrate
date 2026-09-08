"""Greenhouse-specific registered components."""

from __future__ import annotations

from dataclasses import dataclass

from world_substrate.model import register_component


@dataclass
class WateringCanState:
    state: str = "empty"


@dataclass
class PlantState:
    stage: str = "dry"
    bed_id: str = ""


register_component("watering_can", WateringCanState)
register_component("plant", PlantState)
