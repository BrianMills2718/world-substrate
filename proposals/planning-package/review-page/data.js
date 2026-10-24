window.PAGE_DATA = {
 "manifest": {
  "schema_version": "1.0",
  "record_type": "planning_package",
  "repository": "BrianMills2718/world-substrate",
  "subject_revision": "6a8e37e26afc1aaab177d544f808ae560650d8b5",
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
     }
    ]
   },
   "open_questions": {
    "status": "present",
    "path": "docs/planning/open-questions.json"
   },
   "system_model": {
    "status": "present",
    "path": "docs/model/ODD.md"
   },
   "domain_model": {
    "status": "present",
    "path": "docs/model/domain.graph.json",
    "glossary": "docs/model/DOMAIN.md"
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
     }
    ]
   },
   "plan": {
    "status": "present",
    "path": "docs/plans/run-loop-contention.goal.md"
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
   "question": "When several people want the one shared thing in a round, each loser is told 'your choice was no longer allowed after earlier moves this round; choose again' and is shown the round's earlier moves (who, which rule), so it can see who moved. It is not told which of its moves was refused or which earlier move blocked it, and the record does not link the refusal to that move. Should the retry prompt and the row name the refused move and the blocking event?",
   "blocks": "whether a reader of a run (or the readout) can say why a person's move was refused, in any world",
   "resolves_with": "An argument settles it: the run loop already knows which submitted event changed the revision before the loser's pick, so naming it costs nothing and belongs in the run loop, not any world. Build it and check on free replays of saved worlds (c1r24 Waltzman, truck) that each refused row names its blocking event id. Starting point: c1r24 call 18016 shows the round's moves but not the link.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/run_authored_world.py:544",
    "scripts/run_authored_world.py:547",
    "scripts/run_authored_world.py:572",
    "evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md",
    "evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md:125"
   ],
   "touches": [
    "contention",
    "run-loop",
    "resident"
   ]
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
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#225",
    "evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md:116"
   ],
   "touches": [
    "run-loop",
    "share"
   ]
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
   "status": "open",
   "sources": [
    "BrianMills2718/world-substrate#218"
   ],
   "touches": [
    "gen-rules",
    "test-run"
   ]
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
   "question": "After a lost race the retry's own words are stored as said_on_retry, but the 'What happened' readout quotes only said, the words behind the first choice, next to the move the retry made. Should the readout quote the retry's words?",
   "blocks": "whether the readout's quoted words match the move that ran",
   "resolves_with": "Reading the code settles it: the row keeps both (run_authored_world.py:584, :599-600) and the scene replay already prefers said_on_retry (render_scene_replay.py:398), but run_readout.py:93 reads said only. Make the readout prefer said_on_retry the same way and check it on a free replay.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "scripts/run_authored_world.py:584",
    "scripts/run_authored_world.py:599",
    "scripts/run_readout.py:93",
    "scripts/render_scene_replay.py:398"
   ],
   "touches": [
    "contention",
    "readout"
   ]
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
    "scripts/run_authored_world.py:732"
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
   "status": "open",
   "recommendation": "Do the run-loop fixes first (Q6 no double run, Q10 readout words, Q2 refusal linked to its cause), then the executable-law fingerprint.",
   "default": "The next goal is the run-loop fixes (docs/plans/run-loop-contention.goal.md).",
   "sources": [
    "roadmap/README.md:359",
    "roadmap/README.md:427"
   ],
   "touches": [
    "contention",
    "run-loop",
    "law-fingerprint"
   ]
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
   "short": "Repository format not adopted",
   "question": "The ~/code2 repository format check fails: no docs/index.md, docs/architecture/arc42.md, C4 files, openspec specs, lefthook.yml or Makefile. Should world-substrate adopt the format?",
   "blocks": "whether the repo-format check passes",
   "resolves_with": "Prior art settles the shape (phenomenal-meaning adopted it); the work is mechanical: add the files, mostly as indexes over the existing architecture, ODD and trace documents.",
   "owner": "agent",
   "status": "open",
   "sources": [
    "docs/planning/checks.txt"
   ],
   "touches": []
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
    "label": "Waltzman reference code only",
    "color": "#7a8491",
    "explain": "Hand-written code for the Waltzman reference world; no generated world uses it."
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
    "explain": "The one canonical world during a run: entities with typed components, a tick and a revision. Code: src/world_substrate/engine.py."
   },
   {
    "id": "engine",
    "label": "Engine",
    "kind": "Substrate",
    "explain": "Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. Code: src/world_substrate/engine.py:558."
   },
   {
    "id": "event",
    "label": "Event",
    "kind": "Substrate",
    "explain": "The record of one attempt or process step: status, checks, changes, an id like r14-e00012. Code: src/world_substrate/engine.py:505."
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
    "explain": "A rule the world runs by itself each tick when its checks hold. Code: src/world_substrate/engine.py:762."
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
    "explain": "What chooses a person's move (scripted, an AI model or a resident): it can only pick an offered move; installed mechanics, not its words, decide what happens. Code: src/world_substrate/policy.py:50."
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
    "explain": "The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced. Code: src/world_substrate/engine.py:93."
   },
   {
    "id": "causal-trace",
    "label": "Causal trace",
    "kind": "Substrate",
    "explain": "The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run. Code: scripts/world_builder_service.py:1822."
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
    "explain": "Each round: everyone decides, picks are submitted in a rotating order, then processes run. Code: scripts/run_authored_world.py:335."
   },
   {
    "id": "contention",
    "label": "Lost race",
    "kind": "Substrate",
    "explain": "When an earlier pick changed the state, a later pick is resubmitted if still offered, else the person is asked once to choose again, shown the round's earlier moves (who, which rule) but not which one blocked it; if it then picks nothing it gets nothing_left. Code: scripts/run_authored_world.py:544."
   },
   {
    "id": "resident",
    "label": "Resident",
    "kind": "Substrate",
    "explain": "One Concordia AI agent per person: sees its brief, memory and what it can see, answers belief, move, expected effect and work. Code: scripts/concordia_residents.py:29."
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
    "explain": "Description to spec, actions, rules, assembly, scripted test run and score. Code: scripts/world_builder_service.py:1538."
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
    "explain": "The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. Code: scripts/world_builder_service.py:1607."
   },
   {
    "id": "run-log",
    "label": "Run log",
    "kind": "Substrate",
    "explain": "One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. Code: scripts/world_builder_service.py:478."
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
    "explain": "A world built from a description about people: people, information, moments and the fixed people rules. Code: scripts/people_world.py:225."
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
    "explain": "A person the spec names, with goals and beliefs, and the brief only their own resident reads. Code: scripts/people_world.py:355."
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
    "explain": "Roadmap hardening item: fingerprint the exact executable law and compiler version. Code: —."
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
    "id": "Q2",
    "label": "Q2: A refusal is not linked to its cause",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether a reader of a run (or the readout) can say why a person's move was refused, in any world."
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
    "id": "Q6",
    "label": "Q6: One round run twice",
    "kind": "AgentQuestion",
    "explain": "Blocks: wasted spend and shares that keep only one of two runs."
   },
   {
    "id": "Q8",
    "label": "Q8: Rules check a resource but never claim it",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether a finished build is faithful to what was described."
   },
   {
    "id": "Q9",
    "label": "Q9: Test run too short for some tasks",
    "kind": "AgentQuestion",
    "explain": "Blocks: builds wrongly scored as failing and the rewrite spend they cause."
   },
   {
    "id": "Q10",
    "label": "Q10: Retry keeps the first words",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether the readout's quoted words match the move that ran."
   },
   {
    "id": "Q12",
    "label": "Q12: When a people-world run ends",
    "kind": "BrianQuestion",
    "explain": "Blocks: how long visitors watch a run, and its cost."
   },
   {
    "id": "Q13",
    "label": "Q13: Which hardening first",
    "kind": "BrianQuestion",
    "explain": "Blocks: the next goal."
   },
   {
    "id": "Q14",
    "label": "Q14: Agent-harness build not live",
    "kind": "AgentQuestion",
    "explain": "Blocks: whether build repairs come from a harness or from the rules retry (Q1)."
   },
   {
    "id": "Q17",
    "label": "Q17: Offline pipeline views",
    "kind": "BrianQuestion",
    "explain": "Blocks: whether work goes into the offline pipeline at all."
   },
   {
    "id": "agenda",
    "label": "Agenda count",
    "kind": "Concept",
    "explain": "group_decision.agenda_items: a bare number of matters put before the decision; an item has no content."
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
    "id": "contention",
    "label": "Lost race",
    "kind": "Concept",
    "explain": "When an earlier pick changed the state, a later pick is resubmitted if still offered, else the person is asked once to choose again, shown the round's earlier moves (who, which rule) but not which one blocked it; if it then picks nothing it gets nothing_left."
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
    "id": "law-fingerprint",
    "label": "Executable-law fingerprint",
    "kind": "Concept",
    "dashed": true,
    "explain": "Roadmap hardening item: fingerprint the exact executable law and compiler version."
   },
   {
    "id": "notice",
    "label": "Finished-task notice",
    "kind": "Concept",
    "explain": "What the other people a finished task names are told, in the starter's own words about the work."
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
    "explain": "One Concordia AI agent per person: sees its brief, memory and what it can see, answers belief, move, expected effect and work."
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
    "id": "share",
    "label": "Share link and replay",
    "kind": "Concept",
    "explain": "A saved run rebuilt from the run log that a visitor replays with no AI calls."
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
    "id": "Q2-contention",
    "source": "Q2",
    "target": "contention",
    "label": "bears on"
   },
   {
    "id": "Q2-run-loop",
    "source": "Q2",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q2-resident",
    "source": "Q2",
    "target": "resident",
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
    "id": "Q6-run-loop",
    "source": "Q6",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q6-share",
    "source": "Q6",
    "target": "share",
    "label": "bears on"
   },
   {
    "id": "Q8-gen-rules",
    "source": "Q8",
    "target": "gen-rules",
    "label": "bears on"
   },
   {
    "id": "Q8-test-run",
    "source": "Q8",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q9-test-run",
    "source": "Q9",
    "target": "test-run",
    "label": "bears on"
   },
   {
    "id": "Q10-contention",
    "source": "Q10",
    "target": "contention",
    "label": "bears on"
   },
   {
    "id": "Q10-readout",
    "source": "Q10",
    "target": "readout",
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
    "id": "Q13-contention",
    "source": "Q13",
    "target": "contention",
    "label": "bears on"
   },
   {
    "id": "Q13-run-loop",
    "source": "Q13",
    "target": "run-loop",
    "label": "bears on"
   },
   {
    "id": "Q13-law-fingerprint",
    "source": "Q13",
    "target": "law-fingerprint",
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
 "next_plan": "# Goal: no round runs or bills twice, and a run's record says why each move was refused\n\nPlanning package: docs/planning/planning-package.json\n\nFollows [waltzman-tasks-slice2.goal.md](waltzman-tasks-slice2.goal.md), which is done. Chosen from the planning\npackage's open questions: Q6 (one round run twice), Q10 (the readout quotes the wrong words after a retry) and Q2 (a\nrefusal is not linked to its cause). All three are in the substrate's run loop or readout, so they affect every world\non every run. Q13 asks Brian whether this comes before the roadmap's hardening queue; the recommendation and default\nare this goal. Not adopted until Brian answers Q13 or starts it.\nProfile: continuous-light.\n\n## Roadmap\n\n| # | Goal | Depends on | Why here | Status |\n| --- | --- | --- | --- | --- |\n| 1 | best-of-all-worlds.goal.md | – | the live World Builder | done |\n| 2 | waltzman-belief-and-traces.goal.md | 1 | enforced trace reads; #128 design and first slice | done |\n| 3 | waltzman-tasks-slice2.goal.md | 2 | tasks that can fail part-way | done |\n| 4 | this goal | 3 | double-billed rounds and records that misattribute words or refusals, in any world | open |\n\n## The problem, in one example\n\nThe page once sent one round's `/run` twice and the server ran and billed both (#225). Separately, in round 14 of\nthe Waltzman run the community group settles the one agenda item and seven others had wanted it too (c1r24\nTRACE_READ.md:307). Each loser is told \"your choice was no longer allowed after earlier moves this round; choose again\"\n(`scripts/run_authored_world.py:544-545`) and shown the round's moves so far, so it can see that the community group\nsettled (for example country-one, c1r24 call 18016). But the prompt does not name which of its moves was refused, and the row does not record\nwhich event blocked it, so a reader of the run cannot say why without re-deriving the order. Then the \"What happened\"\nreadout quotes each retried person's first words next to the move its retry made (`scripts/run_readout.py:93`).\n\n## Canonical example\n\nA second `/run` for the same round is refused without spending and the page shows the first result. On a free replay\nof a saved world (the c1r24 Waltzman world, and the truck world), when several people pick the same one-of-a-kind move\nin a round, each refused row names its refused move and the blocking event id, the retry prompt names both, and the\nreadout quotes the retry's own words.\n\n## Done when\n\n- **F1. No round runs twice.** The service refuses a second `/run` for the same session, round and base revision with\n  no AI spend, and the page shows the first result. Test sends the same round twice.\n- **F2. The readout quotes the words behind the move that ran.** For a retried move the readout quotes\n  `said_on_retry`, as the scene replay already does (Q10). Tested on free replays of two saved worlds with no AI calls\n  (stand-in residents).\n- **F3. A refusal names its cause.** A row whose pick was refused after an earlier move records the refused move and\n  the blocking event id, and the retry prompt names both (Q2). Tested as F2.\n- **F4. One live owner-allowance canonical run** at the deployed commit, read in full (`run-log.jsonl` and a\n  `TRACE_READ.md` that `scripts/check_trace_reads.py` passes), reporting every lost race and what each loser did next.\n\nJudge each criterion from the full trace of the run it names (llm_client trace ids, Engine event ids, run log), not\nfrom a reported status.\n\n## Boundaries\n\nworld-substrate and its own deploy only. Merge after `scripts/check_project.py` exits 0; deploy and confirm the live\ncommit through the health endpoint; publish-checker before anything new goes public. Owner allowance only; visitor\nallowance stays $3/day. Free replays before the one paid run. No Waltzman-specific code paths. Never restart WSL.\n\n## Forbidden substitutes\n\nHand-edited runs; scripted moves presented as AI; a fix that only changes the Waltzman agenda; rerunning until a\nbehaviour appears.\n\n## Stop rules\n\nStop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence; report it and what\nwould unblock it. Revalidate after three increments or about four hours.\n\n## Do not gate on\n\nBrian's review; agenda content (Q3); the notice wording (Q4).\n\n## Progress\n\n- 2026-10-24: goal written from the planning package (Q2, Q6, Q10).\n- 2026-10-24: Q2 corrected twice after cold reviews: losers are already asked to choose again and shown the round's\n  moves (call 18016); what is missing is the link from a refusal to the move that caused it. Criteria reordered.\n",
 "built_from": "6a8e37e"
};
