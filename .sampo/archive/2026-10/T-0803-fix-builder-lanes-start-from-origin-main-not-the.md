---
id: T-0803
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsetup.py, plugin/lib/fmdoctor.py, plugin/tests/test_setup.py, plugin/tests/test_doctor.py, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-14T16:14:11Z
updated: 2026-10-14T16:20:53Z
base: ac8480359a4b41ebf39457a944ad189d7521a6c0
base_tree: 1b9fa94e43dd2d984f28008b7b7b9b433422ca7d
verified: strong
---
# Builder lanes start from the branch being worked: Foreman's wiring sets worktree.baseRef to head
## Raw request
> FIX!: builder lanes start from origin/main, not the branch being worked: Claude Code's worktree.baseRef defaults to 'fresh' (remote default branch); Foreman's wiring should set worktree.baseRef='head' (CC 2.1.133) and fm doctor check it — today both T-0779 and T-0785 builders stopped on a diverged base (T-0379) and their worktrees were auto-removed
## Interpretation
Claude Code makes Agent isolation worktrees from worktree.baseRef, default 'fresh' (the remote's default branch, here origin/main 5 days behind foreman/build). Both builder lanes today started there, stopped on the diverged base (T-0379) and were auto-removed. worktree.baseRef 'head' (2.1.133) uses the local HEAD. Foreman's wiring (fmsetup.plan_install, which already adds outputStyle and env only when the user hasn't set them) sets it the same way and its uninstall removes only what it added; fm doctor WARNs when the effective value isn't head.
## Assumptions (confidence)
## Acceptance criteria
- [x] install wiring sets worktree.baseRef=head when unset, keeps a user's own value, and uninstall removes only its own; fm doctor warns when it isn't head — verify with `cd plugin/tests && python3 -m unittest test_setup test_doctor`
## Non-goals
## Approach (options → choice → why)
Options: a WorktreeCreate hook that runs git worktree add itself (replaces Claude Code's worktree logic; .worktreeinclude lost); tell builders to reset a fresh worktree (each lane pays a round trip, and an emptied worktree is auto-removed first); set the documented setting. Chose the setting.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing setup and doctor tests
2. [x] Wiring, uninstall, doctor check; apply on this machine; MASTER.md
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_setup.Install.test_builder_worktrees_start_from_head test_doctor.Checks.test_worktree_base` → ✗ exit 1 · Ran 2 tests in 0.057s / FAILED (errors=2) [ran] [tree 150cb11d80a7] (2026-10-14T16:17:12Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_setup test_doctor` → exit 0 · Ran 52 tests in 9.342s / OK [ran] [tree 76c083da820d] (2026-10-14T16:18:02Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_setup test_doctor` → exit 0 · Ran 52 tests in 9.519s / OK [ran] [tree 76c083da820d] (2026-10-14T16:18:12Z)
- `cd plugin/tests && python3 -m unittest test_setup.Install.test_builder_worktrees_start_from_head test_doctor.Checks.test_worktree_base` → ✗ exit 1 · Ran 2 tests in 0.185s / FAILED (errors=2) (start tree + this task's tests) [ran] [tree 76c083da820d] (2026-10-14T16:20:33Z)
- `cd plugin/tests && python3 -m unittest test_setup.Install.test_builder_worktrees_start_from_head test_doctor.Checks.test_worktree_base` → exit 0 · Ran 2 tests in 0.568s / OK [ran] [tree 76c083da820d] (2026-10-14T16:20:33Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_setup test_doctor` → exit 0 · Ran 52 tests in 17.516s / OK [ran] [tree 76c083da820d] (2026-10-14T16:20:51Z)
- (audit operator) `self: diff read; wiring adds worktree.baseRef=head only when unset (a user's value, even 'fresh', stays), records that it did, and uninstall removes only its own value and the worktree object only if it created it; doctor WARNs on anything but head` → fm install-user on this machine added it; a fresh isolation worktree then started at this branch's HEAD (ac84803) instead of origin/main [tree 76c083da820d] (2026-10-14T16:20:51Z)
- (audit self) `self: diff read; wiring adds worktree.baseRef=head only when unset (a user's value, even 'fresh', stays), records that it did, and uninstall removes only its own value and the worktree object only if it created it; doctor WARNs on anything but head` → no findings [tree 76c083da820d] (2026-10-14T16:20:51Z)
## Log
- 2026-10-14T16:14:11Z created
- 2026-10-14T16:14:56Z planned from capture
- 2026-10-14T16:17:01Z focused
- 2026-10-14T16:17:46Z scope: MASTER.md also gets T-0768's agent-frontmatter note (it shipped without one)
- 2026-10-14T16:18:12Z real path: after fm install-user, an Agent with isolation worktree started at ac84803 (this branch's HEAD) instead of origin/main cf39876
- 2026-10-14T16:20:52Z done
- 2026-10-14T16:20:53Z committed a0e801e (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0234-review-1: Verdict: changes needed.** One MEDIUM that can delete a branch `remove()` shouldn't, and one MEDIUM where the contract's "never close" is prose…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower. [stale: plugin/lib/fmcore.py…
- T-0779 [PERFORMANCE S, planned, 2 steps] Lane briefs pass a per-tier effort with the model
- decision 2026-10-04: T-0234 builder lanes: use Claude Code's Agent isolation worktree plus fm focus inside it, not fm lane's sibling folders
- likely tests for the scope: plugin/tests/test_doctor.py, plugin/tests/test_setup.py
## Lessons
- a lane flow that assumes the worktree starts at HEAD must pin that in settings, not trust the default
## Plan gaps
- failed first: step 1 Failing setup and doctor tests
## Files touched
- plugin/tests/test_setup.py
- plugin/tests/test_doctor.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmsetup.py
- MASTER.md
