"""M2 give/exchange vertical: semantic binding plus the derived exchange view.

Roadmap M2 exact next action: audit the M1 give path against the proposed
semantic-binding and transition-envelope contracts, and produce the smallest
versioned binding and trace that preserves the implemented transfer while
making ordinary exchange a detachable derived view.

Reuses the M1 transfer fixture (Robinson/Friday, clay-pot/cup-robinson) rather
than inventing a second world -- friday is additionally granted initial
ownership of clay-pot so a real bidirectional exchange is possible.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from world_substrate.engine import Engine
from world_substrate.exchange import find_exchanges
from world_substrate.model import World
from world_substrate.rules import GiveAction
from world_substrate.semantic import GIVE_BINDING, SEMANTIC_BINDINGS


def _select_give(engine: Engine, actor_id: str, vessel: str, target: str) -> GiveAction:
    page = engine.discover(actor_id, kind="give")
    row = next(
        item
        for item in page["available"]
        if item["action"]["vessel"] == vessel and item["action"]["target"] == target
    )
    value = {**row["action"], "controller": "verification_script"}
    return GiveAction.from_dict(value)


def _exchange_world(root: Path | None = None) -> Engine:
    """The M1 transfer world with clay-pot's initial ownership moved to friday.

    Robinson starts owning cup-robinson (unchanged); friday starts owning
    clay-pot. This makes a real two-way exchange constructible without
    changing anything about the underlying give mechanic.
    """

    engine = build_transfer_engine(root)
    world = World.from_snapshot(engine.initial_snapshot())
    world.entities["clay-pot"].ownership.owner_ref = "actor:friday"
    world.rule_versions = engine.registry.versions()
    return Engine(world, engine.registry)


def test_give_binding_cites_pinned_sense_and_roles() -> None:
    assert GIVE_BINDING.sense_id == "lc:give_transfer"
    assert GIVE_BINDING.roles == {
        "giver": "lc.role.donor",
        "transferred_object": "lc.role.theme",
        "recipient": "lc.role.recipient",
    }
    assert GIVE_BINDING.mechanic_id == "mechanism.ownership.give"
    assert GIVE_BINDING.causal_bearer == "giver"
    assert SEMANTIC_BINDINGS["give"] is GIVE_BINDING


def test_give_binding_names_no_exchange_mechanic() -> None:
    # The binding contract requires a mechanic_id only for a state-changing
    # binding; a derived-only classification has none. Assert the give
    # binding does not smuggle an "exchange" mechanic in as a side door.
    assert "exchange" not in GIVE_BINDING.mechanic_id
    assert any("no transfer" in limit.lower() for limit in GIVE_BINDING.interpretation_limits)


def test_two_independent_gives_are_recognized_as_one_exchange() -> None:
    engine = _exchange_world()

    engine.apply(_select_give(engine, "robinson", "cup-robinson", "friday"))
    engine.apply(_select_give(engine, "friday", "clay-pot", "robinson"))

    exchanges = find_exchanges(engine.world.events, engine.world.commands)

    assert len(exchanges) == 1
    exchange = exchanges[0]
    assert {exchange.actor_a, exchange.actor_b} == {"robinson", "friday"}
    assert {exchange.vessel_a, exchange.vessel_b} == {"cup-robinson", "clay-pot"}


def test_one_give_with_no_reciprocal_is_not_an_exchange() -> None:
    engine = _exchange_world()

    engine.apply(_select_give(engine, "robinson", "cup-robinson", "friday"))
    # friday renages: no reciprocal give is ever attempted.

    exchanges = find_exchanges(engine.world.events, engine.world.commands)

    assert exchanges == []
    # The one completed give still committed -- reneging does not roll it back.
    assert engine.world.entities["cup-robinson"].ownership.owner_ref == "actor:friday"


def test_derived_exchange_classification_performs_no_transfer() -> None:
    engine = _exchange_world()

    engine.apply(_select_give(engine, "robinson", "cup-robinson", "friday"))
    engine.apply(_select_give(engine, "friday", "clay-pot", "robinson"))

    event_count_before = len(engine.world.events)
    command_count_before = len(engine.world.commands)
    revision_before = engine.world.revision
    ownership_before = {
        "cup-robinson": engine.world.entities["cup-robinson"].ownership.owner_ref,
        "clay-pot": engine.world.entities["clay-pot"].ownership.owner_ref,
    }

    exchanges_first_call = find_exchanges(engine.world.events, engine.world.commands)
    exchanges_second_call = find_exchanges(engine.world.events, engine.world.commands)

    assert len(engine.world.events) == event_count_before
    assert len(engine.world.commands) == command_count_before
    assert engine.world.revision == revision_before
    assert {
        "cup-robinson": engine.world.entities["cup-robinson"].ownership.owner_ref,
        "clay-pot": engine.world.entities["clay-pot"].ownership.owner_ref,
    } == ownership_before
    # Idempotent and side-effect-free: calling it twice changes nothing and
    # yields the same classification both times.
    assert exchanges_first_call == exchanges_second_call


def test_final_ownership_matches_two_independent_gives_exactly() -> None:
    # The exchange classification must not itself move anything: final
    # ownership is exactly what two ordinary independent gives produce.
    engine = _exchange_world()

    engine.apply(_select_give(engine, "robinson", "cup-robinson", "friday"))
    engine.apply(_select_give(engine, "friday", "clay-pot", "robinson"))

    assert engine.world.entities["cup-robinson"].ownership.owner_ref == "actor:friday"
    assert engine.world.entities["clay-pot"].ownership.owner_ref == "actor:robinson"


if __name__ == "__main__":
    import traceback

    tests = [
        test_give_binding_cites_pinned_sense_and_roles,
        test_give_binding_names_no_exchange_mechanic,
        test_two_independent_gives_are_recognized_as_one_exchange,
        test_one_give_with_no_reciprocal_is_not_an_exchange,
        test_derived_exchange_classification_performs_no_transfer,
        test_final_ownership_matches_two_independent_gives_exactly,
    ]
    failures = 0
    for test in tests:
        try:
            test()
            print(f"PASS {test.__name__}")
        except Exception:
            failures += 1
            print(f"FAIL {test.__name__}")
            traceback.print_exc()
    if failures:
        raise SystemExit(f"{failures} test(s) failed")
    print("all tests passed")
