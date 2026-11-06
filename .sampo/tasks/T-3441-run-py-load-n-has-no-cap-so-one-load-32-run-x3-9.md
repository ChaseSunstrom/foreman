---
id: T-3441
type: FIX
tier: S
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/README.md, .sampo/research, .sampo/tasks, plugin/tests/run.py, plugin/tests/test_run.py]
depends_on: []
source: discovered
created: 2026-11-06T14:47:16Z
updated: 2026-11-06T15:19:21Z
base: fc66ce46233bff4275210cce926900ba3a5eb08c
base_tree: 8d97eab5734ba217b7f4e0653215b3c412e1343c
lane_stop: merged 2026-11-06T15:14:41Z
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T15:14:43Z
plan0_scope: []
verified: strong
---
# run.py --load N has no cap, so one --load 32 run (x3, 96 busy loops) pushed a 16-CPU…
## Raw request
> FIX: run.py --load N has no cap, so one --load 32 run (x3, 96 busy loops) pushed a 16-CPU host to load 100 for 12 min and starved the ship and every merge; cap --load at the CPU count (or refuse above it) and bound its run time
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] run.py --load N tops the host up to at most twice its CPU count (the busy loops already running count), naming the cut, so three --load 32 runs on 16 CPUs add 32 loops in all, not 96 — verify with `python3 plugin/tests/run.py test_run.Load`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] burn() caps n by 2x CPUs minus the 1-minute load average; a red test first
## Resume here
## Docs impact
the builder updated MASTER.md and docs/map for user-visible behaviour; CHANGELOG line added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree b1b2c54bb7c8] (2026-11-06T15:14:45Z)
- (ac 1) `python3 plugin/tests/run.py test_run.Load` → exit 0 · Ran 7 tests in 0.9s (1 jobs, 16 at a time; slowest: Load 0s) / OK [ran] [tree b1b2c54bb7c8] [world 2f1906870a] (2026-11-06T15:14:52Z)
- (step 1) `python3 plugin/tests/run.py test_run.Load` → exit 0 · Ran 7 tests in 0.9s (1 jobs, 16 at a time; slowest: Load 0s) / OK [ran] [tree b1b2c54bb7c8] [world 2f1906870a] (2026-11-06T15:14:52Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree b1b2c54bb7c8] (2026-11-06T15:14:52Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree b1b2c54bb7c8] (2026-11-06T15:14:52Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree b1b2c54bb7c8] (2026-11-06T15:14:52Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree b1b2c54bb7c8] (2026-11-06T15:14:52Z)
## Log
- 2026-11-06T14:47:16Z created
- 2026-11-06T14:49:56Z set tier=S
- 2026-11-06T14:49:57Z planned: it has criteria and steps
- 2026-11-06T14:50:12Z criterion 1 verify: `python3 plugin/tests/run.py test_run.Burn` → `python3 plugin/tests/run.py test_run.Load`
- 2026-11-06T14:50:12Z lane: ~/.claude/foreman.lanes/T-3441 on foreman/T-3441
- 2026-11-06T15:14:41Z merged foreman/T-3441 (2 file(s))
- 2026-11-06T15:14:42Z lane removed: ~/.claude/foreman.lanes/T-3441
- 2026-11-06T15:14:42Z focused
- 2026-11-06T15:14:43Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T15:14:44Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'plugin/tests/run.py', 'plugin/tests/test_run.py']
- 2026-11-06T15:14:44Z scope: widened at merge to the reviewed lane's own diff (45e9af018), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T15:19:17Z done
- 2026-11-06T15:19:21Z committed 505653aa8 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3243 [FIX M, done, 2 steps] Builder lanes starved for hours: the lane gate (1-min load over 1.5 per CPU) stayed shut… — lesson: a gate on shared load must reserve a mi…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-1836 [FEATURE S, done, 1 steps] Bench_playbooks.py: skip or widen the warm-route CPU limit when the 1-min load is above th
- decision 2026-11-05: Hold main-checkout test runs and closes after T-3151's close until the queued merges (T-3087, T-3108, then T-3053's chain) land
- similar finished tasks took 1–3 steps
## Regression test
none: the lane changes only tests (a guard that pins today's behaviour so a later change can't regress it); there was no failing behaviour to turn green, and its tests pass on the merged tree
## Lessons
- A load generator needs a host-wide cap: per-run limits add up when runs overlap.
## Files touched
- CHANGELOG.md
- plugin/tests/run.py
- plugin/tests/test_run.py
