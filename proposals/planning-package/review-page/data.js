window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/world-substrate",
  "subject_revision": "c9303a74fc3e6a588f03dda787225353b400889f",
  "request": "Brian 2026-10-24 \"do that\" (after: \"ok are we company planning compliant? would it have prevented or mitgated these probelms if we were?\")",
  "parts": {
   "checks": {
    "status": "present",
    "path": "docs/planning/checks.txt",
    "results": [
     {
      "name": "durable documents (arc42)",
      "command": "python3 $HOME/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --repo . --arc42",
      "exit_status": 0,
      "counts": {
       "findings": 0
      }
     },
     {
      "name": "project navigation",
      "command": "python3 $HOME/code2/company-planning/plugins/company-planning/scripts/validate_project_navigation.py .",
      "exit_status": 0,
      "counts": {
       "findings": 0
      }
     },
     {
      "name": "repository format",
      "command": "python3 $HOME/code2/workspace/scripts/repo_format.py .",
      "exit_status": 1,
      "counts": {
       "compliant": 0,
       "of": 1
      },
      "tracked_by": "Q15"
     },
     {
      "name": "trace reads",
      "command": "python3 scripts/check_trace_reads.py",
      "exit_status": 0,
      "counts": {
       "runs": 9,
       "problems": 0
      }
     },
     {
      "name": "project check (tests, system model, docs)",
      "command": "PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --python 3.12 --with pydantic --with gdm-concordia==2.4.0 --with pytest python scripts/check_project.py",
      "note": "counts from its unittest runner line 'Neutral runtime tests: Ran N tests'",
      "exit_status": 0,
      "counts": {
       "tests_run": 710,
       "failed": 0,
       "skipped": 2
      }
     },
     {
      "name": "wiki and Markdown cap",
      "command": "python3 $HOME/code2/project-meta/scripts/md_file_cap.py --repo .",
      "exit_status": 0,
      "counts": {
       "md_files": 134,
       "cap": "exception",
       "orphans": 0
      }
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
    "basis": "src/world_substrate/engine.py:582",
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
     "world": "src/world_substrate/model.py:382",
     "engine": "src/world_substrate/engine.py:198",
     "event": "src/world_substrate/engine.py:529",
     "move": "src/world_substrate/action_authoring.py:49",
     "process": "src/world_substrate/engine.py:829",
     "compiler": "src/world_substrate/action_authoring.py:456",
     "policy": "src/world_substrate/policy.py:50",
     "sense": "src/world_substrate/semantic.py:15",
     "profile": "src/world_substrate/profile.py:266",
     "write-scope": "src/world_substrate/engine.py:88",
     "causal-trace": "src/world_substrate/engine.py:529",
     "world-kind": "scripts/world_builder_service.py:113",
     "builder": "scripts/world_builder_service.py",
     "approval": "scripts/world_builder_service.py:418",
     "fingerprint": "scripts/world_builder_service.py:381",
     "information": "src/world_substrate/information.py:57",
     "run-loop": "scripts/run_authored_world.py:347",
     "contention": "scripts/run_authored_world.py:563",
     "resident": "scripts/concordia_residents.py:44",
     "task": "scripts/attempts.py:17",
     "notice": "scripts/attempts.py:234",
     "build": "scripts/world_builder_service.py:1541",
     "rules-retry": "scripts/world_builder_service.py:263",
     "test-run": "scripts/world_builder_service.py:1610",
     "run-log": "scripts/world_builder_service.py:524",
     "readout": "scripts/run_readout.py:125",
     "scene-replay": "scripts/render_scene_replay.py:398",
     "share": "scripts/world_builder_service.py:598",
     "budget": "scripts/world_builder_service.py:51",
     "people-world": "scripts/people_world.py:364",
     "communicate": "spikes/any-scenario-2026-10/compile_spec.py",
     "moment": "spikes/any-scenario-2026-10/compile_spec.py:48",
     "work-cycle": "spikes/any-scenario-2026-10/compile_spec.py:517",
     "group-decision": "spikes/any-scenario-2026-10/compile_spec.py:86",
     "concern": "spikes/any-scenario-2026-10/compile_spec.py:70",
     "support": "spikes/any-scenario-2026-10/compile_spec.py:66",
     "remedy": "spikes/any-scenario-2026-10/compile_spec.py:332",
     "agenda": "scripts/people_world.py:279",
     "rollout": "spikes/any-scenario-2026-10/compile_spec.py:399",
     "review": "spikes/any-scenario-2026-10/compile_spec.py:442",
     "person": "spikes/any-scenario-2026-10/scenario_spec.py:41",
     "gen-rules": "scripts/people_world.py:260",
     "waltzman-ref": "reference_worlds/waltzman/components.py:11",
     "affordance": "src/world_substrate/engine.py:352",
     "check": "src/world_substrate/rules.py:48",
     "attempt": "src/world_substrate/attempt.py:149",
     "attempt-reading": "src/world_substrate/attempt.py:81",
     "unmatched-attempt": "src/world_substrate/attempt.py:25",
     "observation": "src/world_substrate/engine.py:235",
     "place-way": "scripts/generate_world_bundle.py:96",
     "projection": "src/world_substrate/projection.py:44",
     "causal-parent": "src/world_substrate/rules.py:383",
     "exchange": "src/world_substrate/exchange.py:20",
     "mechanisms": "src/world_substrate/mechanisms/__init__.py:3",
     "kitchen": "reference_worlds/kitchen/mechanics.py"
    }
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
     "run-loop",
     "contention",
     "event",
     "move",
     "check",
     "resident",
     "readout",
     "share",
     "budget",
     "scene-replay",
     "run-log",
     "engine",
     "compiler",
     "gen-rules",
     "build",
     "causal-trace",
     "sense",
     "place-way",
     "process",
     "knock-on-now",
     "skill-roll",
     "causal-parent",
     "test-run",
     "mechanisms"
    ]
   },
   "review_page": {
    "status": "present",
    "path": "proposals/planning-package/review-page/index.html",
    "url": "https://hive.brianmills.dev/plans/world-substrate/main/proposals/planning-package/review-page/"
   },
   "cold_review": {
    "status": "present",
    "path": "docs/planning/cold-review.md",
    "verdict": "pass"
   }
  }
 },
 "questions": [
  {
   "id": "Q1",
   "short": "Rules retry never runs here",
   "question": "The build's rules retry is skipped once 80 s have passed, and in the canonical Waltzman build the test run starts at 85-111 s. Should the cut-off, or the order of the build steps, change so the retry can repair a world?",
   "blocks": "whether a world whose rules fail the part-way or liveness checks can be repaired on the live path, or only scored lower",
   "resolves_with": "An argument already settles that the retry is skipped (85, 101 and 111 s against 80 s). In those runs the test run found no part-way problem, so nothing needed repair (c1r24 TRACE_READ.md:54): it is a latent risk for a world that does. What is left is a technical trade-off against the 150 s first-round target: measure where the build's time goes in the saved build traces (free) and either start the test run earlier or tie the cut-off to the time left before that target.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/world_builder_service.py:263",
    "scripts/world_builder_service.py:1667",
    "docs/plans/waltzman-tasks-slice2.goal.md:100",
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
   "question": "When an earlier move this round changes the state before a person's move, does the record say which event blocked it? On the live open-attempt path the same attempt is resubmitted at the new revision and only its rule's checks decide it (scripts/run_authored_world.py:571-573); menu paths ask once more (:581). On every path the refused row lists the failed check labels (refused_because, :622-627) but not the event that changed the state.",
   "blocks": "whether a reader of a run (or the readout) can say why a person's move was refused, in any world",
   "resolves_with": "An argument settles it: the run loop already knows which submitted event changed the revision before the loser's pick, so naming it costs nothing and belongs in the run loop, not any world. Build it and check on free replays of saved worlds (c1r24 Waltzman, truck) that each refused row names its blocking event id. Starting point: c1r24 call 18016 shows the round's moves but not the link.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "scripts/run_authored_world.py:563",
    "scripts/run_authored_world.py:571",
    "scripts/run_authored_world.py:581",
    "scripts/run_authored_world.py:622",
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
   "resolves_with": "An argument makes the content cause likely (the partnership said at c1r24 round 40 it should not add an item 'when I lack information'), but the residents' behaviour cannot be shown on a free replay, which uses scripted moves with no AI. It needs one paid owner-allowance run, and only once Q12 or a goal makes the agenda matter: the result decides whether to give items content, cost them, or drop the count. A free replay can only check that items carry content.",
   "owner": "agent",
   "status": "open",
   "sources": [
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
   "status": "open",
   "sources": [
    "scripts/attempts.py:234",
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "docs/plans/waltzman-tasks-slice2.goal.md:117"
   ],
   "touches": [
    "notice",
    "task",
    "concern"
   ]
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
   "resolves_with": "An argument settles that it is decidable: a field read by a check but never written by any rule is a static finding. Add it to the test-run findings and check the saved worlds.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "BrianMills2718/world-substrate#218"
   ],
   "touches": [
    "gen-rules",
    "test-run"
   ],
   "evidence": "Settled by argument: a field read by a check but written by no rule is a static finding, decidable from the compiled rules alone. Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F3): add it to the test-run findings and check the saved worlds."
  },
  {
   "id": "Q9",
   "short": "Test run too short for some tasks",
   "question": "The 12-round scripted test run rejects correct rules for task worlds that need more rounds (#217). Should it run longer?",
   "blocks": "builds wrongly scored as failing and the rewrite spend they cause",
   "resolves_with": "One counterexample already exists (the garden world finishes at round 15). Lengthen the free test run for task worlds and check the saved fixtures still score the same.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#217",
    "scripts/world_builder_service.py:108"
   ],
   "touches": [
    "test-run"
   ]
  },
  {
   "id": "Q10",
   "short": "Retry keeps the first words",
   "question": "A menu retry's own words are stored as said_on_retry (scripts/run_authored_world.py:637-638), but the 'What happened' readout quotes only said (:621), the words behind the first choice. Should the readout quote the retry's words?",
   "blocks": "whether the readout's quoted words match the move that ran",
   "resolves_with": "Reading the code settles it: the row keeps both (run_authored_world.py:584, :599-600) and the scene replay already prefers said_on_retry (render_scene_replay.py:398), but run_readout.py:93 reads said only. Make the readout prefer said_on_retry the same way and check it on a free replay.",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "scripts/run_authored_world.py:621",
    "scripts/run_authored_world.py:637",
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
   "question": "A people-world run ends at the round cap even when nothing has changed for 20 rounds. Should it stop when the decision is settled and nothing changes?",
   "blocks": "how long visitors watch a run, and its cost",
   "resolves_with": "This is a product call on what a finished story looks like; no test settles it.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Stop a people-world run when the decision is deployed or rejected and no person's move has changed anything for one full operating-review period (6 rounds, compile_spec.py:442), and say so on the page.",
   "default": "Runs keep ending at the round cap the visitor picked.",
   "sources": [
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "scripts/run_authored_world.py:418",
    "scripts/run_authored_world.py:39"
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
    "roadmap/README.md:211",
    "roadmap/README.md:252",
    "docs/plans/open_attempt.md:8"
   ],
   "touches": [
    "contention",
    "run-loop",
    "law-fingerprint"
   ],
   "evidence": "Brian chose on 2026-10-25: his 'yes' adopted docs/plans/open_attempt.md and started S1, so the open-attempt slices come next, before the run-loop fixes and the hardening queue. The run-loop fixes are settled by argument and agent-owned (Q2, Q6, Q8, Q10), built alongside the slices (docs/plans/open_attempt.md, 'Fixes settled by argument'); the roadmap hardening queue (roadmap/README.md:252-256) follows the plan."
  },
  {
   "id": "Q14",
   "short": "Agent-harness build not live",
   "question": "Decision 008 says worlds are built in an agent harness that drafts, checks and edits, but the live service does not call scripts/world_harness.py. Is the harness to be wired into the live build?",
   "blocks": "whether build repairs come from a harness or from the rules retry (Q1)",
   "resolves_with": "Reading the code and the decision settles the current state (not imported by the service; the decision says it has not been shown on the live server). What it would take is a build-time measurement against the 150 s target, from saved build traces first.",
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
   "question": "The ~/code2 repository format check fails: no docs/index.md, docs/architecture/arc42.md, C4 files, openspec specs, lefthook.yml or Makefile. The shape is settled by prior art (phenomenal-meaning adopted it); what stays open is only that the files are not yet added, so the check still fails.",
   "blocks": "whether the repo-format check passes",
   "resolves_with": "Prior art settles the shape (phenomenal-meaning adopted it); the work is mechanical: add the files, mostly as indexes over the existing architecture, ODD and trace documents.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/checks.txt"
   ],
   "touches": [],
   "evidence": "Settled by prior art: phenomenal-meaning adopted the ~/code2 repository format, so the shape is known and the work is mechanical (indexes over the existing architecture, ODD and trace documents). Build work: docs/plans/open_attempt.md, 'Fixes settled by argument' (F5). Kept open, not resolved, because the planning contract requires a check that still fails to be tracked by an open question; it closes when the repo-format check reports compliant."
  },
  {
   "id": "Q16",
   "short": "Goals skip the package gate",
   "question": "This repository's work ran as /goal documents, which never pass plan adoption, so nothing required a planning package. Should writing a goal require one?",
   "blocks": "whether the next goal can again run without a current system model and question list",
   "resolves_with": "An argument: Brian approved on 2026-10-21 that every plan carries a planning package, and a goal is a plan. But a hard check would refuse new goals in every repository that has no package yet, so how strictly to enforce it is a priority call.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Make the goal validator (agent-skills, skills/authoring-goals/scripts/validate_goal_authority.py) refuse a goal document without a 'Planning package:' line or a named exemption, so goal-driven repositories meet the same gate as adopted plans.",
   "default": "The goal-writing skill only tells authors to name the package; nothing refuses a goal without one. This repository's next goal already names its package.",
   "sources": [
    "~/code2/agent-skills/skills/authoring-goals/SKILL.md",
    "docs/plans/waltzman-tasks-slice2.goal.md:1"
   ],
   "touches": []
  },
  {
   "id": "Q17",
   "short": "Offline pipeline views",
   "question": "The offline any-scenario pipeline has no view of its model and checks (G13) and no approval step (G14). Should it get them, or stay an offline spike?",
   "blocks": "whether work goes into the offline pipeline at all",
   "resolves_with": "A scope call; the live path now builds people worlds itself, so the pipeline matters less.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Keep it an offline spike: no views or approval step, since the live World Builder is where people build worlds.",
   "default": "No work on G13 or G14.",
   "sources": [
    "docs/model/VIEW_COVERAGE.md",
    "docs/decisions/007-any-scenario-path.md"
   ],
   "touches": [
    "build"
   ]
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
    "docs/plans/waltzman-tasks-slice2.goal.md"
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
   "question": "When a resident tries something no installed rule covers, may an AI game master invent a rough effect, marked coarse in the record?",
   "blocks": "slice S4 of docs/plans/open_attempt.md, and how alive a world feels when its rules are thin",
   "resolves_with": "A product call on whether every effect must come from a written rule; no test settles it.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Not yet: the person is told nothing comes of it, and the attempt is listed for the next build's rules writer.",
   "default": "Unmatched attempts change nothing and are listed in the build record.",
   "sources": [
    "docs/plans/open_attempt.md",
    "src/world_substrate/rules.py:288"
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
   "question": "Petri nets already lend World Substrate their transition semantics (docs/plans/linked_process_participants.md:136): a process is close to a transition that fires when enabled with no actor, and output arcs are close to a declared write scope. Could a typed Petri net (AlgebraicPetri) or TypeDB (relations with role players) carry the rest well enough to adopt instead of the table in scripts/build_metamodel.py: guards that read arbitrary component checks over bound participants, partial observation (who notices a firing), and refusal of an attempted move with the failed check named?",
   "blocks": "whether the metamodel keeps its own action-kind and attempt-reading types or adopts an outside carrier for them",
   "resolves_with": "Prior art: read AlgebraicPetri's typed Petri net and TypeDB's relation/role schema and map each onto action kind, role, check, effect, process, observation and refused event. If either holds checks as guards, per-actor noticing and named refusal, adopt it as the carrier for those types; if one of the three has no counterpart, keep the own types and compose (Petri semantics for firing, own types for checks, noticing and refusal).",
   "owner": "agent",
   "status": "resolved",
   "sources": [
    "docs/plans/linked_process_participants.md:136",
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
   "question": "The run page's round text reads row.belief and row.expects (scripts/world_builder_home.html:627-629) and never row.attempt or summary.unmatched_attempts, so a visitor sees the move but not the words behind it, and an attempt that changed nothing shows only as waiting (view gap G17). The plan's inspectable result is that the run page shows each person's own-words attempt. How should the page show them?",
   "blocks": "the plan's inspectable result (docs/plans/open_attempt.md, Actor and result) and S1 being done",
   "resolves_with": "Build and look: show each row's attempt text and reading in the round text and list summary.unmatched_attempts, then open the saved S1 airfield share (evidence/open-attempt/s1-airfield/) in a browser and confirm Sam's refused and unmatched attempts read in his own words.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/model/VIEW_COVERAGE.md:191",
    "scripts/world_builder_home.html:627",
    "docs/plans/open_attempt.md:53",
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
   "question": "S2 runs immediate processes to a fixpoint inside one commit (docs/plans/open_attempt.md, Piece 2). The roadmap and AGENTS.md forbid adding engine capability of World Substrate's own (roadmap/README.md:459), and the roadmap's eligible-work list does not name this work. Is S2 allowed?",
   "blocks": "slice S2",
   "resolves_with": "An argument and Brian's adoption: the forbidden capability is a second engine, scheduler, renderer or cognition loop; a ramification fixpoint is a rule semantics inside the one existing commit (C+ and Event Calculus), with no new loop, clock or scheduler. Brian adopted the plan with that argument on 2026-10-25; record S2 in the roadmap's eligible-work list.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Resolved: Brian's 2026-10-25 'yes' adopted docs/plans/open_attempt.md, whose Current truth section argues the three pieces are rules-layer pieces (none adds an engine, scheduler, renderer or cognition). roadmap/README.md's Exact next action now lists the adopted plan's slices as eligible work (item 4).",
   "sources": [
    "roadmap/README.md:459",
    "docs/plans/open_attempt.md:109"
   ],
   "touches": [
    "knock-on-now",
    "engine"
   ]
  },
  {
   "id": "Q28",
   "short": "Reuse the spill and damage rules",
   "question": "The hand-written mechanisms library already has a vessel-failure spill process and heat damage (src/world_substrate/mechanisms/damage.py:116). Generated worlds start with an empty rule registry and get only the rules writer's declared processes (scripts/scaffold_world.py:209). Should S2's glass chain reuse the library's spill and damage processes, or have the rules writer write its own?",
   "blocks": "how S2's glass chain is built, and whether generated and reference worlds share physics",
   "resolves_with": "Reading the code and one free probe: compare the library processes' read and write paths (entities.<vessel>.condition.value, container, liquid) with what a generated bundle declares; if a generated glass can carry those components, offer the library processes to the build as installable rules and probe the glass chain on the saved airfield fixture; otherwise the rules writer writes declared processes and the library stays reference-only.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/mechanisms/damage.py:116",
    "scripts/scaffold_world.py:209",
    "tests/fixtures/airfield-s1-live.json"
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
    "explain": "Fixed code every people world gets from compile_spec.py; the group-decision family is added when the description has a decision."
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
    "explain": "The one canonical world during a run: entities with typed components, a tick and a revision. Code: src/world_substrate/model.py:382."
   },
   {
    "id": "engine",
    "label": "Engine",
    "kind": "Substrate",
    "explain": "Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. Code: src/world_substrate/engine.py:198."
   },
   {
    "id": "event",
    "label": "Event",
    "kind": "Substrate",
    "explain": "The record of one attempt or process step: status, checks, changes, an id like r14-e00012. Code: src/world_substrate/engine.py:529."
   },
   {
    "id": "move",
    "label": "Move (action)",
    "kind": "Substrate",
    "explain": "Something a person may try; its rule has checks and effects, compiled before use. Code: src/world_substrate/action_authoring.py:49."
   },
   {
    "id": "process",
    "label": "Process",
    "kind": "Substrate",
    "explain": "A rule the world runs by itself each tick when its checks hold. Code: src/world_substrate/engine.py:829."
   },
   {
    "id": "compiler",
    "label": "Compiler",
    "kind": "Substrate",
    "explain": "Turns proposed rules into installed rules and derives what each may read and write. Code: src/world_substrate/action_authoring.py:456."
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
    "explain": "The validated, installed rules of a world, frozen under one id before any run; changing a rule means a new profile. Code: src/world_substrate/profile.py:266."
   },
   {
    "id": "write-scope",
    "label": "Declared write scope",
    "kind": "Substrate",
    "explain": "The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced. Code: src/world_substrate/engine.py:88."
   },
   {
    "id": "causal-trace",
    "label": "Causal trace",
    "kind": "Substrate",
    "explain": "The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run. Code: src/world_substrate/engine.py:529."
   },
   {
    "id": "world-kind",
    "label": "World kind",
    "kind": "Substrate",
    "explain": "Two choices a build makes first: whether the description is about people (people path) or things (causal path), and whether the world is a task, ongoing or open. Code: scripts/world_builder_service.py:113."
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
    "explain": "A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. Code: scripts/world_builder_service.py:418."
   },
   {
    "id": "fingerprint",
    "label": "World fingerprint",
    "kind": "Substrate",
    "explain": "A short hash of the bundle and rules that ties builds, rounds and shares to one world. Code: scripts/world_builder_service.py:381."
   },
   {
    "id": "information",
    "label": "Information item",
    "kind": "Substrate",
    "explain": "A piece of information with a source and per-recipient deliveries; hidden until delivered. Code: src/world_substrate/information.py:57."
   },
   {
    "id": "run-loop",
    "label": "Run loop",
    "kind": "Substrate",
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run. Code: scripts/run_authored_world.py:347."
   },
   {
    "id": "contention",
    "label": "Lost race",
    "kind": "Substrate",
    "explain": "When an earlier move this round changed the state, an open attempt is resubmitted as is at the new revision and only its rule's checks decide it; menu paths resubmit the move if still offered, else ask once more. The refused row names the failed checks, not the event that blocked it. Code: scripts/run_authored_world.py:563."
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
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score. Code: scripts/world_builder_service.py:1541."
   },
   {
    "id": "rules-retry",
    "label": "Rules retry",
    "kind": "Substrate",
    "explain": "A second rules attempt after a rejection or weak score; skipped after 80 s. Code: scripts/world_builder_service.py:263."
   },
   {
    "id": "test-run",
    "label": "Scripted test run",
    "kind": "Substrate",
    "explain": "The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. Code: scripts/world_builder_service.py:1610."
   },
   {
    "id": "run-log",
    "label": "Run log",
    "kind": "Substrate",
    "explain": "One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. Code: scripts/world_builder_service.py:524."
   },
   {
    "id": "readout",
    "label": "Readout",
    "kind": "Substrate",
    "explain": "One AI summary of a run whose every cited event id is checked against the run. Code: scripts/run_readout.py:125."
   },
   {
    "id": "scene-replay",
    "label": "Scene replay",
    "kind": "Substrate",
    "explain": "The page's round-by-round picture of a run: who did what and said what, rebuilt from the run rows; it already quotes a retry's own words. Code: scripts/render_scene_replay.py:398."
   },
   {
    "id": "share",
    "label": "Share link and replay",
    "kind": "Substrate",
    "explain": "A saved run rebuilt from the run log that a visitor replays with no AI calls. Code: scripts/world_builder_service.py:598."
   },
   {
    "id": "budget",
    "label": "Daily allowance",
    "kind": "Substrate",
    "explain": "Visitor $3/day, owner $5/day; spend fails closed. Code: scripts/world_builder_service.py:51."
   },
   {
    "id": "people-world",
    "label": "People world",
    "kind": "Family",
    "explain": "A world built from a description about people: people, information, moments and the fixed people rules. Code: scripts/people_world.py:364."
   },
   {
    "id": "communicate",
    "label": "Communicate rule",
    "kind": "Family",
    "explain": "The reviewed move that delivers an information item to its recipient. Code: spikes/any-scenario-2026-10/compile_spec.py."
   },
   {
    "id": "moment",
    "label": "Scheduled moment",
    "kind": "Family",
    "explain": "A countdown that happens every so many rounds (a weekly meeting, a deadline). Code: spikes/any-scenario-2026-10/compile_spec.py:48."
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
    "explain": "A decision with support, deadline, deployment and review; changed only by fixed rules. Code: spikes/any-scenario-2026-10/compile_spec.py:86."
   },
   {
    "id": "concern",
    "label": "Concern",
    "kind": "Family",
    "explain": "An objection a group holds on a delivered item: open, under remedy or resolved, with answered and remedy_by. Code: spikes/any-scenario-2026-10/compile_spec.py:70."
   },
   {
    "id": "support",
    "label": "Support",
    "kind": "Family",
    "explain": "A member's stance on the decision: none, full or conditional on a concern. Code: spikes/any-scenario-2026-10/compile_spec.py:66."
   },
   {
    "id": "remedy",
    "label": "Remedy",
    "kind": "Family",
    "explain": "A fix of a concern that takes 2 rounds; it can be stopped part-way by the concern's holder objecting. Code: spikes/any-scenario-2026-10/compile_spec.py:332."
   },
   {
    "id": "agenda",
    "label": "Agenda count",
    "kind": "Family",
    "explain": "group_decision.agenda_items: a bare number of matters put before the decision; an item has no content. Code: scripts/people_world.py:279."
   },
   {
    "id": "rollout",
    "label": "Rollout",
    "kind": "Family",
    "explain": "The deployment the world starts when the decision is authorized: 6 rounds, suspended if support falls. Code: spikes/any-scenario-2026-10/compile_spec.py:399."
   },
   {
    "id": "review",
    "label": "Operating review",
    "kind": "Family",
    "explain": "Every 6 rounds after deployment; may reopen each resolved concern once. Code: spikes/any-scenario-2026-10/compile_spec.py:442."
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
    "explain": "The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled. Code: scripts/people_world.py:260."
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
    "explain": "A move the rules say a person can try now, with its open fields; the page a decider picks from or an attempt is read against. Code: src/world_substrate/engine.py:352."
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
    "explain": "What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens. Code: src/world_substrate/attempt.py:149."
   },
   {
    "id": "attempt-reading",
    "label": "Attempt reading",
    "kind": "Substrate",
    "explain": "The interpreter's typed reading of an attempt: one move kind, the entity for each role and the quoted words behind it; refused if it names unknown things or words not said. Code: src/world_substrate/attempt.py:81."
   },
   {
    "id": "unmatched-attempt",
    "label": "Unmatched attempt",
    "kind": "Substrate",
    "explain": "An attempt no move kind covers: it changes nothing, the person learns nothing came of it, and the run lists it for the rules writer. Code: src/world_substrate/attempt.py:25."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Substrate",
    "explain": "What one actor sees this round: the fields its senses and position allow, never the whole world. Code: src/world_substrate/engine.py:235."
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
    "kind": "Theory",
    "explain": "Plan S2: a process marked 'immediately' runs again and again inside one moment until nothing more changes (a glass falls, breaks, someone hears it). Code: none yet."
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
    "explain": "A composite reading (two give events make one exchange) derived from committed events, never a second effect. Code: src/world_substrate/exchange.py:20."
   },
   {
    "id": "mechanisms",
    "label": "Mechanisms library",
    "kind": "Reference",
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds start with an empty registry (Q28). Code: src/world_substrate/mechanisms/__init__.py:3."
   },
   {
    "id": "kitchen",
    "label": "Kitchen flagship",
    "kind": "Reference",
    "explain": "The replicated scarce-knife watched world: hand-written rules of its own on the ordinary Engine. Code: reference_worlds/kitchen/mechanics.py."
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
    "id": "Q4",
    "label": "Q4: Notice only as good as the words",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether E2 (a fix carries its substance) holds for every world or only when residents happen to write specific words."
   },
   {
    "id": "Q9",
    "label": "Q9: Test run too short for some tasks",
    "kind": "AgentQuestion",
    "explain": "Blocks: builds wrongly scored as failing and the rewrite spend they cause."
   },
   {
    "id": "Q12",
    "label": "Q12: When a people-world run ends",
    "kind": "BrianQuestion",
    "explain": "Blocks: how long visitors watch a run, and its cost."
   },
   {
    "id": "Q14",
    "label": "Q14: Agent-harness build not live",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether build repairs come from a harness or from the rules retry (Q1)."
   },
   {
    "id": "Q15",
    "label": "Q15: Repository format files not yet added",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether the repo-format check passes."
   },
   {
    "id": "Q16",
    "label": "Q16: Goals skip the package gate",
    "kind": "BrianQuestion",
    "explain": "Blocks: whether the next goal can again run without a current system model and question list."
   },
   {
    "id": "Q17",
    "label": "Q17: Offline pipeline views",
    "kind": "BrianQuestion",
    "explain": "Blocks: whether work goes into the offline pipeline at all."
   },
   {
    "id": "Q22",
    "label": "Q22: Effects no rule covers",
    "kind": "BrianQuestion",
    "explain": "Blocks: slice S4 of docs/plans/open_attempt.md, and how alive a world feels when its rules are thin."
   },
   {
    "id": "Q26",
    "label": "Q26: Run page hides own-words attempts",
    "kind": "AgentQuestion",
    "explain": "Blocks: the plan's inspectable result (docs/plans/open_attempt.md, Actor and result) and S1 being done."
   },
   {
    "id": "Q28",
    "label": "Q28: Reuse the spill and damage rules",
    "kind": "AgentQuestion",
    "explain": "Blocks: how S2's glass chain is built, and whether generated and reference worlds share physics."
   },
   {
    "id": "agenda",
    "label": "Agenda count",
    "kind": "Concept",
    "explain": "group_decision.agenda_items: a bare number of matters put before the decision; an item has no content."
   },
   {
    "id": "attempt",
    "label": "Attempt (in own words)",
    "kind": "Concept",
    "explain": "What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens."
   },
   {
    "id": "build",
    "label": "Build",
    "kind": "Concept",
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score."
   },
   {
    "id": "concern",
    "label": "Concern",
    "kind": "Concept",
    "explain": "An objection a group holds on a delivered item: open, under remedy or resolved, with answered and remedy_by."
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
    "explain": "A decision with support, deadline, deployment and review; changed only by fixed rules."
   },
   {
    "id": "harness-build",
    "label": "Build in an agent harness",
    "kind": "Concept",
    "dashed": true,
    "explain": "Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it."
   },
   {
    "id": "knock-on-now",
    "label": "Knock-on that runs now",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan S2: a process marked 'immediately' runs again and again inside one moment until nothing more changes (a glass falls, breaks, someone hears it)."
   },
   {
    "id": "mechanisms",
    "label": "Mechanisms library",
    "kind": "Concept",
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds start with an empty registry (Q28)."
   },
   {
    "id": "notice",
    "label": "Finished-task notice",
    "kind": "Concept",
    "explain": "What the other people a finished task names are told, in the starter's own words about the work."
   },
   {
    "id": "rules-retry",
    "label": "Rules retry",
    "kind": "Concept",
    "explain": "A second rules attempt after a rejection or weak score; skipped after 80 s."
   },
   {
    "id": "run-loop",
    "label": "Run loop",
    "kind": "Concept",
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run."
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
    "id": "Q4-notice",
    "source": "Q4",
    "target": "notice",
    "label": "bears on"
   },
   {
    "id": "Q4-task",
    "source": "Q4",
    "target": "task",
    "label": "bears on"
   },
   {
    "id": "Q4-concern",
    "source": "Q4",
    "target": "concern",
    "label": "bears on"
   },
   {
    "id": "Q9-test-run",
    "source": "Q9",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q12-run-loop",
    "source": "Q12",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q12-group-decision",
    "source": "Q12",
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
    "id": "Q17-build",
    "source": "Q17",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q22-build",
    "source": "Q22",
    "target": "build",
    "label": "bears on"
   },
   {
    "id": "Q22-run-loop",
    "source": "Q22",
    "target": "run-loop",
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
    "id": "Q28-mechanisms",
    "source": "Q28",
    "target": "mechanisms",
    "label": "bears on"
   },
   {
    "id": "Q28-knock-on-now",
    "source": "Q28",
    "target": "knock-on-now",
    "label": "bears on"
   },
   {
    "id": "Q28-gen-rules",
    "source": "Q28",
    "target": "gen-rules",
    "label": "bears on"
   }
  ],
  "layout": {
   "direction": "RIGHT"
  }
 },
 "context_diagrams": [
  "C4Context\n  title World Substrate system context\n  Person(author, \"World author\", \"Describes a world, reviews and approves its rules, watches runs\")\n  System(ws, \"World Substrate\", \"Compiler, approval gate, Engine, World Builder service, projections\")\n  System_Ext(llm, \"LLM providers\", \"Reached only through llm_client; proposals and move choices\")\n  System_Ext(runtimes, \"Concordia / Mesa / PDDL\", \"Resident cognition, grids and sweeps, plan validation\")\n  System_Ext(host, \"Cloudflare + personal VPS\", \"Serve the pages and the API\")\n  Rel(author, ws, \"Describes, approves, inspects\")\n  Rel(ws, llm, \"Requests proposals and choices\")\n  Rel(runtimes, ws, \"Submit intents; read observations\")\n  Rel(host, ws, \"Hosts\")\n",
  "C4Container\n  title World Substrate containers\n  Person(author, \"World author\")\n  Container(builder, \"World Builder service\", \"scripts/world_builder_service.py\", \"Approval gate, budget ledger, run log\")\n  Container(compiler, \"Authoring compiler\", \"src/world_substrate/action_authoring.py\", \"Proposal to rules with derived authority\")\n  Container(installer, \"Installer and run loop\", \"scripts/run_authored_world.py + profile.py\", \"Freezes the approved profile, runs residents\")\n  Container(engine, \"Engine\", \"src/world_substrate/engine.py\", \"Atomic commit or refusal, write scopes, events\")\n  Container(projection, \"Projections\", \"projection.py, information.py\", \"Live view and observer visibility from canonical state\")\n  Rel(author, builder, \"HTTP\")\n  Rel(builder, compiler, \"Compile and review\")\n  Rel(builder, installer, \"Run approved mechanics\")\n  Rel(installer, engine, \"Submit envelopes, tick processes\")\n  Rel(engine, projection, \"Snapshot and event deltas\")\n"
 ],
 "disagreements": [
  "**Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).",
  "**The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there."
 ],
 "next_plan": "---\nplan_id: \"open-attempt\"\ndependencies: []\ndependencies_reviewed: \"2026-10-25\"\nplanning_path: durable_solo\nplanning_path_ref: docs/plans/open_attempt/path-decision.json\nmethod_conformance_receipt: docs/plans/open_attempt/conformance-receipt.json\nstatus: adopted\ngoal:\n  outcome: \"World Builder residents say in their own words what they physically try, instead of picking from a list; the world's rules decide what happens, knock-on effects run to the end inside the same moment, and a person's recorded skill (never how expert their words sound) decides how a risky attempt turns out.\"\n  canonical_example: \"A World Builder world generated from 'A small airfield office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown'. In one run Sam tries to walk through the wall and nothing happens, with the wall named as the cause; someone knocks the glass off the desk and in the same event chain it falls, breaks, the water spills and the person in the next room hears it; Sam tries to fly the helicopter and a recorded roll from Sam's piloting level 0 gives a crash or a rough landing, never a clean flight from good wording.\"\n  forbidden_substitutes: \"hand-edited specs, rules or runs; an interpreter that decides success; outcomes written by an LLM rather than by an installed rule; a roll whose dice come from the attempt's wording; a scripted move presented as an attempt; Waltzman-specific code paths; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run.\"\n  boundaries: \"world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change; existing saved worlds still replay unchanged; owner allowance only, visitor allowance stays $3/day; free replays of saved worlds before any paid run; publish-checker before anything new goes public.\"\n  done_when: \"Acceptance checks A1-A9 below pass, each judged from the full trace of the run it names.\"\n  do_not_gate_on: \"letting an AI game master invent effects for attempts no rule covers (Decision D2, deferred); organisations, the decider spectrum and thinking-as-effector (later designs); a clingo cross-check of the reaction rules; Brian's review of a run.\"\n  stop_after: 3\nconflict_surfaces:\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/open-attempt/review-page/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/concordia_residents.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/attempt.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open-attempt.goal.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.verdicts.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/planning-package.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_readout.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/index.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/architecture/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: Makefile, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: lefthook.yml, access: write}\n---\n# Plan: open attempts, knock-on effects that run to the end, and skill rolls\n\nPlanning package: docs/planning/open-attempt/planning-package.json\n\nReview page: [proposals/open-attempt/review-page/](../../proposals/open-attempt/review-page/index.html), live at\n<https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/>.\n\n## Actor and result\n\n**Actor:** a World Builder visitor (and Brian as owner) who pastes a scenario and watches the\ngenerated people act. **Result they can inspect:** the run page and its build record show each\nperson's own-words attempt, what the rules made of it, and why it worked, failed or did nothing.\n**Stable example:** the airfield office in the front matter's `canonical_example`: Sam walks into\nthe wall and is refused with the wall named; the glass chain runs in one moment; Sam's untrained\nflight rolls two dice keep-lower.\n\n## Project outcome\n\nProject outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top, rigorous causal engine underneath; the World Builder is the visitor-facing surface). This plan serves that actor directly: the roadmap's \"user describing a world\" is the\nWorld Builder visitor of the Actor section. **Recurring job and baseline:** a visitor describes a world and\nwatches its people act; before S1 each person could only pick from moves the rules already allowed, so\nimpossible attempts (the wall) never appeared. S1 (merged at `fe8c492`, #239) lets residents say attempts in\ntheir own words, and its live run (`evidence/open-attempt/s1-airfield/`, #247) shows residents acting every round; the\nwall refusal and the untrained flight have not yet been seen in a live run, and knock-on chains (S2) and untrained\nfailures (S3) still never appear. **Inspectable result this plan\ndelivers:** the run page and build record of the airfield world showing the wall refusal, the glass chain\nand the rolled crash. **Stage and investment boundary:** prototype stage; three slices, each one pull\nrequest and at most $3.00 of owner allowance; no new service, engine or repository.\n\n## Outcome step\n\nOutcome probe: `roadmap/README.md#canonical-outcome-probe`\nObserved: `evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md`\nStep: step 3 of the probe, \"the residents act in the generated world each round, and the installed rules decide each effect\"\nClass: vertical\n\nEach slice changes that step end to end (generator, resident, engine, page) and ends in a live traced run.\n\n## Why, in one example\n\nBefore S1 a World Builder resident was handed a list of moves the rules already allowed and picked one\n(the menu reply's `action_id` is that list plus `wait`, still so for the menu schema at\n`scripts/concordia_residents.py:96`). So nobody ever walked into a wall: the wall never appeared as a\nchoice. S1 replaced that with an own-words `attempt` (built; see the slice table). Brian, 2026-10-24: a\nperson should be able to \"attempt to walk through a wall but these should not be successful\", and\nsomeone who \"dont know how\" to fly a helicopter \"should probably crash it\". The survey\n([flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md),\nBrian's \"yes\" on 2026-10-25 to this design) found three pieces missing from World Substrate and\nnamed the established method to copy for each. This plan designs those three, in the order they\ndepend on each other.\n\n## Current truth (read from code before S1, 2026-10-25, main 63caf4c; S1 rows added after it merged at fe8c492)\n\n| Have | Where |\n| --- | --- |\n| The rules list what a person can do now (an affordance page) | `Engine.discover`, `src/world_substrate/engine.py:352` |\n| A move whose checks fail is refused with the failed check recorded, no partial change | `Engine.apply` / `_reject`, `engine.py:582`, `:749` |\n| A move of a kind no rule knows is recorded as unsupported, nothing changes | `Engine.submit`, `engine.py:452`; `UnsupportedAction`, `rules.py:288` |\n| Meaning (sense and roles) is kept apart from mechanics | `SemanticBinding`, `src/world_substrate/semantic.py:15`; Decision 003 |\n| Things the world does by itself run once per round, each citing its causes | `Engine.advance`, `engine.py:786`; `DeclaredProcess`, `action_authoring.py:245` |\n| Who hears or sees what is limited by the world | `world_substrate.information` |\n| No randomness anywhere in rules | no `random`/`seed` in `engine.py` or `action_authoring.py` |\n| S1: a resident answers `attempt` in its own words instead of an offered `action_id` | `OPEN_SCHEMA`, `scripts/concordia_residents.py:45` |\n| S1: one typed call reads the attempt into one action kind and its fields, with no outcome field | `interpret`, `src/world_substrate/attempt.py:149`; `read_interpretation`, `:81` |\n| S1: an unmatched attempt changes nothing and is listed in the build record | `UNMATCHED_KIND`, `attempt.py:25`; `unmatched_attempts`, `scripts/run_authored_world.py:800` |\n| S1 (Q23): generated worlds have places, ways with a passable flag, and a move that checks the way | `scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`; `evidence/open-attempt/q23/README.md` |\n| After S1 (#242, `87b4aa2`): the World Builder page sends open-attempt residents whenever AI chooses the moves | `scripts/world_builder_home.html` on main; `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md` on main |\n\nDecision 006 limits World Substrate to the governed-rules layer. All three pieces below are rules-layer\npieces: one turns words into a typed move, one runs rules to a fixpoint inside one commit, one adds a\nrecorded roll to a rule. None adds an engine, scheduler, renderer or cognition of our own.\n\n## The three pieces\n\n### Piece 1. Open attempt (copy: Inform 7 \"try\" plus Voyager-style attempts sent to an engine)\n\n1. **Decide.** The resident's reply keeps `belief`, `expected_effect`, `work` and `reasoning`, and\n   replaces `action_id` with `attempt`: one sentence of what they physically do, with their body,\n   voice or hands (\"walk east through the wall into the hangar\"). The affordance page is still shown,\n   as \"things you know you can do here\", but it no longer limits the answer.\n2. **Interpret.** One typed light-model call (`llm_client`, the World Builder's current model, low\n   effort) reads the attempt and the world's action kinds with their roles, and returns either\n   `{kind, roles: {role: entity_id}, quoted_span per role}` or `{unmatched: true, nearest_kind,\n   why}`. Its schema has **no success field**: it says what is being tried, never whether it works.\n   The result is recorded as the command, so replay never calls the model again.\n3. **Check.** The matched move goes through `Engine.submit` unchanged. The wall case is an ordinary\n   refusal: the generated `move` rule's \"the way between is open\" check fails (S1's canonical world must show the rules writer gave `move` that check; if it did not, that gap is fixed in the rules writer, never by hand-editing the world), and the event names the wall.\n4. **Unmatched fallback (v1).** An attempt that matches no kind is recorded through the existing\n   unsupported path: nothing in the world changes, the person sees \"you try to …; nothing comes of\n   it\", and the build record lists every unmatched attempt so the rules writer can add a rule in the\n   next build. Letting an AI game master invent an effect is Decision D2, deferred.\n5. **Who notices.** Unchanged: `world_substrate.information` decides who perceives the result.\n   Shouting to someone overseas succeeds as speech and reaches only those in hearing range.\n\n### Piece 2. Knock-on effects that run to the end (copy: C+ / Event Calculus ramification)\n\nA process may declare `timing: \"immediately\"` (default stays `\"each_round\"`, so every existing world is\nunchanged). After a move or round event commits its candidate state, the engine runs every immediate\nprocess whose `due()` holds on the new state, then again on the state that produces, until none is\ndue. Rules:\n\n- each (process, entity) pair fires at most once per moment, so a reaction cannot feed itself;\n- at most 32 reactions per moment; going over refuses the whole moment visibly and changes nothing\n  (the existing \"no partial mutation\" invariant);\n- every reaction event cites its parent event as a hard causal parent, so the chain is readable;\n- order inside one wave is the registry's fixed order, recorded in the events.\n\nGlass: `push glass` moves it off the desk → `falls` (unsupported object above floor) → `breaks`\n(fragile and fell) → `spills` (container broke while holding water) and, also from `breaks`, a `crash sound` event. Five events in\none moment: fall cites push, break cites fall, and spill and sound both cite break. The person next\ndoor then learns of the sound through `information`; that is an observation, not a sixth event.\n\n### Piece 3. Skill rolls (copy: Blades in the Dark action roll, GURPS defaults, progress clocks)\n\nAn action mechanic may declare `roll: {skill: <actor path>, position: controlled|risky|desperate,\noutcomes: {full: [effects], partial: [effects], fail: [effects]}}`.\n\n- Hard gates first: the ordinary checks (holds the key, knows the number, is in the cockpit) run\n  before any roll. No roll without stakes: a mechanic with no `fail` effects may not declare a roll.\n- Dice: as many six-sided dice as the recorded skill level; level 0 rolls two and keeps the lower\n  (GURPS-style default for the untrained). Highest die 6 = full, 4-5 = partial, 1-3 = fail.\n  Position picks which outcome list the rules writer gave for \"partial\" and \"fail\".\n- The dice come from a seeded generator (`seed = hash(run_seed, event_id)`), and the values are\n  recorded in the event, so a replay reproduces them and a reader can check them.\n- Only the skill path is read. The attempt's wording never reaches the roll.\n- Long tasks: a roll's outcome effects may write the counter field a process already reads (the world field behind `Engine._progress`, `engine.py:321`, which only reports it), so a partial result moves a task's counter less than a full one, like a Blades progress clock.\n\nHelicopter: Sam (piloting 0) is in the cockpit (gate passes), rolls two dice, keeps the lower; on\n1-3 the `fail` effects crash the helicopter, damaging it and injuring Sam, and Piece 2 carries on\n(fuel leaks, alarm sounds, the ground crew hears it).\n\n## Requirements\n\nWhat Brian asked, plus what the plan's own claims imply; each row names its check in the acceptance table below. Status per check: S1 is built (merged `fe8c492`, #239): A1 (`tests/test_open_attempt.py`) and A8 (`scripts/check_project.py`) were checked in its pull request, and the owner-allowance airfield run with residents (`evidence/open-attempt/s1-airfield/`, 2026-10-26, merged in #247)\njudged A4 and A9 passing (its TRACE_READ.md passes `scripts/check_trace_reads.py` and samples ordinary attempts, which is R1's trace check) and left A2 and A3 planned and not yet run: the live run never reached the helicopter or the wall, so both run next on the saved airfield world `tests/fixtures/airfield-s1-live.json` (see the S1 live result below); A5-A6 planned in S2; A7 planned in S3; A8 planned in every slice\n(run on each merge commit); A9 planned in S1 (open-attempt part) and completed in S3 (full chain). None is\ndeferred. The claimed property is the requirement itself (an impossible attempt is refused with its cause,\na chain finishes, skill sets the dice), never a count of passing tests.\n\n\n| Id | Requirement (source) | Fails when | Control | Status |\n| --- | --- | --- | --- | --- |\n| R1 | Residents can try anything their body can do (Brian 2026-10-24) | The interpreter quietly maps \"fly the helicopter\" to a safe move | `quoted_span` per role; A2 negative fixture; TRACE_READ samples ordinary attempts | Passing in part: the S1 live run TRACE_READ samples ordinary attempts and passes; A2 planned and not yet run (fixture run next) |\n| R2 | The world, not the interpreter, decides what happens (Decision 003; AGENTS.md \"installed mechanics alone\") | The interpreter refuses or judges success | No success field in its schema (A1); refusals only come from rule checks | Passing: A1 in #239 |\n| R3 | Impossible attempts fail with a cause (Brian 2026-10-24) | A wall attempt is dropped instead of recorded | A3: refused event names the failed check | Planned and not yet run: A3 on the saved airfield world next |\n| R4 | Knock-on effects run on their own to the end (Brian 2026-10-24) | A chain stops after one step, or loops | A5, A6: once-per-pair rule, cap of 32, whole moment refused on overflow | Planned and not yet run (S2) |\n| R5 | Skill decides risky outcomes, not wording (Brian 2026-10-24: LLM knowledge must not leak) | Dice depend on the attempt text, or outcomes are written by the model | A7: same attempt, skill 0 versus 3, different dice pools; dice only from seed | Planned and not yet run (S3) |\n| R6 | Saved worlds and replays keep working (AGENTS.md invariants) | Replay calls the model or rerolls | A8: every retained replay test unchanged; rolls and interpretations replay from records | Passing at the S1 merge (A8); planned for S2 and S3 merges |\n| R7 | Every run is readable in full (core rules) | An interpretation or roll is missing from the trace | A9: run-log.jsonl has each interpreter call's trace id, each roll's dice; TRACE_READ.md passes | Passing for S1 (A9 on the live run); full chain planned in S3 |\n\n## Acceptance checks\n\n| Id | Check | Run and what its trace must show |\n| --- | --- | --- |\n| A1 | Interpreter schema has no success or outcome field | `pytest tests/test_open_attempt.py::test_schema_has_no_outcome` output |\n| A2 | \"Fly the helicopter to the coast\" never binds to `move` | fixture run on the generated airfield world; the command records `kind: pilot`, `quoted_span` \"fly the helicopter\" |\n| A3 | Walking through the wall is refused, wall named | the canonical run's event for Sam's wall attempt: `status: refused`, failed check names the wall entity. Q23 (generated worlds have walls) resolved: `evidence/open-attempt/q23/README.md` |\n| A4 | An unmatched attempt changes nothing and is listed | the canonical run's build record `unmatched_attempts` list, and the event's before/after equal |\n| A5 | The glass chain completes in one moment | canonical run: one moment with push, fall, break, spill and sound events; fall cites push, break cites fall, spill and sound cite break. Judged separately: the neighbour's observation for that moment includes the sound |\n| A6 | A self-feeding reaction is refused whole | `tests/test_open_attempt.py` loop fixture: status refused, world unchanged, cap reason recorded |\n| A7 | Skill, not wording, sets the dice | fixture: identical attempt text, piloting 0 and 3; events show 2-keep-lower versus 3 dice, seed recorded |\n| A8 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with these replay tests named passing in the quoted output: `test_action_envelopes` (unsupported and malformed envelopes replay), `test_first_fill.test_fill_tick_and_replay_match_exactly`, `test_greenhouse_zero_review.test_replay_regenerates_exactly_through_generic_renderer`, `test_castaway_zero_review.test_zero_review_replay_regenerates_exactly` |\n| A9 | The canonical run is fully traced | `evidence/open-attempt/<run>/run-log.jsonl` plus `TRACE_READ.md` passing `scripts/check_trace_reads.py`; read by the implementing agent before reporting |\n\n## Success and disproof\n\nThe plan claims three properties: (1) residents state any physical attempt and only installed rules\ndecide its effect (R1-R3, checked by A1-A4); (2) knock-on effects run to the end inside one moment or the\nmoment is refused whole (R4, A5-A6); (3) recorded skill, not wording, decides risky outcomes (R5, A7);\nwith replay unchanged (R6, A8) and every run fully readable (R7, A9).\n\n**Success:** A1-A9 pass, each judged from the full trace of the run it names. **Disproof:** any one\nof these in the canonical run's trace: an interpreter output carrying a success or outcome; a wall\nattempt that changes the world or is refused without naming the wall; a pilot attempt by a level-0\nperson that ends in a clean flight; dice whose seed is not `hash(run_seed, event_id)`; a replay that\ncalls a model. Trace review: the implementing agent reads every refused, unmatched and rolled attempt\nand a sample of ordinary ones in the named run's `run-log.jsonl` and writes `TRACE_READ.md`; each criterion\nA1-A9 is expected `pass`. Runs are named in order: `evidence/open-attempt/s1-replay/` (free replay of a\nsaved world), `evidence/open-attempt/s1-airfield/` (first owner-allowance run, judged for A2-A4 and A9),\n`evidence/open-attempt/s2-airfield/` (A5), `evidence/open-attempt/s3-airfield/` (A7 and the full A9);\nA1, A6 and A8 are judged from the named pytest and `check_project.py` output saved beside each run.\n\n## When a run fails or surprises us\n\nThis is separate from the anticipated failure modes in the Requirements table: it covers what we did not\nforesee. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,\nintermediate stages (interpretation, checks, reactions, rolls) and the final output (build record, page)\nbefore choosing a fix; cite where it diverged; classify it evidence absent, unused or\ncontradicted, invalid expectation, or unresolved. An unresolved cause permits investigation, not a\nrepair. A repair is verified by a new traced run whose `TRACE_READ.md` links the original run and the divergence it\nfixes; the original stays. Never rerun until a behavior\nappears and report only that run. Review completeness never changes the run verdict: a run's pass or fail\ncomes from its trace against A1-A9, and an incomplete review leaves the claim unreported, not passed.\n\n## Slices, in order\n\n| Slice | What lands | State | Checks |\n| --- | --- | --- | --- |\n| S1 | Close Q23 (rules writer makes places, ways and the wall check), then open attempt: resident `attempt` field, interpreter, unmatched fallback, build-record list | built, not done: merged `fe8c492` (#239); page fix `87b4aa2` (#242); live run `evidence/open-attempt/s1-airfield/` (#247): A4 and A9 pass, A2 and A3 not exercised; the run page does not yet show own-words attempts (Q26) | A1, A8 at merge; free replay `evidence/open-attempt/s1-replay/replay.txt` exit 0; A4, A9 on the owner-allowance run; still owed: A2 and A3 on the saved world `tests/fixtures/airfield-s1-live.json`, and Q26 |\n| S2 | `timing: immediately` processes run to a fixpoint inside one moment | fully_specifiable_now | A5, A6, A8 |\n| S3 | `roll` on action mechanics, seeded and recorded; rules writer prompt can declare it | fully_specifiable_now | A7, A8, then the full canonical run for A9 |\n| S4 | AI game master for unmatched attempts | human_decision_required (D2) | none until decided |\n\n**Kinds the canonical airfield world must contain** (generated, never hand-written): `move` between\nplaces with a check that the way between is open (the wall), `push` an object, `pilot` a craft to a\nplace, and `speak`. Before S1, generated worlds were economy-style (`make-leads`, `shape-slats`) and\nnothing in the rules writer asked for places, ways between them or blocking. That was open question\n**Q23**, S1's first step, resolved 2026-10-25 by a generic fix to the bundle contract and rules writer\n(`scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`): the regenerated airfield\nworld refuses the walk through the wall with \"the way is passable\" failed\n(`evidence/open-attempt/q23/after-fix/probe.txt`). Known limit, open question **Q25**: a way works from its\nfirst place to its second only.\n\n**S1 live result** (`evidence/open-attempt/s1-airfield/TRACE_READ.md`, owner allowance, deployed `87b4aa2`, 9 rounds,\n65 model calls, $0.0319): residents moved every round; A4 passes live (15 refused or unmatched attempts each changed\nnothing and every unmatched one is listed with the interpreter's nearest move); A2 and A3 were not exercised, because\nthe build left the helicopter unreachable: everyone but the mechanic starts in the office, the brick wall is the only\nway to the hangar and is not passable, the builder's own test runs said the practice flight was never possible and the\nbuild was accepted anyway (#244). Two smaller defects were filed: a refusal reason reads as a fact (\"you are the\ndispatcher\") rather than a requirement (#245), and the readout chose the goods-flow lens for a training world (#246).\nS1 is therefore built but not done. Next: A2 as a fixture run of \"fly the helicopter to the coast\" and A3 as an\ninterpreted attempt at the wall, both on the saved world `tests/fixtures/airfield-s1-live.json` (free, no new build),\nthen Q26 (the run page shows each attempt in its owner's words).\n\nEach slice is its own pull request and leaves a working World Builder. S1 alone already lets a\nresident walk into the wall. The rules writer (`scripts/generate_causal_model.py`, its process and mechanic schemas) learns `timing` in S2 and\n`roll` in S3; until then generated worlds simply do not use them.\n\n## Decisions\n\n- **D1 (made, technical):** the interpreter is one typed light-model call per attempt, not a parser\n  and not the resident's own model. Reason: words to (kind, roles) is meaning, which our rules say\n  is never read with regex; a separate call keeps the resident from steering its own interpretation.\n  Cost: one extra small call per attempt, measured in S1's first run against the visitor $3/day cap.\n- **D2 (Brian's call, deferred):** for attempts no rule covers, should an AI game master be allowed\n  to invent a rough effect, marked \"coarse\" in the record? Recommendation: not now. v1 says \"nothing\n  comes of it\" and lists the attempt for the rules writer. If not answered, v1 stays.\n- **D3 (made, technical):** reactions are a `timing` field on the existing process declaration, not a\n  new rule type, so they reuse its selector, checks, effects, linked participants and write scopes.\n\n## System model\n\n- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a refused attempt changes nothing), RULE-PROJECTION-FROM-CANONICAL-ONLY (the page shows only recorded events). Adds: `attempt interpretation` (adds), `unmatched_attempts` (adds), `timing` (adds), `roll` (adds).\n- Scope: the system model is this repository's own (world-substrate only, linked from the documentation entry point\n  `docs/wiki/README.md`), not a shared model. The one shared artefact it touches is the\n  scientific-hypergraph kernel, which it reads at a pinned revision and never changes; the mapping\n  onto it lives here (`docs/model/metamodel-mapping.json`).\n- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) (built by `scripts/build_metamodel.py`) holds the\n  world's own types this plan relies on (action kind, role, check, effect, process, affordance, decider,\n  attempt, attempt reading, unmatched attempt, event, observation) and the two it plans (same-moment\n  knock-on, skill roll), each mapped onto the scientific-hypergraph kernel at `7b0638f`. Its reuse-gate\n  table records the formalisms checked before minting them (bounded-design typed-relational reference,\n  rule 1); AlgebraicPetri and TypeDB were open question Q24, resolved by argument as compose. S2 and S3 flip their type to built in that\n  table in the same pull request.\n- Not changed, and why: actors, places, information reach (`world_substrate.information`), tasks and\n  the budget ledger keep their current model elements; this plan only changes how a move is chosen,\n  how reactions run and how a mechanic resolves, so their definitions stand. RULE-BUDGET-FAILS-CLOSED,\n  RULE-FROZEN-PROFILE and RULE-DERIVED-AUTHORITY are relied on unchanged.\n- Views: [docs/model/VIEW_COVERAGE.md](../model/VIEW_COVERAGE.md) records which view shows each element; each slice adds its rows there. Per element:\n  - `attempt interpretation` (`AttemptReading`): `owner_run_log` shows it (`GET /runs?full=1` keeps the\n    transcript, `scripts/world_builder_service.py:1011`); `home` does not yet, gap G17, now open question Q26 (S1 is not done until it closes).\n  - `unmatched_attempts`: `owner_run_log` shows it in the run summary (`GET /runs` keeps `summary`,\n    written at `scripts/run_authored_world.py:800`); `home` does not yet, gap G17.\n  - `timing` and the reaction wave (S2): `round_replay` and `scenario_state_panel` must show each\n    reaction event with its parent; S2 adds the row.\n  - `roll` (S3): `scenario_state_panel` must show each roll's seed and dice; S3 adds the row.\n- The trace must show, per element: the command's `interpretation` record with the interpreter's trace id; the build record's `unmatched_attempts`; reaction events citing their parent; each roll's seed and dice.\n- S1 adds an `attempt interpretation` record\n  (command field) and the `unmatched_attempts` build-record list; S2 adds the `timing` process field and\n  the reaction-wave events; S3 adds the `roll` mechanic field and the event's `roll` record. Each slice\n  updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request,\n  and the drift test must fail on a renamed field before it passes.\n## Trace visibility\n\n- Each run's `run-log.jsonl` records: the inputs (scenario text, world bundle hash, run seed); every step\n  (round, actor, attempt text); each model call (resident, interpreter, rules writer) with its prompt\n  messages, arguments, typed result and `llm_client` trace id; the model's reasoning where it returns it\n  (the resident's `reasoning` field); every engine event with before/after, failed checks, reaction parent\n  and dice; and the output (build record, page JSON). Kept for ordinary runs, not only failures. No slice is a pure document edit, so no slice\nclaims the no-run exemption; this adoption commit alone is document-only and runs nothing.\n- How to open one: `evidence/open-attempt/<run>/run-log.jsonl` is one JSON object per line (`jq . <file>`);\n  the live run's page links its share id, and `llm_client` trace ids open in its trace store\n  (`python -m llm_client traces --trace-id <id>`). Who reads and when: the implementing agent reads every run's\n  trace before reporting that slice, including the free replay and fixture runs; every failure or surprise\n  in full, and at least five ordinary attempts per run chosen across rounds and actors. This plan has no runs\n  other than World Builder runs and the test suite, whose output is saved beside each run.\n- World Builder runs keep `run-log.jsonl` (every request, interpreter and resident call with\n  `llm_client` trace ids, every event with dice) beside the run; `TRACE_READ.md` per round. The\n  implementing agent reads every refused, unmatched and rolled attempt in the canonical run and a sample\n  of ordinary ones before reporting.\n## Capability reuse\n\nNo catalogue entry fits, because `reuse_candidates.yml` and\n  `capability_registry.yml` hold approvals, notifications, scheduling, document-to-text and search\n  wrappers, none of which interpret actions or run rules. Model calls go through the workspace's shared\n`llm_client` (listed in `~/code2/workspace/docs/capabilities.md`, not a catalogue entry). No new\ncross-project capability is added; the interpreter's first and only consumer is the World Builder run loop.\n\n## Prior art and ownership\n\nDisposition per piece, from [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md): open attempt **extends** the existing unsupported-action path and `Engine.submit` (copying Inform 7 \"try\" and Voyager-style attempts); knock-on effects **extend** `DeclaredProcess` (copying C+/Event Calculus ramification); skill rolls **extend** `DeclaredActionMechanic` (copying Blades in the Dark and GURPS defaults). Owner: World Substrate's rules layer (Decision 006). Parallel-implementation check: no second command path, engine or scheduler; every attempt still enters through `Engine.submit`, and `grep -n \"def submit\" src/world_substrate/engine.py` stays one hit.\n\n## LLM call boundary\n\nCall graph per round: resident call (one per actor, existing) -> attempt interpreter call (one per attempt,\nnew, after the resident's reply, before `Engine.submit`) -> no further model call; rules, reactions and\nrolls are code. The rules writer's calls (existing, at build time) change only in prompt and schema.\nProvider: OpenRouter, model `openrouter/openai/gpt-6-luna` (the World Builder's `DEFAULT_MODEL`,\n`scripts/run_authored_world.py:37`). Spend authority: Brian's owner allowance, granted for this plan on\n2026-10-25. An interpretation becomes authoritative only as a recorded command after an authentic live\nrun; fixtures may use recorded interpretations but are never reported as live.\n\nExisting resident call (unchanged boundary except the field): typed reply `{belief, attempt, expected_effect,\nwork, reasoning}`; `attempt` replaces `action_id`; it has no success field either; the reply is recorded in\n`run-log.jsonl` with its trace id and is never re-read by rules or replay; a failed or malformed reply records\nthe actor as waiting, as today.\n\nOne new call: the attempt interpreter, through `llm_client`, typed output (`kind`, `roles`, `quoted_span` or `unmatched`, `nearest_kind`, `why`), no success field. Its output is recorded as the command and never re-read by rules or replay; it has no authority to change state, and promotion of its output to authority is refused by construction (only `Engine.submit` writes). Failure: a malformed or failed call records the attempt as unmatched with the error, never a guessed move.\n\n## Irreversible actions and spend\n\nNothing irreversible is planned: merges are pull requests (revert with git) and deploys of World Builder's\nown service are redeployable from the previous commit. Boundary: no deletion of saved worlds or run\nrecords, no outreach, no change to other repositories. If a step would be irreversible, it stops and goes\nto Brian first (core rules: \"Ask first only for irreversible actions\"); authorization for everything in\nthis plan is Brian's 2026-10-25 \"yes\". Containment: the deploy is checked through the health endpoint's\nbuild commit and rolled back to the prior commit if it fails. Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 across S1\n(stop and report if a run would exceed it, enforced by the run's `max_budget`); the visitor allowance\nstays $3/day.\n\n## Uncertainties\n\nThe material uncertainties, listed in full as of 2026-10-26: each below could change a slice's scope or an acceptance check's verdict, and none changes whether this plan is adopted. Q24 (whether Petri nets or TypeDB could carry the metamodel's types) was not material to this plan and is resolved by argument (compose).\n\n- Q23 (agent, resolved 2026-10-25): the rules writer now gives `move` a way-open check (`evidence/open-attempt/q23/README.md`).\n- Q25 (agent, resolved by argument 2026-10-26): ways are two-way unless the description declares them one-way; the build is F6 below. Until it lands, each run's `TRACE_READ.md` names any resident stuck behind a way it already used, so it is not read as a refusal by the world.\n- Q26 (agent, open): the run page does not show an attempt in its owner's words or that it matched nothing (G17); S1 is not done until it does.\n- Q27 (agent, resolved 2026-10-26): S2's same-moment fixpoint is a rule semantics inside the one existing commit, not the engine capability the roadmap forbids; the roadmap's eligible-work list now names this plan.\n- Q28 (agent, open): whether S2's glass chain reuses the hand-written spill and damage processes (`src/world_substrate/mechanisms/damage.py:116`) or the rules writer writes its own; settled by reading and one free probe before S2.\n- #244 (agent, open): a build is accepted although its own test runs say a task is never possible; blocks A2 and A3 on a newly built world, not on the saved fixture.\n- Q22 / D2 (Brian): AI game master for unmatched attempts; default \"nothing comes of it\" stays.\n- Interpreter cost per attempt (Q29, resolved 2026-10-26 from S1's live run): the 20 interpreter calls added 11.6% to\n  the run's other calls (about 24% at the 30-round cap), under the 30% that would require batching, so S1 keeps one\n  call per attempt.\n\n## Fixes settled by argument\n\nOpen questions that an argument already answers; each is small, agent-owned, built alongside the slices in its own\npull request, and checked on a free replay of a saved world before any paid run.\n\n| Id | Question | Fix | Check |\n| --- | --- | --- | --- |\n| F1 | Q2 | The refused row names the earlier event this round that changed what its failed checks read (`blocked_by_event`) | free replay of the saved airfield and c1r24 worlds: every refused row after a lost race names an accepted event id of that round |\n| F2 | Q6 | `/run` refuses a second request for the same session, round and base revision | a test that sends the same round twice: one run, one charge |\n| F3 | Q8 | A field read by a check but written by no rule is a test-run finding | the saved worlds' builds list it where #218 found it |\n| F4 | Q10 | The readout quotes `said_on_retry` when present, as the scene replay does | free replay of a saved menu-path run |\n| F5 | Q15 | Adopt the `~/code2` repository format (indexes over the existing documents) | the repo-format check reports compliant |\n| F6 | Q25 | Ways are two-way unless the description declares them one-way | regenerate the airfield world and probe both directions |\n\n## Activation facts\n\nRecorded in [activation-facts.json](open_attempt/activation-facts.json): shared mechanism yes (engine and generator are shared by every world), no empirical comparison, LLM central yes, spend yes (owner allowance). Route: [path-decision.json](open_attempt/path-decision.json), durable_solo. The plan copies established methods (Inform 7, Event Calculus, Blades in the Dark,\nGURPS) but claims conformance to none of them, so `claims_external_standard` is false.\n\n## Durable documents\n\nDurable documents: system_model#ENT-ACTION-ENVELOPE, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, system_model#ENT-RUN-RECORD, plans\n\nS1 changes ENT-ACTION-ENVELOPE (the command gains its interpretation) and ENT-RUN-RECORD (the build\nrecord gains `unmatched_attempts`); S2 changes PROC-PROCESS-TICK and PROC-TRANSITION (reaction waves);\nS3 changes PROC-TRANSITION (rolls). Each ID is in `docs/model/trace.yaml` today. The roles are declared\nin `.agentic/repo.yaml` lines 3-8: `system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`\nand `plans: docs/plans/`. At completion of each slice, `python3\n~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan\ndocs/plans/open_attempt.md --range <adoption revision>..HEAD` must exit 0.\n\n## Authority and non-goals\n\n**Authority:** Brian's \"yes\" on 2026-10-25 to adopt this plan and start S1; one agent writes; world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only.\n\n**Non-goals:** Organisations as agents, the code/fast-model/LLM decider spectrum, thinking as an effector, moving off\nConcordia 2.4.0, a clingo cross-check, and any change to Cybernetic Influence v3. Each comes after this.\n",
 "built_from": "c9303a7"
};
