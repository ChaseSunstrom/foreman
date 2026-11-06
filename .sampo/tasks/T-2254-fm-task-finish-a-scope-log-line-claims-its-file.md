---
id: T-2254
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T02:08:24Z
updated: 2026-10-31T03:09:51Z
base: 9b9447572abbf05968ee2cd5ba817106b4983a8e
base_tree: 33db1ec4cb1ca9d127bead18fbde0ca90faa73cd
plan0_at: 2026-10-31T02:08:25Z
plan0_scope: []
verified: strong
---
# fm task finish: a scope: log line claims its file again even while another task is open (T-1122), only Docs impact waits for others to close
## Raw request
> fm task finish: a scope: log line claims its file again even while another task is open (T-1122), only Docs impact waits for others to close
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_close_gates' scope-log test and test_execution's docs-claim tests both pass — verify with `cd plugin/tests && python3 -m unittest -q test_close_gates test_execution`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] split _claimed: scope globs and scope: log paths always, Docs impact tokens only when every other task touching the file is closed
## Resume here
## Docs impact
none: restores documented behaviour
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_close_gates test_execution` → exit 0 · Ran 34 tests in 18.905s / OK [ran] [tree e040a44294de] (2026-10-31T02:09:08Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_close_gates test_execution` → exit 0 · Ran 34 tests in 18.956s / OK [ran] [tree e040a44294de] (2026-10-31T02:09:29Z)
- (audit edge) `self: a scope: log path is claimed unconditionally again (T-1122's deliberate claim), while a Docs impact token is claimed only when every other task that touched the file is closed (T-2251's review); both test files green` → a scope log naming a file an open task also edits commits it (the task said it's its own); a docs line naming one doesn't [tree e040a44294de] (2026-10-31T02:09:29Z)
- (audit self) `self: a scope: log path is claimed unconditionally again (T-1122's deliberate claim), while a Docs impact token is claimed only when every other task that touched the file is closed (T-2251's review); both test files green` → no findings [tree e040a44294de] (2026-10-31T02:09:29Z)
## Log
- 2026-10-31T02:08:24Z created
- 2026-10-31T02:08:25Z focused
- 2026-10-31T02:09:09Z scope: plugin/lib/fmcli.py (_claimed)
- 2026-10-31T02:10:01Z done
- 2026-10-31T02:10:03Z committed 719973de (1 file)
- 2026-10-31T02:10:50Z guard authorization added: publish
- 2026-10-31T02:14:49Z publish grant used by fm ship
- 2026-10-31T03:09:51Z includes T-2253: Baseline red: `python3 plugin/tests/run.py` fails…
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2251 [FIX M, done, 3 steps] fm task finish counts the docs it names as the task's own files — lesson: A file-ownership rule that infers from edit records needs the tas…
- T-1235 [FIX S, done, 0 steps] Fm task finish --commit committed nothing for T-1234: its files were edited while T-1231 w
- T-2001 [FIX S, done, 3 steps] fm doctor passes core the active task is changing in scope, run.py names the -k that filtered a module out, docs-impact…
- decision 2026-10-30: [revisit: when plugin/lib/fmmandate.py changes @468614546a50] Mission 4: the goal ledger grows fm mandate (one standing goal per project: text, clau…
- similar finished tasks took 0–3 steps
## Regression test
existing test_close_gates.test_a_file_its_scope_log_names_is_committed_with_it: red in ship59's scratch tree (T-2251's change), green now
## Why not caught
the builder ran test_execution, not test_close_gates, where T-1122's test lives; ship59's full run caught it
## Lessons
- When narrowing a shared rule, run every test file that names the rule's ticket (T-1122), not only the new feature's
## Files touched
- plugin/lib/fmcli.py
