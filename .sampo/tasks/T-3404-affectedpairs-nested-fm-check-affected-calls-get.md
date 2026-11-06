---
id: T-3404
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/tests/test_cli.py, CHANGELOG.md, .sampo/**, .fm-scratch/**]
depends_on: []
source: user
created: 2026-11-06T08:02:09Z
updated: 2026-11-06T08:04:11Z
base: d93df53c72c95f989d2e916911c3a9ee0ed06d1c
base_tree: 4b05908da0375ae3fd158c58a64711065f54a8cf
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-06T08:02:11Z
plan0_scope: []
verified: ok
---
# AffectedPairs nested fm check --affected calls get a 300 s base hang guard: at 120 s they still timed out inside a close's own 16-way gate run (72 s each even alone)
## Raw request
> AffectedPairs nested fm check --affected calls get a 300 s base hang guard: at 120 s they still timed out inside a close's own 16-way gate run (72 s each even alone)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] test_cli.AffectedPairs passes alone and inside a close's gate run — verify with `python3 plugin/tests/run.py test_cli.AffectedPairs`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] raise the three nested check --affected timeouts to 300
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 39.9s (5 jobs, 16 at a time; slowest: AffectedPairs.test_a_skipped_red_first_module_isnt_named_to_run_py 20s, AffectedPairs.test_every_linked_test_skipped_is_said_so 17s, AffectedPairs. [ran] [tree 3706fbcd027e] [world 2f1906870a] (2026-11-06T08:03:17Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 17.8s (5 jobs, 16 at a time; slowest: AffectedPairs.test_only_the_red_first_file_itself_is_left_out 17s, AffectedPairs.test_an_affected_run_with_evidence_records_it 10s, AffectedPairs.t [ran] [tree 3706fbcd027e] [world 2f1906870a] (2026-11-06T08:03:36Z)
- (audit self) `three test-only call sites raise a hang guard from 120 s to 300 s base (still x busy_factor); no assertion changed` → no findings [tree ef233f48fea6] (2026-11-06T08:03:36Z)
- (ac 1) `python3 plugin/tests/run.py test_cli.AffectedPairs` → exit 0 · Ran 5 tests in 4.8s (5 jobs, 16 at a time; slowest: AffectedPairs.test_an_affected_run_with_evidence_records_it 3s, AffectedPairs.test_every_linked_test_skipped_is_said_so 2s, AffectedPairs.test_only_ [ran] [tree ef233f48fea6] [world 2f1906870a] (2026-11-06T08:03:44Z)
- (audit self) `self: test-only hang-guard change` → no findings [tree ef233f48fea6] (2026-11-06T08:03:44Z)
## Log
- 2026-11-06T08:02:09Z created
- 2026-11-06T08:02:10Z focused
- 2026-11-06T08:02:11Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-06T08:02:36Z set scope=['plugin/tests/test_cli.py', 'CHANGELOG.md', '.sampo/**', '.fm-scratch/**']
- 2026-11-06T08:04:09Z done
- 2026-11-06T08:04:11Z committed 4f3dc2784 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-3390 [FIX S, done, 1 steps] test_cli.AffectedPairs forks a full fm repo per test and nests fm check --affected; each… — lesson: a test that runs a nested fm check need…
- research T-1505-review: Verdict: approve with nits.** I found no HIGH issues and no failure of the acceptance criteria. I had no shell, so I read the code and ran nothin…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-31: T-2059 dropped: fm next's second finished_lanes call reads a 60 s disk cache, and 5 timed runs each way showed no difference beyond noise (median 0.…
## Regression test
none: a load-only timeout (the nested fm check --affected takes ~70 s idle and ran past 120 s x busy_factor inside a close's own 16-way gate run on 2026-11-06, T-3380); the evidence is the class passing in this close's own loaded run
## Lessons
- size a nested-run test's hang guard from its idle time under the gate's own parallel load, not from a quiet run
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
