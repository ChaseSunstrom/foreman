---
id: T-3531
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-3.md, plugin/lib/sampo/train.py, plugin/tests/test_lane_train.py]
depends_on: []
source: discovered
created: 2026-11-06T20:07:15Z
updated: 2026-11-07T00:42:53Z
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-06T20:33:37Z
plan0_scope: []
lane_stop: merged 2026-11-07T00:04:53Z
verified: strong
unproven: [docs, perf-typed]
---
# The train's pre-filter probes (T-3474) run one lane at a time, about 2-4 min each when a…
## Raw request
> PERFORMANCE: the train's pre-filter probes (T-3474) run one lane at a time, about 2-4 min each when a lane touches a hub file (30+ affected modules), so 12 lanes spend 30-45 min before the gate: run up to 3 probes at once (each in its own scratch tree), and skip a lane whose own affected tests ran green on a base whose diff to the train's base touches none of the lane's affected modules; measure a 12-lane train's probe phase before and after
## Interpretation
Reading 1: speed the probe phase by running up to 3 probes at once (1 under load), results in candidate order, plus skip a lane's affected-tests probe when its recorded green evidence ran on a base whose diff to the train base misses its affected modules. Reading 2: make the whole train parallel (gate runs too) - ruled out: the brief names only the probe phase and the one gate run stays.
## Assumptions (confidence)
## Acceptance criteria
- [x] the train's pre-filter probes run up to 3 lanes at once, each in its own scratch tree, and a lane whose own affected tests ran green on a base whose diff to the train's base touches none of its affected modules skips its probe; the results match a serial run's on the same lanes — verify with `python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) use what exists: ThreadPoolExecutor over the existing _probe per lane, each probe already makes its own worktree; map() keeps candidate order - likely outcome: probe phase ~1/3 wall time. 2) multiprocessing pool - fails if: probes share git lock state and pickling of lane objects; heavier for subprocess-bound work. 3) do less: only the skip rule, keep serial - likely outcome: helps only lanes with fresh evidence, hub-file lanes stay slow. 4) one shared worktree merging all lanes - fails if: one lane's conflict hides others, breaks per-lane attribution. Choice 1 (85%): subprocess-bound probes parallelise fine on threads, minimal diff, ordered results.
## Risks and rollback
## Execution prompt
## Steps
1. [x] parallel probes and the skip rule, test-first, on top of T-3474
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_train` → red as expected (exit 1) · Ran 15 tests in 154.4s (1 jobs, 16 at a time; slowest: Train 145s) / FAILED (1 classes: test_lane_train.Train) [ran] [tree 6b43c7045c3f] [world 2f1906870a] (2026-11-06T20:43:24Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 15 tests in 16.2s (15 jobs, 16 at a time; slowest: Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 8s, Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_bud [ran] [tree 89019ae9f645] [world 2f1906870a] (2026-11-06T20:48:58Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 0fd4e78f60c1] (2026-11-07T00:10:53Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 19 tests in 95.0s (16 jobs, 16 at a time; slowest: Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 8s, AffectedGate 5s, Train.test_a_breaking_lane_is_named_and_left_out_wi [ran] [tree 0fd4e78f60c1] [world 2f1906870a] (2026-11-07T00:12:32Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 0fd4e78f60c1] (2026-11-07T00:12:32Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 0fd4e78f60c1] (2026-11-07T00:12:32Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 0fd4e78f60c1] (2026-11-07T00:12:32Z)
## Log
- 2026-11-06T20:07:15Z created
- 2026-11-06T20:32:45Z set tier=M
- 2026-11-06T20:32:46Z planned: it has criteria and steps
- 2026-11-06T20:32:47Z lane: ~/.claude/foreman.lanes/T-3531 on foreman/T-3531
- 2026-11-06T20:33:36Z focused
- 2026-11-06T20:33:37Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-07T00:04:53Z merged foreman/T-3531 in merge train
- 2026-11-07T00:10:52Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-3.md', 'plugin/lib/sampo/train.py', 'plugin/tests/test_lane_train.py']
- 2026-11-07T00:10:53Z scope: widened at merge to the reviewed lane's own diff (26622eef7), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-07T00:17:41Z done
- 2026-11-07T00:17:47Z committed 3b9018a7c (1336 files)
- 2026-11-07T00:42:53Z lane removed: ~/.claude/foreman.lanes/T-3531; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3474 [PERFORMANCE M, active, 1 steps] Sampo lane train spends gate runs on lanes it could have known were unmergeable: run git…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3417 [PERFORMANCE M, done, 1 steps] test_cli.AffectedPairs takes ~70 s idle and 200-520 s under load (four builders tonight… — lesson: none: a reviewed builder lane; i…
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar finished tasks took 1–4 steps
## Measurements
probe phase of a 12-lane fake train: 30.4 s serial → 11.7 s parallel (0.38x) with spare CPU; 26.8 s → 23.3 s with 15 other test classes running
## Lessons
- Run per-item checks in parallel with each item's own result and notes, gathered in input order, so output never depends on which finished first.
## Files touched
- CHANGELOG.md
- docs/map/files-lib-3.md
- plugin/lib/sampo/train.py
- plugin/tests/test_lane_train.py
