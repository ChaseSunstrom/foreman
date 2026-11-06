---
id: T-1510
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T17:36:41Z
updated: 2026-10-22T19:57:27Z
base: 4c8e8b7d0144707873f2de95c9ec142867874507
base_tree: d5681399ffd822ac76be290206dda17144c594c9
plan0_at: 2026-10-22T19:04:13Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, CHANGELOG.md]
verified: strong
---
# Brainstorm T-1479 round 2 (cluster 15): fm code config get/set/diff/export/undo on tui.tom
## Raw request
> Brainstorm T-1479 round 2 (cluster 15): fm code config get/set/diff/export/undo on tui.toml and code.toml through the comment-preserving writer (T-1496); writes only changed keys, flags dead settings, a pasteable share code
## Interpretation
fm settings grows diff, export, import, undo and a pasteable share code over both surfaces (fm code app's tui.toml and the foreman-ui mod's options), flags settings nothing reads (dead), and writes only changed keys. Builds on T-1496's schema. Works from Claude Code (an fm verb or /foreman: command) as well as fm code.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm settings diff shows changed keys against defaults; export/import round-trips through a share code; undo restores the previous value — verify with `cd plugin/tests && python3 -m unittest test_settings.History`
## Non-goals
## Approach (options → choice → why)
Options: copy files around; chosen: a settings history file in Foreman's state with each change (old, new, surface), undo replays it backwards; the share code is base64 of the changed keys only, validated on import.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] diff, export/import, share code
3. [x] history and undo; dead-setting flags
## Resume here
## Docs impact
plugin/commands/settings.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings` → ✗ exit 1 · Ran 29 tests in 2.0s (10 classes, 16 at a time; slowest: Command 2s, History 0s, Sandbox 0s) / FAILED (1 classes) [ran] [tree 3209566ec280] (2026-10-22T19:10:30Z)
- (step 2) `python3 plugin/tests/run.py test_settings` → exit 0 · Ran 29 tests in 2.0s (10 classes, 16 at a time; slowest: Command 2s, History 1s, Sandbox 0s) / OK [ran] [tree 999992477662] (2026-10-22T19:15:06Z)
- (step 3) `python3 plugin/tests/run.py test_settings` → exit 0 · Ran 29 tests in 1.9s (10 classes, 16 at a time; slowest: Command 2s, History 1s, Sandbox 0s) / OK [ran] [tree 999992477662] (2026-10-22T19:15:08Z)
- (step 3) `python3 plugin/tests/run.py test_settings.History` → exit 0 · Ran 7 tests in 0.7s (1 classes, 16 at a time; slowest: History 1s) / OK [ran] [tree 934419692047] (2026-10-22T19:18:32Z)
- (step 3) `python3 plugin/tests/run.py test_settings.History` → ✗ exit 1 · Ran 13 tests in 1.0s (1 classes, 16 at a time; slowest: History 1s) / FAILED (1 classes) [ran] [tree 27b6a3c18bc1] (2026-10-22T19:28:16Z)
- (step 3) `python3 plugin/tests/run.py test_settings.History` → exit 0 · Ran 13 tests in 0.9s (1 classes, 16 at a time; slowest: History 1s) / OK [ran] [tree 114169484917] (2026-10-22T19:29:53Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings.History` → exit 0 · Ran 13 tests in 1.059s / OK [ran] [tree db50e146559e] (2026-10-22T19:55:51Z)
- (step 1) `python3 plugin/tests/run.py test_settings test_code_tui` → exit 0 · Ran 190 tests in 11.6s (31 classes, 16 at a time; slowest: Command 11s, Fuzz 10s, Events 5s) / OK [ran] [tree db50e146559e] (2026-10-22T19:56:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings.History` → exit 0 · Ran 13 tests in 1.088s / OK [ran] [tree 182aaf3fcdf6] (2026-10-22T19:56:15Z)
- (audit intent) `one fm-reviewer pass (adversary-weighted): 2 MEDIUM + 5 LOW fixed test-first in 89e68ad8; the _style_error escaping in fmcodetui went to T-1512, which holds that file, and landed there` → diff, export/import through a share code, undo of the last set or import [tree 182aaf3fcdf6] (2026-10-22T19:56:15Z)
- (audit adversary) `one fm-reviewer pass (adversary-weighted): 2 MEDIUM + 5 LOW fixed test-first in 89e68ad8; the _style_error escaping in fmcodetui went to T-1512, which holds that file, and landed there` → share codes capped at 32 KB and 300 keys, JSON only, known keys and schema-valid values only, one bad key refuses all; control characters escaped in every message; the slash command runs import only for [A-Za-z0-9_-]+ single-quoted; every write through set_app/set_plugin (guard + lock) [tree 182aaf3fcdf6] (2026-10-22T19:56:15Z)
- (audit edge) `one fm-reviewer pass (adversary-weighted): 2 MEDIUM + 5 LOW fixed test-first in 89e68ad8; the _style_error escaping in fmcodetui went to T-1512, which holds that file, and landed there` → unreadable history raises instead of being overwritten; a failed history save warns without failing the set; duplicate keys by case merge; a broken tui.toml doesn't block the repairing set [tree 182aaf3fcdf6] (2026-10-22T19:56:15Z)
- (audit maintainer) `one fm-reviewer pass (adversary-weighted): 2 MEDIUM + 5 LOW fixed test-first in 89e68ad8; the _style_error escaping in fmcodetui went to T-1512, which holds that file, and landed there` → History tests red first; test_settings 36 pass [tree 182aaf3fcdf6] (2026-10-22T19:56:15Z)
## Log
- 2026-10-22T17:36:41Z created
- 2026-10-22T17:46:46Z steer (T-1520): builds on T-1496's fm settings (list/get/set over both surfaces); this adds diff, export, undo, dead-setting flags and a share code, all usable from Claude Code
- 2026-10-22T17:55:43Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings.py', 'CHANGELOG.md']
- 2026-10-22T19:03:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1510.builder.md
- 2026-10-22T19:04:12Z focused
- 2026-10-22T19:41:46Z merged worktree-agent-a27d3f17b848cf393 (5 file(s))
- 2026-10-22T19:41:47Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a27d3f17b848cf393
- 2026-10-22T19:55:48Z focused
- 2026-10-22T19:56:13Z scope: plugin/commands/settings.md and README.md document the new verbs (asked in the brief); other files from other tasks' merges
- 2026-10-22T19:57:24Z done
- 2026-10-22T19:57:27Z committed aecf628d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- T-1572 [FEATURE M, done, 3 steps] fm code app: a settings screen on the shared schema — lesson: A 'run by Claude Code?' check that reads env vars is a check an agent can…
- decision 2026-10-21: T-1300 ships the renderer, motion, gradients, recording and round 1 of the TUI brainstorm; round 2 is queued as T-1305..T-1315 (with T-1301 wide cha…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmsettings.py, plugin/tests/test_settings.py; re-ground the plan against them before editing
## Why not caught
new feature
## Lessons
- A share code is a paste from someone else: validate it whole before writing anything, and escape everything it can put on screen
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_settings.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcli.py
- plugin/commands/settings.md
- README.md
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- mods/foreman-ui/.claude-plugin/plugin.json
- mods/foreman-ui/hooks/kit.ts
- mods/foreman-ui/hooks/register.tsx
- mods/foreman-ui/hooks/state.ts
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmcore.py
- plugin/lib/fmrelease.py
- plugin/lib/fmsmoke.py
- plugin/lib/smoke_web.cjs
- plugin/skills/playbooks/ratchet.json
- plugin/skills/playbooks/references/ui/visual-qa.md
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/test_code_tui.py
- plugin/tests/test_smoke.py
- plugin/tests/test_smoke_profiles.py
- plugin/tests/test_verify_strength.py
