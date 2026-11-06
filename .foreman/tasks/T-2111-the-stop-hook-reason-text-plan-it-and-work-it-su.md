---
id: T-2111
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_scout.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-30T06:36:03Z
updated: 2026-10-30T13:19:57Z
base: 8bfb9341269c41c1708c15e4038356f0c917cbd6
base_tree: f45b25883a9aa7f68f9b3c5118b91ad4c5101c1d
plan0_at: 2026-10-30T13:16:48Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_scout.py, CHANGELOG.md]
verified: strong
---
# The Stop-hook reason text "Plan it and work it" suits ordinary tasks, not confirm items
## Raw request
> the Stop-hook reason text "Plan it and work it" suits ordinary tasks, not confirm items
> (noticed by an agent; research T-2105-review)
## Interpretation
The Stop hook's scout note tells the session to plan and work every find; a find marked confirm waits on the user's yes, so it gets its own line.
## Assumptions (confidence)
## Acceptance criteria
- [x] A scout drain that files a confirm item tells the session to ask once (fm ask ID confirm), not to plan and work it; ordinary finds keep 'Plan it and work it' — verify with `python3 plugin/tests/run.py test_scout`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: _scout_note words confirm and ordinary finds apart
2. [x] Split the Stop reason by meta confirm in fmhooks
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_scout.ScoutDrive.test_a_find_that_waits_on_the_users_yes_is_asked_not_worked` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: ScoutDrive 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 665181711e7d] (2026-10-30T13:17:18Z)
- `python3 plugin/tests/run.py test_scout.ScoutDrive.test_a_find_that_waits_on_the_users_yes_is_asked_not_worked` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: ScoutDrive 0s) / OK [ran] [tree 665181711e7d] (2026-10-30T13:17:18Z)
- (step 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 27 tests in 17.1s (5 classes, 16 at a time; slowest: Scout 17s, Mandate 5s, ScoutDrive 3s) / OK [ran] [tree d0c4073c01b0] (2026-10-30T13:17:43Z)
- (step 2) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 27 tests in 15.8s (5 classes, 16 at a time; slowest: Scout 15s, Mandate 5s, ScoutDrive 3s) / OK [ran] [tree d0c4073c01b0] (2026-10-30T13:17:59Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 27 tests in 21.5s (5 classes, 16 at a time; slowest: Scout 21s, Mandate 5s, ScoutDrive 2s) / OK [ran] [tree d0c4073c01b0] (2026-10-30T13:18:21Z)
- (audit self) `read the diff: _scout_note splits made by brief meta confirm; Stop path calls it` → a missing brief reads as ordinary (getattr default); find text unchanged for ordinary finds; ids are fm task ids, not untrusted text [tree d0c4073c01b0] (2026-10-30T13:18:21Z)
- (ac 1) `python3 plugin/tests/run.py test_scout` → exit 0 · Ran 27 tests in 13.4s (5 classes, 16 at a time; slowest: Scout 13s, Mandate 3s, ScoutDrive 1s) / OK [ran] [tree d0c4073c01b0] (2026-10-30T13:19:18Z)
- (audit edge) `self audit recorded; red→green on the new ScoutDrive test; test_scout green` → a find whose brief is missing reads as ordinary; only-ordinary and only-confirm lists each give one line [tree d0c4073c01b0] (2026-10-30T13:19:18Z)
- (audit self) `self audit recorded; red→green on the new ScoutDrive test; test_scout green` → no findings [tree d0c4073c01b0] (2026-10-30T13:19:18Z)
## Log
- 2026-10-30T06:36:03Z created
- 2026-10-30T13:16:46Z set type=FIX, tier=S
- 2026-10-30T13:16:46Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_scout.py', 'CHANGELOG.md']
- 2026-10-30T13:16:46Z planned: it has criteria and steps
- 2026-10-30T13:16:47Z focused
- 2026-10-30T13:19:56Z done
- 2026-10-30T13:19:57Z committed 6270e090 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2105-review: Verdict** — changes needed. The confirm task shows the user a false reason, and nothing tests the site export that AC3 relies on. Both fixes are …
- T-1800 [PERFORMANCE M, done, 3 steps] Foreman reasons ahead: names why usage burns, unasked (session start, fm doctor, fm digest) — lesson: Account-wide scans hung on a …
- research T-2138-review: Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, …
- decision 2026-10-30: T-2105: Genesis offers itself through fm scout (probe_genesis, once ever, ≥10 done tasks, no tower, nothing queued) as a confirm task, not a new fm …
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_scout.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_scout.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
