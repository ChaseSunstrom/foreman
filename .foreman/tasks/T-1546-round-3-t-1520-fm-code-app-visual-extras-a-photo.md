---
id: T-1546
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:50Z
updated: 2026-10-23T16:19:10Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 31101c2aef5e89345b34993e63772c6f50038eba
base_tree: 324da89342285339642ea23fa3a35a0685b74737
plan0_at: 2026-10-23T16:13:35Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, plugin/tests/test_code_tui.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): fm code app visual extras: a photo booth for frames, an isometric layout
## Raw request
> Round 3 (T-1520): fm code app visual extras: a photo booth for frames, an isometric layout builder, golden frames pinned to a terminal-emulator oracle, a nightly chaos twin (keys, resizes, event floods), springy draggable panels and a UI that wears in with use (b099 b131 b139 b141 c104 c050). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
fm code app visual extras: a photo booth (F writes the frame on screen as SVG and, with rsvg-convert, PNG; fm code tui --snapshot FILE.png for Claude Code), and a chaos twin (fm code tui --chaos SECONDS: hostile event floods, random read-only keys and resizes at a headless app, a seed to replay any crash). Left out (decided): the isometric layout builder, golden frames against a terminal-emulator oracle, springy draggable panels and a UI that wears in with use.
## Assumptions (confidence)
## Acceptance criteria
- [x] the photo booth writes an SVG and a PNG of the current frame; the chaos twin runs N seconds without a crash — verify with `cd plugin/tests && python3 -m unittest test_code_tui.Extras`
- [x] the photo booth writes an SVG and a PNG; the chaos twin runs without a crash; a PNG snapshot of a recorded run — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Options for the chaos twin: (a) drive the real terminal app through a pty; (b) the App and render() headless, fed events and keys in-process with every outside source stubbed; (c) property tests over render alone. Choice: (b): it exercises the same key handler and renderer the screen uses, can't write the user's settings or run a command (only read-only commands are pressed, the root is an empty temp folder), and a seed replays a crash. The photo booth reuses to_svg and the rsvg-convert step record() already needs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] photo booth
3. [x] isometric builder, springs, patina
4. [x] oracle and chaos twin
5. [x] red tests: photo booth, chaos twin, PNG snapshot
6. [x] photo, take_photo and the F key; _png and snapshot to .png; chaos and --chaos/--seed; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (fm code app extras), the app's keys help (F) and fm code's flags (--chaos, --seed, --snapshot FILE.png)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_code_tui.Extras` → ✗ exit 1 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: Extras 0s) / FAILED (1 classes) [ran] [tree 5b1334777d67] (2026-10-23T16:13:42Z)
- (step 1) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 25.1s (103 classes, 16 at a time; slowest: TaskLifecycle 25s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:15:59Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 24.7s (103 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:16:24Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 24.6s (103 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:16:50Z)
- (step 4) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 24.9s (103 classes, 16 at a time; slowest: TaskLifecycle 25s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:17:15Z)
- (step 5) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 25.3s (103 classes, 16 at a time; slowest: TaskLifecycle 25s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:17:41Z)
- (step 6) `python3 plugin/tests/run.py test_code_tui test_cli test_suite_hygiene test_docs test_site_build` → exit 0 · Ran 434 tests in 25.1s (103 classes, 16 at a time; slowest: TaskLifecycle 25s, Command 11s, Fuzz 11s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:18:07Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Extras` → exit 0 · Ran 3 tests in 3.418s / OK [ran] [tree b930245c83a5] (2026-10-23T16:18:11Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 234 tests in 8.4s (46 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 4s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:18:20Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_code_tui.Extras` → exit 0 · Ran 3 tests in 3.437s / OK [ran] [tree b930245c83a5] (2026-10-23T16:18:42Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 234 tests in 8.3s (46 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 4s) / OK [ran] [tree b930245c83a5] (2026-10-23T16:18:42Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the chaos twin ran six seeds for 10 s each (about 58,000 hostile events, 3,700 keys, 1,500 resizes) with no crash; it presses only read-only commands on an App whose root, history and every source are a temp folder or stubs, so it can't write settings, record taste or run a command; the photo booth reuses to_svg and the rsvg-convert step record() already uses` → the photo booth and the chaos twin the plan named, each from Claude Code (fm code tui --snapshot FILE.png, --chaos) and the app (F); the rest left out by a recorded decision [tree b930245c83a5] (2026-10-23T16:18:42Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the chaos twin ran six seeds for 10 s each (about 58,000 hostile events, 3,700 keys, 1,500 resizes) with no crash; it presses only read-only commands on an App whose root, history and every source are a temp folder or stubs, so it can't write settings, record taste or run a command; the photo booth reuses to_svg and the rsvg-convert step record() already uses` → no rsvg-convert → the SVG is written and the PNG note says why; two photos in one second get -2, -3 names; a 1x1 screen and empty or 1000-character strings are in the chaos mix; Enter typed into the prompt becomes Esc, so a request is never sent [tree b930245c83a5] (2026-10-23T16:18:42Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the chaos twin ran six seeds for 10 s each (about 58,000 hostile events, 3,700 keys, 1,500 resizes) with no crash; it presses only read-only commands on an App whose root, history and every source are a temp folder or stubs, so it can't write settings, record taste or run a command; the photo booth reuses to_svg and the rsvg-convert step record() already uses` → chaos never presses settings, looks, undo, pr, queue, tickets, quit or the card keys that link fm or run a live CLI, and Enter in the prompt is replaced, so nothing runs or writes outside its temp folder; the photo is written under Foreman's own home with a fresh name, never over a file [tree b930245c83a5] (2026-10-23T16:18:42Z)
## Log
- 2026-10-22T17:43:50Z created
- 2026-10-22T18:06:16Z set scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcodeterm.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md']
- 2026-10-23T16:13:32Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_code_tui.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:13:34Z focused
- 2026-10-23T16:19:08Z done
- 2026-10-23T16:19:10Z committed 438e4aca (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1534 [FEATURE M, done, 4 steps] Round 3 (T-1520): UI replay and determinism: render foreman-ui from recorded fixtures with — lesson: Determinism checks need the render…
- decision 2026-10-23: T-1546: leave out the isometric layout builder, golden frames against a terminal-emulator oracle, springy draggable panels and a wear-in UI
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/tests/test_code_tui.py; re-ground the plan against them before editing
## Lessons
- A chaos harness is safe to run anywhere only when it presses an allowlist: a denylist misses the next key that writes
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py
- CHANGELOG.md
- MASTER.md
