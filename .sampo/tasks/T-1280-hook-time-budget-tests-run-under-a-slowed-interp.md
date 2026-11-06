---
id: T-1280
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: followup
created: 2026-10-20T16:55:30Z
updated: 2026-10-20T21:07:07Z
base: f82a0818571c901d67bdbcbe2e847975f6281507
base_tree: cf5e5fbaad4b5115eddc7c975425f5b9b836216a
plan0_at: 2026-10-20T20:53:11Z
plan0_scope: []
verified: strong
---
# Hook paths that start fm under a time limit are tested with every Python start slowed by 0.4 s
## Raw request
> Hook time-budget tests run under a slowed interpreter start (a sitecustomize delay), as T-1277's test does, so a budget that only fits a fast machine fails here before CI
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the hook paths that start fm as a child under a time limit — PreToolUse focusing the next queued request (3 s), the Stop hook closing this session's request (20 s) and closing the requests with evidence (25 s overall) — each have a test that runs them with every Python start slowed by 0.4 s (a sitecustomize on PYTHONPATH) and still sees the child's effect — verify with `python3 plugin/tests/run.py test_hooks`
- [x] one test helper builds the slowed-start folder and T-1277's test uses it — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: a slowed-start helper in helpers.py, then one test per path under it (red where a limit only fits a fast machine)
2. [x] Fix each limit that fails: size it from the child's measured start, or give the slow path room, keeping each hook inside Claude Code's own hook limit
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 189 tests in 54.7s (21 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 38s, PreToolUse 25s) / OK [ran] [tree a84885e3ac7c] (2026-10-20T20:54:45Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 189 tests in 54.7s (21 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 38s, PreToolUse 25s) / OK [ran] [tree a84885e3ac7c] (2026-10-20T20:54:45Z)
- (step 1) `python3 plugin/tests/run.py test_hooks 2>&1 | tail -30` → exit 0 · Ran 189 tests in 54.7s (21 classes, 16 at a time; slowest: Stop 54s, NoTaskGate 38s, PreToolUse 25s) / OK [ran] [tree a84885e3ac7c] (2026-10-20T20:54:45Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 43.0s (21 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 31s, PreToolUse 23s) / OK [ran] [tree a84885e3ac7c] (2026-10-20T20:55:33Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 94.5s (21 classes, 16 at a time; slowest: Stop 94s, NoTaskGate 67s, PreToolUse 53s) / OK [ran] [tree a84885e3ac7c] (2026-10-20T20:57:08Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 38.4s (21 classes, 16 at a time; slowest: Stop 38s, NoTaskGate 30s, PreToolUse 22s) / OK [ran] [tree a127e5e3e55b] (2026-10-20T21:03:03Z)
- (step 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 41.8s (21 classes, 16 at a time; slowest: Stop 42s, NoTaskGate 32s, PreToolUse 23s) / OK [ran] [tree a127e5e3e55b] (2026-10-20T21:03:45Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 43.8s (21 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 35s, PreToolUse 27s) / OK [ran] [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (ac 2) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 189 tests in 43.8s (21 classes, 16 at a time; slowest: Stop 44s, NoTaskGate 35s, PreToolUse 27s) / OK [ran] [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit intent) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → the three hook paths that start fm under a time limit each run with every Python start slowed and still see the child's effect [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit adversary) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → test code only; the sitecustomize lives in the test's temp folder [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit edge) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → the Stop tests use a 40 s timeout so a hang fails the assertion, not the runner; slow_start replaces PYTHONPATH [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit operator) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → CI's slow starts are now reproduced locally before a push [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit maintainer) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → one helper in helpers.py; T-1277's test uses it [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
- (audit self) `self review of a tests-only diff: three hook-path tests under a 0.4 s slowed Python start and a shared slow_start helper; no limit failed, so fmhooks.py is unchanged` → no findings [tree a127e5e3e55b] (2026-10-20T21:04:35Z)
## Log
- 2026-10-20T16:55:30Z created
- 2026-10-20T18:19:43Z planned from capture
- 2026-10-20T20:53:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1280.builder.md
- 2026-10-20T20:53:11Z focused
- 2026-10-20T21:00:52Z merged worktree-agent-ad03eee27eb93a7a9 (2 file(s))
- 2026-10-20T21:00:53Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad03eee27eb93a7a9
- 2026-10-20T21:02:20Z focused
- 2026-10-20T21:07:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1277 [FIX S, done, 2 steps] CI red on Linux 3.12: a long multi-request prompt queues only 4 of 8 tasks inside the hook's 5 s (one fm process per task) — lesson: A hook…
- T-0133 [PERFORMANCE M, done, 3 steps] Agents feel slow: parallel test runner for the gate, measured before and after — lesson: Measure the wait before optimising: one se…
- T-0805 [FIX S, done, 2 steps] The hook benchmark judges by CPU time when the machine is busy, so load alone never fails the gate — lesson: a latency gate on a shared mac…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar finished tasks took 2–3 steps
## Regression test
none: no limit failed under the 0.4 s slowed start, so there was no bug to make red; the three new tests are the guard against a future cut to those limits (each would fail if its child no longer finished in time)
## Lessons
- A time budget for a child process needs a test under a slowed interpreter start, or it only proves the budget fits the fast dev machine
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_hooks.py
- CHANGELOG.md
- plugin/skills/library/cards/jvm/android-car-app.md
- plugin/skills/library/cards/jvm/android-macrobenchmark.md
- plugin/skills/library/cards/jvm/android.md
- plugin/skills/library/cards/jvm/androidx-datastore.md
- plugin/skills/library/cards/jvm/jetpack-compose.md
