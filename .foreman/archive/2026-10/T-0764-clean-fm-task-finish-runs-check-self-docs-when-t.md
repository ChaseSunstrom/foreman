---
id: T-0764
type: CLEAN
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-14T15:36:32Z
updated: 2026-10-14T15:53:25Z
base: e7c9a1cf41b4fae0d3a0410483cbc8a1eef31c1d
base_tree: 82c6f888d49e751e8ec67705391ab1b8fb65adbd
verified: strong
---
# Fm task finish runs check_self_docs when the diff touches fmcli.py or plugin/skills
## Raw request
> CLEAN: fm task finish runs check_self_docs when the diff touches fmcli.py or plugin/skills (T-0741/T-0739 escaped MASTER.md docs with --affected runs)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] A close touching plugin/lib/fmcli.py or plugin/skills is refused when fm doctor's self docs check fails — verify with `cd plugin/tests && python3 -m unittest test_finish_self_docs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: finish refuses a self-docs failure when a skill is touched
2. [x] Add _self_docs_gaps to the finish gaps
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_finish_self_docs 2>&1 | tail -1` → exit 0 · FAILED (errors=4) [ran] [tree ebdba90d86fb] (2026-10-14T15:50:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_finish_self_docs` → exit 0 · Ran 4 tests in 0.002s / OK [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:52:43Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_finish_self_docs` → exit 0 · Ran 4 tests in 0.002s / OK [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:52:43Z)
- `cd plugin/tests && python3 -m unittest test_finish_self_docs` → ✗ exit 1 · Ran 4 tests in 0.006s / FAILED (errors=4) (start tree + this task's tests) [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:52:43Z)
- `cd plugin/tests && python3 -m unittest test_finish_self_docs` → exit 0 · Ran 4 tests in 0.003s / OK [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:52:43Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_finish_self_docs` → exit 0 · Ran 4 tests in 0.002s / OK [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:52:54Z)
- (audit edge) `self: diff read; the check runs only when the task's own diff touches plugin/lib/fmcli.py or plugin/skills (repo-relative from fmmap.changed), costs 0.03 s, and refuses before anything runs; other projects never match those paths` → a project without git (no task base) skips it; the check reads Foreman's home docs, which is the tree being changed when the project is Foreman itself [tree 9fbf7df9dd3f] (2026-10-14T15:52:54Z)
- (audit self) `self: diff read; the check runs only when the task's own diff touches plugin/lib/fmcli.py or plugin/skills (repo-relative from fmmap.changed), costs 0.03 s, and refuses before anything runs; other projects never match those paths` → no findings [tree 9fbf7df9dd3f] (2026-10-14T15:52:54Z)
- (step 2) `python3 plugin/tests/run.py -k test_cli -k test_finish_self_docs -k test_flywheel` → exit 0 · Ran 87 tests in 18.0s (23 classes, 16 at a time; slowest: TaskLifecycle 18s, StateViews 7s, Checks 4s) / OK [ran] [tree 9fbf7df9dd3f] (2026-10-14T15:53:20Z)
- (audit edge) `self: diff read; the check runs only when the task's own diff touches plugin/lib/fmcli.py or plugin/skills (repo-relative from fmmap.changed), costs 0.03 s, and refuses before anything runs; other projects never match those paths` → a project without git (no task base) skips it; the check reads Foreman's home docs, which is the tree being changed when the project is Foreman itself [tree 9fbf7df9dd3f] (2026-10-14T15:53:24Z)
- (audit self) `self: diff read; the check runs only when the task's own diff touches plugin/lib/fmcli.py or plugin/skills (repo-relative from fmmap.changed), costs 0.03 s, and refuses before anything runs; other projects never match those paths` → no findings [tree 9fbf7df9dd3f] (2026-10-14T15:53:24Z)
## Log
- 2026-10-14T15:36:32Z created
- 2026-10-14T15:50:01Z planned from capture
- 2026-10-14T15:50:02Z focused
- 2026-10-14T15:52:28Z focused
- 2026-10-14T15:53:25Z done
- 2026-10-14T15:53:25Z committed 4aecea1 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0136 [FIX M, done, 3 steps] Work done while a task was paused isn't its own change — lesson: When several callers read the same derived value (task_base), fix the valu…
- research t0063-final-review: MEDIUM — `plugin/lib/fmcore.py:842-845` (FIX red→green requirement) and `plugin/lib/fmcli.py:71-73` (M/L lesson requirement) — the user expl…
- T-0078 [FEATURE L, done, 4 steps] A task's own changes: diff from a working-tree snapshot taken at focus, not the last commit — lesson: A check that reads a diff must te…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Behaviour lock
none: this adds a new refusal and changes no existing behaviour; the existing finish tests (test_finish, test_cli) ran green after the change
## Lessons
- a headless claude -p child in a Foreman project runs the drive and works the queue in the same checkout; launch children with Foreman's hooks off
## Files touched
- plugin/tests/test_finish_self_docs.py
- plugin/lib/fmcli.py
