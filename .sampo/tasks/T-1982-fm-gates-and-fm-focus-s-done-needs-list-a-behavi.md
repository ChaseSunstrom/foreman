---
id: T-1982
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T12:26:14Z
updated: 2026-10-29T12:57:09Z
base: a359778137806186a335be4a6d6072a1242ad3a6
base_tree: 05fc7fc5627e74909828647e9ec751d1086bd387
plan0_at: 2026-10-29T12:51:09Z
plan0_scope: []
verified: strong
---
# fm gates says a CLEAN task that edits no project file needs no behaviour lock
## Raw request
> FIX: fm gates and fm focus's 'Done needs' list a behaviour lock for a CLEAN task that edits no project file (a ship task), though fm task finish no longer asks for one there since T-1979; say 'before the first project-file edit (none when it edits none)'
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm gates clean s says the lock is only for a task that edits project files — verify with `python3 plugin/tests/run.py test_speed`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test-first: fm gates clean s names 'none when it edits no project file'; reword the CLEAN line
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 4.1s (1 classes, 16 at a time; slowest: Speed 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 63cc39aa4619] (2026-10-29T12:51:43Z)
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 3.3s (1 classes, 16 at a time; slowest: Speed 3s) / FAILED (1 classes) [ran] [tree 63cc39aa4619] (2026-10-29T12:51:43Z)
- `python3 plugin/tests/run.py test_speed` → ✗ exit 1 · Ran 10 tests in 5.9s (1 classes, 16 at a time; slowest: Speed 4s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8d1ff7853df1] (2026-10-29T12:51:58Z)
- `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 3.6s (1 classes, 16 at a time; slowest: Speed 3s) / OK [ran] [tree 8d1ff7853df1] (2026-10-29T12:51:58Z)
- (step 1) `python3 plugin/tests/run.py test_speed test_verify_strength` → exit 0 · Ran 28 tests in 15.3s (3 classes, 16 at a time; slowest: VerifyStrength 15s, Repeat 8s, Speed 3s) / OK [ran] [tree 6ad45df6e5d8] (2026-10-29T12:52:20Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    41.5     150  [0] / SessionEnd                  35.3    37.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree 6ad45df6e5d8] (2026-10-29T12:56:31Z)
- (ac 1) `python3 plugin/tests/run.py test_speed` → exit 0 · Ran 10 tests in 3.4s (1 classes, 16 at a time; slowest: Speed 3s) / OK [ran] [tree 6ad45df6e5d8] (2026-10-29T12:56:41Z)
- (audit self) `self: wording only; label unchanged so fm focus's Done needs line and its test still match; MASTER 446 updated` → no findings [tree 6ad45df6e5d8] (2026-10-29T12:56:41Z)
## Log
- 2026-10-29T12:26:14Z created
- 2026-10-29T12:51:08Z planned from capture
- 2026-10-29T12:51:08Z focused
- 2026-10-29T12:57:07Z done
- 2026-10-29T12:57:09Z committed 2abd17ce (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1980 [FIX M, done, 4 steps] Batch keeps DONE-WHEN verify, gates name why-not-caught, fm ship marks its test run, first_touch keeps project files — lesson: A marker tha…
- T-1731 [FIX M, done, 4 steps] Lane and close friction: finish --commit and shared files, CLEAN behaviour-lock in builder briefs, check --affected ski… — lesson: Skip a t…
- T-1979 [FIX M, done, 0 steps] C.first_touch counts a Write outside the project (a scratchpad file) as the task's first e
- decision 2026-10-23: Gates behind volt's 2-hour cargo test lock: stop our own queued fm check runs and land the drafted tasks first, then one gate covers all of them bef…
- similar past tasks were M: consider --tier M
## Files touched
- plugin/tests/test_speed.py
- plugin/lib/fmcli.py
- MASTER.md
