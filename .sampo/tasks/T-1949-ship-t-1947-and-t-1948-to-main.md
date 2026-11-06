---
id: T-1949
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:49:36Z
updated: 2026-10-29T10:15:15Z
base: 00ca36e8209572704cdc47bb0c8cb1faeb1a3f7b
base_tree: bcb2c2e5f4e3b035d6f4b3155feb8ffd8588e1ad
plan0_at: 2026-10-29T09:49:45Z
plan0_scope: []
paused_tree: bcb2c2e5f4e3b035d6f4b3155feb8ffd8588e1ad
verified: ok
---
# ship T-1947 and T-1948 to main
## Raw request
> ship T-1947 and T-1948 to main
## Interpretation
Push the finished round-8 commits (T-1947 c46d3330, T-1948 00ca36e8) to main and confirm CI.
## Assumptions (confidence)
## Acceptance criteria
- [x] main holds T-1947 and T-1948 and CI is green — verify with `git fetch -q origin main && git log FETCH_HEAD --format=%s -n3 | grep -q T-1948`
## Non-goals
## Approach (options → choice → why)
fm ship naming both commits, the 3.12 suite as the test, --watch to dogfood T-1946 in the same job.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship the two commits with --watch
## Resume here
<!-- auto -->
- 2026-10-29T09:50:45Z step 1/1: fm ship the two commits with --watch
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/round9.txt
## Docs impact
## Verification evidence
- (ac 1) `git fetch -q origin main && git log FETCH_HEAD --format=%s -n3 | grep -q T-1948` → exit 0 · (no output) [ran] [tree e13fd27ddd43] (2026-10-29T10:14:30Z)
- (step 1) `git fetch -q origin main && git log FETCH_HEAD --format=%s -n3 | grep -q T-1948` → exit 0 · (no output) [ran] [tree e13fd27ddd43] (2026-10-29T10:14:30Z)
- (audit self) `self: fm ship tested 4173 tests on main's scratch tree, pushed 1769d1eb, and --watch read CI green on that sha (ship1949.txt)` → no findings [tree e13fd27ddd43] (2026-10-29T10:14:30Z)
## Log
- 2026-10-29T09:49:36Z created
- 2026-10-29T09:49:44Z guard authorization added: publish
- 2026-10-29T09:49:45Z focused
- 2026-10-29T09:50:53Z paused: focus moved to T-1953
- 2026-10-29T09:52:50Z publish grant used by fm ship
- 2026-10-29T10:15:15Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- T-1791 [FEATURE S, dropped, 3 steps] Push foreman/build to main so the site publishes
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmrelease.py
- plugin/skills/intake/references/execute.md
- plugin/skills/playbooks/references/perf/profiling.md
- plugin/tests/test_cli_ergonomics.py
- plugin/tests/test_ship.py
