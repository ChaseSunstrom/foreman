---
id: T-0426
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T14:00:59Z
updated: 2026-10-14T15:36:51Z
base: d4d8dff8eb7dd3d568ca29a0dc77147558a72c98
base_tree: cfbbea4b5c2ac3dcfd3dafc059bc230abf71b4c0
verified: strong
---
# Hook: a foreground wait loop is refused (run it in the background)
## Raw request
> Hook: a foreground wait loop is refused (run it in the background)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a foreground until/while loop that sleeps 5 s or more is refused with how to background it; the same with run_in_background, a short poll (sleep 1) and a plain sleep-free loop pass — verify with `python3 plugin/tests/run.py -k test_foreground_wait_loops_are_refused`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then the refusal in PreToolUse beside _ask_prompt
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_foreground_wait_loops_are_refused` → ✗ exit 1 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: PreToolUse 0s) / FAILED (1 classes) [ran] [tree 892149c93a4e] (2026-10-09T14:01:16Z)
- (step 1) `python3 plugin/tests/run.py -k test_foreground_wait_loops_are_refused` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: PreToolUse 1s) / OK [ran] [tree 0e0f6734713e] (2026-10-09T14:01:30Z)
- (ac 1) `python3 plugin/tests/run.py -k test_foreground_wait_loops_are_refused` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: PreToolUse 1s) / OK [ran] [tree 3d9d97b19c63] (2026-10-09T14:01:59Z)
- (audit edge) `self: diff read; regex needs until/while before a sleep of 5 s or more (units s/m/h/d, or a variable); run_in_background passes; tested refused and passing forms` → 'while read' and for-loops have no sleep and pass; a sleep in a non-loop is Claude Code's own block; a loop with sleep $N counts as long [tree 3d9d97b19c63] (2026-10-09T14:01:59Z)
- (audit self) `self: diff read; regex needs until/while before a sleep of 5 s or more (units s/m/h/d, or a variable); run_in_background passes; tested refused and passing forms` → no findings [tree 3d9d97b19c63] (2026-10-09T14:01:59Z)
## Log
- 2026-10-09T14:00:59Z created
- 2026-10-09T14:00:59Z focused
- 2026-10-09T14:01:59Z done
- 2026-10-09T14:02:00Z committed c8fa251 (3 files)
- 2026-10-14T15:36:51Z includes T-0758: "can you make sure it doesnt sit idle like it is"
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0115 [FIX M, done, 3 steps] Drive trusts the Stop hook's background_tasks list over its event scan — lesson: Prefer the engine's authoritative payload fields over reco…
- T-0310 [FIX S, done, 1 steps] A headless run (claude -p) never ends a turn waiting on background work it will never hear from — lesson: Wait-for-notification is an inter…
- T-0372 [CLEAN S, done, 1 steps] The headless wait nudge only on Claude Code before 2.1.292 (newer claude -p waits for background work itself) — lesson: When the platform…
- decision 2026-10-04: The recursive brainstorm loop is dry: pass 5 kept 2 small ideas (built as T-0287) and pass 6 (fresh lenses: performance, unspoken needs; 43 titles) …
## Lessons
- Idle hides in the foreground too: a wait loop is a background job run the wrong way.
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
