---
id: T-3240
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_progress.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T20:34:00Z
updated: 2026-11-05T20:52:40Z
base: 4933fd85b33b1241dd661773682d633924e4bfd0
base_tree: c754e9f1885bd83521d5f880f36178a2420d22d7
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T20:51:57Z
plan0_scope: [plugin/tests/test_progress.py, CHANGELOG.md]
verified: strong
---
# CI macOS:…
## Raw request
> CI macOS: test_progress.Progress.test_a_real_process_writes_its_file_and_is_read_with_its_real_start fails on macos-latest 3.14 (run 42086502367; the process-start read is likely /proc-only): make it portable or skip off Linux
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the real-process progress test skips where there is no /proc (macOS), and runs on Linux — verify with `python3 plugin/tests/run.py test_progress`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] skipUnless /proc on the real-process test
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_progress` → exit 0 · Ran 15 tests in 1.0s (2 jobs, 16 at a time; slowest: Progress 1s, Progress 0s) / OK [ran] [tree 76cf661b9f26] [world 2f1906870a] (2026-11-05T20:52:10Z)
- (ac 1) `python3 plugin/tests/run.py test_progress` → exit 0 · Ran 15 tests in 1.1s (2 jobs, 16 at a time; slowest: Progress 1s, Progress 0s) / OK [ran] [tree c89f9cf83eff] [world 2f1906870a] (2026-11-05T20:52:20Z)
- (audit intent) `self: live._started and _ticks read /proc, so off Linux they return None by design; the test now skips where /proc/self/stat doesn't exist and still runs on Linux` → macOS CI no longer fails a Linux-only reader [tree c89f9cf83eff] (2026-11-05T20:52:20Z)
- (audit edge) `self: live._started and _ticks read /proc, so off Linux they return None by design; the test now skips where /proc/self/stat doesn't exist and still runs on Linux` → Linux keeps the real-process check [tree c89f9cf83eff] (2026-11-05T20:52:20Z)
- (audit self) `self: live._started and _ticks read /proc, so off Linux they return None by design; the test now skips where /proc/self/stat doesn't exist and still runs on Linux` → no findings [tree c89f9cf83eff] (2026-11-05T20:52:20Z)
## Log
- 2026-11-05T20:34:00Z created
- 2026-11-05T20:51:55Z planned: it has criteria and steps
- 2026-11-05T20:51:56Z set scope=['plugin/tests/test_progress.py', 'CHANGELOG.md']
- 2026-11-05T20:51:56Z focused
- 2026-11-05T20:51:57Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T20:52:38Z done
- 2026-11-05T20:52:40Z committed 040f45d3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1828 [FIX M, done, 2 steps] FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_c — lesson: macOS ptys drop unread output when the…
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- research T-1284-review: Verdict:** approve with nits. I found no way to make the guard treat an outside write as inside a project, or a project or state write as outside…
- decision 2026-10-15: [revisited: Foreman Desktop releases build Linux and macOS only] Foreman Desktop releases build Linux and macOS only, no Windows (install.sh changed)
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx
## Regression test
none: the failure is macOS-only (no /proc); on Linux the test runs and passes as before (15 tests), and on macOS it now skips by its reason
## Why not caught
only CI runs macOS; nothing local fakes a missing /proc
## Lessons
- a test of a /proc reader needs the same platform guard as the reader
## Files touched
- plugin/tests/test_progress.py
- CHANGELOG.md
