---
id: T-3432
type: FIX
tier: S
status: done
priority: urgent
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/lib/sampo/cli.py, plugin/tests/test_bus.py]
depends_on: []
source: discovered
created: 2026-11-06T12:03:01Z
updated: 2026-11-06T16:29:47Z
base: 26077fb83c0e892ff609b074873efcbde342a5c1
base_tree: c0e2827033a327ad14764d1ffd9e36b35caddf0a
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T12:04:23Z
plan0_scope: []
builder_returned: 2026-11-06T12:05:14Z
lane_stop: merged 2026-11-06T12:12:45Z
verified: strong
unproven: [meaning]
lane_verified: 5594fdc089b274605da8665a4d3393302262ca55
---
# T-3398 made sampo task block/defer release the task's file leases, but T-2870's…
## Raw request
> FIX!: T-3398 made sampo task block/defer release the task's file leases, but T-2870's test_claims.Claims.test_a_bare_drop_with_no_active_task_frees_only_closed_or_taskless_leases requires an open (blocked) task to keep its leases; it is red on foreband/build and refused sampo ship. Release on done/dropped only, as the existing behaviour expects, and update T-3398's block test to match
## Interpretation
Release leases only on done/dropped; blocked/deferred keep them (T-2870).
## Assumptions (confidence)
## Acceptance criteria
- [x] test_claims.Claims and test_bus pass — verify with `python3 plugin/tests/run.py test_claims.Claims test_bus`
## Non-goals
## Approach (options → choice → why)
Narrow the T-3398 condition in cli.mutate to c.CLOSED, preclaim=True; fix its block test.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Release only on closed; fix block test
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims.Claims test_bus` → exit 0 · Ran 46 tests in 31.9s (28 jobs, 16 at a time; slowest: Watch 4s, Approvals 4s, ClaimsReview 3s) / OK [ran] [tree c23bbcf5eeb0] [world 2f1906870a] (2026-11-06T12:05:04Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 1dd49205a84d] (2026-11-06T12:12:49Z)
- `python3 plugin/tests/run.py test_bus` → ✗ exit 1 · Ran 28 tests in 5.2s (7 jobs, 16 at a time; slowest: Approvals 4s, Watch 3s, Lease 3s) / FAILED (1 classes: test_bus.Lease) (start tree + this task's tests) [ran] [tree 1dd49205a84d] [world 2f1906870a] (2026-11-06T12:13:03Z)
- `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 28 tests in 4.1s (23 jobs, 16 at a time; slowest: Approvals 4s, Watch.test_a_resumed_session_keeps_its_watcher 1s, Bus 1s) / OK [ran] [tree 1dd49205a84d] [world 2f1906870a] (2026-11-06T12:13:03Z)
- (ac 1) `python3 plugin/tests/run.py test_claims.Claims test_bus` → exit 0 · Ran 46 tests in 17.8s (9 jobs, 16 at a time; slowest: Claims 4s, Approvals 4s, Watch 3s) / OK [ran] [tree 1dd49205a84d] [world 2f1906870a] (2026-11-06T12:13:25Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 1dd49205a84d] (2026-11-06T12:13:25Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 1dd49205a84d] (2026-11-06T12:13:25Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 1dd49205a84d] (2026-11-06T12:13:25Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 1dd49205a84d] (2026-11-06T12:13:25Z)
## Log
- 2026-11-06T12:03:01Z created
- 2026-11-06T12:03:18Z set tier=S
- 2026-11-06T12:04:20Z planned: it has criteria and steps
- 2026-11-06T12:04:21Z focused
- 2026-11-06T12:04:23Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T12:12:45Z merged worktree-agent-a2b3efde4a856f82d (2 file(s))
- 2026-11-06T12:12:46Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2b3efde4a856f82d
- 2026-11-06T12:12:46Z focused
- 2026-11-06T12:12:48Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/lib/sampo/cli.py', 'plugin/tests/test_bus.py']
- 2026-11-06T12:12:49Z scope: widened at merge to the reviewed lane's own diff (5594fdc08), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T12:13:55Z done
- 2026-11-06T12:13:57Z committed 458042247 (1 file)
- 2026-11-06T16:29:47Z verified: the full suite is green on 1078ed22d, which contains 5594fdc08
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3371 [FIX M, planned, 1 steps] Sampo lease drop run in a lane worktree dropped leases it never claimed (claims.py,…
- T-3354 [FIX S, done, 1 steps] Re-land T-3283 and fix the two tests the closes' affected runs missed: test_claims still expects a lease take over a lane pre-claim to be r…
- decision 2026-11-02: [costly] Genesis build stage: a deferred Mission task is carried, named, not a blocker
- similar finished tasks took 1–4 steps
## Lessons
- none: a reviewed builder lane; its lessons are in the builder's report and the review findings
## Files touched
- plugin/lib/sampo/cli.py
- plugin/tests/test_bus.py
- CHANGELOG.md
