---
id: T-2596
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-02T09:38:26Z
updated: 2026-11-02T09:54:25Z
base: 896cf76ce8e147f16139ea1016692b5ea7ec50a3
base_tree: 0becb41745684d9e10cce79b49316115e3d47fdc
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T09:46:23Z
plan0_scope: []
verified: strong
---
# fm task finish reruns a failed fm check --affected step by its command, not by the evidence label in front of it
## Raw request
> FIX: fm check --evidence ID --step N --affected records its command as 'fm check --affected (affected tests only): <cmd>', a label bash can't run, so fm task finish's rerun of that step fails with a syntax error (T-2587); record the runnable command
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] Brief.failed_cmd strips the 'fm check --affected (affected tests only): ' label, so finish reruns the tests themselves; the recorded evidence keeps its label (T-1747) — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a failed --affected evidence then fm task finish reruns the command (no bash syntax error)
2. [x] strip the label in fmcore Brief.failed_cmd
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 21 tests in 4.2s (10 classes, 16 at a time; slowest: FinishGaps 4s, CommitOwnFiles 4s, StepEvidence 3s) / FAILED (1 classes: test_bookkeeping.FinishGaps) [ran] [tree bab75e5eb8b1] [world 2f1906870a] (2026-11-02T09:46:36Z)
- (step 2) `python3 plugin/tests/run.py test_bookkeeping test_cli` → exit 0 · Ran 166 tests in 21.1s (54 classes, 16 at a time; slowest: TaskLifecycle 21s, CaptureAndIntake 10s, StateViews 9s) / OK [ran] [tree 1a6d56044148] [world 2f1906870a] (2026-11-02T09:47:32Z)
- `python3 plugin/tests/run.py test_bookkeeping` → ✗ exit 1 · Ran 21 tests in 4.4s (10 classes, 16 at a time; slowest: FinishGaps 3s, CommitOwnFiles 3s, StepEvidence 3s) / FAILED (1 classes: test_bookkeeping.FinishGaps) (start tree + this task's tests) [ran] [tree 0e2fb3bd69d5] [world 2f1906870a] (2026-11-02T09:53:24Z)
- `python3 plugin/tests/run.py test_bookkeeping` → exit 0 · Ran 21 tests in 3.3s (10 classes, 16 at a time; slowest: FinishGaps 3s, CommitOwnFiles 3s, StepEvidence 3s) / OK [ran] [tree 0e2fb3bd69d5] [world 2f1906870a] (2026-11-02T09:53:24Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 145 tests in 20.2s (44 classes, 16 at a time; slowest: TaskLifecycle 20s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree 0e2fb3bd69d5] [world 2f1906870a] (2026-11-02T09:53:46Z)
- (audit intent) `self-review: AFFECTED_LABEL is one constant in fmcore that fmcli writes and failed_cmd strips; the recorded evidence keeps its label (T-1747 test passes)` → failed_cmd returns the test command behind the label (test) [tree 0e2fb3bd69d5] (2026-11-02T09:53:46Z)
- (audit edge) `self-review: AFFECTED_LABEL is one constant in fmcore that fmcli writes and failed_cmd strips; the recorded evidence keeps its label (T-1747 test passes)` → a command that merely contains the label text mid-string isn't touched (startswith only); a redacted command still returns None [tree 0e2fb3bd69d5] (2026-11-02T09:53:46Z)
- (audit self) `self-review: AFFECTED_LABEL is one constant in fmcore that fmcli writes and failed_cmd strips; the recorded evidence keeps its label (T-1747 test passes)` → no findings [tree 0e2fb3bd69d5] (2026-11-02T09:53:46Z)
## Log
- 2026-11-02T09:38:26Z created
- 2026-11-02T09:40:33Z planned from capture
- 2026-11-02T09:46:22Z set approved=True
- 2026-11-02T09:46:22Z focused
- 2026-11-02T09:46:23Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T09:47:32Z scope: plugin/lib/fmcli.py — writes the label from the shared constant so the two never drift
- 2026-11-02T09:54:22Z done
- 2026-11-02T09:54:25Z committed 45cecd25 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0773 [FIX S, done, 2 steps] Evidence runs whose output reports failing tests count as failures even when a pipe hides the exit — lesson: evidence must read the run's o…
- playbook Shell script errors (bash -n, ShellCheck, bats) (fm playbooks show build/shell-build)
- research T-2369-review: Verdict: changes needed.** The core loop works: log the miss, lead in `fm next`, refuse finish and done, resolve by run evidence. But the module-…
- decision 2026-10-31: Long tier l001's foreman 0/6 is an exam defect, not a score: hidden checks need private names the goal never states (fmwatch._shown, fmlong.KILL_T) …
- the similar finished task took 2 steps
## Lessons
- A label prefixed to stored data must be one shared constant that every reader strips, or a later reader runs the label
## Plan gaps
- failed first: step 1 red test: a failed --affected evidence then fm task finish reruns the command (no bash syntax error)
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
