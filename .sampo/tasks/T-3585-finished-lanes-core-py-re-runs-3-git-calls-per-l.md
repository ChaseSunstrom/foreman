---
id: T-3585
type: PERFORMANCE
tier: M
status: active
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T03:07:48Z
updated: 2026-11-07T03:30:20Z
lane: ~/.claude/foreman.lanes/T-3585
lane_branch: foreman/T-3585
base: 746ca71b53870cb530fb6a5b61ddf2324ec5760c
base_tree: 624d8cb4b78f002d60e7ad2565e20ee8f6a18b24
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-07T03:18:59Z
plan0_scope: []
---
# finished_lanes (core.py) re-runs 3 git calls per lane (~250 git processes at 83 lanes,…
## Raw request
> PERFORMANCE: finished_lanes (core.py) re-runs 3 git calls per lane (~250 git processes at 83 lanes, ~3 s wall) every time its 60 s cache expires, on whichever hook or fm next comes first (seen in UserPromptSubmit and fm ui profiles on a copy of the real state, T-3573): key the cache per lane on its HEAD/index mtimes instead of a 60 s TTL over the whole set
## Interpretation
Reading 1 (chosen): cut the git processes finished_lanes spawns per refresh by batching the per-lane questions and caching each lane's answer on its HEAD sha + main's sha, with output identical. Reading 2 (ruled out): only lengthen or restructure the 60 s TTL — the refresh would still spawn ~250 git processes, which is what pins the CPU.
## Assumptions (confidence)
## Acceptance criteria
- [ ] the batched finished_lanes returns the same ids as the per-lane version on a fixture repo with lanes ahead/merged/dirty/young, and spawns at most 3 + candidate git calls — verify with `nice -n 10 python3 plugin/tests/run.py test_finished_lanes_batch`
## Non-goals
## Approach (options → choice → why)
1) do less: a longer TTL only — likely outcome: rarer but identical 250-spawn bursts; fails if: any merge or new lane (key change) still triggers the full burst. 2) use what exists: the repo's _git runner and the existing finished.json cache, extended with a per-lane map — likely outcome: reuse, no new module. 3) cache keyed on HEAD/index mtimes — fails if: a file is edited or created without touching the index (status changes, mtimes don't), so the answer goes stale. 4) batch: one 'git worktree list --porcelain' for every lane's HEAD sha, one 'git log --no-walk' for uncached commit times, one 'git rev-list <tips> ^base' for which tips are ahead, per-lane cache keyed on sha+base; status --porcelain only for lanes passing quiet+ahead, TTL-cached as before — likely outcome: ≤3 + candidates spawns, 0 for unchanged lanes within TTL; fails if: a lane isn't in main's worktree list (then the old per-lane calls run for it). Choice 4 (85%), built on 2: same answers, bounded git spawns.
## Risks and rollback
## Execution prompt
## Steps
1. [ ] failing test: fixture repo with several lanes; compare against the old per-lane logic and count git spawns  <- CURRENT
2. [x] batch finished_lanes: worktree list + log --no-walk + rev-list, per-lane sha cache
3. [x] measure git spawns and CPU per call on the real repo before and after
## Resume here
## Docs impact
## Verification evidence
- (step 1) `nice -n 10 python3 plugin/tests/run.py test_finished_lanes_batch` → ✗ exit 1 · Ran 3 tests in 2.2s (1 jobs, 16 at a time; slowest: FinishedLanesBatch 1s) / FAILED (1 classes: test_finished_lanes_batch.FinishedLanesBatch) [ran] [tree 10522da79461] [world 2f1906870a] (2026-11-07T03:24:24Z)
- (step 2) `nice -n 10 python3 plugin/tests/run.py test_finished_lanes_batch test_lanes test_lane_stall` → exit 0 · Ran 221 tests in 85.3s (184 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 9s, LaneStall.test_a_live_lane_with_nothing_new_is_stalled_and_a_fresh_edit [ran] [tree 1628d8d16e43] [world 2f1906870a] (2026-11-07T03:28:09Z)
- (step 3) `nice -n 10 python3 /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad/t3585/measure.py ~/.claude/foreman.lanes/T-3585 30 1e-9` → exit 0 · first: 84 finished (ids hash -3698058674996663563), git spawns 91 {'rev-parse': 1, 'worktree': 1, 'log': 1, 'status': 88}, cpu git 2.31s self 0.05s, wall 4.22s / second (same lanes): 84 finished (ids [ran] [tree 1628d8d16e43] [world 2f1906870a] (2026-11-07T03:30:20Z)
## Log
- 2026-11-07T03:07:48Z created
- 2026-11-07T03:18:34Z planned: it has criteria and steps
- 2026-11-07T03:18:41Z lane: ~/.claude/foreman.lanes/T-3585 on foreman/T-3585
- 2026-11-07T03:18:57Z focused
- 2026-11-07T03:18:59Z predicted from its closes: 4 min, 1 attempt(s)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3580 [FEATURE M, active, 4 steps] PERFORMANCE fm ui (biggest live CPU cost, measured 2026-11-06): the UI pane runs fm ui…
- research rust-fast-path-design: Measured 2026-11-06 on this box (16 cores, load 5-18), niced, against a copy of the state
- T-3542 [PERFORMANCE M, active, 3 steps] The Sampo UI's fm ui --json starts about every 3 s and uses most of a core each time…
- decision 2026-11-05: T-3140's test cache is not merged now: the branch (c5970e7a) is kept and the task blocked; the speed goes after the slowest classes instead (T-3166 …
