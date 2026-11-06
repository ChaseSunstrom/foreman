---
id: T-1661
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmsettingsserve.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/evals/settings/newcomer.json, plugin/tests/test_settings_room.py, MASTER.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-22T20:58:57Z
updated: 2026-10-28T21:57:05Z
group: settings and control room extras
base: dee0bde1af83b3ffdd29330d11c0a8372265241d
base_tree: 3100c4930d7532a033f19d1e39fce41d3968949d
plan0_at: 2026-10-28T21:34:10Z
plan0_scope: []
verified: strong
---
# Control Room extras: a mouse-sketched layout, rotary dials, a fake-model first-time-user run
## Raw request
> Control Room extras: a mouse-sketched layout, rotary dials, a fake-model first-time-user run (from T-1545; waits: after fm settings serve and the playbook eval harness)
## Interpretation
Three Control Room extras, scoped to what tests can prove: the served page sketches the layout as a grid with move buttons (no JS drag: the CSP forbids script), numbers turn by detents in the page and in the app ([ ]), and a newcomer run plays the settings screen with only what it shows.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm settings serve draws the layout as a grid of panels, each with ← ↑ ↓ → buttons that move it (columns and heights in one write, as the app's layout editor does) — verify with `python3 plugin/tests/run.py test_settings_room`
- [x] numbers turn by detents: the served page shows a closed range as a range dial with detent ticks and an open one as a stepped number; the app's settings screen turns the selected number one detent with [ and ] — verify with `python3 plugin/tests/run.py test_settings_room`
- [x] fm settings newcomer plays a first-time user through the app's settings screen with only what it shows (a scripted user by default, --real asks a model), writes nothing, names the step and the missing hint where it got stuck, exits 1 then — verify with `python3 plugin/tests/run.py test_settings_room`
## Non-goals
## Approach (options → choice → why)
JS drag-and-drop (CSP forbids script) / one endpoint per direction / newcomer on a real pty / pure helpers in fmsettings shared by app and page, forms, in-process App replay with recorders → the last → deterministic, no script, nothing written, one move path for app and page
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first: test_settings_room for the three
2. [x] fmsettings.layout_moved and detent; the app's layout editor and [ ] use them
3. [x] served page: layout grid with move buttons (/move), range dials
4. [x] fm settings newcomer: goals file, scripted user, --real, nothing written
5. [x] docs, gates, review
## Resume here
<!-- auto -->
- 2026-10-28T21:47:38Z step 5/5: docs, gates, review
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmsettings.py, plugin/lib/fmsettingsserve.py, plugin/evals/settings/, plugin/tests/test_settings_room.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmsettings.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 11 tests in 2.9s (4 classes, 16 at a time; slowest: Page 3s, Newcomer 0s, Turn 0s) / OK [ran] [tree 167d9959939d] (2026-10-28T21:42:57Z)
- (step 2) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 11 tests in 2.9s (4 classes, 16 at a time; slowest: Page 3s, Newcomer 0s, Turn 0s) / OK [ran] [tree 167d9959939d] (2026-10-28T21:43:00Z)
- (step 3) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 11 tests in 2.9s (4 classes, 16 at a time; slowest: Page 3s, Newcomer 0s, Turn 0s) / OK [ran] [tree 167d9959939d] (2026-10-28T21:43:03Z)
- (step 4) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 11 tests in 2.9s (4 classes, 16 at a time; slowest: Page 3s, Newcomer 0s, Turn 0s) / OK [ran] [tree 167d9959939d] (2026-10-28T21:43:07Z)
- (step 5) `python3 plugin/tests/run.py test_settings_room test_settings_serve test_settings_extras test_code_tui test_settings` → exit 0 · Ran 380 tests in 9.1s (78 classes, 16 at a time; slowest: Serve 9s, Fuzz 8s, Command 8s) / OK [ran] [tree cf92d4510bb0] (2026-10-28T21:51:09Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 17 tests in 3.9s (4 classes, 16 at a time; slowest: Page 4s, Newcomer 0s, Turn 0s) / OK [ran] [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (ac 2) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 17 tests in 3.9s (4 classes, 16 at a time; slowest: Page 4s, Newcomer 0s, Turn 0s) / OK [ran] [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (ac 3) `python3 plugin/tests/run.py test_settings_room` → exit 0 · Ran 17 tests in 3.9s (4 classes, 16 at a time; slowest: Page 4s, Newcomer 0s, Turn 0s) / OK [ran] [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (audit intent) `one fm-reviewer pass over the diff (research T-1661-review): 8 findings, all fixed test-first; full gates green` → the three criteria hold: the served layout grid with move buttons (one write, one undo), dials and stepped numbers with [ ] in the app, and fm settings newcomer playing only what the screen shows and writing nothing [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (audit adversary) `one fm-reviewer pass over the diff (research T-1661-review): 8 findings, all fixed test-first; full gates green` → a stale page's move refused by panel name; newcomer's sandbox refuses writes outside it while the model call spends against the real budget; untrusted text through _safe [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (audit edge) `one fm-reviewer pass over the diff (research T-1661-review): 8 findings, all fixed test-first; full gates green` → Enter sets the typed value, not a turn; 0.3 turns to 0.35 (float division); a failed model call stops its goal, not the run; a bad goals file is refused; hints wrap at 100 and 80 columns [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (audit operator) `one fm-reviewer pass over the diff (research T-1661-review): 8 findings, all fixed test-first; full gates green` → newcomer --real without claude on PATH names the fix; stuck goals name the step and the missing hint; exit 1 when any goal fails [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
- (audit maintainer) `one fm-reviewer pass over the diff (research T-1661-review): 8 findings, all fixed test-first; full gates green` → layout_moved and detent shared by the app and the page; goals in plugin/evals/settings/newcomer.json; 16 tests in test_settings_room [tree cf92d4510bb0] (2026-10-28T21:55:20Z)
## Log
- 2026-10-22T20:58:57Z created
- 2026-10-28T21:33:42Z planned from capture
- 2026-10-28T21:34:08Z planned from capture
- 2026-10-28T21:34:09Z focused
- 2026-10-28T21:34:15Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmsettingsserve.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/evals/settings/newcomer.json', 'plugin/tests/test_settings_room.py', 'MASTER.md', 'CHANGELOG.md']
- 2026-10-28T21:55:47Z done
- 2026-10-28T21:55:48Z committed 2e553d04 (8 files)
- 2026-10-28T21:57:05Z includes T-1864: The hint row in plugin/lib/fmcodetui.py:1868 grew to about 119 cells and may clip "l layou
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1545 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
- T-1658 [FEATURE M, done, 5 steps] Settings extras: log, macro, duel, replay (what-breaks), words-to-diff, undo that adapts — lesson: CLI write tests need a pty: in_claud…
- T-1626 [FEATURE M, done, 5 steps] fm code's motion clock reads the project's Motion Score; fm motion compile --to lab: a page to play, scrub and edit each motion — lesso…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar finished tasks took 5–5 steps
## Lessons
- a form's first submit button is what Enter presses: put the default action first
## Files touched
- plugin/tests/test_settings_room.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmsettings.py
- plugin/lib/fmsettingsserve.py
- plugin/evals/settings/newcomer.json
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
