---
id: T-1156
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T10:45:53Z
updated: 2026-10-16T11:12:58Z
base: 5705a02c3170a483a5adc448cbeb820567b25259
base_tree: 38a44f64b3aa6c0af739cb8589a4ec5394f4b16d
plan0_at: 2026-10-16T10:48:11Z
plan0_scope: []
verified: strong
---
# Flag a live builder lane that shows no commit, worktree change or ledger event for N minut
## Raw request
> FEATURE: Flag a live builder lane that shows no commit, worktree change or ledger event for N minutes in `fm lane list` and `fm next`.
> DONE-WHEN: a test with a lane whose worktree mtime and ledger are older than N minutes sees it listed as stalled, and a lane with a fresh edit is not
## Interpretation
A builder lane whose agent is still live but whose worktree shows no file change, no new commit and no ledger event for N minutes (default 15) is a hang, not slow work: fm lane list marks it 'stalled N min' and fm next says which lane to check or stop.
## Assumptions (confidence)
## Acceptance criteria
- [x] a live lane with every signal older than N minutes is listed as stalled in fm lane list and named by fm next; a lane with a fresh edit, and a stopped lane, are not — verify with `python3 plugin/tests/run.py test_lane_stall`
## Non-goals
## Approach (options → choice → why)
Options: (a) in fmlanes, compare now with the newest of the worktree's file mtimes (tracked + untracked, not ignored), the branch head's commit time and the lane task's last ledger event; (b) watch the agent's transcript file; (c) a heartbeat file the builder writes. Choice: (a); why: needs nothing from the builder and stopped() already walks lanes (fmlanes.py:159-228). Stopped lanes keep their existing 'stopped' label; stalled is only for live ones.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_lane_stall.py): stale lane flagged with minutes; fresh edit not; stopped lane keeps its own label; fm next names the stalled lane
2. [x] The stall check in fmlanes, shown in fm lane list and fm next; threshold via an env or config default of 15 min
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_lane_stall` → ✗ exit 1 · Ran 2 tests in 5.6s (1 classes, 16 at a time; slowest: LaneStall 5s) / FAILED (1 classes) [ran] [tree 8eb135f02626] (2026-10-16T10:49:02Z)
- (step 1) `python3 plugin/tests/run.py test_lane_stall` → exit 0 · Ran 2 tests in 14.4s (1 classes, 16 at a time; slowest: LaneStall 14s) / OK [ran] [tree 6b10318db618] (2026-10-16T10:50:43Z)
- (step 2) `python3 plugin/tests/run.py test_lane_stall test_lanes` → exit 0 · Ran 32 tests in 39.2s (6 classes, 16 at a time; slowest: Lanes 39s, LaneStall 14s, BoardLanes 6s) / OK [ran] [tree 6b10318db618] (2026-10-16T10:51:23Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_stall test_lanes` → exit 0 · Ran 35 tests in 14.8s (6 classes, 16 at a time; slowest: LaneStall 15s, Lanes 10s, BoardLanes 1s) / OK [ran] [tree d6d80e75a71c] (2026-10-16T11:10:54Z)
- (ac 1) `python3 plugin/tests/run.py test_lane_stall` → exit 0 · Ran 5 tests in 16.0s (1 classes, 16 at a time; slowest: LaneStall 16s) / OK [ran] [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
- (audit intent) `reviewer: one fm-reviewer pass found builder_proc is the main session (returned/merged lanes read stalled forever) and per-turn cost; builder skipped merged/returned lanes, cut git timeouts to 10 s, cached 60 s, always emits stalled_min` → a hung builder is named, not mistaken for slow work [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
- (audit adversary) `reviewer: one fm-reviewer pass found builder_proc is the main session (returned/merged lanes read stalled forever) and per-turn cost; builder skipped merged/returned lanes, cut git timeouts to 10 s, cached 60 s, always emits stalled_min` → reads only; cache written via write_atomic in state dir [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
- (audit edge) `reviewer: one fm-reviewer pass found builder_proc is the main session (returned/merged lanes read stalled forever) and per-turn cost; builder skipped merged/returned lanes, cut git timeouts to 10 s, cached 60 s, always emits stalled_min` → FM_STALL_MIN<=0 means default; a fresh lane with no commits relies on the lane_merge event to tell merged from new [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
- (audit operator) `reviewer: one fm-reviewer pass found builder_proc is the main session (returned/merged lanes read stalled forever) and per-turn cost; builder skipped merged/returned lanes, cut git timeouts to 10 s, cached 60 s, always emits stalled_min` → one line with minutes and the resume command [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
- (audit maintainer) `reviewer: one fm-reviewer pass found builder_proc is the main session (returned/merged lanes read stalled forever) and per-turn cost; builder skipped merged/returned lanes, cut git timeouts to 10 s, cached 60 s, always emits stalled_min` → rows/lines zip replaced by an index loop [tree fd5f0476fbe0] (2026-10-16T11:11:22Z)
## Log
- 2026-10-16T10:45:53Z created
- 2026-10-16T10:47:51Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1156.builder.md
- 2026-10-16T10:48:11Z focused
- 2026-10-16T11:10:34Z merged worktree-agent-a0cbed74aa0302f08 (3 file(s))
- 2026-10-16T11:10:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0cbed74aa0302f08
- 2026-10-16T11:10:38Z focused
- 2026-10-16T11:11:05Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T11:12:58Z done
- 2026-10-16T11:12:58Z committed 41972ca (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- T-1106 [FIX S, done, 1 steps] - `fmtidy.unblocked` (fmtidy.py:118) has the same lane and fresh-clone mtime false positiv — lesson: mtime says when a file was written, no…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
## Lessons
- a liveness signal shared by every subagent (the main claude process) can't tell a returned builder from a running one; use the lane's own events
## Plan gaps
- failed first: step 1 Failing tests (test_lane_stall.py): stale lane flagged with minutes; fresh edit not; stopped lane k…
## Files touched
- plugin/tests/test_lane_stall.py
- plugin/lib/fmlanes.py
- plugin/lib/fmcli.py
- MASTER.md
- CHANGELOG.md
