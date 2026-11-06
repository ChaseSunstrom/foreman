---
id: T-2543
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-02T05:28:17Z
updated: 2026-11-02T05:50:21Z
base: 495a7d58488beaadf03463ee0b327cbb84439def
base_tree: 55119335ce5b5888020777b03ef66a66319bead7
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T05:28:41Z
plan0_scope: [plugin/lib/fmexam.py, plugin/tests/test_exam.py, CHANGELOG.md]
verified: strong
---
# fmexam._tool_out retries an exec that fails with ETXTBSY (a file another thread's fork still holds open) instead of failing the clean render
## Raw request
> Flaky: test_exam.ExamPython.test_planted_fails_hidden_checks_and_clean_passes failed once under the full gate ('tool-build-python-…: tool-build check fails on the clean render') and passed on rerun (T-2542's gate). fmexam._tool_out returns None on any OSError or a 20 s timeout: likeliest ETXTBSY (exec of a file a parallel thread's fork still holds open, _pool runs 8 threads) or load; record why it failed, and retry an ETXTBSY exec once
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] _tool_out returns the tool's output when the first exec raises OSError ETXTBSY and the second succeeds; any other OSError or a timeout still returns None — verify with `python3 plugin/tests/run.py test_exam`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: subprocess.run mocked to raise OSError(errno.ETXTBSY) once, then return the output: _tool_out gives the output; ENOENT still gives None
2. [x] fmexam._tool_out retries an ETXTBSY exec up to 3 times, a short sleep apart
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_exam.ProofKinds.test_a_busy_tool_file_is_retried_not_read_as_a_failed_tool` → ✗ exit 1 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: ProofKinds 0s) / FAILED (1 classes: test_exam.ProofKinds) [ran] [tree 46651088bf5e] [world 2f1906870a] (2026-11-02T05:28:59Z)
- (step 2) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 94 tests in 99.1s (23 classes, 16 at a time; slowest: LeanKind 98s, ExamAuthors 85s, JudgmentKinds 77s) / OK [ran] [tree d322052b7d75] [world 2f1906870a] (2026-11-02T05:30:57Z)
- `python3 plugin/tests/run.py test_exam.ProofKinds.test_a_busy_tool_file_is_retried_not_read_as_a_failed_tool` → ✗ exit 1 · Ran 1 tests in 9.7s (1 classes, 16 at a time; slowest: ProofKinds 1s) / FAILED (1 classes: test_exam.ProofKinds) (start tree + this task's tests) [ran] [tree d322052b7d75] [world 2f1906870a] (2026-11-02T05:31:19Z)
- `python3 plugin/tests/run.py test_exam.ProofKinds.test_a_busy_tool_file_is_retried_not_read_as_a_failed_tool` → exit 0 · Ran 1 tests in 2.0s (1 classes, 16 at a time; slowest: ProofKinds 1s) / OK [ran] [tree d322052b7d75] [world 2f1906870a] (2026-11-02T05:31:19Z)
- (ac 1) `python3 plugin/tests/run.py test_exam` → exit 0 · Ran 94 tests in 84.1s (23 classes, 16 at a time; slowest: LeanKind 84s, ExamAuthors 77s, JudgmentKinds 72s) / OK [ran] [tree 0bae73d09793] [world 2f1906870a] (2026-11-02T05:41:10Z)
- (audit edge) `self-review: only errno ETXTBSY retries (3 tries, 0.2 s apart); other OSErrors and timeouts still return None, so a broken tool still fails` → a tool that is busy on all three tries returns None as before; a missing tool (ENOENT) is not retried; the sleep only happens on a busy exec [tree 0bae73d09793] (2026-11-02T05:41:10Z)
- (audit self) `self-review: only errno ETXTBSY retries (3 tries, 0.2 s apart); other OSErrors and timeouts still return None, so a broken tool still fails` → no findings [tree 0bae73d09793] (2026-11-02T05:41:10Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 0bae73d09793] [world 2f1906870a] (2026-11-02T05:43:45Z)
## Log
- 2026-11-02T05:28:17Z created
- 2026-11-02T05:28:40Z planned from capture
- 2026-11-02T05:28:40Z focused
- 2026-11-02T05:28:41Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T05:31:29Z scope: fmexam._tool_out retries an ETXTBSY exec (3 tries, 0.2 s apart); any other OSError or a timeout is still None; test in test_exam.ProofKinds
- 2026-11-02T05:42:55Z done
- 2026-11-02T05:42:57Z committed b51f41f1 (3 files)
- 2026-11-02T05:43:51Z guard authorization added: publish
- 2026-11-02T05:50:21Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2334 [FIX M, done, 2 steps] A task always gets a start point: a git timeout at focus or at finish is retried, never read as no start commit — lesson: A timeout is not …
- research T-2120-review: Verdict:** changes needed. One MEDIUM finding: the exam-defect proof can be satisfied without any exam defect. [stale: plugin/lib/fmexam.py, plug…
- research T-2149-review: Verdict: approve with nits.** I found no defect that breaks the acceptance criteria. I did not run the tests or the `python3 plugin/tests/run.py …
- decision 2026-10-31: [revisited: Parallel Missions 5-8] [check: python3 plugin/tests/run.py test_lanes] Parallel Missions 5-8 still holds: an L stays in the main thread,…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_exam.py
## Why not caught
_tool_out folded every OSError and timeout into None, so a transient ETXTBSY from the 8-thread grading pool read as a broken tool; it surfaced only under the full gate's load, and the gate's flaky-rerun note was the first record of it.
## Lessons
- a grader that folds every OSError into 'the tool failed' turns a transient OS race into a wrong score; retry the one transient errno and keep the rest strict
## Plan gaps
- failed first: step 1 red test: subprocess.run mocked to raise OSError(errno.ETXTBSY) once, then return the output: _tool…
## Files touched
- plugin/tests/test_exam.py
- plugin/lib/fmexam.py
- CHANGELOG.md
