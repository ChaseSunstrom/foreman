---
id: T-2901
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T05:43:42Z
updated: 2026-11-04T05:58:45Z
base: a0593d11c18273ce56e9ce079aa86841feb218a8
base_tree: b8501da25a67c0b8d3c48aaa261751b2b06600d1
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T05:43:43Z
plan0_scope: []
verified: strong
---
# The drive's wait counts a new running set only when its agents change, not each shell a subagent starts, so it stops re-pushing every few minutes while the same agents work
## Raw request
> The drive's wait counts a new running set only when its agents change, not each shell a subagent starts, so it stops re-pushing every few minutes while the same agents work
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] two Stops with the same agent and different shells: the second holds the drive — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: same agent, new shell ids, second Stop returns no block
2. [x] fix: the waited key is the running agents when any run, else the running ids
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_shells_coming_and_going_under_the_same_agents_push_only_once` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 7d103cfb5a5b] [world 2f1906870a] (2026-11-04T05:43:52Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop.test_shells_coming_and_going_under_the_same_agents_push_only_once` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 6adcbfcdeb5c] [world 2f1906870a] (2026-11-04T05:44:01Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → ✗ exit 1 · Ran 258 tests in 51.5s (31 classes, 16 at a time; slowest: Stop 51s, NoTaskGate 28s, PreToolUse 22s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 1ac0d7932f9e] [world 2f1906870a] (2026-11-04T05:48:04Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 258 tests in 125.0s (31 classes, 16 at a time; slowest: Stop 124s, NoTaskGate 77s, PreToolUse 67s) / OK [ran] [tree c0f51f67c42f] [world 2f1906870a] (2026-11-04T05:53:17Z)
- (audit edge) `red test then green; test_hooks, test_board_hooks and test_friction pass; an older test now reads the wait line instead of a second drive_wait event` → with only shells running the key is the running ids as before; an agent starting or ending is still a new set; the wait line still names shells and drops services [tree c0f51f67c42f] (2026-11-04T05:53:17Z)
- (audit intent) `red test then green; test_hooks, test_board_hooks and test_friction pass; an older test now reads the wait line instead of a second drive_wait event` → a subagent's own shells no longer make the drive re-push the main thread every few minutes [tree c0f51f67c42f] (2026-11-04T05:53:17Z)
- (audit self) `red test then green; test_hooks, test_board_hooks and test_friction pass; an older test now reads the wait line instead of a second drive_wait event` → no findings [tree c0f51f67c42f] (2026-11-04T05:53:17Z)
## Log
- 2026-11-04T05:43:42Z created
- 2026-11-04T05:43:42Z focused
- 2026-11-04T05:43:43Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T05:48:04Z paused: focus moved to T-2742
- 2026-11-04T05:51:07Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-04T05:51:07Z focused
- 2026-11-04T05:58:43Z done
- 2026-11-04T05:58:45Z committed 1ba74ae3 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-2790 [FIX M, done, 2 steps] The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a… — lesson: Background work has three starts (run_i…
- T-2872 [FIX S, done, 1 steps] The drive keeps counting a subagent running past LONG_JOB_S when it reads its own events: only the engine's background list marked agents (…
- decision 2026-11-04: [revisited: No mid-run questions] [cites: user steer 2026-11-04T00:02Z: stop asking me for stuff, keep going] [check: fm outcomes --questions --none…
## Why not caught
drive tests used one shell or one agent at a time, never an agent with shells churning under it
## Lessons
- a change detector keyed on everything re-fires on noise: key it on what the reader acts on
## Plan gaps
- failed first: step 1 test: same agent, new shell ids, second Stop returns no block
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
