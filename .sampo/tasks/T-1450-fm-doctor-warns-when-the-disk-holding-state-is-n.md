---
id: T-1450
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T05:50:55Z
updated: 2026-10-22T13:52:39Z
base: aadaec26a744063e786fe993a7f10004c5c6ac32
base_tree: dec137b9dcd987b11fe4550ce073beeb4ef55887
plan0_at: 2026-10-22T13:50:47Z
plan0_scope: [plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py, CHANGELOG.md]
verified: strong
---
# Doctor warns before the disk fills
## Raw request
> fm doctor warns when the disk holding state/ is nearly full (under ~5% or 10 GB free) and names the biggest builder worktrees under known projects' .claude/worktrees (volt 17 = 8.3 GB, gitter 4 = 4.6 GB) so a full disk is caught before hooks fail (ENOSPC 2026-10-22)
## Interpretation
The disk filled at 04:00 on 2026-10-22 and hooks failed with ENOSPC; nothing warned. Doctor should warn when the disk holding state/ is low and say where builder worktrees pile up.
## Assumptions (confidence)
## Acceptance criteria
- [x] low free space warns and names the worktree counts; plenty passes — verify with `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_low_disk_warns`
## Non-goals
## Approach (options → choice → why)
check_disk: shutil.disk_usage(state_dir); WARN under 5% or 10 GB free, naming known projects' .claude/worktrees counts (cheap listdir, no du). Options considered: du sizes (slow on build trees), auto-pruning lanes (destructive, other sessions' work) → counts only.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] check_disk in fmdoctor, wired into the run
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_low_disk_warns` → ✗ exit 1 · Ran 1 test in 0.001s / FAILED (errors=1) [ran] [tree 832140a13524] (2026-10-22T13:50:48Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_low_disk_warns` → exit 0 · Ran 1 test in 0.001s / OK [ran] [tree d8d66f68f49d] (2026-10-22T13:50:54Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_doctor.Checks.test_low_disk_warns` → exit 0 · Ran 1 test in 0.001s / OK [ran] [tree 5e9fa3c07357] (2026-10-22T13:51:41Z)
- (audit edge) `self: check_disk reads shutil.disk_usage on the state dir; WARN under 10 GB or 5% free; names up to 5 projects' .claude/worktrees counts via listdir (no du). Live: WARN 26 GB free (3%), volt 17, gitter 3, foreman 2. test_doctor green.` → disk_usage OSError → PASS 'not measured'; a project folder gone or unreadable is skipped [tree 5e9fa3c07357] (2026-10-22T13:51:41Z)
- (audit operator) `self: check_disk reads shutil.disk_usage on the state dir; WARN under 10 GB or 5% free; names up to 5 projects' .claude/worktrees counts via listdir (no du). Live: WARN 26 GB free (3%), volt 17, gitter 3, foreman 2. test_doctor green.` → points at git worktree list / fm lane rm; never deletes other sessions' worktrees itself [tree 5e9fa3c07357] (2026-10-22T13:51:41Z)
- (audit self) `self: check_disk reads shutil.disk_usage on the state dir; WARN under 10 GB or 5% free; names up to 5 projects' .claude/worktrees counts via listdir (no du). Live: WARN 26 GB free (3%), volt 17, gitter 3, foreman 2. test_doctor green.` → no findings [tree 5e9fa3c07357] (2026-10-22T13:51:41Z)
## Log
- 2026-10-22T05:50:55Z created
- 2026-10-22T05:56:15Z planned from capture
- 2026-10-22T13:50:43Z focused
- 2026-10-22T13:52:38Z done
- 2026-10-22T13:52:39Z committed e78d770b (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0785 [FEATURE S, done, 2 steps] fm doctor names the Foreman features the installed Claude Code is too old for — lesson: a probe for a setting must look where Foreman w…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- research T-0296-review-1: Verdict:** approve with nits. I found no HIGH findings. I read the diff and `fmcore`'s `find_project`/`routing` but did not run any tests. [sta…
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- likely tests for the scope: plugin/tests/test_doctor.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmdoctor.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/lib/fmdoctor.py
- plugin/tests/test_doctor.py
- CHANGELOG.md
