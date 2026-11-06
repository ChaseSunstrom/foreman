---
id: T-2256
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T03:39:51Z
updated: 2026-10-31T03:40:34Z
base: 6d8e5f6432d26157c0d2b2e7efeec94eedcc18a6
base_tree: 9afca3ec4280d39d441ed984a917b752a5d42d81
plan0_at: 2026-10-31T03:39:52Z
plan0_scope: []
verified: strong
---
# Recover git after the interrupted T-2072 builder worktree (0-byte branch ref breaks fetch)
## Raw request
> Recover git after the interrupted T-2072 builder worktree (0-byte branch ref breaks fetch)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] git fetch origin main succeeds and fm lane list shows no missing lanes — verify with `git fetch -q origin main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] move the empty worktree and its 0-byte ref to the scratchpad, prune worktrees, free T-2072's lane
## Resume here
## Docs impact
none: operational
## Verification evidence
- (ac 1) `git fetch -q origin main` → exit 0 · (no output) [ran] [tree 9afca3ec4280] (2026-10-31T03:40:33Z)
- (step 1) `git fetch -q origin main` → exit 0 · (no output) [ran] [tree 9afca3ec4280] (2026-10-31T03:40:33Z)
- (audit edge) `self: the T-2072 builder's worktree creation was cut off when the session ended: a 0-byte branch ref (fetch refused it) and 2037 empty files; moved the folder, the ref and the stale lock into the scratchpad, pruned worktrees (the interrupted ship's /tmp scratch tree too), freed T-2072's lane; fetch works, fsck shows only dangling objects` → nothing lost: every file in the worktree was 0 bytes and the ref pointed nowhere; all moved, not deleted [tree 9afca3ec4280] (2026-10-31T03:40:33Z)
- (audit self) `self: the T-2072 builder's worktree creation was cut off when the session ended: a 0-byte branch ref (fetch refused it) and 2037 empty files; moved the folder, the ref and the stale lock into the scratchpad, pruned worktrees (the interrupted ship's /tmp scratch tree too), freed T-2072's lane; fetch works, fsck shows only dangling objects` → no findings [tree 9afca3ec4280] (2026-10-31T03:40:33Z)
## Log
- 2026-10-31T03:39:51Z created
- 2026-10-31T03:39:51Z focused
- 2026-10-31T03:40:31Z scope: .git refs and worktree admin only (moved aside to the scratchpad, not deleted); no source files
- 2026-10-31T03:40:34Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1943 [FEATURE M, done, 2 steps] Fm ship lands finished commits on the remote's main: fetch, scratch worktree at the fetche — lesson: git cherry matches by patch, so co…
- research T-2090-review: Verdict** — changes needed (two MEDIUM, both fixable in a few lines). I couldn't run the tests, since I only had read tools, so everything below …
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-09-27: Build the smarter-Foreman slate, and further self-improvement rounds, as a candidate in a git worktree (~/.claude/foreman-improve-20260926, branch i…
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
## Regression test
none: an operational repair of a git ref broken by an interrupted worktree creation; the check is git fetch succeeding
## Lessons
- An interrupted worktree creation leaves a 0-byte branch ref that breaks every fetch; check refs/heads for empty files when fetch says 'bad object'
