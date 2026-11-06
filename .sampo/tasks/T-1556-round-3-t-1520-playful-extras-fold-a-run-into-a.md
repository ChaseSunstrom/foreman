---
id: T-1556
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmextras.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_extras.py, plugin/tests/test_code_tui.py, plugin/skills/directions/SKILL.md, plugin/skills/directions/references/sonic.md, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:53Z
updated: 2026-10-23T17:14:07Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: ceca2e33efe1c9066fa999f4a710012fd8e50520
base_tree: 38c7e35542092e19df98d2c87b709f9d7dd21b62
plan0_at: 2026-10-23T17:09:49Z
plan0_scope: [plugin/lib/fmextras.py, plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_extras.py, plugin/skills/directions/SKILL.md, plugin/skills/directions/references/sonic.md, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Playful extras: fold a run into a printable zine, a lathe-turned vase fr
## Raw request
> Round 3 (T-1520): Playful extras: fold a run into a printable zine, a lathe-turned vase from a run, hand-drawn margin sketches on playbooks, Breakout while verify runs, swipe-to-approve on the phone status page, synthesised cursor choreography for demos, and a sonic UI recipe set, off by default (b102 b104 b105 b154 b167 b168 c025). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
Playful, opt-in extras made from an fm code run, offline and stdlib only: fm extras zine (the run as a one-sheet eight-page printable zine, SVG), fm extras vase (the run's events as a lathe profile turned into a closed STL), fm extras cursor (an eased cursor path with click ripples for demos, SVG), Breakout in the fm code app (b) that opens only while a run's checks run, closes when they stop and hands back every key it doesn't play, and a sonic UI recipe set in the directions skill, off by default.
## Assumptions (confidence)
## Acceptance criteria
- [x] the zine and the vase export valid SVG and STL from a fixture run; Breakout runs only while a verify runs and never steals keys from the prompt — verify with `cd plugin/tests && python3 -m unittest test_extras`
## Non-goals
## Approach (options → choice → why)
Options: (a) one module per extra; (b) fold the extras into fmcodetui (already 4,600 lines); (c) one small fmextras module for the run-made things and the game's logic, with only the key, view and close-on-stop wiring in fmcodetui. Chosen (c). The sonic set is Web Audio recipes in the directions references (pages are where sounds belong) rather than a player in the terminal. Left out: swipe-to-approve on a phone page (no phone status page exists, and approving a guard ask from a web page would bypass the person's own dialog) and hand-drawn margin sketches on playbooks (playbooks are read as Markdown by the model; nothing would show them).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] zine and vase
3. [x] Breakout and swipe approve
4. [x] cursor choreography and sonic set
5. [x] plugin parser, MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER.md (fmextras module line), CHANGELOG.md, plugin/skills/directions/SKILL.md (one sentence), plugin/skills/directions/references/sonic.md (new); fm extras -h and the keys poster (b) are the usage.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_extras` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.2s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 6931ac648abf] (2026-10-23T17:09:51Z)
- (step 1) `python3 plugin/tests/run.py test_extras` → exit 0 · Ran 9 tests in 0.4s (5 classes, 16 at a time; slowest: Zine 0s, Vase 0s, Cursor 0s) / OK [ran] [tree a89deee64349] (2026-10-23T17:12:31Z)
- (step 2) `python3 plugin/tests/run.py test_extras` → exit 0 · Ran 9 tests in 0.4s (5 classes, 16 at a time; slowest: Zine 0s, Vase 0s, Cursor 0s) / OK [ran] [tree a89deee64349] (2026-10-23T17:12:32Z)
- (step 3) `python3 plugin/tests/run.py test_extras` → exit 0 · Ran 9 tests in 0.4s (5 classes, 16 at a time; slowest: Zine 0s, Vase 0s, Cursor 0s) / OK [ran] [tree a89deee64349] (2026-10-23T17:12:33Z)
- (step 4) `python3 plugin/tests/run.py test_extras` → exit 0 · Ran 9 tests in 0.4s (5 classes, 16 at a time; slowest: Zine 0s, Vase 0s, Cursor 0s) / OK [ran] [tree a89deee64349] (2026-10-23T17:12:34Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs` → exit 0 · Ran 430 tests in 28.3s (100 classes, 16 at a time; slowest: TaskLifecycle 28s, Command 14s, Fuzz 13s) / OK [ran] [tree a89deee64349] (2026-10-23T17:13:03Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_extras` → exit 0 · Ran 9 tests in 0.390s / OK [ran] [tree a89deee64349] (2026-10-23T17:13:05Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_extras` → exit 0 · Ran 9 tests in 0.540s / OK [ran] [tree 41855d015192] (2026-10-23T17:13:27Z)
- (step 4) `python3 plugin/tests/run.py test_extras` → exit 0 · Ran 9 tests in 0.5s (5 classes, 16 at a time; slowest: Cursor 0s, Zine 0s, Vase 0s) / OK [ran] [tree 41855d015192] (2026-10-23T17:13:36Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_extras` → exit 0 · Ran 9 tests in 0.565s / OK [ran] [tree 41855d015192] (2026-10-23T17:13:38Z)
- (audit intent) `self-review of fmextras and the fm code wiring: zine text escaped and imposed (ring order tested), vase watertight with one winding and positive volume, cursor refuses one point, no distance and non-points without a traceback, Breakout opens only while checks_running, closes in poll when they stop, and only arrows, h/l, Esc and B are the game's; photographed the app with the game open and widened its box so the title and keys show` → a run becomes a zine and a vase, demos get a cursor, a game fills the wait while checks run, pages get a sound set that starts off; swipe-approve and margin sketches left out with a recorded decision [tree 41855d015192] (2026-10-23T17:13:38Z)
- (audit edge) `self-review of fmextras and the fm code wiring: zine text escaped and imposed (ring order tested), vase watertight with one winding and positive volume, cursor refuses one point, no distance and non-points without a traceback, Breakout opens only while checks_running, closes in poll when they stop, and only arrows, h/l, Esc and B are the game's; photographed the app with the game open and widened its box so the title and keys show` → an empty run still makes a two-ring vase; a long title wraps to three lines on the cover; dt is capped at 0.5 s and sub-stepped so the ball never tunnels; extensions binding b keep it (Breakout is on B) [tree 41855d015192] (2026-10-23T17:13:38Z)
- (audit adversary) `self-review of fmextras and the fm code wiring: zine text escaped and imposed (ring order tested), vase watertight with one winding and positive volume, cursor refuses one point, no distance and non-points without a traceback, Breakout opens only while checks_running, closes in poll when they stop, and only arrows, h/l, Esc and B are the game's; photographed the app with the game open and widened its box so the title and keys show` → run files are the user's own and every string is html-escaped into the SVG; nothing is fetched, installed or executed; the game takes no key from the prompt (prompt mode is handled before it, and any key it doesn't play closes it and runs as usual) [tree 41855d015192] (2026-10-23T17:13:38Z)
## Log
- 2026-10-22T17:43:53Z created
- 2026-10-22T18:06:41Z set scope=['plugin/lib/fmpage.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmserve.py', 'plugin/tests/test_extras.py', 'CHANGELOG.md']
- 2026-10-23T16:59:38Z set tier=M, scope=['plugin/lib/fmextras.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_extras.py', 'plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/sonic.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:09:48Z focused
- 2026-10-23T17:12:08Z set scope=['plugin/lib/fmextras.py', 'plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_extras.py', 'plugin/tests/test_code_tui.py', 'plugin/skills/directions/SKILL.md', 'plugin/skills/directions/references/sonic.md', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T17:12:08Z scope: test_code_tui.py added: its view sweep must include the new breakout view
- 2026-10-23T17:14:06Z done
- 2026-10-23T17:14:07Z committed 48e22b97 (9 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1545 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
- decision 2026-10-23: T-1556: left out swipe-to-approve and margin sketches
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/skills/directions/SKILL.md; re-ground the plan against them before editing
## Lessons
- A default key binding can collide with keys tests and extensions assume are free: grep the tests for key= before claiming a letter.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_extras.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/skills/directions/SKILL.md
- plugin/lib/fmextras.py
- plugin/skills/directions/references/sonic.md
- plugin/tests/test_code_tui.py
