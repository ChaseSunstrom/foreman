---
id: T-0761
type: FIX
tier: S
status: dropped
priority: normal
scope: [plugin/lib/fmguard.py, plugin/tests/test_guard.py]
depends_on: []
source: self
created: 2026-10-14T15:36:31Z
updated: 2026-10-14T15:40:59Z
base: 4a9bf49a329a62d797e24dacdb67306687aa8570
base_tree: 94176e91d646b648c8b4d40c838a1ca1135013ed
---
# Guard: a data heredoc that writes a Foreman source file isn't interpreter code driving Foreman
## Raw request
> FIX: guard blocks write-only cat/tee heredocs whose body names Foreman modules (6x): fmguard.py:1395 calls _drives_fm on the raw cmd, not _drop_data_heredocs(cmd); keep 'cat > t.py <<EOF…EOF; python3 t.py' blocked
## Interpretation
cat >> plugin/lib/fmX.py <<'EOF' (a source edit whose text names fmcore's writers) next to a test run is blocked as core 'interpreter code driving Foreman's modules', which a standing core yes can't cover (6x since 10-09). The body only writes Foreman's own source, a core path write the yes already gates. Running what was written (python3 that file, importing it) must still block.
## Assumptions (confidence)
## Acceptance criteria
- [ ] a cat/tee heredoc writing a core source file beside pytest isn't 'driving'; running or importing the written file, or a scratch script, still is — verify with `python3 -m pytest -q plugin/tests/test_guard.py -k 'driving or source_file'`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in InterpreterWrites
2. [x] _drives_fm skips data heredoc bodies that write an unnamed-again core source file
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → ✗ exit 1 · Ran 1 test in 0.018s / FAILED (failures=1) [ran] [tree b122a996670c] (2026-10-14T15:39:53Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_guard test_guard_diff 2>&1 | tail -3` → exit 0 · Ran 83 tests in 5.229s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:40:29Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites` → exit 0 · Ran 8 tests in 0.111s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:40:35Z)
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → ✗ exit 1 · Ran 1 test in 0.018s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree ae935b2e97c8] (2026-10-14T15:40:39Z)
- `cd plugin/tests && python3 -m unittest test_guard.InterpreterWrites.test_writing_a_foreman_source_file_is_not_driving_it` → exit 0 · Ran 1 test in 0.023s / OK [ran] [tree ae935b2e97c8] (2026-10-14T15:40:39Z)
- (ac 1) `python3 -m pytest -q plugin/tests/test_guard.py -k 'driving or source_file'` → ✗ exit 1 · /usr/bin/python3: No module named pytest [ran] [tree ae935b2e97c8] (2026-10-14T15:40:45Z)
- (ac 1) `python3 -m pytest -q plugin/tests/test_guard.py -k 'driving or source_file'` → ✗ exit 1 · /usr/bin/python3: No module named pytest [ran] [tree ae935b2e97c8] (2026-10-14T15:40:50Z)
## Log
- 2026-10-14T15:36:31Z created
- 2026-10-14T15:39:19Z planned from capture
- 2026-10-14T15:39:20Z focused
- 2026-10-14T15:40:59Z dropped: criterion 1's verify used pytest, which isn't installed here, and a criterion with evidence can't be edited; recreated with a unittest verify
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research rsi-pass-2: 1. **Answer.** Of the four guard false positives, two can be made precise without opening a bypass. These are the `secrets.txt` scratch file, and th…
- research rsi-20261004-recon: 1. **Answer.** Four of the five findings are in the guard and the friction digest. The guard blocks most often on a heredoc that only writes…
- T-0170 [FIX M, done, 3 steps] Guard: 'driving Foreman's modules' reads real Python imports, not text that mentions them — lesson: Relax a guard by proving the safe case,…
- decision 2026-10-04: Friction pass 2026-10-04: drop recon findings 1-3 (guard)
- similar past tasks were M: consider --tier M
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_guard.py
