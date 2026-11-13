# Source for docs/planning/open-questions.json and docs/model/open-questions.graph.json.
# Edit here, then run python3 tools/planning/build.py.
Q = [
 {
  "id": "Q1",
  "short": "Rules retry never runs here",
  "question": "The build's rules retry is skipped once 80 s have passed, and in the canonical Waltzman build the test run starts at 85-111 s. Should the cut-off, or the order of the build steps, change so the retry can repair a world?",
  "blocks": "whether a world whose rules fail the part-way or liveness checks can be repaired on the live path, or only scored lower",
  "resolves_with": "Audit 2026-11-12: Known implementation gap. Use remaining-time budgeting on the accepted harness path (Q14); keep consequential findings visible when repair stops. Close on saved failing inputs with an explicit disposition, not historical timing alone.",
  "classification": "implementation_gap",
  "dependencies": ["Q14"],
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
  "dependencies": ["open-attempt S3"],
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
  "resolves_with": "Audit 2026-11-12: Quoted spans enable inspection, not semantic correctness. Preserve original attempts and unmatched results, flag non-wait attempts interpreted as wait, and inspect the negative fly-versus-walk case and full trace before closure. Production5 (2026-11-13) adds a concrete compound-intent case: Mara asks to withhold assent by recording concern; the single-action interpretation selects withdrawal, which is refused because assent is already false. No stance is committed. See evidence/i0-i1/deployed-integration-5/TRACE_READ.md; Brian approved the bounded follow-up on 2026-11-13: require whole-attempt coverage in the existing call; bind concrete means, keep stance separate from assent, and reject incomplete/multiple operations without partial execution, judge invocation or request delivery. See docs/plans/open_attempt.md#whole-attempt-coverage-follow-up-q36. This correction does not close general semantic accuracy or prescribe residents' responses.",
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
  "dependencies": ["complete actor-information contract"],
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
  "dependencies": ["declared-laws S4"],
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
  "dependencies": ["Q45"],
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
  "dependencies": ["Q45"],
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
  "dependencies": ["complete actor-information contract"],
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
  "dependencies": ["complete actor-information contract"],
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
  "dependencies": ["complete actor-information contract", "single-concern influence contract"],
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
  "dependencies": ["Q34"],
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
  "dependencies": ["Q83", "estimate-rules E1"],
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
  "dependencies": ["estimate-rules E1", "deployment timeout policy"],
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
  "dependencies": ["AI-judge J5"],
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
  "dependencies": ["Q83"],
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
  "dependencies": ["scenario pricing contract", "Q96"],
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
  "dependencies": ["Q92"],
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
  "dependencies": ["Q96"],
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
  "dependencies": ["AI-judge Q96 offer lifecycle"],
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
]
