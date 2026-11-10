.PHONY: check code2check
# Git hooks export these (in worktrees especially); they would leak into tests' own throwaway repos.
unexport GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_PREFIX GIT_COMMON_DIR GIT_OBJECT_DIRECTORY
UV ?= uv
# The merge gate (ship runs `make check`): links, authority, pinned sources, trace reads and the test suite.
check:
	$(UV) run -q --no-project --python 3.12 --with pydantic --with pyyaml --with pytest --with pytest-xdist --with gdm-concordia==2.4.0 python scripts/check_project.py
# code2 format checks. Not yet part of `check`: on 2026-11-09 they report 124 requirements without
# scenarios or implementers and 9 decision records without a Source line (see docs/index.md).
code2check:
	code2check sources
	code2check trace
	openspec validate --specs --no-interactive
