---
id: T-1573
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py, README.md, CHANGELOG.md]
depends_on: [T-1572]
source: followup
created: 2026-10-22T18:11:53Z
updated: 2026-10-22T19:40:25Z
base: f81c9c3c9a78b75eb47ae74ef8834e707fa96d68
base_tree: b93341f3263b6f6b1093608ded8d0be1522621a1
plan0_at: 2026-10-22T18:43:14Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py, CHANGELOG.md]
verified: strong
---
# fm code app: live preview and revert-in-10-seconds for settings
## Raw request
> fm code app: live preview and revert-in-10-seconds for settings
## Interpretation
Split from T-1497: a theme or motion change in the settings screen repaints the screen behind it at once (preview without writing), and a written change not kept within 10 s (any key keeps it) reverts in the file and on screen.
## Assumptions (confidence)
## Acceptance criteria
- [x] a theme change repaints behind the overlay before it is kept; an unkept change reverts after 10 s in the file and on screen; any key keeps it — verify with `cd plugin/tests && python3 -m unittest test_code_tui.SettingsPreview`
## Non-goals
## Approach (options → choice → why)
Options: write then undo; chosen: apply the candidate config to the app's cfg only, write on keep, and on timeout restore the old cfg and leave the file as it was.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] preview on the live cfg
3. [x] keep or revert timer
## Resume here
## Docs impact
README.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_code_tui.SettingsPreview` → ✗ exit 1 · Ran 9 tests in 0.3s (1 classes, 16 at a time; slowest: SettingsPreview 0s) / FAILED (1 classes) [ran] [tree 37f064f84355] (2026-10-22T18:46:34Z)
- (step 2) `python3 plugin/tests/run.py -k test_code_tui.SettingsPreview` → exit 0 · Ran 9 tests in 0.7s (1 classes, 16 at a time; slowest: SettingsPreview 0s) / OK [ran] [tree 66dcb5620dae] (2026-10-22T18:49:18Z)
- (step 3) `python3 plugin/tests/run.py -p test_code_tui.py` → exit 0 · Ran 143 tests in 21.2s (20 classes, 16 at a time; slowest: Command 21s, Fuzz 16s, Events 9s) / OK [ran] [tree 66dcb5620dae] (2026-10-22T18:49:40Z)
- (step 3) `python3 plugin/tests/run.py -k test_code_tui.SettingsPreview -k test_settings.PreviewApp` → exit 0 · Ran 11 tests in 0.4s (2 classes, 16 at a time; slowest: SettingsPreview 0s, PreviewApp 0s) / OK [ran] [tree 9966b3dff6d3] (2026-10-22T18:58:39Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsPreview` → exit 0 · Ran 10 tests in 0.073s / OK [ran] [tree d705740d082d] (2026-10-22T19:36:06Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_settings` → exit 0 · Ran 167 tests in 8.5s (29 classes, 16 at a time; slowest: Command 8s, Fuzz 8s, Events 4s) / OK [ran] [tree d705740d082d] (2026-10-22T19:36:15Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.SettingsPreview` → exit 0 · Ran 10 tests in 0.095s / OK [ran] [tree d5681399ffd8] (2026-10-22T19:36:16Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → theme, palette and motion preview live; any key keeps; 10 s without one reverts screen and file [tree d5681399ffd8] (2026-10-22T19:36:16Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → preview runs the same checks and guard as the write, so a kept value equals the previewed one; nothing is written before a keep [tree d5681399ffd8] (2026-10-22T19:36:16Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → monotonic deadline doesn't count suspend (fails safe: nothing written); a refused keep restores the old look with the guard's message [tree d5681399ffd8] (2026-10-22T19:36:16Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → SettingsPreview and PreviewApp tests red first; test_code_tui and test_settings pass [tree d5681399ffd8] (2026-10-22T19:36:16Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → theme, palette and motion preview live; any key keeps; 10 s without one reverts screen and file [tree d5681399ffd8] (2026-10-22T19:38:18Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → preview runs the same checks and guard as the write, so a kept value equals the previewed one; nothing is written before a keep [tree d5681399ffd8] (2026-10-22T19:38:18Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → monotonic deadline doesn't count suspend (fails safe: nothing written); a refused keep restores the old look with the guard's message [tree d5681399ffd8] (2026-10-22T19:38:18Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 4 LOW fixed in 06d2a49e (guard at preview, one return shape via _plan_app, keep-equals-preview test, preview_app refuses what set_app refuses)` → SettingsPreview and PreviewApp tests red first; test_code_tui and test_settings pass [tree d5681399ffd8] (2026-10-22T19:38:18Z)
## Log
- 2026-10-22T18:11:53Z created
- 2026-10-22T18:42:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1573.builder.md
- 2026-10-22T18:43:13Z focused
- 2026-10-22T18:46:55Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-22T18:46:55Z scope: + plugin/lib/fmsettings.py — preview_app runs set_app's checks without writing, so the preview is exactly what keep writes (main thread named fmsettings as the writer)
- 2026-10-22T18:56:46Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmsettings.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/test_settings.py', 'README.md', 'CHANGELOG.md']
- 2026-10-22T18:56:46Z steer: review nits — guard at preview, _plan_app split, keep-test cfg equality, preview_app refusal test in test_settings.py, monotonic note, README line; scope + test_settings.py, README.md
- 2026-10-22T19:03:16Z merged worktree-agent-a0b3f70e7e9bef367 (5 file(s))
- 2026-10-22T19:03:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0b3f70e7e9bef367
- 2026-10-22T19:35:57Z focused
- 2026-10-22T19:38:17Z scope: the other files changed through other tasks' merges and commits (T-1501, T-1505, T-1508, T-1514, T-1585) after T-1573's base; T-1573's own lane touched only its scope
- 2026-10-22T19:40:22Z done
- 2026-10-22T19:40:25Z committed 4c8e8b7d (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1497 [FEATURE L, dropped, 4 steps] fm code app: a settings screen with live preview
- T-1572 [FEATURE M, done, 3 steps] fm code app: a settings screen on the shared schema — lesson: A 'run by Claude Code?' check that reads env vars is a check an agent can…
- research T-1300-review: Verdict: changes needed.** I read the code but couldn't run anything, because this session had no Bash tool. Nothing below was executed, and the …
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- the similar finished task took 3 steps
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, README.md, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/tests/test_code_tui.py, plugin/tests/test_settings.py; re-ground the plan against them before editing
## Why not caught
the first preview_app copied set_app's checks minus the guard
## Lessons
- A preview path that skips the write's checks shows looks it can't keep: share one planning function between preview and write
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_code_tui.py
- plugin/lib/fmsettings.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_settings.py
- README.md
- CHANGELOG.md
- MASTER.md
- plugin/README.md
- plugin/agents/fm-reviewer.md
- plugin/lib/fmauditrun.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmdesign.py
- plugin/lib/fmguard.py
- plugin/lib/fmhooks.py
- plugin/lib/fmlanes.py
- plugin/lib/fmplaybooks.py
- plugin/skills/brainstorm/SKILL.md
- plugin/skills/directions/SKILL.md
- plugin/skills/directions/references/cards.md
- plugin/skills/doctor/SKILL.md
- plugin/skills/improve/SKILL.md
- plugin/skills/intake/SKILL.md
- plugin/skills/intake/references/audit.md
- plugin/skills/library/SKILL.md
- plugin/skills/next/SKILL.md
- plugin/skills/playbooks/ratchet.json
- plugin/skills/playbooks/references/clean/code-simplifier.md
- plugin/skills/playbooks/references/clean/repo-sweep.md
- plugin/skills/playbooks/references/context/context-budget.md
