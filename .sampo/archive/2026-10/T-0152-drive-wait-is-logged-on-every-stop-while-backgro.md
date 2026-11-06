---
id: T-0152
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-03T06:52:18Z
updated: 2026-10-03T06:53:29Z
base: 4de67bf4f53b1f0c4bbed87370a1f8bdbb3fd7c1
base_tree: dcd543e7ffa3674aca0370444f5179c26ed24407
verified: ok
---
# drive_wait is logged once per wait, not on every Stop
## Raw request
> drive_wait is logged on every Stop while background work runs (fmhooks _drive), so one long wait counts as many in fm friction; log it when the waited-on set changes — RSI pass 1
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] three Stops during one background command log one drive_wait — verify with `python3 plugin/tests/run.py -p test_hooks.py -k background_command_runs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test, then fix
## Resume here
## Docs impact
CHANGELOG entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py -p test_hooks.py -k background_command_runs` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 54c0c1b49b63] (2026-10-03T06:53:23Z)
- (step 1) `python3 plugin/tests/run.py -p test_hooks.py -k background_command_runs` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree 54c0c1b49b63] (2026-10-03T06:53:23Z)
- (audit self) `self: the event is skipped only when the same set is still being waited on; the wait itself, its systemMessage and the continue after the notification are unchanged (the rest of the drive tests pass); the key resets once nothing runs` → no findings [tree 54c0c1b49b63] (2026-10-03T06:53:23Z)
- (audit self) `self: the event is skipped only when the same set is still being waited on; the wait itself, its systemMessage and the continue after the notification are unchanged (the rest of the drive tests pass); the key resets once nothing runs` → no findings [tree 54c0c1b49b63] (2026-10-03T06:53:29Z)
## Log
- 2026-10-03T06:52:18Z created
- 2026-10-03T06:52:51Z planned from capture
- 2026-10-03T06:52:51Z focused
- 2026-10-03T06:53:29Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-20261003-pass1: 1. **Answer** — Two causes are grounded in code. The first is the 32 evidence nudges: automatic evidence is tagged `(ac N)`, but the Stop ga…
- T-0125 [FEATURE M, done, 4 steps] Recursive self-improvement loop: fm friction digests Foreman's own friction since the last pass, fm next calls for a pass every N close…
- T-0145 [FEATURE M, done, 3 steps] UI changes reach the running session during a drive: the Stop hook ends the turn once when this session's dev-mods changed, and the rel…
- T-0019 [FEATURE S, done, 1 steps] Drive lets the turn end while background agents or commands are running
- similar finished tasks took 1–4 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Behaviour lock
none run before the first edit: the full suite passed on the T-0125 tree just before (fm check, 550 tests OK, 06:50) and the change only skips a repeated event log line; every drive test still passes after it
## Files touched
- CHANGELOG.md
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
