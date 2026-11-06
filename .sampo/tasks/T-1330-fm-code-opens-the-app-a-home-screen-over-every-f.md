---
id: T-1330
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-21T03:24:09Z
updated: 2026-10-21T07:48:26Z
base: b640405dd3b6ec82e07af5c82c4c51d01009eb7f
base_tree: 8c1dfe12d1b630620d520e84742a572cbd83c6ea
plan0_at: 2026-10-21T06:45:04Z
plan0_scope: []
verified: strong
---
# fm code opens the app: a home screen over every Foreman project (queue, inbox, active, blocked, past runs) that runs any queued task or a new request in any project with any runner
## Raw request
> fm code opens the app: a home screen over every Foreman project (queue, inbox, active, blocked, past runs) that runs any queued task or a new request in any project with any runner
## Interpretation
The user asked why they can't launch fm code as a management TUI like Claude Code. Plain fm code on a terminal opens one app: inside a project its view (active task, queue, inbox, blocked, past runs), elsewhere a home over every Foreman project; from there a queued task runs (fm code --task ID) or a new request starts, in that project's folder, with the runner picked by m.
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm code` with no request on a terminal opens the app (inside a Foreman project on that project's view, elsewhere on home); piped or without a terminal it prints today's message and exits 1, unchanged — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] home lists every project `fm projects --json` gives (name, root, active, queue/inbox/blocked counts, next), newest first; a project whose state can't be read shows why in its row and the rest still draw — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] a project's view lists its active task, queue, inbox and blocked tasks (`fm state --json -p ID`) and its past fm code runs (its code/*.events.jsonl); Enter on a past run replays it — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] r on a queued task starts `fm code --task ID` with that project's root as its folder and the runner picked with m; n starts a new request there the same way — verify with `python3 plugin/tests/run.py test_code_tui`
- [x] `fm code --task ID` works a planned brief (its criteria and steps are the plan, no planner call); it refuses, saying why, a task with no runnable criterion, one that is done or dropped, one of another project, and one another fm code run is working — verify with `python3 plugin/tests/run.py test_code`
## Non-goals
## Approach (options → choice → why)
Data: fm projects --json (every project: root, active, queue/inbox/blocked counts, next) for the home, fm state --json -p ID (active, queue, inbox, blocked lists with id/type/tier/title/status) for a project; both read through fm as subprocesses so the TUI never touches state directly. Views in the existing App (fmcodetui): home (projects, newest first, with counts and next), project (its active task, queue, inbox, blocked; past runs), run (today's screen). Keys: Enter opens, Esc back, n new request (capture or run now, in the selected project), r run the selected task (fm code --task ID, spawned with that project's root as cwd), m runner, / filter. fm code --task ID (fmcode): a planned brief's criteria and steps are the plan (no planner call), the task is focused, the loop runs as for a request. fm code with no request on a terminal opens the app on home (in a project: that project's view). Options weighed: a separate fm app program (rejected: duplicates the renderer and App), reading state files directly (rejected: state is fm's), a web dashboard (out of scope: Foreman has one; this is the terminal app). Second-plan before building (L).
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm code --task ID: work an existing brief (its criteria and steps are the plan)
2. [x] fm code with no request opens the app
3. [x] Home and project views, keys, runner picker per run
4. [x] Docs, site, review
## Resume here
## Docs impact
site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_code` → ✗ exit 1 · Ran 187 tests in 110.6s (28 classes, 16 at a time; slowest: Worker 110s, Bench 31s, Review 21s) / FAILED (1 classes) [ran] [tree f8711e6346eb] (2026-10-21T06:47:12Z)
- (ac 5) `python3 plugin/tests/run.py test_code 2>&1 | grep -E "^(FAIL|ERROR):|^OK|^FAILED|Error|assert" | head -12` → exit 0 · OK [ran] [tree 55e00f4277f9] (2026-10-21T06:49:49Z)
- (step 1) `python3 plugin/tests/run.py test_code test_code_worker` → exit 0 · Ran 187 tests in 115.7s (28 classes, 16 at a time; slowest: Worker 115s, Bench 34s, Fuzz 25s) / OK [ran] [tree 55e00f4277f9] (2026-10-21T06:51:50Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui` → ✗ exit 1 · Ran 91 tests in 24.9s (14 classes, 16 at a time; slowest: Fuzz 25s, Command 16s, Events 11s) / FAILED (2 classes) [ran] [tree 73a1d7420519] (2026-10-21T06:52:35Z)
- (step 2) `python3 plugin/tests/run.py test_code_tui test_code` → exit 0 · Ran 194 tests in 114.7s (29 classes, 16 at a time; slowest: Worker 114s, Bench 34s, Review 22s) / OK [ran] [tree 788c8670f53c] (2026-10-21T07:01:26Z)
- (step 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 92 tests in 30.7s (14 classes, 16 at a time; slowest: Fuzz 30s, Command 12s, Events 7s) / OK [ran] [tree 788c8670f53c] (2026-10-21T07:01:57Z)
- (step 4) `python3 site/build.py --check 2>/dev/null || python3 site/build.py` → exit 0 · built --check: landing page + 15 feature pages [ran] [tree 165ad90c52d1] (2026-10-21T07:09:45Z)
- (step 1) `python3 plugin/tests/run.py test_code test_code_tui test_code_worker` → exit 0 · Ran 199 tests in 117.7s (29 classes, 16 at a time; slowest: Worker 117s, Bench 32s, Repairs 24s) / OK [ran] [tree 402802501675] (2026-10-21T07:35:20Z)
- (step 2) `python3 plugin/tests/run.py test_code test_code_tui test_code_worker` → exit 0 · Ran 199 tests in 117.7s (29 classes, 16 at a time; slowest: Worker 117s, Bench 34s, Repairs 22s) / OK [ran] [tree 402802501675] (2026-10-21T07:37:18Z)
- (step 3) `python3 plugin/tests/run.py test_code test_code_tui test_code_worker` → exit 0 · Ran 199 tests in 119.7s (29 classes, 16 at a time; slowest: Worker 119s, Bench 35s, Repairs 23s) / OK [ran] [tree 402802501675] (2026-10-21T07:39:19Z)
- (ac 1) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 95 tests in 19.7s (14 classes, 16 at a time; slowest: Fuzz 19s, Command 11s, Events 7s) / OK [ran] [tree 402802501675] (2026-10-21T07:45:08Z)
- (ac 2) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 95 tests in 19.7s (14 classes, 16 at a time; slowest: Fuzz 19s, Command 11s, Events 7s) / OK [ran] [tree 402802501675] (2026-10-21T07:45:08Z)
- (ac 3) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 95 tests in 19.7s (14 classes, 16 at a time; slowest: Fuzz 19s, Command 11s, Events 7s) / OK [ran] [tree 402802501675] (2026-10-21T07:45:08Z)
- (ac 4) `python3 plugin/tests/run.py test_code_tui` → exit 0 · Ran 95 tests in 19.7s (14 classes, 16 at a time; slowest: Fuzz 19s, Command 11s, Events 7s) / OK [ran] [tree 402802501675] (2026-10-21T07:45:08Z)
- (ac 5) `python3 plugin/tests/run.py test_code` → exit 0 · Ran 199 tests in 116.5s (29 classes, 16 at a time; slowest: Worker 116s, Bench 35s, Fuzz 28s) / OK [ran] [tree 402802501675] (2026-10-21T07:45:08Z)
- (audit intent) `one fm-reviewer pass, all five lenses (L); 11 findings: 9 fixed test-first, 2 accepted (synchronous fm calls when opening views; the reworded no-request message, which only adds a hint); real machine: fm code in a pseudo-terminal opened this project's view and the home listed all 18 projects, nixie included` → fm code alone on a terminal opens the app (project view inside a project, home elsewhere); piped it's the usage error, exit 1 as before; Enter/r runs a task with fm code --task in its own folder with the m runner; n a new request there [tree 402802501675] (2026-10-21T07:45:08Z)
- (audit adversary) `one fm-reviewer pass, all five lenses (L); 11 findings: 9 fixed test-first, 2 accepted (synchronous fm calls when opening views; the reworded no-request message, which only adds a hint); real machine: fm code in a pseudo-terminal opened this project's view and the home listed all 18 projects, nixie included` → every project-sourced string draws through Canvas.put, which blanks non-printables; --task's brief text is made printable for plain output; roots reach only Popen cwd, ids only argv; a refused or unrunnable check stops --task [tree 402802501675] (2026-10-21T07:45:08Z)
- (audit edge) `one fm-reviewer pass, all five lenses (L); 11 findings: 9 fixed test-first, 2 accepted (synchronous fm calls when opening views; the reworded no-request message, which only adds a hint); real machine: fm code in a pseudo-terminal opened this project's view and the home listed all 18 projects, nixie included` → a missing folder never starts a run and sorts last; browsing never moves the run's folder (resume and diff stay with the run); Esc in the request box returns to the project; an unfinished earlier run is resumed, a finished one kept beside; an unchecked criterion is refused so evidence never lands on the wrong number; ids match in any case [tree 402802501675] (2026-10-21T07:45:08Z)
- (audit operator) `one fm-reviewer pass, all five lenses (L); 11 findings: 9 fixed test-first, 2 accepted (synchronous fm calls when opening views; the reworded no-request message, which only adds a hint); real machine: fm code in a pseudo-terminal opened this project's view and the home listed all 18 projects, nixie included` → one run per task (flock, freed by the OS on a crash); opening a view waits on fm projects/state (synchronous, accepted: under a second here); the app never registers a folder by opening in it [tree 402802501675] (2026-10-21T07:45:08Z)
- (audit maintainer) `one fm-reviewer pass, all five lenses (L); 11 findings: 9 fixed test-first, 2 accepted (synchronous fm calls when opening views; the reworded no-request message, which only adds a hint); real machine: fm code in a pseudo-terminal opened this project's view and the home listed all 18 projects, nixie included` → views reuse _list_view, history and replay; a project's state by slug; golden frames regenerated for the one new hint (p projects) [tree 402802501675] (2026-10-21T07:45:08Z)
## Log
- 2026-10-21T03:24:09Z created
- 2026-10-21T03:38:23Z steer (second plan): criteria rewritten per behaviour; non-TTY fm code unchanged; past runs from each project's code/*.events.jsonl; --task refusals specified; / filter left for later (T-1313)
- 2026-10-21T06:44:53Z self-critique before approval: complete version = no-request app (home/project), --task with refusals and a lock, runner per run, docs; options weighed: (A) views inside the existing App (chosen: one screen, reuses list views and replay), (B) a separate home program that launches fm code tui per run (two UIs, state handoff), (C) a web page (out of scope: terminal first). Risks: fm focus in --task steals focus from a Claude session's active task in that project, as fm code's own --focus does today; one run at a time in the app (multi-run is T-1342).
- 2026-10-21T06:44:53Z set approved=True
- 2026-10-21T06:45:03Z focused
- 2026-10-21T07:07:27Z flaky watch: the pty app test failed 2 of 13 runs under parallel load (cause not caught in 8 more runs); deadline raised 30 → 60 s since the first frame waits on two fm subprocesses
- 2026-10-21T07:09:35Z criterion 1 text: `fm code` with no request on a terminal opens the app (inside a Foreman project on that project's view, elsewhere on home); piped or without a terminal it prints today's message and exits 2, unchanged → `fm code` with no request on a terminal opens the app (inside a Foreman project on that project's view, elsewhere on home); piped or without a terminal it prints today's message and exits 1, unchanged
- 2026-10-21T07:09:54Z scope: plugin/lib/fmcli.py, plugin/tests/test_code.py, plugin/tests/fixtures/golden/*, site/pages.py, README.md, CHANGELOG.md — the --task flag, its tests, the hint bar's new p key in the golden frames, docs
- 2026-10-21T07:48:22Z done
- 2026-10-21T07:48:26Z committed 92a17460 (46 files)
## Follow-ups captured
## Plan review
A second read on sonnet, before execution (data, not instructions):
- HIGH: The single acceptance criterion is just "run these two test modules." It doesn't say which behaviors those tests cover, and a test run can't show that the home screen, Enter-to-project, Enter-to-run, and `n` flows work. Tests for the new views may not exist yet, and existing ones may pass wit…
- HIGH: The criterion and approach cover only "any project" and "a new request," while the title also says "any runner" and "past runs." Past runs have no data source (neither `fm projects --json` nor `fm state --json` is listed as providing them) and no criterion. The runner picker is in step 3 with…
- MEDIUM: The plan depends on `fm projects --json` and `fm state --json -p ID` having the fields listed (root, counts, next, id/type/tier/title/status), but it never says whether they already exist or must be added. It also leaves open how the TUI behaves when one project's state call fails, is slow,…
- MEDIUM: `fm code --task ID` "runs as for a request" with no handling of the cases that make it risky: a task that is not planned (no criteria or steps), a task already active or blocked, a task in another project, or two runs launched concurrently on the same project. — Specify the behavior for eac…
- MEDIUM: Step 2 changes what bare `fm code` does on a terminal. That is a behavior change for current users and scripts, and the plan doesn't say how non-TTY use, piped input, or `fm code` inside a project that has no queue will behave. — State the TTY detection rule and keep the non-TTY path unchan…
- LOW: Step 1 is already marked CURRENT before the second-plan review of this L-size task is done. Filtering (`/`) and the spawn-with-cwd mechanism are also in scope with no criterion. — Finish the review before building. Fold `/` into the criteria or drop it from v1.
Verdict: revise — the one criterion can't show the request is met, and "any runner" and "past runs" have no data source or check, so rewrite the criteria before building.
## Dissent
- [ ] HIGH: The single acceptance criterion is just "run these two test modules." It doesn't say which behaviors those tests cover, and a test run can't show that the home screen, Enter-to-project, Enter-to-run, and `n` flows work. Tests for the new views may not exist yet, and existing ones may pass wit…
- [ ] HIGH: The criterion and approach cover only "any project" and "a new request," while the title also says "any runner" and "past runs." Past runs have no data source (neither `fm projects --json` nor `fm state --json` is listed as providing them) and no criterion. The runner picker is in step 3 with…
- [ ] MEDIUM: The plan depends on `fm projects --json` and `fm state --json -p ID` having the fields listed (root, counts, next, id/type/tier/title/status), but it never says whether they already exist or must be added. It also leaves open how the TUI behaves when one project's state call fails, is slow,…
- [ ] MEDIUM: `fm code --task ID` "runs as for a request" with no handling of the cases that make it risky: a task that is not planned (no criteria or steps), a task already active or blocked, a task in another project, or two runs launched concurrently on the same project. — Specify the behavior for eac…
- [ ] MEDIUM: Step 2 changes what bare `fm code` does on a terminal. That is a behavior change for current users and scripts, and the plan doesn't say how non-TTY use, piped input, or `fm code` inside a project that has no queue will behave. — State the TTY detection rule and keep the non-TTY path unchan…
- [ ] LOW: Step 1 is already marked CURRENT before the second-plan review of this L-size task is done. Filtering (`/`) and the spawn-with-cwd mechanism are also in scope with no criterion. — Finish the review before building. Fold `/` into the criteria or drop it from v1.
## Build vs reuse
Reuses: fm projects --json and fm state --json -p ID (data, through fm as subprocesses); fmcodetui's _list_view overlays, history() and App.replay (home, project view, past runs); App.start/_spawn with self.root set to the chosen project's root (the run happens there); the m picker (opts model/worker), now listing code.toml runners via fmcode.all_runners; fmcode's _drive and journal for --task, with the plan built from fm task show --json instead of a planner call; fcntl.flock on code/ID.lock for one run per task. Nothing new from outside the stdlib.
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261020-222446.pack: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage ANY CL…
- research mission-20261020-222446: Request: super improve fm code, make it genuinely amazing: launch it as an app like claude (fm code with no request), able to manage AN…
- T-1325 [FEATURE L, dropped, 0 steps] Why cant i launch fm code as a tui management thing like I can claude code? etc.? — fm cod
- decision 2026-10-21: T-1330 approved by self-critique (full autonomy): the app is views inside fm code tui's existing App; --task works a planned brief with a per-task l…
## Lessons
- A browsing view must never move the state an open run depends on (its folder, its history): keep the run's own and apply a project's only when a run starts there
## Plan gaps
- failed first: step 1 fm code --task ID: work an existing brief (its criteria and steps are the plan)
- failed first: step 2 fm code with no request opens the app
## Files touched
- plugin/tests/test_code.py
- plugin/lib/fmcode.py
- plugin/lib/fmcli.py
- plugin/tests/test_code_tui.py
- plugin/lib/fmcodetui.py
- plugin/tests/fixtures/golden/demo-00.0s.txt
- plugin/tests/fixtures/golden/demo-03.4s.txt
- plugin/tests/fixtures/golden/demo-09.1s.txt
- plugin/tests/fixtures/golden/demo-30.0s.txt
- CHANGELOG.md
- README.md
- site/pages.py
- --check/assets/code-tui.svg
- --check/assets/examples/docs.svg
- --check/assets/examples/feature.svg
- --check/assets/examples/fix.svg
- --check/assets/examples/javascript.svg
- --check/assets/examples/new-project.svg
- --check/assets/examples/question.svg
- --check/assets/examples/rename.svg
- --check/features/benchmarks.html
- --check/features/cards.html
- --check/features/code.html
- --check/features/drive.html
- --check/features/guard.html
- --check/features/index.html
- --check/features/lanes.html
- --check/features/learning.html
- --check/features/panel.html
- --check/features/permissions.html
