---
id: T-3450
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/ops-1.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/rune.py, plugin/tests/test_round_f.py]
depends_on: []
source: user
created: 2026-11-06T15:23:55Z
updated: 2026-11-06T16:29:49Z
base: c93f915a644c3119310c3572f6ce4b5daa915e87
base_tree: 6a22e400a04231146aa3ad42cf0848d99064e53c
lane_stop: merged 2026-11-06T15:47:47Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T15:47:50Z
plan0_scope: []
verified: strong
unproven: [docs, meaning]
lane_verified: 84590f586cd8e9bd3eef61bb7a7270e6d45e63a9
---
# Re-land T-3120: auto-reverted on the same CheckSkip/Claims/CloseGates reds the slot-pool bug (T-3442) made
## Raw request
> Re-land T-3120: auto-reverted on the same CheckSkip/Claims/CloseGates reds the slot-pool bug (T-3442) made
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] T-3120's gate reuse is back and its tests pass — verify with `python3 plugin/tests/run.py test_round_f`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] revert the revert 0f041f3f1 in a lane; run its tests
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 758b93f0479f] (2026-11-06T15:47:52Z)
- `python3 plugin/tests/run.py test_round_f` → ✗ exit 1 · Ran 26 tests in 22.4s (1 jobs, 16 at a time; slowest: RoundF 5s) / FAILED (1 classes: test_round_f.RoundF) (start tree + this task's tests) [ran] [tree 758b93f0479f] [world 2f1906870a] (2026-11-06T15:48:31Z)
- `python3 plugin/tests/run.py test_round_f` → exit 0 · Ran 26 tests in 10.8s (1 jobs, 16 at a time; slowest: RoundF 5s) / OK [ran] [tree 758b93f0479f] [world 2f1906870a] (2026-11-06T15:48:31Z)
- (ac 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T15:48:31Z [ran] [tree 758b93f0479f] [world 2f1906870a] (2026-11-06T15:48:35Z)
- (step 1) `python3 plugin/tests/run.py test_round_f` → exit 0 · reused: the same command passed on this tree and world at 2026-11-06T15:48:31Z [ran] [tree 758b93f0479f] [world 2f1906870a] (2026-11-06T15:48:35Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 758b93f0479f] (2026-11-06T15:48:35Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 758b93f0479f] (2026-11-06T15:48:35Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 758b93f0479f] (2026-11-06T15:48:35Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree 758b93f0479f] (2026-11-06T15:48:35Z)
## Log
- 2026-11-06T15:23:55Z created
- 2026-11-06T15:24:01Z lane: ~/.claude/foreman.lanes/T-3450 on foreman/T-3450
- 2026-11-06T15:47:47Z merged foreman/T-3450 (5 file(s))
- 2026-11-06T15:47:48Z lane removed: ~/.claude/foreman.lanes/T-3450
- 2026-11-06T15:47:49Z focused
- 2026-11-06T15:47:50Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T15:47:52Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/ops-1.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/core.py', 'plugin/lib/sampo/rune.py', 'plugin/tests/test_round_f.py']
- 2026-11-06T15:47:52Z scope: widened at merge to the reviewed lane's own diff (84590f586), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:54:04Z done
- 2026-11-06T15:54:07Z committed 5c084e268 (1 file)
- 2026-11-06T16:29:49Z verified: the full suite is green on 1078ed22d, which contains 84590f586
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3445 [FIX S, done, 1 steps] Re-land T-2911 and T-3372: both auto-reverted on CheckSkip/Claims reds the slot-pool bug (T-3442) made, red at their parents too — lesson: …
- T-3446 [FIX M, planned, 1 steps] The post-merge suite reverts a merge whose red classes are red at its parent too…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-06: Post-merge suite paused for the serial landing run: its auto-revert reverted T-3410 (0cad059e5, a MASTER.md bullet) on load-only failures (CheckSkip…
- similar finished tasks took 1–4 steps
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A post-merge revert needs the red to be absent at the parent; otherwise the revert is noise.
## Files touched
- CHANGELOG.md
- docs/map/ops-1.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/rune.py
- plugin/tests/test_round_f.py
