---
id: T-1844
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_bookkeeping.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-28T16:45:54Z
updated: 2026-10-28T17:06:04Z
base: 8238edc672bb675a9eaf22c0b8e8bd67ae3101dc
base_tree: 1df5f42e5ff84bb49b7ab29c0f2eb008af6661f4
plan0_at: 2026-10-28T17:00:02Z
plan0_scope: []
verified: strong
---
# FIX: fm task finish re-runs a red step's own failed command instead of refusing
## Raw request
> fm task finish: a test-first step's deliberate red run blocks the close until re-run; accept a later passing run of the same command on another step (hit twice: T-1669, T-1841)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a step whose last run failed is re-run with that command at close and closes when it passes — verify with `python3 plugin/tests/run.py -k test_bookkeeping`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: red step re-run at close
2. [x] finish re-runs the failed command
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_bookkeeping.FinishGaps` → ✗ exit 1 · Ran 3 tests in 2.3s (1 classes, 16 at a time; slowest: FinishGaps 2s) / FAILED (1 classes) [ran] [tree 6ec7d6eed527] (2026-10-28T17:00:43Z)
- (step 1) `python3 plugin/tests/run.py -k test_bookkeeping.FinishGaps` → exit 0 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: FinishGaps 2s) / OK [ran] [tree ffbfdeed4d75] (2026-10-28T17:01:22Z)
- (step 2) `python3 plugin/tests/run.py -k test_bookkeeping -k test_close_gates -k test_diagnosis` → exit 0 · Ran 45 tests in 14.7s (16 classes, 16 at a time; slowest: CloseGates 14s, Refuted 4s, StepEvidence 4s) / OK [ran] [tree ffbfdeed4d75] (2026-10-28T17:01:37Z)
- `python3 plugin/tests/run.py -k test_bookkeeping.FinishGaps` → ✗ exit 1 · Ran 3 tests in 3.0s (1 classes, 16 at a time; slowest: FinishGaps 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 1b10e9919e93] (2026-10-28T17:01:47Z)
- `python3 plugin/tests/run.py -k test_bookkeeping.FinishGaps` → exit 0 · Ran 3 tests in 2.5s (1 classes, 16 at a time; slowest: FinishGaps 2s) / OK [ran] [tree 1b10e9919e93] (2026-10-28T17:01:47Z)
- (ac 1) `python3 plugin/tests/run.py -k test_bookkeeping` → exit 0 · Ran 17 tests in 3.3s (8 classes, 16 at a time; slowest: StepEvidence 3s, CommitOwnFiles 3s, FinishGaps 2s) / OK [ran] [tree 552ba8122bd0] (2026-10-28T17:05:38Z)
- (audit intent) `self: read the diff; the close re-runs only a command fm itself ran and stored for that step, through guard_stored like every stored verify` → a test-first step's red run no longer refuses the close; finish re-runs that command and closes it on a pass (T-1669, T-1841 hit this) [tree 552ba8122bd0] (2026-10-28T17:05:38Z)
- (audit adversary) `self: read the diff; the close re-runs only a command fm itself ran and stored for that step, through guard_stored like every stored verify` → a re-run is guard_stored first (T-0901); a stored command with a redacted secret isn't re-run, it keeps the old gap [tree 552ba8122bd0] (2026-10-28T17:05:38Z)
- (audit edge) `self: read the diff; the close re-runs only a command fm itself ran and stored for that step, through guard_stored like every stored verify` → still red at close fails with the run's output; --run still wins over the stored command; a step with no evidence keeps the old message [tree 552ba8122bd0] (2026-10-28T17:05:38Z)
- (audit self) `self: read the diff; the close re-runs only a command fm itself ran and stored for that step, through guard_stored like every stored verify` → no findings [tree 552ba8122bd0] (2026-10-28T17:05:38Z)
## Log
- 2026-10-28T16:45:54Z created
- 2026-10-28T17:00:02Z planned from capture
- 2026-10-28T17:00:02Z focused
- 2026-10-28T17:00:03Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_bookkeeping.py', 'CHANGELOG.md']
- 2026-10-28T17:06:03Z done
- 2026-10-28T17:06:04Z committed b4caa04f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0870 [FEATURE M, done, 2 steps] fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, …
- T-0165 [FEATURE S, done, 3 steps] A step whose newest run failed closes when the same command passed later (the red run of red→green) — lesson: Evidence rules should fol…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-09: T-0476 quarantine skipped: fm check keeps treating a gate flaky 2+ times as failing
- similar finished tasks took 2–5 steps
## Plan gaps
- failed first: step 1 test: red step re-run at close
## Files touched
- plugin/tests/test_bookkeeping.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
