---
id: T-3602
type: FEATURE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-07T03:49:10Z
updated: 2026-11-07T04:26:08Z
lane: ~/.claude/foreman.lanes/T-3602
lane_branch: foreman/T-3602
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:56:22Z
plan0_scope: []
---
# PERFORMANCE merge blame without reruns (user 2026-11-06: why rerun tests to find which…
## Raw request
> PERFORMANCE merge blame without reruns (user 2026-11-06: why rerun tests to find which branch failed, why can't you just see it): a red train gate bisects by re-running the WHOLE gate (doctor, e2e, bench, mod tests, ~180 test modules) on prefixes — 6+ full runs in the 20:22 batch (~15 min each) to blame T-3500 for test_rename_scan.PluginIds, whose own failure output names the offending files. Blame from the red run itself: (1) map each failing test's output paths and the failing classes' covered/affected files to the lanes whose diffs touch them; (2) if one lane matches, leave it out with no rerun; (3) only when ambiguous, probe prefixes with just the failing classes (seconds, not the whole gate); (4) the final check runs the failing classes plus the tests the removed lane's diff affects, not the whole gate again
## Interpretation
Reading 1 (chosen): a red train gate blames lanes from its own output instead of re-running the whole gate on prefixes: each failing class's failure text, the lanes' diffs and the affected-test map name the culprit; only an ambiguous red bisects, each probe running just the failing command on just the failing classes; the confirm after leaving lanes out runs the failing classes plus the removed lanes' reach and the gates the red stopped before. Reading 2 (ruled out): only make each bisection probe cheaper (class-only) but keep bisecting every red: still log2 n runs per red when the output already names the lane, which is what the user asked about.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a culprit the failure output names is left out with zero probes and a narrowed confirm; an ambiguous red bisects with class-only probes; two culprits both go; a lane depending on a removed one is caught by the confirm — verify with `nice -n 10 python3 plugin/tests/run.py test_lane_train`
- [ ] an ambiguous red bisects with probes of only the failing classes (each probe's command asserted) and the confirm after leaving lanes out runs only the failing classes plus the removed lanes' reach — verify with `nice -n 10 python3 plugin/tests/run.py test_lane_train`
## Non-goals
## Approach (options → choice → why)
1) do less: keep prefix bisection, narrow each probe to the failing classes; likely outcome: minutes instead of hours, but still log2 n runs per red even when the output names the lane. 2) use what exists: blame per failing class from the red run with what the repo has (the failure text, git diffs, cli.affected(only=) as the map's reach, the affected template to narrow a run, _probe's flake/base checks as the model); bisect with class-only probes only when ambiguous; confirm narrowed; fails if: a wrong unique blame leaves an innocent lane out (the confirm still red loops on, so never a red landing). 3) run each lane's reach on the full merge minus that lane: n runs per red; fails if: n is 12. Choice 2 (80%): zero reruns when the output names the lane (the 20:22 case), seconds otherwise; 1 is its ambiguous fallback.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] Failing tests: named culprit with no probe, ambiguous class-only probes, two culprits, dependent lane caught by the confirm  <- CURRENT
2. [x] Blame from the red run: per-class texts, rules a/c/b, class-only bisection, narrowed confirm; report the rule
3. [x] Numbers: replay the 20:22 batch's reds, old vs new gate runs and minutes
4. [x] Review fixes: reproduce red names alone before narrowing or bisecting, complete red-name parsing (fixtures, run.py's never-started, count), every non-suite gate reruns in the confirm
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_lane_train -k culprit -k ambiguous -k independent -k needing -k names_the_failing` → ✗ exit 1 · Ran 6 tests in 65.0s (2 jobs, 16 at a time; slowest: AffectedGate 20s, Train 3s) / FAILED (1 classes: test_lane_train.AffectedGate) [ran] [tree dce2ed0d3f6f] [world 2f1906870a] (2026-11-07T04:04:02Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_lane_train` → exit 0 · Ran 23 tests in 9.8s (23 jobs, 16 at a time; slowest: Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 7s, AffectedGate.test_a_lane_needing_a_left_out_lane_is_caught_by_the_con [ran] [tree 70cfc9f125af] [world 2f1906870a] (2026-11-07T04:09:07Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_close_affected test_doctor test_check_paths` → exit 0 · Ran 157 tests in 63.9s (79 jobs, 16 at a time; slowest: LockProbe 17s, AffectedGate.test_the_gate_names_only_the_affected_modules_and_the_rule_tests 14s, Train.test_a_red_base_stops_the_train_instead_ [ran] [tree cd967ea15e9e] [world 2f1906870a] (2026-11-07T04:13:54Z)
- (step 3) `replay of the 18:56 and 20:22 trains from the ledger, lane reflogs, git diffs and recorded failure tails` → 18:56 train (6 gate lanes, reds DiffGates + PluginIds): old 8 whole gate runs, 45.1 min gate phase (first build 19:25:16, land 20:10:19); new: DiffGates -> T-3550 (rule c: only lane changing test_diff_gates.py), PluginIds -> T-3539 (rule a: only lane whose diff has plugin/tests/test_drive_wait.py, the file the failure names; old bisection blamed T-2879 by order); 1 whole run + 1 narrowed confirm (~2 min est.), 0 probes, ~8 min. 20:22 train (12 lanes): T-3500 blamed 79 min in (5-6 whole runs after the probe phase), killed at 86 min bisecting a second red; new: T-3500 is the only lane of 12 whose diff has plugin/tests/test_lane_land.py, the file PluginIds names: blamed from the first red run, 0 probes [tree cd967ea15e9e] (2026-11-07T04:14:09Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_lane_train -k green_alone -k passed_before -k RedNames` → ✗ exit 1 · Ran 6 tests in 12.6s (3 jobs, 16 at a time; slowest: AffectedGate.test_a_class_green_alone_bisects_with_the_whole_suite_gate 7s, AffectedGate.test_a_gate_that_passed_before_the_red_one_reruns_in_the_c [ran] [tree 6bfaa4fce8e4] [world 2f1906870a] (2026-11-07T04:23:25Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_close_affected test_doctor test_check_paths` → ✗ exit 1 · Ran 162 tests in 93.6s (87 jobs, 16 at a time; slowest: Train.test_a_breaking_lane_is_named_and_left_out_within_the_gate_budget 9s, Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_ [ran] [tree 5d9025a8c516] [world 2f1906870a] (2026-11-07T04:25:08Z)
- (step 4) `nice -n 10 python3 plugin/tests/run.py test_lane_train test_close_affected test_doctor test_check_paths test_docs` → exit 0 · Ran 276 tests in 33.0s (111 jobs, 16 at a time; slowest: Fences 18s, ViewsRepair 15s, Train.test_probes_run_three_at_once_and_leave_out_what_a_serial_run_does 10s) / OK [ran] [tree d3c03e104fce] [world 2f1906870a] (2026-11-07T04:25:48Z)
- (step 3) `replay after the review fixes (same data)` → 18:56 train: old 8 whole gate runs, 45.1 min gate phase -> new 1 whole red run + 1 probe of the 2 red classes alone (seconds) + 1 confirm (the other gates whole, ~100 s from the train's recorded rows: doctor 43, e2e 6, bench 21, ui 13, replay 18; the suite on the red classes + left-out reach, ~1.5 min est.) = 2 gate runs, ~10 min. 20:22 train: T-3500 blamed from the first red run (rule a), 1 probe, no bisection. [tree d3c03e104fce] (2026-11-07T04:26:08Z)
## Log
- 2026-11-07T03:49:10Z created
- 2026-11-07T03:56:03Z planned: it has criteria and steps
- 2026-11-07T03:56:07Z lane: ~/.claude/foreman.lanes/T-3602 on foreman/T-3602
- 2026-11-07T03:56:21Z focused
- 2026-11-07T03:56:22Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3531 [PERFORMANCE M, done, 1 steps] The train's pre-filter probes (T-3474) run one lane at a time, about 2-4 min each when a… — lesson: Run per-item checks in parallel…
- T-3544 [PERFORMANCE M, done, 3 steps] Merge trains test only what changed: the gate runs the tests affected by the batch's merged changes (plus the rule tests), the full…
- T-3474 [PERFORMANCE M, done, 1 steps] Sampo lane train spends gate runs on lanes it could have known were unmergeable: run git… — lesson: A check that costs a full suite…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
