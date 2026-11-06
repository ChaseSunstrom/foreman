---
id: T-2652
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:20:40Z
base: 8de81627b0a16b894b2d446601ae6a1bbd8af495
base_tree: 7c3c746f5438f3f3f5011fa03cc43d9be5262482
predict_minutes: 12
predict_attempts: 1
plan0_at: 2026-11-02T20:15:31Z
plan0_scope: []
verified: strong
---
# fm drill --restore [NAME]: restore an upgrade snapshot into a temp home and prove each project's record reads back (ledger chain, fsck, readers)
## Raw request
> FEATURE: fm drill --restore: restore a snapshot into a temp home and run fm doctor on it (c19: Restore drill / host wipe rehearsal; value 3, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
1. (chosen) Rehearse a host wipe: take a real upgrade snapshot (fmrollback's tar, manifest-checked), lay its projects into a throwaway Foreman home, and prove the record reads back: each project's ledger chain verifies, fsck finds nothing broken, and the readers (fm state, fm outcomes) run without a traceback. Nothing outside the temp home is touched.
2. Run the full fm doctor in the temp home. Rejected as the verdict: doctor's host rows (hooks, timers, plugins) fail in any bare home and say nothing about the snapshot; its state rows are fsck, which this runs per project.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm drill --restore restores the newest snapshot into a temp home, passes when each project's ledger verifies, fsck is clean and the readers run, fails naming the project when one doesn't, and touches nothing outside the temp home — verify with `python3 plugin/tests/run.py test_drill`
## Non-goals
## Approach (options → choice → why)
1. fm drill --restore [NAME] in fmdrill: fmrollback._stage into a Day, copy each slug under the Day's projects, run verify-ledger, fsck and two readers per project with -p, record the result beside the snapshots. Likely outcome: one verb proves a backup restores. Fails if: a restored meta names a real repo root and a reader writes there (only read-only verbs run).
2. use what exists: fm rollback --to NAME. Fails if: it restores into the live state, the opposite of a rehearsal.
3. do less: check the newest snapshot's manifest checksums only. Fails if: a snapshot whose bytes checksum fine but whose state no longer reads (a schema change) passes.
4. a weekly automatic restore drill from fm night. Fails if: a 10 MB unpack and a 73k-line chain verify runs every week unasked; deferred until a restore failure is on record.
Choice 1 (80%): the only option that proves the record reads back, and it reuses both the drill's temp home and rollback's manifest check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: a good snapshot passes, a tampered one fails, the live state is unchanged
2. [x] fm drill --restore in fmdrill reusing fmrollback._stage and Day
3. [x] CHANGELOG and MASTER
## Resume here
## Docs impact
CHANGELOG.md and MASTER.md (fmdrill line)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_drill` → red as expected (exit 1) · Ran 13 tests in 9.8s (3 classes, 16 at a time; slowest: Drill 9s, StateErrors 2s, RestoreDrill 1s) / FAILED (1 classes: test_drill.RestoreDrill) [ran] [tree 989763e5735b] [world 2f1906870a] (2026-11-02T20:16:41Z)
- (ac 1) `python3 plugin/tests/run.py test_drill 2>&1 | grep -E "^(FAIL|ERROR):|Error:|^OK|^FAILED" | head -8` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes: test_drill.RestoreDrill) [ran] [tree 23c815e284b9] [world 2f1906870a] (2026-11-02T20:17:30Z)
- (step 2) `python3 plugin/tests/run.py test_drill test_rollback` → ✗ exit 1 · run.py: no test matches test_rollback [ran] [tree df6a155e410c] [world 2f1906870a] (2026-11-02T20:19:03Z)
- (step 3) `grep -q 'fm drill --restore' CHANGELOG.md && grep -q 'fm drill --restore' MASTER.md` → exit 0 · (no output) [ran] [tree df6a155e410c] [world 2f1906870a] (2026-11-02T20:19:04Z)
- (step 2) `python3 plugin/tests/run.py test_drill test_tidy` → exit 0 · Ran 54 tests in 15.1s (17 classes, 16 at a time; slowest: DeferredTriage 14s, StalePlans 14s, Drill 12s) / OK [ran] [tree df6a155e410c] [world 2f1906870a] (2026-11-02T20:19:30Z)
- (ac 1) `python3 plugin/tests/run.py test_drill` → exit 0 · Ran 13 tests in 9.4s (3 classes, 16 at a time; slowest: Drill 9s, StateErrors 2s, RestoreDrill 2s) / OK [ran] [tree df6a155e410c] [world 2f1906870a] (2026-11-02T20:19:42Z)
- (audit intent) `self: reads the diff end to end; only read-only verbs run in the temp home (verify-ledger, fsck, state, outcomes, each with -p), the snapshot is manifest-checked by fmrollback._stage before anything is copied, and the temp home is kept only on a failure; ran it on the real 1.2.50 snapshot: 22 of 23 projects pass in 23 s, volt fails on a real mid-file tear (captured T-2664)` → the brief asked for a restore into a temp home and fm doctor on it; doctor's host rows fail in any bare home, so its state rows (fsck) plus the ledger chain and two readers are the verdict, as the Interpretation records [tree df6a155e410c] (2026-11-02T20:19:42Z)
- (audit edge) `self: reads the diff end to end; only read-only verbs run in the temp home (verify-ledger, fsck, state, outcomes, each with -p), the snapshot is manifest-checked by fmrollback._stage before anything is copied, and the temp home is kept only on a failure; ran it on the real 1.2.50 snapshot: 22 of 23 projects pass in 23 s, volt fails on a real mid-file tear (captured T-2664)` → no snapshot is a usage error naming fm rollback --list (tested); a damaged tar or manifest mismatch is a failed row, not a traceback; a broken chain fails naming its project (tested) [tree df6a155e410c] (2026-11-02T20:19:42Z)
- (audit operator) `self: reads the diff end to end; only read-only verbs run in the temp home (verify-ledger, fsck, state, outcomes, each with -p), the snapshot is manifest-checked by fmrollback._stage before anything is copied, and the temp home is kept only on a failure; ran it on the real 1.2.50 snapshot: 22 of 23 projects pass in 23 s, volt fails on a real mid-file tear (captured T-2664)` → 23 s for 23 projects on the real snapshot; nothing scheduled, run by hand [tree df6a155e410c] (2026-11-02T20:19:42Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:15:25Z planned from capture
- 2026-11-02T20:15:30Z focused
- 2026-11-02T20:15:31Z predicted from its closes: 12 min, 1 attempt(s)
- 2026-11-02T20:16:41Z scope: plugin/lib/fmcli.py (the drill parser's --restore flag and the --faults help, 3 to 7 since T-2648)
- 2026-11-02T20:20:37Z done
- 2026-11-02T20:20:40Z committed 49f21d01 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2648 [FEATURE S, done, 3 steps] fm drill gains a fault that drops one ledger event class (every task_done line, say): each reader that leans on it must name what's mis…
- T-2657 [FEATURE S, done, 3 steps] flakes.json counts each flaky test's fails and passes; fm doctor lists the three worst by fail rate with the command that flakes them —…
- T-2653 [FEATURE S, done, 3 steps] Every nonzero fm exit prints one Next: command, not only a UsageError that carries one: a PolicyError, LockTimeout, CorruptState or Val…
- decision 2026-11-02: brainstorm-20261102 slate: all 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); the 24 clusters marked build …
## Lessons
- A restore rehearsal earns its keep on its first run: it reads every project's chain, which nothing else does across projects
## Plan gaps
- failed first: step 2 fm drill --restore in fmdrill reusing fmrollback._stage and Day
## Files touched
- plugin/tests/test_drill.py
- plugin/lib/fmdrill.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md
