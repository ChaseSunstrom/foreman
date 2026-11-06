---
id: T-2900
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T05:22:31Z
updated: 2026-11-04T05:26:21Z
base: aaebcf345e7dc08d967ff8dfead7148f037801da
base_tree: 2bef4f49e26b3f52a545651b6948ad4f0f1723d0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T05:22:32Z
plan0_scope: []
verified: strong
---
# A resumed session (SessionStart source resume, a new process) closes the background work its dead process left open, so the drive never waits on an agent or shell that died with the terminal
## Raw request
> A resumed session (SessionStart source resume, a new process) closes the background work its dead process left open, so the drive never waits on an agent or shell that died with the terminal
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] after SessionStart with source resume, _running for that session is empty; compact keeps them — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: a bg_start and a subagent_start before SessionStart resume are closed; before compact they stay
2. [x] fix: session_start records bg_done for each still-open id on resume
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks.Stop.test_a_resumed_session_closes_what_its_dead_process_left_running` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes: test_hooks.Stop) [ran] [tree 4df88b5b82c1] [world 2f1906870a] (2026-11-04T05:22:40Z)
- (step 2) `python3 plugin/tests/run.py test_hooks.Stop.test_a_resumed_session_closes_what_its_dead_process_left_running` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree b8501da25a67] [world 2f1906870a] (2026-11-04T05:22:49Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 257 tests in 66.9s (31 classes, 16 at a time; slowest: Stop 66s, NoTaskGate 42s, PreToolUse 36s) / OK [ran] [tree b8501da25a67] [world 2f1906870a] (2026-11-04T05:25:07Z)
- (audit edge) `red test then green; test_hooks passes` → only source resume closes (a new process); compact and clear keep the same process's work; startup has a new session id with nothing open; the subagent_start key (agent_id) is closed by a bg_done with id, as _running reads either [tree b8501da25a67] (2026-11-04T05:25:07Z)
- (audit intent) `red test then green; test_hooks passes` → after the terminal closed, the drive listed a dead builder as running; a resume now closes what the dead process left open [tree b8501da25a67] (2026-11-04T05:25:07Z)
- (audit self) `red test then green; test_hooks passes` → no findings [tree b8501da25a67] (2026-11-04T05:25:07Z)
## Log
- 2026-11-04T05:22:31Z created
- 2026-11-04T05:22:31Z focused
- 2026-11-04T05:22:32Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T05:26:20Z done
- 2026-11-04T05:26:21Z committed a0593d11 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2790 [FIX M, done, 2 steps] The Stop drive ignores a background Bash job or Monitor the main thread is waiting on (a… — lesson: Background work has three starts (run_i…
- T-2848 [FIX S, done, 1 steps] The Stop drive doesn't count an agent resumed with SendMessage as running background…
- T-0096 [FIX M, done, 3 steps] Drive resumes when background work finished mid-turn — lesson: A wait that depends on an event the hook might never see needs a second sign…
- decision 2026-11-03: [revisited: keep going with everything else] [cites: user steer 2026-11-03: make sure to keep going with everything else when done] [check: python3 …
- similar finished tasks took 1–3 steps
## Why not caught
every drive test ran inside one process; none crossed a resume
## Lessons
- a crash leaves no stop events: any 'still running' derived from start/stop events needs a process boundary that closes the rest
## Plan gaps
- failed first: step 1 test: a bg_start and a subagent_start before SessionStart resume are closed; before compact they st…
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/sampo/hooks.py
