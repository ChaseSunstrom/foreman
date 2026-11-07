---
id: T-3549
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-07T00:22:41Z
updated: 2026-11-07T00:22:53Z
base: e63c58d588ed3a212cc0f8e48f7d1632af267c26
base_tree: 62a07cb21d4238a322f1d7ca88f651169a897e0f
predict_minutes: 1
predict_attempts: 1
plan0_at: 2026-11-07T00:22:43Z
plan0_scope: []
verified: ok
---
# Remove the untracked scripts/probe-plugin-rename.sh from the main checkout: T-2879's lane commits it, and untracked it blocks the train's fast-forward and every close's reuse of the train's pass
## Raw request
> Remove the untracked scripts/probe-plugin-rename.sh from the main checkout: T-2879's lane commits it, and untracked it blocks the train's fast-forward and every close's reuse of the train's pass
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the main checkout has no untracked scripts/ folder — verify with `test ! -e ~/.claude/foreman/scripts`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] remove it (T-2879 carries the committed copy)
## Resume here
## Docs impact
none: an untracked file
## Verification evidence
- (step 1) `test ! -e ~/.claude/foreman/scripts` → exit 0 · (no output) [ran] [tree 9ced726d6854] [world 2f1906870a] (2026-11-07T00:22:46Z)
- (ac 1) `test ! -e ~/.claude/foreman/scripts` → exit 0 · reused: the same command passed on this tree and world at 2026-11-07T00:22:46Z [ran] [tree 9ced726d6854] [world 2f1906870a] (2026-11-07T00:22:48Z)
- (audit self) `self: the file is committed in T-2879's lane and copied to foreman.backups before removal` → pass [tree 9ced726d6854] (2026-11-07T00:22:48Z)
## Log
- 2026-11-07T00:22:41Z created
- 2026-11-07T00:22:42Z focused
- 2026-11-07T00:22:43Z predicted from its closes: 1 min, 1 attempt(s)
- 2026-11-07T00:22:53Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3380 [FEATURE M, done, 4 steps] Merge train: sampo lane train merges N reviewed lanes in a scratch integration worktree, runs the full gates once, bisects a red set to…
- T-3119 [PERFORMANCE M, planned, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-3141 [PERFORMANCE M, done, 2 steps] Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge …
- decision 2026-11-02: [outward] Release 1.2.51 finished by hand after fm release refused a fresh run (version already bumped) and its checkpoints were abandoned: pushed t…
## Lessons
- An untracked file in the main checkout changes its code tree, so every reuse of a gate pass misses; nothing should stay untracked there.
## Files touched
- scripts/probe-plugin-rename.sh
