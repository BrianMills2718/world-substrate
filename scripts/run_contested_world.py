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
import html
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from reference_worlds.kitchen.probe import build_engine as build_kitchen
from reference_worlds.kitchen.terminal import service_complete
from scripts._display import display_path
from world_substrate.policy import LlmPolicy, present, resolve_choice

# A world is a builder plus the actors that contend in it. Castaway was the
# world this runner was written against and is kept because its numbers are on
# record; the kitchen was built afterwards against what that run showed --
# several contested resources and different goals, so the agents are not simply
# racing for the same next action.
WORLDS = {
    "castaway": (build_transfer_engine, ("robinson", "friday")),
    "kitchen": (build_kitchen, ("ama", "bo")),
}

# Termination belongs to the world, not to a fixed turn count in the harness.
# Castaway remains an open-ended probe. The kitchen service has a natural end:
# all represented orders have been filled.
WORLD_TERMINALS = {"kitchen": service_complete}


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



def _progress_of(engine, actors) -> dict:
    """Whatever this world uses to say how each actor is doing.

    Castaway measures survival; the kitchen measures whether the dish is done.
    Neither is substrate law, which is why it is read per world rather than
    assumed.
    """
    out = {}
    for actor in actors:
        entity = engine.world.entities[actor]
        if entity.actor is not None:
            out[actor] = {"health": entity.actor.health}
            continue
        cook = entity.component("cook")
        if cook is not None:
            order = engine.world.entities[cook.order_id].components["order"]
            out[actor] = {
                "plated": list(cook.plated),
                "still_wants": [w for w in order.wants if w not in cook.plated],
                "filled": order.filled,
            }
    return out


class Seat:
    """One actor's decision-maker. Returns the action it wants, and why."""

    def __init__(self, actor: str, policy) -> None:
        self.actor = actor
        self.policy = policy

    def choose(self, engine, page: dict) -> tuple[dict | None, str]:
        raise NotImplementedError


class ScriptedSeat(Seat):
    def choose(self, engine, page):
        row = self.policy.choose(page)
        return (dict(row["action"]) if row else None, self.policy.name)


def _kitchen_context(engine, actor: str) -> dict:
    """What a cook knows that the generic observation does not spell out.

    The order entities are already visible with their `wants`, and the cook's
    own state already carries `order_id`, so a careful reader could join them.
    Saying it plainly costs nothing and removes an inference that has nothing
    to do with what is being tested.

    Deliberately no advice about the other cook. Naming that they exist and
    what they hold is situation; telling a cook to share or to race would make
    whatever follows an instruction rather than an observation.
    """
    cook = engine.world.entities[actor].components["cook"]
    order = engine.world.entities[cook.order_id].components["order"]
    outstanding = [w for w in order.wants if w not in cook.plated]
    others = []
    for other in engine.world.entities.values():
        their = other.component("cook")
        if their is None or other.entity_id == actor:
            continue
        holding = sorted(
            e.entity_id for e in engine.world.entities.values()
            if e.ownership is not None
            and e.ownership.owner_ref == f"actor:{other.entity_id}"
        )
        others.append(
            f"{other.label} ({other.entity_id}) is also cooking here, holding "
            f"{', '.join(holding) if holding else 'nothing'}, and has plated "
            f"{', '.join(their.plated) if their.plated else 'nothing'} so far."
        )
    return {
        "goal": (
            f"{cook.order_id} still needs {', '.join(outstanding)}"
            if outstanding
            else f"{cook.order_id} is complete"
        ),
        "other": "\n".join(others),
    }


WORLD_PROMPTS = {
    "castaway": "prompts/castaway_policy.yaml",
    "kitchen": "prompts/kitchen_policy.yaml",
}
WORLD_CONTEXT = {"kitchen": _kitchen_context}


