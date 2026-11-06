---
id: T-1916
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_which.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-29T04:47:56Z
updated: 2026-10-29T05:29:08Z
base: 9cc8efbdefa3bff0aa601b67dfa5793f1b7e122e
base_tree: ded7edcabe947ae904c0c244062c8bb6480ca761
plan0_at: 2026-10-29T05:20:33Z
plan0_scope: [plugin/lib/fmrecall.py, plugin/lib/fmcli.py, plugin/tests/test_which.py, CHANGELOG.md]
verified: strong
---
# Fm which and fm help name a command's actions
## Raw request
> FIX: fm which and fm help can't name fm lane's actions (merge, brief, rm…): lane takes a choices positional, not subcommands, so 'merge a lane' finds only fm lane's summary
## Interpretation
fm lane's actions are argparse choices, not subparsers, so fm which and fm help WORDS never see 'lane merge'; index each choice the help names with words
## Assumptions (confidence)
## Acceptance criteria
- [x] fm which 'merge a lane' finds fm lane merge — verify with `python3 plugin/tests/run.py test_which test_help test_recall test_cli`
## Non-goals
## Approach (options → choice → why)
Options: a hand list of action docs; parse 'name: words' out of each subcommand's help; index argparse choices with the help clause naming them. Choice: choices plus their help clause, skipping a bare choice with no words. Why: one source (the help), nothing to drift, and fm help and fm which share verb_docs
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test in test_which
2. [x] Action choices indexed in verb_docs; lane help names merge; green
## Resume here
<!-- auto -->
- 2026-10-29T05:24:01Z steps 2/2 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/tests/test_which.py
- touched since last checkpoint: CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmrecall.py, plugin/tests/test_which.py
## Docs impact
CHANGELOG.md
## Verification evidence
- `python3 plugin/tests/run.py test_which` → ✗ exit 1 · Ran 16 tests in 3.4s (3 classes, 16 at a time; slowest: Which 2s, Snapshots 0s, Extract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 248af0e99b79] (2026-10-29T05:22:03Z)
- `python3 plugin/tests/run.py test_which` → exit 0 · Ran 16 tests in 2.9s (3 classes, 16 at a time; slowest: Which 3s, Snapshots 0s, Extract 0s) / OK [ran] [tree 248af0e99b79] (2026-10-29T05:22:03Z)
- (step 1) `python3 plugin/tests/run.py test_which` → exit 0 · Ran 16 tests in 2.9s (3 classes, 16 at a time; slowest: Which 3s, Snapshots 0s, Extract 0s) / OK [ran] [tree 248af0e99b79] (2026-10-29T05:22:09Z)
- (step 2) `python3 plugin/tests/run.py -j 4 test_which test_help test_recall test_cli` → exit 0 · Ran 173 tests in 28.2s (51 classes, 4 at a time; slowest: TaskLifecycle 21s, Recall 16s, CaptureAndIntake 7s) / OK [ran] [tree 248af0e99b79] (2026-10-29T05:22:38Z)
- (step 2) `python3 plugin/tests/run.py test_which test_docs test_help test_recall test_cli` → exit 0 · Ran 244 tests in 25.5s (66 classes, 16 at a time; slowest: TaskLifecycle 25s, Recall 20s, CaptureAndIntake 11s) / OK [ran] [tree 5a8fbaf2dff7] (2026-10-29T05:28:01Z)
- (ac 1) `python3 plugin/tests/run.py test_which test_help test_recall test_cli` → exit 0 · Ran 173 tests in 24.9s (51 classes, 16 at a time; slowest: TaskLifecycle 25s, Recall 19s, CaptureAndIntake 10s) / OK [ran] [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
- (audit intent) `one fm-reviewer pass (5 lenses): 4 findings, all fixed test-first — tie-break toward the command, positional help read, self-restating actions dropped, regex commented` → fm which/help name lane merge, lane resume and playbooks blame as their own commands [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
- (audit adversary) `one fm-reviewer pass (5 lenses): 4 findings, all fixed test-first — tie-break toward the command, positional help read, self-restating actions dropped, regex commented` → choices are parser-defined and re.escape'd; no untrusted input reaches the regex [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
- (audit edge) `one fm-reviewer pass (5 lenses): 4 findings, all fixed test-first — tie-break toward the command, positional help read, self-restating actions dropped, regex commented` → a score tie goes to the shorter name (mcp over mcp new); an action that only restates its command (round close) gets no entry [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
- (audit operator) `one fm-reviewer pass (5 lenses): 4 findings, all fixed test-first — tie-break toward the command, positional help read, self-restating actions dropped, regex commented` → a few dozen regex matches per verb_docs call; test_docs and the criterion modules green [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
- (audit maintainer) `one fm-reviewer pass (5 lenses): 4 findings, all fixed test-first — tie-break toward the command, positional help read, self-restating actions dropped, regex commented` → docstring names T-1916; the regex's intent is commented [tree 5a8fbaf2dff7] (2026-10-29T05:28:38Z)
## Log
- 2026-10-29T04:47:56Z created
- 2026-10-29T05:17:28Z planned from capture
- 2026-10-29T05:17:56Z planned from capture
- 2026-10-29T05:20:32Z focused
- 2026-10-29T05:29:06Z done
- 2026-10-29T05:29:08Z committed 4f3b5f35 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1908 [FIX M, done, 6 steps] FIX: fm which misses subcommands and the rules' own phrases: 'drop a task', 'defer a task' — lesson: an index built from top-level verbs mi…
- T-1909 [FIX M, done, 0 steps] Fm help task refuses ('nothing to look up in task, only words like can, do and it') becaus
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- decision 2026-10-23: Cause: hooks handed Claude the exact fm command each turn, so it never loaded the skill describing the step; descriptions used Foreman jargon or use…
- similar finished tasks took 0–6 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_recall.py
## Why not caught
none: fm which only indexed subparsers; nothing tested actions given as choices of an action positional, which this task now covers
## Lessons
- A ranking change needs every test that reads the ranking, not just the criterion's modules: grep the function's callers' tests (test_docs held can's order).
## Files touched
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmrecall.py
- plugin/tests/test_which.py
