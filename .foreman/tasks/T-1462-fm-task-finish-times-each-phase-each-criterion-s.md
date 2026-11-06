---
id: T-1462
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_close_gates.py, CHANGELOG.md]
depends_on: []
source: self
created: 2026-10-22T14:50:46Z
updated: 2026-10-22T15:22:48Z
base: 7146ace95ec24bde2f8678cd1fb1416e3c9a3b4b
base_tree: 8abe0d4025ac9a53637cf61c8d37616ebf3ede5f
plan0_at: 2026-10-22T15:01:26Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_close_gates.py, CHANGELOG.md]
verified: strong
---
# fm task finish names its slowest run
## Raw request
> fm task finish times each phase (each criterion/step verify run, the affected run) and, when a close takes over 60 s, prints the slowest ('slowest: <cmd> N s'), and close_affected carries its seconds: today several S closes took over 2 min with no record of which run was slow (fmcli.py:922-959, 1065-1071)
## Interpretation
Several S closes took over 2 minutes today with no record of which run was slow: finish runs each criterion/step verify and the final --run in turn (fmcli.py ~922-959, run()), then the linked tests in _close_affected (twice on a failure), and times none of them.
## Assumptions (confidence)
## Acceptance criteria
- [x] a close over the threshold prints its slowest run and close_affected's event carries s — verify with `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run`
## Non-goals
## Approach (options → choice → why)
Time each run() call and the affected run(s) with time.monotonic; log the seconds in close_affected's event ('s') and the finish's done event; when the whole close took over 60 s, print one line before Landed: 'Slowest: <cmd, fitted> N s (of M s)'. No behavior change otherwise.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test (threshold patched low, a sleep verify)
2. [x] time runs, log s, print the slowest
## Resume here
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → exit 0 · Ran 1 test in 2.920s / OK [ran] [tree 3e253cbfd1d9] (2026-10-22T15:02:57Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_close_gates` → exit 0 · Ran 14 tests in 32.654s / OK [ran] [tree 3e253cbfd1d9] (2026-10-22T15:03:30Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → exit 0 · Ran 1 test in 2.416s / OK [ran] [tree f9958a1ba694] (2026-10-22T15:20:00Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → exit 0 · Ran 1 test in 2.625s / OK [ran] [tree f9958a1ba694] (2026-10-22T15:20:04Z)
- `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → ✗ exit 1 · Ran 1 test in 2.598s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree f9958a1ba694] (2026-10-22T15:20:41Z)
- `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → exit 0 · Ran 1 test in 2.205s / OK [ran] [tree f9958a1ba694] (2026-10-22T15:20:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_close_gates.CloseGates.test_a_slow_close_names_its_slowest_run` → exit 0 · Ran 1 test in 2.324s / OK [ran] [tree e0f3042f973e] (2026-10-22T15:20:50Z)
- (audit edge) `builder (sonnet); red proved with fm task prove (fails on the start tree, passes now); merged; test_close_gates green.` → FOREMAN_SLOW_CLOSE_S overrides the 60 s threshold (tests); a failed close stays silent (its error names the runs); --json skips the line [tree e0f3042f973e] (2026-10-22T15:20:50Z)
- (audit adversary) `builder (sonnet); red proved with fm task prove (fails on the start tree, passes now); merged; test_close_gates green.` → prints a fitted command the close already ran; no new input [tree e0f3042f973e] (2026-10-22T15:20:50Z)
- (audit self) `builder (sonnet); red proved with fm task prove (fails on the start tree, passes now); merged; test_close_gates green.` → no findings [tree e0f3042f973e] (2026-10-22T15:20:50Z)
## Log
- 2026-10-22T14:50:46Z created
- 2026-10-22T15:01:13Z planned from capture
- 2026-10-22T15:01:15Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1462.builder.md
- 2026-10-22T15:01:25Z focused
- 2026-10-22T15:19:55Z merged worktree-agent-a57335981642b846f (2 file(s))
- 2026-10-22T15:19:55Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a57335981642b846f
- 2026-10-22T15:19:56Z focused
- 2026-10-22T15:22:46Z done
- 2026-10-22T15:22:48Z committed 4677d377 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1061 [FEATURE M, done, 2 steps] Calibration ledger: a plan predicts its size (files touched, minutes, attempts); the close — lesson: A self-regulating gate needs one r…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- likely tests for the scope: plugin/tests/test_cli.py
## Measurements
slow-close visibility: closes over 60 s named no run → name the slowest run with its seconds; close_affected events now carry s (0.1 s resolution). Per-run overhead: one time.monotonic pair per run (negligible).
## Files touched
- plugin/lib/fmcli.py
- plugin/tests/test_close_gates.py
- CHANGELOG.md
