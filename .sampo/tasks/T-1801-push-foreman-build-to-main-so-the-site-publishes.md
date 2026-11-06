---
id: T-1801
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-27T22:50:16Z
updated: 2026-10-27T22:50:39Z
base: 235932b825c8d78d762cc02b2289cda28c8d6f15
base_tree: c7af71a1e20bf276a8c37a2380f7b2e65fa42ee6
plan0_at: 2026-10-27T22:50:17Z
plan0_scope: []
verified: strong
---
# Push foreman/build to main so the site publishes
## Raw request
> Push foreman/build to main so the site publishes
## Interpretation
Merge foreman/build into origin/main as a 'Merge foreman/build: …' commit and push, so the Pages site rebuilds; the user said yes in chat and in fm ask confirm.
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main has the pushed build commit and its exact tree — verify with `git fetch -q origin && git merge-base --is-ancestor e021641f origin/main && test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse e021641f^{tree})"`
- [x] the site deployed — verify with `gh run view 40597670042 --json conclusion --jq .conclusion | grep -qx success`
## Non-goals
## Approach (options → choice → why)
Gates on build HEAD; merge commit via git merge-tree + commit-tree (no checkout under the other sessions); push; watch Pages.
## Risks and rollback
## Execution prompt
## Steps
1. [x] verify push and deploy
## Resume here
## Docs impact
## Verification evidence
- (step 1) `git fetch -q origin && git merge-base --is-ancestor e021641f origin/main && test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse e021641f^{tree})" && gh run view 40597670042 --json conclusion --jq .conclusion | grep -qx success` → exit 0 · (no output) [ran] [tree 4fa4cbd0499c] (2026-10-27T22:50:24Z)
- (ac 1) `git fetch -q origin && git merge-base --is-ancestor e021641f origin/main && test "$(git rev-parse origin/main^{tree})" = "$(git rev-parse e021641f^{tree})"` → exit 0 · (no output) [ran] [tree 4fa4cbd0499c] (2026-10-27T22:50:26Z)
- (ac 2) `gh run view 40597670042 --json conclusion --jq .conclusion | grep -qx success` → exit 0 · (no output) [ran] [tree 4fa4cbd0499c] (2026-10-27T22:50:26Z)
- (audit edge) `self: merge tree == build tree (checked before commit-tree), no conflicts, pushed a5b5cf7e; full gates green on e021641f; helpers drops only fmsetup.ENV keys, which tests that need them pass explicitly; Pages deploy success` → a future key added to fmsetup.ENV is dropped from tests automatically, so it can't leak the same way [tree 4fa4cbd0499c] (2026-10-27T22:50:26Z)
- (audit self) `self: merge tree == build tree (checked before commit-tree), no conflicts, pushed a5b5cf7e; full gates green on e021641f; helpers drops only fmsetup.ENV keys, which tests that need them pass explicitly; Pages deploy success` → no findings [tree 4fa4cbd0499c] (2026-10-27T22:50:26Z)
## Log
- 2026-10-27T22:50:16Z created
- 2026-10-27T22:50:16Z redo of T-1791: takes over its start point and edited files
- 2026-10-27T22:50:17Z focused
- 2026-10-27T22:50:39Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1791 [FEATURE S, dropped, 3 steps] Push foreman/build to main so the site publishes
- T-1218 [CLEAN S, done, 1 steps] Release Foreman 1.2.35 and push to main so the Pages site publishes
- T-1322 [CLEAN S, done, 2 steps] fm release --push and fm pr name both ways to grant publishing: fm ask ID publish (the user's yes) and fm task set ID --allow publish whe…
- decision 2026-09-26: Released: fast-forwarded main 924fe06 → bd86fd6 (43 commits: T-0018 rounds 1-10, T-0036, T-0038, T-0039) and pushed main + foreman/build to origin
- similar finished tasks took 1–2 steps
## Lessons
- A user-wide env default changes every child process, including test suites: drop the session's own Claude Code env in test helpers when adding one
## Files touched
- plugin/tests/helpers.py
