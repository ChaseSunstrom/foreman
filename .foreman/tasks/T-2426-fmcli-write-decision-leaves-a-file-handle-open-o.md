---
id: T-2426
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_judgment.py]
depends_on: []
source: discovered
created: 2026-10-31T16:21:15Z
updated: 2026-11-02T01:34:32Z
base: e995cf90811af3ba26a3fdcc4bc0119f8dfa7776
base_tree: 31f5b4151fa06cca317929ae33d7b116ef86d17a
predict_minutes: 7
predict_attempts: 1
plan0_at: 2026-11-02T01:25:40Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_judgment.py]
verified: strong
---
# fmcli._write_decision closes the decisions file it reads
## Raw request
> fmcli._write_decision leaves a file handle open (open(path).read() near fmcli.py:4024; ResourceWarning in tests)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] writing a decision onto an existing decisions.md raises no ResourceWarning (the read uses a with block) and the row is appended as before — verify with `python3 plugin/tests/run.py test_judgment`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: with warnings as errors for ResourceWarning and gc.collect(), two fm decide calls in-process (fmcli._write_decision) leave no unclosed file
2. [x] fmcli._write_decision: read decisions.md in a with block; Why not caught; CHANGELOG not needed (no visible change)
## Resume here
## Docs impact
none: no visible change
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_judgment.DecisionFileClosed` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DecisionFileClosed 0s) / FAILED (1 classes: test_judgment.DecisionFileClosed) [ran] [tree 1abae921b813] [world 2f1906870a] (2026-11-02T01:25:44Z)
- (step 1) `python3 plugin/tests/run.py test_judgment.DecisionFileClosed` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: DecisionFileClosed 0s) / OK [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:26:05Z)
- (step 2) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 63 tests in 8.4s (20 classes, 16 at a time; slowest: DoorPark 8s, DoorGate 4s, Followups 3s) / OK [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:26:14Z)
- `python3 plugin/tests/run.py test_judgment.DecisionFileClosed` → ✗ exit 1 · Ran 1 tests in 1.5s (1 classes, 16 at a time; slowest: DecisionFileClosed 0s) / FAILED (1 classes: test_judgment.DecisionFileClosed) (start tree + this task's tests) [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:26:17Z)
- `python3 plugin/tests/run.py test_judgment.DecisionFileClosed` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: DecisionFileClosed 0s) / OK [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:26:17Z)
- (ac 1) `python3 plugin/tests/run.py test_judgment` → exit 0 · Ran 63 tests in 8.8s (20 classes, 16 at a time; slowest: DoorPark 9s, DoorGate 4s, Followups 3s) / OK [ran] [tree a18f9789caa5] [world 2f1906870a] (2026-11-02T01:33:31Z)
- (audit edge) `self-review: _write_decision now reads decisions.md in a with block under the same lock, keeping the default header for a new file; the write path (write_atomic) and the ledger event are unchanged` → a missing file starts from the header; an existing one is read and closed before the atomic write; two writes in a row leave no ResourceWarning [tree a18f9789caa5] (2026-11-02T01:33:31Z)
- (audit self) `self-review: _write_decision now reads decisions.md in a with block under the same lock, keeping the default header for a new file; the write path (write_atomic) and the ledger event are unchanged` → no findings [tree a18f9789caa5] (2026-11-02T01:33:31Z)
## Log
- 2026-10-31T16:21:15Z created
- 2026-11-02T01:18:59Z planned from capture
- 2026-11-02T01:25:39Z focused
- 2026-11-02T01:25:40Z predicted from its closes: 7 min, 1 attempt(s)
- 2026-11-02T01:34:28Z done
- 2026-11-02T01:34:32Z committed 6abadf0c (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1626 [FEATURE M, done, 5 steps] fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion — lesso…
- T-1658 [FEATURE M, done, 5 steps] Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts — lesson: CLI write tests need a pty: in_claud…
- T-2388 [FEATURE M, done, 4 steps] Incident ritual (Mission 7, #10): fm incident opens an urgent FIX on a harm signal recorded red, keeps a timeline, closes only on the s…
- decision 2026-10-23: T-1549: leave out a demo teleprompter pane, a guard near-miss gallery and per-dependency decision cards
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-31): plugin/lib/fmcli.py, plugin/tests/test_judgment.py; re-ground the plan against them before editing
## Why not caught
The suite doesn't turn ResourceWarning into a failure, and CPython's refcounting closes the handle at once, so the leak showed only as a warning under -W default.
## Lessons
- A bare open().read() relies on refcounting to close; use with, so other interpreters and warnings-as-errors runs don't see a leak
## Plan gaps
- failed first: step 1 red test: with warnings as errors for ResourceWarning and gc.collect(), two fm decide calls in-proc…
## Files touched
- plugin/tests/test_judgment.py
- plugin/lib/fmcli.py
