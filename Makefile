.PHONY: check planning-check lockstep
# Git hooks export these (in worktrees especially); they would leak into tests' own throwaway repos.
unexport GIT_DIR GIT_INDEX_FILE GIT_WORK_TREE GIT_PREFIX GIT_COMMON_DIR GIT_OBJECT_DIRECTORY
UV ?= uv
# The merge gate (ship runs `make check`): links, authority, pinned sources, trace reads and the test suite.
check: planning-check
	$(UV) run -q --no-project --python 3.12 --with pydantic --with pyyaml --with pytest --with pytest-xdist --with gdm-concordia==2.4.0 python scripts/check_project.py
# AES canonical Lockstep. The planning/source subset is mandatory at merge.
# Full legacy trace linkage remains a separate failing conformance target; it is not downgraded.
# Installation and plan-format checks do not certify runtime coverage.
# $(LOCKSTEP) check below runs the canonical lockstep check command.
LOCKSTEP ?= uvx -q --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git lockstep
planning-check:
	$(LOCKSTEP) check sources
	$(LOCKSTEP) plan check --acceptance docs/planning/open-attempt/acceptance-criteria.json
	$(LOCKSTEP) plan check --acceptance docs/planning/declared-laws/acceptance-criteria.json
	$(LOCKSTEP) plan check --acceptance docs/planning/ai-judge/acceptance-criteria.json
	$(LOCKSTEP) plan check --acceptance docs/planning/estimate-rules/acceptance-criteria.json
	openspec validate --specs --no-interactive
lockstep: planning-check
	$(LOCKSTEP) check
	$(LOCKSTEP) check trace
