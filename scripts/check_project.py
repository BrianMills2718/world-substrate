#!/usr/bin/env python3
"""Validate World Substrate navigation, authority, links, and pinned sources."""

from __future__ import annotations

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
    "docs/decisions/001-project-scope.md",
    "docs/source-dispositions.md",
    "docs/research/synthesis.md",
    "roadmap/CLAUDE.md",
    "roadmap/README.md",
    "reference_worlds/CLAUDE.md",
    "reference_worlds/README.md",
    "reference_worlds/castaway/probe.py",
    "references/sources.json",
    "scripts/extract_castaway_fixture.py",
    "scripts/run_first_fill_probe.py",
    "scripts/run_boiling_probe.py",
    "scripts/run_pour_probe.py",
    "src/world_substrate/engine.py",
    "src/world_substrate/model.py",
    "src/world_substrate/rules.py",
    "src/world_substrate/mechanisms/thermal.py",
    "tests/CLAUDE.md",
    "tests/test_first_fill.py",
    "tests/test_boiling.py",
    "tests/test_pour.py",
    "tests/fixtures/castaway/README.md",
    "tests/fixtures/castaway/freshwater-v0.json",
    "reference_worlds/castaway/freshwater-fill-v0.json",
    "reference_worlds/castaway/freshwater-v0.json",
    "evidence/m1/first-fill-v0.json",
    "evidence/m1/boiling-v0.json",
    "evidence/m1/pour-v0.json",
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


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED:
        if not (REPO / relative).exists():
            failures.append(f"missing required project surface: {relative}")

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

    for source_id, record in manifest.get("sources", {}).items():
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

    fixture_check = subprocess.run(
        [sys.executable, str(REPO / "scripts/extract_castaway_fixture.py"), "--check"],
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
    print(f"Pinned sources checked: {len(manifest['sources'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
