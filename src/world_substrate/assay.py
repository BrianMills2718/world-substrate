"""Interaction assays: search for consequential state an author never declared.

Installer step 5 of docs/contracts/mechanic-profile-v0.md. Per
docs/decisions/003-semantic-mechanical-boundary.md, a causal-closure assay
produces evidence and residual risk, never a completeness boolean: an author
who omits a dependency entirely leaves nothing in their own declaration to
find. These assays therefore approach the gap from three different directions,
and each one's blind spot is named on its own function.

- `assay_declared_readers` reads declarations only. It is exact but inherits
  every omission already present in the *installed* mechanics' declarations.
- `assay_affordance_changes` reads behaviour. It needs no declaration to be
  correct, but only sees consequences that reach an actor's action set.
- `assay_undeclared_component_reads` audits the declarations the first assay
  depends on. It is a source-text heuristic, not a proof.

Nothing here writes canonical state.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from .engine import _ENVELOPE_METADATA, Engine
from .model import BUILTIN_COMPONENT_TYPES, COMPONENT_TYPES
from .profile import Finding, MechanicPackage, paths_overlap

def _component_names() -> tuple[str, ...]:
    """Every component name a world could actually be using, right now.

    This was a hardcoded tuple of the eleven Castaway components. M6 recorded
    that the assays "transferred with no edits at all", which was true only in
    the sense that they did not crash: the workshop world's components --
    worker, part, tool, assembly -- have *zero* overlap with that tuple, so
    `assay_undeclared_component_reads` could not produce a finding there at
    all, and reported a clean result by construction. Read from the registries
    instead, so a world pack's own components are in scope the moment it
    registers them.
    """
    return tuple(sorted(set(BUILTIN_COMPONENT_TYPES) | set(COMPONENT_TYPES)))


def assay_declared_readers(
    package: MechanicPackage, installed: dict[str, MechanicPackage]
) -> list[Finding]:
    """Installed mechanics that read state this package writes.

    Blind spot: an installed mechanic that reads the written state without
    declaring the read is invisible here. Run
    `assay_undeclared_component_reads` over the same registry to size that.
    """
    findings: list[Finding] = []
    for other_id in sorted(installed):
        if other_id == package.mechanic_id:
            continue
        other = installed[other_id]
        touched = sorted(
            {
                f"{write} -> {read}"
                for write in package.writes
                for read in other.reads
                if paths_overlap(write, read)
            }
        )
        if not touched:
            continue
        if other_id in package.dependencies or any(
            other_id in item for item in package.unsupported_interactions
        ):
            continue
        findings.append(
            Finding(
                "warn",
                "undeclared_consequential_reader",
                f"{other_id} reads state {package.mechanic_id} writes "
                f"({'; '.join(touched)}), and the package names it in neither "
                "dependencies nor unsupported_interactions",
            )
        )
    return findings


def _subject(action: dict[str, Any], known_ids: frozenset[str]) -> str:
    """The entity an attempt acts on: its first non-actor participant.

    This used to scan a hardcoded key list -- vessel, target, source,
    destination -- which is the same Castaway vocabulary the engine's
    write-scope binding carried until M6 removed it there. Every workshop
    action names its participants differently (`item`, `part`, `assembly`), so
    all of them collapsed to "?" and the behavioural assay lost the ability to
    say *which* entity an affordance changed on.

    Asking the world which values name entities is both general and stable:
    `as_dict()` emits fields in a fixed order, so the first non-actor entity is
    deterministic, and it is the same field the old list would have picked for
    every Castaway action.
    """
    for key, value in action.items():
        if key == "actor" or key in _ENVELOPE_METADATA:
            continue
        if isinstance(value, str) and value in known_ids:
            return value
    return "?"


def _blocking_reasons(engine: Engine, actor_ids: Iterable[str]) -> dict[tuple[str, str], set[str]]:
    """Map (action kind, subject entity) -> the set of checks currently blocking it.

    Deliberately coarser than the raw affordance list. Two worlds that diverge
    at all produce different action *parameters* (a vessel holding 459ml
    instead of 439ml offers different pour volumes), and reporting those as
    consequences buries the real signal. What matters is whether a new reason
    starts or stops blocking a kind of action on an entity.
    """
    reasons: dict[tuple[str, str], set[str]] = {}
    known_ids = frozenset(engine.world.entities)
    for actor_id in sorted(actor_ids):
        page = engine.discover(actor_id)
        for row in page["available"]:
            reasons.setdefault(
                (row["action"]["kind"], _subject(row["action"], known_ids)), set()
            )
        for row in page["blocked"]:
            key = (row["action"]["kind"], _subject(row["action"], known_ids))
            reasons.setdefault(key, set()).update(
                item.strip() for item in row.get("reason", "").split(";") if item.strip()
            )
    return reasons


def assay_affordance_changes(
    baseline: Engine,
    candidate: Engine,
    actor_ids: Iterable[str],
    steps: int,
    package: MechanicPackage,
) -> list[Finding]:
    """Affordances the new mechanic silently opened or closed.

    Runs the same world with and without the mechanic installed and compares
    which checks block which actions. Needs no declaration to be correct, so it
    catches consequential readers whose declarations omit the read and which
    `assay_declared_readers` therefore cannot see.

    Blind spot: a consequence that changes no actor's action set is invisible
    here, however incoherent the resulting state is.
    """
    baseline.advance(steps)
    candidate.advance(steps)

    before = _blocking_reasons(baseline, actor_ids)
    after = _blocking_reasons(candidate, actor_ids)

    declared = " ".join(package.dependencies) + " " + " ".join(
        package.unsupported_interactions
    )
    findings: list[Finding] = []
    for key in sorted(before.keys() | after.keys()):
        kind, subject = key
        gained = sorted(after.get(key, set()) - before.get(key, set()))
        if not gained or kind in declared:
            continue
        findings.append(
            Finding(
                "warn",
                "undeclared_affordance_change",
                f"{kind} on {subject} is newly blocked by {gained} once "
                f"{package.mechanic_id} is installed; the package declares no "
                "interaction with the mechanic that owns this action",
            )
        )
    return findings


def _reads_component(source: str, component: str) -> bool:
    """Whether rule source reaches a component, by either access form.

    The eleven built-in components are attributes (`entity.liquid`). A world
    pack's own components are dict entries (`entity.components["tool"]`,
    `.components.get("tool")`, `entity.component("tool")`), so a scan for
    `.tool` finds nothing however complete the name vocabulary is. Widening
    the vocabulary without this change left the assay exactly as blind to
    registered components as it was with the names hardcoded.
    """
    name = re.escape(component)
    patterns = (
        # Word-bounded: `.heat_source_id` is a field of the container
        # component, not an access to the heat_source component.
        rf"\.{name}\b",
        rf"""components\s*\[\s*["']{name}["']""",
        rf"""components\s*\.\s*get\s*\(\s*["']{name}["']""",
        rf"""\bcomponent\s*\(\s*["']{name}["']""",
    )
    return any(re.search(pattern, source) for pattern in patterns)


def assay_undeclared_component_reads(rules: Iterable[Any]) -> list[Finding]:
    """Registered rules whose code reads a component their declaration omits.

    This audits the declarations `assay_declared_readers` depends on. It is a
    source-text heuristic: it looks for `.<component>` in the rule class's
    source plus the source of any module-level helper the class names, and
    compares that against its declared paths. It can still miss a read reached
    through a helper in *another* module or through indirection it cannot see
    by name, and can flag a component mentioned only in a comment. Treat its
    output as a review list, not a verdict.
    """
    import inspect
    import sys as _sys

    def _reachable_source(rule: Any) -> str:
        """The rule class's source plus any module-level helper it names.

        A rule that gates on `vessel.condition` inside a shared `_accessible`
        helper reads that component just as surely as one that inlines the
        check, so a scan of the class alone under-reports.
        """
        try:
            text = inspect.getsource(type(rule))
        except (OSError, TypeError):
            return ""
        # A rule_id like "process.material.vessel-failure-spill" contains
        # ".material" and would otherwise read as a component access.
        for literal in (getattr(rule, "rule_id", ""), getattr(rule, "action_kind", "")):
            if literal:
                text = text.replace(literal, "")
        module = _sys.modules.get(type(rule).__module__)
        if module is None:
            return text
        for name, value in vars(module).items():
            if not name.startswith("_") or not inspect.isfunction(value):
                continue
            if getattr(value, "__module__", None) != module.__name__:
                continue
            if name not in text:
                continue
            try:
                text += "\n" + inspect.getsource(value)
            except (OSError, TypeError):
                continue
        return text

    findings: list[Finding] = []
    for rule in sorted(rules, key=lambda item: item.rule_id):
        source = _reachable_source(rule)
        if not source:
            continue
        declared = " ".join(rule.read_paths) + " " + " ".join(rule.write_paths)
        missing = sorted(
            component
            for component in _component_names()
            if _reads_component(source, component) and component not in declared
        )
        if missing:
            findings.append(
                Finding(
                    "warn",
                    "undeclared_component_read",
                    f"{rule.rule_id} reads {missing} in its own source but "
                    "declares neither read nor write access to them",
                )
            )
    return findings


def assay_conservation(
    engine: Engine, initial_volume_ml: int
) -> list[Finding]:
    """Whether modelled liquid volume still balances against the ledger.

    The project treats accounting as goal-relative rather than universal, so
    this is the freshwater world's identity, not a substrate law:

        in-world volume + spilled + evaporated + drunk == initial volume

    Worth running as its own assay because it is based on neither declarations
    nor affordances. A mechanic that destroys a modelled quantity may change
    no actor's action set at all -- and then the behavioural assay is silent
    while the world quietly stops adding up.
    """
    ledger = engine.world.physical_ledger
    if ledger is None:
        return [
            Finding("warn", "no_ledger", "world has no physical ledger to balance against")
        ]
    in_world = sum(
        entity.liquid.volume_ml
        for entity in engine.world.entities.values()
        if entity.liquid is not None
    )
    accounted = (
        in_world + ledger.spilled_ml + ledger.evaporated.volume_ml + ledger.drunk.volume_ml
    )
    if accounted == initial_volume_ml:
        return []
    return [
        Finding(
            "reject",
            "volume_not_conserved",
            f"in-world {in_world} + spilled {ledger.spilled_ml} + evaporated "
            f"{ledger.evaporated.volume_ml} + drunk {ledger.drunk.volume_ml} = "
            f"{accounted}, but the world started with {initial_volume_ml}",
        )
    ]
