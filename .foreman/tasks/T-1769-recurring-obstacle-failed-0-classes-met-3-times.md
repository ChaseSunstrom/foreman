---
id: T-1769
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/tests/test_recall.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-23T09:30:43Z
updated: 2026-10-23T09:55:36Z
base: 49e1fe713af2c509edf5b49d0d54e58388a54165
base_tree: bb646f5707cfaa167f5a1ce6adbe19b48f02a582
plan0_at: 2026-10-23T09:54:27Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/tests/test_recall.py, CHANGELOG.md]
verified: strong
---
# A test runner's tally became the failure signature, so red-first runs read as a recurring obstacle
## Raw request
> Recurring obstacle: failed (0 classes) (met 3 times, no known fix): remove its cause, or teach the fix with fm fix add
## Interpretation
failure_signature picks the last line naming an error; for a test run that is the runner's own tally (FAILED (1 classes), FAILED (failures=2), pytest's summary, fm quiet's ✗ exit line), which every red run shares. Three red-first runs in a session then escalated as one 'recurring obstacle' (T-1769 itself). Tally lines are skipped when picking the telling line; a failure with nothing but a tally has no signature.
## Assumptions (confidence)
## Acceptance criteria
- [x] a test failure's signature is its own error line, and a bare tally has none — verify with `python3 plugin/tests/run.py test_recall test_fixes`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then _TALLY_LINE in failure_signature
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_recall.Tally` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Tally 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8cf7437ce3d5] (2026-10-23T09:54:35Z)
- `python3 plugin/tests/run.py test_recall.Tally` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Tally 0s) / FAILED (1 classes) [ran] [tree 8cf7437ce3d5] (2026-10-23T09:54:35Z)
- `python3 plugin/tests/run.py test_recall.Tally` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Tally 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree c99fbb825cdc] (2026-10-23T09:54:37Z)
- `python3 plugin/tests/run.py test_recall.Tally` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Tally 0s) / OK [ran] [tree c99fbb825cdc] (2026-10-23T09:54:37Z)
- (step 1) `python3 plugin/tests/run.py test_recall test_fixes` → exit 0 · Ran 38 tests in 16.0s (10 classes, 16 at a time; slowest: Recall 16s, KnownFixes 6s, OtherProjects 6s) / OK [ran] [tree c99fbb825cdc] (2026-10-23T09:54:59Z)
- (ac 1) `python3 plugin/tests/run.py test_recall test_fixes` → exit 0 · Ran 38 tests in 16.1s (10 classes, 16 at a time; slowest: Recall 16s, KnownFixes 6s, OtherProjects 6s) / OK [ran] [tree c99fbb825cdc] (2026-10-23T09:55:15Z)
- (audit edge) `self review; test_recall and test_fixes green` → a run whose output has a real error line keeps that as its signature (AssertionError, ModuleNotFoundError); a bare tally (unittest, run.py, pytest, fm quiet's ✗ line) has none, so it neither escalates nor offers a wrong fix (test) [tree c99fbb825cdc] (2026-10-23T09:55:15Z)
- (audit self) `self review; test_recall and test_fixes green` → no findings [tree c99fbb825cdc] (2026-10-23T09:55:15Z)
## Log
- 2026-10-23T09:30:43Z created
- 2026-10-23T09:53:57Z set tier=S, title=A test runner's tally became the failure signature, so red-first runs read as a recurring obstacle, scope=['plugin/lib/fmrecall.py', 'plugin/tests/test_recall.py', 'CHANGELOG.md']
- 2026-10-23T09:54:27Z focused
- 2026-10-23T09:55:34Z done
- 2026-10-23T09:55:36Z committed 54ea9252 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1032 [FEATURE L, done, 6 steps] Learn a fix once, apply it every time: when a session hits an obstacle and resolves it (e. — lesson: Never name a unittest helper fail(…
- research T-1032-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict:** changes needed. Two MEDIUM findings should be fixed befor…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
- likely tests for the scope: plugin/tests/test_recall.py
## Why not caught
the signature tests used single error lines; none fed a whole test run whose last error-sounding line is the runner's tally
## Files touched
- CHANGELOG.md
- plugin/lib/fmrecall.py
- plugin/tests/test_recall.py
