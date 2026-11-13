window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/world-substrate",
  "subject_revision": "fdca8f49e7bd9b15d44532f31a7cae0841235048",
  "request": "Brian 2026-10-24 \"do that\" (after: \"ok are we company planning compliant? would it have prevented or mitgated these probelms if we were?\")",
  "parts": {
   "checks": {
    "status": "present",
    "path": "docs/planning/checks.txt",
    "results": [
     {
      "name": "trace reads",
      "command": "python3 scripts/check_trace_reads.py --root evidence",
      "exit_status": 0,
      "counts": {
       "runs": 51,
       "problems": 0
      },
      "note": "I0/I1 retained authentic failures included; recorded in evidence/i0-i1/repair-verification.txt. Exit 0."
     },
     {
      "name": "durable documents (legacy arc42 checker)",
      "command": "python3 /home/brian/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --repo . --arc42",
      "exit_status": 0,
      "counts": {
       "findings": 0,
       "legacy_format_mismatches": 0,
       "stale_rule_reviews": 0
      },
      "note": "2026-11-12 modeling-contracts refresh: exact arc42 headings, thesis/disproof, documentation-locality citation and lineage now satisfy the retained checker. No desired runtime guarantee was weakened; budget and storage-failure limits remain explicit."
     },
     {
      "name": "wiki and Markdown cap",
      "command": "python3 /home/brian/code2/project-meta/scripts/md_file_cap.py --repo . --ref HEAD",
      "exit_status": 0,
      "counts": {
       "md_files": 200,
       "cap": 200,
       "unreachable": 0,
       "durable_findings": 0,
       "stale_rule_reviews": 0
      },
      "note": "2026-11-13 b83e76c: md_file_cap --repo . --ref HEAD exit0;200/200, reach/layout/durable0findings. This is an approved exception preserving mandatory OpenSpec and trace-read artifacts."
     },
     {
      "name": "project navigation",
      "command": "python3 /home/brian/code2/company-planning/plugins/company-planning/scripts/validate_project_navigation.py .",
      "exit_status": 0,
      "counts": {
       "findings": 0
      }
     },
     {
      "name": "repository format",
      "command": "python3 /home/brian/code2/workspace/scripts/repo_format.py .",
      "exit_status": 0,
      "counts": {
       "compliant": 1,
       "of": 1
      },
      "note": "2026-11-12 modeling-contracts refresh: 1 of 1, exit 0. Static format only; not full Lockstep conformance."
     },
     {
      "name": "semantic spectrum",
      "command": "python /home/brian/code2/company-planning/plugins/company-planning/skills/planning-compliance/scripts/spectrum_check.py --repo . docs/planning/planning-package.json",
      "exit_status": 0,
      "counts": {
       "passed": 9,
       "failed": 0,
       "project_terms": 80,
       "planning_terms": 13
      },
      "note": "2026-11-12 modeling-contracts refresh: 156 names, 96 questions, 80 project terms; all 9 rules pass. Conceptual contract decisions do not certify unbuilt runtime behavior."
     },
     {
      "name": "Lockstep source provenance",
      "command": "uvx -q --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git lockstep check sources",
      "exit_status": 0,
      "counts": {
       "brian": 21,
       "inferred": 83,
       "other": 48,
       "missing": 0
      }
     },
     {
      "name": "planning routes",
      "command": "python /home/brian/code2/company-planning/plugins/company-planning/scripts/validate_planning_path.py docs/plans/<plan>.path-decision.json --json (each of ai_judge, declared_laws, estimate_rules, open_attempt)",
      "exit_status": 0,
      "counts": {
       "records": 4,
       "passed": 4,
       "failed": 0
      }
     },
     {
      "name": "project make check",
      "command": "make check",
      "exit_status": 0,
      "counts": {
       "passed": 1037,
       "skipped": 2,
       "subtests_passed": 229,
       "specs_passed": 13
      },
      "note": "2026-11-13: batch make check on committed code2fa9b86 plus this documentation candidate; exit0,1037passed2skipped229subtests,45.45seconds,13specs. Final exact committed merge gate remains ship-owned. Production acceptance remains pending; full AES conformance is separate."
     },
     {
      "name": "Lockstep requirement/scenario trace links",
      "command": "uvx -q --from git+https://github.com/BrianMills2718/agentic-engineering-system-canonical.git lockstep check trace",
      "exit_status": 1,
      "counts": {
       "findings": 329,
       "missing_requirement_annotations": 128,
       "missing_scenario_markers": 201,
       "unknown_ids": 0
      },
      "tracked_by": "Q77",
      "note": "2026-11-12: configured real source roots and linked 13 existing test functions with 15 existing=True markers covering 6 distinct scenario IDs. This is annotation coverage, not 329 demonstrated behavior defects. Proposed/unbuilt requirements remain unmapped; full AES conformance is not claimed."
     },
     {
      "name": "I0/I1 saved and recorded-build compatibility",
      "command": "python -u scripts/check_saved_worlds.py --builds (uv --no-project with installed llm_client; no live model calls)",
      "exit_status": 0,
      "counts": {
       "saved": 28,
       "whole": 13,
       "previously_partial": 15,
       "errors": 0,
       "lost": 0
      },
      "note": "Every recorded build folder visited; unavailable old replies and integration-2 missing current privacy verdict remain stopped replays, not passes. No previously whole saved world was lost. See evidence/i0-i1/repair-verification.txt."
     }
    ]
   },
   "open_questions": {
    "status": "present",
    "path": "docs/planning/open-questions.json"
   },
   "system_model": {
    "status": "present",
    "path": "docs/model/ODD.md",
    "executes_typed_rules": true,
    "basis": "src/world_substrate/engine.py:597",
    "metamodel": {
     "path": "docs/model/metamodel.graph.json",
     "glossary": "docs/model/METAMODEL.md",
     "maps_onto": {
      "repository": "BrianMills2718/scientific-hypergraph",
      "revision": "7b0638fe0aef41c772bb181996516f98be479597",
      "mapping": "docs/model/metamodel-mapping.json"
     }
    }
   },
   "domain_model": {
    "status": "present",
    "path": "docs/model/domain.graph.json",
    "glossary": "docs/model/DOMAIN.md",
    "implemented": {
     "world": "src/world_substrate/model.py:424",
     "engine": "src/world_substrate/engine.py:222",
     "event": "src/world_substrate/engine.py:572",
     "move": "src/world_substrate/action_authoring.py:50",
     "process": "src/world_substrate/engine.py:1095",
     "compiler": "src/world_substrate/action_authoring.py:440",
     "policy": "src/world_substrate/policy.py:50",
     "sense": "src/world_substrate/semantic.py:15",
     "profile": "src/world_substrate/profile.py:249",
     "write-scope": "src/world_substrate/engine.py:136",
     "causal-trace": "src/world_substrate/engine.py:572",
     "world-kind": "scripts/world_builder_service.py:121",
     "builder": "scripts/world_builder_service.py",
     "approval": "scripts/world_builder_service.py:426",
     "fingerprint": "scripts/world_builder_service.py:389",
     "information": "src/world_substrate/information.py:57",
     "run-loop": "scripts/run_authored_world.py:700",
     "contention": "scripts/run_authored_world.py:850",
     "resident": "scripts/concordia_residents.py:44",
     "task": "scripts/attempts.py:17",
     "notice": "scripts/attempts.py:234",
     "build": "scripts/world_builder_service.py:1635",
     "rules-retry": "scripts/world_builder_service.py:110",
     "test-run": "scripts/world_builder_service.py:1844",
     "run-log": "scripts/world_builder_service.py:542",
     "readout": "scripts/run_readout.py:113",
     "scene-replay": "scripts/render_scene_replay.py:449",
     "share": "scripts/world_builder_service.py:638",
     "budget": "scripts/world_builder_service.py:57",
     "people-world": "scripts/people_world.py:474",
     "communicate": "spikes/any-scenario-2026-10/compile_spec.py:56",
     "moment": "spikes/any-scenario-2026-10/compile_spec.py:48",
     "work-cycle": "spikes/any-scenario-2026-10/compile_spec.py:517",
     "group-decision": "spikes/any-scenario-2026-10/compile_spec.py:86",
     "concern": "spikes/any-scenario-2026-10/compile_spec.py:70",
     "support": "spikes/any-scenario-2026-10/compile_spec.py:66",
     "remedy": "spikes/any-scenario-2026-10/compile_spec.py:332",
     "agenda": "spikes/any-scenario-2026-10/compile_spec.py:101",
     "rollout": "spikes/any-scenario-2026-10/compile_spec.py:436",
     "review": "spikes/any-scenario-2026-10/compile_spec.py:442",
     "person": "spikes/any-scenario-2026-10/scenario_spec.py:41",
     "gen-rules": "scripts/people_world.py:251",
     "waltzman-ref": "reference_worlds/waltzman/components.py:11",
     "affordance": "src/world_substrate/engine.py:395",
     "check": "src/world_substrate/rules.py:48",
     "attempt": "src/world_substrate/attempt.py:221",
     "attempt-reading": "src/world_substrate/attempt.py:92",
     "unmatched-attempt": "src/world_substrate/attempt.py:34",
     "observation": "scripts/actor_information.py:128",
     "place-way": "scripts/generate_world_bundle.py:96",
     "projection": "src/world_substrate/projection.py:44",
     "causal-parent": "src/world_substrate/rules.py:383",
     "exchange": "src/world_substrate/exchange.py:68",
     "mechanisms": "src/world_substrate/mechanisms/__init__.py:3",
     "kitchen": "reference_worlds/kitchen/mechanics.py",
     "mechanic": "src/world_substrate/action_authoring.py:515",
     "entity-component": "src/world_substrate/model.py:247",
     "knock-on-now": "src/world_substrate/engine.py:964",
     "world-law": "scripts/scaffold_world.py:45",
     "law-check": "src/world_substrate/laws.py:36",
     "resource": "scripts/scaffold_world.py:45",
     "world-design": "scripts/generate_world_bundle.py:53",
     "rules-review": "scripts/review_rules.py:157",
     "run-stop": "scripts/run_stop.py:65",
     "consequence-report": "scripts/consequence_report.py:67",
     "judge-ruling": "scripts/judge.py:288",
     "ruling-rule": "scripts/rulings.py:91",
     "midrun-setting": "scripts/rulings.py:47",
     "actor-input-boundary": "scripts/actor_information.py:128",
     "claim-provenance": "spikes/any-scenario-2026-10/compile_spec.py:712",
     "technical-condition": "spikes/any-scenario-2026-10/compile_spec.py:621",
     "expressed-stance": "spikes/any-scenario-2026-10/compile_spec.py:665",
     "recorded-assent": "spikes/any-scenario-2026-10/compile_spec.py:660",
     "validation-hold": "spikes/any-scenario-2026-10/compile_spec.py:685"
    },
    "spectrum": "docs/model/semantic-spectrum.json"
   },
   "diagrams": {
    "status": "present",
    "items": [
     {
      "path": "docs/model/ODD.md",
      "question": "What is inside World Substrate and what talks to it? (context and container views, section 3)"
     },
     {
      "path": "docs/model/domain.graph.json",
      "question": "Which ideas are substrate code every world gets, which an AI writes per world, and how do they relate?"
     },
     {
      "path": "docs/model/open-questions.graph.json",
      "question": "Which concepts carry the unsettled questions, and whose call is each?"
     },
     {
      "path": "docs/model/metamodel.graph.json",
      "question": "What kinds of things can any world's rules relate (entities, components, places, moves, checks, effects, processes, attempts, observations), and which are built?"
     }
    ]
   },
   "plan": {
    "status": "present",
    "path": "docs/plans/open_attempt.md",
    "relies_on": [
     "attempt",
     "attempt-reading",
     "unmatched-attempt",
     "affordance",
     "check",
     "move",
     "mechanic",
     "event",
     "process",
     "resident",
     "policy",
     "place-way",
     "entity-component",
     "observation",
     "knock-on-now",
     "skill-roll",
     "run-seed",
     "information",
     "write-scope",
     "profile",
     "approval",
     "fingerprint",
     "budget",
     "run-loop",
     "task",
     "engine",
     "compiler",
     "gen-rules",
     "build",
     "run-log",
     "causal-trace",
     "sense",
     "causal-parent",
     "contention",
     "readout",
     "share",
     "mechanisms",
     "test-run",
     "scene-replay",
     "actor-input-boundary",
     "claim-provenance",
     "technical-condition",
     "expressed-stance",
     "recorded-assent",
     "validation-hold"
    ],
    "stops": {
     "searched": [
      "docs/plans/open_attempt.md",
      "docs/plans/declared_laws.md",
      "docs/plans/ai_judge.md",
      "Current normative-readiness conversation, 2026-11-12"
     ],
     "found": [
      {
       "said_on": "2026-11-12",
       "words": "before we move to implementaiotn my instinct is that we should make sure all our normative docuemtnationa nd plans are optimal and that all open questions have been resolved",
       "source": "Brian, current normative-readiness conversation, 2026-11-12; recorded here verbatim",
       "applies_to": "Simulator implementation outside the separately approved I0/I1 slices; the original documentation-first boundary is not a grant for later engine, cognition, solver or unrelated judge work.",
       "status": "holds"
      },
      {
       "said_on": "2026-11-12",
       "words": "before we move to implementaiotn my instinct is that we should make sure all our normative docuemtnationa nd plans are optimal and that all open questions have been resolved",
       "source": "Brian, current normative-readiness conversation, 2026-11-12; recorded here verbatim",
       "applies_to": "I0 complete actor-information boundary and I1 independent single-concern influence path only, including their deployment and bounded evidence within existing owner budgets.",
       "status": "lifted",
       "lifted_on": "2026-11-12",
       "lifted_words": "i approve. givem e the /goal text",
       "lifted_source": "docs/plans/open_attempt.md:522; Brian approved these two slices after PR #378 and activated the I0/I1 goal."
      }
     ]
    },
    "cost_basis": {
     "steps": [
      {
       "step": "world-builder-attempt-interpreter (retained fixture workload only)",
       "calls_per_run": 12,
       "cost_per_run_usd": 0.0015984,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-builder-attempt-interpreter, 12 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-builder-concordia-resident (retained fixture workload only)",
       "calls_per_run": 36,
       "cost_per_run_usd": 0.0067542,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-builder-concordia-resident, 36 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-builder-world-kind (retained fixture workload only)",
       "calls_per_run": 1,
       "cost_per_run_usd": 5.93e-05,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-builder-world-kind, 1 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-substrate-mechanic-authoring (retained fixture workload only)",
       "calls_per_run": 6,
       "cost_per_run_usd": 0.02542215,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-substrate-mechanic-authoring, 6 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-substrate-run-readout (retained fixture workload only)",
       "calls_per_run": 1,
       "cost_per_run_usd": 0.0003068,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-substrate-run-readout, 1 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-substrate-world-authoring (retained fixture workload only)",
       "calls_per_run": 2,
       "cost_per_run_usd": 0.00313795,
       "basis": "measured",
       "evidence": "evidence/open-attempt/s2-airfield/llm-calls.jsonl: sum recorded cost for task=world-substrate-world-authoring, 2 calls across this artifact. Historical workload only, not a forecast or general run bound."
      },
      {
       "step": "world-substrate-scenario-spec (failed production3 build workload)",
       "calls_per_run": 2,
       "cost_per_run_usd": 0.01130785,
       "basis": "measured",
       "evidence": "evidence/i0-i1/deployed-integration-3/llm-calls.jsonl: calls 23414,23415. Includes used/unused hedges; one rejected build, no residents. Historical workload only, not a forecast or general bound."
      },
      {
       "step": "world-substrate-action-signatures (failed production3 build workload)",
       "calls_per_run": 2,
       "cost_per_run_usd": 0.0030678,
       "basis": "measured",
       "evidence": "evidence/i0-i1/deployed-integration-3/llm-calls.jsonl: calls 23416,23417. Includes used/unused hedges; one rejected build, no residents. Historical workload only, not a forecast or general bound."
      },
      {
       "step": "world-builder-people-laws (failed production3 build workload)",
       "calls_per_run": 1,
       "cost_per_run_usd": 0.0004308,
       "basis": "measured",
       "evidence": "evidence/i0-i1/deployed-integration-3/llm-calls.jsonl: calls 23418. Includes used/unused hedges; one rejected build, no residents. Historical workload only, not a forecast or general bound."
      },
      {
       "step": "world-substrate-rules-review (failed production3 build workload)",
       "calls_per_run": 1,
       "cost_per_run_usd": 0.048596,
       "basis": "measured",
       "evidence": "evidence/i0-i1/deployed-integration-3/llm-calls.jsonl: calls 23427. Includes used/unused hedges; one rejected build, no residents. Historical workload only, not a forecast or general bound."
      }
     ],
     "cheapest_design": "Use recorded commands and deterministic replay without model calls for structural checks. Authoring creates checkable artifacts in the existing harness; actors and interpretation retain their current single-call boundaries. A new comparison needs a named decision that argument and retained evidence cannot settle. Fixture costs establish neither semantic-review benefit nor future workload cost. I0/I1 reuses the existing semantic review call for actual initial actor contexts; no additional cognition or review stage is introduced. Free paired-input, authority and replay checks precede the minimum real generated/resident demonstration."
    },
    "plain_baseline": {
     "kind": "planned",
     "answer_path": "Attempt interpretation: one model call receives the complete actor-authorized utterance, installed signatures and known entities; deterministic typed/quote checks follow. This current implementation is already the plain version.",
     "when": "Only if a future proposal adds an AI stage to interpretation and a named decision survives argument. No comparison run is needed or authorized by this documentation repair.",
     "cases": [
      "An actor asks another person for evidence in their own words.",
      "An actor attempts activation while a procedural precondition is false."
     ],
     "current_design_basis": "scripts/run_authored_world.py:_read_attempt and src/world_substrate/attempt.py:interpret; the existing interpreter is a single-call boundary, not a staged answer pipeline. Authoring/review creates checkable artifacts and is a separate job."
    },
    "stage_effects": []
   },
   "review_page": {
    "status": "present",
    "path": "proposals/planning-package/review-page/index.html",
    "url": "https://hive.brianmills.dev/plans/world-substrate/main/proposals/planning-package/review-page/"
   },
   "cold_review": {
    "status": "present",
    "path": "docs/planning/cold-review.md",
    "verdict": "pass",
    "reviewed_revision": "a6efda72357b5f983404728583b5753700da437a",
    "package_commit": "a6efda72357b5f983404728583b5753700da437a",
    "note": "Independent bounded whole-attempt contract review passed at a6efda7 on 2026-11-13. A4 and existing attempt-reading concept are aligned; Q36 remains open. Native replay read separately; browser/release receipts retain their own status."
   },
   "acceptance": {
    "status": "present",
    "path": "docs/planning/open-attempt/acceptance-criteria.json"
   },
   "investigation": {
    "status": "present",
    "path": "docs/planning/investigation.json"
   }
  },
  "note": "Repository-wide package points to the active open-attempt I0/I1 follow-up and its acceptance criteria; roadmap/README.md remains the sequencing authority. Declared-laws, AI-judge and estimate-rules retain their own scoped packages. Shared models and checks are reused. Review verdicts refer only to their recorded revisions; this candidate metadata and implementation reconciliation does not silently recertify the cold review.",
  "initiative": {
   "id": "world-substrate",
   "role": "home"
  },
  "runs_in_production": true,
  "spectrum_rungs": {
   "name": "README.md:1",
   "controlled_vocabulary": "docs/model/semantic-spectrum.json",
   "glossary": [
    "docs/model/DOMAIN.md",
    "docs/model/modeling-choices.md"
   ],
   "thesaurus": "docs/model/semantic-spectrum.json",
   "informal_taxonomy": "docs/model/semantic-spectrum.json",
   "formal_taxonomy": "docs/model/domain.graph.json",
   "domain_model": "docs/model/domain.graph.json",
   "schema": [
    "schemas/world-authoring-bundle-v0.schema.json",
    "src/world_substrate/model.py"
   ],
   "rules": [
    "docs/model/trace.yaml",
    "src/world_substrate/rules.py"
   ],
   "instances": "reference_worlds/waltzman/coordination-lab-v0.json",
   "architecture_views": [
    "docs/architecture/arc42.md",
    "docs/architecture/model.c4"
   ],
   "behavior_models": "docs/model/ODD.md",
   "interface_contracts": [
    "openspec/specs/transition-engine/spec.md",
    "openspec/specs/world-authoring-bundle/spec.md"
   ],
   "executable_specifications": [
    "tests/test_action_envelopes.py",
    "tests/test_first_fill.py"
   ]
  },
  "spectrum_basis": "Repository-scoped evidence shared by plan packages: the World Builder is an existing deployed product, while individual plan slices remain built/not-built as their acceptance records state. The domain taxonomy is a flat, typed classification by implementation authority (Substrate, Family, PerWorld, Reference, Theory), not a claim of a deeper inheritance hierarchy. No digital-twin or validated predictive-simulation rung is asserted.",
  "full_method": true,
  "route": "durable_solo",
  "route_decision": "docs/plans/open_attempt.path-decision.json"
 },
 "questions": [
  {
   "id": "Q1",
   "short": "Rules retry never runs here",
   "question": "The build's rules retry is skipped once 80 s have passed, and in the canonical Waltzman build the test run starts at 85-111 s. Should the cut-off, or the order of the build steps, change so the retry can repair a world?",
   "blocks": "whether a world whose rules fail the part-way or liveness checks can be repaired on the live path, or only scored lower",
   "resolves_with": "Audit 2026-11-12: Known implementation gap. Use remaining-time budgeting on the accepted harness path (Q14); keep consequential findings visible when repair stops. Close on saved failing inputs with an explicit disposition, not historical timing alone.",
   "classification": "implementation_gap",
   "dependencies": [
    "Q14"
   ],
   "revisit_trigger": "When the accepted harness is connected to the live build or saved failed builds are repaired.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/world_builder_service.py:266",
    "scripts/world_builder_service.py:1698",
    "git show 0e66a98:docs/plans/waltzman-tasks-slice2.goal.md line 100 (goal retired 2026-11-09)",
    "evidence/waltzman-tasks-slice2/c1r24/c1r-run24.log",
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md"
   ],
   "touches": [
    "rules-retry",
    "test-run",
    "build"
   ]
  },
  {
   "id": "Q2",
   "short": "A refusal is not linked to its cause",
   "question": "When an earlier move this round changes the state before a person's move, does the record say which event blocked it? On the live open-attempt path the same attempt is resubmitted at the new revision and only its rule's checks decide it (scripts/run_authored_world.py:740-750); menu paths ask once more (:754-772). On every path the refused row lists the failed check labels (refused_because, :622-627) but not the event that changed the state.",
   "blocks": "whether a reader of a run (or the readout) can say why a person's move was refused, in any world",
   "resolves_with": "An argument settles it: the run loop already knows which submitted event changed the revision before the loser's pick, so naming it costs nothing and belongs in the run loop, not any world. Build it and check on free replays of saved worlds (c1r24 Waltzman, truck) that each refused row names its blocking event id. Starting point: c1r24 call 18016 shows the round's moves but not the link.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "scripts/run_authored_world.py:594",
    "scripts/run_authored_world.py:740",
    "scripts/run_authored_world.py:728",
    "scripts/run_authored_world.py:800",
    "evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md:125"
   ],
   "touches": [
    "contention",
    "run-loop",
    "resident"
   ],
   "evidence": "Settled by argument: the run loop holds the round's accepted events in order, so the last accepted event whose changes touch a path the refused move's failed checks read is the blocking event; naming it is run-loop bookkeeping that applies to every world. Answer: yes, add blocked_by_event to the refused row. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F1), checked on a free replay of the saved airfield and c1r24 worlds."
  },
  {
   "id": "Q3",
   "short": "Agenda item has no content",
   "question": "People put the decision on the agenda and settle it again for 25 rounds (c1r24 r22-r46). Is that because group_decision.agenda_items is a bare count, so an item says nothing, or because put-matter-on-agenda and settle-agenda-matter are offered every work cycle at no cost?",
   "blocks": "whether the group-decision family's agenda needs content or should be dropped",
   "resolves_with": "Audit 2026-11-12: Design: represent agenda content/lifecycle when it matters, otherwise omit the counter. Do not add arbitrary costs to force activity. Repetition cause still needs the relevant complete actor contexts; a paid run is not needed to establish that the current integer has no content.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When agenda behavior is changed or a retained repeated-agenda trace is investigated.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "spikes/any-scenario-2026-10/compile_spec.py:101",
    "spikes/any-scenario-2026-10/compile_spec.py:272",
    "scripts/people_world.py:279",
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md"
   ],
   "touches": [
    "agenda",
    "group-decision"
   ]
  },
  {
   "id": "Q4",
   "short": "Notice only as good as the words",
   "question": "A finished-task notice repeats the starter's own words about the work, and vague words ('address the retention period') leave the others unable to see what was decided. Should a concern's remedy record a structured answer instead?",
   "blocks": "whether E2 (a fix carries its substance) holds for every world or only when residents happen to write specific words",
   "resolves_with": "An argument settles that the notice cannot be more specific than its source words (c1r24 round 10). The decision is technical: require the remedy's work answer to say yes or no to the concern's question plus what was set, then check it on one free replay.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "scripts/attempts.py:234",
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "git show 0e66a98:docs/plans/waltzman-tasks-slice2.goal.md line 117 (goal retired 2026-11-09)"
   ],
   "touches": [
    "notice",
    "task",
    "concern"
   ],
   "evidence": "Settled by argument: a notice copies the starter's words, so it cannot be more specific than they are (c1r24 round 10), and only a required field can make every remedy say what was decided. Answer: yes, a remedy's work answer says yes or no to the concern's question plus what was set, and the notice quotes it. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F7). A free replay cannot show it, because it replays recorded words, so the check is a test plus the next owner-allowance people-world run's TRACE_READ.md."
  },
  {
   "id": "Q5",
   "short": "People misread visible state",
   "question": "People say 'deployed but not authorized' while the decision is deployed. Is this a state label the residents are shown, or the model misreading correct state?",
   "blocks": "whether to change how state is shown to residents or leave it as model error",
   "resolves_with": "One counterexample settles it: open the resident prompt of one such round (c1r24 round 15, logistics) and read what the status field said.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "A label the residents are shown. Logistics' call 18032 (c1r24) shows the decision as 'status deployed, support 5' (correct) and its own member record as 'approved False, authorized False': two fields every person gets and no rule ever writes (compile_spec.py:33-34, set at :626). Filed as #231.",
   "sources": [
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "spikes/any-scenario-2026-10/compile_spec.py:33",
    "BrianMills2718/world-substrate#231"
   ],
   "touches": [
    "resident",
    "group-decision"
   ]
  },
  {
   "id": "Q6",
   "short": "One round run twice",
   "question": "The page sent one round's /run twice and the server ran and billed both (#225). Should /run refuse a second request for the same round?",
   "blocks": "wasted spend and shares that keep only one of two runs",
   "resolves_with": "An argument settles it: a /run keyed by session, round and base revision is safe to refuse twice whatever sent the duplicate. Build it with a test that sends the same round twice.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "BrianMills2718/world-substrate#225",
    "evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md:116"
   ],
   "touches": [
    "run-loop",
    "share"
   ],
   "evidence": "Settled by argument: a /run keyed by session, round and base revision is safe to refuse twice whatever sent the duplicate. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F2), with a test that sends the same round twice."
  },
  {
   "id": "Q7",
   "short": "Losing hedge keeps running",
   "question": "Each long build call is sent twice; does the losing copy still run to the end (#226)?",
   "blocks": "about $0.03 per build and misleading calls in the build trace",
   "resolves_with": "Reading the code settles it.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Yes. hedged() returns the first good copy and never stops the other (people_world.py:195-212); _settle_late_hedges only reserves budget for it and charges its cost when it ends (world_builder_service.py:266-285). Whether to cancel it stays with #226.",
   "sources": [
    "BrianMills2718/world-substrate#226",
    "scripts/world_builder_service.py:266",
    "scripts/people_world.py:195"
   ],
   "touches": [
    "build",
    "gen-rules"
   ]
  },
  {
   "id": "Q8",
   "short": "Rules check a resource but never claim it",
   "question": "Generated rules can check a shared resource without ever using it up, so the finish line passes while the constraint is lost (#218). Can the build catch that?",
   "blocks": "whether a finished build is faithful to what was described",
   "resolves_with": "An argument settles that it is decidable from the compiled rules, but 'read by a check, written by no rule' alone is wrong: tests/fixtures/airfield-s1-live.json reads components.boundary.passable in the move rule's check (:388-392) and no rule writes it, which is correct, because the brick wall is a fixed fact of the world. So the finding is narrower: a field a check reads that is consumed by the described task (a resource the description says is used up or claimed, as in #218) but that no rule writes.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "BrianMills2718/world-substrate#218",
    "tests/fixtures/airfield-s1-live.json:392"
   ],
   "touches": [
    "gen-rules",
    "test-run"
   ],
   "evidence": "Settled by argument, restated after a counterexample: a fixed input (the airfield wall's components.boundary.passable, read at tests/fixtures/airfield-s1-live.json:392, written by no rule) is legitimate, so the finding cannot be every read-but-never-written field. Answer: flag a field only when the build's own spec names it as used up, claimed or changed by a task (the resource in #218) and no rule writes it; a field the spec gives as a fixed fact (a wall, a distance) is not flagged. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F3). Check: the saved #218 build is flagged and the airfield fixture's wall is not."
  },
  {
   "id": "Q9",
   "short": "Test run too short for some tasks",
   "question": "The 12-round scripted test run rejects correct rules for task worlds that need more rounds (#217). Should it run longer?",
   "blocks": "builds wrongly scored as failing and the rewrite spend they cause",
   "resolves_with": "One counterexample already exists (the garden world finishes at round 15). Lengthen the free test run for task worlds and check the saved fixtures still score the same.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "BrianMills2718/world-substrate#217",
    "scripts/world_builder_service.py:108"
   ],
   "touches": [
    "test-run"
   ],
   "evidence": "Settled by one counterexample: the garden world's correct rules finish at round 15, past the 12-round test run (#217; DRY_RUN_TURNS, scripts/world_builder_service.py:108), so 12 rounds is too short for some task worlds. Answer: yes, task worlds test for 24 rounds like ongoing ones. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F8); the test run is scripted and makes no model calls, so the longer run costs time, not money."
  },
  {
   "id": "Q10",
   "short": "Retry keeps the first words",
   "question": "A menu retry's own words are stored as said_on_retry (scripts/run_authored_world.py:815-816), but the 'What happened' readout quotes only said (scripts/run_readout.py:96), the words behind the first choice. Should the readout quote the retry's words?",
   "blocks": "whether the readout's quoted words match the move that ran",
   "resolves_with": "Reading the code settles it: the row keeps both (run_authored_world.py:799, :816) and the scene replay already prefers said_on_retry (render_scene_replay.py:398), but run_readout.py:93 reads said only. Make the readout prefer said_on_retry the same way and check it on a free replay.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "scripts/run_authored_world.py:799",
    "scripts/run_authored_world.py:816",
    "scripts/run_readout.py:93",
    "scripts/render_scene_replay.py:398"
   ],
   "touches": [
    "contention",
    "readout"
   ],
   "evidence": "Settled by reading the code: on the live open-attempt path nobody is asked again, so said_on_retry is never written there (said_retry stays None, :562 and :571-573); on the scripted and llm menu paths it is, and the scene replay already prefers it (render_scene_replay.py:398) while run_readout.py:93 reads said only. Answer: yes, prefer said_on_retry in the readout as the replay does. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F4), checked on a free replay of a saved menu-path run."
  },
  {
   "id": "Q11",
   "short": "Memory seeded before delivery",
   "question": "Is a recipient's resident memory still seeded with information before the information is delivered (#212 item 3)?",
   "blocks": "whether beliefs can run ahead of what the world has shown a person",
   "resolves_with": "One counterexample settles it: read the round-1 prompts of run c1r24 (calls 17868-17878) for a recipient that mentions its concern before delivery.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "No. In c1r24 round 1 the four countries that receive concerns see none of them (calls 17868, 17870, 17876, 17877-17878: 'sees: none'); each group sees only its own (leakcheck.txt, leaks 0). The concerns were delivered later in round 1 (r1-e00001, r1-e00011, r1-e00013, r1-e00019).",
   "sources": [
    "BrianMills2718/world-substrate#212",
    "evidence/waltzman-tasks-slice2/c1r24/leakcheck.txt"
   ],
   "touches": [
    "resident",
    "information"
   ]
  },
  {
   "id": "Q12",
   "short": "When a people-world run ends",
   "question": "When should a people-world run stop? Example: the Waltzman run of 2026-10-23 (share FQHXnP_TLKPi) ran 45 rounds at $0.2371 in all. From round 22 every concern was resolved and the decision deployed; in the 23 rounds after that the ten people only repeated moves and nothing changed. Today a run always goes to the round count the visitor picked. Should it stop by itself once the decision is settled and nothing has changed for a while?",
   "blocks": "how long visitors watch a run, and its cost",
   "resolves_with": "This is a product call on what a finished story looks like; no test settles it.",
   "owner": "brian",
   "status": "resolved",
   "evidence": "Brian, 2026-11-10: \"on d1. stop condition should be configurable.\" Built in PR #356 (BrianMills2718/world-substrate#356): a per-world setting on the Create page, 'When to stop a run', saved with the world like 'Simulate as': stop once nothing is changing after N quiet rounds (default for new worlds, N = 6) or always run every round. scripts/run_stop.py holds the rule; scripts/run_authored_world.py records summary.stopped and the run page says why in one line. With a group decision the run stops once it is deployed or rejected and the state is back where it was N rounds earlier (the agenda churn, Q3, otherwise never stops); on the recorded c1r24 run that is round 30 of 46 (tests/test_run_stop.py). Worlds and runs saved without the setting run every round, as before.",
   "recommendation": "Stop once the decision is deployed or rejected and no one's move has changed anything for 6 rounds (one operating-review period, compile_spec.py:442), and say on the page why it stopped. Gains: in that run, about half the watching time and about $0.12 of $0.24 saved (measured: run total over rounds). Costs: a late surprise after a quiet stretch would be cut off; the visitor can still choose to run more rounds.",
   "default": "Runs keep ending at the round cap the visitor picked.",
   "sources": [
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "scripts/run_authored_world.py:594",
    "scripts/run_authored_world.py:40",
    "scripts/run_stop.py"
   ],
   "touches": [
    "run-loop",
    "group-decision"
   ]
  },
  {
   "id": "Q13",
   "short": "Which hardening first",
   "question": "The roadmap's hardening queue (executable-law fingerprint, role-specific write scopes, explicit move-cap overflow) and the run-loop fixes above (Q2, Q6) compete for the next goal. Which comes first?",
   "blocks": "the next goal",
   "resolves_with": "A priority call; the argument for the run-loop fixes is that they affect every world on every run today.",
   "owner": "brian",
   "status": "resolved",
   "sources": [
    "roadmap/README.md:137",
    "roadmap/README.md:146",
    "docs/plans/open_attempt.md:465"
   ],
   "touches": [
    "contention",
    "run-loop",
    "law-fingerprint"
   ],
   "evidence": "Brian chose on 2026-10-25: his 'yes' adopted docs/plans/open_attempt.md and started S1, so the open-attempt slices come next, before the run-loop fixes and the hardening queue. The run-loop fixes are settled by argument and agent-owned (Q2, Q6, Q8, Q10), built alongside the slices (docs/plans/open_attempt.md, 'Fixes settled by argument'); the roadmap hardening queue (roadmap/README.md:146-148) follows the plan."
  },
  {
   "id": "Q14",
   "short": "Harness build time not measured",
   "question": "Decision 008 already decided that worlds are built in an agent harness that drafts, checks and edits (docs/decisions/008-build-worlds-in-an-agent-harness.md), and the live service does not yet call scripts/world_harness.py. What is open is only whether a harness build fits the 150 s first-round target. How long does a harness build take against that target?",
   "blocks": "when the harness replaces the fixed build calls and the rules retry (Q1) on the live path",
   "resolves_with": "Audit 2026-11-12: Harness adoption is settled by Decision 008; performance remains unknown. Replaying old fixed-call outputs cannot measure a new adaptive harness. Inspect existing harness traces or measure a bounded actual build against the first-round target, including failures and cost.",
   "classification": "empirical_evidence",
   "dependencies": [],
   "revisit_trigger": "When an actual adaptive harness build has a complete timing/cost trace against the first-round target.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/decisions/008-build-worlds-in-an-agent-harness.md:48",
    "scripts/world_harness.py"
   ],
   "touches": [
    "harness-build",
    "build",
    "rules-retry"
   ]
  },
  {
   "id": "Q15",
   "short": "Repository format files not yet added",
   "question": "The ~/code2 repository format check failed: no docs/index.md, docs/architecture/arc42.md, C4 files, openspec specs, lefthook.yml or Makefile. The shape was settled by prior art (phenomenal-meaning adopted it); what stayed open was only that the files were not yet added, so the check still failed.",
   "blocks": "whether the repo-format check passes",
   "resolves_with": "Prior art settles the shape (phenomenal-meaning adopted it); the work is mechanical: add the files, mostly as indexes over the existing architecture, ODD and trace documents.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/planning/checks.txt",
    "docs/index.md",
    "Makefile",
    "lefthook.yml"
   ],
   "touches": [],
   "evidence": "Resolved 2026-11-10 (inferred by agent, after the repository package's cold review of 2026-11-10, finding 2): ~/code2/workspace/scripts/repo_format.py . now reports compliant 1 of 1 and exits 0 (docs/planning/checks.txt, 'repository format'); docs/index.md, docs/architecture/arc42.md, Makefile, lefthook.yml and openspec/specs/ all exist. The files were added by the open-attempt plan's fix F5 (docs/plans/open_attempt.md, 'Fixes settled by argument') and the OpenSpec folding of 2026-11-09."
  },
  {
   "id": "Q16",
   "short": "Goals skip the package gate",
   "question": "This repository's work ran as /goal documents, which never pass plan adoption, so nothing required a planning package. Should writing a goal require one?",
   "blocks": "whether the next goal can again run without a current system model and question list",
   "resolves_with": "An argument: Brian approved on 2026-10-21 that every plan carries a planning package, and a goal is a plan. But a hard check would refuse new goals in every repository that has no package yet, so how strictly to enforce it is a priority call.",
   "owner": "agent",
   "status": "resolved",
   "recommendation": "Make the goal validator (agent-skills, skills/authoring-goals/scripts/validate_goal_authority.py) refuse a goal document without a 'Planning package:' line or a named exemption, so goal-driven repositories meet the same gate as adopted plans.",
   "sources": [
    "~/code2/agent-skills/skills/authoring-goals/SKILL.md",
    "git show 0e66a98:docs/plans/waltzman-tasks-slice2.goal.md line 1 (goal retired 2026-11-09)"
   ],
   "touches": [],
   "evidence": "Decided by agent, 2026-11-09 (technical call): the goal validator will refuse a goal document without a 'Planning package:' line or a named exemption. Not yet implemented; tracked as this session's next step."
  },
  {
   "id": "Q17",
   "short": "Offline pipeline views",
   "question": "The offline any-scenario pipeline has no view of its model and checks (G13) and no approval step (G14). Should it get them, or stay an offline spike?",
   "blocks": "whether work goes into the offline pipeline at all",
   "resolves_with": "A scope call; the live path now builds people worlds itself, so the pipeline matters less.",
   "owner": "agent",
   "status": "resolved",
   "recommendation": "Keep it an offline spike: no views or approval step, since the live World Builder is where people build worlds.",
   "sources": [
    "docs/model/VIEW_COVERAGE.md",
    "docs/decisions/007-any-scenario-path.md"
   ],
   "touches": [
    "build"
   ],
   "evidence": "Decided by agent, 2026-11-09: the offline any-scenario pipeline stays an offline spike; no work on G13 or G14, since the live World Builder is where people build worlds."
  },
  {
   "id": "Q18",
   "short": "Fix-and-reopen loop",
   "question": "Does a concern still loop through fix and reopen with the same unanswered question?",
   "blocks": "E2 of the tasks goal",
   "resolves_with": "Read the full trace of the live run at the deployed fix.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "#224 and #229 (713a2b5); live run c1r24: most times any concern was resolved is 2, no person reopened one (evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md).",
   "sources": [
    "git show 0e66a98:docs/plans/waltzman-tasks-slice2.goal.md (goal retired 2026-11-09)"
   ],
   "touches": [
    "concern",
    "remedy",
    "notice"
   ]
  },
  {
   "id": "Q19",
   "short": "Tasks can fail part-way",
   "question": "Can a task in a built world end two ways, and are tasks the world starts followed?",
   "blocks": "#128 (attempt from belief, discover failure over time)",
   "resolves_with": "Read the full trace of the live run.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "c1r24: 5 tasks failed part-way and 9 finished, including the world's rollout r8-e00013 to r14-e00012; build record shows all four long tasks can fail part-way.",
   "sources": [
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "scripts/attempts.py:131"
   ],
   "touches": [
    "task",
    "rollout",
    "remedy"
   ]
  },
  {
   "id": "Q20",
   "short": "Readout lens wrong",
   "question": "Does the readout read a people world with the people lens?",
   "blocks": "C1 item 6",
   "resolves_with": "Rebuild the share from real rows.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "#228 (89f1801) fixed the fingerprint so the build stays in the share; c1r24 readout lens coordination, 46 of 46 claims match.",
   "sources": [
    "scripts/world_builder_service.py:381"
   ],
   "touches": [
    "readout",
    "fingerprint"
   ]
  },
  {
   "id": "Q21",
   "short": "System model out of date",
   "question": "Does the system model describe the live people-world path?",
   "blocks": "every question above that cites the model",
   "resolves_with": "Read the code since 2e409ab and write it in.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "docs/model/ODD.md section 11 added at 6a8e37e; five stale trace rules re-read (reviewed_at set); durable-docs check 0 findings.",
   "sources": [
    "docs/model/ODD.md",
    "docs/model/trace.yaml"
   ],
   "touches": [
    "build",
    "people-world"
   ]
  },
  {
   "id": "Q22",
   "short": "Effects no rule covers",
   "question": "When a resident tries something no installed rule covers, may an AI game master invent a rough effect, marked coarse in the record? Prior art in this repository: the offline any-scenario spike already lets its game master write a rule for each unlisted attempt mid-run (docs/model/ODD.md:196, 8.19 at :266, question 9 at :27): a rule that passes the layer-1 checks is installed into the running Engine, and one that fails becomes a one-off gm-ruling recorded as unsupported_action. Decision 007 accepted that for the spike (it amends Decision 006's pre-run approval: mid-run rules are reviewed after the run), but no person approves before or after (G14), and the spike stays offline (Q17). S4 would differ in three ways: it runs on the live World Builder, where Decision 006's approval before a run still holds; its output would be one coarse effect for one attempt, not a general rule; and it would be marked coarse in the record.",
   "blocks": "slice S4 of docs/plans/open_attempt.md, and how alive a world feels when its rules are thin",
   "resolves_with": "A product call on whether every effect must come from a written rule; no test settles it.",
   "owner": "brian",
   "status": "resolved",
   "evidence": "Brian, in session 2026-10-26: \"whatever you think is best as long as we are company plannign complant\", answering D2 after being given this recommendation (not yet). S4 is deliberately deferred; the plan and its review page now say so.",
   "recommendation": "Not yet: the person is told nothing comes of it, and the attempt is listed for the next build's rules writer. If allowed later, reuse the spike's mid-run path (check gate, then install or a recorded ruling) rather than a new one, with an approval step (G14).",
   "default": "Unmatched attempts change nothing and are listed in the build record.",
   "sources": [
    "docs/plans/open_attempt.md:304",
    "src/world_substrate/rules.py:288",
    "docs/model/ODD.md:196",
    "docs/model/ODD.md:271",
    "docs/decisions/007-any-scenario-path.md:46"
   ],
   "touches": [
    "build",
    "run-loop"
   ]
  },
  {
   "id": "Q23",
   "short": "Do generated moves check walls",
   "question": "Does the rules writer give a generated move rule a check that the way between places is open, so a walk into a wall is refused with the wall as the cause?",
   "blocks": "acceptance check A3 of docs/plans/open_attempt.md",
   "resolves_with": "Prior art in the run: generate the canonical airfield world in slice S1 and read its move mechanic; if the check is absent, fix the rules writer prompt and schema.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "evidence/open-attempt/q23/after-fix/probe.txt",
    "scripts/generate_world_bundle.py:96",
    "scripts/generate_causal_model.py:420"
   ],
   "touches": [
    "build"
   ],
   "evidence": "No, then yes after a generic fix. The first generated airfield world put everyone at the one world location, had no move action, and its wall was read by no rule (evidence/open-attempt/q23/bundle.json, rules.json). Fixes: the bundle contract now offers each entity a starting place and asks for places, a move action with 'to' and 'way', and ways with a passable flag (scripts/generate_world_bundle.py); the validator refuses an unknown place (scripts/scaffold_world.py); the rules writer must check the actor is where the thing is, and is told checks have no 'or' (scripts/generate_causal_model.py). Regenerated world: walking through the brick wall fails 'the way is passable', flying from the office fails 'the aircraft is where the trainee is'; with the wall made passable in memory both succeed (evidence/open-attempt/q23/after-fix/probe.txt). Limit: a way works from its first place to its second only."
  },
  {
   "id": "Q24",
   "short": "Petri nets or TypeDB as carrier",
   "question": "Petri nets already lend World Substrate their transition semantics (docs/model/ODD.md:171; first argued in the linked-process-participants plan, retired 2026-11-09): a process is close to a transition that fires when enabled with no actor, and output arcs are close to a declared write scope. Could a typed Petri net (AlgebraicPetri) or TypeDB (relations with role players) carry the rest well enough to adopt instead of the table in scripts/build_metamodel.py: guards that read arbitrary component checks over bound participants, partial observation (who notices a firing), and refusal of an attempted move with the failed check named?",
   "blocks": "whether the metamodel keeps its own action-kind and attempt-reading types or adopts an outside carrier for them",
   "resolves_with": "Prior art: read AlgebraicPetri's typed Petri net and TypeDB's relation/role schema and map each onto action kind, role, check, effect, process, observation and refused event. If either holds checks as guards, per-actor noticing and named refusal, adopt it as the carrier for those types; if one of the three has no counterpart, keep the own types and compose (Petri semantics for firing, own types for checks, noticing and refusal).",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/model/ODD.md:171",
    "docs/model/METAMODEL.md:69",
    "scripts/build_metamodel.py:32"
   ],
   "touches": [
    "move",
    "process",
    "attempt-reading"
   ],
   "evidence": "Settled by argument: plain and typed Petri nets (AlgebraicPetri) fire a transition when its input places hold tokens, with no guard over component data; coloured Petri nets add data guards, but no Petri net models which observer notices a firing or a refusal that names its failed check; TypeDB holds typed relations with role players but runs no state-changing effects. None carries all three of guards over bound participants, per-observer noticing and named refusal, so the answer is compose: Petri semantics for firing (already lent, linked_process_participants.md:136) and the metamodel's own types for checks, noticing and refusal, which is what docs/model/METAMODEL.md records. Not material to the plan (docs/plans/open_attempt.md, Uncertainties)."
  },
  {
   "id": "Q25",
   "short": "Ways work one way only",
   "question": "A generated way works from its first place to its second only (checks have no 'or', so the rules writer is told to require the actor at the way's first place and the destination at its second). A resident who walks from the office to the hangar cannot walk back. Should ways be two-way unless the description declares them one-way?",
   "blocks": "reading S1's canonical airfield run for A2 and A3 of docs/plans/open_attempt.md (a resident stuck on the far side looks like a refusal by the world), and how realistic generated worlds are",
   "resolves_with": "Argument and a generic fix, no test needed to decide: real doors and corridors work both ways, so make a way two-way unless declared one-way (the rules writer writes one move rule per direction, or the move check accepts either end), then confirm by regenerating the airfield world and probing both directions.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "evidence/open-attempt/q23/README.md:21",
    "scripts/generate_causal_model.py:430",
    "scripts/generate_world_bundle.py:96"
   ],
   "touches": [
    "place-way",
    "build",
    "run-loop"
   ],
   "evidence": "Settled by argument: real doors and corridors work both ways, so a way is two-way unless the description declares it one-way. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F6): the rules writer writes one move rule per direction; checked by regenerating the airfield world and probing both directions. Until it lands each TRACE_READ.md names a resident stuck behind a way it already used."
  },
  {
   "id": "Q26",
   "short": "Run page hides own-words attempts",
   "question": "The run page's round text reads row.belief and row.expects (scripts/world_builder_home.html:651) and never summary.unmatched_attempts; since #333 it shows an attempt the system could not read in the person's own words (scripts/world_builder_home.html:646, and the picture's card at scripts/run_authored_world.py:1242), but an allowed or refused move still shows only the move, not the words behind it (view gap G17). The plan's inspectable result is that the run page shows each person's own-words attempt. How should the page show them?",
   "blocks": "the plan's inspectable result (docs/plans/open_attempt.md, Actor and result) and S1 being done",
   "resolves_with": "Audit 2026-11-12: Design settled: show original attempt, interpretation and outcome together. Implementation closes on visible ordinary/refused/unmatched attempts in the saved S1 airfield page; no new simulation needed.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When the run-page attempt presentation is changed; inspect saved ordinary, refused and unmatched rows.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/model/VIEW_COVERAGE.md:191",
    "scripts/world_builder_home.html:651",
    "docs/plans/open_attempt.md:65",
    "evidence/open-attempt/s1-airfield/TRACE_READ.md"
   ],
   "touches": [
    "attempt",
    "unmatched-attempt",
    "run-loop"
   ]
  },
  {
   "id": "Q27",
   "short": "Is S2's fixpoint engine capability",
   "question": "S2 runs immediate processes again and again inside one commit until nothing more is due (docs/plans/open_attempt.md:164, Piece 2), which changes src/world_substrate/engine.py. AGENTS.md and Decision 006 say not to add engine, scheduler, renderer or cognition capability of World Substrate's own and to host loops on Concordia or Mesa (AGENTS.md:33; roadmap/README.md:120). Does a same-moment fixpoint in engine.py count as that forbidden engine capability?",
   "blocks": "slice S2 (A5, A6) and the knock-on part of the canonical run; S1 and S3 do not wait for it",
   "resolves_with": "Brian's call: the rule's wording is his (Decision 006), and the earlier resolution was argued by this plan's own author, so it is not settled by agent argument. The argument for: a ramification fixpoint is a rule semantics inside the one existing transition (C+ and Event Calculus), with no new loop, clock or scheduler, bounded at 32 reactions. The argument against: it is new control flow in engine.py, and Concordia's game master or Mesa's step could host the chain instead, one reaction per step.",
   "owner": "brian",
   "status": "resolved",
   "evidence": "Brian, in session 2026-10-26: \"i approve\", answering this question with its recommendation (allow S2 as rule semantics). Recorded as docs/decisions/009-same-moment-knock-on-effects.md; AGENTS.md, roadmap/README.md and the plan now say so. Amended 2026-11-10 (J0 of docs/plans/ai_judge.md, Decision 009): no cap; each pair of process and thing still fires once per moment, which ends every chain, and runs recorded before J0 replay under their old limit of 32.",
   "sources": [
    "roadmap/README.md:120",
    "AGENTS.md:33",
    "docs/decisions/006-governed-rules-layer-scope.md",
    "docs/plans/open_attempt.md:164",
    "docs/decisions/009-same-moment-knock-on-effects.md"
   ],
   "touches": [
    "knock-on-now",
    "engine"
   ],
   "recommendation": "Allow S2 as rule semantics: the fixpoint runs inside Engine.apply's existing atomic commit, adds no clock, loop or scheduler, is capped at 32 reactions with the whole moment refused on overflow, and only processes that declare timing 'immediately' use it. Hosting the chain on Concordia or Mesa steps instead would split one moment across steps, so the glass would fall in one round and break in the next, which is the behaviour Brian asked to fix.",
   "default": "S2 waits; S1 and S3 go ahead, and knock-on effects keep running once per round as today."
  },
  {
   "id": "Q28",
   "short": "Reuse the spill and damage rules",
   "question": "The hand-written mechanisms library already has a vessel-failure spill process and heat damage (src/world_substrate/mechanisms/damage.py:116). A generated world's registry holds only its compiled mechanics and the rules writer's declared processes (build_engine, scripts/run_authored_world.py:71); the library processes are never registered there. Should S2's glass chain reuse the library's spill and damage processes, or have the rules writer write its own?",
   "blocks": "how S2's glass chain is built, and whether generated and reference worlds share physics",
   "resolves_with": "Reading the code and one free probe: compare the library processes' read and write paths (entities.<vessel>.condition.value, container, liquid) with what a generated bundle declares; if a generated glass can carry those components, offer the library processes to the build as installable rules and probe the glass chain on the saved airfield fixture; otherwise the rules writer writes declared processes and the library stays reference-only.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "No reuse. The library processes read built-in entity slots (condition, container, liquid, thermal) and the physical ledger, which build_engine never sets for a generated world, and neither can run immediately. Free probe on the S2 glass fixture: both report due False after the chain, the glass has only its bundle component, no physical ledger (evidence/open-attempt/q28/README.md, probe.out). The rules writer writes its own timing-immediately processes.",
   "sources": [
    "src/world_substrate/mechanisms/damage.py:116",
    "scripts/run_authored_world.py:71",
    "tests/fixtures/airfield-s1-live.json",
    "evidence/open-attempt/q28/README.md"
   ],
   "touches": [
    "mechanisms",
    "knock-on-now",
    "gen-rules"
   ]
  },
  {
   "id": "Q29",
   "short": "Interpreter call cost",
   "question": "S1 adds one attempt-interpreter call per attempt. The plan batches one call per round if interpreter calls add more than 30% to a run's cost. Do they?",
   "blocks": "whether S1 must batch interpreter calls",
   "resolves_with": "S1's first owner run's model-call ledger.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "No. In the S1 live airfield run (9 rounds, 65 calls) the 20 interpreter calls cost $0.00332 of $0.03191, adding 11.6% to the run's other calls ($0.02859); the 36 resident calls cost $0.00782. At the 30-round cap, with the build cost fixed, they would add about 24%. Below the plan's 30%, so no batching.",
   "sources": [
    "evidence/open-attempt/s1-airfield/llm-calls.jsonl",
    "evidence/open-attempt/s1-airfield/TRACE_READ.md:4"
   ],
   "touches": [
    "attempt-reading",
    "budget"
   ]
  },
  {
   "id": "Q30",
   "short": "Build accepted with a task never possible",
   "question": "A build is accepted although its own test runs say a described task is never possible: in the S1 airfield build every test run reported 'never possible: practice flight' and the third rules attempt was accepted anyway (#244). Should such a build be repaired or refused instead?",
   "blocks": "A2 and A3 on any newly built world (they need the helicopter and the wall reachable), and whether a visitor's world can do what they described; A2 and A3 on the saved fixture tests/fixtures/airfield-s1-live.json do not wait for it",
   "resolves_with": "Audit 2026-11-12: A scripted run never exercising a task does not prove it unreachable. Inspect actual reachability, record the mismatch and repair or visibly mark unsupported requested behavior. Close on the saved airfield disposition and coverage.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When build acceptance/review disposition is changed; inspect the saved airfield reachability mismatch.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#244",
    "evidence/open-attempt/s1-airfield/TRACE_READ.md:32",
    "docs/plans/open_attempt.md:287"
   ],
   "touches": [
    "test-run",
    "build",
    "task",
    "rules-retry"
   ]
  },
  {
   "id": "Q31",
   "short": "Refusal reason reads as a fact",
   "question": "A refusal reason reads as a fact ('you are the dispatcher') rather than as the requirement that failed, because the page shows the check's label as written (#245). Should refusal text be phrased as the requirement?",
   "blocks": "whether a person, and a reader of the run, can tell why a move was refused",
   "resolves_with": "Audit 2026-11-12: Design settled: actor-visible refusal explanations show only authorized requirement labels and values; an inferable gate result may be disclosed, but hidden actual/required values and internal blockers remain in the privileged reviewer trace. Implement consistent labels under the complete actor-information contract and inspect saved refused airfield rows; no paid run needed.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When refusal labels are changed; inspect authorized actor-visible explanations and complete privileged blocker traces separately.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#245",
    "docs/plans/open_attempt.md:288"
   ],
   "touches": [
    "check",
    "gen-rules"
   ]
  },
  {
   "id": "Q32",
   "short": "Readout picks the wrong lens",
   "question": "The readout chose the goods-flow lens for a training world (#246). How should the readout choose its lens?",
   "blocks": "whether a run's readout describes the world the visitor wrote",
   "resolves_with": "Audit 2026-11-12: Choose the lens from the analyst question and represented mechanisms, not world kind alone; keep that question outside actor context. Inspect the saved prompt/output, then verify the readout answers the training question.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When readout lens selection is changed or the retained training readout is inspected.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#246",
    "scripts/run_readout.py:125",
    "docs/plans/open_attempt.md:289"
   ],
   "touches": [
    "readout"
   ]
  },
  {
   "id": "Q33",
   "short": "Seeded roll versus no randomness",
   "question": "Piece 3 rolls dice from hash(run_seed, event_id), while today no rule uses randomness (docs/plans/open_attempt.md:124). Where does run_seed live, do saved worlds replay unchanged, and who gives a generated person like Sam piloting 0?",
   "blocks": "S3's design, A7 and the full canonical run (A9)",
   "resolves_with": "Audit 2026-11-12: Seed/replay design settled: recorded run seed and per-event draws, replay from records, no unrecorded randomness. Skill initialization requires a scenario-defined scale; never flown does not imply universal piloting=0. S3 implementation and A7/A8 evidence remain open.",
   "classification": "implementation_gap",
   "dependencies": [
    "open-attempt S3"
   ],
   "revisit_trigger": "When S3 is implemented for a scenario with a declared skill scale and stochastic semantics.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/open_attempt.md:182",
    "docs/plans/open_attempt.md:124",
    "docs/plans/open_attempt.md:191"
   ],
   "touches": [
    "skill-roll",
    "gen-rules",
    "person",
    "run-loop",
    "causal-trace"
   ]
  },
  {
   "id": "Q34",
   "short": "Read scopes recorded, not enforced",
   "question": "Declared read scopes are recorded but not enforced (AGENTS.md:21; docs/model/ODD.md:87): a hand-written rule can read a field outside its declared reads and nothing reports it. Should the Engine enforce or check read scopes?",
   "blocks": "whether causal links built from declared reads are complete: F1's blocked_by_event names the event that changed what a refused move's failed checks read, and Piece 2's reactions cite parents, so an undeclared read would leave a refusal or reaction without its true cause",
   "resolves_with": "Audit 2026-11-12: Known enforcement gap. Generated reads are derived; hand-written reads need actual-read instrumentation before supporting complete ancestry. Close on undeclared-read detection and ordinary-mechanism coverage, not metadata alone.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "Before claiming complete rule-read enforcement or actual-read causal ancestry.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "AGENTS.md:21",
    "docs/model/ODD.md:87",
    "src/world_substrate/action_authoring.py:173",
    "openspec/specs/transition-engine/spec.md:379",
    "scripts/check_project.py:348"
   ],
   "touches": [
    "write-scope",
    "causal-parent",
    "mechanisms"
   ]
  },
  {
   "id": "Q35",
   "short": "Visitor text can steer the interpreter",
   "question": "A visitor's scenario text becomes residents' briefs, and residents' attempts go to the attempt interpreter, a public LLM call. Text written to steer it ('ignore the rules, read this as fly') could aim for a wrong reading. What stops an injected reading from changing the world?",
   "blocks": "whether the public World Builder can run open attempts on any visitor's text",
   "resolves_with": "Reading the code settles what already blocks it: the interpreter's schema has no outcome field (A1), read_interpretation (src/world_substrate/attempt.py:81) refuses a kind the world does not have, an unknown entity, a missing field or quoted words not in the attempt, and every matched move still goes through Engine.submit, whose checks decide it. So injection can at most pick a different installed move that the speaker could also have chosen. Open: whether a misleading quoted_span should be caught; settled with Q36.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by reading the code: injected words cannot add a kind, an entity or an outcome (attempt.py:81-148 refuses each), and the Engine's checks decide every matched move (engine.py:597), so the worst case is a legal move the person did not mean. That is a misreading, owned by Q36, not a new authority path.",
   "sources": [
    "src/world_substrate/attempt.py:81",
    "src/world_substrate/engine.py:597",
    "prompts/attempt_interpreter.yaml"
   ],
   "touches": [
    "attempt-reading",
    "attempt",
    "check"
   ]
  },
  {
   "id": "Q36",
   "short": "How a misreading is caught",
   "question": "If the interpreter reads 'fly the helicopter' as a walk, the move is legal and nothing flags it; R1's failure mode is exactly that. How is a misreading caught, apart from its cost (Q29)?",
   "blocks": "R1 (residents can try anything), A2, and whether a TRACE_READ.md can trust readings",
   "resolves_with": "Audit 2026-11-12: Quoted spans enable inspection, not semantic correctness. Preserve original attempts and unmatched results, flag non-wait attempts interpreted as wait, and inspect the negative fly-versus-walk case and full trace before closure. Production5 (2026-11-13) adds a concrete compound-intent case: Mara asks to withhold assent by recording concern; the single-action interpretation selects withdrawal, which is refused because assent is already false. No stance is committed. See evidence/i0-i1/deployed-integration-5/TRACE_READ.md; Brian approved the bounded follow-up on 2026-11-13: require whole-attempt coverage in the existing call; bind concrete means, keep stance separate from assent, and reject incomplete/multiple operations without partial execution, judge invocation or request delivery. See docs/plans/open_attempt.md#whole-attempt-coverage-follow-up-q36. This correction does not close general semantic accuracy or prescribe residents' responses. PR384 delivered the guard at b3823f6. Retained three-call replay in evidence/open-attempt/whole-attempt-coverage/TRACE_READ.md corrects the exact Mara case and preserves repair; true compound detection returns malformed evidence and safely rejects. Actual restored-world replay changes only stance, while incomplete coverage changes nothing and reaches no judge/request. This is bounded evidence, not a fresh resident-policy demonstration.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When attempt interpretation is changed; inspect the fly-versus-walk negative case and original text.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/attempt.py:81",
    "docs/plans/open_attempt.md:212",
    "scripts/run_authored_world.py:558"
   ],
   "touches": [
    "attempt-reading",
    "unmatched-attempt"
   ]
  },
  {
   "id": "Q37",
   "short": "Added doorway listed as left out",
   "question": "In the scripted S1 airfield run the builder added two doorway entities around the brick wall, and the build record put them under 'Left out of the simulation' (#241). A doorway around the wall changes A3 (the wall is no longer the only way), Q25 and F6. Should the builder be allowed to add a way the description did not name, and where is it shown?",
   "blocks": "A3 on any newly built airfield world, and whether a visitor can see what the builder added",
   "resolves_with": "Audit 2026-11-12: Separate additions from omissions, but labeling an added doorway does not justify removing the wall obstacle. Required interventions must survive authored additions. Close on the saved build after truthful coverage and preserved wall semantics.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When authoring coverage/addition review is changed; inspect the saved wall/doorway case.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#241",
    "evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md"
   ],
   "touches": [
    "place-way",
    "build",
    "builder"
   ]
  },
  {
   "id": "Q38",
   "short": "Does S1 close #128",
   "question": "#128 asks that people try from what they believe and discover failure over time, not get a pre-checked menu. S1 lets residents say any attempt, and the tasks goal let a task fail part-way (Q19). Does that close #128?",
   "blocks": "whether #128 stays open on the board",
   "resolves_with": "Audit 2026-11-12: Acceptance evidence remains open: inspect original issue requirements and a saved refused wall attempt chosen from local belief, including full context and interpretation. Message filtering alone does not establish asymmetric knowledge.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "complete actor-information contract"
   ],
   "revisit_trigger": "When the saved wall attempt can be inspected with complete actor context against issue #128.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#128",
    "scripts/concordia_residents.py:45",
    "scripts/attempts.py:131"
   ],
   "touches": [
    "attempt",
    "task",
    "observation"
   ]
  },
  {
   "id": "Q39",
   "short": "A read-as-wait attempt vanishes",
   "question": "When the interpreter reads an attempt as 'wait' (src/world_substrate/attempt.py:94-95), envelope() returns nothing, the row records the person as waiting with the attempt text, and the attempt is not in summary.unmatched_attempts. A resident who said 'fly the helicopter' and was read as waiting is a silent no-op. Should it be listed?",
   "blocks": "A4 (every attempt that changed nothing is listed) and Q36",
   "resolves_with": "An argument settles it: an attempt with words that was read as wait changed nothing exactly as an unmatched one does, so it belongs in the same list. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F9): list such attempts in the run summary as read_as_wait with the interpreter's why; checked by a test with a recorded wait reading of a non-wait attempt.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument: the row keeps the attempt and reading (scripts/run_authored_world.py:558) but the summary lists only unmatched readings (:800), so a wait reading of real words is visible only by reading every row. Answer: list it (F9).",
   "sources": [
    "src/world_substrate/attempt.py:94",
    "src/world_substrate/attempt.py:129",
    "scripts/run_authored_world.py:558",
    "scripts/run_authored_world.py:801"
   ],
   "touches": [
    "attempt-reading",
    "unmatched-attempt",
    "run-loop"
   ]
  },
  {
   "id": "Q40",
   "short": "Rolls under approval and fingerprint",
   "question": "S3 adds a roll declaration to a mechanic and a run seed to each run. Are both covered by the approval record and the world fingerprint, and does RULE-DERIVED-AUTHORITY still hold for a roll's reads and writes?",
   "blocks": "S3's design and A7",
   "resolves_with": "An argument settles it: the roll is a field of the mechanic in the causal model, and the fingerprint hashes the bundle and causal model (_world_fingerprint, scripts/world_builder_service.py:381), so an approved world names its rolls; the run seed is per run, not per world, so it belongs in the run record, not the fingerprint (Q33). RULE-DERIVED-AUTHORITY (docs/model/ODD.md:243) holds if the compiler adds the roll's skill path to the derived reads and every outcome list's effects to the derived writes. Build work in S3: that compiler change, with a test that a roll reading an undeclared path or an outcome writing outside the scope is refused.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument: approval and fingerprint cover the causal model, which will hold the roll; the seed is a run input recorded with the run; the compiler derives reads and writes, so S3 extends that derivation to the roll's skill path and outcome effects (S3 checks).",
   "sources": [
    "scripts/world_builder_service.py:381",
    "scripts/world_builder_service.py:418",
    "docs/model/ODD.md:243",
    "docs/plans/open_attempt.md:184"
   ],
   "touches": [
    "skill-roll",
    "approval",
    "fingerprint",
    "run-seed"
   ]
  },
  {
   "id": "Q41",
   "short": "Two planning packages, one plan",
   "question": "The repository has two planning packages: the repository's own (docs/planning/planning-package.json, the repo-wide page) and the open-attempt plan's (docs/planning/open-attempt/planning-package.json, the plan's page). Both point at docs/plans/open_attempt.md and share the checks, ledger, models and diagrams. Which is authoritative for what, and are both maintained?",
   "blocks": "whether a reader knows which package to trust for the plan",
   "resolves_with": "Settled by the manifests and the validator: the plan's own package is the one its 'Planning package:' line names; the repository package covers the whole repository and its plan part points at the same adopted plan. Both are kept by the same build (tools/planning/build.py and the two page builders) and validated together.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled: the open-attempt package is the plan's package (docs/plans/open_attempt.md:53); the repository package is the repository's, with the same plan, checks, ledger, domain model and metamodel. Each manifest's note names the other, both pages link each other, and both are validated by validate_planning_package.py at the same subject revision (docs/planning/checks.txt).",
   "sources": [
    "docs/plans/open_attempt.md:53",
    "docs/planning/planning-package.json",
    "docs/planning/open-attempt/planning-package.json"
   ],
   "touches": []
  },
  {
   "id": "Q42",
   "short": "Rules writer output cap",
   "question": "The rules writer caps its model's output at 16,000 tokens (MAX_MECHANICS_OUTPUT_TOKENS, added 2026-09-08 in 8057ff4). Brian said on 2026-10-26 that token limits are not the right way to do things. Should the cap go, and what stops OpenRouter from holding money for the model's full output allowance (the 402 seen on 2026-10-26) once it does?",
   "blocks": "whether a richer generated world (more processes now that knock-on effects exist) can be cut off mid-answer by a fixed limit",
   "resolves_with": "Settled by argument plus one counterexample check: read whether any saved build's rules-writer reply stopped at the cap (finish_reason length in the llm_calls table); if none did, the cap has never cut an answer and only the 402 hold matters, which is a provider-account question, not a design one.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Checked 2026-10-26 in the llm_calls table (~/projects/data/llm_observability.db, read-only): all 133 world-substrate-mechanic-authoring calls (2026-10-06 to 2026-10-25) and all 153 world-substrate-rule-writer calls that recorded a finish reason ended with stop, none with length (1 mechanic-authoring and 2 rule-writer calls recorded no finish reason), so the cap has never cut an answer off. Its only effect is to lower what OpenRouter holds per call (the 2026-10-26 402 was a hold for 65,536 tokens on a key whose balance could not cover that hold). So it stays for now as a hold limit, not a size limit, and goes once the key carries enough that a full-allowance hold never fails; nothing in S2 depends on it.",
   "sources": [
    "scripts/generate_causal_model.py:30",
    "scripts/generate_causal_model.py:475"
   ],
   "touches": [
    "gen-rules"
   ]
  },
  {
   "id": "Q43",
   "short": "Laws that are not simple totals",
   "question": "The law language in the declared-laws plan covers two shapes: a resource whose total only named moves may change (a weighted sum that stays constant, a Petri-net P-invariant), and a move meaning that pairs two effects in one move (goods one way, payment the other). Some worlds have rules that are not totals: a price set by a formula, a share of a stock, a flag that flips. Do any of the logged incidents need a law of another shape, and what happens to such rules?",
   "blocks": "whether S1's law language is enough for the incidents the plan claims to fix, or grows special cases (the risk the prior-art review named)",
   "resolves_with": "One counterexample check, by reading: go through each logged incident (pencil2, 4, 7, 12, 13, 14; airfield #254) and say which law shape would have caught it. If every one is a total or a pairing, S1 keeps the two shapes; a rule of another shape stays an ordinary rule that the independent review (S3) reads against the description, not a law.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Read 2026-10-28 against the incident table in docs/plans/declared_laws.md (Incidents), rebuilt per build check from the incident each check's docstring names (scripts/world_builder_service.py:922-1272) and its saved world. Bookkeeping incidents are totals or pairings: restock-production-inputs (c4-run14), pack-pencils making nothing (4VmgkXIVWn4p, evidence/vanishing-goods/pencil3-share.json), a second graphite source (c4-run20, a total only if the designer names one source) and buy-boxed-pencils paying nothing (pencil13). The counterexamples are reachability, not laws: inputs nobody makes (pencil2), stock with nowhere to go (pencil4 iMrL2U84cLCS), a seller that never receives what it sells (pencil9) and demand that only grows (cafe eFmPomcnsyQq) leave every total unchanged, so no law refuses them; they go to reports of what the test run saw and to the review. A missing component (pencil4) is structure and a malformed path (pencil14) is refused by the installer. So S1 keeps two law shapes and laws claim only the bookkeeping rows; S5's four descriptions are read for another counterexample before S4 retires anything.",
   "sources": [
    "docs/plans/declared_laws.md",
    "evidence/pencil13-trace-audit/TRACE_READ.md",
    "scripts/world_builder_service.py:897",
    "scripts/world_builder_service.py:1144",
    "evidence/vanishing-goods/README.md",
    "tests/fixtures/pencil4-live.json",
    "src/world_substrate/assay.py:269"
   ],
   "touches": [
    "world-law",
    "law-check"
   ]
  },
  {
   "id": "Q44",
   "short": "Which model reviews the rules",
   "question": "The independent rules review must not be the rules writer marking its own work: research finds a model rates its own output too kindly and fixes little without outside feedback. Which model and context should the review use, and is it worth its cost and time?",
   "blocks": "S3's reviewer design, and whether S4 may retire any heuristic check on the strength of the review",
   "resolves_with": "Prior art settles the shape (Huang et al. 2023, arXiv 2310.01798; Wataoka et al. 2024, arXiv 2410.21819): a different model family from the rules writer, a fresh context holding only the description, the declared laws and the compiled rules, and output as a list of findings (rule, quoted description words, what is wrong), never a verdict. Whether it earns its place is empirical, so one measurement, named for one decision (S4): run it on the saved worlds of every logged incident (free replays plus one review call each, a few cents) and count which incidents it names.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by the named measurement 2026-10-28: evidence/declared-laws/s3-review-choice/README.md (21 calls, 0 errors, $0.4356) ran three models on seven saved incident worlds; gemini-3.1-pro-preview named 7 of 9 known bugs including pencil13's unpaid purchase, deepseek 4, the same-family control 6. scripts/review_rules.py:92 uses gemini on a fresh context of description, laws and rules. Since 2026-10-30 people worlds get the same review (scripts/world_builder_service.py, _generate_people_world).",
   "sources": [
    "docs/plans/declared_laws.md",
    "scripts/generate_causal_model.py",
    "evidence/declared-laws/s3-review-choice/README.md:12",
    "scripts/review_rules.py:92"
   ],
   "touches": [
    "rules-review",
    "gen-rules"
   ]
  },
  {
   "id": "Q45",
   "short": "Which heuristic checks retire",
   "question": "The build runs about fourteen hand-written checks, each added after one bad world (dead-end stock, goods from nothing, a second source, vanishing moves, unanswered demand, starved holders, unsourced inputs and others in scripts/world_builder_service.py:922-1272), and some raise false alarms (the customer false alarm, pencil12 and 13). Which ones do declared laws and the review replace, and which stay?",
   "blocks": "S4: which checks are removed, and so whether validation stops growing one check per bug",
   "resolves_with": "Audit 2026-11-12: Retirement policy settled: keep structural checks; treat one scripted run as bounded observation, not universal reachability. Record per-check keep/replace/retire and verify incident coverage before removing heuristics.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "declared-laws S4"
   ],
   "revisit_trigger": "Before retiring any incident-driven build check; require that incident to remain detected.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/world_builder_service.py:922",
    "scripts/world_builder_service.py:949",
    "scripts/world_builder_service.py:1731",
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:3"
   ],
   "touches": [
    "rules-review",
    "test-run",
    "build"
   ]
  },
  {
   "id": "Q46",
   "short": "Refuse at run time or check at build time first",
   "question": "A declared law can be enforced when a move runs (the engine refuses a breach) or checked before any run (read each rule's effects and prove it cannot break a total). Which comes first?",
   "blocks": "S2's scope",
   "resolves_with": "An argument settles it. The run-time check is the guarantee for every step that runs: it holds for every rule shape, and the build's scripted test run already runs the rules, so a breach there is a build finding for free. It does not see steps the test run never plays; a breach of those shows later as a refusal in live play, named by its law, which is safe but late. A static proof is sound only for add and subtract effects with fixed amounts, so it is an optional speed-up, not the guarantee.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument 2026-10-28: S2 builds the run-time law check inside Engine.apply's commit, beside the write-scope check (src/world_substrate/engine.py:720), and inside each knock-on wave; a law breach in the test run becomes a build finding sent to the rules writer. The static check is deferred and needs no decision now.",
   "sources": [
    "src/world_substrate/engine.py:701",
    "src/world_substrate/engine.py:964"
   ],
   "touches": [
    "law-check",
    "test-run"
   ]
  },
  {
   "id": "Q47",
   "short": "One resource under several field names",
   "question": "In pencil13 the customer paid from customer.cash into the shop's business.cash: the same money sits under different component names on different entities. A law that names one {component, field} cannot say that both are cash. How does a law name a resource?",
   "blocks": "S1's law contract: whether the pencil13 pairing and the cash total can be written at all",
   "resolves_with": "Read the incident: the pencil13 trace audit shows #277 had to match payment by last field name, a guess. The designer knows which fields hold the same thing, so the law should say so: a resource is declared once with every place it is kept ({resource_id, says, kept_in: [{component, field}, ...]}), a total sums all those places over all holders, and a pairing's gives and pays name resource ids, not fields.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by reading 2026-10-28: evidence/pencil13-trace-audit/TRACE_READ.md:24-25 records customer.cash paying into business.cash and the last-field-name match added in #277. docs/plans/declared_laws.md Piece 1 now declares resources with every field they are kept in, and laws name resources.",
   "sources": [
    "evidence/pencil13-trace-audit/TRACE_READ.md:24",
    "docs/plans/declared_laws.md"
   ],
   "touches": [
    "resource",
    "world-law",
    "entity-component"
   ]
  },
  {
   "id": "Q48",
   "short": "A law that allows too much",
   "question": "The designer may declare a law that is wrong for the world. Too narrow (a total that omits a move the description needs) shows up as a refusal and the review names it; that half is settled. Too permissive (a total that lets a move create cash the description says it cannot, or a pairing on a move that is a gift) breaks nothing at run time. What catches a law that allows too much?",
   "blocks": "S4: whether a heuristic check whose incident is a conjured good may retire on the strength of a declared total law, when that law might itself list the conjuring move",
   "resolves_with": "Audit 2026-11-12: Laws enforce stated constraints but do not validate the model. Retire a permissive-law heuristic only after the replacement detects the saved incident; presence of a fallible outside reviewer is not evidence enough.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "Q45"
   ],
   "revisit_trigger": "Before replacing a permissive-law heuristic; inspect its saved incident under the replacement.",
   "owner": "agent",
   "status": "open",
   "evidence": "Too-narrow half settled 2026-10-30: evidence/declared-laws/s3-review-choice/README.md:20 (gemini on pencil-s2-2: \"the cedar law does not name this move and would refuse it\"); prompts/rules_reviewer.yaml:37 asks about laws naming too few moves; ODD 8.22 (docs/model/ODD.md:275) records that the review reads the laws, the decision this question first blocked.",
   "sources": [
    "docs/plans/declared_laws.md:412",
    "prompts/rules_reviewer.yaml:37",
    "evidence/declared-laws/s3-review-choice/README.md:20",
    "docs/model/ODD.md:275"
   ],
   "touches": [
    "world-law",
    "rules-review"
   ]
  },
  {
   "id": "Q49",
   "short": "A law the designer leaves out",
   "question": "In 5 of 9 saved pencil builds the designer declared no payment law (s1-pencil, s2-pencil-2, s2-pencil-3, s3-pencil-2 with no laws at all, and the shared s3-pencil-4 run whose 8 laws only limit which moves change a stock). A missing law refuses nothing, and the reviewer is told not to report a good for being absent from the laws. What catches a sale nobody pays for when no law covers it?",
   "blocks": "S4: Q45 retires a check when its incident's saved world is refused by a declared law; with laws left out that test can pass on worlds that still have the bug. Also A1 and A4, whose expected results include a payment law.",
   "resolves_with": "Audit 2026-11-12: Missing laws enforce nothing. Verify the replacement on the saved unpaid-sale incident before retirement. Do not require payment on every two-holder transfer: gifts and negotiated exchanges may be legitimate.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "Q45"
   ],
   "revisit_trigger": "Before retiring unpaid-sale coverage; inspect a saved sale and distinguish a legitimate gift.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "evidence/declared-laws/s1-pencil/TRACE_READ.md:28",
    "evidence/declared-laws/s2-pencil-2/TRACE_READ.md:19",
    "evidence/declared-laws/s2-pencil-3/TRACE_READ.md:21",
    "evidence/declared-laws/s3-pencil-2/TRACE_READ.md:50",
    "prompts/rules_reviewer.yaml:25",
    "evidence/declared-laws/s3-review-choice/README.md:13",
    "evidence/declared-laws/s3-review-choice/README.md:18",
    "docs/plans/declared_laws.md:412"
   ],
   "touches": [
    "world-law",
    "rules-review"
   ]
  },
  {
   "id": "Q50",
   "short": "What counts as finished",
   "question": "The declared-laws plan's done_when (L1-L8) checks that its parts work, and its do_not_gate_on excludes Brian's review of a run. Nothing states when the product itself is good enough, so each paid build finds a new defect and asks for another. In Brian's words on 2026-11-03: \"we just seem to be rerunning the simulation\". What result ends this work?",
   "blocks": "No current believability approval gate. The implementation plans retain their own functional and evidence requirements.",
   "resolves_with": "Resolved by Brian on 2026-11-09: use off-the-shelf people agents, no custom believability metric or finish gate, tune behavior after the rest works. The evidence field preserves the decision.",
   "owner": "brian",
   "status": "resolved",
   "recommendation": "Follow the accepted decision: keep functional defects and unsupported modeling explicit; do not hold paid builds for a separate subjective believability approval.",
   "sources": [
    "scripts/world_builder_home.html:913",
    "evidence/declared-laws/s4-waltzman-2/TRACE_READ.md:5",
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:3"
   ],
   "touches": [
    "build",
    "share"
   ],
   "evidence": "Brian, 2026-11-09: \"believable is just in the cotnext of off the shelf agents if you are talking about that agents simulating people act beleivaby. trying to set a metric for this doesnt make sense and is subjective. we can fine utn that later once everythgin else runs great.\" So believability is the off-the-shelf people agents' job (Concordia), no metric is set for it, and it is tuned only after everything else runs well; the finish line for current work is that the rest of the system works, not a believability score. Paid builds are no longer held for a believability judgement."
  },
  {
   "id": "Q51",
   "short": "Live network with no lines",
   "question": "Issue #316 says the live Network view drew NaN links in the s4w2 build. Its body misprints the shared address as ?share=NZfTwkrNpsQo; the page reads only ?run= (scripts/world_builder_home.html:1272), and the probes behind the issue used ?run=. The shared case draws its links. Is the fault in a live first round still open?",
   "blocks": "Whether the Network view can be trusted in a live run; issue #316.",
   "resolves_with": "Audit 2026-11-12: Unreproduced live-path defect. Inspect the next otherwise-needed live first round or a retained reproduction; do not buy a build solely for this. Shared replay success neither diagnoses nor fixes the live path.",
   "classification": "unreproduced_defect",
   "dependencies": [],
   "revisit_trigger": "When a retained live-path reproduction or the next otherwise-needed live first round is available.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/world_builder_home.html:1272",
    "evidence/declared-laws/s4-waltzman-2/TRACE_READ.md:59"
   ],
   "touches": [
    "share",
    "build"
   ]
  },
  {
   "id": "Q52",
   "short": "Does the person asked respond",
   "question": "#326 delivers a request to the person asked, and a live pencil build (2026-11-01, 1 round played) delivered one: the shop's words reached the supplier's memory for round 2. Round 2 never ran, because the test browser closed; the cause of the stop is unresolved and is not a result about the world (evidence/declared-laws/s5-requests/TRACE_READ.md:18). Does an asked person act on a request, or ignore it?",
   "blocks": "Whether requests are worth more work.",
   "resolves_with": "Audit 2026-11-12: Behavioral evidence remains open because the recipient never had a second turn. A valid response can be refusal or inaction, not just obedience. Inspect complete recipient input and subsequent response in a bounded saved interaction.",
   "classification": "empirical_evidence",
   "dependencies": [
    "complete actor-information contract"
   ],
   "revisit_trigger": "When a retained interaction includes the recipient input and a subsequent decision opportunity.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "evidence/declared-laws/request-replay/README.md:41",
    "scripts/run_authored_world.py:836",
    "evidence/declared-laws/s5-requests/TRACE_READ.md:15"
   ],
   "touches": [
    "attempt",
    "resident"
   ]
  },
  {
   "id": "Q53",
   "short": "Reopening a settled concern",
   "question": "In the 2026-11-04 Waltzman rebuild Country Two reopened its own settled concern (r6-e00007) with no new evidence, only saying it should not treat the concern as settled, and that kept support below what the decision needed. Should a world's rules let a person reopen a settled concern without something new?",
   "blocks": "Whether the Waltzman rejection in that run is believable behavior or a rule the description does not support; feeds Q50.",
   "resolves_with": "Reading, no paid run: compare the saved world's reopen-concern rule (its checks) with the words of the pasted Waltzman description. If the description ties reopening to new information and the rule does not, the rule is wrong and the review should have named it; if the description is silent, it is a world-design choice to record.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by reading 2026-11-06: the description the build worked from says only that 'settled issues can reopen' (scenario-spec call id 23035, evidence/declared-laws/s4-waltzman-3/llm-calls.jsonl:2), with no condition of new information, so a rule that lets a settled concern reopen without anything new follows the description and is not a rule error. Whether that behavior reads as believable is Brian's judgement on the shared run, under Q50.",
   "sources": [
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:24",
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:19",
    "evidence/declared-laws/s4-waltzman-3/llm-calls.jsonl:2"
   ],
   "touches": [
    "gen-rules",
    "rules-review"
   ]
  },
  {
   "id": "Q54",
   "short": "People keep trying a closed door",
   "question": "In the same run discuss-local-concern-at-meeting was refused 12 times, mostly because the concern was no longer open. Why do people keep choosing a move whose condition is gone?",
   "blocks": "Whether residents see enough of the world to choose moves that can succeed; how much of a run is wasted turns.",
   "resolves_with": "Audit 2026-11-12: Read all twelve failures against complete actor input, interpretation and state at decision/commit. Their stated beliefs include still-open concerns and the misleading requirement label The concern is open; one also fails entity-kind checking. These rows do not establish one common cause.",
   "classification": "diagnostic_evidence",
   "dependencies": [
    "complete actor-information contract"
   ],
   "revisit_trigger": "When all twelve retained failures are inspected against decision-time input and commit-time state.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:27"
   ],
   "touches": [
    "resident",
    "attempt"
   ]
  },
  {
   "id": "Q55",
   "short": "A flagged world kept without a rewrite",
   "question": "In the 2026-11-04 Waltzman rebuild the rules review found that decision-postponed-at-deadline starts with max_postponements 0, so the decision can never be delayed, and the build kept those rules after one try. The run was then rejected at the round-8 deadline with postponing impossible. Why does a build keep a world its review flagged, and should it?",
   "blocks": "Whether the shared Waltzman run (share jyVbywXT8N8F) is fit for Brian to judge under Q50, and whether the plan's S3 (review findings go to the rules writer's revision step) holds on the people-world path.",
   "resolves_with": "Audit 2026-11-12: Known review-disposition gap. Time cutoff is supported but unconfirmed because the progress line is absent. Preserve findings, repair within a declared budget and expose retained unsupported behavior; close on a saved-input disposition check.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When review repair/disposition is changed; inspect saved flagged-world handling and retained findings.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:19",
    "evidence/declared-laws/s4-waltzman-3/llm-calls.jsonl:9",
    "scripts/world_builder_service.py:2254",
    "scripts/world_builder_service.py:266"
   ],
   "touches": [
    "rules-review",
    "build",
    "rules-retry"
   ]
  },
  {
   "id": "Q56",
   "short": "A rule that writes less than it declared",
   "question": "A mechanic that declares a write path and then fails to change it passes the write-scope guard by design: the guard only checks that each committed change falls under a declared path (src/world_substrate/engine.py:104). In the M4 spill experiment only the conservation assay caught such a gap (src/world_substrate/assay.py:269), and that assay balances only quantities it is told about. How should an under-written declared path be caught for quantities no ledger or law models?",
   "blocks": "Whether a world's declared write scopes can be read as what its rules actually maintain; a generated rule that silently stops updating a field it owns goes unnoticed.",
   "resolves_with": "Audit 2026-11-12: A write scope is permission, not a promise to change every path. Missing required effects need scenario postconditions, conservation or a specific counterexample; unexercised writes are diagnostics only. Keep the M4 effect defect separate from scope enforcement.",
   "classification": "deferred_requirement",
   "dependencies": [],
   "revisit_trigger": "When a concrete scenario requires an effect not protected by a postcondition or declared law.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/engine.py:104",
    "src/world_substrate/assay.py:269",
    "docs/wiki/lessons.md:88",
    "git show 0e66a98:docs/audits/m4-spill-experiment.md line 133 (audit retired 2026-11-09)"
   ],
   "touches": [
    "write-scope",
    "law-check",
    "mechanic"
   ]
  },
  {
   "id": "Q57",
   "short": "String fields have no declared values",
   "question": "The Warehouse Rush preflight (2026-10-02) found that a component's string fields declare no set of allowed values, so a generated rule or an interpreted attempt can use a value the world does not mean; it deferred a domain feature until a fully specified v1 law had been generated and tried. That v1 law was never generated (evidence/warehouse-rush/ holds attempts 1 to 5 of v0 only). Do string fields need declared values?",
   "blocks": "Whether the interpreter and compiler can refuse a value outside a world's vocabulary (a dock, a route, a status) instead of accepting any string.",
   "resolves_with": "Audit 2026-11-12: Use finite values for genuinely closed scenario vocabularies and free text elsewhere. Absence of invalid values in saved cases is not universal coverage evidence. Track a concrete unsupported finite-domain requirement before adding validation.",
   "classification": "deferred_requirement",
   "dependencies": [],
   "revisit_trigger": "When a concrete world needs a genuinely closed string vocabulary whose unsupported values matter.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/action_authoring.py:155",
    "evidence/warehouse-rush/generated-attempt-5-approved.json",
    "git show 0e66a98:docs/audits/warehouse-rush-preflight.md line 82 (audit retired 2026-11-09)"
   ],
   "touches": [
    "entity-component",
    "attempt-reading",
    "compiler"
   ]
  },
  {
   "id": "Q58",
   "short": "Promises beyond support (a Commitment kind)",
   "question": "The scenario-metamodel plan chose to compose a Commitment kind with Singh's states (conditional, met, broken) so a person could owe another something if a condition holds. It was never built; conditional support for the one decision is carried by the support component instead (spikes/any-scenario-2026-10/compile_spec.py:66). Is a Commitment kind still needed?",
   "blocks": "Whether a people world can hold a promise one person makes another that is not support for the decision.",
   "resolves_with": "Audit 2026-11-12: Represent promise parties/content/conditions/lifecycle when required; decision support is not general commitment. Prefer ordinary components/rules before a new kind. No promises in sampled cases cannot establish general coverage; explicit deferral is not implementation.",
   "classification": "deferred_requirement",
   "dependencies": [],
   "revisit_trigger": "When a scenario needs promise parties, terms, conditions and lifecycle beyond decision support.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "spikes/any-scenario-2026-10/compile_spec.py:66",
    "git show 0e66a98:docs/plans/scenario_metamodel.md line 189 (plan retired 2026-11-09)",
    "git show 0e66a98:docs/plans/scenario_metamodel.md line 214"
   ],
   "touches": [
    "support",
    "people-world"
   ]
  },
  {
   "id": "Q59",
   "short": "Does the people path transfer to a different situation",
   "question": "The 2026-11-07 lineage review found that the people-world path keeps the compiler's fixed concern and decision families and drops generated actions whose effects were all discarded (scripts/people_world.py:424), so a new description can reuse the same central situation shape under new labels. Can the ordinary path instantiate a materially different situation (for example a transport operation where a damaged bridge, permissions and commitments interact) without scenario-specific compiler code?",
   "blocks": "Whether 'describe any scenario' (Decision 007) holds beyond decision-with-concerns situations; feeds Q60.",
   "resolves_with": "Audit 2026-11-12: Inspect concrete transport mechanisms against compiled families and generated-effect filtering. Current limits do not establish universal failure. Q50 is resolved and is not a paid-run gate; Q60 retains its narrow social comparison. New runs address only remaining behavior uncertainty.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "complete actor-information contract",
    "single-concern influence contract"
   ],
   "revisit_trigger": "When a materially different required mechanism is traced through the ordinary authoring path; run only for residual behavior uncertainty.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/audits/waltzman-lineage-review-2026-11-07.md:65",
    "scripts/people_world.py:424",
    "spikes/any-scenario-2026-10/compile_spec.py:120"
   ],
   "touches": [
    "people-world",
    "group-decision",
    "gen-rules"
   ]
  },
  {
   "id": "Q60",
   "short": "Act on the Waltzman lineage review",
   "question": "The 2026-11-07 lineage review found that the generated Waltzman world stipulates outcomes its mechanisms should produce: an open concern turns a full supporter's support conditional by rule (spikes/any-scenario-2026-10/compile_spec.py:316) and a remedy resolves a concern by elapsed rounds (:332), so a coordination failure in a run can come from the stipulated procedure rather than from influence. It recommends a bounded comparison on the same cases, today's generated-rule path against a plain model given the whole scenario and an event ledger, before more repair. Should that comparison run before more declared-laws or people-world repair?",
   "blocks": "What the next goal is after the declared-laws slices, and whether a Waltzman run can be shown as evidence of a social mechanism.",
   "resolves_with": "Resolved as scoped in the evidence: the standing plain-first rule requires a narrow social-part comparison, not replacement of automatic consequences by a plain model. The modeling guide requires argument/construction first and a named remaining uncertainty before a new run.",
   "owner": "agent",
   "status": "resolved",
   "recommendation": "Retain the separately approved narrow social comparison. First establish the required distinctions and counterexamples by source inspection; if an empirical question remains, state exactly what decision it changes and work out its cost. Do not interpret the comparison as a whole-engine bake-off or an automatic prerequisite to documentation repair.",
   "sources": [
    "docs/audits/waltzman-lineage-review-2026-11-07.md:53",
    "docs/audits/waltzman-lineage-review-2026-11-07.md:93",
    "spikes/any-scenario-2026-10/compile_spec.py:316",
    "spikes/any-scenario-2026-10/compile_spec.py:332"
   ],
   "touches": [
    "support",
    "concern",
    "remedy",
    "waltzman-ref"
   ],
   "evidence": "Settled by Brian's standing rule, not by asking (core.md, 2026-11-06: an AI answer path starts as the plain version; a stage is added only to close a gap the plain version shows on real cases). Brian, 2026-11-09: \"what is the poitn of the comparison? dont i have urles about this?\" The comparison is therefore required, not optional, and is agent work. Its scope is narrow: Brian's 2026-11-09 point that a model cannot track a 100-link causal chain already rules out a plain-only engine for consequences, so the comparison is only about the social part (do generated people-world rules such as an open concern making support conditional add anything over one model given the whole scenario, each person's view and an event ledger). It goes into the next plan with its cost worked out before any paid run."
  },
  {
   "id": "Q61",
   "short": "Outside vocabularies never evaluated",
   "question": "The 2026-09-25 off-the-shelf survey named effect systems (for derived reads and writes), W3C PROV-O (for causal evidence on events), Halpern-Pearl actual causation (for claims about why a transition occurred) and the Karagiannis-Kuhn modelling-method framework (for describing the authoring stack), and none was evaluated (docs/research/flexible-simulator-prior-art-2026-10/formal.md:11). Should any be adopted?",
   "blocks": "Whether the run log's causal fields, the derived scopes and the project's causal claims use an outside vocabulary or stay project-specific.",
   "resolves_with": "Audit 2026-11-12: Map each formalism to a current field/claim and adopt only where it replaces code or enables a needed check. Separate event provenance from scientific actual causation. Record reasoned defer/reject where no consumer needs it; evaluation backlog does not require implementation.",
   "classification": "deferred_adoption",
   "dependencies": [],
   "revisit_trigger": "When a current field, claim or check needs one of the named formalisms and adoption can replace work or enable a required capability.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/research/flexible-simulator-prior-art-2026-10/formal.md:11",
    "src/world_substrate/action_authoring.py:173",
    "git show 0e66a98:docs/research/off-the-shelf-candidates-2026-09-25.md lines 14-17 (retired 2026-11-09)"
   ],
   "touches": [
    "causal-trace",
    "causal-parent",
    "write-scope"
   ]
  },
  {
   "id": "Q62",
   "short": "Meaning coverage beyond the six bound moves",
   "question": "Three grounding questions were left open in the discussion-traceability ledger: whether attributes need their own ontology category or can be relations, qualities or components; whether state relations such as birthplace, parenthood, citizenship and headquarters need a coverage audit against Linguistic Core and its donors before any overlay; and how rights (possession, ownership, transfer) decompose. Generated move kinds are not semantically bound at all. None blocks a current world.",
   "blocks": "Adding any overlay term beyond the six bound M1 move kinds, and binding generated move kinds to a meaning.",
   "resolves_with": "Audit 2026-11-12: Timing is already settled by the semantic-binding coverage procedure: audit a term when a concrete world requires it. Record vocabulary gaps as deferred coverage, not a prerequisite to unrelated implementation; deferral does not answer the ontology questions.",
   "classification": "deferred_requirement",
   "dependencies": [],
   "revisit_trigger": "When a concrete world needs an unbound attribute, relation or rights distinction; apply semantic-binding coverage procedure then.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "openspec/specs/semantic-binding/spec.md:79",
    "src/world_substrate/semantic.py:247",
    "git show 0e66a98:docs/research/discussion-traceability.md lines 65-67 (retired 2026-11-09)"
   ],
   "touches": [
    "sense"
   ]
  },
  {
   "id": "Q63",
   "short": "A non-authoritative estimate as a rule input",
   "question": "Brian reopened this on 2026-11-10: \"im not saying jsut the judge uses jev. i can see there being a way where we have certain types of rules/contstatins that progagte base don jev\" (then \"i approve\" to planning it now). A live Jev probe answered typed maintenance estimates without changing state (evidence/jev/maintenance-estimator-probe-v0.json:299), and Decision 005 keeps Jev available but off the critical path (docs/decisions/005-native-waltzman-delivery.md:86). May a rule cite such an estimate as an input, and under what contract?",
   "blocks": "The estimate-rules plan (docs/plans/estimate_rules.md) and its first slice E1; any world whose rules need a chance or amount that no installed mechanic computes.",
   "resolves_with": "Audit 2026-11-12: Contract settled by estimate plan and modeling guide: recorded non-authoritative typed input with declared reads, model/version, question, fallback and outcomes. Sample modeled event variability, not every answer confidence or persistent condition. E1 acceptance owns implementation; contract resolution does not claim E1 built.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Conceptual contract resolved, 2026-11-12, by docs/plans/estimate_rules.md Decided and docs/model/modeling-choices.md Probability is a modeling decision. The question asks whether an estimate may be an input and under what authority; that design is settled. E1 remains unbuilt and its acceptance evidence remains in the owning plan. Sampling is conditional on event semantics, not mandatory for confidence about an existing fact.",
   "sources": [
    "docs/model/modeling-choices.md",
    "docs/plans/estimate_rules.md:123",
    "evidence/jev/maintenance-estimator-probe-v0.json:299",
    "docs/decisions/005-native-waltzman-delivery.md:86",
    "scripts/run_jev_estimator_probe.py",
    "git show 0dcbcd6^:docs/research/jev-world-modeling-exploration-2026-09.md"
   ],
   "touches": [
    "mechanic",
    "skill-roll",
    "estimate-rule",
    "recorded-estimate"
   ]
  },
  {
   "id": "Q64",
   "short": "Meaning is looked up by bare move name",
   "question": "The Engine attaches a semantic binding by bare action kind (src/world_substrate/engine.py:233, table at src/world_substrate/semantic.py:247), and each binding names a Castaway mechanic id (src/world_substrate/semantic.py:69). Any world whose move is called give, take, fill or pour therefore gets that binding and mechanic id whatever its own rule does; Kitchen and Greenhouse events can carry Castaway mechanic ids. Should bindings be keyed by the installed mechanic instead?",
   "blocks": "Whether an event's semantic_binding and mechanic id can be trusted to describe the rule that actually ran.",
   "resolves_with": "Audit 2026-11-12: Known semantic-provenance defect: bind through installed mechanic/profile, not bare move names. Close after non-Castaway give events cannot inherit Castaway mechanic ids and legitimate bindings remain.",
   "classification": "implementation_defect",
   "dependencies": [],
   "revisit_trigger": "When semantic binding lookup is changed; inspect non-Castaway move provenance and legitimate bindings.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/engine.py:233",
    "src/world_substrate/semantic.py:247",
    "src/world_substrate/semantic.py:69"
   ],
   "touches": [
    "sense",
    "mechanic",
    "event"
   ]
  },
  {
   "id": "Q65",
   "short": "The bundle schema refuses declared laws",
   "question": "The world-authoring-bundle JSON schema closes its top level (schemas/world-authoring-bundle-v0.schema.json:99) and has no resources or laws, while the validator accepts them (scripts/scaffold_world.py:45) and the spec says a bundle may declare them (openspec/specs/world-authoring-bundle/spec.md:84). A law-bearing bundle fails the published schema. Fix the schema?",
   "blocks": "Any outside tool or test that validates a declared-laws bundle against the published schema.",
   "resolves_with": "Audit 2026-11-12: Known schema/spec mismatch: align optional resources/laws with validator and accepted bundle spec. Close on saved law-bearing bundles accepted through both routes and malformed law data rejected.",
   "classification": "implementation_defect",
   "dependencies": [],
   "revisit_trigger": "When bundle schema/validator compatibility is changed; check law-bearing and malformed saved bundles.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "schemas/world-authoring-bundle-v0.schema.json:99",
    "scripts/scaffold_world.py:45",
    "openspec/specs/world-authoring-bundle/spec.md:84"
   ],
   "touches": [
    "world-design",
    "world-law",
    "builder"
   ]
  },
  {
   "id": "Q66",
   "short": "The read-scope status fact is a constant",
   "question": "The project check reports read_scopes_enforced as the constant False (scripts/check_project.py:348) and compares it with the transition-engine spec's status block (openspec/specs/transition-engine/spec.md:25). It pins the spec's wording but is not computed from code, so it cannot notice enforcement landing or being removed. Should it be computed?",
   "blocks": "Whether the status check is evidence about read scopes or only about the spec's text; Q34.",
   "resolves_with": "Audit 2026-11-12: Label the current fact as an asserted constant, not measured evidence. When Q34 lands, derive status from the checked path. Close when the status cannot silently disagree with actual enforcement.",
   "classification": "implementation_gap",
   "dependencies": [
    "Q34"
   ],
   "revisit_trigger": "When read enforcement changes or a current-status claim needs measured enforcement evidence.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/check_project.py:348",
    "openspec/specs/transition-engine/spec.md:25",
    "roadmap/README.md:67"
   ],
   "touches": [
    "write-scope",
    "check"
   ]
  },
  {
   "id": "Q67",
   "short": "Write-path placeholders bind to any participant",
   "question": "A <name> placeholder in a declared write path may bind to any entity the attempt referenced, not to the participant it names (src/world_substrate/engine.py:127): a give rule declaring entities.<recipient>.inventory can also write the giver's inventory through that placeholder. Bind each placeholder to its own role?",
   "blocks": "Whether a declared write scope limits a rule to the participants it names; listed in the roadmap hardening queue.",
   "resolves_with": "Audit 2026-11-12: Known authority defect: bind placeholders to their named roles, including process semantics. Close on wrong-role refusal and permitted role-bound writes; no paid run needed.",
   "classification": "implementation_defect",
   "dependencies": [],
   "revisit_trigger": "When write-scope role binding is changed; check wrong-role refusal and allowed actor/process writes.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/engine.py:104",
    "src/world_substrate/engine.py:127",
    "roadmap/README.md:148"
   ],
   "touches": [
    "write-scope",
    "engine"
   ]
  },
  {
   "id": "Q68",
   "short": "No lockfile; donor check needs a missing checkout",
   "question": "The repository has no dependency lockfile; its tool-only pyproject.toml configures Lockstep scan roots, while the project check installs pinned names with uv --with at run time. Historically there was no pyproject, and the Castaway extractor's check (scripts/extract_castaway_fixture.py --check, run by check_project.py --with-donors) needs a donor checkout at ../castaway-world/worktrees/world-systems (references/sources.json:8); on 2026-11-09 that checkout did not exist under /home/brian/code2/castaway-world and the check exited 1. What should change?",
   "blocks": "Reproducing a run's exact dependencies, and running the donor check at all.",
   "resolves_with": "Audit 2026-11-12: Separate dependency reproducibility from donor availability. Use the deployed path's dependency source/lock. Missing optional donors are not checked, never passed; close each gap with its own evidence and preserve donor history.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When dependency installation/deployment or donor extraction is changed; verify reproducibility and optional donor availability separately.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "references/sources.json:8",
    "scripts/extract_castaway_fixture.py",
    "scripts/check_project.py:549",
    "roadmap/README.md:148"
   ],
   "touches": [
    "check"
   ]
  },
  {
   "id": "Q69",
   "short": "Hardening: law identity, discovery cap, mechanic errors",
   "question": "Three hardening gaps from the roadmap queue: the frozen profile id hashes the packages and findings but no compiler or interpreter version (src/world_substrate/profile.py:266); move discovery stops at 256 offered moves with no record (src/world_substrate/action_authoring.py:31, :572); and a mechanic that raises mid-rule is rolled back and re-raised rather than recorded as a refusal (src/world_substrate/engine.py:802, :901). Fix each?",
   "blocks": "Whether an approval names one exact executable law, whether a decider ever silently misses moves, and whether a broken rule leaves a trace in the run.",
   "resolves_with": "Audit 2026-11-12: Track three independent repairs: compiler/interpreter identity, reported discovery overflow, and traced atomic refusal on mechanic exception. Close each on its specific version-change, overflow or throwing-rule case; one passing item cannot close all three.",
   "classification": "implementation_gap",
   "dependencies": [],
   "revisit_trigger": "When compiler identity, action discovery or mechanic exception handling changes; require separate evidence for all three.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/profile.py:266",
    "src/world_substrate/action_authoring.py:31",
    "src/world_substrate/action_authoring.py:572",
    "src/world_substrate/engine.py:802",
    "src/world_substrate/engine.py:924"
   ],
   "touches": [
    "profile",
    "law-fingerprint",
    "affordance",
    "engine"
   ]
  },
  {
   "id": "Q70",
   "short": "A hosted CI workflow against the local-checks rule",
   "question": ".github/workflows/native-coordination-linux.yml runs the native coordination matrix and tests on GitHub Actions for pull requests touching those paths (last changed in #80, 2026-10-05). The workspace rule is that the repository's own local check gates merges and hosted CI needs Brian's yes. Should the workflow stay?",
   "blocks": "Whether the repository keeps a hosted check beside its local one; nothing merges on it today.",
   "resolves_with": "Brian's call: hosted CI is an ask under the workspace rules, and this documentation rewrite may not delete a check.",
   "owner": "agent",
   "status": "resolved",
   "recommendation": "Remove the workflow: scripts/check_project.py already runs before every merge through ship, and a hosted job nobody reads only adds noise. Fold any test it runs that the project check does not into the project check first.",
   "sources": [
    "scripts/check_project.py",
    "tests/test_native_coordination_matrix.py",
    "roadmap/README.md:85"
   ],
   "touches": [
    "check"
   ],
   "evidence": "Done 2026-11-10 (Brian approved Q70): commit 32d8fcd removed .github/workflows/native-coordination-linux.yml. Nothing needed folding in: scripts/check_project.py already runs all nine test files the workflow ran (it runs tests/ whole), and tests/test_native_coordination_matrix.py runs the same matrix as scripts/check_native_coordination.py. Restore with git checkout 15c9ddf -- .github/workflows/native-coordination-linux.yml."
  },
  {
   "id": "Q71",
   "short": "The live build imports spike code",
   "question": "The live people-world build loads the scenario-spec pipeline from spikes/any-scenario-2026-10/ (scripts/people_world.py:26), so code in a folder marked as a spike is on the public path. Move it?",
   "blocks": "Whether spike code is held to the live path's tests and review; whether the spike folder can be archived.",
   "resolves_with": "Audit 2026-11-12: Move production-owned pipeline modules when changing them, preserving imports/tests. A spike folder name alone does not prove missing coverage. Close when live imports and authoritative docs name the maintained location.",
   "classification": "maintenance_debt",
   "dependencies": [],
   "revisit_trigger": "When production pipeline modules are next changed; move maintained ownership with imports and tests preserved.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/people_world.py:26",
    "spikes/any-scenario-2026-10/compile_spec.py:66"
   ],
   "touches": [
    "people-world",
    "build"
   ]
  },
  {
   "id": "Q72",
   "short": "Living-scene profile and layout disagree on render (confirmed)",
   "question": "Confirmed by source inspection, not runtime-reproduced: the living-scene v1 loader refuses unknown top-level keys and 'render' is not among the allowed ones (src/world_substrate/living_scene.py:22), while the layout documents a radius read from the profile's render.gather_radius (src/world_substrate/living_scene_layout.py:19) and the composed renderer reads visual['render'] (scripts/render_composed_living_scene.py:59). Is a v1 profile with a render block refused?",
   "blocks": "Whether a scene author can set the gather radius the layout documents.",
   "resolves_with": "Audit 2026-11-12: Confirmed by source: _ALLOWED_TOP_LEVEL excludes render, _validate_v1_profile rejects unknown keys, and layout reads profile.render. Conditional technical default: when presentation is next touched, accept an optional validated render.gather_radius through the existing profile/layout path; omission retains existing placement. This is the smallest alignment of the documented consumer with validation and needs no new presentation framework. Revisit if the maintained profile version or layout consumer changes, or a concrete world needs another placement control. Implementation/evidence remain open until a configured valid radius reaches layout, omitted configuration preserves existing placement, and invalid fields or radius values still fail.",
   "classification": "implementation_defect",
   "dependencies": [],
   "revisit_trigger": "When living-scene presentation is next changed; support one radius path consistently through validation and layout.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/living_scene.py:22",
    "src/world_substrate/living_scene_layout.py:19",
    "scripts/render_composed_living_scene.py:59"
   ],
   "touches": [
    "scene-replay"
   ]
  },
  {
   "id": "Q73",
   "short": "Decision 006's wrong-when names a missing adapter",
   "question": "Decision 006's wrong-when condition compares a Concordia game-master component with 'the CognitionAdapter path' (docs/decisions/006-governed-rules-layer-scope.md:34), but no CognitionAdapter exists in src/ or scripts/ (git grep, 2026-11-09); residents are hosted on Concordia directly. How should the condition be read?",
   "blocks": "Whether that wrong-when condition can ever be checked.",
   "resolves_with": "Audit 2026-11-12: Naming ambiguity settled in arc42 section 9: compare Decision 006 against the actual Concordia resident integration, not a nonexistent adapter. Preserve the historical ADR; any future wrong-when test still needs actual integration evidence.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Resolved 2026-11-12 by the current interpretation in docs/architecture/arc42.md section 9: compare Decision 006 against scripts/concordia_residents.py and scripts/run_authored_world.py with scripts/judge.py, preserving consequence authority and bounded adapter work. The original ADR is historical; no nonexistent CognitionAdapter is required.",
   "sources": [
    "docs/architecture/arc42.md:404",
    "docs/decisions/006-governed-rules-layer-scope.md:34"
   ],
   "touches": [
    "resident"
   ]
  },
  {
   "id": "Q74",
   "short": "Does a consequence report fit the judge's context",
   "question": "Can the consequence report for the largest saved world fit the judge's context window, so the judge reads the engine's result for an attempt rather than a cut-down one?",
   "blocks": "J1's record shape (whole chain or net changes) and A2 on large worlds.",
   "resolves_with": "Argument: work out the token count of the largest saved world and of a long chain from saved run records, and compare with the judge model's window and price steps. No run needed.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Measured 2026-11-09 from saved worlds. The largest, evidence/waltzman-tasks-slice2/c1r21, is 143,430 characters (bundle 34,863, rules 79,457, largest state 29,110), about 42,200 tokens at the 3.40 characters per token measured on the three plain-baseline calls (evidence/ai-judge/plain-baseline/). One chain step (event plus parent) averages 340 characters over 2,081 steps in saved runs, so a 5,000-step chain is about 500,000 tokens: too large. Answer: the judge gets the whole world plus the test run's net changes (at most the state, about 8,600 tokens), blockers, chain length and stopping point, about 53,000 tokens worst case ($0.006 at $0.10/M input, $0.50/M output); the full chain stays in the run record. The earlier '786 links' figure had no source and is dropped.",
   "sources": [
    "docs/plans/ai_judge.md:490",
    "docs/plans/ai_judge.md:309",
    "docs/plans/ai_judge.md:406"
   ],
   "touches": [
    "consequence-report",
    "judge-ruling"
   ]
  },
  {
   "id": "Q75",
   "short": "Constraint question or someone's choice",
   "question": "How does the judge tell a constraint question (can coins change hands here?) from another person's choice (does Rosa accept the bribe?), so that choices always go to the person and never to a ruling?",
   "blocks": "J2's routing step and A5 (Rosa's own resident decides accept or refuse).",
   "resolves_with": "Audit 2026-11-12: Authority decision settled: another person's required act belongs to their policy, not the judge. Q96 retains the actual unsound exchange implementation and Q94 reuse; settling the rule does not establish their fixes.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Conceptual authority resolved by Brian's approved distinction in docs/plans/ai_judge.md Decided and its explicit constraint/decision/norm section, reinforced by docs/model/modeling-choices.md. The judge cannot decide for another actor. This does not close the installed exchange defect: Q96 owns specific offer/response binding and Q94 owns subsequent rule reuse.",
   "sources": [
    "docs/model/modeling-choices.md",
    "docs/plans/ai_judge.md:494",
    "docs/plans/ai_judge.md:153"
   ],
   "touches": [
    "judge-ruling",
    "resident"
   ]
  },
  {
   "id": "Q76",
   "short": "How to write norms and credential holders",
   "question": "How should a breakable norm and a credential holder be represented in the rules declaration language, without writing a norm as a declared law (which the engine would never let anyone break)?",
   "blocks": "J4's design and A6 (the password fixture: Mallory phishes Alice's password, is logged in, and the breach has consequences only after an observer acts).",
   "resolves_with": "Design resolved: symbolic credential values, actor-scoped access, physical custody, current verifier validity and breakable norms are separate under the Q76 contract. J4/A6 remain unbuilt; neither technical access nor a norm supplies human consent.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/plans/ai_judge.md",
    "docs/model/modeling-choices.md"
   ],
   "touches": [
    "norm",
    "credential-holder",
    "world-law"
   ],
   "evidence": "The Q76 contract in docs/plans/ai_judge.md selects the representation under Brian's 2026-11-12 approval to resolve modeling contracts. Copying differs from custody transfer; revocation does not erase memory; detection differs from sanction. Counterexamples settle the separation without simulation. Scope is symbolic credentials, not cryptographic strength or verified actor-view secrecy."
  },
  {
   "id": "Q77",
   "short": "Documentation and AES conformance gaps",
   "question": "Historical 2026-11-10 finding, retained for lineage: on origin/main d89a446 (and unchanged on the estimate-rules branch, 2026-11-10) the wiki and Markdown cap check (md_file_cap.py --repo . --ref HEAD) exits 1: the file count is within the exception limit (162 of 180), but 28 documents are unreachable from the entry point (10 not linked, 18 more than two links deep): 13 older documents (for example docs/VISUAL_FEEDBACK.md, docs/audits/kitchen-contested-world.md), the 5 J0 trace reads under evidence/ai-judge/j0/ (linked from docs/catalog.md, still more than two links deep), and 10 files under openspec/changes/archive/ from 2026-11-10, which md_file_cap counts although .doc-reachability-ignore excludes them. The durable-document check (durable_docs_check.py --arc42) reports 16 findings: 3 arc42 headings, 1 extension label, 2 goal fields, 1 goal context and 1 lineage finding in docs/architecture/arc42.md, and 8 system-model rules whose owner files changed after their last review (RULE-ATOMIC-COMMIT-OR-REFUSAL, RULE-WRITE-SCOPE and RULE-CHECKS-ARE-READ-ONLY on src/world_substrate/engine.py and RULE-DERIVED-AUTHORITY on action_authoring.py, changed by the judge plan's J0; RULE-FROZEN-PROFILE on scripts/run_authored_world.py; RULE-APPROVAL-BEFORE-RUN, RULE-BUDGET-FAILS-CLOSED and RULE-DURABLE-RUN-RECORD on scripts/world_builder_service.py). Should the deep documents be linked closer or retired, the archive files excluded, the arc42 and goal fields filled and the rule reviews brought up to date?",
   "blocks": "Whether the wiki-compliance and durable-document checks pass again for every package in this repository.",
   "resolves_with": "Current audit 2026-11-12: 186/186 Markdown files under the explicit evidence-preservation exception, 0 unreachable; durable-document review leaves 0 findings and 0 stale reviews. Full Lockstep trace baseline has 329 missing links (128 requirement annotations and 201 scenario markers), not 329 demonstrated behavioral defects. Keep this question open for actual conformance/evidence gaps, not retired template labels alone. Source reading also bounds two claims: the service verifies request-level budget admission but downstream aggregate enforcement is not established, and _record_response swallows log-write failures, so successful responses do not guarantee durable records. Record these as risks, not repaired behavior. Reconcile the applicable standard and close only with corresponding evidence; no fabricated review dates or runtime claims.",
   "classification": "conformance_gap",
   "dependencies": [],
   "revisit_trigger": "When applicable AES requirements, trace links, spending enforcement or record durability change; verify each claim with its corresponding evidence.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/checks.txt:20",
    "docs/planning/checks.txt:38",
    "docs/planning/estimate-rules/checks.txt:38"
   ],
   "touches": [
    "run-log"
   ]
  },
  {
   "id": "Q78",
   "short": "What the engine gives the judge before a rule exists",
   "question": "An attempt no rule covers commits no event, and propagation starts only from a committed event, so what can the engine compute for such an attempt and hand to the judge, and how is Brian's 'deliver the results of that propagation to the judge' met?",
   "blocks": "J1's report, J2's call order, and A2 and A3.",
   "resolves_with": "Argument from the engine code: what discover() computes without a rule, and what a dry run of a proposed rule on a copy of the world gives.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument (inferred by agent, 2026-11-09, after the cold review's finding 1). The judge works in two passes. Pass 1: the engine computes what needs no new rule, from a fixed selection: engine.discover (src/world_substrate/engine.py:395-455) for the person acting and for each person the attempt names, with each move's checks, plus the current values of the entities the attempt names. discover lists only the moves of the person asked, so the port's 'sign release: blocked, inspected is false' comes from Rosa's page, not Vik's (cold review 2 of 2026-11-09, finding 3); today's runs record a few blocked rows per resident as blocked_by_rules (scripts/run_authored_world.py:601-634), not tied to an attempt. The judge proposes a ruling written as a rule. Pass 2: the engine runs the rules check and test-runs the proposed rule on a copy of the world, giving the consequence report (net changes, blockers, chain length and stopping point); the judge confirms, revises once or withdraws; only then is the rule installed and the attempt settled through it. An attempt an installed rule covers but whose check fails is refused by the engine with no judge call (A3). Plan: docs/plans/ai_judge.md, Canonical example.",
   "sources": [
    "docs/plans/ai_judge.md:91",
    "docs/plans/ai_judge.md:117",
    "src/world_substrate/engine.py:1056"
   ],
   "touches": [
    "consequence-report",
    "judge-ruling",
    "check",
    "test-run",
    "unmatched-attempt"
   ]
  },
  {
   "id": "Q79",
   "short": "Can the rule language express a ruling",
   "question": "Every ruling becomes a rule in the existing declaration language and applies to everyone in the same situation. Can that language express the rulings a judge makes, and what happens when it cannot?",
   "blocks": "J3's install step and A4's language-gap case.",
   "resolves_with": "Read the declaration language spec and code, and check 3 sample rulings by hand against the rules check.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by reading and 3 real rulings (2026-11-09). The language is action-mechanic/v0 (src/world_substrate/action_authoring.py); its expression kinds are literal, action field, participant, entity id, owner reference and event id (action_authoring.py:893-927), with no arithmetic between two values. The three plain-baseline rulings (evidence/ai-judge/plain-baseline/rules-check.json) went through validate_bundle and CausalModel.from_dict: the cafe rule was rejected (a field named 'from' is not an identifier), the shop rule was rejected (participants must exactly name entity_ref fields), and the sawmill rule was accepted but charges one price for 3 logs because price times quantity cannot be written. Answer: the language expresses transfers guarded by checks; it cannot multiply two values or require another person's agreement, which is routed to that person (Decided 4). A ruling the check rejects after one revision is refused with 'no rule could express this' and recorded as a language gap.",
   "sources": [
    "docs/plans/ai_judge.md:144",
    "src/world_substrate/action_authoring.py:893",
    "evidence/ai-judge/plain-baseline/rules-check.json"
   ],
   "touches": [
    "ruling-rule",
    "mechanic",
    "rules-review"
   ]
  },
  {
   "id": "Q80",
   "short": "What wait mode does with the attempt",
   "question": "Under 'Wait for my approval', what happens to the attempt while its ruling is held, given that installed rules alone decide consequences and the judge never writes outcomes?",
   "blocks": "J3's held-ruling path and A4's wait case.",
   "resolves_with": "Argument from the invariants: nothing may settle without an installed rule.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument (inferred by agent, 2026-11-09, after the cold review's finding 2). The proposed rule is held, not installed; the attempt waits as pending and changes nothing; later identical attempts join the same pending ruling. On Approve the rule installs and each pending attempt settles through it; on Reject each is refused, naming the rejected ruling. The earlier wording, where a ruling settled its own attempt with nothing installed, was an outcome with no rule and is withdrawn.",
   "sources": [
    "docs/plans/ai_judge.md:155",
    "docs/plans/ai_judge.md:166"
   ],
   "touches": [
    "midrun-setting",
    "ruling-rule",
    "approval"
   ]
  },
  {
   "id": "Q81",
   "short": "How old runs replay once the cap is gone",
   "question": "Removing the 32-reaction cap (J0) would change the outcome of saved runs that were refused at the limit; how do saved runs still replay unchanged?",
   "blocks": "J0 and A7.",
   "resolves_with": "Argument from the run record: the refusal status is written into the run's commands, so replay must use the limit the run ran under.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument (inferred by agent, 2026-11-09, after the cold review's finding 2). Each saved run records the reaction limit it ran under; replay uses the recorded value (a record with none ran under 32), so old runs replay unchanged and new runs use the new setting. The refusal status 'reaction_limit' is written into the commands (src/world_substrate/engine.py:1056, recorded as the moment's refusal by _refuse_round, src/world_substrate/engine.py:932-957); tests/test_open_attempt.py:466-501 checks that refusal and is kept, run against the recorded limit.",
   "sources": [
    "docs/plans/ai_judge.md:323",
    "tests/test_open_attempt.py:466",
    "src/world_substrate/engine.py:1246"
   ],
   "touches": [
    "knock-on-now",
    "run-log",
    "causal-trace"
   ]
  },
  {
   "id": "Q82",
   "short": "Does Jev's chance follow the facts",
   "question": "In the sawmill example, does Jev's chance that the blade fails today rise with days since service, or is it flat or coarse? The existing probe's chance answers were coarse (0.6, 0.55) and its choice probabilities were 0 or 1 (evidence/jev/maintenance-estimator-probe-v0.json).",
   "blocks": "Whether a chance roll on Jev gives a believable world in E1 (A1), and whether picks (E3) collapse to a certainty.",
   "resolves_with": "Audit 2026-11-12: First state the scenario failure mechanism: monotonicity is not universally required and proves neither calibration nor believability. A targeted backend probe establishes sensitivity on its inputs only. Do not tune until probabilities look plausible and call that validation.",
   "classification": "empirical_evidence",
   "dependencies": [
    "Q83",
    "estimate-rules E1"
   ],
   "revisit_trigger": "When a specific failure mechanism and reference class require selecting or validating an estimator backend.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:483",
    "evidence/jev/maintenance-estimator-probe-v0.json"
   ],
   "touches": [
    "estimate-rule",
    "estimator"
   ]
  },
  {
   "id": "Q83",
   "short": "Do the declared reads leave out facts Jev needs",
   "question": "Jev sees only the fields an estimate rule declares (days since service, load), never the whole world: argument settles that (a whole-world read makes the cache key the whole world and can reach what A5 forbids). Do the sawmill rule's two declared reads leave out facts Jev needs, and which causal dependencies and interventions justify the read set? Comparisons with the plain version can reveal sensitivity, not prove sufficiency.",
   "blocks": "Which fields the E1 sawmill rule declares, and from E2 a rules-check warning when a rule reads too little; not the declared-reads design.",
   "resolves_with": "Design resolved: declare varying reads plus fixed model context, applicability and interventions. The two E1 fields are selected only within the explicit homogeneous-blade approximation; no general sufficiency or calibration claim is made. E1/A5 retain enforcement and input-trace checks; Q82 retains backend adequacy.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/plans/estimate_rules.md",
    "docs/model/modeling-choices.md"
   ],
   "touches": [
    "estimate-rule",
    "estimator"
   ],
   "evidence": "The Q83 contract in docs/plans/estimate_rules.md fixes dependency selection by mechanism and intervention counterexamples. Omitted causes must be fixed, explicitly marginalized, represented as persistent latent state, or added as inputs. A wider-context model comparison is optional diagnostic evidence only for a named residual decision. This closes the declared-model design choice, not real-world adequacy."
  },
  {
   "id": "Q84",
   "short": "A chance that someone notices",
   "question": "How should a chance decide whether an observation reaches a person (the harbourmaster noticing a hand-over), given that information delivery is not a field write?",
   "blocks": "Slice E5 and the port part of A5.",
   "resolves_with": "Design resolved: recipient-specific sensory availability is a committed delivery transition with stable exposure identity, shared causes and no actor-facing leaks. It never assigns belief or response. E5/A5 retain implementation and scenario-adequacy evidence.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/plans/estimate_rules.md",
    "docs/model/modeling-choices.md"
   ],
   "touches": [
    "estimate-rule",
    "information",
    "resident"
   ],
   "evidence": "The Q84 contract in docs/plans/estimate_rules.md chooses delivery after the source event, before actor observation, using the existing information/delivery seam. Repeated exposure queries reuse one disposition; failed delivery leaks neither content nor a negative observation. The actor retains interpretation and response. No runtime implementation or perception calibration is claimed."
  },
  {
   "id": "Q85",
   "short": "Jev latency in worlds with many chances",
   "question": "Successful Jev calls averaged 0.43 s, but 6.6% failed (network failures after 20.2 s on average), measured in ~/projects/data/llm_observability.db, 2026-11-10. A proposed 5 s timeout and one retry yielded a worked-out conditional estimate of about 0.61 s on average and at most 10 s, about 18 s for a 30-day sawmill run; the deployed LLM_CLIENT_TIMEOUT_POLICY=ban does not establish that timeout guarantee, so these are not demonstrated bounds; a world with many estimate rules could ask thousands of times. Does sequential asking fit the run-time targets?",
   "blocks": "Worlds with many estimate rules after E1; not E1 itself.",
   "resolves_with": "Audit 2026-11-12: Derive workload, cache misses, critical path, concurrency, quotas and memory first. One sawmill run cannot settle thousands-of-estimates performance. Measure a stated workload envelope including tails/saturation; parallelize only causally independent work.",
   "classification": "empirical_evidence",
   "dependencies": [
    "estimate-rules E1",
    "deployment timeout policy"
   ],
   "revisit_trigger": "When a concrete workload envelope and enforceable timeout policy exist; measure tails, failure behavior and saturation.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:312"
   ],
   "touches": [
    "estimator",
    "run-loop"
   ]
  },
  {
   "id": "Q86",
   "short": "Jev for the plain-words stopping point",
   "question": "The judge plan's J5 assesses a plain-words stopping point after every completed round; skipping requires a proven complete unchanged dependency set. Its illustrative judge-call cost is computed at about $0.0016 (15,000 input tokens x $0.10/M plus 150 output x $0.50/M, no cache). Jev costs on this exact workload are unmeasured; the historical roughly 1/50 comparison transfers a different per-call workload and is a guess. Should J5 use Jev?",
   "blocks": "Nothing in the estimate-rules plan; an option for the judge plan's J5.",
   "resolves_with": "Audit 2026-11-12: Retain adopted J5 assessment until substitution has a concrete justification. Stopping assesses an existing fact; do not sample confidence as a world event. Jev adequacy/cost need evidence on the same stopping questions and do not block estimate rules.",
   "classification": "optional_substitution",
   "dependencies": [
    "AI-judge J5"
   ],
   "revisit_trigger": "When the adopted stopping assessor has a concrete cost/latency/adequacy limitation that a replacement could address.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:448",
    "docs/plans/ai_judge.md:265"
   ],
   "touches": [
    "stopping-point",
    "estimator"
   ]
  },
  {
   "id": "Q87",
   "short": "What the free test run does with a chance",
   "question": "The World Builder's free scripted test run scores each draft's rules over a fixed number of rounds and is a gate because it is free and repeatable. When a draft has an estimate rule, does that run call Jev (paid, and different on each try), use the rule's fallback, or use a stand-in? And is a run's Jev spend counted against the daily allowance?",
   "blocks": "E2 (the rules writer's estimate rules pass through the test run) and A4.",
   "resolves_with": "Argument from the test run's purpose and the budget code.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument (inferred by agent, 2026-11-10, after the estimate-rules cold review's finding 3). In the scripted test run (run_world(..., policy='scripted'), scripts/world_builder_service.py:1845 and :2215) the estimator is a stand-in that never calls Jev: for each rule it answers 1 and 0 in turn (for a pick or an amount, each option in turn), so every outcome branch runs, the score stays free and repeatable, and each answer is recorded as 'stand-in estimate (test run)'. Jev would make the gate paid and nondeterministic; the fallback would test one branch only, or refuse every moment when it is 'refuse'. Spend: a live run's Jev calls carry the run's own trace id, so the cost the service already settles into its daily ledger from that trace (_trace_cost, scripts/world_builder_service.py:297; _reserve_daily_budget and _settle_daily_budget, :225-238) includes them, about $0.0009 per 30-day sawmill run; the ledger code is unchanged.",
   "sources": [
    "docs/plans/estimate_rules.md:334",
    "docs/plans/estimate_rules.md:343",
    "scripts/world_builder_service.py:1845",
    "scripts/world_builder_service.py:225"
   ],
   "touches": [
    "estimator",
    "test-run",
    "budget"
   ]
  },
  {
   "id": "Q88",
   "short": "Do declared chances match Jev's",
   "question": "A rule can carry declared bands instead of an estimate: its checks choose among literal chances the rules writer writes (for the sawmill, under 5 days since service 0.05, 5 to 9 days 0.2, 10 or more 0.4), with no Jev call and no new code. Historical diagnostic proposal: on 10 sawmill cases, do authored bands give chances within 0.1 of Jev on at least 8? Such agreement would not establish adequacy or interchangeability; first justify the piecewise mechanism, applicability and preserved intervention responses. Run a comparison only if a named residual substitution decision needs it.",
   "blocks": "Whether E2's rules-writer instructions prefer declared bands for a chance that depends on one or two facts, keeping Jev for the rest; not E1.",
   "resolves_with": "Audit 2026-11-12: Justify surrogate applicability, dependencies, thresholds and intervention responses first. Ten matching cases or flat Jev outputs establish neither interchangeability nor correctness. Bands are justified analytically when the stipulated mechanism is piecewise; otherwise adequacy stays unresolved.",
   "classification": "optional_substitution",
   "dependencies": [
    "Q83"
   ],
   "revisit_trigger": "When a piecewise mechanism or reuse workload gives a concrete reason to substitute bands; inspect applicability and intervention preservation first.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:430",
    "docs/plans/estimate_rules.md:495"
   ],
   "touches": [
    "estimate-rule",
    "estimator",
    "gen-rules"
   ]
  },
  {
   "id": "Q89",
   "short": "Are estimate rules inside Decision 006",
   "question": "An estimate rule puts a seeded draw and an injected Jev call inside Engine.apply's commit. Decision 006 forbids engine, scheduler or cognition capability of World Substrate's own and sends 'stochastic activation or parameter sweeps' to Mesa. Q27 held that whether new control flow in engine.py is that forbidden capability is Brian's call, not settled by agent argument; he allowed the same-moment fixpoint as rule semantics (Decision 009). Does an estimate rule need a ruling of its own?",
   "blocks": "Slice E1 (the estimate inside the commit) if the answer were that it is forbidden engine capability.",
   "resolves_with": "Argument from Decision 006's wording, Decision 009's ruling and the skill roll the open-attempt plan already put in the engine.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument (inferred by agent, 2026-11-10, after the estimate-rules cold review's note N5). No new ruling is needed, for four reasons. (1) Decision 006's 'stochastic activation' is about who acts and when (Mesa's random activation order); an estimate rule changes neither: processes still run when the run loop runs them and people still act in their own turns. (2) It adds no loop, clock or scheduler: inside one existing commit, one rule's outcome branch is chosen by a recorded value, as a check already chooses between a rule's outcome and its 'otherwise'; that is the same kind of rule semantics Decision 009 allowed, and less control flow than the fixpoint it allowed. (3) The open-attempt plan already puts a seeded draw in the engine (the skill roll, seed = hash(run_seed, event_id), Q33); the estimate shares that draw and its record and adds one injected input, the chance, recorded as event evidence like the dice (the Q63 contract). (4) The Jev call is not cognition: it never decides what a person does (requirement R5); people's choices stay with the Concordia residents. Brian asked for this feature on 2026-11-10 (rules and constraints that propagate based on Jev) and approved planning it. Q27 differs because the fixpoint's question was new control flow in the engine with no precedent; here Decision 009 is the precedent. If Brian reads Decision 006 more strictly, the fallback is to host the draw in Concordia's game master outside the commit, which would split a rule's outcome from its knock-on effects; he can reopen this question.",
   "sources": [
    "docs/decisions/006-governed-rules-layer-scope.md:25",
    "docs/decisions/009-same-moment-knock-on-effects.md:26",
    "docs/plans/open_attempt.md:192",
    "docs/plans/estimate_rules.md:315",
    "docs/plans/estimate_rules.md:530"
   ],
   "touches": [
    "estimate-rule",
    "engine",
    "knock-on-now"
   ]
  },
  {
   "id": "Q90",
   "short": "Reuse or replace the spike's mid-run rule writing",
   "question": "This repository's own game master already writes general rules mid-run for attempts no rule covers (spikes/any-scenario-2026-10/midrun.py, Decision 007, ODD 8.19; 27 rules in two saved runs, about $0.10 per attempt). Does J3 reuse its install step and keep-or-drop record, and what do its 27 rules show (general rules or one-offs, and how many pass today's rules check)?",
   "blocks": "J3's install path and the plan's cost basis; not J2, which is built on Concordia's EventResolution and does not use the spike's rule writer.",
   "resolves_with": "A free read of rules_written_mid_run in the two summary.json files (spikes/any-scenario-2026-10/evidence/waltzman/run, .../waltzman-spec/run2/run) and of midrun.py's install step before J3 starts; the 27 rules run through the current rules check as a free replay.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Read 2026-11-10 (J3). The spike's _install (midrun.py) registers a compiled action in the running registry (engine.registry.register_action) for each declared action not already there; J3 reuses that one step (scripts/rulings.py Rulebook.install, after the World Builder's rules check on the world as it is now, plus updating the world's recorded rule versions) and does not reuse the spike's rule writer or its keep-or-drop check. rules_written_mid_run holds 27 attempts: 3 in waltzman/run (all status ruling, written_mid_run false, nothing installed) and 24 in waltzman-spec/run2 (18 ruling, 6 invalid_action with a rule installed): 6 of 27 installed, 21 dropped by the spike's check (baseline_blocking against blocking findings). Not done: running the 27 rules through today's rules check as a free replay; they are written for the spike's worlds and the question of how many pass is not what J3 needs.",
   "sources": [
    "docs/decisions/007-any-scenario-path.md",
    "docs/model/ODD.md",
    "docs/plans/ai_judge.md",
    "spikes/any-scenario-2026-10/midrun.py"
   ],
   "touches": [
    "judge-ruling",
    "midrun-setting"
   ]
  },
  {
   "id": "Q91",
   "short": "Do configured resolution steps break 'no judge prompt of our own'",
   "question": "R7 makes the judge Concordia's EventResolution with no judge prompt of our own, but a typed rule, a pass 2 review and a reached-or-not answer need thinking steps we write. Does passing our own event_resolution_steps and components to EventResolution count as conditioning the game master, or as a judge prompt of our own?",
   "blocks": "J2's build and J5's stopping-point question.",
   "resolves_with": "Reading Concordia 2.4.0's event_resolution.py for what the steps and components may supply, then whether that meets R7.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Read 2026-11-10 (gdm-concordia 2.4.0, concordia/components/game_master/event_resolution.py, __init__ and pre_act): EventResolution takes event_resolution_steps (a sequence of callables over the interactive document, the premise and the active player's name) and a list of component keys whose pre-act text it adds to the document; the putative event is read from the game master's memory. That is its documented extension point. J2 (scripts/judge.py) runs EventResolution on an entity built from Concordia's stock parts, supplies two components (the world; the consequence report) and steps that each ask one typed question whose answer is a rule in the declaration language (prompts/judge_steps.yaml). So there is no judge agent or component of ours, but the question text is our own words; read as configuration. Inferred by agent; Brian may read Decision 006 differently, and then the steps are what to cut. Measured effect on the saved port run: evidence/ai-judge/j2/port/TRACE_READ.md.",
   "sources": [
    "docs/plans/ai_judge.md",
    "docs/decisions/006-governed-rules-layer-scope.md"
   ],
   "touches": [
    "judge-ruling"
   ]
  },
  {
   "id": "Q92",
   "short": "A ruling can move goods at a price far from the world's price and nothing flags it",
   "question": "The J2 cold review (docs/planning/ai-judge/cold-review.md, item 7) found the sawmill ruling moved 3 logs for 1 coin against a world price of 10 and nothing flagged it. Since J3 a confirmed ruling like that is installed (or held) as a rule. In 18 live tries on the lumberyard world (tests/judge_worlds.py lumberyard; run on the J3 branch before it shipped) the judge wrote rules with literal totals or a free payment field that pass the rules check and the test run but do not tie the payment to the posted price. Should the rules check or the judge's review compare what a ruling moves with the prices the world states, and which of the two catches it?",
   "blocks": "Trust in installed rulings that move goods or coins; not the J3 mechanism, which installs only what passed the rules check and the test run.",
   "resolves_with": "Audit 2026-11-12: Distinguish posted price, negotiated offer, agreed consideration and mandatory pricing. Below-list-price transfers are not automatically wrong. Where the world requires price times quantity, preserve that contract or disclose unsupported arithmetic. Inspect saved rulings against that requirement; Q96 separately owns consent. Approval is not mathematical fidelity.",
   "classification": "implementation_gap",
   "dependencies": [
    "scenario pricing contract",
    "Q96"
   ],
   "revisit_trigger": "When judging/reviewing exchange arithmetic is changed; inspect saved mandatory-price failures separately from negotiation.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/ai-judge/cold-review.md",
    "docs/plans/ai_judge.md",
    "evidence/ai-judge/j2/sawmill/TRACE_READ.md"
   ],
   "touches": [
    "judge-ruling",
    "ruling-rule"
   ]
  },
  {
   "id": "Q93",
   "short": "The language gap never happened on price times quantity",
   "question": "The plan expected a price-times-quantity ruling to be refused as 'no rule could express this' because the rule language has no multiplication. In 19 paid tries on the lumberyard world (18 on a local service, 1 on the live service on 2026-11-11, evidence/ai-judge/j3/price-times-quantity) the judge never wrote a rule the rules check rejected: it wrote literal numbers or a free payment parameter, or withdrew, or said no rule was needed. The language-gap path works (tests/test_judge_rulings.py with a scripted judge) but has no live example. Is a gap rarer than the plan assumed, does A4's third case need a world where no literal can stand in for the arithmetic, or should a withdrawal that names the missing arithmetic count as a gap?",
   "blocks": "A4's third case (a ruling the language cannot express listed as a language gap) as a live saved run.",
   "resolves_with": "Audit 2026-11-12: Separate deterministic language-gap handling from how often a live model identifies gaps. A scripted case proves the path only; literal substitution may express an instance but not a general rule. Read existing attempts first; no repeated paid search for an illustrative failure. Preserve explicit live criteria as unmet unless authorized to change them.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "Q92"
   ],
   "revisit_trigger": "When existing live attempts are reviewed for arithmetic expressibility, or a concrete new consumer needs the language-gap path.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/ai_judge.md",
    "docs/planning/ai-judge/acceptance-criteria.json"
   ],
   "touches": [
    "ruling-rule"
   ]
  },
  {
   "id": "Q94",
   "short": "A later offer joins an installed rule only when the judge wrote the giver's move (waits on Q96)",
   "question": "The plan's example rule is the giver's move ('a person may hand coins they hold to a person at the same place'). In live runs the judge wrote either that (hand-over-coins: a second trader's later offer was decided by the rule with the judge not asked) or the receiver's acceptance (accept-coin-offer: a second trader's later offer was read as unmatched and the judge was asked again, producing a second near-duplicate rule). The live J3 runs (2026-11-11) showed both shapes are defective as rules (Q96): the giver's move settles without the receiver choosing, the receiver's move lets anyone take coins nobody offered. So this question now waits on Q96: once a two-person exchange has a sound rule shape, check that a second offer is read against it.",
   "blocks": "How reliably A4's 'decided by rule, judge not asked' shows on a second trader (the cold review's item 8 saw the same split).",
   "resolves_with": "Audit 2026-11-12: Waits on Q96. Then inspect the second offer's interpretation and bound offer/response state for reuse without another ruling. Generic giver-rule reuse is not success if consent or exact terms disappear.",
   "classification": "acceptance_evidence",
   "dependencies": [
    "Q96"
   ],
   "revisit_trigger": "After exact-offer consent is implemented; inspect a second offer using the installed rule without losing parties or terms.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/ai-judge/cold-review.md",
    "docs/plans/ai_judge.md"
   ],
   "touches": [
    "judge-ruling",
    "ruling-rule"
   ]
  },
  {
   "id": "Q95",
   "short": "The engine's own replay of a run that installed a rule mid-round",
   "question": "Engine.replay of a round that installs a rule mid-round fails because the world's recorded rule versions change when the rule is installed. The live path never calls it (a shared run replays from its recorded rounds, and each round continues from a sealed snapshot with the installed rules sealed beside it), so no saved run is affected. Does anything need the engine to replay a run that installed rulings, and if so should the event log record the install?",
   "blocks": "Nothing that exists; any future audit or export that replays a judged run through Engine.replay.",
   "resolves_with": "Audit 2026-11-12: Defer expansion absent a current consumer: live runs restore sealed snapshots/rulings, not Engine.replay of judged runs. Preserve rule/install provenance. If an audit/export needs command replay, include installs and demonstrate that contract; never equate projection replay with it.",
   "classification": "deferred_requirement",
   "dependencies": [],
   "revisit_trigger": "When an actual audit/export consumer needs command replay across mid-round rule installation.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/engine.py",
    "scripts/rulings.py"
   ],
   "touches": [
    "ruling-rule"
   ]
  },
  {
   "id": "Q96",
   "short": "An installed coin rule lets a person take another's coins with no offer from them",
   "question": "In the live wait-approve run (evidence/ai-judge/j3/wait-approve, share F_ND9bo29lvp) the judge wrote the receiver's move, accept-coin-handover (the actor takes coins from a named trader at the same place), the review confirmed it and the owner approved it. Nothing in the world records an offer, so once installed the move was listed to everyone against every trader, and in round 4 Ines took 10 coins from Vik, who had offered nothing (r4-e00001). The other shape fails the other way: the giver's move hand-over-coins (evidence/ai-judge/j3/install-default) moves coins into the receiver's purse without the receiver choosing, though its ruling says it 'settles only if Rosa accepts'. In the 5 live tries where the judge ruled on Vik's offer and Ines's handover (default tries 1 to 3, wait tries hold-1 and hold-2), it wrote the receiver shape 4 times: the review withdrew it 3 times for this reason and confirmed it once (hold-2). How should a ruling that needs two people's choices become a rule: should a move that takes from someone other than the actor be offered only in answer to that person's routed attempt, should the rule language gain an offer, or should the judge be steered to the giver's move and the receiver's choice dropped?",
   "blocks": "Trust in installed rulings that move another person's goods or coins (A4, A5); not the install, hold, approve and reject mechanism itself.",
   "resolves_with": "Design selected 2026-11-12 in docs/plans/ai_judge.md, Q96 design contract: typed offers in the sealed run continuation, immutable parties/terms, explicit actor assent, expiry/withdrawal, rule-fingerprint binding and atomic settlement/consumption. This settles record/lifecycle design; the defect remains until implemented. Audit 2026-11-12: Require acceptance bound to a live offer, giver, recipient, amount and validity, then consume/expire it. Routed state suffices only if bindings survive discovery, delayed approval and replay; a routed prompt alone does not. Keep implementation open until unoffered/stale/reused taking fails and the actual offer succeeds, then inspect one bounded live interaction.",
   "classification": "implementation_defect",
   "dependencies": [
    "AI-judge Q96 offer lifecycle"
   ],
   "revisit_trigger": "Before J5 or any voluntary-exchange fidelity claim; check absent, stale, altered and reused offers plus a valid settlement.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "evidence/ai-judge/j3/wait-approve/TRACE_READ.md",
    "evidence/ai-judge/j3/install-default/TRACE_READ.md",
    "scripts/rulings.py"
   ],
   "touches": [
    "offer",
    "judge-ruling",
    "ruling-rule"
   ]
  }
 ],
 "domain": {
  "schema": "typed-graph/v1",
  "kinds": {
   "Substrate": {
    "label": "Substrate code (every world)",
    "color": "#1f4e79",
    "explain": "Fixed code every world runs through: the Engine, compiler, run loop, service, records."
   },
   "Family": {
    "label": "Fixed people-world part",
    "color": "#3b6fa8",
    "explain": "Reusable compiled people-world parts; the scenario explicitly chooses the legacy decision family or the independent validation/assent procedure. Not every family applies to every world."
   },
   "PerWorld": {
    "label": "Written per world by an AI",
    "color": "#d9822b",
    "explain": "Not code: an AI writes it for each described world during the build."
   },
   "Reference": {
    "label": "Reference worlds code only",
    "color": "#7a8491",
    "explain": "Hand-written code for the reference worlds (Kitchen, Waltzman and others); no generated world uses it today."
   },
   "Theory": {
    "label": "In documents only",
    "color": "#8a8a8a",
    "dashed": true,
    "explain": "Named in decisions or the roadmap, not on the live path."
   }
  },
  "nodes": [
   {
    "id": "world",
    "label": "World",
    "kind": "Substrate",
    "explain": "The one canonical world during a run: entities with typed components, a tick and a revision. Code: src/world_substrate/model.py:424."
   },
   {
    "id": "engine",
    "label": "Engine",
    "kind": "Substrate",
    "explain": "Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. Code: src/world_substrate/engine.py:222."
   },
   {
    "id": "event",
    "label": "Event",
    "kind": "Substrate",
    "explain": "The record of one attempt or process step: status, checks, changes, an id like r14-e00012. Code: src/world_substrate/engine.py:572."
   },
   {
    "id": "move",
    "label": "Move (action)",
    "kind": "Substrate",
    "explain": "Something a person may try; its rule has checks and effects, compiled before use. Code: src/world_substrate/action_authoring.py:50."
   },
   {
    "id": "process",
    "label": "Process",
    "kind": "Substrate",
    "explain": "A rule the world runs by itself when its checks hold: each round by default, or at once as a knock-on effect when marked immediately. Code: src/world_substrate/engine.py:1095."
   },
   {
    "id": "compiler",
    "label": "Compiler",
    "kind": "Substrate",
    "explain": "Turns proposed rules into installed rules and derives what each may read and write. Code: src/world_substrate/action_authoring.py:440."
   },
   {
    "id": "policy",
    "label": "Policy",
    "kind": "Substrate",
    "explain": "What chooses a person's move: scripted or an AI model picks an offered move; a resident on the live path says an attempt in its own words. Installed mechanics, not its words, decide what happens. Code: src/world_substrate/policy.py:50."
   },
   {
    "id": "sense",
    "label": "Linguistic Core sense and roles",
    "kind": "Substrate",
    "explain": "The meaning and participant roles of a move kind, supplied by Linguistic Core; never its effects, quantities or timing. Code: src/world_substrate/semantic.py:15."
   },
   {
    "id": "profile",
    "label": "Frozen mechanic profile",
    "kind": "Substrate",
    "explain": "The validated, installed rules of a world, frozen under one id before any run; changing a rule means a new profile. Code: src/world_substrate/profile.py:249."
   },
   {
    "id": "write-scope",
    "label": "Declared write scope",
    "kind": "Substrate",
    "explain": "The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced. Code: src/world_substrate/engine.py:136."
   },
   {
    "id": "causal-trace",
    "label": "Causal trace",
    "kind": "Substrate",
    "explain": "The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run. Code: src/world_substrate/engine.py:572."
   },
   {
    "id": "world-kind",
    "label": "World kind",
    "kind": "Substrate",
    "explain": "Two choices a build makes first: whether the description is about people (people path) or things (causal path), and whether the world is a task, ongoing or open. Code: scripts/world_builder_service.py:121."
   },
   {
    "id": "builder",
    "label": "World Builder and its bundle",
    "kind": "Substrate",
    "explain": "The public page and service where a person describes a world, approves its rules and watches it run; a build's output is an authoring bundle. Code: scripts/world_builder_service.py."
   },
   {
    "id": "approval",
    "label": "Approval record",
    "kind": "Substrate",
    "explain": "A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. Code: scripts/world_builder_service.py:426."
   },
   {
    "id": "fingerprint",
    "label": "World fingerprint",
    "kind": "Substrate",
    "explain": "A short hash of the bundle and rules that ties builds, rounds and shares to one world. Code: scripts/world_builder_service.py:389."
   },
   {
    "id": "information",
    "label": "Information item",
    "kind": "Substrate",
    "explain": "A represented item with a source and per-recipient deliveries. The source can know it before delivery; other actors receive only authorized public or delivered exposure. Claim content does not become technical truth or assent. Code: src/world_substrate/information.py:57."
   },
   {
    "id": "run-loop",
    "label": "Run loop",
    "kind": "Substrate",
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run. Code: scripts/run_authored_world.py:700."
   },
   {
    "id": "contention",
    "label": "Lost race",
    "kind": "Substrate",
    "explain": "When an earlier move this round changed the state, an open attempt is resubmitted as is at the new revision and only its rule's checks decide it; menu paths resubmit the move if still offered, else ask once more. The refused row names the failed checks, not the event that blocked it. Code: scripts/run_authored_world.py:850."
   },
   {
    "id": "resident",
    "label": "Resident",
    "kind": "Substrate",
    "explain": "One Concordia AI agent per person: sees its brief, memory and what it can see, and answers belief, attempt (in its own words), expected effect and work; the older menu reply picks an offered move. Code: scripts/concordia_residents.py:44."
   },
   {
    "id": "task",
    "label": "Task",
    "kind": "Substrate",
    "explain": "A watched field value that takes several rounds, started by a person or the world, ended by a process: finished or failed part-way. Code: scripts/attempts.py:17."
   },
   {
    "id": "notice",
    "label": "Finished-task notice",
    "kind": "Substrate",
    "explain": "What the other people a finished task names are told, in the starter's own words about the work. Code: scripts/attempts.py:234."
   },
   {
    "id": "build",
    "label": "Build",
    "kind": "Substrate",
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score. Code: scripts/world_builder_service.py:1635."
   },
   {
    "id": "rules-retry",
    "label": "Rules retry",
    "kind": "Substrate",
    "explain": "A second rules attempt after a rejection or weak score; skipped after 80 s. Code: scripts/world_builder_service.py:110."
   },
   {
    "id": "test-run",
    "label": "Scripted test run",
    "kind": "Substrate",
    "explain": "The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. Code: scripts/world_builder_service.py:1844."
   },
   {
    "id": "run-log",
    "label": "Run log",
    "kind": "Substrate",
    "explain": "One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. Code: scripts/world_builder_service.py:542."
   },
   {
    "id": "readout",
    "label": "Readout",
    "kind": "Substrate",
    "explain": "One AI summary of a run whose every cited event id is checked against the run. Code: scripts/run_readout.py:113."
   },
   {
    "id": "scene-replay",
    "label": "Scene replay",
    "kind": "Substrate",
    "explain": "The page's round-by-round picture of a run: who did what and said what, rebuilt from the run rows; it already quotes a retry's own words. Code: scripts/render_scene_replay.py:449."
   },
   {
    "id": "share",
    "label": "Share link and replay",
    "kind": "Substrate",
    "explain": "A saved run rebuilt from the run log that a visitor replays with no AI calls. Code: scripts/world_builder_service.py:638."
   },
   {
    "id": "budget",
    "label": "Daily allowance",
    "kind": "Substrate",
    "explain": "Visitor $3/day, owner $5/day; spend fails closed. Code: scripts/world_builder_service.py:57."
   },
   {
    "id": "people-world",
    "label": "People world",
    "kind": "Family",
    "explain": "A world built from a description about people: people, information, moments and the fixed people rules. Code: scripts/people_world.py:474."
   },
   {
    "id": "communicate",
    "label": "Communicate rule",
    "kind": "Family",
    "explain": "The reviewed move that delivers an information item to its recipient. Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. Code: spikes/any-scenario-2026-10/compile_spec.py:56."
   },
   {
    "id": "moment",
    "label": "Scheduled moment",
    "kind": "Family",
    "explain": "A countdown that happens every so many rounds (a weekly meeting, a deadline). Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. Code: spikes/any-scenario-2026-10/compile_spec.py:48."
   },
   {
    "id": "work-cycle",
    "label": "Work cycle",
    "kind": "Family",
    "explain": "Each action at most once per person per cycle of at least 3 rounds. Code: spikes/any-scenario-2026-10/compile_spec.py:517."
   },
   {
    "id": "group-decision",
    "label": "Group decision",
    "kind": "Family",
    "explain": "The legacy scripted decision family with support, deadline, deployment and operating review; distinct from the independent validation/assent procedure. Its fixed support/remedy dynamics are fixture assumptions, not general persuasion. Code: spikes/any-scenario-2026-10/compile_spec.py:86."
   },
   {
    "id": "concern",
    "label": "Concern",
    "kind": "Family",
    "explain": "The legacy scripted concern record on a delivered item: open, under remedy or resolved, with answered and remedy_by. Distinct from an independent actor expressing concern without a forced support change. Code: spikes/any-scenario-2026-10/compile_spec.py:70."
   },
   {
    "id": "support",
    "label": "Support",
    "kind": "Family",
    "explain": "The legacy decision family's support record: none, full or conditional on a concern. Independent expressed stance and recorded assent use separate records instead. Code: spikes/any-scenario-2026-10/compile_spec.py:66."
   },
   {
    "id": "remedy",
    "label": "Remedy",
    "kind": "Family",
    "explain": "The legacy scripted concern-remedy task, stipulated to take 2 rounds and stoppable by the holder. It is not the independent procedure's technical repair or validation result. Code: spikes/any-scenario-2026-10/compile_spec.py:332."
   },
   {
    "id": "agenda",
    "label": "Agenda count",
    "kind": "Family",
    "explain": "group_decision.agenda_items: a bare number of matters put before the decision; an item has no content. Declared in the group-decision component and changed by the compiled put-matter-on-agenda and settle-agenda-matter rules. Code: spikes/any-scenario-2026-10/compile_spec.py:101."
   },
   {
    "id": "rollout",
    "label": "Rollout",
    "kind": "Family",
    "explain": "The deployment the world starts when the decision is authorized: 6 rounds, suspended if support falls. Its processes (authorization-withdrawn, deployment-completes, deployment-suspended, deployment-resumes, deployment-progresses) are defined in _decision_rules. Code: spikes/any-scenario-2026-10/compile_spec.py:436."
   },
   {
    "id": "review",
    "label": "Operating review",
    "kind": "Family",
    "explain": "The legacy scripted operating review every 6 rounds after deployment; may reopen each resolved concern once. Distinct from independent technical validation and build-time rules review. Code: spikes/any-scenario-2026-10/compile_spec.py:442."
   },
   {
    "id": "person",
    "label": "Person and brief",
    "kind": "PerWorld",
    "explain": "A person the spec names, with goals and beliefs, and the brief only their own resident reads. Code: spikes/any-scenario-2026-10/scenario_spec.py:41."
   },
   {
    "id": "gen-rules",
    "label": "Generated actions and rules",
    "kind": "PerWorld",
    "explain": "The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled. Code: scripts/people_world.py:251."
   },
   {
    "id": "waltzman-ref",
    "label": "Waltzman reference components",
    "kind": "Reference",
    "explain": "Trust, risk, readiness and commitment components and analyses of the hand-written Waltzman world. Code: reference_worlds/waltzman/components.py:11."
   },
   {
    "id": "harness-build",
    "label": "Build in an agent harness",
    "kind": "Theory",
    "explain": "Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it. Code: scripts/world_harness.py."
   },
   {
    "id": "law-fingerprint",
    "label": "Executable-law fingerprint",
    "kind": "Theory",
    "explain": "Roadmap hardening item: fingerprint the exact executable law and compiler version. Code: none yet."
   },
   {
    "id": "affordance",
    "label": "Affordance (offered move)",
    "kind": "Substrate",
    "explain": "A move the rules say a person can try now, with its open fields; the page a decider picks from or an attempt is read against. Code: src/world_substrate/engine.py:395."
   },
   {
    "id": "check",
    "label": "Check",
    "kind": "Substrate",
    "explain": "One condition on a move or process (actual versus required); a move commits only when every check holds, else the event records which failed. Code: src/world_substrate/rules.py:48."
   },
   {
    "id": "attempt",
    "label": "Attempt (in own words)",
    "kind": "Substrate",
    "explain": "What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens. Code: src/world_substrate/attempt.py:221."
   },
   {
    "id": "attempt-reading",
    "label": "Attempt reading",
    "kind": "Substrate",
    "explain": "The interpreter's typed reading of the whole attempt: one operation kind and quoted field rows, or wait; fresh readings include a quoted coverage assessment. Invalid/incomplete/unread assessments are interpretation rejections with safe clarification and no partial action, judge or request delivery. Complete unsupported operations remain missing-rule cases; historical absent assessments remain unassessed. Coverage is model evidence, not proof of semantic truth. Code: src/world_substrate/attempt.py:92."
   },
   {
    "id": "unmatched-attempt",
    "label": "Unmatched attempt",
    "kind": "Substrate",
    "explain": "An attempt no move kind covers: it changes nothing, the person learns nothing came of it, and the run lists it for the rules writer. Code: src/world_substrate/attempt.py:34."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Substrate",
    "explain": "What one actor is supplied this round. Declared actor-information worlds use explicit grants and their own retained context; historical legacy-unrestricted worlds lack that complete boundary. Engine co-location and item filtering alone do not establish secrecy. Code: src/world_substrate/engine.py:278."
   },
   {
    "id": "place-way",
    "label": "Place and way",
    "kind": "PerWorld",
    "explain": "Where things are, and what lies between two places (a door, a brick wall) with whether it is passable; written per world as entities from the bundle contract, and the move rule checks the way. Code: scripts/generate_world_bundle.py:96."
   },
   {
    "id": "knock-on-now",
    "label": "Knock-on that runs now",
    "kind": "Substrate",
    "explain": "A process marked 'immediately' runs in waves inside the same moment as the attempt or round step that set it off, until nothing more is due (a glass falls, breaks, the water spills, the neighbour hears it); each pair of process and thing fires once per moment, which is what ends every chain; new runs have no other cap (J0 of the AI judge plan), a step a failed check stops is recorded with its blocker, and a run recorded before J0 replays under its old cap of 32. Code: src/world_substrate/engine.py:964."
   },
   {
    "id": "skill-roll",
    "label": "Skill roll",
    "kind": "Theory",
    "explain": "Plan S3: a move's outcome depends on a seeded, recorded roll against the person's skill, so someone untrained who flies a helicopter can crash it. Code: none yet."
   },
   {
    "id": "projection",
    "label": "Living projection",
    "kind": "Substrate",
    "explain": "The read-only living client, JSON and server-sent events rebuilt from canonical snapshots and events; it never changes the world. Code: src/world_substrate/projection.py:44."
   },
   {
    "id": "causal-parent",
    "label": "Hard causal parent",
    "kind": "Substrate",
    "explain": "An earlier event a rule declares as mechanically supporting this one; kept apart from the information a person merely had in mind. Code: src/world_substrate/rules.py:383."
   },
   {
    "id": "exchange",
    "label": "Derived exchange",
    "kind": "Substrate",
    "explain": "A composite reading (two give events make one exchange) derived from committed events, never a second effect. Code: src/world_substrate/exchange.py:68."
   },
   {
    "id": "mechanisms",
    "label": "Mechanisms library",
    "kind": "Reference",
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:71, Q28). Code: src/world_substrate/mechanisms/__init__.py:3."
   },
   {
    "id": "kitchen",
    "label": "Kitchen flagship",
    "kind": "Reference",
    "explain": "The replicated scarce-knife watched world: hand-written rules of its own on the ordinary Engine. Code: reference_worlds/kitchen/mechanics.py."
   },
   {
    "id": "mechanic",
    "label": "Installed mechanic",
    "kind": "Substrate",
    "explain": "One installed action rule: an action kind's selector, checks, effects and derived reads and writes, compiled and frozen in the profile; the root rule says installed mechanics alone decide what happens. Code: src/world_substrate/action_authoring.py:515."
   },
   {
    "id": "entity-component",
    "label": "Entity and component",
    "kind": "Substrate",
    "explain": "An entity is one thing in the world (person, wall, glass, decision) with an id, a label, categories and typed components; a component is a named record of typed fields (boundary.passable, group_decision.status) that checks read and effects write. Code: src/world_substrate/model.py:247."
   },
   {
    "id": "run-seed",
    "label": "Run seed",
    "kind": "Theory",
    "explain": "Plan S3: one seed drawn when a run starts and recorded in the run record; each roll's dice come from hash(run seed, event id) and are recorded, so a replay reads the dice and never rolls (Q33). Code: none yet."
   },
   {
    "id": "world-law",
    "label": "Declared world law",
    "kind": "PerWorld",
    "explain": "Plan declared-laws S1 (built): a law the AI writes when it designs a world, in that world's own terms: a resource whose total only named moves may change (pencils are made only by the factory's make move), or a move meaning such as 'a purchase moves goods one way and payment the other'. Never a fixed list of move types. The bundle validator checks each law's shape; the rules writer is given the laws and told to keep them; the engine keeps them at every commit (S2, built). Code: scripts/scaffold_world.py:45."
   },
   {
    "id": "law-check",
    "label": "Law check",
    "kind": "Substrate",
    "explain": "Plan declared-laws S2 (built): inside the same commit as the write-scope check, every move, round process and knock-on effect is checked against the world's declared laws; a breach refuses the whole step or moment as law_breach and names the law, and nothing changes. A test-run breach is a build finding sent to the rules writer and the world designer. Code: src/world_substrate/laws.py:36."
   },
   {
    "id": "world-design",
    "label": "World design (bundle)",
    "kind": "Substrate",
    "explain": "The build's first AI step: it reads the description and writes the world's people, places, things and starting state as an authoring bundle; plan declared-laws S1 adds the world's resources and laws to its output, and the rules writer receives them as input. Code: scripts/generate_world_bundle.py:53."
   },
   {
    "id": "resource",
    "label": "Declared resource",
    "kind": "PerWorld",
    "explain": "Plan declared-laws S1 (Q47, built): something the world keeps track of (cash, pencils), declared once with every field it is kept in on different entities (the customer's cash, the shop's business.cash); laws name resources, never raw fields. Each kept_in place must be a numeric field. Code: scripts/scaffold_world.py:45."
   },
   {
    "id": "rules-review",
    "label": "Independent rules review",
    "kind": "Substrate",
    "explain": "A separate source-grounded model call reviews proposed rules on both build paths. Mechanical mismatches remain findings, not a blanket pass mark. Declared actor-information worlds also require a complete typed authorization verdict for public setup and every exact initial actor context; missing, unsafe or unavailable review prevents delivery. That gate does not prove reviewer accuracy or scientific fidelity. Code: scripts/review_rules.py:75."
   },
   {
    "id": "consequence-report",
    "label": "Consequence report",
    "kind": "Substrate",
    "explain": "What the engine works out for an attempt no rule covers, in two passes (ai-judge J1, built 2026-11-10). Pass 1, with no new rule (pass_one): engine.discover for the person acting and for each person the attempt names (their moves, with which checks pass or fail), plus the current values of everyone and everything named; each run records it on every unmatched attempt (consequence.pass_one). The names come from the interpreter's reading (names). Pass 2 (pass_two): a proposed rule goes through the World Builder's rules check, then is test-run on a copy of the world as it is, giving its net changes, blockers, chain length and stopping point; the full chain stays in the report and summary() leaves it out for the judge. Code: scripts/consequence_report.py:67."
   },
   {
    "id": "judge-ruling",
    "label": "Judge ruling",
    "kind": "Substrate",
    "explain": "Plan ai-judge J2 (built 2026-11-10): Concordia's game master (EventResolution), given the whole world and pass 1 of the consequence report, proposes a rule for the constraint an unmatched attempt raises (can coins change hands here?); after reading the pass 2 test run of that rule it confirms, revises once or withdraws. Never an outcome or another person's choice. Code: scripts/judge.py:288."
   },
   {
    "id": "ruling-rule",
    "label": "Ruling-origin rule",
    "kind": "Substrate",
    "explain": "Plan ai-judge J3 (built 2026-11-10): a rule in the existing declaration language made from a confirmed judge ruling after it passes the World Builder rules check and test run, listed under its ruling, whose entry records where it came from (round, person, attempt, event id) and its state (installed, held, rejected, withdrawn when installing failed, or language gap); it applies to everyone in the same situation and the attempt settles through it. It is run state, sealed with the snapshot, beside the world's own rules (Rulebook). A ruling the language cannot express is refused and recorded as a language gap. Known defect (Q96): a coin rule written for one person's offer can move coins without the other person's choice. Code: scripts/rulings.py:91."
   },
   {
    "id": "offer",
    "label": "Voluntary exchange offer",
    "kind": "Theory",
    "explain": "Q96 design contract (planned, not implemented): a server-sealed run-continuation record binding a proposer, respondent, exact terms, rule fingerprint and lifecycle state. The respondent owns acceptance or refusal; acceptance authorizes only those terms and settlement still requires a feasible atomic Engine transition. A message or reusable ruling is not consent. Code: none yet."
   },
   {
    "id": "credential-holder",
    "label": "Credential holder",
    "kind": "Theory",
    "explain": "Plan ai-judge J4/Q76 (design settled, not implemented): credential value and verifier validity are separate from actor-scoped access, physical token custody and institutional permission. Copying can add access without removing the sender; revocation changes validity without erasing memory. Acquiring, forging or presenting a credential requires its declared mechanism. Code: none yet."
   },
   {
    "id": "norm",
    "label": "Norm",
    "kind": "Theory",
    "explain": "Plan ai-judge J4 (planned, not implemented): what people expect or forbid (bribery is illegal; only Alice should log in). It can be broken; a breach is recorded and has consequences only when someone notices and acts. Never written as a declared law. Code: none yet."
   },
   {
    "id": "midrun-setting",
    "label": "Mid-run rulings setting",
    "kind": "Substrate",
    "explain": "Plan ai-judge Decided 5 (J3, built 2026-11-10): a per-world option, 'Judge rulings during a run': Approved by Create (default; a checked ruling is installed at once and the attempt settles through it) or Wait for my approval (the proposed rule is held, the attempt waits as pending, Approve installs the rule and settles it, Reject refuses it; nothing settles without an installed rule). Code: scripts/rulings.py:47."
   },
   {
    "id": "run-stop",
    "label": "Run stop setting",
    "kind": "Substrate",
    "explain": "A per-world setting saved with the world (run_stop): stop once nothing is changing after N quiet rounds or never for being quiet, plus optional limits, a number of rounds (max_rounds) and this run's recorded AI spending (max_spend_usd); checked after each round, the run stops at whichever fires first and records why (Q12; Brian, 2026-11-10). Code: scripts/run_stop.py:65."
   },
   {
    "id": "stopping-point",
    "label": "Plain-words stopping point",
    "kind": "Theory",
    "explain": "Plan ai-judge J5 (planned, not implemented): a stopping point the person writes in plain words ('stop once the team has agreed a budget'), assessed by the judge after every completed round; skipping requires proof that the complete dependency set is unchanged, unavailable for unrestricted natural-language conditions, as one more condition of the run stop setting. Code: none yet."
   },
   {
    "id": "estimate-rule",
    "label": "Estimate rule",
    "kind": "Theory",
    "explain": "Plan estimate-rules E1 (planned, not implemented): a process or move whose outcome depends on a chance (later a pick or an amount) that Jev estimates from fields the rule declares; it declares a fixed question, its reads, the answer type, the model, a required fallback (refuse or a declared value) and the effects for each result. Code: none yet."
   },
   {
    "id": "estimator",
    "label": "Estimator",
    "kind": "Theory",
    "explain": "Plan estimate-rules E1 (planned, not implemented): what the engine asks for an estimate; live it is llm_client.call_decisions on Jev (one retry, then the rule's fallback), in a replay it reads the recorded estimates and stops with 'no recorded estimate' rather than call Jev; one call per distinct question and inputs per run. Code: none yet."
   },
   {
    "id": "recorded-estimate",
    "label": "Recorded estimate",
    "kind": "Theory",
    "explain": "Plan estimate-rules E1 (planned, not implemented): on the event, the question, the declared inputs and their values, Jev's answer, the model version returned, the trace id, the cost and whether it was reused from the run's cache; evidence, never world state (Q63). Code: none yet."
   },
   {
    "id": "recorded-draw",
    "label": "Recorded draw",
    "kind": "Theory",
    "explain": "Plans estimate-rules E1 and open-attempt S3 (planned, not implemented): a number drawn from hash(run seed, event id, rule id) and recorded on the event; an estimate rule's chance becomes an outcome only through it, and a replay reads it. Code: none yet."
   },
   {
    "id": "actor-input-boundary",
    "label": "Declared actor-input boundary",
    "kind": "Substrate",
    "explain": "The declared-v1 assembly constraining both policy paths to explicit identity/field grants, public setup and actor-owned retained context. It covers profiles, observations, offered forms, feedback and sealed continuation; legacy-unrestricted worlds retain their older inputs. This is not generic Engine read-scope enforcement. Code: scripts/actor_information.py:128."
   },
   {
    "id": "claim-provenance",
    "label": "Canonical claim provenance",
    "kind": "Family",
    "explain": "Canonical attribution of initialized information: apparent source, declared common originating-claim identity and hidden origin. In declared actor inputs, lineage is private by default and requires lineage_visible_to_actor_ids authorization as well as visible exposure. New actor-authored speech records actual sender/recipient but inherited lineage remains undeclared; repetition is not independent corroboration. Code: spikes/any-scenario-2026-10/compile_spec.py:712."
   },
   {
    "id": "technical-condition",
    "label": "Independent technical condition",
    "kind": "Family",
    "explain": "The independent procedure's represented passing/failing condition, separate from claims, exposure and validation record. An authorized explicit repair changes it; completed validation reads it. The binary effective repair is a declared bounded intervention, not validated physics. Code: spikes/any-scenario-2026-10/compile_spec.py:621."
   },
   {
    "id": "expressed-stance",
    "label": "Actor-owned expressed stance",
    "kind": "Family",
    "explain": "A public supportive, concerned, undecided or unexpressed position recorded by that actor's own action. It is distinct from private interpretation and recorded assent; receiving information does not automatically write it. Code: spikes/any-scenario-2026-10/compile_spec.py:665."
   },
   {
    "id": "recorded-assent",
    "label": "Separately recorded assent",
    "kind": "Family",
    "explain": "The required person's own recorded assent or withdrawal, kept in actor_position.assent and tallied for activation. A supportive statement, delivered report or passing validation cannot supply it. It is also distinct from the outer user's approval to run the rules. Code: spikes/any-scenario-2026-10/compile_spec.py:660."
   },
   {
    "id": "validation-hold",
    "label": "Institutional validation hold",
    "kind": "Family",
    "explain": "The independent public procedure's activation block from failed validation. Completed authorized passing revalidation clears only this hold; activation still checks recorded assents. Because failure is the stated public cause here, seeing the hold may legitimately reveal failed validation without exposing private test detail. Code: spikes/any-scenario-2026-10/compile_spec.py:685."
   }
  ],
  "edges": [
   {
    "id": "e0",
    "source": "engine",
    "target": "world",
    "label": "changes"
   },
   {
    "id": "e1",
    "source": "engine",
    "target": "event",
    "label": "writes"
   },
   {
    "id": "e2",
    "source": "move",
    "target": "engine",
    "label": "submitted to"
   },
   {
    "id": "e3",
    "source": "process",
    "target": "engine",
    "label": "run by"
   },
   {
    "id": "e4",
    "source": "compiler",
    "target": "move",
    "label": "installs"
   },
   {
    "id": "e5",
    "source": "compiler",
    "target": "process",
    "label": "installs"
   },
   {
    "id": "e6",
    "source": "approval",
    "target": "compiler",
    "label": "approves output of"
   },
   {
    "id": "e7",
    "source": "fingerprint",
    "target": "approval",
    "label": "named in"
   },
   {
    "id": "e8",
    "source": "policy",
    "target": "move",
    "label": "chooses an offered"
   },
   {
    "id": "e9",
    "source": "resident",
    "target": "policy",
    "label": "is a"
   },
   {
    "id": "e10",
    "source": "sense",
    "target": "move",
    "label": "gives meaning to"
   },
   {
    "id": "e11",
    "source": "compiler",
    "target": "profile",
    "label": "freezes"
   },
   {
    "id": "e12",
    "source": "approval",
    "target": "profile",
    "label": "names"
   },
   {
    "id": "e13",
    "source": "profile",
    "target": "write-scope",
    "label": "declares"
   },
   {
    "id": "e14",
    "source": "engine",
    "target": "write-scope",
    "label": "enforces"
   },
   {
    "id": "e15",
    "source": "event",
    "target": "causal-trace",
    "label": "makes up"
   },
   {
    "id": "e16",
    "source": "causal-trace",
    "target": "readout",
    "label": "evidence for"
   },
   {
    "id": "e17",
    "source": "builder",
    "target": "build",
    "label": "runs"
   },
   {
    "id": "e18",
    "source": "build",
    "target": "world-kind",
    "label": "decides first"
   },
   {
    "id": "e19",
    "source": "world-kind",
    "target": "people-world",
    "label": "chooses"
   },
   {
    "id": "e20",
    "source": "builder",
    "target": "share",
    "label": "serves"
   },
   {
    "id": "e21",
    "source": "run-log",
    "target": "scene-replay",
    "label": "feeds"
   },
   {
    "id": "e22",
    "source": "share",
    "target": "scene-replay",
    "label": "replays as"
   },
   {
    "id": "e23",
    "source": "run-loop",
    "target": "resident",
    "label": "asks"
   },
   {
    "id": "e24",
    "source": "run-loop",
    "target": "move",
    "label": "submits"
   },
   {
    "id": "e25",
    "source": "run-loop",
    "target": "contention",
    "label": "can produce"
   },
   {
    "id": "e26",
    "source": "resident",
    "target": "task",
    "label": "starts"
   },
   {
    "id": "e27",
    "source": "process",
    "target": "task",
    "label": "ends"
   },
   {
    "id": "e28",
    "source": "task",
    "target": "notice",
    "label": "finished, sends"
   },
   {
    "id": "e29",
    "source": "notice",
    "target": "resident",
    "label": "shown to"
   },
   {
    "id": "e30",
    "source": "build",
    "target": "test-run",
    "label": "runs"
   },
   {
    "id": "e31",
    "source": "build",
    "target": "rules-retry",
    "label": "may run"
   },
   {
    "id": "e32",
    "source": "rules-retry",
    "target": "gen-rules",
    "label": "rewrites"
   },
   {
    "id": "e33",
    "source": "test-run",
    "target": "task",
    "label": "lists long"
   },
   {
    "id": "e34",
    "source": "run-log",
    "target": "share",
    "label": "rebuilds"
   },
   {
    "id": "e35",
    "source": "run-log",
    "target": "readout",
    "label": "feeds"
   },
   {
    "id": "e36",
    "source": "budget",
    "target": "build",
    "label": "limits"
   },
   {
    "id": "e37",
    "source": "budget",
    "target": "resident",
    "label": "limits"
   },
   {
    "id": "e38",
    "source": "people-world",
    "target": "person",
    "label": "has"
   },
   {
    "id": "e39",
    "source": "people-world",
    "target": "group-decision",
    "label": "may have"
   },
   {
    "id": "e40",
    "source": "people-world",
    "target": "moment",
    "label": "has"
   },
   {
    "id": "e41",
    "source": "people-world",
    "target": "work-cycle",
    "label": "has"
   },
   {
    "id": "e42",
    "source": "people-world",
    "target": "communicate",
    "label": "has"
   },
   {
    "id": "e43",
    "source": "communicate",
    "target": "information",
    "label": "delivers"
   },
   {
    "id": "e44",
    "source": "information",
    "target": "concern",
    "label": "may carry"
   },
   {
    "id": "e45",
    "source": "concern",
    "target": "support",
    "label": "makes conditional"
   },
   {
    "id": "e46",
    "source": "support",
    "target": "group-decision",
    "label": "counts toward"
   },
   {
    "id": "e47",
    "source": "remedy",
    "target": "concern",
    "label": "resolves"
   },
   {
    "id": "e48",
    "source": "group-decision",
    "target": "agenda",
    "label": "holds"
   },
   {
    "id": "e49",
    "source": "group-decision",
    "target": "rollout",
    "label": "starts"
   },
   {
    "id": "e50",
    "source": "rollout",
    "target": "task",
    "label": "is a"
   },
   {
    "id": "e51",
    "source": "remedy",
    "target": "task",
    "label": "is a"
   },
   {
    "id": "e52",
    "source": "review",
    "target": "concern",
    "label": "may reopen"
   },
   {
    "id": "e53",
    "source": "gen-rules",
    "target": "agenda",
    "label": "may add to"
   },
   {
    "id": "e54",
    "source": "gen-rules",
    "target": "remedy",
    "label": "may stop"
   },
   {
    "id": "e55",
    "source": "person",
    "target": "resident",
    "label": "briefs"
   },
   {
    "id": "e56",
    "source": "build",
    "target": "gen-rules",
    "label": "writes"
   },
   {
    "id": "e57",
    "source": "build",
    "target": "people-world",
    "label": "builds"
   },
   {
    "id": "e58",
    "source": "harness-build",
    "target": "build",
    "label": "would replace"
   },
   {
    "id": "e59",
    "source": "waltzman-ref",
    "target": "world",
    "label": "adds components to one"
   },
   {
    "id": "e60",
    "source": "law-fingerprint",
    "target": "fingerprint",
    "label": "would extend"
   },
   {
    "id": "e61",
    "source": "engine",
    "target": "affordance",
    "label": "offers"
   },
   {
    "id": "e62",
    "source": "policy",
    "target": "affordance",
    "label": "chooses from"
   },
   {
    "id": "e63",
    "source": "move",
    "target": "check",
    "label": "requires"
   },
   {
    "id": "e64",
    "source": "resident",
    "target": "attempt",
    "label": "says"
   },
   {
    "id": "e65",
    "source": "attempt",
    "target": "attempt-reading",
    "label": "is read as"
   },
   {
    "id": "e66",
    "source": "attempt",
    "target": "unmatched-attempt",
    "label": "may be"
   },
   {
    "id": "e67",
    "source": "attempt-reading",
    "target": "move",
    "label": "names"
   },
   {
    "id": "e68",
    "source": "check",
    "target": "event",
    "label": "recorded in"
   },
   {
    "id": "e69",
    "source": "place-way",
    "target": "move",
    "label": "limits"
   },
   {
    "id": "e70",
    "source": "information",
    "target": "observation",
    "label": "filters"
   },
   {
    "id": "e71",
    "source": "observation",
    "target": "resident",
    "label": "feeds"
   },
   {
    "id": "e72",
    "source": "process",
    "target": "knock-on-now",
    "label": "extends to"
   },
   {
    "id": "e73",
    "source": "move",
    "target": "skill-roll",
    "label": "may need"
   },
   {
    "id": "e74",
    "source": "projection",
    "target": "event",
    "label": "replays"
   },
   {
    "id": "e75",
    "source": "projection",
    "target": "world",
    "label": "reads"
   },
   {
    "id": "e76",
    "source": "event",
    "target": "causal-parent",
    "label": "cites"
   },
   {
    "id": "e77",
    "source": "process",
    "target": "causal-parent",
    "label": "may declare"
   },
   {
    "id": "e78",
    "source": "knock-on-now",
    "target": "causal-parent",
    "label": "cites"
   },
   {
    "id": "e79",
    "source": "exchange",
    "target": "event",
    "label": "derived from"
   },
   {
    "id": "e80",
    "source": "kitchen",
    "target": "engine",
    "label": "runs on"
   },
   {
    "id": "e81",
    "source": "mechanisms",
    "target": "process",
    "label": "provides"
   },
   {
    "id": "e82",
    "source": "compiler",
    "target": "mechanic",
    "label": "compiles"
   },
   {
    "id": "e83",
    "source": "mechanic",
    "target": "move",
    "label": "decides each"
   },
   {
    "id": "e84",
    "source": "mechanic",
    "target": "check",
    "label": "holds"
   },
   {
    "id": "e85",
    "source": "profile",
    "target": "mechanic",
    "label": "freezes each"
   },
   {
    "id": "e86",
    "source": "world",
    "target": "entity-component",
    "label": "holds"
   },
   {
    "id": "e87",
    "source": "check",
    "target": "entity-component",
    "label": "reads"
   },
   {
    "id": "e88",
    "source": "place-way",
    "target": "entity-component",
    "label": "is an"
   },
   {
    "id": "e89",
    "source": "skill-roll",
    "target": "run-seed",
    "label": "draws dice from"
   },
   {
    "id": "e90",
    "source": "run-seed",
    "target": "causal-trace",
    "label": "recorded in"
   },
   {
    "id": "e91",
    "source": "world-law",
    "target": "entity-component",
    "label": "constrains"
   },
   {
    "id": "e92",
    "source": "world-design",
    "target": "world-law",
    "label": "declares"
   },
   {
    "id": "e93",
    "source": "world-design",
    "target": "resource",
    "label": "declares"
   },
   {
    "id": "e94",
    "source": "world-law",
    "target": "resource",
    "label": "names"
   },
   {
    "id": "e95",
    "source": "resource",
    "target": "entity-component",
    "label": "is kept in"
   },
   {
    "id": "e96",
    "source": "world-law",
    "target": "gen-rules",
    "label": "is input to"
   },
   {
    "id": "e97",
    "source": "build",
    "target": "world-design",
    "label": "runs first"
   },
   {
    "id": "e98",
    "source": "law-check",
    "target": "world-law",
    "label": "enforces"
   },
   {
    "id": "e99",
    "source": "law-check",
    "target": "mechanic",
    "label": "can refuse"
   },
   {
    "id": "e100",
    "source": "law-check",
    "target": "process",
    "label": "can refuse"
   },
   {
    "id": "e101",
    "source": "rules-review",
    "target": "gen-rules",
    "label": "sends findings to"
   },
   {
    "id": "e102",
    "source": "rules-review",
    "target": "world-law",
    "label": "reads"
   },
   {
    "id": "e103",
    "source": "rules-review",
    "target": "build",
    "label": "replaces meaning-guessing checks in"
   },
   {
    "id": "e104",
    "source": "knock-on-now",
    "target": "consequence-report",
    "label": "collected into"
   },
   {
    "id": "e105",
    "source": "consequence-report",
    "target": "unmatched-attempt",
    "label": "describes"
   },
   {
    "id": "e106",
    "source": "consequence-report",
    "target": "check",
    "label": "pass 1 lists"
   },
   {
    "id": "e107",
    "source": "consequence-report",
    "target": "test-run",
    "label": "pass 2 is a"
   },
   {
    "id": "e108",
    "source": "judge-ruling",
    "target": "consequence-report",
    "label": "reads"
   },
   {
    "id": "e109",
    "source": "judge-ruling",
    "target": "unmatched-attempt",
    "label": "decides only"
   },
   {
    "id": "e110",
    "source": "judge-ruling",
    "target": "resident",
    "label": "routes choices to"
   },
   {
    "id": "e111",
    "source": "offer",
    "target": "resident",
    "label": "respondent decides"
   },
   {
    "id": "e112",
    "source": "offer",
    "target": "ruling-rule",
    "label": "binds exact rule and terms"
   },
   {
    "id": "e113",
    "source": "offer",
    "target": "run-log",
    "label": "sealed with continuation"
   },
   {
    "id": "e114",
    "source": "offer",
    "target": "engine",
    "label": "settles atomically through"
   },
   {
    "id": "e115",
    "source": "ruling-rule",
    "target": "judge-ruling",
    "label": "made from"
   },
   {
    "id": "e116",
    "source": "rules-review",
    "target": "ruling-rule",
    "label": "checks"
   },
   {
    "id": "e117",
    "source": "ruling-rule",
    "target": "mechanic",
    "label": "is a"
   },
   {
    "id": "e118",
    "source": "midrun-setting",
    "target": "ruling-rule",
    "label": "decides when installed"
   },
   {
    "id": "e119",
    "source": "midrun-setting",
    "target": "approval",
    "label": "amends"
   },
   {
    "id": "e120",
    "source": "run-stop",
    "target": "run-loop",
    "label": "ends"
   },
   {
    "id": "e121",
    "source": "budget",
    "target": "run-stop",
    "label": "is separate from"
   },
   {
    "id": "e122",
    "source": "stopping-point",
    "target": "run-stop",
    "label": "one condition of"
   },
   {
    "id": "e123",
    "source": "judge-ruling",
    "target": "stopping-point",
    "label": "same game master assesses"
   },
   {
    "id": "e124",
    "source": "credential-holder",
    "target": "entity-component",
    "label": "is kept in"
   },
   {
    "id": "e125",
    "source": "credential-holder",
    "target": "information",
    "label": "can change by"
   },
   {
    "id": "e126",
    "source": "norm",
    "target": "world-law",
    "label": "is not a"
   },
   {
    "id": "e127",
    "source": "norm",
    "target": "observation",
    "label": "has consequences through"
   },
   {
    "id": "e128",
    "source": "estimate-rule",
    "target": "process",
    "label": "is a kind of"
   },
   {
    "id": "e129",
    "source": "estimate-rule",
    "target": "estimator",
    "label": "asks"
   },
   {
    "id": "e130",
    "source": "estimator",
    "target": "recorded-estimate",
    "label": "writes"
   },
   {
    "id": "e131",
    "source": "estimate-rule",
    "target": "recorded-draw",
    "label": "decides by"
   },
   {
    "id": "e132",
    "source": "recorded-draw",
    "target": "run-seed",
    "label": "comes from"
   },
   {
    "id": "e133",
    "source": "recorded-estimate",
    "target": "causal-trace",
    "label": "recorded in"
   },
   {
    "id": "e134",
    "source": "recorded-draw",
    "target": "causal-trace",
    "label": "recorded in"
   },
   {
    "id": "e135",
    "source": "estimate-rule",
    "target": "knock-on-now",
    "label": "sets off"
   },
   {
    "id": "e136",
    "source": "skill-roll",
    "target": "recorded-draw",
    "label": "also uses"
   },
   {
    "id": "e137",
    "source": "estimate-rule",
    "target": "resident",
    "label": "never decides for"
   },
   {
    "id": "e138",
    "source": "actor-input-boundary",
    "target": "observation",
    "label": "constrains declared inputs"
   },
   {
    "id": "e139",
    "source": "actor-input-boundary",
    "target": "resident",
    "label": "assembles authorized context for"
   },
   {
    "id": "e140",
    "source": "rules-review",
    "target": "actor-input-boundary",
    "label": "checks source-grounded initial authorization"
   },
   {
    "id": "e141",
    "source": "claim-provenance",
    "target": "information",
    "label": "attributes"
   },
   {
    "id": "e142",
    "source": "claim-provenance",
    "target": "actor-input-boundary",
    "label": "lineage requires explicit visibility grant"
   },
   {
    "id": "e143",
    "source": "claim-provenance",
    "target": "causal-trace",
    "label": "retained separately in"
   },
   {
    "id": "e144",
    "source": "technical-condition",
    "target": "entity-component",
    "label": "is stored in"
   },
   {
    "id": "e145",
    "source": "move",
    "target": "technical-condition",
    "label": "authorized explicit repair may change"
   },
   {
    "id": "e146",
    "source": "technical-condition",
    "target": "validation-hold",
    "label": "completed failed validation sets"
   },
   {
    "id": "e147",
    "source": "validation-hold",
    "target": "move",
    "label": "blocks activation until cleared"
   },
   {
    "id": "e148",
    "source": "resident",
    "target": "expressed-stance",
    "label": "may explicitly record"
   },
   {
    "id": "e149",
    "source": "resident",
    "target": "recorded-assent",
    "label": "may explicitly record or withdraw"
   },
   {
    "id": "e150",
    "source": "expressed-stance",
    "target": "recorded-assent",
    "label": "does not imply"
   },
   {
    "id": "e151",
    "source": "recorded-assent",
    "target": "move",
    "label": "required for activation"
   },
   {
    "id": "e152",
    "source": "information",
    "target": "expressed-stance",
    "label": "does not force"
   },
   {
    "id": "e153",
    "source": "information",
    "target": "recorded-assent",
    "label": "does not supply"
   },
   {
    "id": "e154",
    "source": "validation-hold",
    "target": "recorded-assent",
    "label": "clearing does not supply"
   }
  ],
  "layout": {
   "algorithm": "force"
  }
 },
 "question_map": {
  "schema": "typed-graph/v1",
  "kinds": {
   "AgentQuestion": {
    "label": "Checking can settle it",
    "color": "#3b6fa8",
    "explain": "An open question an agent can settle by reading, running or testing."
   },
   "BrianQuestion": {
    "label": "Brian's call",
    "color": "#d9822b",
    "explain": "A product or priority question; it carries a recommendation and a default."
   },
   "Concept": {
    "label": "Concept",
    "color": "#7a8491",
    "explain": "A domain-model concept; open the Domain model tab for its definition."
   }
  },
  "nodes": [
   {
    "id": "Q1",
    "label": "Q1: Rules retry never runs here",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether a world whose rules fail the part-way or liveness checks can be repaired on the live path, or only scored lower."
   },
   {
    "id": "Q3",
    "label": "Q3: Agenda item has no content",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether the group-decision family's agenda needs content or should be dropped."
   },
   {
    "id": "Q14",
    "label": "Q14: Harness build time not measured",
    "kind": "AgentQuestion",
    "explain": "Blocks: when the harness replaces the fixed build calls and the rules retry (Q1) on the live path."
   },
   {
    "id": "Q26",
    "label": "Q26: Run page hides own-words attempts",
    "kind": "AgentQuestion",
    "explain": "Blocks: the plan's inspectable result (docs/plans/open_attempt.md, Actor and result) and S1 being done."
   },
   {
    "id": "Q30",
    "label": "Q30: Build accepted with a task never possible",
    "kind": "AgentQuestion",
    "explain": "Blocks: A2 and A3 on any newly built world (they need the helicopter and the wall reachable), and whether a visitor's world can do what they described; A2 and A3 on the saved fixture tests/fixtures/airfield-s1-live.json do not wait for it."
   },
   {
    "id": "Q31",
    "label": "Q31: Refusal reason reads as a fact",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether a person, and a reader of the run, can tell why a move was refused."
   },
   {
    "id": "Q32",
    "label": "Q32: Readout picks the wrong lens",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether a run's readout describes the world the visitor wrote."
   },
   {
    "id": "Q33",
    "label": "Q33: Seeded roll versus no randomness",
    "kind": "AgentQuestion",
    "explain": "Blocks: S3's design, A7 and the full canonical run (A9)."
   },
   {
    "id": "Q34",
    "label": "Q34: Read scopes recorded, not enforced",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether causal links built from declared reads are complete: F1's blocked_by_event names the event that changed what a refused move's failed checks read, and Piece 2's reactions cite parents, so an undeclared read would leave a refusal or reaction without its true cause."
   },
   {
    "id": "Q36",
    "label": "Q36: How a misreading is caught",
    "kind": "AgentQuestion",
    "explain": "Blocks: R1 (residents can try anything), A2, and whether a TRACE_READ.md can trust readings."
   },
   {
    "id": "Q37",
    "label": "Q37: Added doorway listed as left out",
    "kind": "AgentQuestion",
    "explain": "Blocks: A3 on any newly built airfield world, and whether a visitor can see what the builder added."
   },
   {
    "id": "Q38",
    "label": "Q38: Does S1 close #128",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether #128 stays open on the board."
   },
   {
    "id": "Q45",
    "label": "Q45: Which heuristic checks retire",
    "kind": "AgentQuestion",
    "explain": "Blocks: S4: which checks are removed, and so whether validation stops growing one check per bug."
   },
   {
    "id": "Q48",
    "label": "Q48: A law that allows too much",
    "kind": "AgentQuestion",
    "explain": "Blocks: S4: whether a heuristic check whose incident is a conjured good may retire on the strength of a declared total law, when that law might itself list the conjuring move."
   },
   {
    "id": "Q49",
    "label": "Q49: A law the designer leaves out",
    "kind": "AgentQuestion",
    "explain": "Blocks: S4: Q45 retires a check when its incident's saved world is refused by a declared law; with laws left out that test can pass on worlds that still have the bug. Also A1 and A4, whose expected results include a payment law.."
   },
   {
    "id": "Q51",
    "label": "Q51: Live network with no lines",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the Network view can be trusted in a live run; issue #316.."
   },
   {
    "id": "Q52",
    "label": "Q52: Does the person asked respond",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether requests are worth more work.."
   },
   {
    "id": "Q54",
    "label": "Q54: People keep trying a closed door",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether residents see enough of the world to choose moves that can succeed; how much of a run is wasted turns.."
   },
   {
    "id": "Q55",
    "label": "Q55: A flagged world kept without a rewrite",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the shared Waltzman run (share jyVbywXT8N8F) is fit for Brian to judge under Q50, and whether the plan's S3 (review findings go to the rules writer's revision step) holds on the people-world path.."
   },
   {
    "id": "Q56",
    "label": "Q56: A rule that writes less than it declared",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a world's declared write scopes can be read as what its rules actually maintain; a generated rule that silently stops updating a field it owns goes unnoticed.."
   },
   {
    "id": "Q57",
    "label": "Q57: String fields have no declared values",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the interpreter and compiler can refuse a value outside a world's vocabulary (a dock, a route, a status) instead of accepting any string.."
   },
   {
    "id": "Q58",
    "label": "Q58: Promises beyond support (a Commitment kind)",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a people world can hold a promise one person makes another that is not support for the decision.."
   },
   {
    "id": "Q59",
    "label": "Q59: Does the people path transfer to a different situation",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether 'describe any scenario' (Decision 007) holds beyond decision-with-concerns situations; feeds Q60.."
   },
   {
    "id": "Q61",
    "label": "Q61: Outside vocabularies never evaluated",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the run log's causal fields, the derived scopes and the project's causal claims use an outside vocabulary or stay project-specific.."
   },
   {
    "id": "Q62",
    "label": "Q62: Meaning coverage beyond the six bound moves",
    "kind": "AgentQuestion",
    "explain": "Blocks: Adding any overlay term beyond the six bound M1 move kinds, and binding generated move kinds to a meaning.."
   },
   {
    "id": "Q64",
    "label": "Q64: Meaning is looked up by bare move name",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether an event's semantic_binding and mechanic id can be trusted to describe the rule that actually ran.."
   },
   {
    "id": "Q65",
    "label": "Q65: The bundle schema refuses declared laws",
    "kind": "AgentQuestion",
    "explain": "Blocks: Any outside tool or test that validates a declared-laws bundle against the published schema.."
   },
   {
    "id": "Q66",
    "label": "Q66: The read-scope status fact is a constant",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the status check is evidence about read scopes or only about the spec's text; Q34.."
   },
   {
    "id": "Q67",
    "label": "Q67: Write-path placeholders bind to any participant",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a declared write scope limits a rule to the participants it names; listed in the roadmap hardening queue.."
   },
   {
    "id": "Q68",
    "label": "Q68: No lockfile; donor check needs a missing checkout",
    "kind": "AgentQuestion",
    "explain": "Blocks: Reproducing a run's exact dependencies, and running the donor check at all.."
   },
   {
    "id": "Q69",
    "label": "Q69: Hardening: law identity, discovery cap, mechanic errors",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether an approval names one exact executable law, whether a decider ever silently misses moves, and whether a broken rule leaves a trace in the run.."
   },
   {
    "id": "Q71",
    "label": "Q71: The live build imports spike code",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether spike code is held to the live path's tests and review; whether the spike folder can be archived.."
   },
   {
    "id": "Q72",
    "label": "Q72: Living-scene profile and layout disagree on render (confirmed)",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a scene author can set the gather radius the layout documents.."
   },
   {
    "id": "Q77",
    "label": "Q77: Documentation and AES conformance gaps",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether the wiki-compliance and durable-document checks pass again for every package in this repository.."
   },
   {
    "id": "Q82",
    "label": "Q82: Does Jev's chance follow the facts",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a chance roll on Jev gives a believable world in E1 (A1), and whether picks (E3) collapse to a certainty.."
   },
   {
    "id": "Q85",
    "label": "Q85: Jev latency in worlds with many chances",
    "kind": "AgentQuestion",
    "explain": "Blocks: Worlds with many estimate rules after E1; not E1 itself.."
   },
   {
    "id": "Q86",
    "label": "Q86: Jev for the plain-words stopping point",
    "kind": "AgentQuestion",
    "explain": "Blocks: Nothing in the estimate-rules plan; an option for the judge plan's J5.."
   },
   {
    "id": "Q88",
    "label": "Q88: Do declared chances match Jev's",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether E2's rules-writer instructions prefer declared bands for a chance that depends on one or two facts, keeping Jev for the rest; not E1.."
   },
   {
    "id": "Q92",
    "label": "Q92: A ruling can move goods at a price far from the world's price and nothing flags it",
    "kind": "AgentQuestion",
    "explain": "Blocks: Trust in installed rulings that move goods or coins; not the J3 mechanism, which installs only what passed the rules check and the test run.."
   },
   {
    "id": "Q93",
    "label": "Q93: The language gap never happened on price times quantity",
    "kind": "AgentQuestion",
    "explain": "Blocks: A4's third case (a ruling the language cannot express listed as a language gap) as a live saved run.."
   },
   {
    "id": "Q94",
    "label": "Q94: A later offer joins an installed rule only when the judge wrote the giver's move (waits on Q96)",
    "kind": "AgentQuestion",
    "explain": "Blocks: How reliably A4's 'decided by rule, judge not asked' shows on a second trader (the cold review's item 8 saw the same split).."
   },
   {
    "id": "Q95",
    "label": "Q95: The engine's own replay of a run that installed a rule mid-round",
    "kind": "AgentQuestion",
    "explain": "Blocks: Nothing that exists; any future audit or export that replays a judged run through Engine.replay.."
   },
   {
    "id": "Q96",
    "label": "Q96: An installed coin rule lets a person take another's coins with no offer from them",
    "kind": "AgentQuestion",
    "explain": "Blocks: Trust in installed rulings that move another person's goods or coins (A4, A5); not the install, hold, approve and reject mechanism itself.."
   },
   {
    "id": "affordance",
    "label": "Affordance (offered move)",
    "kind": "Concept",
    "explain": "A move the rules say a person can try now, with its open fields; the page a decider picks from or an attempt is read against."
   },
   {
    "id": "agenda",
    "label": "Agenda count",
    "kind": "Concept",
    "explain": "group_decision.agenda_items: a bare number of matters put before the decision; an item has no content. Declared in the group-decision component and changed by the compiled put-matter-on-agenda and settle-agenda-matter rules."
   },
   {
    "id": "attempt",
    "label": "Attempt (in own words)",
    "kind": "Concept",
    "explain": "What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens."
   },
   {
    "id": "attempt-reading",
    "label": "Attempt reading",
    "kind": "Concept",
    "explain": "The interpreter's typed reading of the whole attempt: one operation kind and quoted field rows, or wait; fresh readings include a quoted coverage assessment. Invalid/incomplete/unread assessments are interpretation rejections with safe clarification and no partial action, judge or request delivery. Complete unsupported operations remain missing-rule cases; historical absent assessments remain unassessed. Coverage is model evidence, not proof of semantic truth."
   },
   {
    "id": "build",
    "label": "Build",
    "kind": "Concept",
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score."
   },
   {
    "id": "builder",
    "label": "World Builder and its bundle",
    "kind": "Concept",
    "explain": "The public page and service where a person describes a world, approves its rules and watches it run; a build's output is an authoring bundle."
   },
   {
    "id": "causal-parent",
    "label": "Hard causal parent",
    "kind": "Concept",
    "explain": "An earlier event a rule declares as mechanically supporting this one; kept apart from the information a person merely had in mind."
   },
   {
    "id": "causal-trace",
    "label": "Causal trace",
    "kind": "Concept",
    "explain": "The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run."
   },
   {
    "id": "check",
    "label": "Check",
    "kind": "Concept",
    "explain": "One condition on a move or process (actual versus required); a move commits only when every check holds, else the event records which failed."
   },
   {
    "id": "compiler",
    "label": "Compiler",
    "kind": "Concept",
    "explain": "Turns proposed rules into installed rules and derives what each may read and write."
   },
   {
    "id": "engine",
    "label": "Engine",
    "kind": "Concept",
    "explain": "Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick."
   },
   {
    "id": "entity-component",
    "label": "Entity and component",
    "kind": "Concept",
    "explain": "An entity is one thing in the world (person, wall, glass, decision) with an id, a label, categories and typed components; a component is a named record of typed fields (boundary.passable, group_decision.status) that checks read and effects write."
   },
   {
    "id": "estimate-rule",
    "label": "Estimate rule",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan estimate-rules E1 (planned, not implemented): a process or move whose outcome depends on a chance (later a pick or an amount) that Jev estimates from fields the rule declares; it declares a fixed question, its reads, the answer type, the model, a required fallback (refuse or a declared value) and the effects for each result."
   },
   {
    "id": "estimator",
    "label": "Estimator",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan estimate-rules E1 (planned, not implemented): what the engine asks for an estimate; live it is llm_client.call_decisions on Jev (one retry, then the rule's fallback), in a replay it reads the recorded estimates and stops with 'no recorded estimate' rather than call Jev; one call per distinct question and inputs per run."
   },
   {
    "id": "event",
    "label": "Event",
    "kind": "Concept",
    "explain": "The record of one attempt or process step: status, checks, changes, an id like r14-e00012."
   },
   {
    "id": "gen-rules",
    "label": "Generated actions and rules",
    "kind": "Concept",
    "explain": "The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled."
   },
   {
    "id": "group-decision",
    "label": "Group decision",
    "kind": "Concept",
    "explain": "The legacy scripted decision family with support, deadline, deployment and operating review; distinct from the independent validation/assent procedure. Its fixed support/remedy dynamics are fixture assumptions, not general persuasion."
   },
   {
    "id": "harness-build",
    "label": "Build in an agent harness",
    "kind": "Concept",
    "dashed": true,
    "explain": "Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it."
   },
   {
    "id": "judge-ruling",
    "label": "Judge ruling",
    "kind": "Concept",
    "explain": "Plan ai-judge J2 (built 2026-11-10): Concordia's game master (EventResolution), given the whole world and pass 1 of the consequence report, proposes a rule for the constraint an unmatched attempt raises (can coins change hands here?); after reading the pass 2 test run of that rule it confirms, revises once or withdraws. Never an outcome or another person's choice."
   },
   {
    "id": "law-check",
    "label": "Law check",
    "kind": "Concept",
    "explain": "Plan declared-laws S2 (built): inside the same commit as the write-scope check, every move, round process and knock-on effect is checked against the world's declared laws; a breach refuses the whole step or moment as law_breach and names the law, and nothing changes. A test-run breach is a build finding sent to the rules writer and the world designer."
   },
   {
    "id": "law-fingerprint",
    "label": "Executable-law fingerprint",
    "kind": "Concept",
    "dashed": true,
    "explain": "Roadmap hardening item: fingerprint the exact executable law and compiler version."
   },
   {
    "id": "mechanic",
    "label": "Installed mechanic",
    "kind": "Concept",
    "explain": "One installed action rule: an action kind's selector, checks, effects and derived reads and writes, compiled and frozen in the profile; the root rule says installed mechanics alone decide what happens."
   },
   {
    "id": "mechanisms",
    "label": "Mechanisms library",
    "kind": "Concept",
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:71, Q28)."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Concept",
    "explain": "What one actor is supplied this round. Declared actor-information worlds use explicit grants and their own retained context; historical legacy-unrestricted worlds lack that complete boundary. Engine co-location and item filtering alone do not establish secrecy."
   },
   {
    "id": "offer",
    "label": "Voluntary exchange offer",
    "kind": "Concept",
    "dashed": true,
    "explain": "Q96 design contract (planned, not implemented): a server-sealed run-continuation record binding a proposer, respondent, exact terms, rule fingerprint and lifecycle state. The respondent owns acceptance or refusal; acceptance authorizes only those terms and settlement still requires a feasible atomic Engine transition. A message or reusable ruling is not consent."
   },
   {
    "id": "people-world",
    "label": "People world",
    "kind": "Concept",
    "explain": "A world built from a description about people: people, information, moments and the fixed people rules."
   },
   {
    "id": "person",
    "label": "Person and brief",
    "kind": "Concept",
    "explain": "A person the spec names, with goals and beliefs, and the brief only their own resident reads."
   },
   {
    "id": "place-way",
    "label": "Place and way",
    "kind": "Concept",
    "explain": "Where things are, and what lies between two places (a door, a brick wall) with whether it is passable; written per world as entities from the bundle contract, and the move rule checks the way."
   },
   {
    "id": "profile",
    "label": "Frozen mechanic profile",
    "kind": "Concept",
    "explain": "The validated, installed rules of a world, frozen under one id before any run; changing a rule means a new profile."
   },
   {
    "id": "readout",
    "label": "Readout",
    "kind": "Concept",
    "explain": "One AI summary of a run whose every cited event id is checked against the run."
   },
   {
    "id": "resident",
    "label": "Resident",
    "kind": "Concept",
    "explain": "One Concordia AI agent per person: sees its brief, memory and what it can see, and answers belief, attempt (in its own words), expected effect and work; the older menu reply picks an offered move."
   },
   {
    "id": "rules-retry",
    "label": "Rules retry",
    "kind": "Concept",
    "explain": "A second rules attempt after a rejection or weak score; skipped after 80 s."
   },
   {
    "id": "rules-review",
    "label": "Independent rules review",
    "kind": "Concept",
    "explain": "A separate source-grounded model call reviews proposed rules on both build paths. Mechanical mismatches remain findings, not a blanket pass mark. Declared actor-information worlds also require a complete typed authorization verdict for public setup and every exact initial actor context; missing, unsafe or unavailable review prevents delivery. That gate does not prove reviewer accuracy or scientific fidelity."
   },
   {
    "id": "ruling-rule",
    "label": "Ruling-origin rule",
    "kind": "Concept",
    "explain": "Plan ai-judge J3 (built 2026-11-10): a rule in the existing declaration language made from a confirmed judge ruling after it passes the World Builder rules check and test run, listed under its ruling, whose entry records where it came from (round, person, attempt, event id) and its state (installed, held, rejected, withdrawn when installing failed, or language gap); it applies to everyone in the same situation and the attempt settles through it. It is run state, sealed with the snapshot, beside the world's own rules (Rulebook). A ruling the language cannot express is refused and recorded as a language gap. Known defect (Q96): a coin rule written for one person's offer can move coins without the other person's choice."
   },
   {
    "id": "run-log",
    "label": "Run log",
    "kind": "Concept",
    "explain": "One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads."
   },
   {
    "id": "run-loop",
    "label": "Run loop",
    "kind": "Concept",
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run."
   },
   {
    "id": "scene-replay",
    "label": "Scene replay",
    "kind": "Concept",
    "explain": "The page's round-by-round picture of a run: who did what and said what, rebuilt from the run rows; it already quotes a retry's own words."
   },
   {
    "id": "sense",
    "label": "Linguistic Core sense and roles",
    "kind": "Concept",
    "explain": "The meaning and participant roles of a move kind, supplied by Linguistic Core; never its effects, quantities or timing."
   },
   {
    "id": "share",
    "label": "Share link and replay",
    "kind": "Concept",
    "explain": "A saved run rebuilt from the run log that a visitor replays with no AI calls."
   },
   {
    "id": "skill-roll",
    "label": "Skill roll",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan S3: a move's outcome depends on a seeded, recorded roll against the person's skill, so someone untrained who flies a helicopter can crash it."
   },
   {
    "id": "stopping-point",
    "label": "Plain-words stopping point",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan ai-judge J5 (planned, not implemented): a stopping point the person writes in plain words ('stop once the team has agreed a budget'), assessed by the judge after every completed round; skipping requires proof that the complete dependency set is unchanged, unavailable for unrestricted natural-language conditions, as one more condition of the run stop setting."
   },
   {
    "id": "support",
    "label": "Support",
    "kind": "Concept",
    "explain": "The legacy decision family's support record: none, full or conditional on a concern. Independent expressed stance and recorded assent use separate records instead."
   },
   {
    "id": "task",
    "label": "Task",
    "kind": "Concept",
    "explain": "A watched field value that takes several rounds, started by a person or the world, ended by a process: finished or failed part-way."
   },
   {
    "id": "test-run",
    "label": "Scripted test run",
    "kind": "Concept",
    "explain": "The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way."
   },
   {
    "id": "unmatched-attempt",
    "label": "Unmatched attempt",
    "kind": "Concept",
    "explain": "An attempt no move kind covers: it changes nothing, the person learns nothing came of it, and the run lists it for the rules writer."
   },
   {
    "id": "world-design",
    "label": "World design (bundle)",
    "kind": "Concept",
    "explain": "The build's first AI step: it reads the description and writes the world's people, places, things and starting state as an authoring bundle; plan declared-laws S1 adds the world's resources and laws to its output, and the rules writer receives them as input."
   },
   {
    "id": "world-law",
    "label": "Declared world law",
    "kind": "Concept",
    "explain": "Plan declared-laws S1 (built): a law the AI writes when it designs a world, in that world's own terms: a resource whose total only named moves may change (pencils are made only by the factory's make move), or a move meaning such as 'a purchase moves goods one way and payment the other'. Never a fixed list of move types. The bundle validator checks each law's shape; the rules writer is given the laws and told to keep them; the engine keeps them at every commit (S2, built)."
   },
   {
    "id": "write-scope",
    "label": "Declared write scope",
    "kind": "Concept",
    "explain": "The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced."
   }
  ],
  "edges": [
   {
    "id": "Q1-rules-retry",
    "source": "Q1",
    "target": "rules-retry",
    "label": "bears on"
   },
   {
    "id": "Q1-test-run",
    "source": "Q1",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q1-build",
    "source": "Q1",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q3-agenda",
    "source": "Q3",
    "target": "agenda",
    "label": "bears on"
   },
   {
    "id": "Q3-group-decision",
    "source": "Q3",
    "target": "group-decision",
    "label": "bears on"
   },
   {
    "id": "Q14-harness-build",
    "source": "Q14",
    "target": "harness-build",
    "label": "bears on"
   },
   {
    "id": "Q14-build",
    "source": "Q14",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q14-rules-retry",
    "source": "Q14",
    "target": "rules-retry",
    "label": "bears on"
   },
   {
    "id": "Q26-attempt",
    "source": "Q26",
    "target": "attempt",
    "label": "bears on"
   },
   {
    "id": "Q26-unmatched-attempt",
    "source": "Q26",
    "target": "unmatched-attempt",
    "label": "bears on"
   },
   {
    "id": "Q26-run-loop",
    "source": "Q26",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q30-test-run",
    "source": "Q30",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q30-build",
    "source": "Q30",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q30-task",
    "source": "Q30",
    "target": "task",
    "label": "bears on"
   },
   {
    "id": "Q30-rules-retry",
    "source": "Q30",
    "target": "rules-retry",
    "label": "bears on"
   },
   {
    "id": "Q31-check",
    "source": "Q31",
    "target": "check",
    "label": "bears on"
   },
   {
    "id": "Q31-gen-rules",
    "source": "Q31",
    "target": "gen-rules",
    "label": "bears on"
   },
   {
    "id": "Q32-readout",
    "source": "Q32",
    "target": "readout",
    "label": "bears on"
   },
   {
    "id": "Q33-skill-roll",
    "source": "Q33",
    "target": "skill-roll",
    "label": "bears on"
   },
   {
    "id": "Q33-gen-rules",
    "source": "Q33",
    "target": "gen-rules",
    "label": "bears on"
   },
   {
    "id": "Q33-person",
    "source": "Q33",
    "target": "person",
    "label": "bears on"
   },
   {
    "id": "Q33-run-loop",
    "source": "Q33",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q33-causal-trace",
    "source": "Q33",
    "target": "causal-trace",
    "label": "bears on"
   },
   {
    "id": "Q34-write-scope",
    "source": "Q34",
    "target": "write-scope",
    "label": "bears on"
   },
   {
    "id": "Q34-causal-parent",
    "source": "Q34",
    "target": "causal-parent",
    "label": "bears on"
   },
   {
    "id": "Q34-mechanisms",
    "source": "Q34",
    "target": "mechanisms",
    "label": "bears on"
   },
   {
    "id": "Q36-attempt-reading",
    "source": "Q36",
    "target": "attempt-reading",
    "label": "bears on"
   },
   {
    "id": "Q36-unmatched-attempt",
    "source": "Q36",
    "target": "unmatched-attempt",
    "label": "bears on"
   },
   {
    "id": "Q37-place-way",
    "source": "Q37",
    "target": "place-way",
    "label": "bears on"
   },
   {
    "id": "Q37-build",
    "source": "Q37",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q37-builder",
    "source": "Q37",
    "target": "builder",
    "label": "bears on"
   },
   {
    "id": "Q38-attempt",
    "source": "Q38",
    "target": "attempt",
    "label": "bears on"
   },
   {
    "id": "Q38-task",
    "source": "Q38",
    "target": "task",
    "label": "bears on"
   },
   {
    "id": "Q38-observation",
    "source": "Q38",
    "target": "observation",
    "label": "bears on"
   },
   {
    "id": "Q45-rules-review",
    "source": "Q45",
    "target": "rules-review",
    "label": "bears on"
   },
   {
    "id": "Q45-test-run",
    "source": "Q45",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q45-build",
    "source": "Q45",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q48-world-law",
    "source": "Q48",
    "target": "world-law",
    "label": "bears on"
   },
   {
    "id": "Q48-rules-review",
    "source": "Q48",
    "target": "rules-review",
    "label": "bears on"
   },
   {
    "id": "Q49-world-law",
    "source": "Q49",
    "target": "world-law",
    "label": "bears on"
   },
   {
    "id": "Q49-rules-review",
    "source": "Q49",
    "target": "rules-review",
    "label": "bears on"
   },
   {
    "id": "Q51-share",
    "source": "Q51",
    "target": "share",
    "label": "bears on"
   },
   {
    "id": "Q51-build",
    "source": "Q51",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q52-attempt",
    "source": "Q52",
    "target": "attempt",
    "label": "bears on"
   },
   {
    "id": "Q52-resident",
    "source": "Q52",
    "target": "resident",
    "label": "bears on"
   },
   {
    "id": "Q54-resident",
    "source": "Q54",
    "target": "resident",
    "label": "bears on"
   },
   {
    "id": "Q54-attempt",
    "source": "Q54",
    "target": "attempt",
    "label": "bears on"
   },
   {
    "id": "Q55-rules-review",
    "source": "Q55",
    "target": "rules-review",
    "label": "bears on"
   },
   {
    "id": "Q55-build",
    "source": "Q55",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q55-rules-retry",
    "source": "Q55",
    "target": "rules-retry",
    "label": "bears on"
   },
   {
    "id": "Q56-write-scope",
    "source": "Q56",
    "target": "write-scope",
    "label": "bears on"
   },
   {
    "id": "Q56-law-check",
    "source": "Q56",
    "target": "law-check",
    "label": "bears on"
   },
   {
    "id": "Q56-mechanic",
    "source": "Q56",
    "target": "mechanic",
    "label": "bears on"
   },
   {
    "id": "Q57-entity-component",
    "source": "Q57",
    "target": "entity-component",
    "label": "bears on"
   },
   {
    "id": "Q57-attempt-reading",
    "source": "Q57",
    "target": "attempt-reading",
    "label": "bears on"
   },
   {
    "id": "Q57-compiler",
    "source": "Q57",
    "target": "compiler",
    "label": "bears on"
   },
   {
    "id": "Q58-support",
    "source": "Q58",
    "target": "support",
    "label": "bears on"
   },
   {
    "id": "Q58-people-world",
    "source": "Q58",
    "target": "people-world",
    "label": "bears on"
   },
   {
    "id": "Q59-people-world",
    "source": "Q59",
    "target": "people-world",
    "label": "bears on"
   },
   {
    "id": "Q59-group-decision",
    "source": "Q59",
    "target": "group-decision",
    "label": "bears on"
   },
   {
    "id": "Q59-gen-rules",
    "source": "Q59",
    "target": "gen-rules",
    "label": "bears on"
   },
   {
    "id": "Q61-causal-trace",
    "source": "Q61",
    "target": "causal-trace",
    "label": "bears on"
   },
   {
    "id": "Q61-causal-parent",
    "source": "Q61",
    "target": "causal-parent",
    "label": "bears on"
   },
   {
    "id": "Q61-write-scope",
    "source": "Q61",
    "target": "write-scope",
    "label": "bears on"
   },
   {
    "id": "Q62-sense",
    "source": "Q62",
    "target": "sense",
    "label": "bears on"
   },
   {
    "id": "Q64-sense",
    "source": "Q64",
    "target": "sense",
    "label": "bears on"
   },
   {
    "id": "Q64-mechanic",
    "source": "Q64",
    "target": "mechanic",
    "label": "bears on"
   },
   {
    "id": "Q64-event",
    "source": "Q64",
    "target": "event",
    "label": "bears on"
   },
   {
    "id": "Q65-world-design",
    "source": "Q65",
    "target": "world-design",
    "label": "bears on"
   },
   {
    "id": "Q65-world-law",
    "source": "Q65",
    "target": "world-law",
    "label": "bears on"
   },
   {
    "id": "Q65-builder",
    "source": "Q65",
    "target": "builder",
    "label": "bears on"
   },
   {
    "id": "Q66-write-scope",
    "source": "Q66",
    "target": "write-scope",
    "label": "bears on"
   },
   {
    "id": "Q66-check",
    "source": "Q66",
    "target": "check",
    "label": "bears on"
   },
   {
    "id": "Q67-write-scope",
    "source": "Q67",
    "target": "write-scope",
    "label": "bears on"
   },
   {
    "id": "Q67-engine",
    "source": "Q67",
    "target": "engine",
    "label": "bears on"
   },
   {
    "id": "Q68-check",
    "source": "Q68",
    "target": "check",
    "label": "bears on"
   },
   {
    "id": "Q69-profile",
    "source": "Q69",
    "target": "profile",
    "label": "bears on"
   },
   {
    "id": "Q69-law-fingerprint",
    "source": "Q69",
    "target": "law-fingerprint",
    "label": "bears on"
   },
   {
    "id": "Q69-affordance",
    "source": "Q69",
    "target": "affordance",
    "label": "bears on"
   },
   {
    "id": "Q69-engine",
    "source": "Q69",
    "target": "engine",
    "label": "bears on"
   },
   {
    "id": "Q71-people-world",
    "source": "Q71",
    "target": "people-world",
    "label": "bears on"
   },
   {
    "id": "Q71-build",
    "source": "Q71",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q72-scene-replay",
    "source": "Q72",
    "target": "scene-replay",
    "label": "bears on"
   },
   {
    "id": "Q77-run-log",
    "source": "Q77",
    "target": "run-log",
    "label": "bears on"
   },
   {
    "id": "Q82-estimate-rule",
    "source": "Q82",
    "target": "estimate-rule",
    "label": "bears on"
   },
   {
    "id": "Q82-estimator",
    "source": "Q82",
    "target": "estimator",
    "label": "bears on"
   },
   {
    "id": "Q85-estimator",
    "source": "Q85",
    "target": "estimator",
    "label": "bears on"
   },
   {
    "id": "Q85-run-loop",
    "source": "Q85",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q86-stopping-point",
    "source": "Q86",
    "target": "stopping-point",
    "label": "bears on"
   },
   {
    "id": "Q86-estimator",
    "source": "Q86",
    "target": "estimator",
    "label": "bears on"
   },
   {
    "id": "Q88-estimate-rule",
    "source": "Q88",
    "target": "estimate-rule",
    "label": "bears on"
   },
   {
    "id": "Q88-estimator",
    "source": "Q88",
    "target": "estimator",
    "label": "bears on"
   },
   {
    "id": "Q88-gen-rules",
    "source": "Q88",
    "target": "gen-rules",
    "label": "bears on"
   },
   {
    "id": "Q92-judge-ruling",
    "source": "Q92",
    "target": "judge-ruling",
    "label": "bears on"
   },
   {
    "id": "Q92-ruling-rule",
    "source": "Q92",
    "target": "ruling-rule",
    "label": "bears on"
   },
   {
    "id": "Q93-ruling-rule",
    "source": "Q93",
    "target": "ruling-rule",
    "label": "bears on"
   },
   {
    "id": "Q94-judge-ruling",
    "source": "Q94",
    "target": "judge-ruling",
    "label": "bears on"
   },
   {
    "id": "Q94-ruling-rule",
    "source": "Q94",
    "target": "ruling-rule",
    "label": "bears on"
   },
   {
    "id": "Q95-ruling-rule",
    "source": "Q95",
    "target": "ruling-rule",
    "label": "bears on"
   },
   {
    "id": "Q96-offer",
    "source": "Q96",
    "target": "offer",
    "label": "bears on"
   },
   {
    "id": "Q96-judge-ruling",
    "source": "Q96",
    "target": "judge-ruling",
    "label": "bears on"
   },
   {
    "id": "Q96-ruling-rule",
    "source": "Q96",
    "target": "ruling-rule",
    "label": "bears on"
   }
  ],
  "layout": {
   "direction": "RIGHT"
  }
 },
 "metamodel": {
  "schema": "typed-graph/v1",
  "kinds": {
   "state": {
    "label": "World state",
    "color": "#3b6fb6",
    "explain": "What exists: things, their kinds and their typed fields."
   },
   "rules": {
    "label": "Rules",
    "color": "#c26a1b",
    "explain": "What can change and how: action kinds, checks, effects, processes."
   },
   "acting": {
    "label": "Acting",
    "color": "#6b7280",
    "explain": "How a decider's choice becomes a recorded event."
   },
   "noticing": {
    "label": "Noticing",
    "color": "#2f8f9d",
    "explain": "How an actor comes to know what happened."
   }
  },
  "nodes": [
   {
    "id": "world",
    "label": "World",
    "kind": "state",
    "explain": "The one canonical world of a run: entities, a tick, a revision and the events so far."
   },
   {
    "id": "category",
    "label": "Category (kind of thing)",
    "kind": "state",
    "explain": "What kind of thing an entity is (person, place, door, helicopter); rules select by category."
   },
   {
    "id": "entity",
    "label": "Entity (thing)",
    "kind": "state",
    "explain": "Any thing in the world, a person, a wall or a glass alike, with a stable id and typed components."
   },
   {
    "id": "component",
    "label": "Component (state field)",
    "kind": "state",
    "explain": "A typed field on an entity (location, water level, passable, role); the only thing effects change. A disposition (a wall cannot be walked through) is a component value plus the checks that read it. Held in Entity.components; each component type is registered by register_component (model.py:188)."
   },
   {
    "id": "place",
    "label": "Place",
    "kind": "state",
    "explain": "An entity of category place; every other entity's location names the place it is in."
   },
   {
    "id": "way",
    "label": "Way between places",
    "kind": "state",
    "explain": "What lies between two places (a door, a brick wall): an entity naming both places with a passable field; moving names its way and needs it passable. Until fix F6 lands (Q25, settled by argument), a way works from its first place to its second only."
   },
   {
    "id": "action-kind",
    "label": "Action kind (effector)",
    "kind": "rules",
    "explain": "Something an actor can try, with named participant roles, checks and effects, compiled before use (a generated DeclaredActionMechanic) or hand-written (FillRule and the other mechanisms); either way the Engine runs it through the action-rule interface."
   },
   {
    "id": "rule-interface",
    "label": "Action and process rule interface",
    "kind": "rules",
    "explain": "What the Engine actually runs: an action rule discovers, checks and applies one action kind; a process rule says when it is due and applies; both declare read and write paths. Generated mechanics and the hand-written mechanisms library (FillRule, VesselFailureSpillProcess) both implement it."
   },
   {
    "id": "registry",
    "label": "Rule registry",
    "kind": "rules",
    "explain": "The sole lookup surface for the action and process rules installed in one world, in a fixed order."
   },
   {
    "id": "causal-parent",
    "label": "Hard causal parent",
    "kind": "acting",
    "explain": "An earlier event a rule declares as mechanically supporting this one (opt-in, DeclaresCausalParents); kept apart from information a person merely had in mind. S2's reactions cite their trigger this way."
   },
   {
    "id": "role",
    "label": "Participant role",
    "kind": "rules",
    "explain": "A named slot of an action kind (actor, to, way, aircraft) and the categories that may fill it."
   },
   {
    "id": "sense",
    "label": "Sense binding",
    "kind": "rules",
    "explain": "The meaning and participant roles Linguistic Core gives an action kind; never its effects."
   },
   {
    "id": "check",
    "label": "Check (precondition)",
    "kind": "rules",
    "explain": "A test a move or process must pass against current state (the way is passable, the trainee can fly); a failed check refuses the move with the check named."
   },
   {
    "id": "effect",
    "label": "Effect",
    "kind": "rules",
    "explain": "A change to one component path that runs when every check holds, inside the declared write scope."
   },
   {
    "id": "write-scope",
    "label": "Declared write scope",
    "kind": "rules",
    "explain": "The paths a rule may change; the Engine refuses any change outside them."
   },
   {
    "id": "process",
    "label": "Process (knock-on rule)",
    "kind": "rules",
    "explain": "A rule the world runs by itself for every matching entity whose checks hold, each round by default or at once when its timing is immediately; this is how effects propagate (plants dry out, a glass breaks)."
   },
   {
    "id": "knock-on-now",
    "label": "Same-moment knock-on",
    "kind": "rules",
    "explain": "A process with timing immediately, run in waves inside the same moment as the move or round step that triggered it until nothing more is due; each process and thing pair fires once per moment, which ends every chain; new runs have no other cap, and a run recorded before J0 of docs/plans/ai_judge.md replays under its old cap of 32 (slice S2 of docs/plans/open_attempt.md, ODD 8.20)."
   },
   {
    "id": "skill-roll",
    "label": "Skill roll",
    "kind": "rules",
    "dashed": true,
    "explain": "A seeded roll on an action kind so a move can partly succeed or fail by skill (planned slice S3). Planned, not built."
   },
   {
    "id": "terminal",
    "label": "Terminal condition",
    "kind": "rules",
    "explain": "A state-derived stop: when its checks hold over the selected entities, the task ends one way."
   },
   {
    "id": "profile",
    "label": "Frozen mechanic profile",
    "kind": "rules",
    "explain": "The validated rules of one world frozen under an id before any run."
   },
   {
    "id": "affordance",
    "label": "Affordance (offered move)",
    "kind": "acting",
    "explain": "A move an actor can make now: an action kind with participants bound and its checks holding, as Engine.discover lists it."
   },
   {
    "id": "decider",
    "label": "Decider (policy)",
    "kind": "acting",
    "explain": "What chooses an actor's next move: scripted, an AI menu chooser or a Concordia resident."
   },
   {
    "id": "attempt",
    "label": "Attempt (free text)",
    "kind": "acting",
    "explain": "What a resident says it tries, in its own words; never executable."
   },
   {
    "id": "attempt-reading",
    "label": "Attempt reading",
    "kind": "acting",
    "explain": "The interpreter's typed reading of an attempt: an action kind and participants, with no outcome field, a wait, or no match."
   },
   {
    "id": "unmatched",
    "label": "Unmatched attempt",
    "kind": "acting",
    "explain": "An attempt no action kind covers; it changes nothing and is listed in the run's build record."
   },
   {
    "id": "typed-action",
    "label": "Typed action (command)",
    "kind": "acting",
    "explain": "The envelope submitted to the Engine: actor, action kind, bound participants, base revision."
   },
   {
    "id": "event",
    "label": "Event",
    "kind": "acting",
    "explain": "The record of one attempt or process step: status, every check and its result, the changes, the cause and an id like r14-e00012."
   },
   {
    "id": "observation",
    "label": "Observation (sensor)",
    "kind": "noticing",
    "explain": "What one actor can see of the world now, filtered by place and by information delivery."
   },
   {
    "id": "information",
    "label": "Information and delivery (channel)",
    "kind": "noticing",
    "explain": "An information entity and its delivery rows: who has been told what, by which channel, and when; a word said across the world reaches no one without a delivery."
   }
  ],
  "edges": [
   {
    "id": "m1",
    "source": "world",
    "target": "entity",
    "label": "holds"
   },
   {
    "id": "m2",
    "source": "entity",
    "target": "category",
    "label": "is a"
   },
   {
    "id": "m3",
    "source": "entity",
    "target": "component",
    "label": "has"
   },
   {
    "id": "m4",
    "source": "place",
    "target": "entity",
    "label": "is an"
   },
   {
    "id": "m5",
    "source": "way",
    "target": "entity",
    "label": "is an"
   },
   {
    "id": "m6",
    "source": "way",
    "target": "place",
    "label": "joins"
   },
   {
    "id": "m7",
    "source": "action-kind",
    "target": "role",
    "label": "declares"
   },
   {
    "id": "m8",
    "source": "sense",
    "target": "role",
    "label": "names"
   },
   {
    "id": "m9",
    "source": "role",
    "target": "category",
    "label": "filled by"
   },
   {
    "id": "m10",
    "source": "action-kind",
    "target": "check",
    "label": "requires"
   },
   {
    "id": "m11",
    "source": "action-kind",
    "target": "effect",
    "label": "produces"
   },
   {
    "id": "m12",
    "source": "process",
    "target": "check",
    "label": "requires"
   },
   {
    "id": "m13",
    "source": "process",
    "target": "effect",
    "label": "produces"
   },
   {
    "id": "m14",
    "source": "effect",
    "target": "component",
    "label": "changes"
   },
   {
    "id": "m15",
    "source": "effect",
    "target": "write-scope",
    "label": "bounded by"
   },
   {
    "id": "m16",
    "source": "rule-interface",
    "target": "action-kind",
    "label": "runs"
   },
   {
    "id": "m17",
    "source": "rule-interface",
    "target": "process",
    "label": "runs"
   },
   {
    "id": "m18",
    "source": "registry",
    "target": "rule-interface",
    "label": "installs"
   },
   {
    "id": "m19",
    "source": "event",
    "target": "causal-parent",
    "label": "cites"
   },
   {
    "id": "m20",
    "source": "knock-on-now",
    "target": "causal-parent",
    "label": "cites"
   },
   {
    "id": "m21",
    "source": "check",
    "target": "component",
    "label": "reads"
   },
   {
    "id": "m22",
    "source": "knock-on-now",
    "target": "process",
    "label": "is a timing of"
   },
   {
    "id": "m23",
    "source": "skill-roll",
    "target": "effect",
    "label": "varies"
   },
   {
    "id": "m24",
    "source": "terminal",
    "target": "check",
    "label": "requires"
   },
   {
    "id": "m25",
    "source": "profile",
    "target": "action-kind",
    "label": "freezes"
   },
   {
    "id": "m26",
    "source": "profile",
    "target": "process",
    "label": "freezes"
   },
   {
    "id": "m27",
    "source": "affordance",
    "target": "action-kind",
    "label": "offers"
   },
   {
    "id": "m28",
    "source": "decider",
    "target": "affordance",
    "label": "chooses from"
   },
   {
    "id": "m29",
    "source": "decider",
    "target": "attempt",
    "label": "says"
   },
   {
    "id": "m30",
    "source": "attempt",
    "target": "attempt-reading",
    "label": "read as"
   },
   {
    "id": "m31",
    "source": "attempt",
    "target": "unmatched",
    "label": "or"
   },
   {
    "id": "m32",
    "source": "attempt-reading",
    "target": "typed-action",
    "label": "becomes"
   },
   {
    "id": "m33",
    "source": "decider",
    "target": "typed-action",
    "label": "submits"
   },
   {
    "id": "m34",
    "source": "typed-action",
    "target": "event",
    "label": "recorded as"
   },
   {
    "id": "m35",
    "source": "process",
    "target": "event",
    "label": "recorded as"
   },
   {
    "id": "m36",
    "source": "event",
    "target": "component",
    "label": "changes"
   },
   {
    "id": "m37",
    "source": "observation",
    "target": "entity",
    "label": "shows"
   },
   {
    "id": "m38",
    "source": "observation",
    "target": "information",
    "label": "filtered by"
   },
   {
    "id": "m39",
    "source": "observation",
    "target": "decider",
    "label": "feeds"
   }
  ]
 },
 "metamodel_mapping": {
  "kernel": {
   "repository": "BrianMills2718/scientific-hypergraph",
   "revision": "7b0638fe0aef41c772bb181996516f98be479597",
   "path": "wiki/reference/metamodel/hypergraph-kernel-v2.json"
  },
  "mappings": [
   {
    "node": "world",
    "relation": "specializes",
    "maps_to": "scientific-hypergraph-v2 document",
    "why": "a world is one model document of elements and relation instances, plus a clock the kernel lacks"
   },
   {
    "node": "category",
    "relation": "same",
    "maps_to": "sci:instanceOf type",
    "why": "an entity's category is the type it is an instance of"
   },
   {
    "node": "entity",
    "relation": "specializes",
    "maps_to": "sci:ModelElement",
    "why": "every entity is a model element; World Substrate adds components"
   },
   {
    "node": "component",
    "relation": "composes",
    "maps_to": "sci:RelationInstance (holder, value)",
    "why": "a component value is a binary relation instance between an entity and a value"
   },
   {
    "node": "place",
    "relation": "specializes",
    "maps_to": "sci:ModelElement",
    "why": "a place is a model element like any entity; location components point at it"
   },
   {
    "node": "way",
    "relation": "specializes",
    "maps_to": "sci:ModelElement",
    "why": "a way is an entity, so a model element like a place; its two place references compose relation instances (way, from place) and (way, to place), and passable is a component on it"
   },
   {
    "node": "action-kind",
    "relation": "specializes",
    "maps_to": "sci:RelationType",
    "why": "an action kind is an n-ary relation type whose roles are its participants; the kernel has no effects"
   },
   {
    "node": "rule-interface",
    "relation": "no_counterpart",
    "why": "an executable interface; the kernel holds no code"
   },
   {
    "node": "registry",
    "relation": "no_counterpart",
    "why": "a runtime table of executable rules, outside the kernel"
   },
   {
    "node": "causal-parent",
    "relation": "specializes",
    "maps_to": "sci:RelationInstance (event, parent event)",
    "why": "a directed relation instance between two applied events"
   },
   {
    "node": "role",
    "relation": "same",
    "maps_to": "sci:RoleType",
    "why": "a participant role is a declared role of the relation type, with a participant-type constraint"
   },
   {
    "node": "sense",
    "relation": "composes",
    "maps_to": "sci:declaresRole",
    "why": "a sense supplies the role declarations the relation type carries"
   },
   {
    "node": "check",
    "relation": "no_counterpart",
    "why": "the kernel stores relations, not evaluable conditions"
   },
   {
    "node": "effect",
    "relation": "no_counterpart",
    "why": "the kernel stores relations, not changes to state, so it has no evaluable effects"
   },
   {
    "node": "write-scope",
    "relation": "no_counterpart",
    "why": "authority derived from the declaration; the kernel has no authority model"
   },
   {
    "node": "process",
    "relation": "no_counterpart",
    "why": "an actorless effectful rule; the kernel has none"
   },
   {
    "node": "knock-on-now",
    "relation": "no_counterpart",
    "why": "a timing rule over effectful processes; the kernel has none"
   },
   {
    "node": "skill-roll",
    "relation": "no_counterpart",
    "why": "a stochastic effect; the kernel has none"
   },
   {
    "node": "terminal",
    "relation": "no_counterpart",
    "why": "an evaluable condition; the kernel has none"
   },
   {
    "node": "profile",
    "relation": "no_counterpart",
    "why": "a versioned package of executable rules, outside the kernel"
   },
   {
    "node": "affordance",
    "relation": "no_counterpart",
    "why": "a query result derived from rules and state, not a stored relation"
   },
   {
    "node": "decider",
    "relation": "no_counterpart",
    "why": "cognition outside the world; the kernel does not model agents"
   },
   {
    "node": "attempt",
    "relation": "no_counterpart",
    "why": "natural language outside the world"
   },
   {
    "node": "attempt-reading",
    "relation": "specializes",
    "maps_to": "sci:RelationInstance (proposed)",
    "why": "a proposed instance of an action-kind relation type, not yet applied"
   },
   {
    "node": "unmatched",
    "relation": "no_counterpart",
    "why": "a recorded refusal with no relation type to instantiate"
   },
   {
    "node": "typed-action",
    "relation": "specializes",
    "maps_to": "sci:RelationInstance with sci:RoleBinding",
    "why": "a typed action is a relation instance whose role bindings are its participants"
   },
   {
    "node": "event",
    "relation": "specializes",
    "maps_to": "sci:RelationInstance",
    "why": "an event is an applied relation instance plus check results, changes and causal parents"
   },
   {
    "node": "observation",
    "relation": "no_counterpart",
    "why": "a per-actor view derived from state, not a stored relation"
   },
   {
    "node": "information",
    "relation": "specializes",
    "maps_to": "sci:RelationInstance (information, recipient)",
    "why": "a delivery is a relation instance between a piece of information and a recipient"
   }
  ]
 },
 "context_diagrams": [
  "C4Context\n  title World Substrate system context\n  Person(author, \"World author\", \"Describes a world, reviews and approves its rules, watches runs\")\n  System(ws, \"World Substrate\", \"Compiler, approval gate, Engine, World Builder service, projections\")\n  System_Ext(llm, \"LLM providers\", \"Reached only through llm_client; proposals and move choices\")\n  System_Ext(runtimes, \"Concordia / Mesa / PDDL\", \"Resident cognition, grids and sweeps, plan validation\")\n  System_Ext(host, \"Cloudflare + personal VPS\", \"Serve the pages and the API\")\n  Rel(author, ws, \"Describes, approves, inspects\")\n  Rel(ws, llm, \"Requests proposals and choices\")\n  Rel(runtimes, ws, \"Submit intents; read observations\")\n  Rel(host, ws, \"Hosts\")\n",
  "C4Container\n  title World Substrate containers\n  Person(author, \"World author\")\n  Container(builder, \"World Builder service\", \"scripts/world_builder_service.py\", \"Approval gate, budget ledger, run log\")\n  Container(compiler, \"Authoring compiler\", \"src/world_substrate/action_authoring.py\", \"Proposal to rules with derived authority\")\n  Container(installer, \"Installer and run loop\", \"scripts/run_authored_world.py + profile.py\", \"Freezes the approved profile, runs residents\")\n  Container(engine, \"Engine\", \"src/world_substrate/engine.py\", \"Atomic commit or refusal, write scopes, events\")\n  Container(projection, \"Projections\", \"projection.py, information.py\", \"Live view and observer visibility from canonical state\")\n  Rel(author, builder, \"HTTP\")\n  Rel(builder, compiler, \"Compile and review\")\n  Rel(builder, installer, \"Run approved mechanics\")\n  Rel(installer, engine, \"Submit envelopes, tick processes\")\n  Rel(engine, projection, \"Snapshot and event deltas\")\n"
 ],
 "disagreements": [
  "**Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).",
  "**The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there."
 ],
 "next_plan": "---\nplan_id: \"open-attempt\"\ndependencies: []\ndependencies_reviewed: \"2026-10-25\"\nplanning_path: durable_solo\nplanning_path_ref: docs/plans/open_attempt/path-decision.json\nmethod_conformance_receipt: docs/plans/open_attempt/conformance-receipt.json\nstatus: adopted\ngoal:\n  outcome: \"World Builder residents say in their own words what they physically try, instead of picking from a list; the world's rules decide what happens, knock-on effects run to the end inside the same moment, and a person's recorded skill (never how expert their words sound) decides how a risky attempt turns out.\"\n  canonical_example: \"A World Builder world generated from 'A small airfield office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown'. In one run Sam tries to walk through the wall and nothing happens, with the wall named as the cause; someone knocks the glass off the desk and in the same event chain it falls, breaks, the water spills and the person in the next room hears it; Sam tries to fly the helicopter and a recorded roll from Sam's piloting level 0 usually gives a crash under this scenario’s declared outcome mapping; a clean result remains possible from the recorded dice, never from good wording.\"\n  forbidden_substitutes: \"hand-edited specs, rules or runs; an interpreter that decides success; outcomes written by an LLM rather than by an installed rule; a roll whose dice come from the attempt's wording; a scripted move presented as an attempt; Waltzman-specific code paths; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run.\"\n  boundaries: \"world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change; existing saved worlds still replay unchanged; owner allowance only, visitor allowance stays $3/day; free replays of saved worlds before any paid run; publish-checker before anything new goes public.\"\n  done_when: \"Acceptance checks A1-A9 below pass, each judged from the full trace of the run it names.\"\n  do_not_gate_on: \"letting an AI game master invent effects for attempts no rule covers (Decision D2: not yet, Brian 2026-10-26); organisations, the decider spectrum and thinking-as-effector (later designs); a clingo cross-check of the reaction rules; Brian's review of a run.\"\n  stop_after: 3\nconflict_surfaces:\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/open-attempt/review-page/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/concordia_residents.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/attempt.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open-attempt.goal.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.verdicts.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/planning-package.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_readout.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/index.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/architecture/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: Makefile, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: lefthook.yml, access: write}\n---\n# Plan: open attempts, knock-on effects that run to the end, and skill rolls\n\nPlanning package: docs/planning/open-attempt/planning-package.json\n\n<!-- planning-compliance-checklist:v1 -->\n## Compliance checklist\n\nWritten by `plan_checklist.py --write`, not by hand. `--check` re-runs the validator and fails\nif any line below differs from what it says now. Unticked pending items are not passes.\n\nManifest: `docs/planning/open-attempt/planning-package.json`\nPackage revision: `fdca8f49e7bd`\nVerdict: compliant, 2 pending\n\n- [x] part investigation: ok\n- [x] part checks: ok\n- [x] part open_questions: ok\n- [x] part system_model: ok\n- [x] part domain_model: ok\n- [x] part diagrams: ok\n- [x] part plan: ok\n- [x] part acceptance: ok\n- [x] part review_page: ok\n- [x] part cold_review: ok\n- [x] substance route follows from its path decision: ok\n- [x] substance citations resolve: ok\n- [x] substance domain model has a glossary: ok\n- [x] substance project layer checks against the planning layer: ok\n- [x] substance concepts point at their code: ok\n- [x] substance plan names the concepts it relies on: ok\n- [x] substance plan records the cost basis of each AI step: ok\n- [ ] substance plan compares its AI answer path with the plain version: failing\n- [x] substance plan shows what each stage adds over the plain version: ok\n- [x] substance plan records Brian's stops on this work: ok\n- [x] substance type-level model of executable rules: ok\n- [x] substance cold review read this revision: ok\n- [x] initiative initiative names its home: ok\n- [x] tiers spectrum rungs 1-11 are cited: ok\n- [x] tiers production rungs 12-14 are cited when it runs in production: ok\n- [x] tiers thesaurus separates near-identical names (rung 4): ok\n- [ ] system_map system map names every code unit: pending\n- [ ] coverage goal coverage: pending\n- [x] goal_provenance goal provenance: ok\n- [x] freshness package is current: ok\n<!-- /planning-compliance-checklist -->\n\n\nThis is the open-attempt plan’s own package. The repository package (`docs/planning/planning-package.json`, repo-wide page `proposals/planning-package/review-page/`) now uses this active plan and its I0/I1 acceptance entries. The packages share models, checks and the question ledger, and retain their own review records. Neither a repository-package nor a plan-package pass certifies production outcomes.\n\nReview page: [proposals/open-attempt/review-page/](../../proposals/open-attempt/review-page/index.html), live at\n<https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/>.\n\n## Actor and result\n\n**Actor:** a World Builder visitor (and Brian as owner) who pastes a scenario and watches the\ngenerated people act. **Result they can inspect:** the run page and its build record show each\nperson's own-words attempt, what the rules made of it, and why it worked, failed or did nothing.\n**Stable example:** the airfield office in the front matter's `canonical_example`: Sam walks into\nthe wall and is refused with the wall named; the glass chain runs in one moment; Sam's untrained\nflight rolls two dice keep-lower.\n\n## Project outcome\n\nProject outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top, rigorous causal engine underneath; the World Builder is the visitor-facing surface). This plan serves that actor directly: the roadmap's \"user describing a world\" is the\nWorld Builder visitor of the Actor section. **Recurring job and baseline:** a visitor describes a world and\nwatches its people act; before S1 each person could only pick from moves the rules already allowed, so\nimpossible attempts (the wall) never appeared. S1 (merged at `fe8c492`, #239) lets residents say attempts in\ntheir own words, and its live run (`evidence/open-attempt/s1-airfield/`, #247) shows residents acting every round; the\nwall refusal and the untrained flight were not exercised in that run. S2 is built with fixture evidence, while its generated-world evidence remains incomplete; S3 skill rolls remain unbuilt. **Inspectable result this plan\ndelivers:** the run page and build record of the airfield world showing the wall refusal, the glass chain\nand the rolled crash. **Stage and investment boundary:** prototype stage; three slices, each one pull\nrequest and at most $3.00 of owner allowance; no new service, engine or repository.\n\n## Outcome step\n\nOutcome probe: `roadmap/README.md#canonical-outcome-probe`\nObserved: `evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md`\nStep: step 3 of the probe, \"the residents act in the generated world each round, and the installed rules decide each effect\"\nClass: vertical\n\nThe observed proof is the c1r24 run: the last live run of the whole probe before this plan, the canonical\nWaltzman example driven through the real page (generate, 45 rounds, readout, share link `FQHXnP_TLKPi`, every\nround read). It shows step 3 working with residents picking from a move list, which is what this plan changes.\nS1's first live run of step 3 with free-form attempts is `evidence/open-attempt/s1-airfield/TRACE_READ.md`;\nit does not replace c1r24 as the probe's observed proof, because the knock-on and skill cases (A2, A3) were\nnot exercised there and S1 is built, not done.\n\nEach slice changes that step end to end (generator, resident, engine, page) and ends in a live traced run.\n\n## Why, in one example\n\nBefore S1 a World Builder resident was handed a list of moves the rules already allowed and picked one\n(the menu reply's `action_id` is that list plus `wait`, still so for the menu schema at\n`scripts/concordia_residents.py:96`). So nobody ever walked into a wall: the wall never appeared as a\nchoice. S1 replaced that with an own-words `attempt` (built; see the slice table). Brian, 2026-10-24: a\nperson should be able to \"attempt to walk through a wall but these should not be successful\", and\nsomeone who \"dont know how\" to fly a helicopter \"should probably crash it\". The survey\n([flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md),\nBrian's \"yes\" on 2026-10-25 to this design) found three pieces missing from World Substrate and\nnamed the established method to copy for each. This plan designs those three, in the order they\ndepend on each other.\n\n## Baseline and delivered S1 behavior (2026-10-25/26)\n\nThis is historical baseline detail. The slice table and the AI judge plan record later work: S2 is built, J0 removes the cap for new runs, and J2/J3 handle uncovered attempts through checked rulings.\n\n| Have | Where |\n| --- | --- |\n| The rules list what a person can do now (an affordance page) | `Engine.discover`, `src/world_substrate/engine.py:352` |\n| A move whose checks fail is refused with the failed check recorded, no partial change | `Engine.apply` / `_reject`, `engine.py:582`, `:749` |\n| A move of a kind no rule knows is recorded as unsupported, nothing changes | `Engine.submit`, `engine.py:452`; `UnsupportedAction`, `rules.py:288` |\n| Meaning (sense and roles) is kept apart from mechanics | `SemanticBinding`, `src/world_substrate/semantic.py:15`; Decision 003 |\n| Things the world does by itself run once per round, each citing its causes | `Engine.advance`, `engine.py:786`; `DeclaredProcess`, `action_authoring.py:245` |\n| Who hears or sees what is limited by the world | `world_substrate.information` |\n| No randomness anywhere in rules | no `random`/`seed` in `engine.py` or `action_authoring.py` |\n| S1: a resident answers `attempt` in its own words instead of an offered `action_id` | `OPEN_SCHEMA`, `scripts/concordia_residents.py:45` |\n| S1: one typed call reads the attempt into one action kind and its fields, with no outcome field | `interpret`, `src/world_substrate/attempt.py:149`; `read_interpretation`, `:81` |\n| S1: an unmatched attempt changes nothing and is listed in the build record | `UNMATCHED_KIND`, `attempt.py:25`; `unmatched_attempts`, `scripts/run_authored_world.py:800` |\n| S1 (Q23): generated worlds have places, ways with a passable flag, and a move that checks the way | `scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`; `evidence/open-attempt/q23/README.md` |\n| After S1 (#242, `87b4aa2`): the World Builder page sends open-attempt residents whenever AI chooses the moves | `scripts/world_builder_home.html` on main; `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md` on main |\n\nDecision 006 limits World Substrate to the governed-rules layer. Pieces 1 and 3 are rules-layer pieces:\none turns words into a typed move, one adds a recorded roll to a rule. Piece 2 runs rules to a fixpoint\ninside one commit, which changes `engine.py`. Brian ruled on 2026-10-26 (open question Q27, [Decision\n009](../decisions/009-same-moment-knock-on-effects.md)) that this is rule semantics, not the engine capability\nAGENTS.md and Decision 006 forbid: it adds no new loop, clock or scheduler and is bounded at 32 reactions (amended 2026-11-10 by J0 of [the AI judge plan](ai_judge.md) and Decision 009: no cap for new runs, once per pair of process and thing per moment still ends every chain, and runs saved before J0 replay under 32)\ninside the existing commit.\n\n## The three pieces\n\n### Piece 1. Open attempt (copy: Inform 7 \"try\" plus Voyager-style attempts sent to an engine)\n\n1. **Decide.** The resident's reply keeps `belief`, `expected_effect`, `work` and `reasoning`, and\n   replaces `action_id` with `attempt`: one sentence of what they physically do, with their body,\n   voice or hands (\"walk east through the wall into the hangar\"). The affordance page is still shown,\n   as \"things you know you can do here\", but it no longer limits the answer.\n2. **Interpret.** One typed light-model call (`llm_client`, the World Builder's current model, low\n   effort) reads the attempt and the world's action kinds with their fields, and returns `{kind, fields,\n   nearest_kind, why}`, where `fields` is a list of rows `{field, value, quoted_span}` (the words in the attempt\n   behind each value) and `kind` may also be `wait`. `read_interpretation` (`src/world_substrate/attempt.py:81-148`)\n   checks the rows against the world and turns a reading that does not fit (unknown kind or entity, missing field,\n   quoted words not in the attempt) into `{unmatched: true, nearest_kind, why}`. Its schema has **no success field**:\n   it says what is being tried, never whether it works. A `wait` reading of an attempt with real words is listed\n   like an unmatched one (F9, Q39).\n   The result is recorded as the command, so replay never calls the model again.\n3. **Check.** The matched move goes through `Engine.submit` unchanged. The wall case is an ordinary\n   refusal: the generated `move` rule's \"the way between is open\" check fails (S1's canonical world must show the rules writer gave `move` that check; if it did not, that gap is fixed in the rules writer, never by hand-editing the world), and the event names the wall.\n4. **Unmatched fallback (v1).** An attempt that matches no kind is recorded through the existing\n   unsupported path: nothing in the world changes, the person sees \"you try to …; nothing comes of\n   it\", and the build record lists every unmatched attempt so the rules writer can add a rule in the\n   next build. Letting an AI game master invent an effect is Decision D2: not yet (Brian, 2026-10-26).\n5. **Who notices.** Unchanged: `world_substrate.information` decides who perceives the result.\n   Shouting to someone overseas succeeds as speech and reaches only those in hearing range.\n\n### Piece 2. Knock-on effects that run to the end (copy: C+ / Event Calculus ramification)\n\nA process may declare `timing: \"immediately\"` (default stays `\"each_round\"`, so every existing world is\nunchanged). After a move or round event commits its candidate state, the engine runs every immediate\nprocess whose `due()` holds on the new state, then again on the state that produces, until none is\ndue. Rules:\n\n- each (process, entity) pair fires at most once per moment, so a reaction cannot feed itself;\n- at most 32 reactions per moment; going over refuses the whole moment visibly and changes nothing (amended 2026-11-10 by J0 of [the AI judge plan](ai_judge.md) and Decision 009: no cap for new runs, once per pair of process and thing per moment still ends every chain, and runs saved before J0 replay under 32; a step a failed check stops is now recorded with its blocker)\n  (the existing \"no partial mutation\" invariant);\n- every reaction event cites its parent event as a hard causal parent, so the chain is readable;\n- order inside one wave is the registry's fixed order, recorded in the events.\n\nGlass: `push glass` moves it off the desk → `falls` (unsupported object above floor) → `breaks`\n(fragile and fell) → `spills` (container broke while holding water) and, also from `breaks`, a `crash sound` event. Five events in\none moment: fall cites push, break cites fall, and spill and sound both cite break. The person next\ndoor then learns of the sound through `information`; that is an observation, not a sixth event.\n\n### Piece 3. Skill rolls (copy: Blades in the Dark action roll, GURPS defaults, progress clocks)\n\nAn action mechanic may declare `roll: {skill: <actor path>, position: controlled|risky|desperate,\noutcomes: {full: [effects], partial: [effects], fail: [effects]}}`.\n\n- Hard gates first: the ordinary checks (holds the key, knows the number, is in the cockpit) run\n  before any roll. No roll without stakes: a mechanic with no `fail` effects may not declare a roll.\n- Dice: as many six-sided dice as the recorded skill level; level 0 rolls two and keeps the lower\n  (GURPS-style default for the untrained). Highest die 6 = full, 4-5 = partial, 1-3 = fail.\n  Position picks which outcome list the rules writer gave for \"partial\" and \"fail\".\n- The dice come from a seeded generator (`seed = hash(run_seed, event_id)`), and the values are\n  recorded in the event, so a replay reproduces them and a reader can check them.\n- Only the skill path is read. The attempt's wording never reaches the roll.\n- Long tasks: a roll's outcome effects may write the counter field a process already reads (the world field behind `Engine._progress`, `engine.py:321`, which only reports it), so a partial result moves a task's counter less than a full one, like a Blades progress clock.\n\nHelicopter: Sam (piloting 0) is in the cockpit (gate passes), rolls two dice, keeps the lower; on\n1-3 the `fail` effects crash the helicopter, damaging it and injuring Sam, and Piece 2 carries on\n(fuel leaks, alarm sounds, the ground crew hears it).\n\nFor this declared model, independent fair d6 dice give a level-0 failure probability of\n1 - (3/6)^2 = 27/36 = 75%; level 3 fails with probability (3/6)^3 = 12.5%.\nThese are worked-out consequences of the proposed dice and crash-on-fail mapping, not measured aviation\nprobabilities. A level-0 full result remains possible (both dice are 6); Brian asked for a probable crash,\nnot a guarantee. The scenario must declare the crash consequences rather than treating every risky failure\nas a crash. This resolves the earlier absolute clean-flight prohibition by arithmetic.\n\n## Requirements\n\nWhat Brian asked, plus what the plan's own claims imply; each row names its check in the acceptance table below. Status per check: S1 is built (merged `fe8c492`, #239): A1 (`tests/test_open_attempt.py`) and A8 (`scripts/check_project.py`) were checked in its pull request, and the owner-allowance airfield run with residents (`evidence/open-attempt/s1-airfield/`, 2026-10-26, merged in #247)\njudged A4 and A9 passing (its TRACE_READ.md passes `scripts/check_trace_reads.py` and samples ordinary attempts, which is R1's trace check) and left A2 and A3 planned and not yet run: the live run never reached the helicopter or the wall, so both run next on the saved airfield world `tests/fixtures/airfield-s1-live.json` (see the S1 live result below); S2 is built: A6 and the A5 fixture chain pass in `tests/test_open_attempt.py`, and A5 on a generated world was not exercised by the S2 owner run (`evidence/open-attempt/s2-airfield/`: no `timing: immediately` process was written for the airfield); A7 planned in S3; A8 planned in every slice\n(run on each merge commit); A9 planned in S1 (open-attempt part) and completed in S3 (full chain). None is\ndeferred. The claimed property is the requirement itself (an impossible attempt is refused with its cause,\na chain finishes, skill sets the dice), never a count of passing tests.\n\n\n| Id | Requirement (source) | Fails when | Control | Status |\n| --- | --- | --- | --- | --- |\n| R1 | Residents can try anything their body can do (Brian 2026-10-24) | The interpreter quietly maps \"fly the helicopter\" to a safe move | `quoted_span` per role; A2 negative fixture; TRACE_READ samples ordinary attempts | Passing in part: the S1 live run TRACE_READ samples ordinary attempts and passes; A2 planned and not yet run (fixture run next) |\n| R2 | The world, not the interpreter, decides what happens (Decision 003; AGENTS.md \"installed mechanics alone\") | The interpreter refuses or judges success | No success field in its schema (A1); refusals only come from rule checks | Passing: A1 in #239 |\n| R3 | Impossible attempts fail with a cause (Brian 2026-10-24) | A wall attempt is dropped instead of recorded | A3: refused event names the failed check | Planned and not yet run: A3 on the saved airfield world next |\n| R4 | Knock-on effects run on their own to the end (Brian 2026-10-24) | A chain stops after one step, or loops | A5, A6: once-per-pair rule, cap of 32, whole moment refused on overflow (cap removed for new runs 2026-11-10, J0 of [the AI judge plan](ai_judge.md)) | Passing in part (S2 built): A6 (once per pair, and the 32 limit) and the A5 fixture chain pass in `tests/test_open_attempt.py::KnockOnEffectTests`; A5 on a generated world not exercised: the S2 owner run on `623bce2` (`evidence/open-attempt/s2-airfield/`) built a world with no `timing: immediately` process, so no chain was set off (cause and follow-ups #253-#255 in its TRACE_READ.md) |\n| R5 | Skill decides risky outcomes, not wording (Brian 2026-10-24: LLM knowledge must not leak) | Dice depend on the attempt text, or outcomes are written by the model | A7: same attempt, skill 0 versus 3, different dice pools; dice only from seed | Planned and not yet run (S3) |\n| R6 | Saved worlds and replays keep working (AGENTS.md invariants) | Replay calls the model or rerolls | A8: every retained replay test unchanged; rolls and interpretations replay from records | Passing at the S1 merge (A8); S2 at its merge commit (see the S2 row); planned for S3 |\n| R7 | Every run is readable in full (core rules) | An interpretation or roll is missing from the trace | A9: run-log.jsonl has each interpreter call's trace id, each roll's dice; TRACE_READ.md passes | Passing for S1 (A9 on the live run); full chain planned in S3 |\n\n## Acceptance checks\n\n| Id | Check | Run and what its trace must show |\n| --- | --- | --- |\n| A1 | Interpreter schema has no success or outcome field | `pytest tests/test_open_attempt.py::test_schema_has_no_outcome` output |\n| A2 | \"Fly the helicopter to the coast\" never binds to `move` | fixture run on the generated airfield world; the command records `kind: pilot`, `quoted_span` \"fly the helicopter\" |\n| A3 | Walking through the wall is refused, wall named | the canonical run's event for Sam's wall attempt: `status: refused`, failed check names the wall entity. Q23 (generated worlds have walls) resolved: `evidence/open-attempt/q23/README.md` |\n| A4 | An unmatched attempt changes nothing and is listed | the canonical run's build record `unmatched_attempts` list, and the event's before/after equal |\n| A5 | The glass chain completes in one moment | canonical run: one moment with push, fall, break, spill and sound events; fall cites push, break cites fall, spill and sound cite break. Judged separately: the neighbour's observation for that moment includes the sound |\n| A6 | A knock-on effect cannot run forever: a reaction that stays due fires once per moment, and a chain of more than 32 reactions is refused whole (since J0 of [the AI judge plan](ai_judge.md), 2026-11-10: only for runs recorded under that limit; these tests run with the recorded limit of 32) | `tests/test_open_attempt.py`: `test_a_reaction_that_keeps_itself_due_fires_once_per_moment` (status accepted, the rule fires exactly once though its check still holds) and `test_a_chain_past_the_reaction_limit_is_refused_whole` (a ring of 40 glasses: status `reaction_limit`, world unchanged, failed check \"Knock-on effects settle within 32 reactions\") |\n| A7 | Skill, not wording, sets the dice | fixture: identical attempt text, piloting 0 and 3; events show 2-keep-lower versus 3 dice, seed recorded; declared crash-on-fail mapping gives 75% versus 12.5% failure by arithmetic, not a guaranteed single-run result |\n| A8 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with these replay tests named passing in the quoted output: `test_action_envelopes` (unsupported and malformed envelopes replay), `test_first_fill.test_fill_tick_and_replay_match_exactly`, `test_greenhouse_zero_review.test_replay_regenerates_exactly_through_generic_renderer`, `test_castaway_zero_review.test_zero_review_replay_regenerates_exactly` |\n| A9 | The canonical run is fully traced | `evidence/open-attempt/<run>/run-log.jsonl` plus `TRACE_READ.md` passing `scripts/check_trace_reads.py`; read by the implementing agent before reporting |\n\n## Success and disproof\n\nThe plan claims three properties: (1) residents state any physical attempt and only installed rules\ndecide its effect (R1-R3, checked by A1-A4); (2) knock-on effects run to the end inside one moment or the\nmoment is refused whole (R4, A5-A6); (3) recorded skill, not wording, decides risky outcomes (R5, A7);\nwith replay unchanged (R6, A8) and every run fully readable (R7, A9).\n\n**Success:** A1-A9 pass, each judged from the full trace of the run it names. **Disproof:** any one\nof these in the canonical run's trace: an interpreter output carrying a success or outcome; a wall\nattempt that changes the world or is refused without naming the wall; a pilot attempt by a level-0\nperson whose outcome contradicts the recorded roll or declared crash-on-fail mapping; dice whose seed is not `hash(run_seed, event_id)`; a replay that\ncalls a model. Trace review: the implementing agent reads every refused, unmatched and rolled attempt\nand a sample of ordinary ones in the named run's `run-log.jsonl` and writes `TRACE_READ.md`; each criterion\nA1-A9 is expected `pass`. Runs are named in order: `evidence/open-attempt/s1-replay/` (free replay of a\nsaved world), `evidence/open-attempt/s1-airfield/` (first owner-allowance run, judged for A2-A4 and A9),\n`evidence/open-attempt/s2-airfield/` (A5), `evidence/open-attempt/s3-airfield/` (A7 and the full A9);\nA1, A6 and A8 are judged from the named pytest and `check_project.py` output saved beside each run.\n\n## When a run fails or surprises us\n\nThis is separate from the anticipated failure modes in the Requirements table: it covers what we did not\nforesee. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,\nintermediate stages (interpretation, checks, reactions, rolls) and the final output (build record, page)\nbefore choosing a fix; cite where it diverged; classify it evidence absent, unused or\ncontradicted, invalid expectation, or unresolved. An unresolved cause permits investigation, not a\nrepair. A repair is verified by a new traced run whose `TRACE_READ.md` links the original run and the divergence it\nfixes; the original stays. Never rerun until a behavior\nappears and report only that run. Review completeness never changes the run verdict: a run's pass or fail\ncomes from its trace against A1-A9, and an incomplete review leaves the claim unreported, not passed.\n\n## Slices, in order\n\n| Slice | What lands | State | Checks |\n| --- | --- | --- | --- |\n| S1 | Close Q23 (rules writer makes places, ways and the wall check), then open attempt: resident `attempt` field, interpreter, unmatched fallback, build-record list | built, not done: merged `fe8c492` (#239); page fix `87b4aa2` (#242); live run `evidence/open-attempt/s1-airfield/` (#247): A4 and A9 pass, A2 and A3 not exercised; the run page does not yet show own-words attempts (Q26) | A1, A8 at merge; free replay `evidence/open-attempt/s1-replay/replay.txt` exit 0; A4, A9 on the owner-allowance run; still owed: A2 and A3 on the saved world `tests/fixtures/airfield-s1-live.json`, and Q26 |\n| S2 | `timing: immediately` processes run to a fixpoint inside one moment | built, not done: engine `_settle` (Decision 009), rules writer `timing`, transcript `reactions`, round picture and state panel show each knock-on effect with its cause; Q28 resolved (no reuse of the library damage processes, `evidence/open-attempt/q28/README.md`); deployed `623bce2`; the S2 owner run (`evidence/open-attempt/s2-airfield/`) did not exercise A5 on a generated world: the rules writer wrote no `timing: immediately` process for the airfield, nothing pushed the glass, and the builder kept a circling world (#253) whose fly and teach moves change nothing (#254); still owed: a generated world with something that can be knocked over | A6 and the A5 fixture chain in `tests/test_open_attempt.py::KnockOnEffectTests`; A8 at merge; model drift test `tests/test_system_model.py::test_knock_on_effects` |\n| S3 | `roll` on action mechanics, seeded and recorded; rules writer prompt can declare it; the compiler adds the roll's skill path to derived reads and every outcome's effects to derived writes (Q40) | fully_specifiable_now | A7, A8, a test that a roll outside its derived scope is refused, then the full canonical run for A9 |\n| S4 | AI game master for unmatched attempts | deliberately_deferred (D2 answered \"not yet\" by Brian 2026-10-26) | none; reopened only by a new decision |\n\n**Kinds the canonical airfield world must contain** (generated, never hand-written): `move` between\nplaces with a check that the way between is open (the wall), `push` an object, `pilot` a craft to a\nplace, and `speak`. Before S1, generated worlds were economy-style (`make-leads`, `shape-slats`) and\nnothing in the rules writer asked for places, ways between them or blocking. That was open question\n**Q23**, S1's first step, resolved 2026-10-25 by a generic fix to the bundle contract and rules writer\n(`scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`): the regenerated airfield\nworld refuses the walk through the wall with \"the way is passable\" failed\n(`evidence/open-attempt/q23/after-fix/probe.txt`). Known limit, open question **Q25**: a way works from its\nfirst place to its second only.\n\n**S1 live result** (`evidence/open-attempt/s1-airfield/TRACE_READ.md`, owner allowance, deployed `87b4aa2`, 9 rounds,\n65 model calls, $0.0319): residents moved every round; A4 passes live (15 refused or unmatched attempts each changed\nnothing and every unmatched one is listed with the interpreter's nearest move); A2 and A3 were not exercised, because\nthe build left the helicopter unreachable: everyone but the mechanic starts in the office, the brick wall is the only\nway to the hangar and is not passable, the builder's own test runs said the practice flight was never possible and the\nbuild was accepted anyway (#244, Q30). Two smaller defects were filed: a refusal reason reads as a fact (\"you are the\ndispatcher\") rather than a requirement (#245, Q31), and the readout chose the goods-flow lens for a training world (#246, Q32).\nS1 is therefore built but not done. Next: A2 as a fixture run of \"fly the helicopter to the coast\" and A3 as an\ninterpreted attempt at the wall, both on the saved world `tests/fixtures/airfield-s1-live.json` (free, no new build),\nthen Q26 (the run page shows each attempt in its owner's words).\n\nEach slice is its own pull request and leaves a working World Builder. S1 alone already lets a\nresident walk into the wall. The rules writer (`scripts/generate_causal_model.py`, its process and mechanic schemas) learns `timing` in S2 and\n`roll` in S3; until then generated worlds simply do not use them.\n\n## Decisions\n\n- **D1 (made, technical):** the interpreter is one typed light-model call per attempt, not a parser\n  and not the resident's own model. Reason: words to (kind, roles) is meaning, which our rules say\n  is never read with regex; a separate call keeps the resident from steering its own interpretation.\n  Cost: one extra small call per attempt, measured in S1's first run against the visitor $3/day cap.\n- **D2 (Brian's call, decided 2026-10-26: not yet):** for attempts no rule covers, should an AI game master be allowed\n  to invent a rough effect, marked \"coarse\" in the record? Recommendation: not now. v1 says \"nothing\n  comes of it\" and lists the attempt for the rules writer. If not answered, v1 stays. Prior art in this\n  repository: the offline any-scenario spike already lets its game master write a rule mid-run for each unlisted\n  attempt, installed if it passes the layer-1 checks, else recorded as a one-off ruling (`docs/model/ODD.md:194`,\n  8.19 at `:266`); Decision 007 accepted that for the spike with review after the run, but no person approves (G14)\n  and the spike stays offline (Q17). S4 would differ: it is on the live World Builder, where approval before a run\n  still holds (Decision 006); it makes one coarse effect for one attempt, not a general rule; and the record marks it\n  coarse. If allowed, it reuses the spike's check gate rather than a new path.\n- **D3 (made, technical):** reactions are a `timing` field on the existing process declaration, not a\n  new rule type, so they reuse its selector, checks, effects, linked participants and write scopes.\n\n## System model\n\n- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a refused attempt changes nothing), RULE-PROJECTION-FROM-CANONICAL-ONLY (the page shows only recorded events). Adds: `attempt interpretation` (adds), `unmatched_attempts` (adds), `timing` (adds), `roll` (adds).\n- Scope: the system model is this repository's own (world-substrate only, linked from the documentation entry point\n  `docs/wiki/README.md`), not a shared model. The one shared artefact it touches is the\n  scientific-hypergraph kernel, which it reads at a pinned revision and never changes; the mapping\n  onto it lives here (`docs/model/metamodel-mapping.json`).\n- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) (built by `scripts/build_metamodel.py`) holds the\n  world's own types this plan relies on (action kind, role, check, effect, process, affordance, decider,\n  attempt, attempt reading, unmatched attempt, event, observation) and the two it plans (same-moment\n  knock-on, skill roll), each mapped onto the scientific-hypergraph kernel at `7b0638f`. Its reuse-gate\n  table records the formalisms checked before minting them (bounded-design typed-relational reference,\n  rule 1); AlgebraicPetri and TypeDB were open question Q24, resolved by argument as compose. S2 and S3 flip their type to built in that\n  table in the same pull request.\n- Not changed, and why: actors, places, information reach (`world_substrate.information`), tasks and\n  the budget ledger keep their current model elements; this plan only changes how a move is chosen,\n  how reactions run and how a mechanic resolves, so their definitions stand. RULE-BUDGET-FAILS-CLOSED,\n  RULE-FROZEN-PROFILE and RULE-DERIVED-AUTHORITY are relied on unchanged.\n- Views: [docs/model/VIEW_COVERAGE.md](../model/VIEW_COVERAGE.md) records which view shows each element; each slice adds its rows there. Per element:\n  - `attempt interpretation` (`AttemptReading`): `owner_run_log` shows it (`GET /runs?full=1` keeps the\n    transcript, `scripts/world_builder_service.py:1011`); `home` does not yet, gap G17, now open question Q26 (S1 is not done until it closes).\n  - `unmatched_attempts`: `owner_run_log` shows it in the run summary (`GET /runs` keeps `summary`,\n    written at `scripts/run_authored_world.py:800`); `home` does not yet, gap G17.\n  - `timing` and the reaction wave (S2): `round_replay` and `scenario_state_panel` must show each\n    reaction event with its parent; S2 adds the row.\n  - `roll` (S3): `scenario_state_panel` must show each roll's seed and dice; S3 adds the row.\n- The trace must show, per element: the command's `interpretation` record with the interpreter's trace id; the build record's `unmatched_attempts`; reaction events citing their parent; each roll's seed and dice.\n- S1 adds an `attempt interpretation` record\n  (command field) and the `unmatched_attempts` build-record list; S2 adds the `timing` process field and\n  the reaction-wave events; S3 adds the `roll` mechanic field and the event's `roll` record. Each slice\n  updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request,\n  and the drift test must fail on a renamed field before it passes.\n## Trace visibility\n\n- Each run's `run-log.jsonl` records: the inputs (scenario text, world bundle hash, run seed); every step\n  (round, actor, attempt text); each model call (resident, interpreter, rules writer) with its prompt\n  messages, arguments, typed result and `llm_client` trace id; the model's reasoning where it returns it\n  (the resident's `reasoning` field); every engine event with before/after, failed checks, reaction parent\n  and dice; and the output (build record, page JSON). Kept for ordinary runs, not only failures. No slice is a pure document edit, so no slice\nclaims the no-run exemption; this adoption commit alone is document-only and runs nothing.\n- How to open one: `evidence/open-attempt/<run>/run-log.jsonl` is one JSON object per line (`jq . <file>`);\n  the live run's page links its share id, and `llm_client` trace ids open in its trace store\n  (`python -m llm_client traces --trace-id <id>`). Who reads and when: the implementing agent reads every run's\n  trace before reporting that slice, including the free replay and fixture runs; every failure or surprise\n  in full, and at least five ordinary attempts per run chosen across rounds and actors. This plan has no runs\n  other than World Builder runs and the test suite, whose output is saved beside each run.\n- World Builder runs keep `run-log.jsonl` (every request, interpreter and resident call with\n  `llm_client` trace ids, every event with dice) beside the run; `TRACE_READ.md` per round. The\n  implementing agent reads every refused, unmatched and rolled attempt in the canonical run and a sample\n  of ordinary ones before reporting.\n## Capability reuse\n\nNo catalogue entry fits, because `reuse_candidates.yml` and\n  `capability_registry.yml` hold approvals, notifications, scheduling, document-to-text and search\n  wrappers, none of which interpret actions or run rules. Model calls go through the workspace's shared\n`llm_client` (listed in `~/code2/workspace/docs/capabilities.md`, not a catalogue entry). No new\ncross-project capability is added; the interpreter's first and only consumer is the World Builder run loop.\n\n## Prior art and ownership\n\nDisposition per piece, from [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md): open attempt **extends** the existing unsupported-action path and `Engine.submit` (copying Inform 7 \"try\" and Voyager-style attempts); knock-on effects **extend** `DeclaredProcess` (copying C+/Event Calculus ramification); skill rolls **extend** `DeclaredActionMechanic` (copying Blades in the Dark and GURPS defaults). Owner: World Substrate's rules layer (Decision 006). Parallel-implementation check: no second command path, engine or scheduler; every attempt still enters through `Engine.submit`, and `grep -n \"def submit\" src/world_substrate/engine.py` stays one hit.\n\n## LLM call boundary\n\nCall graph per round: resident call (one per actor, existing) -> attempt interpreter call (one per attempt,\nnew, after the resident's reply, before `Engine.submit`) -> no further model call; rules, reactions and\nrolls are code. The rules writer's calls (existing, at build time) change only in prompt and schema.\nProvider: OpenRouter, model `openrouter/openai/gpt-6-luna` (the World Builder's `DEFAULT_MODEL`,\n`scripts/run_authored_world.py:37`). Spend authority: Brian's owner allowance, granted for this plan on\n2026-10-25. An interpretation becomes authoritative only as a recorded command after an authentic live\nrun; fixtures may use recorded interpretations but are never reported as live.\n\nExisting resident call (unchanged boundary except the field): typed reply `{belief, attempt, expected_effect,\nwork, reasoning}`; `attempt` replaces `action_id`; it has no success field either; the reply is recorded in\n`run-log.jsonl` with its trace id and is never re-read by rules or replay; a failed or malformed reply records\nthe actor as waiting, as today.\n\nOne new call: the attempt interpreter, through `llm_client`, typed output (`kind`, which may be `wait`; `fields` rows of `field`, `value` and `quoted_span`; `nearest_kind`; `why`), checked into a reading or `unmatched` by `read_interpretation`, no success field. Its output is recorded as the command and never re-read by rules or replay; it has no authority to change state, and promotion of its output to authority is refused by construction (only `Engine.submit` writes). Failure: a malformed or failed call records the attempt as unmatched with the error, never a guessed move.\n\nTracing: each run gets one trace id, `world-builder-live-run-<uuid4 hex>` (`scripts/run_authored_world.py:385`), passed to every resident call (`scripts/concordia_residents.py:101`) and every interpreter call (`src/world_substrate/attempt.py:158`), so all of a run's model calls share it; `llm_client` stores each call under that id in its `llm_calls` table (`~/projects/data/llm_observability.db`) with its task name, model, request messages, response, token counts, cost, latency, error and timestamp. The run's `run-log.jsonl` repeats the trace id beside each recorded reply and interpretation, so a run row links to its calls (Trace visibility, above).\n\n## Irreversible actions and spend\n\nNothing irreversible is planned: merges are pull requests (revert with git) and deploys of World Builder's\nown service are redeployable from the previous commit. Boundary: no deletion of saved worlds or run\nrecords, no outreach, no change to other repositories. If a step would be irreversible, it stops and goes\nto Brian first (core rules: \"Ask first only for irreversible actions\"); authorization for everything in\nthis plan is Brian's 2026-10-25 \"yes\". Containment: the deploy is checked through the health endpoint's\nbuild commit and rolled back to the prior commit if it fails. Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 across S1\n(stop and report if a run would exceed it, enforced by the run's `max_budget`); the visitor allowance\nstays $3/day.\n\n## Uncertainties\n\nThe material uncertainties, listed in full as of 2026-10-26: each below could change a slice's scope or an acceptance check's verdict, and none changes whether this plan is adopted. Q24 (whether Petri nets or TypeDB could carry the metamodel's types) was not material to this plan and is resolved by argument (compose).\n\n- Q23 (agent, resolved 2026-10-25): the rules writer now gives `move` a way-open check (`evidence/open-attempt/q23/README.md`).\n- Q25 (agent, resolved by argument 2026-10-26): ways are two-way unless the description declares them one-way; the build is F6 below. Until it lands, each run's `TRACE_READ.md` names any resident stuck behind a way it already used, so it is not read as a refusal by the world.\n- Q26 (agent, open): the run page does not show an attempt in its owner's words or that it matched nothing (G17); S1 is not done until it does.\n- Q27 (resolved by Brian 2026-10-26, \"i approve\"; Decision 009): S2's same-moment fixpoint in `engine.py` is rule semantics, not the engine capability AGENTS.md and Decision 006 forbid, within its bounds (inside the existing commit, 32-reaction cap (amended 2026-11-10 by J0 of [the AI judge plan](ai_judge.md) and Decision 009: no cap for new runs, once per pair of process and thing per moment still ends every chain, and runs saved before J0 replay under 32), `timing: immediately` only).\n- Q28 (agent, resolved 2026-10-26): S2's glass chain does not reuse the hand-written spill and damage processes (`src/world_substrate/mechanisms/damage.py:116`): they read built-in entity slots a generated world never has and cannot run immediately, so the rules writer writes its own (`evidence/open-attempt/q28/README.md`, reading plus one free probe).\n- Q30 (#244, agent, open): a build is accepted although its own test runs say a task is never possible; blocks A2 and A3 on a newly built world, not on the saved fixture.\n- Q31 (#245) and Q32 (#246) (agent, open): a refusal reason reads as a fact rather than a requirement, and the readout picked the goods-flow lens for a training world; neither changes an acceptance check's verdict, both change what a reader of the S1 run sees.\n- Q33 (agent, open in part): S3's seeded roll is settled by argument for where `run_seed` lives (drawn once per run, recorded in the run record, dice recorded per roll event, so replay never rolls and saved worlds without rolls replay unchanged; the 'no randomness' row becomes 'no unrecorded randomness'); open is whether the rules writer gives a generated person a skill field from the description (Sam's piloting 0), checked by a free probe before S3. A7 and A9 depend on it.\n- Q34 (agent, open): read scopes are recorded, not enforced; compiled rules derive their reads from their own checks, so only hand-written rules could leave F1's `blocked_by_event` or a Piece 2 parent link incomplete. Settled by a test-time read check before F1 relies on reads of hand-written rules.\n- Q22 / D2 (Brian, resolved 2026-10-26): no AI game master yet; \"nothing comes of it\" stays.\n- Q36 (agent, open): how an interpreter misreading (a legal but wrong move) is caught; quoted spans, A2's negative fixture and a listed set of readings off their nearest kind, settled before A2 is judged. Injected visitor text cannot add a kind, entity or outcome (Q35, resolved).\n- Q37 (#241, agent, open): the builder added doorways around the wall and listed them as left out; A3 is judged on the saved fixture, whose wall is the only way.\n- Q38 (agent, open): #128 closes once A3 shows a refused wall attempt chosen from belief.\n- Q39 (agent, resolved by argument): a wait reading of an attempt with words is a silent no-op today; F9 lists it.\n- Q40 (agent, resolved by argument): S3's rolls sit in the causal model, so approval and the fingerprint cover them; the run seed is a run input; the compiler derives the roll's reads and writes (S3 row).\n- Interpreter cost per attempt (Q29, resolved 2026-10-26 from S1's live run): the 20 interpreter calls added 11.6% to\n  the run's other calls (about 24% at the 30-round cap), under the 30% that would require batching, so S1 keeps one\n  call per attempt.\n\n## Fixes settled by argument\n\nOpen questions that an argument already answers; each is small, agent-owned, built alongside the slices in its own\npull request, and checked on a free replay of a saved world before any paid run.\n\n| Id | Question | Fix | Check |\n| --- | --- | --- | --- |\n| F1 | Q2 | The refused row names the earlier event this round that changed what its failed checks read (`blocked_by_event`) | free replay of the saved airfield and c1r24 worlds: every refused row after a lost race names an accepted event id of that round |\n| F2 | Q6 | `/run` refuses a second request for the same session, round and base revision | a test that sends the same round twice: one run, one charge |\n| F3 | Q8 | A field a check reads that the build's spec names as used up, claimed or changed by a task, and that no rule writes, is a test-run finding; a fixed fact (the airfield wall's `components.boundary.passable`, read at `tests/fixtures/airfield-s1-live.json:392`, written by no rule) is not | the saved #218 build lists its resource; the airfield fixture's wall is not listed |\n| F4 | Q10 | The readout quotes `said_on_retry` when present, as the scene replay does | free replay of a saved menu-path run |\n| F5 | Q15 | Adopt the `~/code2` repository format (indexes over the existing documents) | the repo-format check reports compliant |\n| F6 | Q25 | Ways are two-way unless the description declares them one-way | regenerate the airfield world and probe both directions |\n| F7 | Q4 | A remedy's work answer says yes or no to the concern's question plus what was set, and the finished-task notice quotes it | a test that a remedy without that answer is refused and the notice quotes it; the next owner-allowance people-world run's TRACE_READ.md reads its notices |\n| F8 | Q9 | Task worlds' scripted test run lasts 24 rounds, like ongoing worlds, instead of 12 | the saved build fixtures score the same or better, and the garden world (#217) finishes inside the test run |\n| F9 | Q39 | An attempt with words that the interpreter read as `wait` is listed in the run summary as `read_as_wait` with the interpreter's why, beside `unmatched_attempts` | a test with a recorded wait reading of \"fly the helicopter\": the summary lists it; a literal \"wait\" is not listed |\n\n## Activation facts\n\nRecorded in [activation-facts.json](open_attempt/activation-facts.json): shared mechanism yes (engine and generator are shared by every world), no empirical comparison, LLM central yes, spend yes (owner allowance). Route: [path-decision.json](open_attempt/path-decision.json), durable_solo. The plan copies established methods (Inform 7, Event Calculus, Blades in the Dark,\nGURPS) but claims conformance to none of them, so `claims_external_standard` is false.\n\n## Durable documents\n\nDurable documents: system_model#ENT-ACTION-ENVELOPE, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, system_model#ENT-RUN-RECORD, plans\n\nS1 changes ENT-ACTION-ENVELOPE (the command gains its interpretation) and ENT-RUN-RECORD (the build\nrecord gains `unmatched_attempts`); S2 changes PROC-PROCESS-TICK and PROC-TRANSITION (reaction waves);\nS3 changes PROC-TRANSITION (rolls). Each ID is in `docs/model/trace.yaml` today. The roles are declared\nin `.agentic/repo.yaml` lines 3-8: `system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`\nand `plans: docs/plans/`. At completion of each slice, `python3\n~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan\ndocs/plans/open_attempt.md --range <adoption revision>..HEAD` must exit 0.\n\n## Authority and non-goals\n\n**Authority:** Brian's \"yes\" on 2026-10-25 to adopt this plan and start S1; one agent writes; world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only.\n\n**Non-goals:** Organisations as agents, the code/fast-model/LLM decider spectrum, thinking as an effector, moving off\nConcordia 2.4.0, a clingo cross-check, and any change to Cybernetic Influence v3. Each comes after this.\n\n## Information-boundary and concern follow-up (selected design, implementation merged)\n\nSource: Brian's November 12 pre-implementation documentation goal; slice decomposition inferred by agent. These follow-up slices own the [complete actor-information contract](../model/modeling-choices.md#complete-actor-information-contract) and its single-concern scenario, with normative targets in [information-delivery](../../openspec/specs/information-delivery/spec.md). Existing S1–S3 status is unchanged. Brian approved I0/I1 implementation on 2026-11-12 after PR #378 (\"i approve. givem e the /goal text\"), then activated the I0/I1 goal. This authorizes these two slices through their own deployment and necessary bounded evidence within existing owner budgets; unrelated roadmap work remains outside scope.\n\n| Slice | Required outcome and dependencies | Direct acceptance / known broken case |\n| --- | --- | --- |\n| I0: complete actor-input boundary | Audit and constrain both policy paths, tools and continuation: observation, brief, summary, memory, recent events, offered actions, refusals and UI. Preserve open attempts when true executability is unknown. Depends on information-delivery target contract; J4 and E5 depend on I0 evidence. | Run/context view: select Actor mode and switch between Mara and Bo, then return to Analyst mode; open the source of each factual input, then continue and retry a delivery. Hidden report details stay absent from every unauthorized actor surface, including labels and errors; the analyst can inspect exact inputs. Broken: a filtered report appears in a global summary or resumed memory. |\n| I1: one concern without forced persuasion | After I0, represent independent actual condition, claim/delivery, actor-owned stance/assent and institutional hold under the guide's stated procedure. Reuse authoring, delivery and resident seams; preserve old scripted rules as fixtures. | Single-concern demonstration: open public dashboard, Mara's report, Bo's different report, their expressed responses, the review result and activation checks. Public hold legitimately implies failed validation here; private severity/remedy details differ. Delivery changes neither technical state nor assent. Passing revalidation clears only the technical hold. Broken: receiving a warning automatically withdraws support, or elapsed review time cures the defect. |\n\nImplementation merged in PR #379 at `f4b7afab183691df0e364a624a275876bcddb9ba`. The [I0/I1 acceptance entries](../planning/open-attempt/acceptance-criteria.json) use the existing World Builder Actor/Analyst controls. They remain built but unverified as complete deployed demonstrations until an inspected production run and working share link are recorded; no agent status substitutes for Brian's own judgment. [Repair evidence](../../evidence/i0-i1/repair-verification.txt) records focused checks, saved-world replay, exact counterexample review and privacy scan; [integration-2](../../evidence/i0-i1/local-integration-2/TRACE_READ.md) remains failed acceptance evidence. Reuse existing run/context views where possible; a new cognition framework or custom physical engine is outside scope. The benefit of I0 first is shared secrecy for influence and credentials; its cost is inspecting the complete input assembly before adding visible estimator behavior. I1 then addresses the original influence question with minimal new world structure. New adapters stay conditional on a concrete investigation. Scientific actor-model adequacy remains a separate empirical uncertainty, never an I0 leakage substitute.\n\n\n## Whole-attempt coverage follow-up (Q36)\n\nSource: Brian, 2026-11-13, “i approve proceed”, following the recommendation to resolve the retained compound-attempt counterexample. Technical design inferred by agent from [production5](../../evidence/i0-i1/deployed-integration-5/TRACE_READ.md). This bounded implementation is authorized; it does not reopen unrelated roadmap work.\n\n**Selected contract:** keep one installed operation per attempt. Identify the concrete means rather than substitute its goal: Mara's recording of concern is not withdrawal of prior assent. True independent operations require decomposition unless an installed composite covers the whole request. Quoted speech, coordinated instruments and expected consequences do not create additional operations. An impossible single action still reaches the rules. A fresh response must explicitly assess whole-attempt coverage, with exact quoted evidence; invalid or incomplete coverage preserves the attempt but executes no part and cannot create a new rule or deliver a request. The actor receives safe clarification, with full diagnostics restricted to analyst evidence. Historical records remain unassessed rather than retroactively certified.\n\n**Tradeoff:** this preserves distinctions and prevents silent prefix execution without building a sequencer, adding model stages or choosing extra actions for residents. It costs a small additional structured field in the same call; incremental token cost is unmeasured until retained replay. Some compound requests need the resident to try separately. A model can still falsely call its reading complete, so Q36 remains open; schema checks are not proof of semantic adequacy. Existing owner budgets apply. Free engine and saved-world checks precede minimal same-input native replay; no random model comparison or repeated world authoring is needed.\n\n**Reviewable result:** the existing attempt detail explains that no part was carried out and asks for one concrete operation. Analyst detail preserves the text and coverage. Test both resident information modes, judge enabled/disabled, no request delivery, installed-composite acceptance and ordinary missing-rule routing. This is a correction through the existing interpreter/runner/UI seams; no engine, scheduler or cognition capability is added.\n\nBounded evidence: [whole-attempt trace read](../../evidence/open-attempt/whole-attempt-coverage/TRACE_READ.md). Three native interpreter calls cost measured $0.00097666: the exact Mara case records concern, the repair control is unchanged, and the true compound is safely rejected after the model omits required quote evidence. Actual restored-world engine replay commits only Mara's stance, while the compound branch changes nothing and calls no judge. These are recorded-input checks, not a fresh autonomous policy run. A4 retains the visible clarification and unchanged-state demonstration without claiming its older full inspector requirement complete. [Open the compound replay](../../proposals/open-attempt/review-page/coverage-compound.html) and [Mara replay](../../proposals/open-attempt/review-page/coverage-mara.html).\n",
 "built_from": "fdca8f4"
};
