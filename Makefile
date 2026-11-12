.PHONY: check lockstep
# Git hooks export these (in worktrees especially); they would leak into tests' own throwaway repos.
unexport GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_PREFIX GIT_COMMON_DIR GIT_OBJECT_DIRECTORY
UV ?= uv
# The merge gate (ship runs `make check`): links, authority, pinned sources, trace reads and the test suite.
check:
	$(UV) run -q --no-project --python 3.12 --with pydantic --with pyyaml --with pytest --with pytest-xdist --with gdm-concordia==2.4.0 python scripts/check_project.py
# code2 format checks, run by Lockstep (agentic-engineering-system; replaced code2check 2026-11-12).
# Not yet part of `check`: on 2026-11-12 they report 344 trace findings (requirements without
# scenarios or implementers) and 9 decision records without a Source line.
LOCKSTEP ?= uvx -q --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git lockstep
lockstep:
	$(LOCKSTEP) check sources
	$(LOCKSTEP) check trace
	openspec validate --specs --no-interactive
