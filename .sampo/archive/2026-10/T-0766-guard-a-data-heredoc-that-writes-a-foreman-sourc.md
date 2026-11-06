---
id: T-0766
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: self
created: 2026-10-14T15:41:03Z
updated: 2026-10-14T15:41:18Z
base: 4a9bf49a329a62d797e24dacdb67306687aa8570
base_tree: ae935b2e97c8cfc8363470286d82b9391bda8f87
verified: strong
---
# Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
## Raw request
> Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
## Interpretation
Recreates T-0761 (its verify named pytest, not installed). cat >> plugin/lib/fmX.py <<'EOF' naming fmcore's writers beside a test run was blocked as core 'interpreter code driving Foreman's modules', which a standing core yes can't cover (6x since 10-09). Running or importing what was written must still block.
## Assumptions (confidence)
## Acceptance criteria
- [x] a heredoc writing a core source file beside a test run isn't 'driving'; run/imported/scratch/unquoted forms still are — verify with `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in InterpreterWrites
2. [x] _drives_fm skips data heredoc bodies that write an unnamed-again core source file
## Resume here
## Docs impact
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → ✗ exit 1 · Ran 1 test in 0.018s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ae935b2e97c8] (2026-10-14T15:41:08Z)
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 test in 0.023s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:41:08Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 test in 0.023s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:41:08Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff 2>&1 | tail -3` → exit 0 · Ran 83 tests in 5.235s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:41:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 8 tests in 0.108s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:41:14Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 8 tests in 0.109s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:41:18Z)
- (audit adversary) `self: diff read end to end; only drops a body when the line is a single-target cat/tee with a quoted delimiter into a real (symlink-resolved) core dir and the file's stem appears nowhere else; every other form keeps the old text match` → run-by-path, import-by-name, scratch target, unquoted delimiter all still block (tests); tee to two targets and cat <<'EOF' > path don't match the strict regex so stay blocked; symlink from plugin/lib to scratch resolved by realpath [tree ae935b2e97c8] (2026-10-14T15:41:18Z)
- (audit edge) `self: diff read end to end; only drops a body when the line is a single-target cat/tee with a quoted delimiter into a real (symlink-resolved) core dir and the file's stem appears nowhere else; every other form keeps the old text match` → relative path from cwd resolved via _resolve; a stem named only inside another data body still counts once (bodies dropped before counting) [tree ae935b2e97c8] (2026-10-14T15:41:18Z)
- (audit self) `self: diff read end to end; only drops a body when the line is a single-target cat/tee with a quoted delimiter into a real (symlink-resolved) core dir and the file's stem appears nowhere else; every other form keeps the old text match` → no findings [tree ae935b2e97c8] (2026-10-14T15:41:18Z)
## Log
- 2026-10-14T15:41:03Z created
- 2026-10-14T15:41:03Z focused
- 2026-10-14T15:41:18Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0761 [FIX S, dropped, 2 steps] Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research rsi-20261004-recon: 1. **Answer.** Four of the five findings are in the guard and the friction digest. The guard blocks most often on a heredoc that only writes…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- likely tests for the scope: plugin/tests/test_guard.py
## Lessons
- a guard relaxation keyed on what a heredoc writes must check the target is never run or imported by name in the same command, and resolve symlinks before trusting the path
