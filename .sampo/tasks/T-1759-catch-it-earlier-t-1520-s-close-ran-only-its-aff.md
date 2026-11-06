---
id: T-1759
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-23T06:36:54Z
updated: 2026-10-23T09:13:03Z
base: 5dcfbf720ade82fd79ae142483856a573a7becf5
base_tree: c0322f62ceaf07cb30c34dc7bee9907b005d4413
plan0_at: 2026-10-23T09:10:37Z
plan0_scope: [plugin/lib/fmhooks.py, plugin/tests/test_hooks.py, CHANGELOG.md]
verified: strong
---
# A piped fm check reads green when the gates are red: say so on the Bash call
## Raw request
> T-1758 (Rules file over the doctor's 6,400-char budget since T-1520 (6,416): trim it back under) wasn't caught before it shipped: T-1520's close ran only its affected tests, and the push followed a background fm check piped through tail: the notification's exit 0 was tail's, while the gate itself said ✗
## Interpretation
T-1758 reached main because a background 'fm check | tail' exited with tail's 0. Prevention: a PreToolUse note on any Bash call that pipes fm check (no pipefail): its exit is the last program's; read the ✓/✗ line before push or close. A note, not a block: piping for brevity is legitimate.
## Assumptions (confidence)
## Acceptance criteria
- [x] a Bash call piping fm check (also fm quiet -- fm check, after &&, with 2>&1, in the background) gets the note; no pipe, pipefail, ||, fm checkpoint and echo text don't — verify with `python3 plugin/tests/run.py test_hooks.GatePipe`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then _gate_pipe_note in the PreToolUse builders
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 0.9s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 03202893cf7e] (2026-10-23T09:10:39Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) [ran] [tree 03202893cf7e] (2026-10-23T09:10:39Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → ✗ exit 1 · Ran 1 tests in 1.0s (1 classes, 16 at a time; slowest: GatePipe 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree d6e2c11df0ff] (2026-10-23T09:10:41Z)
- `python3 plugin/tests/run.py test_hooks.GatePipe` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / OK [ran] [tree d6e2c11df0ff] (2026-10-23T09:10:41Z)
- (step 1) `python3 plugin/tests/run.py test_hooks` → exit 0 · Ran 202 tests in 41.5s (25 classes, 16 at a time; slowest: Stop 41s, NoTaskGate 29s, PreToolUse 23s) / OK [ran] [tree d6e2c11df0ff] (2026-10-23T09:12:14Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks.GatePipe` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: GatePipe 0s) / OK [ran] [tree d6e2c11df0ff] (2026-10-23T09:12:15Z)
- (audit edge) `self review; test_hooks green; a live PreToolUse call with 'fm check 2>&1 | tail -5' carries the note` → 2>&1 before the pipe, env prefixes, fm quiet -- fm check, after && and a newline all note; pipefail, ||, fm checkpoint, echo text and other tools don't (test) [tree d6e2c11df0ff] (2026-10-23T09:12:15Z)
- (audit self) `self review; test_hooks green; a live PreToolUse call with 'fm check 2>&1 | tail -5' carries the note` → no findings [tree d6e2c11df0ff] (2026-10-23T09:12:15Z)
## Log
- 2026-10-23T06:36:54Z created
- 2026-10-23T09:08:11Z set type=FIX, tier=S, scope=['plugin/lib/fmhooks.py', 'plugin/tests/test_hooks.py', 'CHANGELOG.md']
- 2026-10-23T09:08:12Z set title=A piped fm check reads green when the gates are red: say so on the Bash call
- 2026-10-23T09:10:36Z focused
- 2026-10-23T09:13:01Z done
- 2026-10-23T09:13:03Z committed a5afa311 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1758 [FIX S, done, 1 steps] Rules file over the doctor's 6,400-char budget since T-1520 (6,416): trim it back under — lesson: A gate run in the background must not be …
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-23: Edit the main checkout while a background fm check runs under heavy builder load
- similar finished tasks took 1–5 steps
- likely tests for the scope: plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-23): CHANGELOG.md; re-ground the plan against them before editing
## Why not caught
nothing looked at how a gate was run, only at its exit; the pipe hid the gate's ✗ behind tail's 0
## Files touched
- CHANGELOG.md
- plugin/lib/fmhooks.py
- plugin/tests/test_hooks.py
