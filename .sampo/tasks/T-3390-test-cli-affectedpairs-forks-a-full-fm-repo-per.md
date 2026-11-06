---
id: T-3390
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_cli.py, CHANGELOG.md, .sampo/**]
depends_on: []
source: discovered
created: 2026-11-06T06:54:36Z
updated: 2026-11-06T07:19:41Z
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: b1664293f265f646b6af04bd901955f023ac1bf1
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T07:18:21Z
plan0_scope: [plugin/tests/test_cli.py, CHANGELOG.md, .sampo/**]
verified: ok
unproven: [meaning]
---
# test_cli.AffectedPairs forks a full fm repo per test and nests fm check --affected; each…
## Raw request
> FIX: test_cli.AffectedPairs forks a full fm repo per test and nests fm check --affected; each test times out at 50-107 s at load ~30 and reds every lane's affected check; scale the caps with busy_factor or share one fixture (T-3306, T-3350, T-3339, T-3371 builders)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the three AffectedPairs tests that run a nested fm check --affected give it a 120 s base timeout (scaled by busy_factor), so a loaded host doesn't time them out — verify with `python3 plugin/tests/run.py test_cli.AffectedPairs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] pass timeout=120 to the nested check --affected calls in AffectedPairs
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 1.2s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 1s, AffectedPairs.test_only_the_red_first_file_itself_is_left_out 1s, AffectedPairs.test [ran] [tree 9dcd709d65a1] [world 2f1906870a] (2026-11-06T07:19:02Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 3.1s (1 jobs, 16 at a time; slowest: AffectedPairs 3s) / OK [ran] [tree 9dcd709d65a1] [world 2f1906870a] (2026-11-06T07:19:05Z)
- (audit self) `three test-only call sites raise a hang guard from 30 s to 120 s base (still × busy_factor); no assertion changed, nothing else in the class touched` → no findings [tree 9dcd709d65a1] (2026-11-06T07:19:05Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T07:19:05Z [ran] [tree 9dcd709d65a1] [world 2f1906870a] (2026-11-06T07:19:07Z)
- (audit self) `self: test-only hang-guard change, no assertion touched` → no findings [tree 9dcd709d65a1] (2026-11-06T07:19:07Z)
## Log
- 2026-11-06T06:54:36Z created
- 2026-11-06T07:18:15Z set tier=S, scope=['plugin/tests/test_cli.py', 'CHANGELOG.md', '.sampo/**']
- 2026-11-06T07:18:20Z planned: it has criteria and steps
- 2026-11-06T07:18:21Z focused
- 2026-11-06T07:18:21Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T07:19:36Z done
- 2026-11-06T07:19:41Z committed df600329d (6235 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- T-3338 [FIX S, active, 2 steps] Test runner under load: run.py scales each class's timer with busy_factor (the --deadline clamp unchanged) and records a killed class's t…
- T-2961 [FIX M, done, 1 steps] Baseline red:… — lesson: A lane's affected tests don't include the repo-wide scans (test_left_out); a merge of new library lines should run…
- decision 2026-11-04: [cites: user steer 2026-11-04: MOON CATALOGUE AT SCALE: grow the Moons catalogue to 10,000 candidate moons, all about what Sampo can do for its user…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_guard_sampo.py
## Regression test
none: the failure is a timeout that shows only under host load (the 30 s base timeout × busy_factor ran out while the nested fm check --affected waited for CPU in a 16-way test run); a deterministic red would need a stubbed clock in forkcli. The fix only raises the hang guard on three calls; the evidence is the class passing in the close's own loaded affected run
## Lessons
- a test that runs a nested fm check needs a hang guard sized for a nested test run, not the 30 s default
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
