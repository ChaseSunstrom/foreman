---
id: T-2396
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_prove.py, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-10-31T14:03:47Z
updated: 2026-11-01T23:50:20Z
group: Mission 7 proof inbox
base: c9705e5cc2154e332f6a4b9948bb0b952883edc4
base_tree: 728f8b7d6ad6755c1a32293a797ae8d65be39d1b
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-11-01T23:36:42Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_prove.py, CHANGELOG.md]
verified: strong
---
# ui-unshot counts terminal UIs (TUI screens, statuslines, the pane's hooks) by ui_paths
## Raw request
> FEATURE: ui-unshot also counts terminal UIs (fm code's TUI, the statusline, the pane) by the project's declared UI paths, not only web file extensions (Mission 7 inbox, tier 2)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove lists a done task that changed a TUI screen, a statusline or a mod's hooks with no run rendering it as tui-unshot; a web file still needs fm shot/smoke/stories/flow (ui-unshot); a terminal file is cleared by a green run naming its stem, or claude plugin test for a mod's hooks; a no-op that only names it (echo) clears nothing — verify with `python3 plugin/tests/run.py test_proof test_site`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a done task with fmcodetui.py changed and no UI run is flagged ui-unshot; with evidence 'python3 plugin/lib/fmcodetui.py --demo' it isn't; a .css file still needs fm shot
2. [x] fmcore._need_ui: ui_paths(x['files']) instead of _UI_FILE; terminal ones (not a web extension) clear on a run naming the file's stem or claude plugin test, with a hint naming the terminal-ui playbook
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_proof` → ✗ exit 1 · Ran 39 tests in 28.7s (8 classes, 16 at a time; slowest: Proof 28s, Stop 2s, Meaning 2s) / FAILED (1 classes: test_proof.Proof) [ran] [tree 1a3fc77f8bd8] (2026-11-01T23:37:40Z)
- (step 1) `python3 plugin/tests/run.py test_proof.Proof.test_a_terminal_ui_needs_a_run_that_renders_it` → exit 0 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Proof 1s) / OK [ran] [tree c62c9f933ab3] (2026-11-01T23:42:27Z)
- (step 2) `python3 plugin/tests/run.py test_proof test_site` → exit 0 · Ran 75 tests in 18.4s (28 classes, 16 at a time; slowest: Proof 18s, Header 5s, Stop 2s) / OK [ran] [tree c62c9f933ab3] (2026-11-01T23:42:46Z)
- (ac 1) `python3 plugin/tests/run.py test_proof test_site` → exit 0 · Ran 75 tests in 18.4s (28 classes, 16 at a time; slowest: Proof 18s, Header 5s, Stop 2s) / OK [ran] [tree 8eb16b4d8cfc] (2026-11-01T23:49:36Z)
- (audit adversary) `self-review: tui-unshot reads only terminal rows of ui_paths (TUI screens, statuslines, mods/*/hooks), skips tests and fixtures; a green run counts only when one of its && steps names the file's stem (or claude plugin test for a mod's hooks) and doesn't start with a no-op (echo, printf, true, :, test, [, touch, mkdir, cat); web files keep ui-unshot and its fm shot clear` → 'echo fmcodetui' and 'cat fmcodetui.py' name the file but clear nothing; a pipe can't hide behind the stem either way since the green status is fm's own run [tree 8eb16b4d8cfc] (2026-11-01T23:49:36Z)
- (audit edge) `self-review: tui-unshot reads only terminal rows of ui_paths (TUI screens, statuslines, mods/*/hooks), skips tests and fixtures; a green run counts only when one of its && steps names the file's stem (or claude plugin test for a mod's hooks) and doesn't start with a no-op (echo, printf, true, :, test, [, touch, mkdir, cat); web files keep ui-unshot and its fm shot clear` → a pane hook needs claude plugin test; a TUI cleared by a run naming it; a web file with a terminal-looking run still needs fm shot [tree 8eb16b4d8cfc] (2026-11-01T23:49:36Z)
- (audit self) `self-review: tui-unshot reads only terminal rows of ui_paths (TUI screens, statuslines, mods/*/hooks), skips tests and fixtures; a green run counts only when one of its && steps names the file's stem (or claude plugin test for a mod's hooks) and doesn't start with a no-op (echo, printf, true, :, test, [, touch, mkdir, cat); web files keep ui-unshot and its fm shot clear` → no findings [tree 8eb16b4d8cfc] (2026-11-01T23:49:36Z)
## Log
- 2026-10-31T14:03:47Z created
- 2026-11-01T23:04:34Z planned from capture
- 2026-11-01T23:36:41Z focused
- 2026-11-01T23:36:42Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-11-01T23:42:25Z criterion 1 verify: `python3 plugin/tests/run.py test_prove` → `python3 plugin/tests/run.py test_proof test_site`
- 2026-11-01T23:42:25Z criterion 1 text: fm prove's ui-unshot flags a done task that changed fmcodetui.py, a statusline or mods/*/hooks/*.ts with no proof; a web file still needs fm shot/smoke/stories/flow; a terminal file is cleared by a recorded run naming it (its stem) or claude plugin test for the pane → fm prove lists a done task that changed a TUI screen, a statusline or a mod's hooks with no run rendering it as tui-unshot; a web file still needs fm shot/smoke/stories/flow (ui-unshot); a terminal file is cleared by a green run naming its stem, or claude plugin test for a mod's hooks; a no-op that only names it (echo) clears nothing
- 2026-11-01T23:42:46Z scope: a separate tui-unshot kind (a kind's clear is one static regex; a terminal proof names the file); test_proof (not test_prove) holds the tests; site/pages.py names the new kind (its test reads every kind from the code)
- 2026-11-01T23:43:01Z scope: MASTER.md entry
- 2026-11-01T23:50:17Z done
- 2026-11-01T23:50:20Z committed d6c7f9eb (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1501-review: Verdict:** approve with nits. I found no HIGH issues and did not run the tests. I traced each `AUDIT_LENSES` consumer by reading the code. [stale…
- T-0084 [FEATURE L, done, 7 steps] Foreman UI mod: docked pane, prompt band, toasts, /fm, one-press approve/next/drive/inbox — lesson: Mods: functions that take $ must be…
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- decision 2026-10-31: Mission 6 (tools, #5) approach A: wire the parts Foreman has into one loop on the active task (T-2270's hook notices the miss; fm which, fm lib and …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-31): CHANGELOG.md, plugin/lib/fmcore.py, plugin/tests/test_prove.py; re-ground the plan against them before editing
## Lessons
- When a proof's tool can't reach a surface (fm shot and a terminal), require a run that names the thing and isn't a no-op, rather than leaving the surface uncounted
## Plan gaps
- failed first: step 1 red test: a done task with fmcodetui.py changed and no UI run is flagged ui-unshot; with evidence '…
## Files touched
- plugin/tests/test_proof.py
- plugin/lib/fmcore.py
- site/pages.py
- MASTER.md
- CHANGELOG.md
