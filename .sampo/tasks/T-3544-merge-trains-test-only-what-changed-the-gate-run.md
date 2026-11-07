---
id: T-3544
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-3.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/lib/sampo/train.py, plugin/tests/test_affected_rules.py, plugin/tests/test_lane_train.py]
depends_on: []
source: user
created: 2026-11-06T22:07:14Z
updated: 2026-11-07T00:42:54Z
base: 483ea8c998fcabcdbad613d057b6da06eed34146
base_tree: 8d82ac7ab38937b5a64f2ab3af4b2c2fdfd175da
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-06T22:18:07Z
plan0_scope: []
lane_stop: merged 2026-11-07T00:04:53Z
verified: strong
unproven: [docs, perf-typed]
---
# Merge trains test only what changed: the gate runs the tests affected by the batch's merged changes (plus the rule tests), the full suite moves to the background post-merge verify and the night, and a red names its failing classes on each lane so nobody reruns a full suite to find them
## Raw request
> Merge trains test only what changed: the gate runs the tests affected by the batch's merged changes (plus the rule tests), the full suite moves to the background post-merge verify and the night, and a red names its failing classes on each lane so nobody reruns a full suite to find them
## Interpretation
Reading 1 (chosen): the train's full-suite gate (the gate equal to the affected template's runner with no names) runs only the tests the batch's merged changes reach (cli.affected since the base, rule tests included; repo-shape tests like test_rename_aliases join RULE_TESTS after T-3316's miss); the recorded pass carries its modules so closes (T-3526) and ship (T-3468) reuse it; a red gate names failing classes and its last 15 lines on the left-out lane; the full suite runs after landing as the post-merge verify; FOREMAN_FULL_GATE=1 restores the full run. Reading 2 (ruled out): drop the suite gate from trains entirely and rely on the post-merge verify alone: a red batch would land and be reverted lane by lane, costlier than an affected run.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo lane train runs run.py on the union of the lanes' affected modules plus RULE_TESTS instead of the full suite (the other gates unchanged), records that pass so closes and ship reuse it, starts the full suite as the post-merge verify in the background (pm_run, newest first), and a left-out lane's reason and brief name the failing classes and the gate's last lines; FOREMAN_FULL_GATE=1 restores the full suite — verify with `python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) Recompute cli.affected on each bisection prefix; likely outcome: correct but one map/diff pass per gate run, and a base gate gets no tests. 2) Compute once on the merged batch, filter to the test files present in each prefix; likely outcome: one call, the full suite's bisection semantics on a subset; fails if: a prefix-only interaction escapes, which the post-merge verify catches. 3) Map-link new modules to the shape tests; fails if: every future shape test needs a link. 4) use what exists: cli.affected, RULE_TESTS, pm_record/pm_spawn/pm_run, _cached_pass, the probe's class regex; likely outcome: all of 2 is glue over these. 5) do less: only the post-merge verify, no gate change; fails if: the 20-45 min gate stays, which is the complaint. Choice 2 (80%): smallest diff, reuses every piece, shape tests in RULE_TESTS cover probe, close and train at once.
## Risks and rollback
## Execution prompt
## Steps
1. [x] affected gate in the train, test-first
2. [x] failing classes on the left-out reason and the brief (T-3532)
3. [x] full suite as the post-merge verify; numbers on a real train
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_train.AffectedGate` → ✗ exit 1 · Ran 19 tests in 75.5s (1 jobs, 16 at a time; slowest: AffectedGate 49s) / FAILED (1 classes: test_lane_train.AffectedGate) [ran] [tree 16c86368e0d2] [world 2f1906870a] (2026-11-06T22:19:54Z)
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_close_affected test_ship test_affected_rules` → exit 0 · Ran 81 tests in 101.3s (9 jobs, 16 at a time; slowest: Ship 99s, Train 37s, CloseAffectedReuse 7s) / OK [ran] [tree becd5af15931] [world 2f1906870a] (2026-11-06T22:23:43Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_lane_train.AffectedGate.test_a_red_gate_names_the_failing_class_on_the_left_out_lane test_lane_train.Train.test_a_red_base_stops_the_train_instead_of_blaming_a_lane` → exit 0 · Ran 2 tests in 12.6s (2 jobs, 16 at a time; slowest: AffectedGate 3s, Train 1s) / OK [ran] [tree becd5af15931] [world 2f1906870a] (2026-11-06T22:25:44Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_doctor test_suite_hygiene test_redefinitions test_rename_aliases test_docs.MapShards test_docs.PluginFiles` → exit 0 · Ran 172 tests in 21.7s (54 jobs, 16 at a time; slowest: Train 18s, RenameAliases 8s, AffectedGate 7s) / OK [ran] [tree becd5af15931] [world 2f1906870a] (2026-11-06T22:26:10Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 62a07cb21d42] (2026-11-07T00:17:51Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 19 tests in 22.4s (19 jobs, 16 at a time; slowest: Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 8s, Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_bud [ran] [tree 62a07cb21d42] [world 2f1906870a] (2026-11-07T00:18:18Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 62a07cb21d42] (2026-11-07T00:18:18Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 62a07cb21d42] (2026-11-07T00:18:18Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 62a07cb21d42] (2026-11-07T00:18:18Z)
## Log
- 2026-11-06T22:07:14Z created
- 2026-11-06T22:17:09Z lane: ~/.claude/foreman.lanes/T-3544 on foreman/T-3544
- 2026-11-06T22:18:06Z focused
- 2026-11-06T22:18:07Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-07T00:04:53Z merged foreman/T-3544 in merge train
- 2026-11-07T00:17:50Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-3.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/train.py', 'plugin/tests/test_affected_rules.py', 'plugin/tests/test_lane_train.py']
- 2026-11-07T00:17:51Z scope: widened at merge to the reviewed lane's own diff (5bf522cb5), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-07T00:22:35Z done
- 2026-11-07T00:22:38Z committed e63c58d58 (1 file)
- 2026-11-07T00:42:54Z lane removed: ~/.claude/foreman.lanes/T-3544; dropped: merged and closed; the train merge path never removed it
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3425 [FIX M, done, 1 steps] The post-merge suite auto-reverted T-3410's docs-only merge (0cad059e5: a MASTER.md… — lesson: none: a reviewed builder lane; its lessons a…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- T-3474 [PERFORMANCE M, done, 1 steps] Sampo lane train spends gate runs on lanes it could have known were unmergeable: run git… — lesson: A check that costs a full suite…
- T-3141 [PERFORMANCE M, done, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge …
## Measurements
train test gate: all 389 test modules per run (about 20 min each, 14 runs on the 15:00 train) → 98 of 389 for 11 typical queued lanes (191 with the T-2879 rename outlier)
## Lessons
- A safety net that runs everything belongs after landing, in the background; the blocking gate runs only what the change can reach plus the repo-wide scans no map link points to.
## Plan gaps
- failed first: step 1 affected gate in the train, test-first
## Files touched
- CHANGELOG.md
- docs/map/files-lib-3.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/train.py
- plugin/tests/test_affected_rules.py
- plugin/tests/test_lane_train.py
