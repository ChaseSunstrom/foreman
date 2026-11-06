---
id: T-2758
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmshot.py, plugin/lib/sampo/shot.py, plugin/tests/test_fmshot.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: discovered
created: 2026-11-03T03:25:11Z
updated: 2026-11-03T14:56:11Z
builder_model: sonnet
base: 9628d9939e2e68b6da799c4d6c0608efb630d5b7
base_tree: be5b5deb8a8127bbd0dc1b2c54f634131e1ebf3d
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-03T04:17:11Z
plan0_scope: [plugin/lib/fmshot.py, plugin/lib/sampo/shot.py, plugin/tests/test_fmshot.py, MASTER.md, CHANGELOG.md]
lane_stop: merged 2026-11-03T04:27:13Z
verified: strong
unproven: [docs, meaning]
---
# fm shot takes --width W[,W…] and --scheme light|dark|both: one run shoots the page matrix, each into PAGE-W-SCHEME/ (T-2758)
## Raw request
> FEATURE: fm shot takes --width (several, e.g. 1280,768,320) and --scheme light|dark|both and --reduce-motion, so a page's screenshot matrix is one command; T-2753's builder and its review each hand-wrote a chrome-headless loop for it
## Interpretation
Reading 1 (chosen): fm shot gains two flags so a page's screenshot matrix (widths × colour schemes) is one command through one browser, each view in its own folder; the existing defaults and --profile stay as they are. Reading 2: a --matrix preset (desktop, tablet, phone × both schemes); rejected for now: explicit widths say the same and a preset can be added when two callers want the same list.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm shot --width 1280,320 --scheme both PAGE shoots four views through one browser into page-1280-light/, page-1280-dark/, page-320-light/ and page-320-dark/, each setting the width with setDeviceMetricsOverride and prefers-color-scheme with setEmulatedMedia (alongside --reduced-motion when given) — verify with `python3 plugin/tests/run.py test_fmshot`
- [x] without --width or --scheme, folders and calls stay as before, and --width with --profile keeps the profile's height and scale — verify with `python3 plugin/tests/run.py test_fmshot test_shot`
## Non-goals
## Approach (options → choice → why)
1. Loop views inside _run: for each page, for each (width, scheme), re-issue Emulation.setDeviceMetricsOverride and setEmulatedMedia, then shoot into PAGE-W-SCHEME/. Likely outcome: one browser, a small diff in _run and view(). Fails if: setEmulatedMedia replaces the whole feature list, so reduced motion must be sent with the scheme each time (it does replace; send both).
2. Start one Browser per view. Likely outcome: simplest code. Fails if: a 3×2 matrix of 5 pages starts 6 browsers, each a second or more.
3. Use what exists: Browser already sets metrics and media at start, view() already maps --profile to a size, _slug/_folder already make unique folders, and the stub browser in test_fmshot logs every call; reuse all of them, adding only the loop and the folder suffix. Likely outcome: no new helpers. Fails if: _folder's clearing of stale frames misfires on suffixed names (it clears per folder, so it doesn't).
4. Do less: document a chrome-headless loop in the ui-design skill. Fails if: every lane hand-writes it again (twice this session).
Choice 1 with 3 (85%): one browser, views looped, existing helpers reused.
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/lib/fmcli.py, plugin/lib/fmgenesis.py, plugin/tests/test_genesis.py, plugin/lib/fmhooks.py, plugin/lib/fmcore.py; past FIXes T-1129, T-1131, T-1132, T-1133, T-1134.
## Execution prompt
## Steps
1. [x] red tests in test_fmshot with the stub browser: the four folders, the emulation calls per view, the default unchanged, --width beside --profile, a bad width (0, 20000, words) refused
2. [x] fmshot: parse --width and --scheme, loop the views per page, re-issue the metrics and media per view, suffix the folder only when a flag is given
3. [x] MASTER.md's fm shot line and a CHANGELOG line
## Resume here
<!-- auto -->
- 2026-11-03T14:54:54Z step 2/3: fmshot: parse --width and --scheme, loop the views per page, re-issue the metrics and media per view, suffix the folder only when a flag is given
- git: foreman/build; 0 uncommitted
## Docs impact
none: fm shot -h documents the flags
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_fmshot test_shot 2>&1 | tail -15` → ✗ exit 1 · Ran 41 tests in 27.4s (7 classes, 16 at a time; slowest: Diff 25s, Capture 16s, Unruly 7s) / FAILED (1 classes: test_fmshot.Capture) [ran] [tree d2342d121a9c] [world 2f1906870a] (2026-11-03T04:18:26Z)
- (step 1) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 41 tests in 29.1s (7 classes, 16 at a time; slowest: Diff 28s, Capture 20s, InABrowser 8s) / OK [ran] [tree 47088b877559] [world 2f1906870a] (2026-11-03T04:20:38Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 33 tests in 24.9s (4 classes, 16 at a time; slowest: Diff 24s, Capture 17s, Unruly 7s) / OK [ran] [tree 255e2fab14f1] [world 2f1906870a] (2026-11-03T04:34:33Z)
- (ac 2) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 41 tests in 26.3s (7 classes, 16 at a time; slowest: Diff 26s, Capture 17s, Unruly 7s) / OK [ran] [tree 255e2fab14f1] [world 2f1906870a] (2026-11-03T04:35:00Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot` → exit 0 · Ran 33 tests in 21.6s (4 classes, 16 at a time; slowest: Diff 21s, Capture 14s, Unruly 6s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:55:37Z)
- (ac 2) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 41 tests in 21.4s (7 classes, 16 at a time; slowest: Diff 21s, Capture 14s, Unruly 6s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:55:37Z)
- (step 2) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 41 tests in 21.4s (7 classes, 16 at a time; slowest: Diff 21s, Capture 14s, Unruly 6s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:55:37Z)
- (step 3) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 41 tests in 21.4s (7 classes, 16 at a time; slowest: Diff 21s, Capture 14s, Unruly 6s) / OK [ran] [tree 1b964dd8dbe8] [world 2f1906870a] (2026-11-03T14:55:37Z)
- (audit intent) `self: read the merged diff; one browser shoots the width x scheme matrix` → fm shot --width W,W --scheme light|dark|both shoots the page matrix into PAGE-W-SCHEME folders [tree 1b964dd8dbe8] (2026-11-03T14:55:37Z)
- (audit edge) `self: read the merged diff; one browser shoots the width x scheme matrix` → no --width/--scheme keeps the old folders and calls; --width with --profile keeps the profile's height and scale [tree 1b964dd8dbe8] (2026-11-03T14:55:37Z)
- (audit adversary) `self: read the merged diff; one browser shoots the width x scheme matrix` → widths are parsed as ints and schemes from a fixed set; the page URL is the user's own argument, as before [tree 1b964dd8dbe8] (2026-11-03T14:55:37Z)
## Log
- 2026-11-03T03:25:11Z created
- 2026-11-03T03:28:33Z planned from capture
- 2026-11-03T03:28:44Z set approved=True
- 2026-11-03T03:28:45Z blocked: waits on T-2748, which moves plugin/lib/fmshot.py to plugin/lib/sampo/shot.py; planned and approved, ready for a builder lane once that merges
- 2026-11-03T04:17:01Z unblocked
- 2026-11-03T04:17:01Z unblocked: T-2748 merged; fmshot now lives at plugin/lib/sampo/shot.py (plugin/lib/fmshot.py is a shim; edit sampo/shot.py)
- 2026-11-03T04:17:02Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2758.builder.md
- 2026-11-03T04:17:10Z focused
- 2026-11-03T04:17:11Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-03T04:27:13Z merged worktree-agent-a665bc865ad3be0af (4 file(s))
- 2026-11-03T04:27:17Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a665bc865ad3be0af
- 2026-11-03T05:48:23Z focused
- 2026-11-03T05:48:25Z scope: files outside the scope since focus came from other lanes' merge commits, not this task's edits
- 2026-11-03T05:48:27Z paused: focus moved to T-2764
- 2026-11-03T14:54:52Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T14:54:52Z focused
- 2026-11-03T14:56:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Visual QA: screenshots, an eyeball pass and a receipt (fm playbooks show ui/visual-qa)
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- research T-1509-review: Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits. [st…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar past tasks were L: consider --tier L
- the similar finished task took 6 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_fmshot.py, plugin/tests/test_shot.py
## Preflight
Changed in scope since this was planned (2026-11-03): CHANGELOG.md, MASTER.md, plugin/lib/sampo/shot.py, plugin/tests/test_fmshot.py; re-ground the plan against them before editing
## Lessons
- Matrix flags belong on one browser session, not one launch per view
## Files touched
- plugin/tests/test_fmshot.py
- plugin/lib/sampo/shot.py
- plugin/lib/sampo/cli.py
- MASTER.md
