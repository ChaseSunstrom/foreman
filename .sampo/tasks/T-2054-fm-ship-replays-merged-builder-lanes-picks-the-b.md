---
id: T-2054
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T21:10:41Z
updated: 2026-10-29T21:18:51Z
base: 359406608fa48718797644000ed847668cf7d388
base_tree: cc7cd12f7a01ac85ed8789bc6bb1c2cf0e02a151
plan0_at: 2026-10-29T21:10:42Z
plan0_scope: []
verified: strong
---
# fm ship replays merged builder lanes: picks the branch's first-parent chain after the last ship (merges with -m 1) when main still matches it, since a lane commit doesn't cherry-pick alone
## Raw request
> fm ship replays merged builder lanes: picks the branch's first-parent chain after the last ship (merges with -m 1) when main still matches it, since a lane commit doesn't cherry-pick alone
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a plain fm ship lands a merged lane whose merge resolved a conflict — verify with `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: a lane commit that conflicts alone ships through its merge
2. [x] first-parent picks after the shipped ref when main's tree matches it; merges with -m 1
## Resume here
<!-- auto -->
- 2026-10-29T21:12:38Z steps 2/2 done
- git: foreman/build; 3 uncommitted: plugin/lib/fmcli.py, plugin/lib/fmrelease.py, plugin/tests/test_ship.py
- touched since last checkpoint: plugin/tests/test_ship.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ship2054.json, plugin/lib/fmrelease.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/ship2054b.json, plugin/lib/fmcli.py
## Docs impact
plugin/lib/fmcli.py
## Verification evidence
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship.Ship.test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Ship 0s) / FAILED (1 classes) [ran] [tree a76a35f65b08] (2026-10-29T21:10:57Z)
- (step 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship.Ship.test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Ship 0s) / OK [ran] [tree 6fa1cdb751f2] (2026-10-29T21:11:41Z)
- (step 2) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship test_which` → exit 0 · Ran 33 tests in 9.3s (4 classes, 16 at a time; slowest: Ship 9s, Which 2s, Snapshots 0s) / OK [ran] [tree 6fa1cdb751f2] (2026-10-29T21:11:50Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmrelease.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 war; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                28.9    31.7     150  [0] / SessionEnd                  25.0    26.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree 6fa1cdb751f2] (2026-10-29T21:15:18Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship.Ship.test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge` → ✗ exit 1 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Ship 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6fa1cdb751f2] (2026-10-29T21:15:37Z)
- `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship.Ship.test_a_merged_lane_whose_merge_settled_a_conflict_ships_through_the_merge` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Ship 0s) / OK [ran] [tree 6fa1cdb751f2] (2026-10-29T21:15:37Z)
- (ac 1) `~/.local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12 plugin/tests/run.py test_ship` → exit 0 · Ran 17 tests in 9.3s (1 classes, 16 at a time; slowest: Ship 9s) / OK [ran] [tree 6fa1cdb751f2] (2026-10-29T21:15:59Z)
- (audit edge) `self: read the diff; replay only when main's tree equals the shipped ref (diff --quiet; an error code falls back to git cherry), merges picked with -m 1 against the branch side; full gates 4264 OK; proved red then green` → a merge whose first-parent diff is empty would stop the cherry-pick with a clear 'nothing was pushed' error, never a bad push; main moved since the last ship falls back to git cherry as before [tree 6fa1cdb751f2] (2026-10-29T21:15:59Z)
- (audit adversary) `self: read the diff; replay only when main's tree equals the shipped ref (diff --quiet; an error code falls back to git cherry), merges picked with -m 1 against the branch side; full gates 4264 OK; proved red then green` → no new input reaches git: picks come from rev-list on our own refs; the push still re-checks main and needs the task's publish grant [tree 6fa1cdb751f2] (2026-10-29T21:15:59Z)
- (audit self) `self: read the diff; replay only when main's tree equals the shipped ref (diff --quiet; an error code falls back to git cherry), merges picked with -m 1 against the branch side; full gates 4264 OK; proved red then green` → no findings [tree 6fa1cdb751f2] (2026-10-29T21:15:59Z)
## Log
- 2026-10-29T21:10:41Z created
- 2026-10-29T21:10:42Z focused
- 2026-10-29T21:16:21Z done
- 2026-10-29T21:16:23Z committed 16e394ce (3 files)
- 2026-10-29T21:16:29Z guard authorization added: publish
- 2026-10-29T21:18:51Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-1945 [FEATURE S, done, 0 steps] Fm ship remembers the last commit it shipped (a ref under refs/foreman/) and its default p
- T-1948 [FEATURE S, done, 3 steps] fm ship remembers what it shipped and can watch CI
- decision 2026-10-16: T-1069 self-approved under full autonomy: a race clones the brief as a 'b' task so each builder works under its own id; pick merges the winner throu…
- similar finished tasks took 0–3 steps
## Lessons
- A merged lane's own commit can't be cherry-picked alone when its merge settled a conflict; ship the branch's first-parent steps instead
## Plan gaps
- failed first: step 1 failing test: a lane commit that conflicts alone ships through its merge
## Files touched
- plugin/tests/test_ship.py
- plugin/lib/fmrelease.py
- plugin/lib/fmcli.py
