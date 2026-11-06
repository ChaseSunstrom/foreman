---
id: T-0855
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: self
created: 2026-10-15T13:45:22Z
updated: 2026-10-15T13:58:44Z
batch: [T-0844, T-0850, T-0851, T-0852, T-0853]
base: c596d3e0094e2de932fe332f4ca80e357e543948
base_tree: cd60c2e11f502e6c3e0b227c3972cd26fcc4da23
verified: strong
---
# A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,…
## Raw request
> T-0844: A fresh install passes its own fm doctor (no backups yet is a warning, not a failure), and fm doctor shows only warnings and failures unless -v
> T-0850: fm check with no gates detects the project's test runner (unittest, pytest, npm test, cargo test, go test) and offers the fm check add line
> T-0851: uninstall leaves no empty settings/rules dirs or stray folders behind and reports 'restored to unset', not 'None'
> T-0852: fm digest counts tasks folded into another (done-in) as folded, not ungraded
> T-0853: fm works in a plain shell after install: install.sh adds a ~/.local/bin/fm shim (uninstall removes it), and the install output says so
## Interpretation
Five newcomer defects verified in a clean-HOME install (2026-10-15): a fresh install fails its own doctor (no backups) and prints 40 lines of passes; fm check with no gates doesn't find the test runner; fm digest shows tasks folded into others as 'ungraded' (159 of 370 last week); uninstall leaves empty dirs and prints 'defaultMode = None'; fm isn't on PATH in a plain shell.
## Assumptions (confidence)
## Acceptance criteria
- [x] T-0844: A fresh install passes its own fm doctor (no backups yet is a warning, not a failure), and works — verify with `python3 plugin/tests/run.py test_doctor`
- [x] T-0850: Fm check with no gates detects the project's test runner (unittest, pytest, npm test, carg works — verify with `python3 plugin/tests/run.py test_firstrun_shell`
- [x] T-0851: Uninstall leaves no empty settings/rules dirs or stray folders behind and reports 'restore works — verify with `python3 plugin/tests/run.py test_setup`
- [x] T-0852: Fm digest counts tasks folded into another (done-in) as folded, not ungraded works — verify with `python3 plugin/tests/run.py test_firstrun_shell`
- [x] T-0853: Fm works in a plain shell after install: install.sh adds a ~/.local/bin/fm shim (uninstall works — verify with `python3 plugin/tests/run.py test_setup`
## Non-goals
## Approach (options → choice → why)
Options: (a) small local fixes: doctor's missing backup becomes WARN and plain output lists only non-PASS rows (-v shows all); fm check with no gates detects the runner from files present and prints the fm check add line; digest counts done_in tasks as 'folded'; uninstall removes empty dirs it leaves and prints 'unset'; install.sh links ~/.local/bin/fm to the plugin's bin/fm (uninstall removes the link only if it's ours); (b) a setup wizard; (c) docs. Chose (a): each is the smallest fix of a verified newcomer defect.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-0844: A fresh install passes its own fm doctor (no backups yet is a warning, not a failure), and
2. [x] T-0850: Fm check with no gates detects the project's test runner (unittest, pytest, npm test, carg
3. [x] T-0851: Uninstall leaves no empty settings/rules dirs or stray folders behind and reports 'restore
4. [x] T-0852: Fm digest counts tasks folded into another (done-in) as folded, not ungraded
5. [x] T-0853: Fm works in a plain shell after install: install.sh adds a ~/.local/bin/fm shim (uninstall
## Resume here
## Docs impact
README: install now names the ~/.local/bin/fm link
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 32 tests in 20.2s (11 classes, 16 at a time; slowest: Command 20s, ViewsRepair 14s, RestoreState 0s) / OK [ran] [tree c13650e5dac1] (2026-10-15T13:47:27Z)
- (step 2) `python3 plugin/tests/run.py test_firstrun_shell test_map` → exit 0 · Ran 10 tests in 1.2s (5 classes, 16 at a time; slowest: Map 1s, Digest 1s, Cold 0s) / OK [ran] [tree 46136632466d] (2026-10-15T13:49:31Z)
- (step 4) `python3 plugin/tests/run.py test_firstrun_shell test_outcomes` → exit 0 · Ran 11 tests in 1.3s (9 classes, 16 at a time; slowest: Reopen 1s, Outcomes 1s, TrackRecord 1s) / OK [ran] [tree 46136632466d] (2026-10-15T13:49:33Z)
- (step 3) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 30 tests in 1.6s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 2a9c07bc4059] (2026-10-15T13:50:42Z)
- (step 5) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 31 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree ab4540c90ee9] (2026-10-15T13:51:19Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 1330 tests in 74.9s (443 classes, 16 at a time; slowest: Stop 46s, Command 27s, TaskLifecycle 27s) / FAILED (2 classes) [ran] [tree 2abcf0cbf686] (2026-10-15T13:54:26Z)
- (step 2) `python3 plugin/tests/run.py test_firstrun_shell test_map test_round_g test_ecosystem` → exit 0 · Ran 33 tests in 2.9s (11 classes, 16 at a time; slowest: HarnessCanary 3s, RoundG 2s, Sweep 1s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:56:00Z)
- `python3 plugin/tests/run.py test_firstrun_shell test_doctor test_setup` → ✗ exit 1 · Ran 66 tests in 14.0s (19 classes, 16 at a time; slowest: ViewsRepair 14s, Command 13s, Install 2s) / FAILED (5 classes) (start tree + this task's tests) [ran] [tree 5952bf91e407] (2026-10-15T13:56:34Z)
- `python3 plugin/tests/run.py test_firstrun_shell test_doctor test_setup` → exit 0 · Ran 66 tests in 19.9s (19 classes, 16 at a time; slowest: Command 20s, ViewsRepair 14s, Install 2s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:56:34Z)
- (step 5) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmdoctor.py, plugin/lib/fmmap.py, plugin/lib/fmoutcomes.py, plugin/lib/fms; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed (slower: 5.9 s vs a usual 3.9 s); python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.8    34.8     150  [0] / SessionEnd                  30.4    32.6     150  [0]; claude plugin test mods/foreman-ui → [ran] [tree 5952bf91e407] (2026-10-15T13:58:11Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor` → exit 0 · Ran 32 tests in 19.8s (11 classes, 16 at a time; slowest: Command 20s, ViewsRepair 13s, RestoreState 0s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (ac 2) `python3 plugin/tests/run.py test_firstrun_shell` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: Digest 1s, FirstCheck 0s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (ac 3) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 31 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (ac 4) `python3 plugin/tests/run.py test_firstrun_shell` → exit 0 · Ran 3 tests in 0.6s (2 classes, 16 at a time; slowest: Digest 1s, FirstCheck 0s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (ac 5) `python3 plugin/tests/run.py test_setup` → exit 0 · Ran 31 tests in 1.8s (6 classes, 16 at a time; slowest: Install 2s, Uninstall 1s, InstallScript 0s) / OK [ran] [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (audit intent) `self: five newcomer defects verified in a clean-HOME install, each fixed test-first; full suite 1,330 OK; two existing tests updated for intended changes (check's new hint wording; adopt no longer offered unittest beside make test after I narrowed the fallback)` → a fresh install's doctor now warns, not fails, on no backups and prints only problems (-v for all); fm check with no gates prints a ready fm check add line (pytest when configured, unittest discover only when nothing else runs the tests); digest says 'folded into another' and the track record no longer counts folded tasks; uninstall removes an empty settings.json and rules/ and says 'unset'; install-user links ~/.local/bin/fm (never over someone else's fm) and uninstall removes only its own link [tree 5952bf91e407] (2026-10-15T13:58:43Z)
- (audit edge) `self: five newcomer defects verified in a clean-HOME install, each fixed test-first; full suite 1,330 OK; two existing tests updated for intended changes (check's new hint wording; adopt no longer offered unittest beside make test after I narrowed the fallback)` → an empty settings.json is removed even if the user made it (Claude Code treats missing as {}); the track record's counts drop by the folded tasks (more honest, numbers change); pytest detection reads at most 200 KB of pyproject/setup.cfg [tree 5952bf91e407] (2026-10-15T13:58:43Z)
## Log
- 2026-10-15T13:45:22Z created
- 2026-10-15T13:45:44Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_doctor`
- 2026-10-15T13:45:44Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_cli`
- 2026-10-15T13:45:44Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_install`
- 2026-10-15T13:45:44Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_cost`
- 2026-10-15T13:45:44Z criterion 5 verify: `` → `python3 plugin/tests/run.py test_install`
- 2026-10-15T13:45:57Z criterion 2 verify: `python3 plugin/tests/run.py test_cli` → `python3 plugin/tests/run.py test_firstrun_shell`
- 2026-10-15T13:45:57Z criterion 3 verify: `python3 plugin/tests/run.py test_install` → `python3 plugin/tests/run.py test_setup`
- 2026-10-15T13:45:58Z criterion 4 verify: `python3 plugin/tests/run.py test_cost` → `python3 plugin/tests/run.py test_firstrun_shell`
- 2026-10-15T13:45:58Z criterion 5 verify: `python3 plugin/tests/run.py test_install` → `python3 plugin/tests/run.py test_setup`
- 2026-10-15T13:45:58Z focused
- 2026-10-15T13:58:43Z done
- 2026-10-15T13:58:44Z committed 1f0e57a (11 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0672 [SECURITY L, done, 6 steps] Milestone: Features — Guard and safety — lesson: a safety claim shown to the user (restorable) must state its limits; a reviewer will …
- T-0854 [FIX M, active, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what…
- research mission-20261015-083935: Request: can you keep going? super super improve? recursively? genuinely, make it THE plugin, everything, etc.
- decision 2026-09-26: T-0014 permission mode: fm serve passes --permission-mode only when given; otherwise Remote Control uses the user's own defaultMode (bypass here, se…
- similar past tasks were L: consider --tier L
## Why not caught
none: found by the first clean-HOME walkthrough; nothing exercised a newcomer's install before
## Lessons
- Walk through your own install in a clean HOME before calling it ready: five defects no test caught showed up in ten minutes
## Files touched
- plugin/tests/test_doctor.py
- plugin/lib/fmcli.py
- plugin/lib/fmdoctor.py
- plugin/tests/test_firstrun_shell.py
- plugin/lib/fmmap.py
- plugin/lib/fmcost.py
- plugin/lib/fmoutcomes.py
- plugin/tests/test_setup.py
- plugin/lib/fmsetup.py
- README.md
- plugin/tests/test_round_g.py
