---
id: T-1572
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py, README.md, CHANGELOG.md]
depends_on: [T-1496]
source: followup
created: 2026-10-22T18:11:53Z
updated: 2026-10-22T18:42:01Z
base: 9897d70607d1afe6235b9b59f7b39a2a009d8e59
base_tree: b8ef008cbd276b21dfce4ad223a954b2033dd0d4
plan0_at: 2026-10-22T18:12:14Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: a settings screen on the shared schema
## Raw request
> fm code app: a settings screen on the shared schema
## Interpretation
Brainstorm T-1479 cluster 6, split from T-1497: change themes, layout, keys, motion and models from inside fm code app: an overlay (one key opens it) listing fmsettings' schema by group, with search, a modified-only view, the current value and default, a takes-effect badge (now / next run), and a :set key value line; writes go through fm settings' comment-preserving writer.
## Assumptions (confidence)
## Acceptance criteria
- [x] the overlay lists every setting by group, search narrows it, modified-only shows changed keys, each row shows value, default and badge — verify with `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen`
- [x] :set key value writes one key through fm settings and the screen shows it — verify with `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen.test_set_line`
## Non-goals
## Approach (options → choice → why)
Options: a separate settings app (two UIs); chosen: one more view in fmcodetui's view stack, reusing _overlay and _list_view, driven by fmsettings.SCHEMA; :set parses like fm settings set.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] overlay: groups, search, modified-only, badge
3. [x] :set line
## Resume here
## Docs impact
README.md
## Verification evidence
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen 2>&1 | tail -5` → ✗ exit 1 · Ran 5 tests in 0.089s / FAILED (failures=5) [ran] [tree 1eb55a0a46e9] (2026-10-22T18:16:00Z)
- (step 1) `python3 -m unittest discover -s plugin/tests -p test_code_tui.py -k SettingsScreen` → ✗ exit 1 · Ran 5 tests in 0.021s / FAILED (failures=5) [ran] [tree 1eb55a0a46e9] (2026-10-22T18:16:02Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen 2>&1 | tail -30` → exit 0 · Ran 5 tests in 0.080s / OK [ran] [tree 004bbae9a435] (2026-10-22T18:18:42Z)
- (step 2) `python3 -m unittest discover -s plugin/tests -p test_code_tui.py -k SettingsScreen` → exit 0 · Ran 5 tests in 0.051s / OK [ran] [tree d63957006195] (2026-10-22T18:20:12Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_code_tui.py -k test_set_line` → exit 0 · Ran 1 test in 0.027s / OK [ran] [tree d63957006195] (2026-10-22T18:20:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen 2>&1 | tail -3` → exit 0 · Ran 5 tests in 0.067s / OK [ran] [tree bee923353611] (2026-10-22T18:20:41Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^FAILED|Error:" | head -30` → ✗ exit 1 · Ran 12 tests in 0.007s / FAILED (errors=12) [ran] [tree 761bce49d1f3] (2026-10-22T18:32:00Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen 2>&1 | grep -E "^(FAIL|ERROR):|^Ran|^FAILED|^OK|Error|assert" | head -30` → exit 0 · Ran 12 tests in 0.154s / OK [ran] [tree 75ef3f30e199] (2026-10-22T18:33:14Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_code_tui.py -k SettingsScreen` → exit 0 · Ran 12 tests in 0.118s / OK [ran] [tree a47f282fbf7b] (2026-10-22T18:35:51Z)
- (step 3) `python3 -m unittest discover -s plugin/tests -p test_settings.py` → exit 0 · Ran 16 tests in 2.833s / OK [ran] [tree a47f282fbf7b] (2026-10-22T18:35:55Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen` → exit 0 · Ran 12 tests in 0.111s / OK [ran] [tree 8fcc56f0864d] (2026-10-22T18:40:52Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen.test_set_line` → exit 0 · Ran 1 test in 0.040s / OK [ran] [tree 8fcc56f0864d] (2026-10-22T18:40:59Z)
- (step 1) `python3 plugin/tests/run.py test_settings test_code_tui` → exit 0 · Ran 156 tests in 12.3s (27 classes, 16 at a time; slowest: Command 12s, Fuzz 11s, Events 5s) / OK [ran] [tree 8fcc56f0864d] (2026-10-22T18:41:12Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen` → exit 0 · Ran 12 tests in 0.123s / OK [ran] [tree b755e46e23ad] (2026-10-22T18:41:22Z)
- (ac 2) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsScreen.test_set_line` → exit 0 · Ran 1 test in 0.045s / OK [ran] [tree b755e46e23ad] (2026-10-22T18:41:22Z)
- (audit intent) `one fm-reviewer pass (adversary, edge, maintainer, intent, operator): 2 MEDIUM + 6 LOW fixed in b334926f, plus T-1574 review's env-only in_claude_code bypass (fails closed now) and the 'next session' wording` → settings overlay with groups, search, changed-only, badges and a :set line writing through fm settings [tree b755e46e23ad] (2026-10-22T18:41:22Z)
- (audit adversary) `one fm-reviewer pass (adversary, edge, maintainer, intent, operator): 2 MEDIUM + 6 LOW fixed in b334926f, plus T-1574 review's env-only in_claude_code bypass (fails closed now) and the 'next session' wording` → blank CLAUDECODE with no TTY now goes through the guard; a value already wrong in tui.toml is refused, not written; pasted ESC/DEL dropped [tree b755e46e23ad] (2026-10-22T18:41:22Z)
- (audit edge) `one fm-reviewer pass (adversary, edge, maintainer, intent, operator): 2 MEDIUM + 6 LOW fixed in b334926f, plus T-1574 review's env-only in_claude_code bypass (fails closed now) and the 'next session' wording` → ≤13-row terminals keep one list row; RecursionError on deep [ caught; home cursor kept on return [tree b755e46e23ad] (2026-10-22T18:41:22Z)
- (audit maintainer) `one fm-reviewer pass (adversary, edge, maintainer, intent, operator): 2 MEDIUM + 6 LOW fixed in b334926f, plus T-1574 review's env-only in_claude_code bypass (fails closed now) and the 'next session' wording` → width test asserts column alignment at 60/80/140; tests for empty search, guarded :set, Esc back [tree b755e46e23ad] (2026-10-22T18:41:22Z)
## Log
- 2026-10-22T18:11:53Z created
- 2026-10-22T18:12:03Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1572.builder.md
- 2026-10-22T18:12:14Z focused
- 2026-10-22T18:40:04Z merged worktree-agent-a438644857f730466 (5 file(s))
- 2026-10-22T18:40:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a438644857f730466
- 2026-10-22T18:40:43Z focused
- 2026-10-22T18:41:12Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_settings.py', 'README.md', 'CHANGELOG.md']
- 2026-10-22T18:41:13Z scope: README lists the , key (review item 9); test_settings.py term() helper for the fail-closed guard check (review item 10, from T-1574's review)
- 2026-10-22T18:41:59Z done
- 2026-10-22T18:42:01Z committed f210f73f (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1497 [FEATURE L, dropped, 4 steps] fm code app: a settings screen with live preview
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_settings.py
## Why not caught
T-1496's review looked at the guard call, not at how the caller decides to skip it
## Lessons
- A 'run by Claude Code?' check that reads env vars is a check an agent can unset: fail closed on a positive interactive signal (a TTY) instead
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcodetui.py
- ANDON.md
- plugin/tests/test_settings.py
- README.md
- CHANGELOG.md
