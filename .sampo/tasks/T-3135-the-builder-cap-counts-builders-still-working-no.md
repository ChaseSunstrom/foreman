---
id: T-3135
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/lanes.py, plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py, CHANGELOG.md, docs/map/*.md]
depends_on: []
source: user
created: 2026-11-05T04:46:59Z
updated: 2026-11-05T04:56:25Z
base: 7f5d1f67e0f36baf23d56dcf1dcf1297d560c50d
base_tree: 5c27205f66dea973c90bdda7460b2c6d2e5fae2c
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T04:47:43Z
plan0_scope: [plugin/lib/sampo/lanes.py, plugin/lib/sampo/hooks.py, plugin/tests/test_lanes.py, CHANGELOG.md, docs/map/*.md]
verified: strong
---
# The builder cap counts builders still working, not finished lanes waiting on a merge; unmerged finished lanes get their own larger cap, so a slow merge queue no longer stops all new building
## Raw request
> The builder cap counts builders still working, not finished lanes waiting on a merge; unmerged finished lanes get their own larger cap, so a slow merge queue no longer stops all new building
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] lane brief refuses only when the cap's worth of builders are still working (a lane whose builder returned a commit, with a clean tree and no live builder, is finished) or when UNMERGED_MAX (20) finished lanes wait unmerged, naming which; the drive's slot count agrees; BUILDERS_MAX is 16 — verify with `python3 plugin/tests/run.py test_lanes test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: three finished unmerged lanes and one working builder allow a fifth lane; 6 working refuse; 12 unmerged refuse
2. [x] the two counts in lanes.builders_cap and lanes_free
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 160 tests in 36.3s (14 classes, 16 at a time; slowest: Lanes 36s, LaneRecovery 27s, RaceEvidence 15s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 79635d4e6db8] [world 2f1906870a] (2026-11-05T04:49:22Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_hooks` → exit 0 · Ran 418 tests in 71.2s (45 classes, 16 at a time; slowest: Stop 71s, Lanes 43s, NoTaskGate 41s) / OK [ran] [tree 66b8f5c94b24] [world 2f1906870a] (2026-11-05T04:52:33Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_hooks` → exit 0 · Ran 418 tests in 94.6s (45 classes, 16 at a time; slowest: Stop 94s, Lanes 68s, NoTaskGate 64s) / OK [ran] [tree 66b8f5c94b24] [world 2f1906870a] (2026-11-05T04:54:29Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T04:54:29Z [ran] [tree 66b8f5c94b24] [world 2f1906870a] (2026-11-05T04:55:07Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 160 tests in 36.0s (14 classes, 16 at a time; slowest: Lanes 35s, LaneRecovery 27s, RaceEvidence 15s) / OK [ran] [tree 66b8f5c94b24] [world 2f1906870a] (2026-11-05T04:55:07Z)
- (audit intent) `self: the cap now counts working builders (out minus c.finished_lanes(quiet_min=0)), finished lanes get UNMERGED_MAX 20, the drive's lanes_free agrees, BUILDERS_MAX 16; an unreadable lane counts as working` → on 2026-11-05 six slots were held by finished lanes and nothing could start; with this, finished lanes free their slot (test) and lane max reaches 16 (this project set to 12) [tree 66b8f5c94b24] (2026-11-05T04:55:07Z)
- (audit edge) `self: the cap now counts working builders (out minus c.finished_lanes(quiet_min=0)), finished lanes get UNMERGED_MAX 20, the drive's lanes_free agrees, BUILDERS_MAX 16; an unreadable lane counts as working` → a builder still alive counts as working even with commits (finished_lanes skips live builders); finished_lanes failing counts everything as working; host_strain still refuses a lane on an overloaded host; 20 unmerged lanes refuse with the list [tree 66b8f5c94b24] (2026-11-05T04:55:07Z)
- (audit self) `self: the cap now counts working builders (out minus c.finished_lanes(quiet_min=0)), finished lanes get UNMERGED_MAX 20, the drive's lanes_free agrees, BUILDERS_MAX 16; an unreadable lane counts as working` → no findings [tree 66b8f5c94b24] (2026-11-05T04:55:07Z)
## Log
- 2026-11-05T04:46:59Z created
- 2026-11-05T04:47:41Z set approved=True
- 2026-11-05T04:47:41Z set scope=['plugin/lib/sampo/lanes.py', 'plugin/lib/sampo/hooks.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md', 'docs/map/*.md']
- 2026-11-05T04:47:41Z focused
- 2026-11-05T04:47:43Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T04:51:22Z criterion 1 verify: `python3 plugin/tests/run.py test_lanes` → `python3 plugin/tests/run.py test_lanes test_hooks`
- 2026-11-05T04:51:22Z criterion 1 text: lane brief refuses only when 6 builders are still working (a lane whose builder returned a commit is finished) or when 12 finished lanes wait unmerged; the refusal names which; 2026-11-05's case (six slots held by three finished, merge-waiting lanes and a three-task branch) would have let new builders start → lane brief refuses only when the cap's worth of builders are still working (a lane whose builder returned a commit, with a clean tree and no live builder, is finished) or when UNMERGED_MAX (20) finished lanes wait unmerged, naming which; the drive's slot count agrees; BUILDERS_MAX is 16
- 2026-11-05T04:56:23Z done
- 2026-11-05T04:56:25Z committed 9bb63c17 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2038 [FIX M, done, 2 steps] Finished builder lanes sit unmerged for days unseen: T-1670 and T-1784 each have a… — lesson: A status that polls git per item needs a cach…
- T-2797 [FIX M, done, 3 steps] Gates under machine load wait or stretch instead of failing: fm lane brief holds a new lane past 1.5 load per core, and fm task finish, fm …
- T-2914 [FEATURE M, done, 3 steps] Meaning is planned, not labelled after: a user's M or L plan names each clause of their request that no criterion checks before work st…
- decision 2026-11-03: [revisited: keep going with everything else] [cites: user steer 2026-11-03: make sure to keep going with everything else when done] [check: python3 …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_ambient.py, plugin/tests/test_board_export.py, plugin/tests/test_bookkeeping.py, plugin/tests/test_bus.py, plugin/tests/test_code.py, plug…
## Why not caught
the cap test only ever counted briefed builders; no test had a finished lane waiting on a merge beside a new brief, so a slow merge queue freezing all building was never exercised
## Lessons
- A concurrency cap must count the thing it protects: builders working, not branches waiting on someone else's queue; otherwise one slow stage downstream freezes every stage upstream.
## Plan gaps
- failed first: step 1 failing test: three finished unmerged lanes and one working builder allow a fifth lane; 6 working r…
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/hooks.py
- CHANGELOG.md
