---
role: audit
status: active
reviewed_through: 2026-09-09
---

# Waltzman Coordination Lab v0 audit

This is an audit of the **World Substrate product demo using Waltzman Coordination Lab as its reviewed reference world**. Waltzman/Cybernetic Influence supply scenario and analytic lineage; World Substrate is the engine and product being demonstrated.

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
by contrast, names the meeting-completion and explicit commitment events its
installed rule declares as hard causal parents. Communication events are not
silently promoted into the gate's ancestry.

These are **mechanic-declared causal relations inside this represented world**.
The Engine validates that named parent event IDs exist in retained history; the
current runtime does not infer parentage from instrumented reads or claim that
the scenario mechanics establish scientific causality in the real world.

## Living client and stream

`scripts/run_waltzman_demo.py` retains:

- `evidence/waltzman/demo-baseline-v0.json`;
- `evidence/waltzman/demo-intervention-v0.json`;
- `evidence/waltzman/causal-adequacy-v0.json`; and
- `evidence/renders/waltzman-demo-v0.html`.

The HTML client reconstructs state from the projection bundles and supports
branch switching, play/pause/step/scrub, information/causal/constraint layers,
and detachable Waltzman analysis. The artifact is self-contained: its canonical
baseline/intervention projection bundles are embedded in the generated HTML.
`scripts/waltzman_demo_service.py` additionally exposes the same data over JSON
and a one-way SSE event stream, but that service is not required for the first
public standalone demo.

## Causal adequacy

The retained bounded report is a **declared dependency inventory**. It maps eight
consequential scenario assumptions to represented state and the installed rule
surfaces intended to enforce them, and it explicitly refuses a global
completeness claim.

At v0, a dependency being mapped to installed rules is not a counterfactual
proof that those rules are necessary and sufficient, nor evidence that the
scenario dependency is true of the real world. Stronger automatic
counterfactual/mutation verification is a deferred research option rather than a
first-demo requirement.

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
- This reference-world client remains valid presentation/evidence, but the
  2026-09-09 stakeholder decision supersedes publishing it as the finished
  outreach demo. The sendable demo must add natural-language authoring and fresh
  execution, then reuse these living-view semantics for inspection. The fastest
  path reuses Cybernetic V3's existing authoring/run pipeline rather than
  rebuilding general authoring in World Builder first.
- Generic live authoring does not yet generate these richer information,
  institution, and activity mechanics from conversation. The public Waltzman
  demo must therefore be presented as a reviewed reference world, not as a
  claim that the current Builder generated its complete law.
- Future durable generated-law provenance should bind approval/run identity to
  the exact executable law and compiler/interpreter version. That hardening is
  important for the broader product but is not a blocker for publishing this
  hand-authored reference demo.
