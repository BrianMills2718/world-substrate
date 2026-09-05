# Read-scope enforcement contract v0

**Status:** proposed, not implemented. Declared **read** scopes are recorded on every event and unchecked; declared **write** scopes are enforced (`scope_violation`). This document is the design the roadmap's open obligation asks for, with the mechanism named, its cost measured, and its blind spots stated. Nothing here is built.  
**Purpose:** decide whether an undeclared read can be caught at runtime, and at what price

## Why writes were easy and reads are not

A write leaves a trace in state. `Engine.apply` clones the world, lets the rule
run, diffs `material_dict()` before against after, and any changed path the
rule never declared is a `scope_violation`. The evidence is the diff.

A read leaves nothing. After a rule inspects `vessel.condition.value` the world
is byte-identical, so no amount of state comparison can recover the fact. The
read has to be observed while it happens or not at all.

## Mechanism: a recording proxy at the rule boundary

`Engine` passes the rule a proxy that wraps `World`, records every attribute and
key access as a dotted path, and returns a proxy for any value that could be
read further:

```text
rule.checks(RecordingWorld(world, recorder), action)
  -> recorder holds {"world.entities.clay-pot.liquid.volume_ml", ...}
  -> compare against rule.read_paths, with the same placeholder matching
     `_path_permitted` already uses for writes
  -> undeclared reads become a finding, or a refusal
```

The comparison is the part that already exists: read and write paths use one
grammar, and `_path_permitted` already resolves `<name>` placeholders against
the entities an attempt named. Only the observation is new.

This was prototyped against the freshwater world to get the numbers below. The
prototype is not in the repository; it existed to make this document's cost
claim a measurement instead of a guess.

## Measured cost

Isolated `rule.checks()` on the transfer world, 2000 repetitions, best of three,
warmed:

| | per call | total |
| --- | --- | --- |
| plain | 8.5 us | 16.9 ms |
| through the recording proxy | 92.0 us | 184.1 ms |
| **overhead** | **10.9x** | |

The prototype recorded 71 distinct read paths across a 30-action trace, 64 of
them entity-level field reads.

10.9x is affordable in a verification pass and not in a run loop. `checks()` is
called for every discovered action on every `discover()`, so a page that offers
twenty affordances pays it twenty times before an actor does anything.

## Recommended staging

1. **Recording, off by default.** A `--verify-reads` mode for probes, tests and
   the mechanic installer. It reports undeclared reads as findings and changes
   no behaviour. This is where the 10.9x is paid and it is the right price for
   a check that runs deliberately.
2. **Refusing, once declarations are clean.** Only after a full trace under (1)
   reports nothing, and only behind an explicit flag, because a false positive
   here refuses a legitimate action rather than emitting a warning.

Do not make it always-on. The project's own tool-loading default is that a
capability not needed in most runs should not be paid for in every run.

## What it still cannot see

- **Reads through an unproxied reference.** A rule that pulls a raw object out
  once and passes it to a module-level helper reads through the raw object, and
  the proxy is not in that path. This is the same indirection blind spot
  `assay_undeclared_component_reads` has, arrived at from the other direction.
- **Per-execution, not static.** It proves that no undeclared read *occurred in
  this run*. A rule that reads a field only on a branch the run did not take is
  not covered, so this is a test-coverage-shaped guarantee, not a proof.
- **Bulk projections read everything.** `as_dict()` and `dataclasses.asdict()`
  touch every field of a component, so any rule that calls one appears to read
  the whole component. Either the projection is exempted, and reads through it
  become invisible, or it is not, and every such rule must declare a read it
  does not conceptually perform. Neither is obviously right and this is the
  design's weakest point.
- **The proxy can change behaviour if it is incomplete.** The prototype's first
  version defined `__len__` but not `__bool__`, so `if vessel:` became
  `len(Entity)` and raised `TypeError` inside a rule that was correct. A
  transparent proxy has to emulate the whole protocol surface it stands in
  front of, and getting that wrong is a defect in the enforcement mechanism
  that presents as a defect in the rule.
- **Reads by processes are universally quantified.** A process iterates all
  entities, so its recorded paths name every entity it touched while its
  declaration names `<x>`. The write-scope guard already passes `None` for
  bound refs on processes; reads need the same treatment and the same loss of
  precision.

## Relationship to the existing assay

`assay.assay_undeclared_component_reads` attacks the same gap statically, by
scanning rule source for component access. It is a heuristic with a stated
blind spot, and it audits declarations rather than executions. The two are
complementary: the assay can flag a read on a branch no test exercises, and the
proxy can catch a read through indirection the assay cannot name. Neither is
sufficient, which is the same shape as the three interaction assays.