class LlmSeat(Seat):
    """An LLM picks from ids the engine minted, exactly as M5 did.

    The consequence boundary is unchanged and deliberately so: the model
    returns an `action_id`, `resolve_choice` matches it against the ids on the
    current page, and anything unmatched is refused. Two models in one world
    does not widen what either may cause.
    """

    def __init__(self, actor: str, policy, recent, extra=None) -> None:
        super().__init__(actor, policy)
        self._recent = recent
        self._extra = extra

    def choose(self, engine, page):
        context = present(engine, self.actor, page)
        context["recent"] = self._recent(engine, self.actor)
        if self._extra is not None:
            context.update(self._extra(engine, self.actor))
        action_id, reasoning = self.policy.select(page, context)
        choice = resolve_choice(page, action_id, reasoning)
        if choice.kind != "action" or choice.action is None:
            return None, reasoning
        return dict(choice.action), reasoning


def _recent_for(engine, actor: str, seen: dict) -> list[str]:
    """What has happened since this actor last looked.

    Each actor needs this to react to the other at all; without it neither can
    tell that the world moved for a reason.
    """
    start = seen.get(actor, 0)
    lines = []
    for event in engine.world.events[start:]:
        bearer = (event.get("causal_bearer") or {}).get("id")
        if event["status"] != "accepted" or not bearer:
            continue
        rule = event["rule_id"].rsplit(".", 1)[-1]
        who = "you" if bearer == actor else bearer
        lines.append(f"{who}: {rule}")
    seen[actor] = len(engine.world.events)
    return lines[-5:]


def _referent(action: dict) -> str:
    """The one entity an action names, e.g. a vessel, item, or burner id.

    Same fix as `policy.describe_action`: render whatever field the envelope
    actually carries instead of a hardcoded Castaway-only key. This display
    note kept `w.get("vessel", "?")`, so every kitchen action -- which names
    `item`, `burner`, or `order` instead -- printed "from ?" regardless of
    what was actually contested.
    """
    for key, value in action.items():
        if key not in {"actor", "kind", "base_revision", "controller"}:
            return str(value)
    return "?"


