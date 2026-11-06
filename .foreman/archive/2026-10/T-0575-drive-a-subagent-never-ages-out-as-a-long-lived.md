---
id: T-0575
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-09T14:37:23Z
updated: 2026-10-09T14:38:14Z
base: d1eaa386d187ff96e512793cf3dcb6e33a41403a
base_tree: 3ccfb942141e680f5ccc96917b006dedc15e172f
verified: strong
---
# Drive: a subagent never ages out as a long-lived service
## Raw request
> Drive: a subagent never ages out as a long-lived service
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a running agent stays a reason to wait past 20 min, a shell or workflow still ages out — verify with `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then age out only non-agent jobs
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → ✗ exit 1 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes) [ran] [tree c9c81d1c2c6a] (2026-10-09T14:37:31Z)
- (step 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 47fbac500b88] (2026-10-09T14:37:43Z)
- (ac 1) `python3 plugin/tests/run.py -k test_long_jobs_and_an_empty_queue_never_idle` → exit 0 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 617130e57a1b] (2026-10-09T14:38:14Z)
- (audit edge) `self: one set from the engine's list (type == agent); red→green; hooks suite OK` → on builds without background_tasks every job is treated as before (events path) [tree 617130e57a1b] (2026-10-09T14:38:14Z)
- (audit self) `self: one set from the engine's list (type == agent); red→green; hooks suite OK` → no findings [tree 617130e57a1b] (2026-10-09T14:38:14Z)
## Log
- 2026-10-09T14:37:23Z created
- 2026-10-09T14:37:24Z focused
- 2026-10-09T14:38:14Z done
- 2026-10-09T14:38:14Z committed d226d7e (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0415 [FIX M, done, 3 steps] Drive: long-lived jobs and an empty queue never leave a session idle — lesson: A wait rule keyed on 'anything running' breaks when somethin…
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-0139 [FIX S, done, 1 steps] Snapshot tool: its own tmux server and a clean environment, so FOREMAN_STATE can't leak into the user's tmux — lesson: A helper that starts…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
## Lessons
- Age is a proxy for 'service' only for things that don't end by design; agents do.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
