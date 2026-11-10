window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/world-substrate",
  "subject_revision": "c99cbc704c5a8f2876c464b313373d343108cf1e",
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
       "runs": 33,
       "problems": 0
      }
     },
     {
      "name": "project check (tests, system model, docs)",
      "command": "PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --python 3.12 --with pydantic --with gdm-concordia==2.4.0 --with pytest --with pytest-xdist python scripts/check_project.py",
      "note": "counts from its line 'Neutral runtime tests: N passed, M skipped' (pytest-xdist)",
      "exit_status": 0,
      "counts": {
       "tests_run": 862,
       "failed": 0,
       "skipped": 2
      }
     },
     {
      "name": "wiki and Markdown cap",
      "command": "python3 $HOME/code2/project-meta/scripts/md_file_cap.py --repo . --ref HEAD",
      "exit_status": 0,
      "counts": {
       "md_files": 174,
       "cap": "exception",
       "orphans": 0
      },
      "note": "Run with --ref HEAD: without it the script checks the default branch, not this change."
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
     "world": "src/world_substrate/model.py:382",
     "engine": "src/world_substrate/engine.py:222",
     "event": "src/world_substrate/engine.py:572",
     "move": "src/world_substrate/action_authoring.py:49",
     "process": "src/world_substrate/engine.py:1095",
     "compiler": "src/world_substrate/action_authoring.py:456",
     "policy": "src/world_substrate/policy.py:50",
     "sense": "src/world_substrate/semantic.py:15",
     "profile": "src/world_substrate/profile.py:266",
     "write-scope": "src/world_substrate/engine.py:136",
     "causal-trace": "src/world_substrate/engine.py:572",
     "world-kind": "scripts/world_builder_service.py:116",
     "builder": "scripts/world_builder_service.py",
     "approval": "scripts/world_builder_service.py:421",
     "fingerprint": "scripts/world_builder_service.py:384",
     "information": "src/world_substrate/information.py:57",
     "run-loop": "scripts/run_authored_world.py:594",
     "contention": "scripts/run_authored_world.py:740",
     "resident": "scripts/concordia_residents.py:44",
     "task": "scripts/attempts.py:17",
     "notice": "scripts/attempts.py:234",
     "build": "scripts/world_builder_service.py:1591",
     "rules-retry": "scripts/world_builder_service.py:266",
     "test-run": "scripts/world_builder_service.py:1797",
     "run-log": "scripts/world_builder_service.py:556",
     "readout": "scripts/run_readout.py:125",
     "scene-replay": "scripts/render_scene_replay.py:398",
     "share": "scripts/world_builder_service.py:603",
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
     "affordance": "src/world_substrate/engine.py:395",
     "check": "src/world_substrate/rules.py:48",
     "attempt": "src/world_substrate/attempt.py:149",
     "attempt-reading": "src/world_substrate/attempt.py:81",
     "unmatched-attempt": "src/world_substrate/attempt.py:25",
     "observation": "src/world_substrate/engine.py:278",
     "place-way": "scripts/generate_world_bundle.py:96",
     "projection": "src/world_substrate/projection.py:44",
     "causal-parent": "src/world_substrate/rules.py:383",
     "exchange": "src/world_substrate/exchange.py:68",
     "mechanisms": "src/world_substrate/mechanisms/__init__.py:3",
     "kitchen": "reference_worlds/kitchen/mechanics.py",
     "mechanic": "src/world_substrate/action_authoring.py:456",
     "entity-component": "src/world_substrate/model.py:223",
     "knock-on-now": "src/world_substrate/engine.py:964",
     "world-law": "scripts/scaffold_world.py:45",
     "law-check": "src/world_substrate/laws.py:36",
     "resource": "scripts/scaffold_world.py:45",
     "world-design": "scripts/generate_world_bundle.py:53",
     "rules-review": "scripts/review_rules.py:92",
     "run-stop": "scripts/run_stop.py:65"
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
    "path": "docs/plans/declared_laws.md",
    "relies_on": [
     "world-law",
     "law-check",
     "rules-review",
     "gen-rules",
     "test-run",
     "build",
     "mechanic",
     "process",
     "knock-on-now",
     "engine",
     "entity-component",
     "write-scope",
     "rules-retry",
     "exchange",
     "causal-trace",
     "run-log",
     "world-design",
     "resource"
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
    "verdict": "pass",
    "reviewed_revision": "c99cbc704c5a8f2876c464b313373d343108cf1e",
    "package_commit": "686445ea2efb4978bc7a6207b4811e29f0a1c737"
   },
   "acceptance": {
    "status": "present",
    "path": "docs/planning/declared-laws/acceptance-criteria.json"
   }
  },
  "note": "This is the repository's package: covers the whole repository; its plan part points at the newest adopted plan, docs/plans/declared_laws.md, whose own package is docs/planning/declared-laws/planning-package.json. The open-attempt plan keeps docs/planning/open-attempt/planning-package.json. All three share the checks, open-questions ledger, domain model, metamodel and diagrams, and are rebuilt by tools/planning/ (open question Q41). Only this package is validated at each push; the two plan packages keep the revision of their own last review."
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
   "resolves_with": "Build and look: show each row's attempt text and reading in the round text and list summary.unmatched_attempts, then open the saved S1 airfield share (evidence/open-attempt/s1-airfield/) in a browser and confirm Sam's refused and unmatched attempts read in his own words.",
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
   "resolves_with": "Progress 2026-11-03 (#333): the engine's own checks now read as requirements ('the one acting is allowed to make this move', src/world_substrate/action_authoring.py:655; 'the {name} named exists', src/world_substrate/action_authoring.py:664) and shared recordings show the old engine names in the same plain words (scripts/world_builder_service.py:664); the rules writer's labels are still shown as written, so the question stays open for them. An argument settles the cause: the label is the rules writer's own sentence, shown as is. The choice is technical (ask the rules writer for requirement-style labels, or show 'needs: <label>' with actual against required); check on the saved airfield world's refused rows.",
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
   "resolves_with": "Reading the compiler settles generated rules: their reads are derived from their own selector, checks and effects (_derived_reads, src/world_substrate/action_authoring.py:173), so they cannot read outside them. Open are hand-written mechanisms and reference worlds. Technical choice: a test-time state view that records each hand-written rule's actual reads and fails on an undeclared one; check with a test rule that reads an undeclared field. The transition-engine spec keeps the measured recording-proxy design (openspec/specs/transition-engine/spec.md:379); until one lands the project check reports read_scopes_enforced as a constant (scripts/check_project.py:348, Q66).",
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
   "resolves_with": "Argument plus a check, no paid run: each reading keeps quoted_span per field (attempt.py:81), so a reader can compare the words with the kind. The plan's checks are A2's negative fixture (fly never binds to move) and the TRACE_READ.md sample of ordinary attempts. Technical addition: list every wait reading of a non-wait attempt (Q39) in the run summary so the trace read covers them all, not a sample. (Listing readings whose kind differs from nearest_kind would catch nothing: read_interpretation sets nearest_kind to the matched kind, attempt.py:122.)",
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
   "resolves_with": "Read #128's wanted list against the code: attempts from belief are built (S1, scripts/concordia_residents.py:45), part-way failure is built (Q19, scripts/attempts.py:131), and a person learns an outcome only from what they see (observation, engine.py:278). Close #128 once A3 shows a refused wall attempt chosen from belief in a saved run, citing that row.",
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
   "resolves_with": "Part argument, part the Q44 measurement. Argument: checks that report what the scripted test run actually saw (idle or stalled people, circling, moves never possible, people never together, refusals at the start) are observations of a real run, not guesses, so they stay. Checks that guess at bookkeeping from the rules' shape (conjuring processes, vanishing moves, second sources) retire one by one, each only when the saved world of its incident (docs/plans/declared_laws.md, Incidents) is refused by a declared law. Checks that guess at reachability (unsourced inputs, starved holders, unanswered demand, dead-end stock) cannot be replaced by laws (Q43); each becomes a report of what the test run saw (a move never possible, a field that only grew), which stays, or retires only when the review names its incident on the saved world. The missing-component check is a structural fact and stays. Moving processes retire only if the review names c4-run16's shape. Progress 2026-10-30: the people-world change (scripts/people_world.py:298) asks people worlds for laws and sends their rules to the review too. One live people-world build has run since (evidence/declared-laws/s4-waltzman-2/TRACE_READ.md:5): it declared no laws, which fits that world, and its review was skipped; #317 fixed the skip, and the next live people-world build (evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:3, 2026-11-04) exercised it: the designer again declared no laws (llm-calls id 23037 returned empty resources and laws) and the review ran (id 23042) with two findings, one of them that decision-postponed-at-deadline starts with max_postponements 0 so the decision can never be delayed; the build kept those rules without a rewrite (Q55). Laws can be dropped or left out (Q49), no check has been retired yet, and the retirement table is still owed.",
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
   "resolves_with": "Argument: a permissive law is model output read by the same outside reviewer, which is asked about moves that conjure or destroy a good the description says comes from somewhere (prompts/rules_reviewer.yaml:35). So S4 retires a conjuring check only when the review names the conjuring move on the incident's saved world, not when a law merely exists. That rule is the answer; it stays open until S4 applies it to the conjuring checks' saved worlds, and reopens if the review misses a permissive law on one of them.",
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
   "resolves_with": "Argument from the runs: the review already looks for 'a purchase that moves goods but no money' (prompts/rules_reviewer.yaml:30-31) whether or not a law names it, so the catch is the review, not the law. S4 therefore retires a pairing check only when the review names the unpaid move on the incident's saved world; the s3-review-choice run shows that held for pencil13 (gemini) and failed for pencil-s2-kept (no reviewer), so the pairing checks stay until the review catches pencil-s2-kept. Asking the designer for a pairing law on every move that changes two holders' stock is the other route; it is a prompt change to try only if the review keeps missing it.",
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
   "blocks": "Whether the paid builds in S5, L5, A4 and A6 run now, and which defect is fixed next. Merges under the plan stay ungated by Brian's review; only new paid builds wait.",
   "resolves_with": "Brian's judgement on a working run, not a test: he reads one shared Waltzman run and says what is wrong. Since 2026-11-04 a shared run recorded after #317 and #320 exists: the Waltzman rebuild at 096c129, share jyVbywXT8N8F (evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:3, saved without a readout), but its rules carry a review finding the build kept (no postponement possible, Q55), and the rules are written afresh on each build (5 of 5 needed and no postponement here, 4 of 5 and one postponement in s4-waltzman-2, evidence/declared-laws/s4-waltzman-3/TRACE_READ.md:16), so it is the one to judge only once Q55 is answered or with that caveat stated beside it; the recommendation to keep one saved world and improve it is what makes builds that differ comparable. His first reaction (\"this is blank and doesnt play\") was answered by #328 and #329: a shared run's picture is now drawn from its recorded rounds (scripts/world_builder_home.html:913).",
   "owner": "brian",
   "status": "resolved",
   "recommendation": "Finished when Brian reads one shared Waltzman run and the people behave believably and something surprising follows from their choices. Keep one saved world and improve it; his reaction to it picks the next fix.",
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
   "resolves_with": "The shared case held twice: the probes behind the issue (786 links, no NaN) and a browser check on 2026-11-03 (no console error, links drawn). Only the live first-round case stays unreproduced. Read the console in the next live run; no paid run for this alone.",
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
   "resolves_with": "Reading what the person asked tries in the next round. Replaying a saved world through /run costs cents and needs no rebuild; a new build needs Brian's yes.",
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
   "resolves_with": "Reading, no paid run: the recorded rounds keep each person's stated reason and what they could see; read the 12 refused rows' reasons against the open-concern state they were shown.",
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
   "resolves_with": "The cause by reading, no paid run: the people-world loop breaks before a rewrite once the build has run longer than PEOPLE_REWRITE_BY_S (80 s, scripts/world_builder_service.py:266, checked at :2254); this build's first call was 15:53:10 and its review returned 15:55:29, while cost ($0.14) was far under PEOPLE_WORLD_BUDGET ($1.30, :94), so the time limit is the likely cause; the progress line that would confirm it is not saved. What remains is technical: when the review names a rule, either rewrite despite the time limit or keep the rules and show the finding beside the run. Check it on a free replay of the saved world before any new build.",
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
   "resolves_with": "Argument first: a declared world law (scripts/scaffold_world.py:45, src/world_substrate/laws.py) already balances a named resource inside the same commit, so a world that declares the quantity as a resource gets the check. For paths no law covers the choice is technical: have the scripted test run list each declared write path that no accepted event ever changed. Check it free on a copy of the M4 spill rule with one write removed.",
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
   "resolves_with": "Reading, no paid run: read the interpreter rows of the saved declared-laws and open-attempt runs for a string value the world does not mean. If one appears, add declared values to string fields and have the compiler and the attempt reading refuse others; if none appears, record the gap as not yet earned and close it.",
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
   "resolves_with": "One counterexample settles it: look in the saved pasted descriptions (evidence/declared-laws) for a promise other than support for the decision. If one exists and the people-world rules cannot hold it, build the Commitment kind from Singh's states; if every case is decision support, close it as covered.",
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
   "resolves_with": "Argument first, no paid run: list which parts of such a description the fixed families in spikes/any-scenario-2026-10/compile_spec.py cannot hold, by reading compile_spec.py and assemble_people_world. A paid build of a different situation waits for Q50 and Q60.",
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
   "resolves_with": "A priority call by Brian: the review's recommendations are proposals and none is adopted (docs/audits/waltzman-lineage-review-2026-11-07.md:121).",
   "owner": "agent",
   "status": "resolved",
   "recommendation": "Yes: run the bounded comparison first on the existing Waltzman case and one materially different case, starting with the plain version (one model given the whole scenario, each person's view and an event ledger, its proposed changes validated), per the 2026-11-06 plain-version rule; state the question and what result counts against each approach before running, and measure one complete case before any batch.",
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
   "resolves_with": "Prior-art reading, no run: map each onto the field or claim it would serve (PROV-O onto cause and causal_parent_event_ids; effect typing onto _derived_reads and _derived_writes at src/world_substrate/action_authoring.py:173; Halpern-Pearl onto the exact-history intervention). Adopt one only where it replaces project code or makes a claim checkable; otherwise record compose or reject with the reason.",
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
   "resolves_with": "The semantic-binding spec's vocabulary coverage audit is the procedure (openspec/specs/semantic-binding/spec.md:79): run it when a world first needs one of these terms. No run until then.",
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
   "resolves_with": "Answered by argument in docs/plans/estimate_rules.md (Decided 1-7); closes when slice E1 lands and its acceptance checks A1-A3 pass. The contract carried from the retired Jev note and kept: an estimate is a recorded, non-authoritative input, like the skill roll's recorded dice; it never becomes canonical state or consequence authority by itself, only through an installed rule that declares its question, reads, answer type, model, a required fallback and its outcomes, and turns a chance into an outcome by a recorded draw from the run seed (never a threshold); the event records the estimate, its inputs and the model version; replay reads the record and never calls Jev; approximate ranking never silently drops a valid action.",
   "owner": "agent",
   "status": "open",
   "sources": [
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
   "resolves_with": "Technical, no run: key the binding by the installed mechanic (or have the profile carry it), and add a test that a non-Castaway world's give event carries no Castaway mechanic id.",
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
   "resolves_with": "Technical, no run: add optional resources and laws to the schema matching _validate_laws, and a test that one saved law-bearing bundle passes both the schema and the validator.",
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
   "resolves_with": "Technical: when Q34's read check lands, compute the fact from code (for example whether the Engine hands rules a read-recording view); until then the check's output names the fact as a constant.",
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
   "resolves_with": "Technical, no run: bind each placeholder to the participant of the same name, and add a test rule that writes the wrong participant through a correctly shaped path and is refused.",
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
   "question": "The repository has no lockfile or pyproject (the project check installs pinned names with uv --with at run time), and the Castaway extractor's check (scripts/extract_castaway_fixture.py --check, run by check_project.py --with-donors) needs a donor checkout at ../castaway-world/worktrees/world-systems (references/sources.json:8); on 2026-11-09 that checkout did not exist under /home/brian/code2/castaway-world and the check exited 1. What should change?",
   "blocks": "Reproducing a run's exact dependencies, and running the donor check at all.",
   "resolves_with": "Technical: add a lockfile when a dependency enters a reproducible production path (roadmap hardening queue); make the donor check report the missing checkout as skipped with its path, or restore the donor worktree from the archived castaway-world repository at the pinned revision.",
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
   "resolves_with": "Technical, no paid run: add the compiler version to the frozen identity; record overflow as a finding when discovery reaches the cap; record a mechanic exception as a refused event with the exception text. One test each.",
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
   "resolves_with": "Technical: move what the live path imports into scripts/ or src/ when it is next changed, keeping its tests; no run needed.",
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
   "short": "Living-scene profiles refuse a render key the layout reads (plausible)",
   "question": "Plausible, not reproduced: the living-scene v1 loader refuses unknown top-level keys and 'render' is not among the allowed ones (src/world_substrate/living_scene.py:22), while the layout documents a radius read from the profile's render.gather_radius (src/world_substrate/living_scene_layout.py:19) and the composed renderer reads visual['render'] (scripts/render_composed_living_scene.py:59). Is a v1 profile with a render block refused?",
   "blocks": "Whether a scene author can set the gather radius the layout documents.",
   "resolves_with": "Reading plus one free test: load a v1 profile with a render block; if it is refused, allow the key (or move the setting under presentation) and fix the docstring.",
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
   "resolves_with": "Argument: read it against today's Concordia resident path. Decision records are not edited; arc42 section 9 states the reading, and a later decision record restates it if the condition is ever tested.",
   "owner": "agent",
   "status": "open",
   "sources": [
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
   "resolves_with": "Argument, in J2's design: an attempt whose effect needs another resident's act is routed to that resident (the #326 request path, generalised); the judge sees only what remains. One counterexample from the port world would reopen it.",
   "owner": "agent",
   "status": "open",
   "sources": [
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
   "resolves_with": "Prior art first: Crawford and Ostrom's grammar of institutions, Institutional Grammar 2.0 (Frantz and Siddiki), and Cybernetic Influence v3's split of identity proof, permission, availability and outcome; a short design step opens J4.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/ai_judge.md:497",
    "docs/plans/ai_judge.md:204"
   ],
   "touches": [
    "norm",
    "credential-holder",
    "world-law"
   ]
  },
  {
   "id": "Q77",
   "short": "Wiki cap and durable-document checks fail on main",
   "question": "On origin/main 0dcbcd6 the wiki and Markdown cap check (md_file_cap.py --repo . --ref HEAD) exits 1: the file count is now within the exception limit (143 of 180), but 13 documents are more than two links deep from the entry point (for example docs/VISUAL_FEEDBACK.md, docs/audits/kitchen-contested-world.md) and the durable-document check (durable_docs_check.py --arc42) reports 12 findings (3 arc42 headings, 1 extension label, 2 goal fields and 2 goal context or lineage findings in docs/architecture/arc42.md, and 4 system-model rules whose owner files, scripts/world_builder_service.py (3 rules) and scripts/run_authored_world.py (1), changed after their last review in a commit that only reworded a comment). Should the deep documents be linked closer or retired, and the arc42 and goal fields and rule reviews brought up to date?",
   "blocks": "Whether the wiki-compliance and durable-document checks pass again for every package in this repository.",
   "resolves_with": "Argument: read the 13 deep documents and link or retire them by the documentation rules (docs/AGENTS.md); fill the arc42 goal fields from docs/GOAL.md; re-read the 4 rules against the comment-only changes in those two files and set reviewed_at. No run needed.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/ai-judge/checks.txt:3",
    "docs/planning/ai-judge/checks.txt:32"
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
   "resolves_with": "One probe, E1's first step before the live run: 10 Jev calls, one for each of days 1 to 10 since service at load 14 (about $0.0003, measured per-call cost $0.0000279 from llm-cost estimate --task feedback-collector.triage --model jev), run as E1's first step. If flat, E1 reports it and the rule's question or reads change before the live run.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:454",
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
   "question": "Jev sees only the fields an estimate rule declares (days since service, load), never the whole world: argument settles that (a whole-world read makes the cache key the whole world and can reach what A5 forbids). Do the sawmill rule's two declared reads leave out facts Jev needs, as the plain version (Jev given the whole world) would show?",
   "blocks": "Which fields the E1 sawmill rule declares, and from E2 a rules-check warning when a rule reads too little; not the declared-reads design.",
   "resolves_with": "E1's side-by-side comparison on 10 cases: Jev with the declared reads, Jev with the whole world, and gpt-6-luna with the declared reads (under $0.01, computed in docs/plans/estimate_rules.md 'LLM call boundary and cost'). If the whole-world answers track the facts better, the rule declares more reads; it never reads the whole world.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:435",
    "docs/plans/open_attempt.md:194"
   ],
   "touches": [
    "estimate-rule",
    "estimator"
   ]
  },
  {
   "id": "Q84",
   "short": "A chance that someone notices",
   "question": "How should a chance decide whether an observation reaches a person (the harbourmaster noticing a hand-over), given that information delivery is not a field write?",
   "blocks": "Slice E5 and the port part of A5.",
   "resolves_with": "A short design step opening E5: an estimate on the delivery of an information item (src/world_substrate/information.py:57), recorded like any estimate; what the person does after stays their resident's choice.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:109",
    "src/world_substrate/information.py:57"
   ],
   "touches": [
    "estimate-rule",
    "information",
    "resident"
   ]
  },
  {
   "id": "Q85",
   "short": "Jev latency in worlds with many chances",
   "question": "Successful Jev calls averaged 0.43 s, but 6.6% failed (network failures after 20.2 s on average), measured in ~/projects/data/llm_observability.db, 2026-11-10. With a 5 s timeout and one retry a chance takes about 0.61 s on average and at most 10 s (computed), about 18 s for a 30-day sawmill run; a world with many estimate rules could ask thousands of times. Does sequential asking fit the run-time targets?",
   "blocks": "Worlds with many estimate rules after E1; not E1 itself.",
   "resolves_with": "E1's measured run times; add parallel asking within one moment only if a run shows it is needed.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:311"
   ],
   "touches": [
    "estimator",
    "run-loop"
   ]
  },
  {
   "id": "Q86",
   "short": "Jev for the plain-words stopping point",
   "question": "The judge plan's J5 asks the judge after a changed round whether a plain-words stopping point is reached (about $0.0016 per call, gpt-6-luna). A Jev chance question over the world state would cost about 1/50 of that. Should J5 use Jev?",
   "blocks": "Nothing in the estimate-rules plan; an option for the judge plan's J5.",
   "resolves_with": "The judge plan's call when J5 is built: Jev answers a probability that J5 would turn into stop or not, and Jev has not been shown to read a whole world's state well; J5 can test it on its own saved runs.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/plans/estimate_rules.md:421",
    "docs/plans/ai_judge.md:264"
   ],
   "touches": [
    "stopping-point",
    "estimator"
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
    "explain": "Something a person may try; its rule has checks and effects, compiled before use. Code: src/world_substrate/action_authoring.py:49."
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
    "explain": "Two choices a build makes first: whether the description is about people (people path) or things (causal path), and whether the world is a task, ongoing or open. Code: scripts/world_builder_service.py:116."
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
    "explain": "A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. Code: scripts/world_builder_service.py:421."
   },
   {
    "id": "fingerprint",
    "label": "World fingerprint",
    "kind": "Substrate",
    "explain": "A short hash of the bundle and rules that ties builds, rounds and shares to one world. Code: scripts/world_builder_service.py:384."
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
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run. Code: scripts/run_authored_world.py:714."
   },
   {
    "id": "contention",
    "label": "Lost race",
    "kind": "Substrate",
    "explain": "When an earlier move this round changed the state, an open attempt is resubmitted as is at the new revision and only its rule's checks decide it; menu paths resubmit the move if still offered, else ask once more. The refused row names the failed checks, not the event that blocked it. Code: scripts/run_authored_world.py:740."
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
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score. Code: scripts/world_builder_service.py:1591."
   },
   {
    "id": "rules-retry",
    "label": "Rules retry",
    "kind": "Substrate",
    "explain": "A second rules attempt after a rejection or weak score; skipped after 80 s. Code: scripts/world_builder_service.py:266."
   },
   {
    "id": "test-run",
    "label": "Scripted test run",
    "kind": "Substrate",
    "explain": "The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. Code: scripts/world_builder_service.py:1797."
   },
   {
    "id": "run-log",
    "label": "Run log",
    "kind": "Substrate",
    "explain": "One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. Code: scripts/world_builder_service.py:556."
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
    "explain": "A saved run rebuilt from the run log that a visitor replays with no AI calls. Code: scripts/world_builder_service.py:603."
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
    "explain": "What one actor sees this round: the fields its senses and position allow, never the whole world. Code: src/world_substrate/engine.py:278."
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
    "explain": "Plan declared-laws S3 (built): a separate model call with a fresh context reads the description, the declared laws and the written rules, and lists concrete mismatches (each naming a rule and the words it contradicts) for the rules writer to fix; findings, never a pass mark. Runs on things worlds and, from 2026-10-30, on people worlds. Code: scripts/review_rules.py:92."
   },
   {
    "id": "consequence-report",
    "label": "Consequence report",
    "kind": "Theory",
    "explain": "Plan ai-judge J1 (planned, not implemented): what the engine works out for an attempt no rule covers, in two passes. Pass 1, with no new rule: engine.discover for the person acting and for each person the attempt names (their moves, with which checks pass or fail), plus the current values of the entities the attempt names. Pass 2: the judge's proposed rule test-run on a copy of the world, giving its net changes, blockers, chain length and stopping point; the full chain stays in the run record. Code: none yet."
   },
   {
    "id": "judge-ruling",
    "label": "Judge ruling",
    "kind": "Theory",
    "explain": "Plan ai-judge J2 (planned, not implemented): Concordia's game master (EventResolution), given the whole world and pass 1 of the consequence report, proposes a rule for the constraint an unmatched attempt raises (can coins change hands here?); after reading the pass 2 test run of that rule it confirms, revises once or withdraws. Never an outcome or another person's choice. Code: none yet."
   },
   {
    "id": "ruling-rule",
    "label": "Ruling-origin rule",
    "kind": "Theory",
    "explain": "Plan ai-judge J3 (planned, not implemented): a rule in the existing declaration language made from a confirmed judge ruling after it passes the World Builder rules check and test run, recording the ruling id and round it came from; it applies to everyone in the same situation and the attempt settles through it. A ruling the language cannot express is refused and recorded as a language gap. Code: none yet."
   },
   {
    "id": "credential-holder",
    "label": "Credential holder",
    "kind": "Theory",
    "explain": "Plan ai-judge J4 (planned, not implemented): who holds a credential (a password, a signed release) as a fact in the world that can change: told, overheard, copied, forged or phished. The mechanism checks the credential, not the holder. Code: none yet."
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
    "kind": "Theory",
    "explain": "Plan ai-judge Decided 5 (planned, not implemented): a per-world option, 'Judge rulings during a run': Approved by Create (default; a checked ruling is installed at once and the attempt settles through it) or Wait for my approval (the proposed rule is held, the attempt waits as pending, Approve installs the rule and settles it, Reject refuses it; nothing settles without an installed rule). Code: none yet."
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
    "explain": "Plan ai-judge J5 (planned, not implemented): a stopping point the person writes in plain words ('stop once the team has agreed a budget'), assessed by the judge after each round that changed something, as one more condition of the run stop setting. Code: none yet."
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
    "source": "ruling-rule",
    "target": "judge-ruling",
    "label": "made from"
   },
   {
    "id": "e112",
    "source": "rules-review",
    "target": "ruling-rule",
    "label": "checks"
   },
   {
    "id": "e113",
    "source": "ruling-rule",
    "target": "mechanic",
    "label": "is a"
   },
   {
    "id": "e114",
    "source": "midrun-setting",
    "target": "ruling-rule",
    "label": "decides when installed"
   },
   {
    "id": "e115",
    "source": "midrun-setting",
    "target": "approval",
    "label": "amends"
   },
   {
    "id": "e116",
    "source": "run-stop",
    "target": "run-loop",
    "label": "ends"
   },
   {
    "id": "e117",
    "source": "budget",
    "target": "run-stop",
    "label": "is separate from"
   },
   {
    "id": "e118",
    "source": "stopping-point",
    "target": "run-stop",
    "label": "one condition of"
   },
   {
    "id": "e119",
    "source": "judge-ruling",
    "target": "stopping-point",
    "label": "same game master assesses"
   },
   {
    "id": "e120",
    "source": "credential-holder",
    "target": "entity-component",
    "label": "is kept in"
   },
   {
    "id": "e121",
    "source": "credential-holder",
    "target": "information",
    "label": "can change by"
   },
   {
    "id": "e122",
    "source": "norm",
    "target": "world-law",
    "label": "is not a"
   },
   {
    "id": "e123",
    "source": "norm",
    "target": "observation",
    "label": "has consequences through"
   },
   {
    "id": "e124",
    "source": "estimate-rule",
    "target": "process",
    "label": "is a kind of"
   },
   {
    "id": "e125",
    "source": "estimate-rule",
    "target": "estimator",
    "label": "asks"
   },
   {
    "id": "e126",
    "source": "estimator",
    "target": "recorded-estimate",
    "label": "writes"
   },
   {
    "id": "e127",
    "source": "estimate-rule",
    "target": "recorded-draw",
    "label": "decides by"
   },
   {
    "id": "e128",
    "source": "recorded-draw",
    "target": "run-seed",
    "label": "comes from"
   },
   {
    "id": "e129",
    "source": "recorded-estimate",
    "target": "causal-trace",
    "label": "recorded in"
   },
   {
    "id": "e130",
    "source": "recorded-draw",
    "target": "causal-trace",
    "label": "recorded in"
   },
   {
    "id": "e131",
    "source": "estimate-rule",
    "target": "knock-on-now",
    "label": "sets off"
   },
   {
    "id": "e132",
    "source": "skill-roll",
    "target": "recorded-draw",
    "label": "also uses"
   },
   {
    "id": "e133",
    "source": "estimate-rule",
    "target": "resident",
    "label": "never decides for"
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
    "id": "Q15",
    "label": "Q15: Repository format files not yet added",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether the repo-format check passes."
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
    "id": "Q63",
    "label": "Q63: A non-authoritative estimate as a rule input",
    "kind": "AgentQuestion",
    "explain": "Blocks: The estimate-rules plan (docs/plans/estimate_rules.md) and its first slice E1; any world whose rules need a chance or amount that no installed mechanic computes.."
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
    "label": "Q72: Living-scene profiles refuse a render key the layout reads (plausible)",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether a scene author can set the gather radius the layout documents.."
   },
   {
    "id": "Q73",
    "label": "Q73: Decision 006's wrong-when names a missing adapter",
    "kind": "AgentQuestion",
    "explain": "Blocks: Whether that wrong-when condition can ever be checked.."
   },
   {
    "id": "Q75",
    "label": "Q75: Constraint question or someone's choice",
    "kind": "AgentQuestion",
    "explain": "Blocks: J2's routing step and A5 (Rosa's own resident decides accept or refuse).."
   },
   {
    "id": "Q76",
    "label": "Q76: How to write norms and credential holders",
    "kind": "AgentQuestion",
    "explain": "Blocks: J4's design and A6 (the password fixture: Mallory phishes Alice's password, is logged in, and the breach has consequences only after an observer acts).."
   },
   {
    "id": "Q77",
    "label": "Q77: Wiki cap and durable-document checks fail on main",
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
    "id": "Q83",
    "label": "Q83: Do the declared reads leave out facts Jev needs",
    "kind": "AgentQuestion",
    "explain": "Blocks: Which fields the E1 sawmill rule declares, and from E2 a rules-check warning when a rule reads too little; not the declared-reads design.."
   },
   {
    "id": "Q84",
    "label": "Q84: A chance that someone notices",
    "kind": "AgentQuestion",
    "explain": "Blocks: Slice E5 and the port part of A5.."
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
    "id": "compiler",
    "label": "Compiler",
    "kind": "Concept",
    "explain": "Turns proposed rules into installed rules and derives what each may read and write."
   },
   {
    "id": "credential-holder",
    "label": "Credential holder",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan ai-judge J4 (planned, not implemented): who holds a credential (a password, a signed release) as a fact in the world that can change: told, overheard, copied, forged or phished. The mechanism checks the credential, not the holder."
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
    "id": "information",
    "label": "Information item",
    "kind": "Concept",
    "explain": "A piece of information with a source and per-recipient deliveries; hidden until delivered."
   },
   {
    "id": "judge-ruling",
    "label": "Judge ruling",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan ai-judge J2 (planned, not implemented): Concordia's game master (EventResolution), given the whole world and pass 1 of the consequence report, proposes a rule for the constraint an unmatched attempt raises (can coins change hands here?); after reading the pass 2 test run of that rule it confirms, revises once or withdraws. Never an outcome or another person's choice."
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
    "id": "norm",
    "label": "Norm",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan ai-judge J4 (planned, not implemented): what people expect or forbid (bribery is illegal; only Alice should log in). It can be broken; a breach is recorded and has consequences only when someone notices and acts. Never written as a declared law."
   },
   {
    "id": "observation",
    "label": "Observation",
    "kind": "Concept",
    "explain": "What one actor sees this round: the fields its senses and position allow, never the whole world."
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
    "id": "recorded-estimate",
    "label": "Recorded estimate",
    "kind": "Concept",
    "dashed": true,
    "explain": "Plan estimate-rules E1 (planned, not implemented): on the event, the question, the declared inputs and their values, Jev's answer, the model version returned, the trace id, the cost and whether it was reused from the run's cache; evidence, never world state (Q63)."
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
    "explain": "Plan declared-laws S3 (built): a separate model call with a fresh context reads the description, the declared laws and the written rules, and lists concrete mismatches (each naming a rule and the words it contradicts) for the rules writer to fix; findings, never a pass mark. Runs on things worlds and, from 2026-10-30, on people worlds."
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
    "explain": "Plan ai-judge J5 (planned, not implemented): a stopping point the person writes in plain words ('stop once the team has agreed a budget'), assessed by the judge after each round that changed something, as one more condition of the run stop setting."
   },
   {
    "id": "support",
    "label": "Support",
    "kind": "Concept",
    "explain": "A member's stance on the decision: none, full or conditional on a concern."
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
    "id": "Q63-mechanic",
    "source": "Q63",
    "target": "mechanic",
    "label": "bears on"
   },
   {
    "id": "Q63-skill-roll",
    "source": "Q63",
    "target": "skill-roll",
    "label": "bears on"
   },
   {
    "id": "Q63-estimate-rule",
    "source": "Q63",
    "target": "estimate-rule",
    "label": "bears on"
   },
   {
    "id": "Q63-recorded-estimate",
    "source": "Q63",
    "target": "recorded-estimate",
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
    "id": "Q73-resident",
    "source": "Q73",
    "target": "resident",
    "label": "bears on"
   },
   {
    "id": "Q75-judge-ruling",
    "source": "Q75",
    "target": "judge-ruling",
    "label": "bears on"
   },
   {
    "id": "Q75-resident",
    "source": "Q75",
    "target": "resident",
    "label": "bears on"
   },
   {
    "id": "Q76-norm",
    "source": "Q76",
    "target": "norm",
    "label": "bears on"
   },
   {
    "id": "Q76-credential-holder",
    "source": "Q76",
    "target": "credential-holder",
    "label": "bears on"
   },
   {
    "id": "Q76-world-law",
    "source": "Q76",
    "target": "world-law",
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
    "id": "Q83-estimate-rule",
    "source": "Q83",
    "target": "estimate-rule",
    "label": "bears on"
   },
   {
    "id": "Q83-estimator",
    "source": "Q83",
    "target": "estimator",
    "label": "bears on"
   },
   {
    "id": "Q84-estimate-rule",
    "source": "Q84",
    "target": "estimate-rule",
    "label": "bears on"
   },
   {
    "id": "Q84-information",
    "source": "Q84",
    "target": "information",
    "label": "bears on"
   },
   {
    "id": "Q84-resident",
    "source": "Q84",
    "target": "resident",
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
 "next_plan": "---\nplan_id: \"declared-laws\"\ndependencies: []\ndependencies_reviewed: \"2026-10-28\"\nplanning_path: reset\nplanning_path_ref: docs/plans/declared_laws/path-decision.json\nmethod_conformance_receipt: docs/plans/declared_laws/conformance-receipt.json\nstatus: adopted\ngoal:\n  outcome: \"A World Builder world stops depending on a growing list of hand-written checks for past bugs: the AI that designs a world also declares that world's own laws (which goods can only appear or vanish through which moves, and what a move such as a purchase must move each way); the engine refuses any move or knock-on effect that breaks a declared law and names the law; and a separate AI review, not the rules writer, reads the written rules against the description and the laws and lists concrete mismatches for the rules writer to fix.\"\n  canonical_example: \"Paste the pencil description (~/code/.scratch/open-attempt-s2/pencil.txt, the one behind pencil2-pencil14) into https://brianmills.dev/world-builder/ and press Create simulation. The build record lists the world's declared laws in plain words (for example 'pencils are made only by the factory's make move' and 'buying boxed pencils moves boxes to the shop and cash to the factory'); a move whose rules would make pencils from nothing or take boxes without paying is refused in the test run with that law named, and the rules writer is told so; the review lists any rule that contradicts the description (pencil13's buy-boxed-pencils, which paid nothing) by name; and the world that is kept runs with no law refusals from its own rules.\"\n  forbidden_substitutes: \"a fixed list of built-in move types that every world must use (Brian 2026-10-28: it 'destorys the whol e potin'); laws or rules written by hand for the pencil world; pencil-specific or Waltzman-specific code paths; a review by the same call or context that wrote the rules; a review that returns a pass mark instead of findings; retiring a heuristic check without showing that the saved world of each incident it caught is refused by a law or named by the review; laptop runs presented as live; runs without run-log.jsonl and a TRACE_READ.md that scripts/check_trace_reads.py passes; rerunning until a behavior appears and reporting only that run.\"\n  boundaries: \"world-substrate and its own deploy only; Cybernetic Influence v3 and Concordia read-only; each slice merges after scripts/check_project.py exits 0 on the committed change, then deploys and the live commit is confirmed through the health endpoint; saved worlds without laws replay unchanged; owner allowance only, visitor allowance stays $3/day, no new spend route without Brian's yes; free replays of saved worlds before any paid run; publish-checker before anything new goes public; never restart WSL.\"\n  done_when: \"Acceptance checks L1-L8 below pass, each judged from the full trace of the run it names.\"\n  do_not_gate_on: \"a static build-time proof of laws (Q46: deferred); laws of shapes other than totals and pairings (Q43); the AI game master for unmatched attempts (Decision D2 of the open-attempt plan); the open-attempt plan's S3 skill rolls; Brian's review of a run.\"\n  stop_after: 3\nconflict_surfaces:\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/declared_laws.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/plans/declared_laws/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/planning/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/declared-laws/review-page/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: proposals/planning-package/review-page/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tools/planning/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/model/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: roadmap/README.md, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/engine.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/laws.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/rules.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/build_metamodel.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: src/world_substrate/action_authoring.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_world_bundle.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/scaffold_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/generate_causal_model.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/review_rules.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_service.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/run_authored_world.py, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: scripts/world_builder_home.html, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: prompts/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: tests/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: evidence/declared-laws/, access: write}\n  - {kind: repository_path, repository: BrianMills2718/world-substrate, target: docs/catalog.md, access: write}\n---\n# Plan: worlds declare their own laws, the engine enforces them, and an independent review reads the rules\n\nPlanning package: docs/planning/declared-laws/planning-package.json\n\n<!-- planning-compliance-checklist:v1 -->\n## Compliance checklist\n\nWritten by `plan_checklist.py --write`, not by hand. `--check` re-runs the validator and fails\nif any line below differs from what it says now. Unticked pending items are not passes.\n\nManifest: `docs/planning/planning-package.json`\nPackage revision: `c99cbc704c5a`\nVerdict: compliant, 2 pending\n\n- [ ] part investigation: pending\n- [x] part checks: ok\n- [x] part open_questions: ok\n- [x] part system_model: ok\n- [x] part domain_model: ok\n- [x] part diagrams: ok\n- [x] part plan: ok\n- [x] part acceptance: ok\n- [x] part review_page: ok\n- [x] part cold_review: ok\n- [ ] substance route follows from its path decision: failing\n- [x] substance citations resolve: ok\n- [x] substance domain model has a glossary: ok\n- [ ] substance project layer checks against the planning layer: failing\n- [x] substance concepts point at their code: ok\n- [x] substance plan names the concepts it relies on: ok\n- [x] substance type-level model of executable rules: ok\n- [x] substance cold review read this revision: ok\n- [ ] initiative initiative names its home: pending\n- [ ] tiers spectrum rungs 1-11 are cited: failing\n- [ ] tiers production rungs 12-14 are cited when it runs in production: failing\n- [ ] tiers thesaurus separates near-identical names (rung 4): failing\n- [x] coverage goal coverage: ok\n- [x] freshness package is current: ok\n<!-- /planning-compliance-checklist -->\n\n\nThis is the plan's own package. The repository's package (`docs/planning/planning-package.json`, page\n`proposals/planning-package/review-page/`) covers the whole repository; its plan part now points at this plan,\nand both share the checks, open-questions ledger, models and diagrams rebuilt by `tools/planning/` (Q41).\n\nReview page: [proposals/declared-laws/review-page/](../../proposals/declared-laws/review-page/index.html), live at\n<https://hive.brianmills.dev/plans/world-substrate/main/proposals/declared-laws/review-page/>.\n\n## Actor and result\n\n**Actor:** a World Builder visitor (and Brian as owner) who pastes a description and watches the generated world\nrun. **Result they can inspect:** the build record lists the world's declared laws in plain words, every move the\nlaws refused (with the law named), and the independent review's findings; the run page shows a world whose goods\ncome from somewhere and go somewhere. **Stable example:** the pencil description in the front matter.\n\n## Project outcome\n\nProject outcome: roadmap/README.md#actor-recurring-job-and-investment-boundary (generative living worlds on top,\nrigorous causal engine underneath). **External job the World Builder serves:** the visitor (an analyst such as Rand\nWaltzman exploring an influence scenario, a teacher, a planner of a small supply chain) is thinking through how a real\nsituation could play out: who would do what, what would run out, what a change would set off. **Their baseline without\nit:** a tabletop exercise or wargame with people playing the parts, a written scenario, or a spreadsheet or\nstock-and-flow model they build by hand; each is slow to set up, and a spreadsheet keeps the books but does not let\npeople try things freely. **How the World Builder helps:** it turns their plain description into a running world in\nminutes, in which people try moves freely and the books are kept, so they can watch the situation unfold and rerun it.\nThis plan serves that job by making the books right (money and goods neither appear nor vanish except as the world's own\nlaws allow), which a reader needs before trusting what the run shows. **Recurring job and baseline:** a visitor describes a world and watches it run.\nBaseline from pencil2 to pencil14 (2026-10-27/28): each live build found one more way the rules writer got the\nbookkeeping wrong (goods from nothing, stock with nowhere to go, a purchase that pays nothing, a move that changes\nnothing, a malformed field path), and each was fixed by one more hand-written check in\n`scripts/world_builder_service.py:922-1272`, some of which then raised false alarms. pencil14 at `5d6a48e` failed\noutright (422 after about 287 s, job `f0b6d1a3dc0a40848456e6fe2ce172c0`: \"mechanic installer rejected\nshipment-arrival: malformed_path\"; driver log in `evidence/pencil14-build-failure/`). **Inspectable result of this plan:** the canonical example above, live.\n\n## Outcome step\n\nOutcome probe: `roadmap/README.md#canonical-outcome-probe`\nObserved: `evidence/pencil13-trace-audit/TRACE_READ.md`\nStep: step 2 of the probe, \"The builder generates the world (places, things, people, the moves they may attempt) and its rules.\"\nClass: vertical\n\npencil13 is the last live pencil run read round by round: 5 sales moved cash, goods were conserved along factory,\ntruck, shop and customer, and the shop's buy-boxed-pencils move paid the factory nothing, which no check caught.\nEach slice changes the build and the run end to end and ends in a live traced run.\n\n## Why, in one example\n\nThe rules writer is a capable model: it knows that buying pencils means paying for them. But it writes every move as\nraw field changes (\"add 10 to shop.boxes, subtract 10 from factory.boxes\"), and nothing compares those changes with\nwhat it knows. So a purchase that forgets the payment installs and runs (pencil13). Our answer so far was a new\ncheck per mistake, each guessing at meaning from the rules' shape. Brian, 2026-10-28: \"my guess is that you hjave been\nfixing symptoms not root problems\". Fixed move types (transfer, exchange, transform) would stop the mistakes by\nstopping the flexibility; Brian rejected that (\"seems to me liek it destorys the whol e potin of what we are doing\").\nThis plan keeps the moves free and asks the model to state, once, what must hold in this world, then holds the\nrules to it.\n\n## Incidents this plan must catch\n\nOne row per build check that guesses at meaning, with the incident its docstring names (`scripts/world_builder_service.py`)\nand the saved world that shows it, plus the incident no check caught. This is the proof set L6 and S4 use: a check\nretires only when its incident's saved world is refused by a law or named by the review.\n\n| Incident | Saved world | Shape | Caught today by | After this plan |\n| --- | --- | --- | --- | --- |\n| A purchase that pays nothing (buy-boxed-pencils) | pencil13 `3SogfsdEGx9M`, `tests/fixtures/pencil13-kept.json` | pairing | nothing | pairing law refuses it; the review names it |\n| A process restocks goods an action makes (restock-production-inputs) | c4-run14, `evidence/best-of-all-worlds/final-1a5498f/c4-run14.log`, trace `world-builder-live/world/41373883...` | total | `_conjuring_processes` (`:867`) | total law: the good may change only by its making move |\n| A move uses up goods and makes nothing (pack-pencils) | `4VmgkXIVWn4p`, `evidence/vanishing-goods/pencil3-share.json` | total | `_vanishing_moves` (`:1114`) | total law: pencils may leave only by being used |\n| A raw good with two sources (mine-graphite and graphite-renews) | c4-run20, trace `world-builder-live/world/5c2f3bc4...` | total, only if the designer names one source | `_second_source_processes` (`:1143`), report only | total law when declared; otherwise not a mistake |\n| Inputs nobody makes (clay, paint, erasers, ferrules) | pencil2 `NZD33sh3iX29`, `tests/fixtures/pencil2-live.json` | reachability, not a law | `_unsourced_inputs` (`:840`) | the test run's \"never possible\" report and the review |\n| A move needs a component no entity has (ship-pencil-boxes) | pencil4 `iMrL2U84cLCS`, `tests/fixtures/pencil4-live.json` | structure, not a law | `_missing_components` (`:943`) | stays: a structural fact read from the bundle |\n| Stock with nowhere to go (the supplier's clay and paint) | pencil4 `iMrL2U84cLCS` | reachability, not a law (Q43) | `_dead_end_stock` (`:960`) | a test-run report of stock that only grew, and the review |\n| The customer flagged as a dead end though it uses pencils | pencil12, pencil13 | false alarm | `_dead_end_stock` (patched in #275, #277) | goes with the guess |\n| A seller starts with none of what it sells and nothing gives it any | pencil9 `q2sG4d_J7279`, `tests/fixtures/pencil9-live.json` | reachability, not a law | `_starved_holders` (`:1023`) | the test run's \"never possible\" report and the review |\n| Demand that only grows (orders_waiting) | cafe `eFmPomcnsyQq`, `evidence/vanishing-goods/cafe2-share.json` | reachability, not a law | `_unanswered_demand` (`:1130`) | a test-run report of a field that only grew, and the review |\n| Processes carry goods that actors should carry | c4-run16, trace `world-builder-live/world/cde24f89...` | role, not a law | `_moving_processes` (`:1178`) | the review |\n| Malformed field path | pencil14, `evidence/pencil14-build-failure/README.md` | not a law | installer, already refused | unchanged |\n\nLaws catch the bookkeeping rows (four). The reachability rows are about what can never happen or what piles up: no\nlaw refuses them because every total is unchanged, so they move to reports of what the test run saw, which stay, and\nto the review.\n\n## Current truth (read from code 2026-10-28, main `5d6a48e`)\n\n| Have | Where |\n| --- | --- |\n| A move's candidate state is checked for writes outside its declared scope and refused whole | `Engine.apply`, `src/world_substrate/engine.py:686-720` |\n| Knock-on effects settle in waves inside the same commit | `_settle`, `engine.py:896`; Decision 009 |\n| Effects are rows `{participant, path, op: set|add|subtract, value}` | `EFFECT_OPS`, `src/world_substrate/action_authoring.py:42`; rows read at `:1052`, applied at `:1109` |\n| A process (tick or knock-on) that writes outside its scope raises `ScopeViolation` and the state is restored (`engine.py:1005-1015`). A moment is refused only for `reaction_limit`, `_settle` returning `None`: in `Engine.apply` through `_reject` with the move's rule id (`engine.py:760-781`), in `Engine.advance` through `_refuse_round` with the process's rule id, which ends the advance (`engine.py:858-866`, `:871-895`) | `src/world_substrate/engine.py` |\n| A world-specific conservation check exists for one reference world only, \"not a substrate law\" | `assay_conservation`, `src/world_substrate/assay.py:269` |\n| A read-only derived view pairs two give events into one exchange | `src/world_substrate/exchange.py:68` |\n| About fourteen build checks guess meaning from rule shape or report the test run | `scripts/world_builder_service.py:922-1272`, used at `:1700-1760` |\n| The rules writer revises only the moves it changes | `merge_revision`, `scripts/generate_causal_model.py` (#278) |\n| Nothing declares a law, and nothing reviews the rules against the description | absent |\n\n## The three pieces\n\n### Piece 1. The world declares its laws (copy: Petri-net place invariants; Concordia's stock-and-flow ledger)\n\nThe world designer's output gains `resources` and `laws`, each with a plain sentence for the page. A **resource** is\ndeclared once with every place it is kept, because the same thing can sit under different names on different\nentities (pencil13: the customer pays from `customer.cash` into the shop's `business.cash`; Q47):\n`{resource_id, says, kept_in: [{component, field}, ...]}`. A resource's amount on an entity is the sum of the fields\nit is kept in there. Laws come in two shapes and name resources, never raw fields:\n\n- **total**: `{law_id, says, resource: <resource id>, may_change_by: [move or process ids]}`. The resource's amount\n  summed over every entity may change only in a step made by a listed move or process (the factory's `make-pencils`,\n  the customer's `use-pencil`); every other step must leave it unchanged. This is a P-invariant with named exempt\n  transitions, and it covers both \"nothing from nothing\" and \"nothing vanishes\".\n- **pairing**: `{law_id, says, move: <move id>, gives: {resource, from, to}, pays: {resource, from, to}}`, where\n  `from` and `to` are the move's participant roles. Every step of that move that moves `gives` from one to the other\n  must also move `pays` the other way, both non-zero. \"A purchase moves goods one way and payment the other.\"\n\nLaws do not cover stock with nowhere to go: piling up leaves every total unchanged, so it is a reachability question\n(Q43), left to the test-run report and the review. A law can itself be wrong for the world; the review reads the\nlaws against the description too (Q48).\n\nLaws name the world's own fields and moves. There is no fixed list of goods or moves; the designer writes the\nlaws\nfor whatever the description holds. A world with no `laws` behaves exactly as today. The rules writer sees the laws as\ninput and is told every move must keep them.\n\n### Piece 2. The engine enforces declared laws (extends the existing scope check)\n\n`src/world_substrate/laws.py` holds one pure function, `law_breaches(laws, before, after, step_id)`, called at every\ncommit point. Two cases, because moves and processes are refused differently today:\n\n- **A move** (`Engine.apply`, right after the write-scope check at `engine.py:686-720`): a breach refuses the whole\n  step with status `law_breach` and a failed check that quotes the law's `says` sentence, exactly as a scope\n  violation of a move does today: nothing changes, the refusal event is recorded.\n- **A process** (a tick in `Engine.advance`, or a knock-on wave in `_settle`): today a scope breach here raises\n  `ScopeViolation` and the state is restored with no event (`engine.py:1005-1015`), because a process is\n  engine-trusted. A law breach is different: it is a mistake in model-written rules, so it must be recorded, not a\n  crash. `_apply_process` runs the law check after its scope check and reports a breach (the process id and the law)\n  instead of committing. `_settle` then stops and returns a refusal record, `{status, process_id, law_id, says}`, in\n  place of today's bare `None` (which becomes the same record with status `reaction_limit`). The two callers refuse\n  the whole moment as they refuse `reaction_limit` today:\n  - **in `Engine.apply`** (a move's knock-on effects): the world is restored and `_reject` records the move refused\n    with status `law_breach`; the event carries the move's rule id, and its failed check quotes the law's sentence\n    and names the process that broke it;\n  - **in `Engine.advance`** (a tick process, or the knock-on effects of one): `_refuse_round` gains `status` and\n    `check` arguments; the tick is undone and one event with status `law_breach` carries the process's rule id and\n    the law. As with `reaction_limit` today, the advance returns there: later steps of a multi-step advance do not\n    run, and the next round starts from the restored state. Because the build's scripted test run runs the rules, a breach there is\na build finding sent to the rules writer by name (Q46). This is the existing invariant \"Mechanics propose; one\nenclosing transition validates and commits or refuses\" (AGENTS.md), with the world's own laws added to what the\nenclosing transition validates; it adds no loop, clock or scheduler (Decision 006).\n\n### Piece 3. An independent review reads the rules (copy: LLM+P and Guan et al. 2023 validator feedback)\n\n`scripts/review_rules.py`: one typed `llm_client` call, a different model family from the rules writer, with a fresh\ncontext holding only the description, the laws and the compiled rules. It returns findings, each\n`{rule_id, description_words, problem}`, never a pass mark (Q44). Findings go to the rules writer's existing revision\nstep (`merge_revision`), and the build record lists them. Laws catch bookkeeping; the review catches meaning a law\ncannot state (a move that changes nothing, a rule that contradicts the description).\n\n## Requirements\n\n| Id | Requirement (source) | Fails when | Control | Status |\n| --- | --- | --- | --- | --- |\n| R1 | Moves stay free; no fixed move types (Brian 2026-10-28) | a law shape forces a move into a template | laws constrain totals and pairings only; L1 | Built and run live (S1: #280, `evidence/declared-laws/s1-pencil/`) |\n| R2 | The world's own laws are written by the AI that designs it (Brian 2026-10-28 design 1) | laws are hand-written or pencil-specific | L1 on the live pencil build and S5's other descriptions | Built (S1); S5 planned |\n| R3 | The engine enforces declared laws generically and names the law (design 2) | a breach commits, or a refusal names no law | L2, L3 | Built (S2: `src/world_substrate/laws.py`, `tests/test_laws.py`); L3 live half runs on the deployed build |\n| R4 | A separate review checks rules against description and laws (design 3) | the reviewer is the writer, or returns a verdict | L4 | Built (S3); live check `evidence/declared-laws/s3-pencil/`: L4 held, L5 failed (an unreviewed try was kept; rank and reviewer prompt fixed; the reviewer now sees starting values and preview law refusals reach the build record, #293); second build `evidence/declared-laws/s3-pencil-2/`: no review ran because the last try of each structure failed to compile (fixed: the best unreviewed try is now reviewed), and its replay names the starved shop; third build `evidence/declared-laws/s3-pencil-3/`: both reviews ran and named the missing arrival, the redesign wrote it, and the compiler refused it because the destination field may be empty (fixed: `ref:` links accept `entity_ref_or_null`; the free replay then delivers and sells); fourth build `evidence/declared-laws/s3-pencil-4/`: both reviews ran, the redesign added the moves the first review asked for, and the whole chain ran live to a sale, but the dry run had said eight moves were never offered because discovery stopped at 256 moves before reaching the right buyer (fixed: discovery narrows participants by their own checks first; the free replay offers every move and sells 7); the same build kept a try in which pencils could never be sold over one that ran every move, because an ongoing world counted as alive only with a world process (fixed: alive is what the test run saw, still active at the end; the recorded build replayed with today's code keeps a try that offers every move); the free check over saved worlds (`scripts/check_saved_worlds.py`, 12 of 25 whole) showed the rewrite was told the wrong gap: when a step's only source was refused by a law every time, the note named the source as if it ran, a role no one fits gave an empty note, and a check's comparison was left out (fixed: the note names the law and what it found, the role and the part its closest fit lacks, and the comparison) |\n| R5 | Validation stops growing one check per bug | a heuristic retires without proof, or a new one is added | L6 | Planned (S4) |\n| R6 | Saved worlds replay unchanged (AGENTS.md invariants) | a world with no laws behaves differently | L7 | Planned in every slice |\n| R7 | Every run is readable in full (core rules) | a law refusal or review call is missing from the trace | L8 | Planned in every slice |\n\n## Acceptance checks\n\n| Id | Check | Run and what its trace must show |\n| --- | --- | --- |\n| L1 | The designer declares laws in the world's own terms | `evidence/declared-laws/s1-pencil/`: the build record's `laws` names the pencil world's own resources and moves, each with a `says` sentence; no law was hand-edited (the bundle's laws equal the model reply in the trace) |\n| L2 | A step that breaks a total or a pairing is refused whole, law named | `tests/test_laws.py`: the pencil13 fixture's buy-boxed-pencils with a pairing law gives status `law_breach`, world unchanged, failed check quotes the law; a make move outside `may_change_by` is refused the same way; a move whose knock-on wave breaks a law is refused through `_reject` (status `law_breach`, the move's rule id, a failed check naming the process and quoting the law); a tick process that breaks a law is refused through `_refuse_round` (status `law_breach`, the process's rule id, the law quoted) and the advance stops there; a write-scope breach by a process still raises `ScopeViolation` |\n| L3 | A test-run breach reaches the rules writer by name | `evidence/declared-laws/s2-pencil/`: if the test run refused a step, the next rules call's request quotes the law; if none was refused, the TRACE_READ says so and L2 carries the claim |\n| L4 | The review is independent and returns findings | `evidence/declared-laws/s3-pencil/`: the review call's model differs from the rules writer's, its request holds only description, laws and rules, and its reply is a findings list; run on `tests/fixtures/pencil13-kept.json` it names buy-boxed-pencils |\n| L5 | The canonical example runs live | `evidence/declared-laws/s3-pencil/` (or S5): the kept world's run shows sales moving cash both ways, no law refusals from its own rules, and the build record lists laws and findings |\n| L6 | Each retired heuristic is covered | `evidence/declared-laws/s4-retire/README.md`: per retired check, every incident it caught (table above) is refused by a law or named by the review on its saved world; checks that report the test run stay |\n| L7 | Existing worlds replay unchanged | `scripts/check_project.py` on each slice's merge commit, exit 0, with the open-attempt plan's A8 replay tests named passing |\n| L8 | Every run is fully traced | each `evidence/declared-laws/<run>/` has `run-log.jsonl` and a `TRACE_READ.md` that passes `scripts/check_trace_reads.py`, read by the implementing agent before reporting |\n\n## What Brian judges on the working page\n\nL1-L8 are the agent's checks. What a person opens and sees to decide it works is in\n`docs/planning/declared-laws/acceptance-criteria.json`, each with steps on the World Builder, the expected result\nand a broken case that looks different:\n\n| Id | Criterion | Broken case to tell it apart |\n| --- | --- | --- |\n| A1 | The build record shows the world's own laws in plain words | no laws, or laws naming things the world lacks |\n| A2 | A move that breaks a law is refused and the page names the law | pencil13's buy-boxed-pencils shows as done with no payment |\n| A3 | The review names where rules miss the description, quoting it | empty, \"looks good\", or findings with no quoted words |\n| A4 | The pencil world runs with every sale paying | goods move and cash does not; or the build fails (pencil14) |\n| A5 | Moves stay free, in each world's own terms, with no fixed move kinds | every move labelled transfer, exchange or transform |\n| A6 | Four very different descriptions (pencil, airfield, kitchen, the long Waltzman scenario) each build a world that keeps its own laws | pencil laws reworded, a committed step that breaks a law, or only pencils work |\n| A7 | Mistakes are caught by laws and the review, not a growing list of hand-written checks | a new mistake fixed by adding another guess check |\n\n## Success and disproof\n\n**What L1-L8 are:** the agent's acceptance checks for R1-R7, one row each in the table above. Each is a direct check\nof the claimed property, not a stand-in for it: L1 reads the laws themselves in the build record and compares them\nwith the designer's reply; L2 and L3 read the refusal events and the rules writer's next request; L4 reads the review\ncall's model, request and findings; L5 reads the kept world's own run, sale by sale; L6 replays each incident's saved\nworld and reads whether a law or a finding names it; L7 replays law-free saved worlds; L8 reads each run's trace\nfiles. A test count, a merged pull request or a status line alone satisfies none of them.\n\n**Success:** L1-L8 pass, each judged from the full trace of the run it names. **Disproof:** any of these in a named\nrun's trace: a law that names a field or move the world does not have; a committed step whose before and after break a\ndeclared law; a refusal without the law's sentence; a review call sharing the rules writer's model or conversation; a\nretired check with an incident neither a law nor the review catches; a law-free saved world whose replay differs.\nTrace review: the implementing agent reads every law refusal, every review finding and a sample of at least five\nordinary steps per run, and writes `TRACE_READ.md`; each of L1-L8 is expected `pass`. Where each trace lives:\nL1, L3, L4, L5 and L6 in `evidence/declared-laws/<run>/run-log.jsonl` (with `TRACE_READ.md` beside it) plus the\n`llm_client` trace ids it records; L2 and L7 in the `scripts/check_project.py` output for the slice's merge commit,\nsaved as `evidence/declared-laws/<slice>/check_project.txt`, with the named tests' assertions read; L8 is the reading\nof those files itself. An acceptance criterion that names only an outcome (\"tests pass\", \"pull request merged\", \"the\nstatus reads ok\") fails this rule; every row names what its trace must show. Exemption: a criterion with no run (a\npure document edit, such as this adoption commit) says so and why in its slice's `TRACE_READ.md`; no criterion\nL1-L8 is exempt.\n\n## When a run fails or surprises us\n\nThis procedure is separate from the anticipated failure modes in Requirements and Uncertainties: those are designed\nfor in advance, while this is what to do when a real run fails or surprises us in a way nobody planned. Keep the run and its trace ids; read the full inputs, prompts, each model and tool call's arguments and results,\nintermediate stages (laws, rules, review findings, test-run refusals) and the output (build record, page) before\nchoosing a fix; cite where it diverged; classify it evidence absent (never retrieved), evidence returned but unused or contradicted, invalid\nexpectation, or unresolved. An unresolved cause permits investigation, not a repair. A repair is verified by a new traced run whose\n`TRACE_READ.md` links the original; the original stays. A new symptom is first asked \"which law or review finding\nshould have caught this?\" and fixed there; a new heuristic check is the last resort and is recorded as a question.\nNever rerun until a behavior appears and report only that run. Review completeness never changes the run verdict.\n\n## Slices, in order\n\n| Slice | What lands | State | Checks |\n| --- | --- | --- | --- |\n| S1 | `resources` and `laws` in the world design contract (`scripts/generate_world_bundle.py`) and its validator; laws passed to the rules writer; build record and page list them | built (#280) | L1, L7, L8; one live pencil build |\n| S2 | `law_breaches` in `src/world_substrate/laws.py`, called in `Engine.apply` after the scope check and in `_apply_process` (ticks and knock-on waves); `_settle` returns a refusal record; `_reject` and `_refuse_round` record `law_breach`; status `law_breach`; test-run breaches become build findings | built (#284) | L2, L3, L7; free replays of saved worlds first |\n| S3 | `scripts/review_rules.py` and its findings into the rules writer's revision step | built (#291-#304; Q44 resolved); on the people-world path a build past its 80 s rewrite limit keeps a world its review flagged (Q55, open) | L4, L5, L8 |\n| S4 | retire the heuristics Q45 names, one by one, each with its incident proof | conditional (Q45; none retired yet) | L6, L7 |\n| S5 | live builds of four varied descriptions in parallel (pencil, airfield, a kitchen, the Waltzman scenario) | follows the plain-version comparison (Q60) (S1-S3 built; Q50 settled 2026-11-09; one Waltzman rebuild ran 2026-11-04 on his yes for that build, `evidence/declared-laws/s4-waltzman-3/`) | L1, L5, L8 per run; read for Q43 counterexamples |\n\nEach slice is its own pull request and leaves a working World Builder.\n\n## Decisions\n\n- **D1 (Brian, 2026-10-28, \"yes lets make it companhy plannign complaint\"):** the three-part design (laws declared\n  by the designer, enforced by the engine, an independent review) replaces fixed move types.\n- **D2 (made, technical):** law checking sits beside the write-scope check inside the existing commit, not in a new\n  engine stage (Q46; Decision 006).\n- **D3 (made, technical):** two law shapes, total and pairing (Q43). Anything else stays an ordinary rule the review reads.\n- **D4 (made, technical):** borrow the semantics of Concordia's `stock_flow_ledger.py` (holders, an outside boundary,\n  `is_conserved`) but do not adopt it: its fixed operation set is the fixed-move-types design Brian rejected.\n\n## System model\n\n- Model: [docs/model/ODD.md](../model/ODD.md); relied on: RULE-ATOMIC-COMMIT-OR-REFUSAL (a law breach changes\n  nothing), RULE-DERIVED-AUTHORITY. Adds: `world-law` (the bundle's `laws`), `law-check` (status `law_breach`),\n  `rules-review` (the build record's `review_findings`). Each is a node in\n  [docs/model/domain.graph.json](../model/domain.graph.json) marked \"in documents only\" until its slice builds it.\n- Scope: this repository's own model, linked from `docs/wiki/README.md`; the scientific-hypergraph mapping is unchanged.\n- Each slice updates ODD.md, `world_substrate_model.toml` and `tests/test_system_model.py` in the same pull request;\n  the drift test must fail on a renamed field before it passes. Views: `owner_run_log` and `home` must show the laws,\n  each law refusal with its sentence, and the review findings; each slice adds its row to `docs/model/VIEW_COVERAGE.md`.\n- The trace must show, per element: the bundle's `laws` as the designer's reply; each `law_breach` event with the law\n  id and before/after; each review call's trace id, model and findings.\n\n## Trace visibility\n\n- Each run's `run-log.jsonl` records the inputs (description, bundle hash), every build step with its time, each model\n  call (designer, rules writer, reviewer, residents) with request messages, typed result and `llm_client` trace id,\n  every engine event with before/after and failed checks (including `law_breach`), and the output (build record, page\n  JSON). Kept for ordinary runs, not only failures; this adoption commit alone is document-only and runs nothing.\n- The model's reasoning, where the model exposes it: each call's reasoning text (OpenRouter `reasoning` field, and\n  the residents' `reasoning` field in `scripts/run_authored_world.py:454`) is kept in the run log with the call, not\n  dropped; a model that exposes none is recorded as such.\n- How to open one: `jq . evidence/declared-laws/<run>/run-log.jsonl`; model calls in the VPS `llm_calls` table by\n  trace id. Who reads and when: the implementing agent reads every run's trace before reporting its slice: every law\n  refusal and review finding in full, and at least five ordinary steps per run across rounds and actors.\n\n## Capability reuse\n\nNo catalogue entry fits, because `reuse_candidates.yml` and `capability_registry.yml` hold approvals, notifications,\nscheduling, document-to-text and search wrappers, none of which check rules or conservation. Model calls go through\nthe shared `llm_client` (listed in `~/code2/workspace/docs/capabilities.md`). No new cross-project capability is added;\nthe law check's and the review's first and only consumer is the World Builder build.\n\n## Prior art and ownership\n\nPrior-art review 2026-10-28 (summarised in Decisions D3-D4): Petri-net place invariants (laws as weighted sums with\nexempt transitions); Concordia contrib `stock_flow_ledger.py` (Apache-2.0, semantics borrowed); LLM+P and Guan et al.\n2023, AutoToS, WorldCoder (a model writes a world model, a validator feeds corrections back); Huang et al. 2023\n(arXiv 2310.01798), SCORE (2404.17140) and Wataoka et al. 2024 (2410.21819): self-review without outside feedback is\nweak and self-preferring, hence D2 of Piece 3. Overall disposition: **compose**, with a small law language of our own.\nPer candidate:\n\n| Candidate | Disposition | What we take |\n| --- | --- | --- |\n| Petri-net place invariants | compose (idea only) | a law is a weighted sum that only named moves may change |\n| Concordia contrib `stock_flow_ledger.py` | bounded exception (semantics borrowed, code not adopted) | holders, an outside boundary, `is_conserved`; its fixed operation set is the fixed-move-types design Brian rejected (D4) |\n| LLM+P, Guan et al. 2023, AutoToS, WorldCoder | compose (method) | a model writes the world model and an outside validator feeds named corrections back to it (Pieces 2 and 3) |\n| Huang et al. 2023, SCORE, Wataoka et al. 2024 | reuse (finding) | the reviewer must be a different model and context from the writer (Piece 3) |\nOwner: World Substrate's rules layer. Parallel-implementation check: one commit path; `grep -n \"def apply\"\nsrc/world_substrate/engine.py` stays one hit and `law_breaches` has one caller per commit site.\n\n## LLM call boundary\n\nBuild call graph: world designer (existing; output gains `laws`) -> rules writer (existing; laws added to its input,\ntest-run law refusals and review findings added to its revision input) -> reviewer (new, one call per build attempt,\nafter compile, before the test run's verdict) -> no further model call. Laws and review findings have no authority to\nchange state: laws only refuse, and findings only reach the rules writer. Rules writer and designer stay on the World\nBuilder's model; the reviewer uses a different family through `llm_client` (Q44). Structured result boundaries:\nthe **world designer** returns the world bundle JSON defined by `_contract()` (`scripts/generate_world_bundle.py:93`),\nparsed with `safe_json_loads` and accepted only by `validate_bundle` (`scripts/scaffold_world.py:45`); S1 adds\n`resources` and `laws` to both, and a reply that fails validation goes back for repair, up to `MAX_REPAIRS`. The\n**rules writer** returns the causal model JSON whose schema `causal_model_schema(bundle)`\n(`scripts/generate_causal_model.py:330`) builds from the bundle, then `tidy_proposal` and the installer check it; a\nrevision is merged by `merge_revision`. The **reviewer** (new, S3) returns `{\"findings\": [{\"rule_id\": str,\n\"description_words\": str, \"problem\": str}]}` through `llm_client`'s typed structured call, with `rule_id` checked\nagainst the compiled rules' ids; any other shape is recorded as a failed review. Failure: a failed or malformed\nreview call is recorded with its error and the build continues without findings, visibly. Tracing: each build's calls\nshare its trace id, as today.\n\nProvider: OpenRouter through `llm_client`; designer and rules writer on the World Builder's `DEFAULT_MODEL`\n(`scripts/run_authored_world.py:38`), the reviewer on a model of another family chosen in S3 (Q44). Spend authority:\nBrian's owner allowance, given for this plan by his 2026-10-28 \"yes\" and his added OpenRouter credit; the visitor\nallowance stays $3/day. Promotion condition: laws and review findings count as working only after an authentic live\nbuild on the deployed service (owner allowance, through the real page) whose `run-log.jsonl` and `TRACE_READ.md` show\nthem; fixture and replay results support a slice but are never reported as live.\n\n## Evaluation design\n\nOne measurement (Q44), for one decision. **Decision it changes:** S4, whether each guessing check retires. If the review\nand the laws together catch every incident a check caught, that check goes; if not, it stays and the miss becomes an\nopen question. **Why argument cannot settle it:** whether a different model, given the description and the rules,\nnotices a payment missing from a purchase is a fact about that model on these worlds; the prior art says self-review\nis weak but says nothing about this reviewer on these rules. **Parity:** every candidate reviewer gets the same input\n(description, laws, compiled rules of each saved incident world, no other context) and the same findings schema, and\nis scored only on whether it names the incident's rule; the heuristics it is compared with run on the same saved\nworlds. **Cost:** about seven saved worlds, one review call each, a few cents and minutes on free replays; a wrong\nretirement would let the next pencil-style bug run unnoticed, which has already cost several paid builds and days.\nWhy measuring is cheaper than choosing now and correcting later: retiring a check is reversible in code, but a wrong\nretirement is found only when a live build ships a broken world to a visitor, after paid builds and a trace read\n(pencil2-pencil14 took about $2 and two days to surface their bugs); the replay costs cents and minutes and runs before\nany retirement. **Under each result:** a reviewer that names an incident's rule lets that check retire in S4; one that\nmisses it keeps the check and opens a question; if no candidate names more than half, S3's review stays advisory and\nS4 retires only checks a law covers.\n\n## Irreversible actions and spend\n\nWho authorizes spend: Brian alone. He authorized this plan's owner-allowance builds on 2026-10-28 (\"yes lets make it\ncompanhy plannign complaint\", with the OpenRouter credit he added: \"there is more money\"); any spend past the caps\nbelow, or any new spend route, needs his yes first. Nothing irreversible: merges are pull requests and deploys redeploy from the previous commit. No deletion of saved\nworlds or run records, no outreach, no change to other repositories. Spend: owner allowance only, after free replays;\nabout $0.15 per live pencil build, at most $1.00 per slice and $3.00 across the plan before reporting; S5's four builds\nare about $0.60. The visitor allowance stays $3/day.\n\n## Uncertainties\n\n- Q50 (Brian, settled 2026-11-09): believability is the off-the-shelf people agents' job, with no metric, tuned\n  only once everything else runs well. S5's paid builds now wait only on the plain-version comparison (Q60).\n- Q43 (agent, resolved by reading): two law shapes cover every logged incident; S5 is read for a counterexample.\n- Q44 (agent, resolved): which model reviews; settled by the review run on the saved incident worlds\n  (`evidence/declared-laws/s3-review-choice/README.md`).\n- Q45 (agent, open): which heuristic checks retire; settled per check in S4.\n- Q46 (agent, resolved by argument): run-time refusal first; a static proof is optional.\n- Q48 (agent, open in part) and Q49 (agent, open): a law too permissive, and a law the designer leaves out.\n- Q55 (agent, open): the 2026-11-04 Waltzman rebuild kept rules its review flagged (no postponement possible); the\n  shared run is read only with that stated.\n- Wrong or missing laws: a designer that declares too few laws catches less, never more wrongly; a designer that\n  declares a wrong law makes the test run refuse a legitimate move, which shows as a law refusal in the build record\n  and goes to the rules writer and the review. L1 and S5's reads check both.\n\n## Activation facts\n\nRecorded in [activation-facts.json](declared_laws/activation-facts.json): shared mechanism yes (the engine and\nthe build serve every world), one empirical comparison (Q44, see Evaluation design), LLM central yes, spend yes (owner\nallowance), deploys yes (see Deployment). Route: [path-decision.json](declared_laws/path-decision.json), reset: this re-plans the World Builder's\nvalidation after the one-check-per-bug approach hit an implementation obstacle (pencil2-pencil14), with no single\nidentified fix. One writer still runs the slices in order. The plan copies\nestablished methods but claims conformance to none, so `claims_external_standard` is false.\n\n## Deployment\n\nEach slice deploys once, after its pull request merges (squash) on `main`. Targets and commands:\n\n| Target | Deploy command | Live check that the new version serves | Rollback |\n| --- | --- | --- | --- |\n| World Builder API on the personal VPS (container `world-builder`, `/srv/apps/world-builder`) and the pages Worker `world-builder-pages` (home, play, build) | `scripts/deploy_world_builder.sh <merged commit>`: runs the local gate unless that tree already passed, then personal-vps `apps/world-builder/deploy.sh` for the API and `deploy/cloudflare/world-builder/build.sh` plus Wrangler for the pages | `curl https://brianmills.dev/world-builder/api/health` reports `build_commit` equal to the merged commit (the script waits for it and exits 3 otherwise); the home page served at <https://brianmills.dev/world-builder/> contains the slice's new text (S1: \"Laws this world keeps\") | API: `ssh personal-vps 'docker tag world-builder:<previous short sha> world-builder:current && cd /srv/apps/world-builder && docker-compose up -d'` (the last 3 image tags are kept); pages: rerun `scripts/deploy_world_builder.sh <previous commit>` |\n\nNo deploy runs while a live run is in progress on the service.\n\n## Durable documents\n\nDurable documents: system_model#ENT-RUN-RECORD, system_model#PROC-TRANSITION, system_model#PROC-PROCESS-TICK, plans\n\nThese roles are declared in the repository's `durable_documents` block (`.agentic/repo.yaml:3-11`): `system_model`\nis `{prose: docs/model/ODD.md, trace: docs/model/trace.yaml}`, where ENT-RUN-RECORD, PROC-TRANSITION and\nPROC-PROCESS-TICK are ids (`docs/model/trace.yaml:22, 28, 31`), and `plans` is `docs/plans/`.\n\nS1 changes ENT-RUN-RECORD (the build record gains `laws`); S2 changes PROC-TRANSITION and PROC-PROCESS-TICK (law\nchecks in each commit and wave); S3 changes ENT-RUN-RECORD (`review_findings`). At completion of each slice,\n`python3 ~/code2/company-planning/plugins/company-planning/scripts/durable_docs_check.py --plan\ndocs/plans/declared_laws.md --range <adoption revision>..HEAD` must exit 0.\n\n## Authority and non-goals\n\n**Authority:** Brian's \"yes lets make it companhy plannign complaint\" on 2026-10-28 to this design; one agent writes;\nworld-substrate and its own deploy only.\n\n**Non-goals:** fixed move types; laws of shapes other than totals and pairings; a static proof of laws; changes to\nthe open-attempt plan's S3 skill rolls; any change to Cybernetic Influence v3 or Concordia.\n",
 "built_from": "c99cbc7"
};
