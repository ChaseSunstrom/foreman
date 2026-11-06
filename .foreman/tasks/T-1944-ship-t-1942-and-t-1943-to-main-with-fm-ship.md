---
id: T-1944
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-29T09:25:51Z
updated: 2026-10-29T09:29:06Z
base: eae4fd38db80b5d2f725cea45aa7bd43cf3473c3
base_tree: 3a9f2c759fe2f83aaddcb0f49f854bbdb4ac45e1
plan0_at: 2026-10-29T09:25:51Z
plan0_scope: []
verified: strong
---
# Ship T-1942 and T-1943 to main with fm ship
## Raw request
> Ship T-1942 and T-1943 to main with fm ship
## Interpretation
Push T-1942 (aba6065e) and T-1943 (eae4fd38) to main by dogfooding fm ship.
## Assumptions (confidence)
## Acceptance criteria
- [x] main holds both commits — verify with `git fetch -q origin main && git log FETCH_HEAD --format=%s -n5 | grep -q T-1943`
## Non-goals
## Approach (options → choice → why)
Name both commits (git cherry also lists older playbook commits that landed through a merge), test with the 3.12 suite in the scratch tree.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm ship aba6065e eae4fd38 with the 3.12 suite as the test
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin main && git log FETCH_HEAD --format=%s -n5 | grep -q T-1943` → exit 0 · (no output) [ran] [tree 3a9f2c759fe2] (2026-10-29T09:29:04Z)
- (ac 1) `git fetch -q origin main && git log FETCH_HEAD --format=%s -n5 | grep -q T-1943` → exit 0 · (no output) [ran] [tree 3a9f2c759fe2] (2026-10-29T09:29:05Z)
- (audit edge) `dogfooded fm ship on the real repo: both commits cherry-picked onto fetched main, 3.12 suite green there (4170 tests), main re-checked, pushed, grant spent` → git cherry listed 7 older playbook commits that landed through a merge; naming the two commits shipped only them [tree 3a9f2c759fe2] (2026-10-29T09:29:05Z)
- (audit self) `dogfooded fm ship on the real repo: both commits cherry-picked onto fetched main, 3.12 suite green there (4170 tests), main re-checked, pushed, grant spent` → no findings [tree 3a9f2c759fe2] (2026-10-29T09:29:05Z)
## Log
- 2026-10-29T09:25:51Z created
- 2026-10-29T09:25:51Z focused
- 2026-10-29T09:25:59Z guard authorization added: publish
- 2026-10-29T09:25:59Z focused
- 2026-10-29T09:28:53Z publish grant used by fm ship
- 2026-10-29T09:29:06Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- T-1150 [RESEARCH M, done, 3 steps] Forever loop round 2: brainstorm past everything shipped through 1.2.32, ground every idea, queue what's real — lesson: one grounding …
- T-0366 [FIX M, done, 3 steps] Ship T-0364 to JARVIS: merge its 2 local commits into main, bump plugin to 1.2.0, refresh its plugin cache — lesson: A directory-marketplac…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–3 steps
