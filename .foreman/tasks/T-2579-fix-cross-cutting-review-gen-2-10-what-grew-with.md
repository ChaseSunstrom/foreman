---
id: T-2579
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: genesis-review
created: 2026-11-02T08:23:26Z
updated: 2026-11-02T09:16:01Z
trigger: genesis-review
trigger_key: e2a19beeb9f6885a
base: 150192f985c8d9fb7d32b70bd6c195c4a069b93d
base_tree: 3d18f0859cd917411fe1b83e3477e7a662512109
predict_minutes: 9
predict_attempts: 1
plan0_at: 2026-11-02T08:41:03Z
plan0_scope: []
verified: strong
---
# test_ci_matrix checks the matrix's invariant (each OS's shard jobs are exactly 1..N for the N its run line divides by) instead of pinning today's three macOS shards
## Raw request
> FIX: cross-cutting review gen-2 #10 (what grew without earning it): 22 ++ / A test that pins a 3-shard macOS layout turns the next suite-size overrun into a test edit plus a workflow edit; it measures nothing about growth, only freezes today's cure. [plugin/tests/test_ci_matrix.py]
> genesis-review 2:10
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the test derives N per OS from the workflow (Ubuntu's shard list, macOS's include entries, the run line's expression) and passes for any consistent N; a workflow missing one shard job or with a run-line count that differs from the jobs fails — verify with `python3 plugin/tests/run.py test_ci_matrix`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] rewrite the test against the invariant, with in-test broken variants (a dropped job, a mismatched count) that it must reject
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_matrix` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: CiMatrix 0s) / OK [ran] [tree 3b050b21883f] [world 2f1906870a] (2026-11-02T08:41:12Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_matrix` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: CiMatrix 0s) / OK [ran] [tree 3b050b21883f] [world 2f1906870a] (2026-11-02T08:46:34Z)
- (audit intent) `self-review: problems() derives N per job kind from the run line and the shard jobs from the matrix; the test rejects a dropped macOS job and a run line dividing by 4; passes on the real workflow` → the next re-split edits only the workflow; the test checks the invariant (jobs 1..N for the run line's N), not today's 3 and 2 [tree 3b050b21883f] (2026-11-02T08:46:34Z)
- (audit edge) `self-review: problems() derives N per job kind from the run line and the shard jobs from the matrix; the test rejects a dropped macOS job and a run line dividing by 4; passes on the real workflow` → an include without experimental: true counts as a main job only through the main shard list; a missing run line is reported, not crashed on [tree 3b050b21883f] (2026-11-02T08:46:34Z)
- (audit self) `self-review: problems() derives N per job kind from the run line and the shard jobs from the matrix; the test rejects a dropped macOS job and a run line dividing by 4; passes on the real workflow` → no findings [tree 3b050b21883f] (2026-11-02T08:46:34Z)
- `fm prove --docs` → exit 0 · · unproven site/genesis/gen-1/seed.md: subcommand fm decide: text in a file; a run of a documented command proves it (--yes-run) / Does not prove: that the prose is right: only that each documented co [ran] [tree 6e93e16aabfa] [world 2f1906870a] (2026-11-02T09:16:01Z)
## Log
- 2026-11-02T08:23:26Z created
- 2026-11-02T08:27:04Z planned from capture
- 2026-11-02T08:41:02Z set approved=True
- 2026-11-02T08:41:03Z focused
- 2026-11-02T08:41:03Z predicted from its closes: 9 min, 1 attempt(s)
- 2026-11-02T08:46:49Z done
- 2026-11-02T08:46:51Z committed f6e15301 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2575 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #6 (what grew without earning it): 729…
- T-2576 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #7 (what grew without earning it): 174 ++++- / The model…
- T-2577 [FIX L, dropped, 0 steps] FIX: cross-cutting review gen-2 #8 (what grew without earning it): A 23:1 add-to-cut…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
## Regression test
none: a test-only change with no code under fix; the test proves itself against two broken workflow variants built in-test (a dropped shard job, a run line dividing by more shards than jobs) that it must reject, and passes on the real workflow
## Lessons
- A test that pins a config value freezes it; test the invariant the value serves and prove the test against broken variants built in-test
## Files touched
- plugin/tests/test_ci_matrix.py
