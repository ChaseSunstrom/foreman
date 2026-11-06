---
id: T-3374
type: FIX
tier: M
status: planned
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-06T06:21:34Z
updated: 2026-11-06T06:59:54Z
lane: ~/.claude/foreman/.claude/worktrees/agent-ab37ed7dacde022d1
lane_branch: worktree-agent-ab37ed7dacde022d1
base: 63f19d902a1815ca2f5e9fb9433545a642c72f24
base_tree: 1b9837219c451629fdffd9906b71771442a157e6
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-06T06:27:56Z
plan0_scope: []
builder_returned: 2026-11-06T06:59:54Z
---
# A stale per-worktree index.lock (.git/worktrees/<lane>/index.lock, left by a killed…
## Raw request
> FIX: a stale per-worktree index.lock (.git/worktrees/<lane>/index.lock, left by a killed test) blocks every git write in that lane; lane status/doctor should name it and clear it when no process holds the worktree (T-3364)
## Interpretation
Reading 1: only name the stale lock. Reading 2: name and clear safely (chosen, per the brief).
## Assumptions (confidence)
## Acceptance criteria
- [ ] stale lock named by list/fsck, cleared by recover only when old and unheld — verify with `python3 plugin/tests/test_lane_lock.py`
## Non-goals
## Approach (options → choice → why)
1) new lanes.py helpers + lane list/recover + doctor fsck; fails if: recover needs a stop cause first 2) use what exists: fsck's _broken_lanes and lane list rows; fails if: they skip the lock 3) do less: name only; fails if: lane stays blocked. Choice 1 (80%): helpers in lanes.py, list names, recover clears first, fsck names
## Risks and rollback
## Execution prompt
## Steps
1. [x] test, helpers, wiring
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/test_lane_lock.py` → exit 0 · Ran 4 tests in 2.441s / OK (ran] (tree e581b1abb6bf] (world 2f1906870a] (2026-11-06T06:29:03Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_lock test_lane_twins test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 406 tests in 441.4s (78 jobs, 16 at a time; slowest: Lanes 33s, LaneRecovery 30s, RaceEvidence 13s) / FAILED (1 classes: test_left_out.LeftOut) (ran] (tree e581b1abb6bf] (world 2f1906870a] (2026-11-06T06:36:29Z)
- (step 1) `python3 plugin/tests/run.py test_lane_lock` → exit 0 · Ran 6 tests in 85.9s (1 jobs, 16 at a time; slowest: LaneIndexLock 1s) / OK (ran] (tree 24511bf626b5] (world 2f1906870a] (2026-11-06T06:57:26Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_lane_lock test_lane_twins test_lanes test_left_out test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 408 tests in 49.4s (214 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, RenameScan.test_no_fm_only_command_regex 5s, ViewsRepair 4s) / FAILED ( (ran] (tree 24511bf626b5] (world 2f1906870a] (2026-11-06T06:58:19Z)
- (step 1) `python3 plugin/tests/run.py test_lane_lock` → exit 0 · Ran 6 tests in 17.7s (1 jobs, 16 at a time; slowest: LaneIndexLock 1s) / OK (ran] (tree 221076a24e35] (world 2f1906870a] (2026-11-06T06:59:50Z)
## Log
- 2026-11-06T06:21:34Z created
- 2026-11-06T06:27:53Z planned: it has criteria and steps
- 2026-11-06T06:27:55Z focused
- 2026-11-06T06:27:56Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-06T06:53:22Z focused
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1667-review: Verdict: changes needed.** One MEDIUM and one more MEDIUM-ish lead, both small to fix. I could only read files (no shell), so I did not run the t…
- research T-1405-review: Verdict:** approve with nits. I found no CRITICAL or HIGH defect. I read the code and tests in the worktree and ran nothing, because the tools I …
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- decision 2026-10-22: T-1405: an unreadable /proc process of ours keeps a stale index.lock only when it is a git; any other unreadable process doesn't block (31 of this h…
