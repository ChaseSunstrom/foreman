---
id: T-2874
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:12:28Z
updated: 2026-11-04T03:18:38Z
base: e72f2b7862a8445583057bb6225c61eeaab719d3
base_tree: 2a9bc98b4c9bbb08cafc5de188ee7aa23beafbeb
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T03:12:30Z
plan0_scope: []
verified: strong
unproven: [meaning]
---
# The drive's T-2873 union added every agent the event scan saw start, finished ones too, so two done agents held the drive; only the scan's still-running agents join the engine's list
## Raw request
> The drive's T-2873 union added every agent the event scan saw start, finished ones too, so two done agents held the drive; only the scan's still-running agents join the engine's list
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a stopped agent never joins the engine's list; a live one does — verify with `python3 plugin/tests/run.py test_hooks.Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] the intersection with the scan's running set, tested
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 67 tests in 53.2s (1 classes, 16 at a time; slowest: Stop 53s) / OK [ran] [tree 2a9bc98b4c9b] [world 2f1906870a] (2026-11-04T03:18:31Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → ✗ exit 1 · Ran 1 tests in 2.5s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 2a9bc98b4c9b] [world 2f1906870a] (2026-11-04T03:18:36Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → exit 0 · Ran 1 tests in 1.2s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 2a9bc98b4c9b] [world 2f1906870a] (2026-11-04T03:18:36Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T03:18:31Z [ran] [tree 2a9bc98b4c9b] [world 2f1906870a] (2026-11-04T03:18:37Z)
- (audit edge) `self-review plus the live scan: scanned is every agent the window saw start; only its intersection with the running set joins the engine list; the test now holds a started-then-stopped agent out` → an agent whose stop was never recorded still falls to the 2 h backstop [tree 2a9bc98b4c9b] (2026-11-04T03:18:37Z)
- (audit self) `self-review plus the live scan: scanned is every agent the window saw start; only its intersection with the running set joins the engine list; the test now holds a started-then-stopped agent out` → no findings [tree 2a9bc98b4c9b] (2026-11-04T03:18:37Z)
## Log
- 2026-11-04T03:12:28Z created
- 2026-11-04T03:12:29Z focused
- 2026-11-04T03:12:30Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T03:18:38Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0121 [FIX M, done, 3 steps] A subagent that ended without its finish event stays 'running' for hours in the dashboard — lesson: Never derive 'still running' from the a…
- T-2872 [FIX S, done, 1 steps] The drive keeps counting a subagent running past LONG_JOB_S when it reads its own events: only the engine's background list marked agents (…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- decision 2026-10-31: [reverses: a later Mission's lane waits only for earlier-Mission lanes launched before it] Mission-order merging, revised: lanes that are ready merg…
## Why not caught
T-2873's test had no stopped agent in the window
