"""Committed events are never mutated, so worlds may share them.

`World.clone()` shares the event log instead of deep-copying it, which is what
made a trace stop being quadratic in its own length. That is only safe while
events stay append-only, and the roadmap's objection to making this change was
exactly that it "trades deepcopy isolation for a never-mutate-an-event
convention that nothing currently enforces".

This file is the enforcement. It fingerprints every event the moment it first
appears and re-checks the entire log after every subsequent transition, so a
rule that writes to a committed event fails here rather than silently
rewriting the history of every world that shares it.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from reference_worlds.workshop.probe import build_engine as build_workshop


def fingerprint(event: dict) -> str:
    return hashlib.sha256(
        json.dumps(event, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


class EventLogWatcher:
    """Records each event once and re-verifies the whole log every step."""

    def __init__(self, case: unittest.TestCase) -> None:
        self.case = case
        self.seen: dict[int, tuple[str, str]] = {}

    def check(self, engine) -> None:
        for index, event in enumerate(engine.world.events):
            current = fingerprint(event)
            if index not in self.seen:
                self.seen[index] = (event["event_id"], current)
                continue
            event_id, original = self.seen[index]
            self.case.assertEqual(
                event["event_id"],
                event_id,
                f"event {index} changed identity: {event_id} -> {event['event_id']}",
            )
            self.case.assertEqual(
                current,
                original,
                f"committed event {event_id} was mutated after it was recorded",
            )


class CommittedEventsAreImmutable(unittest.TestCase):
    def drive(self, engine, actor_id, steps=24, minimum_events=5):
        watcher = EventLogWatcher(self)
        watcher.check(engine)
        for step in range(steps):
            page = engine.discover(actor_id)
            if page["available"]:
                row = page["available"][step % len(page["available"])]
                engine.submit({**row["action"], "controller": "immutability-test"})
            else:
                engine.advance(1)
            watcher.check(engine)
        self.assertGreater(len(engine.world.events), minimum_events)
        return watcher

    def test_across_a_freshwater_trace(self):
        self.drive(build_transfer_engine(), "robinson")

    def test_across_a_workshop_trace(self):
        self.drive(build_workshop(), "mira")

    def test_refusals_and_invalid_envelopes_do_not_disturb_the_log(self):
        engine = build_transfer_engine()
        watcher = EventLogWatcher(self)
        self.drive(engine, "robinson", steps=6, minimum_events=3)
        watcher.check(engine)
        # A stale revision, an unsupported kind, and a malformed envelope.
        engine.submit(
            {"actor": "robinson", "kind": "fill", "vessel": "clay-pot",
             "source": "unsafe-pool", "volume_ml": 10, "base_revision": 0,
             "controller": "test"}
        )
        watcher.check(engine)
        engine.submit(
            {"actor": "robinson", "kind": "levitate",
             "base_revision": engine.world.revision, "controller": "test"}
        )
        watcher.check(engine)
        engine.submit({"actor": "", "kind": "", "base_revision": "no"})
        watcher.check(engine)

    def test_a_clone_shares_event_objects_rather_than_copying_them(self):
        engine = build_transfer_engine()
        self.drive(engine, "robinson", steps=4, minimum_events=3)
        clone = engine.world.clone()
        self.assertEqual(len(clone.events), len(engine.world.events))
        for original, copied in zip(engine.world.events, clone.events):
            self.assertIs(copied, original)
        # The list itself is separate, so appending to one does not touch the
        # other -- that is the part that must still be copied.
        clone.events.append({"event_id": "sentinel"})
        self.assertNotEqual(len(clone.events), len(engine.world.events))

    def test_material_state_is_still_deep_copied(self):
        engine = build_transfer_engine()
        clone = engine.world.clone()
        pot = engine.world.entities["clay-pot"]
        clone.entities["clay-pot"].liquid.volume_ml = 4321
        self.assertNotEqual(pot.liquid.volume_ml, 4321)

    def test_a_mutated_event_is_actually_caught(self):
        """The guard has to be able to go red, or it is decoration."""
        engine = build_transfer_engine()
        watcher = self.drive(engine, "robinson", steps=4, minimum_events=3)
        engine.world.events[0]["status"] = "tampered"
        with self.assertRaises(AssertionError):
            watcher.check(engine)


if __name__ == "__main__":
    unittest.main()
