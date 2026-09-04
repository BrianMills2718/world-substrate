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

from collections.abc import Iterable
from typing import Any

from .engine import Engine
from .profile import Finding, MechanicPackage, paths_overlap

_COMPONENT_NAMES = (
    "actor",
    "carrying",
    "portable",
    "location",
    "ownership",
    "condition",
    "container",
    "liquid",
    "thermal",
    "material",
    "heat_source",
)


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


def _subject(action: dict[str, Any]) -> str:
    for key in ("vessel", "target", "source", "destination"):
        value = action.get(key)
        if isinstance(value, str) and value:
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
    for actor_id in sorted(actor_ids):
        page = engine.discover(actor_id)
        for row in page["available"]:
            reasons.setdefault((row["action"]["kind"], _subject(row["action"])), set())
        for row in page["blocked"]:
            key = (row["action"]["kind"], _subject(row["action"]))
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


def assay_undeclared_component_reads(rules: Iterable[Any]) -> list[Finding]:
    """Registered rules whose code reads a component their declaration omits.

    This audits the declarations `assay_declared_readers` depends on. It is a
    source-text heuristic: it looks for `.<component>` in a rule's own source
    and compares that against its `read_paths`. It can miss a read reached
    through a helper in another module, and can flag a component named only in
    a comment. Treat its output as a review list, not a verdict.
    """
    import inspect

    findings: list[Finding] = []
    for rule in sorted(rules, key=lambda item: item.rule_id):
        try:
            source = inspect.getsource(type(rule))
        except (OSError, TypeError):
            continue
        declared = " ".join(rule.read_paths) + " " + " ".join(rule.write_paths)
        missing = sorted(
            component
            for component in _COMPONENT_NAMES
            if f".{component}" in source and component not in declared
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
