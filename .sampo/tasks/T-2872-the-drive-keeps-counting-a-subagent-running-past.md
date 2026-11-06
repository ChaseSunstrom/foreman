---
id: T-2872
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T02:57:41Z
updated: 2026-11-04T03:03:00Z
base: 3c20bba9240f37c1ad770d32e4738ad853f3fec7
base_tree: fe8978621c6cdbeccd80f4e8ebbbfe53398cc818
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T02:57:42Z
plan0_scope: []
verified: strong
---
# The drive keeps counting a subagent running past LONG_JOB_S when it reads its own events: only the engine's background list marked agents (T-0575), so without it a 45-minute builder or designer round read as a service and the drive pushed new work over it
## Raw request
> The drive keeps counting a subagent running past LONG_JOB_S when it reads its own events: only the engine's background list marked agents (T-0575), so without it a 45-minute builder or designer round read as a service and the drive pushed new work over it
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] from the event scan, a subagent started (or resumed) longer than LONG_JOB_S ago and not stopped still counts as running work; a long plain job is still a service — verify with `python3 plugin/tests/run.py test_hooks.Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then _running reports which ids are agents (subagent_start, a resume's bg_start)
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_hooks.Stop.test_from_the_event_scan_a_long_subagent_still_holds_the_drive` → ✗ exit 1 · Ran 1 tests in 4.7s (1 classes, 16 at a time; slowest: Stop 2s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 7690bdbbdd32] [world 2f1906870a] (2026-11-04T02:58:07Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_from_the_event_scan_a_long_subagent_still_holds_the_drive` → ✗ exit 1 · Ran 1 tests in 2.7s (1 classes, 16 at a time; slowest: Stop 2s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 7690bdbbdd32] [world 2f1906870a] (2026-11-04T02:58:07Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop 2>&1 | tail -1` → exit 0 · OK [ran] [tree 8548720e90f8] [world 2f1906870a] (2026-11-04T02:59:28Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop 2>&1 | tail -1` → exit 0 · OK [ran] [tree 8548720e90f8] [world 2f1906870a] (2026-11-04T02:59:28Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 66 tests in 52.5s (1 classes, 16 at a time; slowest: Stop 52s) / OK [ran] [tree bf31ec0b972b] [world 2f1906870a] (2026-11-04T03:01:32Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_from_the_event_scan_a_long_subagent_still_holds_the_drive` → ✗ exit 1 · Ran 1 tests in 2.6s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree bf31ec0b972b] [world 2f1906870a] (2026-11-04T03:01:36Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_from_the_event_scan_a_long_subagent_still_holds_the_drive` → exit 0 · Ran 1 tests in 1.4s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree bf31ec0b972b] [world 2f1906870a] (2026-11-04T03:01:36Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T03:01:32Z [ran] [tree bf31ec0b972b] [world 2f1906870a] (2026-11-04T03:01:37Z)
- (audit edge) `self-review: _running fills an agents set from subagent_start rows and resume bg_starts (now marked agent), and the drive uses it as the engine list's agent marks when there is no engine list; a long plain job is still a service (tested)` → a resume recorded before this change has no agent mark, but its SubagentStart row (Claude Code fires one on resume) marks it; an agent that never ends still falls to the 2 h backstop [tree bf31ec0b972b] (2026-11-04T03:01:37Z)
- (audit adversary) `self-review: _running fills an agents set from subagent_start rows and resume bg_starts (now marked agent), and the drive uses it as the engine list's agent marks when there is no engine list; a long plain job is still a service (tested)` → event rows are Sampo's own; the change only keeps the drive waiting longer for real agents [tree bf31ec0b972b] (2026-11-04T03:01:37Z)
- (audit self) `self-review: _running fills an agents set from subagent_start rows and resume bg_starts (now marked agent), and the drive uses it as the engine list's agent marks when there is no engine list; a long plain job is still a service (tested)` → no findings [tree bf31ec0b972b] (2026-11-04T03:01:37Z)
## Log
- 2026-11-04T02:57:41Z created
- 2026-11-04T02:57:42Z focused
- 2026-11-04T02:57:42Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T03:02:57Z done
- 2026-11-04T03:03:00Z committed 756e327a (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0364 [FIX L, done, 5 steps] Foreman keeps working while background jobs run, plans and brainstorms wider, uses subagents — lesson: Read the user's transcripts before t…
- T-2848 [FIX S, done, 1 steps] The Stop drive doesn't count an agent resumed with SendMessage as running background…
- T-2790 [FIX M, done, 2 steps] The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a… — lesson: Background work has three starts (run_i…
- decision 2026-11-01: [revisited: finish round 1 completely] [cites: user steer 2026-10-31: (2) Finish round 1 completely, in order: Mission 4's remaining work, then writ…
- similar finished tasks took 1–5 steps
## Why not caught
T-0575 tested agents only through the engine's background_tasks list, which this build doesn't send
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
