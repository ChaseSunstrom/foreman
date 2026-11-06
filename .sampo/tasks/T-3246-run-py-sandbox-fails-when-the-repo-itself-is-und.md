---
id: T-3246
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/sandbox.py, plugin/tests/run.py, plugin/tests/test_sandbox.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-05T21:10:42Z
updated: 2026-11-05T23:56:04Z
base: a4f92e3e75937e73d3af196e96757a2f3c60fe71
base_tree: 2e9de6aaadaa7b9242913a404e52551dec50bb01
predict_minutes: 3
predict_attempts: 1
plan0_at: 2026-11-05T21:10:43Z
plan0_scope: [plugin/lib/sampo/sandbox.py, plugin/tests/run.py, plugin/tests/test_sandbox.py, CHANGELOG.md]
verified: strong
unproven: [red]
---
# run.py --sandbox fails when the repo itself is under /tmp (sampo ship's scratch tree): the job's fresh /tmp hides it and bwrap can't chdir; bind what a job reads from under /tmp or /run back read-only
## Raw request
> run.py --sandbox fails when the repo itself is under /tmp (sampo ship's scratch tree): the job's fresh /tmp hides it and bwrap can't chdir; bind what a job reads from under /tmp or /run back read-only
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a job whose working folder or read paths sit under /tmp gets them bound back read-only, so run.py --sandbox works from a repo under /tmp — verify with `python3 plugin/tests/run.py test_sandbox`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: argv binds back a cwd and a read path under /tmp; run.py --sandbox runs a class from a repo copy under /tmp
2. [x] argv(reads=...) and run.py's sandboxed() passing the repo
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_sandbox.RepoUnderTmp` → ✗ exit 1 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: RepoUnderTmp 0s) / FAILED (1 classes: test_sandbox.RepoUnderTmp) [ran] [tree 231ac423393f] [world 2f1906870a] (2026-11-05T21:10:54Z)
- (step 2) `python3 plugin/tests/run.py test_sandbox test_run` → exit 0 · Ran 126 tests in 4.8s (57 jobs, 16 at a time; slowest: Ship 4s, Hang.test_a_class_that_hangs_is_killed_and_named_with_its_stack 4s, Hang.test_the_run_deadline_kills_a_running_class_and_skips_unstarted [ran] [tree b9d640ddb73a] [world 2f1906870a] (2026-11-05T21:11:48Z)
- `python3 plugin/tests/run.py test_sandbox.RepoUnderTmp` → ✗ exit 1 · Ran 1 tests in 1.7s (1 jobs, 16 at a time; slowest: RepoUnderTmp 0s) / FAILED (1 classes: test_sandbox.RepoUnderTmp) (start tree + this task's tests) [ran] [tree 261da8f1a1f7] [world 2f1906870a] (2026-11-05T21:11:51Z)
- `python3 plugin/tests/run.py test_sandbox.RepoUnderTmp` → exit 0 · Ran 1 tests in 0.5s (1 jobs, 16 at a time; slowest: RepoUnderTmp 0s) / OK [ran] [tree 261da8f1a1f7] [world 2f1906870a] (2026-11-05T21:11:51Z)
- (ac 1) `python3 plugin/tests/run.py test_sandbox` → exit 0 · Ran 36 tests in 1.5s (9 jobs, 16 at a time; slowest: SessionTier 1s, AllowTier 1s, JobTier 1s) / OK [ran] [tree 261da8f1a1f7] [world 2f1906870a] (2026-11-05T21:11:53Z)
- (audit intent) `self: argv binds back read-only each home, read path and the working folder that sits under the fresh /tmp or /run, unless it's already a writable bind; run.py passes the repo as a read; reproduced the ship failure from a detached tree under /tmp and it passes` → sampo ship's scratch tree runs the sandboxed runner test green [tree 261da8f1a1f7] (2026-11-05T21:11:53Z)
- (audit adversary) `self: argv binds back read-only each home, read path and the working folder that sits under the fresh /tmp or /run, unless it's already a writable bind; run.py passes the repo as a read; reproduced the ship failure from a detached tree under /tmp and it passes` → the bound-back folders are read-only (the test's write fails); a writable folder isn't rebound read-only over itself [tree 261da8f1a1f7] (2026-11-05T21:11:53Z)
- (audit edge) `self: argv binds back read-only each home, read path and the working folder that sits under the fresh /tmp or /run, unless it's already a writable bind; run.py passes the repo as a read; reproduced the ship failure from a detached tree under /tmp and it passes` → a home, a read and the cwd that are the same folder are bound once [tree 261da8f1a1f7] (2026-11-05T21:11:53Z)
- (audit self) `self: argv binds back read-only each home, read path and the working folder that sits under the fresh /tmp or /run, unless it's already a writable bind; run.py passes the repo as a read; reproduced the ship failure from a detached tree under /tmp and it passes` → no findings [tree 261da8f1a1f7] (2026-11-05T21:11:53Z)
## Log
- 2026-11-05T21:10:42Z created
- 2026-11-05T21:10:42Z focused
- 2026-11-05T21:10:43Z predicted from its closes: 3 min, 1 attempt(s)
- 2026-11-05T21:12:16Z done
- 2026-11-05T21:12:19Z committed 1abcaddf (4 files)
- 2026-11-05T21:12:20Z guard authorization added: publish
- 2026-11-05T23:56:04Z guard authorization added: publish
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3222 [FEATURE L, done, 5 steps] Network and filesystem sandboxing as a Sampo feature: one sampo sandbox verb that turns… — lesson: running the whole suite inside the n…
- research T-1553-review: Verdict:** changes needed. This is a read-only review, so I did not run any of the reproducers. Each finding comes from reading the code. [stale:…
- playbook Ship a branch to main (fm playbooks show release/ship-to-main)
- decision 2026-11-05: [check: python3 plugin/tests/run.py test_models] A setting the user gives once is checked from every context Sampo runs in (login shell, hook, night…
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_sandbox.py
## Why not caught
the tests ran from ~/.claude/foreman, never from a tree under /tmp as ship does; RepoUnderTmp now does
## Lessons
- a sandbox that replaces /tmp must bind back what its caller keeps there: test from a tree under /tmp
## Plan gaps
- failed first: step 1 failing test: argv binds back a cwd and a read path under /tmp; run.py --sandbox runs a class from …
## Files touched
- plugin/tests/test_sandbox.py
- plugin/lib/sampo/sandbox.py
- plugin/tests/run.py
- CHANGELOG.md
