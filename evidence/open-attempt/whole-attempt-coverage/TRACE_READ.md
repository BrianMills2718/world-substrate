# Whole-attempt coverage — bounded replay evidence

Revision: `ecef00db38d3d32cf6fd4c08b5ffe5741d4aec5d`. Native trace: `world-substrate-interpreter-replay-e609d37b`. This is retained-input interpreter replay followed by model-free installed-rule replay, not another generated world or fresh resident-policy run. Original production5 is preserved unchanged.

Read all three complete native prompts/responses, shared schema, structured attempts and call lifecycle; independent planning reviewer also read all three. Three calls, zero tools, zero retries/provider failures; 7,658 tokens, measured provider cost **$0.00097666**; measured wrapper duration18.76788408 seconds, exit0. Reasoning-token counts are retained; reasoning prose is not exposed by this route. Credential identifier is redacted by the existing export helper; exact model messages/outputs are unchanged.

## Interpreter calls

- 9687240 replays production5 call23462 with exactly the same actor, utterance, signatures and entities through prompt1.4. Mara's “I withhold my assent to activating the prototype pump by recording a concerned position for myself, Mara.” now binds `state-concerned`, position-mara, with complete coverage and the exact concrete recording span. The old result was withdraw-assent. No new actor choice is inferred.
- 9687241 replays23455 unchanged: Ari's technical-authority repair still binds `repair-condition`, the same authority and condition, complete coverage.
- 9687242 is an explicitly varied attempt using Ari's same signatures/entities: repair the condition **and** send Mara a report. The raw response identifies both operations and says requires_decomposition, but incorrectly gives empty unrepresented_spans. The strict validator therefore returns invalid_coverage. Preserve this defect: detection is not a valid coverage assessment. No retry was run to obtain a preferred response.

## Round 2

Model-free branches restore the actual production5 round1 snapshot. Recorded residents supply the tested utterance, others wait; the recorded native reading is submitted through the actual runner with rule creation enabled. These are checkable engine replays, not observed autonomous behavior.

Mara branch: `r2-e00001` accepts state-concerned and changes only her stance to concerned. Assent remains false; it does not withdraw consent or activate anything. `engine-mara.json` retains the whole trace; exact replay matches,2steps. Compound branch: `r2-e00001` records unsupported_action for invalid_coverage, with no changes, no judge call, no request delivery, and constant actor clarification; exact replay matches,2steps. `engine-compound.json` retains text, normalized reading, feedback and memory; the original malformed coverage remains in native call9687242.

## Findings

The concrete means case is corrected and ordinary repair retained. Invalid/incomplete interpretations cannot use the missing-rule judge/request path. Focused actual-runner checks cover declared and historical information modes, judge enabled/disabled, and provider/schema failure as well as explicit incomplete coverage:68passed,exit0. Independent code review reproduced and then confirmed closure of the LLMError bypass: zero judge calls/no delivery/constant safe clarification. Saved worlds:28,13whole,15previouslypartial,0errors,0lost,exit0. Full planning regeneration initially exposed legacy page builders assuming the old active-page scaffold; they now preserve their own scaffold and all five builders complete. See verification.txt for commands and counts.

Q36 remains open: the interpreter can still misread or falsely mark coverage complete. A malformed compound assessment safely rejecting is not proof of semantic correctness. No rule sequencer, cognition framework, extra model stage, forced social ending or universal fidelity claim follows. Browser and final release receipts retain their own outcome.
