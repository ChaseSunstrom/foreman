---
id: T-1612
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, plugin/tests/test_settings_safety.py, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:54:20Z
updated: 2026-10-23T11:03:27Z
group: settings surfaces and safety
base: 60063b1ccb935e4ae07c9a0c0a91a8bf7b773120
base_tree: 33b072bf672f9cc9bb7b67609c25703a34b0aa22
plan0_at: 2026-10-23T10:59:45Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmcli.py, plugin/tests/test_settings.py, CHANGELOG.md]
verified: strong
---
# Settings headless check: fm settings check renders tui.toml headlessly and warns when the
## Raw request
> Settings headless check: fm settings check renders tui.toml headlessly and warns when the app and a headless render disagree (follow-up of T-1543)
## Interpretation
fm settings check draws the current tui.toml every way Foreman does: the app (render, every layout, wide and narrow: render_error), a headless snapshot (the same frame as SVG, what --snapshot and the docs use) and the plain lines --plain prints, over the sample run. When one fails where another draws, it says which and why and exits 1; all agreeing is one line and exit 0.
## Assumptions (confidence)
## Acceptance criteria
- [x] a config every path draws passes; one that only the headless snapshot or --plain trips is named with its error and exit 1 — verify with `python3 plugin/tests/run.py test_settings test_settings_safety`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test, then check_render and the check action
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_safety.HeadlessCheck` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: HeadlessCheck 0s) / FAILED (1 classes) [ran] [tree a521fec87196] (2026-10-23T11:00:06Z)
- (step 1) `python3 plugin/tests/run.py test_settings_safety test_settings test_cli` → exit 0 · Ran 222 tests in 23.5s (54 classes, 16 at a time; slowest: TaskLifecycle 23s, Serve 9s, AuditPrep 9s) / OK [ran] [tree 30c7f6984bf5] (2026-10-23T11:01:54Z)
- (ac 1) `python3 plugin/tests/run.py test_settings test_settings_safety` → exit 0 · Ran 104 tests in 9.0s (19 classes, 16 at a time; slowest: Serve 9s, Rules 4s, Command 2s) / OK [ran] [tree 30c7f6984bf5] (2026-10-23T11:02:20Z)
- (ac 1) `python3 plugin/tests/run.py test_settings test_settings_safety` → exit 0 · Ran 104 tests in 9.0s (19 classes, 16 at a time; slowest: Serve 9s, Rules 4s, Command 2s) / OK [ran] [tree 30c7f6984bf5] (2026-10-23T11:02:29Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → fm settings check draws tui.toml the three ways Foreman does (app layouts via render_error, the snapshot SVG, --plain lines) and names the way that can't, exit 1, with fm settings bisect as the next step [tree 30c7f6984bf5] (2026-10-23T11:02:29Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → the default config passes; a failure in the snapshot or --plain alone is named with its error; an App that can't be built, or a sample run that raises, is named as the sample run; error text goes through _safe before printing [tree 30c7f6984bf5] (2026-10-23T11:02:29Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → no findings [tree 30c7f6984bf5] (2026-10-23T11:02:29Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → fm settings check draws tui.toml the three ways Foreman does (app layouts via render_error, the snapshot SVG, --plain lines) and names the way that can't, exit 1, with fm settings bisect as the next step [tree 30c7f6984bf5] (2026-10-23T11:03:00Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → the default config passes; a failure in the snapshot or --plain alone is named with its error; an App that can't be built, or a sample run that raises, is named as the sample run; error text goes through _safe before printing [tree 30c7f6984bf5] (2026-10-23T11:03:00Z)
- (audit self) `self review in the main thread (subagents paused by the usage budget): re-read check_render against the gallery's own sample-run code (same App construction, no side effects) and the cmd branch; one finding fixed test-first (an App that fails to build raised a traceback instead of a named failure)` → no findings [tree 30c7f6984bf5] (2026-10-23T11:03:00Z)
## Log
- 2026-10-22T20:54:20Z created
- 2026-10-23T10:38:12Z set tier=S, scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings.py', 'CHANGELOG.md']
- 2026-10-23T10:59:44Z focused
- 2026-10-23T11:00:40Z scope: the test lives in plugin/tests/test_settings_safety.py beside render_error's own tests
- 2026-10-23T11:02:10Z criterion 1 verify: `python3 plugin/tests/run.py test_settings` → `python3 plugin/tests/run.py test_settings test_settings_safety`
- 2026-10-23T11:02:59Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_settings.py', 'plugin/tests/test_settings_safety.py', 'CHANGELOG.md']
- 2026-10-23T11:03:25Z done
- 2026-10-23T11:03:27Z committed 9059fe26 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1496-review: Verdict:** approve with nits. I found no TOML injection, no path traversal and no settings.json write that skips the guard. I had no shell, so I …
- T-1305 [FEATURE S, done, 1 steps] Fm code tui close receipt: on close a receipt card (task, checks, files, tokens, time, com
- research T-1283-review: Verdict: changes needed.** I read the diff and the surrounding `fmcode.py`. I couldn't run anything, so every finding comes from reading the code…
- decision 2026-10-21: T-1300 ships the renderer, motion, gradients, recording and round 1 of the TUI brainstorm; round 2 is queued as T-1305..T-1315 (with T-1301 wide cha…
- the similar finished task took 1 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmsettings.py, plugin/tests/test_settings.py; re-ground the plan against them before editing
## Lessons
- A check that builds the thing it checks must build it inside its own try: the construction is the likeliest failure
## Plan gaps
- failed first: step 1 failing test, then check_render and the check action
## Files touched
- plugin/tests/test_settings_safety.py
- CHANGELOG.md
- plugin/lib/fmcli.py
- plugin/lib/fmsettings.py
