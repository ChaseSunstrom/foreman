---
id: T-1139
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-16T09:43:37Z
updated: 2026-10-16T10:06:45Z
base: 828f1d3d9dfd6ced812b1f9d458ae65b7cc4510e
base_tree: 8769fdbbea7ff0d18133c39976cc06e66db438b2
plan0_at: 2026-10-16T10:02:57Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
verified: strong
---
# Fm doctor's hook-errors check reports an error from code that no longer exists (NameError
## Raw request
> fm doctor's hook-errors check reports an error from code that no longer exists (NameError BATCH_AT at 04:56Z, from a half-written edit before T-1089 landed): mark an error whose traceback line no longer matches the file as stale, or count only errors since the hook code last changed
## Interpretation
fm doctor's hook-errors check warned about 'NameError BATCH_AT' from 04:56Z, raised by a half-written edit before T-1089 landed. The code at that traceback line no longer reads that way, so the warning is stale noise.
## Assumptions (confidence)
## Acceptance criteria
- [x] a logged traceback whose plugin line no longer matches the file passes as stale; one whose line still matches warns — verify with `python3 plugin/tests/run.py test_doctor`
## Non-goals
## Approach (options → choice → why)
An error whose last traceback frame inside the plugin shows a source line that the file no longer has at that line number counts as stale. The check counts fresh errors only and mentions stale ones as 'from code changed since'. A recurring real bug stays fresh, because its line is unchanged.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then the staleness check
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k HookErrors test_doctor` → ✗ exit 1 · Ran 47 tests in 25.0s (17 classes, 16 at a time; slowest: Command 25s, ViewsRepair 17s, Checks 1s) / FAILED (1 classes) [ran] [tree ea5361499b81] (2026-10-16T10:03:31Z)
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 47 tests in 24.8s (17 classes, 16 at a time; slowest: Command 25s, ViewsRepair 17s, Checks 0s) / OK [ran] [tree 26d5465b677e] (2026-10-16T10:04:04Z)
- `python3 plugin/tests/run.py test_doctor` → ✗ exit 1 · Ran 47 tests in 36.4s (17 classes, 16 at a time; slowest: Command 36s, ViewsRepair 22s, Checks 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b46517365772] (2026-10-16T10:05:27Z)
- `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 47 tests in 30.1s (17 classes, 16 at a time; slowest: Command 30s, ViewsRepair 22s, Checks 1s) / OK [ran] [tree b46517365772] (2026-10-16T10:05:27Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 47 tests in 24.5s (17 classes, 16 at a time; slowest: Command 24s, ViewsRepair 17s, Checks 0s) / OK [ran] [tree b46517365772] (2026-10-16T10:05:52Z)
- (audit self) `self: stale only when the last plugin frame's shown source line differs from the file's line now (a live, recurring bug keeps the same line and still warns, tested); frames outside the plugin and errors with no frame count as fresh; the real doctor now passes the BATCH_AT error as stale` → no findings [tree b46517365772] (2026-10-16T10:05:52Z)
## Log
- 2026-10-16T09:43:37Z created
- 2026-10-16T10:02:57Z set scope=['plugin/lib/fmdoctor.py', 'plugin/tests/test_doctor.py', 'CHANGELOG.md']
- 2026-10-16T10:02:57Z focused
- 2026-10-16T10:04:20Z scope: CHANGELOG.md — release note
- 2026-10-16T10:06:45Z done
- 2026-10-16T10:06:45Z committed c75bfff (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- decision 2026-10-03: Self-improvement passes need N closed tasks AND 2 h since the last pass
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_doctor.py
## Lessons
- A health check about past errors should ask whether the code that raised them still exists
## Plan gaps
- failed first: step 1 Test then the staleness check
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- CHANGELOG.md
