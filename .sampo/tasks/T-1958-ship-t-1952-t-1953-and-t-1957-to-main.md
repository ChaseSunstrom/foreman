---
id: T-1958
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T10:14:02Z
updated: 2026-10-29T10:38:29Z
base: 735fb29e30d45955e24a32e343cfb7f866c5225d
base_tree: e13fd27ddd437fa4e3a1ba742154ae6f3ee8d988
plan0_at: 2026-10-29T10:14:07Z
plan0_scope: []
paused_tree: e13fd27ddd437fa4e3a1ba742154ae6f3ee8d988
verified: strong
---
# ship T-1952, T-1953 and T-1957 to main
## Raw request
> ship T-1952, T-1953 and T-1957 to main
## Interpretation
Land the round 9 and 10 commits on main behind the publish grant.
## Assumptions (confidence)
## Acceptance criteria
- [x] main has the three commits and CI is green — verify with `git fetch -q origin main && git log FETCH_HEAD --format=%s -n5 | grep -q T-1957`
## Non-goals
## Approach (options → choice → why)
fm ship with no shas (it starts after refs/foreman/shipped) and the 3.12 suite as --test, which T-1953 now remembers; --watch for CI. Rejected: raw git push (skips the scratch-tree test).
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship the three commits with --watch
## Resume here
<!-- auto -->
- 2026-10-29T10:15:57Z step 1/1: fm ship the three commits with --watch
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/round11.txt
## Docs impact
## Verification evidence
- (ac 1) `git fetch -q origin main && git log FETCH_HEAD --format=%s -n5 | grep -q T-1957` → exit 0 · (no output) [ran] [tree 53f59661335e] (2026-10-29T10:36:40Z)
- (step 1) `fm ship --check 3931eea0 443d9271 735fb29e` → exit 0 · origin main has the changes of 3931eea0, 443d9271, 735fb29e [ran] [tree 53f59661335e] (2026-10-29T10:36:40Z)
- (audit edge) `self: fm ship pushed the three commits at 805f5cf after the suite passed in the scratch tree (4180 OK) and CI went green on that commit; fm ship --check confirms main has each by patch` → CI watched the exact pushed commit, not main's tip [tree 53f59661335e] (2026-10-29T10:36:40Z)
- (audit self) `self: fm ship pushed the three commits at 805f5cf after the suite passed in the scratch tree (4180 OK) and CI went green on that commit; fm ship --check confirms main has each by patch` → no findings [tree 53f59661335e] (2026-10-29T10:36:40Z)
## Log
- 2026-10-29T10:14:02Z created
- 2026-10-29T10:14:06Z guard authorization added: publish
- 2026-10-29T10:14:07Z focused
- 2026-10-29T10:17:24Z publish grant used by fm ship
- 2026-10-29T10:17:59Z paused: focus moved to T-1962
- 2026-10-29T10:38:29Z done
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
- plugin/lib/fmcore.py
- plugin/lib/fmhooks.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrelease.py
- plugin/tests/test_check_paths.py
- plugin/tests/test_cli_ergonomics.py
- plugin/tests/test_round_f.py
- plugin/tests/test_ship.py
