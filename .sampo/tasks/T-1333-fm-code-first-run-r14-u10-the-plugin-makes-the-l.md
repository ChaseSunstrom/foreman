---
id: T-1333
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsetup.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/lib/fmcodetui.py, plugin/tests/test_setup.py, plugin/tests/test_doctor.py, plugin/tests/test_code_tui.py, plugin/tests/helpers.py, README.md, CHANGELOG.md]
depends_on: []
source: followup
created: 2026-10-21T03:47:19Z
updated: 2026-10-23T13:54:23Z
base: ec6e271da612fb70a496345480641b80c63d7f0a
base_tree: 991c084fbec8f25a2e334a5ac1d7e6245c04d87f
plan0_at: 2026-10-23T13:47:25Z
plan0_scope: [plugin/lib/fmsetup.py, plugin/lib/fmhooks.py, plugin/lib/fmdoctor.py, plugin/lib/fmcodetui.py, plugin/tests/test_setup.py, plugin/tests/test_doctor.py, plugin/tests/test_code_tui.py, README.md, CHANGELOG.md]
verified: strong
---
# Fm code first run (R14+U10): the plugin makes the ~/.local/bin/fm link when absent and not
## Raw request
> fm code first run (R14+U10): the plugin makes the ~/.local/bin/fm link when absent and not someone else's; fm doctor FAILs with the fix when a login shell can't find fm; the app's first launch shows three chips (fm on PATH, a runner found, this folder is a project) each with a one-key fix, then offers 'explain this repo' as the first request
## Interpretation
A plugin installed from the marketplace never runs install.sh, so ~/.local/bin/fm is never made and fm works only inside Claude Code; an updated plugin leaves the link pointing at a deleted version folder. (1) Session start makes the link when nothing is there, or re-points a Foreman link whose target is gone; anything else (another program's fm, a working link to another Foreman checkout) stays. (2) fm doctor, with the link Foreman's, starts a fresh login shell (only the profile's PATH) and FAILs with the profile line to add when it can't find fm. (3) The app's welcome, before this project's first run, shows three chips (fm on PATH, a runner found, this folder is a project), each with a one-key fix (l links fm, m picks a runner, i makes the folder a project), and e opens the question box with 'explain this repo'.
## Assumptions (confidence)
## Acceptance criteria
- [x] the link is made when absent and re-pointed when Foreman's and broken, never otherwise; session start does it outside tests and workers — verify with `python3 plugin/tests/run.py test_setup`
- [x] fm doctor FAILs with the profile fix when a login shell can't find a Foreman fm link — verify with `python3 plugin/tests/run.py test_doctor`
- [x] the welcome before a project's first run shows the three chips and their keys; l, i and e do their fix; a project with a past run shows the usual welcome — verify with `python3 plugin/tests/run.py test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete version: the link made and repaired without touching anyone else's, the doctor's check of what a new terminal really sees, the first-run chips with fixes, and the first question offered. Options for the link: at session start (chosen: every install path runs it, a stat and a readlink), at install only (misses marketplace installs and updates), a PATH line in the user's profile (edits a file the user owns, skip). For the doctor: a login shell with a bare PATH (chosen: what a new terminal sees), parsing profile files (guesswork). For the chips: on the welcome screen when this project has no past run, keys only where tui.toml binds nothing (chosen), a separate first-run screen (another mode to keep).
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests: the link, the login shell, the chips
2. [x] ensure_fm_link and the session start call, the doctor probe, the welcome chips and keys; README and CHANGELOG
## Resume here
## Docs impact
README.md (Quick start: the first session puts fm on PATH, the doctor's fix; fm code tui paragraph: the first-run welcome), CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_setup test_doctor test_code_tui` → ✗ exit 1 · Ran 321 tests in 9.1s (74 classes, 16 at a time; slowest: Fuzz 9s, Command 8s, Install 4s) / FAILED (4 classes) [ran] [tree 6892992ff147] (2026-10-23T13:49:55Z)
- (step 1) `python3 plugin/tests/run.py test_setup test_doctor test_code_tui` → exit 0 · Ran 321 tests in 9.0s (74 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Install 3s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:52:08Z)
- (step 2) `python3 plugin/tests/run.py test_setup test_doctor test_code_tui test_hooks test_session test_session_files test_docs` → exit 0 · Ran 615 tests in 45.9s (127 classes, 16 at a time; slowest: Stop 46s, NoTaskGate 33s, PreToolUse 27s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:52:55Z)
- (ac 1) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 35 tests in 2.6s (9 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 1s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:52:58Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 67 tests in 2.0s (23 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, RuleConflicts 1s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:53:00Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 219 tests in 8.1s (42 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:53:09Z)
- (ac 1) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 35 tests in 2.6s (9 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 1s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
- (ac 2) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 67 tests in 1.9s (23 classes, 16 at a time; slowest: Command 2s, ViewsRepair 2s, RuleConflicts 1s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 219 tests in 8.1s (42 classes, 16 at a time; slowest: Fuzz 8s, Command 7s, Events 3s) / OK [ran] [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
- (audit intent) `self review in the main thread (subagents paused by the usage budget): the link targets the running plugin's own bin/fm, is made only where nothing is or a Foreman link is broken, and never in tests (FOREMAN_NO_LINK set for every test) or workers; the doctor's probe runs the user's own login shell with a bare PATH and a 5 s cap, and only once the link is Foreman's (a test home has none, so tests never run it); the chips are computed once a launch and after a fix, keys act only on the idle welcome and only where tui.toml binds nothing; the first-run welcome, rendered: two checks pass on this machine, the project one shows i` → a marketplace install gets fm in every shell without install.sh, a broken PATH is a FAIL with the exact line to add, and a first launch says what's missing and how to fix it with one key [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
- (audit edge) `self review in the main thread (subagents paused by the usage budget): the link targets the running plugin's own bin/fm, is made only where nothing is or a Foreman link is broken, and never in tests (FOREMAN_NO_LINK set for every test) or workers; the doctor's probe runs the user's own login shell with a bare PATH and a 5 s cap, and only once the link is Foreman's (a test home has none, so tests never run it); the chips are computed once a launch and after a fix, keys act only on the idle welcome and only where tui.toml binds nothing; the first-run welcome, rendered: two checks pass on this machine, the project one shows i` → a plugin update deleting the linked version (re-pointed), a dev checkout's working link (kept), another tool's fm (kept), a login profile that prints first (the last /path line counts), fish (fish_add_path), a login shell that finds a different fm first (FAIL naming it), a project with past runs (usual welcome), a tui.toml binding l, i or e (the binding wins) [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
- (audit adversary) `self review in the main thread (subagents paused by the usage budget): the link targets the running plugin's own bin/fm, is made only where nothing is or a Foreman link is broken, and never in tests (FOREMAN_NO_LINK set for every test) or workers; the doctor's probe runs the user's own login shell with a bare PATH and a 5 s cap, and only once the link is Foreman's (a test home has none, so tests never run it); the chips are computed once a launch and after a fix, keys act only on the idle welcome and only where tui.toml binds nothing; the first-run welcome, rendered: two checks pass on this machine, the project one shows i` → the target is the plugin's own path, never repo text; a planted broken link with foreman in its name is only replaced by Foreman's own; the probe runs the profile the user's terminal runs anyway, with no input and a timeout [tree 48c693ce4cc1] (2026-10-23T13:53:31Z)
## Log
- 2026-10-21T03:47:19Z created
- 2026-10-23T13:47:12Z set tier=M, scope=['plugin/lib/fmsetup.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_setup.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_code_tui.py', 'README.md', 'CHANGELOG.md']
- 2026-10-23T13:47:24Z focused
- 2026-10-23T13:48:55Z set scope=['plugin/lib/fmsetup.py', 'plugin/lib/fmhooks.py', 'plugin/lib/fmdoctor.py', 'plugin/lib/fmcodetui.py', 'plugin/tests/test_setup.py', 'plugin/tests/test_doctor.py', 'plugin/tests/test_code_tui.py', 'plugin/tests/helpers.py', 'README.md', 'CHANGELOG.md']
- 2026-10-23T13:54:21Z done
- 2026-10-23T13:54:23Z committed 62e18040 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- T-1397 [FEATURE M, done, 1 steps] Intake offer: fm code prints one line when an indexed skill matches the request (name, lic — lesson: Stack cards name tools (cargo) mor…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
- likely tests for the scope: plugin/tests/test_doctor.py, plugin/tests/test_hooks.py, plugin/tests/test_setup.py
## Preflight
Changed in scope since this was planned (2026-10-21): CHANGELOG.md, README.md, plugin/lib/fmcodetui.py, plugin/lib/fmdoctor.py, plugin/lib/fmhooks.py, plugin/tests/test_code_tui.py, plugin/tests/test_doctor.py; re-ground the plan against them before editing
## Lessons
- A check of what a new terminal sees has to start one: a login shell with a bare PATH, not this process's PATH
## Plan gaps
- failed first: step 1 red tests: the link, the login shell, the chips
## Files touched
- plugin/tests/helpers.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_doctor.py
- plugin/tests/test_setup.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmhooks.py
- plugin/lib/fmsetup.py
- CHANGELOG.md
- README.md
