---
id: T-3478
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/selfcheck.py, plugin/tests/test_selfcheck.py, CHANGELOG.md, docs/map/**, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-3.md]
depends_on: []
source: user
created: 2026-11-06T18:31:50Z
updated: 2026-11-06T21:59:32Z
base: 89d0d3468a2770da2f90299261ea1f467b4500ce
base_tree: 9b757399c14a04329ce334557e059834a049f1f8
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T18:32:32Z
plan0_scope: [plugin/lib/sampo/selfcheck.py, plugin/tests/test_selfcheck.py, CHANGELOG.md, docs/map/**]
lane_stop: merged 2026-11-06T18:53:59Z
verified: strong
unproven: [meaning]
---
# Self-check: the landing rate: N finished lanes wait, M landed in the last 2 h (minutes each), the pile clears in H hours at that rate; a wait the user had to ask about ('why is this taking so long just to push?') is the miss
## Raw request
> Self-check: the landing rate: N finished lanes wait, M landed in the last 2 h (minutes each), the pile clears in H hours at that rate; a wait the user had to ask about ('why is this taking so long just to push?') is the miss
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo next names waiting lanes, the last 2 h's landings with minutes each and the hours to clear, once 5+ lanes wait — verify with `python3 plugin/tests/run.py test_selfcheck`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then a landing_rate check in selfcheck.py from the ledger's lane_merge events
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_selfcheck` → ✗ exit 1 · Ran 7 tests in 1.5s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / FAILED (1 classes: test_selfcheck.SelfCheck) [ran] [tree 6040bbf81ad8] [world 2f1906870a] (2026-11-06T18:32:48Z)
- (step 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 7 tests in 1.4s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree ee63fab2b479] [world 2f1906870a] (2026-11-06T18:33:46Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree b636b2d992f0] (2026-11-06T18:59:22Z)
- (ac 1) `python3 plugin/tests/run.py test_selfcheck` → exit 0 · Ran 7 tests in 1.4s (1 jobs, 16 at a time; slowest: SelfCheck 1s) / OK [ran] [tree b636b2d992f0] [world 2f1906870a] (2026-11-06T18:59:26Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree b636b2d992f0] (2026-11-06T18:59:26Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree b636b2d992f0] (2026-11-06T18:59:26Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree b636b2d992f0] (2026-11-06T18:59:26Z)
- (audit self) `lane review before merge, review findings fixed in a further round; self audit after the merge` → no findings [tree b636b2d992f0] (2026-11-06T18:59:26Z)
## Log
- 2026-11-06T18:31:50Z created
- 2026-11-06T18:31:56Z lane: ~/.claude/foreman.lanes/T-3478 on foreman/T-3478
- 2026-11-06T18:32:29Z focused
- 2026-11-06T18:32:32Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T18:53:59Z merged foreman/T-3478 in merge train
- 2026-11-06T18:59:22Z set scope=['plugin/lib/sampo/selfcheck.py', 'plugin/tests/test_selfcheck.py', 'CHANGELOG.md', 'docs/map/**', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-3.md']
- 2026-11-06T18:59:22Z scope: widened at merge to the reviewed lane's own diff (0395ecdc9), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T19:02:05Z done
- 2026-11-06T19:02:09Z committed f2e37710f (1 file)
- 2026-11-06T21:59:32Z lane removed: ~/.claude/foreman.lanes/T-3478; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3127 [FEATURE M, planned, 3 steps] Self-awareness part 2: turn-end self-checks, one per miss class, that fire with numbers before the user would ask (T-3123)
- T-2915 [FEATURE M, done, 4 steps] MASTER.md opens whole in one Read: each over-long section moves to docs/map shards, MASTER.md keeps a one-line-per-entry index with lin…
- T-3297 [PERFORMANCE L, done, 4 steps] PERF part 1: one slot pool for every test run on the machine, a fork server for the tests' fm calls, a perf bench, and a builder ce…
- decision 2026-11-01: [revisited: long-horizon tier is the deciding end-of-run score] [cites: user steer 2026-10-30: standing rules for the rest of the genesis run] [chec…
- similar past tasks were L: consider --tier L
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Why not caught
the builder's own failing test before the fix, then the lane review; no earlier gate covered this path (see the brief's Regression test)
## Lessons
- A wait nobody measured is invisible: the line read every turn has to carry the rate.
## Plan gaps
- failed first: step 1 failing test, then a landing_rate check in selfcheck.py from the ledger's lane_merge events
## Files touched
- CHANGELOG.md
- docs/map/files-lib-3.md
- plugin/lib/sampo/selfcheck.py
- plugin/tests/test_selfcheck.py
