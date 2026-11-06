---
id: T-2848
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-11-03T22:04:01Z
updated: 2026-11-03T22:54:59Z
base: 363b6c3fc2514131dc51df5d37eeab7ada83e6cb
base_tree: 8136bffa2548af31aa06242d309cec9d6cb452f7
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-03T22:51:33Z
plan0_scope: []
verified: strong
---
# The Stop drive doesn't count an agent resumed with SendMessage as running background…
## Raw request
> FIX: the Stop drive doesn't count an agent resumed with SendMessage as running background work (no subagent_start is recorded for a resume), so a designer or builder sent a new round is invisible to the drive's wait list; record a start when SendMessage's result says 'Resuming agent X' (sibling of T-2790)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a SendMessage that resumes an agent is a background start and its notice ends it — verify with `python3 plugin/tests/run.py test_hooks.Stop`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: PostToolUse already turns Bash and Monitor results into bg_start events (T-2790); SendMessage's result carries resumedAgentId, and the completion notice's task-id is that agent id, so one more branch records bg_start for it. Likely outcome: 3 lines. Fails if a queued message ('Message queued for delivery') is counted: that agent is already running and counted, so only resumedAgentId counts.
2. Do less: leave it; the wait list misses resumed agents. Fails: drive pushes busywork while a designer round runs.
Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a resumed agent counts as running; then record bg_start from resumedAgentId
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_agent_resumed_by_sendmessage_is_a_background_start` → ✗ exit 1 · Ran 1 tests in 2.6s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 7a726523757c] [world 2f1906870a] (2026-11-03T22:51:45Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_agent_resumed_by_sendmessage_is_a_background_start` → ✗ exit 1 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 7a726523757c] [world 2f1906870a] (2026-11-03T22:51:45Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 65 tests in 46.6s (1 classes, 16 at a time; slowest: Stop 46s) / OK [ran] [tree f667e53c5f07] [world 2f1906870a] (2026-11-03T22:53:34Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_agent_resumed_by_sendmessage_is_a_background_start` → ✗ exit 1 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree f667e53c5f07] [world 2f1906870a] (2026-11-03T22:53:43Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_agent_resumed_by_sendmessage_is_a_background_start` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree f667e53c5f07] [world 2f1906870a] (2026-11-03T22:53:43Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T22:53:34Z [ran] [tree f667e53c5f07] [world 2f1906870a] (2026-11-03T22:53:43Z)
- (audit edge) `self-review: the branch matches only resumedAgentId (a dict or JSON text); a queued message records nothing, since that agent's start is already counted; the notice's task-id ends it` → queued vs resumed message, and the result as a dict or as text, both tested [tree f667e53c5f07] (2026-11-03T22:53:43Z)
- (audit adversary) `self-review: the branch matches only resumedAgentId (a dict or JSON text); a queued message records nothing, since that agent's start is already counted; the notice's task-id ends it` → a tool_response is Claude Code's own output; the id only keys a wait list with a 2 h backstop [tree f667e53c5f07] (2026-11-03T22:53:43Z)
- (audit self) `self-review: the branch matches only resumedAgentId (a dict or JSON text); a queued message records nothing, since that agent's start is already counted; the notice's task-id ends it` → no findings [tree f667e53c5f07] (2026-11-03T22:53:43Z)
## Log
- 2026-11-03T22:04:01Z created
- 2026-11-03T22:51:26Z set tier=S
- 2026-11-03T22:51:32Z criterion 1 verify: `python3 plugin/tests/run.py test_hooks.Drive` → `python3 plugin/tests/run.py test_hooks.Stop`
- 2026-11-03T22:51:32Z planned: it has criteria and steps
- 2026-11-03T22:51:32Z focused
- 2026-11-03T22:51:33Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-03T22:54:57Z done
- 2026-11-03T22:54:59Z committed ade86480 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-2790 [FIX M, done, 2 steps] The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a… — lesson: Background work has three starts (run_i…
- T-1176 [FIX S, done, 2 steps] Stop drive: (1) offers 'fm lane brief … launch the builder' for RESEARCH and release tasks
- decision 2026-11-01: [revisited: optional work dropped] [cites: user steer 2026-10-31: (3) Don't stop or skip work for budget, pace or "optional work dropped": wait out …
- similar finished tasks took 2–5 steps
## Why not caught
T-2790 covered Bash and Monitor starts; SendMessage resumes were a third path into the background with no event
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
