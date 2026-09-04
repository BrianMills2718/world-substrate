"""Mechanic packages, installation validation, and frozen profiles.

Implements docs/contracts/mechanic-profile-v0.md. A package is the reviewable
unit an offline mechanics agent authors; installation validates the declared
contract and freezes a profile identity before a run.

Installation proves that a declared contract is internally valid and that the
selected assays passed. It does not prove global causal closure -- an author
can omit a consequential dependency entirely, and no amount of checking their
own declaration recovers what they never wrote down. See
world_substrate.assay for the interaction assays that narrow, but do not
close, that gap.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from typing import Any

REPRESENTATIONS = frozenset(
    {
        "deterministic",
        "stochastic",
        "empirical",
        "scripted",
        "external",
        "model-mediated",
    }
)


@dataclass(frozen=True)
class Finding:
    """One installation or assay result."""

    severity: str  # "reject" | "warn"
    code: str
    detail: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class MechanicPackage:
    """The declared contract for one installable mechanic."""

    mechanic_id: str
    version: str
    causal_bearer: str
    representation: str
    reads: tuple[str, ...]
    writes: tuple[str, ...]
    # When this mechanic can commit. "action" mechanics are separate
    # transitions that the enclosing commit boundary already serialises, so
    # two of them writing the same path is ordinary, not a conflict. "tick"
    # mechanics fire together inside one advance() and are ordered only by
    # `order`, so two of those writing the same path at the same order really
    # is unarbitrated.
    commit_occasion: str = "action"
    order: int | None = None
    requires: tuple[str, ...] = ()
    optional_modifiers: tuple[str, ...] = ()
    forbids: tuple[str, ...] = ()
    emits: tuple[str, ...] = ()
    effects: tuple[str, ...] = ()
    invariants: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    unsupported_interactions: tuple[str, ...] = ()
    limits: tuple[str, ...] = ()
    tests: tuple[str, ...] = ()
    semantic_bindings: tuple[str, ...] = ()
    trace_contract: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            key: (list(value) if isinstance(value, tuple) else value)
            for key, value in asdict(self).items()
        }


def _path_segments_valid(path: str) -> bool:
    if not path:
        return False
    for segment in path.split("."):
        if not segment:
            return False
        if segment.startswith("<") != segment.endswith(">"):
            return False
    return True


def paths_overlap(left: str, right: str) -> bool:
    """Whether two declared state paths can name the same state.

    A ``<name>`` segment matches any single segment. Comparison runs to the
    shorter path, so ``entities.<vessel>.condition`` overlaps
    ``entities.<vessel>.condition.value``.
    """
    for left_segment, right_segment in zip(left.split("."), right.split(".")):
        if left_segment.startswith("<") or right_segment.startswith("<"):
            continue
        if left_segment != right_segment:
            return False
    return True


def validate_package(
    package: MechanicPackage,
    rule: Any,
    installed: dict[str, MechanicPackage],
) -> list[Finding]:
    """Installer steps 1-4 and 6 of mechanic-profile-v0.

    Step 5 (tests plus interaction assays) is the caller's, because running a
    mechanic's tests and assays needs a world; see world_substrate.assay.
    """
    findings: list[Finding] = []

    if not package.mechanic_id or not package.version:
        findings.append(
            Finding("reject", "identity_missing", "mechanic_id and version are required")
        )
    if package.mechanic_id in installed:
        findings.append(
            Finding(
                "reject",
                "identity_conflict",
                f"{package.mechanic_id} is already installed",
            )
        )
    if getattr(rule, "rule_id", None) != package.mechanic_id:
        findings.append(
            Finding(
                "reject",
                "identity_mismatch",
                f"package declares {package.mechanic_id} but the rule is "
                f"{getattr(rule, 'rule_id', None)}",
            )
        )
    if getattr(rule, "version", None) != package.version:
        findings.append(
            Finding(
                "reject",
                "version_mismatch",
                f"package declares version {package.version} but the rule is "
                f"{getattr(rule, 'version', None)}",
            )
        )

    for label, paths in (("reads", package.reads), ("writes", package.writes)):
        for path in paths:
            if not _path_segments_valid(path):
                findings.append(
                    Finding("reject", "malformed_path", f"{label}: {path!r}")
                )

    # The package is the declaration the engine enforces, so it must be the
    # same declaration the rule carries. A package that widens or narrows its
    # rule's scope would make the installed contract a fiction.
    if tuple(package.reads) != tuple(getattr(rule, "read_paths", ())):
        findings.append(
            Finding(
                "reject",
                "reads_disagree_with_rule",
                f"package {list(package.reads)} != rule "
                f"{list(getattr(rule, 'read_paths', ()))}",
            )
        )
    if tuple(package.writes) != tuple(getattr(rule, "write_paths", ())):
        findings.append(
            Finding(
                "reject",
                "writes_disagree_with_rule",
                f"package {list(package.writes)} != rule "
                f"{list(getattr(rule, 'write_paths', ()))}",
            )
        )

    for other_id, other in sorted(installed.items()):
        # Only mechanics that can commit on the same occasion can conflict.
        # Distinct actions are distinct transitions, already arbitrated by the
        # singular commit boundary and optimistic concurrency; processes share
        # one tick and are arbitrated only by their declared `order`.
        if package.commit_occasion != "tick" or other.commit_occasion != "tick":
            continue
        if package.order != other.order:
            continue
        for write in package.writes:
            for other_write in other.writes:
                if paths_overlap(write, other_write):
                    declared = (
                        other_id in package.dependencies
                        or any(other_id in item for item in package.unsupported_interactions)
                    )
                    if not declared:
                        findings.append(
                            Finding(
                                "reject",
                                "overlapping_write_without_arbitration",
                                f"{package.mechanic_id} writes {write} at order "
                                f"{package.order}, which {other_id} also writes at "
                                "the same order, and names no ordering, "
                                "arbitration, or composition for it",
                            )
                        )

    for dependency in package.dependencies:
        if dependency not in installed:
            findings.append(
                Finding(
                    "reject",
                    "unresolved_dependency",
                    f"{dependency} is not installed",
                )
            )

    if package.representation not in REPRESENTATIONS:
        findings.append(
            Finding(
                "reject",
                "unknown_representation",
                f"{package.representation!r} is not one of {sorted(REPRESENTATIONS)}",
            )
        )
    if not package.tests:
        findings.append(
            Finding("reject", "no_declared_tests", "a package must declare its tests")
        )
    if not package.limits:
        findings.append(
            Finding(
                "warn",
                "no_declared_limits",
                "no omissions or assumptions recorded; review manually",
            )
        )
    if not package.trace_contract:
        findings.append(
            Finding("warn", "no_trace_contract", "no required explanation declared")
        )

    return findings


@dataclass
class MechanicProfile:
    """The validated set of mechanics frozen for one run."""

    packages: dict[str, MechanicPackage] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    frozen_id: str | None = None

    def install(self, package: MechanicPackage, rule: Any) -> list[Finding]:
        if self.frozen_id is not None:
            raise ValueError("cannot install into a frozen profile")
        findings = validate_package(package, rule, self.packages)
        if any(finding.severity == "reject" for finding in findings):
            return findings
        self.packages[package.mechanic_id] = package
        self.findings.extend(findings)
        return findings

    def freeze(self) -> str:
        """Freeze a profile identity before the run."""
        payload = json.dumps(
            {
                "packages": {
                    key: self.packages[key].as_dict() for key in sorted(self.packages)
                },
                "findings": [finding.as_dict() for finding in self.findings],
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
        self.frozen_id = hashlib.sha256(payload).hexdigest()[:16]
        return self.frozen_id


def retrofit_package(rule: Any, causal_bearer: str) -> MechanicPackage:
    """Wrap an existing M1 rule as a package without inventing declarations.

    The promoted M1 rules predate this contract. Their `read_paths` and
    `write_paths` are the declaration they actually carry, so a retrofitted
    package reproduces exactly that and claims nothing more. In particular it
    does not repair an M1 rule that under-declares its reads -- that gap is
    real and an assay should be able to see it.
    """
    order = getattr(rule, "order", None)
    return MechanicPackage(
        mechanic_id=rule.rule_id,
        version=rule.version,
        causal_bearer=causal_bearer,
        representation="deterministic",
        reads=tuple(rule.read_paths),
        writes=tuple(rule.write_paths),
        commit_occasion="tick" if order is not None else "action",
        order=order,
        tests=("tests/ (the promoted M1 suite)",),
        limits=(
            (
                "Retrofitted from a promoted M1 rule that predates the mechanic "
                "package contract; its declared reads and writes are reproduced "
                "verbatim and were not re-derived from its implementation."
            ),
        ),
        trace_contract="M1 causal event with checks and state-path changes.",
    )
