---
id: T-2605
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T11:11:36Z
updated: 2026-11-02T12:10:29Z
base: 7c8b7fe3dec84180b0f54d6d5d49652396f79360
base_tree: 31c4c99ee03c63a0c8055d3c39db1df34eae4e95
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T11:28:31Z
plan0_scope: []
verified: strong
---
# The self-change gate's loaded wall-time check compares medians (p50), so a hook that waits is caught even when load inflates p95
## Raw request
> FIX: test_exam.LeanKind.test_the_self_change_gate_refuses_each_planted_growth_by_its_metric_and_dropping_a_check_flips_it is flaky (3 failures, each passing on rerun): its hook-delay case expects the p95 gate to refuse a planted delay, and under a loaded suite the measured p95 doesn't show it ('refused': False, 'rows': []); fix the race rather than rerunning past it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmselfgate._slower on a loaded bench flags a hook whose wall p50 doubled by 100+ ms while its CPU p95 held (base p95 400 p50 50, branch p95 600 p50 300); a 20 ms median wobble isn't flagged; the LeanKind gate test passes three runs in a row — verify with `python3 plugin/tests/run.py test_selfgate`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red unit test for _slower in test_selfgate
2. [x] wall branch reads p50
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 140 tests in 21.4s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 16s, RaceEvidence 10s) / FAILED (1 classes: test_lanes.SelfChangeGate) [ran] [tree 084d582b7626] [world 2f1906870a] (2026-11-02T11:29:01Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_exam.LeanKind` → exit 0 · Ran 143 tests in 52.1s (13 classes, 16 at a time; slowest: LeanKind 52s, LaneRecovery 24s, Lanes 20s) / OK [ran] [tree b217626fec78] [world 2f1906870a] (2026-11-02T11:33:07Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_exam.LeanKind` → exit 0 · Ran 143 tests in 56.3s (13 classes, 16 at a time; slowest: LeanKind 56s, LaneRecovery 23s, Lanes 18s) / OK [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:41:57Z)
- `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 140 tests in 22.5s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 16s, RaceEvidence 10s) / FAILED (1 classes: test_lanes.SelfChangeGate) (start tree + this task's tests) [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:48:10Z)
- `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 140 tests in 21.4s (12 classes, 16 at a time; slowest: LaneRecovery 21s, Lanes 16s, RaceEvidence 9s) / OK [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:48:10Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · run.py: no test matches test_selfgate [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:48:12Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · run.py: no test matches test_selfgate [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:48:26Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_exam.LeanKind` → exit 0 · Ran 143 tests in 49.5s (13 classes, 16 at a time; slowest: LeanKind 49s, LaneRecovery 22s, Lanes 17s) / OK [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:49:24Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → ✗ exit 1 · run.py: no test matches test_selfgate [ran] [tree 5b8024d6d1db] [world 2f1906870a] (2026-11-02T11:49:26Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LoadedWallCheck 0s) / OK [ran] [tree 96b53ef08f9e] [world 2f1906870a] (2026-11-02T11:50:51Z)
- (ac 1) `python3 plugin/tests/run.py test_selfgate` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: LoadedWallCheck 0s) / OK [ran] [tree 96b53ef08f9e] [world 2f1906870a] (2026-11-02T11:56:06Z)
- (audit intent) `self-review: the loaded wall branch compares p50 when both runs have it, else p95 (the existing test's data); the hook-delay mutation's metric is the 'hook ' prefix every _slower row starts with; the new test lives in test_selfgate.py; full gate passed twice under load with no flaky rerun` → a 250 ms wait doubles the median and refuses under load (test); a 20 ms median wobble doesn't; LeanKind passed three runs alone and two loaded full suites [tree 96b53ef08f9e] (2026-11-02T11:56:06Z)
- (audit edge) `self-review: the loaded wall branch compares p50 when both runs have it, else p95 (the existing test's data); the hook-delay mutation's metric is the 'hook ' prefix every _slower row starts with; the new test lives in test_selfgate.py; full gate passed twice under load with no flaky rerun` → an unloaded bench still compares CPU p95 then wall p95 as before; benches without p50 fall back to p95 [tree 96b53ef08f9e] (2026-11-02T11:56:06Z)
- (audit self) `self-review: the loaded wall branch compares p50 when both runs have it, else p95 (the existing test's data); the hook-delay mutation's metric is the 'hook ' prefix every _slower row starts with; the new test lives in test_selfgate.py; full gate passed twice under load with no flaky rerun` → no findings [tree 96b53ef08f9e] (2026-11-02T11:56:06Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-2/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 6b076d7c543a] [world 2f1906870a] (2026-11-02T11:59:33Z)
## Log
- 2026-11-02T11:11:36Z created
- 2026-11-02T11:18:37Z planned from capture
- 2026-11-02T11:28:31Z set approved=True
- 2026-11-02T11:28:31Z focused
- 2026-11-02T11:28:31Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T11:33:07Z scope: plugin/lib/fmselfgate.py and test_lanes — the flaky test's cause sits in the gate it drives, not in test_exam
- 2026-11-02T11:47:26Z scope: plugin/lib/fmexam.py — the hook-delay mutation's metric reads the row prefix, since a loaded bench now reports p50 wall
- 2026-11-02T11:56:05Z scope: plugin/tests/test_selfgate.py — the new test's own file, matching the criterion's command
- 2026-11-02T11:57:47Z done
- 2026-11-02T11:57:50Z committed 155db67d (4 files)
- 2026-11-02T11:59:33Z guard authorization added: publish
- 2026-11-02T12:10:29Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2363 [FEATURE M, done, 3 steps] #12 exam kind lean: planted growth the self-change gate must refuse; the scorecard stops borrowing kinds (Mission 8, #12) — lesson: A m…
- T-1777 [PERFORMANCE M, done, 2 steps] PreToolUse:Bash:script hook runs at about 90% of its 300 ms budget (p50 271 ms, p95 277 ms — lesson: A latency budget for a time-bo…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-22: Recommendation: keep 2 SE as the bench gate's fail line (3-5% false alarms); add an inconclusive verdict for a pass-total loss between 1 and 2 SE th…
## Why not caught
the wall check was tested only with an unloaded base p95 (40 ms), never with one load had inflated
## Lessons
- Under load, compare medians: a wait shifts every run, a spike shifts only the tail
## Plan gaps
- failed first: step 1 red unit test for _slower in test_selfgate
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmselfgate.py
- plugin/lib/fmexam.py
- plugin/tests/test_selfgate.py
- CHANGELOG.md
