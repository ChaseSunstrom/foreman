---
id: T-1555
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmmarks.py, plugin/lib/fmcli.py, plugin/tests/test_marks.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:53Z
updated: 2026-10-23T16:53:04Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 66e6b3da661203bf613184f030eee2ea6d9118d9
base_tree: c1813d933ea3241aa8d587017088ecc3c4000d2b
plan0_at: 2026-10-23T16:49:31Z
plan0_scope: [plugin/lib/fmmarks.py, plugin/lib/fmcli.py, plugin/tests/test_marks.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Fonts, icons and marks: an offline font shelf with vetted pairings, subs
## Raw request
> Round 3 (T-1520): Fonts, icons and marks: an offline font shelf with vetted pairings, subset and self-host, a consistent icon family and empty-state illustration set, and a generated project wordmark (a143 a172 c016 c057 c064). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
A new verb, fm marks, gives a project its marks offline and stdlib only: icons (one 24 grid, one 2-unit stroke, round caps, currentColor; each file plus an icons.svg sprite), empty-state illustrations built from those same icon paths, a wordmark (monogram tile plus the name in a hue drawn from the name, escaped), and a font shelf of vetted open-licence pairings marked against fc-list, with a subset for self-hosting when fontTools is installed (never installed here). Usable from Claude Code as an fm verb.
## Assumptions (confidence)
## Acceptance criteria
- [x] the icon generator writes a consistent SVG set on one grid and stroke; the wordmark is valid SVG — verify with `cd plugin/tests && python3 -m unittest test_marks`
## Non-goals
## Approach (options → choice → why)
Options: (a) bundle font files and an icon font in the repo (size, licences); (b) generate icons from primitives at runtime (circle/line helpers): more code, same result; (c) a fixed table of hand-drawn paths on one grid, emitted with one shared attribute set so grid and stroke are the same by construction. Chosen (c), plus a pairings table checked against fc-list and pyftsubset via fontTools when present: smallest code, consistent output, no new dependency. Left out: a pane card and a /foreman: command (the fm verb is the plugin surface).
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] font shelf cards and subset recipe
3. [x] icons and empty states
4. [x] wordmark
5. [x] plugin parser, MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER.md (plugin/lib modules line for fmmarks, fm marks span), CHANGELOG.md entry; fm marks -h is the usage.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_marks` → ✗ exit 1 (never ran: no tests ran) · Ran 1 tests in 1.0s (2 classes, 16 at a time; slowest: Sync 1s, _FailedTest 0s) / FAILED (1 classes) [ran] [tree 5830957aef3c] (2026-10-23T16:49:36Z)
- (step 1) `python3 plugin/tests/run.py test_marks` → exit 0 · Ran 5 tests in 1.0s (2 classes, 16 at a time; slowest: Sync 1s, Marks 1s) / OK [ran] [tree 38c7e3554209] (2026-10-23T16:51:49Z)
- (step 2) `python3 plugin/tests/run.py test_marks` → exit 0 · Ran 5 tests in 1.0s (2 classes, 16 at a time; slowest: Sync 1s, Marks 1s) / OK [ran] [tree 38c7e3554209] (2026-10-23T16:51:50Z)
- (step 3) `python3 plugin/tests/run.py test_marks` → exit 0 · Ran 5 tests in 1.0s (2 classes, 16 at a time; slowest: Sync 1s, Marks 1s) / OK [ran] [tree 38c7e3554209] (2026-10-23T16:51:52Z)
- (step 4) `python3 plugin/tests/run.py test_marks` → exit 0 · Ran 5 tests in 1.1s (2 classes, 16 at a time; slowest: Sync 1s, Marks 1s) / OK [ran] [tree 38c7e3554209] (2026-10-23T16:51:54Z)
- (step 5) `python3 plugin/tests/run.py test_cli test_suite_hygiene test_docs` → exit 0 · Ran 196 tests in 26.0s (54 classes, 16 at a time; slowest: TaskLifecycle 26s, StateViews 10s, Fences 10s) / OK [ran] [tree 38c7e3554209] (2026-10-23T16:52:21Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_marks` → exit 0 · Ran 4 tests in 0.615s / OK [ran] [tree 38c7e3554209] (2026-10-23T16:52:22Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_marks` → exit 0 · Ran 4 tests in 0.597s / OK [ran] [tree 38c7e3554209] (2026-10-23T16:52:35Z)
- (audit intent) `self-review of fmmarks and its parser: one shared attribute set for icons, sprite and empty states; the name escaped in attribute and text; stroke bounded; fc-list and fontTools optional with the recipe said when missing; rendered icons, wordmark and an empty state to PNG and fixed a clipped line and a sun-like settings icon` → fm marks gives icons on one grid and stroke, empty states from them, a wordmark and a font shelf, offline, from Claude Code as an fm verb [tree 38c7e3554209] (2026-10-23T16:52:35Z)
- (audit edge) `self-review of fmmarks and its parser: one shared attribute set for icons, sprite and empty states; the name escaped in attribute and text; stroke bounded; fc-list and fontTools optional with the recipe said when missing; rendered icons, wordmark and an empty state to PNG and fixed a clipped line and a sun-like settings icon` → a 48-character empty-state line clipped at 240 wide: lines now capped at LINE=36 and tested; --stroke 9 refused; a blank name becomes Untitled; fc-list missing marks ? instead of failing [tree 38c7e3554209] (2026-10-23T16:52:35Z)
- (audit adversary) `self-review of fmmarks and its parser: one shared attribute set for icons, sprite and empty states; the name escaped in attribute and text; stroke bounded; fc-list and fontTools optional with the recipe said when missing; rendered icons, wordmark and an empty state to PNG and fixed a clipped line and a sun-like settings icon` → the wordmark name is html-escaped in aria-label and text (test with R&D <Lab>); fc-list runs with a fixed argv and a timeout; nothing is fetched or installed [tree 38c7e3554209] (2026-10-23T16:52:35Z)
## Log
- 2026-10-22T17:43:53Z created
- 2026-10-22T18:06:39Z set scope=['plugin/skills/library/cards/looks', 'plugin/lib/fmdesign.py', 'plugin/tests/test_marks.py', 'CHANGELOG.md']
- 2026-10-23T16:49:28Z set scope=['plugin/lib/fmmarks.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_marks.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:49:30Z focused
- 2026-10-23T16:53:03Z done
- 2026-10-23T16:53:04Z committed ceca2e33 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1528 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): One scene description, many renderers: scene.json compiles to three.js,
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py; re-ground the plan against them before editing
## Lessons
- Render generated SVG to PNG and look before closing: a test of structure passed while a line was clipped and an icon read as the wrong thing.
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- plugin/tests/test_marks.py
- plugin/lib/fmcli.py
- plugin/lib/fmmarks.py
- CHANGELOG.md
- MASTER.md
