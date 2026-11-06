---
id: T-1148
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-16T10:08:44Z
updated: 2026-10-16T10:15:38Z
base: 72f7222091b108cedef8858dc990bc200b5037a0
base_tree: d0b30fee36d6ff1acd5de669845ad6df53e04503
plan0_at: 2026-10-16T10:13:00Z
plan0_scope: [plugin/lib/fmbus.py, plugin/tests/test_claims.py, CHANGELOG.md]
verified: strong
---
# Fm lease take with a path relative to the repo root from a subdirectory records a doubled
## Raw request
> fm lease take with a path relative to the repo root from a subdirectory records a doubled path (mods/foreman-ui/mods/foreman-ui/...): resolve a target that doesn't exist from cwd but does from the repo root against the root
## Interpretation
A builder in mods/foreman-ui ran 'fm lease take mods/foreman-ui/tests/x.tsx'. The target was resolved against cwd and recorded as mods/foreman-ui/mods/foreman-ui/tests/x.tsx, a lease on nothing.
## Assumptions (confidence)
## Acceptance criteria
- [x] from a subdirectory, a repo-root-relative existing path is leased as itself, a cwd-relative one as before — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
In cmd_lease, a target that doesn't exist relative to cwd but does relative to the repo root resolves against the root. A target existing from cwd keeps the cwd meaning, and a new file keeps the cwd meaning.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Test then the root fallback in cmd_lease
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 16 tests in 5.7s (3 classes, 16 at a time; slowest: Claims 5s, ClaimsReview 5s, Stop 3s) / FAILED (1 classes) [ran] [tree 51937988b3bb] (2026-10-16T10:13:15Z)
- (step 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 5.3s (3 classes, 16 at a time; slowest: Claims 5s, ClaimsReview 5s, Stop 3s) / OK [ran] [tree 106ecfd4d51b] (2026-10-16T10:13:24Z)
- (step 1) `python3 plugin/tests/run.py test_claims test_bus` → exit 0 · Ran 31 tests in 11.0s (8 classes, 16 at a time; slowest: Watch 11s, Claims 11s, ClaimsReview 11s) / OK [ran] [tree 106ecfd4d51b] (2026-10-16T10:14:22Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 16 tests in 6.7s (3 classes, 16 at a time; slowest: Claims 7s, ClaimsReview 6s, Stop 4s) / OK [ran] [tree 5b1cb9774b3d] (2026-10-16T10:14:29Z)
- (audit self) `self review of the branch: the root fallback applies only when the target doesn't exist from cwd but does from the root; existing cwd-relative and new files keep the cwd meaning (tested); a new root-relative file still doubles (accepted, noted)` → no findings [tree 5b1cb9774b3d] (2026-10-16T10:14:29Z)
## Log
- 2026-10-16T10:08:44Z created
- 2026-10-16T10:09:44Z set scope=['plugin/lib/fmbus.py', 'plugin/tests/test_claims.py', 'CHANGELOG.md']
- 2026-10-16T10:12:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1148.builder.md
- 2026-10-16T10:13:00Z focused
- 2026-10-16T10:14:03Z merged worktree-agent-a669a6a082f5654fc (2 file(s))
- 2026-10-16T10:14:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a669a6a082f5654fc
- 2026-10-16T10:14:10Z focused
- 2026-10-16T10:14:22Z scope: CHANGELOG.md — release note
- 2026-10-16T10:15:36Z done
- 2026-10-16T10:15:38Z committed 6a87a2f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0774 [FIX S, done, 2 steps] Guard: heredoc python started by 'cd DIR && python3 -' resolves its relative open() targets in DIR only — lesson: a guard relaxation that t…
- T-1125 [FIX S, done, 1 steps] Guard false positive: a command 'cd ROOT && python3 heredoc writing CHANGELOG.md (relative — lesson: Before calling a guard block a false p…
- research wave2-plan-a4b64956d53d543cc: === T-1058 [stale: plugin/lib/fmbacktest.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py changed since it was written]
- decision 2026-10-15: Round 7 slate: 8 small reliability/delight builds (bare fm answers what now, close shows undo, demo ends in this repo, doctor state budget, night le…
- similar finished tasks took 1–2 steps
- likely tests for the scope: plugin/tests/test_bus.py
## Lessons
- Resolve a user's path the way they most likely meant it, and only where the other reading names nothing
## Plan gaps
- failed first: step 1 Test then the root fallback in cmd_lease
## Files touched
- plugin/tests/test_claims.py
- plugin/lib/fmbus.py
- CHANGELOG.md
