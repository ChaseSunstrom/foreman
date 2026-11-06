---
id: T-1004
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T00:53:04Z
updated: 2026-10-16T01:07:11Z
base: 32d6e2ac8091849e7f71e62b8ac4de2f86f8940b
base_tree: d0ae48532fa70580c0408ffb4cfc325d0bbe01ac
verified: strong
---
# A one-off session records no evidence on another session's task
## Raw request
> One-off sessions (FOREMAN_ONEOFF=1, e.g. the shot.py harness) auto-record evidence onto another session's focused task: a Haiku harness ran python3 plugin/tests/run.py test_ui and it closed T-1002 step 3 (2026-10-16T00:52Z). A one-off session should record nothing on tasks it doesn't own.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a passing Bash run of the task's verify command in a FOREMAN_ONEOFF=1 session records no evidence; the same run in the working session still does — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: PostToolUse from a FOREMAN_ONEOFF=1 session records evidence on the active task
2. [x] post_tool_use skips _auto_evidence/_runner_evidence when _oneoff()
3. [x] docs: CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 12 tests in 2.1s (8 classes, 16 at a time; slowest: CommitOwnFiles 2s, StepEvidence 2s, CommitAfterFocus 2s) / FAILED (1 classes) [ran] [tree f4abb2727f1e] (2026-10-16T01:03:05Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping test_hooks` → ✗ exit 1 · Ran 165 tests in 35.4s (28 classes, 16 at a time; slowest: Stop 35s, PreToolUse 20s, SessionStart 16s) / FAILED (1 classes) [ran] [tree 3ab67b3f81b2] (2026-10-16T01:03:51Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping test_hooks` → exit 0 · Ran 165 tests in 32.8s (28 classes, 16 at a time; slowest: Stop 33s, PreToolUse 18s, SessionStart 14s) / OK [ran] [tree 0bfcd5ccedb7] (2026-10-16T01:05:23Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 12 tests in 3.2s (8 classes, 16 at a time; slowest: CommitOwnFiles 3s, StepEvidence 3s, CommitAfterFocus 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 0bfcd5ccedb7] (2026-10-16T01:05:35Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 12 tests in 4.4s (8 classes, 16 at a time; slowest: StepEvidence 4s, CommitOwnFiles 4s, CommitAfterFocus 4s) / OK [ran] [tree 0bfcd5ccedb7] (2026-10-16T01:05:35Z)
- (step 3) `grep -q 'T-1004' CHANGELOG.md` → exit 0 · (no output) [ran] [tree 3c7c1f723dec] (2026-10-16T01:05:41Z)
- (ac 1) `python3 plugin/tests/run.py test_bookkeeping test_hooks` → exit 0 · Ran 165 tests in 48.3s (28 classes, 16 at a time; slowest: Stop 48s, PreToolUse 33s, SessionStart 27s) / OK [ran] [tree 3c7c1f723dec] (2026-10-16T01:06:30Z)
- (audit edge) `self` → claude -p without FOREMAN_DRIVE_TASK is a one-off too (intended: it answers a prompt); fm run (DRIVE_TASK set) and bench (FOREMAN_BENCH) still record; tests can no longer inherit a one-off env [tree 3c7c1f723dec] (2026-10-16T01:06:30Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 153 tests in 34.7s (20 classes, 16 at a time; slowest: Stop 35s, PreToolUse 19s, Approvals 15s) / OK [ran] [tree 3c7c1f723dec] (2026-10-16T01:07:09Z)
- (audit edge) `red→green proved by fm task prove; hooks and bookkeeping suites green` → fm run and bench sessions still record; a headless claude -p no longer does [tree 3c7c1f723dec] (2026-10-16T01:07:09Z)
- (audit self) `red→green proved by fm task prove; hooks and bookkeeping suites green` → no findings [tree 3c7c1f723dec] (2026-10-16T01:07:09Z)
## Log
- 2026-10-16T00:53:04Z created
- 2026-10-16T00:54:17Z root cause: fmhooks.post_tool_use → _auto_evidence/_runner_evidence record onto c.active_brief() for any session in the project; a one-off session (_oneoff()) owns no task. Fix: skip both when _oneoff(); consider the lease holder for two interactive sessions
- 2026-10-16T00:55:04Z planned from capture
- 2026-10-16T00:56:29Z plan (grounded): fmhooks.post_tool_use line ~1797 'if p and tool == "Bash"' → add 'and not _oneoff()'; _oneoff() also covers claude -p without FOREMAN_DRIVE_TASK (intended: a one-off owns no task). helpers.setUp must also pop FOREMAN_ONEOFF, CLAUDE_CODE_ENTRYPOINT and FOREMAN_DRIVE_TASK (restore in tearDown) so a suite run from a one-off or headless session (the harness ran test_ui) behaves the same; red test in test_bookkeeping.py beside the T-0704 auto-evidence tests: same verify run with env FOREMAN_ONEOFF=1 records nothing
- 2026-10-16T01:02:53Z focused
- 2026-10-16T01:07:10Z done
- 2026-10-16T01:07:11Z committed 07c967e (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0978-small-models: Measured, not guessed. Sources: two recorded Sonnet demo sessions (T-0979; T-0983/T-0984 were written by them), one
- T-0775 [FIX S, done, 2 steps] One-off headless claude -p sessions answer their prompt and stop; they never drive the queue — lesson: a headless session Foreman didn't st…
- T-0994 [FIX M, done, 3 steps] Ambient runs close only the step whose own verify ran; unmappable files get no ambient evidence (T-0994) — lesson: Automatic evidence must …
- decision 2026-09-26: T-0014 fm run: minimal one-shot worker (fresh claude -p per task, drive scoped to that task via FOREMAN_DRIVE_TASK, per-task timeout, stop on no pro…
- similar finished tasks took 2–3 steps
## Why not caught
T-0995 made one-off sessions skip the drive and the fleet but no test ran a one-off session's Bash through PostToolUse
## Plan gaps
- failed first: step 1 red test: PostToolUse from a FOREMAN_ONEOFF=1 session records evidence on the active task
- failed first: step 2 post_tool_use skips _auto_evidence/_runner_evidence when _oneoff()
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmhooks.py
- plugin/tests/helpers.py
- CHANGELOG.md
