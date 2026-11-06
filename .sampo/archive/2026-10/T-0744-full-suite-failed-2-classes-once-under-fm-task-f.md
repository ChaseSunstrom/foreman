---
id: T-0744
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T20:32:08Z
updated: 2026-10-09T21:27:53Z
base: ccfeccd1e215396f338375d238b9a3f458d8b9ab
base_tree: 55fc0c8653bc9ca6a5683b8e774ec99ba961c4d5
verified: ok
---
# Full suite flakes under load: find and fix the timing-sensitive classes
## Raw request
> Full suite failed 2 classes once under fm task finish --run during T-0690 (Stop 69s, TaskLifecycle 45s) and passed on both reruns: find the timing-sensitive classes
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two concurrent full-suite runs both pass — verify with `python3 plugin/tests/run.py`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] reproduce under load and name the classes
2. [x] fix the timing assumption
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_suite_hygiene.py` → ✗ exit 1 · Ran 4 tests in 0.4s (2 classes, 16 at a time; slowest: UndefinedNames 0s, SuiteHygiene 0s) / FAILED (1 classes) [ran] [tree ddb70f587b80] (2026-10-09T21:21:18Z)
- (step 1) `python3 plugin/tests/run.py -p test_suite_hygiene.py -p test_shot.py -p test_ambient.py -p test_orchestration.py` → exit 0 · Ran 14 tests in 8.5s (8 classes, 16 at a time; slowest: Stall 8s, Ambient 2s, Packet 0s) / OK [ran] [tree 8dd0576f36d0] (2026-10-09T21:21:35Z)
- (step 2) `three concurrent full-suite runs` → all three OK (before the fix: 3-4 failing classes each — test_hooks.Stop, test_ambient, test_orchestration.ConflictBrief, test_shot.Harness) [tree 26fb9d7d1c1d] (2026-10-09T21:25:25Z)
- (ac 1) `python3 plugin/tests/run.py` → exit 0 · Ran 1247 tests in 63.1s (414 classes, 16 at a time; slowest: Stop 40s, TaskLifecycle 26s, Bench 22s) / OK [ran] [tree 26fb9d7d1c1d] (2026-10-09T21:26:28Z)
- (audit self) `self: root cause was environmental input, not timing — host_strain() reads the real load, so lanes and ambient runs switched off under load; tests now see a pinned calm host unless they set FOREMAN_HOST themselves (test_orchestration still does); the screenshot harness takes its own tmux socket per test run and removes it` → no findings [tree 26fb9d7d1c1d] (2026-10-09T21:26:28Z)
- `python3 plugin/tests/run.py -p test_suite_hygiene.py` → exit 0 · Ran 4 tests in 0.4s (2 classes, 16 at a time; slowest: UndefinedNames 0s, SuiteHygiene 0s) / OK (start tree + this task's tests) [ran] [tree 26fb9d7d1c1d] (2026-10-09T21:26:33Z)
- `python3 plugin/tests/run.py -p test_suite_hygiene.py` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: UndefinedNames 0s, SuiteHygiene 0s) / OK [ran] [tree 26fb9d7d1c1d] (2026-10-09T21:26:33Z)
- (step 1) `python3 plugin/tests/run.py -p test_suite_hygiene.py` → exit 0 · Ran 4 tests in 0.5s (2 classes, 16 at a time; slowest: UndefinedNames 0s, SuiteHygiene 0s) / OK [ran] [tree 26fb9d7d1c1d] (2026-10-09T21:26:39Z)
- `python3 plugin/tests/run.py` → exit 0 · Ran 1247 tests in 72.7s (414 classes, 16 at a time; slowest: Stop 46s, TaskLifecycle 28s, Recall 26s) / OK [ran] [tree 26fb9d7d1c1d] (2026-10-09T21:27:52Z)
- (audit self) `self: root cause was environmental input, not timing — host_strain() reads the real load, so lanes and ambient runs switched off under load; tests now see a pinned calm host unless they set FOREMAN_HOST themselves (test_orchestration still does); the screenshot harness takes its own tmux socket per test run and removes it` → no findings [tree 26fb9d7d1c1d] (2026-10-09T21:27:52Z)
## Log
- 2026-10-09T20:32:08Z created
- 2026-10-09T21:16:25Z planned from capture
- 2026-10-09T21:16:28Z focused
- 2026-10-09T21:27:53Z done
- 2026-10-09T21:27:53Z committed ec9c63c (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0736 [FIX S, done, 2 steps] Not-verified warning at finish fires even when the full suite ran (T-0703: fm check-free r
- T-0274 [FEATURE M, done, 3 steps] Gate and CLI friction: flake ledger in fm check, nearest-command help on fm typos — lesson: Before adding a mechanism, read how the cod…
- research T-0417-review: Changes needed. The placeholder selector and the alert rule will flag healthy apps. A permanent spinner can also make the crawl hit its timeout a…
- decision 2026-09-26: User approved (AskUserQuestion, 2026-09-26): once everything is finished and all gates pass, fast-forward main to foreman/build and push both branch…
- similar finished tasks took 2–3 steps
## Why not caught
none: the suite only ever ran on a quiet machine before the milestone closes started stacking full runs; the hygiene test now pins the calm host and the socket
## Plan gaps
- failed first: step 1 reproduce under load and name the classes
- failed first: step 2 fix the timing assumption
## Files touched
- plugin/tests/test_suite_hygiene.py
- mods/foreman-ui/tools/shot.py
- plugin/tests/helpers.py
- plugin/tests/test_shot.py
