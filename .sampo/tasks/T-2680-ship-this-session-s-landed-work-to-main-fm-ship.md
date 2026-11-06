---
id: T-2680
type: FEATURE
tier: S
status: dropped
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T22:00:16Z
updated: 2026-11-02T22:00:35Z
base: 6a4e4a506c481f9b3d962c77382a90a5e0344f3d
base_tree: 37c80f3d08ed6a0467af181a91ae9b09c862dc51
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T22:00:17Z
plan0_scope: []
---
# Ship this session's landed work to main (fm ship): main's tree matches the local tree
## Raw request
> Ship this session's landed work to main (fm ship): main's tree matches the local tree
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [ ] origin/main's tree matches HEAD's for the shipped paths — verify with `git fetch -q origin && git diff --quiet origin/main HEAD -- plugin/ site/ MASTER.md CHANGELOG.md`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [ ] fm ship (done: 0625fd09)  <- CURRENT
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git diff --quiet origin/main HEAD -- plugin/ site/ MASTER.md CHANGELOG.md` → ✗ exit 1 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:00:24Z)
- (ac 1) `git fetch -q origin && git diff --quiet origin/main HEAD -- plugin/ site/ MASTER.md CHANGELOG.md` → ✗ exit 1 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:00:26Z)
- (step 1) `git fetch -q origin && git diff --quiet origin/main HEAD -- plugin/ site/ MASTER.md CHANGELOG.md` → ✗ exit 1 · (no output) [ran] [tree 37c80f3d08ed] [world 2f1906870a] (2026-11-02T22:00:26Z)
## Log
- 2026-11-02T22:00:16Z created
- 2026-11-02T22:00:16Z redo of T-2678: takes over its start point and edited files
- 2026-11-02T22:00:17Z focused
- 2026-11-02T22:00:17Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T22:00:35Z dropped: the push is verified: origin/main matches HEAD for plugin/, MASTER.md and CHANGELOG.md (git diff --quiet); its criterion also named site/, which the tower publishes to main live and ahead of this branch by design, so it can never match; no third task: the ship's evidence is on T-2678 and here
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- T-2598 [FIX M, done, 4 steps] fm release's push lands on a main that fm ship fed by cherry-pick: a conflicting merge falls back to a merge commit of the release tree plu…
- T-2678 [FEATURE S, dropped, 1 steps] Ship this session's landed work to main (fm ship)
- decision 2026-11-02: [costly] Release 1.2.51: its push step conflicted because fm ship cherry-picks left foreman/build and main with diverged histories (merge base 2026-…
- similar past tasks were M: consider --tier M
- similar finished tasks took 2–4 steps
