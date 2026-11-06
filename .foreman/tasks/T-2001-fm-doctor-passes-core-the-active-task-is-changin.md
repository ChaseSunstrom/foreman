---
id: T-2001
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdocs.py, plugin/lib/fmdoctor.py, plugin/tests/run.py, plugin/tests/test_docsdrift.py, plugin/tests/test_doctor.py, plugin/tests/test_run.py]
depends_on: []
source: user
created: 2026-10-29T14:47:48Z
updated: 2026-10-29T15:19:30Z
batch: [T-1998, T-1999, T-2000]
base: b49ccf6d2b3e575ed7781fdb9bad4e1faff59d5d
base_tree: d9d71bc8f2431d88165d838224a052120a2e8c18
plan0_at: 2026-10-29T15:12:28Z
plan0_scope: [plugin/lib/fmdocs.py, plugin/lib/fmdoctor.py, plugin/tests/run.py, plugin/tests/test_docsdrift.py, plugin/tests/test_doctor.py, plugin/tests/test_run.py]
verified: strong
---
# fm doctor passes core the active task is changing in scope, run.py names the -k that filtered a module out, docs-impact…
## Raw request
> T-1998: FIX: fm doctor's core-integrity check warns "commit it through a task, or git checkout it back" about protected core the focused task is changing inside its own scope (every fm check of a core task shows it); files in the active task's scope pass with a note naming that task, files outside it still warn
> @plugin/lib/fmdoctor.py @plugin/tests/test_doctor.py
> DONE-WHEN: core changed only inside the active task's scope passes and names the task; a file outside it still warns :: python3 plugin/tests/run.py test_doctor -k core_integrity
> T-1999: FIX: run.py with a name and a -k that matches none of its tests says only "no test matches test_run", as if the module were missing; it now names the -k too, and the usage line lists NAME
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: the message names the -k patterns that filtered the module out :: python3 plugin/tests/run.py test_run -k UnknownNames
> T-2000: FEATURE: the docs-impact blocker for a missing doc suggests up to three tracked paths when several end with the name (one exact match already suggested, T-1995)
> @plugin/lib/fmdocs.py @plugin/tests/test_docsdrift.py
> DONE-WHEN: two tracked docs ending with the name are both suggested :: python3 plugin/tests/run.py test_docsdrift -k suggests
## Interpretation
Do T-1998, T-1999, T-2000 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-2001. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1998: core changed only inside the active task's scope passes and names the task; a file outside it still warns — verify with `python3 plugin/tests/run.py test_doctor -k CoreIntegrity`
- [x] T-1999: the message names the -k patterns that filtered the module out — verify with `python3 plugin/tests/run.py test_run -k UnknownNames`
- [x] T-2000: two tracked docs ending with the name are both suggested — verify with `python3 plugin/tests/run.py test_docsdrift -k suggests`
## Non-goals
## Approach (options → choice → why)
Doctor: (a) skip the check while any task is active, (b) pass the active brief in and split changed files by its scope, (c) read the ledger's touched files. Choice (b): only in-scope files pass, so an unrelated core edit still warns; the caller passes c.active_brief_fast of the home project, tests pass a stand-in. run.py: name the -k patterns in the missing message (one f-string). Docs: suggest up to three tracked paths when several end with the name (one join).
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1998: fm doctor's core-integrity check warns "commit it through a task, or git checkout it…
2. [x] T-1999: run.py with a name and a -k that matches none of its tests says only "no test matches…
3. [x] T-2000: The docs-impact blocker for a missing doc suggests up to three tracked paths when…
## Resume here
## Docs impact
CHANGELOG.md Unreleased: one T-2001 entry. MASTER.md: no change (doctor's checks aren't listed one by one; run.py usage line updated in its docstring).
## Verification evidence
- `python3 plugin/tests/run.py test_doctor test_docsdrift test_run -k active_task_changes_in_scope -k suggests_the_tracked -k filters_out_names` → ✗ exit 1 · Ran 3 tests in 1.4s (3 classes, 16 at a time; slowest: UnknownNames 0s, TaskDocsDrift 0s, CoreIntegrity 0s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree bba6b94ed5d4] (2026-10-29T15:12:47Z)
- `python3 plugin/tests/run.py test_doctor test_docsdrift test_run -k active_task_changes_in_scope -k suggests_the_tracked -k filters_out_names` → ✗ exit 1 · Ran 3 tests in 0.8s (3 classes, 16 at a time; slowest: UnknownNames 1s, TaskDocsDrift 0s, CoreIntegrity 0s) / FAILED (3 classes) [ran] [tree bba6b94ed5d4] (2026-10-29T15:12:47Z)
- `python3 plugin/tests/run.py test_doctor test_docsdrift test_run -k active_task_changes_in_scope -k suggests_the_tracked -k filters_out_names` → ✗ exit 1 · Ran 3 tests in 2.1s (3 classes, 16 at a time; slowest: UnknownNames 1s, TaskDocsDrift 0s, CoreIntegrity 0s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree e772ad6d1872] (2026-10-29T15:13:13Z)
- `python3 plugin/tests/run.py test_doctor test_docsdrift test_run -k active_task_changes_in_scope -k suggests_the_tracked -k filters_out_names` → exit 0 · Ran 3 tests in 1.0s (3 classes, 16 at a time; slowest: UnknownNames 1s, TaskDocsDrift 0s, CoreIntegrity 0s) / OK [ran] [tree e772ad6d1872] (2026-10-29T15:13:13Z)
- (step 1) `python3 plugin/tests/run.py test_doctor -k CoreIntegrity` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / OK [ran] [tree e772ad6d1872] (2026-10-29T15:14:10Z)
- (step 2) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 57 tests in 4.6s (32 classes, 16 at a time; slowest: Hang 4s, Ambient 4s, Ship 4s) / OK [ran] [tree e772ad6d1872] (2026-10-29T15:14:15Z)
- (step 3) `python3 plugin/tests/run.py test_docsdrift` → exit 0 · Ran 14 tests in 0.7s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree e772ad6d1872] (2026-10-29T15:14:16Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.4    42.4     150  [0] / SessionEnd                  35.5    38.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree 2e0e05de4e2f] (2026-10-29T15:18:40Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor -k core_integrity` → ✗ exit 1 · run.py: no test matches test_doctor with -k core_integrity [ran] [tree 2e0e05de4e2f] (2026-10-29T15:18:54Z)
- (ac 2) `python3 plugin/tests/run.py test_run -k UnknownNames` → exit 0 · Ran 3 tests in 1.3s (1 classes, 16 at a time; slowest: UnknownNames 1s) / OK [ran] [tree 2e0e05de4e2f] (2026-10-29T15:18:54Z)
- (ac 3) `python3 plugin/tests/run.py test_docsdrift -k suggests` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: TaskDocsDrift 0s) / OK [ran] [tree 2e0e05de4e2f] (2026-10-29T15:18:54Z)
- `python3 plugin/tests/run.py test_doctor -k CoreIntegrity` → exit 0 · Ran 3 tests in 0.4s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / OK [ran] [tree 2e0e05de4e2f] (2026-10-29T15:18:54Z)
- (ac 1) `python3 plugin/tests/run.py test_doctor -k CoreIntegrity` → exit 0 · Ran 3 tests in 0.3s (1 classes, 16 at a time; slowest: CoreIntegrity 0s) / OK [ran] [tree 2e0e05de4e2f] (2026-10-29T15:19:16Z)
- (audit intent) `self: read the diff; doctor splits changed core by the active brief's scope globs (scope_drift), passes only when every changed file is inside it and lists them, warns for the rest; a task with no scope changes nothing; run.py's missing line adds the -k patterns; task_docs adds a 'one of …' hint for 2+ matches, capped at three` → a core task's own fm check no longer warns 'git checkout it back' (doctor 48→49 pass live); misfiltered names and ambiguous doc paths say what happened [tree 2e0e05de4e2f] (2026-10-29T15:19:16Z)
- (audit adversary) `self: read the diff; doctor splits changed core by the active brief's scope globs (scope_drift), passes only when every changed file is inside it and lists them, warns for the rest; a task with no scope changes nothing; run.py's missing line adds the -k patterns; task_docs adds a 'one of …' hint for 2+ matches, capped at three` → a broad scope (plugin/**) would pass any core edit in doctor, but doctor is a report, not the guard: core edits still need the core grant, the PASS line lists the files, and the task's review covers them at finish [tree 2e0e05de4e2f] (2026-10-29T15:19:16Z)
- (audit edge) `self: read the diff; doctor splits changed core by the active brief's scope globs (scope_drift), passes only when every changed file is inside it and lists them, warns for the rest; a task with no scope changes nothing; run.py's missing line adds the -k patterns; task_docs adds a 'one of …' hint for 2+ matches, capped at three` → no active task or an unscoped one keeps the old warning; a rename's 'old -> new' porcelain path doesn't glob-match and still warns, as before [tree 2e0e05de4e2f] (2026-10-29T15:19:16Z)
- (audit self) `self: read the diff; doctor splits changed core by the active brief's scope globs (scope_drift), passes only when every changed file is inside it and lists them, warns for the rest; a task with no scope changes nothing; run.py's missing line adds the -k patterns; task_docs adds a 'one of …' hint for 2+ matches, capped at three` → no findings [tree 2e0e05de4e2f] (2026-10-29T15:19:16Z)
## Log
- 2026-10-29T14:47:48Z created
- 2026-10-29T14:47:53Z set tier=S
- 2026-10-29T15:12:28Z focused
- 2026-10-29T15:14:33Z scope: CHANGELOG.md gets the batch's Unreleased entry, as every task's does
- 2026-10-29T15:19:09Z steer: ac 1's -k core_integrity matched no test (class is CoreIntegrity); T-1994's AND rule now fails it instead of running the whole module
- 2026-10-29T15:19:28Z done
- 2026-10-29T15:19:30Z committed 0f5e8a5c (7 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1996 [FEATURE S, done, 2 steps] run.py runs only tests matching a name and a -k, the docs-impact blocker names the path it meant
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
- similar finished tasks took 2–7 steps
- likely tests for the scope: plugin/tests/test_docs.py, plugin/tests/test_doctor.py
## Why not caught
the warning was a WARN, never a failure, so gates passed and nobody read it; T-1996's gate output showed it
## Files touched
- plugin/tests/test_doctor.py
- plugin/tests/test_docsdrift.py
- plugin/tests/test_run.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmdocs.py
- plugin/tests/run.py
- CHANGELOG.md
