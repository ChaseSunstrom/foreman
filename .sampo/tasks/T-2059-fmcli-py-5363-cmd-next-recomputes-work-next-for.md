---
id: T-2059
type: PERFORMANCE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T22:46:38Z
updated: 2026-10-31T00:39:20Z
lane_branch: worktree-agent-a95989947824687a0
base: fcfb2e78586fba67e25e7bee4548611b1d1fc732
base_tree: fa96709da4f5d7b33564826f81709bc3342fc7ce
plan0_at: 2026-10-31T00:36:57Z
plan0_scope: []
---
# fmcli.py:5363` `cmd_next` recomputes work `next_for` already did (finished lanes), and…
## Raw request
> fmcli.py:5363` `cmd_next` recomputes work `next_for` already did (finished lanes), and the same duplication may exist for `stalled` and `stopped
> (noticed by an agent; research T-2038-review)
## Interpretation
fm next (fmcli.cmd_next) calls c.next_for, which already computes finished_lanes, then computes finished_lanes again and also fmlanes.stopped and fmlanes.stalled. fm next runs every turn, so duplicate lane scans cost on every turn in every session.
## Assumptions (confidence)
## Acceptance criteria
- [ ] fm next scans finished, stopped and stalled lanes once each per call, with unchanged output — verify with `cd plugin/tests && python3 -m unittest -q test_next.NextLaneScans`
## Non-goals
## Approach (options → choice → why)
Options: (1) next_for returns the lane facts it computed (finished, stopped, stalled) with its answer, and cmd_next reuses them; (2) memoize finished_lanes per process (stale across a long-lived process like fm serve); (3) leave it (it runs every turn). Choice 1, measured first: time fm next on this project before and after, and keep the change only if it saves.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] time fm next before; red test counting lane scans (mocks)  <- CURRENT
2. [x] next_for hands its lane facts to cmd_next; time after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_next.NextLaneScans` → ✗ exit 1 · Ran 1 test in 0.292s / FAILED (failures=1) [ran] [tree b14f987bf89d] (2026-10-31T00:37:35Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_next.NextLaneScans test_nudges.OneLoad` → exit 0 · Ran 3 tests in 1.352s / OK [ran] [tree 6b158636ab12] (2026-10-31T00:37:46Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_core test_guard_cases test_next test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [23.36s] [ran] [tree 6b158636ab12] (2026-10-31T00:38:55Z)
## Log
- 2026-10-29T22:46:38Z created
- 2026-10-31T00:36:29Z planned: it has criteria and steps
- 2026-10-31T00:36:29Z set tier=S, type=PERFORMANCE, approved=True
- 2026-10-31T00:36:43Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2059.builder.md
- 2026-10-31T00:36:57Z focused
- 2026-10-31T00:39:20Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a95989947824687a0 (branch worktree-agent-a95989947824687a0 kept: not merged); dropped: measured: no saving (the second call hits a 60 s cache); dropped by decision
- 2026-10-31T00:39:20Z dropped: measured, no saving: the duplicate finished_lanes call hits its 60 s cache; median fm next 0.205 s before vs 0.229 s after (noise); decided in decisions.md
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-2038-review: Verdict: approve with nits.** The acceptance tests cover the two stated behaviours: a clean, quiet lane that is ahead gets a merge line, and a di…
- research T-2138-review: Verdict: approve with nits.** The gate does what the acceptance criterion says. I did not run the tests. The nits below are scope and test gaps, …
- research T-2146-review: Changes needed. These are two small, cheap fixes, not a redesign. [stale: plugin/lib/fmhooks.py, plugin/lib/fmrecall.py, plugin/tests/test_hooks.…
- decision 2026-10-16: Recommendation: build the slate T-1042..T-1053 plus T-1028 widened (recorded in research brainstorm-20261016-catalogue); the user then asked for eve…
