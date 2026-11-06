---
id: T-1291
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T21:07:24Z
updated: 2026-10-20T23:58:16Z
base: 8461274b48e63f0a21929b3e68fe7acb996e6ae0
base_tree: 8c74d178776862a4a47442483c43ff5d27d66339
plan0_at: 2026-10-20T23:28:42Z
plan0_scope: []
verified: strong
---
# The guard corpus's /tmp hard-reset case means the same on macOS: it's judged with the temp folder it was labelled under, so fm night and fm replay --cases stop reporting drift there
## Raw request
> The guard corpus's '/tmp hard reset' case assumes Linux's temp layout, so fm night / fm replay --cases report it as drift on every macOS machine and capture spurious FIX tasks: store the case's folder as 'the state fallback's parent' or skip it where gettempdir() isn't /tmp
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fmreplay judges every labelled case with tempfile's folder pinned to /tmp (the corpus's labelling layout), so with TMPDIR=/var/tmp the /tmp case still blocks and drift() is empty — verify with `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test with TMPDIR=/var/tmp through fmreplay.drift
2. [x] Pin the temp folder inside fmreplay's verdicts (restored after), not only in the test
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (ac 1) `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases 2>&1 | tail -5` → exit 0 · Ran 20 tests in 7.5s (3 classes, 16 at a time; slowest: GuardCases 7s, Replay 5s, Core 0s) / OK [ran] [tree c9df27cba92d] (2026-10-20T23:29:29Z)
- (step 1) `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases 2>&1 | tail -5` → exit 0 · Ran 20 tests in 7.5s (3 classes, 16 at a time; slowest: GuardCases 7s, Replay 5s, Core 0s) / OK [ran] [tree c9df27cba92d] (2026-10-20T23:29:29Z)
- (step 1) `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 6.6s (3 classes, 16 at a time; slowest: GuardCases 6s, Replay 4s, Core 0s) / OK [ran] [tree c9df27cba92d] (2026-10-20T23:29:58Z)
- (step 2) `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 8.3s (3 classes, 16 at a time; slowest: GuardCases 8s, Replay 5s, Core 0s) / OK [ran] [tree c9df27cba92d] (2026-10-20T23:30:07Z)
- (step 1) `python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 6.1s (3 classes, 16 at a time; slowest: GuardCases 6s, Replay 4s, Core 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:54:25Z)
- (step 2) `python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 5.5s (3 classes, 16 at a time; slowest: GuardCases 5s, Replay 4s, Core 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:54:31Z)
- (ac 1) `python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 5.1s (3 classes, 16 at a time; slowest: GuardCases 5s, Replay 4s, Core 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:54:37Z)
- (ac 1) `TMPDIR=/var/tmp python3 plugin/tests/run.py test_replay test_guard_cases` → exit 0 · Ran 20 tests in 5.5s (3 classes, 16 at a time; slowest: GuardCases 5s, Replay 4s, Core 0s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit intent) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → the /tmp case judges the same on macOS [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit adversary) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → a test helper's pin, restored after; the guard itself unchanged [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit edge) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → building the guard context moved inside the try, so a failing case is an error verdict, not a crashed run [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit operator) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → fm night stops capturing spurious drift tasks on macOS [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit maintainer) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → the pin lives where verdicts are made, not in each caller [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- (audit self) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; the builder showed red with the fix stashed under TMPDIR=/var/tmp, green with it` → no findings [tree 983fb246a7c1] (2026-10-20T23:54:43Z)
- `python3 plugin/tests/run.py test_guard_cases` → ✗ exit 1 · Ran 12 tests in 6.3s (1 classes, 16 at a time; slowest: GuardCases 5s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 983fb246a7c1] (2026-10-20T23:56:33Z)
- `python3 plugin/tests/run.py test_guard_cases` → exit 0 · Ran 12 tests in 5.2s (1 classes, 16 at a time; slowest: GuardCases 5s) / OK [ran] [tree 983fb246a7c1] (2026-10-20T23:56:33Z)
- (audit intent) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → the /tmp case judges the same on macOS [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
- (audit adversary) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → a pin restored after; the guard itself unchanged [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
- (audit edge) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → building the guard context moved inside the try, so a failing case is an error verdict, not a crashed run [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
- (audit operator) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → fm night stops capturing spurious drift tasks on macOS [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
- (audit maintainer) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → the pin lives where verdicts are made, not in each caller [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
- (audit self) `self review: fmreplay.verdicts pins tempfile.tempdir to /tmp while judging (restored in finally), so drift() is the same wherever gettempdir points; proved red without, green with, under TMPDIR=/var/tmp` → no findings [tree 983fb246a7c1] (2026-10-20T23:56:40Z)
## Log
- 2026-10-20T21:07:24Z created
- 2026-10-20T23:28:18Z planned from capture
- 2026-10-20T23:28:26Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1291.builder.md
- 2026-10-20T23:28:41Z focused
- 2026-10-20T23:49:08Z merged worktree-agent-ac6133d71ad3d1706 (2 file(s))
- 2026-10-20T23:49:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac6133d71ad3d1706
- 2026-10-20T23:54:14Z focused
- 2026-10-20T23:58:16Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1162 [FEATURE M, done, 2 steps] Add `fm guard wrong "<cmd>" --should allow|block` to store a labelled case that `fm replay — lesson: a guard verdict can depend on wher…
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- T-1284 [FIX M, planned, 5 steps] macOS: fm code --worker, the guard's /tmp case, the reaper, relate and context-tax tests pass on macOS, and the job fits its time limit
- decision 2026-10-15: [revisited: Foreman Desktop releases build Linux and macOS only] Foreman Desktop releases build Linux and macOS only, no Windows (install.sh changed)
## Why not caught
none before: CI ran Linux only until the macOS leg; the test now runs with a non-/tmp temp folder
## Lessons
- A labelled corpus must be judged in the environment it was labelled in, or the labels drift by platform
## Files touched
- plugin/tests/test_guard_cases.py
- plugin/lib/fmreplay.py
- CHANGELOG.md
- plugin/lib/fmguard.py
- plugin/tests/test_guard_state_key.py
