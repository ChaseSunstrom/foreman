---
id: T-1657
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/tests/test_settings_power.py, CHANGELOG.md]
depends_on: [T-1656]
source: user
created: 2026-10-22T20:58:46Z
updated: 2026-10-23T03:11:07Z
group: settings surfaces and safety
base: a415c14c8c646334c1dbd1232e349da8e222c873
base_tree: 44d5dec1f0db635d80310e846f371fc234f9aae9
plan0_at: 2026-10-23T02:26:19Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcodetui.py, plugin/tests/test_settings_power.py, CHANGELOG.md]
verified: strong
---
# Settings rules: a layout that switches while verify runs; an extension's settings schema in the settings screen
## Raw request
> Settings rules: a layout that switches while verify runs; an extension's settings schema in the settings screen
## Interpretation
Settings rules: tui.toml [[rule]] entries switch the layout or a panel while an event holds (verify running, a lane failing, a review open) and switch back after; extensions can declare their settings schema so their keys appear and validate in the settings screen.
## Assumptions (confidence)
## Acceptance criteria
- [x] a rule switches layout during a verify event and an extension's keys are listed — verify with `python3 plugin/tests/run.py test_settings_power.Rules`
## Non-goals
## Approach (options → choice → why)
Options: hard-coded layout switches (inflexible); rules evaluated on state changes; scripting hooks (unsafe). Choice: declarative rules over known events: safe, testable, no code in config.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] rule evaluation on state
3. [x] merge extension schemas
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_power.Rules` → ✗ exit 1 · Ran 11 tests in 7.6s (1 classes, 16 at a time; slowest: Rules 1s) / FAILED (1 classes) [ran] [tree 4ac1affd08dd] (2026-10-23T02:32:25Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Rules 2>&1 | grep -B3 -A15 "^FAIL\|^ERROR" | head -40` → ✗ exit 1 · Ran 11 tests in 1.0s (1 classes, 16 at a time; slowest: Rules 1s) / FAILED (1 classes) [ran] [tree 3ac8371ddb4a] (2026-10-23T02:35:56Z)
- (step 2) `python3 plugin/tests/run.py test_settings_power.Rules` → exit 0 · Ran 11 tests in 1.0s (1 classes, 16 at a time; slowest: Rules 1s) / OK [ran] [tree c67e01261a8c] (2026-10-23T02:37:41Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power test_settings test_settings_safety test_code_tui` → exit 0 · Ran 254 tests in 9.9s (40 classes, 16 at a time; slowest: Fuzz 9s, Command 9s, Events 4s) / OK [ran] [tree c67e01261a8c] (2026-10-23T02:37:51Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power.Rules` → ✗ exit 1 · Ran 17 tests in 35.0s (1 classes, 16 at a time; slowest: Rules 33s) / FAILED (1 classes) [ran] [tree 4a06f66d935e] (2026-10-23T02:46:18Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power test_settings test_settings_safety test_code_tui test_docs` → exit 0 · Ran 325 tests in 34.2s (54 classes, 16 at a time; slowest: Fuzz 32s, Command 32s, Fences 19s) / OK [ran] [tree 04c39508a9e6] (2026-10-23T02:51:41Z)
- (step 3) `python3 plugin/tests/run.py test_settings_power test_settings test_code_tui test_docs` → exit 0 · Ran 325 tests in 12.1s (54 classes, 16 at a time; slowest: Fuzz 11s, Command 10s, Fences 10s) / OK [ran] [tree 98bf63cef777] (2026-10-23T03:02:45Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power test_settings test_code_tui` → exit 0 · Ran 260 tests in 9.9s (40 classes, 16 at a time; slowest: Fuzz 9s, Command 9s, Rules 5s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:10:31Z)
- (step 1) `python3 plugin/tests/run.py test_settings_power.Rules` → exit 0 · Ran 17 tests in 4.7s (1 classes, 16 at a time; slowest: Rules 5s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:10:36Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_power.Rules` → exit 0 · Ran 17 tests in 4.6s (1 classes, 16 at a time; slowest: Rules 4s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:10:42Z)
- (audit intent) `fm-reviewer full pass; MEDIUMs fixed test-first: extensions load lazily (list/diff/export/import/undo and ext.* get/set) under a 3 s SIGALRM timebox with stdin closed and BaseException caught (hanging and sys.exit extensions tested); columns-not-a-list can't crash layout checks and _settings_reload is guarded; int ext settings reject floats and bools; LOWs: printable choices, bidi escaped, last declaration wins consistently, profile sets include ext keys, 'rule.' matching, API version 2, a 'rule N' chip, swallowed rule errors said once` → [[rule]] tables switch the fm code layout or a panel while a run event holds and switch back; extensions declare settings that fm settings and the settings screen list, check and set under [ext.NAME] [tree dc2f7fc78782] (2026-10-23T03:10:42Z)
- (audit adversary) `fm-reviewer full pass; MEDIUMs fixed test-first: extensions load lazily (list/diff/export/import/undo and ext.* get/set) under a 3 s SIGALRM timebox with stdin closed and BaseException caught (hanging and sys.exit extensions tested); columns-not-a-list can't crash layout checks and _settings_reload is guarded; int ext settings reject floats and bools; LOWs: printable choices, bidi escaped, last declaration wins consistently, profile sets include ext keys, 'rule.' matching, API version 2, a 'rule N' chip, swallowed rule errors said once` → rules touch only layout and panels, never keys, colours or motion; extension code runs only for commands that need its keys, timeboxed, its output on stderr [tree dc2f7fc78782] (2026-10-23T03:10:42Z)
- (audit edge) `fm-reviewer full pass; MEDIUMs fixed test-first: extensions load lazily (list/diff/export/import/undo and ext.* get/set) under a 3 s SIGALRM timebox with stdin closed and BaseException caught (hanging and sys.exit extensions tested); columns-not-a-list can't crash layout checks and _settings_reload is guarded; int ext settings reject floats and bools; LOWs: printable choices, bidi escaped, last declaration wins consistently, profile sets include ext keys, 'rule.' matching, API version 2, a 'rule N' chip, swallowed rule errors said once` → a bad rule is passed over and said once; a rule layout the app can't draw falls back at startup; up to 16 rules [tree dc2f7fc78782] (2026-10-23T03:10:42Z)
- (audit design) `fm-reviewer full pass; MEDIUMs fixed test-first: extensions load lazily (list/diff/export/import/undo and ext.* get/set) under a 3 s SIGALRM timebox with stdin closed and BaseException caught (hanging and sys.exit extensions tested); columns-not-a-list can't crash layout checks and _settings_reload is guarded; int ext settings reject floats and bools; LOWs: printable choices, bidi escaped, last declaration wins consistently, profile sets include ext keys, 'rule.' matching, API version 2, a 'rule N' chip, swallowed rule errors said once` → a 'rule N' chip names why the layout moved [tree dc2f7fc78782] (2026-10-23T03:10:42Z)
## Log
- 2026-10-22T20:58:46Z created
- 2026-10-22T20:58:47Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_settings_power.py', 'CHANGELOG.md']
- 2026-10-22T20:58:47Z split from T-1544 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:58:48Z set depends_on=['T-1656']
- 2026-10-22T21:30:01Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_settings_power.Rules`
- 2026-10-22T21:30:24Z criterion 1 text: a rule switches layout during a verify event and an extension's keys are listed — verify with python3 plugin/tests/run.py test_settings_power.Rules → a rule switches layout during a verify event and an extension's keys are listed
- 2026-10-23T02:26:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1657.builder.md
- 2026-10-23T02:26:18Z focused
- 2026-10-23T03:05:01Z merged worktree-agent-af4f3f9a96246ac6a (8 file(s))
- 2026-10-23T03:05:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af4f3f9a96246ac6a
- 2026-10-23T03:10:20Z focused
- 2026-10-23T03:10:36Z scope: plugin/commands/settings.md, test_code_tui.py (DEFAULTS has ext), fmnew.py (the extension recorder knows setting), MASTER.md
- 2026-10-23T03:11:07Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- T-1511 [FEATURE M, done, 4 steps] Brainstorm T-1479 round 2 (cluster 16): key, layout and runner editors inside the fm code — lesson: Rebindable navigation needs a floor…
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- likely tests for the scope: plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_settings_power.py; re-ground the plan against them before editing
## Lessons
- A repair command must never run untrusted plugin code by default: load it lazily and timebox it
## Plan gaps
- failed first: step 1 failing test
## Files touched
- plugin/tests/test_settings_power.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmsettings.py
- plugin/commands/settings.md
- plugin/tests/test_code_tui.py
- plugin/lib/fmnew.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/tests/test_control_room.py
