---
id: T-1845
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_diagnosis.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-28T16:50:21Z
updated: 2026-10-28T16:59:56Z
base: efe0e5525ff3f0f0b4a0c6ce985d5f8e417e73c3
base_tree: 376bfc759b8ea86e8bbd217b273732ba2b31e6b2
plan0_at: 2026-10-28T16:54:06Z
plan0_scope: []
verified: strong
---
# FIX: fm task prove names the changed non-test files it copied onto the start tree when the check passes there
## Raw request
> FIX: fm task prove copies every changed file under tests/ onto the start tree, so a change to a test runner or helper there (plugin/tests/run.py in T-1842) passes vacuously; copy only test-named files plus helpers new since base
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a vacuous prove names each changed non-test file under a tests folder it copied, and says to record the red run in the Regression test section — verify with `python3 plugin/tests/run.py -k test_diagnosis.Prove`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: prove names a copied runner
2. [x] prove verdict note
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_diagnosis.Prove` → ✗ exit 1 · Ran 2 tests in 1.7s (1 classes, 16 at a time; slowest: Prove 1s) / FAILED (1 classes) [ran] [tree a6249258409d] (2026-10-28T16:54:19Z)
- (step 1) `python3 plugin/tests/run.py -k test_diagnosis.Prove` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Prove 1s) / OK [ran] [tree ba74c10670f0] (2026-10-28T16:54:35Z)
- (step 2) `python3 plugin/tests/run.py -k test_diagnosis -k test_verification -k test_verify_strength` → exit 0 · Ran 37 tests in 18.1s (15 classes, 16 at a time; slowest: VerifyStrength 18s, Repeat 10s, Refuted 5s) / OK [ran] [tree ba74c10670f0] (2026-10-28T16:54:54Z)
- `python3 plugin/tests/run.py -k test_diagnosis.Prove` → ✗ exit 1 · Ran 2 tests in 2.7s (1 classes, 16 at a time; slowest: Prove 1s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree ba74c10670f0] (2026-10-28T16:54:59Z)
- `python3 plugin/tests/run.py -k test_diagnosis.Prove` → exit 0 · Ran 2 tests in 1.4s (1 classes, 16 at a time; slowest: Prove 1s) / OK [ran] [tree ba74c10670f0] (2026-10-28T16:54:59Z)
- (ac 1) `python3 plugin/tests/run.py -k test_diagnosis.Prove` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Prove 1s) / OK [ran] [tree 1df5f42e5ff8] (2026-10-28T16:59:30Z)
- (audit intent) `self: read the diff; the note only adds text to a not-proved verdict, exit codes unchanged` → a vacuous prove now names the runner/helper it copied (tests/run.py in T-1842) and points to the Regression test section [tree 1df5f42e5ff8] (2026-10-28T16:59:30Z)
- (audit edge) `self: read the diff; the note only adds text to a not-proved verdict, exit codes unchanged` → a new test-named file isn't listed; the note shows only when the start tree passed, at most 5 names; a proved or fails-on-current verdict is unchanged [tree 1df5f42e5ff8] (2026-10-28T16:59:30Z)
- (audit self) `self: read the diff; the note only adds text to a not-proved verdict, exit codes unchanged` → no findings [tree 1df5f42e5ff8] (2026-10-28T16:59:30Z)
## Log
- 2026-10-28T16:50:21Z created
- 2026-10-28T16:50:28Z set type=FIX, tier=S
- 2026-10-28T16:54:05Z planned from capture
- 2026-10-28T16:54:06Z focused
- 2026-10-28T16:54:07Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_diagnosis.py', 'CHANGELOG.md']
- 2026-10-28T16:59:54Z done
- 2026-10-28T16:59:56Z committed 8238edc6 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0809 [FIX S, dropped, 2 steps] fm task prove treats only test files as tests, not every file in a tests folder
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- research T-0271-review-1: Changes needed. `task_prove_hunks` can record passing evidence when nothing was proven, and mishandles files with spaces and deleted files. I r…
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
## Plan gaps
- failed first: step 1 test: prove names a copied runner
## Files touched
- plugin/tests/test_diagnosis.py
- plugin/lib/fmcli.py
- CHANGELOG.md
