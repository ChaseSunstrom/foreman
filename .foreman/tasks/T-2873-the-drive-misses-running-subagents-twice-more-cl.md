---
id: T-2873
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T03:04:03Z
updated: 2026-11-04T03:07:42Z
base: 756e327afc997a8990dfc5e2dad1c877b6c0a097
base_tree: bf31ec0b972b6dcbce10047c31d7d15f55f2771a
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T03:04:04Z
plan0_scope: []
verified: strong
---
# The drive misses running subagents twice more: Claude Code's background_tasks list omits them yet wins over the event scan (T-0115), and _running's 1,500-line tail spans under an hour of a busy shared events file, short of its 2 h backstop
## Raw request
> The drive misses running subagents twice more: Claude Code's background_tasks list omits them yet wins over the event scan (T-0115), and _running's 1,500-line tail spans under an hour of a busy shared events file, short of its 2 h backstop
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] with an engine list that omits them, the event scan's agents still hold the drive; a start 3,000 lines back still counts — verify with `python3 plugin/tests/run.py test_hooks.Stop`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests, then the union and a wider tail
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → ✗ exit 1 · Ran 1 tests in 3.5s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree a3c56586fa0b] [world 2f1906870a] (2026-11-04T03:04:20Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → ✗ exit 1 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree a3c56586fa0b] [world 2f1906870a] (2026-11-04T03:04:20Z)
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · Ran 67 tests in 51.4s (1 classes, 16 at a time; slowest: Stop 51s) / OK [ran] [tree 2ccfc27e0db8] [world 2f1906870a] (2026-11-04T03:06:28Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → ✗ exit 1 · Ran 1 tests in 2.1s (1 classes, 16 at a time; slowest: Stop 1s) / FAILED (1 classes: test_hooks.Stop) (start tree + this task's tests) [ran] [tree 2ccfc27e0db8] [world 2f1906870a] (2026-11-04T03:06:32Z)
- `python3 plugin/tests/run.py test_hooks.Stop.test_an_engine_list_without_the_agents_and_a_far_start_still_hold_the_drive` → exit 0 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 2ccfc27e0db8] [world 2f1906870a] (2026-11-04T03:06:32Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.Stop` → exit 0 · reused: the same command passed on this tree and world at 2026-11-04T03:06:28Z [ran] [tree 2ccfc27e0db8] [world 2f1906870a] (2026-11-04T03:06:33Z)
- (audit edge) `self-review, then the live scan: the engine's list and the scan's agents are unioned (agents end with a SubagentStop row, so a missed end can't strand them past the 2 h backstop), and the tail covers 6,000 lines of the shared file, enough for the backstop here; the live scan now sees the round-5 designer it had dropped` → an agent whose stop row was lost still falls to BG_WAIT_S (2 h); a plain shell job stays engine-list-only as T-0115 chose [tree 2ccfc27e0db8] (2026-11-04T03:06:33Z)
- (audit operator) `self-review, then the live scan: the engine's list and the scan's agents are unioned (agents end with a SubagentStop row, so a missed end can't strand them past the 2 h backstop), and the tail covers 6,000 lines of the shared file, enough for the backstop here; the live scan now sees the round-5 designer it had dropped` → Stop reads up to 6,000 lines' bytes (about 1.5 MB here), decoding only this session's rows; Stop is not on the PreToolUse hot path [tree 2ccfc27e0db8] (2026-11-04T03:06:33Z)
- (audit self) `self-review, then the live scan: the engine's list and the scan's agents are unioned (agents end with a SubagentStop row, so a missed end can't strand them past the 2 h backstop), and the tail covers 6,000 lines of the shared file, enough for the backstop here; the live scan now sees the round-5 designer it had dropped` → no findings [tree 2ccfc27e0db8] (2026-11-04T03:06:33Z)
## Log
- 2026-11-04T03:04:03Z created
- 2026-11-04T03:04:04Z focused
- 2026-11-04T03:04:04Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T03:07:41Z done
- 2026-11-04T03:07:42Z committed d3cc89c2 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0909-review: Verdict: changes needed.** The 14-day bars are wrong on this repo today, and the pane order does not match the third acceptance criterion. I coul…
- T-0115 [FIX M, done, 3 steps] Drive trusts the Stop hook's background_tasks list over its event scan — lesson: Prefer the engine's authoritative payload fields over reco…
- T-2872 [FIX S, done, 1 steps] The drive keeps counting a subagent running past LONG_JOB_S when it reads its own events: only the engine's background list marked agents (…
- decision 2026-10-16: T-0275: a script over the guard's parse budget stays allowed after the literal scan, not refused
- similar finished tasks took 1–3 steps
## Why not caught
T-0115 trusted the engine list as complete, and the 1,500-line tail was sized for one quiet session
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
