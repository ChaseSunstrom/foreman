---
id: T-3474
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/train.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lane_train.py, CHANGELOG.md, MASTER.md, docs/map/**, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-3.md]
depends_on: []
source: discovered
created: 2026-11-06T17:41:38Z
updated: 2026-11-07T00:42:49Z
base: 8b61cb1082cf8cdc9efee5ee9ef7869d024fc263
base_tree: f997eb98c8d4be4238b3699f7edc2ec5717a28e2
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T19:01:01Z
plan0_scope: [plugin/lib/sampo/train.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lane_train.py, CHANGELOG.md, MASTER.md, docs/map/**]
lane_stop: merged 2026-11-06T21:46:50Z
verified: strong
unproven: [docs, perf-typed]
---
# Sampo lane train spends gate runs on lanes it could have known were unmergeable: run git…
## Raw request
> sampo lane train spends gate runs on lanes it could have known were unmergeable: run git merge-tree against the base for each candidate first (instant, no tree) and leave conflicting ones out up front with the files, so a red bisection only ever covers clean lanes; the first train today: 7 lanes, 6 gate runs, 2 landed, 3 left out on conflicts that merge-tree names in milliseconds
## Interpretation
Reading 1 (chosen): before the train's first gate run, leave out lanes knowable as unlandable cheaply: git merge-tree --write-tree base tip (exit 1 = conflict, files named) and the lane's affected tests (cli.affected since=base) run on base+lane in a throwaway detached worktree (red = left out, failing classes named); survivors go through the unchanged build/gate/bisect flow. Reading 2 (ruled out): only the merge-tree conflict filter, as the raw request names; ruled out because the brief also asks for the affected-tests probe and reds cost more gate runs than conflicts (build() already catches conflicts without a gate run).
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo lane train leaves a lane out before any gate run when it conflicts with the base (git merge-tree) or its affected tests fail on the base plus that lane, naming the files or classes; a clean, green lane still lands in one gate run — verify with `python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) per-lane probe in train._run after _held/_verify: merge-tree, then the affected tests in a temp worktree, one lane after another. Likely outcome: a conflicting or red lane costs milliseconds or a minute instead of a bisection. Fails if: a flaky affected test leaves a good lane out (the full gate has no flaky rerun either).
2) run all lanes' affected tests once on the merged train tree. Likely outcome: one probe run. Fails if: a red can't be blamed on one lane without bisecting again.
3) parallel per-lane probes. Likely outcome: faster wall clock. Fails if: the saturated machine slows every probe and pool code grows the diff.
4) use what exists: cli.affected (fm check --affected, release._affected_first) for the selection, release's FAIL/ERROR class regex, _git and train.py's scratch-worktree pattern. Likely outcome: no new selection code; it is the base of option 1.
5) do less: only the merge-tree filter. Likely outcome: honest conflict messages. Fails if: red lanes still bisect with full gate runs.

Choice 1 (80%): one helper _probe in train.py built on option 4; a timeout (124) or a no-tests run (5) is inconclusive and the lane goes on; a merge-tree error other than exit 1 goes on. Why: smallest diff that blames exactly one lane, no new deps.
## Risks and rollback
Blast radius (sampo graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py; past FIXes T-1303, T-1671, T-1674, T-1678, T-1707.
## Execution prompt
## Steps
1. [x] failing tests, then the merge-tree and affected-test filters before the train's first gate run
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lane_train` → ✗ exit 1 · Ran 10 tests in 10.6s (10 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 2s, Train.test_a_middle_culprit_costs_one_regate_more 1s, Train.test_a_co [ran] [tree b138082921a6] [world 2f1906870a] (2026-11-06T19:01:47Z)
- (step 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 10 tests in 15.0s (10 jobs, 16 at a time; slowest: Train.test_a_conflicting_lane_is_skipped_with_its_files_and_main_only_fast_forwards 2s, Train.test_a_breaking_lane_is_named_and_left_out_within_t [ran] [tree 9b26afba4439] [world 2f1906870a] (2026-11-06T19:03:11Z)
- (step 1) `python3 plugin/tests/run.py test_lane_train` → ✗ exit 1 · Ran 12 tests in 1.7s (12 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 1s, Train.test_a_middle_culprit_costs_one_regate_more 1s, Train.test_a_con [ran] [tree 6df66577d5b0] [world 2f1906870a] (2026-11-06T19:07:04Z)
- (step 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 12 tests in 1.6s (12 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 1s, Train.test_a_middle_culprit_costs_one_regate_more 1s, Train.test_a_con [ran] [tree 7b38bd20d8ec] [world 2f1906870a] (2026-11-06T19:07:54Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree ad679841a16b] (2026-11-06T21:53:25Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 12 tests in 158.9s (12 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 3s, Train.test_a_middle_culprit_costs_one_regate_more 2s, Train.test_a_c [ran] [tree ad679841a16b] [world 2f1906870a] (2026-11-06T21:56:09Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree ad679841a16b] (2026-11-06T21:56:09Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree ad679841a16b] (2026-11-06T21:56:09Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree ad679841a16b] (2026-11-06T21:56:09Z)
## Log
- 2026-11-06T17:41:38Z created
- 2026-11-06T18:27:02Z set tier=M, scope=['plugin/lib/sampo/train.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_train.py', 'CHANGELOG.md', 'MASTER.md', 'docs/map/**']
- 2026-11-06T18:27:06Z planned: it has criteria and steps
- 2026-11-06T18:27:37Z criterion 1 removed: sampo lane train leaves a lane out before any gate run when it conflicts with the base (git merge-tree) or its affected tests fail on the base plus that lane, naming the files or classes; a clean, green lane still lands in one gate run — verify with `python3 plugin/tests/run.py test_train`
- 2026-11-06T18:27:38Z set scope=['plugin/lib/sampo/train.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lane_train.py', 'CHANGELOG.md', 'MASTER.md', 'docs/map/**']
- 2026-11-06T18:28:30Z lane: ~/.claude/foreman.lanes/T-3474 on foreman/T-3474
- 2026-11-06T19:00:58Z focused
- 2026-11-06T19:01:01Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-06T21:46:50Z merged foreman/T-3474 in merge train
- 2026-11-06T21:53:24Z set scope=['plugin/lib/sampo/train.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lane_train.py', 'CHANGELOG.md', 'MASTER.md', 'docs/map/**', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-3.md']
- 2026-11-06T21:53:24Z scope: widened at merge to the reviewed lane's own diff (7ec3be4b0), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T22:10:58Z done
- 2026-11-06T22:11:04Z committed ae1cf7a6e (1 file)
- 2026-11-07T00:42:49Z lane removed: ~/.claude/foreman.lanes/T-3474; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3406 [FIX M, done, 1 steps] Sampo lane train can never pass in this repo: its gates run in a scratch worktree, where… — lesson: none: a reviewed builder lane; its less…
- T-3425 [FIX M, done, 1 steps] The post-merge suite auto-reverted T-3410's docs-only merge (0cad059e5: a MASTER.md… — lesson: none: a reviewed builder lane; its lessons a…
- T-3268 [FEATURE M, active, 4 steps] Moon C-000616: lane_preview trial-merges every open lane branch against main and each other (git merge-tree) and lane list names the …
- decision 2026-11-06: Post-merge suite back on (supersedes the pause): a close runs only its criteria and affected tests, not the full suite, so the post-merge run is the…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Measurements
full gate runs per train: 6 (train 1, 2 of 7 landed) and 5 (train 2) → 1 when the probes catch the conflicting and red lanes first (test_lane_train: 0 gate runs for a conflicting lane, 1 for a clean one)
## Lessons
- A check that costs a full suite to fail should come after every check that can fail the same lane in a minute.
## Plan gaps
- failed first: step 1 failing tests, then the merge-tree and affected-test filters before the train's first gate run
## Files touched
- CHANGELOG.md
- docs/map/files-lib-3.md
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/train.py
- plugin/tests/test_lane_train.py
