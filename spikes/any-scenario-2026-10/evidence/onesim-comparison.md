# YuLan-OneSim on the Waltzman scenario (2026-10-08)

This was a separate test Brian asked for: "look directly at OneSim". It is not part of a plan. The full evidence (requests, timings, generated scenario, local patch) is in `~/code/.scratch/onesim-test/evidence/`, outside git. It cost $3.03 on OpenRouter.

- **Built:** from the same scenario text, OneSim (github.com/RUC-GSAI/YuLan-OneSim, NeurIPS 2025) produced:
  - an ODD document;
  - agent types, including all four concern groups (`05_agent_types.json`);
  - a contact list wiring each group to particular members;
  - a behavior graph;
  - about 1,200 lines of generated code.
- **Missing:**
  - The behavior graph's events are concern raised, received, discussed and settled, plus votes (`06b_workflow.json`). There is no event for reopening an issue or making support conditional.
  - Nothing tracks meetings slowing.
  - A concern travels as an id with no content.
- **Broke:** behavior-graph generation failed every attempt on two models until a two-line local patch (`local_patch.diff`).
- **Not run:** the budget was spent on building, so no simulation ran and the generated code is unverified.
- **Verdict:** do not adopt it whole. Worth borrowing:
  - its interview step, which asks clarifying questions while writing the ODD document;
  - its behavior graph as an intermediate form checked by code for completeness;
  - its generate-then-repair step for code.
