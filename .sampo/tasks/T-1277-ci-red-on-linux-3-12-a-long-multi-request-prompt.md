---
id: T-1277
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T14:57:31Z
updated: 2026-10-20T15:04:08Z
base: fd6a19a69c13b82e2545f043d676af57fe6b9525
base_tree: 480da00bb01aacf930da5c45b9b51c43748678f5
plan0_at: 2026-10-20T14:57:32Z
plan0_scope: []
verified: strong
---
# CI red on Linux 3.12: a long multi-request prompt queues only 4 of 8 tasks inside the hook's 5 s (one fm process per task)
## Raw request
> CI red on Linux 3.12: a long multi-request prompt queues only 4 of 8 tasks inside the hook's 5 s (one fm process per task)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a 16-request prompt queues all 16 tasks in order inside the hook's time, on this machine and CI — verify with `python3 plugin/tests/run.py test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test: 16 requests queue all 16
2. [x] Queue them through fm in-process, one interpreter for all
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → exit 0 · Ran 1 test in 1.916s / OK [ran] [tree d43184af36e6] (2026-10-20T14:57:43Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → exit 0 · Ran 1 test in 1.925s / OK [ran] [tree d43184af36e6] (2026-10-20T14:58:00Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → exit 0 · Ran 1 test in 1.927s / OK [ran] [tree d43184af36e6] (2026-10-20T14:58:07Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → ✗ exit 1 · Ran 1 test in 4.902s / FAILED (failures=1) [ran] [tree 3c419ca5316e] (2026-10-20T14:58:23Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate` → exit 0 · Ran 27 tests in 17.651s / OK [ran] [tree 4d20905ce778] (2026-10-20T14:58:57Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 186 tests in 37.4s (21 classes, 16 at a time; slowest: Stop 37s, PreToolUse 21s, NoTaskGate 20s) / OK [ran] [tree 1017b703b5af] (2026-10-20T15:00:30Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 186 tests in 37.4s (21 classes, 16 at a time; slowest: Stop 37s, PreToolUse 21s, NoTaskGate 20s) / OK [ran] [tree 1017b703b5af] (2026-10-20T15:00:30Z)
- (audit intent) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → main's CI was red on Linux 3.12 from T-1242's own test; the cause was process starts, not the logic, so the fix removes them [tree 1017b703b5af] (2026-10-20T15:00:30Z)
- (audit edge) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → fm run in-process restores the cwd and FOREMAN_SESSION_ID even when it raises; a SystemExit from fm is an exit code; the 3.2 s budget still stops a very slow queue, and the agent's own queue picks up what's left [tree 1017b703b5af] (2026-10-20T15:00:30Z)
- (audit self) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → no findings [tree 1017b703b5af] (2026-10-20T15:00:30Z)
- `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → ✗ exit 1 · Ran 1 test in 4.902s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree 1017b703b5af] (2026-10-20T15:01:56Z)
- `cd plugin/tests && python3 -m unittest test_hooks.NoTaskGate.test_a_long_multi_request_prompt_queues_every_request` → exit 0 · Ran 1 test in 1.505s / OK [ran] [tree 1017b703b5af] (2026-10-20T15:01:56Z)
- `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 186 tests in 58.6s (21 classes, 16 at a time; slowest: Stop 58s, PreToolUse 34s, NoTaskGate 33s) / OK [ran] [tree 1017b703b5af] (2026-10-20T15:03:00Z)
- (audit intent) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → main's CI was red on Linux 3.12 from T-1242's own test; the cause was process starts, not the logic, so the fix removes them [tree 1017b703b5af] (2026-10-20T15:03:00Z)
- (audit edge) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → fm run in-process restores the cwd and FOREMAN_SESSION_ID even when it raises; a SystemExit from fm is an exit code; the 3.2 s budget still stops a very slow queue, and the agent's own queue picks up what's left [tree 1017b703b5af] (2026-10-20T15:03:00Z)
- (audit self) `self review; reproduced CI's failure locally with a sitecustomize that slows every interpreter start by 0.4 s, then fixed` → no findings [tree 1017b703b5af] (2026-10-20T15:03:00Z)
## Log
- 2026-10-20T14:57:31Z created
- 2026-10-20T14:57:32Z focused
- 2026-10-20T15:04:08Z done
- 2026-10-20T15:04:08Z committed 59bc9679 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1242 [FEATURE L, done, 3 steps] Marathon showcase: a long unattended run that keeps finishing work across forced compactions, Foreman vs plain Claude Code, cheap (Haik…
- research mission-20261020-084536.pack: continue, super improve foreman, and with latest claude code
- research mission-20261020-084536: Request: continue, super improve foreman, and with latest claude code
- decision 2026-10-16: T-1242 L plan approval under standard autonomy: the user's explicit request ('showcase that it is able to go for a long time with new ideas, after c…
- similar past tasks were L: consider --tier L
- the similar finished task took 3 steps
## Why not caught
the test ran on a fast machine, where 8 process starts fit in 5 s; it now runs with a 0.4 s start penalty per process
## Lessons
- A hook's time budget measured on this machine says little about CI: test it under a slowed interpreter start
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md
