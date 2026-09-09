---
role: audit
status: active
reviewed_through: 2026-09-08
---

# Waltzman Coordination Lab v0 audit

## Question

Can the current product deliverable run as one real World Substrate world—not a
synthetic agent-town animation—while preserving asymmetric information,
installed consequence authority, duration/institution semantics, inspectable
causal distinctions, detachable Waltzman analysis, and a represented
intervention fork?

## Implemented vertical

`reference_worlds/waltzman/` defines one bounded coordination world with six
residents, four consequential prerequisites, explicit resident commitments, a
duration-bearing coordination meeting, a coalition decision institution,
represented information/delivery records, and a stabilization package.

The run uses the ordinary Engine and policy seam:

```text
canonical World
  -> scheduled prerequisite changes + asymmetric brief delivery
  -> Engine-minted resident affordances
  -> explicit resident commitment changes / represented communication
  -> duration-bearing meeting
  -> coalition institution gate
  -> blocked baseline
  -> exact-history fork
  -> represented stabilization intervention
  -> resident reassessment
  -> coalition gate recovers
```

No model or renderer writes canonical state.

## Outcome

The deterministic baseline reaches tick 6 with **2 support / 4 conditional**
commitments and the coalition gate `blocked`.

The intervention branch replays the entire 21-event baseline prefix exactly,
then changes the four represented prerequisites through the installed
intervention mechanic. Residents separately reassess their commitments; the
gate recomputes at tick 7 as **6 support / 0 conditional** and becomes `ready`.

Both branches pass exact command replay. Applying only the initial snapshot plus
retained event deltas also reconstructs each final material world exactly.

## Information and causal evidence

The run proves that represented information can be asymmetric. Before a
briefing is delivered, the recipient cannot observe either its content or the
pending delivery record. After delivery, the intended recipient can observe it
while unrelated residents cannot.

Selene's `start_meeting` event retains three delivered resident messages as
`information_context`, but declares no hard causal parents. The coalition gate,
by contrast, names the meeting-completion and explicit commitment events it
mechanically consumes. Communication events are not silently promoted into the
gate's ancestry.

## Living client and stream

`scripts/run_waltzman_demo.py` retains:

- `evidence/waltzman/demo-baseline-v0.json`;
- `evidence/waltzman/demo-intervention-v0.json`;
- `evidence/waltzman/causal-adequacy-v0.json`; and
- `evidence/renders/waltzman-demo-v0.html`.

The HTML client reconstructs state from the projection bundles and supports
branch switching, play/pause/step/scrub, information/causal/constraint layers,
and detachable Waltzman analysis. `scripts/waltzman_demo_service.py` exposes
the same data over JSON and a one-way SSE event stream.

## Causal adequacy

The retained bounded report maps eight consequential scenario dependencies to
the represented state and installed rules that enforce them. The report has
zero known enforcement gaps inside that declared scope and explicitly refuses a
global completeness claim.

Residual risk includes unmodeled psychological belief/trust dynamics, channel
latency/corruption/deception, simplified institution structure, lack of
predictive behavioral validation, and the fact that the stabilization package
is a scenario intervention rather than a real-world effect claim.

## Verification

```bash
python scripts/run_waltzman_demo.py --check
python -m unittest discover -s tests -p 'test_waltzman*.py' -v
python -m unittest discover -s tests -p 'test_*.py'
```

At this audit revision the Waltzman acceptance suite has 14 passing tests and
the full repository suite has 319 passing tests.

## Remaining boundaries

This is a first integrated local product gate, not a claim that every planned
generic layer is complete.

- The Waltzman fixture uses the existing integer tick loop with scheduled
  process predicates and one explicit duration-bearing activity. A generic
  future-event scheduler/SimPy adapter is still unimplemented because this demo
  does not require it.
- Persistent resident memory/planning is not integrated; the demo uses the
  existing bounded policy seam, which is sufficient for the accepted scripted
  scenario.
- The current public standalone visualization remains the previously authorized
  synthetic prototype. Publishing/replacing it is a separate deployment
  authority decision.
- Generic live authoring does not yet generate these richer information,
  institution, and activity mechanics from conversation.