def contested_run(turns: int, seats: dict | None = None, world: str = "castaway") -> dict:
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

    `turns` is a ceiling, not a required trace length. A world may declare a
    terminal predicate; when it becomes true the run ends before another pair
    of policies is asked to act.
    """
    build, actors = WORLDS[world]
    terminal = WORLD_TERMINALS.get(world)
    engine = build(REPO)
    if seats is None:
        shared = Greedy()
        seats = {actor: ScriptedSeat(actor, shared) for actor in actors}
    transcript = []

    for turn in range(1, turns + 1):
        if terminal is not None and terminal(engine.world):
            break
        revision = engine.world.revision
        intents, reasons = {}, {}
        for actor in actors:
            page = engine.discover(actor)
            intents[actor], reasons[actor] = seats[actor].choose(engine, page)

        # Alternate who commits first. A fixed order hands the same actor
        # every tie: in the first kitchen run Ama retried 0 turns out of 14 and
        # Bo retried 14, Ama filled her order and Bo plated nothing. That is
        # the loop choosing a winner, not the world. Alternating keeps it
        # deterministic while making "who loses a race" a property of the
        # world rather than of iteration order.
        order = actors if turn % 2 else tuple(reversed(actors))
        results = {}
        for actor in order:
            wanted = intents[actor]
            if wanted is None:
                results[actor] = {"status": "no_action", "wanted": None, "did": None,
                              "said": reasons[actor]}
                continue
            controller = f"policy:{seats[actor].policy.name}"
            outcome = engine.submit({**wanted, "controller": controller})
            record = {
                "wanted": wanted,
                "did": wanted,
                "retried": False,
                "said": reasons[actor],
            }

            if outcome["status"] == "stale_revision":
                # The world moved. Look again and choose from what is actually
                # there now, which is what any real agent would do.
                record["retried"] = True
                page = engine.discover(actor)
                # Was the original plan actually taken away, or merely stale?
                # `lost_what_it_wanted` cannot tell these apart and saturates:
                # whoever commits second is stale every turn by construction,
                # so it read 14 of 14 while the real rate was 1 of 14. This is
                # the number that means something.
                def _same(a: dict, b: dict) -> bool:
                    return all(
                        a.get(k) == b.get(k)
                        for k in ("kind", "item", "burner", "order", "vessel")
                    )

                record["plan_still_available"] = any(
                    _same(row["action"], wanted) for row in page["available"]
                )
                again, said_again = seats[actor].choose(engine, page)
                record["said_on_retry"] = said_again
                if again is None:
                    record["did"] = None
                    outcome = {"status": "nothing_left", "event": {"checks": []}}
                else:
                    record["did"] = again
                    outcome = engine.submit({**again, "controller": controller})

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
                "committed_first": order[0],
                "progress": _progress_of(engine, actors),
            }
        )

    terminal_reached = bool(terminal is not None and terminal(engine.world))
    contended = [
        (t["turn"], actor)
        for t in transcript
        for actor in actors
        if t["actors"][actor].get("retried")
        and t["actors"][actor].get("plan_still_available") is False
    ]
    displaced = [
        (t["turn"], actor)
        for t in transcript
        for actor in actors
        if t["actors"][actor].get("lost_what_it_wanted")
    ]
    still_refused = [
        (t["turn"], actor, t["actors"][actor]["status"])
        for t in transcript
        for actor in actors
        if t["actors"][actor]["status"] not in ("accepted", "no_action")
    ]
    return {
        "schema_version": "world-substrate-contested-run/v3",
        "world": world,
        "actors": list(actors),
        "claim": (
            "Two policies decide from the same revision and commit in order; "
            "whoever is refused for a stale revision re-observes and chooses "
            "again. What remains is what the retry cannot fix: an intent the "
            "other actor made impossible between rendering and acting. A "
            "world-specific terminal predicate may end the run before its turn cap."
        ),
        "turns_run": len(transcript),
        "summary": {
            "turns": len(transcript),
            "terminal_reached": terminal_reached,
            "retried_because_stale": len(displaced),
            "plan_actually_taken_by_the_other": len(contended),
            "refused_after_retry": len(still_refused),
            "refusal_kinds": sorted({r[2] for r in still_refused}),
        },
        "transcript": transcript,
    }



def as_html(payload: dict) -> str:
    """The contested run, as one column of intent per actor beside one world."""
    actors = payload["actors"]
    rows = []
    for t in payload["transcript"]:
        cells = []
        for actor in actors:
            a = t["actors"][actor]
            wanted = (a.get("wanted") or {}).get("kind")
            did = (a.get("did") or {}).get("kind")
            cls = "lost" if a.get("lost_what_it_wanted") else (
                "idle" if a["status"] == "no_action" else "acted"
            )
            head = html.escape(did or wanted or "wait")
            if a.get("lost_what_it_wanted"):
                head = (
                    f"<s>{html.escape(wanted or '?')}</s> &rarr; "
                    f"{html.escape(did or 'nothing left')}"
                )
            said = html.escape(str(a.get("said") or ""))
            then = ""
            if a.get("said_on_retry"):
                then = (
                    "<div class=then>then: "
                    f"{html.escape(str(a['said_on_retry']))}</div>"
                )
            cells.append(
                f"<td class='{cls}'><b>{head}</b><div class=said>{said}</div>{then}</td>"
            )
        rows.append(
            f"<tr><td class=t>t{t['turn']}</td>{''.join(cells)}</tr>"
        )
    s = payload["summary"]
    cost = payload.get("cost_usd")
    terminal_note = " Service complete." if s.get("terminal_reached") else ""
    return f"""<!doctype html><meta charset=utf-8><title>Two agents, one world</title>
