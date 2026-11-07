---
id: T-3609
type: FIX
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: self
created: 2026-11-07T04:29:59Z
updated: 2026-11-07T04:42:34Z
lane: ~/.claude/foreman.lanes/T-3609
lane_branch: foreman/T-3609
base: 020346f6dd8d82f6614b6c5fc59884a8991a8bde
base_tree: ae55df2d760a986497b69351e68d31ce932e6339
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-07T04:32:53Z
plan0_scope: []
---
# _mark_builder (hooks.py ~4854) loses the builder-return mark when the project lock is…
## Raw request
> FIX: _mark_builder (hooks.py ~4854) loses the builder-return mark when the project lock is busy: it takes the lock with LOCK_QUICK (1 s) and parses every brief under it; ~120 LockTimeout tracebacks in hooks.log, and a lost mark leaves builder_returned unset, so the builder cap and lane wait (lanes.py ~404, ~1737, live.py ~155) count a returned builder as live. Find the brief outside the lock, lock only to re-read and save that one brief, retry on timeout, log a one-line counted note instead of a traceback (self-improvement pass)
## Interpretation
Reading 1 (chosen): the mark must survive lock contention, so the lock covers only one brief's re-read and save, retried on a timeout; contention is a one-line counted note. Reading 2 (ruled out): only silence the traceback (catch LockTimeout, log a line): the mark would still be lost, and the lost mark is the defect (builder cap and lane wait count a returned builder as live).
## Assumptions (confidence)
## Acceptance criteria
- [ ] a mark arriving while another process holds the project lock still lands, retries on timeout, and logs one counted line instead of a traceback — verify with `nice -n 10 python3 plugin/tests/run.py test_builder_mark`
- [ ] the existing builder start/stop mark behaviour still holds — verify with `nice -n 10 python3 plugin/tests/run.py test_lanes.Lanes.test_a_builders_own_stop_frees_its_slot_while_the_launcher_lives`
## Non-goals
## Approach (options → choice → why)
1) do less: raise the lock wait from LOCK_QUICK to LOCK_SLOW. Fails if: every brief is still parsed under the lock, so it holds it longer for everyone and still times out under 8 lanes. 2) inline lock + find_brief + save with a retry loop. Likely outcome: works, but duplicates the read-modify-write T-3558 already wrapped. 3) use what exists: find the brief outside the lock, then cli.mutate (T-3558's lock-only-for-the-write helper: re-read one brief, apply, save, log, views after the lock) with 3 tries of its 5 s wait (15 s at most, in an async hook). Likely outcome: the lock holds for one brief; a no-op mark takes no lock. Choice 3 (85%): reuses the helper, shortest correct diff, contention becomes one counted hooks.log line.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: lock held by another process when the mark arrives  <- CURRENT
2. [x] find the brief outside the lock, mark it via cli.mutate with retries and a one-line note
3. [x] run the targeted tests and the existing builder-mark test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_builder_mark` → ✗ exit 1 · Ran 3 tests in 25.2s (1 jobs, 16 at a time; slowest: BuilderMark 3s) / FAILED (1 classes: test_builder_mark.BuilderMark) [ran] [tree ac047184b909] [world 2f1906870a] (2026-11-07T04:33:46Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_builder_mark` → exit 0 · Ran 3 tests in 14.0s (1 jobs, 16 at a time; slowest: BuilderMark 3s) / OK [ran] [tree 9899ddb6c9c7] [world 2f1906870a] (2026-11-07T04:34:53Z)
- (step 3) `nice -n 10 python3 plugin/tests/run.py test_builder_mark test_lanes.Lanes.test_a_builders_own_stop_frees_its_slot_while_the_launcher_lives` → exit 0 · Ran 4 tests in 136.7s (2 jobs, 16 at a time; slowest: Lanes 3s, BuilderMark 3s) / OK [ran] [tree 9899ddb6c9c7] [world 2f1906870a] (2026-11-07T04:42:34Z)
## Log
- 2026-11-07T04:29:59Z created
- 2026-11-07T04:32:35Z planned: it has criteria and steps
- 2026-11-07T04:32:38Z lane: ~/.claude/foreman.lanes/T-3609 on foreman/T-3609
- 2026-11-07T04:32:53Z focused
- 2026-11-07T04:32:53Z predicted from its closes: 6 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3535 [FIX M, active, 3 steps] 139 hook errors swallowed in 24 h (122 in builders), the latest a LockTimeout on the…
- T-1453 [FIX S, done, 2 steps] Stop hook still judges the turn when the project lock is busy
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- decision 2026-11-06: Sync is off until its export is cheap: every state write re-exported all ~3,300 briefs under the project lock (sync.export inside regen_views), so c…
- similar finished tasks took 2–3 steps
- start here (files T-1453 touched): plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md
