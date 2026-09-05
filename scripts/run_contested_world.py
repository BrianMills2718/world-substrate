#!/usr/bin/env python3
"""Two policies in one world, and the divergence no annotation can close.

The three-run series in the M5 audit showed that surfacing what the world
already knew took a single policy from 60 health to a perfect 100. That is a
good result and it retires the interesting failure: an agent shown everything
plays correctly.

What it cannot retire is a second agent. An affordance page is computed at a
revision. Every row on it was true when rendered and may be false by the time
the actor commits, because someone else moved in between. No warning fixes
that, because at render time there is nothing yet to warn about.

This runs both Castaway actors against the same world and records, per turn,
what each one decided from its own page and what the world did with it. The
engine already had everything needed: `base_revision` on every action,
`stale_revision` refusal, atomic commit, and a causal trace per attempt. None of
it had ever been exercised by two live policies.

Scripted policies by default. No model is called unless one is passed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from scripts._display import display_path

ACTORS = ("robinson", "friday")


class Greedy:
    """Takes the largest drink it can see, else the first thing offered.

    Deliberately simple: the point of this run is the collision, not the
    cleverness of either side.
    """

    name = "greedy"

    def choose(self, page: dict) -> dict | None:
        drinks = [
            row for row in page["available"] if row["action"]["kind"] == "drink"
        ]
        if drinks:
            return max(drinks, key=lambda r: r["action"].get("volume_ml", 0))
        return page["available"][0] if page["available"] else None


def contested_run(turns: int) -> dict:
    """Both actors decide from one revision; the loser re-decides and retries.

    The first version of this loop let both decide and both submit, and the
    second actor was refused on `base_revision` every single turn. That is
    starvation produced by the loop, not contention produced by the world: an
    optimistic-concurrency protocol with no retry always refuses whoever went
    second, whatever the world contains.

    So the loser now re-observes and chooses again. What that leaves is the
    part no protocol fix removes -- the actor wanted something, and by the time
    it could act the thing was gone, taken by the other actor. That is a belief
    falsified by another agent rather than by an omission in the page, and
    nothing the affordance list could have said at render time would have
    warned about it.
    """
    engine = build_transfer_engine(REPO)
    policy = Greedy()
    transcript = []

    for turn in range(1, turns + 1):
        revision = engine.world.revision
        intents = {}
        for actor in ACTORS:
            page = engine.discover(actor)
            row = policy.choose(page)
            intents[actor] = dict(row["action"]) if row else None

        results = {}
        for actor in ACTORS:
            wanted = intents[actor]
            if wanted is None:
                results[actor] = {"status": "no_action", "wanted": None, "did": None}
                continue
            outcome = engine.submit({**wanted, "controller": f"policy:{policy.name}"})
            record = {"wanted": wanted, "did": wanted, "retried": False}

            if outcome["status"] == "stale_revision":
                # The world moved. Look again and choose from what is actually
                # there now, which is what any real agent would do.
                record["retried"] = True
                page = engine.discover(actor)
                row = policy.choose(page)
                if row is None:
                    record["did"] = None
                    outcome = {"status": "nothing_left", "event": {"checks": []}}
                else:
                    record["did"] = dict(row["action"])
                    outcome = engine.submit(
                        {**row["action"], "controller": f"policy:{policy.name}"}
                    )

            record["status"] = outcome["status"]
            record["refused_because"] = [
                check["label"]
                for check in outcome["event"]["checks"]
                if not check["ok"] and check["label"] != "Base revision is current"
            ]
            # The interesting quantity: it had to settle for something else.
            record["lost_what_it_wanted"] = bool(
                record["retried"] and record["did"] != record["wanted"]
            )
            results[actor] = record

        engine.advance(1)
        transcript.append(
            {
                "turn": turn,
                "revision_when_decided": revision,
                "actors": results,
                "health": {
                    actor: engine.world.entities[actor].actor.health
                    for actor in ACTORS
                },
            }
        )

    displaced = [
        (t["turn"], actor)
        for t in transcript
        for actor in ACTORS
        if t["actors"][actor].get("lost_what_it_wanted")
    ]
    still_refused = [
        (t["turn"], actor, t["actors"][actor]["status"])
        for t in transcript
        for actor in ACTORS
        if t["actors"][actor]["status"] not in ("accepted", "no_action")
    ]
    return {
        "schema_version": "world-substrate-contested-run/v1",
        "claim": (
            "Two policies decide from the same revision and commit in order; "
            "whoever is refused for a stale revision re-observes and chooses "
            "again. What remains is what the retry cannot fix: an intent the "
            "other actor made impossible between rendering and acting."
        ),
        "turns_run": len(transcript),
        "summary": {
            "turns": len(transcript),
            "lost_what_it_wanted": len(displaced),
            "refused_after_retry": len(still_refused),
            "refusal_kinds": sorted({r[2] for r in still_refused}),
        },
        "transcript": transcript,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=12)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = contested_run(args.turns)
    for t in payload["transcript"]:
        print(f"t{t['turn']:>2} @rev{t['revision_when_decided']}")
        for actor in ACTORS:
            a = t["actors"][actor]
            wanted = (a.get("wanted") or {}).get("kind", "-")
            did = (a.get("did") or {}).get("kind", "-")
            note = ""
            if a.get("lost_what_it_wanted"):
                w, d = a["wanted"], a["did"]
                note = (f"  <<< wanted {w.get('kind')} {w.get('volume_ml','')}"
                        f" from {w.get('vessel','?')}, settled for {d.get('kind')}"
                        f" {d.get('volume_ml','')}")
            elif a.get("retried"):
                note = "  (retried, same choice still available)"
            print(f"     {actor:9} {wanted:6} -> {did:6} {a['status']:18}{note}")
            if a.get("refused_because"):
                print(f"               refused: {'; '.join(a['refused_because'])}")
    print(json.dumps(payload["summary"], indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {display_path(args.output, REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