<style>
body{{font:15px/1.5 -apple-system,Segoe UI,sans-serif;margin:2rem auto;max-width:1050px;color:#1a1a1a}}
h1{{font-size:1.4rem;margin-bottom:.2rem}} p.sub{{color:#555;margin-top:0}}
table{{border-collapse:collapse;width:100%;margin-top:1.2rem}}
td{{border-top:1px solid #e6e6e6;padding:.55rem .6rem;vertical-align:top;width:47%}}
th{{text-align:left;padding:.4rem .6rem;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#666}}
.t{{width:2.4rem;color:#999;font-variant-numeric:tabular-nums}}
.said{{color:#555;font-size:.88rem;margin-top:.2rem}}
.then{{color:#a3301c;font-size:.86rem;margin-top:.3rem}}
.lost{{background:#fff6f4}} .idle{{color:#999}} .idle b{{font-weight:400}}
.legend{{margin-top:1.4rem;font-size:.85rem;color:#666;border-top:1px solid #eee;padding-top:.8rem}}
</style>
<h1>Two agents, one world, no way to talk to each other</h1>
<p class=sub>Both choose from their own affordance page at the same revision, then commit in
order. Struck-through means the plan was still true when the page was rendered and false by
the time it could act. {s['plan_actually_taken_by_the_other']} of {s['turns']} turns had the
plan genuinely taken by the other cook; {s['retried_because_stale']} were merely stale, where
the plan was still on offer and the policy chose differently on a second look. Neither agent can see the other's intent; the only channel between them
is the world.</p>
<table><tr><th></th>{"".join(f"<th>{html.escape(a)}</th>" for a in actors)}</tr>{''.join(rows)}</table>
<p class=legend>{'Model: ' + html.escape(str(payload.get('model'))) + '. ' if payload.get('model') else ''}
{'Cost $' + format(cost, '.5f') + '. ' if cost is not None else ''}
Every action is one the engine offered; a policy returns an id and never an effect.
Refusals after retry: {s['refused_after_retry']}.{terminal_note}</p>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=12)
    parser.add_argument("--world", default="kitchen", choices=sorted(WORLDS))
    parser.add_argument(
        "--model",
        help="seat both actors with this model instead of the scripted rule",
    )
    parser.add_argument("--max-budget", type=float, default=2.0)
    parser.add_argument("--html", type=Path)
    parser.add_argument(
        "--prompt",
        help=(
            "override the world's prompt, to separate a prompt's effect from "
            "everything else that changed alongside it"
        ),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    seats = None
    trace_id = None
    if args.model:
        import uuid

        trace_id = f"world-substrate-contested-{uuid.uuid4().hex[:10]}"
        seen: dict[str, int] = {}
        seats = {
            actor: LlmSeat(
                actor,
                LlmPolicy(
                    model=args.model,
                    trace_id=f"{trace_id}-{actor}",
                    max_budget=args.max_budget,
                    template=str(REPO / (args.prompt or WORLD_PROMPTS[args.world])),
                    name=f"llm:{actor}",
                ),
                lambda engine, actor, _seen=seen: _recent_for(engine, actor, _seen),
                WORLD_CONTEXT.get(args.world),
            )
            for actor in WORLDS[args.world][1]
        }

    payload = contested_run(args.turns, seats, args.world)
    if args.model:
        from llm_client import get_cost

        payload["model"] = args.model
        payload["cost_usd"] = round(
            sum(get_cost(trace_id=f"{trace_id}-{a}") for a in WORLDS[args.world][1]), 6
        )
    # Persist first. This run costs money and a display bug had already
    # destroyed one of them at turn six; the artifact must not depend on the
    # summary printing correctly.
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {display_path(args.output, REPO)}")
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(as_html(payload))
        print(f"wrote {display_path(args.html, REPO)}")

    for t in payload["transcript"]:
        print(f"t{t['turn']:>2} @rev{t['revision_when_decided']}")
        for actor in payload["actors"]:
            a = t["actors"][actor]
            wanted = (a.get("wanted") or {}).get("kind", "-")
            did = (a.get("did") or {}).get("kind", "-")
            note = ""
            if a.get("lost_what_it_wanted"):
                w, d = a["wanted"] or {}, a["did"]
                settled = (
                    f"settled for {d.get('kind')} {d.get('volume_ml', '')}"
                    if d
                    else "and nothing was left"
                )
                note = (f"  <<< wanted {w.get('kind')} {w.get('volume_ml', '')}"
                        f" from {_referent(w)}, {settled}")
            elif a.get("retried"):
                note = "  (retried, same choice still available)"
            print(f"     {actor:9} {wanted:6} -> {did:6} {a['status']:18}{note}")
            if a.get("said") and a["said"] != "greedy":
                print(f"               said: {str(a['said'])[:96]}")
            if a.get("said_on_retry"):
                print(f"               then: {str(a['said_on_retry'])[:96]}")
            if a.get("refused_because"):
                print(f"               refused: {'; '.join(a['refused_because'])}")
    print(json.dumps(payload["summary"], indent=2))
    if payload.get("cost_usd") is not None:
        print(f"cost: ${payload['cost_usd']:.5f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
