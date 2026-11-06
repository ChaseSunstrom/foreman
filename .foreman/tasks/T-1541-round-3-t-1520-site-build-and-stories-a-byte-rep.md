---
id: T-1541
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, site/build.py, site/pages.py, site/style.css, plugin/tests/test_site_build.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-22T17:43:49Z
updated: 2026-10-23T16:05:21Z
inferred_deps: [T-1520]
inferred_why: T-1520: named in its request
group: round 3 creative and playbook extras
base: 234a8ee4c7cc27f5a190d73d293c72cea3d52e05
base_tree: d1d861461de447c362e3335b71d52df8dfc5606b
plan0_at: 2026-10-23T16:00:43Z
plan0_scope: [plugin/lib/fmcodetui.py, plugin/lib/fmcli.py, site/build.py, site/pages.py, site/style.css, plugin/tests/test_site_build.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Round 3 (T-1520): Site build and stories: a byte-reproducible site and demo build, case-st
## Raw request
> Round 3 (T-1520): Site build and stories: a byte-reproducible site and demo build, case-study pages from proved runs, generated release covers, a release-over-release design wall, and a hand-lettered title card when a task closes proved (a076 a138 b030 b080 a160). Plugin parity: usable from Claude Code (an fm verb, a /foreman: command or skill, a hook note or the foreman-ui pane) as well as fm code. A browser, GPU or model dependency is optional: detected and used when present, never required, never installed silently.
## Interpretation
A byte-reproducible site and demo build (the fm code snapshots drawn at a fixed time), case-study pages from proved runs (the recorded fm code example runs, published on purpose: stats.py never publishes this repo's task titles or commands), generated release covers on a release-over-release wall, and a hand-lettered title card when a task closes proved (fm task card; fm task finish writes it).
## Assumptions (confidence)
## Acceptance criteria
- [x] two builds of the site from the same commit are byte-identical; a case-study page renders from a fixture ledger — verify with `cd plugin/tests && python3 -m unittest test_site_build`
## Non-goals
## Approach (options → choice → why)
Options for case studies: (a) this repo's proved tasks from the ledger (breaks stats.py's rule: no task titles, paths or commands published); (b) the recorded example runs the site already shows as cards; (c) new fixture runs. Choice: (b), a page per run from its own events. Reproducibility: find what differs between two builds (the snapshots' colour pulse read the wall clock) and pin it, with a test that builds twice. Covers and cards are deterministic SVG from data, no fonts embedded.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests
2. [x] reproducible build
3. [x] case studies, covers, design wall
4. [x] title card
5. [x] red tests: two builds identical, a case study from a fixture, the wall, a title card
6. [x] snapshot at t=0; case_study_html and stories/; _wall; title_card, write_card, fm task card and the finish hook; CHANGELOG, MASTER
## Resume here
## Docs impact
~/.claude/foreman/CHANGELOG.md, ~/.claude/foreman/MASTER.md (Site build and stories), site/ pages (case studies, the releases wall), fm task's own help (card)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site_build` → ✗ exit 1 · Ran 4 tests in 0.9s (3 classes, 16 at a time; slowest: TitleCard 1s, Reproducible 1s, Stories 0s) / FAILED (3 classes) [ran] [tree b49a1f24d37c] (2026-10-23T16:00:50Z)
- (step 1) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.4s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 11s) / OK [ran] [tree 85150770609f] (2026-10-23T16:02:34Z)
- (step 2) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.4s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Fuzz 11s, Command 11s) / OK [ran] [tree 85150770609f] (2026-10-23T16:02:59Z)
- (step 3) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.4s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 10s) / OK [ran] [tree 85150770609f] (2026-10-23T16:03:25Z)
- (step 4) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.3s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 10s, Fuzz 10s) / OK [ran] [tree 85150770609f] (2026-10-23T16:03:50Z)
- (step 5) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.6s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 11s) / OK [ran] [tree 85150770609f] (2026-10-23T16:04:15Z)
- (step 6) `python3 plugin/tests/run.py test_site_build test_docs test_code_tui test_cli test_suite_hygiene` → exit 0 · Ran 431 tests in 24.7s (102 classes, 16 at a time; slowest: TaskLifecycle 24s, Command 11s, Fuzz 11s) / OK [ran] [tree 85150770609f] (2026-10-23T16:04:40Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_site_build` → exit 0 · Ran 4 tests in 1.097s / OK [ran] [tree 85150770609f] (2026-10-23T16:04:42Z)
- (ac 1) `cd plugin/tests && python3 -m unittest test_site_build` → exit 0 · Ran 4 tests in 1.095s / OK [ran] [tree 85150770609f] (2026-10-23T16:04:53Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): two builds compared file by file found the one difference (fm code snapshots read the wall clock for their colour pulse) and pinned it at t=0; case studies come from the recorded example runs, keeping stats.py's rule that this repo's task titles and commands are never published; viewed a case-study page and a title card as images: both fit after narrowing the card's lines for the fallback face` → a byte-reproducible site and demo build, case-study pages from proved runs, generated release covers on a wall, and a hand-lettered title card at a proved close, each from Claude Code (fm task card, fm task finish) or the site build [tree 85150770609f] (2026-10-23T16:04:53Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): two builds compared file by file found the one difference (fm code snapshots read the wall clock for their colour pulse) and pinned it at t=0; case studies come from the recorded example runs, keeping stats.py's rule that this repo's task titles and commands are never published; viewed a case-study page and a title card as images: both fit after narrowing the card's lines for the fallback face` → no releases → no wall section; a run with no plan title uses its request; a title past three lines ends with …; a task with no proof gets a usage error from fm task card and no card at finish; the card's face falls back to cursive when none of the hand faces is installed, sized so the fallback still fits [tree 85150770609f] (2026-10-23T16:04:53Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): two builds compared file by file found the one difference (fm code snapshots read the wall clock for their colour pulse) and pinned it at t=0; case studies come from the recorded example runs, keeping stats.py's rule that this repo's task titles and commands are never published; viewed a case-study page and a title card as images: both fit after narrowing the card's lines for the fallback face` → every value a recorded run or a task title carries is HTML-escaped in the case study and the card (a title with <qty> is tested); the card writes only inside the project's state folder or the --out path given, through write_atomic; nothing is fetched or embedded [tree 85150770609f] (2026-10-23T16:04:53Z)
## Log
- 2026-10-22T17:43:49Z created
- 2026-10-22T18:06:06Z set scope=['site', 'plugin/lib/fmpage.py', 'plugin/tests/test_site_build.py', 'CHANGELOG.md']
- 2026-10-23T16:00:25Z set tier=M, scope=['plugin/lib/fmcodetui.py', 'plugin/lib/fmcli.py', 'site/build.py', 'site/pages.py', 'site/style.css', 'plugin/tests/test_site_build.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T16:00:42Z focused
- 2026-10-23T16:05:19Z done
- 2026-10-23T16:05:21Z committed 6aebec45 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1523 [FEATURE M, done, 5 steps] Round 3 (T-1520): Playbooks drafted from finished runs and history: a draft from a proved — lesson: A brief is already a distilled tran…
- T-1553 [SECURITY M, done, 3 steps] Guard oracle: a stub-exec run agrees with the guard's reading — lesson: A tool that runs things to check them must treat 'didn't run' …
- T-1542 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, ta
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- similar finished tasks took 3–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, site/build.py, site/pages.py, site/style.css; re-ground the plan against them before editing
## Lessons
- To make a build reproducible, build twice and diff: the one wall-clock read was in a snapshot's colour pulse, not where a timestamp would be looked for
## Plan gaps
- failed first: step 1 failing tests
## Files touched
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmcodetui.py
- site/build.py
- site/pages.py
- site/style.css
- plugin/tests/test_site_build.py
