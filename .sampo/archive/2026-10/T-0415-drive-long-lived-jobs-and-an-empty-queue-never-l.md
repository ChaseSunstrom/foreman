---
id: T-0415
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T13:18:07Z
updated: 2026-10-09T13:20:59Z
base: 7cf9ed8e3158def25961bd3e9e49d9251c68bde3
base_tree: 791b2b8d2ed6b18eb700369edf697647f9107f6e
verified: strong
---
# Drive: long-lived jobs and an empty queue never leave a session idle
## Raw request
> Drive: long-lived jobs and an empty queue never leave a session idle
## Interpretation
The user, watching JARVIS: "it has been sitting idle still again, stop letting it sit idle for how long it has been". JARVIS waited 10–46 min at a time from 09:34 to 12:52: the engine listed two jobs that ran for hours (sqc4hknpy, swpfwthjr: a workflow and a shell, never finishing), so every Stop took the running branch, which pushes once per job set and offers only other queued tasks; its queue had nothing else, so each turn ended to wait on a CI pipeline. A job that has run for long is a service, not something to wait for, and an empty queue in full autonomy is a reason to find work, not to wait.
## Assumptions (confidence)
## Acceptance criteria
- [x] a job running 20+ min no longer holds the drive; with no active task the next one is pushed though jobs run; with nothing queued in full autonomy the wait push says to check the product end to end and capture — verify with `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle`
## Non-goals
## Approach (options → choice → why)
(A, chosen) three changes in fmhooks._drive: (1) a job first seen running more than 20 min ago no longer holds the drive (first-seen per id kept in the drive state), (2) with no active task, running jobs don't hold the drive: the next queued task is pushed as usual, (3) in full autonomy, when nothing else is queued, the push while jobs run says to check the product end to end as the user uses it and capture each defect, then work the first. (B, rejected) drop OFFERS_MAX: offers were not the gap (nothing to offer). (C, rejected) ignore every background job: a fresh gate run is worth waiting on.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first: long-lived job, no active task, empty queue rows
2. [x] drive: first-seen age, no-active pass-through, product-check push
3. [x] gate, changelog, ship to JARVIS
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 218bc6d64854] (2026-10-09T13:19:26Z)
- (step 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 218bc6d64854] (2026-10-09T13:19:26Z)
- (step 2) `python3 plugin/tests/run.py -p test_hooks.py` → exit 0 · Ran 129 tests in 17.9s (18 classes, 16 at a time; slowest: Stop 18s, Approvals 10s, SessionStart 9s) / OK [ran] [tree 218bc6d64854] (2026-10-09T13:19:44Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                31.7    32.6     150  [0] / SessionEnd                  29.2    31.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 13:13 UTC; python3 plugin/tests/run.py → exit 0 · Ran 954 tests in [ran] [tree 218bc6d64854] (2026-10-09T13:20:51Z)
- (ac 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 218bc6d64854] (2026-10-09T13:20:59Z)
- (audit intent) `self: diff read; the three changes are each pinned by the test (no-active push, empty-queue product check, 20-min job ages out); hooks suite and full gate pass` → JARVIS's pattern (two hours-long jobs + empty queue + CI wait) now gets a work push every time instead of a wait [tree 218bc6d64854] (2026-10-09T13:20:59Z)
- (audit edge) `self: diff read; the three changes are each pinned by the test (no-active push, empty-queue product check, 20-min job ages out); hooks suite and full gate pass` → a fresh job still holds the drive once per set as before; a job aged out just drops from the set; since{} keeps only ids still running; a 25-min CI run now lets the step push through, bounded by DRIVE_MAX and the no-progress stop [tree 218bc6d64854] (2026-10-09T13:20:59Z)
- (audit adversary) `self: diff read; the three changes are each pinned by the test (no-active push, empty-queue product check, 20-min job ages out); hooks suite and full gate pass` → no new input is trusted; ids come from the engine's list or Foreman's own events [tree 218bc6d64854] (2026-10-09T13:20:59Z)
- (audit operator) `self: diff read; the three changes are each pinned by the test (no-active push, empty-queue product check, 20-min job ages out); hooks suite and full gate pass` → no setting; the drive's messages say why [tree 218bc6d64854] (2026-10-09T13:20:59Z)
- (audit maintainer) `self: diff read; the three changes are each pinned by the test (no-active push, empty-queue product check, 20-min job ages out); hooks suite and full gate pass` → one constant, four lines in _drive, one message branch [tree 218bc6d64854] (2026-10-09T13:20:59Z)
## Log
- 2026-10-09T13:18:07Z created
- 2026-10-09T13:18:07Z focused
- 2026-10-09T13:20:59Z done
- 2026-10-09T13:20:59Z committed 888a100 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- decision 2026-10-08: T-0364 plan: once-per-running-set parallel push; widen detectors; capability-map + approaches lenses; subagent triggers
- similar finished tasks took 3–5 steps
## Lessons
- A wait rule keyed on 'anything running' breaks when something always runs: age the jobs, and make an empty queue a reason to find work.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
