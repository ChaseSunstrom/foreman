---
id: T-2613
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmlong.py, plugin/tests/test_long.py, CHANGELOG.md, MASTER.md, plugin/skills/genesis/SKILL.md]
depends_on: []
source: genesis
created: 2026-11-02T13:58:28Z
updated: 2026-11-02T14:15:15Z
base: 71981f466d735a499fab5abc726756e603d547eb
base_tree: 80e2251b21d2e7d5eb32b207414f9d42cf2b10df
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T13:58:58Z
plan0_scope: [plugin/lib/fmlong.py, plugin/tests/test_long.py, CHANGELOG.md, MASTER.md, plugin/skills/genesis/SKILL.md]
verified: strong
---
# fm exam long grade splits false dones into misses on names the goal never states and real misses
## Raw request
> FEATURE: fm exam long grade splits false dones: the runner keeps each failing check's last traceback line; a failure naming a missing attribute, key or import that the goal text never mentions is out of the goal's reach, anything else is real; a false-done goal whose misses are all out of reach reads apart ("false done N (M only on names the goal never states)"), and the JSON carries each failed check's class and line; MASTER, CHANGELOG and the genesis skill's exam step say it
## Interpretation
Reading 1 (chosen): the grader keeps why each hidden check failed and classes a failure naming a missing attribute, key or import that the goal text never mentions as out of the goal's reach; a false-done goal whose misses are all out of reach reads apart, so the long tier's false-done number separates the exam's reach from Foreman's misses (T-2556 did this by hand: 17 of 31). Reading 2: drop such goals at gen, as pinned values are dropped; rejected because it changes which goals the exam asks mid-tower and hides the misses instead of showing them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a failing hidden check naming an attribute, key or import absent from the goal text is classed reach; one the goal names, or an assertion failure, is real — verify with `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split`
- [x] the grade's JSON carries each failed check's class and line, false_done_reach counts false-done goals whose misses are all reach, and the text prints the split — verify with `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split`
- [x] the long tier's existing tests pass — verify with `python3 plugin/tests/run.py test_long`
## Non-goals
## Approach (options → choice → why)
1) RUNNER writes each failing id's last traceback line to a .why file beside ok.json; _passed fills an optional why dict; grade adds misses [{check, line, reach}] and false_reach; _totals counts false_done_reach; the text adds 'false done N (M only on names the goal never states)'. Likely outcome: l001's regrade splits its 6 false dones. Fails if: a real bug happens to name an unstated symbol (counted reach; only names the goal text lacks count, so a stated name is always real). 2) use what exists: keep research long-false-done refreshed by hand each generation. Fails if: the end-of-run exam prints one number again. 3) do less: drop goals whose checks use unstated names at gen. Fails if: it changes the exam's goals mid-tower and hides misses. Choice 1 (80%): the grader already runs every check, so keeping its failure line costs one field and keys and goals stay untouched.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1056, T-1106, T-1117, T-1122, T-1124.
## Execution prompt
## Steps
1. [x] red: test_long.ReachSplit
2. [x] runner .why, _passed why, _reach, grade misses and false_reach, totals and text
3. [x] regrade l001 and l002 at zero tokens and record the split
4. [x] docs: CHANGELOG, MASTER (fmlong), genesis skill step 4
## Resume here
## Docs impact
CHANGELOG (Unreleased entry); MASTER.md fmlong line (T-2613 note); plugin/skills/genesis/SKILL.md step 4 (the long grade's split). No site page: the exam page reads the grade line.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split` → ✗ exit 1 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Long 1s) / FAILED (1 classes: test_long.Long) [ran] [tree 9f1cab864ddf] [world 2f1906870a] (2026-11-02T14:00:23Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 58 tests in 33.9s (9 classes, 16 at a time; slowest: Long 34s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree cfc538f38863] [world 2f1906870a] (2026-11-02T14:01:25Z)
- (step 3) `fm exam long grade l001 --agent foreman && fm exam long grade l002 --agent foreman` → exit 0 · where the time went: tools none kept; fm verbs none kept / false done 6 (0 only on names the goal never states) [ran] [tree cfc538f38863] [world 2f1906870a] (2026-11-02T14:04:17Z)
- (step 4) `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree c352ca099b67] [world 2f1906870a] (2026-11-02T14:04:51Z)
- (step 2) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 59 tests in 34.0s (9 classes, 16 at a time; slowest: Long 34s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree 8be29feb541c] [world 2f1906870a] (2026-11-02T14:07:19Z)
- (audit edge) `self (subagents held by the budget guard)` → found and fixed: an answer's exception whose str() raises would have crashed the runner in its except block and lost every other check's result (test added). A stated name is always real (word match on the goal); return-shape failures aren't classed, so the split is a lower bound (13 of 31 vs the hand read's 17). Unanswered goals carry no misses and never read reach. [tree 8be29feb541c] (2026-11-02T14:07:20Z)
- (audit intent) `self` → the grade prints false done N (M only on names the goal never states) and carries each failed check's line and class; l001 foreman 6 -> 2 reach, l002 0 of 6; keys and goals are untouched, and untrusted failure text is plain'd and cut before it enters the JSON [tree 8be29feb541c] (2026-11-02T14:07:20Z)
- (ac 1) `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree 8be29feb541c] [world 2f1906870a] (2026-11-02T14:13:37Z)
- (ac 2) `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree 8be29feb541c] [world 2f1906870a] (2026-11-02T14:13:37Z)
- (ac 3) `python3 plugin/tests/run.py test_long` → exit 0 · Ran 59 tests in 34.0s (9 classes, 16 at a time; slowest: Long 34s, DoorFault 5s, MissionEightFaults 2s) / OK [ran] [tree 8be29feb541c] [world 2f1906870a] (2026-11-02T14:13:37Z)
- (step 1) `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Long 1s) / OK [ran] [tree 8be29feb541c] [world 2f1906870a] (2026-11-02T14:13:37Z)
- (audit intent) `self-review over the diff (subagents held by the budget guard); one edge found and fixed (runner exception text)` → the grade prints false done N (M only on names the goal never states) with each failed check's line and class; l001 foreman 6 -> 2 reach, l002 0 of 6; keys and goals untouched [tree 8be29feb541c] (2026-11-02T14:13:37Z)
- (audit edge) `self-review over the diff (subagents held by the budget guard); one edge found and fixed (runner exception text)` → an exception whose str() raises no longer crashes the runner (test); a stated name is always real; return shapes aren't classed, so the split is a lower bound (13 of 31 vs 17 by hand) [tree 8be29feb541c] (2026-11-02T14:13:37Z)
## Log
- 2026-11-02T13:58:28Z created
- 2026-11-02T13:58:57Z planned from capture
- 2026-11-02T13:58:57Z set approved=True
- 2026-11-02T13:58:58Z focused
- 2026-11-02T13:58:58Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T14:00:16Z criterion 1 verify: `python3 plugin/tests/run.py test_long.ReachSplit` → `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split`
- 2026-11-02T14:00:16Z criterion 2 verify: `python3 plugin/tests/run.py test_long.ReachSplit` → `python3 plugin/tests/run.py test_long.Long.test_a_failure_on_a_name_the_goal_never_states_is_out_of_reach test_long.Long.test_grade_classes_each_failed_check_and_counts_all_reach_false_dones test_long.Long.test_the_grade_text_prints_the_split`
- 2026-11-02T14:15:13Z done
- 2026-11-02T14:15:15Z committed c0c2ba3f (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2556 [RESEARCH M, done, 2 steps] Diagnose the long tier's false dones: class every failed hidden check on l001 and l002 against what the goal stated — lesson: a done-r…
- research long-false-done: Source: fm exam long l001 and l002, foreman arm (2026-10-31). Each goal's hidden checks were rerun on the session's kept tree the grader's way …
- T-2166 [FEATURE M, done, 4 steps] Cold read on every tower write: fm genesis put (and the tower's own writers: exam_line,… — lesson: A nondeterministic cold reader finds…
- decision 2026-11-02: Recommendation: build T-2557 (a goal session's done claim checks each stated Done-when line and requirement against the tree, or names it missing), …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_audit.py, plugin/tests/test_board_surfaces.py, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_cost.py, plugin/test…
## Lessons
- When an automatic rule replaces a hand classification, state up front which way it may differ: this one is a lower bound by design (a key that appears as an ordinary word reads as stated), and 13 against the hand read's 17 is that design, not a miss
## Plan gaps
- failed first: step 1 red: test_long.ReachSplit
## Files touched
- plugin/tests/test_long.py
- plugin/lib/fmlong.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/genesis/SKILL.md
