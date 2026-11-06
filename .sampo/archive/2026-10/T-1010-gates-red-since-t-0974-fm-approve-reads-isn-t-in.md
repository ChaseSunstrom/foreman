---
id: T-1010
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-16T01:18:18Z
updated: 2026-10-16T01:20:12Z
base: 75d559b8c152621da758e33659335e77ab1aa6fa
base_tree: 0e45846bd83548ef377d0c5e9aec91c18e96489a
verified: strong
---
# Gates red since T-0974: fm approve-reads isn't in fm help's tiers (test_help, test_diff_ga
## Raw request
> Gates red since T-0974: fm approve-reads isn't in fm help's tiers (test_help, test_diff_gates) and the doctor self-docs fixture expects the old command list
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the three failing tests pass — verify with `python3 plugin/tests/run.py test_help test_diff_gates test_doctor`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red: test_help, test_diff_gates, test_doctor fail on approve-reads
2. [x] approve-reads in the Project and settings tier; doctor fixture's expected list
## Resume here
## Docs impact
none: test fixture and help tier only
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_help test_diff_gates test_doctor` → ✗ exit 1 · Ran 47 tests in 22.8s (21 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, DiffGates 8s) / FAILED (3 classes) [ran] [tree 0e45846bd835] (2026-10-16T01:18:48Z)
- (step 2) `python3 plugin/tests/run.py test_help test_diff_gates test_doctor` → exit 0 · Ran 58 tests in 22.7s (21 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, DiffGates 8s) / OK [ran] [tree 404fc1bdbfac] (2026-10-16T01:19:16Z)
- (ac 1) `python3 plugin/tests/run.py test_help test_diff_gates test_doctor` → exit 0 · Ran 58 tests in 22.9s (21 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, DiffGates 8s) / OK [ran] [tree 404fc1bdbfac] (2026-10-16T01:19:47Z)
- (audit edge) `self` → approve-reads placed once, in Project and settings beside trust/standing (test_help holds every command once); doctor fixture list follows argparse order [tree 404fc1bdbfac] (2026-10-16T01:19:48Z)
- (ac 1) `python3 plugin/tests/run.py test_help test_diff_gates test_doctor` → exit 0 · Ran 58 tests in 22.8s (21 classes, 16 at a time; slowest: Command 23s, ViewsRepair 16s, DiffGates 8s) / OK [ran] [tree 404fc1bdbfac] (2026-10-16T01:20:11Z)
- (audit edge) `the three failures reproduced, fixed, green` → fm help --json tiers still list each command once [tree 404fc1bdbfac] (2026-10-16T01:20:11Z)
- (audit self) `the three failures reproduced, fixed, green` → no findings [tree 404fc1bdbfac] (2026-10-16T01:20:11Z)
## Log
- 2026-10-16T01:18:18Z created
- 2026-10-16T01:18:52Z focused
- 2026-10-16T01:20:11Z done
- 2026-10-16T01:20:12Z committed 13b9efe (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Python Testing Patterns (skills/playbooks/references/lang/python-testing.md)
- T-0854 [FIX M, done, 5 steps] A newcomer's first fm commands make sense: short --help, task new shows its values and an example, init/status say what… — lesson: The firs…
- T-0698 [FIX M, done, 4 steps] Friction batch 2026-10-09: IFS false block from heredoc data, an undefined-name gate, MASTER.md read hint, builder refused-command list — l…
- decision 2026-10-09: Self-approve T-0679 (FEATURE L, first versions only)
- similar past tasks were M: consider --tier M
- similar finished tasks took 4–5 steps
- start here (files T-0854 touched): plugin/tests/test_firstrun.py, plugin/lib/fmcli.py, plugin/tests/test_help.py
## Why not caught
fm check labelled the red suite 'pre-existing' by command exit, so new failing tests inside an already-red command passed T-0974's close; compare failing test names, not the exit
## Plan gaps
- failed first: step 1 red: test_help, test_diff_gates, test_doctor fail on approve-reads
## Files touched
- plugin/lib/fmcli.py
- plugin/tests/test_doctor.py
