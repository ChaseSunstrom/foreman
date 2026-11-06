---
id: T-1771
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmfixes.py, plugin/tests/test_fixes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T10:10:22Z
updated: 2026-10-23T10:26:09Z
base: 2dc7938a25c1b5a12a596dc99af64ef9bf7daaf4
base_tree: 39a05e33cecd370caa0e0db76ffa2736b4f5113d
plan0_at: 2026-10-23T10:24:31Z
plan0_scope: [plugin/lib/fmfixes.py, plugin/tests/test_fixes.py, CHANGELOG.md]
verified: strong
---
# Known-fix learner kept a debugging sed on a test file (print instrumentation) as the fix f
## Raw request
> Known-fix learner kept a debugging sed on a test file (print instrumentation) as the fix for a failing test run, and offered it later; an edit of the test that failed isn't a fix of what it tests
## Interpretation
The known-fix learner keeps 'a failure, then a passing command on the same thing' as a fix to offer. An Edit between them already marks the pass as a code fix, but a Bash command that writes files (sed -i, fm edit, a redirect into a file, git checkout) wasn't: a debugging sed on a test file was kept and later offered as the fix for a failing test run. A passing command that itself writes files now ends the window without learning.
## Assumptions (confidence)
## Acceptance criteria
- [x] a pass by a command that writes files teaches no fix; a pass that writes nothing (output to /dev/null) still does — verify with `python3 plugin/tests/run.py test_fixes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then _WRITES in on_success
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 17 tests in 7.2s (2 classes, 16 at a time; slowest: KnownFixes 6s, Fix 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 99bfdd1c1e93] (2026-10-23T10:24:50Z)
- `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 17 tests in 6.5s (2 classes, 16 at a time; slowest: KnownFixes 6s, Fix 0s) / FAILED (1 classes) [ran] [tree 99bfdd1c1e93] (2026-10-23T10:24:50Z)
- `python3 plugin/tests/run.py test_fixes` → ✗ exit 1 · Ran 17 tests in 7.2s (2 classes, 16 at a time; slowest: KnownFixes 6s, Fix 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9ad1784be7ab] (2026-10-23T10:25:05Z)
- `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 17 tests in 6.9s (2 classes, 16 at a time; slowest: KnownFixes 7s, Fix 0s) / OK [ran] [tree 9ad1784be7ab] (2026-10-23T10:25:05Z)
- (step 1) `python3 plugin/tests/run.py test_fixes test_hooks` → exit 0 · Ran 219 tests in 43.1s (27 classes, 16 at a time; slowest: Stop 43s, NoTaskGate 30s, PreToolUse 24s) / OK [ran] [tree 9ad1784be7ab] (2026-10-23T10:25:53Z)
- (ac 1) `python3 plugin/tests/run.py test_fixes` → exit 0 · Ran 17 tests in 8.9s (2 classes, 16 at a time; slowest: KnownFixes 9s, Fix 0s) / OK [ran] [tree 9ad1784be7ab] (2026-10-23T10:26:03Z)
- (audit edge) `self review; test_fixes and test_hooks green` → sed -i, fm edit and a redirect into a file end the window unlearned; a pass whose output goes to /dev/null or 2>&1 still teaches; an Edit between already did (tests) [tree 9ad1784be7ab] (2026-10-23T10:26:03Z)
- (audit self) `self review; test_fixes and test_hooks green` → no findings [tree 9ad1784be7ab] (2026-10-23T10:26:03Z)
## Log
- 2026-10-23T10:10:22Z created
- 2026-10-23T10:16:41Z set scope=['plugin/lib/fmfixes.py', 'plugin/tests/test_fixes.py', 'CHANGELOG.md']
- 2026-10-23T10:24:30Z focused
- 2026-10-23T10:26:06Z done
- 2026-10-23T10:26:09Z committed 430711e0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-1032-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two MEDIUM findings should be fixed befor…
- research wave1-plan-a4e57ddf98089606d: === T-1074 [stale: plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- similar past tasks were L: consider --tier L
- likely tests for the scope: plugin/tests/test_fixes.py
## Why not caught
the learner's tests covered the Edit tool between a failure and a pass, not a Bash command that edits files itself
## Files touched
- CHANGELOG.md
- plugin/lib/fmfixes.py
- plugin/tests/test_fixes.py
