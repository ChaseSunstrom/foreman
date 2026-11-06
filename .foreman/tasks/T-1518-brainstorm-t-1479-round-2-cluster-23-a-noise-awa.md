---
id: T-1518
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrelease.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:44Z
updated: 2026-10-22T20:02:15Z
base: 176fd1db1ff84d68270493e2a5c90eed32dec5dd
base_tree: 8f09a3455dfe31e4fab84a3e0ece16d2e1aaebd5
plan0_at: 2026-10-22T19:20:38Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_verify_strength.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 23): a noise-aware perf evidence kind (repeated runs, s
## Raw request
> Brainstorm T-1479 round 2 (cluster 23): a noise-aware perf evidence kind (repeated runs, spread), the release canary spotting load flaps, and a before/after view plus a reading order for a UI task's receipt
## Interpretation
Evidence and review aids: a perf evidence kind that runs a command N times and records median and spread (noise-aware), the release canary spotting load flaps (a failure that passes on an idle rerun), and for UI tasks a before/after view and a reading order of the changed files. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task evidence --repeat 5 records median and spread; the canary marks a load flap; a UI task's receipt lists files in reading order — verify with `cd plugin/tests && python3 -m unittest test_verify_strength.Repeat`
## Non-goals
## Approach (options → choice → why)
Options: one-shot timings; chosen: fm task evidence --repeat N records median and spread; the canary reruns a failure when load is high; fm task receipt prints the reading order.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] load flap
3. [x] reading order
4. [x] repeat runs with median and spread
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verify_strength` → red as expected (exit 1) · Ran 15 tests in 24.2s (2 classes, 16 at a time; slowest: VerifyStrength 24s, Repeat 5s) / FAILED (1 classes) [ran] [tree c8f8c7818e35] (2026-10-22T19:28:05Z)
- (step 2) `python3 plugin/tests/run.py test_verify_strength.Repeat.test_the_canary_marks_a_load_flap_and_keeps_a_real_failure` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Repeat 0s) / OK [ran] [tree 663b7502f562] (2026-10-22T19:28:45Z)
- (step 3) `python3 plugin/tests/run.py test_verify_strength.Repeat.test_a_ui_tasks_receipt_lists_files_in_reading_order 2>&1 | grep -v "^ File" | tail -20` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Repeat 1s) / OK [ran] [tree 9fb57e18bcee] (2026-10-22T19:29:22Z)
- (step 3) `python3 plugin/tests/run.py test_verify_strength.Repeat.test_a_ui_tasks_receipt_lists_files_in_reading_order` → exit 0 · Ran 1 tests in 0.8s (1 classes, 16 at a time; slowest: Repeat 1s) / OK [ran] [tree 9fb57e18bcee] (2026-10-22T19:29:26Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength 2>&1 | grep -v "^ File" | tail -8` → exit 0 · Ran 15 tests in 14.3s (2 classes, 16 at a time; slowest: VerifyStrength 14s, Repeat 4s) / OK [ran] [tree ab068f8468c7] (2026-10-22T19:30:28Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 5 tests in 4.3s (1 classes, 16 at a time; slowest: Repeat 4s) / OK [ran] [tree ab068f8468c7] (2026-10-22T19:30:42Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 5 tests in 5.1s (1 classes, 16 at a time; slowest: Repeat 5s) / OK [ran] [tree ab068f8468c7] (2026-10-22T19:30:52Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 5 tests in 4.8s (1 classes, 16 at a time; slowest: Repeat 5s) / OK [ran] [tree 9adf8f6d519c] (2026-10-22T19:33:30Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 5 tests in 8.1s (1 classes, 16 at a time; slowest: Repeat 8s) / OK [ran] [tree 9adf8f6d519c] (2026-10-22T19:33:39Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength.Repeat` → red as expected (exit 1) · Ran 7 tests in 19.4s (1 classes, 16 at a time; slowest: Repeat 18s) / FAILED (1 classes) [ran] [tree 4b84260b10fe] (2026-10-22T19:44:55Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 7 tests in 11.7s (1 classes, 16 at a time; slowest: Repeat 11s) / OK [ran] [tree 9a11765492cc] (2026-10-22T19:46:45Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_strength.Repeat` → exit 0 · Ran 7 tests in 10.8s (1 classes, 16 at a time; slowest: Repeat 11s) / OK [ran] [tree 9a11765492cc] (2026-10-22T19:46:57Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_verify_strength.Repeat` → exit 0 · Ran 7 tests in 7.432s / OK [ran] [tree 697ca6d58db6] (2026-10-22T20:00:05Z)
- (step 1) `python3 plugin/tests/run.py test_verify_strength test_release` → exit 0 · Ran 47 tests in 16.2s (7 classes, 16 at a time; slowest: VerifyStrength 16s, Release 16s, BoardVerbs 14s) / OK [ran] [tree 697ca6d58db6] (2026-10-22T20:00:22Z)
- (step 2) `python3 plugin/tests/run.py test_verify_strength test_release` → exit 0 · Ran 47 tests in 16.2s (7 classes, 16 at a time; slowest: Release 16s, VerifyStrength 16s, BoardVerbs 10s) / OK [ran] [tree 697ca6d58db6] (2026-10-22T20:00:42Z)
- (step 3) `python3 plugin/tests/run.py test_verify_strength test_release` → exit 0 · Ran 47 tests in 15.2s (7 classes, 16 at a time; slowest: VerifyStrength 15s, Release 14s, Repeat 8s) / OK [ran] [tree 697ca6d58db6] (2026-10-22T20:00:58Z)
- (step 4) `python3 plugin/tests/run.py test_verify_strength test_release` → exit 0 · Ran 47 tests in 14.8s (7 classes, 16 at a time; slowest: VerifyStrength 15s, Release 13s, Repeat 8s) / OK [ran] [tree 697ca6d58db6] (2026-10-22T20:01:13Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_verify_strength.Repeat` → exit 0 · Ran 7 tests in 7.451s / OK [ran] [tree d5b5ea49889f] (2026-10-22T20:01:31Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 2 MEDIUM + 5 LOW fixed test-first in 901b1e22` → repeat runs with median and spread, load flaps in the canary, a reading-order receipt [tree d5b5ea49889f] (2026-10-22T20:01:31Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 2 MEDIUM + 5 LOW fixed test-first in 901b1e22` → each run goes through the same guarded run_command; a mixed set can't record exit 0; --repeat refuses typed results and --expect-fail; flaps are captured, never green [tree d5b5ea49889f] (2026-10-22T20:01:31Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 2 MEDIUM + 5 LOW fixed test-first in 901b1e22` → no run before the timeout returns 124; one finished run prints spread n/a; reruns only for real nonzero exits at high load, within 600 s; undecodable sentinel output is replaced, not fatal [tree d5b5ea49889f] (2026-10-22T20:01:31Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 2 MEDIUM + 5 LOW fixed test-first in 901b1e22` → Repeat tests red first; test_verify_strength and test_release pass [tree d5b5ea49889f] (2026-10-22T20:01:31Z)
## Log
- 2026-10-22T17:36:44Z created
- 2026-10-22T17:56:16Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-10-22T19:20:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1518.builder.md
- 2026-10-22T19:20:38Z focused
- 2026-10-22T19:25:25Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmrelease.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-10-22T19:41:43Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmrelease.py', 'plugin/lib/fmeco.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-10-22T19:46:29Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmrelease.py', 'plugin/tests/test_verify_strength.py', 'CHANGELOG.md']
- 2026-10-22T19:52:06Z merged worktree-agent-adf67ac8e42984dcd (4 file(s))
- 2026-10-22T19:52:07Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-adf67ac8e42984dcd
- 2026-10-22T19:59:57Z focused
- 2026-10-22T20:01:22Z scope: fmrelease.py (the canary) widened by the builder; other files from other tasks' merges
- 2026-10-22T20:02:13Z done
- 2026-10-22T20:02:15Z committed 3e0f5f5a (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-0780 [FEATURE S, done, 2 steps] Audit findings reach the host's review UI: fm audit prep asks for ReportFindings fields and tells the main thread to report them — less…
- T-1380 [FIX S, done, 2 steps] Sentinel skips point-in-time checks and reruns a failure once
- decision 2026-10-14: [revisit: after 2026-10-15] Round 1 of the T-0760 brainstorm: build 12 briefs (T-0775..T-0786) plus the 5 discovered fixes (T-0759, T-0765, T-0767, …
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrelease.py, plugin/tests/test_verify_strength.py; re-ground the plan against them before editing
## Why not caught
the first canary rerun treated any second-try pass as load
## Lessons
- A flap detector must require the condition it blames (high load) before excusing a failure, or every intermittent regression reads as noise
## Files touched
- plugin/tests/test_verify_strength.py
- plugin/lib/fmrelease.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- README.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmsettings.py
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/test_code_tui.py
- plugin/tests/test_settings.py
