---
id: T-1003
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T00:29:41Z
updated: 2026-10-16T01:02:49Z
base: e62fc86df1629815709a89a25de27bbaf49a0df0
base_tree: 758fb56f326eff508fce203720490a5ac79e5f3c
verified: strong
---
# Fleet drops a killed session even after a later SessionStart swept its by-pid records
## Raw request
> Fleet still lists killed sessions when their by-pid records were swept by a later SessionStart: the statusline snapshot should carry its own claude pid and start time, and live() check that
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a session snapshot whose recorded claude pid is dead (or reused) is not live, with no by-pid record left — verify with `python3 plugin/tests/run.py test_bus`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: snapshot with a dead pid and no by-pid entry still listed by fmbus.live()
2. [x] statusline snapshot records its claude pid and start; live() drops a snapshot whose process is gone
3. [x] docs: CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_bus` → ✗ exit 1 · Ran 15 tests in 10.1s (5 classes, 16 at a time; slowest: Watch 10s, Approvals 5s, Conductor 4s) / FAILED (1 classes) [ran] [tree 73d7fabee9d5] (2026-10-16T00:56:28Z)
- (step 2) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 15 tests in 10.0s (5 classes, 16 at a time; slowest: Watch 10s, Approvals 5s, Conductor 4s) / OK [ran] [tree 498a4e4de444] (2026-10-16T00:56:46Z)
- (ac 1) `python3 plugin/tests/run.py test_bus test_statusline_ui` → exit 0 · Ran 21 tests in 5.6s (6 classes, 16 at a time; slowest: Watch 6s, Approvals 4s, Conductor 2s) / OK [ran] [tree 3b2337f3c32f] (2026-10-16T01:02:25Z)
- (step 3) `grep -q 'T-1003' CHANGELOG.md` → exit 0 · (no output) [ran] [tree d0ae48532fa7] (2026-10-16T01:02:37Z)
- (audit edge) `self` → a live statusline run records this session's claude pid (8019, comm claude); older snapshots without a pid stay live; a reused pid (start differs) and a dead one drop (test); /proc walk wrapped so the line never fails [tree d0ae48532fa7] (2026-10-16T01:02:37Z)
- (ac 1) `python3 plugin/tests/run.py test_bus` → exit 0 · Ran 15 tests in 5.5s (5 classes, 16 at a time; slowest: Watch 5s, Approvals 4s, Conductor 2s) / OK [ran] [tree d0ae48532fa7] (2026-10-16T01:02:47Z)
- (audit edge) `builder branch read in full; merged; verified a real statusline run records the claude pid; test_bus and test_statusline_ui green` → no-pid snapshots stay live; dead or reused pid drops; statusline never fails on the lookup [tree d0ae48532fa7] (2026-10-16T01:02:47Z)
- (audit self) `builder branch read in full; merged; verified a real statusline run records the claude pid; test_bus and test_statusline_ui green` → no findings [tree d0ae48532fa7] (2026-10-16T01:02:47Z)
## Log
- 2026-10-16T00:29:41Z created
- 2026-10-16T00:54:59Z planned from capture
- 2026-10-16T00:55:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1003.builder.md
- 2026-10-16T00:56:05Z focused
- 2026-10-16T01:02:19Z merged worktree-agent-a8def862ba0c0338f (3 file(s))
- 2026-10-16T01:02:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8def862ba0c0338f
- 2026-10-16T01:02:19Z focused
- 2026-10-16T01:02:48Z done
- 2026-10-16T01:02:49Z committed 32d6e2a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0323-review: Changes needed. No path-traversal hole found. Stop, hand-off and the message path have real defects. [stale: plugin/lib/fmcli.py, plugin/lib/fmse…
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- T-0938 [FIX M, done, 3 steps] Pane stays put: volatile cards hold their height and linger instead of popping in and out — lesson: Layout stability is a time property: te…
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
## Why not caught
T-1001's test seeded by-pid records for the killed session, so it never covered a later SessionStart sweeping them
## Plan gaps
- failed first: step 1 red test: snapshot with a dead pid and no by-pid entry still listed by fmbus.live()
## Files touched
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- plugin/hooks/statusline
- CHANGELOG.md
