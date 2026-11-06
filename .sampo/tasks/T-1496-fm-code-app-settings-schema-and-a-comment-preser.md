---
id: T-1496
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, plugin/tests/test_code_tui.py, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks, mods/foreman-ui/tests, CHANGELOG.md, README.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:12Z
updated: 2026-10-22T18:11:18Z
base: 50de32040502fe538a8cd4c49419caa87c433fe4
base_tree: c90b26a3afb336afb5bdcf6131df1b6e02a0cd83
plan0_at: 2026-10-22T17:42:00Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, plugin/tests/test_code_tui.py, mods/foreman-ui/.claude-plugin/plugin.json, mods/foreman-ui/hooks, mods/foreman-ui/tests, CHANGELOG.md, README.md]
verified: strong
---
# fm code app: settings schema and a comment-preserving tui.toml writer
## Raw request
> fm code app: settings schema and a comment-preserving tui.toml writer
## Interpretation
Brainstorm T-1479 cluster 5: config in the TUI needs a model first. One schema list of every setting (key, type, default, choices or range, group, one-line help, takes effect: now or next run) derived from DEFAULTS, and a writer that changes one key in tui.toml in place, keeping comments, order and unrelated keys, creating the table when missing; a change is validated by load_config on the new text and a dry render before it is written (atomic replace).
## Assumptions (confidence)
## Acceptance criteria
- [x] every DEFAULTS key has a schema entry, and a set keeps comments and other keys byte-identical — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Settings`
- [x] a value load_config rejects or a render that raises is refused and the file is unchanged — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Settings.test_a_bad_value_leaves_the_file`
- [x] one schema in plugin/lib covers the app's tui.toml and the foreman-ui mod's userConfig; overlapping settings (motion, palette) share one name and value set, old values still accepted; fm settings list shows both surfaces with value, default and where it is stored — verify with `cd plugin/tests && python3 -m unittest test_settings`
## Non-goals
## Approach (options → choice → why)
Options: rewrite the whole file from the config (loses comments); a TOML library (not stdlib for writing); chosen: a line-based editor for the flat tables tui.toml uses (find [table], find key = …, replace the value, else insert), values written with the same quoting print_config uses.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] SETTINGS schema from DEFAULTS
3. [x] set_setting: in-place TOML edit, validate, dry render, atomic write
## Resume here
## Docs impact
CHANGELOG.md line; MASTER.md entry
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest test_code_tui.Settings test_settings` → ✗ exit 1 · Ran 6 tests in 0.003s / FAILED (errors=6) [ran] [tree c6d18db27bc8] (2026-10-22T17:46:24Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_code_tui.Settings.test_every_default_has_a_schema_entry test_settings.Schema` → exit 0 · Ran 4 tests in 0.003s / OK [ran] [tree dbde8a3e3b7a] (2026-10-22T17:51:13Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Settings test_settings` → exit 0 · Ran 15 tests in 1.008s / OK [ran] [tree dbde8a3e3b7a] (2026-10-22T17:51:14Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Settings test_settings` → exit 0 · Ran 16 tests in 2.655s / OK [ran] [tree 61740848060d] (2026-10-22T17:55:53Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Settings.test_a_bad_value_leaves_the_file` → exit 0 · Ran 1 test in 0.030s / OK [ran] [tree 61740848060d] (2026-10-22T17:55:57Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_code_tui.Settings test_settings` → exit 0 · Ran 25 tests in 1.653s / OK [ran] [tree d2db2cd399bd] (2026-10-22T18:07:42Z)
- `cd plugin/tests && python3 -m unittest test_settings test_code_tui.Settings` → ✗ exit 1 · Ran 11 tests in 0.035s / FAILED (errors=11) (start tree + this task's tests) [ran] [tree 75239ae9b764] (2026-10-22T18:09:40Z)
- `cd plugin/tests && python3 -m unittest test_settings test_code_tui.Settings` → exit 0 · Ran 25 tests in 1.825s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:40Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Settings` → exit 0 · Ran 10 tests in 0.045s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:41Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Settings.test_a_bad_value_leaves_the_file` → exit 0 · Ran 1 test in 0.022s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:41Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_settings` → exit 0 · Ran 15 tests in 1.769s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:43Z)
- (step 1) `cd plugin/tests && python3 -m unittest test_settings test_code_tui.Settings` → exit 0 · Ran 25 tests in 1.772s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:46Z)
- (step 2) `cd plugin/tests && python3 -m unittest test_settings test_code_tui.Settings` → exit 0 · Ran 25 tests in 1.761s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:48Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_settings test_code_tui.Settings` → exit 0 · Ran 25 tests in 1.816s / OK [ran] [tree 75239ae9b764] (2026-10-22T18:09:50Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Settings` → exit 0 · Ran 10 tests in 0.049s / OK [ran] [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.Settings.test_a_bad_value_leaves_the_file` → exit 0 · Ran 1 test in 0.023s / OK [ran] [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (ac 3) `cd plugin/tests && python3 -m unittest test_settings` → exit 0 · Ran 15 tests in 1.706s / OK [ran] [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (audit adversary) `builder (high) test-first; red proved (11 errors on the start tree); one fm-reviewer pass found no TOML injection, traversal or guard skip, and 2 medium + 6 low issues, all fixed test-first by the builder (guard consulted for both files inside Claude Code, lane confinement passed, config dir outside home refused, unhashable values no longer crash, file locks, per-line endings, surrogates, user key bindings listed, load errors shown); test_settings, test_code_tui and the mod's tests green` → values are re-serialised from the parsed value, never the raw argument; keys are schema keys or parsed key names; inside Claude Code the guard decides both writes; an env -u CLAUDECODE bypass captured as T-1570 [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (audit edge) `builder (high) test-first; red proved (11 errors on the start tree); one fm-reviewer pass found no TOML injection, traversal or guard skip, and 2 medium + 6 low issues, all fixed test-first by the builder (guard consulted for both files inside Claude Code, lane confinement passed, config dir outside home refused, unhashable values no longer crash, file locks, per-line endings, surrogates, user key bindings listed, load errors shown); test_settings, test_code_tui and the mod's tests green` → a broken tui.toml lists with its errors and can be repaired by fm settings set; concurrent fm writers serialise on a lock (Claude Code's own writes aren't covered) [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (audit intent) `builder (high) test-first; red proved (11 errors on the start tree); one fm-reviewer pass found no TOML injection, traversal or guard skip, and 2 medium + 6 low issues, all fixed test-first by the builder (guard consulted for both files inside Claude Code, lane confinement passed, config dir outside home refused, unhashable values no longer crash, file locks, per-line endings, surrogates, user key bindings listed, load errors shown); test_settings, test_code_tui and the mod's tests green` → one schema and vocabulary for fm code app and the Claude Code plugin's pane, as the user asked (plugin parity) [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (audit maintainer) `builder (high) test-first; red proved (11 errors on the start tree); one fm-reviewer pass found no TOML injection, traversal or guard skip, and 2 medium + 6 low issues, all fixed test-first by the builder (guard consulted for both files inside Claude Code, lane confinement passed, config dir outside home refused, unhashable values no longer crash, file locks, per-line endings, surrogates, user key bindings listed, load errors shown); test_settings, test_code_tui and the mod's tests green` → fmsettings.py owns the schema; fmcodetui reads it; T-1497 builds the screen and /foreman:settings on it [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
- (audit operator) `builder (high) test-first; red proved (11 errors on the start tree); one fm-reviewer pass found no TOML injection, traversal or guard skip, and 2 medium + 6 low issues, all fixed test-first by the builder (guard consulted for both files inside Claude Code, lane confinement passed, config dir outside home refused, unhashable values no longer crash, file locks, per-line endings, surrogates, user key bindings listed, load errors shown); test_settings, test_code_tui and the mod's tests green` → CHANGELOG and MASTER.md describe fm settings [tree ec8cd1dfbc81] (2026-10-22T18:10:04Z)
## Log
- 2026-10-22T17:36:12Z created
- 2026-10-22T17:41:38Z steer (user, T-1520): everything must work in the Claude Code plugin too, not only fm code. The schema covers both surfaces: the fm code app's tui.toml and the foreman-ui mod's userConfig (mods/foreman-ui/.claude-plugin/plugin.json: freshAt, freshTokens, mascot, motion, palette, chat…), with one name and one value set where they overlap (motion is full/reduced/off in the app but full/calm/off in the mod: settle one vocabulary, accepting the old word)
- 2026-10-22T17:41:39Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings.py', 'plugin/tests/test_code_tui.py', 'mods/foreman-ui/.claude-plugin/plugin.json', 'mods/foreman-ui/hooks', 'mods/foreman-ui/tests', 'CHANGELOG.md', 'README.md']
- 2026-10-22T17:41:46Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1496.builder.md
- 2026-10-22T17:41:59Z focused
- 2026-10-22T17:54:50Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings.py', 'plugin/tests/test_code_tui.py', 'mods/foreman-ui/.claude-plugin/plugin.json', 'mods/foreman-ui/hooks', 'mods/foreman-ui/tests', 'CHANGELOG.md', 'README.md', 'MASTER.md']
- 2026-10-22T17:54:51Z scope: MASTER.md added for the fmsettings system-map entry (docs gate)
- 2026-10-22T18:09:32Z merged worktree-agent-a7430adfe5a0a3d43 (11 file(s))
- 2026-10-22T18:09:32Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a7430adfe5a0a3d43
- 2026-10-22T18:09:32Z focused
- 2026-10-22T18:11:16Z done
- 2026-10-22T18:11:18Z committed 181fc4d0 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1497 [FEATURE L, planned, 4 steps] fm code app: a settings screen with live preview
- research T-1328-review: Verdict: changes needed.** One crash, one silent fallback that sends code to a cloud CLI, one unguarded command-bearing config file, and a gap ag…
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
new capability
## Lessons
- Decide 'is Claude running this?' once (CLAUDECODE) and route protected writes through the guard there; the user's own terminal writes directly.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_code_tui.py
- plugin/tests/test_settings.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcli.py
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- MASTER.md
- README.md
- CHANGELOG.md
