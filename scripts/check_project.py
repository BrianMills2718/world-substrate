#!/usr/bin/env python3
"""Validate World Substrate navigation, authority, links, and pinned sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
SKIP = {".git", ".venv", ".company-planning", "work", "runs"}
REQUIRED = (
    "CLAUDE.md",
    "AGENTS.md",
    "README.md",
    "docs/CLAUDE.md",
    "docs/wiki/README.md",
    "docs/architecture.md",
    "docs/contracts/core-v0.md",
    "docs/contracts/semantic-mechanical-binding-v0.md",
    "docs/contracts/mechanic-profile-v0.md",
    "docs/contracts/transition-envelope-v0.md",
    "docs/contracts/read-scope-enforcement-v0.md",
    "docs/decisions/001-project-scope.md",
    "docs/decisions/002-observability-and-replay.md",
    "docs/decisions/003-semantic-mechanical-boundary.md",
    "docs/source-dispositions.md",
    "docs/research/synthesis.md",
    "docs/research/world-substrate-strategy-session.md",
    "docs/research/agent-ecology2-review.md",
    "docs/research/cybernetic-influence-lineage-review.md",
    "docs/research/discussion-traceability.md",
    "docs/audits/m2-give-path-audit.md",
    "docs/audits/m3-overheat-authoring-experiment.md",
    "docs/audits/m4-spill-experiment.md",
    "docs/audits/m5-policy-consumer.md",
    "docs/audits/m6-second-world.md",
    "docs/audits/m7-authoring-rate.md",
    "roadmap/CLAUDE.md",
    "roadmap/README.md",
    "reference_worlds/CLAUDE.md",
    "reference_worlds/README.md",
    "reference_worlds/castaway/probe.py",
    "reference_worlds/workshop/probe.py",
    "reference_worlds/workshop/mechanics.py",
    "reference_worlds/workshop/components.py",
    "references/sources.json",
    "scripts/extract_castaway_fixture.py",
    "scripts/run_first_fill_probe.py",
    "scripts/run_boiling_probe.py",
    "scripts/run_pour_probe.py",
    "scripts/run_drink_probe.py",
    "scripts/run_transfer_probe.py",
    "scripts/replay_transfer_evidence.py",
    "scripts/run_freshwater_probe.py",
    "scripts/run_overheat_assay_probe.py",
    "scripts/run_spill_assay_probe.py",
    "scripts/run_llm_policy.py",
    "scripts/run_authoring_experiment.py",
    "src/world_substrate/authoring.py",
    "src/world_substrate/policy.py",
    "scripts/validate_e2e_receipt.py",
    "src/world_substrate/engine.py",
    "src/world_substrate/model.py",
    "src/world_substrate/rules.py",
    "src/world_substrate/mechanisms/thermal.py",
    "src/world_substrate/mechanisms/ownership.py",
    "src/world_substrate/mechanisms/damage.py",
    "src/world_substrate/profile.py",
    "src/world_substrate/assay.py",
    "tests/CLAUDE.md",
    "tests/test_owner_ref.py",
    "tests/test_observability_fields.py",
    "tests/test_first_fill.py",
    "tests/test_boiling.py",
    "tests/test_pour.py",
    "tests/test_drink.py",
    "tests/test_transfer.py",
    "tests/test_action_envelopes.py",
    "tests/test_evidence_gates.py",
    "tests/fixtures/castaway/README.md",
    "tests/fixtures/castaway/freshwater-v0.json",
    "reference_worlds/castaway/freshwater-fill-v0.json",
    "reference_worlds/castaway/freshwater-v0.json",
    "evidence/m1/first-fill-v0.json",
    "evidence/m1/boiling-v0.json",
    "evidence/m1/pour-v0.json",
    "evidence/m1/drink-v0.json",
    "evidence/m1/transfer-v0.json",
    "evidence/m1/transfer-replay-v1.json",
    "evidence/m1/freshwater-v0.json",
    "evidence/m1/freshwater-v0.md",
    "evidence/m1/end-to-end-observation-v1.json",
)
WIKI_SECTIONS = (
    "## What this project is",
    "## Start here",
    "## Concepts and terminology",
    "## Sources and evidence",
    "## Accepted authorities and decisions",
    "## Working context",
    "## Needs resolution",
    "## Architecture and workflow",
    "## Human-reviewable artifacts",
    "## Roadmap",
)
ROADMAP_SECTIONS = (
    "## Outcome and success criteria",
    "## Canonical outcome probe",
    "## Current truth",
    "## Applicable context",
    "## Constraints and authorities",
    "## Vertical slices and current work",
    "### Milestone horizon",
    "### Active slice",
    "## Decisions and assumptions",
    "## Evidence and review artifacts",
    "## Risks and needs resolution",
    "## Human decisions",
    "## Refresh and reset triggers",
    "## Exact next action",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_has_revision(path: Path, revision: str) -> bool:
    """Return whether a pinned source revision remains available locally.

    A donor checkout may advance without changing the revision reviewed by this
    project. The pin protects provenance; it is not a demand that every donor
    worktree stay checked out at that commit.
    """
    result = subprocess.run(
        ["git", "-C", str(path), "cat-file", "-e", f"{revision}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def markdown_files() -> list[Path]:
    return [
        path
        for path in REPO.rglob("*.md")
        if not SKIP.intersection(path.relative_to(REPO).parts)
    ]


# --- Contract status against the code it describes ---------------------------
#
# `REQUIRED` above asserts that a contract file exists and is linked. Nothing
# asserted that what it *says about itself* is still true, which is why
# semantic-mechanical-binding-v0.md spent several commits claiming one binding
# of seven while six were implemented, and claiming no binding reached an event
# after they all did. A prose rule in docs/CLAUDE.md said to keep proposed
# contracts distinct from implemented behaviour, and nothing made it fire.
#
# A contract opts in by declaring the facts it depends on:
#
#     <!-- status-facts
#     semantic_bindings_bound: 6
#     semantic_binding_on_events: true
#     -->
#
# Every declared fact is recomputed here by *running the engine*, never by
# reading the constant the contract is describing -- a check that reads
# SEMANTIC_BINDINGS to confirm a claim about SEMANTIC_BINDINGS could not fail.
#
# This is a floor, not a guarantee. A contract that declares nothing is
# unchecked, and a status line can still be wrong about anything it did not
# reduce to a named fact.

STATUS_FACT_BLOCK = re.compile(
    r"<!--\s*status-facts\s*\n(.*?)-->", re.DOTALL
)


def _parse_status_facts(text: str) -> dict[str, object]:
    match = STATUS_FACT_BLOCK.search(text)
    if match is None:
        return {}
    facts: dict[str, object] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, raw = line.partition(":")
        raw = raw.strip()
        if raw in ("true", "false"):
            facts[key.strip()] = raw == "true"
        elif raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            facts[key.strip()] = sorted(
                item.strip().strip("\"'") for item in inner.split(",") if item.strip()
            )
        else:
            facts[key.strip()] = int(raw)
    return facts


def _live_facts(root: Path) -> dict[str, object]:
    """Recompute each checkable fact by exercising the engine."""
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "src"))
    from reference_worlds.castaway.probe import build_transfer_engine
    from world_substrate.rules import Check
    from world_substrate.semantic import SEMANTIC_BINDINGS

    engine = build_transfer_engine(root)
    kinds = set(engine.registry.action_kinds())

    # Apply a real action and read its committed event, rather than trusting
    # that attaching the binding was wired up.
    page = engine.discover("robinson")
    row = next(r for r in page["available"] if r["action"]["kind"] == "fill")
    event = engine.submit({**row["action"], "controller": "check"})["event"]
    bound_on_event = event["status"] == "accepted" and event["semantic_binding"] is not None

    # Submit a rule that reaches an entity it never declared, and confirm the
    # engine refuses it. A claim that write scopes are enforced should fail
    # here if the guard is removed.
    class _Probe:
        rule_id = "check.write-scope-probe"
        version = "1"
        action_kind = "check_probe"
        read_paths = ()
        write_paths = ("entities.<x>.container.boiling_ticks",)

        def discover(self, world, actor_id):
            return []

        def action_from_dict(self, value):
            return _ProbeAction(value["actor"], value["base_revision"], value["controller"])

        def checks(self, world, action):
            return [Check("actor exists", action.actor_id in world.entities)]

        def apply(self, world, action, event_id):
            world.entities["clay-pot"].liquid.salt_mg += 1

    # A plain class rather than a dataclass: `from __future__ import
    # annotations` makes a nested dataclass resolve its annotations through
    # `sys.modules[cls.__module__]`, which is absent when this file is imported
    # by spec rather than run as __main__ -- so the probe blew up in the tests
    # that check it while working fine on the command line.
    class _ProbeAction:
        kind = "check_probe"

        def __init__(self, actor_id, base_revision, controller_id):
            self.actor_id = actor_id
            self.base_revision = base_revision
            self.controller_id = controller_id

        def as_dict(self):
            return {
                "actor": self.actor_id,
                "kind": self.kind,
                "base_revision": self.base_revision,
                "controller": self.controller_id,
            }

    engine.registry.register_action(_Probe())
    engine.world.rule_versions = engine.registry.versions()
    refused = engine.submit(
        {
            "actor": "robinson",
            "kind": "check_probe",
            "base_revision": engine.world.revision,
            "controller": "check",
        }
    )

    return {
        "semantic_bindings_bound": len(kinds & set(SEMANTIC_BINDINGS)),
        "semantic_bindings_total": len(kinds),
        "semantic_binding_on_events": bound_on_event,
        "unbound_action_kinds": sorted(kinds - set(SEMANTIC_BINDINGS)),
        "write_scopes_enforced": refused["status"] == "scope_violation",
        "read_scopes_enforced": False,
    }


def check_contract_status(root: Path) -> list[str]:
    """Every fact a contract declares about itself must still hold."""
    failures: list[str] = []
    live = _live_facts(root)
    declared_anywhere = 0
    for name in REQUIRED:
        if not name.startswith("docs/contracts/"):
            continue
        path = root / name
        if not path.exists():
            continue
        for key, expected in _parse_status_facts(path.read_text()).items():
            declared_anywhere += 1
            if key not in live:
                failures.append(f"{name}: unknown status fact {key!r}")
                continue
            if live[key] != expected:
                failures.append(
                    f"{name}: status claims {key}={expected!r}, "
                    f"the code says {live[key]!r}"
                )
    if declared_anywhere == 0:
        failures.append(
            "no contract declares any status facts; the status check is inert"
        )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--with-donors",
        action="store_true",
        help="also verify locally available donor repositories and regenerate the pinned fixture",
    )
    args = parser.parse_args()
    failures: list[str] = []

    for relative in REQUIRED:
        if not (REPO / relative).exists():
            failures.append(f"missing required project surface: {relative}")

    failures.extend(check_contract_status(REPO))

    agents = REPO / "AGENTS.md"
    if not agents.is_symlink() or agents.readlink() != Path("CLAUDE.md"):
        failures.append("root AGENTS.md must be a symlink to CLAUDE.md")

    nested_agents = [
        path.relative_to(REPO)
        for path in REPO.rglob("AGENTS.md")
        if path != agents and not SKIP.intersection(path.relative_to(REPO).parts)
    ]
    if nested_agents:
        failures.append(
            "nested AGENTS.md files are forbidden: "
            + ", ".join(map(str, nested_agents))
        )

    root = (REPO / "CLAUDE.md").read_text()
    if len(root.splitlines()) > 45:
        failures.append(
            f"root CLAUDE.md is {len(root.splitlines())} lines; reorganize instead of expanding it"
        )
    for route in ("docs/wiki/README.md", "roadmap/README.md"):
        if route not in root:
            failures.append(f"root CLAUDE.md does not route to {route}")
        if route not in (REPO / "README.md").read_text():
            failures.append(f"root README.md does not route to {route}")

    if list(REPO.rglob("*HANDOFF*.md")):
        failures.append(
            "special handoff documents compete with normal project navigation"
        )

    wiki = (REPO / "docs/wiki/README.md").read_text()
    for section in WIKI_SECTIONS:
        if section not in wiki:
            failures.append(f"wiki is missing required section: {section}")
    if "role: derived-navigation" not in wiki:
        failures.append("wiki must declare role: derived-navigation")

    roadmap = (REPO / "roadmap/README.md").read_text()
    for section in ROADMAP_SECTIONS:
        if section not in roadmap:
            failures.append(f"roadmap is missing required section: {section}")
    if "role: canonical-planning" not in roadmap:
        failures.append("roadmap must declare role: canonical-planning")

    for path in markdown_files():
        for raw in LINK.findall(path.read_text(errors="replace")):
            target = raw.strip().strip("<>")
            if not target or target.startswith("#") or SCHEME.match(target):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                failures.append(f"broken link: {path.relative_to(REPO)} -> {raw}")

    try:
        manifest = json.loads((REPO / "references/sources.json").read_text())
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid source manifest: {exc}")
        manifest = {"sources": {}}

    if manifest.get("schema_version") != "world-substrate-sources/v1":
        failures.append("unexpected source-manifest schema version")

    try:
        maturity_receipt = json.loads(
            (REPO / "evidence/m1/end-to-end-observation-v1.json").read_text()
        )
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid M1 maturity receipt: {exc}")
    else:
        receipt_check = subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts/validate_e2e_receipt.py"),
                str(REPO / "evidence/m1/end-to-end-observation-v1.json"),
                "--claim-kind",
                "maturity_promotion",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if receipt_check.returncode != 0:
            detail = receipt_check.stderr.strip() or receipt_check.stdout.strip()
            failures.append(f"M1 maturity receipt contract failed: {detail}")
        source_revision = maturity_receipt.get("source_revision")
        if not isinstance(source_revision, str) or not git_has_revision(
            REPO, source_revision
        ):
            failures.append("M1 maturity receipt source revision is unavailable")

    for source_id, record in manifest.get("sources", {}).items():
        if not isinstance(record, dict):
            failures.append(f"invalid source record {source_id}")
            continue
        missing_fields = [
            field
            for field in ("role", "local_path", "disposition")
            if not isinstance(record.get(field), str) or not record[field]
        ]
        for field in missing_fields:
            failures.append(f"source {source_id} lacks {field}")
        if missing_fields:
            continue
        if not args.with_donors:
            continue
        source_path = (REPO / record["local_path"]).resolve()
        if not source_path.exists():
            failures.append(f"missing source {source_id}: {source_path}")
            continue
        expected_revision = record.get("revision")
        if expected_revision:
            try:
                revision_exists = git_has_revision(source_path, expected_revision)
            except OSError as exc:
                failures.append(f"cannot inspect source revision {source_id}: {exc}")
            else:
                if not revision_exists:
                    failures.append(
                        f"pinned source revision unavailable {source_id}: {expected_revision}"
                    )
        expected_hash = record.get("sha256")
        if expected_hash and sha256(source_path) != expected_hash:
            failures.append(f"source hash drift {source_id}")
        subset_hash = record.get("content_subset_sha256")
        if subset_hash:
            artifact_path = (REPO / record["artifact_path"]).resolve()
            if not artifact_path.exists():
                failures.append(f"missing pinned artifact {source_id}: {artifact_path}")
            elif sha256(artifact_path) != subset_hash:
                failures.append(f"pinned artifact hash drift {source_id}")

    if args.with_donors:
        fixture_check = subprocess.run(
            [
                sys.executable,
                str(REPO / "scripts/extract_castaway_fixture.py"),
                "--check",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if fixture_check.returncode != 0:
            detail = fixture_check.stderr.strip() or fixture_check.stdout.strip()
            failures.append(f"derived Castaway fixture check failed: {detail}")

    first_fill_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_first_fill_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if first_fill_check.returncode != 0:
        detail = first_fill_check.stderr.strip() or first_fill_check.stdout.strip()
        failures.append(f"neutral first-fill evidence check failed: {detail}")

    boiling_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_boiling_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if boiling_check.returncode != 0:
        detail = boiling_check.stderr.strip() or boiling_check.stdout.strip()
        failures.append(f"neutral boiling evidence check failed: {detail}")

    pour_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_pour_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if pour_check.returncode != 0:
        detail = pour_check.stderr.strip() or pour_check.stdout.strip()
        failures.append(f"neutral pour evidence check failed: {detail}")

    drink_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_drink_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if drink_check.returncode != 0:
        detail = drink_check.stderr.strip() or drink_check.stdout.strip()
        failures.append(f"neutral drink evidence check failed: {detail}")

    transfer_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_transfer_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if transfer_check.returncode != 0:
        detail = transfer_check.stderr.strip() or transfer_check.stdout.strip()
        failures.append(f"neutral transfer evidence check failed: {detail}")

    replay_check = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts/replay_transfer_evidence.py"),
            "--check",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if replay_check.returncode != 0:
        detail = replay_check.stderr.strip() or replay_check.stdout.strip()
        failures.append(f"fresh-process transfer replay check failed: {detail}")

    freshwater_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/run_freshwater_probe.py"), "--check"],
        check=False,
        capture_output=True,
        text=True,
    )
    if freshwater_check.returncode != 0:
        detail = freshwater_check.stderr.strip() or freshwater_check.stdout.strip()
        failures.append(f"complete freshwater evidence check failed: {detail}")

    first_fill_tests = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(REPO / "tests"),
            "-p",
            "test_*.py",
        ],
        check=False,
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    if first_fill_tests.returncode != 0:
        detail = first_fill_tests.stderr.strip() or first_fill_tests.stdout.strip()
        failures.append(f"neutral runtime tests failed: {detail}")

    if failures:
        print("World Substrate project check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("World Substrate project check passed.")
    print("Reading path: CLAUDE.md -> docs/wiki/README.md -> task authority")
    print("Planning path: README.md -> roadmap/README.md -> active slice")
    print(f"Pinned source records checked: {len(manifest['sources'])}")
    if args.with_donors:
        print("Locally available donor revisions and artifacts checked.")
    else:
        print("Donor checkout verification skipped (use --with-donors to enable).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
