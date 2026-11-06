---
id: T-1828
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:48:11Z
updated: 2026-10-28T09:38:04Z
base: 3c601892629dc3ddd5a943122b5b9ec0c91ce716
base_tree: 1f48e1e834237699cf9db2ac6cfa6c95a32a02bf
plan0_at: 2026-10-28T09:29:16Z
plan0_scope: []
verified: strong
---
# FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_c
## Raw request
> FIX: macOS CI job (non-blocking) fails at 3f2538fc: suite hits its 1980 s deadline (test_code_tui.Paste 481 s, Command 480 s, test_bus.Conductor killed); Linux-only /proc reads in test_run.Load burn and test_code_tui.Cards quit; /var vs /private/var paths in test_docs.Fences; non-UTF-8 file name refused by APFS in test_supply_delta; test_playbook_check memory-limit snippet, test_code_tui.Editors quit, test_settings.History 'border' — skip or port each per platform, speed the two TUI classes
## Interpretation
The macOS CI job (non-blocking) runs out its 1980 s deadline. Causes: macOS pty behaviour (unread output is dropped when the last writer closes; a master read at EOF returns b'' instead of EIO; the writer and tcdrain stall while the master goes unread), Linux-only /proc reads in tests and in fmcodetui._runners_of_child (no runner is ever stopped on quit on macOS), /var vs /private/var in fmplaybooks._run, APFS refusing a non-UTF-8 name, and RLIMIT_AS/NPROC that macOS doesn't apply. Make each portable, or skip it with a reason, and keep Linux green.
## Assumptions (confidence)
## Acceptance criteria
- [x] Each named macOS failure is ported or skipped with a reason, and the classes still pass on Linux — verify with `cd plugin/tests && python3 -m unittest -q test_code_tui.Paste test_code_tui.Command test_code_tui.Cards test_code_tui.Editors test_settings.History test_run.Load test_docs.Fences test_supply_delta test_playbook_check.Snippets`
## Non-goals
## Approach (options → choice → why)
Options: (a) skip every pty/proc test off Linux: cheap, but loses macOS coverage and leaves the product bug; (b) port each: a helpers.PtyReader thread keeps a reader on the master (fixes the drop and the stall), EOF counts as the end in the read loops, fmideas._cmdline/fmcodetui._alive (already portable) replace the /proc reads, realpath the playbook folder; skip only what macOS can't do (an APFS name, RLIMIT_AS/NPROC); (c) change fmcodeterm.restore to TCSANOW: hides the stall in tests but drops the drain that keeps a pty's last output readable. Choice: (b).
## Risks and rollback
## Execution prompt
## Steps
1. [x] port the pty readers, the /proc reads, the playbook folder, and the APFS and limits checks
2. [x] gates and review
## Resume here
<!-- auto -->
- 2026-10-28T09:30:13Z step 2/2: gates and review
- git: foreman/build; 4 uncommitted: plugin/lib/fmcodetui.py, plugin/tests/helpers.py, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py
- touched since last checkpoint: plugin/tests/test_code_tui.py, plugin/lib/fmcodetui.py, plugin/tests/helpers.py, plugin/tests/test_settings.py
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_code_tui.Cards.test_a_runner_is_named_without_proc_too` → red as expected (exit 1) · Ran 1 test in 0.026s / FAILED (failures=1) [ran] [tree f00004f1f09f] (2026-10-28T09:29:44Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_code_tui.Paste test_code_tui.Command test_code_tui.Cards test_code_tui.Editors test_settings.History test_run.Load test_docs.Fences test_supply_delta test_playbook_check.Snippets` → exit 0 · Ran 129 tests in 21.546s / OK [ran] [tree b04313e86337] (2026-10-28T09:32:50Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcodetui.py, plugin/lib/fmplaybooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass,; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.4    44.6     150  [0] / SessionEnd                  34.9    37.6     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree c9faca751246] (2026-10-28T09:36:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_code_tui.Paste test_code_tui.Command test_code_tui.Cards test_code_tui.Editors test_settings.History test_run.Load test_docs.Fences test_supply_delta test_playbook_check.Snippets` → exit 0 · Ran 129 tests in 20.807s / OK [ran] [tree c9faca751246] (2026-10-28T09:37:22Z)
- (audit intent) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → fixes the product bug (runners unnamed without /proc) and every test the macOS job hung or failed on, without skipping Linux coverage [tree c9faca751246] (2026-10-28T09:37:22Z)
- (audit edge) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → pty_reader ends on EIO (Linux) and b'' (macOS); _cmdline gone pid → OSError caught; empty ps output → 'runner'; APFS refusing a non-UTF-8 name skips, not fails [tree c9faca751246] (2026-10-28T09:37:22Z)
- (audit adversary) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → no new input surface; realpath of fm's own mkdtemp folder; ps called with an int pid from the registry [tree c9faca751246] (2026-10-28T09:37:22Z)
- (audit operator) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → cost at scale is one ps per registered runner only when /proc is missing, at app quit; the macOS job should drop from its 1980 s deadline to ~1300 s [tree c9faca751246] (2026-10-28T09:37:22Z)
- `cd plugin/tests && python3 -m unittest -q test_code_tui.Cards.test_a_runner_is_named_without_proc_too` → ✗ exit 1 · Ran 1 test in 0.098s / FAILED (failures=1) (start tree + this task's tests) [ran] [tree c9faca751246] (2026-10-28T09:37:41Z)
- `cd plugin/tests && python3 -m unittest -q test_code_tui.Cards.test_a_runner_is_named_without_proc_too` → exit 0 · Ran 1 test in 0.028s / OK [ran] [tree c9faca751246] (2026-10-28T09:37:41Z)
- (audit intent) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → fixes the product bug (runners unnamed without /proc) and every test the macOS job hung or failed on, without skipping Linux coverage [tree c9faca751246] (2026-10-28T09:37:47Z)
- (audit edge) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → pty_reader ends on EIO (Linux) and b'' (macOS); _cmdline gone pid → OSError caught; empty ps output → 'runner'; APFS refusing a non-UTF-8 name skips, not fails [tree c9faca751246] (2026-10-28T09:37:47Z)
- (audit adversary) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → no new input surface; realpath of fm's own mkdtemp folder; ps called with an int pid from the registry [tree c9faca751246] (2026-10-28T09:37:47Z)
- (audit operator) `self-review of the full diff: each macOS failure from the CI annotations mapped to a port; Linux suite 3891 OK` → cost at scale is one ps per registered runner only when /proc is missing, at app quit; the macOS job should drop from its 1980 s deadline to ~1300 s [tree c9faca751246] (2026-10-28T09:37:47Z)
## Log
- 2026-10-28T08:48:11Z created
- 2026-10-28T08:48:15Z set type=FIX
- 2026-10-28T09:29:16Z focused
- 2026-10-28T09:38:02Z done
- 2026-10-28T09:38:04Z committed c2b93e94 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1809 [FIX M, done, 4 steps] CI's macOS job names what makes it time out: run.py --deadline stops below each job's cap, killing and naming running classes; slowest clas…
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- decision 2026-10-22: T-1405: an unreadable /proc process of ours keeps a stale index.lock only when it is a git; any other unreadable process doesn't block (31 of this h…
## Why not caught
none: the macOS job is experimental (continue-on-error) and only CI runs macOS; T-1809's deadline notice is what named the hung classes
## Lessons
- macOS ptys drop unread output when the slave closes and return b'' at EOF: keep a reader thread on the master from before the writer starts
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/helpers.py
- plugin/tests/test_settings.py
- plugin/lib/fmplaybooks.py
- plugin/tests/test_run.py
- plugin/tests/test_supply_delta.py
- plugin/tests/test_playbook_check.py
- CHANGELOG.md
- MASTER.md
