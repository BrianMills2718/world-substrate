---
role: research
status: active
reviewed_through: 2026-09-08
---

# Multi-timescale execution — one world clock, many cadences

## Why this matters

Rich persistent worlds should not force every mechanism, resident, analysis, and visual animation onto one turn rate. The Dwarf Fortress research synthesis already records **mixed simulation resolution** as a reusable lesson. The practical consequence for World Substrate is stronger: use one canonical simulated timeline, let mechanisms schedule work at independently meaningful cadences, and wake expensive resident cognition only when it has a reason to think.

This is a target architecture, not current implementation truth. The current engine has an integer `World.tick`; `Engine.advance()` iterates registered processes each step and calls each process's `due(world)` hook. The built-in clock and hydration examples are due every step. There is no first-class future-event queue, duration-bearing activity contract, or event-driven cognition wakeup model yet.

## Keep the clocks distinct

| Clock / cadence | Meaning | Authority |
| --- | --- | --- |
| **Render time** | browser frames, interpolation, playback speed | presentation only |
| **Simulation time** | canonical time coordinate inside the represented world | World Substrate |
| **Process cadence** | when weather, metabolism, machinery, deliveries, meetings, etc. become eligible to act | world mechanics + scheduler |
| **Activity duration** | represented interval for walking, repairing, testing, transporting, meeting, etc. | world mechanics |
| **Resident cognition cadence** | when an external resident runtime deliberates/replans | private cognition runtime, bounded by observation/action seam |
| **Institution cadence** | scheduled votes, reviews, shifts, deadlines, reporting cycles | installed institution/process mechanics |
| **Analysis cadence** | when observer-only metrics/lenses are recomputed | read-only analysis |

Only simulation time is canonical world time. Rendering may run at 60 fps or 1000x playback without changing world history. Analysis can sample at any cadence without becoming causal. Cognition may wake rarely even while cheap world processes continue to run.

## Target scheduling model

The target is **one canonical simulated timeline with independently scheduled triggers**, not a hierarchy of hard-coded seconds/minutes/days.

A future scheduler may jump directly to the next due trigger:

```text
09:12:00  laboratory failure process
09:12:03  monitoring system creates a report
09:14:00  report delivery process
09:15:00  resident task completes -> cognition wakeup
09:22:00  movement activity completion
10:00:00  coalition meeting begins
13:00:00  supply delivery arrives
next day 08:00  staffing review
```

The scheduler determines **when something gets an opportunity to happen**. World Substrate mechanics still determine **whether the transition is legal and what becomes true**.

This is the intended SimPy boundary. SimPy may own clock advancement, event ordering, timeouts, and process wakeups. A wakeup must enter the normal World Substrate process/transition authority; SimPy resource state must not become a parallel source of truth.

## Instant transitions versus duration-bearing activities

Some world changes are naturally atomic at the chosen resolution: sign a record, send an utterance, flip a switch, commit a vote. Others should be represented as ongoing activities: walk, repair, drive, run a laboratory test, conduct a meeting.

Do not simulate duration merely by committing the final state immediately and stretching an animation over it. A duration-bearing activity should be represented in world state at whatever fidelity the selected world needs, with enough identity/status/timing information for other mechanics to observe, interrupt, or constrain it.

A completion trigger is a new causal opportunity, not a guaranteed delayed write. If the road closes while a resident is traveling, or authority is revoked during a long task, the completion mechanic must consult the then-current canonical world and commit/refuse accordingly.

The exact `Activity`/scheduled-trigger schema is deliberately not fixed here; the first Coordination-Lab/process slice should earn the minimum representation from a concrete world.

## Resident cognition should not run on every microstep

The resident harness should usually choose a task/intention, then allow cheaper mechanics to execute the world until a meaningful wake condition occurs. Candidate wake conditions include:

- a selected task/activity completes or fails;
- important new information is delivered;
- another resident initiates an interaction;
- an expected resource disappears or a goal becomes impossible;
- an installed institution requests a decision;
- a scheduled reflection/planning moment arrives; or
- an explicit interruption threshold is crossed.

This keeps expensive LLM cognition outside the hot simulation loop, reduces cost/latency, and makes resident intentions persist instead of being re-decided every tiny world step. Pydantic AI remains replaceable machinery behind `CognitionAdapter`; the world decides what the resident could observe and what attempts were offered.

## Timescale is not fidelity

Cadence and modeling fidelity are independent. A process that fires every second may be extremely coarse; a yearly institutional process may be richly represented. A smaller timestep does not by itself make the model more truthful.

For each represented mechanism ask separately:

1. **When does it operate or become eligible?** — cadence/timing.
2. **What state and causal detail does it represent?** — fidelity/representation depth.

## Implications for the living UI

The living client should eventually support time acceleration and semantic time zoom without becoming a clock authority. At slow playback the user may see walking and conversations; at faster playback those details can collapse into activity blocks while meetings, deliveries, daily cycles, or institutional patterns remain legible.

Playback speed, interpolation, and frame rate remain presentation state. The client follows canonical simulation timestamps/events; it never manufactures elapsed world time.

## Integration sequence

Do not add SimPy or activity duration to the current live-projection slice. First prove that a retained real run projects correctly. Then add first-class information/conversation semantics. When the Coordination Lab or another target world needs independently timed processes/meetings/travel/task durations, add the smallest canonical time/activity contract and integrate SimPy behind it.

The first multi-timescale conformance proof should establish:

- one canonical simulation-time ordering across actions/processes;
- two or more processes with genuinely different cadences;
- at least one duration-bearing activity whose completion rechecks current world state;
- resident cognition that is not invoked on every scheduler event;
- render playback speed that cannot change canonical outcomes; and
- causal evidence that retains trigger/schedule/activity provenance without treating the scheduler as consequence authority.

## Related authority and research

- [Architecture](../architecture.md) — durable process/time/cognition boundaries.
- [Roadmap](../../roadmap/README.md) — when this capability enters the active product sequence.
- [Technology procurement](technology-procurement-2026-09.md) — SimPy and Pydantic AI selection boundaries.
- [Research synthesis](synthesis.md) — Dwarf Fortress mixed-resolution lesson.
- [Core contract v0](../contracts/core-v0.md) — current integer-tick `advance()` baseline, not the richer target scheduler.
