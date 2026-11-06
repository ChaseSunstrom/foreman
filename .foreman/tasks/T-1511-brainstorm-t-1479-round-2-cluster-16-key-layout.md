---
id: T-1511
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/commands/settings.md, plugin/tests/test_code_tui.py, CHANGELOG.md, plugin/lib/fmcode.py, plugin/tests/test_settings.py, plugin/lib/fmcli.py]
depends_on: []
source: followup
created: 2026-10-22T17:36:41Z
updated: 2026-10-22T20:36:54Z
base: dae2bc0356d9333f304a393a4e5728dfb0d008d4
base_tree: 49abcd4592c4f6c68f961747c84c2e16877821ec
plan0_at: 2026-10-22T20:04:43Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/commands/settings.md, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 16): key, layout and runner editors inside the fm code
## Raw request
> Brainstorm T-1479 round 2 (cluster 16): key, layout and runner editors inside the fm code app's settings screen (after T-1497): press a key to bind it, drag panels by keys, test a runner in place
## Interpretation
Inside fm code app's settings screen (T-1497): press a key to bind it to a command, move panels with keys to change the layout, and test a runner from code.toml in place. The /foreman:settings command shows the same bindings and layout for the plugin side. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] a captured key binds to a command and persists; a panel moved by keys changes layout; a runner test reports its result — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Editors`
## Non-goals
## Approach (options → choice → why)
Options: a separate editor app; chosen: three sub-views of the settings overlay, each writing through the comment-preserving writer.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] key capture
3. [x] layout by keys
4. [x] runner test
## Resume here
## Docs impact
plugin/commands/settings.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k Editors -k test_list_keys_or_layout` → ✗ exit 1 · Ran 7 tests in 0.3s (2 classes, 16 at a time; slowest: Command 0s, Editors 0s) / FAILED (2 classes) [ran] [tree 0ad855265b74] (2026-10-22T20:09:54Z)
- (step 2) `python3 plugin/tests/run.py -k Editors.test_a_captured -k Editors.test_capture_refuses` → exit 0 · Ran 2 tests in 0.2s (1 classes, 16 at a time; slowest: Editors 0s) / OK [ran] [tree 7f00fd822cdd] (2026-10-22T20:15:04Z)
- (step 3) `python3 plugin/tests/run.py -k Editors.test_a_panel_moved` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Editors 0s) / OK [ran] [tree 7f00fd822cdd] (2026-10-22T20:15:04Z)
- (step 4) `python3 plugin/tests/run.py -k Editors.test_a_runner -k Editors.test_only_a_runner -k test_list_keys_or_layout` → exit 0 · Ran 4 tests in 0.8s (2 classes, 16 at a time; slowest: Editors 1s, Command 0s) / OK [ran] [tree 7f00fd822cdd] (2026-10-22T20:15:05Z)
- (step 1) `python3 plugin/tests/run.py -k Editors -k test_list_keys_or_layout` → ✗ exit 1 · Ran 13 tests in 5.9s (2 classes, 16 at a time; slowest: Editors 6s, Command 0s) / FAILED (2 classes) [ran] [tree f7df1a4700a9] (2026-10-22T20:26:59Z)
- (step 2) `python3 plugin/tests/run.py -k Editors.test_a_captured -k Editors.test_capture_refuses -k Editors.test_arrows_pages -k Editors.test_the_last_key -k Editors.test_a_quit_help` → exit 0 · Ran 5 tests in 0.4s (1 classes, 16 at a time; slowest: Editors 0s) / OK [ran] [tree 77d7b7658022] (2026-10-22T20:29:37Z)
- (step 3) `python3 plugin/tests/run.py -k Editors.test_a_panel_moved -k Editors.test_a_failure_between -k Editors.test_the_layout_editor_says` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: Editors 0s) / OK [ran] [tree 77d7b7658022] (2026-10-22T20:29:38Z)
- (step 4) `python3 plugin/tests/run.py -k Editors.test_a_runner -k Editors.test_only_a_runner -k Editors.test_quitting_mid -k test_list_keys_or_layout` → exit 0 · Ran 5 tests in 0.8s (2 classes, 16 at a time; slowest: Editors 1s, Command 0s) / OK [ran] [tree 77d7b7658022] (2026-10-22T20:29:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Editors` → exit 0 · Ran 12 tests in 0.698s / OK [ran] [tree 2d369cb4f055] (2026-10-22T20:34:02Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_settings test_code` → exit 0 · Ran 353 tests in 76.5s (59 classes, 16 at a time; slowest: Worker 76s, Fakes 45s, Bench 20s) / OK [ran] [tree 2d369cb4f055] (2026-10-22T20:35:28Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Editors` → exit 0 · Ran 12 tests in 0.617s / OK [ran] [tree 453a71aa5c17] (2026-10-22T20:35:31Z)
- (audit intent) `one fm-reviewer pass: 3 MEDIUM + 3 LOW fixed test-first in 340d33a` → key capture, layout by keys, runner test, and the same views from /foreman:settings [tree 453a71aa5c17] (2026-10-22T20:35:31Z)
- (audit adversary) `one fm-reviewer pass: 3 MEDIUM + 3 LOW fixed test-first in 340d33a` → only registered runners run, with the dangerous-flag check and nothing auto-approved; a quit kills a runner test's process group; every write through set_apps (guard, lock, one history entry) [tree 453a71aa5c17] (2026-10-22T20:35:31Z)
- (audit edge) `one fm-reviewer pass: 3 MEDIUM + 3 LOW fixed test-first in 340d33a` → binding can't lock lists (arrows, pages, Enter always work there); a failure between layout keys writes nothing; narrow screens say a move won't show yet [tree 453a71aa5c17] (2026-10-22T20:35:31Z)
- (audit maintainer) `one fm-reviewer pass: 3 MEDIUM + 3 LOW fixed test-first in 340d33a` → Editors tests red first; test_code_tui, test_settings and test_code pass [tree 453a71aa5c17] (2026-10-22T20:35:31Z)
## Log
- 2026-10-22T17:36:41Z created
- 2026-10-22T17:46:47Z steer (T-1520): plugin parity: key and layout editing has a Claude Code counterpart (/foreman:settings shows the bindings; the foreman-ui pane's layout options are edited through the same schema)
- 2026-10-22T17:55:46Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/commands/settings.md', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-22T20:04:20Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1511.builder.md
- 2026-10-22T20:04:43Z focused
- 2026-10-22T20:09:43Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/commands/settings.md', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'plugin/lib/fmcode.py', 'plugin/tests/test_settings.py']
- 2026-10-22T20:09:43Z scope: + fmcode.py (test_runner: the runner test beside worker_argv/run_bounded) and test_settings.py (fm settings list keys|layout for /foreman:settings)
- 2026-10-22T20:26:12Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/commands/settings.md', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'plugin/lib/fmcode.py', 'plugin/tests/test_settings.py', 'plugin/lib/fmcli.py']
- 2026-10-22T20:26:13Z steer: review fixes (navigation lock-out, live reserved keys, runner test killed on stop, one-write multi-key set_app, list group help, narrow note); scope + fmcli.py (settings key help)
- 2026-10-22T20:33:56Z merged worktree-agent-a56203e5c905cc10e (7 file(s))
- 2026-10-22T20:33:58Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a56203e5c905cc10e
- 2026-10-22T20:33:59Z focused
- 2026-10-22T20:35:30Z scope: fmcode.py (test_runner, run_bounded on_spawn), test_settings.py, fmcli.py help text; other files from other tasks' merges
- 2026-10-22T20:36:52Z done
- 2026-10-22T20:36:54Z committed 4265fed4 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1510 [FEATURE M, done, 3 steps] Brainstorm T-1479 round 2 (cluster 15): fm code config get/set/diff/export/undo on tui.tom — lesson: A share code is a paste from someo…
- T-1572 [FEATURE M, done, 3 steps] fm code app: a settings screen on the shared schema — lesson: A 'run by Claude Code?' check that reads env vars is a check an agent can…
- T-1497 [FEATURE L, dropped, 4 steps] fm code app: a settings screen with live preview
- decision 2026-10-21: fm code brainstorm round 1: 39 build clusters and 5 planned ones are queued (29 new tasks T-1333..T-1361 plus steers on T-1305, T-1308, T-1327..T-13…
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/commands/settings.md, plugin/lib/fmcli.py, plugin/lib/fmcode.py, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py; re-ground the plan against them before editing
## Why not caught
the first capture refused only a static list of keys
## Lessons
- Rebindable navigation needs a floor that can't be rebound, or one keypress locks the user out of the screen that would undo it
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_code_tui.py
- plugin/tests/test_settings.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodetui.py
- plugin/commands/settings.md
- plugin/lib/fmcli.py
- CHANGELOG.md
