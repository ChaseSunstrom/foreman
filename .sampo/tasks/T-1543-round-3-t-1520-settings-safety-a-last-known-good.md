---
id: T-1543
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings_safety.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:49Z
updated: 2026-10-22T21:08:52Z
base: 916ce98a0ac104308bf013d633fcd92d65c3fa29
base_tree: dd1e2c8772b2a8e501c1f787507bd08e1a61e2f0
plan0_at: 2026-10-22T20:37:57Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings_safety.py, CHANGELOG.md]
verified: strong
---
# Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misren
## Raw request
> Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misrenders, external-edit merge when tui.toml changes under the app, a scope picker on save (run, project, everywhere), settings a repo's policy pins, bisecting the setting that broke the screen, detecting config that works in the app but not headless, and a monkey test of the settings screen (b142 a122 a117 c136 b016 b143 c143 a075). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Round 3 (T-1520): Settings safety: a last-known-good config that boots if a new one misrenders, external-edit merge when tui.toml changes under the app, a scope picker on save (run, project, everywhere), settings a repo's policy pins, bisecting the setting that broke the screen, detecting config that works in the app but not headless, and a monkey test of the settings screen (b142 a122 a117 c136 b016 b143 c143 a075). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently. 
## Assumptions (confidence)
## Acceptance criteria
- [x] a config that fails to render boots the last good one and says so; an external edit merges; fm settings bisect names the bad key — verify with `cd plugin/tests && python3 -m unittest test_settings_safety`
## Non-goals
## Approach (options → choice → why)
Options: trust every write; chosen: a last-known-good tui.toml kept on each good start and booted when a new one fails to render, a merge when tui.toml changes under the running app, a scope picker on save (this run, this project, everywhere), settings a repo's policy pins (shown locked with the reason), fm settings bisect to find the setting that broke the screen, a warning for config that works in the app but not headless, and a monkey test of the settings screen. Same for the pane's options where they apply.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] last-known-good and external merge
3. [x] scopes and policy pins: deferred, captured as T-1611 (scope picker, repo policy pins), with T-1612 (headless check) and T-1613 (Claude Code pane parity)
4. [x] bisect and monkey test (the headless check went to T-1612)
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_safety` → ✗ exit 1 · Ran 12 tests in 0.3s (4 classes, 16 at a time; slowest: ExternalEdit 0s, LastKnownGood 0s, Bisect 0s) / FAILED (4 classes) [ran] [tree 133526e56240] (2026-10-22T20:43:49Z)
- (step 2) `python3 plugin/tests/run.py test_settings_safety test_settings test_code_tui` → exit 0 · Ran 215 tests in 10.3s (36 classes, 16 at a time; slowest: Command 10s, Fuzz 9s, Events 5s) / OK [ran] [tree 83f5795cad73] (2026-10-22T20:50:37Z)
- (step 4) `python3 plugin/tests/run.py test_settings_safety` → exit 0 · Ran 12 tests in 0.9s (4 classes, 16 at a time; slowest: Monkey 1s, Bisect 0s, ExternalEdit 0s) / OK [ran] [tree 83f5795cad73] (2026-10-22T20:50:38Z)
- (step 4) `python3 plugin/tests/run.py test_settings_safety test_bus` → ✗ exit 1 · Ran 35 tests in 17.9s (10 classes, 16 at a time; slowest: Watch 18s, ExternalEdit 11s, Bus 9s) / FAILED (2 classes) [ran] [tree f260b8b441f1] (2026-10-22T20:57:06Z)
- (step 4) `python3 plugin/tests/run.py test_settings_safety test_bus test_settings test_code_tui` → exit 0 · Ran 238 tests in 24.4s (42 classes, 16 at a time; slowest: Command 24s, Fuzz 20s, Watch 19s) / OK [ran] [tree a41931c49c13] (2026-10-22T20:59:23Z)
- (step 1) `python3 plugin/tests/run.py test_settings_safety test_bus test_settings` → exit 0 · Ran 72 tests in 10.5s (20 classes, 16 at a time; slowest: Watch 10s, Approvals 5s, Bus 5s) / OK [ran] [tree 7b4848d2ef23] (2026-10-22T21:07:17Z)
- (step 3) `fm task show T-1611 | grep -q 'scope picker' && fm task show T-1612 | grep -q headless && fm task show T-1613 | grep -q 'pane parity'` → exit 0 · (no output) [ran] [tree 7b4848d2ef23] (2026-10-22T21:07:18Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings_safety` → exit 0 · Ran 17 tests in 1.483s / OK [ran] [tree 7b4848d2ef23] (2026-10-22T21:07:20Z)
- (audit adversary) `fm-reviewer adversary pass (research/T-1543-review.md)` → watcher hang on a FIFO and unbounded reads: fixed in the shared reader (_read_raw: regular file, non-blocking open, 1 MB cap, stat-gated reread), tested with a FIFO, /dev/zero link and 1.2 MB file; last-good can't smuggle a refused key (tested); bisect writes only temp copies [tree 7b4848d2ef23] (2026-10-22T21:07:43Z)
- (audit edge) `review edge lens` → unreadable file said once; z cycle reloads through _settings_reload; invalid-TOML conflict named as such [tree 7b4848d2ef23] (2026-10-22T21:07:43Z)
- (audit operator) `fm settings bisect and the app's boot fallback, tests and the settings.md command` → bisect names the key; boot says it used the last good copy; ponytail: same-size edit in one clock tick waits for the next change [tree 7b4848d2ef23] (2026-10-22T21:07:44Z)
- (audit maintainer) `review maintainer lens` → _build comment added; monkey test reaches a :set; fm bus send usage crash fixed with a test [tree 7b4848d2ef23] (2026-10-22T21:07:45Z)
- (audit design) `review design lens (no screenshots)` → status-bar notes only; no layout change [tree 7b4848d2ef23] (2026-10-22T21:07:45Z)
- (audit intent) `criterion: last good boots and says so; external edit merges; bisect names the bad key` → met (17 tests after merge); scope picker, policy pins, headless check and pane parity deferred to T-1611..T-1613 [tree 7b4848d2ef23] (2026-10-22T21:07:47Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings_safety` → exit 0 · Ran 17 tests in 1.840s / OK [ran] [tree 7b4848d2ef23] (2026-10-22T21:08:02Z)
- (audit adversary) `one fm-reviewer five-lens + design pass; 6 findings fixed test-first by the builder; criterion green after the merge` → tui.toml reads bounded and non-blocking everywhere; the last good copy goes through the same schema [tree 7b4848d2ef23] (2026-10-22T21:08:02Z)
- (audit edge) `one fm-reviewer five-lens + design pass; 6 findings fixed test-first by the builder; criterion green after the merge` → unreadable or invalid tui.toml said once, the running look kept [tree 7b4848d2ef23] (2026-10-22T21:08:02Z)
## Log
- 2026-10-22T17:43:49Z created
- 2026-10-22T18:06:10Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings_safety.py', 'CHANGELOG.md']
- 2026-10-22T20:37:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1543.builder.md
- 2026-10-22T20:37:56Z focused
- 2026-10-22T20:58:54Z scope: plugin/commands/settings.md (bisect for Claude Code parity: /foreman:settings bisect), plugin/lib/fmbus.py + plugin/tests/test_bus.py (one-line fm bus send usage crash, asked by the coordinator)
- 2026-10-22T21:06:36Z merged worktree-agent-ab88041037341cbf8 (8 file(s))
- 2026-10-22T21:06:39Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ab88041037341cbf8
- 2026-10-22T21:06:40Z focused
- 2026-10-22T21:08:52Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1510 [FEATURE M, done, 3 steps] Brainstorm T-1479 round 2 (cluster 15): fm code config get/set/diff/export/undo on tui.tom — lesson: A share code is a paste from someo…
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_settings_safety.py; re-ground the plan against them before editing
## Why not caught
the watcher's tests only edited a regular file
## Lessons
- A file watcher must stat before it opens: a FIFO or device swapped in for a config file blocks open() and freezes the UI thread
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_settings_safety.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcli.py
- plugin/commands/settings.md
- plugin/tests/test_bus.py
- plugin/lib/fmbus.py
- CHANGELOG.md
