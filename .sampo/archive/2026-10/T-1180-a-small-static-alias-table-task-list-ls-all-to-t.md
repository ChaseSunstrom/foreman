---
id: T-1180
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T12:47:44Z
base: 9639b132abc2af07fdf537adf8a271fbf0354c36
base_tree: 4eb3f91df65dfbaca8d720d87cc9d5e5839905c5
plan0_at: 2026-10-16T12:44:27Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_gate_friction.py, CHANGELOG.md]
verified: strong
---
# A small static alias table (task list/ls/all to the queue view, task get/view/info to task
## Raw request
> FEATURE: A small static alias table (task list/ls/all to the queue view, task get/view/info to task show, and similar common guesses) runs the real command and prints one quiet "(ran `fm ...`)" line; unknown guesses still get the nearest-match error.
> DONE-WHEN: a new test in plugin/tests/test_cli.py runs `fm task ls` and `fm task list` and sees exit 0 with the "(ran" note, and `fm task nonsense` still exits non-zero with its error.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm task list / ls / tasks / list / ls run the queue view, fm task get|view|info ID run task show, fm inbox list and fm lane ls run their list views, each with one '(ran fm …)' note; fm task nonsense still errors — verify with `python3 plugin/tests/run.py test_gate_friction`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_gate_friction (Typos)
2. [x] Alias table applied in main before parsing
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_gate_friction` → ✗ exit 1 · Ran 8 tests in 10.5s (2 classes, 16 at a time; slowest: Flakes 9s, Typos 7s) / FAILED (1 classes) [ran] [tree 3804ac5d7df4] (2026-10-16T12:44:58Z)
- (step 2) `python3 plugin/tests/run.py test_gate_friction test_help` → exit 0 · Ran 13 tests in 3.2s (4 classes, 16 at a time; slowest: Typos 3s, Flakes 3s, Help 2s) / OK [ran] [tree 6e5df843accd] (2026-10-16T12:45:13Z)
- (ac 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 8 tests in 3.8s (2 classes, 16 at a time; slowest: Typos 4s, Flakes 3s) / OK [ran] [tree 2030243a4e17] (2026-10-16T12:45:28Z)
- (step 1) `python3 plugin/tests/run.py test_gate_friction` → exit 0 · Ran 8 tests in 3.8s (2 classes, 16 at a time; slowest: Typos 4s, Flakes 3s) / OK [ran] [tree 2030243a4e17] (2026-10-16T12:45:28Z)
- (audit adversary) `self: one table applied before parsing; each alias maps to a read-only view (queue, task show, lane list, inbox), never a mutating or user-only command, so the guard's fm-word rules see nothing new; unknown guesses still get the nearest-match error` → aliases can't reach a write or a user-only verb [tree 2030243a4e17] (2026-10-16T12:45:28Z)
- (audit edge) `self: one table applied before parsing; each alias maps to a read-only view (queue, task show, lane list, inbox), never a mutating or user-only command, so the guard's fm-word rules see nothing new; unknown guesses still get the nearest-match error` → fm -p PROJECT task list works; a real subcommand named like an alias would win only if added to the table first [tree 2030243a4e17] (2026-10-16T12:45:28Z)
- (audit self) `self: one table applied before parsing; each alias maps to a read-only view (queue, task show, lane list, inbox), never a mutating or user-only command, so the guard's fm-word rules see nothing new; unknown guesses still get the nearest-match error` → no findings [tree 2030243a4e17] (2026-10-16T12:45:28Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T12:44:22Z set tier=S, scope=['plugin/lib/fmcli.py', 'plugin/tests/test_gate_friction.py', 'CHANGELOG.md']
- 2026-10-16T12:44:24Z focused
- 2026-10-16T12:44:46Z criterion 1 verify: `python3 plugin/tests/run.py -k test_common_guesses_run_the_real_command` → `python3 plugin/tests/run.py test_gate_friction`
- 2026-10-16T12:47:43Z done
- 2026-10-16T12:47:44Z committed db1389ae (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-20261016-round4: 195 ideas, 46 clusters, each grounded against plugin/lib, hooks, skills, workflows, mods/foreman-ui and CHANGELOG.md. Paths are rela…
- research T-0274-review-1: Verdict: approve with nits.** `note_flakes` can't change the exit code or hide a failure. The findings are a regex false-name problem, one miss…
- T-1170 [FIX S, done, 2 steps] An unknown fm command prints argparse's full list of 170 choices (and a poor 'did you mean
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Plan gaps
- failed first: step 1 Failing test in test_gate_friction (Typos)
## Files touched
- plugin/tests/test_gate_friction.py
- plugin/lib/fmcli.py
- CHANGELOG.md
