---
id: T-1807
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T03:17:21Z
updated: 2026-10-28T03:21:38Z
base: d678abcf1f0397222ff16e03f35841121605e538
base_tree: 80c74128f069f7ea931ddae1508781e201c90dcf
plan0_at: 2026-10-28T03:17:21Z
plan0_scope: []
verified: strong
---
# Crash-hygiene tests fake git with a script: Ubuntu 26's copied sleep dies at once, a zombie with no cwd
## Raw request
> Crash-hygiene tests fake git with a script: Ubuntu 26's copied sleep dies at once, a zombie with no cwd
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the live-git tests pass with a script for git — verify with `cd plugin/tests && python3 -m unittest -q test_crash_hygiene`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] live_git writes a sh script named git (read on a pipe); tearDown closes pipes
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -W error::ResourceWarning -m unittest -q test_crash_hygiene` → exit 0 · Ran 19 tests in 4.273s / OK [ran] [tree ec1c0ccd540d] (2026-10-28T03:17:53Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_crash_hygiene` → exit 0 · Ran 19 tests in 4.283s / OK [ran] [tree ec1c0ccd540d] (2026-10-28T03:21:32Z)
- (audit edge) `self-review: the fake git is now /bin/sh running a script named git; comm is the script name (checked: comm=git, cwd as set, one thread); read blocks on the stdin pipe; tearDown's with-block closes the pipe and reaps; ResourceWarning as error: clean` → a zombie fake git would again pass the denied test but fail the cwd ones; a script can't be broken by how coreutils is built [tree ec1c0ccd540d] (2026-10-28T03:21:32Z)
- (audit intent) `self-review: the fake git is now /bin/sh running a script named git; comm is the script name (checked: comm=git, cwd as set, one thread); read blocks on the stdin pipe; tearDown's with-block closes the pipe and reaps; ResourceWarning as error: clean` → both CI ubuntu jobs stop failing these two tests; what they prove (a live git in the repo keeps the lock) is unchanged [tree ec1c0ccd540d] (2026-10-28T03:21:32Z)
- (audit self) `self-review: the fake git is now /bin/sh running a script named git; comm is the script name (checked: comm=git, cwd as set, one thread); read blocks on the stdin pipe; tearDown's with-block closes the pipe and reaps; ResourceWarning as error: clean` → no findings [tree ec1c0ccd540d] (2026-10-28T03:21:32Z)
## Log
- 2026-10-28T03:17:21Z created
- 2026-10-28T03:17:21Z focused
- 2026-10-28T03:17:54Z scope: plugin/tests/test_crash_hygiene.py only (live_git and tearDown)
- 2026-10-28T03:21:37Z done
- 2026-10-28T03:21:38Z committed d0243417 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- T-1799 [FIX M, done, 3 steps] CI green on ubuntu: runner-specific test failures fixed — lesson: marshal.dumps sets ref flags from refcounts: compare two code objects onl…
- research T-1405-review: Verdict:** approve with nits. I found no CRITICAL or HIGH defect. I read the code and tests in the worktree and ran nothing, because the tools I …
- decision 2026-10-21: Revert and drop T-1441 (auto-accepting Foreman's own plugins in the supply check)
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–4 steps
## Regression test
Red is CI only: check runs 122598572984 (3.12) and 122598572927 (3.14) on eba67050 fail test_a_stale_lock_with_a_live_git_in_the_repo_is_kept and test_a_git_in_a_subdirectory_of_the_repo_keeps_it (removed=True: the copied uutils sleep exits, its zombie has no cwd; the denied-mock test still passes, which pins it). Green: the same tests with a script for git, locally and on the next CI run.
## Why not caught
local coreutils is GNU: a copied sleep runs under any name; only Ubuntu 26's uutils build dies when copied, and T-1799's argv[0] fix assumed dispatch by argv[0]
## Lessons
- a fake process for a /proc test: a #! script gives the comm you want with no dependency on how coreutils was built
## Files touched
- plugin/tests/test_crash_hygiene.py
