---
id: T-1574
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/commands/settings.md, mods/foreman-ui/hooks, mods/foreman-ui/tests, plugin/tests/test_settings.py, CHANGELOG.md]
depends_on: [T-1496]
source: followup
created: 2026-10-22T18:11:54Z
updated: 2026-10-22T18:39:45Z
base: da3f8e19d24879d3bd9d7c5d5547f239d533d598
base_tree: 7ebc09218f63241b32f45eae28afa20116644bc5
plan0_at: 2026-10-22T18:17:35Z
plan0_scope: [plugin/commands/settings.md, mods/foreman-ui/hooks, mods/foreman-ui/tests, plugin/tests/test_settings.py, CHANGELOG.md]
verified: strong
---
# Claude Code: /foreman:settings and a pane that picks up changed settings
## Raw request
> Claude Code: /foreman:settings and a pane that picks up changed settings
## Interpretation
Split from T-1497, plugin parity: a /foreman:settings command (plugin/commands/settings.md) shows the grouped settings of both surfaces through fm settings list and sets one through fm settings set (the guard decides inside Claude Code); the foreman-ui pane applies a changed motion or palette on its next poll without a restart.
## Assumptions (confidence)
## Acceptance criteria
- [x] the command file exists and runs fm settings list; the pane's state picks up a changed motion/palette on the next poll in the mod's tests — verify with `cd plugin/tests && python3 -m unittest test_settings.PluginSurface`
## Non-goals
## Approach (options → choice → why)
Options: a mod-only settings UI (TSX); chosen: a slash command that runs fm settings (one implementation), plus the mod reading its options on each poll rather than once at start.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] /foreman:settings command
3. [x] pane re-reads options each poll
## Resume here
## Docs impact
plugin/commands/settings.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings.PluginSurface 2>&1 | tail -5` → ✗ exit 1 · Ran 2 tests in 0.001s / FAILED (failures=1, errors=1) [ran] [tree f6bcbc34f9f6] (2026-10-22T18:20:48Z)
- (step 1) `claude plugin test mods/foreman-ui` → ✗ exit 1 · 1 fail / Ran 127 tests across 2 files. [10.60s] [ran] [tree f6bcbc34f9f6] (2026-10-22T18:21:27Z)
- (step 2) `python3 -m unittest -q plugin/tests/test_settings.py -k test_the_command_lists_and_sets_through_fm_settings` → ✗ exit 1 (never ran: the test module test_settings couldn't import) · Ran 1 test in 0.000s / FAILED (errors=1) [ran] [tree bc58973f6319] (2026-10-22T18:21:35Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_settings.py -k test_the_command_lists_and_sets_through_fm_settings` → exit 0 · Ran 1 test in 0.000s / OK [ran] [tree bc58973f6319] (2026-10-22T18:21:39Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 127 tests across 2 files. [11.25s] [ran] [tree 65569988afdc] (2026-10-22T18:23:56Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_settings.py` → exit 0 · Ran 17 tests in 1.875s / OK [ran] [tree 65569988afdc] (2026-10-22T18:23:58Z)
- (step 3) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 129 tests across 2 files. [12.79s] [ran] [tree cc88d0275817] (2026-10-22T18:31:03Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_settings.py` → exit 0 · Ran 17 tests in 1.816s / OK [ran] [tree cc88d0275817] (2026-10-22T18:31:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings.PluginSurface` → exit 0 · Ran 2 tests in 0.000s / OK [ran] [tree f99a0440c9fb] (2026-10-22T18:38:58Z)
- (step 1) `claude plugin test mods/foreman-ui` → exit 0 · 0 fail / Ran 129 tests across 2 files. [12.73s] [ran] [tree f99a0440c9fb] (2026-10-22T18:39:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_settings.PluginSurface` → exit 0 · Ran 2 tests in 0.000s / OK [ran] [tree b8ef008cbd27] (2026-10-22T18:39:18Z)
- (audit intent) `one fm-reviewer pass: MEDIUM test gap and 4 LOW fixed in 97b84434; the env-only in_claude_code bypass went to T-1572 (fmsettings lease) and is fixed there` → /foreman:settings runs fm settings list/get/set; the pane applies a changed motion or palette on the next poll [tree b8ef008cbd27] (2026-10-22T18:39:18Z)
- (audit adversary) `one fm-reviewer pass: MEDIUM test gap and 4 LOW fixed in 97b84434; the env-only in_claude_code bypass went to T-1572 (fmsettings lease) and is fixed there` → the command never writes settings.json itself; guard refusals are shown as fm's message [tree b8ef008cbd27] (2026-10-22T18:39:18Z)
- (audit edge) `one fm-reviewer pass: MEDIUM test gap and 4 LOW fixed in 97b84434; the env-only in_claude_code bypass went to T-1572 (fmsettings lease) and is fixed there` → an engine without $.config keeps polling shells and agents; the first poll applies, not just records; motion off mid-work calls sleep() [tree b8ef008cbd27] (2026-10-22T18:39:18Z)
- (audit maintainer) `one fm-reviewer pass: MEDIUM test gap and 4 LOW fixed in 97b84434; the env-only in_claude_code bypass went to T-1572 (fmsettings lease) and is fixed there` → mod tests 129 pass; mid-work motion test and first-poll test fail when their fixes are reverted [tree b8ef008cbd27] (2026-10-22T18:39:18Z)
## Log
- 2026-10-22T18:11:54Z created
- 2026-10-22T18:17:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1574.builder.md
- 2026-10-22T18:17:35Z focused
- 2026-10-22T18:38:47Z merged worktree-agent-ac8f742c9fdc7c5b4 (4 file(s))
- 2026-10-22T18:38:50Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac8f742c9fdc7c5b4
- 2026-10-22T18:38:50Z focused
- 2026-10-22T18:39:43Z done
- 2026-10-22T18:39:45Z committed 9897d706 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-ab508671842de9f2d: === T-1069 [stale: mods/foreman-ui/hooks/register.tsx, mods/foreman-ui/tests/foreman-ui.test.tsx, mods/foreman-ui/types/index.d.ts…
- T-1497 [FEATURE L, dropped, 4 steps] fm code app: a settings screen with live preview
- T-1572 [FEATURE M, active, 3 steps] fm code app: a settings screen on the shared schema
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
## Why not caught
the first test flipped motion before any work began, so the timer it meant to stop never existed
## Lessons
- A test that changes a setting before work starts can't see a mid-work change: start the work first, then flip the setting
## Plan gaps
- failed first: step 1 failing tests
- failed first: step 2 /foreman:settings command
## Files touched
- plugin/tests/test_settings.py
- mods/foreman-ui/tests/foreman-ui.test.tsx
- plugin/commands/settings.md
- mods/foreman-ui/hooks/register.tsx
- CHANGELOG.md
