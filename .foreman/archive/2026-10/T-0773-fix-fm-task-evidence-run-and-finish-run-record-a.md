---
id: T-0773
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py]
depends_on: []
source: discovered
created: 2026-10-14T15:52:36Z
updated: 2026-10-14T16:04:19Z
group: fm task add and evidence hardening
base: cfeff7118aeaa168486249a8796b8fe6c9c9cb66
base_tree: 049246abcba9ac7f8823573593c0a932656295f7
verified: strong
---
# Evidence runs whose output reports failing tests count as failures even when a pipe hides the exit
## Raw request
> FIX: fm task evidence --run (and finish --run) record a pipeline's last exit: 'cmd | tail -3' logged 'exit 0 · FAILED (errors=1)' twice today (T-0768, T-0764) — run with pipefail, or flag a FAILED/Traceback tail on exit 0 as inconclusive
## Interpretation
fm runs verify commands with bash -c; 'cmd | tail -3' exits with tail's 0, so evidence read 'exit 0 · FAILED (errors=1)' twice today (T-0768, T-0764's first step). pipefail would also fail '| grep -q' and '| head' (SIGPIPE/BrokenPipeError upstream), so the runner reads the output like its zero-tests check (R3): a test-runner failure summary on exit 0 is a failure.
## Assumptions (confidence)
## Acceptance criteria
- [x] a command whose output ends in a unittest/pytest/jest/cargo/go failure summary but exits 0 records ✗ with a note; passing output is unchanged — verify with `cd plugin/tests && python3 -m unittest test_core.RunCommand`
## Non-goals
## Approach (options → choice → why)
Options: bash -o pipefail (false failures on | head and | grep -q); PIPESTATUS bookkeeping (complex, last pipeline only); scan for runner failure summaries next to _NO_TESTS. Chose the scan: same pattern as R3, no exit-code semantics change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for a piped failing run
2. [x] Failure-summary scan in run_command
## Resume here
## Docs impact
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_core.RunCommand` → ✗ exit 1 · Ran 1 test in 0.002s / FAILED (failures=1) [ran] [tree d55384468b07] (2026-10-14T16:02:03Z)
- (step 2) `python3 plugin/tests/run.py -k test_core -k test_verifying -k test_verify_strength -k test_round_g -k test_round_i` → exit 0 · Ran 107 tests in 11.7s (25 classes, 16 at a time; slowest: VerifyStrength 12s, RoundI 6s, RoundG 2s) / OK [ran] [tree 39420d9eddf5] (2026-10-14T16:02:22Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_core.RunCommand` → exit 0 · Ran 1 test in 0.045s / OK [ran] [tree d7c13935a282] (2026-10-14T16:02:31Z)
- `cd plugin/tests && python3 -m unittest test_core.RunCommand` → ✗ exit 1 · Ran 1 test in 0.002s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree d7c13935a282] (2026-10-14T16:02:32Z)
- `cd plugin/tests && python3 -m unittest test_core.RunCommand` → exit 0 · Ran 1 test in 0.045s / OK [ran] [tree d7c13935a282] (2026-10-14T16:02:32Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_core.RunCommand` → exit 0 · Ran 1 test in 0.043s / OK [ran] [tree d7c13935a282] (2026-10-14T16:04:19Z)
- (audit edge) `self: diff read; the scan runs only on exit 0 and only matches runner summary lines anchored at line start (unittest FAILED (…=N), pytest ==== N failed ====, jest Tests: N failed, cargo test result: FAILED, go --- FAIL:), so passing output is untouched; full gates stayed green with it live` → a passing run that prints a nested runner's failing summary at line start would now count as a failure; the full suite (which runs such nested fixtures) stayed green, and the note says why so a reader can see it [tree d7c13935a282] (2026-10-14T16:04:19Z)
- (audit self) `self: diff read; the scan runs only on exit 0 and only matches runner summary lines anchored at line start (unittest FAILED (…=N), pytest ==== N failed ====, jest Tests: N failed, cargo test result: FAILED, go --- FAIL:), so passing output is untouched; full gates stayed green with it live` → no findings [tree d7c13935a282] (2026-10-14T16:04:19Z)
## Log
- 2026-10-14T15:52:36Z created
- 2026-10-14T16:00:44Z planned from capture
- 2026-10-14T16:01:55Z focused
- 2026-10-14T16:04:19Z done
- 2026-10-14T16:04:19Z committed 76c2090 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0414 [FIX M, done, 3 steps] Guard: a data-reading python -c is judged by what runs before it — lesson: A parser that drops quoting can't be trusted about structure the…
- research t0024-t0025-grounding: `fm task evidence ID [--step N|--ac N] CMD RESULT` (fmcli.py ~185, parser ~710): both strings typed by Claude;
- decision 2026-10-06: fm task ac edit (T-0333) kept but limited to criteria with no evidence and logged (T-0342), reconciling the 2026-10-04 drop of T-0305: planning-time…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_core.py
## Lessons
- evidence must read the run's outcome, not only its exit: a pipe's exit is the last program's
## Plan gaps
- failed first: step 1 Failing test for a piped failing run
## Files touched
- plugin/tests/test_core.py
- plugin/lib/fmcore.py
