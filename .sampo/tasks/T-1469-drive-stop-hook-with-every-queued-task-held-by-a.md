---
id: T-1469
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T15:59:54Z
updated: 2026-10-22T16:18:06Z
base: 217f13bca7ea7a3880719fed999abd4a16f85f6e
base_tree: 0834679cb3c574167b420176a708b5bb3e781c36
plan0_at: 2026-10-22T16:01:11Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_drive_side.py, CHANGELOG.md]
verified: strong
---
# Drive counts builder lanes as background work
## Raw request
> Drive (Stop hook): with every queued task held by a builder lane, it still says 'Next: T-xxxx: fm focus T-xxxx', which fm focus refuses ('held by lane …'); it should count live lanes as background work (like background agents) and say what to do while they run, not loop on an impossible focus (2026-10-22: ~10 repeated stops)
## Interpretation
_drive (fmhooks.py ~3282) treats a task a builder lane holds as the next one to focus ('Next: T-x: fm focus T-x') when the main session has no active task, though fm focus refuses it ('held by lane'); with every queued task in a lane it loops on that impossible step every Stop.
## Assumptions (confidence)
## Acceptance criteria
- [x] with the only queued task held by a lane, Stop names the lane as running work instead of 'fm focus' — verify with `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld`
## Non-goals
## Approach (options → choice → why)
When choosing the next work, skip briefs a live lane holds (lane-active in fm lane list); when that leaves nothing, say the lanes are working (their notifications wake the session) and offer the inbox or nothing, like the background-agent branch. Options: make fm focus take a lane's task (breaks the one-owner rule) → rejected.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] skip lane-held tasks in _drive
## Resume here
<!-- auto -->
- 2026-10-22T16:09:07Z step 1/2: failing test
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1469.edit, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1469-fix.edit, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1263-approach.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1263-ac.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/cap-cloned.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1472-approach.md, /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/t1473-approach.md
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld` → ✗ exit 1 · Ran 1 test in 1.366s / FAILED (failures=1) [ran] [tree 5b7140f6b7ce] (2026-10-22T16:10:39Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld` → ✗ exit 1 · Ran 1 test in 1.642s / FAILED (failures=1) [ran] [tree adc1459a85b4] (2026-10-22T16:10:58Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld` → exit 0 · Ran 1 test in 1.731s / OK [ran] [tree c118daecc8e9] (2026-10-22T16:11:23Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_drive_side.LaneHeld` → exit 0 · Ran 1 test in 1.372s / OK [ran] [tree 38def7a240fc] (2026-10-22T16:14:55Z)
- (audit edge) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → the note repeats only when the set of lanes changes (d['lanes']); an active main-session task is unaffected [tree 38def7a240fc] (2026-10-22T16:14:55Z)
- (audit intent) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → today's ~10 repeated impossible 'fm focus' stops [tree 38def7a240fc] (2026-10-22T16:14:55Z)
- (audit self) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → no findings [tree 38def7a240fc] (2026-10-22T16:14:55Z)
- (audit edge) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → the note repeats only when the set of lanes changes (d['lanes']); an active main-session task is unaffected [tree 38def7a240fc] (2026-10-22T16:16:34Z)
- (audit intent) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → today's ~10 repeated impossible 'fm focus' stops [tree 38def7a240fc] (2026-10-22T16:16:34Z)
- (audit adversary) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → fewer pushes only for lane-held tasks; nothing a user must answer is hidden [tree 38def7a240fc] (2026-10-22T16:16:34Z)
- (audit self) `self: lane-held briefs (meta builder, not closed) are skipped when the drive picks work from active/queue/inbox; with nothing else, one note naming the lanes, then silence until the set changes. test_drive_side (incl. LaneHeld) and test_hooks.Stop green.` → no findings [tree 38def7a240fc] (2026-10-22T16:16:34Z)
## Log
- 2026-10-22T15:59:54Z created
- 2026-10-22T16:00:55Z planned from capture
- 2026-10-22T16:01:01Z set scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_drive_side.py', 'CHANGELOG.md']
- 2026-10-22T16:01:10Z focused
- 2026-10-22T16:09:11Z paused: focus moved to T-1302
- 2026-10-22T16:10:35Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-22T16:10:35Z focused
- 2026-10-22T16:16:33Z scope: plugin/lib/fmcodetui.py and plugin/tests/test_code_tui.py are T-1302's, merged and committed (6c1c344b) while this task was checkpointed; this task changes only fmhooks.py and test_drive_side.py
- 2026-10-22T16:18:04Z done
- 2026-10-22T16:18:06Z committed a618859e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261009-091631.pack: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just sim…
- research T-1057-review: MEDIUM** — `plugin/lib/fmloop.py:14,36` — "past every earlier ideas.md" is only the newest 6. [stale: plugin/evals/guard-force-push/prompt.md, pl…
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- likely tests for the scope: plugin/tests/test_hooks.py
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_drive_side.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
