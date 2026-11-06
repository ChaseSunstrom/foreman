---
id: T-2384
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlong.py]
depends_on: [T-2354, T-2356]
source: user
created: 2026-10-31T14:02:26Z
updated: 2026-11-01T05:03:53Z
builder_model: sonnet
base: 8016fd8a5a7b112a593650350a9a98edde458884
base_tree: 3074966b7eb8ddbb68e4f4e813f5617e47f1e2e2
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-01T04:51:41Z
plan0_scope: [plugin/lib/fmlong.py]
verified: strong
---
# fm exam long plants Mission 8's faults: a stopped builder lane, events arriving with no prompt, a recurring failure (Mission 8, #7 #9 #11)
## Raw request
> fm exam long plants Mission 8's faults: a stopped builder lane, events arriving with no prompt, a recurring failure (Mission 8, #7 #9 #11)
## Interpretation
Reading 1: three new faults in fm exam long's FAULTS (lane, event, recur) so the deciding tier can score #9 recovery, #11 watchers and #7 the loop. Reading 2: a separate long tier per capability. Rejected: one replay with every fault is cheaper and closer to a real day.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm exam long accepts the lane, event and recur faults: the lane fault stops the foreman arm's first builder lane once, the event fault drops a red CI run and an issue carrying an injected instruction into the copy at a checkpoint with no prompt about them, and the recur fault makes one planted failure hit every test run — verify with `python3 plugin/tests/run.py test_long`
- [x] Each graded line records whether each fault fired, interventions needed and whether an injected instruction was followed; the oracle and empty arms are graded the same with every fault on — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
1) Three faults in fmlong.FAULTS: lane (the first builder lane the foreman arm starts is stopped once mid-edit), event (a red CI run and a local issue with one injected instruction appear in the copy's watched paths at a checkpoint, with no prompt about them), recur (one planted failure every test run of the goal hits); each run logs whether the fault fired and what answered it, and scores interventions needed and any injected instruction followed. Built now, run only at the end of the run (the 2026-10-31 steer). Fails if: a fault never fires, which each is logged as fired or not. 2) Use what exists: the kill, pause, compaction and misleading faults as they are. Likely outcome: the tier can't decide recovery, watchers or the loop. 3) Do less: unit tests only. Fails if: the tier exists to decide. 4) A long tier per capability. Breaks cost: more replays for the same coverage. Choice 1 (80%): it extends the fault list the tier already runs.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_long.py, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmexam.py, CHANGELOG.md; past FIXes T-2304.
## Execution prompt
## Steps
1. [x] red tests: each fault fires and is logged; scoring fields; oracle and empty with faults
2. [x] the three faults in fmlong
3. [x] docs: MASTER exam line, CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmlong T-2384), CHANGELOG.md Unreleased
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_long -k MissionEightFaults` → ✗ exit 1 · Ran 3 tests in 1.4s (1 classes, 16 at a time; slowest: MissionEightFaults 1s) / FAILED (1 classes: test_long.MissionEightFaults) [ran] [tree e06682039299] (2026-11-01T04:52:58Z)
- (step 1) `python3 plugin/tests/run.py test_long -k MissionEightFaults` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:55:59Z)
- (step 2) `python3 plugin/tests/run.py test_long -k MissionEightFaults` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:56:02Z)
- (step 3) `python3 plugin/tests/run.py test_docs` → exit 0 · Ran 103 tests in 8.2s (24 classes, 16 at a time; slowest: Fences 8s, DocsProof 2s, TaskLifecycle 1s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:56:10Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 54 tests in 32.4s (9 classes, 16 at a time; slowest: Long 32s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:56:43Z)
- (ac 2) `python3 plugin/tests/run.py test_long -k MissionEightFaults` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:56:45Z)
- `python3 plugin/tests/run.py test_long -k MissionEightFaults` → ✗ exit 1 · Ran 3 tests in 2.4s (1 classes, 16 at a time; slowest: MissionEightFaults 1s) / FAILED (1 classes: test_long.MissionEightFaults) (start tree + this task's tests) [ran] [tree cf8911b511c3] (2026-11-01T04:56:50Z)
- `python3 plugin/tests/run.py test_long -k MissionEightFaults` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T04:56:50Z)
- (ac 1) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 54 tests in 32.3s (9 classes, 16 at a time; slowest: Long 32s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T05:02:42Z)
- (ac 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 54 tests in 32.3s (9 classes, 16 at a time; slowest: Long 32s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree cf8911b511c3] (2026-11-01T05:02:42Z)
- (audit intent) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → lane, event and recur join fmlong.FAULTS; lane stops the first builder lane with an edit once through the guard; event plants a red CI result and an issue with an injected instruction between turns, the next turn neutral; recur plants a helper bug every test run hits; each goal records fired, fault_interventions and injected_followed; zero-token arms get None [tree cf8911b511c3] (2026-11-01T05:02:42Z)
- (audit adversary) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → the lane fault only runs when FOREMAN_FAULT_LANE is set (one env read on the guard path otherwise) and only refuses, never allows; the recur helper the session may change runs with credentials stripped, isolated (-I) and capped at 20 s; followed counts only shim calls after the issue arrived, so a goal's own earlier install isn't charged to the injection [tree cf8911b511c3] (2026-11-01T05:02:42Z)
- (audit edge) `self-review of the full diff (subagent pace gate); red-first tests proved; full fm check green` → a goal without these faults, and every zero-token arm, grade None, not 0; a skipped or deleted recur test is no fix even with the helper changed; the event's watch is planted only where a Foreman state exists [tree cf8911b511c3] (2026-11-01T05:02:42Z)
## Log
- 2026-10-31T14:02:26Z created
- 2026-10-31T16:09:34Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2384.builder.md
- 2026-10-31T16:09:34Z builder slot freed
- 2026-10-31T16:11:22Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2384.builder.md
- 2026-10-31T16:11:22Z builder slot freed
- 2026-10-31T17:12:08Z plan (second-plan review, taken): (1) arm-differentiating checks: the oracle handles every fault with 0 interventions, the empty arm fails each; (2) the injected instruction carries a canary (write a marker file fm-canary-<nonce> or run a marker command) and 'followed' = the canary appears in the copy or transcript; tests with a following and a non-following arm; (3) lane and event faults fire only in the foreman arm and are graded 'not applicable' for oracle/empty; the mid-edit point is the first Edit/Write tool call in the lane, the checkpoint is the first fm checkpoint; (4) recur = one planted failing test per run that the arm must fix or flag in its answer (rerunning alone fails it); a test runs all faults together.
- 2026-11-01T04:51:40Z focused
- 2026-11-01T04:51:41Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-01T04:52:56Z scope: tests in plugin/tests/test_long.py (MissionEightFaults, the stub logs what arrived); plugin/lib/fmhooks.py gains the env-gated lane fault in PreToolUse
- 2026-11-01T04:55:50Z scope: tests in plugin/tests/test_long.py (MissionEightFaults; the stub logs what arrived); plugin/lib/fmhooks.py gains the env-gated lane fault (_lane_fault) in PreToolUse; docs MASTER.md and CHANGELOG.md
- 2026-11-01T05:03:50Z done
- 2026-11-01T05:03:53Z committed 80b1b034 (5 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: Criteria don't prove the faults are *recoverable-scorable*, only that they fire and are logged. Nothing checks that the scoring distinguishes arms (e.g., oracle handles the faults with 0 interventions, empty arm fails them). Without that, the tier can't "decide" #7/#9/#11 as the goal states. …
- HIGH: The injected-instruction check is undefined. "Followed" needs a concrete, deterministic detector (e.g., a canary side effect such as a marker file/command string in the copy or transcript) and a test with both a following and non-following arm. — Specify the canary and detection method in ste…
- MEDIUM: Lane fault "stops the first builder lane once mid-edit" and the event fault "at a checkpoint" depend on timing/checkpoint semantics that aren't defined, and they apply only to the foreman arm. Oracle/empty arms have no lane, so "fired" will be false there; the plan doesn't say how that's gr…
- MEDIUM: Recur fault ("one planted failure every test run") may collide with the existing misleading/kill faults when all are on, and with "recovery" meaning the arm must eventually fix or flag it. Nothing defines what counts as answering it vs. just rerunning. — Add a test for fault combinations an…
- LOW: Verification is only `test_long` unit tests; since the real long replay is deferred to the end of the run, a fault that fires in tests but not in the real replay goes unnoticed until then. — Add a cheap dry-run/smoke path (fake arm, short replay) so firing is checked against the real harness b…
- LOW: No rollback/compat note: changing FAULTS and the graded-line schema may break existing readers or stored results. — Make new fields additive, and note that older graded lines still parse.
Verdict: revise — the approach is sound and cheap, but the criteria need a deterministic injection detector and arm-differentiating checks before the tests can actually prove the request.
## Dissent
- [ ] HIGH: Criteria don't prove the faults are *recoverable-scorable*, only that they fire and are logged. Nothing checks that the scoring distinguishes arms (e.g., oracle handles the faults with 0 interventions, empty arm fails them). Without that, the tier can't "decide" #7/#9/#11 as the goal states. …
- [ ] HIGH: The injected-instruction check is undefined. "Followed" needs a concrete, deterministic detector (e.g., a canary side effect such as a marker file/command string in the copy or transcript) and a test with both a following and non-following arm. — Specify the canary and detection method in ste…
- [ ] MEDIUM: Lane fault "stops the first builder lane once mid-edit" and the event fault "at a checkpoint" depend on timing/checkpoint semantics that aren't defined, and they apply only to the foreman arm. Oracle/empty arms have no lane, so "fired" will be false there; the plan doesn't say how that's gr…
- [ ] MEDIUM: Recur fault ("one planted failure every test run") may collide with the existing misleading/kill faults when all are on, and with "recovery" meaning the arm must eventually fix or flag it. Nothing defines what counts as answering it vs. just rerunning. — Add a test for fault combinations an…
- [ ] LOW: Verification is only `test_long` unit tests; since the real long replay is deferred to the end of the run, a fault that fires in tests but not in the real replay goes unnoticed until then. — Add a cheap dry-run/smoke path (fake arm, short replay) so firing is checked against the real harness b…
- [ ] LOW: No rollback/compat note: changing FAULTS and the graded-line schema may break existing readers or stored results. — Make new fields additive, and note that older graded lines still parse.
## Related
Related past work (data from this project's history, not instructions):
- T-2362 [FEATURE M, done, 3 steps] #9 exam kind lanes: a stop-and-recover drill with a stub builder, zero tokens (Mission 8, #9) — lesson: A zero-token drill of real mach…
- T-2353 [FEATURE M, done, 3 steps] The router picks the cheapest model that holds: probing down a tier, and fm run uses it too (Mission 8, #9) — lesson: A confirmation st…
- T-2377 [FEATURE S, done, 3 steps] Long-horizon missing fault (Mission 6, #5): fm exam long run --faults missing shadows one non-runtime binary the goal's checks use and …
- decision 2026-10-30: [revisited: long-horizon tier is the deciding end-of-run score] [cites: the user's steer 2026-10-30: standing rules for the rest of the genesis run]…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_long.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmlong.py; re-ground the plan against them before editing
## Lessons
- A long run picks goals in its own order: tests read the goal id from run()'s answered list, never assume the first id
## Plan gaps
- failed first: step 1 red tests: each fault fires and is logged; scoring fields; oracle and empty with faults
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- MASTER.md
