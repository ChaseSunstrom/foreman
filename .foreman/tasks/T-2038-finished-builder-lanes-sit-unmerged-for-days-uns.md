---
id: T-2038
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T20:06:44Z
updated: 2026-10-29T22:55:24Z
base: db2109cd05c5cfb706d00028e31309977a7e221b
base_tree: 569c5a90c2c15e74fe08f264dab7dceb3c7528c0
plan0_at: 2026-10-29T22:43:29Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py, CHANGELOG.md]
verified: strong
---
# Finished builder lanes sit unmerged for days unseen: T-1670 and T-1784 each have a…
## Raw request
> FIX: finished builder lanes sit unmerged for days unseen: T-1670 and T-1784 each have a commit on their lane branch since 2026-10-23, yet SessionStart says 'Active: none', the queue is empty and fm next/drive never name them; a lane whose branch is ahead with a clean worktree should surface as 'merge it: fm lane merge ID'
## Interpretation
A builder lane whose branch is ahead of the main checkout's branch, with a clean tree and no commit for 30 minutes, is finished: fm next and the drive should name fm lane merge ID for it, and fm next should stop suggesting fm lane resume for it.
## Assumptions (confidence)
## Acceptance criteria
- [x] a clean, quiet lane ahead of main is named for merge, not resume; a dirty or fresh one isn't — verify with `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished`
## Non-goals
## Approach (options → choice → why)
Options: (1) a finished_lanes(p, briefs) helper in fmcore read by next_for, cmd_next and the drive; (2) a lane state file the builder writes on finishing (needs builder changes, misses old lanes); (3) only a doctor warning (not seen during work). Choice: 1, because it is derived from git, so it covers the already-stranded T-1670 and T-1784, and it costs no git call when no lane exists.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests for finished lanes
2. [x] finished_lanes in fmcore; next_for, cmd_next and the drive use it
## Resume here
<!-- auto -->
- 2026-10-29T22:45:19Z steps 2/2 done
- git: foreman/build; 5 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmhooks.py, plugin/tests/test_lanes.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/cl2038.json, CHANGELOG.md
## Docs impact
CHANGELOG.md
## Verification evidence
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished` → ✗ exit 1 · Ran 2 tests in 0.604s / FAILED (failures=1, errors=1) (start tree + this task's tests) [ran] [tree 6babf7bca8b6] (2026-10-29T22:43:45Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished` → ✗ exit 1 · Ran 2 tests in 0.472s / FAILED (failures=1, errors=1) [ran] [tree 6babf7bca8b6] (2026-10-29T22:43:45Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished` → ✗ exit 1 · Ran 2 tests in 0.600s / FAILED (failures=1, errors=1) (start tree + this task's tests) [ran] [tree 8fcea9920f71] (2026-10-29T22:44:01Z)
- `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished` → exit 0 · Ran 2 tests in 0.480s / OK [ran] [tree 8fcea9920f71] (2026-10-29T22:44:01Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished test_lanes.Lanes.test_the_drive_names_a_finished_lane_for_merge_once` → exit 0 · Ran 3 tests in 0.775s / OK [ran] [tree c3d12a1ef43c] (2026-10-29T22:44:46Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_drive_side` → exit 0 · Ran 43 tests in 16.344s / OK [ran] [tree c3d12a1ef43c] (2026-10-29T22:45:02Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_lanes test_drive_side` → exit 0 · Ran 45 tests in 25.827s / OK [ran] [tree c1aebdfa8184] (2026-10-29T22:48:48Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.1    30.8     150  [0] / SessionEnd                  25.1    26.8     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree c1aebdfa8184] (2026-10-29T22:52:19Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_lanes.Lanes.test_a_finished_lane_asks_for_a_merge_not_a_resume test_lanes.Lanes.test_a_dirty_or_fresh_lane_is_not_finished` → exit 0 · Ran 2 tests in 0.490s / OK [ran] [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
- (audit intent) `fm-reviewer pass (research T-2038-review): 5 findings verified and fixed test-first (cache, detached main, live builder, merged-lane test, ternary); full gate exit 0, 4269 tests` → next_for feeds SessionStart, prompts, the drive and the pane; a finished lane is named for merge in each, with no active task first [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
- (audit adversary) `fm-reviewer pass (research T-2038-review): 5 findings verified and fixed test-first (cache, detached main, live builder, merged-lane test, ternary); full gate exit 0, 4269 tests` → inputs are git output via _git (no shell, GIT_* stripped); nothing user-controlled reaches a command [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
- (audit edge) `fm-reviewer pass (research T-2038-review): 5 findings verified and fixed test-first (cache, detached main, live builder, merged-lane test, ternary); full gate exit 0, 4269 tests` → detached main uses the sha; timeouts fail closed; a live builder, dirty tree, fresh commit or merged lane is not named (tests) [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
- (audit operator) `fm-reviewer pass (research T-2038-review): 5 findings verified and fixed test-first (cache, detached main, live builder, merged-lane test, ternary); full gate exit 0, 4269 tests` → cached 60 s (FM_STALL_CACHE_S) keyed on main's sha and the lane set, so the pane's 2 s refresh costs no git and a merge clears it at once [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
- (audit maintainer) `fm-reviewer pass (research T-2038-review): 5 findings verified and fixed test-first (cache, detached main, live builder, merged-lane test, ternary); full gate exit 0, 4269 tests` → one function in fmcore beside stranded/andons; tests cover finished, dirty, fresh, live, merged and the cache [tree c1aebdfa8184] (2026-10-29T22:52:31Z)
## Log
- 2026-10-29T20:06:44Z created
- 2026-10-29T22:43:27Z set tier=M, scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmhooks.py', 'plugin/tests/test_lanes.py', 'CHANGELOG.md']
- 2026-10-29T22:43:28Z planned: it has criteria and steps
- 2026-10-29T22:43:28Z focused
- 2026-10-29T22:53:10Z done
- 2026-10-29T22:53:12Z committed 0a4b1aac (5 files)
- 2026-10-29T22:53:19Z guard authorization added: publish
- 2026-10-29T22:55:24Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- decision 2026-10-23: Pause the feature backlog (112 FEATURE items: 77 M, 34 S, 1 L) until weekly usage is back on pace; every FIX, SECURITY, PERFORMANCE and CLEAN item i…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-29): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py; re-ground the plan against them before editing
## Why not caught
nothing in fm next or the drive looked at lane branches that were ahead; stopped() only checked the builder process, so a finished lane read as stopped and said resume
## Lessons
- A status that polls git per item needs a cache keyed on what invalidates it (main's sha), or every pane tick pays for it
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
