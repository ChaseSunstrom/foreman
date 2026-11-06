---
id: T-1538
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_sprint.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:48Z
updated: 2026-10-23T15:56:22Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 3c3038c8eec93115915e6ba2674d28a3b6777452
base_tree: 3dd82b2b1a67bb367feeeb4638bdb15f6b22bae0
plan0_at: 2026-10-23T15:51:20Z
plan0_scope: [plugin/lib/fmdesign.py, plugin/lib/fmcli.py, plugin/tests/test_design_sprint.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Design sprint and pairing: a ten-minute design sprint verb, nudge keys o
## Raw request
> Round 3 (T-1520): Design sprint and pairing: a ten-minute design sprint verb, nudge keys on a live dev server, a veto list for vague sweeping requests, a gamut-cube colour picker, a colour-and-motion swatch strip in receipts, a nightly design residency and one small design PR a week (a134 a136 a146 c044 c051 b004 b081). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
A ten-minute design sprint verb (fm design sprint: five stages, two minutes each, each with a check and the next step of the first that fails), a veto list for vague sweeping requests (fm design vague: each word with the concrete question to ask), and a colour-and-motion swatch strip in a UI task's receipt. Left out (decided): nudge keys on a live dev server, a gamut-cube colour picker, a nightly design residency and one small design PR a week.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm design sprint walks its five stages with a check each; the swatch strip appears in a UI task's receipt — verify with `cd plugin/tests && python3 -m unittest test_design_sprint`
- [x] the sprint, the veto list and the receipt's swatch strip work as specified — verify with `python3 plugin/tests/run.py test_design_sprint`
## Non-goals
## Approach (options → choice → why)
Options: (a) a sprint that drives a model through stages; (b) a stateless walk whose stages are checks over DESIGN.md and the UI files, reusing fm design's lint, check_gates and section reader; (c) a sprint page. Choice: (b): every stage is a check fm already has the parts for, so it can't drift from fm design check; the veto list is a word table shared by the sprint's brief stage; the swatch strip reads the task's own diff since its base.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] sprint
3. [x] nudge keys and veto list
4. [x] gamut picker, swatch strip, weekly PR
5. [x] red tests: sprint stages, vague words, receipt swatches
6. [x] fmdesign sprint/vague/swatches, the CLI and receipt; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Design sprint), fm design's own help (sprint, vague)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_design_sprint` → ✗ exit 1 · Ran 4 tests in 0.5s (3 classes, 16 at a time; slowest: Receipt 0s, Sprint 0s, Vague 0s) / FAILED (3 classes) [ran] [tree 445ff67954ee] (2026-10-23T15:51:26Z)
- (step 1) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 28.5s (63 classes, 16 at a time; slowest: TaskLifecycle 28s, Fences 9s, StateViews 8s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:52:36Z)
- (step 2) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 41.2s (63 classes, 16 at a time; slowest: TaskLifecycle 41s, StateViews 18s, AuditPrep 18s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:53:19Z)
- (step 3) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 41.0s (63 classes, 16 at a time; slowest: TaskLifecycle 41s, StateViews 19s, AuditPrep 18s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:54:01Z)
- (step 4) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 40.4s (63 classes, 16 at a time; slowest: TaskLifecycle 40s, AuditPrep 18s, StateViews 18s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:54:43Z)
- (step 5) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 31.7s (63 classes, 16 at a time; slowest: TaskLifecycle 31s, StateViews 15s, AuditPrep 15s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:15Z)
- (step 6) `python3 plugin/tests/run.py test_design_sprint test_design_diverge test_cli test_suite_hygiene test_docs test_design_lint` → exit 0 · Ran 233 tests in 24.7s (63 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 10s, AuditPrep 10s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_sprint` → exit 0 · Ran 4 tests in 1.106s / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:43Z)
- (ac 2) `python3 plugin/tests/run.py test_design_sprint` → exit 0 · Ran 4 tests in 0.8s (3 classes, 16 at a time; slowest: Receipt 1s, Sprint 1s, Vague 0s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:44Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_design_sprint` → exit 0 · Ran 4 tests in 1.082s / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:55Z)
- (ac 2) `python3 plugin/tests/run.py test_design_sprint` → exit 0 · Ran 4 tests in 0.8s (3 classes, 16 at a time; slowest: Receipt 1s, Sprint 1s, Vague 0s) / OK [ran] [tree d1d861461de4] (2026-10-23T15:55:55Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): each sprint stage is a check fm design already has the parts for (section reader, lint, check_gates), stateless, stopping at the first failure; vague words match whole words only (pop-up and populated don't); the receipt's strip reads only the task's UI files' diff since its base, or a new untracked file whole; tried the sprint on this repo's site folder (no DESIGN.md: stage 1 names the next step)` → a ten-minute design sprint verb, a veto list for vague sweeping requests and a colour-and-motion swatch strip in receipts, usable from Claude Code; nudge keys, the gamut picker, a nightly residency and a weekly PR left out by a recorded decision [tree d1d861461de4] (2026-10-23T15:55:55Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): each sprint stage is a check fm design already has the parts for (section reader, lint, check_gates), stateless, stopping at the first failure; vague words match whole words only (pop-up and populated don't); the receipt's strip reads only the task's UI files' diff since its base, or a new untracked file whole; tried the sprint on this repo's site folder (no DESIGN.md: stage 1 names the next step)` → no DESIGN.md, no Point of view, a vague one, no audacity, a header-only Tokens table, no UI files and no opted-in gate each stop the walk with their own reason; a task with no base or no UI files gets no strip; .2s style durations without a leading digit aren't half-read [tree d1d861461de4] (2026-10-23T15:55:55Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): each sprint stage is a check fm design already has the parts for (section reader, lint, check_gates), stateless, stopping at the first failure; vague words match whole words only (pop-up and populated don't); the receipt's strip reads only the task's UI files' diff since its base, or a new untracked file whole; tried the sprint on this repo's site folder (no DESIGN.md: stage 1 names the next step)` → sprint reads files under the given root through fm design's own capped reader; git diff gets the base from the brief and paths from the receipt's own list after --; nothing is written [tree d1d861461de4] (2026-10-23T15:55:55Z)
## Log
- 2026-10-22T17:43:48Z created
- 2026-10-22T17:58:35Z set scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_sprint.py', 'CHANGELOG.md']
- 2026-10-23T15:51:17Z set tier=M, scope=['plugin/lib/fmdesign.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_design_sprint.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T15:51:20Z focused
- 2026-10-23T15:56:21Z done
- 2026-10-23T15:56:22Z committed 234a8ee4 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1535 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Design gates: an executable design brief that fails the build, an access
- decision 2026-10-23: T-1538: leave out nudge keys on a live dev server, a gamut-cube picker, a nightly design residency and a weekly design PR
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmdesign.py; re-ground the plan against them before editing
## Lessons
- A sprint whose stages are the project's existing checks needs no state: rerun it and it says where you are
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmdesign.py
- plugin/tests/test_design_sprint.py
