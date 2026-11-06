---
id: T-1996
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmdocs.py, plugin/tests/run.py, plugin/tests/test_run.py, plugin/tests/test_docsdrift.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-29T14:39:06Z
updated: 2026-10-29T14:46:31Z
batch: [T-1994, T-1995]
base: db2eddf2810c69c09e1d917c9c402ec185975220
base_tree: 423798ddabfcccbc134c18e78272f614a97b6ad5
plan0_at: 2026-10-29T14:39:32Z
plan0_scope: [plugin/lib/fmdocs.py, plugin/tests/run.py, plugin/tests/test_run.py]
verified: strong
---
# run.py runs only tests matching a name and a -k, the docs-impact blocker names the path it meant
## Raw request
> T-1994: PERF: run.py test_cli -k pattern runs all of test_cli (names and -k are unioned), so a per-step check meant to run one test runs the whole module; with both given, names pick the modules and -k filters within them, as pytest does
> @plugin/tests/run.py @plugin/tests/test_run.py
> DONE-WHEN: run.py with a name and a -k runs only the tests matching both :: python3 plugin/tests/run.py -k test_run
> T-1995: FEATURE: fm task done's docs-impact blocker for a missing doc names the tracked file it most likely meant (rules/foreman.md → plugin/rules/foreman.md)
> @plugin/lib/fmdocs.py
> DONE-WHEN: the blocker suggests the one tracked path ending with the named one :: python3 plugin/tests/run.py -k test_docs
## Interpretation
Do T-1994, T-1995 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1996. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1994: run.py with a name and a -k runs only the tests matching both — verify with `python3 plugin/tests/run.py -k test_run`
- [x] T-1995: the blocker suggests the one tracked path ending with the named one — verify with `python3 plugin/tests/run.py -k test_docs`
## Non-goals
## Approach (options → choice → why)
T-1994: (a) names and -k both given → a test must match a name AND a -k (pytest's file -k pattern); run_one passes only the -k (the class already sits in a named module); (b) keep the union, warn on stderr; (c) document it only. Choice (a): what every reader of 'run.py test_x -k y' expects; fm check affected passes {names} alone, unchanged. T-1995: (a) git ls-files, the one tracked .md ending with /<named> goes in the blocker as '(path?)'; (b) os.walk search; (c) none. Choice (a): tracked files only, one call, no guess when 0 or 2+ match.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1994: run.py test_cli -k pattern runs all of test_cli (names and -k are unioned), so a…
2. [x] T-1995: fm task done's docs-impact blocker for a missing doc names the tracked file it most…
## Resume here
<!-- auto -->
- 2026-10-29T14:40:44Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmdocs.py, plugin/tests/run.py, plugin/tests/test_docsdrift.py, plugin/tests/test_run.py
- touched since last checkpoint: plugin/tests/test_run.py, plugin/tests/test_docsdrift.py, plugin/tests/run.py, plugin/lib/fmdocs.py, CHANGELOG.md, MASTER.md
## Docs impact
CHANGELOG.md Unreleased: one T-1996 entry. MASTER.md line 317 (dev loop): test_x -k NAME narrows within a module.
## Verification evidence
- `python3 plugin/tests/run.py -k test_a_name_and_a_k_select -k test_names_are_k -k test_a_missing_named_doc` → ✗ exit 1 · Ran 3 tests in 1.3s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, Args 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 84bc0351b427] (2026-10-29T14:39:44Z)
- `python3 plugin/tests/run.py -k test_a_name_and_a_k_select -k test_names_are_k -k test_a_missing_named_doc` → ✗ exit 1 · Ran 3 tests in 0.5s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, Args 0s) / FAILED (2 classes) [ran] [tree 84bc0351b427] (2026-10-29T14:39:44Z)
- `python3 plugin/tests/run.py -k test_a_name_and_a_k_select -k test_names_are_k -k test_a_missing_named_doc` → ✗ exit 1 · Ran 3 tests in 1.2s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, Args 0s) / FAILED (2 classes) (start tree + this task's tests) [ran] [tree 9d23400d2d84] (2026-10-29T14:40:12Z)
- `python3 plugin/tests/run.py -k test_a_name_and_a_k_select -k test_names_are_k -k test_a_missing_named_doc` → exit 0 · Ran 3 tests in 0.4s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, Args 0s) / OK [ran] [tree 9d23400d2d84] (2026-10-29T14:40:12Z)
- (step 1) `python3 plugin/tests/run.py test_run` → exit 0 · Ran 56 tests in 4.6s (32 classes, 16 at a time; slowest: Hang 4s, Ambient 4s, Ship 4s) / OK [ran] [tree d9d71bc8f243] (2026-10-29T14:40:42Z)
- (step 2) `python3 plugin/tests/run.py test_docsdrift` → exit 0 · Ran 14 tests in 0.7s (2 classes, 16 at a time; slowest: TaskDocsDrift 0s, DocsDrift 0s) / OK [ran] [tree d9d71bc8f243] (2026-10-29T14:40:43Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmdocs.py — commit it through a task, or git checkout it back / fm doctor: OK (48 pass, 6 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.1    43.9     150  [0] / SessionEnd                  34.5    36.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-u [ran] [tree d9d71bc8f243] (2026-10-29T14:45:53Z)
- (ac 1) `python3 plugin/tests/run.py -k test_run` → exit 0 · Ran 56 tests in 4.6s (32 classes, 16 at a time; slowest: Hang 4s, Ambient 4s, Ship 4s) / OK [ran] [tree d9d71bc8f243] (2026-10-29T14:46:17Z)
- (ac 2) `python3 plugin/tests/run.py -k test_docs` → exit 0 · Ran 75 tests in 9.2s (18 classes, 16 at a time; slowest: Fences 9s, TaskLifecycle 1s, Site 1s) / OK [ran] [tree d9d71bc8f243] (2026-10-29T14:46:17Z)
- (audit intent) `self: read the diff; run.py classes() ANDs names with -k and main passes -k alone to each class (the class already sits in a named module); fm check affected and CI pass names or --shard only, so their selection is unchanged; task_docs looks up tracked .md only when a named doc is missing and suggests a path only when exactly one ends with it` → run.py test_run -k shards runs only Args (proved red→green); a misnamed docs path now says (plugin/rules/foreman.md?) [tree d9d71bc8f243] (2026-10-29T14:46:17Z)
- (audit edge) `self: read the diff; run.py classes() ANDs names with -k and main passes -k alone to each class (the class already sits in a named module); fm check affected and CI pass names or --shard only, so their selection is unchanged; task_docs looks up tracked .md only when a named doc is missing and suggests a path only when exactly one ends with it` → a name finer than a class (test_run.Args.test_x) plus -k runs every -k match in that class; a name with no -k match now fails as 'no test matches', which is right since nothing ran; git missing → no hint, same blocker as before [tree d9d71bc8f243] (2026-10-29T14:46:17Z)
- (audit self) `self: read the diff; run.py classes() ANDs names with -k and main passes -k alone to each class (the class already sits in a named module); fm check affected and CI pass names or --shard only, so their selection is unchanged; task_docs looks up tracked .md only when a named doc is missing and suggests a path only when exactly one ends with it` → no findings [tree d9d71bc8f243] (2026-10-29T14:46:17Z)
## Log
- 2026-10-29T14:39:06Z created
- 2026-10-29T14:39:32Z focused
- 2026-10-29T14:39:49Z set scope=['plugin/lib/fmdocs.py', 'plugin/tests/run.py', 'plugin/tests/test_run.py', 'plugin/tests/test_docsdrift.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-29T14:39:49Z scope widened: the docs test, CHANGELOG and MASTER
- 2026-10-29T14:46:29Z done
- 2026-10-29T14:46:31Z committed b49ccf6d (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1736 [CLEAN M, done, 4 steps] Small cleanups: one WCAG contrast function, unique help-tier positions, doctor's variation selectors, a MASTER.md modul… — lesson: A doc …
- decision 2026-10-22: T-1585: the guard refuses commands that name CLAUDECODE or CLAUDE_CODE_ENTRYPOINT to unset or override them, not a whole fresh environment (env -i, …
- likely tests for the scope: plugin/tests/test_docs.py
## Files touched
- plugin/tests/test_run.py
- plugin/tests/test_docsdrift.py
- plugin/tests/run.py
- plugin/lib/fmdocs.py
- CHANGELOG.md
- MASTER.md
