window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/world-substrate",
  "subject_revision": "c028b4b66639189e168ddb76b97cf93bae60d3e6",
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
       "runs": 11,
       "problems": 0
      }
     },
     {
      "name": "project check (tests, system model, docs)",
      "command": "PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --python 3.12 --with pydantic --with gdm-concordia==2.4.0 --with pytest python scripts/check_project.py",
      "note": "counts from its unittest runner line 'Neutral runtime tests: Ran N tests'",
      "exit_status": 0,
      "counts": {
       "tests_run": 718,
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
     "affordance": "src/world_substrate/engine.py:352",
     "check": "src/world_substrate/rules.py:48",
     "attempt": "src/world_substrate/attempt.py:149",
     "attempt-reading": "src/world_substrate/attempt.py:81",
     "unmatched-attempt": "src/world_substrate/attempt.py:25",
     "observation": "src/world_substrate/engine.py:235",
     "place-way": "scripts/generate_world_bundle.py:96",
     "projection": "src/world_substrate/projection.py:44",
     "causal-parent": "src/world_substrate/rules.py:383",
     "exchange": "src/world_substrate/exchange.py:68",
     "mechanisms": "src/world_substrate/mechanisms/__init__.py:3",
     "kitchen": "reference_worlds/kitchen/mechanics.py",
     "mechanic": "src/world_substrate/action_authoring.py:456",
     "entity-component": "src/world_substrate/model.py:223"
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
     "scene-replay"
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
  },
  "note": "This is the repository's package: covers the whole repository; its plan part points at the same adopted plan as the open-attempt package. The other package is docs/planning/open-attempt/planning-package.json; both share the checks, open-questions ledger, domain model, metamodel and diagrams, are rebuilt by tools/planning/ and validated at the same subject revision (open question Q41)."
 },
 "questions": [
  {
   "id": "Q1",
   "short": "Rules retry never runs here",
   "question": "The build's rules retry is skipped once 80 s have passed, and in the canonical Waltzman build the test run starts at 85-111 s. Should the cut-off, or the order of the build steps, change so the retry can repair a world?",
   "blocks": "whether a world whose rules fail the part-way or liveness checks can be repaired on the live path, or only scored lower",
   "resolves_with": "An argument already settles that the retry is skipped (85, 101 and 111 s against 80 s). In those runs the test run found no part-way problem, so nothing needed repair (c1r24 TRACE_READ.md:54): it is a latent risk for a world that does. What is left is a technical trade-off against the 150 s first-round target, settled by reading saved traces, not by a new run. Read first evidence/waltzman-tasks-slice2/c1r24/c1r-run24.log, whose step lines carry their times (rules writing from 41.9 s to 111.1 s, so that one call alone passes 80 s), then the /generate-world row in that folder's run-log.jsonl (2026-10-23T22:03:42Z, trace world-builder-live/people/3c7dab9eb26d4bbc99bbd5bbc9418522) for the call-by-call times; then either start the test run earlier or tie the cut-off to the time left before that target.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/world_builder_service.py:263",
    "scripts/world_builder_service.py:1667",
    "docs/plans/waltzman-tasks-slice2.goal.md:100",
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
   "resolves_with": "Argument settles the content cause for the record: group_decision.agenda_items is a bare integer (spikes/any-scenario-2026-10/compile_spec.py:101) that put-matter-on-agenda adds 1 to and settle-agenda-matter subtracts 1 from (:272-275), so an item cannot carry what it is about, and the partnership said at c1r24 round 40 it should not add one 'when I lack information'. What argument cannot settle is which of three fixes to make: give items content (a matter names its question), cost them (one per person per cycle), or drop the count. That choice turns on why residents repeat the pair, which a free replay cannot show (it replays recorded moves). So one paid owner-allowance run, and only once Q12 or a goal makes the agenda matter: if residents still repeat put-and-settle when items carry content, cost them; if they stop, content was the cause; if the count changes no outcome, drop it.",
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
    "docs/plans/waltzman-tasks-slice2.goal.md:117"
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
    "docs/plans/open_attempt.md:465"
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
   "short": "Harness build time not measured",
   "question": "Decision 008 already decided that worlds are built in an agent harness that drafts, checks and edits (docs/decisions/008-build-worlds-in-an-agent-harness.md), and the live service does not yet call scripts/world_harness.py. What is open is only whether a harness build fits the 150 s first-round target. How long does a harness build take against that target?",
   "blocks": "when the harness replaces the fixed build calls and the rules retry (Q1) on the live path",
   "resolves_with": "A measurement, from saved traces first: time the harness's draft-check-edit loop on the saved c1r24 and airfield build inputs (free, the build traces hold the prompts) and compare with the 85-111 s fixed builds; a paid harness build only if the saved inputs cannot be replayed.",
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
   "question": "When a resident tries something no installed rule covers, may an AI game master invent a rough effect, marked coarse in the record? Prior art in this repository: the offline any-scenario spike already lets its game master write a rule for each unlisted attempt mid-run (docs/model/ODD.md:194, 8.19 at :266, question 9 at :27): a rule that passes the layer-1 checks is installed into the running Engine, and one that fails becomes a one-off gm-ruling recorded as unsupported_action. Decision 007 accepted that for the spike (it amends Decision 006's pre-run approval: mid-run rules are reviewed after the run), but no person approves before or after (G14), and the spike stays offline (Q17). S4 would differ in three ways: it runs on the live World Builder, where Decision 006's approval before a run still holds; its output would be one coarse effect for one attempt, not a general rule; and it would be marked coarse in the record.",
   "blocks": "slice S4 of docs/plans/open_attempt.md, and how alive a world feels when its rules are thin",
   "resolves_with": "A product call on whether every effect must come from a written rule; no test settles it.",
   "owner": "brian",
   "status": "open",
   "recommendation": "Not yet: the person is told nothing comes of it, and the attempt is listed for the next build's rules writer. If allowed later, reuse the spike's mid-run path (check gate, then install or a recorded ruling) rather than a new one, with an approval step (G14).",
   "default": "Unmatched attempts change nothing and are listed in the build record.",
   "sources": [
    "docs/plans/open_attempt.md:304",
    "src/world_substrate/rules.py:288",
    "docs/model/ODD.md:194",
    "docs/model/ODD.md:266",
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
   "question": "S2 runs immediate processes again and again inside one commit until nothing more is due (docs/plans/open_attempt.md:164, Piece 2), which changes src/world_substrate/engine.py. AGENTS.md and Decision 006 say not to add engine, scheduler, renderer or cognition capability of World Substrate's own and to host loops on Concordia or Mesa (AGENTS.md:39; roadmap/README.md:459). Does a same-moment fixpoint in engine.py count as that forbidden engine capability?",
   "blocks": "slice S2 (A5, A6) and the knock-on part of the canonical run; S1 and S3 do not wait for it",
   "resolves_with": "Brian's call: the rule's wording is his (Decision 006), and the earlier resolution was argued by this plan's own author, so it is not settled by agent argument. The argument for: a ramification fixpoint is a rule semantics inside the one existing transition (C+ and Event Calculus), with no new loop, clock or scheduler, bounded at 32 reactions. The argument against: it is new control flow in engine.py, and Concordia's game master or Mesa's step could host the chain instead, one reaction per step.",
   "owner": "brian",
   "status": "open",
   "sources": [
    "roadmap/README.md:459",
    "AGENTS.md:39",
    "docs/decisions/006-governed-rules-layer-scope.md",
    "docs/plans/open_attempt.md:164"
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
   "question": "The hand-written mechanisms library already has a vessel-failure spill process and heat damage (src/world_substrate/mechanisms/damage.py:116). A generated world's registry holds only its compiled mechanics and the rules writer's declared processes (build_engine, scripts/run_authored_world.py:55-58); the library processes are never registered there. Should S2's glass chain reuse the library's spill and damage processes, or have the rules writer write its own?",
   "blocks": "how S2's glass chain is built, and whether generated and reference worlds share physics",
   "resolves_with": "Reading the code and one free probe: compare the library processes' read and write paths (entities.<vessel>.condition.value, container, liquid) with what a generated bundle declares; if a generated glass can carry those components, offer the library processes to the build as installable rules and probe the glass chain on the saved airfield fixture; otherwise the rules writer writes declared processes and the library stays reference-only.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/mechanisms/damage.py:116",
    "scripts/run_authored_world.py:58",
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
  },
  {
   "id": "Q30",
   "short": "Build accepted with a task never possible",
   "question": "A build is accepted although its own test runs say a described task is never possible: in the S1 airfield build every test run reported 'never possible: practice flight' and the third rules attempt was accepted anyway (#244). Should such a build be repaired or refused instead?",
   "blocks": "A2 and A3 on any newly built world (they need the helicopter and the wall reachable), and whether a visitor's world can do what they described; A2 and A3 on the saved fixture tests/fixtures/airfield-s1-live.json do not wait for it",
   "resolves_with": "Reading the S1 airfield build record settles what happened (evidence/open-attempt/s1-airfield/TRACE_READ.md:32). The fix is technical: treat a described task reported never possible as a rules-retry trigger (within Q1's time cut-off) and, if it survives, say so on the page; check on the saved airfield build that it is flagged.",
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
   "resolves_with": "An argument settles the cause: the label is the rules writer's own sentence, shown as is. The choice is technical (ask the rules writer for requirement-style labels, or show 'needs: <label>' with actual against required); check on the saved airfield world's refused rows.",
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
   "resolves_with": "Read the S1 airfield run's readout call and prompt to see what the lens choice was given; the fix is technical (choose from the world's kind and description, with the reason recorded). Check with one owner-allowance readout call on the saved run, no new build.",
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
   "resolves_with": "An argument settles the first two: the run loop draws run_seed once when a run starts and records it in the run record, and each roll event records its dice, so a replay reads the dice and never rolls; a world with no roll never draws, so every saved world replays unchanged (A8). The rule stays a function of state plus the recorded seed, so the invariant becomes 'no unrecorded randomness'. The third part is open: the rules writer must give people skill fields from the description ('has never flown' gives piloting 0) and the roll may read only that field. Settled in S3 by a free probe that regenerates the airfield spec and reads Sam's recorded skill.",
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
   "resolves_with": "Reading the compiler settles generated rules: their reads are derived from their own selector, checks and effects (_derived_reads, src/world_substrate/action_authoring.py:173), so they cannot read outside them. Open are hand-written mechanisms and reference worlds. Technical choice: a test-time state view that records each hand-written rule's actual reads and fails on an undeclared one; check with a test rule that reads an undeclared field.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "AGENTS.md:21",
    "docs/model/ODD.md:87",
    "src/world_substrate/action_authoring.py:173"
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
   "evidence": "Settled by reading the code: injected words cannot add a kind, an entity or an outcome (attempt.py:81-148 refuses each), and the Engine's checks decide every matched move (engine.py:582), so the worst case is a legal move the person did not mean. That is a misreading, owned by Q36, not a new authority path.",
   "sources": [
    "src/world_substrate/attempt.py:81",
    "src/world_substrate/engine.py:582",
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
   "resolves_with": "Argument plus a check, no paid run: each reading keeps quoted_span per field (attempt.py:81), so a reader can compare the words with the kind. The plan's checks are A2's negative fixture (fly never binds to move) and the TRACE_READ.md sample of ordinary attempts. Technical addition: list every wait reading of a non-wait attempt (Q39) in the run summary so the trace read covers them all, not a sample. (Listing readings whose kind differs from nearest_kind would catch nothing: read_interpretation sets nearest_kind to the matched kind, attempt.py:122.)",
   "owner": "agent",
   "status": "open",
   "sources": [
    "src/world_substrate/attempt.py:81",
    "docs/plans/open_attempt.md:212",
    "scripts/run_authored_world.py:557"
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
   "resolves_with": "Reading the build record settles what happened (evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md, finding 3). The fix is technical: a builder addition gets its own field and heading ('Added to make it run'), and A3 is judged on the saved fixture tests/fixtures/airfield-s1-live.json, whose wall is the only way (Q30).",
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
   "resolves_with": "Read #128's wanted list against the code: attempts from belief are built (S1, scripts/concordia_residents.py:45), part-way failure is built (Q19, scripts/attempts.py:131), and a person learns an outcome only from what they see (observation, engine.py:235). Close #128 once A3 shows a refused wall attempt chosen from belief in a saved run, citing that row.",
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
   "evidence": "Settled by argument: the row keeps the attempt and reading (scripts/run_authored_world.py:557) but the summary lists only unmatched readings (:800), so a wait reading of real words is visible only by reading every row. Answer: list it (F9).",
   "sources": [
    "src/world_substrate/attempt.py:94",
    "src/world_substrate/attempt.py:129",
    "scripts/run_authored_world.py:557",
    "scripts/run_authored_world.py:800"
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
   "resolves_with": "An argument settles it: the roll is a field of the mechanic in the causal model, and the fingerprint hashes the bundle and causal model (_world_fingerprint, scripts/world_builder_service.py:381), so an approved world names its rolls; the run seed is per run, not per world, so it belongs in the run record, not the fingerprint (Q33). RULE-DERIVED-AUTHORITY (docs/model/ODD.md:238) holds if the compiler adds the roll's skill path to the derived reads and every outcome list's effects to the derived writes. Build work in S3: that compiler change, with a test that a roll reading an undeclared path or an outcome writing outside the scope is refused.",
   "owner": "agent",
   "status": "resolved",
   "evidence": "Settled by argument: approval and fingerprint cover the causal model, which will hold the roll; the seed is a run input recorded with the run; the compiler derives reads and writes, so S3 extends that derivation to the roll's skill path and outcome effects (S3 checks).",
   "sources": [
    "scripts/world_builder_service.py:381",
    "scripts/world_builder_service.py:418",
    "docs/model/ODD.md:238",
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
    "explain": "The interpreter's typed reading of an attempt: one move kind and its field rows (field, value, quoted_span: the words in the attempt behind that value), or the kind 'wait'; read as unmatched if it names an unknown kind or entity, misses a field, or quotes words not said. Code: src/world_substrate/attempt.py:81."
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
    "explain": "A composite reading (two give events make one exchange) derived from committed events, never a second effect. Code: src/world_substrate/exchange.py:68."
   },
   {
    "id": "mechanisms",
    "label": "Mechanisms library",
    "kind": "Reference",
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:58, Q28). Code: src/world_substrate/mechanisms/__init__.py:3."
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
    "explain": "One installed action rule: an action kind's selector, checks, effects and derived reads and writes, compiled and frozen in the profile; the root rule says installed mechanics alone decide what happens. Code: src/world_substrate/action_authoring.py:456."
   },
   {
    "id": "entity-component",
    "label": "Entity and component",
    "kind": "Substrate",
    "explain": "An entity is one thing in the world (person, wall, glass, decision) with an id, a label, categories and typed components; a component is a named record of typed fields (boundary.passable, group_decision.status) that checks read and effects write. Code: src/world_substrate/model.py:223."
   },
   {
    "id": "run-seed",
    "label": "Run seed",
    "kind": "Theory",
    "explain": "Plan S3: one seed drawn when a run starts and recorded in the run record; each roll's dice come from hash(run seed, event id) and are recorded, so a replay reads the dice and never rolls (Q33). Code: none yet."
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
    "id": "Q12",
    "label": "Q12: When a people-world run ends",
    "kind": "BrianQuestion",
    "explain": "Blocks: how long visitors watch a run, and its cost."
   },
   {
    "id": "Q14",
    "label": "Q14: Harness build time not measured",
    "kind": "AgentQuestion",
    "explain": "Blocks: when the harness replaces the fixed build calls and the rules retry (Q1) on the live path."
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
    "id": "Q27",
    "label": "Q27: Is S2's fixpoint engine capability",
    "kind": "BrianQuestion",
    "explain": "Blocks: slice S2 (A5, A6) and the knock-on part of the canonical run; S1 and S3 do not wait for it."
   },
   {
    "id": "Q28",
    "label": "Q28: Reuse the spill and damage rules",
    "kind": "AgentQuestion",
    "explain": "Blocks: how S2's glass chain is built, and whether generated and reference worlds share physics."
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
    "explain": "The interpreter's typed reading of an attempt: one move kind and its field rows (field, value, quoted_span: the words in the attempt behind that value), or the kind 'wait'; read as unmatched if it names an unknown kind or entity, misses a field, or quotes words not said."
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
    "id": "engine",
    "label": "Engine",
    "kind": "Concept",
    "explain": "Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick."
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
    "explain": "Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:58, Q28)."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Concept",
    "explain": "What one actor sees this round: the fields its senses and position allow, never the whole world."
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
    "id": "readout",
    "label": "Readout",
    "kind": "Concept",
    "explain": "One AI summary of a run whose every cited event id is checked against the run."
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
    "id": "skill-roll",
    "label": "Skill roll",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan S3: a move's outcome depends on a seeded, recorded roll against the person's skill, so someone untrained who flies a helicopter can crash it."
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
    "id": "Q27-knock-on-now",
    "source": "Q27",
    "target": "knock-on-now",
    "label": "bears on"
   },
   {
    "id": "Q27-engine",
    "source": "Q27",
    "target": "engine",
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
    "explain": "A rule the world runs by itself each round for every matching entity whose checks hold; this is how effects propagate (plants dry out, lessons arrive)."
   },
   {
    "id": "knock-on-now",
    "label": "Same-moment knock-on",
    "kind": "rules",
    "dashed": true,
    "explain": "A process with timing immediately, run to a fixpoint inside the same moment as the move that triggered it (planned slice S2 of docs/plans/open_attempt.md). Planned, not built."
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
 "next_plan": "---\nplan_id: \"open-attempt\"\ndependencies: []\ndependencies_reviewed: \"2026-10-25\"\nplanning_path: durable_solo\nplanning_path_ref: docs/plans/open_attempt/path-decision.json\nmethod_conformance_receipt: docs/plans/open_attempt/conformance-receipt.json\nstatus: adopted\ngoal:\n  outcome: \"World Builder residents say in their own words what they physically try, instead of picking from a list; the world's rules decide what happens, knock-on effects run to the end inside the same moment, and a person's recorded skill (never how expert their words sound) decides how a risky attempt turns out.\"\n  canonical_example: \"A World Builder world generated from 'A small airfield office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown'. In one run Sam tries to walk through the wall and nothing happens, with the wall named as the cause; someone knocks the glass off the desk and in the same event chain it falls, breaks, the water spills and the person in the next room hears it; Sam tries to fly the helicopter and a recorded roll from Sam's piloting level 0 gives a crash or a rough landing, never a clean flight from good wording.\"\n  forbidden_substitutes: \"hand-edited specs, rules or runs; an interpreter that decides success; outcomes written by an LLM rather than by an installed rule; a roll whose dice come from the attempt's wording; a scripted move presented as an attempt; Waltzman-specific code paths; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run.\"\n  boundaries: \"world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change; existing saved worlds still replay unchanged; owner allowance only, visitor allowance stays $3/day; free replays of saved worlds before any paid run; publish-checker before anything new goes public.\"\n  done_when: \"Acceptance checks A1-A9 below pass, each judged from the full trace of the run it names.\"\n  do_not_gate_on: \"letting an AI game master invent effects for attempts no rule covers (Decision D2, deferred); organisations, the decider spectrum and thinking-as-effector (later designs); a clingo cross-check of the reaction rules; Brian's review of a run.\"\n  stop_after: 3\nconflict_surfaces:\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/open-attempt/review-page/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/open-questions.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/concordia_residents.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/attempt.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/open-attempt/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open-attempt.goal.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/open_attempt.verdicts.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/planning-package.json, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_readout.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/index.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/architecture/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: openspec/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: Makefile, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: lefthook.yml, access: write}\n---\n# Plan: open attempts, knock-on effects that run to the end, and skill rolls\n\nPlanning package: docs/planning/open-attempt/planning-package.json\n\nThis is the plan's own package. The repository's package (`docs/planning/planning-package.json`, repo-wide page\n`proposals/planning-package/review-page/`) covers the whole repository and its plan part points at this same plan;\nboth share the checks, open-questions ledger, models and diagrams, are rebuilt by `tools/planning/` and are validated\nat the same subject revision (open question Q41).\n\nReview page: [proposals/open-attempt/review-page/](../../proposals/open-attempt/review-page/index.html), live at\n<https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/>.\n\n## Actor and result\n\n**Actor:** a World Builder visitor (and Brian as owner) who pastes a scenario and watches the\ngenerated people act. **Result they can inspect:** the run page and its build record show each\nperson's own-words attempt, what the rules made of it, and why it worked, failed or did nothing.\n**Stable example:** the airfield office in the front matter's `canonical_example`: Sam walks into\nthe wall and is refused with the wall named; the glass chain runs in one moment; Sam's untrained\nflight rolls two dice keep-lower.\n\n## Project outcome\n\nProject outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top, rigorous causal engine underneath; the World Builder is the visitor-facing surface). This plan serves that actor directly: the roadmap's \"user describing a world\" is the\nWorld Builder visitor of the Actor section. **Recurring job and baseline:** a visitor describes a world and\nwatches its people act; before S1 each person could only pick from moves the rules already allowed, so\nimpossible attempts (the wall) never appeared. S1 (merged at `fe8c492`, #239) lets residents say attempts in\ntheir own words, and its live run (`evidence/open-attempt/s1-airfield/`, #247) shows residents acting every round; the\nwall refusal and the untrained flight have not yet been seen in a live run, and knock-on chains (S2) and untrained\nfailures (S3) still never appear. **Inspectable result this plan\ndelivers:** the run page and build record of the airfield world showing the wall refusal, the glass chain\nand the rolled crash. **Stage and investment boundary:** prototype stage; three slices, each one pull\nrequest and at most $3.00 of owner allowance; no new service, engine or repository.\n\n## Outcome step\n\nOutcome probe: `roadmap/README.md#canonical-outcome-probe`\nObserved: `evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md`\nStep: step 3 of the probe, \"the residents act in the generated world each round, and the installed rules decide each effect\"\nClass: vertical\n\nThe observed proof is the c1r24 run: the last live run of the whole probe before this plan, the canonical\nWaltzman example driven through the real page (generate, 45 rounds, readout, share link `FQHXnP_TLKPi`, every\nround read). It shows step 3 working with residents picking from a move list, which is what this plan changes.\nS1's first live run of step 3 with free-form attempts is `evidence/open-attempt/s1-airfield/TRACE_READ.md`;\nit does not replace c1r24 as the probe's observed proof, because the knock-on and skill cases (A2, A3) were\nnot exercised there and S1 is built, not done.\n\nEach slice changes that step end to end (generator, resident, engine, page) and ends in a live traced run.\n\n## Why, in one example\n\nBefore S1 a World Builder resident was handed a list of moves the rules already allowed and picked one\n(the menu reply's `action_id` is that list plus `wait`, still so for the menu schema at\n`scripts/concordia_residents.py:96`). So nobody ever walked into a wall: the wall never appeared as a\nchoice. S1 replaced that with an own-words `attempt` (built; see the slice table). Brian, 2026-10-24: a\nperson should be able to \"attempt to walk through a wall but these should not be successful\", and\nsomeone who \"dont know how\" to fly a helicopter \"should probably crash it\". The survey\n([flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md),\nBrian's \"yes\" on 2026-10-25 to this design) found three pieces missing from World Substrate and\nnamed the established method to copy for each. This plan designs those three, in the order they\ndepend on each other.\n\n## Current truth (read from code before S1, 2026-10-25, main 63caf4c; S1 rows added after it merged at fe8c492)\n\n| Have | Where |\n| --- | --- |\n| The rules list what a person can do now (an affordance page) | `Engine.discover`, `src/world_substrate/engine.py:352` |\n| A move whose checks fail is refused with the failed check recorded, no partial change | `Engine.apply` / `_reject`, `engine.py:582`, `:749` |\n| A move of a kind no rule knows is recorded as unsupported, nothing changes | `Engine.submit`, `engine.py:452`; `UnsupportedAction`, `rules.py:288` |\n| Meaning (sense and roles) is kept apart from mechanics | `SemanticBinding`, `src/world_substrate/semantic.py:15`; Decision 003 |\n| Things the world does by itself run once per round, each citing its causes | `Engine.advance`, `engine.py:786`; `DeclaredProcess`, `action_authoring.py:245` |\n| Who hears or sees what is limited by the world | `world_substrate.information` |\n| No randomness anywhere in rules | no `random`/`seed` in `engine.py` or `action_authoring.py` |\n| S1: a resident answers `attempt` in its own words instead of an offered `action_id` | `OPEN_SCHEMA`, `scripts/concordia_residents.py:45` |\n| S1: one typed call reads the attempt into one action kind and its fields, with no outcome field | `interpret`, `src/world_substrate/attempt.py:149`; `read_interpretation`, `:81` |\n| S1: an unmatched attempt changes nothing and is listed in the build record | `UNMATCHED_KIND`, `attempt.py:25`; `unmatched_attempts`, `scripts/run_authored_world.py:800` |\n| S1 (Q23): generated worlds have places, ways with a passable flag, and a move that checks the way | `scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`; `evidence/open-attempt/q23/README.md` |\n| After S1 (#242, `87b4aa2`): the World Builder page sends open-attempt residents whenever AI chooses the moves | `scripts/world_builder_home.html` on main; `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md` on main |\n\nDecision 006 limits World Substrate to the governed-rules layer. Pieces 1 and 3 are rules-layer pieces:\none turns words into a typed move, one adds a recorded roll to a rule. Piece 2 runs rules to a fixpoint\ninside one commit, which changes `engine.py`; whether that counts as the engine capability AGENTS.md and\nDecision 006 forbid is Brian's call (open question Q27). The plan's recommendation is that it does not (no\nnew loop, clock or scheduler, bounded at 32 reactions inside the existing commit); until he answers, S2 waits\nand S1 and S3 go ahead.\n\n## The three pieces\n\n### Piece 1. Open attempt (copy: Inform 7 \"try\" plus Voyager-style attempts sent to an engine)\n\n1. **Decide.** The resident's reply keeps `belief`, `expected_effect`, `work` and `reasoning`, and\n   replaces `action_id` with `attempt`: one sentence of what they physically do, with their body,\n   voice or hands (\"walk east through the wall into the hangar\"). The affordance page is still shown,\n   as \"things you know you can do here\", but it no longer limits the answer.\n2. **Interpret.** One typed light-model call (`llm_client`, the World Builder's current model, low\n   effort) reads the attempt and the world's action kinds with their fields, and returns `{kind, fields,\n   nearest_kind, why}`, where `fields` is a list of rows `{field, value, quoted_span}` (the words in the attempt\n   behind each value) and `kind` may also be `wait`. `read_interpretation` (`src/world_substrate/attempt.py:81-148`)\n   checks the rows against the world and turns a reading that does not fit (unknown kind or entity, missing field,\n   quoted words not in the attempt) into `{unmatched: true, nearest_kind, why}`. Its schema has **no success field**:\n   it says what is being tried, never whether it works. A `wait` reading of an attempt with real words is listed\n   like an unmatched one (F9, Q39).\n   The result is recorded as the command, so replay never calls the model again.\n3. **Check.** The matched move goes through `Engine.submit` unchanged. The wall case is an ordinary\n   refusal: the generated `move` rule's \"the way between is open\" check fails (S1's canonical world must show the rules writer gave `move` that check; if it did not, that gap is fixed in the rules writer, never by hand-editing the world), and the event names the wall.\n4. **Unmatched fallback (v1).** An attempt that matches no kind is recorded through the existing\n   unsupported path: nothing in the world changes, the person sees \"you try to …; nothing comes of\n   it\", and the build record lists every unmatched attempt so the rules writer can add a rule in the\n   next build. Letting an AI game master invent an effect is Decision D2, deferred.\n5. **Who notices.** Unchanged: `world_substrate.information` decides who perceives the result.\n   Shouting to someone overseas succeeds as speech and reaches only those in hearing range.\n\n### Piece 2. Knock-on effects that run to the end (copy: C+ / Event Calculus ramification)\n\nA process may declare `timing: \"immediately\"` (default stays `\"each_round\"`, so every existing world is\nunchanged). After a move or round event commits its candidate state, the engine runs every immediate\nprocess whose `due()` holds on the new state, then again on the state that produces, until none is\ndue. Rules:\n\n- each (process, entity) pair fires at most once per moment, so a reaction cannot feed itself;\n- at most 32 reactions per moment; going over refuses the whole moment visibly and changes nothing\n  (the existing \"no partial mutation\" invariant);\n- every reaction event cites its parent event as a hard causal parent, so the chain is readable;\n- order inside one wave is the registry's fixed order, recorded in the events.\n\nGlass: `push glass` moves it off the desk → `falls` (unsupported object above floor) → `breaks`\n(fragile and fell) → `spills` (container broke while holding water) and, also from `breaks`, a `crash sound` event. Five events in\none moment: fall cites push, break cites fall, and spill and sound both cite break. The person next\ndoor then learns of the sound through `information`; that is an observation, not a sixth event.\n\n### Piece 3. Skill rolls (copy: Blades in the Dark action roll, GURPS defaults, progress clocks)\n\nAn action mechanic may declare `roll: {skill: <actor path>, position: controlled|risky|desperate,\noutcomes: {full: [effects], partial: [effects], fail: [effects]}}`.\n\n- Hard gates first: the ordinary checks (holds the key, knows the number, is in the cockpit) run\n  before any roll. No roll without stakes: a mechanic with no `fail` effects may not declare a roll.\n- Dice: as many six-sided dice as the recorded skill level; level 0 rolls two and keeps the lower\n  (GURPS-style default for the untrained). Highest die 6 = full, 4-5 = partial, 1-3 = fail.\n  Position picks which outcome list the rules writer gave for \"partial\" and \"fail\".\n- The dice come from a seeded generator (`seed = hash(run_seed, event_id)`), and the values are\n  recorded in the event, so a replay reproduces them and a reader can check them.\n- Only the skill path is read. The attempt's wording never reaches the roll.\n- Long tasks: a roll's outcome effects may write the counter field a process already reads (the world field behind `Engine._progress`, `engine.py:321`, which only reports it), so a partial result moves a task's counter less than a full one, like a Blades progress clock.\n\nHelicopter: Sam (piloting 0) is in the cockpit (gate passes), rolls two dice, keeps the lower; on\n1-3 the `fail` effects crash the helicopter, damaging it and injuring Sam, and Piece 2 carries on\n(fuel leaks, alarm sounds, the ground crew hears it).\n\n## Requirements\n\nWhat Brian asked, plus what the plan's own claims imply; each row names its check in the acceptance table below. Status per check: S1 is built (merged `fe8c492`, #239): A1 (`tests/test_open_attempt.py`) and A8 (`scripts/check_project.py`) were checked in its pull request, and the owner-allowance airfield run with residents (`evidence/open-attempt/s1-airfield/`, 2026-10-26, merged in #247)\njudged A4 and A9 passing (its TRACE_READ.md passes `scripts/check_trace_reads.py` and samples ordinary attempts, which is R1's trace check) and left A2 and A3 planned and not yet run: the live run never reached the helicopter or the wall, so both run next on the saved airfield world `tests/fixtures/airfield-s1-live.json` (see the S1 live result below); A5-A6 planned in S2; A7 planned in S3; A8 planned in every slice\n(run on each merge commit); A9 planned in S1 (open-attempt part) and completed in S3 (full chain). None is\ndeferred. The claimed property is the requirement itself (an impossible attempt is refused with its cause,\na chain finishes, skill sets the dice), never a count of passing tests.\n\n\n| Id | Requirement (source) | Fails when | Control | Status |\n| --- | --- | --- | --- | --- |\n| R1 | Residents can try anything their body can do (Brian 2026-10-24) | The interpreter quietly maps \"fly the helicopter\" to a safe move | `quoted_span` per role; A2 negative fixture; TRACE_READ samples ordinary attempts | Passing in part: the S1 live run TRACE_READ samples ordinary attempts and passes; A2 planned and not yet run (fixture run next) |\n| R2 | The world, not the interpreter, decides what happens (Decision 003; AGENTS.md \"installed mechanics alone\") | The interpreter refuses or judges success | No success field in its schema (A1); refusals only come from rule checks | Passing: A1 in #239 |\n| R3 | Impossible attempts fail with a cause (Brian 2026-10-24) | A wall attempt is dropped instead of recorded | A3: refused event names the failed check | Planned and not yet run: A3 on the saved airfield world next |\n| R4 | Knock-on effects run on their own to the end (Brian 2026-10-24) | A chain stops after one step, or loops | A5, A6: once-per-pair rule, cap of 32, whole moment refused on overflow | Planned and not yet run (S2) |\n| R5 | Skill decides risky outcomes, not wording (Brian 2026-10-24: LLM knowledge must not leak) | Dice depend on the attempt text, or outcomes are written by the model | A7: same attempt, skill 0 versus 3, different dice pools; dice only from seed | Planned and not yet run (S3) |\n| R6 | Saved worlds and replays keep working (AGENTS.md invariants) | Replay calls the model or rerolls | A8: every retained replay test unchanged; rolls and interpretations replay from records | Passing at the S1 merge (A8); planned for S2 and S3 merges |\n| R7 | Every run is readable in full (core rules) | An interpretation or roll is missing from the trace | A9: run-log.jsonl has each interpreter call's trace id, each roll's dice; TRACE_READ.md passes | Passing for S1 (A9 on the live run); full chain planned in S3 |\n\n## Acceptance checks\n\n| Id | Check | Run and what its trace must show |\n| --- | --- | --- |\n| A1 | Interpreter schema has no success or outcome field | `pytest tests/test_open_attempt.py::test_schema_has_no_outcome` output |\n| A2 | \"Fly the helicopter to the coast\" never binds to `move` | fixture run on the generated airfield world; the command records `kind: pilot`, `quoted_span` \"fly the helicopter\" |\n| A3 | Walking through the wall is refused, wall named | the canonical run's event for Sam's wall attempt: `status: refused`, failed check names the wall entity. Q23 (generated worlds have walls) resolved: `evidence/open-attempt/q23/README.md` |\n| A4 | An unmatched attempt changes nothing and is listed | the canonical run's build record `unmatched_attempts` list, and the event's before/after equal |\n| A5 | The glass chain completes in one moment | canonical run: one moment with push, fall, break, spill and sound events; fall cites push, break cites fall, spill and sound cite break. Judged separately: the neighbour's observation for that moment includes the sound |\n| A6 | A self-feeding reaction is refused whole | `tests/test_open_attempt.py` loop fixture: status refused, world unchanged, cap reason recorded |\n| A7 | Skill, not wording, sets the dice | fixture: identical attempt text, piloting 0 and 3; events show 2-keep-lower versus 3 dice, seed recorded |\n| A8 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with these replay tests named passing in the quoted output: `test_action_envelopes` (unsupported and malformed envelopes replay), `test_first_fill.test_fill_tick_and_replay_match_exactly`, `test_greenhouse_zero_review.test_replay_regenerates_exactly_through_generic_renderer`, `test_castaway_zero_review.test_zero_review_replay_regenerates_exactly` |\n| A9 | The canonical run is fully traced | `evidence/open-attempt/<run>/run-log.jsonl` plus `TRACE_READ.md` passing `scripts/check_trace_reads.py`; read by the implementing agent before reporting |\n\n## Success and disproof\n\nThe plan claims three properties: (1) residents state any physical attempt and only installed rules\ndecide its effect (R1-R3, checked by A1-A4); (2) knock-on effects run to the end inside one moment or the\nmoment is refused whole (R4, A5-A6); (3) recorded skill, not wording, decides risky outcomes (R5, A7);\nwith replay unchanged (R6, A8) and every run fully readable (R7, A9).\n\n**Success:** A1-A9 pass, each judged from the full trace of the run it names. **Disproof:** any one\nof these in the canonical run's trace: an interpreter output carrying a success or outcome; a wall\nattempt that changes the world or is refused without naming the wall; a pilot attempt by a level-0\nperson that ends in a clean flight; dice whose seed is not `hash(run_seed, event_id)`; a replay that\ncalls a model. Trace review: the implementing agent reads every refused, unmatched and rolled attempt\nand a sample of ordinary ones in the named run's `run-log.jsonl` and writes `TRACE_READ.md`; each criterion\nA1-A9 is expected `pass`. Runs are named in order: `evidence/open-attempt/s1-replay/` (free replay of a\nsaved world), `evidence/open-attempt/s1-airfield/` (first owner-allowance run, judged for A2-A4 and A9),\n`evidence/open-attempt/s2-airfield/` (A5), `evidence/open-attempt/s3-airfield/` (A7 and the full A9);\nA1, A6 and A8 are judged from the named pytest and `check_project.py` output saved beside each run.\n\n## When a run fails or surprises us\n\nThis is separate from the anticipated failure modes in the Requirements table: it covers what we did not\nforesee. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,\nintermediate stages (interpretation, checks, reactions, rolls) and the final output (build record, page)\nbefore choosing a fix; cite where it diverged; classify it evidence absent, unused or\ncontradicted, invalid expectation, or unresolved. An unresolved cause permits investigation, not a\nrepair. A repair is verified by a new traced run whose `TRACE_READ.md` links the original run and the divergence it\nfixes; the original stays. Never rerun until a behavior\nappears and report only that run. Review completeness never changes the run verdict: a run's pass or fail\ncomes from its trace against A1-A9, and an incomplete review leaves the claim unreported, not passed.\n\n## Slices, in order\n\n| Slice | What lands | State | Checks |\n| --- | --- | --- | --- |\n| S1 | Close Q23 (rules writer makes places, ways and the wall check), then open attempt: resident `attempt` field, interpreter, unmatched fallback, build-record list | built, not done: merged `fe8c492` (#239); page fix `87b4aa2` (#242); live run `evidence/open-attempt/s1-airfield/` (#247): A4 and A9 pass, A2 and A3 not exercised; the run page does not yet show own-words attempts (Q26) | A1, A8 at merge; free replay `evidence/open-attempt/s1-replay/replay.txt` exit 0; A4, A9 on the owner-allowance run; still owed: A2 and A3 on the saved world `tests/fixtures/airfield-s1-live.json`, and Q26 |\n| S2 | `timing: immediately` processes run to a fixpoint inside one moment | human_decision_required (Q27); specified and ready once Brian answers | A5, A6, A8 |\n| S3 | `roll` on action mechanics, seeded and recorded; rules writer prompt can declare it; the compiler adds the roll's skill path to derived reads and every outcome's effects to derived writes (Q40) | fully_specifiable_now | A7, A8, a test that a roll outside its derived scope is refused, then the full canonical run for A9 |\n| S4 | AI game master for unmatched attempts | human_decision_required (D2) | none until decided |\n\n**Kinds the canonical airfield world must contain** (generated, never hand-written): `move` between\nplaces with a check that the way between is open (the wall), `push` an object, `pilot` a craft to a\nplace, and `speak`. Before S1, generated worlds were economy-style (`make-leads`, `shape-slats`) and\nnothing in the rules writer asked for places, ways between them or blocking. That was open question\n**Q23**, S1's first step, resolved 2026-10-25 by a generic fix to the bundle contract and rules writer\n(`scripts/generate_world_bundle.py:96`, `scripts/generate_causal_model.py:430`): the regenerated airfield\nworld refuses the walk through the wall with \"the way is passable\" failed\n(`evidence/open-attempt/q23/after-fix/probe.txt`). Known limit, open question **Q25**: a way works from its\nfirst place to its second only.\n\n**S1 live result** (`evidence/open-attempt/s1-airfield/TRACE_READ.md`, owner allowance, deployed `87b4aa2`, 9 rounds,\n65 model calls, $0.0319): residents moved every round; A4 passes live (15 refused or unmatched attempts each changed\nnothing and every unmatched one is listed with the interpreter's nearest move); A2 and A3 were not exercised, because\nthe build left the helicopter unreachable: everyone but the mechanic starts in the office, the brick wall is the only\nway to the hangar and is not passable, the builder's own test runs said the practice flight was never possible and the\nbuild was accepted anyway (#244, Q30). Two smaller defects were filed: a refusal reason reads as a fact (\"you are the\ndispatcher\") rather than a requirement (#245, Q31), and the readout chose the goods-flow lens for a training world (#246, Q32).\nS1 is therefore built but not done. Next: A2 as a fixture run of \"fly the helicopter to the coast\" and A3 as an\ninterpreted attempt at the wall, both on the saved world `tests/fixtures/airfield-s1-live.json` (free, no new build),\nthen Q26 (the run page shows each attempt in its owner's words).\n\nEach slice is its own pull request and leaves a working World Builder. S1 alone already lets a\nresident walk into the wall. The rules writer (`scripts/generate_causal_model.py`, its process and mechanic schemas) learns `timing` in S2 and\n`roll` in S3; until then generated worlds simply do not use them.\n\n## Decisions\n\n- **D1 (made, technical):** the interpreter is one typed light-model call per attempt, not a parser\n  and not the resident's own model. Reason: words to (kind, roles) is meaning, which our rules say\n  is never read with regex; a separate call keeps the resident from steering its own interpretation.\n  Cost: one extra small call per attempt, measured in S1's first run against the visitor $3/day cap.\n- **D2 (Brian's call, deferred):** for attempts no rule covers, should an AI game master be allowed\n  to invent a rough effect, marked \"coarse\" in the record? Recommendation: not now. v1 says \"nothing\n  comes of it\" and lists the attempt for the rules writer. If not answered, v1 stays. Prior art in this\n  repository: the offline any-scenario spike already lets its game master write a rule mid-run for each unlisted\n  attempt, installed if it passes the layer-1 checks, else recorded as a one-off ruling (`docs/model/ODD.md:194`,\n  8.19 at `:266`); Decision 007 accepted that for the spike with review after the run, but no person approves (G14)\n  and the spike stays offline (Q17). S4 would differ: it is on the live World Builder, where approval before a run\n  still holds (Decision 006); it makes one coarse effect for one attempt, not a general rule; and the record marks it\n  coarse. If allowed, it reuses the spike's check gate rather than a new path.\n- **D3 (made, technical):** reactions are a `timing` field on the existing process declaration, not a\n  new rule type, so they reuse its selector, checks, effects, linked participants and write scopes.\n\n## System model\n\n- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a refused attempt changes nothing), RULE-PROJECTION-FROM-CANONICAL-ONLY (the page shows only recorded events). Adds: `attempt interpretation` (adds), `unmatched_attempts` (adds), `timing` (adds), `roll` (adds).\n- Scope: the system model is this repository's own (world-substrate only, linked from the documentation entry point\n  `docs/wiki/README.md`), not a shared model. The one shared artefact it touches is the\n  scientific-hypergraph kernel, which it reads at a pinned revision and never changes; the mapping\n  onto it lives here (`docs/model/metamodel-mapping.json`).\n- Types: [docs/model/METAMODEL.md](../model/METAMODEL.md) (built by `scripts/build_metamodel.py`) holds the\n  world's own types this plan relies on (action kind, role, check, effect, process, affordance, decider,\n  attempt, attempt reading, unmatched attempt, event, observation) and the two it plans (same-moment\n  knock-on, skill roll), each mapped onto the scientific-hypergraph kernel at `7b0638f`. Its reuse-gate\n  table records the formalisms checked before minting them (bounded-design typed-relational reference,\n  rule 1); AlgebraicPetri and TypeDB were open question Q24, resolved by argument as compose. S2 and S3 flip their type to built in that\n  table in the same pull request.\n- Not changed, and why: actors, places, information reach (`world_substrate.information`), tasks and\n  the budget ledger keep their current model elements; this plan only changes how a move is chosen,\n  how reactions run and how a mechanic resolves, so their definitions stand. RULE-BUDGET-FAILS-CLOSED,\n  RULE-FROZEN-PROFILE and RULE-DERIVED-AUTHORITY are relied on unchanged.\n- Views: [docs/model/VIEW_COVERAGE.md](../model/VIEW_COVERAGE.md) records which view shows each element; each slice adds its rows there. Per element:\n  - `attempt interpretation` (`AttemptReading`): `owner_run_log` shows it (`GET /runs?full=1` keeps the\n    transcript, `scripts/world_builder_service.py:1011`); `home` does not yet, gap G17, now open question Q26 (S1 is not done until it closes).\n  - `unmatched_attempts`: `owner_run_log` shows it in the run summary (`GET /runs` keeps `summary`,\n    written at `scripts/run_authored_world.py:800`); `home` does not yet, gap G17.\n  - `timing` and the reaction wave (S2): `round_replay` and `scenario_state_panel` must show each\n    reaction event with its parent; S2 adds the row.\n  - `roll` (S3): `scenario_state_panel` must show each roll's seed and dice; S3 adds the row.\n- The trace must show, per element: the command's `interpretation` record with the interpreter's trace id; the build record's `unmatched_attempts`; reaction events citing their parent; each roll's seed and dice.\n- S1 adds an `attempt interpretation` record\n  (command field) and the `unmatched_attempts` build-record list; S2 adds the `timing` process field and\n  the reaction-wave events; S3 adds the `roll` mechanic field and the event's `roll` record. Each slice\n  updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request,\n  and the drift test must fail on a renamed field before it passes.\n## Trace visibility\n\n- Each run's `run-log.jsonl` records: the inputs (scenario text, world bundle hash, run seed); every step\n  (round, actor, attempt text); each model call (resident, interpreter, rules writer) with its prompt\n  messages, arguments, typed result and `llm_client` trace id; the model's reasoning where it returns it\n  (the resident's `reasoning` field); every engine event with before/after, failed checks, reaction parent\n  and dice; and the output (build record, page JSON). Kept for ordinary runs, not only failures. No slice is a pure document edit, so no slice\nclaims the no-run exemption; this adoption commit alone is document-only and runs nothing.\n- How to open one: `evidence/open-attempt/<run>/run-log.jsonl` is one JSON object per line (`jq . <file>`);\n  the live run's page links its share id, and `llm_client` trace ids open in its trace store\n  (`python -m llm_client traces --trace-id <id>`). Who reads and when: the implementing agent reads every run's\n  trace before reporting that slice, including the free replay and fixture runs; every failure or surprise\n  in full, and at least five ordinary attempts per run chosen across rounds and actors. This plan has no runs\n  other than World Builder runs and the test suite, whose output is saved beside each run.\n- World Builder runs keep `run-log.jsonl` (every request, interpreter and resident call with\n  `llm_client` trace ids, every event with dice) beside the run; `TRACE_READ.md` per round. The\n  implementing agent reads every refused, unmatched and rolled attempt in the canonical run and a sample\n  of ordinary ones before reporting.\n## Capability reuse\n\nNo catalogue entry fits, because `reuse_candidates.yml` and\n  `capability_registry.yml` hold approvals, notifications, scheduling, document-to-text and search\n  wrappers, none of which interpret actions or run rules. Model calls go through the workspace's shared\n`llm_client` (listed in `~/code2/workspace/docs/capabilities.md`, not a catalogue entry). No new\ncross-project capability is added; the interpreter's first and only consumer is the World Builder run loop.\n\n## Prior art and ownership\n\nDisposition per piece, from [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md): open attempt **extends** the existing unsupported-action path and `Engine.submit` (copying Inform 7 \"try\" and Voyager-style attempts); knock-on effects **extend** `DeclaredProcess` (copying C+/Event Calculus ramification); skill rolls **extend** `DeclaredActionMechanic` (copying Blades in the Dark and GURPS defaults). Owner: World Substrate's rules layer (Decision 006). Parallel-implementation check: no second command path, engine or scheduler; every attempt still enters through `Engine.submit`, and `grep -n \"def submit\" src/world_substrate/engine.py` stays one hit.\n\n## LLM call boundary\n\nCall graph per round: resident call (one per actor, existing) -> attempt interpreter call (one per attempt,\nnew, after the resident's reply, before `Engine.submit`) -> no further model call; rules, reactions and\nrolls are code. The rules writer's calls (existing, at build time) change only in prompt and schema.\nProvider: OpenRouter, model `openrouter/openai/gpt-6-luna` (the World Builder's `DEFAULT_MODEL`,\n`scripts/run_authored_world.py:37`). Spend authority: Brian's owner allowance, granted for this plan on\n2026-10-25. An interpretation becomes authoritative only as a recorded command after an authentic live\nrun; fixtures may use recorded interpretations but are never reported as live.\n\nExisting resident call (unchanged boundary except the field): typed reply `{belief, attempt, expected_effect,\nwork, reasoning}`; `attempt` replaces `action_id`; it has no success field either; the reply is recorded in\n`run-log.jsonl` with its trace id and is never re-read by rules or replay; a failed or malformed reply records\nthe actor as waiting, as today.\n\nOne new call: the attempt interpreter, through `llm_client`, typed output (`kind`, which may be `wait`; `fields` rows of `field`, `value` and `quoted_span`; `nearest_kind`; `why`), checked into a reading or `unmatched` by `read_interpretation`, no success field. Its output is recorded as the command and never re-read by rules or replay; it has no authority to change state, and promotion of its output to authority is refused by construction (only `Engine.submit` writes). Failure: a malformed or failed call records the attempt as unmatched with the error, never a guessed move.\n\nTracing: each run gets one trace id, `world-builder-live-run-<uuid4 hex>` (`scripts/run_authored_world.py:385`), passed to every resident call (`scripts/concordia_residents.py:101`) and every interpreter call (`src/world_substrate/attempt.py:158`), so all of a run's model calls share it; `llm_client` stores each call under that id in its `llm_calls` table (`~/projects/data/llm_observability.db`) with its task name, model, request messages, response, token counts, cost, latency, error and timestamp. The run's `run-log.jsonl` repeats the trace id beside each recorded reply and interpretation, so a run row links to its calls (Trace visibility, above).\n\n## Irreversible actions and spend\n\nNothing irreversible is planned: merges are pull requests (revert with git) and deploys of World Builder's\nown service are redeployable from the previous commit. Boundary: no deletion of saved worlds or run\nrecords, no outreach, no change to other repositories. If a step would be irreversible, it stops and goes\nto Brian first (core rules: \"Ask first only for irreversible actions\"); authorization for everything in\nthis plan is Brian's 2026-10-25 \"yes\". Containment: the deploy is checked through the health endpoint's\nbuild commit and rolled back to the prior commit if it fails. Spend: owner allowance only, after a free replay; at most $1.00 per owner run and $3.00 across S1\n(stop and report if a run would exceed it, enforced by the run's `max_budget`); the visitor allowance\nstays $3/day.\n\n## Uncertainties\n\nThe material uncertainties, listed in full as of 2026-10-26: each below could change a slice's scope or an acceptance check's verdict, and none changes whether this plan is adopted. Q24 (whether Petri nets or TypeDB could carry the metamodel's types) was not material to this plan and is resolved by argument (compose).\n\n- Q23 (agent, resolved 2026-10-25): the rules writer now gives `move` a way-open check (`evidence/open-attempt/q23/README.md`).\n- Q25 (agent, resolved by argument 2026-10-26): ways are two-way unless the description declares them one-way; the build is F6 below. Until it lands, each run's `TRACE_READ.md` names any resident stuck behind a way it already used, so it is not read as a refusal by the world.\n- Q26 (agent, open): the run page does not show an attempt in its owner's words or that it matched nothing (G17); S1 is not done until it does.\n- Q27 (Brian, open, re-opened 2026-10-26): does S2's same-moment fixpoint in `engine.py` count as the engine capability AGENTS.md and Decision 006 forbid? The earlier resolution was argued by this plan's author, so it goes to Brian. Recommendation: allow it as rule semantics inside the existing commit. Default: S2 waits; S1 and S3 go ahead.\n- Q28 (agent, open): whether S2's glass chain reuses the hand-written spill and damage processes (`src/world_substrate/mechanisms/damage.py:116`) or the rules writer writes its own; settled by reading and one free probe before S2.\n- Q30 (#244, agent, open): a build is accepted although its own test runs say a task is never possible; blocks A2 and A3 on a newly built world, not on the saved fixture.\n- Q31 (#245) and Q32 (#246) (agent, open): a refusal reason reads as a fact rather than a requirement, and the readout picked the goods-flow lens for a training world; neither changes an acceptance check's verdict, both change what a reader of the S1 run sees.\n- Q33 (agent, open in part): S3's seeded roll is settled by argument for where `run_seed` lives (drawn once per run, recorded in the run record, dice recorded per roll event, so replay never rolls and saved worlds without rolls replay unchanged; the 'no randomness' row becomes 'no unrecorded randomness'); open is whether the rules writer gives a generated person a skill field from the description (Sam's piloting 0), checked by a free probe before S3. A7 and A9 depend on it.\n- Q34 (agent, open): read scopes are recorded, not enforced; compiled rules derive their reads from their own checks, so only hand-written rules could leave F1's `blocked_by_event` or a Piece 2 parent link incomplete. Settled by a test-time read check before F1 relies on reads of hand-written rules.\n- Q22 / D2 (Brian): AI game master for unmatched attempts; default \"nothing comes of it\" stays.\n- Q36 (agent, open): how an interpreter misreading (a legal but wrong move) is caught; quoted spans, A2's negative fixture and a listed set of readings off their nearest kind, settled before A2 is judged. Injected visitor text cannot add a kind, entity or outcome (Q35, resolved).\n- Q37 (#241, agent, open): the builder added doorways around the wall and listed them as left out; A3 is judged on the saved fixture, whose wall is the only way.\n- Q38 (agent, open): #128 closes once A3 shows a refused wall attempt chosen from belief.\n- Q39 (agent, resolved by argument): a wait reading of an attempt with words is a silent no-op today; F9 lists it.\n- Q40 (agent, resolved by argument): S3's rolls sit in the causal model, so approval and the fingerprint cover them; the run seed is a run input; the compiler derives the roll's reads and writes (S3 row).\n- Interpreter cost per attempt (Q29, resolved 2026-10-26 from S1's live run): the 20 interpreter calls added 11.6% to\n  the run's other calls (about 24% at the 30-round cap), under the 30% that would require batching, so S1 keeps one\n  call per attempt.\n\n## Fixes settled by argument\n\nOpen questions that an argument already answers; each is small, agent-owned, built alongside the slices in its own\npull request, and checked on a free replay of a saved world before any paid run.\n\n| Id | Question | Fix | Check |\n| --- | --- | --- | --- |\n| F1 | Q2 | The refused row names the earlier event this round that changed what its failed checks read (`blocked_by_event`) | free replay of the saved airfield and c1r24 worlds: every refused row after a lost race names an accepted event id of that round |\n| F2 | Q6 | `/run` refuses a second request for the same session, round and base revision | a test that sends the same round twice: one run, one charge |\n| F3 | Q8 | A field a check reads that the build's spec names as used up, claimed or changed by a task, and that no rule writes, is a test-run finding; a fixed fact (the airfield wall's `components.boundary.passable`, read at `tests/fixtures/airfield-s1-live.json:392`, written by no rule) is not | the saved #218 build lists its resource; the airfield fixture's wall is not listed |\n| F4 | Q10 | The readout quotes `said_on_retry` when present, as the scene replay does | free replay of a saved menu-path run |\n| F5 | Q15 | Adopt the `~/code2` repository format (indexes over the existing documents) | the repo-format check reports compliant |\n| F6 | Q25 | Ways are two-way unless the description declares them one-way | regenerate the airfield world and probe both directions |\n| F7 | Q4 | A remedy's work answer says yes or no to the concern's question plus what was set, and the finished-task notice quotes it | a test that a remedy without that answer is refused and the notice quotes it; the next owner-allowance people-world run's TRACE_READ.md reads its notices |\n| F8 | Q9 | Task worlds' scripted test run lasts 24 rounds, like ongoing worlds, instead of 12 | the saved build fixtures score the same or better, and the garden world (#217) finishes inside the test run |\n| F9 | Q39 | An attempt with words that the interpreter read as `wait` is listed in the run summary as `read_as_wait` with the interpreter's why, beside `unmatched_attempts` | a test with a recorded wait reading of \"fly the helicopter\": the summary lists it; a literal \"wait\" is not listed |\n\n## Activation facts\n\nRecorded in [activation-facts.json](open_attempt/activation-facts.json): shared mechanism yes (engine and generator are shared by every world), no empirical comparison, LLM central yes, spend yes (owner allowance). Route: [path-decision.json](open_attempt/path-decision.json), durable_solo. The plan copies established methods (Inform 7, Event Calculus, Blades in the Dark,\nGURPS) but claims conformance to none of them, so `claims_external_standard` is false.\n\n## Durable documents\n\nDurable documents: system_model#ENT-ACTION-ENVELOPE, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, system_model#ENT-RUN-RECORD, plans\n\nS1 changes ENT-ACTION-ENVELOPE (the command gains its interpretation) and ENT-RUN-RECORD (the build\nrecord gains `unmatched_attempts`); S2 changes PROC-PROCESS-TICK and PROC-TRANSITION (reaction waves);\nS3 changes PROC-TRANSITION (rolls). Each ID is in `docs/model/trace.yaml` today. The roles are declared\nin `.agentic/repo.yaml` lines 3-8: `system_model: {prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`\nand `plans: docs/plans/`. At completion of each slice, `python3\n~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan\ndocs/plans/open_attempt.md --range <adoption revision>..HEAD` must exit 0.\n\n## Authority and non-goals\n\n**Authority:** Brian's \"yes\" on 2026-10-25 to adopt this plan and start S1; one agent writes; world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only.\n\n**Non-goals:** Organisations as agents, the code/fast-model/LLM decider spectrum, thinking as an effector, moving off\nConcordia 2.4.0, a clingo cross-check, and any change to Cybernetic Influence v3. Each comes after this.\n",
 "built_from": "c028b4b"
};
