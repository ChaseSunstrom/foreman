---
id: T-3444
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, .fm-scratch/**, .sampo/archive, .sampo/decisions.md, .sampo/fixes.md, .sampo/fleet, .sampo/fleet.md, .sampo/README.md, .sampo/research, .sampo/tasks, docs/map/files-lib-2.md, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py]
depends_on: []
source: discovered
created: 2026-11-06T14:57:44Z
updated: 2026-11-06T21:59:30Z
base: b2637ff28fed89fb38365309077dd4982e40675f
base_tree: e2603b01514d315470af506975b10c5db03ad682
lane_stop: merged 2026-11-06T17:18:26Z
verified: strong
unproven: [docs, perf-typed]
---
# Lane merge re-runs every criterion in the lane serially while the merge queue waits (4…
## Raw request
> PERF: lane merge re-runs every criterion in the lane serially while the merge queue waits (4 min at load 15, 16 min at load 100, per lane, 80 lanes queued). Record each criterion pass keyed by the lane's clean tip tree, reuse it at merge when the tree is unchanged, and add a precheck action (sampo lane precheck ID...) a queue runner can run ahead in parallel for the next lanes, so the serial merge only does git merge + the close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] merge reuses a criterion pass recorded on the same clean lane tree and re-runs it after the lane changes or with tracked edits; sampo lane precheck ID records passes without merging — verify with `python3 plugin/tests/run.py test_lanes.LanePrecheck`
## Non-goals
## Approach (options → choice → why)
Complete version: a criterion pass is recorded on the brief keyed by the lane's tip tree and the command, only when the lane has no tracked changes; merge reuses a pass on the same clean tree (saying so) and re-runs anything else; sampo lane precheck ID runs the same verify ahead and records, so a queue runner can check the next lanes in parallel while one merge lands. Rivals: (1) reuse the builder's own evidence runs (no extra run, but evidence is per step and its command often differs from the criterion's); (2) a separate state file of passes (more code, no gain over the brief's meta); (3) merge trains (one gate for N, but bisecting on load reds made them slower tonight). Chosen: the brief record plus precheck; (1) captured as a later gain.
## Risks and rollback
## Execution prompt
## Steps
1. [x] _verify records and reuses passes keyed by tree; lane precheck action; tests red first
## Resume here
## Docs impact
the lane diff carries its own doc edits (merged as reviewed); a CHANGELOG line is added here
## Verification evidence
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 4292d2cb372e] (2026-11-06T17:23:56Z)
- (step 1) `python3 plugin/tests/run.py test_lanes.LanePrecheck` → exit 0 · Ran 8 tests in 21.1s (1 jobs, 16 at a time; slowest: LanePrecheck 4s) / OK [ran] [tree 4292d2cb372e] [world 2f1906870a] (2026-11-06T17:28:42Z)
- (audit self) `builder lane reviewed by one fm-reviewer before merge; its should-level findings fixed by the builder in a further round and committed; merged diff re-read at merge` → no open findings [tree 330d3b5b7557] (2026-11-06T18:26:24Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes.LanePrecheck` → exit 0 · Ran 8 tests in 2.1s (1 jobs, 16 at a time; slowest: LanePrecheck 2s) / OK [ran] [tree 330d3b5b7557] [world 2f1906870a] (2026-11-06T18:26:28Z)
- (audit intent) `lane review before merge, review findings fixed in a further round; self audit after the merge` → one fm-reviewer checked each criterion against its test before merge; FIX FIRST items were fixed and committed by the builder [tree 330d3b5b7557] (2026-11-06T18:26:28Z)
- (audit edge) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the reviewer's edge findings were fixed in the builder's further round or captured [tree 330d3b5b7557] (2026-11-06T18:26:28Z)
- (audit adversary) `lane review before merge, review findings fixed in a further round; self audit after the merge` → the lane's own diff had one fm-reviewer pass before merge (security-focused where it touched the guard or hooks); the other security-sensitive hits are .sampo/ sync-mirror task notes from the 63f19d902 mirror move (state text, no code), which the commit secret scan covers [tree 330d3b5b7557] (2026-11-06T18:26:28Z)
## Log
- 2026-11-06T14:57:44Z created
- 2026-11-06T14:58:13Z set tier=M
- 2026-11-06T14:58:14Z planned: it has criteria and steps
- 2026-11-06T14:58:15Z lane: ~/.claude/foreman.lanes/T-3444 on foreman/T-3444
- 2026-11-06T17:18:26Z merged foreman/T-3444 in merge train
- 2026-11-06T17:23:56Z set scope=['CHANGELOG.md', '.fm-scratch/**', '.sampo/archive', '.sampo/decisions.md', '.sampo/fixes.md', '.sampo/fleet', '.sampo/fleet.md', '.sampo/README.md', '.sampo/research', '.sampo/tasks', 'docs/map/files-lib-2.md', 'plugin/lib/sampo/cli.py', 'plugin/lib/sampo/lanes.py', 'plugin/tests/test_lanes.py']
- 2026-11-06T17:23:56Z scope: widened at merge to the reviewed lane's own diff (8f74b07d7), the CHANGELOG line this close adds, the builder's gitignored .fm-scratch files, and .sampo/** (the sync mirror moved from .foreman/ in 63f19d902)
- 2026-11-06T18:30:07Z done
- 2026-11-06T21:59:30Z lane removed: ~/.claude/foreman.lanes/T-3444; dropped: its task is closed; the lane was left behind after the merge
## Follow-ups captured
## Measurements
merge-time criteria for 7 train lanes: ~25 min serial (train 10:29, its gate run started 10:56 per the run.py process start) → none for a lane prechecked on an unchanged tree (T-3127's precheck 11:20 recorded its passes for reuse); measured from the train's process times, the after side on one lane so far
## Lessons
- A serial queue spends most of its time on work that could run ahead: move every check that does not need the merged tree off the critical path.
## Files touched
- CHANGELOG.md
- docs/map/files-lib-2.md
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/lanes.py
- plugin/tests/test_lanes.py
