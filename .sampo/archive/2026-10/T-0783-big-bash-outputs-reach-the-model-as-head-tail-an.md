---
id: T-0783
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/hooks/compact, plugin/lib/fmsetup.py, plugin/lib/fmcli.py, plugin/tests/test_compact.py, plugin/tests/test_setup.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-14T15:55:14Z
updated: 2026-10-14T17:46:25Z
inferred_deps: [T-0760]
inferred_why: T-0760: named in its request
group: hook latency and output token cost
base: aaeb2f3b1a01e37e1e847ea77e20357f753eb769
base_tree: 494db01b0a58cf7fcab1b6be6d07db2177775315
verified: strong
---
# Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in)
## Raw request
> PERF: Big Bash outputs reach the model as head, tail and error lines with the full text in a file
> CONTEXT: T-0760, cluster token-economy. Measured over 30 days: 44.3M chars of Bash results; outputs over 4,000 chars hold 7.3M chars above that line (16.6%). PostToolUse hookSpecificOutput.updatedToolOutput {stdout, stderr, interrupted, isImage} replaces what Claude sees (2.1.121); needs a sync hook (Foreman's PostToolUse is async). Must never hide a failing line; fm quiet already does this by hand.
> DONE-WHEN: a sync Bash-only PostToolUse handler, opt-in via fm setting, rewrites outputs over a threshold to head + tail + every error/fail/warn line + the path of the full text; under the threshold it adds no measurable latency (bench_hooks); a test covers a failing pytest output keeping its failure lines.
## Interpretation
30 days of Bash results: 44.3M chars; outputs over 4,000 chars carry 7.3M chars beyond that line (16.6%), each re-read every later turn. PostToolUse hookSpecificOutput.updatedToolOutput {stdout, stderr, interrupted, isImage} replaces what Claude sees (2.1.121) but needs a synchronous hook; Foreman's PostToolUse is async. A separate sync Bash-only PostToolUse handler, on only when the user turns it on (fm compact-output on), rewrites outputs over 6,000 chars: first 40 lines, every line that reads as an error/failure/warning (deduplicated, capped), last 60 lines, and the path of the full text. Never touches outputs under the threshold, images or interrupted runs.
## Assumptions (confidence)
## Acceptance criteria
- [x] with compact output on, a 20,000-char failing test output comes back under 8,000 chars keeping every FAIL/Error line and the full-text path; off, the hook returns nothing — verify with `cd plugin/tests && python3 -m unittest test_hooks.PostToolUse.test_compact_output`
- [x] bench_hooks stays within budget with the new handler — verify with `python3 plugin/tests/bench_hooks.py --runs 20`
## Non-goals
## Approach (options → choice → why)
Options: always on (risk: hiding what the model needed costs retries); opt-in setting; teach fm quiet harder (already exists, rarely used). Chose opt-in with the full text one Read away; measure tokens saved per session in fm cost before suggesting it on.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing hook test
2. [x] fm compact-output on|off and the sync handler
3. [x] hooks.json entry, bench, MASTER.md
## Resume here
<!-- auto -->
- 2026-10-14T17:06:04Z step 1/3: Failing hook test
- git: foreman/build; 0 uncommitted
## Docs impact
MASTER.md: CLI line and a Compact output bullet with the measured numbers
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_compact -k test_compact_output_is_a_user_hook_only_while_on` → ✗ exit 1 · Ran 4 tests in 0.3s (2 classes, 16 at a time; slowest: Install 0s, Compact 0s) / FAILED (2 classes) [ran] [tree 77b3853ee65c] (2026-10-14T17:24:51Z)
- (step 2) `python3 plugin/tests/run.py test_compact test_setup` → exit 0 · Ran 33 tests in 1.6s (7 classes, 16 at a time; slowest: Install 1s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 3112e1c456cc] (2026-10-14T17:26:59Z)
- (ac 1) `python3 plugin/tests/run.py test_compact` → exit 0 · Ran 5 tests in 0.5s (2 classes, 16 at a time; slowest: Install 0s, Compact 0s) / OK [ran] [tree 3112e1c456cc] (2026-10-14T17:27:00Z)
- (ac 2) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                35.1    41.6     150  [0] / SessionEnd                  31.2    34.6     150  [0] [ran] [tree 3112e1c456cc] (2026-10-14T17:27:13Z)
- (step 3) `python3 -c "import sys; sys.path.insert(0,'plugin/lib'); import fmdoctor as d; r=d.check_self_docs(); print(r.status, r.detail); sys.exit(r.status!='PASS')"` → exit 0 · PASS docs match the code [ran] [tree 9a32a9ad6eb6] (2026-10-14T17:27:22Z)
- (step 1) `python3 plugin/tests/run.py test_compact -k test_compact_output_is_a_user_hook_only_while_on` → exit 0 · Ran 5 tests in 0.5s (2 classes, 16 at a time; slowest: Install 0s, Compact 0s) / OK [ran] [tree d08722cb5373] (2026-10-14T17:36:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PostToolUse.test_compact_output` → ✗ exit 1 · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree d08722cb5373] (2026-10-14T17:36:32Z)
- (ac 2) `python3 plugin/tests/bench_hooks.py --runs 20` → exit 0 · Notification                32.9    34.8     150  [0] / SessionEnd                  29.9    32.9     150  [0] [ran] [tree d08722cb5373] (2026-10-14T17:36:32Z)
- (step 2) `python3 plugin/tests/run.py test_compact test_setup` → exit 0 · Ran 34 tests in 1.5s (8 classes, 16 at a time; slowest: Install 1s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 2e92bea492bf] (2026-10-14T17:37:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PostToolUse.test_compact_output` → exit 0 · Ran 1 test in 0.138s / OK [ran] [tree 2e92bea492bf] (2026-10-14T17:37:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PostToolUse.test_compact_output` → exit 0 · Ran 1 test in 0.142s / OK [ran] [tree fa2a1fa2c765] (2026-10-14T17:44:25Z)
- (audit intent) `self: script, wiring and docs read; off is no hook at all; on adds one PostToolUse Bash hook pointing at the running plugin's script (backed up; off and uninstall remove only it); the script leaves outputs under 6,000 chars, interrupted runs and images alone, writes the full text under state/outputs/<session>/, and keeps the first 40 and last 60 lines plus every distinct failure-looking line (exception names included), long lines clipped around the failure word` → the user wanted large token savings; measured ~1.04M tokens over 30 days of this machine's real Bash output, opt-in so a missed detail never costs a retry unasked [tree fa2a1fa2c765] (2026-10-14T17:44:25Z)
- (audit edge) `self: script, wiring and docs read; off is no hook at all; on adds one PostToolUse Bash hook pointing at the running plugin's script (backed up; off and uninstall remove only it); the script leaves outputs under 6,000 chars, interrupted runs and images alone, writes the full text under state/outputs/<session>/, and keeps the first 40 and last 60 lines plus every distinct failure-looking line (exception names included), long lines clipped around the failure word` → the end-to-end test caught exception class names (AssertionError) slipping past the word-boundary pattern and the hook command pointing at the state home instead of the plugin; both fixed; on 1,090 real outputs every distinct failure line is kept [tree fa2a1fa2c765] (2026-10-14T17:44:25Z)
- (step 2) `python3 plugin/tests/run.py test_compact test_setup` → exit 0 · Ran 34 tests in 1.5s (8 classes, 16 at a time; slowest: Install 1s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree aa1a5ef44118] (2026-10-14T17:44:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_hooks.PostToolUse.test_compact_output` → exit 0 · Ran 1 test in 0.139s / OK [ran] [tree aa1a5ef44118] (2026-10-14T17:44:45Z)
- (audit intent) `self: script, wiring and docs read; off is no hook at all; on adds one PostToolUse Bash hook pointing at the running plugin's script (backed up; off and uninstall remove only it); the script leaves outputs under 6,000 chars, interrupted runs and images alone, writes the full text under state/outputs/<session>/, and keeps the first 40 and last 60 lines plus every distinct failure-looking line (exception names included), long lines clipped around the failure word` → the user wanted large token savings; measured ~1.04M tokens over 30 days of this machine's real Bash output, opt-in so a missed detail never costs a retry unasked [tree aa1a5ef44118] (2026-10-14T17:46:24Z)
- (audit adversary) `self: script, wiring and docs read; off is no hook at all; on adds one PostToolUse Bash hook pointing at the running plugin's script (backed up; off and uninstall remove only it); the script leaves outputs under 6,000 chars, interrupted runs and images alone, writes the full text under state/outputs/<session>/, and keeps the first 40 and last 60 lines plus every distinct failure-looking line (exception names included), long lines clipped around the failure word` → saved outputs can hold secrets, so the folder is 0700 and files 0600 opened with O_NOFOLLOW (checked), like Claude Code's own transcripts; sha1 only names files; the hook reads its payload from Claude Code and runs nothing; pruning captured as T-0811 [tree aa1a5ef44118] (2026-10-14T17:46:24Z)
- (audit edge) `self: script, wiring and docs read; off is no hook at all; on adds one PostToolUse Bash hook pointing at the running plugin's script (backed up; off and uninstall remove only it); the script leaves outputs under 6,000 chars, interrupted runs and images alone, writes the full text under state/outputs/<session>/, and keeps the first 40 and last 60 lines plus every distinct failure-looking line (exception names included), long lines clipped around the failure word` → the end-to-end test caught exception class names slipping past the word-boundary pattern and the hook command pointing at the state home instead of the plugin; both fixed [tree aa1a5ef44118] (2026-10-14T17:46:24Z)
## Log
- 2026-10-14T15:55:14Z created
- 2026-10-14T16:10:07Z planned from capture
- 2026-10-14T17:05:35Z focused
- 2026-10-14T17:06:05Z paused: focus moved to T-0804
- 2026-10-14T17:24:35Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-14T17:24:35Z focused
- 2026-10-14T17:24:35Z set scope=['plugin/hooks/compact', 'plugin/lib/fmsetup.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_compact.py', 'plugin/tests/test_setup.py', 'MASTER.md']
- 2026-10-14T17:24:35Z steer (design): no plugin hooks.json entry (a sync handler would start Python on every Bash call while the feature is off); fm compact-output on|off adds/removes a PostToolUse Bash hook in ~/.claude/settings.json (backed up, like the wiring; fm uninstall-user removes it) that runs plugin/hooks/compact, a standalone stdlib-only script; it takes effect in new sessions
- 2026-10-14T17:36:13Z scope: fmcli.py also lists compact-output in fm help's tiers (test_help pins every command once)
- 2026-10-14T17:37:07Z scope: test_hooks.py holds the criterion's end-to-end test (PostToolUse.test_compact_output, the name criterion 1 was written with); it caught _compact_cmd pointing at foreman_home/plugin instead of the running plugin root
- 2026-10-14T17:43:00Z scope: test_suite_hygiene.py skips folders in plugin/hooks (loading the compact script for the measurement left hooks/__pycache__/ and the undefined-names test crashed on it)
- 2026-10-14T17:46:24Z scope: test_suite_hygiene.py skips folders under plugin/hooks (a __pycache__ from loading the compact script crashed it)
- 2026-10-14T17:46:24Z done
- 2026-10-14T17:46:25Z committed ad52fc6 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- T-0702 [FEATURE M, dropped, 3 steps] Frontier 02 — Context firewall and cheap reader
- research claude-code-features-20261014: Foreman uses: 14 hook events, 4 async hooks, 6 agents (tools/model/color only), output style, statusline.
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_hooks.py
## Preflight
Changed in scope since this was planned (2026-10-14): MASTER.md, plugin/hooks/hooks.json, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py; re-ground the plan against them before editing
## Measurements
30 days of this machine's Bash results over 6,000 chars: 1,090 outputs, 10,752,367 → 6,609,592 characters (39% less, ~1.04M tokens); every distinct failure-looking line kept (10 outputs repeat a line at another indentation, shown once); hook p50 14.8 ms (small) / 18.8 ms (3,000 lines); off: no hook, 0 ms
## Lessons
- measure a lossy compressor on the real corpus and test it end to end: two versions looked right in unit tests and dropped failures
## Plan gaps
- failed first: step 1 Failing hook test
## Files touched
- plugin/tests/test_compact.py
- plugin/tests/test_setup.py
- plugin/hooks/compact
- plugin/lib/fmcli.py
- plugin/lib/fmsetup.py
- MASTER.md
- plugin/tests/test_hooks.py
- plugin/tests/test_suite_hygiene.py
- plugin/lib/fmlanes.py
- plugin/tests/test_lanes.py
